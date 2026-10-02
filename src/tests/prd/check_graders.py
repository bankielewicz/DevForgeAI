"""Checks the regex and file graders added for SPEC-002 v2 offline, before any paid run.

For each new prd case (VER-24 to VER-38) and the graders added to records-provenance (VER-09) and
constraints-not-design (VER-10), it runs the case's scaffold in a temporary workspace, writes a
hand-made good result (the files and final reply a correct run would leave), and runs
grade_evals.mjs: every regex and file grader must pass. Then it writes bad results, each breaking one
obligation, and checks that exactly the graders aimed at it fail. llm graders are skipped here, as
grade_evals.mjs skips them. Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/prd/check_graders.py
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

CASES = Path("src/claude/DevForgeAI/evals/prd")
RUNNER = Path("src/tests/prd/grade_evals.mjs")
SESSION = "0f8e2a4c-5b6d-4e7f-8a9b-1c2d3e4f5a6b"
RESOLUTION = ("Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
              "quality.required_categories=floor only (default)")
PRD = "docs/specs/prd/PRD-001.md"


def grade(case, files, reply):
    """Scaffolds the case, applies `files` ({path: text, or None to delete}), grades; {grader: PASS|FAIL}."""
    case_dir = CASES / case
    with tempfile.TemporaryDirectory() as tmp:
        ws, reply_file = Path(tmp) / "ws", Path(tmp) / "reply.txt"
        ws.mkdir()
        subprocess.run(["bash", str((case_dir / "scaffold.sh").resolve())], cwd=ws, check=True)
        for path, text in files(ws).items() if callable(files) else files.items():
            target = ws / path
            if text is None:
                target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(text)
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


def new_prd(*, context="internal", authors='["Priya Nair", "claude-code"]', model="claude-opus-5-5",
            session=SESSION, row_session=SESSION, upstream_extra="", prose="", nfrs="non_functional_requirements: []\n",
            sms=None, open_questions="- None.\n", section8="Mobile-friendly web pages; no app to install.\n"):
    """A new PRD-001 from the food bank BRN-001, in the shape the skill's output rules give."""
    sms = sms or ('success_metrics:\n  - id: SM-01\n    status: active\n    metric: "Share of shifts that start fully staffed"\n'
                  '    baseline: "[NEEDS CLARIFICATION: baseline]"\n    target: "[NEEDS CLARIFICATION: target for share of '
                  'shifts that start fully staffed]"\n    measured_by: "[NEEDS CLARIFICATION: source]"\n    upstream:\n'
                  '      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}\n')
    return f"""\
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: draft
version: 1
created: 2026-09-29
updated: 2026-09-29
owner: "Priya Nair"
authors: {authors}
generated_by:
  tool: "claude-code"
  model: "{model}"
  session: "{session}"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {{id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}}
  - {{id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}}
{upstream_extra}supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "[NEEDS CLARIFICATION: name of the current release]"
stage: null
operating_context: {context}
stakeholders: []
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Volunteers sign up for shifts online and get a reminder the day before.

## 2. Problem and opportunity

Sign-up by phone leaves shifts unfilled (BRN-001#PRB-01), and volunteers forget shifts (BRN-001#PRB-02).

## 3. Users and personas

Volunteers and the shift coordinator.

## 4. Goals and non-goals

**Goals**
- Shifts filled online.

**Non-goals** (explicitly out of scope)
- A native mobile app (rejected in the brainstorm).

## 5. Success metrics

```yaml items
{sms}```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let volunteers see open shifts and sign up online."
    priority: null
    release: null
    notes: null
    upstream:
      - {{id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}}
  - id: FR-002
    status: active
    statement: "The system shall text each volunteer a reminder the day before their shift."
    priority: null
    release: null
    notes: null
    upstream:
      - {{id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}}
```

## 7. Non-functional requirements

{prose}```yaml items
{nfrs}```

## 8. User experience

{section8}
## 9. Constraints and dependencies

None beyond section 7.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that most volunteers will sign up online once they can see open shifts."
    validation: "Share of shifts filled online in the first month"
    state: open
    upstream:
      - {{id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}}
```

## 11. Release and rollout

[NEEDS CLARIFICATION: rollout plan]

## 12. Open questions

{open_questions}
## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session {row_session}) | Initial draft from BRN-001. {RESOLUTION} | all |
"""


