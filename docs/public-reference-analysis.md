# Large public repository references

## Selection and method

Inspected 2026-11-13 through primary GitHub metadata and source files. Popularity counts below are dated discovery context, not scores for organization, security or fitness. These repositories were selected for concrete maintainable boundaries, contribution guidance and verifiable checks, across different project sizes and stacks. Their suites were not executed and their current CI status is not asserted. No code is bundled.

| Repository | Stars at inspection | Revision | Observed license |
| --- | ---: | --- | --- |
| microsoft/vscode | 195,362 | 86c90223b04dd9a1394ac4e95f8463cdfdf4ea9b | MIT |
| astral-sh/uv | 91,979 | 9b4fe9027f1682ed3e3c96d990ce9a9e1bb51b5d | MIT OR Apache-2.0 |
| django/django | 91,730 | 6c8143cf012e562dd713d91490853d7909a83a5f | BSD-3-Clause |
| fastapi/fastapi | 104,683 | 5add7a458d629b07311d48261f696b5ac2bb9a5f | MIT |

## VS Code: discoverable contributions and explicit test classes

[CONTRIBUTING.md](https://github.com/microsoft/vscode/blob/86c90223b04dd9a1394ac4e95f8463cdfdf4ea9b/CONTRIBUTING.md) requests reproducible reports with environment, expected and observed behavior. [package.json](https://github.com/microsoft/vscode/blob/86c90223b04dd9a1394ac4e95f8463cdfdf4ea9b/package.json) specifies the package manager and distinct commands; the aggregate test entry intentionally redirects contributors toward the appropriate scripts rather than claiming to run everything.

[Component tests](https://github.com/microsoft/vscode/blob/86c90223b04dd9a1394ac4e95f8463cdfdf4ea9b/src/vs/base/test/common/arrays.test.ts) and the [Linux PR workflow](https://github.com/microsoft/vscode/blob/86c90223b04dd9a1394ac4e95f8463cdfdf4ea9b/.github/workflows/pr-linux-test.yml) illustrate behavioral tests and separate unit, integration and smoke checks.

**Apply:** document the actual verification entry points, associate tests with owning components, and require a reproducible issue description. **Limit:** do not reproduce a desktop editor's build graph, runner fleet or test matrix in a small service. A familiar command name does not establish its coverage.

## uv: justified workspace boundaries and controlled snapshots

[Cargo.toml](https://github.com/astral-sh/uv/blob/9b4fe9027f1682ed3e3c96d990ce9a9e1bb51b5d/Cargo.toml) centralizes a real multi-package workspace and shared dependencies. [CONTRIBUTING.md](https://github.com/astral-sh/uv/blob/9b4fe9027f1682ed3e3c96d990ce9a9e1bb51b5d/CONTRIBUTING.md) describes focused tests, Python-version coverage and review of snapshot changes. The [CI workflow](https://github.com/astral-sh/uv/blob/9b4fe9027f1682ed3e3c96d990ce9a9e1bb51b5d/.github/workflows/ci.yml) illustrates scoped permissions and pinned external workflow references. The [README](https://github.com/astral-sh/uv/blob/9b4fe9027f1682ed3e3c96d990ce9a9e1bb51b5d/README.md) documents dual licensing; API license summaries alone may be incomplete.

**Apply:** shared dependency policy when multiple packages already exist, targeted developer checks, explicit snapshot review, and reviewed CI dependencies. **Limit:** never approve changed snapshots merely to make tests pass, or introduce a workspace without genuine package boundaries.

## Django: contribution paths and negative behavior tests

[CONTRIBUTING.rst](https://github.com/django/django/blob/6c8143cf012e562dd713d91490853d7909a83a5f/CONTRIBUTING.rst) provides a discoverable contribution path. [Request handlers](https://github.com/django/django/blob/6c8143cf012e562dd713d91490853d7909a83a5f/django/core/handlers/base.py) separate middleware loading and exception handling. [Exception tests](https://github.com/django/django/blob/6c8143cf012e562dd713d91490853d7909a83a5f/tests/handlers/test_exception.py) exercise invalid inputs and observable error responses. The [test workflow](https://github.com/django/django/blob/6c8143cf012e562dd713d91490853d7909a83a5f/.github/workflows/tests.yml) covers supported operating systems and Python variants.

**Apply:** documented contribution entry points, explicit error boundaries, and regression tests for invalid inputs. **Limit:** support only the platforms the target commits to; Django's process and extensive matrix are not universal requirements.

## FastAPI: explicit metadata and invalid-contract regression

[pyproject.toml](https://github.com/fastapi/fastapi/blob/5add7a458d629b07311d48261f696b5ac2bb9a5f/pyproject.toml) declares package metadata and dependency constraints. [Routing implementation](https://github.com/fastapi/fastapi/blob/5add7a458d629b07311d48261f696b5ac2bb9a5f/fastapi/routing.py) has a clear domain responsibility. [Invalid additional response tests](https://github.com/fastapi/fastapi/blob/5add7a458d629b07311d48261f696b5ac2bb9a5f/tests/test_additional_responses_bad.py) make rejected configuration observable. The [test workflow](https://github.com/fastapi/fastapi/blob/5add7a458d629b07311d48261f696b5ac2bb9a5f/.github/workflows/test.yml) illustrates path filters, pinned actions, restricted permissions and a platform/version matrix.

**Apply:** explicit package metadata and public contracts, negative tests where misconfiguration matters, CI dependencies pinned to reviewed revisions. **Limit:** a framework's compatibility matrix is much broader than a single application's; path filtering must still cover changes to shared dependencies and configuration.

## Decision rules for AYR (Arquitect Your Repository)

- Transfer a pattern only with its triggering need, concrete benefit, owning component and verification path.
- Keep error cases alongside happy-path acceptance, where relevant.
- Distinguish unit, integration, smoke and live-provider evidence instead of saying only "tests pass".
- Review snapshot changes and CI dependency updates as behavior changes.
- Prefer contribution instructions proportionate to expected collaborators.
- Do not install agents from these repositories or assume they define an agent team. Architectural references and capability sources serve different purposes.
