"""Resolve the frozen first-party line denominator from raw llvm-cov JSON."""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path
import re


getcontext().prec = 40


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage-json", type=Path, required=True)
    parser.add_argument("--package-root", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--candidate-manifest-sha256", required=True)
    parser.add_argument("--profraw-root", type=Path, required=True)
    args = parser.parse_args()

    coverage_path = args.coverage_json.resolve(strict=True)
    package_root = args.package_root.resolve(strict=True)
    manifest_path = args.candidate_manifest.resolve(strict=True)
    if sha256(manifest_path) != args.candidate_manifest_sha256:
        raise SystemExit("candidate manifest digest mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected: dict[Path, str] = {}
    for item in manifest:
        path = Path(item["path"]).resolve(strict=True)
        if path.suffix == ".rs" and path.is_relative_to(package_root / "src"):
            expected[path] = path.relative_to(package_root).as_posix()
    live_source = {path.resolve(strict=True) for path in (package_root / "src").rglob("*.rs")}
    if set(expected) != live_source:
        raise SystemExit("frozen manifest source inventory differs from live src/**/*.rs")

    payload = json.loads(coverage_path.read_text(encoding="utf-8"))
    if payload.get("type") != "llvm.coverage.json.export" or len(payload.get("data", [])) != 1:
        raise SystemExit("unexpected llvm-cov JSON envelope")
    observed: dict[Path, dict[str, object]] = {}
    out_of_scope: list[str] = []
    unexpected_source: list[str] = []
    for entry in payload["data"][0]["files"]:
        path = Path(entry["filename"]).resolve(strict=True)
        if path in expected:
            if path in observed:
                raise SystemExit(f"duplicate coverage source: {path}")
            observed[path] = entry
        elif path.is_relative_to(package_root / "src"):
            unexpected_source.append(str(path))
        else:
            out_of_scope.append(str(path))
    if unexpected_source:
        raise SystemExit(f"unexpected first-party source in coverage JSON: {unexpected_source}")
    missing_paths = sorted(set(expected) - set(observed), key=lambda path: expected[path])
    zero_executable_sources: list[str] = []
    for path in missing_paths:
        meaningful = [
            line.strip()
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("//")
        ]
        if not meaningful or any(
            re.fullmatch(r"pub mod [a-z][a-z0-9_]*;", line) is None
            for line in meaningful
        ):
            raise SystemExit(f"declared executable source absent from coverage JSON: {path}")
        zero_executable_sources.append(expected[path])

    files: list[dict[str, object]] = []
    covered_total = 0
    count_total = 0
    branch_covered_total = 0
    branch_count_total = 0
    for path, relative in sorted(expected.items(), key=lambda pair: pair[1]):
        if path not in observed:
            files.append(
                {
                    "path": relative,
                    "sha256": sha256(path),
                    "covered_lines": 0,
                    "executable_lines": 0,
                    "line_percent": "100",
                    "covered_branches": 0,
                    "branches": 0,
                }
            )
            continue
        entry = observed[path]
        line_summary = entry["summary"]["lines"]
        branch_summary = entry["summary"]["branches"]
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
                "sha256": sha256(path),
                "covered_lines": covered,
                "executable_lines": count,
                "line_percent": str(
                    Decimal(100) if count == 0 else Decimal(covered) * Decimal(100) / Decimal(count)
                ),
                "covered_branches": branch_covered,
                "branches": branch_count,
            }
        )
    if count_total == 0:
        raise SystemExit("zero executable-line denominator")
    line_percent = Decimal(covered_total) * Decimal(100) / Decimal(count_total)
    profraw_root = args.profraw_root.resolve(strict=True)
    profraw_files = sorted(profraw_root.rglob("*.profraw"))
    profraw = [
        {
            "path": path.relative_to(profraw_root).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in profraw_files
    ]
    result = {
        "schema_version": 1,
        "collector_format": payload["type"],
        "collector_format_version": payload.get("version"),
        "coverage_json": str(coverage_path),
        "coverage_json_sha256": sha256(coverage_path),
        "candidate_manifest": str(manifest_path),
        "candidate_manifest_sha256": sha256(manifest_path),
        "declared_source_file_count": len(expected),
        "reported_source_file_count": len(observed),
        "zero_executable_source_files": zero_executable_sources,
        "first_party_exclusions": [],
        "out_of_scope_reported_file_count": len(set(out_of_scope)),
        "out_of_scope_reported_files": sorted(set(out_of_scope)),
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
        "profraw_bytes": sum(int(item["bytes"]) for item in profraw),
        "profraw": profraw,
    }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0 if line_percent >= Decimal(95) else 1


if __name__ == "__main__":
    raise SystemExit(main())
