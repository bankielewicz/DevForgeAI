"""Read-only audit of the developer-frozen candidate and selected inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path


REPARSE_ATTRIBUTE = 0x400


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def files_without_reparse(root: Path, excluded_root_name: str | None) -> list[Path]:
    files: list[Path] = []

    def visit(directory: Path) -> None:
        with os.scandir(directory) as scan:
            children = sorted(scan, key=lambda item: item.name.casefold())
        for child in children:
            path = Path(child.path)
            stat = child.stat(follow_symlinks=False)
            attributes = int(getattr(stat, "st_file_attributes", 0))
            if attributes & REPARSE_ATTRIBUTE:
                raise RuntimeError(f"unexpected reparse: {path}")
            if child.is_dir(follow_symlinks=False):
                if directory == root and excluded_root_name and child.name == excluded_root_name:
                    continue
                visit(path)
            elif child.is_file(follow_symlinks=False):
                files.append(path)

    visit(root)
    return files


def parse_binding(value: str) -> tuple[Path, str]:
    path_text, separator, digest = value.rpartition("::")
    if not separator:
        raise argparse.ArgumentTypeError("binding must be ABSOLUTE_PATH::LOWERCASE_SHA256")
    path = Path(path_text)
    if not path.is_absolute() or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise argparse.ArgumentTypeError("invalid binding")
    return path, digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--candidate-manifest-sha256", required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    parser.add_argument("--binding", action="append", type=parse_binding, default=[])
    args = parser.parse_args()

    package = args.package.resolve(strict=True)
    manifest_path = args.candidate_manifest.resolve(strict=True)
    snapshot = args.snapshot.resolve(strict=True)
    errors: list[str] = []
    if sha256(manifest_path) != args.candidate_manifest_sha256:
        errors.append("candidate manifest digest mismatch")
    for path, expected in args.binding:
        resolved = path.resolve(strict=True)
        actual = sha256(resolved)
        if actual != expected:
            errors.append(f"binding mismatch: {resolved}: {actual}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, list):
        raise SystemExit("candidate manifest must be an array")
    manifest_map: dict[Path, dict[str, object]] = {}
    for entry in manifest:
        path = Path(entry["path"]).resolve(strict=False)
        if not path.is_relative_to(package):
            errors.append(f"manifest path outside package: {path}")
            continue
        if path in manifest_map:
            errors.append(f"duplicate manifest path: {path}")
            continue
        manifest_map[path] = entry

    live_files = files_without_reparse(package, "target")
    if set(live_files) != set(manifest_map):
        errors.append(
            "live inventory differs: "
            + json.dumps(
                {
                    "missing": sorted(str(path) for path in set(manifest_map) - set(live_files)),
                    "extra": sorted(str(path) for path in set(live_files) - set(manifest_map)),
                },
                sort_keys=True,
            )
        )

    live_matches = 0
    snapshot_matches = 0
    for path, entry in manifest_map.items():
        if path.is_file() and path.stat().st_size == int(entry["bytes"]) and sha256(path) == entry["sha256"]:
            live_matches += 1
        else:
            errors.append(f"live bytes differ: {path}")
        snap = snapshot / path.relative_to(package)
        if snap.is_file() and snap.stat().st_size == int(entry["bytes"]) and sha256(snap) == entry["sha256"]:
            snapshot_matches += 1
        else:
            errors.append(f"snapshot bytes differ: {snap}")

    snapshot_files = files_without_reparse(snapshot, None)
    expected_snapshot = {snapshot / path.relative_to(package) for path in manifest_map}
    if set(snapshot_files) != expected_snapshot:
        errors.append("snapshot inventory differs from candidate manifest")

    result = {
        "schema_version": 1,
        "candidate_manifest": str(manifest_path),
        "candidate_manifest_sha256": sha256(manifest_path),
        "manifest_entries": len(manifest),
        "live_file_count": len(live_files),
        "live_matches": live_matches,
        "snapshot_file_count": len(snapshot_files),
        "snapshot_matches": snapshot_matches,
        "input_bindings_checked": len(args.binding),
        "errors": errors,
        "status": "PASS" if not errors else "FAIL",
    }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

