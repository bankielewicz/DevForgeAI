"""Read-only integrity locators; semantic disposition remains a QA review."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(r"C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe")
MANIFEST = Path(
    r"C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260915T2306060954875Z\candidate-manifest.json"
)

PROHIBITED = re.compile(
    r"#\s*\[\s*(?:ignore|should_panic|coverage)|"
    r"\b(?:mockall|automock|mock!|double::|fake::|no_coverage)\b",
    re.IGNORECASE,
)
GAMING_LOCATORS = re.compile(
    r"assert!\s*\(\s*true\s*\)|unwrap_or\s*\(\s*true\s*\)|"
    r"process::exit\s*\(\s*0\s*\)|catch_unwind|--ignored|--skip|"
    r"\b(?:retry|rerun|flaky)\b",
    re.IGNORECASE,
)


def matching_lines(path: Path, pattern: re.Pattern[str]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if pattern.search(line):
            result.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "line": number,
                    "text": line.strip(),
                }
            )
    return result


def test_attributes(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    result: list[dict[str, object]] = []
    for index, line in enumerate(lines):
        if line.strip() != "#[test]":
            continue
        function = None
        for following in range(index + 1, min(index + 8, len(lines))):
            match = re.search(r"\bfn\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", lines[following])
            if match:
                function = match.group(1)
                break
        result.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "line": index + 1,
                "function": function,
            }
        )
    return result


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rust = sorted(Path(item["path"]) for item in manifest if item["path"].endswith(".rs"))
    prohibited: list[dict[str, object]] = []
    gaming: list[dict[str, object]] = []
    tests: list[dict[str, object]] = []
    conditional_attributes: list[dict[str, object]] = []
    macros: list[dict[str, object]] = []
    for path in rust:
        prohibited.extend(matching_lines(path, PROHIBITED))
        gaming.extend(matching_lines(path, GAMING_LOCATORS))
        tests.extend(test_attributes(path))
        conditional_attributes.extend(matching_lines(path, re.compile(r"#\s*\[\s*cfg(?:_attr)?")))
        macros.extend(matching_lines(path, re.compile(r"\bmacro_rules!|#\s*\[\s*proc_macro")))
    cargo = (ROOT / "Cargo.toml").read_text(encoding="utf-8")
    output = {
        "schema_version": 1,
        "manifest_entries": len(manifest),
        "rust_files": len(rust),
        "physical_test_attributes": len(tests),
        "tests": tests,
        "prohibited_pattern_locators": prohibited,
        "gaming_pattern_locators": gaming,
        "conditional_attribute_locators": conditional_attributes,
        "macro_definition_locators": macros,
        "cargo_contains_mock_named_dependency": bool(
            re.search(r"(?im)^\s*[A-Za-z0-9_-]*(?:mock|fake|double)[A-Za-z0-9_-]*\s*=", cargo)
        ),
    }
    print(json.dumps(output, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
