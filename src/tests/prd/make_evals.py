"""Generates the prd eval cases added for SPEC-002 v2 (VER-24 to VER-32), v4 (VER-33 to VER-36; issues #36
and #38) and v5 (VER-38; issue #39), and the grader files added to three existing cases (VER-09
records-provenance, VER-10 constraints-not-design, VER-37 architecture-context). The 20 cases written for v1
are hand-written; this script never touches their prompts, scaffolds or existing graders, only adds the
new grader files listed in EXTRA_GRADERS.

Fixtures are defined once here, except two that are parsed from existing v1 scaffolds so there is one
copy: the Riverside Food Bank BRN-001 (from invalid-policy-stops, shared by 13 v1 cases) and VER-06's
Ledgerly PRD-001 and BRN-002 (from extend-or-new). Every fixture is validated against src/schemas/
before anything is written. A fixture that is invalid on purpose must fail in exactly the expected
place (VER-27's FR-001 priority), and every policy fixture also goes through the skill's own
scripts/validate_policy.py (VER-28 to VER-31 must fail on the named field). Run from the repository
root:

    PYTHONDONTWRITEBYTECODE=1 python3 src/tests/prd/make_evals.py
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path("src/claude/DevForgeAI/evals/prd")
SCHEMAS = Path("src/schemas")
VALIDATE_POLICY = Path("src/claude/DevForgeAI/skills/prd/scripts/validate_policy.py")
TOOLS = "[Skill, Read, Glob, Grep, Write, Edit, Bash]"
PRD = "docs/specs/prd/PRD-001.md"


def replace(text, old, new):
    assert text.count(old) == 1, f"fixture edit anchor not unique: {old!r}"
    return text.replace(old, new)


def scaffold_fixtures(case):
    """The heredoc fixtures a v1 scaffold writes, by path."""
    text = (ROOT / case / "scaffold.sh").read_text()
    return dict(re.findall(r"cat > (\S+) <<'FIXTURE'\n(.*?)FIXTURE\n", text, re.S))


# --- Fixtures -------------------------------------------------------------------------------------

BRN_FOOD = scaffold_fixtures("invalid-policy-stops")["docs/specs/brainstorm/BRN-001.md"]
_LEDGERLY = scaffold_fixtures("extend-or-new")
BRN_LEDGERLY_1 = _LEDGERLY["docs/specs/brainstorm/BRN-001.md"]
PRD_LEDGERLY = _LEDGERLY["docs/specs/prd/PRD-001.md"]
BRN_LEDGERLY_2 = _LEDGERLY["docs/specs/brainstorm/BRN-002.md"]

# A second brainstorm for the same initiative and owner as the food bank's PRD-001 (VER-27, VER-32).
BRN_FOOD_2 = """\
---
id: BRN-002
type: brainstorm
title: "Shift swaps for Riverside Food Bank volunteers"
status: converged
version: 1
created: 2026-09-22
updated: 2026-09-23
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: ""
approved_on: null
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- brainstorm-specific ---
participants: ["Priya Nair"]
sources: ["Coordinator call log, September 2026"]
---

# BRN-002 — Shift swaps for Riverside Food Bank volunteers

## 1. Context

Volunteers now book warehouse shifts online (PRD-001). When a volunteer can't make a booked shift, they
still phone the coordinator, who rings round for cover.

## 2. Problems

```yaml items
problems:
  - id: PRB-01
    status: active
    statement: "A volunteer who can't make a booked shift must phone the coordinator to find cover"
    who: "Volunteer"
    evidence: "Coordinator call log, September 2026"
    severity: medium
```

## 3. Target users

Volunteers who have booked shifts, and the shift coordinator.

## 4. Ideas

```yaml items
ideas:
  - id: IDEA-01
    status: active
    idea: "A volunteer offers a booked shift for swap, and another volunteer takes it online"
    addresses:
      - PRB-01
    value: "high"
    effort: "medium"
    risk: "low"
    score: null
    disposition: promoted
    reason: "Removes most cover calls"
  - id: IDEA-02
    status: active
    idea: "Automatic cover suggestions based on each volunteer's past shifts"
    addresses:
      - PRB-01
    value: "medium"
    effort: "high"
    risk: "medium"
    score: null
    disposition: parked
    reason: "Wait until swaps are in use"
```

## 5. Evaluation method

Value, effort and risk rated high, medium or low with the coordinator (diverge-converge).

## 6. Convergence

Online swaps were promoted. Automatic cover suggestions were parked.

## 7. Assumptions and open questions

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "We believe that volunteers will take swapped shifts without the coordinator asking them."
    validation: "Share of swap offers taken within 24 hours in the first month"
    state: open
