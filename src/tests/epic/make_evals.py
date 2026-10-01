"""Generates evals/epic/<case>/ (SPEC-004 v2 VER-01..12, 14 to 19): prompts, graders, case.yaml and the inline
scaffold fixtures. Every fixture is defined once here, from SPEC-004 §9's shared fixture, and validated
against src/schemas/ before anything is written. Edit fixtures and graders here, then regenerate; it
overwrites the case files and never deletes a grader, so remove renamed ones by hand. Run from the
repository root:

    python3 src/tests/epic/make_evals.py
"""
import json
import os
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry, Resource

ROOT = Path("src/claude/DevForgeAI/evals/epic")
SCHEMAS = Path("src/schemas")
TOOLS = "[Skill, Read, Glob, Grep, Write, Edit, Bash]"

# --- Fixtures -------------------------------------------------------------------------------------
# SPEC-004 v2 §9: PRD-001 v2 ("Spring launch") and ARCH-001, which cites it at version 2, in the shape the
# current prd (SKL-002 v3) and architecture (SKL-003 v5) skills write.
#   FR-001  must/current   DEC-01 open; a [NEEDS ADR] marker names it          -> blocked (DEC-01)
#   FR-002  must/current   DEC-02 resolved by ADR-001 (accepted)                -> eligible
#   FR-003  should/current no DEC                                               -> eligible
#   FR-004  could/current  no DEC                                               -> eligible
#   FR-005  null/later     DEC-06 open (prd writes a later requirement so)      -> later; DEC-06 open; not undecided
#   FR-006  wont/current   no DEC                                               -> wont
#   FR-007  null/current   no DEC                                               -> undecided
#   FR-008  must/current   DEC-03 resolved by ADR-002, superseded by ADR-003    -> blocked (DEC-03)
#   FR-009  must/current   no DEC; a [NEEDS ADR] marker names it                -> blocked (unmatched marker)
#   FR-010  must/current   DEC-04 (audit storage) resolved by ADR-003; a payment-provider marker
#                          names it and no DEC answers it                       -> blocked (unmatched marker)
#   FR-011  must/current   DEC-05 resolved by ADR-004, whose file is missing    -> unknown
#   FR-012  must/current   DEC-07 resolved by POL-001#SET-01 (passes the check) -> eligible
#   NFR-001 must/current   DEC-02                                               -> eligible
#   NFR-002 null/null      no DEC; the constraint NFR for POL-001#SET-01        -> undecided (the PRD owner decides)


def fr(num, statement, priority, release, idea="IDEA-01"):
    return f"""\
  - id: FR-{num}
    status: active
    statement: "{statement}"
    priority: {priority}
    release: {release}
    notes: null
    upstream:
      - {{id: BRN-001, item: {idea}, relation: derives, version: 1, hash: null}}
"""


FRS = "".join([
    fr("001", "The system shall let a volunteer sign in.", "must", "current"),
    fr("002", "The system shall let a signed-in volunteer book an open warehouse shift.", "must", "current"),
    fr("003", "The system shall show the coordinator each day's roster of booked volunteers.", "should", "current",
       "IDEA-02"),
    fr("004", "The system shall let a volunteer add a booked shift to their phone's calendar.", "could", "current"),
    fr("005", "The system shall let two volunteers swap booked shifts with each other.", "null", "later"),
    fr("006", "The system shall reimburse volunteers' travel costs.", "wont", "current", "IDEA-03"),
    fr("007", "The system shall let the coordinator message every volunteer booked on a shift.", "null", "current",
       "IDEA-02"),
    fr("008", "The system shall text a volunteer a reminder the day before a booked shift.", "must", "current"),
    fr("009", "The system shall import the current volunteer list from the coordinator's spreadsheet.", "must",
       "current", "IDEA-02"),
    fr("010", "The system shall let a volunteer pay the yearly membership fee online.", "must", "current",
       "IDEA-03"),
    fr("011", "The system shall send each month's volunteer hours to the regional food bank network.", "must",
       "current", "IDEA-02"),
    fr("012", "The system shall email a volunteer a confirmation when they book a shift.", "must", "current"),
])

MARKER_IDP = "[NEEDS ADR: identity provider for volunteer sign-in; affects FR-001]"
MARKER_IMPORT = ("[NEEDS ADR: how the volunteer list is imported from the coordinator's spreadsheet and kept "
                 "in step with it; affects FR-009]")
MARKER_PAYMENT = "[NEEDS ADR: payment provider for membership fees; affects FR-010]"

# POL-001#SET-01 as the prd and architecture skills record it (ADR-003 A5; policy.md R5 and the resolution line).
MAIL_PLATFORM, MAIL_CAPABILITY = "Regional network mail relay (SMTP)", "transactional email"
SIGNIN_PLATFORM, SIGNIN_CAPABILITY = "Riverside council sign-in (OIDC)", "volunteer sign-in"  # POL-002 (VER-16)


def mandate(platform, capability, setting):
    return f"architecture.mandated_platforms={platform} for {capability} ({setting})"


MAIL_ENTRY = mandate(MAIL_PLATFORM, MAIL_CAPABILITY, "POL-001#SET-01")
SIGNIN_ENTRY = mandate(SIGNIN_PLATFORM, SIGNIN_CAPABILITY, "POL-002#SET-01")


def resolution(*mandates):
    """A resolution line in the policy.md format; architecture and prd resolve no testing keys."""
    return ("Policy resolution: interview.max_calls=8 (default); "
            + "; ".join(mandates or ["architecture.mandated_platforms=none (default)"])
            + "; quality.required_categories=floor only (default)")

PRD = f"""\
---
id: PRD-001
type: prd
title: "Volunteer shift sign-up for the Riverside Food Bank"
status: approved
version: 2
created: 2026-09-14
updated: 2026-09-18
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-18
upstream:
  - {{id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Spring launch"
stage: mvp
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-001 — Volunteer shift sign-up for the Riverside Food Bank

## 1. Summary

Let the food bank's volunteers book warehouse shifts themselves instead of by phone, remind them before
each shift, and give the coordinator a live roster.

## 2. Problem and opportunity

The coordinator fills three warehouse shifts a day by phone, and about one shift in six starts
short-staffed (BRN-001#PRB-01).

## 3. Users and personas

About 120 active volunteers, who book from their phones, and one volunteer coordinator.

## 4. Goals and non-goals

**Goals**
- Volunteers book their own shifts, and fewer shifts start short-staffed.

**Non-goals** (explicitly out of scope)
- Payroll; volunteers aren't paid.

## 5. Success metrics

```yaml items
success_metrics:
  - id: SM-01
    status: active
    metric: "Share of shifts that start fully staffed"
    baseline: "83%"
    target: "95% by the end of the spring launch"
    measured_by: "Coordinator's shift log"
    upstream:
      - {{id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}}
```

## 6. Functional requirements

```yaml items
functional_requirements:
{FRS}```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: privacy
    statement: "Volunteer phone numbers are visible only to the coordinator."
    priority: must
    release: current
  - id: NFR-002
    status: active
    category: constraint
    statement: "Emails to volunteers are sent through the {MAIL_PLATFORM} (applies to {MAIL_CAPABILITY})."
    priority: null
    release: null
    upstream:
      - {{id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}}
```

## 8. User experience

Mobile-first web pages; no app to install.

## 9. Constraints and dependencies

The food bank is a member of the regional food bank network, whose IT policy applies: email goes through
the network's mail relay (NFR-002).

## 10. Assumptions and risks

```yaml items
assumptions:
  - id: ASM-01
    status: active
    statement: "Most volunteers have a smartphone with a web browser."
    validation: "Ask at the September volunteer meeting"
    state: open
    upstream:
      - {{id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}}
```

## 11. Release and rollout

The spring launch covers every warehouse shift; shift swaps (FR-005) follow in a later release.

## 12. Open questions

- {MARKER_IDP}
- {MARKER_IMPORT}
- {MARKER_PAYMENT}

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-14 | claude-code (session fixture-session) | Initial draft from BRN-001. {resolution(MAIL_ENTRY)} | all |
| 1 | 2026-09-16 | Priya Nair | Approved | status |
| 2 | 2026-09-18 | Priya Nair | Added FR-012 (booking confirmation email) and moved FR-005 to a later release | FR-005, FR-012 |
| 2 | 2026-09-18 | Priya Nair | Approved | status |
"""


def replace(text, old, new):
    assert text.count(old) == 1, f"fixture edit anchor not unique: {old!r}"
    return text.replace(old, new)


