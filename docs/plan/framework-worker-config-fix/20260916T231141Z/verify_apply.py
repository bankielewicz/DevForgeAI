"""Exercise the exact edit algorithm on two harmless workspace fixtures."""
import hashlib
import json
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
PS7 = r"C:\Program Files\PowerShell\7\pwsh.exe"
source = (RUN / "apply_notify.ps1").read_text(encoding="utf-8")
original = b'notify = ["root-notifier"]\r\n[history]\r\npersistence = "save-all"\r\nnotify = ["ignored-notifier"]\r\n'
removed = b'notify = ["ignored-notifier"]\r\n'
expected = original[:-len(removed)]
sha = lambda data: hashlib.sha256(data).hexdigest()
results = []
for name, stale in (("valid-edit", False), ("refuse-stale-input", True)):
    case = RUN / name
    case.mkdir(exist_ok=False)
    config, backup = case / "config.toml", case / "config.toml.bak"
    script = source.replace(r"C:\Users\bryan\.codex\config.toml.before-history-notify-fix-20260916T231141Z.bak", str(backup))
    script = script.replace(r"C:\Users\bryan\.codex\config.toml", str(config))
    assert str(config.resolve()).startswith(str(RUN) + "\\")
    (case / "apply_notify.ps1").write_text(script, encoding="utf-8")
    actual_before = original + (b"# concurrent change\r\n" if stale else b"")
    config.write_bytes(actual_before)
    plan = {"config": str(config), "backup": str(backup), "before_sha256": sha(original),
            "after_sha256": sha(expected), "remove_byte_offset": len(expected), "remove_byte_length": len(removed)}
    (case / "prepared-change.json").write_text(json.dumps(plan), encoding="utf-8")
    command = [PS7, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(case / "apply_notify.ps1")]
    result = subprocess.run(command, capture_output=True, timeout=30)
    (case / "stdout.bin").write_bytes(result.stdout)
    (case / "stderr.bin").write_bytes(result.stderr)
    if stale:
        assert result.returncode != 0 and config.read_bytes() == actual_before and not backup.exists()
        assert b"Config changed since preparation" in result.stderr
    else:
        assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
        assert config.read_bytes() == expected and backup.read_bytes() == original
    results.append({"case": name, "exit_code": result.returncode, "assertions": "PASS", "argv": command})
(RUN / "edit-algorithm-checks.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print(json.dumps(results, indent=2))
