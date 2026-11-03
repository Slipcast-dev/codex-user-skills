#!/usr/bin/env python3
"""Создаёт страницы категорий из явных назначений в catalog/skills.json.

Использует только стандартную библиотеку Python 3.11+. Не выполняет код навыков.
Редактируйте категорию в JSON, затем запускайте этот файл из любой папки.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def escape_cell(value: str) -> str:
    """Защищает разделитель Markdown-таблицы и убирает переводы строк."""
    return value.replace('|', '\\|').replace('\n', ' ')


def build() -> None:
    """Обновляет навигацию и сведения о лицензиях без изменения исходных навыков."""
    items: list[dict[str, Any]] = json.loads((ROOT / 'catalog/skills.json').read_text(encoding='utf-8'))['skills']
    categories: list[dict[str, Any]] = json.loads((ROOT / 'catalog/categories.json').read_text(encoding='utf-8'))
    rows: list[str] = []
    for category in categories:
        slug = category['id']
        group = sorted((item for item in items if item['category'] == slug), key=lambda item: item['name'])
        category['count'] = len(group)
        rows.append(f"| [{category['title']}](categories/{slug}.md) | {len(group)} |")
        lines = [f"# {category['title']}", '', f'{len(group)} навыков. [Все категории](../CATALOG.md).', '', '| Навык | Назначение |', '| --- | --- |']
        lines.extend(f"| [{item['name']}](../{item['path']}/SKILL.md) | {escape_cell(item['description'])} |" for item in group)
        (ROOT / f'categories/{slug}.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    provenance_path = ROOT / 'catalog/provenance.json'
    provenance = json.loads(provenance_path.read_text(encoding='utf-8'))
    provenance['skills'] = [
        {key: item[key] for key in ['name', 'source_scope', 'source_package', 'license', 'license_path', 'license_paths']}
        for item in sorted(items, key=lambda item: item['name'])
    ]
    provenance_path.write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'catalog/categories.json').write_text(json.dumps(categories, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'CATALOG.md').write_text(f'# Каталог навыков Codex\n\n{len(items)} пользовательских навыков в {len(categories)} категориях. У каждого навыка одна основная категория; она описывает назначение, а не источник.\n\n| Категория | Навыков |\n| --- | ---: |\n' + '\n'.join(rows) + '\n\n[Полный JSON-каталог](catalog/skills.json). Названия и описания на страницах категорий ведут к каждому навыку.\n\nПапки сохранены рядом в `skills/`, чтобы сохранить исходные ссылки `../другой-навык/`. Категории служат навигацией по коллекции. Назначения категорий редактируются явно в JSON; автоматически при изменении описания они не меняются.\n', encoding='utf-8')
    counts = Counter(item['license'] for item in items)
    lines = ['# Происхождение и лицензии', '', 'Это независимая коллекция пользовательских навыков для OpenAI Codex. Снимок: 2026-11-03. Системные и плагинные навыки в него не включены.', '', 'Исходные LICENSE, NOTICE, ссылки и сведения об авторах сохранены в папках навыков. Поле `source-package` перенесено из исходных метаданных и не доказывает полноту цепочки происхождения. Имена пакетов не заменяют адреса upstream-репозиториев; неизвестные адреса не выдумываются.', '', 'Лицензия корневого LICENSE распространяется только на новые инструменты обслуживания и оформление этой коллекции. Она не перелицензирует содержимое `skills/`.', '', '| Указанная лицензия | Навыков |', '| --- | ---: |']
    lines.extend(f'| {license_id} | {count} |' for license_id, count in sorted(counts.items()))
    lines += ['', '`NOASSERTION` означает, что отдельный файл лицензии отсутствует. Владелец коллекции подтвердил право публичного распространения этих материалов. Это подтверждение не задаёт лицензию для дальнейшего использования: уточняйте условия у правообладателя. Не считайте такие материалы автоматически MIT или public domain.', '', 'Перечень ниже содержит все навыки и прямые ссылки на известные лицензии. Для каждого навыка также сохранены источник и путь в [catalog/provenance.json](catalog/provenance.json).', '', '| Навык | Исходный пакет | Лицензия |', '| --- | --- | --- |']
    for item in sorted(items, key=lambda item: item['name']):
        license_paths = item.get('license_paths', [])
        license_cell = ", ".join(f"[{Path(path).name}]({path})" for path in license_paths) if license_paths else 'Не указана (NOASSERTION)'
        lines.append(f"| [{item['name']}]({item['path']}/SKILL.md) | {escape_cell(item['source_package'])} | {license_cell} |")
    (ROOT / 'THIRD_PARTY_NOTICES.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f'Каталог обновлён: {len(items)} навыков, {len(categories)} категорий.')


if __name__ == '__main__':
    build()