def nfr(num, category, statement, upstream=""):
    return (f"  - id: NFR-{num:03d}\n    status: active\n    category: {category}\n    statement: \"{statement}\"\n"
            f"    priority: null\n    release: null\n{upstream}")


BRN_LINK = "    upstream:\n      - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}\n"


def extended(text, *, status="in-review", approval_cleared=True, authors=None, reviewed=None, rows_edit=None,
             row_text="Extended from BRN-002: FR-003 added. Status approved to in-review, approval cleared. "
                      "This revision has not been reviewed.", brn_link=True, version=2):
    """The food bank PRD-001 after a valid extension from BRN-002 (the edits a correct run makes)."""
    t = edit(text, "version: 1\ncreated: 2026-09-14\nupdated: 2026-09-20",
             f"version: {version}\ncreated: 2026-09-14\nupdated: 2026-09-29")
    t = edit(t, "status: approved", f"status: {status}")
    if approval_cleared:
        t = edit(t, 'approved_by: "Priya Nair"\napproved_on: 2026-09-20', 'approved_by: ""\napproved_on: null')
    t = edit(t, 'session: "fixture-session"', f'session: "{SESSION}"')
    if authors:
        t = edit(t, 'authors: ["Priya Nair", "claude-code"]', f"authors: {authors}")
    if reviewed is not None:
        t = edit(t, 'reviewed_by: ["Marcus Lee"]', f"reviewed_by: {reviewed}")
    link = "      - {id: BRN-002, item: IDEA-01, relation: derives, version: 1, hash: null}\n" if brn_link else ""
    fr2_end = "    notes: null\n    upstream:\n      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n```"
    t = edit(t, fr2_end, fr2_end[:-3] +
             "  - id: FR-003\n    status: active\n"
             '    statement: "The system shall let a volunteer offer a booked shift for swap and another volunteer take it online."\n'
             f"    priority: null\n    release: null\n    notes: null\n    upstream:\n{link}```")
    if rows_edit:
        t = edit(t, *rows_edit)
    return t + f"| 2 | 2026-09-29 | claude-code (session {SESSION}) | {row_text} {RESOLUTION} | FR-003 |\n"


# --- Scenarios: (case, label, files, reply, graders expected to fail) ---------------------------

S = []

# VER-24 quality-answers-kept-apart
SEC_PROSE = "Security: the user confirmed nothing is needed beyond the hosting platform.\n\n"
Q_OPEN = ("- [NEEDS CLARIFICATION: constraint requirements for internal]\n"
          "- [NEEDS CLARIFICATION: privacy requirements for internal]\n")
SM_ONLINE = ('success_metrics:\n  - id: SM-01\n    status: active\n    metric: "Share of shifts filled online"\n'
             '    baseline: "[NEEDS CLARIFICATION: baseline for share of shifts filled online]"\n'
             '    target: "[NEEDS CLARIFICATION: target for share of shifts filled online]"\n'
             '    measured_by: "[NEEDS CLARIFICATION: where sign-ups are counted]"\n')
