#!/usr/bin/env python3
"""Resolve the frozen first-party coverage denominator from llvm-cov JSON."""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path


SOURCE_FILES = [
    "src/effective_profile.rs",
    "src/journal.rs",
    "src/launch_policy.rs",
    "src/lib.rs",
    "src/main.rs",
    "src/native_identity.rs",
    "src/oracle.rs",
    "src/process_windows.rs",
    "src/profile_sources.rs",
    "src/protocol.rs",
    "src/request.rs",
    "src/runner.rs",
]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-json", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--profraw-root", type=Path, required=True)
    args = parser.parse_args()

    coverage_path = args.coverage_json.resolve(strict=True)
    package_root = args.package_root.resolve(strict=True)
    expected = {(package_root / relative).resolve(strict=True): relative for relative in SOURCE_FILES}
    payload = json.loads(coverage_path.read_text(encoding="utf-8"))
    if payload.get("type") != "llvm.coverage.json.export" or len(payload.get("data", [])) != 1:
        raise SystemExit("unexpected llvm-cov JSON envelope")

    observed: dict[Path, dict[str, object]] = {}
    unexpected: list[str] = []
    for entry in payload["data"][0]["files"]:
        path = Path(entry["filename"]).resolve(strict=True)
        if path not in expected:
            unexpected.append(str(path))
            continue
        if path in observed:
            raise SystemExit(f"duplicate coverage file: {path}")
        observed[path] = entry
    if unexpected:
        raise SystemExit(f"unexpected files in first-party coverage JSON: {unexpected}")

    files: list[dict[str, object]] = []
    covered_total = 0
    count_total = 0
    branch_covered_total = 0
    branch_count_total = 0
    for path, relative in expected.items():
        entry = observed.get(path)
        line_summary = entry["summary"]["lines"] if entry is not None else {"covered": 0, "count": 0}
        branch_summary = entry["summary"]["branches"] if entry is not None else {"covered": 0, "count": 0}
        covered = int(line_summary["covered"])
        count = int(line_summary["count"])
        branch_covered = int(branch_summary["covered"])
        branch_count = int(branch_summary["count"])
        covered_total += covered
        count_total += count
        branch_covered_total += branch_covered
        branch_count_total += branch_count
        files.append(
            {
                "path": relative,
                "sha256": digest(path),
                "covered_lines": covered,
                "executable_lines": count,
                "line_percent": str((Decimal(covered) * Decimal(100) / Decimal(count)) if count else Decimal(100)),
                "covered_branches": branch_covered,
                "branches": branch_count,
                "present_in_llvm_json": entry is not None,
            }
        )

    getcontext().prec = 28
    line_percent = Decimal(covered_total) * Decimal(100) / Decimal(count_total)
    profraw_root = args.profraw_root.resolve(strict=True)
    profraw_files = sorted(profraw_root.rglob("*.profraw"))
    profraw = [
        {"path": path.relative_to(profraw_root).as_posix(), "bytes": path.stat().st_size, "sha256": digest(path)}
        for path in profraw_files
    ]
    result = {
        "schema_version": 1,
        "collector_format": payload["type"],
        "collector_format_version": payload.get("version"),
        "coverage_json": str(coverage_path),
        "coverage_json_sha256": digest(coverage_path),
        "declared_source_file_count": len(SOURCE_FILES),
        "reported_source_file_count": len(observed),
        "first_party_exclusions": [],
        "files": files,
        "covered_lines": covered_total,
        "executable_lines": count_total,
        "line_percent": str(line_percent),
        "threshold_percent": "95",
        "threshold_status": "PASS" if line_percent >= Decimal(95) else "FAIL",
        "covered_branches": branch_covered_total,
        "branches": branch_count_total,
        "branch_status": "NOT_RUN" if branch_count_total == 0 else "MEASURED",
        "profraw_root": str(profraw_root),
        "profraw_count": len(profraw),
        "profraw_bytes": sum(item["bytes"] for item in profraw),
        "profraw": profraw,
    }
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
