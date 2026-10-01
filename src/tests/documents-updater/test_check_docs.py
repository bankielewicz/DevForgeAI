"""Unit tests for the documents-updater validator script (SPEC-006 VER-09).

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/tests/documents-updater -p 'test_*.py'
"""

import contextlib
import importlib.util
import io
import re
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = (Path(__file__).resolve().parents[2]
          / "claude/DevForgeAI/skills/documents-updater/scripts/check_docs.py")
spec = importlib.util.spec_from_file_location("check_docs", SCRIPT)
check_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_docs)

CLEAN_README = """\
# wordcount

Counts words and lines in text files, for anyone scripting over plain text.

## Prerequisites

- Python 3.10 or later

## Quick start

1. Install from the checkout:

   ```bash
   pip install .
   ```

2. Count a file:

   ```bash
   wordcount notes.txt
   ```

## Templates in code are fine

```jinja
Hello {{ user.name }}, see [the docs](missing.md) and {{.Name}}.
```

Inline `{{placeholder}}` and ${{ secrets.TOKEN }} are fine too.

## Usage

See [usage](#usage), [prerequisites](#prerequisites), the [guide](docs/guide.md#set-up),
the [docs folder](docs/) and [the site](https://example.com/x.md).

## Usage

The second heading gets the anchor [usage-1](#usage-1).

![Screenshot of the output](docs/shot.png)
"""

CLEAN_CHANGELOG = """\
# Changelog

All notable changes to this project are documented in this file.

## Unreleased

### Added

- Added `--json` to print counts as a JSON object for scripts.

### Fixed

- Fixed counting of words separated by tabs.

## [1.0.0] - 2026-01-10

### Added

- Added `--lines` to count lines.

## [0.9.0] - 2025-12-01

### Added

- Added `--lines` to count lines.

[1.0.0]: https://example.com/compare/v0.9.0...v1.0.0
"""


class CheckDocsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()
        (self.root / "docs/guide.md").write_text("# Guide\n\n## Set up\n\nSteps.\n")
        (self.root / "docs/shot.png").write_bytes(b"\x89PNG")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        path = self.root / name
        path.write_text(textwrap.dedent(text))
        return path

    def findings(self, name, text):
        return check_docs.check(self.write(name, text))

    def errors(self, name, text):
        return [m for _, sev, m in self.findings(name, text) if sev == "error"]

    def warnings(self, name, text):
        return [m for _, sev, m in self.findings(name, text) if sev == "warning"]

    def assertError(self, name, text, fragment):
        errors = self.errors(name, text)
        self.assertTrue(any(fragment in e for e in errors), f"no error containing {fragment!r}: {errors}")

    # Clean documents

    def test_clean_readme_and_changelog_have_no_findings(self):
        self.assertEqual(self.findings("README.md", CLEAN_README), [])
        self.assertEqual(self.findings("CHANGELOG.md", CLEAN_CHANGELOG), [])

    def test_front_matter_title_replaces_h1(self):
        self.assertEqual(self.errors("page.md", "---\ntitle: Page\n---\n\n## Section\n\nText.\n"), [])

    def test_leading_rule_is_not_front_matter(self):
        # A document may open with a horizontal rule; only a `key:` line after `---` starts front
        # matter, so the H1 between two rules is still seen.
        text = "---\n\n# Title\n\nText.\n\n---\n\n## Section\n\nBody.\n"
        self.assertEqual(self.errors("a.md", text), [])

    def test_setext_and_html_headings_count(self):
        self.assertEqual(self.errors("a.md", "Title\n=====\n\nText.\n\nPart\n----\n\nMore.\n"), [])
        self.assertEqual(self.errors("b.md", '<h1 align="center">Tool</h1>\n\n## Use\n\nText.\n'), [])

    # Structure

    def test_missing_and_second_h1(self):
        self.assertError("a.md", "## Only a section\n\nText.\n", "no H1")
        self.assertError("b.md", "# One\n\nText.\n\n# Two\n\nText.\n", "second H1")

    def test_skipped_heading_level(self):
        self.assertError("a.md", "# T\n\n## A\n\nText.\n\n#### Deep\n\nText.\n", "skips from H2 to H4")

    def test_unclosed_fence(self):
        self.assertError("a.md", "# T\n\n```bash\nls\n", "never closed")

    def test_empty_section_but_not_parent_heading(self):
        self.assertError("a.md", "# T\n\n## Empty\n\n## Full\n\nText.\n", "empty section: 'Empty'")
        self.assertError("b.md", "# T\n\nText.\n\n## Last\n\n<!-- nothing -->\n", "empty section: 'Last'")
        self.assertEqual(self.errors("c.md", "# T\n\n## Parent\n\n### Child\n\nText.\n"), [])

    def test_headings_in_code_and_comments_are_ignored(self):
        text = "# T\n\n```md\n# Not a heading\n```\n\n<!--\n# Also not\n-->\n\nText.\n"
        self.assertEqual(self.errors("a.md", text), [])

    def test_comment_marker_in_inline_code_hides_nothing(self):
        # Regression: `<!--` mid-line once hid every later fence and heading.
        text = ("# T\n\n- no `<!--` or `<!-- guide: -->` remain.\n\n## Later\n\n"
                "```bash\necho [x](nope.md) {{ .Values.x }}\n```\n")
        self.assertEqual(self.errors("a.md", text), [])
        self.assertError("b.md", text + "\n## Empty\n", "empty section: 'Empty'")

    # Template leftovers

    def test_placeholder_in_prose_and_in_code(self):
        self.assertError("a.md", "# {{Project name}}\n\nText.\n", "placeholder left: {{Project name}}")
        self.assertError("b.md", "# T\n\n```bash\n{{command from the repository}}\n```\n",
                         "placeholder left in code")

    def test_placeholders_in_inline_code_and_every_placeholder_reported(self):
        self.assertError("a.md", "# T\n\n| Tests | `{{command from the repository}}` |\n",
                         "placeholder left in code")
        self.assertEqual(self.errors("b.md", "# T\n\nSet `{{ .Values.image }}` in Helm.\n"), [])
        errors = self.errors("c.md", "# T\n\n{{one}} and {{two}}\n")
        self.assertEqual(len([e for e in errors if "placeholder" in e]), 2, errors)

    def test_guide_comment(self):
        self.assertError("a.md", "# T\n\n<!-- guide: delete me -->\nText.\n", "guide comment")

    # Links

    def test_broken_link_and_anchor(self):
        self.assertError("a.md", "# T\n\nSee [x](nope.md).\n", "broken link: nope.md")
        self.assertError("b.md", "# T\n\nSee [x](docs/guide.md#nowhere).\n", "broken anchor")
        self.assertError("c.md", "# T\n\nSee [x](#missing).\n", "broken anchor: #missing")
        self.assertError("d.md", "# T\n\n[ref]: missing/file.md\n", "broken link")

    def test_footnote_definitions_are_not_links(self):
        text = "# T\n\nSee the note.[^1]\n\n[^1]: This is a footnote.\n[^long-note]: Another one.\n"
        self.assertEqual(self.errors("a.md", text), [])

    def test_image_without_alt_text_is_a_warning(self):
        text = "# T\n\n![](docs/shot.png)\n"
        self.assertEqual(self.errors("a.md", text), [])
        self.assertTrue(any("alt text" in w for w in self.warnings("a.md", text)))

    def test_links_in_subfolder_resolve_from_the_file(self):
        (self.root / "docs/sub").mkdir()
        path = self.root / "docs/sub/page.md"
        path.write_text("# P\n\nBack to the [guide](../guide.md#set-up).\n")
        self.assertEqual(check_docs.check(path), [])

    # Changelog

    def test_changelog_unreleased_rules(self):
        self.assertError("CHANGELOG.md", "# C\n\n## Unreleased\n\n- a\n\n## Unreleased\n\n- b\n",
                         "second Unreleased")
        self.assertError("CHANGELOG.md", "# C\n\n## [1.0.0]\n\n- a\n\n## Unreleased\n\n- b\n",
                         "must come before")

    def test_changelog_duplicates(self):
        dup_cat = "# C\n\n## Unreleased\n\n### Added\n\n- a\n\n### Added\n\n- b\n"
        self.assertError("CHANGELOG.md", dup_cat, "duplicate category")
        dup_entry = "# C\n\n## Unreleased\n\n### Added\n\n- Added `--json`.\n- Added  `--json`\n"
        self.assertError("CHANGELOG.md", dup_entry, "duplicate Unreleased entry")

    def test_changelog_nested_bullets_are_not_entries(self):
        # Only the section's least-indented bullets are entries; a repeated sub-bullet is not a
        # duplicate entry, while repeated entries indented under a category still are.
        nested = ("# C\n\n## Unreleased\n\n### Added\n\n- Added X.\n  - Requires Y.\n"
                  "- Added Z.\n  - Requires Y.\n")
        self.assertEqual(self.errors("CHANGELOG.md", nested), [])
        indented = "# C\n\n## Unreleased\n\n### Added\n\n  - Added X.\n    - Note.\n  - Added X.\n"
        self.assertError("CHANGELOG.md", indented, "duplicate Unreleased entry")

    def test_changelog_empty_unreleased_is_allowed(self):
        # Keep a Changelog keeps an empty Unreleased section after a release; an empty category
        # under it is still an error, and so is an empty Unreleased outside a changelog.
        text = ("# Changelog\n\n## [Unreleased]\n\n## [1.0.0] - 2026-01-10\n\n### Added\n\n- First.\n\n"
                "[Unreleased]: https://example.com/compare/v1.0.0...HEAD\n")
        self.assertEqual(self.errors("CHANGELOG.md", text), [])
        self.assertError("CHANGELOG.md", "# C\n\n## Unreleased\n\n### Added\n\n## [1.0.0]\n\n- a\n",
                         "empty section: 'Added'")
        self.assertError("notes.md", "# C\n\n## Unreleased\n\n## Later\n\nText.\n",
                         "empty section: 'Unreleased'")

    def test_changelog_warnings(self):
        text = "# C\n\n## [Unreleased]\n\n### Improvements\n\n- a\n"
        self.assertEqual(self.errors("CHANGELOG.md", text), [])
        warnings = self.warnings("CHANGELOG.md", text)
        self.assertTrue(any("not a Keep a Changelog category" in w for w in warnings), warnings)
        self.assertTrue(any("no link definition" in w for w in warnings), warnings)

    def test_changelog_sections_end_at_h1_releases(self):
        # Conventional-changelog files use H1 for minor releases; Unreleased stops there.
        text = "# Changelog\n\n## Unreleased\n\n- Added a.\n\n# [1.1.0] (2026-01-01)\n\n- Added a.\n"
        self.assertFalse(any("duplicate" in e for e in self.errors("CHANGELOG.md", text)))

    def test_changelog_rules_apply_only_to_changelog_files(self):
        text = "# C\n\n## Unreleased\n\n- a\n\n## Unreleased\n\n- b\n"
        self.assertEqual(self.errors("notes.md", text), [])

    # Command line

    def test_exit_codes(self):
        good = self.write("README.md", CLEAN_README)
        bad = self.write("bad.md", "## No title\n")
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(check_docs.main([str(good)]), 0)
            self.assertEqual(check_docs.main([str(good), str(bad)]), 1)
            self.assertEqual(check_docs.main([str(self.root / "absent.md")]), 1)
        self.assertIn("bad.md:1: error: no H1", out.getvalue())

    def test_assets_are_flagged_until_filled(self):
        assets = SCRIPT.parent.parent / "assets"
        names = sorted(p.name for p in assets.glob("*.md"))
        self.assertEqual(len(names), 12, names)
        for path in assets.glob("*.md"):
            with self.subTest(asset=path.name):
                errors = [m for _, sev, m in check_docs.check(path) if sev == "error"]
                self.assertTrue(any("guide comment" in e for e in errors), errors)

    def test_every_asset_placeholder_is_detected(self):
        # With the guide comments deleted, each line that still holds a {{placeholder}} must be
        # reported, so a half-filled template can't pass step 6.
        assets = SCRIPT.parent.parent / "assets"
        for asset in assets.glob("*.md"):
            with self.subTest(asset=asset.name):
                text = re.sub(r"<!--\s*guide:.*?-->\n?", "", asset.read_text(), flags=re.S)
                path = self.write(asset.name, text)
                flagged = {line for line, sev, m in check_docs.check(path)
                           if sev == "error" and "placeholder" in m}
                expected = {n for n, l in enumerate(text.split("\n"), 1) if "{{" in l}
                self.assertEqual(expected - flagged, set(), f"undetected placeholder lines in {asset.name}")


if __name__ == "__main__":
    unittest.main()
