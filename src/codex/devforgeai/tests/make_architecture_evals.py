"""Generates Codex evals/architecture/<case>/ (SPEC-003 VER-01..11, 14, 15, 16): prompts, graders, case.yaml
and the inline scaffold fixtures. Every fixture is defined once here and validated against src/schemas/
before anything is written; the two policies are read from src/staging/examples/policy-two-orgs/.
Edit fixtures and graders here, then regenerate; it overwrites the case files and never deletes a
grader, so remove renamed ones by hand. Run from the repository root:

    python3 -B src/codex/devforgeai/tests/make_architecture_evals.py
"""
import json
import os
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

ROOT = Path("src/codex/devforgeai/evals/architecture")
SCHEMAS = Path("src/schemas")
POLICIES = Path("src/staging/examples/policy-two-orgs")
TOOLS = "[exec_command, apply_patch, request_user_input]"

# --- Fixtures -------------------------------------------------------------------------------------

PRD_V1 = """\
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
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-20
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
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

Let the food bank's volunteers book warehouse shifts themselves instead of by phone, and give the
coordinator a live roster.

## 2. Problem and opportunity

The coordinator fills three warehouse shifts a day by phone, and about one shift in six starts
short-staffed (BRN-001#PRB-01).

## 3. Users and personas

About 120 active volunteers, who book from their phones, and one volunteer coordinator.

## 4. Goals and non-goals

**Goals**
- Volunteers book their own shifts.

**Non-goals** (explicitly out of scope)
- Payroll and donations; volunteers aren't paid.

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
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

## 6. Functional requirements

```yaml items
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a volunteer sign in."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a signed-in volunteer book an open warehouse shift."
    priority: must
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-003
    status: active
    statement: "The system shall show the coordinator each day's roster of booked volunteers."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: security
    statement: "An administrator can revoke a volunteer's signed-in sessions, and a revoked session stops working within 5 minutes."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
  - id: NFR-003
    status: active
    category: constraint
    statement: "The food bank has no on-site server, so the system runs on hosted services (applies to the whole product)."
    priority: must
    release: current
```

## 8. User experience

Mobile-first web pages; no app to install.

## 9. Constraints and dependencies

NFR-003 records the hosting constraint.

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most volunteers have a smartphone with a web browser."
    validation: "Ask at the September volunteer meeting"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

## 11. Release and rollout

Pilot with the Tuesday and Thursday shifts, then every shift.

## 12. Open questions

- [NEEDS ADR: identity provider for volunteer sign-in; affects FR-001]

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | all |
| 1 | 2026-09-20 | Priya Nair | Approved | status |
"""


def replace(text, old, new):
    assert text.count(old) == 1, f"fixture edit anchor not unique: {old!r}"
    return text.replace(old, new)


# VER-15/16: version 2 after a priority-only change.
PRD_V2 = replace(PRD_V1, "version: 1\ncreated: 2026-09-14\nupdated: 2026-09-20",
                 "version: 2\ncreated: 2026-09-14\nupdated: 2026-09-24")
PRD_V2 = replace(PRD_V2, "approved_on: 2026-09-20", "approved_on: 2026-09-24")
PRD_V2 = replace(PRD_V2, 'roster of booked volunteers."\n    priority: should',
                 'roster of booked volunteers."\n    priority: must')
PRD_V2 += ("| 2 | 2026-09-24 | Priya Nair | Priority change only: FR-003 should to must. No requirement text changed | FR-003 |\n"
           "| 2 | 2026-09-24 | Priya Nair | Approved | status |\n")

# VER-09: a constraint that conflicts with Organization A's mandated identity platform.
NFR_GOOGLE = "Volunteers sign in with their personal Google accounts (applies to sign-in)."
PRD_CONFLICT = replace(PRD_V1, "(applies to the whole product).\"\n    priority: must\n    release: current\n",
                       "(applies to the whole product).\"\n    priority: must\n    release: current\n"
                       "  - id: NFR-004\n    status: active\n    category: constraint\n"
                       f"    statement: \"{NFR_GOOGLE}\"\n    priority: must\n    release: current\n")
PRD_CONFLICT = replace(PRD_CONFLICT, "NFR-003 records the hosting constraint.",
                       "NFR-003 records the hosting constraint, and NFR-004 the sign-in accounts.")

# VER-05: three requirements, matching the existing ARCH-001's two questions.
PRD_SMALL = replace(PRD_V1, """\
  - id: FR-003
    status: active
    statement: "The system shall show the coordinator each day's roster of booked volunteers."
    priority: should
    release: current
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
""", "")
PRD_SMALL = replace(PRD_SMALL, """\
  - id: NFR-001
    status: active
    category: security
    statement: "An administrator can revoke a volunteer's signed-in sessions, and a revoked session stops working within 5 minutes."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
  - id: NFR-003
    status: active
    category: constraint
    statement: "The food bank has no on-site server, so the system runs on hosted services (applies to the whole product)."
    priority: must
    release: current
""", """\
  - id: NFR-001
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
""")
PRD_SMALL = replace(PRD_SMALL, "NFR-003 records the hosting constraint.", "None beyond section 7.")
PRD_SMALL = replace(PRD_SMALL, ", and give the\ncoordinator a live roster.", ".")


