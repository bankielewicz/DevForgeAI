"""Retain offline console-helper checks. Never invoke native Codex."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\DevForgeAI")
RUN = Path(__file__).resolve().parent
PS5 = Path(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe")
PS7 = Path(r"C:\Program Files\PowerShell\7\pwsh.exe")
SCRIPT = ROOT / "Start-CodexAppServerDiagnostic.ps1"
SNAPSHOT = Path("docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-snapshot/src")
FIXTURE = Path("docs/plan/framework-worker-trials/20260916T202125Z-diagnostic/fixture/task.json")


def record(name, argv):
    output = RUN / name
    output.mkdir(exist_ok=False)
    result = subprocess.run([str(item) for item in argv], cwd=ROOT, capture_output=True, timeout=60)
    (output / "stdout.bin").write_bytes(result.stdout)
    (output / "stderr.bin").write_bytes(result.stderr)
    receipt = {"argv": [str(item) for item in argv], "cwd": str(ROOT), "exit_code": result.returncode}
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    return result


def invoke(shell, script):
    return [shell, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", script, "-CheckOnly"]


def red():
    result = record("red-legacy", [PS5, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", RUN / "legacy-argument-repro.ps1"])
    observed = json.loads(result.stdout.decode("utf-8-sig"))
    assert result.returncode != 0 and observed["actual_arguments"] == 0
    assert observed["expected_arguments"] == 116 and observed["worker_started"] is False
    print("Expected RED observed: Windows PowerShell 5.1 produced zero of 116 arguments; no worker was launched.")


def green():
    expected = json.loads((ROOT / SNAPSHOT / "restrictive-launch-policy.json").read_bytes())["argv"]
    trial_root = ROOT / "docs/plan/framework-worker-trials"
    before = {p.name for p in trial_root.iterdir()}
    checks = []
    for shell, name in ((PS7, "green-powershell7"), (PS5, "green-powershell51")):
        result = record(name, invoke(shell, SCRIPT))
        assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
        observed = json.loads(result.stdout.decode("utf-8-sig"))
        assert observed["argument_count"] == 116 and observed["argv"] == expected
        assert int(observed["powershell_version"].split(".")[0]) >= 7
        assert observed["worker_started"] is False
        assert observed["child_only_removed_environment_names"] == ["ANTHROPIC_API_KEY"]
        checks.append({"case": name, "result": "PASS", "argument_count": 116})
    assert {p.name for p in trial_root.iterdir()} == before, "CheckOnly created a runtime directory"

    rejected = RUN / "rejected-policy-fixture"
    (rejected / SNAPSHOT).mkdir(parents=True, exist_ok=False)
    (rejected / SCRIPT.name).write_bytes(SCRIPT.read_bytes())
    for name in ("native-executable-identity.json", "restrictive-launch-policy.json"):
        (rejected / SNAPSHOT / name).write_bytes((ROOT / SNAPSHOT / name).read_bytes())
    (rejected / FIXTURE).parent.mkdir(parents=True)
    (rejected / FIXTURE).write_bytes((ROOT / FIXTURE).read_bytes())
    (rejected / SNAPSHOT / "restrictive-launch-policy.json").write_text('{"argv": []}\n', encoding="utf-8")
    result = record("green-rejected-policy", invoke(PS7, rejected / SCRIPT.name))
    assert result.returncode != 0
    assert b"launch policy SHA256 mismatch" in result.stderr
    checks.append({"case": "reject-changed-policy-before-launch", "result": "PASS"})
    summary = {"checks": checks, "native_codex_launches": 0, "native_launch_and_ctrl_c": "NOT_RUN",
               "script_sha256": hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
               "scope": "Manual diagnostic helper; no framework acceptance"}
    (RUN / "verification.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    {"red": red, "green": green}[sys.argv[1]]()
