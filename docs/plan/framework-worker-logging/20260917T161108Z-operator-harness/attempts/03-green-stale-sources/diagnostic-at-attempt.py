"""Operator diagnostic support; Rust retains admission and inspection authority."""
import json
import os
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
TRIAL = HERE.parent
sys.path.insert(0, str(TRIAL))
from supervisor import binding, capture, write_new


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)


def selected_config():
    return read_json(HERE / "configuration.json")


def verify_preservation(config=None):
    """Check preserved evidence and the selected live inventory independently."""
    config = selected_config() if config is None else config
    checked = {}

    def check(expected):
        path = str(expected["path"])
        if path not in checked:
            checked[path] = binding(path)
        actual = checked[path]
        require(actual["sha256"] == expected["sha256"], "binding_drift: " + path)
        require("bytes" not in expected or actual["bytes"] == expected["bytes"], "size_drift: " + path)

    for group in config["preserved_manifests"]:
        check(group["binding"])
        document = read_json(group["binding"]["path"])
        for selector in group["selectors"]:
            rows = document
            for key in selector:
                rows = rows[key]
            if isinstance(rows, dict):
                rows = rows.values()
            for expected in rows:
                check(expected)
        if isinstance(document, dict):
            for link in document.get("reparse_points", []):
                require(os.readlink(link["path"]).removeprefix("\\\\?\\") == link["target"].removeprefix("\\\\?\\"), "retained_reparse_drift")
    for expected in config["extra_bindings"]:
        check(expected)
    for link in config["junctions"]:
        require(os.lstat(link["path"]).st_reparse_tag == 0xA0000003, "junction_tag_drift")
        require(os.readlink(link["path"]).removeprefix("\\\\?\\") == link["target"].removeprefix("\\\\?\\"), "junction_target_drift")
    check(config["approved_inventory"])
    inventory = read_json(config["approved_inventory"]["path"])
    current = [row for row in inventory["entries"] if row["state"] == "file"]
    for expected in current:
        check(expected)
    fixture = Path(config["request"]["checkout_root"])
    require(sorted(path.name for path in fixture.iterdir()) == ["task.json"], "fixture_membership_changed")
    check(config["fixture"])
    return {"unique_files_hashed": len(checked), "current_reviewed_files_hashed": len(current),
            "approved_inventory": config["approved_inventory"], "framework_acceptance": "NOT_EVALUATED"}
