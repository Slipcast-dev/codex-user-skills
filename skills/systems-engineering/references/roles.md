# Роли и минимальный состав
| Агент | Когда нужен | Запись |
|---|---|---|
| systems-architect | Выбор модели, ABI/API, существенное проектирование, ADR/DAG | Назначенные спецификации |
| hardware-os-researcher | Непроверенные даташиты, errata, API/SDK | Справочный отчёт |
| kernel-driver | KMDF/UMDF/DriverKit/eBPF/Linux | Назначенные драйверные исходники |
| firmware-rtos | Bare-Metal, RTOS, bootloader | Код и конфигурация платы |
| ipc-daemon | Сервис/SDK, ioctl, Netlink, RPC | User-space слой |
| application-ui | GUI/CLI/веб/мобильное управление | Приложение |
| build-toolchain | Build/cross-compile/packaging/signing | Build/CI/упаковка |
| static-analysis-critic | Независимый анализ и контракты | Отчёт |
| memory-security-critic | Память, DMA, права, гонки, formal scope | Отчёт |
| sandbox-hil-verifier | Runtime/stress/fuzz в явно выделенной VM/HIL | Тестовые артефакты |
| systems-bug-fixer | Подтверждённый системный дефект | Назначенный patch/регрессия |
| supervisor (существующий) | Диагностика зависаний/повторов по запросу | Назначенный отчёт |
| code-reviewer (существующий) | Дополнительное общее ревью при необходимости | Отчёт |
| test-engineer (существующий) | Unit/contract tests, mocks | Тесты, не product code |

В исходниках ОС и SDK используйте только поддержанные язык/runtime; общие C++20 рекомендации
не означают, что C++ поддержан конкретным ядром или toolchain. Существующим общим агентам
передавайте запрет исполнения на хосте и контракт пакетов как часть задания.

Типичный DAG: architect → (research, если нужен) → executor → build →
(static, security параллельно) → runtime VM/HIL → приёмка.
Для простого mock UI не нужны kernel/firmware/VM. Для драйвера без VM gate runtime остаётся blocked.
Оркестратор — основной чат с этим skill, systems-architect — ограниченная планирующая роль.