Q24 = dict(prose=SEC_PROSE, open_questions=Q_OPEN, sms=SM_ONLINE)
R24 = "PRD-001 written to docs/specs/prd/PRD-001.md (from BRN-001; new)\n"
c = "quality-answers-kept-apart"
S += [
    (c, "good", {PRD: new_prd(**Q24)}, R24, set()),
    (c, "good: no rules are needed", {PRD: new_prd(**dict(Q24, prose="Security: no sign-in rules are needed beyond what the user named.\n\n"))}, R24, set()),
    (c, "good, none as a bullet", {PRD: new_prd(**dict(Q24, prose="- **Security:** none beyond the platform, as the user answered.\n\n"))}, R24, set()),
    (c, "security NFR written", {PRD: new_prd(**dict(Q24, nfrs="non_functional_requirements:\n" + nfr(1, "security", "Sign-in is required.")))}, R24, {"no-security-nfr"}),
    (c, "none only inside a YAML statement", {PRD: new_prd(**dict(Q24, prose="", nfrs="non_functional_requirements:\n" + nfr(1, "other", "Security needs nothing beyond the platform.")))}, R24, {"security-none-in-prose"}),
    (c, "none in section 8, not 7", {PRD: new_prd(**dict(Q24, prose="", section8="Security: none beyond the platform.\n"))}, R24, {"security-none-in-prose"}),
    (c, "security marked unanswered", {PRD: new_prd(**dict(Q24, open_questions=Q_OPEN + "- [NEEDS CLARIFICATION: security requirements for internal]\n"))}, R24, {"security-not-marked-unanswered"}),
    (c, "privacy marker missing", {PRD: new_prd(**dict(Q24, open_questions="- [NEEDS CLARIFICATION: constraint requirements for internal]\n"))}, R24, {"privacy-marker"}),
    (c, "privacy NFR invented", {PRD: new_prd(**dict(Q24, nfrs="non_functional_requirements:\n" + nfr(1, "privacy", "Phone numbers stay private.")))}, R24, {"no-privacy-nfr"}),
    (c, "metric target invented", {PRD: new_prd(**dict(Q24, sms=SM_ONLINE.replace('"[NEEDS CLARIFICATION: target for share of shifts filled online]"', '"90% by the end of the pilot"')))}, R24, {"metric-target-marked"}),
    (c, "context left null", {PRD: new_prd(**dict(Q24, context="null"))}, R24, {"context-internal"}),
    # With no file, grade_evals.mjs fails every file grader, not_contains ones included.
    (c, "no PRD", {}, "Nothing written.", {"prd-exists", "context-internal", "security-none-in-prose", "privacy-marker", "metric-target-marked",
                                           "no-security-nfr", "no-privacy-nfr", "security-not-marked-unanswered"}),
]

# VER-25 none-does-not-waive-policy
COMP_PROSE = "Compliance: the user answered none; POL-001#SET-01 still requires it for internal use (see open questions).\n\n"
COMP_Q = (Q_OPEN + "- [NEEDS CLARIFICATION: security requirements for internal]\n"
          "- [NEEDS CLARIFICATION: compliance requirements for internal; required by POL-001#SET-01, the user answered none]\n")
Q25 = dict(prose=COMP_PROSE, open_questions=COMP_Q,
           upstream_extra="  - {id: POL-001, item: SET-01, relation: informed_by, version: 1, hash: null}\n")
c = "none-does-not-waive-policy"
S += [
    (c, "good", {PRD: new_prd(**Q25)}, R24, set()),
    (c, "compliance NFR invented", {PRD: new_prd(**dict(Q25, nfrs="non_functional_requirements:\n" + nfr(1, "compliance", "Follow SOC 2.")))}, R24, {"no-compliance-nfr"}),
    (c, "none not recorded", {PRD: new_prd(**dict(Q25, prose=""))}, R24, {"compliance-none-recorded"}),
    # Section 7 sentences two VER-25 runs wrote in SKL-002 v4's pass C (kept traces): both record the none.
    (c, "good: no regulation applies", {PRD: new_prd(**dict(Q25, prose="Compliance: the user confirmed that no regulation applies.\n\n"))}, R24, set()),
    (c, "good: no requirement is needed", {PRD: new_prd(**dict(Q25, prose="Compliance: the user stated that no regulation applies, so no compliance requirement is needed.\n\n"))}, R24, set()),
    (c, "compliance named, no none", {PRD: new_prd(**dict(Q25, prose="Compliance: see the open questions.\n\n"))}, R24, {"compliance-none-recorded"}),
    (c, "marker without the setting", {PRD: new_prd(**dict(Q25, open_questions=Q_OPEN + "- [NEEDS CLARIFICATION: compliance requirements for internal]\n"))}, R24, {"marker-names-setting"}),
    (c, "none treated as waiving policy", {PRD: new_prd(**dict(Q25, open_questions=Q_OPEN))}, R24, {"marker-names-setting"}),
]

