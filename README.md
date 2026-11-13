# AYR (Arquitect Your Repository)

## What it is

A portable skill that prepares software repositories for humans, Claude Code, and Codex: discover useful capabilities, choose a proportionate structure, coordinate responsibilities, and leave reproducible verification and continuation notes.

**v0.1.0-beta · MIT licensed.** An early public release for real-project feedback. See [beta scope and validation](docs/releases/v0.1.0-beta.md) for tested behavior and remaining limits.

Installation mechanics are tested on Windows PowerShell and Linux Bash. Complete AYR interviews and AYR-to-GSD handoffs remain experimental: release-time client runs were blocked by usage limits or execution policy before instructions could be loaded. See the evaluation record for the difference between successful installation and workflow validation.

## Use

Ask the assistant to use ayr, for example:

> Use ayr to prepare a small Python API in this repository. Preserve existing work, evaluate useful agents/skills, and document how to run and verify it.

The workflow starts with a short project interview before changing files or choosing the architecture and agent team. It asks up to three questions per round about the product, users, first working outcome and relevant constraints, reuses information already provided, and waits for answers to dependent decisions. You can explicitly ask it to skip the interview and proceed with stated assumptions. A complete brief avoids repeated questions.

The portable skill ID is `ayr`; the visible name is **AYR (Arquitect Your Repository)**. Claude discovers the skill as `/ayr` and Codex supports `$ayr` or a natural-language request. The included `commands/AYR.md` adapter provides the uppercase command name for clients supporting custom slash commands. The skill itself requires no GitHub CLI, Node, RAG service, fixed agent catalog, or particular operating system. Optional discovery/integrations use tools actually available.

## Install for Claude Code and Codex

The examples use one canonical clone in `~/.agents/skills/ayr` and a link in `~/.claude/skills/ayr`. Both destinations must be absent; existing installations are never overwritten. Git is required. Use Bash on Linux/macOS and PowerShell on Windows; Git Bash on Windows is not the supported symlink installation route.

Stage the clone outside skill discovery, record its exact commit SHA, and review its instructions and referenced files before activating it. The commands detach at that captured revision and verify it again before activation. For a previously reviewed release, use its exact commit instead. Run staging and activation in the same terminal.

### Bash: stage and review

```bash
ayr_prepare() {
  ayr_revision=''
  ayr_stage="$(mktemp -d "${TMPDIR:-/tmp}/ayr.XXXXXX")" || return 1
  git clone https://github.com/JaimeMoscardoS/AYR.git "$ayr_stage" || return 1
  ayr_revision="$(git -C "$ayr_stage" rev-parse HEAD)" || return 1
  [[ "$ayr_revision" =~ ^[0-9a-f]{40,64}$ ]] || return 1
  git -C "$ayr_stage" checkout --detach "$ayr_revision" || return 1
  test -f "$ayr_stage/SKILL.md" || return 1
  git -C "$ayr_stage" ls-tree -r --name-only HEAD || return 1
  cat "$ayr_stage/SKILL.md"
}
ayr_prepare
```

Review the listed references and any executable resources as data. After accepting that revision, activate it:

```bash
ayr_activate() {
  [[ "${ayr_revision:-}" =~ ^[0-9a-f]{40,64}$ ]] || { printf '%s\n' 'No valid reviewed revision.' >&2; return 1; }
  test -n "${ayr_stage:-}" && test -f "$ayr_stage/SKILL.md" || return 1
  ayr_actual="$(git -C "$ayr_stage" rev-parse HEAD)" || return 1
  test "$ayr_actual" = "$ayr_revision" || return 1
  ayr_changes="$(git -C "$ayr_stage" status --porcelain --untracked-files=all --ignored)" || return 1
  test -z "$ayr_changes" || { printf '%s\n' 'Staging changed; review a clean checkout before activation.' >&2; return 1; }
  ayr_canonical="$HOME/.agents/skills/ayr"
  ayr_claude="$HOME/.claude/skills/ayr"
  if [ -e "$ayr_canonical" ] || [ -L "$ayr_canonical" ] ||
     [ -e "$ayr_claude" ] || [ -L "$ayr_claude" ]; then
    printf '%s\n' 'An installation already exists; review it separately.' >&2
    return 1
  fi
  mkdir -p "$HOME/.agents/skills" "$HOME/.claude/skills" || return 1
  mv "$ayr_stage" "$ayr_canonical" || return 1
  ln -s "$ayr_canonical" "$ayr_claude"
}
ayr_activate
```

### PowerShell: stage and review

```powershell
$ayrRevision = $null
$ayrStage = Join-Path ([IO.Path]::GetTempPath()) ('ayr-' + [guid]::NewGuid().ToString('N'))
git clone https://github.com/JaimeMoscardoS/AYR.git $ayrStage
if ($LASTEXITCODE -ne 0) { throw 'Clone failed.' }
$ayrRevision = git -C $ayrStage rev-parse HEAD
if ($LASTEXITCODE -ne 0) { throw 'Cannot resolve revision.' }
if ($ayrRevision -notmatch '^[0-9a-f]{40,64}$') { throw 'Invalid revision.' }
git -C $ayrStage checkout --detach $ayrRevision
if ($LASTEXITCODE -ne 0) { throw 'Revision checkout failed.' }
git -C $ayrStage ls-tree -r --name-only HEAD
Get-Content -Encoding utf8 -LiteralPath (Join-Path $ayrStage 'SKILL.md')
```

