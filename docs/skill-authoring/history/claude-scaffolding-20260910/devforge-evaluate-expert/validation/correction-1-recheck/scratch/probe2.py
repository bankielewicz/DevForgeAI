#!/usr/bin/env python3
"""Second probe batch: precedence and reporting completeness in the link grader."""
import importlib.util, shutil, sys
from pathlib import Path
FENCE = Path(__file__).resolve().parent
NEW = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/"
           "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/graders.py")
OLD = FENCE / "restored" / "graders_e641797.py"
def load(n, p):
    s = importlib.util.spec_from_file_location(n, str(p)); m = importlib.util.module_from_spec(s)
    sys.modules[n] = m; s.loader.exec_module(m); return m
GN, GO = load("gn2", NEW), load("go2", OLD)
FM = "---\nname: fixture-scope-note\ndescription: A probe fixture.\n---\n\n"
CASES = [
 ("P2-failure-hides-unsupported",
  FM + '[broken](missing.md)\n\n[ok](refs/a.md "title")\n',
  {"refs/a.md": "a\n"},
  "one plain broken link plus one unsupported titled link"),
 ("P2-two-unsupported-only-first-named",
  FM + '[a](x "t")\n\n<img src="y.png">\n',
  {},
  "two unsupported representations on different lines"),
 ("P2-refdef-inside-fence",
  FM + "```\n[missing]: nothere.md\n```\n",
  {},
  "reference definition inside a fence is skipped"),
]
for pid, skill, extra, note in CASES:
    root = FENCE / "fixtures" / pid
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "SKILL.md").write_text(skill, encoding="utf-8", newline="\n")
    for rel, c in extra.items():
        t = root / rel; t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(c, encoding="utf-8", newline="\n")
    for label, mod in (("e641797", GO), ("f8a5741", GN)):
        b = {"files_read": 0, "bytes_read": 0}
        o = mod.GRADERS["package_relative_links"](root, {"file": "SKILL.md"}, b, {})
        print(f"{pid} [{label}] {o['result']} observed={o['observed']!r}")
        print(f"    reason={o['reason']}")
    print(f"    note: {note}\n")
