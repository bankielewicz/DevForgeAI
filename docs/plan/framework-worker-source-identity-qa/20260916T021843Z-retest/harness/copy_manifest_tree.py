"""Copy the current bytes at exactly the paths named by a frozen manifest."""

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
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    args = parser.parse_args()

    manifest = json.loads(args.manifest.resolve(strict=True).read_text(encoding="utf-8"))
    source = args.source.resolve(strict=True)
    destination = args.destination.resolve(strict=False)
    if destination.exists():
        raise SystemExit("destination already exists")
    expected = {entry["path"] for entry in manifest}
    actual = {
        path.relative_to(source).as_posix()
        for path in source.rglob("*")
        if path.is_file()
    }
    if actual != expected:
        raise SystemExit("source file set differs from frozen manifest")

    copied = []
    for relative_text in sorted(expected):
        relative = Path(relative_text)
        source_path = source / relative
        destination_path = destination / relative
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, destination_path)
        source_hash = sha256(source_path)
        destination_hash = sha256(destination_path)
        if source_hash != destination_hash:
            raise SystemExit(f"copy identity mismatch: {relative_text}")
        copied.append(
            {
                "path": relative_text,
                "bytes": destination_path.stat().st_size,
                "sha256": destination_hash,
            }
        )
    print(json.dumps({"schema_version": 1, "copied_count": len(copied), "files": copied}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
