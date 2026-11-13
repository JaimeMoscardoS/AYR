# AYR

### Arquitect Your Repository

[![Checks](https://github.com/JaimeMoscardoS/AYR/actions/workflows/validate.yml/badge.svg)](https://github.com/JaimeMoscardoS/AYR/actions/workflows/validate.yml)
[![Version](https://img.shields.io/badge/version-0.1.0--beta-blue)](https://github.com/JaimeMoscardoS/AYR/releases/tag/v0.1.0-beta)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Turn a project idea into a repository you can understand, build and continue.**

AYR is a workflow skill for Claude Code and Codex. It starts by asking about your project, chooses useful skills and agent responsibilities, and prepares a structure that fits the work. When you ask for implementation, it continues toward a first working flow with checks.

[Install](docs/installation.md) · [Examples](#examples) · [How it works](#how-it-works) · [GSD integration](#working-with-gsd) · [Beta evidence](docs/evaluation.md)

> **Public beta:** real Windows/Linux installation checks and a complete small-project demonstration are recorded. Standalone client workflows and the live GSD handoff still have unverified paths. Read [what is tested](#what-is-tested) before relying on those integrations.

## What it helps with

- **Starting with an unclear idea:** clarify users, the first useful outcome and the constraints before choosing a stack.
- **Preparing a repository for AI-assisted work:** document boundaries, commands, verification and continuation for both assistants.
- **Choosing capabilities:** reuse installed skills, inspect missing capabilities and bring in specialists only for actual tasks.
- **Keeping work coordinated:** assign ownership, respect dependencies and retain one workflow owner and one project state.

A small CLI can stay a script and tests. A larger application can use component boundaries and an existing planning workflow. AYR does not require a monorepo, a fixed team, a RAG service or a subscription beyond whatever your chosen coding client needs.

## Get started

1. [Install AYR](docs/installation.md) using PowerShell on Windows or Bash on Linux. The guide stages the source for review before activating it and avoids overwriting an existing installation.
2. Open **the project you want to work on** in your coding client. The skill installation folder is not your project.
3. Invoke the skill with your request.

| Client | Invocation |
| --- | --- |
| Claude Code | `/ayr`, or `/AYR` after installing the included command adapter |
| Codex | `$ayr`, or “Use AYR…”; uppercase custom-command presentation depends on the client |

The portable skill ID is `ayr`. Its visible name is **AYR (Arquitect Your Repository)**. The [command adapter](commands/AYR.md) and [installation guide](docs/installation.md) explain the uppercase alias.

Prefer an archive? [Download the beta ZIP](https://github.com/JaimeMoscardoS/AYR/releases/download/v0.1.0-beta/AYR-v0.1.0-beta.zip), inspect it and follow the client directory guidance in the installation guide. It contains an `ayr/` folder, not a dependency installer.

## Examples

**Explore an idea**

> Use AYR to help me start a local reading tracker. Ask about the first useful workflow before choosing the implementation.

**Build a first working flow**

> Use AYR to create a small Python API. It needs one authenticated endpoint and tests. Preserve the existing project conventions and implement the first working flow.

**Prepare without implementing**

> Use AYR to prepare this repository for Claude Code and Codex. Document the architecture and run/test commands, select relevant skills and leave a clear next task. Do not implement application features.

**Continue a project that already uses GSD**

> Use AYR to inspect this project's capabilities. Preserve the existing GSD requirements, roadmap and checkpoints, and route the next work through that workflow.

The interview asks up to three focused questions per round, reuses answers already given and waits before decisions that depend on your response. “No preference” delegates that particular choice; “I don't know” leads to a recommendation rather than a silent assumption. You can explicitly ask to skip questions and proceed with stated assumptions.

## How it works

```text
Understand the project
        |
Select the capabilities it needs
        |
Prepare boundaries, ownership and structure
        |
Build the authorized first flow or hand off to the chosen workflow
        |
Verify, report limits and leave a continuation
```

AYR reads relevant project context and optional knowledge sources, checks the actual repository and selects only the instructions needed for the next step. It records recommendations separately from capabilities that are really activated.

**Typical outputs:** a useful README; consistent `AGENTS.md` and `CLAUDE.md`; code and tests when requested; a short record of selected capabilities; and observed check results with outstanding work. Existing documents are reused. Architecture decisions, contracts, CI and planning are added when the project needs them.

## Working with GSD

[GSD](https://github.com/open-gsd/gsd-core) is an optional workflow for planning, executing and verifying projects in phases, with persistent project state. Its active public home is GSD Core; AYR's named routes are examples from inspected installed skills, so command and resource compatibility must be checked for your package version. GSD is not bundled here.

AYR can select existing skills for design, research, debugging, review and verification. They remain separate, optional capabilities: AYR does not bundle their code or install a whole collection.

When GSD already owns a project, its requirements, roadmap, state and checkpoints remain authoritative. AYR uses its progress/resume routing and hands over the brief and accepted decisions. It does not create a second roadmap or launch a competing director. New substantial work may benefit from GSD; small tasks can use a lighter path.

A listed skill is not necessarily ready. AYR checks its entry point, referenced resources and runtime support. A missing resource becomes a named blocker, not a fabricated successful handoff.

See [the routing guide](references/skill-routing.md) and [coordination rules](references/coordination.md). The live AYR-to-GSD handoff is **experimental and not yet verified**.

## What is tested

| Evidence | Observed result | Scope |
| --- | --- | --- |
| Package CI | Passes on Windows and Linux | Discovery fields, local links and selected portability/token patterns |
| Native installation | Four scenarios pass per OS | Real local Git clone/checkout and junction/symlink; existing install, modified staging and empty SHA are rejected |
| Small-project demonstration | Interview followed by a working reading-list CLI | Native agent session, fictional client, standard-library Python |
| Demo verification | 10 application tests and 14 independent CLI invocations | Persistence, Unicode, stable IDs, idempotence and preserving data on invalid inputs |
| Standalone client probes | Blocked by quota or execution policy | Not counted as successful end-to-end runs |
| Live GSD handoff | Pending | State was preserved in the blocked attempt; no completed handoff is claimed |

The installation suite redirects the clone URL to a local Git fixture; it tests actual filesystem mechanics, not anonymous access to GitHub. macOS installation is not tested by this release. The demo does not establish reliability for larger projects.

Read the [evaluation record](docs/evaluation.md) and [release notes](docs/releases/v0.1.0-beta.md) for the evidence and limits.

## Trust and permissions

Skills can influence an assistant's actions. Review AYR and any capability it proposes before loading or executing them. AYR asks for source/revision, license, permissions, executable resources and network/data access to be assessed. Stars and install counts are not security guarantees.

AYR is **not a sandbox or security scanner**. Its instructions cannot enforce isolation or override your client's permissions. Repository creation, publication and deployment remain within the scope you authorize. Private project information belongs inside its authorized boundary.

See [discovery and trust](references/discovery.md) and [security reporting](SECURITY.md).

## Inside the repository

| Path | Purpose |
| --- | --- |
| [SKILL.md](SKILL.md) | Main workflow loaded by the assistant |
| [references/](references/skill-routing.md) | Conditional routing, coordination, structure and trust guidance |
| [commands/AYR.md](commands/AYR.md) | Optional uppercase command adapter |
| [agents/openai.yaml](agents/openai.yaml) | Display metadata; not a runtime agent definition |
| [templates/bootstrap-record.md](templates/bootstrap-record.md) | Optional output contract |
| [docs/](docs/source-analysis.md) | Installation, design rationale, source analysis and evaluation |
| [tests/](tests/test_package.py) | Package checks and isolated installation tests |

The [public repository analysis](docs/public-reference-analysis.md) explains patterns from VS Code, uv, Django and FastAPI, with immutable source links and limits on what to copy.

## Contribute

For a bug report, include your OS, client/version, the request, expected behavior and the observed result. Use a minimal non-sensitive reproduction. For a workflow improvement, explain the concrete failure it solves and how to verify the change.

Run the checks with Python 3.11+ and Git:

```sh
python -m unittest discover -s tests -v
```

Use your installed launcher (`python3`, `py -3` or an explicit executable) if `python` is absent from PATH. Each OS intentionally skips the other platform's four installation cases.

See [CONTRIBUTING.md](CONTRIBUTING.md). Contributions and reuse are covered by the [MIT license](LICENSE).