# VER-26 stated-choice-honored
PRD_002 = (scaffolded("stated-choice-honored", "docs/specs/prd/PRD-001.md")
           .replace("PRD-001", "PRD-002").replace("BRN-001", "BRN-002").replace("status: approved", "status: draft"))
R26_BLOCK = "PRD-002 written to docs/specs/prd/PRD-002.md (from BRN-002; new)\nRequirements: 3 functional\n\n"
c = "stated-choice-honored"
S += [
    (c, "good: as your request asked", {"docs/specs/prd/PRD-002.md": PRD_002}, R26_BLOCK + "New PRD, as your request asked.\n", set()),
    (c, "good: you asked", {"docs/specs/prd/PRD-002.md": PRD_002}, R26_BLOCK + "You asked for a new PRD, so I wrote PRD-002 and left PRD-001 unchanged.\n", set()),
    (c, "good: the request answered the gate", {"docs/specs/prd/PRD-002.md": PRD_002}, R26_BLOCK + "Your request (\"Write a new PRD for BRN-002\") answered the new-versus-extend gate.\n", set()),
    (c, "reply names no source", {"docs/specs/prd/PRD-002.md": PRD_002}, R26_BLOCK + "I recommend a new PRD: account closure is a separate initiative with its own owner.\n", {"names-request-as-source"}),
    (c, "PRD-001 extended instead", {PRD: edit(scaffolded(c, PRD), "version: 1\n", "version: 2\n")}, R26_BLOCK.replace("PRD-002", "PRD-001") + "Extended PRD-001, as your request asked.\n",
     {"prd-002-exists", "prd-002-from-brn-002", "prd-001-unchanged", "names-request-as-source"}),
]

# VER-27 failed-extension-stays-in-review
c = "failed-extension-stays-in-review"
FOOD_BAD = scaffolded(c, PRD)
R27 = ("Validation failed (ERR-06). Check 1: 1 error: FR-001 has priority `high`, which isn't a MoSCoW value. It can't be\n"
       "repaired: FR-001 is an existing item an extension must leave unchanged, so I stopped after the initial check.\n"
       "PRD-001 is left in-review with its approval cleared. It is not ready for the architecture step until its owner\n"
       "fixes FR-001.\n")
FAILED_ROW = "Extended from BRN-002: FR-003 added. Status approved to in-review, approval cleared. This revision has not been reviewed."
S += [
    (c, "good", {PRD: extended(FOOD_BAD)}, R27, set()),
    (c, "approved restored", {PRD: extended(FOOD_BAD, status="approved", approval_cleared=False)}, R27, {"prd-in-review", "approval-cleared"}),
    (c, "approval kept", {PRD: extended(FOOD_BAD, approval_cleared=False)}, R27, {"approval-cleared"}),
    (c, "FR-001 repaired", {PRD: edit(extended(FOOD_BAD), "priority: high", "priority: must")}, R27, {"fr-001-unchanged"}),
    (c, "reply names no item", {PRD: extended(FOOD_BAD)}, "Validation failed after 1 check; PRD-001 is in-review.\n", {"reply-names-fr-001"}),
]


# VER-28 to VER-31: policy errors
def policy_reply(field, setting=""):
    where = f", {setting}," if setting else ","
    return (f"Policy error in docs/specs/policy/POL-001.md{where} field {field}: invalid (schema). Nothing was written; "
            "fix the policy and run again.\n")


for c, field, extra in [("policy-bad-date", "updated", ""), ("policy-bad-authors", "authors", ""),
                        ("policy-bad-link", "upstream[0].relation", ""),
                        ("policy-bad-type", "value", "SET-01 (interview.max_calls)")]:
    graders = {"names-field"} | ({"names-setting"} if extra else set())
    S += [
        (c, "good", {}, policy_reply(field, extra), set()),
        (c, "PRD written anyway", {PRD: new_prd()}, "PRD-001 written.\n", {"no-prd-written", "names-file"} | graders),
        (c, "file not named", {}, "Policy error: the policy is invalid. Nothing was written.\n", {"names-file"} | graders),
        (c, "field not named", {}, f"Policy error in docs/specs/policy/POL-001.md{', SET-01' if extra else ''}: it is invalid. Nothing was written.\n",
         {"names-field"}),
    ]