Review the listed resources before running the activation block. Windows uses a directory junction, which does not require enabling symbolic links:

```powershell
$ayrCanonical = [IO.Path]::GetFullPath((Join-Path $HOME '.agents/skills/ayr'))
$ayrClaude = [IO.Path]::GetFullPath((Join-Path $HOME '.claude/skills/ayr'))
if ($ayrRevision -notmatch '^[0-9a-f]{40,64}$') { throw 'No valid reviewed revision.' }
if (-not (Test-Path -LiteralPath (Join-Path $ayrStage 'SKILL.md') -PathType Leaf)) { throw 'Skill entry point is missing.' }
if ((Get-Item -LiteralPath $ayrCanonical -Force -ErrorAction SilentlyContinue) -or
    (Get-Item -LiteralPath $ayrClaude -Force -ErrorAction SilentlyContinue)) {
    throw 'An installation already exists; review it separately.'
}
$ayrActual = git -C $ayrStage rev-parse HEAD
if ($LASTEXITCODE -ne 0 -or $ayrActual -ne $ayrRevision) {
    throw 'Staged revision does not match; activation stopped.'
}
$ayrChanges = git -C $ayrStage status --porcelain --untracked-files=all --ignored
if ($LASTEXITCODE -ne 0 -or $ayrChanges) { throw 'Staging changed; review a clean checkout before activation.' }
$ayrSource = (Resolve-Path -LiteralPath $ayrStage).Path
if (-not $ayrSource.StartsWith([IO.Path]::GetFullPath([IO.Path]::GetTempPath()), [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Staging source must remain inside the temporary directory.'
}
New-Item -ItemType Directory -Force -Path (Split-Path $ayrCanonical), (Split-Path $ayrClaude) | Out-Null
Write-Output "Moving reviewed clone from $ayrSource to $ayrCanonical"
Move-Item -LiteralPath $ayrSource -Destination $ayrCanonical -ErrorAction Stop
New-Item -ItemType Junction -Path $ayrClaude -Target $ayrCanonical -ErrorAction Stop | Out-Null
```

Restart or reload the clients and check that each discovers the skill. The commands install instructions only; they do not launch agents or configure additional capabilities. A client with different discovery rules may require its documented adapter.

For the uppercase command, copy `commands/AYR.md` from the installed skill to `~/.claude/commands/AYR.md` and `~/.codex/prompts/AYR.md`, creating parent directories and checking that neither destination already exists. Custom-command presentation depends on the client; the portable skill invocation remains `ayr`.

## Start in your target project

Open the folder you want to build or prepare in your coding client, then invoke `/AYR` in Claude Code or `$ayr` in Codex with your request. The skill installation folder contains instructions; it is not the project workspace. For example, open your expense-tracker project and ask: "Use ayr to help me build a simple expense tracker. Start by asking about one useful daily workflow." The interview accepts uncertainty and helps choose proportionate defaults; a complete brief avoids repeated questions.

## What the workflow produces

- Project context, constraints and justified structure.
- Consistent project instructions for both assistants.
- A compact selection of skills and agent responsibilities with source, revision, license, permissions and review outcome.
- Work ownership and dependencies when delegation helps.
- Actual check results, outstanding work, and a concrete continuation.

A small project stays small. Existing architecture and instructions take precedence over copying reference layouts.

## How agents are organized

AYR integrates existing skills by phase instead of creating its own duplicate skill family. It can select design, research, debugging, review and verification capabilities as needed. For substantial staged projects, it can hand off to GSD; an existing GSD project retains its requirements, roadmap and state. Small tasks keep a lighter route. See [existing-skill routing](references/skill-routing.md) for selection, readiness checks and handoffs. Listed skills are optional integrations, not bundled or automatically installed dependencies.

One lead owns scope, integration and evidence. Explorers establish constraints; implementers own bounded files; reviewers independently check relevant risks. UI, security, data and domain specialists are selected only for concrete needs. Independent work can run in parallel with exclusive writable ownership; integration follows dependencies. A runtime without subagents executes responsibilities sequentially.

See [coordination](references/coordination.md), [discovery and trust](references/discovery.md), and [repository patterns](references/repository-patterns.md). RAG is optional context retrieval, with source/freshness checks and no required provider.

## Why these patterns

The [design rationale](docs/source-analysis.md) explains general patterns and public references. It distinguishes source inspection from executed tests. No third-party source code or skill packages are bundled.

The [large public reference analysis](docs/public-reference-analysis.md) adds VS Code, uv, Django and FastAPI with dated popularity, immutable source links, useful patterns and their limits. These are architecture and contribution references, not agents to install or layouts to copy wholesale.

## Validation

Run `python -m unittest discover -s tests -v` with Python 3.11+ for package integrity: skill discovery fields, local links, workstation paths and two common token patterns in Markdown. This is not a general secret scanner, third-party safety certification or proof of assistant behavior. See [behavioral evaluation](docs/evaluation.md) for scenario evidence and limits. Use your available Python launcher (`python3`, `py -3`, or an explicit executable) if `python` is absent from PATH.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Report a reproducible issue with client version, the expected result and the observed behavior. Exclude secrets and identifying details from private projects.
