#!/usr/bin/env python3
"""Проверяет структуру публичного каталога, не исполняя сторонние навыки."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def check() -> list[str]:
    """Возвращает найденные ошибки имён, категорий, лицензий и навигации."""
    errors: list[str] = []
    data = json.loads((ROOT / 'catalog/skills.json').read_text(encoding='utf-8'))
    items = data['skills']
    categories = json.loads((ROOT / 'catalog/categories.json').read_text(encoding='utf-8'))
    slugs = {category['id'] for category in categories}
    names = [item['name'] for item in items]
    if len(names) != len(set(names)):
        errors.append('Повторяющиеся имена навыков')
    actual = {path.parent.name for path in (ROOT / 'skills').glob('*/SKILL.md')}
    if actual != set(names):
        errors.append('Состав каталога не совпадает с папками SKILL.md')
    provenance = json.loads((ROOT / 'catalog/provenance.json').read_text(encoding='utf-8'))
    expected_provenance = [
        {key: item[key] for key in ['name', 'source_scope', 'source_package', 'license', 'license_path', 'license_paths']}
        for item in sorted(items, key=lambda item: item['name'])
    ]
    if provenance['skills'] != expected_provenance:
        errors.append('Происхождение не соответствует основному каталогу')
    counts = Counter(item['category'] for item in items)
    for item in items:
        name = item['name']
        path = ROOT / item['path']
        if item['path'] != f'skills/{name}' or not re.fullmatch(r'[a-z0-9][a-z0-9-]*', name):
            errors.append(f'Некорректный путь или имя: {name}')
            continue
        if item['category'] not in slugs or not item['description']:
            errors.append(f'Нет описания или категории: {name}')
        text = (path / 'SKILL.md').read_text(encoding='utf-8')
        if not text.startswith('---\n') or not re.search(r'^name:\s*[\'\"]?' + re.escape(name) + r'[\'\"]?\s*$', text.split('\n---', 1)[0], re.M):
            errors.append(f'Имя frontmatter не совпадает: {name}')
        actual_licenses = sorted(str(file.relative_to(ROOT)) for file in path.iterdir()
                                 if file.name.lower() in {'license', 'license.txt', 'license.md', 'copying'})
        if item['license_paths'] != actual_licenses:
            errors.append(f'Неполный список лицензий: {name}')
        for license_path in item['license_paths']:
            if not (ROOT / license_path).is_file():
                errors.append(f'Нет указанной лицензии: {name}')
    for category in categories:
        if category['count'] != counts[category['id']]:
            errors.append(f"Неверный счётчик: {category['id']}")
    # Проверяем только созданную навигацию. Исходные внешние ссылки навыков
    # могут требовать дополнительных ресурсов и не являются тестом каталога.
    docs = list((ROOT / 'categories').glob('*.md')) + list(ROOT.glob('*.md'))
    for doc in docs:
        content = doc.read_text(encoding='utf-8')
        if '{{SKILL_COUNT}}' in content or '{{CATEGORY_COUNT}}' in content:
            errors.append(f'Незаменённый шаблон: {doc.relative_to(ROOT)}')
        for target in re.findall(r'\]\(([^\s)]+)\)', content):
            if '://' in target or target.startswith('#'):
                continue
            target = unquote(target.split('#', 1)[0])
            if target and not (doc.parent / target).exists():
                errors.append(f'Нет локальной ссылки {target} в {doc.relative_to(ROOT)}')
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if '.git' in relative.parts:
            continue
        if path.is_symlink():
            errors.append(f'Неожиданная символическая ссылка: {relative}')
        if path.name in {'.DS_Store', '.env', '.env.local', '__pycache__'} or path.suffix == '.pyc':
            errors.append(f'Служебный файл в публикации: {relative}')
    return errors


def main() -> int:
    """Печатает диагностику и код возврата, пригодный для GitHub Actions."""
    try:
        errors = check()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'Ошибка чтения каталога: {error}', file=sys.stderr)
        return 1
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('OK: состав, категории, frontmatter, лицензии и локальная навигация проверены.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