```

- None.

## 8. Candidate success signals

- Fewer calls to the coordinator about cover.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
| 1 | 2026-09-23 | claude-code (session fixture-session) | Converged |
"""


def food_prd(fr_001_priority="must"):
    """The approved food bank PRD-001, as the skill writes one, then reviewed and approved (VER-27, VER-32)."""
    return f"""\
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: approved
version: 1
created: 2026-09-14
updated: 2026-09-20
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Marcus Lee"]
approved_by: "Priya Nair"
approved_on: 2026-09-20
upstream:
  - {{id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}}
  - {{id: BRN-001, item: PRB-02, relation: derives, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Pilot"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Volunteers see open warehouse shifts and sign up online, and get a text reminder the day before, so
fewer shifts start short-staffed.

## 2. Problem and opportunity

Volunteers can only sign up by phoning the coordinator, so shifts go unfilled (BRN-001#PRB-01), and
volunteers forget shifts they signed up for, so the warehouse runs short-staffed (BRN-001#PRB-02).

## 3. Users and personas

About 120 active volunteers who pick their own shifts, and the shift coordinator who manages the rota.

## 4. Goals and non-goals

**Goals**
- Most shifts are filled online, without phone calls.
- Fewer volunteer no-shows.

**Non-goals** (explicitly out of scope)
- A native mobile app (rejected in the brainstorm).
- Badges and a leaderboard (parked in the brainstorm).

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of shifts that start fully staffed"
    baseline: "83%"
    target: "95% by the end of the pilot"
    measured_by: "Coordinator's shift log"
    upstream:
      - {{id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}}
  - id: SM-02
    status: active
    metric: "Volunteer no-shows per month"
    baseline: "14"
    target: "7 by the end of the pilot"
    measured_by: "Coordinator's no-show tally"
    upstream:
      - {{id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall show volunteers the open warehouse shifts and let them sign up online."
    priority: {fr_001_priority}
    release: current
    notes: null
    upstream:
      - {{id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}}
  - id: FR-002
    status: active
    statement: "The system shall send each signed-up volunteer a text reminder the day before their shift."
    priority: should
    release: current
    notes: null
    upstream:
      - {{id: BRN-001, item: IDEA-03, relation: derives, version: 1, hash: null}}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: constraint
    statement: "The system runs on hosted services, because the food bank has no on-site server (applies to the whole product)."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: security
    statement: "A volunteer signs in before they can sign up for a shift."
    priority: must
    release: current
  - id: NFR-003
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
```

## 8. User experience

Mobile-friendly web pages; no app to install.

## 9. Constraints and dependencies

NFR-001 records the hosting constraint.

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

Pilot with the Tuesday and Thursday shifts, then every shift.

## 12. Open questions

- None.

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
{EARLIER_ROWS}"""


EARLIER_ROWS = (
    "| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: "
    "interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
    "quality.required_categories=floor only (default) | all |\n"
    "| 1 | 2026-09-19 | Marcus Lee | Reviewed: no changes requested | none |\n"
    "| 1 | 2026-09-20 | Priya Nair | Approved | status |\n")
PRD_FOOD = food_prd()
PRD_FOOD_BAD = food_prd("high")  # VER-27: a priority the self-check rejects, in an item an extension can't touch
FR_001_BAD = re.search(r"  - id: FR-001\n(?:    [^\n]*\n)+?(?=  - id:)", PRD_FOOD_BAD).group(0)
PRD_FOOD_BAD_DATE = PRD_FOOD.replace("updated: 2026-09-20", "updated: 2026-02-30")  # issue #15; no case uses it

# VER-34: the food bank brainstorm revisited after PRD-001 was written, with a new problem and a new promoted idea.
BRN_FOOD_V2 = BRN_FOOD
for _old, _new in [
    ("version: 1\ncreated: 2026-09-10\nupdated: 2026-09-12\n", "version: 2\ncreated: 2026-09-10\nupdated: 2026-09-24\n"),
    ("    severity: medium\n```\n\n## 3. Target users",
     "    severity: medium\n"
     "  - id: PRB-03\n    status: active\n"
     '    statement: "Volunteers without forklift or food-safety training sign up for shifts that need it"\n'
     '    who: "Shift coordinator"\n    evidence: "Coordinator notes, September 2026"\n    severity: medium\n'
     "```\n\n## 3. Target users"),
    ('    reason: "A mobile-friendly website covers the need"\n```',
     '    reason: "A mobile-friendly website covers the need"\n'
     "  - id: IDEA-05\n    status: active\n"
     '    idea: "Each shift lists the training it needs, and only volunteers with that training can sign up for it"\n'
     '    addresses:\n      - PRB-03\n    value: "high"\n    effort: "medium"\n    risk: "low"\n    score: null\n'
     '    disposition: promoted\n    reason: "Stops untrained sign-ups for forklift and food-safety shifts"\n```'),
    ("A native app was rejected.", "A native app was rejected. Revisited on 2026-09-24: shift training requirements were promoted."),
    ("| 1 | 2026-09-12 | claude-code (session fixture-session) | Converged |\n",
     "| 1 | 2026-09-12 | claude-code (session fixture-session) | Converged |\n"
     "| 2 | 2026-09-24 | claude-code (session fixture-session) | Revisited: PRB-03 and IDEA-05 added, IDEA-05 promoted |\n"),
]:
    BRN_FOOD_V2 = replace(BRN_FOOD_V2, _old, _new)
# VER-34: the same PRD-001 before review and approval, so that extending it raises no BEH-09 suspect-epic warning,
# which would also match the suspect-link grader.
PRD_FOOD_DRAFT = PRD_FOOD
for _old, _new in [
    ("status: approved\n", "status: draft\n"),
    ('reviewed_by: ["Marcus Lee"]\napproved_by: "Priya Nair"\napproved_on: 2026-09-20\n',
     'reviewed_by: []\napproved_by: ""\napproved_on: null\n'),
    ("| 1 | 2026-09-19 | Marcus Lee | Reviewed: no changes requested | none |\n"
     "| 1 | 2026-09-20 | Priya Nair | Approved | status |\n", ""),
]:
    PRD_FOOD_DRAFT = replace(PRD_FOOD_DRAFT, _old, _new)
# Every item PRD_FOOD_DRAFT holds, in file order; an extension must leave each one byte-identical.
DRAFT_ITEMS = [re.search(rf"  - id: {i}\n(?:    [^\n]*\n)+", PRD_FOOD_DRAFT).group(0)
               for i in ("SM-01", "SM-02", "FR-001", "FR-002", "NFR-001", "NFR-002", "NFR-003", "ASM-01")]
# VER-35: a second brainstorm still in progress: a draft whose ideas are all open, so nothing is promoted.
BRN_FOOD_2_DRAFT = BRN_FOOD_2
for _old, _new in [
    ("status: converged\n", "status: draft\n"),
    ('    disposition: promoted\n    reason: "Removes most cover calls"\n', "    disposition: open\n    reason: null\n"),
    ('    disposition: parked\n    reason: "Wait until swaps are in use"\n', "    disposition: open\n    reason: null\n"),
    ("Online swaps were promoted. Automatic cover suggestions were parked.", "Not converged yet: both ideas are open."),
    ("| 1 | 2026-09-23 | claude-code (session fixture-session) | Converged |\n",
     "| 1 | 2026-09-23 | claude-code (session fixture-session) | Draft |\n"),
]:
    BRN_FOOD_2_DRAFT = replace(BRN_FOOD_2_DRAFT, _old, _new)
# VER-38 (issue #39): one more candidate success signal, which measures no promoted idea and gives its own numbers.
BRN_FOOD_SIGNAL = replace(BRN_FOOD, "- Fewer volunteer no-shows.\n",
                          "- Fewer volunteer no-shows.\n- Volunteer satisfaction overall, not tied to any one idea: the "
                          "quarterly volunteer survey averages 3.4 out of 5 today, and the board's target is 4.0 by the "
                          "end of the pilot.\n")
# VER-33: a workspace with no docs/specs/ at all, only a README naming the product.
README_VOLUNTEER = ("# Riverside Food Bank volunteer app\n\n"
                    "A web app where food bank volunteers see open warehouse shifts and sign up for them.\n")


def policy(settings, *, updated="2026-09-01", authors='["Architecture board"]',
           upstream="  - {id: ADR-104, relation: constrains, version: 2, hash: null}"):
    """An approved, vendored organization policy."""
    return f"""\
