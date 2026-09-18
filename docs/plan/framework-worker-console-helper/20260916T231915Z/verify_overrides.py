"""Offline regression for literal quotes in the pinned CLI's dotted override keys.

Runs the manual helper only with -CheckOnly. The replay models the published
0.154.0 path.split('.') behavior; it does not launch or qualify native Codex.
"""
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import tomli

RUN = Path(__file__).resolve().parent
ROOT = Path(r"C:\Projects\DevForgeAI")
SCRIPT = ROOT / "Start-CodexAppServerDiagnostic.ps1"
SNAPSHOT = ROOT / "docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-snapshot"
POLICY = SNAPSHOT / "src/restrictive-launch-policy.json"
PS7 = r"C:\Program Files\PowerShell\7\pwsh.exe"
PS5 = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
POLICY_SHA = "1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5"
CONFIG = Path(r"C:\Users\bryan\.codex\config.toml")
KEY_PATTERN = re.compile(r'^(mcp_servers|plugins|apps)\."([A-Za-z0-9_@-]+)"\.enabled=false$')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2)
        stream.write("\n")


def fixture(argv):
    value = {"mcp_servers": {"node_repl": {"command": "synthetic-node", "args": []},
                             "openaiDeveloperDocs": {"url": "https://example.invalid/mcp"}},
             "apps": {"_default": {"enabled": True}}, "plugins": {}}
    for arg in argv:
        match = KEY_PATTERN.fullmatch(arg)
        if match and match[1] != "mcp_servers":
            value[match[1]][match[2]] = {"enabled": True}
    return value


def replay(argv, initial):
    assert argv[:4] == ["app-server", "--listen", "stdio://", "--strict-config"]
    value = copy.deepcopy(initial)
    for index in range(4, len(argv), 2):
        assert argv[index] == "-c"
        key, raw = argv[index + 1].split("=", 1)
        parsed = tomli.loads("value = " + raw)["value"]
        segments = key.strip().split(".")
        target = value
        for segment in segments[:-1]:
            target = target.setdefault(segment, {})
        target[segments[-1]] = parsed
    return value


def assert_targets(actual, initial):
    for category in ("mcp_servers", "plugins", "apps"):
        assert set(actual[category]) == set(initial[category]), f"Unexpected {category} keys"
        assert all(item.get("enabled") is False for item in actual[category].values()), category
    for name, server in actual["mcp_servers"].items():
        assert "command" in server or "url" in server, f"invalid transport: {name!r}"


def check_shell(shell, label):
    case = RUN / label
    case.mkdir(exist_ok=False)
    command = [shell, "-NoLogo", "-NoProfile", "-NonInteractive", "-File", str(SCRIPT), "-CheckOnly"]
    result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=60)
    (case / "stdout.bin").write_bytes(result.stdout)
    (case / "stderr.bin").write_bytes(result.stderr)
    write(case / "receipt.json", {"argv": command, "cwd": str(ROOT), "exit_code": result.returncode})
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    data = json.loads(result.stdout.decode("utf-8-sig"))
    assert data["worker_started"] is False and data["argument_count"] == 116
    return data


def main(mode):
    assert sha(POLICY.read_bytes()) == POLICY_SHA
    frozen = json.loads(POLICY.read_bytes())["argv"]
    initial = fixture(frozen)
    config_hash = sha(CONFIG.read_bytes())
    if mode == "red":
        with (RUN / "original-console-helper.ps1").open("xb") as stream:
            stream.write(SCRIPT.read_bytes())
        data = check_shell(PS7, "red")
        actual = replay(data["argv"], initial)
        invalid = [name for name, server in actual["mcp_servers"].items() if "command" not in server and "url" not in server]
        assert invalid == ['"node_repl"', '"openaiDeveloperDocs"']
        try:
            assert_targets(actual, initial)
        except AssertionError as error:
            result = {"status": "EXPECTED_RED", "assertion": str(error), "invalid_transport_names": invalid,
                      "native_codex_launches": 0, "config_sha256": config_hash}
        else:
            raise AssertionError("Expected malformed override failure was not reproduced")
        write(RUN / "red-result.json", result)
        print(json.dumps(result, indent=2))
        return

    expected = [KEY_PATTERN.sub(lambda m: f"{m[1]}.{m[2]}.enabled=false", arg) for arg in frozen]
    changed = [{"index": i, "before": old, "after": new} for i, (old, new) in enumerate(zip(frozen, expected)) if old != new]
    results = []
    for shell, label in ((PS7, "green-ps7"), (PS5, "green-ps51")):
        data = check_shell(shell, label)
        assert data["argv"] == expected
        assert data["manual_override_corrections"] == len(changed)
        actual = replay(data["argv"], initial)
        assert_targets(actual, initial)
        assert actual["model_provider"] == "openai"
        assert actual["forced_login_method"] == "chatgpt"
        assert actual["sandbox_mode"] == "read-only" and actual["approval_policy"] == "never"
        results.append({"case": label, "result": "PASS", "corrections": len(changed)})
    assert sha(CONFIG.read_bytes()) == config_hash and sha(POLICY.read_bytes()) == POLICY_SHA
    # Bind every frozen candidate file in both the development and retained copies.
    manifest = json.loads((SNAPSHOT.parent / "candidate-v2-manifest.json").read_bytes())
    for base in (SNAPSHOT, ROOT / "devforgeai/experiments/codex-worker-probe"):
        for entry in manifest:
            content = (base / entry["path"]).read_bytes()
            assert len(content) == entry["bytes"] and sha(content) == entry["sha256"]
    result = {"cases": results, "changed_arguments": changed, "config_sha256_unchanged": config_hash,
              "frozen_files_verified": 2 * len(manifest), "helper_sha256": sha(SCRIPT.read_bytes()),
              "native_codex_launches": 0, "native_startup": "NOT_RETESTED",
              "scope": "Offline override replay and helper preparation; not framework acceptance"}
    write(RUN / "verification.json", result)
    print(json.dumps({key: value for key, value in result.items() if key != "changed_arguments"}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
