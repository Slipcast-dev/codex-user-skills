[Русский](SECURITY.md) | [English](SECURITY.en.md)

# Security policy

This repository contains instructions and supporting programs from third-party authors. Catalog validation checks structure and consistency; it is not a security audit of every skill.

## Supported materials

Reports are accepted for the current `main` branch and the latest published release. Fixes are released when ready; no response time is guaranteed.

## Report a vulnerability

Use [Security → Report a vulnerability](https://github.com/Slipcast-dev/codex-user-skills/security/advisories/new) when private vulnerability reporting is available for the repository.

Include the skill name, file path, version or commit, potential impact, and a safe way to reproduce the issue. Do not send live keys, passwords, or third-party data. Use artificial values in examples.

Do not open a public issue containing a live secret, personal data, or details of an unresolved vulnerability. If the private form is unavailable, you may open an issue requesting a private contact channel without technical details, or use [GitHub Support](https://support.github.com/contact) for platform-related problems.

## Using skills

Before installing a skill, read `SKILL.md` and any included scripts. Review requested permissions and external dependencies. Store secrets in environment variables or secure storage; skill instructions should not require publishing secrets in messages or code.

If a published key is compromised, revoke it with the relevant service first. Removing a line from the current file does not remove it from Git history.