# VER-08: the same PRD, still a draft.
PRD_DRAFT = replace(PRD, "status: approved\nversion: 2", "status: draft\nversion: 2")
PRD_DRAFT = replace(PRD_DRAFT, 'reviewed_by: ["Priya Nair"]\napproved_by: "Priya Nair"\napproved_on: 2026-09-18',
                    'reviewed_by: []\napproved_by: ""\napproved_on: null')
PRD_DRAFT = replace(PRD_DRAFT, "| 1 | 2026-09-16 | Priya Nair | Approved | status |\n", "")
PRD_DRAFT = replace(PRD_DRAFT, "| 2 | 2026-09-18 | Priya Nair | Approved | status |\n", "")


def fr2(num, statement):
    """An FR of PRD-002, the coordinator's reports (VER-18)."""
    return fr(num, statement, "must", "current").replace("BRN-001, item: IDEA-01", "BRN-002, item: IDEA-01")


# VER-18: a second approved PRD for the same system; its FR-003 shares a number with PRD-001's FR-003.
PRD2 = f"""\
---
id: PRD-002
type: prd
title: "Coordinator reports for the Riverside Food Bank"
status: approved
version: 1
created: 2026-09-25
updated: 2026-09-26
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: 2026-09-26
upstream:
  - {{id: BRN-002, item: PRB-01, relation: derives, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- prd-specific ---
target_release: "Autumn reports"
stage: evolution
operating_context: internal
stakeholders: ["Priya Nair"]
---

# PRD-002 — Coordinator reports for the Riverside Food Bank

## 1. Summary

Give the coordinator monthly reports on shifts and volunteer hours, built on the shift sign-up system
(PRD-001).

## 2. Problem and opportunity

The coordinator rebuilds the monthly figures by hand from the shift log (BRN-002#PRB-01).

## 3. Users and personas

The volunteer coordinator.

## 4. Goals and non-goals

**Goals**
- Monthly figures without manual work.

**Non-goals** (explicitly out of scope)
- Payroll.

## 5. Success metrics

```yaml items
success_metrics: []
```

## 6. Functional requirements

```yaml items
functional_requirements:
{fr2("001", "The system shall show the coordinator each month's filled and short-staffed shifts.")}{
fr2("002", "The system shall show the coordinator each volunteer's hours for a chosen month.")}{
fr2("003", "The system shall export each month's report to the regional food bank network.")}```

## 7. Non-functional requirements

```yaml items
non_functional_requirements:
  - id: NFR-001
    status: active
    category: constraint
    statement: "Emails to volunteers are sent through the {MAIL_PLATFORM} (applies to {MAIL_CAPABILITY})."
    priority: null
    release: null
    upstream:
      - {{id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}}
```

## 8. User experience

Report pages in the coordinator's web app.

## 9. Constraints and dependencies

Builds on PRD-001's shift data.

## 10. Assumptions and risks

```yaml items
assumptions: []
```

## 11. Release and rollout

All three reports ship in the autumn.

## 12. Open questions

- None.

## 13. Epic map

<!-- GENERATED: epics whose upstream cites this PRD. Do not edit by hand. -->

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-25 | claude-code (session fixture-session) | Initial draft from BRN-002. {resolution(MAIL_ENTRY)} | all |
| 1 | 2026-09-26 | Priya Nair | Approved | status |
"""


def prd_link(item, version=2):
    return f"  - {{id: PRD-001, item: {item}, relation: informed_by, version: {version}, hash: null}}\n"


def adr(num, title, status, created, context, outcome, history, upstream,
        supersedes="[]", superseded_by="null"):
    """An ADR fixture in the architecture skill's assets/adr.md shape."""
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

Reviewed when the spring launch ends.

## Pros and cons of the options

### {title}
- Good, because it settles the question now.

### Do nothing for now
- Bad, because epics would each decide on their own.

## Status history

| Date | Status | Note |
|---|---|---|
{history}"""


ADR_DATA = adr(
    "001", "Keep shift, booking and contact data in one managed PostgreSQL database owned by the shift service",
    "accepted", "2026-09-21",
    "Bookings (PRD-001#FR-002) and private phone numbers (PRD-001#NFR-001) need one owner (ARCH-001#DEC-02).",
    "one managed PostgreSQL database, owned by the shift service, because it keeps phone numbers behind one API.",
    "| 2026-09-21 | accepted | Decided by Priya Nair |\n", prd_link("FR-002") + prd_link("NFR-001"))

ADR_SMS = adr(
    "002", "Send shift reminders through the SMS modem on the food bank's on-premises server", "superseded",
    "2026-09-21",
    "Volunteers get a text reminder before each shift (PRD-001#FR-008, ARCH-001#DEC-03), and the food bank "
    "owned a server with an SMS modem in its back office.",
    "the on-premises SMS modem, because it was already paid for.",
    "| 2026-09-21 | accepted | Decided by Priya Nair |\n| 2026-09-24 | superseded | Superseded by ADR-003 |\n",
    prd_link("FR-008"), superseded_by="ADR-003")

ADR_AUDIT = adr(
    "003", "Retire the on-premises server and keep membership-payment audit records in the hosting provider's log store",
    "accepted", "2026-09-24",
    "Membership payments (PRD-001#FR-010) need an audit trail kept for seven years (ARCH-001#DEC-04). The "
    "back-office server is being removed at the end of October, so nothing can stay on it, including the SMS "
    "modem that ADR-002 chose. This decision settles where audit records are kept; how reminders are sent "
    "instead is a separate decision that has not been made.",
    "the hosting provider's log store with seven-year retention, and retire the on-premises server.",
    "| 2026-09-24 | accepted | Decided by Priya Nair |\n", prd_link("FR-010"), supersedes="[ADR-002]")


def policy(set_status, version=1):
    """POL-001: the regional network's mandated email platform (SPEC-004 §9). Version 2 (VER-17) adds a testing
    setting, SET-02, and leaves SET-01 exactly as it was."""
    updated, ref = ("2026-09-26", "v1.1.0") if version == 2 else ("2026-08-15", "v1.0.0")
    set_02 = """\
  - id: SET-02
    status: active
    key: testing.coverage_threshold
    class: organizational_policy
    value: 80
    overridable_by: []
    rationale: "Member food banks' systems keep at least 80% line coverage"
""" if version == 2 else ""
    row_2 = "| 2 | 2026-09-26 | Network IT group | Added SET-02 (testing.coverage_threshold) | SET-02 |\n" if version == 2 else ""
    return f"""\
---
id: POL-001
type: policy
title: "Regional Food Bank Network IT policy (vendored)"
status: approved
version: {version}
created: 2026-08-01
updated: {updated}
owner: "Regional Food Bank Network IT group"
authors: ["Regional Food Bank Network IT group"]
reviewed_by: ["Regional Food Bank Network IT group"]
approved_by: "Regional Food Bank Network director"
approved_on: {updated}
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: organization
source: {{repository: "github.com/regional-food-bank-network/it-policy", ref: "{ref}"}}
---

# POL-001 — Regional Food Bank Network IT policy (vendored)

## 1. Scope and ownership

Applies to the systems of every member food bank. Owned by the network's IT group; changes need the
director's approval.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: {set_status}
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "{MAIL_CAPABILITY}"
      platform: "{MAIL_PLATFORM}"
      source: "Network IT standard 4 (email)"
    overridable_by: []
    rationale: "Member food banks send email only through the network relay, so every message passes its privacy checks"
{set_02}```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-08-15 | Network IT group | Initial policy | SET-01 |
{row_2}"""


POL = policy("active")
POL_REVOKED = policy("deprecated")  # VER-15: the setting that resolves DEC-07 is no longer active
POL_V2 = policy("active", version=2)  # VER-17: POL-001 bumped, SET-01 unchanged

# VER-16: the food bank's own project policy, approved after PRD-001 v2 and before ARCH-001.
POL_PROJECT = f"""\
---
id: POL-002
type: policy
title: "Riverside Food Bank IT policy"
status: approved
version: 1
created: 2026-09-19
updated: 2026-09-20
owner: "Priya Nair"
authors: ["Priya Nair"]
reviewed_by: []
approved_by: "Priya Nair"
approved_on: 2026-09-20
upstream: []
supersedes: []
superseded_by: null
blocked_by: []
# --- policy-specific ---
scope: project
source: null
---

# POL-002 — Riverside Food Bank IT policy

## 1. Scope and ownership

Applies to the Riverside Food Bank's own systems. Owned by the volunteer coordinator.

## 2. Settings

```yaml items
settings:
  - id: SET-01
    status: active
    key: architecture.mandated_platforms
    class: organizational_policy
    value:
      capability: "{SIGNIN_CAPABILITY}"
      platform: "{SIGNIN_PLATFORM}"
      source: "Riverside council IT agreement, 2026"
    overridable_by: []
    rationale: "The council funds the food bank's systems on condition that people sign in through its service"
