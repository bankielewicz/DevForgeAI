"""Read-only Rust integrity locators; semantic disposition remains manual QA."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


PROHIBITED = re.compile(
    r"#\s*\[\s*(?:ignore|should_panic|coverage)|"
    r"\b(?:mockall|automock|mock!|double::|fake::|no_coverage)\b",
    re.IGNORECASE,
)
GAMING = re.compile(
    r"assert!\s*\(\s*true\s*\)|unwrap_or\s*\(\s*true\s*\)|"
    r"process::exit\s*\(\s*0\s*\)|catch_unwind|--ignored|--skip|"
    r"\b(?:retry|rerun|flaky)\b",
    re.IGNORECASE,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def matching_lines(root: Path, path: Path, pattern: re.Pattern[str]) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if pattern.search(line):
            result.append(
                {"path": path.relative_to(root).as_posix(), "line": number, "text": line.strip()}
            )
    return result


def test_attributes(root: Path, path: Path) -> list[dict[str, object]]:
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
            {"path": path.relative_to(root).as_posix(), "line": index + 1, "function": function}
        )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--candidate-manifest", type=Path, required=True)
    parser.add_argument("--candidate-manifest-sha256", required=True)
    args = parser.parse_args()
    root = args.package.resolve(strict=True)
    manifest_path = args.candidate_manifest.resolve(strict=True)
    if sha256(manifest_path) != args.candidate_manifest_sha256:
        raise SystemExit("candidate manifest digest mismatch")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rust = sorted(
        Path(item["path"]).resolve(strict=True)
        for item in manifest
        if str(item["path"]).endswith(".rs")
    )
    if any(not path.is_relative_to(root) for path in rust):
        raise SystemExit("Rust manifest path outside package")

    prohibited: list[dict[str, object]] = []
    gaming: list[dict[str, object]] = []
    tests: list[dict[str, object]] = []
    conditional: list[dict[str, object]] = []
    macros: list[dict[str, object]] = []
    for path in rust:
        prohibited.extend(matching_lines(root, path, PROHIBITED))
        gaming.extend(matching_lines(root, path, GAMING))
        tests.extend(test_attributes(root, path))
        conditional.extend(matching_lines(root, path, re.compile(r"#\s*\[\s*cfg(?:_attr)?")))
        macros.extend(matching_lines(root, path, re.compile(r"\bmacro_rules!|#\s*\[\s*proc_macro")))
    cargo = (root / "Cargo.toml").read_text(encoding="utf-8")
    result = {
        "schema_version": 1,
        "candidate_manifest_sha256": sha256(manifest_path),
        "manifest_entries": len(manifest),
        "rust_files": len(rust),
        "physical_test_attributes": len(tests),
        "tests": tests,
        "prohibited_pattern_locators": prohibited,
        "gaming_pattern_locators": gaming,
        "conditional_attribute_locators": conditional,
        "macro_definition_locators": macros,
        "cargo_contains_mock_named_dependency": bool(
            re.search(r"(?im)^\s*[A-Za-z0-9_-]*(?:mock|fake|double)[A-Za-z0-9_-]*\s*=", cargo)
        ),
        "semantic_conclusion": "NOT_EVALUATED_BY_LOCATOR",
    }
    print(json.dumps(result, sort_keys=True, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

