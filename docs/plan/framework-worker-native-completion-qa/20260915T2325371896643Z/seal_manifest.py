#!/usr/bin/env python3
"""Create the non-circular immutable index for delivered QA evidence."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "artifact-manifest.json"
EXCLUDED_TREES = {"target", "target-clippy"}


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.as_posix() == OUTPUT.name:
        return False
    if relative.parts[0] in EXCLUDED_TREES:
        return False
    if relative.parts[0] == "target-coverage":
        return path.suffix == ".profraw"
    return True


def main() -> int:
    entries = []
    for path in sorted((item for item in ROOT.rglob("*") if item.is_file() and included(item)), key=lambda item: item.relative_to(ROOT).as_posix()):
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    manifest = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_root": str(ROOT),
        "candidate_manifest_sha256": "809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd",
        "self_exclusion": "artifact-manifest.json is excluded to avoid a circular digest",
        "build_tree_exclusions": [
            "target/ disposable non-coverage Cargo outputs",
            "target-clippy/ disposable Clippy Cargo outputs",
            "target-coverage/ non-profraw Cargo outputs; all .profraw files are included",
        ],
        "entry_count": len(entries),
        "entries": entries,
    }
    OUTPUT.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
