"""Structure checks for SPEC-013's Claude Code adapter (src/claude/DevForgeAI/hooks/), VER-16.

- hooks/hooks.json names one module, and it exists;
- .claude-plugin/plugin.json names the $.state contract (types) and the tracking setting (DM-05);
- CLAUDE.md's deploy command and its source-and-deploy check leave the module's tests and the engine's generated
  files out of the deployed copy;
- VER-04's expected event lines, kept in hooks/progress.test.ts between marker comments, validate against
  SPEC-012's events.schema.json (the run ID's random digits normalised to hex).

The adapter's behaviour is tested by `claude plugin test src/claude/DevForgeAI` (VER-04 to VER-14); its
`claude plugin validate` result is recorded in SPEC-013 §9.

Run from the repository root:
    PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
"""
import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[3]
PLUGIN = ROOT / "src/claude/DevForgeAI"
HOOKS = PLUGIN / "hooks"
SCHEMA = PLUGIN / "progress/schemas/events.schema.json"
CLAUDE_MD = ROOT / "CLAUDE.md"
BEGIN = "// EXPECTED-EVENTS-BEGIN"
END = "// EXPECTED-EVENTS-END"


def expected_events():
    """VER-04's expected lines, as the JSON strings the test file holds."""
    text = (HOOKS / "progress.test.ts").read_text(encoding="utf-8")
    block = text[text.index(BEGIN):text.index(END)]
    literals = re.findall(r"^\s*'(\{.*\})',?\s*$", block, re.M)
    # The test file writes each line as a single-quoted TypeScript string: \\n there is \n in the line's JSON.
    return [lit.replace("\\\\", "\\") for lit in literals]


class AdapterStructure(unittest.TestCase):
    def test_hooks_json_names_one_module_that_exists(self):
        hooks = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))
        self.assertEqual(list(hooks), ["modules"])
        self.assertEqual(hooks["modules"], ["./progress.tsx"])
        self.assertTrue((HOOKS / "progress.tsx").is_file())

    def test_plugin_json_names_types_and_the_tracking_setting(self):
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["types"], "./types/index.d.ts")
        self.assertTrue((PLUGIN / "types/index.d.ts").is_file())
        tracking = manifest["userConfig"]["tracking"]
        self.assertEqual(tracking["type"], "string")
        self.assertEqual(tracking["options"], ["on", "off"])
        self.assertEqual(tracking["default"], "on")

    def test_the_deploy_command_leaves_tests_and_generated_files_out(self):
        text = CLAUDE_MD.read_text(encoding="utf-8")
        deploy = [line for line in text.splitlines() if line.startswith("X") and "--exclude" in line]
        joined = " ".join(deploy)
        for pattern in ("'*.test.ts'", "'*.test.tsx'", "/tsconfig.json", "/.claude-plugin/types/"):
            self.assertIn(pattern, joined)
        self.assertIn('rsync -a --delete "${X[@]}" src/claude/DevForgeAI/ .claude/skills/devforgeai/', text)
        self.assertIn('diff -rq "${D[@]}" src/claude/DevForgeAI .claude/skills/devforgeai', text)
        excluded = " ".join(line for line in text.splitlines() if line.startswith("D=("))
        for pattern in ("'*.test.ts'", "'*.test.tsx'", "tsconfig.json"):
            self.assertIn(pattern, excluded)

    def test_ver04_expected_lines_validate_against_the_events_schema(self):
        validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
        lines = expected_events()
        self.assertEqual(len(lines), 14)
        for line in lines:
            event = json.loads(line.replace("-RANDOM8", "-00000000"))
            errors = [e.message for e in validator.iter_errors(event)]
            self.assertEqual(errors, [], line)
        self.assertEqual([json.loads(l)["seq"] for l in lines], list(range(1, 15)))


if __name__ == "__main__":
    unittest.main()
