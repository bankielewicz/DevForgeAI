"""Retain immutable inputs and complete stdout/stderr for one helper trial."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


run_root = Path(__file__).resolve().parent.parent
attempt = Path(__file__).resolve().parent / sys.argv[1]
attempt.mkdir(exist_ok=False)
rows = []
for relative in ("scripts/observe.py", "tests/test_observe.py"):
    source = run_root / "candidate" / relative
    data = source.read_bytes()
    frozen = attempt / "input" / relative
    frozen.parent.mkdir(parents=True, exist_ok=True)
    frozen.write_bytes(data)
    rows.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
(attempt / "input-manifest.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
temporary = attempt / "temporary"
temporary.mkdir()
environment = dict(os.environ)
for key in ("TEMP", "TMP", "TMPDIR"):
    environment[key] = str(temporary)
environment["SV_TEST_RECEIPT_DIR"] = str(attempt / "cases")
command = [sys.executable, "-B", "-X", "utf8", "-m", "unittest", "discover", "-s", str(attempt / "input" / "tests"), "-v"]
(attempt / "command.json").write_text(json.dumps({"argv": command, "cwd": str(attempt), "environment": {key: environment[key] for key in ("TEMP", "TMP", "TMPDIR", "SV_TEST_RECEIPT_DIR")}}, indent=2), encoding="utf-8")
result = subprocess.run(command, cwd=attempt, env=environment, capture_output=True, encoding="utf-8", timeout=300, check=False)
(attempt / "stdout.txt").write_text(result.stdout, encoding="utf-8")
(attempt / "stderr.txt").write_text(result.stderr, encoding="utf-8")
(attempt / "result.json").write_text(json.dumps({"exit_code": result.returncode}, indent=2), encoding="utf-8")
print(result.stdout)
print(result.stderr)
print(f"Retained attempt: {attempt}")
sys.exit(result.returncode)
