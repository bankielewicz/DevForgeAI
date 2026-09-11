#!/usr/bin/env python3
"""Apply the link and frontmatter graders to the package's own documents at both commits.

Measures whether the new unsupported-representation detectors change the answer
for real DevForgeAI documents, not only for authored fixtures.
"""
import importlib.util, sys
from pathlib import Path

FENCE = Path(__file__).resolve().parent
NEW = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/"
           "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert/scripts/graders.py")
OLD = FENCE / "restored" / "graders_e641797.py"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

GN, GO = load("gnew", NEW), load("gold", OLD)

ROOTS = [
    Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/"
         "providers/claude/plugins/devforgeai/skills/devforge-evaluate-expert"),
]
# every SKILL.md in the Claude plugin, for the frontmatter grader
PLUGIN = Path("/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910/"
              "providers/claude/plugins/devforgeai/skills")

def run(mod, root, grader, args):
    b = {"files_read": 0, "bytes_read": 0}
    try:
        o = mod.GRADERS[grader](root, args, b, {})
    except Exception as e:
        return ("EXCEPTION", type(e).__name__, str(e))
    return (o["result"], o["observed"], o["reason"])

changed = 0
print("== package_relative_links over the candidate's own Markdown")
root = ROOTS[0]
for md in sorted(root.rglob("*.md")):
    rel = md.relative_to(root).as_posix()
    if rel.startswith("evals/fixtures/"):
        continue
    o = run(GO, root, "package_relative_links", {"file": rel})
    n = run(GN, root, "package_relative_links", {"file": rel})
    flag = "" if o[0] == n[0] else "   <== CHANGED"
    if o[0] != n[0]:
        changed += 1
    print(f"  {rel:48s} e641797={o[0]:14s} f8a5741={n[0]:14s}{flag}")
    if o[0] != n[0]:
        print(f"      f8a5741 reason: {n[2]}")
print(f"  changed results: {changed}")

print()
print("== frontmatter_fields over every Claude plugin SKILL.md")
fchanged = 0
for skill in sorted(PLUGIN.iterdir()):
    sm = skill / "SKILL.md"
    if not sm.is_file():
        continue
    o = run(GO, skill, "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]})
    n = run(GN, skill, "frontmatter_fields", {"file": "SKILL.md", "fields": ["name", "description"]})
    flag = "" if o[0] == n[0] else "   <== CHANGED"
    if o[0] != n[0]:
        fchanged += 1
    print(f"  {skill.name:36s} e641797={o[0]:14s} f8a5741={n[0]:14s}{flag}")
print(f"  changed results: {fchanged}")