def adr(num, title, status, created, context, outcome, history, upstream,
        supersedes="[]", superseded_by="null"):
    """An ADR fixture in the assets/adr.md shape."""
    return f"""\
---
id: ADR-{num}
type: adr
title: "{title}"
status: {status}
version: 1
created: {created}
updated: {created}
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: []
approved_by: "Priya Nair"
approved_on: {created}
upstream:
{upstream}supersedes: {supersedes}
superseded_by: {superseded_by}
blocked_by: []
# --- adr-specific ---
consulted: []
informed: []
---

# ADR-{num} — {title}

## Context and problem statement

{context}

## Decision drivers

- Low running cost for a volunteer-run charity.

## Considered options

1. {title}
2. Do nothing for now

## Decision outcome

**Chosen option:** {outcome}

### Consequences

- Good: one clear answer for every epic.
- Bad: it has to be revisited if the food bank's setup changes.

### Confirmation

Reviewed when the pilot ends.

## Pros and cons of the options

### {title}
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
{history}"""


def link(item, version=1):
    return f"  - {{id: PRD-001, item: {item}, relation: informed_by, version: {version}, hash: null}}\n"


ADR_LOGGING = adr(
    "001", "Keep application logs for 30 days in the hosting provider's log service", "accepted", "2026-09-18",
    "Sign-in failures (PRD-001#FR-001) must be traceable for a month, and nobody at the food bank runs a log server.",
    "keep logs for 30 days in the hosting provider's log service, because it costs nothing extra.",
    "| 2026-09-18 | accepted | Decided by Priya Nair |\n", link("FR-001"))

ADR_DATA = adr(
    "001", "Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service",
    "accepted", "2026-09-21",
    "Bookings (PRD-001#FR-002) and private phone numbers (PRD-001#NFR-001) need one owner.",
    "one managed PostgreSQL database, owned by the shift service, because it keeps phone numbers behind one API.",
    "| 2026-09-21 | accepted | Decided by Priya Nair |\n", link("FR-002") + link("NFR-001"))

ADR_KEYCLOAK = adr(
    "002", "Run Keycloak on the food bank's on-premises server for volunteer sign-in", "superseded", "2026-09-21",
    "Volunteers must sign in (PRD-001#FR-001), and the food bank owned a server in its back office.",
    "Keycloak on the on-premises server, because the server was already paid for.",
    "| 2026-09-21 | accepted | Decided by Priya Nair |\n| 2026-09-26 | superseded | Superseded by ADR-003 |\n",
    link("FR-001"), superseded_by="ADR-003")

ADR_HOSTING = adr(
    "003", "Retire the on-premises server and run every service on the hosting provider", "accepted", "2026-09-26",
    "The back-office server is being removed at the end of October, so nothing can keep running on it, "
    "including the Keycloak instance that ADR-002 chose. This decision is about hosting only: which identity "
    "provider replaces Keycloak is a separate decision that has not been made.",
    "run every service on the hosting provider, because the server is being removed.",
    "| 2026-09-26 | accepted | Decided by Priya Nair |\n", link("FR-001") + link("FR-002"), supersedes="[ADR-002]")

ADR_AUTH0 = adr(
    "001", "Use Auth0 for volunteer sign-in", "accepted", "2026-09-22",
    "Volunteers must sign in (PRD-001#FR-001) without the food bank running an identity server.",
    "Auth0 on its free tier, because it needs no server and supports passwordless email links.",
    "| 2026-09-22 | accepted | Decided by Priya Nair |\n", link("FR-001"))


def arch(*, status, created, updated, approved, prd_version, outcome, context, drivers, mermaid, components,
         decisions, evidence, deployment, changelog, session="fixture-session"):
    """An ARCH fixture in the assets/arch.md shape."""
    approved_by, approved_on, reviewed = (f'"Priya Nair"', updated, '["Priya Nair"]') if approved else ('""', "null", "[]")
    return f"""\
---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: {status}
version: 1
created: {created}
updated: {updated}
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "{session}"
reviewed_by: {reviewed}
approved_by: {approved_by}
approved_on: {approved_on}
upstream:
  - {{id: PRD-001, relation: informed_by, version: {prd_version}, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Riverside Food Bank volunteer shift sign-up"
outcome: {outcome}
inspection_scope: []
---

# ARCH-001 — Riverside Food Bank volunteer shift sign-up architecture

## 1. Context and scope

{context}

## 2. Quality drivers

{drivers}

## 3. Components

```mermaid
flowchart LR
{mermaid}```

```yaml items
components:
{components}```

## 4. Architectural questions

```yaml items
decisions:
{decisions}```

## 5. Evidence inspected

```yaml items
evidence:
{evidence}```

## 6. Deployment

{deployment}

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
{changelog}"""


def item(lines):
    return "".join(f"    {l}\n" if i else f"  - {l}\n" for i, l in enumerate(lines))


def ups(*items, version=1):
    return ["upstream:"] + [f"  - {{id: PRD-001, item: {i}, relation: informed_by, version: {version}, hash: null}}"
                            for i in items]


CMP_WEB = item(["id: CMP-01", "status: active", 'name: "Volunteer web app"',
                'responsibility: "Sign-in and booking screens; holds no data of its own"', "owns_data: []",
                "interacts_with:", '  - "CMP-02"', '  - "CMP-03"', 'deployment: "Static site on the hosting provider"'])
CMP_SHIFTS = item(["id: CMP-02", "status: active", 'name: "Shift service"',
                   'responsibility: "Shifts, bookings and volunteer contact details"', "owns_data:",
                   '  - "Shifts and bookings"', '  - "Volunteer phone numbers"', "interacts_with:", '  - "CMP-01"',
                   'deployment: "One hosted service with its database"'] + ups("NFR-002"))
