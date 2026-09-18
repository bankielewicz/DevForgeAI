"""Emit bounded, deterministic JSONL observations. Never issue acceptance."""

import argparse
import hashlib
import importlib.util
import json
import platform
import re
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
GRADER_IDS = ("package_links", "manifest_accounting")
VERSION = "1.0.0"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def is_link(path):
    info = path.lstat()
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & 0x400)


def strict_json(text):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key: " + key)
            result[key] = value
        return result

    def constant(value):
        raise ValueError("non-finite JSON value: " + value)

    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)

REQUIRED = {
    "SKILL.md", "scripts/run_evaluation.py", "scripts/graders.py",
    "references/evaluation.md", "evals/cases.jsonl", "evals/runtime.json",
    "evals/evidence.schema.json", "tests/test_evaluation.py",
    "evals/fixtures/portable/source/SKILL.md",
    "evals/fixtures/portable/destination/SKILL.md",
    "evals/fixtures/portable/evidence/source-manifest.json",
    "evals/fixtures/portable/evidence/destination-manifest.json",
    "evals/fixtures/portable/evidence/file-dispositions.json",
}


def package_binding(root):
    # Bootstrap with standard-library code before importing any grader bytes.
    files, total = {}, 0
    pending = [root]
    if not root.is_dir() or is_link(root):
        raise ValueError("package-root must be a regular directory")
    while pending:
        for item in sorted(pending.pop().iterdir()):
            if item.name.casefold() in ("backup", "backups") or is_link(item):
                raise ValueError("excluded package boundary: " + item.name)
            if item.is_dir():
                pending.append(item)
            elif item.is_file():
                if len(files) >= 2000 or total + item.stat().st_size > 32 * 1024 * 1024:
                    raise ValueError("package exceeds 2000 files or 32 MiB")
                data = item.read_bytes()
                total += len(data)
                if total > 32 * 1024 * 1024:
                    raise ValueError("package exceeds 32 MiB")
                files[item.relative_to(root).as_posix()] = data
            else:
                raise ValueError("non-regular package entry")
    manifest_bytes = files.pop("evals/build-manifest.json")
    manifest = strict_json(manifest_bytes.decode("utf-8-sig"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != "1" or manifest.get("graders") != {name: VERSION for name in GRADER_IDS}:
        raise ValueError("unsupported build manifest or grader versions")
    expected = manifest["artifacts"]
    actual = {name: digest(data) for name, data in files.items()}
    if not REQUIRED <= set(actual) or actual != expected:
        raise ValueError("required build artifact missing, unlisted or digest mismatch")
    if Path(__file__).resolve() != (root / "scripts/run_evaluation.py").resolve():
        raise ValueError("package-root must own the running runner")
    # Execute exactly the verified bytes, so a subsequent path edit cannot
    # replace the module between digest comparison and module loading.
    module_path = root / "scripts/graders.py"
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader("bound_graders", loader=None))
    exec(compile(files["scripts/graders.py"], str(module_path), "exec"), module.__dict__)
    return digest(manifest_bytes), actual["scripts/graders.py"], module.grade


def load_cases(data):
    if len(data) > 1024 * 1024:
        raise ValueError("cases exceed 1 MiB")
    lines = data.decode("utf-8-sig").splitlines()
    if not lines or len(lines) > 1000:
        raise ValueError("cases require 1 to 1000 JSONL records")
    cases, seen = [], set()
    for line in lines:
        case = strict_json(line)
        if not isinstance(case, dict) or set(case) != {"case_id", "grader_id", "params", "expected"}:
            raise ValueError("case fields must be case_id, grader_id, params, expected")
        case_id = case["case_id"]
        if not isinstance(case_id, str) or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", case_id) or case_id in seen:
            raise ValueError("invalid or duplicate case_id")
        if case["grader_id"] not in GRADER_IDS or case["expected"] not in ("PASS", "FAIL") or not isinstance(case["params"], dict):
            raise ValueError("unknown grader or invalid expected/params")
        seen.add(case_id)
        cases.append(case)
    if set(case["grader_id"] for case in cases) != set(GRADER_IDS):
        raise ValueError("suite must exercise every required grader")
    return cases


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("package-root", "candidate-root", "cases", "output", "run-id"):
        parser.add_argument("--" + name, required=True)
    args = parser.parse_args(argv)
    output = Path(args.output).absolute()
    package = Path(args.package_root).absolute()
    candidate = Path(args.candidate_root).absolute()
    cases_path = Path(args.cases).absolute()
    base = {
        "schema_version": "1", "run_id": args.run_id,
        "python_version": platform.python_version(), "platform": platform.platform(),
        "case_id": None, "grader_id": None, "grader_version": VERSION,
        "grader_sha256": None, "build_manifest_sha256": None, "cases_sha256": None,
        "candidate_digests": {}, "observations": [], "status": "ERROR",
        "expected": None, "expectation_met": False, "error": None,
    }
    records = []
    safe_output = False
    code = 2
    try:
        if not re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", args.run_id):
            raise ValueError("invalid run-id")
        for path in (package, candidate, cases_path, output.parent):
            for part in [path, *path.parents]:
                if part.exists() and is_link(part):
                    raise ValueError("link/reparse input or output boundary")
        if not output.parent.is_dir() or output.exists() or output.is_symlink():
            raise ValueError("output requires an existing directory and a new file")
        if any(output.resolve().is_relative_to(root.resolve()) for root in (package, candidate)) or output.resolve() == cases_path.resolve():
            raise ValueError("output must be outside package/candidate and cannot overwrite cases")
        safe_output = True
        base["build_manifest_sha256"], base["grader_sha256"], grade = package_binding(package)
        if sys.version_info < (3, 10):
            raise ValueError("Python 3.10 or newer required")
        if cases_path.stat().st_size > 1024 * 1024:
            raise ValueError("cases exceed 1 MiB")
        case_data = cases_path.read_bytes()
        base["cases_sha256"] = digest(case_data)
        cases = load_cases(case_data)
        code = 0
        for case in cases:
            record = dict(base, case_id=case["case_id"], grader_id=case["grader_id"], expected=case["expected"])
            try:
                record.update(grade(case["grader_id"], candidate, case["params"]))
                record["expectation_met"] = record["status"] == case["expected"]
                if not record["expectation_met"]:
                    code = max(code, 1)
            except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
                record["error"] = type(exc).__name__ + ": " + str(exc)
                code = 2
            records.append(record)
    except (ValueError, OSError, KeyError, TypeError, UnicodeError) as exc:
        records = [dict(base, error=type(exc).__name__ + ": " + str(exc))]
    payload = "".join(json.dumps(record, sort_keys=True, allow_nan=False) + "\n" for record in records)
    if safe_output:
        try:
            with output.open("x", encoding="utf-8", newline="\n") as stream:
                stream.write(payload)
        except OSError as exc:
            print("Evidence output error: " + str(exc), file=sys.stderr)
            return 2
        print(json.dumps({"records": len(records), "exit_code": code, "output": str(output), "authority": "NONE"}))
    else:
        print(payload, end="", file=sys.stderr)
    return code


if __name__ == "__main__":
    sys.exit(main())