---
id: POL-001
type: policy
title: "Harbor engineering policy (vendored)"
status: approved
version: 1
created: 2026-06-01
updated: {updated}
owner: "Architecture board"
authors: {authors}
reviewed_by: ["Architecture board"]
approved_by: "CTO"
approved_on: 2026-09-01
upstream:
{upstream}
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {{repository: "github.com/harbor/engineering-policy", ref: "v1.0.0"}}
---

# POL-001 — Harbor engineering policy (vendored)

## 1. Scope and ownership

Applies to every product in this repository.

## 2. Settings

```yaml items
settings:
{settings}```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-09-01 | Architecture board | Current settings | all |
"""


MAX_CALLS = """\
  - id: SET-01
    status: active
    key: interview.max_calls
    class: interaction_default
    value: 6
    overridable_by:
      - project
      - local
    rationale: "Keep interviews short"
"""
COMPLIANCE = """\
  - id: SET-01
    status: active
    key: quality.required_categories
    class: organizational_policy
    value:
      - compliance
    applies_when:
      operating_context:
        - internal
        - pilot
        - production
    overridable_by: []
    rationale: "SOC 2 scope covers internal tools"
"""
POL_BASE = policy(MAX_CALLS)
POL_COMPLIANCE = policy(COMPLIANCE)
POL_BAD_DATE = policy(MAX_CALLS, updated="2026-13-45")
POL_BAD_AUTHORS = policy(MAX_CALLS, authors='"Architecture board"')
POL_BAD_LINK = policy(MAX_CALLS, upstream="  - {id: ADR-104, version: 2, hash: null}")
POL_BAD_TYPE = policy(MAX_CALLS.replace("    value: 6\n", '    value: "eight"\n'))

# --- Fixture validation ---------------------------------------------------------------------------


class _Loader(yaml.SafeLoader):
    """Keeps dates as strings, as the schemas expect."""


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def validate(label, text, schema, expect=()):
    """Validates a fixture; `expect` lists the schema error paths a fixture invalid on purpose must have."""
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    doc = {"frontmatter": yaml.load(m.group(1), Loader=_Loader)}
    for block in re.findall(r"```yaml items\n(.*?)```", text, re.S):
        for key, value in yaml.load(block, Loader=_Loader).items():
            doc.setdefault(key, []).extend(value)
    registry = Registry()
    for p in SCHEMAS.glob("*.json"):
        s = json.loads(p.read_text())
        registry = registry.with_resource(s["$id"], Resource.from_contents(s)).with_resource(
            p.name, Resource.from_contents(s))
    found = Draft202012Validator(json.loads((SCHEMAS / schema).read_text()), registry=registry,
                                 format_checker=FormatChecker()).iter_errors(doc)
    errors = {tuple(e.path): e.message for e in found}
    assert set(errors) == set(expect), f"{label} against {schema}: expected errors at {list(expect)}, got {errors}"
    assert "\nFIXTURE\n" not in text, f"{label} contains the heredoc delimiter"


def check_policy_script(label, text, expect=None):
    """Runs the skill's validate_policy.py on one policy fixture: exit 0, or exit 1 with an error line naming
    `expect` ("<part>: <field>")."""
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "POL-001.md").write_text(text)
        p = subprocess.run([sys.executable, "-B", str(VALIDATE_POLICY), tmp], capture_output=True, text=True)
    if expect is None:
        assert p.returncode == 0, f"{label}: the policy script rejects a fixture meant to be valid:\n{p.stdout}"
    else:
        assert p.returncode == 1 and f": {expect}: " in p.stdout, f"{label}: expected '{expect}' error:\n{p.stdout}"


FIXTURES = {
    "BRN_FOOD": (BRN_FOOD, "brainstorm.schema.json"), "BRN_FOOD_2": (BRN_FOOD_2, "brainstorm.schema.json"),
    "BRN_LEDGERLY_1": (BRN_LEDGERLY_1, "brainstorm.schema.json"),
    "BRN_LEDGERLY_2": (BRN_LEDGERLY_2, "brainstorm.schema.json"),
    "PRD_LEDGERLY": (PRD_LEDGERLY, "prd.schema.json"), "PRD_FOOD": (PRD_FOOD, "prd.schema.json"),
    "PRD_FOOD_BAD": (PRD_FOOD_BAD, "prd.schema.json", [("functional_requirements", 0, "priority")]),
    "PRD_FOOD_BAD_DATE": (PRD_FOOD_BAD_DATE, "prd.schema.json", [("frontmatter", "updated")]),
    "BRN_FOOD_V2": (BRN_FOOD_V2, "brainstorm.schema.json"),
    "BRN_FOOD_2_DRAFT": (BRN_FOOD_2_DRAFT, "brainstorm.schema.json"), "PRD_FOOD_DRAFT": (PRD_FOOD_DRAFT, "prd.schema.json"),
    "BRN_FOOD_SIGNAL": (BRN_FOOD_SIGNAL, "brainstorm.schema.json"),
    "POL_BASE": (POL_BASE, "policy.schema.json"), "POL_COMPLIANCE": (POL_COMPLIANCE, "policy.schema.json"),
    "POL_BAD_DATE": (POL_BAD_DATE, "policy.schema.json", [("frontmatter", "updated")]),
    "POL_BAD_AUTHORS": (POL_BAD_AUTHORS, "policy.schema.json", [("frontmatter", "authors")]),
    "POL_BAD_LINK": (POL_BAD_LINK, "policy.schema.json", [("frontmatter", "upstream", 0)]),
    "POL_BAD_TYPE": (POL_BAD_TYPE, "policy.schema.json", [("settings", 0, "value")]),
}
POLICY_SCRIPT = {
    "POL_BASE": None, "POL_COMPLIANCE": None,
    "POL_BAD_DATE": "frontmatter: updated", "POL_BAD_AUTHORS": "frontmatter: authors",
    "POL_BAD_LINK": "frontmatter: upstream[0].relation", "POL_BAD_TYPE": "SET-01 (interview.max_calls): value",
}

# --- Graders --------------------------------------------------------------------------------------

ITEM = r"(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?"  # the rest of one item's lines, never the next item
# "no regulation applies" and "no compliance requirement is needed" record a none too (SKL-002 v4's pass C:
# 2 of 3 VER-25 runs wrote them and failed the narrower pattern).
NONE_WORDS = (r"(?:\b[Nn]one\b|\b[Nn]othing\b|\b[Nn]o (?:additional|further|extra|separate|specific|dedicated)\b"
              r"|\b[Nn]ot needed\b|\bbeyond (?:the|what)\b"
              r"|\b[Nn]o [a-z-]+(?: [a-z-]+){0,3} (?:applies|apply|is needed|are needed|is required|are required)\b)")


def prose_none(category):
    """Section 7 prose (not an indented YAML line) recording the user's none for a category."""
    cat = f"[{category[0].upper()}{category[0]}]{category[1:]}"
    return (rf"## 7\. Non-functional requirements\n(?:(?!## )[^\n]*\n)*?(?=[^ \t\n`])[^\n]*\b{cat}\b[^\n]*{NONE_WORDS}"
            rf"|## 7\. Non-functional requirements\n(?:(?!## )[^\n]*\n)*?(?=[^ \t\n`])[^\n]*{NONE_WORDS}[^\n]*\b{cat}\b")