MERMAID = "    W[CMP-01 Volunteer web app] --> S[CMP-02 Shift service]\n    W --> I[CMP-03 Identity provider]\n"
Q_IDP = 'question: "Which identity provider handles volunteer sign-in?"'
Q_REVOKE = 'question: "How are a volunteer\'s sessions revoked within 5 minutes (NFR-001)?"'
EVD_PRD = item(["id: EVD-01", "status: active", 'source: "PRD-001"', "kind: prd",
                'finding: "Version 1, status approved: sign-in (FR-001) with session revocation (NFR-001); the identity provider is a NEEDS ADR marker."',
                "classification: context"])
INITIAL_ROW = ("| 1 | 2026-09-21 | claude-code (session fixture-session) | Initial draft for PRD-001 v1. Policy resolution: "
               "interview.max_calls=8 (default); architecture.mandated_platforms=none (default); "
               "quality.required_categories=floor only (default) | all |\n")

# VER-07: a draft ARCH-001 for the same system, both identity questions open.
ARCH_EXISTING = arch(
    status="draft", created="2026-09-21", updated="2026-09-21", approved=False, prd_version=1, outcome="create",
    context="Defined against PRD-001 version 1 (approved): volunteers sign in, book warehouse shifts, and the "
            "coordinator sees the roster. No inspection scope was named, and no code was inspected.",
    drivers="NFR-001 (session revocation) and NFR-002 (private phone numbers) drive the design; NFR-003 rules "
            "out an on-site server.",
    mermaid=MERMAID,
    components=CMP_WEB + CMP_SHIFTS + item(["id: CMP-03", "status: active", 'name: "Identity provider"',
                                            'responsibility: "Authenticates volunteers and issues sessions"',
                                            "owns_data:", '  - "Volunteer credentials"', "interacts_with:",
                                            '  - "CMP-01"', 'deployment: "External; the provider is open (DEC-01)"']
                                           + ups("NFR-001")),
    decisions=item(["id: DEC-01", "status: active", Q_IDP, "blocking: true", "state: open", "resolved_by: []",
                    "notes: null"] + ups("FR-001"))
              + item(["id: DEC-02", "status: active", Q_REVOKE, "blocking: true", "state: open",
                      "resolved_by: []", "notes: null"] + ups("FR-001", "NFR-001")),
    evidence=EVD_PRD,
    deployment="The web app and the shift service run on the hosting provider (NFR-003).",
    changelog=INITIAL_ROW)

# VER-05: an approved ARCH-001 whose DEC-01 resolver (ADR-002) was since superseded by ADR-003.
ARCH_SUPERSEDED = arch(
    status="approved", created="2026-09-21", updated="2026-09-22", approved=True, prd_version=1, outcome="create",
    context="Defined against PRD-001 version 1 (approved): volunteers sign in and book warehouse shifts. Payroll "
            "and donations are outside the system. No inspection scope was named, and no code was inspected.",
    drivers="NFR-001 (phone numbers visible only to the coordinator) drives data ownership.",
    mermaid=MERMAID,
    components=CMP_WEB + CMP_SHIFTS.replace("NFR-002", "NFR-001")
    + item(["id: CMP-03", "status: active", 'name: "Identity provider"',
            'responsibility: "Authenticates volunteers and issues sessions"', "owns_data:",
            '  - "Volunteer credentials"', "interacts_with:", '  - "CMP-01"',
            'deployment: "Keycloak on the food bank\'s on-premises server (ADR-002)"']),
    decisions=item(["id: DEC-01", "status: active", Q_IDP, "blocking: true", "state: resolved",
                    "resolved_by: [ADR-002]", "notes: null"] + ups("FR-001"))
              + item(["id: DEC-02", "status: active",
                      'question: "Where are shift, booking and contact data stored, and which component owns them?"',
                      "blocking: true", "state: resolved", "resolved_by: [ADR-001]", "notes: null"]
                     + ups("FR-002", "NFR-001")),
    evidence=item(["id: EVD-01", "status: active", 'source: "PRD-001"', "kind: prd",
                   'finding: "Version 1, status approved: sign-in (FR-001), booking (FR-002) and private phone numbers (NFR-001)."',
                   "classification: context"])
             + item(["id: EVD-02", "status: active", 'source: "ADR-001"', "kind: adr",
                     'finding: "Version 1, status accepted: the shift service owns shift, booking and contact data in one managed PostgreSQL database."',
                     "classification: decided"])
             + item(["id: EVD-03", "status: active", 'source: "ADR-002"', "kind: adr",
                     'finding: "Version 1, status accepted: Keycloak on the on-premises server handles volunteer sign-in."',
                     "classification: decided"]),
    deployment="The web app and the shift service run on the hosting provider; Keycloak runs on the "
               "on-premises server (ADR-002).",
    changelog=INITIAL_ROW + "| 1 | 2026-09-22 | Priya Nair | Approved | status |\n")


