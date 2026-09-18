"""Copy exactly the regular files named by the frozen candidate manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
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
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()

    manifest_path = args.manifest.resolve(strict=True)
    candidate = args.candidate.resolve(strict=True)
    destination = args.destination.resolve(strict=False)
    if destination.exists():
        raise SystemExit("destination already exists")
    entries = json.loads(manifest_path.read_text(encoding="utf-8"))
    if len(entries) != 56 or any(entry.get("kind") != "file" for entry in entries):
        raise SystemExit("unexpected frozen manifest shape")

    copied: list[dict[str, object]] = []
    for entry in entries:
        relative = Path(entry["path"])
        source = candidate / relative
        if (
            not source.is_file()
            or source.stat().st_size != entry["bytes"]
            or sha256(source) != entry["sha256"]
        ):
            raise SystemExit(f"candidate identity mismatch: {entry['path']}")
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if target.stat().st_size != entry["bytes"] or sha256(target) != entry["sha256"]:
            raise SystemExit(f"copy identity mismatch: {entry['path']}")
        copied.append({"path": entry["path"], "bytes": entry["bytes"], "sha256": entry["sha256"]})

    print(
        json.dumps(
            {
                "schema_version": 1,
                "manifest": str(manifest_path),
                "manifest_sha256": sha256(manifest_path),
                "candidate": str(candidate),
                "destination": str(destination),
                "copied_files": copied,
                "copied_count": len(copied),
            },
            ensure_ascii=True,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
