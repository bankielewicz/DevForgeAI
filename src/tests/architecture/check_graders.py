"""Checks the regex and file graders of the architecture cases added for SPEC-003 v3 (VER-17 policy-bad-date,
VER-18 failed-amendment-stays-in-review) offline, before any paid run: a hand-made good result must pass
every regex and file grader, and each bad result must fail exactly the graders aimed at it. llm graders
are skipped, as grade_evals.mjs skips them. Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/architecture/check_graders.py
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CASES = Path("src/claude/DevForgeAI/evals/architecture")
RUNNER = Path("src/tests/architecture/grade_evals.mjs")
SESSION = "0f8e2a4c-5b6d-4e7f-8a9b-1c2d3e4f5a6b"
ARCH = "docs/specs/arch/ARCH-001.md"
RESOLUTION = ("Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
              "quality.required_categories=floor only (default)")


def grade(case, files, reply):
    case_dir = CASES / case
    with tempfile.TemporaryDirectory() as tmp:
        ws, reply_file = Path(tmp) / "ws", Path(tmp) / "reply.txt"
        ws.mkdir()
        subprocess.run(["bash", str((case_dir / "scaffold.sh").resolve())], cwd=ws, check=True)
        for path, text in files.items():
            (ws / path).parent.mkdir(parents=True, exist_ok=True)
            (ws / path).write_text(text)
        reply_file.write_text(reply)
        out = subprocess.run(["node", str(RUNNER), str(case_dir), str(ws), str(reply_file)],
                             capture_output=True, text=True).stdout
    return dict((m.group(2), m.group(1)) for m in re.finditer(r"^  (PASS|FAIL)  (\S+)\.md", out, re.M))


def scaffolded(case, path):
    text = (CASES / case / "scaffold.sh").read_text()
    return dict(re.findall(r"cat > (\S+) <<'FIXTURE'\n(.*?)FIXTURE\n", text, re.S))[path]


def edit(text, old, new):
    assert text.count(old) == 1, f"anchor not unique: {old!r}"
    return text.replace(old, new)


def amended(text, *, status="in-review", clear=True, fix_cmp_01=False):
    """ARCH-001 after the amendment and ERR-05, as a correct run leaves it."""
    t = edit(text, "status: approved\nversion: 1\ncreated: 2026-09-21\nupdated: 2026-09-22",
             f"status: {status}\nversion: 2\ncreated: 2026-09-21\nupdated: 2026-09-29")
    if clear:
        t = edit(t, 'approved_by: "Priya Nair"\napproved_on: 2026-09-22', 'approved_by: ""\napproved_on: null')
    t = edit(t, 'session: "fixture-session"', f'session: "{SESSION}"')
    t = edit(t, "  - {id: PRD-001, relation: informed_by, version: 1, hash: null}",
             "  - {id: PRD-001, relation: informed_by, version: 2, hash: null}")
    t = edit(t, "outcome: create", "outcome: amend")
    if fix_cmp_01:
        t = edit(t, "    status: current\n", "    status: active\n")
    t = edit(t, "\n```\n\n## 5. Evidence inspected",
             "\n  - id: DEC-03\n    status: active\n"
             "    question: \"Where is the coordinator's daily roster served from?\"\n"
             "    blocking: true\n    state: open\n    resolved_by: []\n    notes: null\n    upstream:\n"
             "      - {id: PRD-001, item: FR-003, relation: informed_by, version: 2, hash: null}\n"
             "```\n\n## 5. Evidence inspected")
    return t + (f"| 2 | 2026-09-29 | claude-code (session {SESSION}) | Amended for PRD-001 v2: DEC-03 added for the "
                f"roster question. {RESOLUTION} | DEC-03 |\n"
                f"| 2 | 2026-09-29 | claude-code (session {SESSION}) | Validation failed (ERR-05): CMP-01 status "
                "current is not active or deprecated. Left in-review. Approval cleared. | none |\n")


R17 = ("Policy error in docs/specs/policy/POL-001.md, frontmatter field updated: 2026-13-45 is not a valid calendar "
       "date (schema). Nothing was written.\n")
R18 = ("Validation failed (ERR-05). Check 1: 1 error: CMP-01 has status `current`. It can't be repaired, because\n"
       "CMP-01 is an existing item the amendment must leave unchanged. ARCH-001 is left in-review with its approval\n"
       "cleared. Readiness wasn't validated.\n")
FAIL_ARCH = scaffolded("failed-amendment-stays-in-review", ARCH)

S = [
    ("policy-bad-date", "good", {}, R17, set()),
    ("policy-bad-date", "ARCH written anyway", {ARCH: FAIL_ARCH}, R17, {"no-arch-written"}),
    ("policy-bad-date", "ADR written anyway", {"docs/specs/adr/ADR-001.md": "x"}, R17, {"no-adr-written"}),
    ("policy-bad-date", "field not named", {}, "Policy error in docs/specs/policy/POL-001.md. Nothing was written.\n",
     {"names-field"}),
    ("policy-bad-date", "file not named", {}, "The updated date is wrong. Nothing was written.\n", {"names-file"}),
    ("failed-amendment-stays-in-review", "good", {ARCH: amended(FAIL_ARCH)}, R18, set()),
    ("failed-amendment-stays-in-review", "approved restored", {ARCH: amended(FAIL_ARCH, status="approved", clear=False)},
     R18, {"arch-in-review", "approval-cleared"}),
    ("failed-amendment-stays-in-review", "approval kept", {ARCH: amended(FAIL_ARCH, clear=False)}, R18, {"approval-cleared"}),
    ("failed-amendment-stays-in-review", "CMP-01 repaired", {ARCH: amended(FAIL_ARCH, fix_cmp_01=True)}, R18,
     {"cmp-01-unchanged"}),
    ("failed-amendment-stays-in-review", "second ARCH created", {"docs/specs/arch/ARCH-002.md": FAIL_ARCH}, R18,
     {"arch-in-review", "approval-cleared", "no-arch-002"}),
    ("failed-amendment-stays-in-review", "reply names no component", {ARCH: amended(FAIL_ARCH)},
     "Validation failed after 1 check; ARCH-001 is in-review.\n", {"reply-names-cmp-01"}),
]


def main():
    failures = 0
    for case, label, files, reply, expect in S:
        failed = {g for g, r in grade(case, files, reply).items() if r == "FAIL"}
        ok = failed == expect
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {case}: {label}" + ("" if ok else f"\n     expected to fail {sorted(expect)}, failed {sorted(failed)}"))
    print(f"{len(S) - failures} of {len(S)} scenarios as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