def arch_reviewed(prd_version, outcome, review_row):
    """VER-15/16: an approved ARCH-001 with DEC-01 resolved by ADR-001 (Auth0) and DEC-02 open."""
    return arch(
        status="approved", created="2026-09-21", updated="2026-09-22", approved=True, prd_version=prd_version,
        outcome=outcome,
        context="Defined against PRD-001 version 1 (approved): volunteers sign in, book warehouse shifts, and the "
                "coordinator sees the roster. No inspection scope was named, and no code was inspected.",
        drivers="NFR-001 (session revocation) and NFR-002 (private phone numbers) drive the design; NFR-003 rules "
                "out an on-site server.",
        mermaid=MERMAID,
        components=CMP_WEB + CMP_SHIFTS + item(["id: CMP-03", "status: active", 'name: "Identity provider"',
                                                'responsibility: "Authenticates volunteers and issues sessions"',
                                                "owns_data:", '  - "Volunteer credentials"', "interacts_with:",
                                                '  - "CMP-01"', 'deployment: "External: Auth0 (ADR-001)"']
                                               + ups("NFR-001")),
        decisions=item(["id: DEC-01", "status: active", Q_IDP, "blocking: true", "state: resolved",
                        "resolved_by: [ADR-001]", "notes: null"] + ups("FR-001"))
                  + item(["id: DEC-02", "status: active", Q_REVOKE, "blocking: true", "state: open",
                          "resolved_by: []", "notes: null"] + ups("FR-001", "NFR-001")),
        evidence=EVD_PRD + item(["id: EVD-02", "status: active", 'source: "ADR-001"', "kind: adr",
                                 'finding: "Version 1, status accepted: Auth0 handles volunteer sign-in."',
                                 "classification: decided"]),
        deployment="The web app and the shift service run on the hosting provider (NFR-003); Auth0 is external.",
        changelog=INITIAL_ROW + "| 1 | 2026-09-22 | Priya Nair | Approved | status |\n" + review_row)


REVIEW_ROW = ("| 1 | 2026-09-25 | claude-code (session prior-review-session) | Reviewed against PRD-001 v2: reuse "
              "confirmed, no architectural change. Policy resolution: interview.max_calls=8 (default); "
              "architecture.mandated_platforms=none (default); quality.required_categories=floor only (default) | none |\n")
ARCH_TO_REVIEW = arch_reviewed(1, "create", "")
ARCH_REVIEWED = arch_reviewed(2, "reuse", REVIEW_ROW)

POL_A = (POLICIES / "org-a/POL-001.md").read_text()
POL_B = (POLICIES / "org-b/POL-001.md").read_text()

# --- Fixture validation ---------------------------------------------------------------------------


class _Loader(yaml.SafeLoader):
    """Keeps dates as strings, as the schemas expect."""


