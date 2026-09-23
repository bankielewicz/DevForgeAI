---
id: SPEC-003
type: spec
title: "Architecture Definition skill (MVP)"
status: draft
version: 1
created: 2026-09-23
updated: 2026-09-23
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a2b1015f-3340-4c70-80ed-b674d486fadd"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: STORY-003, relation: specifies, version: 1, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 7, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 7, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 7, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: the Architecture Definition step"}
  - {id: ADR-003, relation: constrains, version: 2, hash: null, note: "accepted: configuration contract v1"}
  - {id: SPEC-002, relation: informed_by, version: 9, hash: null, note: "consumes the prd skill's downstream contract (SPEC-002 §5)"}
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
│   ├── arch.md                  # THE ARCH template (moved from src/staging/templates/)
│   └── adr.md                   # THE ADR template (moved from src/staging/templates/)
└── references/
    ├── readiness.md             # question identification and the decision-specific readiness rule
    ├── inspection.md            # bounded read-only inspection and evidence classification
    ├── defaults.md              # framework-default layer for the v1 settings (copied from the prd skill)
    ├── policy.md                # ADR-003 resolution contract (copied from the prd skill)
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

Keeping two copies of `policy.md` and `defaults.md`, one in each skill, is the ADR-003 consequence:
every skill resolves policy until `devforgeai check` exists. The architecture skill's copies must stay
byte-identical to the prd skill's, which the SPEC-003 VER-12 manual check confirms.

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
| `components` (`CMP-NN`) | Boundaries: responsibility, data owned, interactions, deployment unit; upstream links to the quality drivers and constraints |
| `decisions` (`DEC-NN`) | Architectural questions: `question`, `blocking`, `state` (open or resolved), `resolved_by` (ADR or POL setting IDs); upstream links to every affected requirement at the PRD version examined |
| `evidence` (`EVD-NN`) | Every source consulted, with `classification`: observed, policy or decided |
| §7 | Requirement changes proposed to the PRD owner |

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
  devforgeai-version: "1"
