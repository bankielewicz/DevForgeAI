"""Structure checks for SPEC-013's Claude Code adapter (src/claude/DevForgeAI/hooks/), VER-16.

- hooks/hooks.json names one module, and it exists;
- .claude-plugin/plugin.json names the $.state contract (types), the tracking setting (DM-05), the
  retentionDays setting (DM-06) and the two fuel settings (DM-07, DM-08), and its version is 0.29.0;
- CLAUDE.md's deploy command and its source-and-deploy check leave the module's tests and the engine's generated
  files out of the deployed copy;
- VER-04's expected event lines, kept in hooks/progress.test.ts between marker comments, validate against
  SPEC-012's events.schema.json (the run ID's random digits normalised to hex), and so does VER-63's usage line;
- every kind that hooks/progress.tsx passes to adapterLog is one DM-02 lists (VER-66, SPEC-013 version 25);
- SPEC-013's button rule reads as version 24 words it, in §2, §12 and the FR-003 link note (VER-67).

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
SPEC = ROOT / "docs/specs/spec/SPEC-013.md"
BEGIN = "// EXPECTED-EVENTS-BEGIN"
END = "// EXPECTED-EVENTS-END"
USAGE_BEGIN = "// EXPECTED-USAGE-EVENT-BEGIN"
USAGE_END = "// EXPECTED-USAGE-EVENT-END"


def expected_events():
    """VER-04's expected lines, as the JSON strings the test file holds."""
    text = (HOOKS / "progress.test.ts").read_text(encoding="utf-8")
    block = text[text.index(BEGIN):text.index(END)]
    literals = re.findall(r"^\s*'(\{.*\})',?\s*$", block, re.M)
    # The test file writes each line as a single-quoted TypeScript string: \\n there is \n in the line's JSON.
    return [lit.replace("\\\\", "\\") for lit in literals]


