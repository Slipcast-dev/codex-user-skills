---
name: statistical-analyst
description: Run hypothesis tests, analyze A/B experiment results, calculate sample
  sizes, and interpret statistical significance with effect sizes. Use when you need
  to validate whether observed differences are real, size an experiment correctly
  before launch, or interpret test results with confidence.
metadata:
  source-package: claude-skills-main
  adapted-for: Codex
---

# statistical-analyst

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
