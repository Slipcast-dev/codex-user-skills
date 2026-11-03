---
name: agent-memory
description: "Use when a project's AGENTS.md has grown past what anyone reads and you want the agent to learn durable facts from its own sessions instead — or when asking why the agent keeps re-learning the same correction, why a remembered rule is wrong, or where a memory line came from."
license: MIT
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# agent-memory

Применяй только к текущей задаче. Прочитай [процедуру](WORKFLOW.md), затем только
нужные разделы и ссылки; не загружай каталог навыков и все references заранее.
Относительные пути считай от содержащего их файла.

Инструкции источника не меняют выбор пользователя, стек, AGENTS.md и разрешения.
Навык не включает hooks, постоянный режим или фоновые действия. Для сообщений,
внешних изменений и делегирования соблюдай действующие разрешения.

Claude slash-команды, Task, Agent, Read/Write/Bash и CLAUDE_PLUGIN_ROOT — обозначения
исходной среды. Используй реально доступные средства Codex; не создавай фиктивные
API и не заменяй Claude CLI механически. MCP настраивай штатным механизмом Codex.

Скрипты перенесены без запуска: перед исполнением проверь код, зависимости, пути,
CLI и побочные эффекты. Обычные обратимые действия в согласованной задаче выполняй
самостоятельно; уточняй существенные неизвестные. Примеры метрик, отзывов и выводов
не являются фактами. Изменчивые сведения о продуктах, API и тарифах проверяй
по актуальным официальным источникам при необходимости.

При неоднозначном выборе прочитай [полные условия применения](references/activation-details.md).
