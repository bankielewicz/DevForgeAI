"""Builds the project folders the context skill's manual checks need, beyond the eval scaffolds
(docs/runbooks/spec-011-manual-checks.md). It is never part of the plugin.

Run from anywhere, with the folder to build in (it must not exist yet):
    python3 make_fixtures.py <kind> <folder>
Kinds:
    many-items   the shared fixture, plus a pyproject.toml declaring 70 third-party packages (VER-21 d)
    long-doc     the example project, with front-end.md padded to about 480 lines (VER-21 e)
    hooks-every  the example project, with the VER-22 (a) hook: corrupt tech-stack.md after every Edit
    hooks-approval  the shared fixture, with the VER-22 (b) hook: corrupt tech-stack.md after approval
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parents[2] / "claude/DevForgeAI/evals/context"


def scaffold(case, folder):
    subprocess.run(["bash", str(EVALS / case / "scaffold.sh")], cwd=folder, check=True)


def hook(folder, mode):
    claude = folder / ".claude"
    claude.mkdir()
    shutil.copy(HERE / "corrupt_after_edit.py", claude / "corrupt_after_edit.py")
    command = f'python3 "$CLAUDE_PROJECT_DIR/.claude/corrupt_after_edit.py" {mode} docs/specs/context/tech-stack.md'
    settings = {"hooks": {"PostToolUse": [{"matcher": "Edit", "hooks": [{"type": "command", "command": command}]}]}}
    (claude / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")


def main(kind, folder):
    folder = Path(folder)
    folder.mkdir(parents=True)
    if kind == "many-items":
        scaffold("writes-the-set", folder)
        deps = "".join(f'    "package{i:02d}>=1.{i}",\n' for i in range(1, 71))
        (folder / "pyproject.toml").write_text(f'[project]\nname = "shiftlog"\ndependencies = [\n{deps}]\n')
    elif kind == "long-doc":
        scaffold("revision-clears-approval", folder)
        path = folder / "docs/specs/context/front-end.md"
        text = path.read_text()
        filler4 = "".join(f"- **Convention:** command `c{i:03d}` prints one line per shift.\n" for i in range(260))
        filler6 = "".join(f"- **Convention:** table style rule {i:03d} applies to every listing.\n" for i in range(160))
        text = text.replace("\n## 5. Accessibility", "\n" + filler4 + "\n## 5. Accessibility", 1)
        text = text.replace("\n## Change Log", "\n" + filler6 + "\n## Change Log", 1)
        text = text.replace("\n# CTX-011 — Front end\n", "\n# CTX-011 — Front end\n\n## Contents\n\n- [1. Components "
                            "covered](#1-components-covered)\n- [2. Framework and structure](#2-framework-and-structure)"
                            "\n- [3. State](#3-state)\n- [4. Interaction and output](#4-interaction-and-output)\n- [5. "
                            "Accessibility](#5-accessibility)\n- [6. Design system](#6-design-system)\n", 1)
        path.write_text(text)
    elif kind == "hooks-every":
        scaffold("revision-clears-approval", folder)
        hook(folder, "every")
    elif kind == "hooks-approval":
        scaffold("writes-the-set", folder)
        hook(folder, "approval")
    else:
        sys.exit(f"unknown kind {kind}")
    print(f"built {kind} in {folder}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
