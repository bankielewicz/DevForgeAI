from pathlib import Path
import re,unittest
from make_prd_evals import adapt,SOURCE

class ProviderGraderTests(unittest.TestCase):
    def test_new_row_uses_codex_and_requires_unreviewed(self):
        path=Path('extension-keeps-review-history/graders/new-row-unreviewed.md')
        text=adapt(path,(SOURCE/path).read_bytes()).decode()
        pattern=re.split(r'^---[ \t]*$',text,maxsplit=2,flags=re.M)[-1].strip()
        cases=[('codex','This revision has not been reviewed.',True),
               ('claude-code','This revision has not been reviewed.',False),
               ('codex','This revision has been reviewed.',False),
               ('codex','Added FR-003.',False)]
        for tool,note,expected in cases:
            with self.subTest(tool=tool,note=note):
                row=f'\n| 2 | 2026-09-29 | {tool} (session unavailable) | {note} | FR-003 |\n'
                self.assertEqual(bool(re.search(pattern,row)),expected)

    def test_historical_authorship_graders_are_not_rewritten(self):
        for name in ['authors-unchanged.md','earlier-rows-unchanged.md']:
            path=Path('extension-keeps-review-history/graders')/name
            with self.subTest(name=name):
                raw=(SOURCE/path).read_bytes();self.assertEqual(adapt(path,raw),raw)

    def test_extension_fixture_authors_remain_claude(self):
        path=Path('extension-keeps-review-history/scaffold.sh')
        raw=(SOURCE/path).read_bytes();self.assertEqual(adapt(path,raw),raw)
        self.assertIn(b'authors: ["Priya Nair", "claude-code"]',raw)

if __name__=='__main__':unittest.main()