# VER-32 extension-keeps-review-history
c = "extension-keeps-review-history"
FOOD = scaffolded(c, PRD)
R32 = "PRD-001 written to docs/specs/prd/PRD-001.md (from BRN-002; extended to version 2)\n"
S += [
    (c, "good", {PRD: extended(FOOD)}, R32, set()),
    (c, "good: unreviewed wording", {PRD: extended(FOOD, row_text="Extended from BRN-002: FR-003 added; unreviewed revision.")}, R32, set()),
    (c, "not extended", {}, R32, {"extended-to-version-2", "new-fr-from-brn-002", "prd-in-review", "approval-cleared", "new-row-unreviewed"}),
    (c, "no BRN-002 link", {PRD: extended(FOOD, brn_link=False)}, R32, {"new-fr-from-brn-002"}),
    (c, "stays approved", {PRD: extended(FOOD, status="approved", approval_cleared=False)}, R32, {"prd-in-review", "approval-cleared"}),
    (c, "authors rewritten", {PRD: extended(FOOD, authors='["claude-code"]')}, R32, {"authors-unchanged"}),
    (c, "reviewed_by emptied", {PRD: extended(FOOD, reviewed="[]")}, R32, {"reviewed-by-unchanged"}),
    (c, "earlier row edited", {PRD: extended(FOOD, rows_edit=("| Reviewed: no changes requested |", "| Reviewed |"))}, R32, {"earlier-rows-unchanged"}),
    (c, "new row says nothing about review", {PRD: extended(FOOD, row_text="Extended from BRN-002: FR-003 added.")}, R32, {"new-row-unreviewed"}),
]

# VER-09 records-provenance: the four added graders, alongside the v1 graders
c = "records-provenance"
S += [
    (c, "good", {PRD: new_prd()}, R24, set()),
    (c, "requirement text says unavailable", {PRD: new_prd(nfrs="non_functional_requirements:\n" + nfr(1, "reliability", "Unavailable shifts are hidden."))}, R24, set()),
    (c, "identity unavailable", {PRD: new_prd(model="unavailable")}, R24, {"model-is-a-claude-model-id", "identity-not-unavailable"}),
    (c, "tool missing from authors", {PRD: new_prd(authors='["Priya Nair"]')}, R24, {"authors-include-the-tool"}),
    (c, "Change Log names another session", {PRD: new_prd(row_session="11111111-2222-3333-4444-555555555555")}, R24, {"changelog-session-matches"}),
]

# VER-10 constraints-not-design: the two added graders
c = "constraints-not-design"
CONSTRAINTS = ("non_functional_requirements:\n"
               + nfr(1, "constraint", "The system runs on AWS (applies to the whole product).")
               + nfr(2, "constraint", "Payments go through Stripe (applies to checkout).")
               + nfr(3, "security", "Staff accounts need two-factor sign-in.", BRN_LINK))
S += [
    (c, "good (a later NFR has a BRN link)", {PRD: new_prd(nfrs=CONSTRAINTS)}, R24, set()),
    (c, "AWS linked to the BRN", {PRD: new_prd(nfrs=CONSTRAINTS.replace("(applies to the whole product).\"\n    priority: null\n    release: null\n",
                                                                       "(applies to the whole product).\"\n    priority: null\n    release: null\n" + BRN_LINK))}, R24, {"aws-no-brn-link"}),
    (c, "Stripe linked to the BRN", {PRD: new_prd(nfrs=CONSTRAINTS.replace("(applies to checkout).\"\n    priority: null\n    release: null\n",
                                                                          "(applies to checkout).\"\n    priority: null\n    release: null\n" + BRN_LINK))}, R24, {"stripe-no-brn-link"}),
]