```

## Change Log

| Version | Date | Author | Change | Settings affected |
|---|---|---|---|---|
| 1 | 2026-09-20 | Priya Nair | Initial policy | SET-01 |
"""


def item(lines):
    return "".join(f"    {l}\n" if i else f"  - {l}\n" for i, l in enumerate(lines))


def ups(*items, version=2, prd="PRD-001"):
    return ["upstream:"] + [f"  - {{id: {prd}, item: {i}, relation: informed_by, version: {version}, hash: null}}"
                            for i in items]


def dec(num, question, state, resolved_by, *cites, prd="PRD-001", version=2):
    return item([f"id: DEC-{num}", "status: active", f'question: "{question}"', "blocking: true", f"state: {state}",
                 f"resolved_by: {resolved_by}", "notes: null"] + ups(*cites, version=version, prd=prd))


def evd(num, source, kind, finding, classification):
    return item([f"id: EVD-{num}", "status: active", f'source: "{source}"', f"kind: {kind}", f'finding: "{finding}"',
                 f"classification: {classification}"])


def kinds(*ks):
    return ["kinds:"] + [f'  - "{k}"' for k in ks]


def arch(prd_version, *, signin=False, prd2=False, extra_dec=""):
    """ARCH-001, approved, citing PRD-001 at prd_version (SPEC-004 §9; VER-06 uses version 1).

    signin: DEC-01 is resolved by the project policy's mandated sign-in platform, POL-002#SET-01 (VER-16).
    prd2: amended to version 2 and approved again, also covering PRD-002 v1 (VER-18).
    extra_dec: a DEC-08 item block (VER-18, VER-19)."""
    mandates = (MAIL_ENTRY, SIGNIN_ENTRY) if signin else (MAIL_ENTRY,)
    version, updated, outcome = (2, "2026-09-28", "amend") if prd2 else (1, "2026-09-24", "create")
    prd2_link = "  - {id: PRD-002, relation: informed_by, version: 1, hash: null}\n" if prd2 else ""
    amended = (f"| 2 | 2026-09-27 | claude-code (session fixture-session) | Amended to cover PRD-002 v1: DEC-08 added. "
               f"Status approved to in-review, approval cleared. {resolution(*mandates)} | DEC-08 |\n"
               "| 2 | 2026-09-28 | Priya Nair | Approved | status |\n") if prd2 else ""
    signin_dec = ("resolved", "[POL-002#SET-01]") if signin else ("open", "[]")
    signin_cmp = ([f'deployment: "External: {SIGNIN_PLATFORM}"', "upstream:",
                   "  - {id: POL-002, item: SET-01, relation: constrains, version: 1, hash: null}"] if signin
                  else ['deployment: "External; the provider is open (DEC-01)"'])
    signin_deploy = (f"sign-in goes through the {SIGNIN_PLATFORM} (POL-002#SET-01)" if signin
                     else "the identity provider is open (DEC-01)")
    more_evd = (evd("07", "POL-002#SET-01", "policy", f"Version 1, status approved, setting active: {SIGNIN_CAPABILITY} "
                    f"goes through the {SIGNIN_PLATFORM}.", "policy") if signin
                else evd("07", "PRD-002", "prd", "Version 1, status approved: three functional requirements for the "
                         "coordinator's reports.", "context") if prd2 else "")
    scope = (" Version 2 also covers PRD-002 version 1 (approved), the coordinator's reports." if prd2 else "")
    return f"""\
---
id: ARCH-001
type: arch
title: "Riverside Food Bank volunteer shift sign-up architecture"
status: approved
version: {version}
created: 2026-09-22
updated: {updated}
owner: "Priya Nair"
authors: ["Priya Nair", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fixture-session"
reviewed_by: ["Priya Nair"]
approved_by: "Priya Nair"
approved_on: {updated}
upstream:
  - {{id: PRD-001, relation: informed_by, version: {prd_version}, hash: null}}
{prd2_link}supersedes: []
superseded_by: null
blocked_by: []
# --- arch-specific ---
system: "Riverside Food Bank volunteer shift sign-up"
outcome: {outcome}
inspection_scope: []
---

# ARCH-001 — Riverside Food Bank volunteer shift sign-up architecture

## 1. Context and scope

Defined against PRD-001 version {prd_version} (approved): volunteers sign in, book warehouse shifts and get
reminders; the coordinator sees the roster; membership fees are paid online. Payroll is outside the
system. No inspection scope was named, and no code was inspected.{scope}

## 2. Quality drivers

NFR-001 (phone numbers visible only to the coordinator) drives data ownership. The regional network's
mandated mail relay (POL-001#SET-01, PRD-001#NFR-002) constrains email.

## 3. Components

```mermaid
flowchart LR
    W[CMP-01 Volunteer web app] --> S[CMP-02 Shift service]
    W --> I[CMP-03 Identity provider]
    S --> M[CMP-04 Mail relay]
