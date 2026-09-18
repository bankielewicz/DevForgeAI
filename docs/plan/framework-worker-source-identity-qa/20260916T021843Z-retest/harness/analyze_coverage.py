"""Independently reconcile LLVM line coverage to the frozen source manifest."""

from __future__ import annotations

import argparse
from decimal import Decimal, getcontext
import hashlib
import json
from pathlib import Path
import re
import sys


getcontext().prec = 80


def sha256(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def declaration_only(path: Path) -> bool:
    module = re.compile(r"pub\s+mod\s+[A-Za-z_][A-Za-z0-9_]*\s*;\s*$")
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("//!") or module.fullmatch(stripped):
            continue
        return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coverage", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--source-denominator", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    coverage_path = args.coverage.resolve(strict=True)
    candidate = args.candidate.resolve(strict=True)
    denominator = json.loads(args.source_denominator.read_text(encoding="utf-8"))
    coverage = json.loads(coverage_path.read_text(encoding="utf-8"))
    if len(coverage.get("data", [])) != 1:
        raise SystemExit("expected exactly one LLVM data object")

    expected: dict[str, dict[str, object]] = {}
    for entry in denominator["files"]:
        relative = entry["path"].replace("\\", "/")
        path = candidate / Path(relative)
        if not path.is_file() or path.stat().st_size != entry["bytes"] or sha256(path) != entry["sha256"]:
            raise SystemExit(f"frozen source mismatch: {relative}")
        expected[str(path).lower()] = {"relative": relative, "path": path, "entry": entry}

    observed: dict[str, dict[str, int]] = {}
    unexpected = []
    for file_record in coverage["data"][0].get("files", []):
        filename = str(Path(file_record["filename"]).resolve()).lower()
        try:
            filename_path = Path(file_record["filename"]).resolve()
            filename_path.relative_to(candidate)
        except ValueError:
            continue
        if filename not in expected:
            unexpected.append(str(filename_path))
            continue
        lines = file_record["summary"]["lines"]
        if filename in observed:
            raise SystemExit(f"duplicate LLVM file record: {filename_path}")
        observed[filename] = {"covered": int(lines["covered"]), "count": int(lines["count"])}
    if unexpected:
        raise SystemExit("unexpected first-party source in LLVM JSON: " + ", ".join(unexpected))

    rows = []
    covered_total = 0
    count_total = 0
    for key, item in sorted(expected.items(), key=lambda pair: str(pair[1]["relative"])):
        path = item["path"]
        if key in observed:
            covered = observed[key]["covered"]
            count = observed[key]["count"]
        elif declaration_only(path):
            covered = 0
            count = 0
        else:
            raise SystemExit(f"executable source omitted from LLVM JSON: {item['relative']}")
        if covered < 0 or count < 0 or covered > count:
            raise SystemExit(f"invalid line counts: {item['relative']}")
        covered_total += covered
        count_total += count
        rows.append({"path": item["relative"], "covered": covered, "count": count})
    if count_total == 0:
        raise SystemExit("zero executable-line denominator")

    percent = Decimal(covered_total) * Decimal(100) / Decimal(count_total)
    result = {
        "schema_version": 1,
        "coverage_json": str(coverage_path),
        "coverage_json_sha256": sha256(coverage_path),
        "candidate": str(candidate),
        "source_files": len(rows),
        "first_party_exclusions": [],
        "executed_lines": covered_total,
        "executable_lines": count_total,
        "percent": format(percent, "f"),
        "required_percent": "95",
        "passes_floor": percent >= Decimal(95),
        "files": rows,
    }
    output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(output, encoding="utf-8")
    sys.stdout.write(output)
    return 0 if result["passes_floor"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
