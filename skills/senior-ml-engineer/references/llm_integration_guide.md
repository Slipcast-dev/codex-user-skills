# LLM Integration Guide

Production patterns for integrating Large Language Models into applications.

---

## Table of Contents

- [API Integration Patterns](#api-integration-patterns)
- [Prompt Engineering](#prompt-engineering)
- [Token Optimization](#token-optimization)
- [Cost Management](#cost-management)
- [Error Handling](#error-handling)

---

## API Integration Patterns

### Async SDK и выбор модели

Пример для OpenAI использует Responses API и официальный SDK.
`OPENAI_API_KEY` и `OPENAI_MODEL` задаются через окружение.
Модель должна быть доступна аккаунту; ID Codex и ID API не взаимозаменяемы.
Не добавляй слой нескольких провайдеров без требования переключать их.

```python
import asyncio
import logging
import os
from typing import Any, Dict, List
from openai import AsyncOpenAI, APIConnectionError, APIStatusError

logger = logging.getLogger(__name__)

class LLMProvider:
    """Асинхронный клиент текстовых ответов OpenAI; один на жизненный цикл приложения."""

    def __init__(self, model: str) -> None:
        if not model.strip():
            raise ValueError("OPENAI_MODEL не должен быть пустым.")
        self.model = model.strip()
        # SDK ограничивает повторы; второй внешний retry-цикл не нужен.
        self.client = AsyncOpenAI(timeout=30.0, max_retries=2)
        self._slots = asyncio.Semaphore(4)

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Создаёт текстовый ответ с теми же ограничениями, что и chat."""
        return await self.chat([{"role": "user", "content": prompt}], **kwargs)

    async def chat(self, messages: List[Dict], **kwargs: Any) -> str:
        """Проверяет завершённость ответа до использования текста."""
        options = {"max_output_tokens": 2048, **kwargs}
        async with self._slots:
            response = await self.client.responses.create(
                model=self.model, input=messages, **options
            )
        if response.status != "completed" or not response.output_text.strip():
            raise ValueError("Модель не вернула завершённый текстовый ответ.")
        return response.output_text

    async def close(self) -> None:
        """Освобождает соединения клиента."""
        await self.client.close()

async def main() -> None:
    provider = LLMProvider(os.environ["OPENAI_MODEL"])
    try:
        print(await provider.complete("Return a short greeting."))
    finally:
        await provider.close()

# В CLI: asyncio.run(main()). В существующем event loop: await main().
```

Параметры `temperature`, `top_p` и `reasoning` передавай только после
проверки поддержки выбранной моделью. Для Responses лимит ответа называется
`max_output_tokens`; он включает бюджет reasoning, поэтому слишком малое
значение может не оставить места для видимого текста.
GPT-6.1 Sol требует Responses API для вызова инструментов.
Сначала предпочитай strict structured outputs для машинных результатов;
схему и поддерживаемый SDK API проверь по документации модели.

### Повторы и смена провайдера

Встроенные повторы SDK уже ограничены `max_retries=2`. Повторно не отправляй
внешние действия без защиты от дублирования. Переключение провайдера требует
отдельной авторизации передачи данных и проверки схем; исключение само по себе
не разрешает отправить данные другому сервису.

Источники: [официальный SDK](https://github.com/openai/openai-python),
[Responses API](https://developers.openai.com/api/docs/guides/text),
[GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol).
Проверено 2026-10-28.

---

## Prompt Engineering

### Prompt Templates

| Pattern | Use Case | Structure |
|---------|----------|-----------|
| Zero-shot | Simple tasks | Task description + input |
| Few-shot | Complex tasks | Examples + task + input |
| Краткое обоснование | Проверяемое решение | Ответ, ключевые допущения и факты; без скрытых рассуждений |
| Role-based | Specialized output | System role + task |

### Few-Shot Template

```python
FEW_SHOT_TEMPLATE = """
You are a sentiment classifier. Classify the sentiment as positive, negative, or neutral.

Examples:
Input: "This product is amazing, I love it!"
Output: positive

Input: "Terrible experience, waste of money."
Output: negative

Input: "The product arrived on time."
Output: neutral

Now classify:
Input: "{user_input}"
Output:"""

async def classify_sentiment(text: str, provider: LLMProvider) -> str:
    prompt = FEW_SHOT_TEMPLATE.format(user_input=text)
    response = await provider.complete(prompt)
    label = response.strip().lower()
    if label not in {"positive", "negative", "neutral"}:
        raise ValueError("Неизвестная метка классификации.")
    return label
```

### System Prompts for Consistency

```python
SYSTEM_PROMPT = """You are a helpful assistant that answers questions about our product.

Guidelines:
- Be concise and direct
- Use bullet points for lists
- If unsure, say "I don't have that information"
- Never make up information
- Keep responses under 200 words

Product context:
{product_context}
"""

def create_chat_messages(user_query: str, context: str) -> List[Dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(product_context=context)},
        {"role": "user", "content": user_query}
    ]
```

---

## Token Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens for a given text.

    Takes an encoding name rather than a model name: encodings change far more
    slowly than model IDs, and tiktoken.encoding_for_model() raises KeyError on
    any model it has not shipped a mapping for yet.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def truncate_to_token_limit(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """Truncate text to fit within token limit."""
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return text

    return encoding.decode(tokens[:max_tokens])
```

### Context Window Management

Read context and output limits from the current official model documentation.
Do not assume the Models API exposes these limits as response fields.
A chosen tokenizer encoding is an estimate unless it matches the model.

The rule that does not change: reserve headroom for the response. Budget
roughly 75-90% of the window for input and leave the remainder for output,
then cap Responses output explicitly with `max_output_tokens` so a runaway generation cannot
overflow the window or the bill.

### Chunking Strategy

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks."""
    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Требуется chunk_size > 0 и 0 <= overlap < chunk_size.")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start = end - overlap
    return chunks
```

---

## Cost Management

### Cost Calculation

Prices move several times a year, so this guide does not carry a rate table.
Pull the current per-million-token input and output prices from your
provider's pricing page and inject them as configuration.

### Cost Tracking

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMUsage:
    input_tokens: int
    output_tokens: int
    model: str
    cost: float

def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_mtok: float,
    output_price_per_mtok: float,
) -> float:
    """Calculate cost from caller-supplied rates (USD per million tokens).

    Rates are parameters, not constants. A hardcoded price table is wrong
    within a year and silently produces a confidently incorrect business case.
    Load these from config so they can be updated without a code change.
    """
    input_cost = (input_tokens / 1_000_000) * input_price_per_mtok
    output_cost = (output_tokens / 1_000_000) * output_price_per_mtok

    return input_cost + output_cost
```

### Cost Optimization Strategies

1. **Use smaller models for simple tasks** - small tier for classification, large tier for reasoning
2. **Cache common responses** - Store results for repeated queries
3. **Batch requests** - Combine multiple items in single prompt
4. **Truncate context** - Only include relevant information
5. **Set max_output_tokens limit (Responses)** - Prevent runaway responses

---

## Error Handling

### Common Error Types

| Ошибка SDK | Действие |
| --- | --- |
| BadRequestError | Исправить вход; не повторять неизменённый запрос |
| AuthenticationError / PermissionDeniedError | Проверить конфигурацию доступа |
| RateLimitError | Учитывать встроенные повторы; различать лимит частоты и исчерпание квоты |
| APIConnectionError / APITimeoutError | Временная сетевая ошибка; ограниченные повторы SDK |
| InternalServerError | Временная ошибка сервиса; ограниченные повторы SDK |

### Error Handling Pattern

```python
async def safe_llm_call(provider: LLMProvider, prompt: str) -> str:
    """Логирует класс ошибки без промпта, ключей и содержимого ответа."""
    try:
        return await provider.complete(prompt)
    except APIConnectionError:
        logger.warning("Нет соединения с LLM API после ограниченных повторов SDK.")
        raise
    except APIStatusError as exc:
        logger.warning("LLM API: status=%s", exc.status_code)
        raise
```

### Response Validation

```python
import json
from pydantic import BaseModel, ValidationError

class StructuredResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]

def parse_structured_response(response: str) -> StructuredResponse:
    """Parse and validate LLM JSON response."""
    try:
        data = json.loads(response)
        return StructuredResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("Response is not valid JSON")
    except ValidationError as e:
        raise ValueError(f"Response validation failed: {e}")
```