_Loader.yaml_implicit_resolvers = {k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
                                   for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def validate(label, text, schema):
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
    errors = [f"{list(e.path)}: {e.message}" for e in Draft202012Validator(
        json.loads((SCHEMAS / schema).read_text()), registry=registry).iter_errors(doc)]
    assert not errors, f"{label} fails {schema}: {errors}"
    assert "\nFIXTURE\n" not in text, f"{label} contains the heredoc delimiter"


FIXTURES = {
    "PRD_V1": (PRD_V1, "prd.schema.json"), "PRD_V2": (PRD_V2, "prd.schema.json"),
    "PRD_CONFLICT": (PRD_CONFLICT, "prd.schema.json"), "PRD_SMALL": (PRD_SMALL, "prd.schema.json"),
    "ADR_LOGGING": (ADR_LOGGING, "adr.schema.json"), "ADR_DATA": (ADR_DATA, "adr.schema.json"),
    "ADR_KEYCLOAK": (ADR_KEYCLOAK, "adr.schema.json"), "ADR_HOSTING": (ADR_HOSTING, "adr.schema.json"),
    "ADR_AUTH0": (ADR_AUTH0, "adr.schema.json"), "ARCH_EXISTING": (ARCH_EXISTING, "arch.schema.json"),
    "ARCH_SUPERSEDED": (ARCH_SUPERSEDED, "arch.schema.json"), "ARCH_TO_REVIEW": (ARCH_TO_REVIEW, "arch.schema.json"),
    "ARCH_REVIEWED": (ARCH_REVIEWED, "arch.schema.json"), "POL_A": (POL_A, "policy.schema.json"),
    "POL_B": (POL_B, "policy.schema.json"),
}


def scaffold(comment, **files):
    """A scaffold.sh that writes each fixture; keyword names are paths with '/' written as '__'."""
    out = f"#!/usr/bin/env bash\n# {comment}\nset -euo pipefail\n"
    paths = [k.replace("__", "/") for k in files]
    out += "mkdir -p " + " ".join(sorted({os.path.dirname(p) for p in paths})) + "\n"
    for p, text in zip(paths, files.values()):
        out += f"cat > {p} <<'FIXTURE'\n{text}FIXTURE\n"
    return out


SHARED = dict(docs__specs__prd__PRD_001=PRD_V1)


def files(**kw):
    return {k.replace("_001", "-001.md").replace("_002", "-002.md").replace("_003", "-003.md"): v for k, v in kw.items()}


# --- Graders --------------------------------------------------------------------------------------

ARCH = "docs/specs/arch/ARCH-001.md"
ITEM = r"(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?"  # the rest of one item's lines, never the next item
Q_IDENTITY = (r'(?![^"\n]*[Rr]evo)[^"\n]*(?:[Ii]dentity|[Aa]uthenticat|IdP\b|[Ss]ign[- ]in (?:provider|service|'
              r'system|platform)|[Ll]og[- ]?in provider)[^"\n]*')
Q_REVOCATION = r'[^"\n]*[Rr]evo[^"\n]*'
CITES_FR_001 = r"[ \t]+- \{id: PRD-001, item: FR-001,"


def dec(question, state, then=""):
    return rf'- id: DEC-\d{{2}}\n{ITEM}[ \t]+question: "{question}"\n{ITEM}[ \t]+state: {state}\n{ITEM}{then}'


def regex(target, match, pattern, flags=None):
    t = target if target == "last_message" else "{source: file, path: %s}" % target
    fl = f"flags: {flags}\n" if flags else ""
    return f"---\ntype: regex\ntarget: {t}\nmatch: {match}\n{fl}---\n{pattern}\n"


def exists(path, value):
    return f"---\ntype: file_exists\npath: {path}\nexists: {str(value).lower()}\n---\n"


FIRED = "---\ntype: skill_loaded\npath_suffix: skills/architecture/SKILL.md\narm: plugin\n---\n"
NOT_FIRED = ("---\ntype: skill_loaded\npath_suffix: skills/architecture/SKILL.md\n"
             "min: 0\nmax: 0\narm: both\n---\n")
ASKS_WITH_NATIVE_TOOL = ("---\ntype: request_user_input\nmin: 1\narm: plugin\n---\n"
                         "The selection between reusing and amending ARCH-001 must be presented "
                         "through Codex's native request_user_input tool.\n")

IDENTITY_OPEN = regex(ARCH, "contains", dec(Q_IDENTITY, "open", CITES_FR_001))
REVOCATION_OPEN = regex(ARCH, "contains", dec(Q_REVOCATION, "open", CITES_FR_001))
OUTCOME_NULL = regex(ARCH, "contains", r"^outcome: null[ \t]*$", "m")
BLOCKS_FR_001 = regex("last_message", "contains", r"[Bb]locked[\s\S]{0,200}?\bFR-001\b[^\n]{0,60}\bDEC-\d{2}")
ARCH_CREATED = exists(ARCH, True)
RESOLVED_BY = r"resolved_by:(?:[^\n]*{0}|\n[ \t]+- \"?{0})"
ALL_SECTIONS = (r"## 1\. Context and scope\n[\s\S]*\n## 2\. Quality drivers\n[\s\S]*\n## 3\. Components\n[\s\S]*"
                r"\n## 4\. Architectural questions\n[\s\S]*\n## 5\. Evidence inspected\n[\s\S]*\n## 6\. Deployment\n"
                r"[\s\S]*\n## 7\. Requirement changes proposed to the PRD owner\n[\s\S]*\n## 8\. Open questions\n"
                r"[\s\S]*\n## Change Log\n")
PROMPT = "Define the architecture for PRD-001, so we know which requirements are ready for epics.\nProceed without questions.\n"

# Every supplied kinds field must be a non-empty quoted block list of known kinds.
# A valid first kind or an uncertainty marker must not mask an unknown/flow-form field.
CMP_KIND = r"(?:user-interface|service|platform|api|relational-store|data-store|external)"
CMP_KINDS = (
    rf'\A(?![\s\S]*^    kinds:(?![ \t]*\r?\n(?:      - "{CMP_KIND}"[ \t]*\r?\n)+(?!      - )))'
    rf'[\s\S]*(?:^    kinds:[ \t]*\r?\n      - "{CMP_KIND}"[ \t]*\r?$|\[NEEDS CLARIFICATION: kinds of CMP-\d{{2}}\])'
)

CASES = {
    "creates-arch": {
        "ver": "01", "files": SHARED, "prompt": PROMPT,
        "description": "VER-01: no policy and no ARCH; writes ARCH-001 with open identity-provider and session-revocation questions citing FR-001, the PRD as a context EVD, outcome null, and FR-001 reported blocked.",
        "graders": {
            "skill-fired": FIRED,
            "cmp-kinds": regex(ARCH, "contains", CMP_KINDS, "m"),
            "arch-exists": ARCH_CREATED,
            "identity-dec-open": IDENTITY_OPEN,
            "revocation-dec-open": REVOCATION_OPEN,
            "prd-evidence-context": regex(ARCH, "contains",
                                          rf"- id: EVD-\d{{2}}\n{ITEM}[ \t]+kind: prd\n{ITEM}[ \t]+classification: context\n"),
            "outcome-null": OUTCOME_NULL,
            "has-components": regex(ARCH, "contains", r"```mermaid\n[\s\S]*?```\n[\s\S]*^  - id: CMP-01\n", "m"),
            "all-sections": regex(ARCH, "contains", ALL_SECTIONS),
            "no-leftovers": regex(ARCH, "not_contains", r"<!--|ARCH-000|PRD-000|YYYY-MM-DD|<component>|<the architectural question>"),
            "handoff-blocks-fr-001": BLOCKS_FR_001,
        },
    },
    "org-a-policy": {
        "ver": "02", "files": dict(SHARED, docs__specs__policy__POL_001=POL_A), "prompt": PROMPT,
        "description": "VER-02: with Organization A's policy, the identity-provider question is resolved by POL-001#SET-01, session revocation stays open, FR-001 stays blocked, and outcome stays null.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "identity-resolved-by-policy": regex(ARCH, "contains", dec(
                Q_IDENTITY, "resolved", r'[ \t]+resolved_by:(?: \[[ \t]*"?POL-001#SET-01"?[ \t]*\]|\n[ \t]+- "?POL-001#SET-01"?\n)')),
            "revocation-dec-open": REVOCATION_OPEN,
            "outcome-null": OUTCOME_NULL,
            "handoff-blocks-fr-001": BLOCKS_FR_001,
        },
    },
    "org-b-policy": {
        "ver": "03", "files": dict(SHARED, docs__specs__policy__POL_001=POL_B), "prompt": PROMPT,
        "description": "VER-03: with Organization B's policy (no identity mandate), the identity-provider question stays open with an empty resolved_by.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "identity-dec-open-empty": regex(ARCH, "contains", dec(Q_IDENTITY, "open", r"[ \t]+resolved_by: \[\][ \t]*\n")),
            "no-policy-resolution": regex(ARCH, "not_contains", RESOLVED_BY.format("POL-")),
        },
    },
    "unrelated-adr": {
        "ver": "04", "files": dict(SHARED, docs__specs__adr__ADR_001=ADR_LOGGING), "prompt": PROMPT,
        "description": "VER-04: an accepted logging ADR-001 that cites FR-001 resolves neither identity question; FR-001 stays blocked.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "identity-dec-open": IDENTITY_OPEN,
            "revocation-dec-open": REVOCATION_OPEN,
            "nothing-resolved-by-adr-001": regex(ARCH, "not_contains", RESOLVED_BY.format("ADR-001")),
            "handoff-blocks-fr-001": BLOCKS_FR_001,
        },
    },
    "superseded-adr": {
        "ver": "05",
        "files": dict(docs__specs__prd__PRD_001=PRD_SMALL, docs__specs__arch__ARCH_001=ARCH_SUPERSEDED,
                      docs__specs__adr__ADR_001=ADR_DATA, docs__specs__adr__ADR_002=ADR_KEYCLOAK,
                      docs__specs__adr__ADR_003=ADR_HOSTING),
        "prompt": "Update the architecture for PRD-001: amend ARCH-001. I confirm the amend outcome.\n"
                  "Proceed without asking me anything else.\n",
        "description": "VER-05: amending ARCH-001 after ADR-002 was superseded reopens DEC-01, keeps DEC-02 resolved by ADR-001, records ADR-002 as context, and reports FR-001 blocked by DEC-01.",
        "graders": {
            "dec-01-open": regex(ARCH, "contains", rf"- id: DEC-01\n{ITEM}[ \t]+state: open\n[ \t]+resolved_by: \[\][ \t]*\n"),
            "dec-02-still-adr-001": regex(ARCH, "contains", rf"- id: DEC-02\n{ITEM}[ \t]+state: resolved\n[ \t]+resolved_by: \[ADR-001\][ \t]*\n"),
            "adr-002-context-evidence": regex(ARCH, "contains",
                                              rf'- id: EVD-\d{{2}}\n{ITEM}[ \t]+source: "[^"\n]*ADR-002[^"\n]*"\n{ITEM}[ \t]+classification: context\n'),
            "names-superseded-resolver": regex("last_message", "contains",
                                               r"ADR-002[^\n]{0,150}(?:[Ss]upersed|[Rr]eplac)|(?:[Ss]upersed|[Rr]eplac)[^\n]{0,150}ADR-002"),
            "readiness-mapping": """\
---
type: llm
---

Context the reply was written in: PRD-001 has exactly three requirements, FR-001, FR-002 and NFR-001.
The existing ARCH-001 had two architectural questions: DEC-01 (identity provider), which cites FR-001
only, and DEC-02 (data ownership), which cites FR-002 and NFR-001 only. DEC-01 was resolved by
ADR-002, which has since been superseded by ADR-003, an ADR about hosting, not identity. DEC-02 is
resolved by ADR-001, which is still accepted. The user asked to amend ARCH-001.

Judge only the readiness that the final reply reports.
PASS if all of these hold:
- FR-001 is reported blocked, with DEC-01 named as a blocker.
- FR-002 and NFR-001 are each reported ready, or reported blocked only by questions numbered DEC-03
  or higher (questions this run added). Neither is attributed to DEC-01 or DEC-02.
- All three requirements appear in the readiness report.
- No other sentence contradicts the lists (for example, saying FR-001 is ready or everything is ready).
FAIL if any of these fails, or if the reply says DEC-01 is still resolved, by ADR-002 or by ADR-003.
""",
        },
    },
    "no-acceptance-without-user": {
        "ver": "06", "files": SHARED, "prompt": PROMPT,
        "description": "VER-06: with no user, no ADR is written or accepted, no question is resolved by an ADR, and outcome stays null.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "no-adr-written": exists("docs/specs/adr/**", False),
            "nothing-resolved-by-an-adr": regex(ARCH, "not_contains", RESOLVED_BY.format("ADR-")),
            "outcome-null": OUTCOME_NULL,
        },
    },
    "existing-arch-not-duplicated": {
        "ver": "07", "files": dict(SHARED, docs__specs__arch__ARCH_001=ARCH_EXISTING), "prompt": PROMPT,
        "description": "VER-07: an ARCH-001 already covers the system, so the skill proposes reuse or amend and asks; no ARCH-002 is created and ARCH-001 is unchanged.",
        "graders": {
            "skill-fired": FIRED,
            "no-arch-002": exists("docs/specs/arch/ARCH-002.md", False),
            "arch-001-unchanged": regex(ARCH, "contains", r"^status: draft\n^version: 1\n^created: 2026-09-21\n^updated: 2026-09-21\n", "m"),
            "offers-reuse-and-amend": regex("last_message", "contains", r"\b[Rr]euse\b[\s\S]*\b[Aa]mend|\b[Aa]mend[\s\S]*\b[Rr]euse\b"),
            "asks-with-request-user-input": ASKS_WITH_NATIVE_TOOL,
            "recommends-and-asks": """\
---
type: llm
---

The workspace already held PRD-001 (version 1, approved) and ARCH-001, a draft architecture
description for the same system, defined against PRD-001 version 1. The user asked to define the
architecture for PRD-001 and to proceed without questions.
The Codex evidence supplied for review includes the native request_user_input question together with
any final reply. Judge that combined user-visible output. PASS if it points to the existing ARCH-001,
recommends reusing or amending it with at least one reason, and asks the user to choose before
anything is written.
FAIL if it says it created or changed an architecture document, treats "proceed without questions"
as permission to pick reuse or amend itself, or never mentions ARCH-001.
""",
        },
    },
    "insufficient-evidence": {
        "ver": "08", "files": SHARED,
        "prompt": "Define the architecture for PRD-001. For sign-in, reuse our current auth service.\nProceed without questions.\n",
        "description": "VER-08: 'reuse our current auth service' with no inspection scope and no code: the outcome is not reuse and a NEEDS CLARIFICATION marker names the missing evidence.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "outcome-not-reuse": regex(ARCH, "not_contains", r"^outcome: reuse\b", "m"),
            "clarification-marker": regex(ARCH, "contains",
                                          r"\[NEEDS CLARIFICATION:[^\]\n]*(?:[Aa]uth|[Ee]vidence|[Ii]nspect|[Ss]cope|[Cc]ode)"),
        },
    },
    "prd-change-handed-back": {
        "ver": "09",
        "files": dict(docs__specs__prd__PRD_001=PRD_CONFLICT, docs__specs__policy__POL_001=POL_A), "prompt": PROMPT,
        "description": "VER-09: NFR-004 (personal Google accounts) conflicts with Organization A's mandated identity platform; ARCH section 7 and the handoff propose a PRD change, and PRD-001 is unchanged.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "section-7-names-nfr-004": regex(ARCH, "contains",
                                             r"## 7\. Requirement changes proposed to the PRD owner\n(?:(?!## )[^\n]*\n)*?[^\n]*NFR-004"),
            "prd-version-unchanged": regex("docs/specs/prd/PRD-001.md", "contains",
                                           r"^status: approved\n^version: 1\n^created: 2026-09-14\n^updated: 2026-09-20\n", "m"),
            "prd-nfr-004-unchanged": regex("docs/specs/prd/PRD-001.md", "contains", re.escape(f'statement: "{NFR_GOOGLE}"')),
            "handoff-names-nfr-004": regex("last_message", "contains", r"NFR-004"),
        },
    },
    "hands-off-to-epic": {
        "ver": "10", "files": SHARED, "prompt": PROMPT,
        "description": "VER-10 (current branch): no epic skill ships, so the reply lists ready and blocked requirements and ends with a Next step paragraph naming $devforgeai:epic PRD-001 as not built yet.",
        "graders": {
            "ends-with-next-step": regex("last_message", "contains",
                                         r"(?:^|\n)[ \t]*(?:\*\*|__)?Next step[^\n]*(?:\n(?![ \t]*\n)[^\n]*)*\s*$"),
            "names-epic-command": regex("last_message", "contains", r"\$devforgeai:epic`? `?PRD-001\b"),
            "says-not-built": regex("last_message", "contains",
                                    r"Next step[\s\S]*(?:\bnot|n't)[^\n.]{0,40}?\b(?:built|exist|available)"),
            "next-step-has-no-path": regex("last_message", "not_contains", r"Next step[\s\S]*docs/specs/prd"),
            "no-path-argument": regex("last_message", "not_contains", r"\$devforgeai:epic[ \t]+`?[^\s`]*(?:/|\.md)"),
            "lists-ready": regex("last_message", "contains", r"[Rr]eady for epic work"),
            "lists-blocked-with-decs": BLOCKS_FR_001,
            "no-epic-written": exists("docs/specs/epic/**", False),
        },
    },
    "ignores-unrelated-request": {
        "ver": "11", "files": SHARED, "negative": True,
        "prompt": "Explain the architecture of the Linux kernel: how the scheduler, memory management and the\nvirtual file system fit together.\n",
        "description": "VER-11: a request to explain the Linux kernel's architecture must not trigger the skill or write an ARCH.",
        "graders": {
            "skill-not-fired": NOT_FIRED,
            "no-arch-written": exists("docs/specs/arch/**", False),
        },
    },
    "records-provenance": {
        "ver": "14", "files": SHARED, "prompt": PROMPT,
        "description": "VER-14: with no policy, the ARCH records generated_by, an empty reviewed_by, null hashes, a Policy resolution line with the three defaults, and no POL link.",
        "graders": {
            "arch-exists": ARCH_CREATED,
            "generated-by-filled": regex(ARCH, "contains",
                                         r'^generated_by:\n^  tool: "codex"\n^  model: "[^"\n]+"\n^  session: "[^"\n]+"\n', "m"),
            "session-substituted": regex(ARCH, "contains",
                                         r'^  session: "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"', "m"),
            "reviewed-by-empty": regex(ARCH, "contains", r"^reviewed_by: \[\]", "m"),
            "hashes-null": regex(ARCH, "not_contains", r"hash: (?!null\b)"),
            "changelog-names-session": regex(ARCH, "contains",
                                             r"## Change Log[\s\S]*\| codex \(session [0-9a-f]{8}-[0-9a-f-]{27}\) \|"),
            "resolution-max-calls": regex(ARCH, "contains", r"Policy resolution:[^\n]*interview\.max_calls=8 \(default\)"),
            "resolution-platforms": regex(ARCH, "contains",
                                          r"Policy resolution:[^\n]*architecture\.mandated_platforms=none \(default\)"),
            "resolution-categories": regex(ARCH, "contains",
                                           r"Policy resolution:[^\n]*quality\.required_categories=floor only \(default\)"),
            "no-policy-link": regex(ARCH, "not_contains", r"id: POL-"),
        },
    },
    "reuse-records-review": {
        "ver": "15",
        "files": dict(docs__specs__prd__PRD_001=PRD_V2, docs__specs__arch__ARCH_001=ARCH_TO_REVIEW,
                      docs__specs__adr__ADR_001=ADR_AUTH0),
        "prompt": "PRD-001 is now at version 2, but only a priority changed. Reuse ARCH-001 for it; I confirm the\n"
                  "reuse outcome. Proceed without questions.\n",
        "description": "VER-15: confirming reuse against PRD-001 v2 relinks ARCH-001's frontmatter to v2, sets outcome reuse, keeps version, status, approval and item links, and adds exactly one review row.",
        "graders": {
            "prd-link-v2": regex(ARCH, "contains",
                                 r"^upstream:\n  - \{id: PRD-001, relation: informed_by, version: 2, hash: null\}\n", "m"),
            "outcome-reuse": regex(ARCH, "contains", r"^outcome: reuse[ \t]*$", "m"),
            "version-status-unchanged": regex(ARCH, "contains",
                                              r"^status: approved\n^version: 1\n^created: 2026-09-21\n^updated: 2026-09-22\n", "m"),
            "approval-unchanged": regex(ARCH, "contains", r'^approved_by: "Priya Nair"\n^approved_on: 2026-09-22\n', "m"),
            "generated-by-unchanged": regex(ARCH, "contains", r'^  session: "fixture-session"\n', "m"),
            "item-link-still-v1": regex(ARCH, "contains",
                                        r"- \{id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null\}"),
            "review-row": regex(ARCH, "contains",
                                r"\| Reviewed against PRD-001 v2: reuse confirmed, no architectural change[^\n|]*Policy resolution:"),
            "one-review-row": regex(ARCH, "not_contains", r"Reviewed against PRD-\d{3} v\d[\s\S]*Reviewed against PRD-\d{3} v\d"),
        },
    },
    "reuse-review-idempotent": {
        "ver": "16",
        "files": dict(docs__specs__prd__PRD_001=PRD_V2, docs__specs__arch__ARCH_001=ARCH_REVIEWED,
                      docs__specs__adr__ADR_001=ADR_AUTH0),
        "prompt": "PRD-001 is now at version 2, but only a priority changed. Reuse ARCH-001 for it; I confirm the\n"
                  "reuse outcome. Proceed without questions.\n",
        "description": "VER-16: ARCH-001 already cites PRD-001 v2 and has one review row, so confirming reuse again writes nothing.",
        "graders": {
            "version-status-unchanged": regex(ARCH, "contains",
                                              r"^status: approved\n^version: 1\n^created: 2026-09-21\n^updated: 2026-09-22\n", "m"),
            "prd-link-v2": regex(ARCH, "contains",
                                 r"^upstream:\n  - \{id: PRD-001, relation: informed_by, version: 2, hash: null\}\n", "m"),
            "one-review-row": regex(ARCH, "contains",
                                    r"^(?![\s\S]*Reviewed against PRD-\d{3} v\d[\s\S]*Reviewed against PRD-\d{3} v\d)[\s\S]*"
                                    r"\(session prior-review-session\) \| Reviewed against PRD-001 v2: reuse confirmed"),
            "no-arch-002": exists("docs/specs/arch/ARCH-002.md", False),
        },
    },
}


def main():
    for label, (text, schema) in FIXTURES.items():
        validate(label, text, schema)
    for name, case in CASES.items():
        d = ROOT / name
        (d / "graders").mkdir(parents=True, exist_ok=True)
        tags = f"[architecture, ver-{case['ver']}" + (", negative-trigger]" if case.get("negative") else "]")
        turns, timeout = ("15", "300") if case.get("negative") else ("60", "1200")
        (d / "prompt.md").write_text(
            f"---\ndescription: \"{case['description']}\"\ntags: {tags}\nmax_turns: {turns}\n"
            f"timeout_seconds: {timeout}\nallowed_tools: {TOOLS}\n---\n{case['prompt']}")
        (d / "case.yaml").write_text(f"schema_version: \"1.1\"\nname: {name}\ncontext:\n  scaffold_script: scaffold.sh\n")
        (d / "scaffold.sh").write_text(scaffold(f"Seeds the fixtures for SPEC-003 VER-{case['ver']} ({name}).",
                                                **files(**case["files"])))
        os.chmod(d / "scaffold.sh", 0o755)
        for g, body in case["graders"].items():
            (d / "graders" / f"{g}.md").write_text(body)
    print("validated", len(FIXTURES), "fixtures; wrote", len(CASES), "cases")


if __name__ == "__main__":
    main()
