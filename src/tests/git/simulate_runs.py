"""Checks the git eval graders offline with scripted runs. Each case gets a good run (the commands and
reply the skill should produce) and a bad run (what the graders must catch): the scaffold runs in a
temporary directory, the commands run there, and grade_evals.mjs scores the regex, file_exists and
tool_used graders (llm graders are skipped). Every good run should pass every checked grader; each bad
run should fail at least one. Rerun after changing a fixture or grader in make_evals.py. From the
repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/git/simulate_runs.py [case[:bad] ...]
"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
E = REPO / "src/claude/DevForgeAI/evals/git"
SK = REPO / "src/claude/DevForgeAI/skills/git"
ST = f"python3 {SK}/scripts/repo_state.py --default-branch main"
SC = f"python3 {SK}/scripts/scan_staged.py"
T = "PYTHONDONTWRITEBYTECODE=1 python3 -m unittest"

RUNS = {
    "delivers-task-changes": ([
        "git fetch origin", "git ls-remote --symref origin HEAD", ST,
        "git add -- app.py test_json.py", SC, T,
        "h1=$(git hash-object app.py); h2=$(git hash-object test_json.py); echo $h1 $h2 > $TMPDIR/h",
        "git switch -c feat/json-output",
        "git commit -q -m 'feat: add --json output'",
        "read h1 h2 < $TMPDIR/h; [ \"$(git rev-parse feat/json-output:app.py)\" = \"$h1\" ]",
        "git switch -q main",
        "printf '.claude/worktrees/\\n' >> .git/info/exclude",
        "git worktree add -q .claude/worktrees/feat-json-output feat/json-output",
        "cd .claude/worktrees/feat-json-output && git fetch -q origin && git rebase -q origin/main && " + T
        + " && git push -q -u origin feat/json-output",
    ], "Proposed ignore patterns: add `__pycache__/` and `*:Zone.Identifier` to .gitignore.\n\n"
       "Result: done\nPhases: start, commit, push\nChecks: python3 -m unittest: passed (2 tests)\n"),
    "delivers-task-changes:bad": ([
        "git add -A", "git commit -q -m 'add json'", "git push -q origin main:feat/json-output",
    ], "Result: done\n"),
    "blocks-secrets": ([ST, SC + " || true"],
        "config.py line 3 holds an AWS access key ID and .env is an environment file: both blocked.\n\nResult: blocked\n"),
    "blocks-secrets:bad": (["git add .env", "git commit -q -m x", "git push -q origin main"],
        "Committed config.py (AKIA" + "2E7QW4NB6YJ3VKTM).\nResult: done\n"),
    "starts-worktree-from-fresh-base": ([
        "git fetch origin", ST, "printf '.claude/worktrees/\\n' >> .git/info/exclude",
        "git worktree add -q --no-track -b feat/verbose .claude/worktrees/feat-verbose origin/main",
    ], "Result: done\n"),
    "starts-worktree-from-fresh-base:bad": ([
        "printf '.claude/worktrees/\\n' >> .gitignore",
        "git worktree add -q -b feat/verbose .claude/worktrees/feat-verbose main",
    ], "Result: done\n"),
    "connects-new-repository": ([
        "git init -q -b main", "git remote add origin \"$PWD/remote/app.git\"", "git fetch origin",
        "git ls-remote --symref origin HEAD",
    ], "Nothing pushed. I can make a bootstrap commit and push it if you want.\nResult: awaiting_approval\n"),
    "connects-new-repository:bad": ([
        "git init -q -b main", "git remote add origin \"$PWD/remote/app.git\"", "git add -- app.py README.md",
        "git commit -q -m init", "git push -q origin main",
    ], "Result: done\n"),
    "keeps-existing-origin": ([ST, "git remote -v"],
        "origin already points at /x/remote/origin.git; you asked for remote/mirror.git. Change it?\n\n"
        "Result: awaiting_approval\n"),
    "keeps-existing-origin:bad": (["git remote set-url origin \"$PWD/remote/mirror.git\""], "Result: done\n"),
    "stops-on-unrelated-histories": (["git fetch origin", "git merge-base main origin/main || true", ST],
        "Local main and origin/main are unrelated: they share no commit.\nResult: awaiting_approval\n"),
    "stops-on-unrelated-histories:bad": ([
        "git fetch -q origin", "git merge -q --allow-unrelated-histories -m m origin/main", "git push -q origin main",
    ], "Result: done\n"),
    "aborts-conflicting-rebase": ([
        "git fetch -q origin", ST, "git rebase origin/main || git rebase --abort",
    ], "The rebase conflicted in app.py, so I aborted it.\n\nResult: blocked\n"),
    "aborts-conflicting-rebase:bad": (["git fetch -q origin", "git rebase origin/main || true"], "Result: done\n"),
    "sync-fast-forwards": ([
        "git fetch --prune origin", ST,
        "git update-ref refs/devforgeai-backup/main/$(date -u +%Y%m%dT%H%M%SZ) refs/heads/main",
        "git merge -q --ff-only origin/main",
    ], "Result: done\n"),
    "sync-fast-forwards:bad": (["git pull -q", "git fetch -q origin", "git reset -q --hard origin/main"], "Result: done\n"),
    "sync-refuses-divergence": (["git fetch --prune origin", ST, "git log --oneline origin/main..main"],
        "main has a local-only commit, abc Add weekly summary to the to-do list.\nResult: awaiting_approval\n"),
    "sync-refuses-divergence:bad": (["git fetch -q origin", "git rebase -q origin/main"], "Result: done\n"),
    "sync-keeps-differing-edit": ([
        "git fetch --prune origin", ST,
        "git update-ref refs/devforgeai-backup/main/$(date -u +%Y%m%dT%H%M%SZ) refs/heads/main",
        "git hash-object config.yaml; git rev-parse origin/main:config.yaml",
    ], "config.yaml differs from the incoming version. Options: carry to a branch, stash, or leave.\n"
       "Result: awaiting_approval\n"),
    "sync-keeps-differing-edit:bad": ([
        "git fetch -q origin", "git stash -q", "git merge -q --ff-only origin/main", "git stash pop -q || true",
    ], "Result: done\n"),
    "sync-reconciles-identical-edits": ([
        "git fetch --prune origin", ST,
        "git update-ref refs/devforgeai-backup/main/$(date -u +%Y%m%dT%H%M%SZ) refs/heads/main",
        "git checkout HEAD -- config.yaml", "rm -- CHANGES.md", "git merge -q --ff-only origin/main",
    ], "Result: done\n"),
    "sync-reconciles-identical-edits:bad": (["git fetch -q origin", "git merge -q --ff-only origin/main || true"],
        "Result: blocked\n"),
    "prune-classifies-worktrees": ([
        "git fetch --prune origin", ST, "git worktree list --porcelain",
    ], "| Worktree | Status |\n|---|---|\n| feat-export | removable: merged, clean |\n"
       "| feat-csv | kept: untracked scratch.txt |\n| feat-charts | kept: not merged, 1 unpushed commit; idle (20 days) |\n"
       "| feat-search | kept: not merged; stale (35 days) |\n| feat-demo | kept: locked (kept for the customer demo) |\n\n"
       "Result: awaiting_approval\n"),
    "prune-classifies-worktrees:bad": ([
        "git worktree remove .claude/worktrees/feat-export", "git worktree remove --force .claude/worktrees/feat-csv",
    ], "feat-demo is stale.\nResult: done\n"),
    "status-is-read-only": (["git fetch origin", ST, "git status", "git worktree list", "git stash list"],
        "main is behind origin/main by 1 commit. Changes: app.py (modified), notes.txt (untracked).\n"
        "Worktrees: feat/export (clean), feat/charts (1 unpushed commit).\n\nResult: done\n"),
    "status-is-read-only:bad": (["git fetch origin", "git merge -q --ff-only origin/main || true", "git stash -q"],
        "Result: done\n"),
    "nothing-to-deliver": (["git fetch origin", ST], "Nothing to commit.\n\nResult: no_change\n"),
    "nothing-to-deliver:bad": (["git switch -q -c feat/empty", "git commit -q --allow-empty -m empty",
                                 "git push -q origin feat/empty"], "Result: done\n"),
    "ignores-unrelated-request": ([], "git merge joins histories with a merge commit; git rebase replays commits.\n"),
    "ignores-unrelated-request:bad": (["git pull -q --rebase"], "Done.\n"),
    "suggests-documents-updater": ([
        "git fetch origin", ST, "git diff --name-only $(git merge-base HEAD origin/main) HEAD",
        "git push -q origin feat/json-output",
    ], "The branch changes app.py but neither README.md nor CHANGELOG.md. I recommend running "
       "/devforgeai:documents-updater first.\n\nResult: partial\n"),
    "suggests-documents-updater:bad": ([
        "printf '\\n--json prints JSON.\\n' >> README.md", "printf '# Changelog\\n' > CHANGELOG.md",
    ], "Updated the docs.\nResult: done\n"),
}

SKILL_CALL = {"tool": "Skill", "input": {"skill": "devforgeai:git"}}


def simulate(key):
    name = key.split(":")[0]
    cmds, reply = RUNS[key]
    case = E / name
    with tempfile.TemporaryDirectory(prefix="git-sim-") as tmp:
        w = Path(tmp) / "ws"
        w.mkdir()
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        subprocess.run(["bash", str(case / "scaffold.sh")], cwd=w, env=env, check=True, capture_output=True)
        before = Path(tmp) / "before.txt"
        before.write_text(subprocess.run(["find", ".", "-type", "f"], cwd=w, capture_output=True, text=True).stdout)
        calls = [] if name == "ignores-unrelated-request" else [SKILL_CALL]
        if key == "suggests-documents-updater:bad":
            calls.append({"tool": "Skill", "input": {"skill": "devforgeai:documents-updater"}})
        for c in cmds:
            r = subprocess.run(["bash", "-c", c], cwd=w, env=env, capture_output=True, text=True)
            if r.returncode != 0 and not key.endswith(":bad"):
                print(f"  command failed ({r.returncode}): {c}\n  {r.stderr.strip()[:300]}")
            calls.append({"tool": "Bash", "input": {"command": c, "description": "Run step"}})
        (Path(tmp) / "reply.txt").write_text(reply)
        (Path(tmp) / "calls.json").write_text(json.dumps(calls))
        print(f"== {key}")
        r = subprocess.run(["node", str(REPO / "src/tests/git/grade_evals.mjs"), str(case), str(w),
                            str(Path(tmp) / "reply.txt"), str(Path(tmp) / "calls.json"), str(before)],
                           capture_output=True, text=True)
        print(r.stdout.rstrip())
        return r.returncode


if __name__ == "__main__":
    keys = sys.argv[1:] or list(RUNS)
    for k in keys:
        simulate(k)
