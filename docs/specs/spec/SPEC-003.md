---
id: SPEC-003
type: spec
title: "Architecture Definition skill (MVP)"
status: approved
version: 3
created: 2026-09-23
updated: 2026-09-29
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a2b1015f-3340-4c70-80ed-b674d486fadd"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-09-29
upstream:
  - {id: STORY-003, relation: specifies, version: 3, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 10, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: the Architecture Definition step"}
  - {id: ADR-003, relation: constrains, version: 2, hash: null, note: "accepted: configuration contract v1"}
  - {id: SPEC-002, relation: informed_by, version: 2, hash: null, note: "consumes the prd skill's downstream contract (SPEC-002 §5)"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/architecture", "src/schemas/arch.schema.json"]
---

# SPEC-003 — Architecture Definition skill (MVP)

## 1. Overview

The `architecture` skill ships in the `devforgeai` plugin and is invoked as
`/devforgeai:architecture PRD-NNN`. It performs the Architecture Definition step (ADR-002):
- it identifies the architectural questions that separate epics must share;
- it settles each one only by an explicit decision, an accepted ADR or approved policy;
- it records the result in an architecture description, `docs/specs/arch/ARCH-NNN.md`, plus ADRs;
- it reports exactly which requirements are ready for epic work.

Three rules shape everything else:
- **Readiness is decision-specific.** A requirement is ready only when every blocking question that
  cites it is resolved. An ADR or policy setting resolves the question it answers, never "the requirement".
- **Decisions are accepted one by one.** Confirming the overall outcome (reuse, amend or create) is
  not accepting the decisions inside it.
- **Evidence is honest.** Inspection is bounded and recorded. Observed practice isn't policy, and
  insufficient evidence is stated as unknown.

The skill is recorded as `SKL-003` in its `provenance.yaml`.

## 2. Constraints

- **NFR-001 to NFR-003:** as for the prd skill.
- **ADR-001 v4:** built in a worktree and deployed with the hardened snippet; evals run from a plain terminal.
- **ADR-002:** the step's position and its reuse, amend and create outcomes.
- **ADR-003:** policy resolution R1–R5, the SV rules, the resolution line, and evidence classification (observed practice vs approved policy).
- **SPEC-002 §5 (consumed):**
  - PRD paths and stable IDs;
  - `release` and `priority` semantics, where `null` is undecided;
  - `[NEEDS ADR]` markers;
  - `status: draft` until the user approves.
- **Out of scope:** experts, exhaustive code indexing, detailed feature design (API fields, migrations, class structures), and the epic skill.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/architecture/
├── SKILL.md                     # workflow checklist, decision rules, output contract
├── provenance.yaml              # SKL-003, implements SPEC-003
├── assets/
│   ├── arch.md                  # THE ARCH template (moved from src/templates/)
│   └── adr.md                   # THE ADR template (moved from src/templates/)
├── scripts/
│   └── validate_policy.py       # policy validation against the schemas and SV rules (copied from the prd skill)
└── references/
    ├── readiness.md             # question identification and the decision-specific readiness rule
    ├── inspection.md            # bounded read-only inspection and evidence classification
    ├── defaults.md              # framework-default layer for the v1 settings (copied from the prd skill)
    ├── policy.md                # ADR-003 resolution contract (copied from the prd skill)
    ├── schemas/                 # policy.schema.json and common.schema.json, unchanged copies of src/schemas/
    └── output-rules.md          # ARCH and ADR item-block rules
src/claude/DevForgeAI/evals/architecture/<case>/   # one case per automated VER item (§9)
```

```mermaid
flowchart LR
    I[Select PRD BEH-01] --> R[Read PRD BEH-02]
    R --> P[Resolve policy BEH-03]
    P --> S[Select or create ARCH BEH-04]
    S --> X[Bounded inspection BEH-05]
    X --> Q[Identify questions BEH-06]
    Q --> D[Resolve explicitly BEH-07]
    D --> O[Confirm outcome BEH-08]
    O --> W[Write ARCH and ADRs BEH-09 BEH-10 BEH-13]
    W --> V[Validate BEH-14]
    V --> H[Readiness and handoff BEH-11 BEH-15]
```

Keeping two copies of `policy.md`, `defaults.md`, `scripts/validate_policy.py` and the schema copies, one
set in each skill, is the ADR-003 consequence: every skill resolves policy until `devforgeai check` exists
(PRD-001 FR-018), and SPEC-002 §5 makes the script the one maintained validation path. The architecture
skill's copies must stay byte-identical to the prd skill's, and the schema copies to `src/schemas/`, which
VER-12 (f) confirms.

## 4. Data model

**Input:** a PRD at `docs/specs/prd/PRD-NNN.md`, read-only. **Also read:**
- approved policy in `docs/specs/policy/`;
- ADRs in `docs/specs/adr/`;
- existing ARCH documents in `docs/specs/arch/`;
- sources within the inspection scope.

**Output:** `docs/specs/arch/ARCH-NNN.md`, valid against `arch.schema.json`, and new ADRs at
`docs/specs/adr/ADR-NNN.md`, valid against `adr.schema.json`.

| ARCH part | Holds |
|---|---|
| Frontmatter `outcome` | `reuse`, `amend`, `create` or `null`. Written only when the user confirms it |
| Frontmatter `system`, `inspection_scope` | What the description covers; the components or directories the user named |
| `components` (`CMP-NN`) | Boundaries: responsibility, kinds (below), data owned, interactions, deployment unit; upstream links to the quality drivers and constraints |
| `decisions` (`DEC-NN`) | Architectural questions: `question`, `blocking`, `state` (open or resolved), `resolved_by` (ADR or POL setting IDs); upstream links to every affected requirement at the PRD version examined |
| `evidence` (`EVD-NN`) | Every project source consulted for architecture analysis, with its `kind` and, independently, a `classification`: observed, policy, decided or context |
| §7 | Requirement changes proposed to the PRD owner |

**Component kinds.** Each CMP records its `kinds`: one or more of the values below. A component may have
several, such as a service that also exposes an API (`service` and `api`). The kinds select the project
context documents (ADR-004 D2).

| Kind | A component that is… |
|---|---|
| `user-interface` | a surface people use: web, desktop, mobile or CLI |
| `service` | application or business logic |
| `platform` | background jobs, workers, integrations with external systems, hosting |
| `api` | an interface exposed to another component or to external consumers |
| `relational-store` | a relational database |
| `data-store` | a non-relational store: document, key-value, object, search or cache |
| `external` | a system outside the project, such as a mandated identity platform |

A component written before this version has no `kinds`. Amending an ARCH leaves existing components
unchanged, so consumers ask about a missing kind (SPEC-009 ERR-08).

**Evidence classification** (`references/inspection.md`). Framework instructions and templates are not
project evidence. Each EVD records the document version and status examined where applicable, and its
`classification` is independent of its `kind`:
- `observed`: findings from code or configuration directly inspected within `inspection_scope`;
- `policy`: an approved, active, applicable policy setting;
- `decided`: an accepted, non-superseded ADR;
- `context`: any other consulted input or historical material, such as the input PRD (`kind: prd`), an
  existing ARCH (`kind: document`), a proposed, rejected or superseded ADR, or a documentation claim not
  corroborated by the implementation.

`context` establishes neither implemented behavior nor an accepted decision; the PRD remains the
requirements authority through its links. No classification resolves a DEC by itself (BEH-07). Ignored
policy is reported in the resolution line and gets no policy link.

**The readiness rule** (`references/readiness.md`). A requirement R is **ready** for epic work
when, for every active `DEC` with `blocking: true` whose upstream cites R:
- `state` is `resolved`, and
- every `resolved_by` entry is either an ADR with `status: accepted` and no `superseded_by`, or
  an approved policy's active setting.

Otherwise R is **blocked**, and the report names the DEC IDs. A superseded ADR returns its
questions to open, until an accepted successor resolves them.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: architecture
description: Performs DevForgeAI Architecture Definition for a PRD. It identifies the architectural questions separate epics must share, settles each only by an explicit decision, an accepted ADR or approved policy, and writes an architecture description (ARCH) with ADRs and a report of which requirements are ready for epic work. Use after a PRD is written, when deciding system architecture, components, data ownership or deployment, or when resolving NEEDS ADR markers.
argument-hint: "PRD-NNN"
metadata:
  devforgeai-id: "SKL-003"
  devforgeai-version: "<SKL-003's provenance.yaml version, quoted>"
```

- **The name must be exactly `architecture`.** The prd skill's handoff looks for `${CLAUDE_PLUGIN_ROOT}/skills/architecture/SKILL.md`.
- **The version isn't fixed here.** `metadata.devforgeai-version` must equal `provenance.yaml`'s `version`,
  so a skill fix bumps the skill, not this spec.
- **Tools:**
  - code inspection: read-only, and every path read, listed or searched is inside the inspection scope. Read, Glob and Grep when available, otherwise read-only shell commands (ls, find, grep, cat, head) with explicit paths inside the scope; never a whole-repository listing or search. The project documents read by contract (docs/specs/prd/, arch/, adr/, policy/ and .claude/devforgeai.local.md) are outside this rule, and validating the documents written (BEH-14) is separate from inspection;
  - Write and Edit for the ARCH and ADRs;
  - Bash only to run `python3` with the shared policy validation script (SPEC-002 §5);
  - AskUserQuestion, with at most 4 questions per call.
- **Downstream contract (consumed by the epic workflow, and by the context and story steps):**
  - the ARCH path and stable CMP, DEC and EVD IDs;
  - epics may be written only for requirements that the readiness rule reports ready;
  - an epic carries one versioned, document-level `informed_by` link to its ARCH (SPEC-004 §5) and
    never cites CMP items; stories record the specific components they touch (SPEC-009);
  - each CMP's `kinds`, which select the project context documents (ADR-004 D2);
  - the readiness report in the handoff is advisory; the rule in §4 is the contract.

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Take the PRD from $ARGUMENTS (PRD-NNN). With no argument, list the PRDs in docs/specs/prd/ with their titles and status, and ask. Never take a file path."
  - id: BEH-02
    status: active
    rule: "Read the PRD's requirements, constraints, stage, operating context and [NEEDS ADR] markers, and record its version in every link. If the PRD is a draft, warn that the result is a proposal. Never turn an unanswered product question (a null priority, a release or a [NEEDS CLARIFICATION] marker) into an architectural decision. Never edit the PRD."
  - id: BEH-03
    status: active
    rule: "Resolve policy exactly as the prd skill does (ADR-003 A3–A5, references/policy.md): the R1–R5 sequence, the SV rules, local preferences, the resolution line, and stopping on invalid policy. Approved policy documents are validated in full through the shared validation script, as SPEC-002 §5 and BEH-17 R1 specify; when the script can't run while approved policy exists, stop (ERR-02)."
  - id: BEH-04
    status: active
    rule: "Select the architecture description. Read docs/specs/arch/ARCH-*.md. If one covers the same system, propose reusing it (no change) or amending it (new questions or components), with reasons, and ask. Create a new ARCH, the next free ARCH-NNN.md, only when none covers the system or the user chooses to. Never create a second baseline automatically. Ask when several could apply."
  - id: BEH-05
    status: active
    rule: "Inspect only the components or directories the user names (inspection_scope). Code inspection is read-only, and every path it reads, lists or searches is inside inspection_scope: use Read, Glob and Grep when available, otherwise read-only shell commands (ls, find, grep, cat, head) with explicit paths inside the scope, with no redirection, no writes and no running or building project code; never list or search the whole repository. The project documents read by contract (docs/specs/prd/, arch/, adr/ and policy/, and .claude/devforgeai.local.md) are outside this rule, and validating the documents written (BEH-14) is separate from inspection. References such as imports and configuration may be followed only within that scope; ask before going outside it. Record every project source consulted for architecture analysis as an EVD item, with the version and status examined where applicable, classified independently of its kind as observed (code or configuration directly inspected within inspection_scope), policy (an approved, active, applicable setting), decided (an accepted, non-superseded ADR) or context (any other consulted input or historical material, including the input PRD, existing ARCHs, proposed, rejected or superseded ADRs, and documentation claims not corroborated by the implementation). Context establishes neither implemented behavior nor an accepted decision, and no classification resolves a DEC by itself. When evidence is insufficient, say so explicitly with a [NEEDS CLARIFICATION] marker, and never recommend reuse on assumption."
  - id: BEH-06
    status: active
    rule: "Identify the architectural questions that separate epics must share: component boundaries and responsibilities, data ownership, major interactions and interfaces, deployment, and how quality requirements are met. Every [NEEDS ADR] marker in the PRD becomes a DEC. Each DEC cites every affected requirement in its upstream links and is blocking unless the user says otherwise. Leave feature-level detail to specs."
  - id: BEH-07
    status: active
    rule: "Resolve each question only by one of three means. (1) An approved, active mandated-platform setting that answers exactly this question: resolved_by POL-NNN#SET-NN, applied as policy, not a user decision. (2) An existing accepted, non-superseded ADR that the user confirms answers exactly this question. (3) The user's explicit decision among the options presented with trade-offs, which is written as a new ADR with status accepted and approved_by the user. Anything else stays open. A deferred decision may be written as a proposed ADR that resolves nothing. An ADR or setting resolves only the question it answers, never every question that cites the same requirement."
  - id: BEH-08
    status: active
    rule: "Propose the outcome with reasons: reuse (the existing ARCH covers the PRD unchanged), amend (the existing ARCH needs new or changed questions or components) or create (no ARCH covers the system). Reusing one platform or component is not a reuse outcome. Write outcome only when the user confirms it, and keep it null otherwise. Confirming the outcome accepts no decision. When the user confirms reuse and the ARCH's frontmatter PRD link is older than the PRD's version, record the review (BEH-09); when that link already equals the PRD's version, confirming reuse writes nothing."
  - id: BEH-09
    status: active
    rule: "Write or amend the ARCH. A new ARCH starts as draft. Amending bumps the version, continues item numbering, keeps existing items unchanged except for DEC state and resolved_by transitions (each logged in the Change Log), and returns an approved ARCH to in-review. A review record, written when the user confirms reuse against a newer PRD version, makes exactly three changes: the frontmatter PRD link moves to the reviewed version, outcome becomes reuse, and one Change Log row is added, 'Reviewed against PRD-NNN vN: reuse confirmed, no architectural change', ending with the policy resolution line. Everything else stays byte-identical, including version, updated, status, the approval fields and every item with its links, which still show as suspect. It is a relink, not an amendment, so an approved ARCH stays approved. With no user, nothing is confirmed and nothing is written."
  - id: BEH-10
    status: active
    rule: "Describe the components that separate epics must share, as CMP items with a Mermaid overview. Link each to the quality drivers (NFR items) and constraints it serves, and to the POL setting when a mandated platform applies (relation constrains). Give each CMP its kinds (§4): one or more of user-interface, service, platform, api, relational-store, data-store and external. When a kind is uncertain, ask. With no user present, record only the kinds the PRD or the evidence states; when none is certain, leave kinds out and add [NEEDS CLARIFICATION: kinds of CMP-NN] to the open questions. When amending, existing components stay unchanged, with or without kinds."
  - id: BEH-11
    status: active
    rule: "Compute readiness with the §4 rule for every requirement cited by any DEC. Check each ADR's current status and superseded_by at the time of writing; a question whose resolving ADR has been superseded is reported open."
  - id: BEH-12
    status: active
    rule: "When architecture shows a requirement is infeasible, too costly or conflicting, write the proposed change in ARCH §7 and in the handoff, addressed to the PRD owner. Never edit the PRD. A manual PRD amendment, approved by its owner, is how it changes in v1."
  - id: BEH-13
    status: active
    rule: "Fill provenance on the ARCH and every ADR written: generated_by with the tool, model and session; authors; reviewed_by empty; every hash null; today's dates. Write ADRs from ${CLAUDE_SKILL_DIR}/assets/adr.md and the ARCH from ${CLAUDE_SKILL_DIR}/assets/arch.md, deleting author comments."
  - id: BEH-14
    status: active
    rule: "Validate the ARCH and every ADR written against the self-check list in references/output-rules.md, reading each file back. Run one initial check, then at most three repair-and-readback cycles, so at most four checks. A repair changes a file to address a reported error; when an error can't be repaired, stop early and report it instead of repeating an unchanged check. Record each check and repair in the reply. Never run a devforgeai command: the CLI doesn't exist and a program by that name on PATH can't be trusted (SPEC-004 §2)."
  - id: BEH-15
    status: active
    rule: "Hand off with the ARCH path, the outcome (or that it is unconfirmed), the ADRs written with their status, the requirements ready for epic work, the requirements blocked with their DEC IDs, the proposed PRD changes, and the policy resolution line. Then name the next step: if ${CLAUDE_PLUGIN_ROOT}/skills/epic/SKILL.md exists, tell the user to run /devforgeai:epic with the PRD ID; otherwise say the epic workflow (planned as /devforgeai:epic) is not built yet and that, once it is, /devforgeai:epic with the PRD ID runs for the ready requirements. The next step comes last in the final reply, as its own paragraph outside any code block, starting with the words Next step; nothing follows it. Never start it."
  - id: BEH-16
    status: active
    rule: "Never modify a PRD, BRN or policy document, and never modify an existing ADR other than to record a supersession the user explicitly approved."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The PRD ID given does not exist"
    handling: "List the available PRD IDs and write nothing"
    user_result: "The list of PRDs"
  - id: ERR-02
    status: active
    condition: "Policy is invalid (including any schema error the shared validation script reports), contradictory or disallowed (ADR-003 A4), or the script can't run while approved policy exists"
    handling: "Stop before writing anything, naming the file, the setting and the rule"
    user_result: "The policy error; no ARCH or ADR written"
  - id: ERR-03
    status: active
    condition: "Inspection would need to go outside the named scope"
    handling: "Ask before reading outside it; if not allowed, record the gap as an explicit unknown"
    user_result: "A scope question, or an unknown recorded"
  - id: ERR-04
    status: active
    condition: "Several existing ARCH documents could cover the system"
    handling: "List them with their systems and ask; never pick one silently"
    user_result: "A choice of ARCH"
  - id: ERR-05
    status: active
    condition: "Validation still fails after the initial check and three repair cycles, or an error can't be repaired"
    handling: "Stop. Keep the user's architectural choices and unrelated content, and never leave approved or accepted on content that failed validation. A new ARCH stays draft. An amended ARCH keeps the status BEH-09 gave it, so an approved ARCH whose content changed stays in-review with approved_by and approved_on cleared; a review record that fails validation is treated the same way. A new ADR the user accepted becomes proposed with empty approval fields and is kept, and the DEC state and resolved_by that depended on it return to open. Add one matching audit record (Change Log row, and Status history row for an ADR). End with a validation-failure report listing the checks, the repairs and the unresolved errors; skip the readiness handoff and never present readiness as validated"
    user_result: "A validation-failure report: the file paths, the checks and repairs made, the unresolved errors and the statuses left; no readiness presented as validated"
  - id: ERR-06
    status: active
    condition: "The user stops mid-session"
    handling: "Offer to save a draft ARCH with every unanswered question open and the outcome null"
    user_result: "Either a draft file or no file, as the user chose"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the decision and readiness rules and the output contract; readiness, inspection, policy and output rules live in references/"
    measured_by: "SKILL.md line count and description length"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 10, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version"
    measured_by: "Reading against skill-frontmatter.schema.json and skill.schema.json, and comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 10, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged architecture and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 10, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Version 3 | Not run. Changed: BEH-03, BEH-14, ERR-02, ERR-05, VER-12 (f) and (i); new: VER-17 and VER-18. The rows below record versions 1 and 2 |
| Structural: schemas, templates, fixtures and cross-document links | Fixtures: `src/tests/architecture/make_evals.py` validates all 15 against `src/schemas/` before it writes the cases. Schemas, templates and cross-document links: not run |
| Behavioural: automated VER items, one eval case each | Built as SKL-003 v1 and merged in PR #4; deployed. 14 eval cases (VER-01..11, 14, 15, 16). `claude plugin eval`, 3 runs with the no-plugin baseline, 2026-09-28, plugin 0.3.0: 14 of 14 at 1.00 in every run, mean Δ +0.67. That run checked VER-10's not-built branch; PR #5 switched `hands-off-to-epic` to the shipped branch, which scored 1.00 in 1 run with the baseline |
| Behavioural: manual VER items (VER-12, VER-13) | Not run |
| Demonstration vs ADR-003 | ADR-003's demonstration plan (its Organization A and B pass criteria) is refined by VER-02 and VER-03, not met literally. Under Organization A the identity-provider question resolves by `POL-001#SET-01` while session revocation stays open, with no reuse outcome (`outcome: null`). Under Organization B the identity-provider question is an open DEC, not a `[NEEDS ADR]` marker. ADR-003 is unchanged |

**Shared fixture:** one policy-neutral PRD (`PRD-001`) in which FR-001, "users sign in", is affected by two
architectural questions (a `[NEEDS ADR]` marker for the identity provider, and NFR-001 requiring session
revocation), with no identity ADR. It's written fresh and checked against `prd.schema.json`. Unless a case says
otherwise, the prompt says to proceed without questions, so evals exercise the no-user path.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture, no policy, no ARCH: writes docs/specs/arch/ARCH-001.md with a DEC for the identity provider and a DEC for session revocation, both open and citing PRD-001#FR-001; an EVD with kind prd and classification context records the PRD; outcome null; the handoff lists FR-001 as blocked; at least one CMP carries kinds from the §4 list, or its kinds are marked [NEEDS CLARIFICATION]. Eval case creates-arch: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-02
      - BEH-04
      - BEH-06
      - BEH-09
      - BEH-10
      - BEH-14
      - BEH-15
    upstream:
      - {id: STORY-003, item: AC-01, relation: verifies, version: 3, hash: null}
  - id: VER-02
    status: active
    obligation: "Demonstration, Organization A: the shared fixture plus Organization A's policy (src/staging/examples/policy-two-orgs/org-a/POL-001.md). The identity-provider DEC is resolved_by POL-001#SET-01; the session-revocation DEC stays open; FR-001 is still blocked; outcome is null (not reuse). Eval case org-a-policy: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-03
      - BEH-07
      - BEH-08
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 3, hash: null}
  - id: VER-03
    status: active
    obligation: "Demonstration, Organization B: identical to VER-02 except for Organization B's policy. The identity-provider DEC stays open with an empty resolved_by. Eval case org-b-policy: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 3, hash: null}
  - id: VER-04
    status: active
    obligation: "Unrelated ADR: the fixture adds an accepted ADR-001 about logging that cites PRD-001#FR-001. Both identity DECs stay open, nothing is resolved_by ADR-001, and FR-001 is blocked. Eval case unrelated-adr: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 3, hash: null}
  - id: VER-05
    status: active
    obligation: "Superseded ADR: an existing ARCH-001 has the provider DEC resolved_by ADR-002, which is superseded by ADR-003 (a different topic). The prompt chooses to amend ARCH-001 and confirms that outcome. The handoff names ADR-002 as the superseded resolver (equivalent wording such as 'replaced' is accepted; negated or reversed statements are not) and reports readiness derived from the amended ARCH: FR-001 blocked by DEC-01; FR-002 and NFR-001 ready, because DEC-02 stays resolved by the accepted ADR-001, unless the amendment adds a DEC (DEC-03 or higher) that cites them. Every requirement is listed, no summary contradicts the lists, and no requirement is attributed to a DEC that doesn't cite it. In the amended ARCH-001 the provider DEC is open with an empty resolved_by, DEC-02 is still resolved by ADR-001, and an EVD records ADR-002 with classification context. Eval case superseded-adr: regex on the file and last_message, plus an llm grader for the readiness mapping."
    level: e2e
    covers:
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 3, hash: null}
  - id: VER-06
    status: active
    obligation: "No user, no acceptance: in VER-01's run, no ADR in docs/specs/adr/ has status accepted, no DEC is resolved_by an ADR, and outcome is null. Eval case no-acceptance-without-user: regex not_contains on the written files."
    level: e2e
    covers:
      - BEH-07
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 3, hash: null}
  - id: VER-07
    status: active
    obligation: "Existing ARCH-001 for the same system: the skill proposes reuse or amend and asks; no ARCH-002.md is created. Eval case existing-arch-not-duplicated: file_exists false, regex on last_message."
    level: e2e
    covers:
      - BEH-04
      - ERR-04
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-08
    status: active
    obligation: "Insufficient evidence: the prompt says 'reuse our current auth service' but names no inspection scope, and no code exists. The outcome is not reuse, and the file has a [NEEDS CLARIFICATION] marker about the missing evidence. Eval case insufficient-evidence: regex on the file."
    level: e2e
    covers:
      - BEH-05
    upstream:
      - {id: STORY-003, item: AC-05, relation: verifies, version: 3, hash: null}
  - id: VER-09
    status: active
    obligation: "Requirement handback: the fixture PRD has an NFR that conflicts with Organization A's mandated platform. ARCH §7 and the handoff propose a change for the PRD owner; PRD-001.md still has its original version line. Eval case prd-change-handed-back: regex on the ARCH and the PRD."
    level: e2e
    covers:
      - BEH-12
      - BEH-16
    upstream:
      - {id: STORY-003, item: AC-08, relation: verifies, version: 3, hash: null}
  - id: VER-10
    status: active
    obligation: "Handoff: the final reply lists ready and blocked requirements with DEC IDs and hands off to the epic step (BEH-15), and no epic is written. The handoff is the last paragraph of the reply, outside any code block; it starts with the words Next step, and nothing follows it. It names the PRD by its ID, never by a file path. What it says depends on the plugin. Without an epic skill, it says the epic workflow (planned as /devforgeai:epic) is not built yet and that, once it is, /devforgeai:epic PRD-001 runs for the ready requirements. With an epic skill, it tells the user to run /devforgeai:epic PRD-001. The graders read the reply and the written files, never whether the epic skill exists. Eval case hands-off-to-epic checks the branch the plugin ships, with regex on last_message and file_exists false; the change that ships the epic skill switches the case to the other branch."
    level: e2e
    covers:
      - BEH-15
    upstream:
      - {id: STORY-003, item: AC-09, relation: verifies, version: 3, hash: null}
  - id: VER-11
    status: active
    obligation: "A request such as 'explain the architecture of the Linux kernel' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
    upstream:
      - {id: STORY-003, item: AC-10, relation: verifies, version: 3, hash: null}
  - id: VER-12
    status: active
    obligation: "Manual, interactive: (a) each decision is presented with trade-offs and becomes an accepted ADR only after an explicit answer; confirming the outcome accepts nothing else. (b) Bounded inspection of a real directory records EVD items with their kind and classification (observed, policy, decided or context) and asks before leaving the scope; every inspection command in the transcript uses only paths inside the scope or the contract document folders, and none lists or searches the whole repository. A request that needs a file outside the scope (the session lifetime in shared/config.js) is run in two fresh fixture copies: the skill asks before reading it; answered yes, it reads the file, adds it to inspection_scope and records an observed EVD; answered no, it doesn't read it and records an explicit unknown naming the path. (c) A draft PRD shows the proposal warning when the PRD is read, before any question or write, and again in the handoff. (d) Stopping mid-session offers a draft save. (e) An invalid policy stops the skill with the rule named. (f) The architecture skill's references/policy.md, defaults.md, scripts/validate_policy.py and references/schemas/ copies are byte-identical to the prd skill's, and the schema copies to src/schemas/. (g) An unknown PRD ID lists the available PRDs. (h) SKILL.md is within the NFR-001 limits. (i) ERR-05, with one decision accepted before validation: the skill stops after the initial check and at most three repair cycles, keeps the choice as a proposed ADR with empty approval fields, returns the dependent DEC to open, adds the audit record, and ends with a validation-failure report without presenting readiness as validated. (j) In a fresh fixture copy, amending an existing ARCH whose links cite PRD v2, against PRD v3 with one new [NEEDS ADR] marker: links on existing items stay at v2, the links added in this run (and the frontmatter PRD link) use v3, and validation passes without ERR-05. (k) In a fresh fixture copy, an explicitly approved supersession of an accepted ADR passes validation: the old ADR changes only status: superseded, superseded_by and one Status history row; the new ADR is accepted with supersedes: [ADR-old]; the DEC's resolved_by changes from [ADR-old] to [ADR-new], logged in the Change Log; the old ADR is recorded as a context EVD; and readiness reports the requirement ready. (l) A component whose kind is uncertain is asked about, and the answer is recorded as its kinds."
    level: manual
    covers:
      - BEH-01
      - BEH-05
      - BEH-09
      - BEH-13
      - BEH-14
      - ERR-01
      - ERR-02
      - ERR-03
      - ERR-05
      - ERR-06
      - QR-01
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 3, hash: null}
      - {id: STORY-003, item: AC-05, relation: verifies, version: 3, hash: null}
  - id: VER-13
    status: active
    obligation: "Operator check for the demonstration: run VER-02 and VER-03 with the same PRD, prompt and other fixtures, in fresh workspaces. A SHA-256 manifest of the deployed plugin (find .claude/skills/devforgeai -path '*/evals/results' -prune -o -type f -print0 | sort -z | xargs -0 sha256sum) is identical before VER-02, between the runs and after VER-03, and git diff src/ is empty. Record the three manifest hashes in the PR."
    level: manual
    covers:
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 3, hash: null}
  - id: VER-14
    status: active
    obligation: "Provenance and policy recording: in VER-01's run (no policy), the ARCH's generated_by has non-empty tool, model and session, reviewed_by is empty, every hash is null, the Change Log's 'Policy resolution:' line contains interview.max_calls=8 (default), architecture.mandated_platforms=none (default) and quality.required_categories=floor only (default), and the ARCH contains no 'id: POL-' link. Eval case records-provenance: one regex per check on the file, and a not_contains for 'id: POL-'."
    level: e2e
    covers:
      - BEH-13
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-11, relation: verifies, version: 3, hash: null}
      - {id: STORY-003, item: AC-06, relation: verifies, version: 3, hash: null}
  - id: VER-15
    status: active
    obligation: "Review record: an approved ARCH-001 cites PRD-001 version 1, and PRD-001 is at version 2 after a priority-only change. The prompt chooses to reuse ARCH-001 and confirms the reuse outcome. In ARCH-001 the frontmatter PRD link is at version 2, outcome is reuse, version, status and the approval fields are unchanged, a DEC's upstream link still cites version 1, and the Change Log has exactly one review row. Eval case reuse-records-review: regex on the file."
    level: e2e
    covers:
      - BEH-08
      - BEH-09
    upstream:
      - {id: STORY-005, item: AC-12, relation: verifies, version: 2, hash: null}
  - id: VER-16
    status: active
    obligation: "Review record, repeated: as VER-15, but ARCH-001 already cites PRD-001 version 2 and has one review row. ARCH-001 is unchanged: the same version, and still exactly one review row. Eval case reuse-review-idempotent: regex on the file."
    level: e2e
    covers:
      - BEH-08
      - BEH-09
    upstream:
      - {id: STORY-005, item: AC-12, relation: verifies, version: 2, hash: null}
  - id: VER-17
    status: active
    obligation: "Malformed policy stops Architecture Definition: the shared fixture plus an approved organization policy whose updated date is 2026-13-45. No ARCH or ADR is written, and the reply names the policy file and the field. Eval case policy-bad-date: file_exists false for docs/specs/arch/ARCH-001.md, regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-02
    upstream:
      - {id: STORY-003, item: AC-06, relation: verifies, version: 3, hash: null}
  - id: VER-18
    status: active
    obligation: "Failed amendment of an approved ARCH: an approved ARCH-001 whose existing CMP-01 has a value the self-check rejects, which an amendment must leave unchanged (BEH-09); the prompt chooses to amend ARCH-001 for a new PRD question and confirms that outcome. ARCH-001 ends in-review with approved_by and approved_on cleared, CMP-01 is byte-identical, and the reply lists the checks (at most four) and the unresolved error and presents no readiness as validated. Eval case failed-amendment-stays-in-review: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-09
      - BEH-14
      - ERR-05
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
```

## 10. Rollout, migration and rollback

The skill and the ARCH type are new; removing the skill directory rolls it back. The schema change is
additive: the `ARCH` document prefix and the `CMP`, `DEC` and `EVD` item prefixes.

## 11. Implementation plan

1. Create a worktree for STORY-003 per ADR-001 v4, using the hardened deploy snippet.
2. `git mv src/templates/arch.md` and `src/templates/adr.md` into `skills/architecture/assets/`, and update the templates README rows.
3. Copy `references/policy.md` and `references/defaults.md` from the prd skill unchanged, then write `readiness.md`, `inspection.md` and `output-rules.md`.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-003 implementing SPEC-003.
5. Write the shared fixture PRD and the other fixtures, checking each against its schema, then the eval cases for VER-01 to VER-11 and VER-14.
6. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Run VER-02 and VER-03 with the VER-13 operator check, and do VER-12 by hand.

**Version 3** (after approval): add the shared policy files (§3) to the architecture skill as SKL-003 v3,
implement BEH-14 and ERR-05 as changed, and add the eval cases for VER-17 and VER-18. The Codex
architecture skill follows the same contract. Evaluate each provider independently, with the existing
thresholds.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| ADRs only, no ARCH document | Nothing citable for component boundaries, and nowhere to track questions and readiness |
| Unblock a requirement when any accepted ADR cites it | Unblocks FR-001 once the identity provider is chosen while session revocation is still open. Readiness is per question instead (§4) |
| Require the user to name every file to inspect | Too much friction. Named components or directories, with read-only discovery inside them, instead |
| Crawl the whole codebase | Unbounded cost, and it mixes observed practice with decisions. Bounded inspection and EVD classification instead |
| Require an approved PRD first | Makes architectural exploration expensive. Drafts are allowed with a warning, and product questions are never turned into decisions |
| Let the skill amend PRD requirements | Downstream never edits upstream, and the PRD's extension mode is append-only. Proposed changes go to the PRD owner (BEH-12) |

## 13. Open questions

- None. (PRD-001 v8 records FR-013 as must/current, decided by Bryan on 2026-09-24.)

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-27 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Baseline for this workspace, reset from SPEC-003 v11 on Bryan's decision, since nothing has been built from it here. Versions 1–8 are in DevForgeAI-SDF2's git history (docs/specs/spec/SPEC-003.md, main at ef78b83); v11, with its Change Log for v9–v11, is kept at docs/archive/2026-09-27-spec-reset/SPEC-003-v11.md. Changed from v11, decided by Bryan: VER-10 checks the handoff branch that matches the plugin, with BEH-15's placement (v11 expected a shipped epic skill; added before approval, as for SPEC-002 VER-07); §5 no longer fixes the skill version (it named DevForgeAI-SDF2's SKL-003 v6), and QR-02 compares the two version values (DevForgeAI-SDF2 issue #14). Removed as DevForgeAI-SDF2 history: §9's run records (now not run; the Demonstration row is kept) and VER-12 (i)'s sentence about v9 and STORY-004. SPEC-002 link at v1. Awaiting Bryan's approval | frontmatter, §5, QR-02, §9, VER-10, VER-12 |
| 1 | 2026-09-27 | Bryan | Approved | status |
| 1 | 2026-09-28 | claude-code (session 383de882-2b59-4b3b-808b-83bb1ab93b9b) | Status update only, at Bryan's instruction, with no version bump: §9 records that the skill is built (SKL-003 v1, PR #4) and deployed, and its fixture checks and eval results. No requirement, behavior or VER item changed | §9 |
| 2 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Bryan's decisions of 2026-09-29. Components carry kinds (M4): §4 lists them and their mapping to ADR-004's context documents, BEH-10 classifies them and asks when a kind is uncertain, and VER-01 and VER-12 (l) check it. §5 aligned with SPEC-004 and the shipped epic skill (M8): an epic has one document-level informed_by link to its ARCH and never cites CMP items; stories record the components they touch (SPEC-009). PRD-001 links re-reviewed at v10. Awaiting Bryan's approval | §4, §5, BEH-10, VER-01, VER-12, frontmatter, status |
| 2 | 2026-09-29 | Bryan | Approved | status |
| 3 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Aligned with SPEC-002 v2 (Bryan, 2026-09-29). ERR-05 follows D-03's rule: content that failed validation is never left approved or accepted; an approved ARCH whose amendment or review record fails stays in-review with approval cleared, and a newly accepted ADR becomes proposed. BEH-14 and ERR-05 count one initial check plus at most three repair cycles (D-04). BEH-03, ERR-02, §3 and §5: policy is validated in full through the shared script (D-09), and VER-12 (f) covers its byte-identity. New VER-17 (malformed policy) and VER-18 (failed amendment). SPEC-002 link at v2. Awaiting Bryan's approval | §3, §5, BEH-03, BEH-14, ERR-02, ERR-05, VER-12, VER-17, VER-18, §9, §11, frontmatter, status |
| 3 | 2026-09-29 | Bryan | Approved | status |