```

```yaml items
components:
{item(["id: CMP-01", "status: active", 'name: "Volunteer web app"'] + kinds("user-interface") + [
       'responsibility: "Sign-in, booking, roster and payment screens; holds no data of its own"', "owns_data: []",
       "interacts_with:", '  - "CMP-02"', '  - "CMP-03"', 'deployment: "Static site on the hosting provider"'])
 }{item(["id: CMP-02", "status: active", 'name: "Shift service"'] + kinds("service", "relational-store") + [
         'responsibility: "Shifts, bookings, reminders and volunteer contact details"', "owns_data:",
         '  - "Shifts and bookings"', '  - "Volunteer phone numbers"', "interacts_with:", '  - "CMP-01"',
         '  - "CMP-04"', 'deployment: "One hosted service with its database (ADR-001)"'] + ups("NFR-001"))
 }{item(["id: CMP-03", "status: active", 'name: "Identity provider"'] + kinds("external") + [
         'responsibility: "Authenticates volunteers and issues sessions"', "owns_data:", '  - "Volunteer credentials"',
         "interacts_with:", '  - "CMP-01"'] + signin_cmp)
 }{item(["id: CMP-04", "status: active", 'name: "Mail relay"'] + kinds("external") + [
         'responsibility: "Delivers the emails the shift service sends; external, provided by the regional network"',
         "owns_data: []", "interacts_with:", '  - "CMP-02"', f'deployment: "External: {MAIL_PLATFORM}"', "upstream:",
         "  - {id: PRD-001, item: NFR-002, relation: informed_by, version: 2, hash: null}",
         "  - {id: POL-001, item: SET-01, relation: constrains, version: 1, hash: null}"])
 }```

## 4. Architectural questions

```yaml items
decisions:
{dec("01", "Which identity provider handles volunteer sign-in?", *signin_dec, "FR-001")
 }{dec("02", "Where are shift, booking and contact data stored, and which component owns them?", "resolved",
       "[ADR-001]", "FR-002", "NFR-001")
 }{dec("03", "How are shift reminders sent to volunteers' phones?", "resolved", "[ADR-002]", "FR-008")
 }{dec("04", "Where are the audit records of membership payments stored?", "resolved", "[ADR-003]", "FR-010")
 }{dec("05", "How are each month's volunteer hours sent to the regional food bank network?", "resolved",
       "[ADR-004]", "FR-011")
 }{dec("06", "How are shift-swap requests passed between volunteers?", "open", "[]", "FR-005")
 }{dec("07", "Which email service sends booking confirmations?", "resolved", "[POL-001#SET-01]", "FR-012")
 }{extra_dec}```

## 5. Evidence inspected

```yaml items
evidence:
{evd("01", "PRD-001", "prd", f"Version {prd_version}, status approved: twelve functional requirements, NFR-001 and "
     "NFR-002; three NEEDS ADR markers.", "context")
 }{evd("02", "ADR-001", "adr", "Version 1, status accepted: the shift service owns shift, booking and contact data "
       "in one managed PostgreSQL database.", "decided")
 }{evd("03", "ADR-002", "adr", "Version 1, status accepted: reminders go through the on-premises SMS modem.",
       "decided")
 }{evd("04", "ADR-003", "adr", "Version 1, status accepted: membership-payment audit records are kept in the "
       "hosting provider's log store.", "decided")
 }{evd("05", "ADR-004", "adr", "Version 1, status accepted: monthly hours are uploaded as a CSV file to the "
       "regional network's portal.", "decided")
 }{evd("06", "POL-001#SET-01", "policy", "Version 1, status approved, setting active: transactional email goes "
       "through the regional network mail relay.", "policy")
 }{more_evd}```

## 6. Deployment

The web app and the shift service run on the hosting provider; {signin_deploy},
and email goes through the regional network's relay.

## 7. Requirement changes proposed to the PRD owner

- None.

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-22 | claude-code (session fixture-session) | Initial draft for PRD-001 v{prd_version}. {resolution(*mandates)} | all |
| 1 | 2026-09-24 | Priya Nair | Approved | status |
{amended}"""


ARCH = arch(2)
ARCH_STALE = arch(1)  # VER-06: not reviewed against PRD-001 version 2
# VER-16: an organization and a project policy each mandate a platform, for different capabilities.
ARCH_TWO_LAYERS = arch(2, signin=True)
# VER-18: ARCH-001 v2 also covers PRD-002, and its open DEC-08 cites only PRD-002#FR-003.
ARCH_TWO_PRDS = arch(2, prd2=True, extra_dec=dec(
    "08", "How are the coordinator's monthly reports exported to the regional network?", "open", "[]", "FR-003",
    prd="PRD-002", version=1))
# VER-19: an open hosting question blocks every requirement that would otherwise be eligible.
ARCH_HOSTING_OPEN = arch(2, extra_dec=dec(
    "08", "Which hosting provider runs the web app and the shift service?", "open", "[]",
    "FR-002", "FR-003", "FR-004", "FR-012", "NFR-001"))
ARCH_BAD_DATE = ARCH.replace("updated: 2026-09-24", "updated: 2026-02-30")  # issue #15; no case uses it

SENTINEL = "SENTINEL-7F3A: hand-written note that every run must leave in place."


def epic(*, title, status, session, links, goal, scope_in, dw, changelog):
    """An existing EPIC-001 in the assets/epic.md shape (VER-07, VER-14)."""
    approved_by, approved_on, reviewed = (('"Priya Nair"', "2026-09-25", '["Priya Nair"]') if status == "approved"
                                          else ('""', "null", "[]"))
    return f"""\
---
id: EPIC-001
type: epic
title: "{title}"
status: {status}
version: 1
created: 2026-09-25
updated: 2026-09-25
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
{links}  - {{id: ARCH-001, relation: informed_by, version: 1, hash: null}}
supersedes: []
superseded_by: null
blocked_by: []
# --- epic-specific ---
priority: must
target_release: "Spring launch"
---

# EPIC-001 — {title}

## 1. Goal

{goal}

## 2. Business value

Fewer phone calls for the coordinator and fewer short-staffed shifts (PRD-001#SM-01).

## 3. Scope

**In scope**
{scope_in}
**Out of scope**
- Shift swaps (not planned for the spring launch)

## 4. Done when

```yaml items
done_when:
{dw}```

## 5. Dependencies and risks

Relies on ARCH-001#DEC-02 (ADR-001) for where bookings and phone numbers are stored.

## 6. Technical notes (optional)

{SENTINEL}

## 7. Story map

<!-- GENERATED from stories whose upstream cites this epic: story, title, status, DW satisfied.
     Do not edit by hand. -->

## 8. Open questions

- None.

## Change Log

| Version | Date | Author | Change |
|---|---|---|---|
{changelog}"""


def refines(item_id, note=None):
    n = f', note: "{note}"' if note else ""
    return f"  - {{id: PRD-001, item: {item_id}, relation: refines, version: 2, hash: null{n}}}\n"


# VER-07: an approved EPIC-001 that already refines FR-002, FR-008 and part of NFR-001.
EPIC_COVERING = epic(
    title="Shift booking and reminders", status="approved", session="fixture-session",
    links=refines("FR-002") + refines("FR-008") + refines("NFR-001", "partial: phone numbers on booking and reminders"),
    goal="Volunteers book an open warehouse shift from their phone and get a text reminder the day before, "
         "without calling the coordinator.",
    scope_in="- Booking an open shift (PRD-001#FR-002)\n- Text reminders (PRD-001#FR-008)\n",
    dw=item(["id: DW-01", "status: active",
             'criterion: "A volunteer books a shift on their phone and gets a reminder the day before it"',
             'evidence_method: "End-to-end test on a phone-sized browser"']),
    changelog="| 1 | 2026-09-25 | Priya Nair | Written by hand; approved |\n")

# VER-14: EPIC-001 as a first run would have written it, covering every eligible requirement.
EPIC_FIRST_RUN = epic(
    title="Self-service shift booking", status="draft", session="prior-epic-session",
    links=refines("FR-002") + refines("FR-003") + refines("FR-004") + refines("FR-012") + refines("NFR-001"),
    goal="Volunteers book warehouse shifts themselves and get a confirmation email, and the coordinator "
         "sees each day's roster.",
    scope_in=("- Booking an open shift (PRD-001#FR-002)\n- The coordinator's daily roster (PRD-001#FR-003)\n"
              "- Adding a shift to a phone calendar (PRD-001#FR-004)\n- Booking confirmation email (PRD-001#FR-012)\n"),
    dw=item(["id: DW-01", "status: active",
             'criterion: "A volunteer books a shift, gets the confirmation email, and appears on that day\'s roster"',
             'evidence_method: "End-to-end test with a test mailbox"']),
    changelog="| 1 | 2026-09-25 | claude-code (session prior-epic-session) | Initial draft from PRD-001 v2 and ARCH-001 v1 |\n")

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
    return doc


def setting(pol_text, set_id):
    return next(s for s in validate(set_id, pol_text, "policy.schema.json")["settings"] if s["id"] == set_id)


def last_resolution(arch_text):
    """The resolution line in an ARCH's last Change Log row that carries one (SPEC-004 v2 §4, check 3)."""
    return [l for l in arch_text.splitlines() if l.startswith("| ") and "Policy resolution:" in l][-1]


def entry(pol_text, pol_id, set_id):
    value = setting(pol_text, set_id)["value"]
    return mandate(value["platform"].strip(), value["capability"].strip(), f"{pol_id}#{set_id}")


def check_shared_fixture():
    """The shared fixture matches SPEC-004 v2 §9's table, so a regenerated case can't drift from the spec, and each
    variant holds the premise its VER item names."""
    prd = validate("PRD", PRD, "prd.schema.json")
    frs = {r["id"]: (r["priority"], r["release"]) for r in prd["functional_requirements"]}
    assert frs == {"FR-001": ("must", "current"), "FR-002": ("must", "current"), "FR-003": ("should", "current"),
                   "FR-004": ("could", "current"), "FR-005": (None, "later"), "FR-006": ("wont", "current"),
                   "FR-007": (None, "current"), "FR-008": ("must", "current"), "FR-009": ("must", "current"),
                   "FR-010": ("must", "current"), "FR-011": ("must", "current"), "FR-012": ("must", "current")}, frs
    nfrs = {r["id"]: (r["category"], r["priority"], r["release"]) for r in prd["non_functional_requirements"]}
    assert nfrs == {"NFR-001": ("privacy", "must", "current"), "NFR-002": ("constraint", None, None)}, nfrs
    decs = {d["id"]: (d["state"], d["resolved_by"], [u["item"] for u in d["upstream"]])
            for d in validate("ARCH", ARCH, "arch.schema.json")["decisions"]}
    assert decs == {"DEC-01": ("open", [], ["FR-001"]), "DEC-02": ("resolved", ["ADR-001"], ["FR-002", "NFR-001"]),
                    "DEC-03": ("resolved", ["ADR-002"], ["FR-008"]), "DEC-04": ("resolved", ["ADR-003"], ["FR-010"]),
                    "DEC-05": ("resolved", ["ADR-004"], ["FR-011"]), "DEC-06": ("open", [], ["FR-005"]),
                    "DEC-07": ("resolved", ["POL-001#SET-01"], ["FR-012"])}, decs
    # Every CMP carries kinds (architecture v5, self-check 8).
    for a in (ARCH, ARCH_TWO_LAYERS, ARCH_TWO_PRDS, ARCH_HOSTING_OPEN):
        assert all(c.get("kinds") for c in validate("ARCH", a, "arch.schema.json")["components"])
    # Check 3: each ARCH's latest resolution line holds the entry built from the policy it applied.
    assert entry(POL, "POL-001", "SET-01") == MAIL_ENTRY and MAIL_ENTRY in last_resolution(ARCH)
    assert entry(POL_PROJECT, "POL-002", "SET-01") == SIGNIN_ENTRY
    assert MAIL_ENTRY in last_resolution(ARCH_TWO_LAYERS) and SIGNIN_ENTRY in last_resolution(ARCH_TWO_LAYERS)
    # VER-16: the two layers mandate different capabilities (compared as validate_policy.py does).
    caps = {setting(p, "SET-01")["value"]["capability"].strip().lower() for p in (POL, POL_PROJECT)}
    assert len(caps) == 2, caps
    # VER-17: POL-001 is newer than the ARCH's link, and SET-01 is unchanged.
    assert validate("POL_V2", POL_V2, "policy.schema.json")["frontmatter"]["version"] == 2
    assert setting(POL_V2, "SET-01") == setting(POL, "SET-01") and MAIL_ENTRY in last_resolution(ARCH)
    # VER-18: ARCH-001 v2 cites both PRDs; DEC-08 cites only PRD-002#FR-003.
    two = validate("ARCH_TWO_PRDS", ARCH_TWO_PRDS, "arch.schema.json")
    assert [(u["id"], u["version"]) for u in two["frontmatter"]["upstream"]] == [("PRD-001", 2), ("PRD-002", 1)]
    assert [(u["id"], u["item"]) for d in two["decisions"] if d["id"] == "DEC-08" for u in d["upstream"]] == [
        ("PRD-002", "FR-003")]
    assert "FR-003" in {r["id"] for r in validate("PRD2", PRD2, "prd.schema.json")["functional_requirements"]}
    # VER-19: DEC-08 is open and cites every requirement that would otherwise be eligible.
    hosting = [d for d in validate("ARCH_HOSTING_OPEN", ARCH_HOSTING_OPEN, "arch.schema.json")["decisions"]
               if d["id"] == "DEC-08"]
    assert [(d["state"], [u["item"] for u in d["upstream"]]) for d in hosting] == [
        ("open", ["FR-002", "FR-003", "FR-004", "FR-012", "NFR-001"])]


FIXTURES = {
    "PRD": (PRD, "prd.schema.json"), "PRD_DRAFT": (PRD_DRAFT, "prd.schema.json"),
    "ADR_DATA": (ADR_DATA, "adr.schema.json"), "ADR_SMS": (ADR_SMS, "adr.schema.json"),
    "ADR_AUDIT": (ADR_AUDIT, "adr.schema.json"), "POL": (POL, "policy.schema.json"),
    "POL_REVOKED": (POL_REVOKED, "policy.schema.json"), "ARCH": (ARCH, "arch.schema.json"),
    "ARCH_STALE": (ARCH_STALE, "arch.schema.json"), "EPIC_COVERING": (EPIC_COVERING, "epic.schema.json"),
    "EPIC_FIRST_RUN": (EPIC_FIRST_RUN, "epic.schema.json"),
    "ARCH_BAD_DATE": (ARCH_BAD_DATE, "arch.schema.json", [("frontmatter", "updated")]),
    "POL_V2": (POL_V2, "policy.schema.json"), "POL_PROJECT": (POL_PROJECT, "policy.schema.json"),
    "PRD2": (PRD2, "prd.schema.json"), "ARCH_TWO_LAYERS": (ARCH_TWO_LAYERS, "arch.schema.json"),
    "ARCH_TWO_PRDS": (ARCH_TWO_PRDS, "arch.schema.json"), "ARCH_HOSTING_OPEN": (ARCH_HOSTING_OPEN, "arch.schema.json"),
}


def scaffold(comment, files):
    """A scaffold.sh that writes each fixture at its path."""
    out = f"#!/usr/bin/env bash\n# {comment}\nset -euo pipefail\n"
    out += "mkdir -p " + " ".join(sorted({os.path.dirname(p) for p in files})) + "\n"
    for p, text in files.items():
        out += f"cat > {p} <<'FIXTURE'\n{text}FIXTURE\n"
    return out


P_PRD, P_ARCH, P_POL = "docs/specs/prd/PRD-001.md", "docs/specs/arch/ARCH-001.md", "docs/specs/policy/POL-001.md"
ADRS = {"docs/specs/adr/ADR-001.md": ADR_DATA, "docs/specs/adr/ADR-002.md": ADR_SMS,
        "docs/specs/adr/ADR-003.md": ADR_AUDIT}
SHARED = {P_PRD: PRD, P_ARCH: ARCH, **ADRS, P_POL: POL}


def shared(**changes):
    """The shared fixture with some files replaced (a path mapped to None is left out)."""
    out = dict(SHARED)
    for p, text in changes.items():
        path = {"prd": P_PRD, "arch": P_ARCH, "pol": P_POL, "epic": "docs/specs/epic/EPIC-001.md",
                "pol2": "docs/specs/policy/POL-002.md", "prd2": "docs/specs/prd/PRD-002.md"}[p]
        if text is None:
            out.pop(path)
        else:
            out[path] = text
    return out


# --- Graders --------------------------------------------------------------------------------------

E1, E2, E3 = (f"docs/specs/epic/EPIC-00{n}.md" for n in (1, 2, 3))


def regex(target, match, pattern, flags=None):
    t = target if target == "last_message" else "{source: file, path: %s}" % target
    fl = f"flags: {flags}\n" if flags else ""
    return f"---\ntype: regex\ntarget: {t}\nmatch: {match}\n{fl}---\n{pattern}\n"


def exists(path, value):
    return f"---\ntype: file_exists\npath: {path}\nexists: {str(value).lower()}\n---\n"


def llm(text):
    return f"---\ntype: llm\n---\n\n{text}"


def refines_re(item_id):
    return rf"\{{id: PRD-001, item: {item_id}, relation: refines, version: 2, hash: null"


def has_refines(path, *item_ids):
    return regex(path, "contains", "".join(rf"(?=[\s\S]*{refines_re(i)})" for i in item_ids))


def lacks_refines(path, *item_ids):
    return regex(path, "not_contains", rf"item: (?:{'|'.join(item_ids)}), relation: refines")


def row(req, *parts):
    """A left-out row: the requirement and every part on one line, in any order."""
    return regex("last_message", "contains", rf"\b{req}\b" + "".join(rf"(?=[^\n]{{0,300}}{p})" for p in parts), "i")


SKILL_RE = "'\"skill\"\\s*:\\s*\"(?:[\\w-]+:)?epic\"'"
FIRED = f"---\ntype: tool_used\ntool: Skill\ninput_match: {SKILL_RE}\n---\n"
NOT_FIRED = f"---\ntype: tool_used\ntool: Skill\ninput_match: {SKILL_RE}\nmin: 0\nmax: 0\narm: both\n---\n"

INELIGIBLE = ["FR-001", "FR-005", "FR-006", "FR-007", "FR-008", "FR-009", "FR-010", "FR-011", "NFR-002"]
ELIGIBLE = ["FR-002", "FR-003", "FR-004", "FR-012", "NFR-001"]
ALL_SECTIONS = (r"## 1\. Goal\n[\s\S]*\n## 2\. Business value\n[\s\S]*\n## 3\. Scope\n[\s\S]*\n## 4\. Done when\n"
                r"[\s\S]*\n## 5\. Dependencies and risks\n[\s\S]*\n## 6\. Technical notes \(optional\)\n[\s\S]*"
                r"\n## 7\. Story map\n[\s\S]*\n## 8\. Open questions\n[\s\S]*\n## Change Log\n")
DW_ITEM = r'- id: DW-01\n[ \t]+status: active\n[ \t]+criterion: "[^"\n]+"\n[ \t]+evidence_method: "[^"\n]+"\n'
STORY_MAP = (r"## 7\. Story map\n\n<!-- GENERATED from stories whose upstream cites this epic: story, title, "
             r"status, DW satisfied\.\n[ \t]*Do not edit by hand\. -->\n\n## 8\. Open questions")
LEFTOVERS = (r"<!--(?! GENERATED from stories)|EPIC-000|PRD-000|YYYY-MM-DD|<capability name>|<item>|"
             r"<integrated outcome>|<end-to-end test|<question>|<which part>|<how this epic")
ENDS_WITH_NEXT_STEP = r"(?:^|\n)[ \t]*(?:\*\*|__)?Next step[^\n]*(?:\n(?![ \t]*\n)[^\n]*)*\s*$"
UNCHANGED_E1 = regex(E1, "contains", rf"^version: 1\n^created: 2026-09-25\n^updated: 2026-09-25\n[\s\S]*{SENTINEL}", "m")
NO_WRITE = exists("docs/specs/epic/**", False)

PROMPT_ONE = "Write the epics for PRD-001: put every eligible requirement into one epic.\nProceed without questions.\n"

CASES = {
    "selects-ready-current": {
        "ver": "01", "files": SHARED, "prompt": PROMPT_ONE,
        "description": "VER-01: the shared fixture with one epic requested; EPIC-001 refines exactly FR-002, FR-003, FR-004, FR-012 and NFR-001 at PRD-001 v2 (not NFR-002, which is undecided), from the template, with a DW item and the GENERATED story map.",
        "graders": {
            "skill-fired": FIRED,
            "epic-001-exists": exists(E1, True),
            "refines-fr-002": has_refines(E1, "FR-002"),
            "refines-fr-003": has_refines(E1, "FR-003"),
            "refines-fr-004": has_refines(E1, "FR-004"),
            "refines-fr-012": has_refines(E1, "FR-012"),
            "refines-nfr-001": has_refines(E1, "NFR-001"),
            "refines-nothing-else": lacks_refines(E1, *INELIGIBLE),
            "one-epic-only": exists("docs/specs/epic/EPIC-002.md", False),
            "priority-must": regex(E1, "contains", r"^priority: must[ \t]*$", "m"),
            "all-sections": regex(E1, "contains", ALL_SECTIONS),
            "done-when-item": regex(E1, "contains", DW_ITEM),
            "story-map-generated": regex(E1, "contains", STORY_MAP),
            "no-leftovers": regex(E1, "not_contains", LEFTOVERS),
        },
    },
    "blocked-not-included": {
        "ver": "02", "files": SHARED, "prompt": PROMPT_ONE,
        "description": "VER-02: no epic refines FR-001, FR-008, FR-009, FR-010 or FR-011; the reply reports FR-001 blocked by DEC-01, FR-008 by DEC-03 with ADR-002 superseded, FR-009 and FR-010 by unmatched NEEDS ADR markers, FR-011 unknown (ADR-004 missing), and never FR-002 or FR-012 as blocked.",
        "graders": {
            "epic-001-exists": exists(E1, True),
            "no-blocked-refines": lacks_refines(E1, "FR-001", "FR-008", "FR-009", "FR-010", "FR-011"),
            "fr-001-blocked-dec-01": row("FR-001", r"\bblocked\b", r"\bDEC-01\b"),
            "fr-008-blocked-dec-03": row("FR-008", r"\bblocked\b", r"\bDEC-03\b", r"ADR-002", r"supersed"),
            "fr-009-unmatched-marker": row("FR-009", r"\bblocked\b", r"marker"),
            "fr-010-unmatched-marker": row("FR-010", r"\bblocked\b", r"marker"),
            "fr-011-unknown": row("FR-011", r"\bunknown\b", r"ADR-004"),
            "ready-not-blocked": llm("""\
The workspace held PRD-001 (version 2) and ARCH-001. By the readiness rule, FR-002 (its question
DEC-02 is resolved by the accepted ADR-001) and FR-012 (DEC-07 is resolved by an approved, active
policy setting, POL-001#SET-01) are ready and eligible for an epic. FR-001, FR-008, FR-009 and
FR-010 are blocked, and FR-011 is unknown.

Judge only what the final reply says about FR-002 and FR-012.
PASS if neither FR-002 nor FR-012 is reported as blocked, unknown or left out, and the reply
presents both as included in an epic (or ready).
FAIL if either one is called blocked or unknown, is listed among the left-out requirements, or if
the reply says DEC-01 or DEC-02 blocks FR-002.
"""),
        },
    },
    "reports-left-out": {
        "ver": "03", "files": SHARED, "prompt": PROMPT_ONE,
        "description": "VER-03: the reply gives one row each for FR-005 (later; DEC-06 open; no action for the current release; not undecided), FR-006 (won't have), FR-007 and NFR-002 (undecided, for the PRD owner), each with a next action, and asks no question about them.",
        "graders": {
            "fr-005-later-dec-06": row("FR-005", r"\blater\b", r"\bDEC-06\b", r"current release"),
            "fr-006-wont": row("FR-006", r"\bwon[’']?t\b"),
            "fr-007-undecided": row("FR-007", r"\bundecided\b", r"PRD owner"),
            "nfr-002-undecided": row("NFR-002", r"\bundecided\b", r"PRD owner"),
            "one-row-each-no-questions": llm("""\
The workspace held PRD-001 with FR-005 (release later and priority null, which is how the PRD skill
writes every later requirement; its architectural question DEC-06 is open), FR-006 (priority wont),
FR-007 (priority null with release current, meaning undecided) and NFR-002 (priority and release both
null, meaning undecided). The user asked for one epic covering every eligible requirement and said to
proceed without questions.

Judge only the final reply.
PASS if all of these hold:
- FR-005, FR-006, FR-007 and NFR-002 each appear in a list of requirements left out of the epics,
  each in exactly one row, with its reasons and one next action: FR-005 is later, with no action for
  the current release; FR-006 is won't have, with none for this release; FR-007 and NFR-002 are
  undecided, and the PRD owner decides.
- FR-005's row doesn't call it undecided: a later requirement's null priority is normal.
- The reply asks the user no question about any of the four.
These are next actions, not missing ones: "No action for the current release" (FR-005), "No action
for this release" (FR-006), and "The PRD owner decides" (FR-007, NFR-002), which reports who owns the
decision and is not a question to the user. A row may list more than one reason, as FR-005's does
("later" and its open DEC-06). Mentions of these requirements in notes or in the Next step are not
rows.
FAIL if any of the four is missing, has a row with no next action at all, appears in more than one
row, is put in an epic, if FR-005 is called undecided, or if the reply asks the user a question about
any of them, such as which priority or release one should have.
"""),
        },
    },
    "orders-by-priority": {
        "ver": "04", "files": SHARED,
        "prompt": "Write the epics for PRD-001: one epic per priority level (Must, Should and Could), with NFR-001 only\n"
                  "in the Must epic.\nProceed without questions.\n",
        "description": "VER-04: one epic per priority; EPIC-001 is must (FR-002, FR-012, NFR-001), EPIC-002 should (FR-003), EPIC-003 could (FR-004).",
        "graders": {
            "epic-001-must": regex(E1, "contains", r"^priority: must[ \t]*$", "m"),
            "epic-001-refines": has_refines(E1, "FR-002", "FR-012", "NFR-001"),
            "epic-001-only-must": lacks_refines(E1, "FR-003", "FR-004", *INELIGIBLE),
            "epic-002-should": regex(E2, "contains", r"^priority: should[ \t]*$", "m"),
            "epic-002-refines": has_refines(E2, "FR-003"),
            "epic-002-only-fr-003": lacks_refines(E2, "FR-002", "FR-004", "FR-012", "NFR-001", *INELIGIBLE),
            "epic-003-could": regex(E3, "contains", r"^priority: could[ \t]*$", "m"),
            "epic-003-refines": has_refines(E3, "FR-004"),
            "epic-003-only-fr-004": lacks_refines(E3, "FR-002", "FR-003", "FR-012", "NFR-001", *INELIGIBLE),
            "no-epic-004": exists("docs/specs/epic/EPIC-004.md", False),
        },
    },
    "no-arch-hands-back": {
        "ver": "05", "files": shared(arch=None, pol=None), "prompt": PROMPT_ONE,
        "description": "VER-05: the shared PRD and ADRs with no ARCH; no epic is written and the reply tells the user to run /devforgeai:architecture PRD-001 first.",
        "graders": {
            "skill-fired": FIRED,
            "no-epic-written": NO_WRITE,
            "names-architecture-command": regex("last_message", "contains", r"/devforgeai:architecture`? `?PRD-001\b"),
            "says-readiness-from-arch": llm("""\
The workspace held PRD-001 and three ADRs, but no architecture description (ARCH) citing PRD-001.
The epic skill must write no epic, because which requirements are ready for epic work is computed
from the ARCH.

Judge only the final reply.
PASS if it says, in any wording, that no ARCH exists for PRD-001 and that epics (or which
requirements are ready for them) depend on it, and tells the user to run /devforgeai:architecture
PRD-001 first.
FAIL if it treats the missing ARCH as meaning nothing blocks, proposes or writes epics, or gives no
reason for handing back to the architecture step.
"""),
        },
    },
    "stale-arch-stops": {
        "ver": "06", "files": shared(arch=ARCH_STALE), "prompt": PROMPT_ONE,
        "description": "VER-06: ARCH-001 cites PRD-001 version 1 while the PRD is at version 2; no epic is written, and the reply names both versions and tells the user to review the architecture with /devforgeai:architecture PRD-001.",
        "graders": {
            "no-epic-written": NO_WRITE,
            "names-architecture-command": regex("last_message", "contains", r"/devforgeai:architecture`? `?PRD-001\b"),
            "names-both-versions": llm("""\
The workspace held PRD-001 at version 2 and ARCH-001, whose frontmatter link to PRD-001 is at version 1:
the architecture was last reviewed against PRD-001 version 1. The epic skill must stop without
writing an epic.

Judge only the final reply.
PASS if it says the architecture (ARCH-001) was defined or reviewed against PRD-001 version 1 while
PRD-001 is now at version 2, and tells the user to review the architecture against the current PRD
version, without writing or proposing epics as if the architecture were current.
FAIL if either version is missing or attributed to the wrong document, if it says the ARCH must be
rewritten or amended before anything else (a review that confirms reuse is enough), or if it says it
wrote an epic.
"""),
        },
    },
    "existing-epic-not-duplicated": {
        "ver": "07", "files": shared(epic=EPIC_COVERING),
        "prompt": "Write the epics for PRD-001: put every eligible requirement into one epic, and NFR-001 applies to\nit.\n"
                  "Proceed without questions.\n",
        "description": "VER-07: an approved EPIC-001 refines FR-002, FR-008 and part of NFR-001; it stays unchanged, the new EPIC-002 refines FR-003, FR-004, FR-012 and NFR-001 but not FR-002, and the reply reports FR-002 covered and FR-008 covered and now blocked by DEC-03.",
        "graders": {
            "epic-001-unchanged": UNCHANGED_E1,
            "epic-002-refines": has_refines(E2, "FR-003", "FR-004", "FR-012", "NFR-001"),
            "epic-002-not-covered": lacks_refines(E2, "FR-002", *INELIGIBLE),
            "fr-002-covered": row("FR-002", r"\bcovered\b", r"EPIC-001"),
            "fr-008-covered-and-blocked": row("FR-008", r"\bcovered\b", r"EPIC-001", r"\bDEC-03\b"),
            "nfr-001-not-covered": llm("""\
The workspace held PRD-001 and an existing, approved EPIC-001 that refines FR-002, FR-008 and part of
NFR-001. By the skill's rule, an FR that an existing epic refines is "covered" and gets no new epic,
but an NFR is never covered: an eligible NFR is attached to every new epic it constrains. The user
asked for one new epic covering everything eligible, with NFR-001 applying to it.

Judge only the final reply.
PASS if the reply reports FR-002 as covered by EPIC-001 and does not report NFR-001 as covered or
left out; NFR-001 is presented as part of the new epic.
FAIL if NFR-001 is listed as covered, already refined, or left out, or if the reply says EPIC-001
was changed.
"""),
        },
    },
    "draft-inputs": {
        "ver": "08", "files": shared(prd=PRD_DRAFT), "prompt": PROMPT_ONE,
        "description": "VER-08: PRD-001 is a draft; EPIC-001 and the reply say the epics are proposals because the PRD is a draft.",
        "graders": {
            "epic-001-exists": exists(E1, True),
            "epic-says-proposal": regex(E1, "contains", r"proposal[^\n]{0,200}\bdraft\b|\bdraft\b[^\n]{0,200}proposal", "i"),
            "reply-says-proposal": regex("last_message", "contains",
                                         r"proposal[^\n]{0,200}\bdraft\b|\bdraft\b[^\n]{0,200}proposal", "i"),
        },
    },
    "unconfirmed-grouping": {
        "ver": "09", "files": SHARED, "prompt": "Write the epics for PRD-001.\nProceed without questions.\n",
        "description": "VER-09: no grouping given and no one to confirm; EPIC-001 is written as a draft with a NEEDS CLARIFICATION marker in section 8 saying the grouping is unconfirmed.",
        "graders": {
            "epic-001-exists": exists(E1, True),
            "status-draft": regex(E1, "contains", r"^status: draft[ \t]*$", "m"),
            "grouping-marker-in-section-8": regex(E1, "contains",
                                                  r"## 8\. Open questions\n(?:(?!## )[^\n]*\n)*?[^\n]*\[NEEDS CLARIFICATION:"
                                                  r"[^\]\n]*grouping[^\]\n]*(?:not confirmed|unconfirmed)[^\]\n]*\]"),
        },
    },
    "hands-off-to-story": {
        "ver": "10", "files": SHARED, "prompt": PROMPT_ONE,
        "description": "VER-10: the reply ends with a Next step paragraph naming the story step with EPIC-001 as its input, by ID, and no story is written.",
        "graders": {
            "ends-with-next-step": regex("last_message", "contains", ENDS_WITH_NEXT_STEP),
            "next-step-names-story-command": regex("last_message", "contains", r"Next step[\s\S]*/devforgeai:story"),
            "next-step-names-epic-001": regex("last_message", "contains", r"Next step[\s\S]*\bEPIC-001\b"),
            "no-path-argument": regex("last_message", "not_contains", r"/devforgeai:story[ \t]+`?[^\s`]*(?:/|\.md)"),
            "no-story-written": exists("docs/specs/story/**", False),
            "handoff-quality": llm("""\
Look at the final paragraph of the reply, the one that starts with "Next step".
PASS if it names the story step as next, with EPIC-001 as its input by ID: either telling the user to
run /devforgeai:story with EPIC-001, or saying stories are written by hand from the story template for
now and that the story skill (planned as /devforgeai:story) runs with EPIC-001 once it is built.
FAIL if it passes a file path instead of the ID, names a different next step, if anything follows
that paragraph, or if the reply says it wrote or started writing a story.
"""),
        },
    },
    "ignores-unrelated-request": {
        "ver": "11", "files": SHARED, "negative": True,
        "prompt": "Write an epic poem about the sea, in six stanzas.\n",
        "description": "VER-11: a request for an epic poem must not trigger the skill or write an epic.",
        "graders": {
            "skill-not-fired": NOT_FIRED,
            "no-epic-written": NO_WRITE,
        },
    },
    "records-provenance": {
        "ver": "12", "files": SHARED, "prompt": PROMPT_ONE,
        "description": "VER-12: EPIC-001 records generated_by, an empty reviewed_by, null hashes, status draft, no approval, target_release 'Spring launch' and an informed_by link to ARCH-001.",
        "graders": {
            "epic-001-exists": exists(E1, True),
            "generated-by-filled": regex(E1, "contains",
                                         r'^generated_by:\n^  tool: "claude-code"\n^  model: "[^"\n]+"\n^  session: "[^"\n]+"\n', "m"),
            "session-substituted": regex(E1, "contains",
                                         r'^  session: "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"', "m"),
            "reviewed-by-empty": regex(E1, "contains", r"^reviewed_by: \[\][ \t]*$", "m"),
            "hashes-null": regex(E1, "not_contains", r"hash: (?!null\b)"),
            "status-draft": regex(E1, "contains", r"^status: draft[ \t]*$", "m"),
            "not-approved": regex(E1, "contains", r'^approved_by: ""\n^approved_on: null[ \t]*$', "m"),
            "target-release": regex(E1, "contains", r'^target_release: "Spring launch"[ \t]*$', "m"),
            "informed-by-arch": regex(E1, "contains", r"\{id: ARCH-001, relation: informed_by, version: 1, hash: null\}"),
            "changelog-names-session": regex(E1, "contains",
                                             r"## Change Log[\s\S]*\| claude-code \(session [0-9a-f]{8}-[0-9a-f-]{27}\) \|"),
        },
    },
    "rerun-writes-nothing": {
        "ver": "14", "files": shared(epic=EPIC_FIRST_RUN), "prompt": PROMPT_ONE,
        "description": "VER-14: EPIC-001 already refines everything eligible, as a first run would have written; no EPIC-002 is written, EPIC-001 is unchanged, and the reply says no requirement needs a new epic, gives NFR-001 an 'already refined by EPIC-001' row and doesn't call NFR-001 covered.",
        "graders": {
            "no-epic-002": exists("docs/specs/epic/EPIC-002.md", False),
            "epic-001-unchanged": UNCHANGED_E1,
            "says-nothing-to-write": regex("last_message", "contains",
                                           r"\bno new epics?\b|\bno (?:\w+ ){0,2}requirements? (?:\w+ ){0,2}needs? (?:a )?new epic",
                                           "i"),
            "nfr-001-already-refined": row("NFR-001", r"already refined", r"EPIC-001"),
            "nfr-001-not-covered": regex("last_message", "not_contains", r"\bNFR-001\b[^\n]{0,40}\bcovered\b", "i"),
        },
    },
    "policy-resolver-revoked": {
        "ver": "15", "files": shared(pol=POL_REVOKED), "prompt": PROMPT_ONE,
        "description": "VER-15: POL-001's SET-01 is deprecated, so FR-012 is unknown: EPIC-001 doesn't refine it, and the reply names POL-001#SET-01 and the failed check.",
        "graders": {
            "epic-001-exists": exists(E1, True),
            "no-fr-012": lacks_refines(E1, "FR-012"),
            "fr-012-unknown": row("FR-012", r"\bunknown\b", r"POL-001#SET-01", r"(?:deprecated|not active|inactive)"),
        },
    },
    "epic-two-policy-layers": {
        "ver": "16", "files": shared(arch=ARCH_TWO_LAYERS, pol2=POL_PROJECT), "prompt": PROMPT_ONE,
        "description": "VER-16: an organization policy (POL-001, transactional email) and a project policy (POL-002, volunteer sign-in) each mandate a platform; both resolvers count, so EPIC-001 also refines FR-001 (DEC-01 resolved by POL-002#SET-01) and FR-012, and the reply reports neither as unknown.",
        "graders": {
            "skill-fired": FIRED,
            "epic-001-exists": exists(E1, True),
            "refines-fr-001-and-fr-012": has_refines(E1, "FR-001", "FR-012"),
            "refines-the-rest": has_refines(E1, "FR-002", "FR-003", "FR-004", "NFR-001"),
            "refines-nothing-else": lacks_refines(E1, *[i for i in INELIGIBLE if i != "FR-001"]),
            "policy-resolvers-count": llm("""\
The workspace held two approved policies: the regional network's organization policy POL-001, whose
SET-01 mandates a mail relay for "transactional email", and the food bank's project policy POL-002,
whose SET-01 mandates a council sign-in service for "volunteer sign-in". They mandate platforms for
different capabilities, so they don't conflict. In ARCH-001, DEC-01 (which identity provider handles
volunteer sign-in, and the question PRD-001's NEEDS ADR marker for FR-001 asks) is resolved by
POL-002#SET-01, and DEC-07 (the email service) by POL-001#SET-01. So FR-001 and FR-012 are ready and
eligible.

Judge only the final reply.
PASS if neither FR-001 nor FR-012 is reported as unknown, blocked or left out, and the reply presents
both as included in the epic.
FAIL if either one is called unknown or blocked, is listed among the left-out requirements, or if the
reply says the two policies conflict or that a second policy setting the same key disqualifies either.
"""),
        },
    },
    "epic-policy-bump-unchanged": {
        "ver": "17", "files": shared(pol=POL_V2), "prompt": PROMPT_ONE,
        "description": "VER-17: POL-001 is at version 2 (a testing setting added) while ARCH-001 links SET-01 at version 1; SET-01 is unchanged and ARCH-001's resolution line holds it, so EPIC-001 refines FR-012 and the reply notes the newer policy version.",
        "graders": {
            "skill-fired": FIRED,
            "epic-001-exists": exists(E1, True),
            "refines-fr-012": has_refines(E1, "FR-012"),
            "refines-the-rest": has_refines(E1, "FR-002", "FR-003", "FR-004", "NFR-001"),
            "refines-nothing-else": lacks_refines(E1, *INELIGIBLE),
            "notes-newer-policy": llm("""\
The workspace held POL-001 at version 2: version 2 only added a testing setting (SET-02) and left
SET-01, the mandated mail relay for transactional email, exactly as it was. ARCH-001 still links
POL-001#SET-01 at version 1, and its latest policy resolution line records that same mail relay for
transactional email. So the resolver of DEC-07 still counts, and FR-012 is ready and eligible.

Judge only the final reply.
PASS if both hold:
- FR-012 is not reported as unknown, blocked or left out; it is presented as included in the epic.
- The reply notes, in any wording, that POL-001 is newer (version 2) than the version ARCH-001
  linked or applied (version 1), for example as a note that the setting still counts or is
  unchanged.
FAIL if FR-012 is called unknown or blocked or is left out, or if the reply never mentions that
POL-001 is at a newer version than ARCH-001's link.
"""),
        },
    },
    "epic-second-prd-same-number": {
        "ver": "18", "files": shared(arch=ARCH_TWO_PRDS, prd2=PRD2), "prompt": PROMPT_ONE,
        "description": "VER-18: ARCH-001 v2 also covers PRD-002, and its open DEC-08 cites only PRD-002#FR-003; PRD-001's FR-003 stays eligible, EPIC-001 refines it and links ARCH-001 at version 2, and the reply doesn't report FR-003 blocked by DEC-08.",
        "graders": {
            "skill-fired": FIRED,
            "epic-001-exists": exists(E1, True),
            "refines-eligible": has_refines(E1, *ELIGIBLE),
            "refines-nothing-else": lacks_refines(E1, *INELIGIBLE),
            "no-prd-002-links": regex(E1, "not_contains", r"\{id: PRD-002\b"),
            "informed-by-arch-v2": regex(E1, "contains", r"\{id: ARCH-001, relation: informed_by, version: 2, hash: null\}"),
            "fr-003-not-blocked": llm("""\
The workspace held PRD-001 and PRD-002, two PRDs for the same system, and ARCH-001 version 2, which
covers both. ARCH-001's open question DEC-08 cites only PRD-002's FR-003 (a monthly report export).
PRD-001 also has an FR-003 (the coordinator's daily roster), which no open question cites. A
question blocks only the requirements of the PRD its links name, so PRD-001's FR-003 is ready and
eligible.

Judge only the final reply, which is about PRD-001.
PASS if PRD-001's FR-003 is presented as included in the epic and is not reported as blocked by
DEC-08, blocked at all, or left out.
FAIL if the reply says FR-003 is blocked by DEC-08 (or by any open question), leaves it out, or puts
PRD-002's requirements in the epic.
"""),
        },
    },
    "epic-nothing-eligible": {
        "ver": "19", "files": shared(arch=ARCH_HOSTING_OPEN), "prompt": PROMPT_ONE,
        "description": "VER-19: an open hosting question (DEC-08) blocks every requirement that would otherwise be eligible; no epic is written, the reply says nothing is eligible yet (not that no requirement needs a new epic), and the next step is /devforgeai:architecture PRD-001, with no story step.",
        "graders": {
            "skill-fired": FIRED,
            "no-epic-written": NO_WRITE,
            "no-needs-claim": regex("last_message", "not_contains",
                                    r"\bno (?:\w+ ){0,2}requirements? (?:\w+ ){0,2}needs? (?:a )?new epic"
                                    r"|\bnone (?:of them )?needs? (?:a )?new epic", "i"),
            "ends-with-next-step": regex("last_message", "contains", ENDS_WITH_NEXT_STEP),
            "next-step-architecture": regex("last_message", "contains",
                                            r"Next step[\s\S]*/devforgeai:architecture`? `?PRD-001\b"),
            "no-story-step": regex("last_message", "not_contains", r"/devforgeai:story"),
            "says-not-eligible-yet": llm("""\
The workspace held PRD-001 and ARCH-001. ARCH-001 has an open question, DEC-08 (which hosting
provider runs the web app and the shift service), that cites FR-002, FR-003, FR-004, FR-012 and
NFR-001: every requirement that would otherwise be eligible for an epic. Every other requirement is
left out for its own reason. So no requirement is eligible for an epic yet, and no epic exists.

Judge only the final reply.
PASS if all of these hold:
- It says no epic was written because no requirement is eligible (or ready) for an epic yet, and
  names the open question DEC-08 as what blocks FR-002, FR-003, FR-004, FR-012 and NFR-001.
- It doesn't say that no requirement needs a new epic, or that everything is already covered.
- Its next step is to resolve the architecture question with /devforgeai:architecture PRD-001; it
  names no story step.
FAIL if any of these is missing, if it writes or proposes an epic, or if it tells the user to write
stories or run /devforgeai:story.
"""),
        },
    },
}


def main():
    for label, (text, schema, *expect) in FIXTURES.items():
        validate(label, text, schema, *expect)
    check_shared_fixture()
    for name, case in CASES.items():
        d = ROOT / name
        (d / "graders").mkdir(parents=True, exist_ok=True)
        tags = f"[epic, ver-{case['ver']}" + (", negative-trigger]" if case.get("negative") else "]")
        turns, timeout = ("15", "300") if case.get("negative") else ("60", "1200")
        (d / "prompt.md").write_text(
            f"---\ndescription: \"{case['description']}\"\ntags: {tags}\nmax_turns: {turns}\n"
            f"timeout_seconds: {timeout}\nallowed_tools: {TOOLS}\n---\n{case['prompt']}")
        (d / "case.yaml").write_text(f"schema_version: \"1.1\"\nname: {name}\ncontext:\n  scaffold_script: scaffold.sh\n")
        (d / "scaffold.sh").write_text(scaffold(f"Seeds the fixtures for SPEC-004 VER-{case['ver']} ({name}).", case["files"]))
        os.chmod(d / "scaffold.sh", 0o755)
        for g, body in case["graders"].items():
            (d / "graders" / f"{g}.md").write_text(body)
    print("validated", len(FIXTURES), "fixtures; wrote", len(CASES), "cases")


if __name__ == "__main__":
    main()