# VER-33 no-brainstorm-yet
c = "no-brainstorm-yet"
R33 = "No brainstorm exists yet in this project, so there is no BRN to turn into a PRD. Run /devforgeai:brainstorm first.\n"
S += [
    (c, "good", {}, R33, set()),
    (c, "says ideas already cited", {}, "Every promoted idea is already cited by a PRD, so there is nothing to process.\n",
     {"points-to-brainstorm", "never-says-already-cited"}),
    (c, "no pointer", {}, "No brainstorm exists yet.\n", {"points-to-brainstorm"}),
    (c, "PRD written anyway", {PRD: new_prd()}, R33, {"no-prd-written", "no-docs-written"}),
    (c, "PRD drafted from the README", {"PRD.md": "# PRD\n"}, R33, {"no-root-prd"}),
    (c, "brainstorm started on its own", {"docs/specs/brainstorm/BRN-001.md": "---\nid: BRN-001\n---\n"}, R33,
     {"no-docs-written"}),
]


# VER-34 revisited-brainstorm-extends
def revisited(text, *, idea_version=2, extra_fr="", fr1_edit=None):
    """The draft food bank PRD-001 after a valid extension from BRN-001 version 2 (FR-003 from IDEA-05)."""
    t = edit(text, "version: 1\ncreated: 2026-09-14\nupdated: 2026-09-20", "version: 2\ncreated: 2026-09-14\nupdated: 2026-09-29")
    t = edit(t, 'session: "fixture-session"', f'session: "{SESSION}"')
    t = edit(t, "  - {id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}\n",
             "  - {id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}\n"
             "  - {id: BRN-001, item: PRB-03, relation: derives, version: 2, hash: null}\n")
    fr2_end = "    notes: null\n    upstream:\n      - {id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}\n```"
    t = edit(t, fr2_end, fr2_end[:-3] +
             "  - id: FR-003\n    status: active\n"
             '    statement: "The system shall let a volunteer sign up only for shifts whose required training they have."\n'
             "    priority: null\n    release: null\n    notes: null\n    upstream:\n"
             f"      - {{id: BRN-001, item: IDEA-05, relation: derives, version: {idea_version}, hash: null}}\n{extra_fr}```")
    if fr1_edit:
        t = edit(t, *fr1_edit)
    return t + (f"| 2 | 2026-09-29 | claude-code (session {SESSION}) | Extended from BRN-001 version 2: FR-003 added; IDEA-01 and IDEA-03 left out (already cited). "
                f"This revision has not been reviewed. {RESOLUTION} | FR-003 |\n")


c = "revisited-brainstorm-extends"
DRAFT = scaffolded(c, PRD)
R34_BLOCK = ("PRD-001 written to docs/specs/prd/PRD-001.md (from BRN-001; extended to version 2)\n"
             "Validation: passed at check 1 of at most 4 (no repairs)\n\n")
R34_LEFT = "IDEA-01 and IDEA-03 left out: PRD-001#FR-001 and PRD-001#FR-002 already cite them.\n"
R34_SUSPECT = "Suspect links: FR-001, FR-002, SM-01, SM-02 and ASM-01 cite BRN-001 version 1; BRN-001 is now at version 2.\n"
IDEA_01_AGAIN = ("  - id: FR-004\n    status: active\n    statement: \"The system shall show open shifts.\"\n"
                 "    priority: null\n    release: null\n    notes: null\n    upstream:\n"
                 "      - {id: BRN-001, item: IDEA-01, relation: derives, version: 2, hash: null}\n")
