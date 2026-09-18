"""Create a non-circular immutable index of delivered QA evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "artifact-manifest.json"
DISPOSABLE_TREES = {"target", "target-clippy"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def included(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.as_posix() == OUTPUT.name:
        return False
    if relative.parts[0] in DISPOSABLE_TREES:
        return False
    if relative.parts[0] == "target-coverage":
        return path.suffix == ".profraw"
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-manifest-sha256", required=True)
    args = parser.parse_args()
    entries = []
    for path in sorted(
        (item for item in ROOT.rglob("*") if item.is_file() and included(item)),
        key=lambda item: item.relative_to(ROOT).as_posix(),
    ):
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )
    external_entries = []
    external_index = ROOT / "external-fixtures-after.json"
    if external_index.exists():
        external_payload = json.loads(external_index.read_text(encoding="utf-8"))
        external_root = Path(external_payload["root"]).resolve(strict=True)
        for item in external_payload["new_entries"]:
            path = (external_root / item["name"] / item["task"]).resolve(strict=True)
            external_entries.append(
                {
                    "path": str(path),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    payload = {
        "schema_version": 1,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "evidence_root": str(ROOT),
        "candidate_manifest_sha256": args.candidate_manifest_sha256,
        "self_exclusion": "artifact-manifest.json is excluded to avoid a circular digest",
        "build_tree_exclusions": [
            "target/ disposable non-coverage Cargo outputs",
            "target-clippy/ disposable Clippy Cargo outputs",
            "target-coverage/ non-profraw Cargo outputs; all .profraw files are included",
        ],
        "root_entry_count": len(entries),
        "external_entry_count": len(external_entries),
        "entry_count": len(entries) + len(external_entries),
        "entries": entries,
        "external_entries": external_entries,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
