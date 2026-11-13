# Install AYR

AYR is a set of instructions and supporting references. You need a coding client that supports skills, and Git for the clone recipes below. The ZIP option does not require Git. Python 3.11+ is needed only to run this repository's tests. Optional specialist skills are not bundled.

## Install from the release ZIP

1. Download `AYR-v0.1.0-beta.zip` from the [release](https://github.com/JaimeMoscardoS/AYR/releases/tag/v0.1.0-beta) and extract it into a staging directory outside your client's skill discovery folders.
2. Inspect `ayr/SKILL.md` and its referenced resources. The archive contains the complete `ayr/` package, not an installer or a Git repository.
3. For both clients, ensure `~/.agents/skills/ayr` and `~/.claude/skills/ayr` are absent. Create their parent directories, move the reviewed `ayr/` directory into `~/.agents/skills/ayr`, and create a directory symlink (Linux/macOS) or junction (Windows) at `~/.claude/skills/ayr` pointing to that canonical directory. Use your operating system's directory/link facilities; preserve any existing installation instead of overwriting it. For a single client, place the reviewed package directly in that client's skill directory.
4. Follow the command-adapter and recognition steps below, then open your target project. Do not run the Git clone/checkout blocks against a ZIP installation: the archive has no `.git` directory. To update it, review and replace the package from a chosen release with your client closed.

The archive layout is checked before release. The automated installation suite exercises the Git recipes, not this manual ZIP placement route.

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

## Check the installation

Open a target project folder in your client and ask it to use `ayr`. It should load `SKILL.md` and ask about unanswered product decisions before changing project files. A complete brief should avoid repeated questions. Merely seeing the skill name in a catalog does not prove it was invoked.

Do not run these fresh-install recipes over an existing installation. To update a detached clone, fetch a chosen revision, review the changes and check out that exact commit. Keep the shared clone and command adapters consistent; do not merge unrelated copies.
