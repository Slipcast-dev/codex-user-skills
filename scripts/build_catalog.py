#!/usr/bin/env python3
"""Генерирует русскую и английскую навигацию из единого каталога.

Требуется только стандартная библиотека Python 3.11+. Категории и состав
навыков общие для двух языков. Оригиналы в skills/ не изменяются.
Переводы описаний хранят исходный текст для обнаружения устаревшего перевода.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ('ru', 'en')
TEXT = {
    'ru': {
        'catalog': 'Каталог навыков Codex',
        'summary': '{skills} пользовательских навыков в {categories} категориях.',
        'classification': 'У каждого навыка одна основная категория по назначению.',
        'category': 'Категория',
        'count': 'Навыков',
        'skill': 'Навык',
        'description': 'Описание из исходного навыка',
        'category_summary': '{skills} навыков. [Все категории](../CATALOG.md).',
        'language_note': (
            'Навигация и документация доступны на русском и английском. '
            'Инструкции и ресурсы навыков сохранены на языках оригиналов. '
            'Описания в этой версии приведены из исходных навыков; '
            'английская версия каталога содержит переводы русских описаний.'
        ),
        'json': '[Полный JSON-каталог](catalog/skills.json).',
        'layout': (
            'Папки сохранены рядом в `skills/`, чтобы сохранить исходные '
            'ссылки `../другой-навык/`. Категории служат навигацией. '
            'Назначения категорий редактируются явно в JSON; при изменении '
            'описания они не меняются автоматически.'
        ),
        'notices': 'Происхождение и лицензии',
        'scope': (
            'Независимая коллекция пользовательских навыков для OpenAI Codex. '
            'Снимок: {date}. Системные и плагинные навыки не включены.'
        ),
        'attribution': (
            'Исходные LICENSE, NOTICE, ссылки и сведения об авторах '
            'сохранены в папках навыков. Поле `source-package` перенесено '
            'из исходных метаданных и не доказывает полноту цепочки '
            'происхождения. Имена пакетов не заменяют адреса upstream; '
            'неизвестные адреса не выдумываются.'
        ),
        'license_scope': (
            'Корневой LICENSE распространяется только на новые инструменты '
            'обслуживания и оформление коллекции. Он не перелицензирует '
            '`skills/`. Оригинальные юридические тексты лицензий не переводятся.'
        ),
        'license': 'Указанная лицензия',
        'unknown': (
            '`NOASSERTION` означает отсутствие отдельного файла лицензии. '
            'Отсутствие лицензии не задаёт условия дальнейшего использования: '
            'уточняйте их у правообладателя. Не считайте такие материалы '
            'автоматически MIT или public domain. `LicenseRef-Multiple` '
            'означает несколько сохранённых файлов лицензий; изучите каждый.'
        ),
        'provenance': (
            'Ниже перечислены все навыки и известные лицензии. '
            'Источники и пути также доступны в '
            '[catalog/provenance.json](catalog/provenance.json).'
        ),
        'package': 'Исходный пакет',
        'license_heading': 'Файлы лицензий',
        'missing': 'Не указана (NOASSERTION)',
    },
    'en': {
        'catalog': 'Codex Skills Catalog',
        'summary': '{skills} user skills in {categories} categories.',
        'classification': 'Each skill has one primary category based on purpose.',
        'category': 'Category',
        'count': 'Skills',
        'skill': 'Skill',
        'description': 'Description (English)',
        'category_summary': '{skills} skills. [All categories](../CATALOG.en.md).',
        'language_note': (
            'Repository navigation and documentation are available in Russian '
            'and English. Skill instructions and resources retain their source '
            'languages. This catalog uses original English descriptions and '
            'English translations of Russian descriptions.'
        ),
        'json': '[Full JSON catalog](catalog/skills.json).',
        'layout': (
            'Skill folders remain side by side under `skills/` to preserve '
            'original `../other-skill/` references. Categories provide '
            'navigation. Category assignments are edited explicitly in JSON '
            'and do not change automatically when descriptions change.'
        ),
        'notices': 'Provenance and Third-Party Notices',
        'scope': (
            'An independent collection of user skills for OpenAI Codex. '
            'Snapshot: {date}. Bundled system and plugin skills are excluded.'
        ),
        'attribution': (
            'Original LICENSE and NOTICE files, links and attribution are '
            'preserved inside skill folders. The `source-package` field was '
            'copied from source metadata and does not establish a complete '
            'provenance chain. Package names do not replace upstream '
            'repository URLs; unknown URLs have not been invented.'
        ),
        'license_scope': (
            'The root LICENSE applies only to new catalog maintenance tools '
            'and repository presentation. It does not relicense `skills/`. '
            'Original legal license texts are not translated.'
        ),
        'license': 'Recorded license',
        'unknown': (
            '`NOASSERTION` means that a separate license file is missing. '
            'Missing license files do not specify downstream usage terms: '
            'contact the rights holder to clarify them. Do not assume '
            'MIT or public-domain status. `LicenseRef-Multiple` indicates '
            'multiple preserved license files; review each one.'
        ),
        'provenance': (
            'Every skill and its known license files are listed below. '
            'Sources and paths are also recorded in '
            '[catalog/provenance.json](catalog/provenance.json).'
        ),
        'package': 'Source package',
        'license_heading': 'License files',
        'missing': 'Not specified (NOASSERTION)',
    },
}


def read_json(relative: str) -> Any:
    """Читает UTF-8 JSON одинаково на Windows, macOS и Linux."""
    return json.loads((ROOT / relative).read_text(encoding='utf-8'))


def page_name(stem: str, language: str) -> str:
    """Сохраняет прежние русские URL и добавляет суффикс английской версии."""
    return f'{stem}{".en" if language == "en" else ""}.md'


def switcher(stem: str) -> str:
    """Создаёт взаимные ссылки между версиями одной страницы."""
    return f'[Русский]({stem}.md) | [English]({stem}.en.md)'


def escape_cell(value: str) -> str:
    """Экранирует разделители Markdown-таблицы и переводы строк."""
    return value.replace('|', '\\|').replace('\n', ' ')


def write_page(relative: str, lines: list[str]) -> None:
    """Записывает детерминированную страницу с UTF-8 и финальным переводом строки."""
    (ROOT / relative).write_text('\n'.join(lines) + '\n', encoding='utf-8')


def build_navigation(
    items: list[dict[str, Any]],
    categories: list[dict[str, Any]],
    translations: dict[str, dict[str, str]],
    language: str,
) -> None:
    """Строит списки категорий и их навыков для одного языка."""
    text = TEXT[language]
    rows: list[str] = []
    for category in categories:
        slug = category['id']
        title = category['title_en' if language == 'en' else 'title']
        group = [item for item in items if item['category'] == slug]
        relative = f'categories/{page_name(slug, language)}'
        rows.append(f'| [{title}]({relative}) | {len(group)} |')
        lines = [
            switcher(slug), '', f'# {title}', '',
            text['category_summary'].format(skills=len(group)), '',
            text['language_note'], '',
            f"| {text['skill']} | {text['description']} |",
            '| --- | --- |',
        ]
        for item in group:
            description = item['description']
            if language == 'en' and item['name'] in translations:
                description = translations[item['name']]['description']
            lines.append(
                f"| [{item['name']}](../{item['path']}/SKILL.md) | "
                f'{escape_cell(description)} |'
            )
        write_page(relative, lines)
    write_page(page_name('CATALOG', language), [
        switcher('CATALOG'), '', f"# {text['catalog']}", '',
        text['summary'].format(skills=len(items), categories=len(categories)),
        text['classification'], '', text['language_note'], '',
        f"| {text['category']} | {text['count']} |",
        '| --- | ---: |', *rows, '', text['json'], '', text['layout'],
    ])


def build_notices(
    items: list[dict[str, Any]], date: str, language: str,
) -> None:
    """Переводит пояснения к лицензиям, сохраняя исходные юридические файлы."""
    text = TEXT[language]
    counts = Counter(item['license'] for item in items)
    lines = [
        switcher('THIRD_PARTY_NOTICES'), '', f"# {text['notices']}", '',
        text['scope'].format(date=date), '', text['attribution'], '',
        text['license_scope'], '',
        f"| {text['license']} | {text['count']} |", '| --- | ---: |',
    ]
    lines.extend(
        f'| {license_id} | {count} |'
        for license_id, count in sorted(counts.items())
    )
    lines += [
        '', text['unknown'], '', text['provenance'], '',
        f"| {text['skill']} | {text['package']} | {text['license_heading']} |",
        '| --- | --- | --- |',
    ]
    for item in items:
        licenses = ', '.join(
            f'[{Path(path).name}]({path})' for path in item['license_paths']
        ) or text['missing']
        lines.append(
            f"| [{item['name']}]({item['path']}/SKILL.md) | "
            f"{escape_cell(item['source_package'])} | {licenses} |"
        )
    write_page(page_name('THIRD_PARTY_NOTICES', language), lines)


def build() -> None:
    """Обновляет обе локализации из общих данных, не меняя исходные навыки."""
    items = sorted(read_json('catalog/skills.json')['skills'],
                   key=lambda item: item['name'])
    categories = read_json('catalog/categories.json')
    translations = read_json('catalog/descriptions.en.json')
    by_name = {item['name']: item for item in items}
    # Устаревший перевод нельзя молча выдавать за текущее описание навыка.
    for name, translation in translations.items():
        if translation['source_description'] != by_name[name]['description']:
            raise ValueError(f'Устаревший английский перевод: {name}')
    counts = Counter(item['category'] for item in items)
    for category in categories:
        category['count'] = counts[category['id']]
    provenance = read_json('catalog/provenance.json')
    keys = ('name', 'source_scope', 'source_package', 'license',
            'license_path', 'license_paths')
    provenance['skills'] = [
        {key: item[key] for key in keys} for item in items
    ]
    for relative, data in (
        ('catalog/categories.json', categories),
        ('catalog/provenance.json', provenance),
    ):
        (ROOT / relative).write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )
    for language in LANGUAGES:
        build_navigation(items, categories, translations, language)
        build_notices(items, provenance['snapshot_date'], language)
    print(f'RU/EN: {len(items)} навыков, {len(categories)} категорий.')


if __name__ == '__main__':
    build()