def lit(text):
    """A one-line regex that matches `text` literally, with newlines written as \\n."""
    return re.sub(r"([\\^$.|?*+()\[\]{}])", r"\\\1", text).replace("\n", r"\n")


def regex(target, match, pattern, flags=None):
    t = target if target == "last_message" else "{source: file, path: %s}" % target
    fl = f"flags: {flags}\n" if flags else ""
    return f"---\ntype: regex\ntarget: {t}\nmatch: {match}\n{fl}---\n{pattern}\n"


def exists(path, value):
    return f"---\ntype: file_exists\npath: {path}\nexists: {str(value).lower()}\n---\n"


def llm(body):
    return f"---\ntype: llm\n---\n\n{body}"


NO_PRD = exists(PRD, False)
PRD_EXISTS = exists(PRD, True)
IN_REVIEW = regex(PRD, "contains", r"^status: in-review[ \t]*$", "m")
APPROVAL_CLEARED = regex(PRD, "contains", r'^approved_by: ""[ \t]*\n^approved_on: null[ \t]*$', "m")
POLICY_PROMPT = "Write the PRD for BRN-001. Proceed without questions.\n"
SKILL_FIRED = (ROOT / "selects-unprocessed-brn" / "graders" / "skill-fired.md").read_text()
# Each block, then the next item or the end of its fence, so a line added inside an item also fails.
ITEMS_UNCHANGED = r"[\s\S]*".join(lit(b) + r"(?=  - id:|```)" for b in DRAFT_ITEMS)
REVISITED_CONTEXT = """\
Context the reply was written in: BRN-001 is at version 2. Its promoted ideas IDEA-01 and IDEA-03 are
already cited by the draft PRD-001 (IDEA-01 by FR-001 and SM-01, IDEA-03 by FR-002 and SM-02) at BRN-001
version 1, and its new promoted IDEA-05 isn't cited yet. The user asked to extend PRD-001 from BRN-001 and
to proceed without questions. A correct run adds requirements for IDEA-05 only and passes validation.

"""
EXTEND_PROMPT = "Extend PRD-001 from BRN-002. Proceed without questions.\n"
# VER-38: the start of the success metric whose metric names volunteer satisfaction, in any field order.
SATISFACTION_SM = rf'- id: SM-\d{{2}}\n(?={ITEM}[ \t]+metric: "[^"\n]*[Ss]atisfaction)'


