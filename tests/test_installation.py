"""Run documented installation against local Git fixtures, never a network clone.

Windows exercises PowerShell with literal home references redirected to a synthetic
directory. Linux exercises Bash with HOME set only in the child environment.
This verifies installation mechanics, not coding-client discovery or safety.
"""
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DocumentedInstallation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.git = shutil.which('git')
        if not cls.git:
            raise unittest.SkipTest('Git is required for installation fixtures')
        readme = (ROOT / 'docs' / 'installation.md').read_text(encoding='utf-8')
        cls.blocks = {}
        for language in ('bash', 'powershell'):
            blocks = re.findall(r'```' + language + r'\n(.*?)```', readme, re.S)
            if len(blocks) != 2:
                raise AssertionError(f'Expected two {language} installation blocks')
            cls.blocks[language] = blocks
        urls = re.findall(r'git clone (https://github\.com/\S+\.git)', readme)
        if len(urls) != 2 or len(set(urls)) != 1:
            raise AssertionError('Expected one explicit clone URL in both recipes')
        cls.clone_url = urls[0]
        cls.workspace = tempfile.TemporaryDirectory(prefix='ayr-install-test-')
        cls.addClassCleanup(cls.workspace.cleanup)
        cls.base = Path(cls.workspace.name).resolve()
        cls.source = cls.base / 'source'
        shutil.copytree(ROOT, cls.source, ignore=shutil.ignore_patterns(
            '.git', '__pycache__', '.venv', 'node_modules', '.env', '.env.*'))
        cls.empty_hooks = cls.base / 'empty-hooks'
        cls.empty_hooks.mkdir()
        cls.git_env = os.environ.copy()
        # Override hooks/signing only for fixture processes; no user config edits.
        cls.git_env.update({
            'GIT_CONFIG_COUNT': '3',
            'GIT_CONFIG_KEY_0': 'core.hooksPath',
            'GIT_CONFIG_VALUE_0': str(cls.empty_hooks),
            'GIT_CONFIG_KEY_1': 'commit.gpgsign',
            'GIT_CONFIG_VALUE_1': 'false',
            'GIT_CONFIG_KEY_2': 'core.autocrlf',
            'GIT_CONFIG_VALUE_2': 'false',
            'GIT_TERMINAL_PROMPT': '0',
        })
        cls.git_call('init', '-b', 'main')
        cls.git_call('add', '.')
        cls.git_call('-c', 'user.name=Installation fixture', '-c',
                     'user.email=fixture@example.invalid', 'commit', '-m', 'Fixture')
        cls.source_revision = cls.git_call('rev-parse', 'HEAD').strip()

    @classmethod
    def git_call(cls, *args):
        result = subprocess.run([cls.git, '-C', str(cls.source), *args],
                                env=cls.git_env, capture_output=True, text=True,
                                encoding='utf-8', errors='replace', timeout=60)
        if result.returncode:
            raise AssertionError(result.stdout + result.stderr)
        return result.stdout

    def setUp(self):
        self.case = Path(tempfile.mkdtemp(prefix='case-', dir=self.base))
        self.fake_home = self.case / 'home'
        self.fake_home.mkdir()
        self.stage_parent = self.case / 'staging'
        self.stage_parent.mkdir()
        self.real_home_before = self.home_fingerprint()

    def tearDown(self):
        self.assertEqual(self.real_home_before, self.home_fingerprint(),
                         'The real user skill installation must remain unchanged')
        self.assertEqual('', self.git_call('status', '--porcelain', '--ignored'))
        self.assertEqual(self.source_revision, self.git_call('rev-parse', 'HEAD').strip())

    @staticmethod
    def home_fingerprint():
        result = []
        for relative in ('.agents/skills/ayr', '.claude/skills/ayr'):
            location = Path.home() / relative
            entry = location / 'SKILL.md'
            result.append((relative, os.path.lexists(location),
                           hashlib.sha256(entry.read_bytes()).hexdigest()
                           if entry.is_file() else None))
        return result

    def environment(self):
        env = self.git_env.copy()
        env.update({
            'AYR_TEST_GIT': self.git,
            'AYR_TEST_SOURCE': str(self.source),
            'AYR_TEST_URL': self.clone_url,
            'AYR_TEST_HOME': str(self.fake_home),
            'TMPDIR': str(self.stage_parent),
            'TEMP': str(self.stage_parent),
            'TMP': str(self.stage_parent),
        })
        return env

    def run_bash(self, scenario):
        if os.name == 'nt':
            self.skipTest('Bash installation is exercised on Linux, not Git Bash')
        bash = shutil.which('bash')
        if not bash:
            self.skipTest('Bash is not installed')
        prepare, activate = self.blocks['bash']
        wrapper = '''git() {
  if [ "${1:-}" = clone ]; then
    [ "$2" = "$AYR_TEST_URL" ] || return 97
    "$AYR_TEST_GIT" clone --no-local "$AYR_TEST_SOURCE" "$3"
  else
    "$AYR_TEST_GIT" "$@"
  fi
}
'''
        mutation = {
            'success': '',
            'repeat': '',
            'dirty': 'printf "modified\\n" >> "$ayr_stage/SKILL.md"\n',
            'empty_sha': "ayr_revision=''\n",
        }[scenario]
        script = wrapper + prepare + '\n[ "$?" -eq 0 ] || exit 90\n' + mutation
        script += activate + '\nayr_test_status=$?\n'
        if scenario == 'repeat':
            script += '[ "$ayr_test_status" -eq 0 ] || exit 91\n'
            script += prepare + '\n[ "$?" -eq 0 ] || exit 92\n' + activate
            script += '\nayr_test_status=$?\n'
        script += 'exit "$ayr_test_status"\n'
        env = self.environment()
        env['HOME'] = str(self.fake_home)  # Child-process configuration only.
        return subprocess.run([bash], input=script, env=env, cwd=self.case,
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=90)

    def run_powershell(self, scenario):
        if os.name != 'nt':
            self.skipTest('Windows PowerShell/junction installation needs Windows')
        powershell = shutil.which('powershell')
        if not powershell:
            self.skipTest('Windows PowerShell is not installed')
        prepare, activate = [block.replace('$HOME', '$env:AYR_TEST_HOME')
                             for block in self.blocks['powershell']]
        wrapper = '''$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
function git {
    if ($args[0] -eq 'clone') {
        if ($args[1] -ne $env:AYR_TEST_URL) { throw 'Unexpected clone source.' }
        & $env:AYR_TEST_GIT clone --no-local $env:AYR_TEST_SOURCE $args[2]
    } else {
        & $env:AYR_TEST_GIT @args
    }
    $script:LASTEXITCODE = $LASTEXITCODE
}
'''
        mutation = {
            'success': '',
            'repeat': '',
            'dirty': "Add-Content -Encoding utf8 -LiteralPath (Join-Path $ayrStage 'SKILL.md') -Value 'modified'\n",
            'empty_sha': "$ayrRevision = ''\n",
        }[scenario]
        script = wrapper + prepare + '\n' + mutation + activate + '\n'
        if scenario == 'repeat':
            script += prepare + '\n' + activate + '\n'
        script += 'exit 0\n'
        entry = self.case / 'install.ps1'
        entry.write_text(script, encoding='utf-8-sig')
        return subprocess.run([powershell, '-NoProfile', '-NonInteractive',
                               '-File', str(entry)], env=self.environment(),
                              cwd=self.case, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=90)

    def assert_installation(self):
        canonical = self.fake_home / '.agents/skills/ayr'
        linked = self.fake_home / '.claude/skills/ayr'
        self.assertTrue((canonical / '.git').is_dir())
        self.assertTrue(linked.is_dir())
        self.assertTrue(os.path.samefile(canonical, linked))
        self.assertEqual((self.source / 'SKILL.md').read_bytes(),
                         (linked / 'SKILL.md').read_bytes())
        self.assertEqual((self.source / 'commands/AYR.md').read_bytes(),
                         (linked / 'commands/AYR.md').read_bytes())
        result = subprocess.run([self.git, '-C', str(canonical), 'rev-parse', 'HEAD'],
                                env=self.git_env, capture_output=True, text=True,
                                timeout=30)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual(self.source_revision, result.stdout.strip())

    def check_scenario(self, runtime, scenario):
        run = self.run_bash if runtime == 'bash' else self.run_powershell
        result = run(scenario)
        output = result.stdout + result.stderr
        if scenario == 'success':
            self.assertEqual(0, result.returncode, output)
            self.assert_installation()
        elif scenario == 'repeat':
            self.assertNotEqual(0, result.returncode, output)
            self.assertIn('An installation already exists', output)
            self.assert_installation()
        else:
            self.assertNotEqual(0, result.returncode, output)
            self.assertFalse((self.fake_home / '.agents/skills/ayr').exists())
            self.assertFalse((self.fake_home / '.claude/skills/ayr').exists())
            self.assertIn('Staging changed' if scenario == 'dirty'
                          else 'No valid reviewed revision', output)

    def test_bash_installation_and_link(self):
        self.check_scenario('bash', 'success')

    def test_bash_existing_installation_is_preserved(self):
        self.check_scenario('bash', 'repeat')

    def test_bash_dirty_checkout_is_rejected(self):
        self.check_scenario('bash', 'dirty')

    def test_bash_empty_revision_is_rejected(self):
        self.check_scenario('bash', 'empty_sha')

    def test_powershell_installation_and_junction(self):
        self.check_scenario('powershell', 'success')

    def test_powershell_existing_installation_is_preserved(self):
        self.check_scenario('powershell', 'repeat')

    def test_powershell_dirty_checkout_is_rejected(self):
        self.check_scenario('powershell', 'dirty')

    def test_powershell_empty_revision_is_rejected(self):
        self.check_scenario('powershell', 'empty_sha')


if __name__ == '__main__':
    unittest.main()