S += [
    (c, "good", {PRD: revisited(DRAFT)}, R34_BLOCK + R34_LEFT + R34_SUSPECT, set()),
    (c, "not extended", {}, R34_BLOCK + R34_LEFT + R34_SUSPECT, {"extended-to-version-2", "new-fr-from-idea-05"}),
    (c, "IDEA-05 linked at version 1", {PRD: revisited(DRAFT, idea_version=1)}, R34_BLOCK + R34_LEFT + R34_SUSPECT,
     {"new-fr-from-idea-05"}),
    (c, "IDEA-01 drafted again", {PRD: revisited(DRAFT, extra_fr=IDEA_01_AGAIN)}, R34_BLOCK + R34_LEFT + R34_SUSPECT,
     {"no-idea-redrafted"}),
    (c, "FR-001 link moved to version 2", {PRD: revisited(DRAFT, fr1_edit=(
        "      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}\n  - id: FR-002",
        "      - {id: BRN-001, item: IDEA-01, relation: derives, version: 2, hash: null}\n  - id: FR-002"))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"existing-items-unchanged"}),
    (c, "IDEA-01 drafted again at version 1", {PRD: revisited(DRAFT, extra_fr=IDEA_01_AGAIN.replace("version: 2", "version: 1"))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"no-idea-redrafted"}),
    (c, "parked IDEA-02 cited", {PRD: revisited(DRAFT, extra_fr=IDEA_01_AGAIN.replace("IDEA-01", "IDEA-02"))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"no-idea-redrafted"}),
    (c, "SM-01 target rewritten", {PRD: revisited(DRAFT, fr1_edit=('target: "95% by the end of the pilot"', 'target: "90%"'))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"existing-items-unchanged"}),
    (c, "NFR-003 deleted", {PRD: revisited(DRAFT, fr1_edit=(
        '  - id: NFR-003\n    status: active\n    category: privacy\n'
        '    statement: "Volunteer phone numbers are visible only to the coordinator."\n'
        '    priority: must\n    release: current\n', ""))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"existing-items-unchanged"}),
    (c, "line added inside FR-001", {PRD: revisited(DRAFT, fr1_edit=(
        "relation: derives, version: 1, hash: null}\n  - id: FR-002",
        "relation: derives, version: 1, hash: null}\n      - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}\n  - id: FR-002"))},
     R34_BLOCK + R34_LEFT + R34_SUSPECT, {"existing-items-unchanged"}),
    (c, "validation failed", {PRD: revisited(DRAFT)},
     "Validation failed (ERR-06): FR-001 cites BRN-001 version 1, not the current version 2.\n" + R34_LEFT + R34_SUSPECT,
     {"validation-passed"}),
]

# VER-35 no-unprocessed-brn
c = "no-unprocessed-brn"
R35 = ("No brainstorm can be turned into a PRD right now. Nothing was written.\n"
       "- BRN-002 (draft) has no promoted idea yet: converge it with /devforgeai:brainstorm.\n"
       "- BRN-001: every promoted idea is already cited by PRD-001.\n")
S += [
    (c, "good", {}, R35, set()),
    (c, "v3-like reply", {}, "Every promoted idea is already cited by a PRD, so there is nothing to process.\n",
     {"lists-brn-002-with-status", "points-to-brainstorm"}),
    (c, "PRD-002 written", {"docs/specs/prd/PRD-002.md": "---\nid: PRD-002\n---\n"}, R35, {"no-prd-002"}),
    (c, "PRD-001 changed", {PRD: edit(scaffolded(c, PRD), "version: 1\n", "version: 2\n")}, R35, {"prd-001-unchanged"}),
]

# VER-36 all-ideas-cited-stops
c = "all-ideas-cited-stops"
R36 = ("No new PRD was written: PRD-001 already cites every promoted idea of BRN-001 (IDEA-01 in FR-001, "
       "IDEA-03 in FR-002).\n")
S += [
    (c, "good", {}, R36, set()),
    (c, "PRD-002 written (v3)", {"docs/specs/prd/PRD-002.md": "---\nid: PRD-002\n---\n"},
     "PRD-002 written to docs/specs/prd/PRD-002.md (from BRN-001; new)\n", {"no-prd-002", "names-prd-001"}),
    (c, "PRD-001 changed", {PRD: edit(scaffolded(c, PRD), "version: 1\n", "version: 2\n")}, R36, {"prd-001-unchanged"}),
]

# VER-37 needs-adr-handoff: its two regex graders (copies of VER-14's); its llm grader is skipped here
c = "needs-adr-handoff"
R37 = "PRD-001 written to docs/specs/prd/PRD-001.md (from BRN-001; new)\n"
MARKER = "## 12. Open questions\n\n- [NEEDS ADR: synchronous booking writes vs scheduled import; affects FR-001, FR-002]\n"
S += [
    (c, "good", {PRD: MARKER}, R37, set()),
    (c, "marker names other FRs", {PRD: MARKER.replace("FR-001, FR-002", "FR-003")}, R37, {"marker-names-booking-fr"}),
    (c, "no marker", {PRD: "## 12. Open questions\n\n- None.\n"}, R37, {"needs-adr-marker", "marker-names-booking-fr"}),
]