def policy_case(ver, fixture, what, field_graders):
    return {
        "ver": ver, "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/policy/POL-001.md": fixture},
        "prompt": POLICY_PROMPT,
        "description": f"VER-{ver}: an approved policy whose {what} makes the skill stop, write no PRD, and name the file and the field.",
        "graders": {"no-prd-written": NO_PRD, "names-file": regex("last_message", "contains", r"POL-001"),
                    **field_graders},
    }


CASES = {
    "quality-answers-kept-apart": {
        "ver": "24", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD},
        "prompt": "Write the PRD for BRN-001. The operating context is internal: only our coordinator and volunteers\n"
                  "use it, with real volunteer data. Security needs nothing beyond what the hosting platform already\n"
                  "gives us. Track the share of shifts filled online as a success metric; there's no target yet.\n"
                  "Proceed without questions.\n",
        "description": "VER-24: an explicit none for security, no privacy answer and a metric with no target yet are kept apart: no security NFR and the none recorded in section 7's prose, a privacy marker, and the metric kept with a marked target.",
        "graders": {
            "prd-exists": PRD_EXISTS,
            "context-internal": regex(PRD, "contains", r"^operating_context: internal\b", "m"),
            "no-security-nfr": regex(PRD, "not_contains", r"category: security\b"),
            "security-none-in-prose": regex(PRD, "contains", prose_none("security")),
            "security-not-marked-unanswered": regex(PRD, "not_contains", r"\[NEEDS CLARIFICATION: security requirements"),
            "privacy-marker": regex(PRD, "contains", r"## 12\. Open questions[\s\S]*\[NEEDS CLARIFICATION: privacy "
                                                     r"requirements for internal\][\s\S]*## 13\. Epic map"),
            "no-privacy-nfr": regex(PRD, "not_contains", r"category: privacy\b"),
            "metric-target-marked": regex(PRD, "contains", rf'- id: SM-\d{{2}}\n{ITEM}[ \t]+metric: "[^"\n]*(?:[Oo]nline|'
                                                           rf'[Ff]illed)[^"\n]*"\n{ITEM}[ \t]+target: "\[NEEDS CLARIFICATION:'),
        },
    },
    "none-does-not-waive-policy": {
        "ver": "25",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/policy/POL-001.md": POL_COMPLIANCE},
        "prompt": "Write the PRD for BRN-001. The operating context is internal. Compliance: none, no regulation\n"
                  "applies to us. Proceed without questions.\n",
        "description": "VER-25: the organization policy requires compliance for internal; the user answers compliance 'none'. The PRD invents no compliance NFR, records the none, and keeps a NEEDS CLARIFICATION marker naming the policy setting.",
        "graders": {
            "prd-exists": PRD_EXISTS,
            "no-compliance-nfr": regex(PRD, "not_contains", r"category: compliance\b"),
            "compliance-none-recorded": regex(PRD, "contains", prose_none("compliance")),
            "marker-names-setting": regex(PRD, "contains",
                                          r"\[NEEDS CLARIFICATION:[^\]\n]*[Cc]ompliance[^\]\n]*SET-01[^\]\n]*\]"
                                          r"|\[NEEDS CLARIFICATION:[^\]\n]*SET-01[^\]\n]*[Cc]ompliance[^\]\n]*\]"),
        },
    },
    "stated-choice-honored": {
        "ver": "26",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_LEDGERLY_1, "docs/specs/prd/PRD-001.md": PRD_LEDGERLY,
                  "docs/specs/brainstorm/BRN-002.md": BRN_LEDGERLY_2},
        "prompt": "Write a new PRD for BRN-002. Proceed without questions.\n",
        "description": "VER-26: with VER-06's fixture, a request that says to write a new PRD for BRN-002 is followed without asking: PRD-002 is written, PRD-001 stays at version 1, and the reply names the request as the source of the choice.",
        "graders": {
            "prd-002-exists": exists("docs/specs/prd/PRD-002.md", True),
            "prd-002-from-brn-002": regex("docs/specs/prd/PRD-002.md", "contains", r"\{id: BRN-002, item: IDEA-\d{2}, relation: derives"),
            "prd-001-unchanged": regex(PRD, "contains", r"^status: approved\n^version: 1\n^created: 2026-08-05\n^updated: 2026-08-20\n", "m"),
            "names-request-as-source": regex(
                "last_message", "contains",
                r"(?:[Nn]ew PRD|PRD-002)[^\n.]{0,120}(?:\brequest|\byou (?:asked|said|chose|stated|requested)|\bas "
                r"(?:you )?(?:asked|instructed|requested)|\byour (?:instruction|choice|prompt|message))"
                r"|(?:\b[Rr]equest|\b[Yy]ou (?:asked|said|chose|stated|requested)|\b[Aa]s (?:you )?(?:asked|instructed|requested)"
                r"|\b[Yy]our (?:instruction|choice|prompt|message))[^\n.]{0,120}(?:new PRD|PRD-002)"),
        },
    },
    "failed-extension-stays-in-review": {
        "ver": "27",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/prd/PRD-001.md": PRD_FOOD_BAD,
                  "docs/specs/brainstorm/BRN-002.md": BRN_FOOD_2},
        "prompt": EXTEND_PROMPT,
        "description": "VER-27: extending the approved PRD-001, whose existing FR-001 has a priority the self-check rejects, fails validation; PRD-001 ends in-review with its approval cleared and FR-001 unchanged, and the reply lists the checks, repairs and error and doesn't present the PRD as ready for the architecture step.",
        "graders": {
            "prd-in-review": IN_REVIEW,
            "approval-cleared": APPROVAL_CLEARED,
            "fr-001-unchanged": regex(PRD, "contains", lit(FR_001_BAD)),
            "reply-names-fr-001": regex("last_message", "contains", r"FR-001"),
            "failure-report": llm("""\
Context the reply was written in: PRD-001 was an approved PRD. Its existing requirement FR-001 has
`priority: high`, a value the self-check rejects (priority must be must, should, could, wont or null).
The user asked to extend PRD-001 from BRN-002, a brainstorm of the same initiative, and to proceed
without questions. An extension must leave existing items byte-identical, so no repair within the
extension rules can fix FR-001, and validation fails.

Judge only the final reply. PASS if all of these hold:
- It reports that validation failed and names the unresolved error in FR-001 (its priority value).
- It lists the validation checks it made and any repairs, and there are at most four checks: an
  initial check plus at most three repair cycles. Stopping early because the error can't be
  repaired is fine.
- It says PRD-001 is left in-review (not approved), with its approval cleared.
- It doesn't present the PRD as ready for the architecture step: it doesn't tell the user to run
  /devforgeai:architecture now, and doesn't call the PRD valid or complete.
FAIL if any of these fails, or if the reply says it changed FR-001.
"""),
        },
    },
    "policy-bad-date": policy_case("28", POL_BAD_DATE, "updated date is 2026-13-45",
                                   {"names-field": regex("last_message", "contains", r"\bupdated\b")}),
    "policy-bad-authors": policy_case("29", POL_BAD_AUTHORS, "authors is a string, not a list,",
                                      {"names-field": regex("last_message", "contains", r"\bauthors\b")}),
    "policy-bad-link": policy_case("30", POL_BAD_LINK, "upstream link record has no relation",
                                   {"names-field": regex("last_message", "contains", r"\brelation\b")}),
    "policy-bad-type": policy_case("31", POL_BAD_TYPE, "interview.max_calls value is the string 'eight'",
                                   {"names-setting": regex("last_message", "contains", r"SET-01"),
                                    "names-field": regex("last_message", "contains", r"\bvalue\b")}),
    "extension-keeps-review-history": {
        "ver": "32",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/prd/PRD-001.md": PRD_FOOD,
                  "docs/specs/brainstorm/BRN-002.md": BRN_FOOD_2},
        "prompt": EXTEND_PROMPT,
        "description": "VER-32: extending the approved, reviewed PRD-001 keeps its authors, reviewed_by and earlier Change Log rows, returns it to in-review with the approval cleared, and the new Change Log row says the revision hasn't been reviewed.",
        "graders": {
            "extended-to-version-2": regex(PRD, "contains", r"^version: 2[ \t]*$", "m"),
            "new-fr-from-brn-002": regex(PRD, "contains", r"\{id: BRN-002, item: IDEA-01, relation: derives, version: 1, hash: null\}"),
            "prd-in-review": IN_REVIEW,
            "approval-cleared": APPROVAL_CLEARED,
            "authors-unchanged": regex(PRD, "contains", r'^authors: \["Priya Nair", "claude-code"\][ \t]*$', "m"),
            "reviewed-by-unchanged": regex(PRD, "contains", r'^reviewed_by: \["Marcus Lee"\][ \t]*$', "m"),
            "earlier-rows-unchanged": regex(PRD, "contains", lit(EARLIER_ROWS)),
            "new-row-unreviewed": regex(PRD, "contains",
                                        r"\n\| 2 \| \d{4}-\d{2}-\d{2} \| claude-code \(session [^)\n]+\) \|[^\n]*"
                                        r"(?:(?:has not|hasn't|have not|not)(?: yet)? been reviewed|[Uu]nreviewed)"),
        },
    },
    "no-brainstorm-yet": {
        "ver": "33", "files": {"README.md": README_VOLUNTEER},
        "prompt": "Let's write the PRD for our volunteer app.\n",
        "description": "VER-33: with no brainstorm in the workspace and no BRN named, the skill says that no brainstorm exists yet, points to /devforgeai:brainstorm, never says that promoted ideas are already cited, and writes no PRD.",
        "graders": {
            "skill-fired": SKILL_FIRED,
            "points-to-brainstorm": regex("last_message", "contains", r"/devforgeai:brainstorm\b"),
            "never-says-already-cited": regex("last_message", "not_contains", r"already cited", "i"),
            "no-prd-written": NO_PRD,
            "no-docs-written": exists("docs/**", False),
            "no-root-prd": exists("PRD.md", False),
            "says-no-brainstorm": llm("""\
Context the reply was written in: the workspace has no docs/specs/ folder, so no brainstorm (BRN)
document exists. The user asked to write a PRD and named no brainstorm.

Judge only the final reply. PASS if all of these hold:
- It says that no brainstorm exists yet, or that there is no BRN to turn into a PRD.
- It tells the user to start with /devforgeai:brainstorm.
- It doesn't present a PRD as written.
FAIL if any of these fails, or if it says that promoted ideas are already cited by a PRD.
"""),
        },
    },
    "revisited-brainstorm-extends": {
        "ver": "34",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD_V2, "docs/specs/prd/PRD-001.md": PRD_FOOD_DRAFT},
        "prompt": "Extend PRD-001 from BRN-001. Proceed without questions.\n",
        "description": "VER-34: BRN-001 version 2 adds a promoted IDEA-05; extending the draft PRD-001, which cites IDEA-01 and IDEA-03 at version 1, drafts FRs from IDEA-05 only, leaves the existing items unchanged, passes validation, and reports the version 1 links as suspect.",
        "graders": {
            "extended-to-version-2": regex(PRD, "contains", r"^version: 2[ \t]*$", "m"),
            "new-fr-from-idea-05": regex(PRD, "contains", rf"- id: FR-\d{{3}}\n{ITEM}[ \t]+- \{{id: BRN-001, item: IDEA-05, "
                                                          r"relation: derives, version: 2, hash: null\}"),
            # The draft cites IDEA-01 and IDEA-03 twice each (an FR and an SM); a third citation, at any version,
            # is a re-drafted item. The parked IDEA-02 and rejected IDEA-04 never appear.
            "no-idea-redrafted": regex(PRD, "not_contains", r"(?:item: IDEA-01,[\s\S]*){3}|(?:item: IDEA-03,[\s\S]*){3}"
                                                            r"|IDEA-0[24]\b"),
            "existing-items-unchanged": regex(PRD, "contains", ITEMS_UNCHANGED),
            "validation-passed": regex("last_message", "contains", r"Validation:\**[ \t]*passed", "i"),
            # llm graders keep the reply as evidence (Bryan, 2026-10-01: the first v3 run failed two regexes here
            # and kept no copy of the reply). One duty each, so a reply that misses both scores 5 of 7, below 0.8.
            "reply-names-left-out-ideas": llm(REVISITED_CONTEXT + """\
Judge only the final reply. PASS if it names both IDEA-01 and IDEA-03, by ID, as left out (not drafted
again) because PRD-001 already cites them, and names for each a PRD-001 item that cites it (FR-001 or SM-01
for IDEA-01; FR-002 or SM-02 for IDEA-03). Any wording counts, such as "IDEA-01 left out: PRD-001#FR-001
cites it" or "IDEA-01 and IDEA-03 are already covered by FR-001 and FR-002".
FAIL if either ID or its citing item is missing, or if the reply says it drafted new requirements from
IDEA-01 or IDEA-03.
"""),
            "reply-reports-suspect-links": llm(REVISITED_CONTEXT + """\
Judge only the final reply. PASS if it tells the user that PRD-001's existing links to BRN-001 cite
version 1 while BRN-001 is now at version 2, so they point to an older version and need review. Any wording
counts; the word "suspect" isn't required, and the reply needn't list every such link.
FAIL if the reply doesn't mention them, or if it counts them as validation errors, as repairs, or as a
reason a check failed.
"""),
        },
    },
    "no-unprocessed-brn": {
        "ver": "35",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/prd/PRD-001.md": PRD_FOOD,
                  "docs/specs/brainstorm/BRN-002.md": BRN_FOOD_2_DRAFT},
        "prompt": "Let's write the next PRD from our brainstorms.\n",
        "description": "VER-35: no BRN can be processed, for two reasons: PRD-001 cites every promoted idea of BRN-001, and BRN-002 is a draft with only open ideas. The skill lists BRN-002 with its status, points to /devforgeai:brainstorm, says BRN-001's ideas are already cited by PRD-001, and writes nothing.",
        "graders": {
            "skill-fired": SKILL_FIRED,
            "lists-brn-002-with-status": regex("last_message", "contains",
                                               r"BRN-002[^\n]{0,200}\b(?:draft|not converged|open)\b"
                                               r"|\b(?:draft|not converged)\b[^\n]{0,200}BRN-002", "i"),
            "points-to-brainstorm": regex("last_message", "contains", r"/devforgeai:brainstorm\b"),
            "no-prd-002": exists("docs/specs/prd/PRD-002.md", False),
            "prd-001-unchanged": regex(PRD, "contains", lit(PRD_FOOD)),
            "reply-explains-both-brns": llm("""\
Context the reply was written in: BRN-001's promoted ideas (IDEA-01 and IDEA-03) are all cited by PRD-001.
BRN-002 is a draft brainstorm whose ideas are all open, so it has no promoted idea. The user asked to write
the next PRD and named no brainstorm, so no BRN can be processed.

Judge only the final reply. PASS if all of these hold:
- It says that BRN-002 has no promoted idea yet (a draft, not converged) and points to /devforgeai:brainstorm
  to converge it.
- It says that BRN-001's promoted ideas are already cited by PRD-001.
- It doesn't present a PRD as written.
FAIL if any of these fails, or if it offers BRN-001 or BRN-002 as ready to turn into a PRD.
"""),
        },
    },
    "all-ideas-cited-stops": {
        "ver": "36",
        "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD, "docs/specs/prd/PRD-001.md": PRD_FOOD},
        "prompt": "Write a new PRD for BRN-001. Proceed without questions.\n",
        "description": "VER-36: PRD-001 already cites every promoted idea of BRN-001, so a stated request for a new PRD from BRN-001 stops under ERR-04: no PRD-002, PRD-001 unchanged, and the reply says PRD-001 already cites them.",
        "graders": {
            "no-prd-002": exists("docs/specs/prd/PRD-002.md", False),
            "prd-001-unchanged": regex(PRD, "contains", lit(PRD_FOOD)),
            "names-prd-001": regex("last_message", "contains", r"PRD-001\b"),
            "reply-says-all-cited": llm("""\
Context the reply was written in: BRN-001's promoted ideas are IDEA-01 and IDEA-03, and PRD-001 already
cites both. The user asked for a new PRD from BRN-001 and said to proceed without questions.

Judge only the final reply. PASS if it says that no new PRD was written because PRD-001 already cites every
promoted idea of BRN-001 (any wording), and doesn't present a new PRD as written.
FAIL if it presents a PRD-002 or any other new PRD as written, or doesn't give that reason.
"""),
        },
    },
    "unlinked-signal-keeps-target": {
        "ver": "38", "files": {"docs/specs/brainstorm/BRN-001.md": BRN_FOOD_SIGNAL},
        "prompt": POLICY_PROMPT,
        "description": "VER-38 (issue #39): a candidate success signal that measures no promoted idea gives its own baseline, target and source; its metric keeps them, with no NEEDS CLARIFICATION target and no upstream link.",
        "graders": {
            "prd-exists": PRD_EXISTS,
            "satisfaction-metric": regex(PRD, "contains", SATISFACTION_SM),
            "baseline-kept": regex(PRD, "contains", rf'{SATISFACTION_SM}{ITEM}[ \t]+baseline: "[^"\n]*\b3\.4\b'),
            "target-kept": regex(PRD, "contains", rf'{SATISFACTION_SM}{ITEM}[ \t]+target: "(?![^"\n]*NEEDS CLARIFICATION)'
                                                   rf'[^"\n]*\b4\.0\b'),
            "measured-by-survey": regex(PRD, "contains", rf'{SATISFACTION_SM}{ITEM}[ \t]+measured_by: "[^"\n]*[Ss]urvey'),
            "no-upstream": regex(PRD, "not_contains", rf'{SATISFACTION_SM}{ITEM}[ \t]+upstream:[ \t]*(?:\n[ \t]+- |\[[ \t]*\{{)'),
        },
    },
}

