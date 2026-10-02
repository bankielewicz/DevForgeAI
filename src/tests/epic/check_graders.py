"""Checks the regex and file graders of the SPEC-004 v4 epic cases (VER-20 to VER-26) offline, before any paid run.

For each case it runs the case's scaffold in a temporary workspace, writes a scripted result (the epic files and
the final reply a run would leave) and runs grade_evals.mjs. A v4-like result must pass every regex and file
grader; each bad result must fail exactly the graders aimed at it. grade_evals.mjs skips llm graders, so a
v3-like result's case score is computed with its llm graders counted as failed: for the cases that test new
behaviour (VER-20, 21, 22, 24 and 25) it must stay under the 0.8 bar, so SKL-004 v3 fails them at case level.
VER-23 and VER-26 are guards that v3 may pass. Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/epic/check_graders.py
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CASES = Path("src/claude/DevForgeAI/evals/epic")
RUNNER = Path("src/tests/epic/grade_evals.mjs")
E1, E2 = "docs/specs/epic/EPIC-001.md", "docs/specs/epic/EPIC-002.md"
NEW_BEHAVIOUR = {"epic-mandate-changed-blocked", "epic-legacy-record-no-user", "epic-legacy-record-asks",
                 "epic-nfr-blocked-review", "epic-nfr-unknown-review"}


def grade(case, files, reply):
    """Scaffolds the case, applies `files` ({path: text}), grades; {grader: PASS|FAIL}."""
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


def epic(num, *items):
    """The part of a written epic the graders read: its refines links."""
    links = "".join(f"  - {{id: PRD-001, item: {i}, relation: refines, version: 2, hash: null}}\n" for i in items)
    return f"---\nid: EPIC-00{num}\ntype: epic\nupstream:\n{links}  - {{id: ARCH-001, relation: informed_by}}\n---\n"


def llm_count(case):
    return sum("type: llm" in g.read_text() for g in (CASES / case / "graders").glob("*.md"))


REST = ("FR-002", "FR-003", "FR-004", "NFR-001")
ELIGIBLE = ("FR-002", "FR-003", "FR-004", "FR-012", "NFR-001")
NEW_EPIC = ("FR-002", "FR-004", "FR-012")
S = []  # (case, label, files, reply, graders expected to fail, "v3" marks the v3-like result)

c = "epic-mandate-changed-blocked"
R20 = ('- FR-012: blocked by DEC-07 (POL-001#SET-01 now mandates "Network-hosted mail service (HTTPS API) for '
       'transactional email"; ARCH-001 recorded "Regional network mail relay (SMTP) for transactional email"). '
       "Resolve it with /devforgeai:architecture PRD-001.\n")
S += [
    (c, "good", {E1: epic(1, *REST)}, R20, set(), ""),
    (c, "v3-like: unknown", {E1: epic(1, *REST)},
     '- FR-012: unknown: POL-001#SET-01 fails the policy check: changed since ARCH-001 applied it; now "Network-hosted '
     'mail service (HTTPS API) for transactional email" (check 3). Review the architecture with /devforgeai:architecture '
     "PRD-001.\n", {"fr-012-blocked-by-dec-07"}, "v3"),
    (c, "FR-012 refined", {E1: epic(1, *ELIGIBLE)}, R20, {"no-fr-012"}, ""),
    (c, "a requirement missing", {E1: epic(1, "FR-002", "FR-003", "NFR-001")}, R20, {"refines-the-rest"}, ""),
]

c = "epic-legacy-record-no-user"
R21 = ("FR-012 is included. Note: ARCH-001 recorded POL-001#SET-01 without a platform "
       "(architecture.mandated_platforms=POL-001#SET-01), so the platform couldn't be confirmed; with no questions "
       "asked, the setting still counts.\n")
S += [
    (c, "good", {E1: epic(1, *ELIGIBLE)}, R21, set(), ""),
    (c, "v3-like: unknown", {E1: epic(1, *REST)},
     "- FR-012: unknown: POL-001#SET-01 fails the policy check: ARCH-001's latest resolution no longer applies it "
     "(check 3).\n", {"refines-fr-012"}, "v3"),
    (c, "an ineligible requirement", {E1: epic(1, *ELIGIBLE, "FR-001")}, R21, {"refines-nothing-else"}, ""),
]

c = "epic-legacy-record-asks"
S += [
    (c, "good", {}, "Before I write the epic: when DEC-07 was resolved, did POL-001#SET-01 mandate the Regional "
                    "network mail relay (SMTP) for transactional email?\n", set(), ""),
    (c, "v3-like: writes", {E1: epic(1, *REST)}, "EPIC-001 written to docs/specs/epic/EPIC-001.md\n",
     {"no-epic-written"}, "v3"),
]

c = "epic-missing-record-unknown"
R23 = ("- FR-012: unknown: POL-001#SET-01 fails the policy check: ARCH-001's latest resolution doesn't record it "
       "(check 3). Fix that input, or review the architecture, then run again.\n")
S += [
    (c, "good (v3 should match it: guard)", {E1: epic(1, *REST)}, R23, set(), ""),
    (c, "treated as the older form", {E1: epic(1, *ELIGIBLE)}, "FR-012 is included.\n", {"no-fr-012", "fr-012-unknown"},
     ""),
    (c, "called blocked", {E1: epic(1, *REST)}, "- FR-012: blocked by DEC-07.\n", {"fr-012-unknown"}, ""),
]

c = "epic-nfr-blocked-review"
R24 = ("- FR-003: covered by EPIC-001.\n"
       "- NFR-001: refined by EPIC-001; blocked by DEC-08 (open). Review EPIC-001's work before continuing.\n"
       "- NFR-003: later (release later); refined by EPIC-001; blocked by DEC-08 (open). No action for the current "
       "release.\n")
S += [
    (c, "good", {E2: epic(2, *NEW_EPIC)}, R24, set(), ""),
    (c, "v3-like: no review signal", {E2: epic(2, *NEW_EPIC)},
     "- FR-003: covered by EPIC-001.\n- NFR-001: blocked by DEC-08 (open). Resolve it with /devforgeai:architecture "
     "PRD-001.\n- NFR-003: later (release later); blocked by DEC-08 (open). No action for the current release.\n",
     {"nfr-001-refined-and-blocked"}, "v3"),
    (c, "NFR-001 attached to the new epic", {E2: epic(2, *NEW_EPIC, "NFR-001")}, R24, {"epic-002-no-nfr"}, ""),
    (c, "FR-003 duplicated", {E2: epic(2, *NEW_EPIC, "FR-003")}, R24, {"epic-002-no-nfr"}, ""),
    (c, "EPIC-001 changed", lambda c=c: {E2: epic(2, *NEW_EPIC),
                                         E1: scaffolded(c, E1).replace("version: 1\n", "version: 2\n", 1)},
     R24, {"epic-001-unchanged"}, ""),
]

c = "epic-nfr-unknown-review"
R25 = ("- FR-003: covered by EPIC-001.\n"
       "- NFR-001: refined by EPIC-001; unknown: ADR-005 not found. Review EPIC-001's work before continuing.\n")
S += [
    (c, "good", {E2: epic(2, *NEW_EPIC)}, R25, set(), ""),
    (c, "v3-like: no review signal", {E2: epic(2, *NEW_EPIC)},
     "- FR-003: covered by EPIC-001.\n- NFR-001: unknown: DEC-08's resolver ADR-005 not found. Fix that input, or "
     "review the architecture, then run again.\n", {"nfr-001-refined-unknown", "nfr-001-review-epic-001"}, "v3"),
    (c, "NFR-001 attached to the new epic", {E2: epic(2, *NEW_EPIC, "NFR-001")}, R25, {"epic-002-no-nfr"}, ""),
    (c, "NFR-001 called covered", {E2: epic(2, *NEW_EPIC)}, R25 + "- NFR-001: covered by EPIC-001.\n",
     {"nfr-001-not-covered"}, ""),
    (c, "good: says NFR-001 isn't covered", {E2: epic(2, *NEW_EPIC)},
     R25 + "NFR-001 is refined by EPIC-001, not covered: it stays out of EPIC-002.\n", set(), ""),
    (c, "EPIC-001 gains a link, same version", lambda c=c: {
        E2: epic(2, *NEW_EPIC),
        E1: scaffolded(c, E1).replace("relation: refines, version: 2, hash: null}\n  - {id: ARCH-001",
                                      "relation: refines, version: 2, hash: null}\n"
                                      "  - {id: PRD-001, item: FR-002, relation: refines, version: 2, hash: null}\n"
                                      "  - {id: ARCH-001", 1)},
     R25, {"epic-001-unchanged"}, ""),
]

c = "epic-unrelated-policy-marker"
R26 = ("- FR-010: blocked by the marker [NEEDS ADR: payment provider for membership fees] without a matching question "
       "(DEC-04 and DEC-08 answer other questions). Resolve it with /devforgeai:architecture PRD-001.\n")
S += [
    (c, "good (v3 should match it: guard)", {E1: epic(1, *ELIGIBLE)}, R26, set(), ""),
    (c, "marker cleared by DEC-08", {E1: epic(1, *ELIGIBLE, "FR-010")}, "FR-010 is included.\n",
     {"no-fr-010", "fr-010-blocked-by-marker"}, ""),
]


def main():
    failures = 0
    for case, label, files, reply, expect, kind in S:
        results = grade(case, files() if callable(files) else files, reply)
        failed = {g for g, r in results.items() if r == "FAIL"}
        ok = failed == expect
        note = ""
        if kind == "v3":
            total = len(results) + llm_count(case)
            score = (len(results) - len(failed)) / total
            note = f" (case score {score:.2f} with llm graders failed)"
            if case in NEW_BEHAVIOUR and score >= 0.8:
                ok, note = False, note + ": not under the 0.8 bar"
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {case}: {label}{note}"
              + ("" if failed == expect else f"\n     expected to fail {sorted(expect)}, failed {sorted(failed)}"))
    print(f"{len(S) - failures} of {len(S)} scenarios as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
