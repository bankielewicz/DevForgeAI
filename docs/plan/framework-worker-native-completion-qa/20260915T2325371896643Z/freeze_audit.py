"""Read-only frozen-candidate identity check for this QA run."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys


WORKSPACE = Path(r"C:\Projects\DevForgeAI")
PACKAGE = WORKSPACE / "devforgeai" / "experiments" / "codex-worker-probe"
DELIVERY = (
    WORKSPACE
    / "docs"
    / "plan"
    / "framework-worker-native-completion"
    / "20260915T2306060954875Z"
)
MANIFEST = DELIVERY / "candidate-manifest.json"
SNAPSHOT = DELIVERY / "candidate-snapshot"
REPARSE_ATTRIBUTE = 0x400
EXPECTED = {
    MANIFEST: "809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd",
    DELIVERY / "inputs-manifest.json": "3fafe784e180b37cabaf8e276c8f324ea464fd568dcfa9a05688a55db9e88288",
    WORKSPACE / "docs/specs/framework/runtime/codex-worker-feasibility-v1.md": "7cb5b0cb87e515bb4d59235b615922ab4ea07ef607b8111dde6cc73c8f101b23",
    WORKSPACE / "docs/specs/framework/runtime/codex-worker-native-readiness-v1.md": "c3c0673cbf95ae7aa056d9fd0009ce89947309b943013fd7838438d6ee66b06d",
    WORKSPACE / "docs/specs/framework/runtime/codex-worker-preflight-v1.md": "6e781f23f221d1033896716512e9162579653b529d107e0040d49c499574afd1",
    WORKSPACE / "AGENTS.md": "d47868fef2b87df0b2c065cfe235cfe9f12fcf9eeffa7af1f0973d7d21916fa7",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def files_without_reparse(root: Path) -> list[Path]:
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
                if path == PACKAGE / "target":
                    continue
                visit(path)
            elif child.is_file(follow_symlinks=False):
                files.append(path)

    visit(root)
    return files


def main() -> int:
    observations: dict[str, object] = {"schema_version": 1, "errors": []}
    errors: list[str] = observations["errors"]  # type: ignore[assignment]
    for path, expected in EXPECTED.items():
        actual = digest(path)
        if actual != expected:
            errors.append(f"identity mismatch: {path}: {actual}")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest_map = {Path(entry["path"]): entry for entry in manifest}
    live_files = files_without_reparse(PACKAGE)
    live_set = set(live_files)
    if len(manifest) != 48:
        errors.append(f"manifest count: {len(manifest)}")
    if live_set != set(manifest_map):
        missing = sorted(str(path) for path in set(manifest_map) - live_set)
        extra = sorted(str(path) for path in live_set - set(manifest_map))
        errors.append(f"live inventory differs: missing={missing} extra={extra}")

    live_matches = 0
    snapshot_matches = 0
    for path, entry in manifest_map.items():
        if not path.is_relative_to(PACKAGE):
            errors.append(f"manifest path outside package: {path}")
            continue
        actual_size = path.stat().st_size
        actual_hash = digest(path)
        if actual_size == entry["bytes"] and actual_hash == entry["sha256"]:
            live_matches += 1
        else:
            errors.append(f"live bytes differ: {path}")
        snapshot = SNAPSHOT / path.relative_to(PACKAGE)
        if (
            snapshot.is_file()
            and snapshot.stat().st_size == entry["bytes"]
            and digest(snapshot) == entry["sha256"]
        ):
            snapshot_matches += 1
        else:
            errors.append(f"snapshot bytes differ: {snapshot}")

    snapshot_files = files_without_reparse(SNAPSHOT)
    expected_snapshot = {SNAPSHOT / path.relative_to(PACKAGE) for path in manifest_map}
    if set(snapshot_files) != expected_snapshot:
        errors.append("snapshot inventory differs from manifest")

    observations.update(
        {
            "manifest_entries": len(manifest),
            "live_file_count": len(live_files),
            "live_matches": live_matches,
            "snapshot_file_count": len(snapshot_files),
            "snapshot_matches": snapshot_matches,
            "input_and_spec_bindings": len(EXPECTED),
            "status": "PASS" if not errors else "FAIL",
        }
    )
    print(json.dumps(observations, sort_keys=True, ensure_ascii=True))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