# New graders for three v1 cases; their existing graders stay as they are.
AWS_OR_STRIPE_ITEM = r'statement: "[^"\n]*\b{0}\b[^"\n]*"\n{1}[ \t]+- \{{id: BRN-'
EXTRA_GRADERS = {
    "records-provenance": {
        "model-is-a-claude-model-id": regex(PRD, "contains", r'^  model: "claude-[a-z0-9][a-z0-9.-]*"', "m"),
        "identity-not-unavailable": regex(PRD, "not_contains", r'^  (?:tool|model|session): "?unavailable\b', "m"),
        "authors-include-the-tool": regex(PRD, "contains", r'^authors: \[[^\]\n]*"claude-code"[^\]\n]*\]', "m"),
        "changelog-session-matches": regex(PRD, "contains",
                                           r'^  session: "([0-9a-f-]{36})"[\s\S]*\| claude-code \(session \1\) \|', "m"),
    },
    "constraints-not-design": {
        "aws-no-brn-link": regex(PRD, "not_contains", AWS_OR_STRIPE_ITEM.format("AWS", ITEM)),
        "stripe-no-brn-link": regex(PRD, "not_contains", AWS_OR_STRIPE_ITEM.format("Stripe", ITEM)),
    },
    "architecture-context": {  # VER-37
        "handoff-names-both-ways": llm("""\
Context the reply was written in: the user asked for a PRD from BRN-001 and named ADR-002 (accepted:
ClinicCore is the calendar of record) and ADR-003 (proposed: synchronous booking writes vs a scheduled
import). A proposed ADR resolves nothing, so a correct PRD records the booking decision as a [NEEDS ADR]
marker naming the booking requirements. An open decision is resolved in the architecture step, by an
accepted ADR or by an approved mandated platform (a policy setting) that answers exactly that question.

Judge only the final reply. PASS if all of these hold:
- It lists the open booking decision (the [NEEDS ADR] marker) with the requirements it names.
- It says that epics for those requirements must wait until the architecture step resolves that decision.
- It names both ways the decision can be resolved: an accepted ADR, or an approved mandated platform (or
  policy setting) that answers it. Any wording counts.
FAIL if any of these fails, or if it says or implies that only an accepted ADR can resolve the decision,
such as "epics must wait until an accepted ADR resolves it" with no other way named.
"""),
    },
}


