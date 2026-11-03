---
name: agent-spending-mandate
description: "Write a spending mandate that lets an AI agent buy things for you within strict limits: what it may buy, from whom, up to how much per purchase and in total, until when, and what needs your yes."
metadata:
  source-package: pm-claude-skills-main
  adapted-for: Codex
---

# agent-spending-mandate

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
