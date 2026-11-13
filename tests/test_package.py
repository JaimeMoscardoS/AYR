"""Package integrity checks; not a behavioral or third-party safety certification."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageIntegrity(unittest.TestCase):
    def test_skill_discovery_fields_are_present(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertTrue(text.startswith('---\n'))
        self.assertIn('\n---\n', text[4:])
        frontmatter = text.split('\n---\n', 1)[0][4:]
        fields = {}
        for line in frontmatter.splitlines():
            key, separator, value = line.partition(':')
            self.assertTrue(separator, 'Expected single-line frontmatter fields')
            self.assertNotIn(key, fields, 'Duplicate frontmatter field')
            fields[key] = value.strip().strip('\"\'')
        self.assertEqual(fields.get('name'), 'ayr')
        self.assertTrue(fields.get('description'), 'A non-empty discovery description is required')

    def test_local_markdown_links_resolve_inside_package(self):
        for document in ROOT.rglob('*.md'):
            if '.git' in document.parts:
                continue
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', document.read_text(encoding='utf-8')):
                if '://' in target or target.startswith('#'):
                    continue
                destination = (document.parent / target.split('#')[0]).resolve()
                with self.subTest(document=str(document), target=target):
                    self.assertTrue(destination.is_relative_to(ROOT))
                    self.assertTrue(destination.is_file())

    def test_no_workstation_paths_endpoints_or_credential_patterns(self):
        patterns = [r'[A-Za-z]:[/\\]Users[/\\]', r'127\.0\.0\.1:\d+',
                    r'gh[pousr]_[A-Za-z0-9]{20,}', r'sk-[A-Za-z0-9]{24,}']
        for document in ROOT.rglob('*.md'):
            if '.git' in document.parts:
                continue
            text = document.read_text(encoding='utf-8')
            for pattern in patterns:
                with self.subTest(document=str(document), pattern=pattern):
                    self.assertIsNone(re.search(pattern, text))


if __name__ == '__main__':
    unittest.main()
