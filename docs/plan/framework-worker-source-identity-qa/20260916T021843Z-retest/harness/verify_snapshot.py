"""Verify the frozen QA package copy against the selected candidate manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--snapshot", required=True, type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve(strict=True)
    candidate = args.candidate.resolve(strict=True)
    snapshot = args.snapshot.resolve(strict=True)
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))

    mismatches: list[dict[str, object]] = []
    expected_paths = {entry["path"] for entry in expected}
    for entry in expected:
        relative = entry["path"]
        if entry["kind"] != "file":
            mismatches.append({"path": relative, "reason": "non_file_manifest_entry"})
            continue
        for role, root in (("candidate", candidate), ("snapshot", snapshot)):
            path = root / Path(relative)
            if not path.is_file():
                mismatches.append({"path": relative, "role": role, "reason": "missing"})
                continue
            if path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
                mismatches.append({"path": relative, "role": role, "reason": "identity_mismatch"})

    snapshot_paths = {
        path.relative_to(snapshot).as_posix()
        for path in snapshot.rglob("*")
        if path.is_file()
    }
    extras = sorted(snapshot_paths - expected_paths)
    missing = sorted(expected_paths - snapshot_paths)
    result = {
        "schema_version": 1,
        "manifest": str(manifest_path),
        "manifest_sha256": sha256(manifest_path),
        "candidate": str(candidate),
        "snapshot": str(snapshot),
        "expected_files": len(expected),
        "snapshot_files": len(snapshot_paths),
        "mismatches": mismatches,
        "snapshot_extra_files": extras,
        "snapshot_missing_files": missing,
        "exact_match": not mismatches and not extras and not missing,
    }
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if result["exact_match"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
