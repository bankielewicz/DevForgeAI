"""Reconcile Cargo's listed Rust tests with the frozen physical test inventory."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re


TEST_LINE = re.compile(r"^(.+): test$")
TEST_ATTRIBUTE = re.compile(r"(?m)^\s*#\s*\[\s*test\s*\]\s*$")
IGNORE_ATTRIBUTE = re.compile(r"(?m)^\s*#\s*\[\s*ignore(?:\s*=.*)?\]\s*$")
SHOULD_PANIC_ATTRIBUTE = re.compile(r"(?m)^\s*#\s*\[\s*should_panic(?:\s*\(.*\))?\s*\]\s*$")


def listed(path: Path) -> list[str]:
    names: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TEST_LINE.fullmatch(line.strip())
        if match:
            names.append(match.group(1))
    return names


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-list", required=True, type=Path)
    parser.add_argument("--lib-list", required=True, type=Path)
    parser.add_argument("--package", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    all_tests = listed(args.all_list.resolve(strict=True))
    unit_tests = listed(args.lib_list.resolve(strict=True))
    package = args.package.resolve(strict=True)
    physical: dict[str, int] = {}
    ignored: dict[str, int] = {}
    should_panic: dict[str, int] = {}
    for root in (package / "src", package / "tests"):
        for path in sorted(root.rglob("*.rs")):
            text = path.read_text(encoding="utf-8")
            relative = path.relative_to(package).as_posix()
            count = len(TEST_ATTRIBUTE.findall(text))
            if count:
                physical[relative] = count
            ignore_count = len(IGNORE_ATTRIBUTE.findall(text))
            if ignore_count:
                ignored[relative] = ignore_count
            panic_count = len(SHOULD_PANIC_ATTRIBUTE.findall(text))
            if panic_count:
                should_panic[relative] = panic_count

    duplicates = sorted(name for name, count in Counter(all_tests).items() if count != 1)
    physical_count = sum(physical.values())
    result = {
        "schema_version": 1,
        "all_target_test_count": len(all_tests),
        "required_unit_test_count": len(unit_tests),
        "integration_test_count": len(all_tests) - len(unit_tests),
        "physical_test_attribute_count": physical_count,
        "all_names_unique": not duplicates,
        "duplicate_names": duplicates,
        "unit_names_are_all_target_subset": set(unit_tests).issubset(set(all_tests)),
        "ignored_attributes": ignored,
        "should_panic_attributes": should_panic,
        "physical_tests_by_file": physical,
        "required_unit_tests": unit_tests,
        "all_target_tests": all_tests,
        "reconciled": (
            bool(all_tests)
            and len(all_tests) == physical_count
            and not duplicates
            and set(unit_tests).issubset(set(all_tests))
            and not ignored
            and not should_panic
        ),
    }
    output = json.dumps(result, ensure_ascii=True, indent=2) + "\n"
    args.output.write_text(output, encoding="utf-8")
    print(output, end="")
    return 0 if result["reconciled"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