def scaffold(comment, files):
    out = f"#!/usr/bin/env bash\n# {comment}\nset -euo pipefail\n"
    dirs = sorted({os.path.dirname(p) for p in files} - {""})
    if dirs:
        out += "mkdir -p " + " ".join(dirs) + "\n"
    for p, text in files.items():
        out += f"cat > {p} <<'FIXTURE'\n{text}FIXTURE\n"
    return out


def main():
    for label, (text, schema, *expect) in FIXTURES.items():
        validate(label, text, schema, *expect)
    for label, expect in POLICY_SCRIPT.items():
        check_policy_script(label, FIXTURES[label][0], expect)
    for name, case in CASES.items():
        d = ROOT / name
        (d / "graders").mkdir(parents=True, exist_ok=True)
        (d / "prompt.md").write_text(
            f"---\ndescription: \"{case['description']}\"\ntags: [prd, ver-{case['ver']}]\nmax_turns: 60\n"
            f"timeout_seconds: 1200\nallowed_tools: {TOOLS}\n---\n{case['prompt']}")
        (d / "case.yaml").write_text(f"schema_version: \"1.1\"\nname: {name}\ncontext:\n  scaffold_script: scaffold.sh\n")
        (d / "scaffold.sh").write_text(scaffold(f"Seeds the fixtures for SPEC-002 VER-{case['ver']} ({name}).",
                                                case["files"]))
        os.chmod(d / "scaffold.sh", 0o755)
        for g, body in case["graders"].items():
            (d / "graders" / f"{g}.md").write_text(body)
    for name, graders in EXTRA_GRADERS.items():
        for g, body in graders.items():
            path = ROOT / name / "graders" / f"{g}.md"
            assert not path.exists() or path.read_text() == body, f"would overwrite a different grader: {path}"
            path.write_text(body)
    print("validated", len(FIXTURES), "fixtures; wrote", len(CASES), "cases and",
          sum(map(len, EXTRA_GRADERS.values())), "added graders")


if __name__ == "__main__":
    main()