```

- **The name must be exactly `architecture`.** The prd skill's handoff looks for `${CLAUDE_PLUGIN_ROOT}/skills/architecture/SKILL.md`.
- **Tools:**
  - Read, Glob and Grep, read-only and within the inspection scope for code;
  - Write and Edit for the ARCH and ADRs;
  - AskUserQuestion, with at most 4 questions per call.
- **Downstream contract (consumed by the epic workflow):**
  - the ARCH path and stable CMP, DEC and EVD IDs;
  - epics may be written only for requirements that the readiness rule reports ready;
  - epics cite components with `refines` or `informed_by` links, for example `{id: ARCH-001, item: CMP-02, relation: informed_by}`;
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
    rule: "Resolve policy exactly as the prd skill does (ADR-003 A3–A5, references/policy.md): the R1–R5 sequence, the SV rules, local preferences, the resolution line, and stopping on invalid policy."
  - id: BEH-04
    status: active
    rule: "Select the architecture description. Read docs/specs/arch/ARCH-*.md. If one covers the same system, propose reusing it (no change) or amending it (new questions or components), with reasons, and ask. Create a new ARCH, the next free ARCH-NNN.md, only when none covers the system or the user chooses to. Never create a second baseline automatically. Ask when several could apply."
  - id: BEH-05
    status: active
    rule: "Inspect only the components or directories the user names (inspection_scope), read-only, with Glob, Grep and Read. References such as imports and configuration may be followed only within that scope; ask before going outside it. Record every source consulted as an EVD item, classified as observed (what the code does), policy (an approved setting) or decided (an accepted ADR). When evidence is insufficient, say so explicitly with a [NEEDS CLARIFICATION] marker, and never recommend reuse on assumption."
  - id: BEH-06
    status: active
    rule: "Identify the architectural questions that separate epics must share: component boundaries and responsibilities, data ownership, major interactions and interfaces, deployment, and how quality requirements are met. Every [NEEDS ADR] marker in the PRD becomes a DEC. Each DEC cites every affected requirement in its upstream links and is blocking unless the user says otherwise. Leave feature-level detail to specs."
  - id: BEH-07
    status: active
    rule: "Resolve each question only by one of three means. (1) An approved, active mandated-platform setting that answers exactly this question: resolved_by POL-NNN#SET-NN, applied as policy, not a user decision. (2) An existing accepted, non-superseded ADR that the user confirms answers exactly this question. (3) The user's explicit decision among the options presented with trade-offs, which is written as a new ADR with status accepted and approved_by the user. Anything else stays open. A deferred decision may be written as a proposed ADR that resolves nothing. An ADR or setting resolves only the question it answers, never every question that cites the same requirement."
  - id: BEH-08
    status: active
    rule: "Propose the outcome with reasons: reuse (the existing ARCH covers the PRD unchanged), amend (the existing ARCH needs new or changed questions or components) or create (no ARCH covers the system). Reusing one platform or component is not a reuse outcome. Write outcome only when the user confirms it, and keep it null otherwise. Confirming the outcome accepts no decision."
  - id: BEH-09
    status: active
    rule: "Write or amend the ARCH. A new ARCH starts as draft. Amending bumps the version, continues item numbering, keeps existing items unchanged except for DEC state and resolved_by transitions (each logged in the Change Log), and returns an approved ARCH to in-review."
  - id: BEH-10
    status: active
    rule: "Describe the components that separate epics must share, as CMP items with a Mermaid overview. Link each to the quality drivers (NFR items) and constraints it serves, and to the POL setting when a mandated platform applies (relation constrains)."
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
    rule: "Validate the ARCH and every ADR written. If devforgeai is on PATH, use devforgeai check --json; otherwise check against references/output-rules.md. Repeat until clean, at most three attempts."
  - id: BEH-15
    status: active
    rule: "Hand off with the ARCH path, the outcome (or that it is unconfirmed), the ADRs written with their status, the requirements ready for epic work, the requirements blocked with their DEC IDs, the proposed PRD changes, and the policy resolution line. Then name the next step: if ${CLAUDE_PLUGIN_ROOT}/skills/epic/SKILL.md exists, tell the user to run /devforgeai:epic with the PRD ID; otherwise say the epic workflow is not built yet. Never start it."
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
    condition: "Policy is invalid, contradictory or disallowed (ADR-003 A4)"
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
    condition: "Validation still fails after three fix attempts"
    handling: "Stop, leave statuses as they were before this write, and list the remaining errors"
    user_result: "The file paths and the unresolved errors"
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
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 7, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted"
    measured_by: "Reading against skill-frontmatter.schema.json and skill.schema.json"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 7, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged architecture and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 7, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: `arch.schema.json`, the ARCH template, the negative schema tests, and cross-document links | **Completed** on 2026-09-23 |
| Behavioural: every VER below | **Planned.** Nothing has run until STORY-003 is built |

**Shared fixture:** one policy-neutral PRD (`PRD-001`) in which FR-001, "users sign in", is affected by two
architectural questions (a `[NEEDS ADR]` marker for the identity provider, and NFR-001 requiring session
revocation), with no identity ADR. It's written fresh and checked against `prd.schema.json`. Unless a case says
otherwise, the prompt says to proceed without questions, so evals exercise the no-user path.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture, no policy, no ARCH: writes docs/specs/arch/ARCH-001.md with a DEC for the identity provider and a DEC for session revocation, both open and citing PRD-001#FR-001; outcome null; the handoff lists FR-001 as blocked. Eval case creates-arch: regex on the file and last_message."
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
      - {id: STORY-003, item: AC-01, relation: verifies, version: 1, hash: null}
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
      - {id: STORY-003, item: AC-07, relation: verifies, version: 1, hash: null}
  - id: VER-03
    status: active
    obligation: "Demonstration, Organization B: identical to VER-02 except for Organization B's policy. The identity-provider DEC stays open with an empty resolved_by. Eval case org-b-policy: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 1, hash: null}
  - id: VER-04
    status: active
    obligation: "Unrelated ADR: the fixture adds an accepted ADR-001 about logging that cites PRD-001#FR-001. Both identity DECs stay open, nothing is resolved_by ADR-001, and FR-001 is blocked. Eval case unrelated-adr: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 1, hash: null}
  - id: VER-05
    status: active
    obligation: "Superseded ADR: an existing ARCH-001 has the provider DEC resolved_by ADR-002, which is superseded by ADR-003 (a different topic). The handoff reports the provider DEC open and FR-001 blocked, naming the superseded ADR. Eval case superseded-adr: regex on last_message."
    level: e2e
    covers:
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 1, hash: null}
  - id: VER-06
    status: active
    obligation: "No user, no acceptance: in VER-01's run, no ADR in docs/specs/adr/ has status accepted, no DEC is resolved_by an ADR, and outcome is null. Eval case no-acceptance-without-user: regex not_contains on the written files."
    level: e2e
    covers:
      - BEH-07
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 1, hash: null}
  - id: VER-07
    status: active
    obligation: "Existing ARCH-001 for the same system: the skill proposes reuse or amend and asks; no ARCH-002.md is created. Eval case existing-arch-not-duplicated: file_exists false, regex on last_message."
    level: e2e
    covers:
      - BEH-04
      - ERR-04
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 1, hash: null}
  - id: VER-08
    status: active
    obligation: "Insufficient evidence: the prompt says 'reuse our current auth service' but names no inspection scope, and no code exists. The outcome is not reuse, and the file has a [NEEDS CLARIFICATION] marker about the missing evidence. Eval case insufficient-evidence: regex on the file."
    level: e2e
    covers:
      - BEH-05
    upstream:
      - {id: STORY-003, item: AC-05, relation: verifies, version: 1, hash: null}
  - id: VER-09
    status: active
    obligation: "Requirement handback: the fixture PRD has an NFR that conflicts with Organization A's mandated platform. ARCH §7 and the handoff propose a change for the PRD owner; PRD-001.md still has its original version line. Eval case prd-change-handed-back: regex on the ARCH and the PRD."
    level: e2e
    covers:
      - BEH-12
      - BEH-16
    upstream:
      - {id: STORY-003, item: AC-08, relation: verifies, version: 1, hash: null}
  - id: VER-10
    status: active
    obligation: "Handoff: the final reply lists ready and blocked requirements with DEC IDs, names the epic workflow and, since this plugin has no epic skill, says it is not built yet. Eval case hands-off-to-epic: regex on last_message."
    level: e2e
    covers:
      - BEH-15
    upstream:
      - {id: STORY-003, item: AC-09, relation: verifies, version: 1, hash: null}
  - id: VER-11
    status: active
    obligation: "A request such as 'explain the architecture of the Linux kernel' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
    upstream:
      - {id: STORY-003, item: AC-10, relation: verifies, version: 1, hash: null}
  - id: VER-12
    status: active
    obligation: "Manual, interactive: (a) each decision is presented with trade-offs and becomes an accepted ADR only after an explicit answer; confirming the outcome accepts nothing else. (b) Bounded inspection of a real directory records EVD items with their classification and asks before leaving the scope. (c) A draft PRD shows the proposal warning. (d) Stopping mid-session offers a draft save. (e) An invalid policy stops the skill with the rule named. (f) The architecture skill's references/policy.md and defaults.md are byte-identical to the prd skill's. (g) An unknown PRD ID lists the available PRDs. (h) SKILL.md is within the NFR-001 limits."
    level: manual
    covers:
      - BEH-01
      - BEH-05
      - BEH-13
      - ERR-01
      - ERR-02
      - ERR-03
      - ERR-05
      - ERR-06
      - QR-01
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 1, hash: null}
  - id: VER-13
    status: active
    obligation: "Operator check for the demonstration: run VER-02 and VER-03 with the same PRD, prompt and other fixtures, in fresh workspaces. A SHA-256 manifest of the deployed plugin (find .claude/skills/devforgeai -path '*/evals/results' -prune -o -type f -print0 | sort -z | xargs -0 sha256sum) is identical before VER-02, between the runs and after VER-03, and git diff src/ is empty. Record the three manifest hashes in the PR."
    level: manual
    covers:
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 1, hash: null}
  - id: VER-14
    status: active
    obligation: "Provenance and policy recording: in VER-01's run, the ARCH's generated_by has non-empty tool, model and session, reviewed_by is empty, every hash is null, and the Change Log carries 'Policy resolution:' with 'no approved policy'. Eval case records-provenance: regex on the file."
    level: e2e
    covers:
      - BEH-13
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-11, relation: verifies, version: 1, hash: null}
      - {id: STORY-003, item: AC-06, relation: verifies, version: 1, hash: null}
```

## 10. Rollout, migration and rollback

The skill and the ARCH type are new; removing the skill directory rolls it back. The schema change is
additive: the `ARCH` document prefix and the `CMP`, `DEC` and `EVD` item prefixes.

## 11. Implementation plan

1. Create a worktree for STORY-003 per ADR-001 v4, using the hardened deploy snippet.
2. `git mv src/staging/templates/arch.md` and `src/staging/templates/adr.md` into `skills/architecture/assets/`, and update the templates README rows.
3. Copy `references/policy.md` and `references/defaults.md` from the prd skill unchanged, then write `readiness.md`, `inspection.md` and `output-rules.md`.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-003 implementing SPEC-003.
5. Write the shared fixture PRD and the other fixtures, checking each against its schema, then the eval cases for VER-01 to VER-11 and VER-14.
6. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Run VER-02 and VER-03 with the VER-13 operator check, and do VER-12 by hand.

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

- [NEEDS CLARIFICATION: PRD-001#FR-013 priority and release are null for Bryan to decide]

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft | all |
