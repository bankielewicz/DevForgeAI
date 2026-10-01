"""PostToolUse hook for the context skill's manual checks VER-22 (a) and (b)
(docs/runbooks/spec-011-manual-checks.md). It is never part of the plugin.

After an Edit of the named context document, it changes the frontmatter line `type: context` to
`type: contxt`, so context_check.py reports a schema error that no repair survives:
    python3 corrupt_after_edit.py every docs/specs/context/tech-stack.md      (VER-22 a)
    python3 corrupt_after_edit.py approval docs/specs/context/tech-stack.md   (VER-22 b)
"every" corrupts after every Edit of the file; "approval" only after an Edit whose new text sets
`status: approved`. Each corruption is logged to .claude/corrupt.log in the project.
"""
import json
import sys
from pathlib import Path

mode, target = sys.argv[1], sys.argv[2]
event = json.load(sys.stdin)
tool_input = event.get("tool_input") or {}
path = Path(tool_input.get("file_path", ""))
if event.get("tool_name") != "Edit" or not path.as_posix().endswith(target):
    sys.exit(0)
if mode == "approval" and "status: approved" not in tool_input.get("new_string", ""):
    sys.exit(0)
text = path.read_text(encoding="utf-8")
corrupted = text.replace("\ntype: context\n", "\ntype: contxt\n", 1)
if corrupted != text:
    path.write_text(corrupted, encoding="utf-8")
    log = Path(event.get("cwd") or ".") / ".claude/corrupt.log"
    log.parent.mkdir(exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(f"corrupted {target} after an Edit ({mode})\n")
