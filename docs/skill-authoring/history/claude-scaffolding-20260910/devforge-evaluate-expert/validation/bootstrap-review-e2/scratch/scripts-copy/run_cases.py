#!/usr/bin/env python3
"""Run authored skill-evaluation cases from a JSONL file and emit observations.

What this is
------------
An evidence producer. It reads a JSONL case file and a candidate or output
location, dispatches each case's assertions to the deterministic graders in
`graders.py`, and writes one JSONL observations file.

What this is not
----------------
It is not a gate, a validator or an acceptance decision, and it must not be used
as a substitute for one.

  * Assertions exist only because a case_id in the case file names them. There is
    no fixed rule catalogue that applies to every package.
  * The output contains no aggregate field anywhere: no overall, no coverage
    summary, no counts of passing cases, no percentage.
  * Results use MATCH / MISMATCH / INDETERMINATE, deliberately disjoint from the
    framework's PASS / FAIL / NOT_RUN / COULD_NOT_RUN / NOT_APPLICABLE vocabulary,
    so an observation row cannot be pasted into a results record as an authority
    outcome.
  * The exit status describes this program, never the candidate. See below.

Skill-package structural inspection (S001-S013) and evidence reduction are not
implemented in the DevForge CLI. A complete set of matching rows here does not
close that dependency, and the evaluation report must still name it.

Prerequisites
-------------
/usr/bin/python3 3.12, standard library only. No PyYAML and no third-party
package. No network, no subprocess, and no import or execution of candidate code.
This program writes exactly one new file, at --out, and never writes inside the
candidate tree.

Usage
-----
    python3 run_cases.py --cases CASES.jsonl --candidate DIR --out OBS.jsonl
                         [--mode source|installed] [--case-id ID]... [--help]

All paths must be absolute. --out must not already exist, its parent must exist,
and it must lie outside --candidate.

Exit status
-----------
    0  This program completed and wrote a complete observations file. It says
       nothing about whether any assertion matched.
    1  Invalid invocation or unusable input: a missing or unreadable case file,
       an unreadable candidate root, a malformed JSONL line, or an --out that
       already exists or sits inside the candidate.
    2  Unexpected internal error. Never looks like a completed run.

Output
------
JSONL. One header record, then one record per selected case:

    {"record": "header", "schema_version": "devforge.skill-eval-observations/v1",
     "runner_identity": {...}, "grader_identity": [...], "case_file": {...},
     "python_version": "...", "candidate_root": "...", "mode": "...",
     "case_selection": "...", "case_count": N, "authority": "none ..."}

    {"record": "case", "case_id": "...", "tier": "...",
     "execution_status": "COMPLETED|COULD_NOT_RUN|SKIPPED",
     "assertions": [{"assertion_id": "...", "grader": "...",
                     "result": "MATCH|MISMATCH|INDETERMINATE",
                     "observed": "...", "reason": "...", "evidence": {...}}],
     "metrics": {"files_read": N, "bytes_read": N, "duration_ms": N}}
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import graders  # noqa: E402  (resolved from this script's own directory)

SCHEMA = "devforge.skill-eval-observations/v1"
MAX_CASE_BYTES = 8 * 1024 * 1024
AUTHORITY = (
    "none - observations only. This runner does not gate admission, decide "
    "acceptance, or aggregate any verdict."
)
CUSTODY = (
    "The identities below are self-reported by this run. A protected manifest "
    "binding the runner, graders, runtime and case inputs outside evaluated-agent "
    "write access is not implemented in the DevForge CLI."
)


class InputError(Exception):
    """Unusable invocation or input; reported on stderr with exit status 1."""


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(65536), b""):
            value.update(block)
    return value.hexdigest()


def no_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError(f"duplicate JSON key: {key}")
        seen[key] = value
    return seen


def load_cases(path: Path):
    if not path.is_file():
        raise InputError(f"case file is not a readable file: {path}")
    if path.stat().st_size > MAX_CASE_BYTES:
        raise InputError(f"case file exceeds {MAX_CASE_BYTES} bytes: {path}")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise InputError(f"cannot read case file {path}: {exc}") from exc

    cases, seen = [], set()
    for number, line in enumerate(text.split("\n"), 1):
        if not line.strip() or line.lstrip().startswith("//"):
            continue
        try:
            case = json.loads(line, object_pairs_hook=no_duplicates)
        except ValueError as exc:
            raise InputError(f"{path}:{number}: malformed JSON line: {exc}") from exc
        if not isinstance(case, dict):
            raise InputError(f"{path}:{number}: each line must be a JSON object")
        case_id = case.get("case_id")
        if not isinstance(case_id, str) or not case_id.strip():
            raise InputError(f"{path}:{number}: case_id must be a non-empty string")
        if case_id in seen:
            raise InputError(f"{path}:{number}: duplicate case_id {case_id!r}")
        seen.add(case_id)
        assertions = case.get("assertions", [])
        if not isinstance(assertions, list):
            raise InputError(f"{path}:{number}: assertions must be a list")
        for assertion in assertions:
            if not isinstance(assertion, dict):
                raise InputError(f"{path}:{number}: each assertion must be an object")
            name = assertion.get("grader")
            if name is not None and name not in graders.GRADERS:
                raise InputError(f"{path}:{number}: unknown grader {name!r}")
        cases.append(case)
    if not cases:
        raise InputError(f"no cases found in {path}")
    return cases


def run_case(case, candidate_root: Path, mode: str):
    started = time.monotonic()
    budget = {"files_read": 0, "bytes_read": 0}
    rows, blocked = [], False

    root = candidate_root
    subpath = case.get("candidate_subpath")
    if isinstance(subpath, str) and subpath:
        resolved = graders.resolve_in(candidate_root, subpath)
        if resolved is None or not resolved.is_dir():
            return {
                "record": "case",
                "case_id": case["case_id"],
                "tier": case.get("tier"),
                "execution_status": "COULD_NOT_RUN",
                "cause": f"candidate_subpath {subpath!r} does not resolve to a directory inside the candidate root",
                "assertions": [],
                "metrics": {"files_read": 0, "bytes_read": 0, "duration_ms": 0},
            }
        root = resolved

    case_mode = case.get("mode")
    for assertion in case.get("assertions", []):
        name = assertion.get("grader")
        if name is None:
            rows.append({
                "assertion_id": assertion.get("assertion_id"),
                "grader": None,
                "result": "INDETERMINATE",
                "observed": "no-deterministic-grader",
                "reason": assertion.get("routed_to")
                and f"no deterministic assertion; routed to {assertion['routed_to']} in the independent review"
                or "no deterministic assertion for this expectation",
                "evidence": None,
            })
            continue
        if case_mode and case_mode != mode:
            rows.append({
                "assertion_id": assertion.get("assertion_id"),
                "grader": name,
                "result": "INDETERMINATE",
                "observed": f"mode={mode}",
                "reason": f"the case declares mode {case_mode!r} and this run used {mode!r}",
                "evidence": None,
            })
            continue
        outcome = graders.GRADERS[name](root, assertion.get("args", {}), budget, case)
        blocked = blocked or outcome.get("blocks_case", False)
        rows.append({
            "assertion_id": assertion.get("assertion_id"),
            "grader": name,
            "result": outcome["result"],
            "observed": outcome["observed"],
            "reason": outcome["reason"],
            "evidence": outcome["evidence"],
        })

    record = {
        "record": "case",
        "case_id": case["case_id"],
        "tier": case.get("tier"),
        "execution_status": "COULD_NOT_RUN" if blocked else "COMPLETED",
        "assertions": rows,
        "metrics": {
            "files_read": budget["files_read"],
            "bytes_read": budget["bytes_read"],
            "duration_ms": int((time.monotonic() - started) * 1000),
        },
    }
    if blocked:
        record["cause"] = "a required observation could not be established; see the assertion reasons"
    return record


def build_parser():
    parser = argparse.ArgumentParser(
        prog="run_cases.py",
        description=(
            "Run authored skill-evaluation cases and emit per-case observations. "
            "Produces evidence only: no aggregate verdict, no admission, no acceptance. "
            "The exit status describes this program, not the candidate."
        ),
        epilog=(
            "Exit 0: this program wrote a complete observations file (regardless of any "
            "assertion result). Exit 1: invalid invocation or unusable input. Exit 2: "
            "unexpected internal error."
        ),
    )
    parser.add_argument("--cases", required=True, type=Path, help="Absolute path to the JSONL case file.")
    parser.add_argument("--candidate", required=True, type=Path, help="Absolute path to the candidate or output root (never written to).")
    parser.add_argument("--out", required=True, type=Path, help="Absolute path for a new observations JSONL file; must not exist.")
    parser.add_argument("--mode", choices=("source", "installed"), default="source",
                        help="Evaluation mode a case may condition on. Default: source.")
    parser.add_argument("--case-id", action="append", dest="case_ids", default=None,
                        help="Run only this case_id. Repeatable. Default: every case.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        cases_path = args.cases.expanduser().resolve()
        candidate = args.candidate.expanduser().resolve()
        out = args.out.expanduser().resolve()

        if not candidate.is_dir():
            raise InputError(f"candidate root is not a readable directory: {candidate}")
        if out.exists() or out.is_symlink():
            raise InputError(f"output already exists and is never overwritten: {out}")
        if not out.parent.is_dir():
            raise InputError(f"output parent directory does not exist: {out.parent}")
        if graders.contained(out, candidate):
            raise InputError("output must be outside the candidate tree")

        cases = load_cases(cases_path)
        selected = cases
        selection = "all"
        if args.case_ids:
            wanted = set(args.case_ids)
            unknown = wanted - {case["case_id"] for case in cases}
            if unknown:
                raise InputError("unknown case id(s): " + ", ".join(sorted(unknown)))
            selected = [case for case in cases if case["case_id"] in wanted]
            selection = "subset: " + ",".join(sorted(wanted))

        here = Path(__file__).resolve()
        grader_file = here.parent / "graders.py"
        header = {
            "record": "header",
            "schema_version": SCHEMA,
            "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "python_version": sys.version.split()[0],
            "runner_identity": {"path": str(here), "sha256": digest(here)},
            "grader_identity": [{"path": str(grader_file), "sha256": digest(grader_file)}],
            "case_file": {"path": str(cases_path), "sha256": digest(cases_path)},
            "candidate_root": str(candidate),
            "mode": args.mode,
            "case_selection": selection,
            "case_count": len(selected),
            "authority": AUTHORITY,
            "custody_note": CUSTODY,
        }

        records = [header]
        skipped = {case["case_id"] for case in cases} - {case["case_id"] for case in selected}
        for case in cases:
            if case["case_id"] in skipped:
                records.append({
                    "record": "case",
                    "case_id": case["case_id"],
                    "tier": case.get("tier"),
                    "execution_status": "SKIPPED",
                    "cause": "not selected by --case-id",
                    "assertions": [],
                    "metrics": {"files_read": 0, "bytes_read": 0, "duration_ms": 0},
                })
            else:
                records.append(run_case(case, candidate, args.mode))

        with out.open("x", encoding="utf-8", newline="\n") as stream:
            for record in records:
                json.dump(record, stream, ensure_ascii=False, allow_nan=False, sort_keys=False)
                stream.write("\n")
        print(f"wrote {len(records) - 1} case record(s) to {out}")
        return 0

    except InputError as error:
        print(f"run_cases.py: unusable input: {error}", file=sys.stderr)
        return 1
    except Exception as error:  # noqa: BLE001 - an internal fault must never look complete
        print(f"run_cases.py: internal error, no complete output produced: "
              f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
