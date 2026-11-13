# Project instructions

## What it is
AYR (Arquitect Your Repository) is a portable repository-bootstrap skill. SKILL.md is the entry point; references/ contains conditional procedures; templates/ contains an optional output contract; docs/ records rationale and evaluation.

## Boundaries
Preserve portability across users, operating systems and providers. Never embed workstation paths, private endpoints, credentials, or mandatory proprietary services. Do not bundle third-party definitions without reviewing their license and behavior. Keep repository visibility unchanged unless the owner requests it.

## Changes and verification
Keep the entry point compact and link substantial detail. Update source analysis when evidence changes and distinguish inspection from execution. Keep AGENTS.md and CLAUDE.md semantically consistent.
Run `python -m unittest discover -s tests -v` (Python 3.11+) and `git diff --check`. Package tests check links and selected portability/token patterns, not overall safety or assistant behavior. Record representative behavioral evidence for workflow changes.
