"""Retain one command attempt and the exact source/test identity it checked."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

EVIDENCE = Path(__file__).resolve().parent
ROOT = EVIDENCE.parents[3]


def main():
    name, cwd, *command = sys.argv[1:]
    destination = EVIDENCE / (name + ".json")
    if destination.exists():
        raise SystemExit("Attempt already exists: " + str(destination))
    paths = subprocess.check_output(["git", "ls-files", "-z", "src/codex/devforgeai/tests",
                                     "src/codex/devforgeai/skills/brainstorm"], cwd=ROOT).decode().split("\0")
    paths += [str(p.relative_to(ROOT)) for p in (ROOT / "src/codex/devforgeai/tests").glob("test_*.py")]
    record = {
        "command": command,
        "cwd": str(Path(cwd).resolve()),
        "started": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "status_before": subprocess.check_output(["git", "status", "--porcelain=v1"], cwd=ROOT,
                                                  env=dict(os.environ, GIT_OPTIONAL_LOCKS="0"), text=True),
        "files": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sorted(set(paths)) if p},
    }
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    record.update(exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr,
                  finished=datetime.datetime.now(datetime.timezone.utc).isoformat())
    destination.write_text(json.dumps(record, indent=2) + "\n")
    print(result.stdout + result.stderr)
    print("Evidence:", destination, "exit:", result.returncode)
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
