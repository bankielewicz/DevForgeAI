---
id: SPEC-004
type: spec
title: "Epic skill (MVP)"
status: draft
version: 1
created: 2026-09-24
updated: 2026-09-24
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
  - {id: STORY-005, relation: specifies, version: 1, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 9, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 9, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 9, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: epics come after the Architecture Definition step"}
  - {id: SPEC-003, relation: informed_by, version: 6, hash: null, note: "consumes the readiness rule (§4) and the downstream contract (§5)"}
  - {id: SPEC-002, relation: informed_by, version: 10, hash: null, note: "priority and release semantics, where null is undecided (§5)"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/epic"]
---

# SPEC-004 — Epic skill (MVP)

## 1. Overview

The `epic` skill ships in the `devforgeai` plugin and is invoked as `/devforgeai:epic PRD-NNN`. It
performs the epic step, after Architecture Definition (ADR-002):
- it selects the PRD's requirements that are ready for epic work and in the current release;
- it proposes how to group them into epics, and writes them once the user confirms;
- it reports every requirement it left out, with the reason;
- it hands off to the story step.

Three rules shape everything else:
- **The ARCH file is the readiness contract.** Readiness is computed from the architecture
  description and the ADRs' current status (SPEC-003 §4), never from any skill's reply.
- **Release selects, priority orders.** `release: current` decides what gets an epic. MoSCoW priority
  orders the epics (Must, then Should, then Could) and never selects or excludes on its own, except
  `wont`. A `null` priority or release is undecided and goes back to the PRD owner.
- **The skill adds, it never rewrites.** It writes new epics only. Existing epics, the PRD, the ARCH and
  ADRs are read-only.

The skill is recorded as `SKL-004` in its `provenance.yaml`.

## 2. Constraints

- **NFR-001 to NFR-003:** as for the other skills.
- **ADR-001 v4:** built in a worktree and deployed with the hardened snippet; evals run from a plain terminal.
- **ADR-002:** the epic step follows the Architecture Definition step.
- **SPEC-003 §4 and §5 (consumed):** the ARCH path, stable DEC IDs, the decision-specific readiness rule,
  and "epics may be written only for requirements that the readiness rule reports ready".
- **SPEC-002 §5 (consumed):** PRD paths and stable IDs; `priority` (MoSCoW) and `release` (current or
  later) are independent, and `null` is undecided; `[NEEDS ADR]` markers; the PRD's `target_release`.
- **Out of scope:**
  - writing stories, sprint planning, and modifying existing epics;
  - organizational policy: PRD-001 FR-006 to FR-008 cover only prd and Architecture Definition, and
    FR-012 (release later) covers the rest, so this skill copies neither `policy.md` nor `defaults.md`;
  - the `devforgeai check` CLI branch. The CLI doesn't exist, and anything named `devforgeai` on PATH
    can't be trusted by name. The skill validates with its own self-check list.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/epic/
├── SKILL.md                     # workflow checklist, selection and grouping rules, output contract
├── provenance.yaml              # SKL-004, implements SPEC-004
├── assets/
│   └── epic.md                  # THE epic template (moved from src/staging/templates/)
└── references/
    ├── selection.md             # the ARCH lookup, the readiness rule and the selection rule (§4)
    └── output-rules.md          # epic frontmatter, links, done-when items and the self-check list
src/claude/DevForgeAI/evals/epic/<case>/   # one case per automated VER item (§9)
```

```mermaid
flowchart LR
    I[Select PRD BEH-01] --> R[Read PRD BEH-02]
    R --> A[Find the current ARCH BEH-03]
    A --> Y[Compute readiness BEH-04]
    Y --> S[Select requirements BEH-05 BEH-06]
    S --> G[Propose and confirm grouping BEH-07]
    G --> W[Write epics BEH-08 BEH-09]
    W --> V[Validate BEH-10]
    V --> H[Report and hand off BEH-11]
```

## 4. Data model

**Input:** a PRD at `docs/specs/prd/PRD-NNN.md`. **Also read:**
- ARCH documents in `docs/specs/arch/`;
- ADRs in `docs/specs/adr/`;
- existing epics in `docs/specs/epic/`.

All of these are read-only. **Output:** new epics at `docs/specs/epic/EPIC-NNN.md`, valid against
`epic.schema.json`.

**The current ARCH.** The skill uses the ARCH whose frontmatter `upstream` links cite this PRD. It is
**current** when that link's `version` equals the PRD's `version`. No such ARCH, or an ARCH that examined
an older PRD version, means the skill writes nothing and hands back to the architecture step
(ERR-02, ERR-03).

**Readiness** (`references/selection.md`), exactly SPEC-003 §4, applied to the ARCH file. A requirement R
is **ready** when, for every active `DEC` with `blocking: true` whose `upstream` cites R:
- `state` is `resolved`, and
- every `resolved_by` entry is an ADR whose file now has `status: accepted` and no `superseded_by`, or an
  approved policy's active setting.

A DEC blocks only the requirements its own `upstream` cites. A PRD `[NEEDS ADR]` marker that names R, with
no DEC citing R, blocks R ("marker without a question").

**The selection rule.** A requirement R of the PRD (an FR or an NFR) is **eligible** when all hold:
1. R is `status: active`;
2. R is ready;
3. `release: current`;
4. `priority` is `must`, `should` or `could`;
5. no existing epic that is active (not `superseded` or `deprecated`) has a `refines` link to this PRD's R
   (the PRD ID and the item both match), at any version.

Every other requirement is **left out**, with the first reason that applies:

| Reason | When |
|---|---|
| `deprecated` | R is not active |
| `blocked` | R is not ready; the report names the blocking DEC IDs, and any superseded resolver |
| `later` | `release: later` |
| `wont` | `priority: wont` |
| `undecided` | `priority` or `release` is `null`; reported to the PRD owner |
| `covered` | an active existing epic refines this PRD's R; the report names the epic |

**Grouping.** Each eligible FR is refined by exactly one new epic. An eligible NFR is refined by every
new epic whose capability it constrains, with `note: "partial: <which part>"` when shared. An epic's
`priority` is the highest priority among the **FRs** it refines; a shared NFR never raises it (an epic that
refines only NFRs takes the NFRs' highest priority). New epics are numbered, and
listed, Must first, then Should, then Could.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: epic
description: Turns a DevForgeAI PRD into epic documents for the requirements that are ready for epic work and in the current release. It reads readiness from the architecture description (ARCH), proposes how to group the requirements into epics, writes them once the user confirms, and reports every requirement left out and why. Use after Architecture Definition, when splitting a PRD into epics or planning delivery.
argument-hint: "PRD-NNN"
metadata:
  devforgeai-id: "SKL-004"
  devforgeai-version: "<SKL-004's provenance.yaml version, quoted>"
```

- **The name must be exactly `epic`.** The architecture skill's handoff looks for `${CLAUDE_PLUGIN_ROOT}/skills/epic/SKILL.md`.
- **The version isn't fixed here.** `metadata.devforgeai-version` must equal `provenance.yaml`'s `version`,
  so a skill fix bumps the skill, not this spec.
- **Tools:** Read and Glob (or read-only `ls` and `cat` on `docs/specs/` when Glob isn't available); Write
  for new epics, and Edit only on epics written in this run (BEH-10's fix loop); AskUserQuestion, with at most
  4 questions per call. No code inspection, and no shell
  command other than read-only listing and reading of `docs/specs/`.
- **Downstream contract (consumed by the story step):**
  - the epic path and stable `DW-NN` IDs; stories cite them with `satisfies` links;
  - each epic's `refines` links name the requirements its stories must satisfy;
  - each epic links the ARCH it relied on (`informed_by`, at the ARCH's version), so an ARCH change makes
    the epic's link suspect;
  - epics start as `draft`; only the user approves them.

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Take the PRD from $ARGUMENTS (PRD-NNN). With no argument, list the PRDs in docs/specs/prd/ with their titles and status, and ask. Never take a file path."
  - id: BEH-02
    status: active
    rule: "Read the PRD's requirements (FR and NFR items with status, priority and release), its target_release, its status and its [NEEDS ADR] markers, and record its version in every link. If the PRD or the ARCH is a draft, say in the handoff and in each epic written that the epics are proposals because an input is a draft. Never edit the PRD."
  - id: BEH-03
    status: active
    rule: "Find the ARCH whose frontmatter upstream links cite this PRD, and check that its PRD link version equals the PRD's version (§4). Use it only then; otherwise stop as ERR-02, ERR-03 or ERR-04."
  - id: BEH-04
    status: active
    rule: "Compute readiness for every active FR and NFR of the PRD from the ARCH file and the ADR files, exactly as SPEC-003 §4, reading each resolving ADR's current status and superseded_by now. A DEC blocks only the requirements its own upstream cites. A [NEEDS ADR] marker naming a requirement that no DEC cites blocks it. Never use a skill's reply as the source."
  - id: BEH-05
    status: active
    rule: "Apply the selection rule (§4): a requirement is eligible only when it is active, ready, release current, priority must, should or could, and not already refined by an active existing epic (§4). Give every other requirement its reason: deprecated, blocked (with the DEC IDs and any superseded resolver), later, wont, undecided (for the PRD owner) or covered (with the epic ID)."
  - id: BEH-06
    status: active
    rule: "Read every existing epic in docs/specs/epic/. A requirement of this PRD that an active existing epic (not superseded or deprecated) refines, at any version and matching both the PRD ID and the item, is covered. Never modify, renumber or duplicate an existing epic."
  - id: BEH-07
    status: active
    rule: "Propose how to group the eligible requirements into epics: each a deliverable capability, each eligible FR in exactly one epic, a shared NFR in every epic it constrains. Show each proposed epic's title, requirements and priority, and ask the user to confirm or change the grouping; write nothing until they do. A grouping stated in the request counts as confirmed. If no one can confirm (the request says to proceed without questions and gives no grouping), write the proposal and add to §8 of each epic: [NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]."
  - id: BEH-08
    status: active
    rule: "Write each confirmed epic to the next free docs/specs/epic/EPIC-NNN.md from ${CLAUDE_SKILL_DIR}/assets/epic.md, numbered Must first, then Should, then Could. Frontmatter: status draft; priority the highest among the FRs it refines (a shared NFR never raises it; an NFR-only epic takes its NFRs' highest priority); target_release the PRD's target_release; upstream a refines link to every requirement it groups at the PRD version (partial note for a shared NFR) and an informed_by link to the ARCH at its version. Fill the goal, value and scope, at least one DW item with a criterion and an evidence method, and the dependencies. Keep the story map as a GENERATED placeholder."
  - id: BEH-09
    status: active
    rule: "Fill provenance on every epic written: generated_by with the tool, model and session; authors; reviewed_by empty; every hash null; today's dates; approved_by empty. Delete every template author comment."
  - id: BEH-10
    status: active
    rule: "Validate every epic written against the self-check list in references/output-rules.md, reading each file back. Fix and check again, at most three attempts. Don't call any devforgeai command."
  - id: BEH-11
    status: active
    rule: "Hand off with each epic written (path, title, priority and the requirements it refines), every requirement left out grouped by reason (blocked with DEC IDs, later, wont, undecided for the PRD owner, covered with the epic ID, deprecated), and the proposal warning if an input is a draft. Then name the next step, the story step, with the new epic IDs as its input: if ${CLAUDE_PLUGIN_ROOT}/skills/story/SKILL.md exists, tell the user to run /devforgeai:story with an epic ID; otherwise say stories are written by hand from the story template for now. Never write a story."
  - id: BEH-12
    status: active
    rule: "Never modify a PRD, BRN, ARCH, ADR, policy document or existing epic."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The PRD ID given does not exist"
    handling: "List the available PRD IDs with titles and status, and write nothing"
    user_result: "The list of PRDs"
  - id: ERR-02
    status: active
    condition: "No ARCH cites the PRD"
    handling: "Write nothing. Say that readiness comes from the architecture description, and tell the user to run /devforgeai:architecture with the PRD ID first"
    user_result: "A handback to the architecture step; no epic written"
  - id: ERR-03
    status: active
    condition: "The ARCH that cites the PRD examined an older PRD version"
    handling: "Write nothing. Name both versions and tell the user to amend the ARCH with /devforgeai:architecture and the PRD ID"
    user_result: "A handback to amend the ARCH; no epic written"
  - id: ERR-04
    status: active
    condition: "Several ARCH documents cite the PRD"
    handling: "List them with their systems and PRD link versions, and ask; never pick one silently"
    user_result: "A choice of ARCH"
  - id: ERR-05
    status: active
    condition: "No requirement is eligible"
    handling: "Write nothing, and report every requirement with its reason"
    user_result: "The left-out report; no epic written"
  - id: ERR-06
    status: active
    condition: "Validation still fails after three fix attempts"
    handling: "Stop. Keep the epics written as draft, and report the file paths and the unresolved errors. Don't present the epics as ready for the story step"
    user_result: "A validation-failure report"
  - id: ERR-07
    status: active
    condition: "The user stops before confirming the grouping"
    handling: "Write nothing, and say how to resume: run the skill again with the PRD ID"
    user_result: "No epic written"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the selection and grouping rules and the output contract; the ARCH lookup, readiness and output rules live in references/"
    measured_by: "SKILL.md line count and description length"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 9, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version"
    measured_by: "Reading against skill-frontmatter.schema.json and skill.schema.json, and comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 9, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged epic and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 9, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: SPEC-004's chain (PRD-001 v9, EPIC-005, STORY-005), schemas and cross-document links | **Completed** on 2026-09-24 |
| Behavioural: every VER below | **Planned.** Nothing has run until STORY-005 is built |

**Shared fixture.** One approved PRD, `PRD-001` v2 with `target_release: "Spring launch"`, and one
approved `ARCH-001` whose frontmatter cites PRD-001 v2. Each is written fresh and checked against its
schema. The ADRs are `ADR-001` (accepted), `ADR-002` (superseded by `ADR-003`) and `ADR-003` (accepted,
a different topic).

| Requirement | Priority / release | ARCH | Expected |
|---|---|---|---|
| FR-001 | must / current | DEC-01 open, cites only FR-001; a PRD `[NEEDS ADR]` marker names FR-001 | left out: blocked by DEC-01 |
| FR-002 | must / current | DEC-02 resolved by ADR-001, cites FR-002 and NFR-001 | eligible |
| FR-003 | should / current | no DEC | eligible |
| FR-004 | could / current | no DEC | eligible |
| FR-005 | must / later | no DEC | left out: later |
| FR-006 | wont / current | no DEC | left out: wont |
| FR-007 | null / current | no DEC | left out: undecided |
| FR-008 | must / current | DEC-03 resolved by ADR-002, superseded | left out: blocked by DEC-03 |
| FR-009 | must / current | no DEC; a PRD `[NEEDS ADR]` marker names FR-009 | left out: blocked (marker without a question) |
| NFR-001 | must / current | DEC-02 | eligible |

So the eligible set is FR-002, FR-003, FR-004 and NFR-001. FR-001 shows that DEC-01 blocks only what it
cites (FR-002 stays eligible), FR-008 shows that a superseded resolver blocks again, and FR-009 shows that
a `[NEEDS ADR]` marker with no question still blocks. File graders
check the written epics, not the reply, because a wrong epic is worse than a wrong sentence. Unless a
case says otherwise, the prompt states the grouping, so the run is non-interactive and confirmed.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture; the prompt asks for one epic covering everything eligible. docs/specs/epic/EPIC-001.md refines FR-002, FR-003, FR-004 and NFR-001 at PRD-001 version 2, and contains no refines link to FR-001, FR-005, FR-006, FR-007, FR-008 or FR-009. Eval case selects-ready-current: regex on the file."
    level: e2e
    covers:
      - BEH-02
      - BEH-03
      - BEH-04
      - BEH-05
      - BEH-08
      - BEH-10
    upstream:
      - {id: STORY-005, item: AC-01, relation: verifies, version: 1, hash: null}
  - id: VER-02
    status: active
    obligation: "In VER-01's setup, no epic refines FR-001, FR-008 or FR-009, and the reply reports FR-001 blocked by DEC-01, FR-008 blocked by DEC-03 (naming ADR-002 as superseded) and FR-009 blocked by a [NEEDS ADR] marker with no question; FR-002 is not reported blocked. Eval case blocked-not-included: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 1, hash: null}
  - id: VER-03
    status: active
    obligation: "In VER-01's setup, the reply reports FR-005 as later, FR-006 as won't have, and FR-007 as undecided for the PRD owner. Eval case reports-left-out: regex on last_message."
    level: e2e
    covers:
      - BEH-05
      - BEH-11
    upstream:
      - {id: STORY-005, item: AC-03, relation: verifies, version: 1, hash: null}
  - id: VER-04
    status: active
    obligation: "Shared fixture; the prompt asks for one epic per priority level, with NFR-001 only in the Must epic. EPIC-001.md has priority must and refines FR-002 and NFR-001; EPIC-002.md has priority should and refines FR-003; EPIC-003.md has priority could and refines FR-004. Eval case orders-by-priority: regex on the three files."
    level: e2e
    covers:
      - BEH-07
      - BEH-08
    upstream:
      - {id: STORY-005, item: AC-06, relation: verifies, version: 1, hash: null}
  - id: VER-05
    status: active
    obligation: "The shared PRD and ADRs with no ARCH: no docs/specs/epic/EPIC-001.md is written, and the reply tells the user to run /devforgeai:architecture PRD-001 first. Eval case no-arch-hands-back: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-02
    upstream:
      - {id: STORY-005, item: AC-04, relation: verifies, version: 1, hash: null}
  - id: VER-06
    status: active
    obligation: "The shared fixture with the ARCH's PRD link at version 1 while PRD-001 is at version 2: no EPIC-001.md is written, and the reply names both versions and tells the user to amend the ARCH with /devforgeai:architecture PRD-001. Eval case stale-arch-stops: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-03
    upstream:
      - {id: STORY-005, item: AC-04, relation: verifies, version: 1, hash: null}
  - id: VER-07
    status: active
    obligation: "The shared fixture plus an existing EPIC-001.md (version 1, a unique sentinel line) that refines FR-002. EPIC-001.md still has version 1 and the sentinel; the new EPIC-002.md refines FR-003, FR-004 and NFR-001 and not FR-002; the reply reports FR-002 as covered by EPIC-001. Eval case existing-epic-not-duplicated: regex on both files and last_message."
    level: e2e
    covers:
      - BEH-06
      - BEH-12
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 1, hash: null}
  - id: VER-08
    status: active
    obligation: "The shared fixture with PRD-001 at status draft: EPIC-001.md and the reply say the epics are proposals because the PRD is a draft. Eval case draft-inputs: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-02
    upstream:
      - {id: STORY-005, item: AC-08, relation: verifies, version: 1, hash: null}
  - id: VER-09
    status: active
    obligation: "Shared fixture; the prompt says to proceed without questions and gives no grouping. EPIC-001.md exists, has status draft, and carries a [NEEDS CLARIFICATION] marker saying the grouping is unconfirmed. Eval case unconfirmed-grouping: regex on the file."
    level: e2e
    covers:
      - BEH-07
    upstream:
      - {id: STORY-005, item: AC-05, relation: verifies, version: 1, hash: null}
  - id: VER-10
    status: active
    obligation: "In VER-01's setup, the final reply names the story step as next with EPIC-001 as its input, and no file is written under docs/specs/story/. The grader doesn't check whether the story skill exists, so shipping it won't break this case. Eval case hands-off-to-story: regex on last_message and file_exists false."
    level: e2e
    covers:
      - BEH-11
    upstream:
      - {id: STORY-005, item: AC-09, relation: verifies, version: 1, hash: null}
  - id: VER-11
    status: active
    obligation: "A request such as 'write an epic poem about the sea' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
    upstream:
      - {id: STORY-005, item: AC-10, relation: verifies, version: 1, hash: null}
  - id: VER-12
    status: active
    obligation: "In VER-01's run, EPIC-001.md has non-empty generated_by tool, model and session, reviewed_by empty, every hash null, status draft, approved_by empty, target_release 'Spring launch', and an informed_by link to ARCH-001. Eval case records-provenance: regex on the file."
    level: e2e
    covers:
      - BEH-09
    upstream:
      - {id: STORY-005, item: AC-11, relation: verifies, version: 1, hash: null}
  - id: VER-13
    status: active
    obligation: "Manual, interactive, one fixture copy per check: (a) the skill proposes a grouping, the user changes it, and the epics written follow the changed grouping; (b) an unknown PRD ID lists the available PRDs and writes nothing; (c) two ARCHs citing the PRD are listed and the skill asks; (d) with no eligible requirement it writes nothing and reports every reason; (e) stopping before confirming writes nothing; (f) SKILL.md is within the NFR-001 limits, and metadata.devforgeai-version equals provenance.yaml's version; (g) run on this repository's own PRD-001, which has no ARCH, it writes nothing and hands back to the architecture step; (h) by reading only: SKILL.md states the three-attempt limit and the ERR-06 failure report. ERR-06 can't be forced without a CLI, so (h) is a reading check, not an exercise."
    level: manual
    covers:
      - BEH-01
      - BEH-07
      - ERR-01
      - ERR-04
      - ERR-05
      - ERR-06
      - ERR-07
      - QR-01
    upstream:
      - {id: STORY-005, item: AC-05, relation: verifies, version: 1, hash: null}
```

## 10. Rollout, migration and rollback

The skill is new; removing its directory rolls it back. No schema changes: `epic.schema.json` already
covers the epic document. Shipping the skill makes the architecture skill's `hands-off-to-epic` case
(SPEC-003 VER-10), which expects "not built yet", fail. SPEC-003 is approved, so its VER-10 change needs
Bryan's explicit approval during the build, as SPEC-002 v10 did for prd's handoff.

## 11. Implementation plan

1. Create a worktree for STORY-005 per ADR-001 v4, using the hardened deploy snippet.
2. `git mv src/staging/templates/epic.md` into `skills/epic/assets/`, and update the templates README rows.
3. Write `references/selection.md` and `references/output-rules.md` from §4, BEH-03 to BEH-10 and the epic schema.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-004 implementing SPEC-004.
5. Write the shared fixture and the case variants, checking each file against its schema, then the eval cases for VER-01 to VER-12.
6. Propose the SPEC-003 VER-10 change and its graders for Bryan's approval.
7. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Do VER-13 by hand.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| Epics for every current-release requirement | Starts delivery on unsettled foundations; ADR-002 puts architecture first |
| Read readiness from the architecture skill's reply | The reply misreported readiness once in three runs; the ARCH file was right every time |
| Treat a PRD with no ARCH as "nothing blocking" | Every requirement would look ready without anyone having looked. The skill hands back instead |
| Select by priority (Musts only) | MoSCoW keeps Shoulds and Coulds in the release as contingency; priority orders, release selects |
| Extend or rewrite existing epics | Needs a change-control design; v1 reports covered requirements and adds new epics only |
| Validate with `devforgeai check` when on PATH | The CLI doesn't exist, and an unrelated `devforgeai` was found on PATH; self-check only |

## 13. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft | all |
