"""Final immutable-input, installed-mapping, and QA-binary readback."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


REPARSE_ATTRIBUTE = 0x400
EXTENDED_PREFIX = "\\\\?\\"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def candidate_files(root: Path) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if relative == "target" or relative.startswith("target/"):
            continue
        stat = path.lstat()
        if int(getattr(stat, "st_file_attributes", 0)) & REPARSE_ATTRIBUTE:
            result[relative] = {"kind": "reparse"}
        elif path.is_file():
            result[relative] = {
                "kind": "file",
                "bytes": stat.st_size,
                "sha256": sha256(path),
            }
    return result


def normalize_target(value: str) -> str:
    return value[len(EXTENDED_PREFIX) :] if value.startswith(EXTENDED_PREFIX) else value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--qa-root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve(strict=True)
    qa_root = args.qa_root.resolve(strict=True)
    freeze_path = qa_root / "freeze-bindings.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    manifest_path = Path(freeze["candidate_manifest"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate = Path(freeze["candidate_root"]).resolve(strict=True)
    expected = {
        entry["path"]: {
            "kind": entry["kind"],
            **({"bytes": entry["bytes"], "sha256": entry["sha256"]} if entry["kind"] == "file" else {}),
        }
        for entry in manifest
    }
    actual = candidate_files(candidate)
    candidate_exact = actual == expected

    specification_results = []
    for specification in freeze["specifications"]:
        path = workspace / specification["path"]
        observed = sha256(path)
        specification_results.append(
            {
                "path": str(path.resolve(strict=True)),
                "expected_sha256": specification["sha256"],
                "observed_sha256": observed,
                "unchanged": observed == specification["sha256"],
            }
        )

    record_path = candidate / "src" / "plugin-source-identity.json"
    record = json.loads(record_path.read_text(encoding="utf-8"))
    if len(record.get("junctions", [])) != 1:
        raise SystemExit("compiled source-identity record is not singular")
    mapping = record["junctions"][0]
    logical = Path(mapping["path"])
    physical = Path(mapping["target"])
    logical_stat = logical.lstat()
    observed_target_raw = os.readlink(logical)
    observed_target = normalize_target(observed_target_raw)
    installed = {
        "logical_path": str(logical),
        "compiled_target": str(physical),
        "compiled_reparse_tag": mapping["reparse_tag"],
        "observed_target_raw": observed_target_raw,
        "observed_target_normalized": observed_target,
        "observed_reparse_tag": int(getattr(logical_stat, "st_reparse_tag", 0)),
        "observed_attributes": int(getattr(logical_stat, "st_file_attributes", 0)),
        "physical_target_is_directory": physical.is_dir(),
        "exact_selected_mapping": (
            os.path.normcase(os.path.normpath(observed_target))
            == os.path.normcase(os.path.normpath(str(physical)))
            and int(getattr(logical_stat, "st_reparse_tag", 0)) == mapping["reparse_tag"]
            and physical.is_dir()
        ),
    }

    executable = qa_root / "target-original" / "debug" / "devforgeai-codex-worker-probe.exe"
    retained_attempts = ["01-environment", "02-environment", "13-public-source-identity", "24-frozen-snapshot-readback", "30-matrix-fmt-check", "35-independent-negative-matrix", "47-recovered-attempt35-helper-readback"]
    result = {
        "schema_version": 1,
        "candidate": str(candidate),
        "candidate_manifest": str(manifest_path),
        "candidate_manifest_sha256": sha256(manifest_path),
        "candidate_expected_files": len(expected),
        "candidate_observed_entries": len(actual),
        "candidate_exact": candidate_exact,
        "specifications": specification_results,
        "plugin_source_identity": {
            "path": str(record_path),
            "sha256": sha256(record_path),
            "schema_version": record.get("schema_version"),
            "adapter": record.get("adapter"),
            "junction_count": len(record["junctions"]),
        },
        "installed_mapping_metadata_only": installed,
        "qa_built_original_package_executable": {
            "path": str(executable),
            "bytes": executable.stat().st_size,
            "sha256": sha256(executable),
        },
        "retained_failed_attempts": {
            label: (qa_root / label).is_dir() for label in retained_attempts
        },
        "installed_profile_collected": False,
        "codex_started": False,
    }
    result["pass"] = (
        candidate_exact
        and sha256(manifest_path) == freeze["candidate_manifest_sha256"]
        and all(item["unchanged"] for item in specification_results)
        and installed["exact_selected_mapping"]
        and all(result["retained_failed_attempts"].values())
    )
    output = args.output.resolve(strict=False)
    if output.exists():
        raise SystemExit("output already exists")
    output.write_text(json.dumps(result, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