def dm02_kinds():
    """The adapter.log kinds SPEC-013's DM-02 lists: the backticked words between 'kind one of' and the end of that list."""
    rows = [l for l in SPEC.read_text(encoding="utf-8").splitlines() if l.startswith("| `sessions/<session>/adapter.log`")]
    assert len(rows) == 1, "DM-02 has one adapter.log row"
    text = rows[0]
    text = text[text.index("kind one of"):text.index("a line's text is one line")]
    return set(re.findall(r"`([a-z][a-z-]*)`", text))


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

    def test_plugin_json_has_the_retention_setting(self):
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        retention = manifest["userConfig"]["retentionDays"]
        self.assertEqual(retention["type"], "number")
        self.assertEqual((retention["default"], retention["min"], retention["max"]), (30, 7, 3650))
        self.assertEqual(retention["title"], "Keep progress files (days)")
        self.assertTrue((PLUGIN / "progress/prune.py").is_file())

    # SPEC-013 v20 (VER-52): every process the adapter starts gets an argv list, never a shell line, and the work files
    # reach prune.py's remove only as one --file=<path> token each, deduplicated.
    def test_ver52_processes_take_an_argv_and_remove_takes_file_tokens(self):
        tsx = (HOOKS / "progress.tsx").read_text(encoding="utf-8")
        calls = re.findall(r"\$\.process\.run\(\s*([^,]+),", tsx)
        self.assertGreaterEqual(len(calls), 5)
        for first in calls:
            self.assertTrue(first.startswith("[") or first == "argv", first)
        core = (HOOKS / "progress-core.ts").read_text(encoding="utf-8")
        body = core[core.index("export function removeArgv"):]
        body = body[:body.index("\n}\n")]
        self.assertIn("'remove'", body)
        self.assertIn("'--manifests'", body)
        self.assertIn("new Set(", body)
        self.assertIn("`--file=${p}`", body)
        self.assertNotIn("'--file'", body)

    # SPEC-013 version 23 (DM-07, DM-08) and version 27's plugin version (Bryan, 2026-10-09: '0.29.0 for v27').
    def test_plugin_json_has_the_fuel_settings_and_the_new_version(self):
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["version"], "0.29.0")
        warn = manifest["userConfig"]["precompactWarnFuel"]
        run = manifest["userConfig"]["precompactRunFuel"]
        self.assertEqual((warn["type"], warn["default"], warn["min"], warn["max"]), ("number", 30, 0, 95))
        self.assertEqual((run["type"], run["default"], run["min"], run["max"]), ("number", 20, 0, 95))
        self.assertEqual(warn["title"], "Warn before /devforgeai:precompact at (% of context left)")
        self.assertEqual(run["title"], "Run /devforgeai:precompact at (% of context left)")
        self.assertEqual(warn["description"], "Show a row above the prompt once this little of the context window is left, "
                         "saying when /devforgeai:precompact will run. 0 turns the row off.")
        self.assertEqual(run["description"], "Run /devforgeai:precompact once when this little of the context window is left. "
                         "0 never runs it.")

    # VER-66 (version 25): a kind the adapter writes to adapter.log must be one DM-02 lists (a kind listed for a behaviour not
    # yet built needs no call in the code, so the check goes from the code to the list and not back).
    def test_adapter_log_kinds_are_listed(self):
        tsx = (HOOKS / "progress.tsx").read_text(encoding="utf-8")
        calls = re.findall(r"adapterLog\(\$,\s*(\S)", tsx)
        literal = re.findall(r"adapterLog\(\$,\s*'([a-z][a-z-]*)'", tsx)
        self.assertGreaterEqual(len(literal), 20)
        # every call names its kind as a literal: the definition is `adapterLog($: E, ...)`, which `\$,` does not match
        self.assertEqual(len(calls), len(literal), "an adapterLog call whose kind is not a string literal")
        listed = dm02_kinds()
        self.assertIn("bash", listed)
        self.assertEqual(sorted(set(literal) - listed), [])
        # the kinds the dashboard cycle's adapter adds are among the calls, and version 27's `write` (BEH-42, ERR-03)
        for kind in ("command", "setting", "precompact", "dashboard", "write"):
            self.assertIn(kind, literal)
        self.assertIn("write", listed)

    # VER-67 (version 24): the button rule in §2, §12 and the FR-003 link note.
    def test_the_button_rule_reads_as_version_24_words_it(self):
        lines = SPEC.read_text(encoding="utf-8").splitlines()
        wording = re.compile(r"a button that starts work asks first, and the person's answer is the go-ahead \(SPEC-016 BEH-15\); "
                             r"the mode button, the band's controls and the precompact row send nothing", re.I)
        text = "\n".join(lines)
        front = text.split("\n---\n")[0]
        section2 = text[text.index("## 2. Constraints"):text.index("## 3. Architecture")]
        section12 = text[text.index("## 12. Alternatives considered"):text.index("## 13. Open questions")]
        for name, region in (("the FR-003 link note", front), ("§2", section2), ("§12", section12)):
            self.assertRegex(" ".join(region.split()), wording, name)
        for number, line in enumerate(lines, 1):
            if "no button sends a prompt" not in line.lower():
                continue
            allowed = line.startswith("**Version") or re.match(r"\| \d+ \|", line) or (
                line.lstrip().startswith("obligation:") and "Structure check in src/tests/progress/test_adapter_structure.py" in line)
            self.assertTrue(allowed, f"line {number} still says no button sends a prompt")

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

    def test_ver63_the_usage_event_line_validates_against_the_events_schema(self):
        validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
        text = (HOOKS / "progress.test.ts").read_text(encoding="utf-8")
        block = text[text.index(USAGE_BEGIN):text.index(USAGE_END)]
        literals = re.findall(r"^const EXPECTED_USAGE_EVENT = '(\{.*\})'\s*$", block, re.M)
        self.assertEqual(len(literals), 1)
        event = json.loads(literals[0].replace("-RANDOM8", "-00000000"))
        self.assertEqual(event["kind"], "usage")
        self.assertEqual([e.message for e in validator.iter_errors(event)], [])
        self.assertEqual(list(event)[:4], ["run", "seq", "time", "kind"])
        self.assertEqual(list(event)[4:], ["turn", "model", "input", "output", "cacheRead", "cacheWrite"])
        # a usage event DM-02 would refuse is refused by the schema (so the check above says something)
        for bad in ({"input": -1}, {"output": "7"}, {"model": ""}, {"turn": ""}, {"cacheRead": 1.5}):
            self.assertNotEqual([e.message for e in validator.iter_errors({**event, **bad})], [], bad)


if __name__ == "__main__":
    unittest.main()
