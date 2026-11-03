[Русский](CONTRIBUTING.md) | [English](CONTRIBUTING.en.md)

# Contributing

Thank you for helping maintain this collection of user skills for Codex. Contributions are accepted through pull requests.

## Before making a change

1. Find the existing skill in [the catalog](CATALOG.en.md) and check open [issues](https://github.com/Slipcast-dev/codex-user-skills/issues).
2. Make sure you have the right to distribute every file you add. Include the license, author attribution, and a link to the original project for borrowed material.
3. Read [the code of conduct](CODE_OF_CONDUCT.en.md). Report vulnerabilities according to [the security policy](SECURITY.en.md).

## Add a skill

- Add the complete folder at `skills/<unique-name>/`.
- Include a `SKILL.md` with YAML frontmatter containing `name` and `description`.
- The folder name must match `name`; the description must explain the skill's purpose clearly.
- Use relative paths for resources within the skill. Check links to neighboring skills and document external dependencies.
- Do not include API keys, passwords, personal data, local user paths, logs, or caches.
- Preserve original `LICENSE`, `NOTICE`, and author attribution. Do not replace a third-party license with this repository's license.

Bundled Codex system skills and contents of installed plugins are outside this collection's scope. Preserve skill instructions and resources in their source languages; bilingual repository navigation does not require translating the operational skill files.

## Catalog and categories

Each skill needs accurate fields in [catalog/skills.json](catalog/skills.json): name, description, primary category, path, provenance, and license. Choose the category by purpose; record provenance separately.

English category titles are stored in the `title_en` field of `catalog/categories.json`. English translations of Russian descriptions are stored in `catalog/descriptions.en.json`: each skill entry has `source_description` containing the exact original text and `description` containing the English translation. When the original description changes, update both fields; validation detects stale translations. Do not translate operational `SKILL.md` files merely to localize navigation.

Category pages and [CATALOG.en.md](CATALOG.en.md) must agree with the catalog. After changing catalog data, run:

```sh
python3 scripts/build_catalog.py
python3 scripts/check_catalog.py
```

The generator updates category pages, counts, and license information. Keep Russian and English navigation consistent. Do not reassign unrelated skills automatically because one description changed.

## Pull requests

Include:

- the problem and the result of the change;
- affected skills and categories;
- the source and license of new materials;
- checks performed and known limitations.

Check local links, agreement between catalog entries and files, and absence of secrets. Wait for GitHub Actions checks. Catalog structure validation does not replace a quality or security review of a skill; do not run third-party scripts merely to pass a check.

Catalog maintenance tools use Python 3.11 or newer. Individual skills define their own dependencies in their documentation.
