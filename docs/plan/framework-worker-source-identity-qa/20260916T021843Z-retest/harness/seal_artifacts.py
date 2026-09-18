"""Create the final external QA artifact index exactly once."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def included(relative: Path) -> bool:
    parts = relative.parts
    if not parts:
        return False
    if parts[0] == "artifact-index.json" or parts[0].startswith("target-"):
        return False
    if parts[:2] == ("harness", "packages") or "__pycache__" in parts:
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    output = args.output.resolve(strict=False)
    if output.exists():
        raise SystemExit("artifact index already exists")
    if output.parent != root:
        raise SystemExit("artifact index must be written at the QA root")

    entries = []
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().casefold()):
        relative = path.relative_to(root)
        if not included(relative):
            continue
        stat = path.lstat()
        attributes = int(getattr(stat, "st_file_attributes", 0))
        if attributes & 0x400:
            entries.append(
                {
                    "path": relative.as_posix(),
                    "kind": "reparse",
                    "file_attributes": attributes,
                    "reparse_tag": int(getattr(stat, "st_reparse_tag", 0)),
                    "target": os.readlink(path),
                }
            )
        elif path.is_file():
            entries.append(
                {
                    "path": relative.as_posix(),
                    "kind": "file",
                    "bytes": stat.st_size,
                    "sha256": sha256(path),
                }
            )
    document = {
        "schema_version": 1,
        "root": str(root),
        "excluded_generated_prefixes": ["target-*", "harness/packages", "__pycache__"],
        "binding_note": "Copied Rust package trees are bound by frozen manifests and QA delta records; generated build targets are excluded.",
        "entry_count": len(entries),
        "entries": entries,
    }
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    descriptor = os.open(output, flags)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(document, stream, ensure_ascii=True, indent=2)
            stream.write("\n")
    except BaseException:
        output.unlink(missing_ok=True)
        raise
    print(json.dumps({"output": str(output), "entry_count": len(entries)}, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
