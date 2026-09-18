"""Bind the QA-only Rust test delta from the exact frozen package snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--snapshot", required=True, type=Path)
    parser.add_argument("--allowed-change", action="append", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve(strict=True)
    candidate = args.candidate.resolve(strict=True)
    snapshot = args.snapshot.resolve(strict=True)
    expected_entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {entry["path"]: entry for entry in expected_entries}
    allowed = set(args.allowed_change)
    if len(allowed) != len(args.allowed_change):
        raise SystemExit("duplicate allowed-change argument")

    candidate_mismatches: list[str] = []
    snapshot_unexpected: list[str] = []
    observed_changes: list[dict[str, object]] = []
    snapshot_paths = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*")
        if path.is_file()
    }
    if snapshot_paths != set(expected):
        snapshot_unexpected = sorted(snapshot_paths.symmetric_difference(set(expected)))

    for relative, entry in expected.items():
        candidate_path = candidate / Path(relative)
        snapshot_path = snapshot / Path(relative)
        if (
            not candidate_path.is_file()
            or candidate_path.stat().st_size != entry["bytes"]
            or sha256(candidate_path) != entry["sha256"]
        ):
            candidate_mismatches.append(relative)
            continue
        if not snapshot_path.is_file():
            continue
        snapshot_hash = sha256(snapshot_path)
        changed = (
            snapshot_path.stat().st_size != entry["bytes"]
            or snapshot_hash != entry["sha256"]
        )
        if changed:
            observed_changes.append(
                {
                    "path": relative,
                    "original_bytes": entry["bytes"],
                    "original_sha256": entry["sha256"],
                    "qa_bytes": snapshot_path.stat().st_size,
                    "qa_sha256": snapshot_hash,
                }
            )

    observed = {entry["path"] for entry in observed_changes}
    result = {
        "schema_version": 1,
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "candidate": str(candidate),
        "snapshot": str(snapshot),
        "candidate_mismatches": candidate_mismatches,
        "snapshot_file_set_differences": snapshot_unexpected,
        "allowed_changes": sorted(allowed),
        "observed_changes": observed_changes,
        "exact_allowed_delta": (
            not candidate_mismatches
            and not snapshot_unexpected
            and observed == allowed
        ),
    }
    output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["exact_allowed_delta"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