# VER-38 unlinked-signal-keeps-target (issue #39)
c = "unlinked-signal-keeps-target"
SM_LINKED = new_prd().split("success_metrics:\n")[1].split("```")[0]  # the default SM-01, linked to IDEA-01
SM_SAT = ('  - id: SM-02\n    status: active\n    metric: "Average volunteer satisfaction in the quarterly survey"\n'
          '    baseline: "3.4 out of 5"\n    target: "4.0 out of 5 by the end of the pilot"\n'
          '    measured_by: "Quarterly volunteer survey"\n')
IDEA_LINK = "      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}\n"


def sat_prd(sat=SM_SAT, after=""):
    return {PRD: new_prd(sms="success_metrics:\n" + SM_LINKED + sat + after)}


R38 = "PRD-001 written to docs/specs/prd/PRD-001.md (from BRN-001; new)\n"
V38 = {"baseline-kept", "target-kept", "measured-by-survey"}
S += [
    (c, "good", sat_prd(), R38, set()),
    (c, "good, fields reordered", sat_prd(edit(SM_SAT, '    target: "4.0 out of 5 by the end of the pilot"\n    measured_by: "Quarterly volunteer survey"\n',
                                                '    measured_by: "Quarterly volunteer survey"\n    target: "4.0 out of 5 by the end of the pilot"\n')), R38, set()),
    (c, "good, an unanswered linked metric follows",
     sat_prd(after=SM_LINKED.replace("SM-01", "SM-03")), R38, set()),
    (c, "v4: target marked", sat_prd(edit(SM_SAT, '"4.0 out of 5 by the end of the pilot"',
                                          '"[NEEDS CLARIFICATION: target for average volunteer satisfaction]"')), R38, {"target-kept"}),
    (c, "target marked though 4.0 is quoted", sat_prd(edit(SM_SAT, '"4.0 out of 5 by the end of the pilot"',
                                                           '"[NEEDS CLARIFICATION: confirm 4.0 by the end of the pilot]"')), R38, {"target-kept"}),
    (c, "baseline marked", sat_prd(edit(SM_SAT, '"3.4 out of 5"', '"[NEEDS CLARIFICATION: baseline]"')), R38, {"baseline-kept"}),
    (c, "source marked", sat_prd(edit(SM_SAT, '"Quarterly volunteer survey"', '"[NEEDS CLARIFICATION: source]"')), R38, {"measured-by-survey"}),
    (c, "linked to IDEA-01", sat_prd(SM_SAT + "    upstream:\n" + IDEA_LINK), R38, {"no-upstream"}),
    (c, "linked, flow form", sat_prd(SM_SAT + "    upstream: [{id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}]\n"),
     R38, {"no-upstream"}),
    (c, "no satisfaction metric", sat_prd(""), R38, V38),
    # With no file, grade_evals.mjs fails every file grader, not_contains ones included.
    (c, "no PRD", {}, "Nothing written.", V38 | {"no-upstream"}),
]

ADDED = {"records-provenance": {"model-is-a-claude-model-id", "identity-not-unavailable", "authors-include-the-tool",
                                "changelog-session-matches"},
         "constraints-not-design": {"aws-no-brn-link", "stripe-no-brn-link"}}


def main():
    failures = 0
    for case, label, files, reply, expect in S:
        results = grade(case, files, reply)
        if case in ADDED:  # a v1 case: judge only the added graders (and every grader in the good result)
            failed = {g for g, r in results.items() if r == "FAIL" and (g in ADDED[case] or not expect)}
        else:
            failed = {g for g, r in results.items() if r == "FAIL"}
        ok = failed == expect
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {case}: {label}" + ("" if ok else f"\n     expected to fail {sorted(expect)}, failed {sorted(failed)}"))
    print(f"{len(S) - failures} of {len(S)} scenarios as expected")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
