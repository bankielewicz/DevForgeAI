"""Prepare and verify the one-line user-config correction without logging values."""
import copy
import hashlib
import json
import sys
from pathlib import Path

import tomli

RUN = Path(__file__).resolve().parent
CONFIG = Path(r"C:\Users\bryan\.codex\config.toml")
BACKUP = CONFIG.with_name("config.toml.before-history-notify-fix-20260916T231141Z.bak")
EXPECTED = "96cd4027e5007bebca8a3237603fd096342091307b7c44a8a4a8a7e1046d76c1"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def proposal(original):
    assert sha(original) == EXPECTED, "Config changed; do not apply the prepared correction"
    parsed = tomli.loads(original.decode("utf-8-sig"))
    assert isinstance(parsed["notify"], list) and all(isinstance(v, str) for v in parsed["notify"])
    assert "notify" in parsed["history"], "Reported invalid field is absent"
    lines = original.splitlines(keepends=True)
    assert lines[77].strip() == b"[history]"
    assert lines[89].lstrip().startswith(b"notify =")
    start = sum(map(len, lines[:89]))
    removed = len(lines[89])
    corrected = original[:start] + original[start + removed:]
    expected = copy.deepcopy(parsed)
    del expected["history"]["notify"]
    actual = tomli.loads(corrected.decode("utf-8-sig"))
    assert actual == expected, "Unexpected semantic change"
    assert actual["notify"] == parsed["notify"], "Root notifier changed"
    return corrected, start, removed


def write(name, value):
    with (RUN / name).open("x", encoding="utf-8") as output:
        json.dump(value, output, indent=2)
        output.write("\n")


def prepare():
    original = CONFIG.read_bytes()
    corrected, start, removed = proposal(original)
    plan = {"config": str(CONFIG), "backup": str(BACKUP), "before_sha256": sha(original),
            "after_sha256": sha(corrected), "remove_byte_offset": start, "remove_byte_length": removed,
            "removed_original_line": 90, "top_level_notify_unchanged": True,
            "all_other_parsed_values_unchanged": True, "remaining_bytes_unchanged": True,
            "native_launches": 0}
    write("prepared-change.json", plan)
    print(json.dumps(plan, indent=2))


def verify():
    plan = json.loads((RUN / "prepared-change.json").read_text(encoding="utf-8"))
    original = BACKUP.read_bytes()
    expected, _, _ = proposal(original)
    current = CONFIG.read_bytes()
    assert current == expected and sha(current) == plan["after_sha256"]
    result = {"backup_sha256": sha(original), "config_sha256": sha(current),
              "toml_parse": "PASS", "history_notify_removed": True,
              "top_level_notify_unchanged": True, "all_other_bytes_unchanged": True,
              "native_launches": 0, "native_startup": "NOT_RETESTED"}
    write("verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    {"prepare": prepare, "verify": verify}[sys.argv[1]]()
