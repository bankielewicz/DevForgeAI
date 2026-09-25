---
id: SPEC-004
type: spec
title: "Epic skill (MVP)"
status: draft
version: 2
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
  - {id: SPEC-003, relation: informed_by, version: 8, hash: null, note: "consumes the readiness rule (§4) and the downstream contract (§5)"}
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
  - organizational policy resolution: PRD-001 FR-006 to FR-008 cover only prd and Architecture Definition,
    and FR-012 (release later) covers the rest. This skill doesn't resolve policy (no R1–R5, no resolution
    line) and copies neither `policy.md` nor `defaults.md`. It reads `docs/specs/policy/` only for the
    bounded resolver check in §4;
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
- existing epics in `docs/specs/epic/`;
- approved policy documents in `docs/specs/policy/`, only for the bounded resolver check below.

All of these are read-only. **Output:** new epics at `docs/specs/epic/EPIC-NNN.md`, valid against
`epic.schema.json`.

**The current ARCH.** The skill uses the ARCH whose frontmatter `upstream` links cite this PRD. It is
**current** when that link's `version` equals the PRD's `version`. The architecture skill records that link
when it creates or amends an ARCH and, from SKL-003 v5 (SPEC-003 v7), when the user confirms reuse against a
newer PRD version: a **review record**. The frontmatter PRD link moves to the reviewed version, `outcome`
becomes `reuse`, and one Change Log row is added; the ARCH's `version`, `status`, approval fields and every
item stay byte-identical. A second review against the same PRD version writes nothing. A version mismatch means a review is
due, not that the architecture must change. No such ARCH, or one not reviewed against the PRD's current
version, means the skill writes nothing and hands back to `/devforgeai:architecture PRD-NNN` (ERR-02, ERR-03).

**Readiness** (`references/selection.md`), exactly SPEC-003 §4, applied to the ARCH file. A requirement R
is **ready** when, for every active `DEC` with `blocking: true` whose `upstream` cites R:
- `state` is `resolved`, and
- every `resolved_by` entry is an ADR whose file now has `status: accepted` and no `superseded_by`, or a
  policy setting that passes the bounded resolver check below.

A DEC blocks only the requirements its own `upstream` cites. Every PRD `[NEEDS ADR]` marker needs **its own
matching DEC**: one whose question answers the marker's decision and whose `upstream` cites every
requirement the marker names. When no DEC clearly answers a marker, every requirement it names is blocked
("marker without a matching question"), even if other DECs citing them are resolved. When readiness can't
be established, for example a resolving ADR's file is missing, R is `unknown`: never asserted ready or
blocked.

**Policy resolvers: a bounded check, not policy resolution.** A `POL-NNN#SET-NN` resolver counts only when
all four hold:
1. `docs/specs/policy/POL-NNN.md` exists and has `status: approved`;
2. setting `SET-NN` in it has `status: active`;
3. the policy document's `version` equals the version of the ARCH's link to that setting (ADR-003 A5
   records every applied setting as a link);
4. no other approved document in `docs/specs/policy/` sets the same key.

Otherwise R is `unknown`, naming the condition that failed. The next action is to review the architecture
with `/devforgeai:architecture`, which re-resolves policy.

**The selection rule.** A requirement R of the PRD (an FR or an NFR) is **eligible** when all hold:
1. R is `status: active`;
2. R is ready;
3. `release: current`;
4. `priority` is `must`, `should` or `could`;
5. for an FR only: no active existing epic (not `superseded` or `deprecated`) has a `refines` link to this
   PRD's R (the PRD ID and the item both match), at any version. NFRs are never "covered": an eligible NFR
   is attached to every new epic it constrains, even when an existing epic already refines it (Grouping).

Every other requirement is **left out**. The report gives each one **one compact row with every reason that
applies**, in the order below, and **one next action: the first listed reason's**. Several reasons never mean
several questions.

| Reason | When | Next action |
|---|---|---|
| `deprecated` | R is not active | none |
| `wont` | `priority: wont` | none for this release |
| `later` | `release: later` | none for the current release |
| `undecided` | `priority` or `release` is `null` | the PRD owner decides |
| `covered` | an active existing epic refines this PRD's FR; names the epic | none, unless it is also blocked: then review that epic's work before continuing |
| `blocked` | R is not ready; names the blocking DEC IDs, any superseded resolver, or the marker without a matching question | resolve it with `/devforgeai:architecture` |
| `unknown` | readiness can't be established: a missing or unreadable input, or a policy resolver that fails the bounded check; names it | fix that input, or review the architecture, then run again |

For example: `FR-005: later; DEC-04 open. No action for the current release.` and
`FR-008: covered by EPIC-002; now blocked by DEC-03 (ADR-002 superseded). Review EPIC-002's work before continuing.`

**Grouping.** Each eligible FR is refined by exactly one new epic. An eligible NFR is **attached** to every
new epic whose capability it constrains, with `note: "partial: <which part>"` when shared; attaching it never
creates a second deliverable. A **standalone NFR epic** is written only for an eligible NFR that no active
epic, existing or new in this run, refines. So rerunning with unchanged inputs writes nothing (ERR-05).
An epic's `priority` is the highest priority among the FRs it refines; a shared NFR never raises it, and a
standalone NFR epic takes its NFR's priority. New epics are numbered, and listed, Must first, then Should,
then Could.

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
    rule: "Find the ARCH whose frontmatter upstream links cite this PRD, and check that its PRD link version equals the PRD's version (§4), which the architecture skill records on create, amend or a confirmed reuse review. Use it only then; otherwise stop as ERR-02, ERR-03 or ERR-04."
  - id: BEH-04
    status: active
    rule: "Compute readiness for every active FR and NFR of the PRD from the ARCH file and the ADR files, exactly as SPEC-003 §4, reading each resolving ADR's current status and superseded_by now. A DEC blocks only the requirements its own upstream cites. A policy resolver counts only if it passes the bounded check in §4 (approved document, active setting, the ARCH's link version, no other approved document setting the same key); resolve no policy beyond that. Match every PRD [NEEDS ADR] marker to its own DEC (one whose question answers the marker's decision); when none clearly does, every requirement the marker names is blocked, even if other DECs citing it are resolved. When readiness can't be established, report the requirement as unknown, naming the missing input or failed check. Never use a skill's reply as the source."
  - id: BEH-05
    status: active
    rule: "Apply the selection rule (§4): a requirement is eligible only when it is active, ready, release current, priority must, should or could, and, for an FR, not already refined by an active existing epic. NFRs are never covered. Give every other requirement one compact row with every reason that applies (deprecated, wont, later, undecided, covered with the epic ID, blocked with the DEC IDs or unmatched marker, unknown), in the §4 order, and one next action, the first listed reason's."
  - id: BEH-06
    status: active
    rule: "Read every existing epic in docs/specs/epic/. An FR of this PRD that an active existing epic (not superseded or deprecated) refines, at any version and matching both the PRD ID and the item, is covered; if it is also blocked now, say so. NFRs are never covered. Never modify, renumber or duplicate an existing epic."
  - id: BEH-07
    status: active
    rule: "Propose how to group the eligible requirements into epics: each a deliverable capability, each eligible FR in exactly one epic, an eligible NFR attached to every new epic it constrains, and a standalone NFR epic only for an eligible NFR that no active epic, existing or new, refines (§4). Show each proposed epic's title, requirements and priority, and ask the user to confirm or change the grouping; write nothing until they do. A grouping stated in the request counts as confirmed. If no one can confirm (the request says to proceed without questions and gives no grouping), write the proposal and add to §8 of each epic: [NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]."
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
    rule: "Hand off with each epic written (path, title, priority and the requirements it refines), then the left-out rows (§4: every reason that applies and one next action per requirement, with no extra questions), and the proposal warning if an input is a draft. Then name the next step, the story step, with the new epic IDs as its input: if ${CLAUDE_PLUGIN_ROOT}/skills/story/SKILL.md exists, tell the user to run /devforgeai:story with an epic ID; otherwise say stories are written by hand from the story template for now. Never write a story."
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
    condition: "The ARCH that cites the PRD hasn't been reviewed against the PRD's current version (its PRD link version is older)"
    handling: "Write nothing. Name both versions, and tell the user to review the architecture against this PRD version with /devforgeai:architecture and the PRD ID; confirming reuse there records the review, and changes are made only if the review finds them"
    user_result: "A handback to review the architecture; no epic written"
  - id: ERR-04
    status: active
    condition: "Several ARCH documents cite the PRD"
    handling: "List them with their systems and PRD link versions, and ask; never pick one silently"
    user_result: "A choice of ARCH"
  - id: ERR-05
    status: active
    condition: "Nothing to write: every eligible FR is already covered, and every eligible NFR is already refined by an active epic (for example, a rerun with unchanged inputs)"
    handling: "Write nothing, say that no requirement needs a new epic, and report every left-out requirement with its reason"
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
| Structural: SKL-004 (commits f3238cf, 119750b, 641a388) | **Completed** on 2026-09-25. Every document, the moved template and every fixture pass their schemas; SKILL.md frontmatter and provenance pass, with `devforgeai-version` equal to the provenance `version`; no stale links; no symlinks under `src/`; `diff -r -x results` clean; the schema-copy loop prints nothing; `claude plugin validate --strict` passes. A scratch reference implementation of §4 run over the fixtures reproduces the shared-fixture table above |
| Behavioural (a): case thresholds (QR-03) | **Passed** on SKL-004 v2 (build 119750b, deployed hash `c9c30f53b6620e25fc4722de6d081516ec95c92397b3c22cc02d1ae7ecb29e0a`), 2026-09-25, **Claude Code 2.1.282**, 3 runs per arm against the no-plugin baseline, threshold 0.8. `--tag epic` `results/2026-09-25T06-20-54-668Z`, $28.99: all 14 cases ≥ 0.8, mean Δ +0.43. With / without / Δ: selects-ready-current 1.00/0.38/+0.62; blocked-not-included 1.00/0.44/+0.56; reports-left-out 1.00/0.25/+0.75; orders-by-priority 1.00/0.62/+0.38; no-arch-hands-back 1.00/0.00/+1.00; stale-arch-stops 1.00/0.33/+0.67; existing-epic-not-duplicated 1.00/0.86/+0.14; draft-inputs 1.00/0.33/+0.67; unconfirmed-grouping 1.00/0.67/+0.33; hands-off-to-story 1.00/0.75/+0.25; ignores-unrelated-request 1.00/1.00/0.00; records-provenance 1.00/0.85/+0.15; rerun-writes-nothing 1.00/0.75/+0.25; policy-resolver-revoked 0.89/0.67/+0.22. All 45 epics the with-plugin runs wrote pass the schema and the output-rule checks. The full-plugin run is row (e) |
| Behavioural (b): individual grader failures, with-plugin arm, kept apart | **Smoke run 1** (SKL-004 v1, build f3238cf, `--runs 1 --ablation none`, `results/2026-09-25T02-07-51-544Z`, $5.65): four, all on replies whose rows state the right reason in other words: blocked-not-included `fr-009-marker-unmatched` and `fr-010-marker-unmatched` ("the … open question in the PRD has no matching decision"), `fr-011-unknown-adr-004` (ADR-004 "is not in docs/specs/adr/"), reports-left-out `fr-007-undecided-owner` ("no priority set"). **Tag run 2** (row a): one, policy-resolver-revoked run 1 `fr-012-unknown-set-01` ("FR-012: can't be checked, because … POL-001#SET-01 … is deprecated. Review the architecture …, then run again"; its file graders passed). The original scores stand. Bryan ruled (R2-Q1) that these call for a grader repair, not a broadening (row c) |
| Behavioural (c): grader repair (R2-Q1, commit 641a388) | Bryan showed that `fr-012-unknown-set-01` rejected the correct paraphrase and accepted three wrong replies (negated, a wrong policy ID, "blocked" containing "unknown"). The 14 left-out reason graders are now row-scoped: in the requirement's own row they require the ID, the reason's meaning, the exact cause IDs and the next action, and reject negation, wrong IDs, contradictory readiness and a missing cause. 106 independent examples are committed as `grader-tests.yaml` in the four cases and pass offline against the grader files; the old FR-012 grader, run on the same examples, reproduces Bryan's finding. **Regrade of every saved reply** with the repaired graders, original scores unchanged: smoke run 1 (14 runs), four differences, all fail → pass; tag run 2 with-plugin (42 runs), one, fail → pass; tag run 2 without-plugin (42 runs), one **pass → fail** (existing-epic-not-duplicated run 3, `fr-002-covered-by-epic-001`: "FR-002 and FR-008: already covered by EPIC-001." gives no next action). Engine check on 641a388 (deployed hash `e9d10b4f40ea709d11e748fba74068575d50233129f9759423d8545007094473`, `--runs 1 --ablation none`, $1.78): the four repaired cases each 1.00, every grader file run (10/10, 5/5, 13/13, 4/4), so the engine ignores `grader-tests.yaml` and the repaired expressions compile |
| Behavioural (d): format obligation (SKL-004 v2's reason-label instruction) | **Partly followed.** In tag run 2's with-plugin replies, 200 of 236 left-out bullet rows (84%) name each reason by its §4 table word (blocked 86%, later 100%, won't 100%, covered 85%, unknown 75%, undecided 56%), against 82% in smoke run 1 before the instruction. The rest paraphrase ("can't be checked", "no priority set", "replaced by"). Not a SPEC-004 obligation; no wording round for it (R2-Q1) |
| Behavioural (e): full-plugin run | **Passed, no regression.** Build 641a388 (deployed hash `e9d10b4f…`, unchanged after the run), 2026-09-25, Claude Code 2.1.282, 3 runs per arm, threshold 0.8, `results/2026-09-25T12-50-56-368Z`, $106.50, 18 927 s: **56 of 56 cases ≥ 0.8**, mean with-plugin score 0.995, mean Δ +0.53, lowest 0.92. Epic 14/14 (blocked-not-included 0.93, the rest 1.00); architecture 14/14 (superseded-adr 0.93, the rest 1.00, including hands-off-to-epic, reuse-records-review and reuse-review-idempotent); brainstorm 8/8 (uses-named-framework 0.94); prd 20/20 (selects-unprocessed-brn 0.92). **Individual with-plugin grader failures, five in four runs, kept apart:** (1) epic blocked-not-included run 2, `fr-009-marker-unmatched` and `fr-010-marker-unmatched`: **grader false negatives, confirmed by the reply text** ("FR-009 (roster export to accounting): blocked because no architecture question answers the 'accounting system integration' marker. Resolve it with `/devforgeai:architecture PRD-001`."; FR-010 likewise). The repaired graders' no-match vocabulary lacked "no architecture question answers"; repaired later in 4bfcdeb (R3-Q4, row h). (2) architecture superseded-adr run 1: a real misreport, recorded in SPEC-003 §9 row (o) and deferred to STORY-004. (3) brainstorm uses-named-framework run 2, `file-fields-and-method` (llm, PASS FAIL FAIL on a 16 000-character file): R1 passes a mechanical field check and section 5 matches the passing runs; three blind offline Haiku passes (neutral IDs, shuffled, answer key hidden, with two negative controls) judged it PASS in all three: **probable judge false negative, not reproduced**. The offline judges were noisy too: each negative control passed once, and run 3 was failed once. (4) prd selects-unprocessed-brn run 2, `offers-only-brn-002` (llm, FAIL ×3): the reply offers only BRN-002, says BRN-001 is already covered by PRD-001, and asks; three blind passes judged it PASS in all three, and both negative controls FAIL in all three: **probable judge false negative, not reproduced**. The brainstorm and prd skills are unchanged since STORY-001 and STORY-002 |
| Behavioural (f): VER-13, manual (build 119750b, hash c9c30f53…) | 2026-09-24, Claude Code 2.1.282, one fixture copy per check, driven by the build session in cmux worker2 on Bryan's instruction (R1-Q4); fixture names are test data. **(a)** passed: the proposed four epics were changed to two (FR-002, FR-012, NFR-001 must; FR-003, FR-004, NFR-001 should), and the epics written follow the change exactly, with no unconfirmed-grouping marker. **(b)** passed: PRD-009 → PRD-001 listed, nothing written. **(c)** passed: ARCH-001 and ARCH-002 listed with systems and PRD link versions; it asked; nothing written. **(d)** passed: nothing written, one row for each of FR-001 to FR-012 and NFR-001 matching the reference implementation, no question. **(e)** passed: stopped at the grouping question, nothing written, resume instruction given. **(f)** passed: SKILL.md 202 lines, description 405 characters, `devforgeai-version` "2" equals provenance `version: 2`. **(g)** passed: in a clone of this repository at 119750b, PRD-001 v9 has no ARCH; nothing written; handed back to `/devforgeai:architecture PRD-001` (with the draft warning; PRD-001 is a draft). **(h)** passed as a **reading check**: SKILL.md step 8 states the three-attempt limit and the ERR-06 validation-failure report; ERR-06 isn't exercised. **(i)** passed every listed clause: PRD-001 v3 (priority only) → ERR-03 naming v2 and v3; the confirmed reuse changed only the PRD link, `outcome` and one review row; the epic skill then wrote two epics at PRD v3 linking ARCH-001 at its version 2; a second confirmed reuse changed nothing. In (i) the architecture skill wrote ARCH-001 with `sed -i` through Bash, not Edit (SPEC-003 §9 row p); fixed in SKL-003 v6 and (i) re-passed with no Bash write (SPEC-003 §9 row q). Evidence: `~/devforgeai-evidence/STORY-005/ver13/`. These checks and row (a) cover the shipped build: `git diff --stat 119750b 641a388 -- src/claude/DevForgeAI/skills` is empty (641a388 changes only 14 epic graders and adds `grader-tests.yaml`) |
| Behavioural (h): round 3 (commits 4bfcdeb, 9e2b6b5, 6bce650) | 2026-09-25, Claude Code 2.1.282. **Grader repair (R3-Q4):** `fr-009` and `fr-010-marker-unmatched` accept "no architecture question answers the … marker" (113 committed examples, all as labelled); regrade of every saved reply changes only the full run's blocked-not-included run 2 (fail → pass). **blocked-not-included on the shipped build 6bce650** (`results/2026-09-25T21-08-10-535Z`, $2.18): 0.93 (Δ +0.48); run 1 failed `fr-009` and `fr-010-marker-unmatched` on correct rows ("FR-009: blocked, because the 'accounting system integration' question in the PRD has no matching decision in ARCH-001. Resolve it with `/devforgeai:architecture PRD-001`."): **grader false negatives**, the marker term accepts only "marker", "NEEDS ADR" or "open question". Follow-up, not changed. VER-13 (i) re-passed on SKL-003 v6 (SPEC-003 §9 row q). The epic skill is unchanged since 119750b |
| Behavioural (g): observed, not graded | The skill's readiness table (a SKILL.md device, not an obligation) was skipped in some non-interactive runs and in VER-13 (i) step 4; the selection was right in every run read |

**Shared fixture.** One approved PRD, `PRD-001` v2 with `target_release: "Spring launch"`, and one
approved `ARCH-001` whose frontmatter cites PRD-001 v2. Each is written fresh and checked against its
schema. The ADRs are `ADR-001` (accepted, answers DEC-02), `ADR-002` (superseded by `ADR-003`) and `ADR-003`
(accepted, a different topic: it answers DEC-04, audit storage). `docs/specs/policy/POL-001.md` is an approved
organization policy at version 1 whose `SET-01` (`architecture.mandated_platforms`) resolves DEC-07; the ARCH links it
at version 1.

| Requirement | Priority / release | ARCH | Expected |
|---|---|---|---|
| FR-001 | must / current | DEC-01 open, cites only FR-001; a PRD `[NEEDS ADR]` marker names FR-001 | left out: blocked by DEC-01 |
| FR-002 | must / current | DEC-02 resolved by ADR-001, cites FR-002 and NFR-001 | eligible |
| FR-003 | should / current | no DEC | eligible |
| FR-004 | could / current | no DEC | eligible |
| FR-005 | must / later | DEC-06 open, cites FR-005 | left out: later; DEC-06 open, no action for the current release |
| FR-006 | wont / current | no DEC | left out: wont |
| FR-007 | null / current | no DEC | left out: undecided |
| FR-008 | must / current | DEC-03 resolved by ADR-002, superseded | left out: blocked by DEC-03 |
| FR-009 | must / current | no DEC; a PRD `[NEEDS ADR]` marker names FR-009 | left out: blocked (marker without a matching question) |
| FR-010 | must / current | DEC-04 (audit storage) resolved by ADR-003, cites FR-010; a PRD `[NEEDS ADR]` marker for a different decision (payment provider) names FR-010, and no DEC answers it | left out: blocked (marker without a matching question) |
| FR-011 | must / current | DEC-05 resolved by ADR-004, whose file doesn't exist | left out: unknown (ADR-004 not found) |
| FR-012 | must / current | DEC-07 resolved by `POL-001#SET-01`: approved, active, POL-001 v1 equals the ARCH's link version, and no other policy sets the key | eligible |
| NFR-001 | must / current | DEC-02 | eligible |

So the eligible set is FR-002, FR-003, FR-004, FR-012 and NFR-001. FR-001 shows that DEC-01 blocks only what it
cites (FR-002 stays eligible), FR-008 shows that a superseded resolver blocks again, and FR-009 shows that
a `[NEEDS ADR]` marker with no question still blocks, and FR-010 shows that one resolved DEC doesn't
answer a different marker. File graders
check the written epics, not the reply, because a wrong epic is worse than a wrong sentence. Unless a
case says otherwise, the prompt states the grouping, so the run is non-interactive and confirmed.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture; the prompt asks for one epic covering everything eligible. docs/specs/epic/EPIC-001.md refines FR-002, FR-003, FR-004, FR-012 and NFR-001 at PRD-001 version 2, and contains no refines link to FR-001 or FR-005 to FR-011. Eval case selects-ready-current: regex on the file."
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
    obligation: "In VER-01's setup, no epic refines FR-001, FR-008, FR-009, FR-010 or FR-011, and the reply reports FR-001 blocked by DEC-01, FR-008 blocked by DEC-03 (naming ADR-002 as superseded), FR-009 and FR-010 blocked by a [NEEDS ADR] marker without a matching question, and FR-011 as unknown because ADR-004 isn't found; FR-002 and FR-012 are not reported blocked or unknown. Eval case blocked-not-included: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 1, hash: null}
  - id: VER-03
    status: active
    obligation: "In VER-01's setup, the reply gives one row each for FR-005 (later, with DEC-06 open and no action for the current release), FR-006 (won't have) and FR-007 (undecided, for the PRD owner), each with a next action, and asks no question about them. Eval case reports-left-out: regex on last_message."
    level: e2e
    covers:
      - BEH-05
      - BEH-11
    upstream:
      - {id: STORY-005, item: AC-03, relation: verifies, version: 1, hash: null}
  - id: VER-04
    status: active
    obligation: "Shared fixture; the prompt asks for one epic per priority level, with NFR-001 only in the Must epic. EPIC-001.md has priority must and refines FR-002, FR-012 and NFR-001; EPIC-002.md has priority should and refines FR-003; EPIC-003.md has priority could and refines FR-004. Eval case orders-by-priority: regex on the three files."
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
    obligation: "The shared fixture with the ARCH's PRD link at version 1 while PRD-001 is at version 2: no EPIC-001.md is written, and the reply names both versions and tells the user to review the architecture with /devforgeai:architecture PRD-001. Eval case stale-arch-stops: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-03
    upstream:
      - {id: STORY-005, item: AC-04, relation: verifies, version: 1, hash: null}
  - id: VER-07
    status: active
    obligation: "The shared fixture plus an existing EPIC-001.md (version 1, a unique sentinel line) that refines FR-002, FR-008 and NFR-001 (partial). The prompt asks for one epic covering everything eligible, with NFR-001 applying to it. EPIC-001.md still has version 1 and the sentinel; the new EPIC-002.md refines FR-003, FR-004, FR-012 and NFR-001 and not FR-002; the reply reports FR-002 as covered by EPIC-001, reports FR-008 as covered by EPIC-001 and now blocked by DEC-03, and doesn't report NFR-001 as covered. Eval case existing-epic-not-duplicated: regex on both files and last_message."
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
    obligation: "Manual, interactive, one fixture copy per check: (a) the skill proposes a grouping, the user changes it, and the epics written follow the changed grouping; (b) an unknown PRD ID lists the available PRDs and writes nothing; (c) two ARCHs citing the PRD are listed and the skill asks; (d) with no eligible requirement it writes nothing and reports every reason; (e) stopping before confirming writes nothing; (f) SKILL.md is within the NFR-001 limits, and metadata.devforgeai-version equals provenance.yaml's version; (g) run on this repository's own PRD-001, which has no ARCH, it writes nothing and hands back to the architecture step; (h) by reading only: SKILL.md states the three-attempt limit and the ERR-06 failure report; (i) the review loop: PRD-001 gets a priority-only change to version 3, the skill stops (ERR-03), /devforgeai:architecture PRD-001 with reuse confirmed moves the ARCH's frontmatter PRD link to version 3, sets outcome reuse and adds one Change Log row, with the ARCH's version, status, approval fields and items unchanged, and the skill then writes epics; confirming reuse again at version 3 changes nothing in the ARCH. ERR-06 can't be forced without a CLI, so (h) is a reading check, not an exercise."
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
      - BEH-03
    upstream:
      - {id: STORY-005, item: AC-05, relation: verifies, version: 1, hash: null}
      - {id: STORY-005, item: AC-12, relation: verifies, version: 1, hash: null}
  - id: VER-14
    status: active
    obligation: "The shared fixture plus an existing EPIC-001.md (version 1, a unique sentinel line) that already refines FR-002, FR-003, FR-004, FR-012 and NFR-001, as a first run would have written. No docs/specs/epic/EPIC-002.md is written, EPIC-001.md still has version 1 and the sentinel, and the reply says no requirement needs a new epic. Eval case rerun-writes-nothing: file_exists false, regex on the file and last_message."
    level: e2e
    covers:
      - BEH-06
      - BEH-07
      - ERR-05
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 1, hash: null}
  - id: VER-15
    status: active
    obligation: "The shared fixture with POL-001's SET-01 at status deprecated: EPIC-001.md contains no refines link to FR-012, and the reply reports FR-012 as unknown, naming POL-001#SET-01 and the failed check. Eval case policy-resolver-revoked: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 1, hash: null}
```

## 10. Rollout, migration and rollback

The skill is new; removing its directory rolls it back. No schema changes: `epic.schema.json` already
covers the epic document. Two changes to the approved architecture skill ship with it, both approved by
Bryan on 2026-09-24 (PR #10) and specified in the SKL-004 build brief: SPEC-003 v7 and SKL-003 v5.
- **The review record:** a confirmed reuse against a newer PRD version records the review (§4). Without
  it, a reuse writes nothing and this skill's current-ARCH check would reject the ARCH forever.
- **VER-10:** the architecture skill's `hands-off-to-epic` case expects "not built yet", which fails once
  this skill ships, as SPEC-002 v10 did for prd's handoff.

## 11. Implementation plan

1. Create a worktree for STORY-005 per ADR-001 v4, using the hardened deploy snippet.
2. `git mv src/staging/templates/epic.md` into `skills/epic/assets/`, and update the templates README rows.
3. Write `references/selection.md` and `references/output-rules.md` from §4, BEH-03 to BEH-10 and the epic schema.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-004 implementing SPEC-004.
5. Write the shared fixture and the case variants, checking each file against its schema, then the eval cases for VER-01 to VER-12, VER-14 and VER-15.
6. Make the two approved architecture changes (SPEC-003 v7, SKL-003 v5): the review record and VER-10.
7. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Do VER-13 by hand.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| Epics for every current-release requirement | Starts delivery on unsettled foundations; ADR-002 puts architecture first |
| Read readiness from the architecture skill's reply | The reply misreported readiness once in three runs; the ARCH file was right every time |
| Treat a PRD with no ARCH as "nothing blocking" | Every requirement would look ready without anyone having looked. The skill hands back instead |
| Select by priority (Musts only) | MoSCoW keeps Shoulds and Coulds in the release as contingency; priority orders, release selects |
| Extend or rewrite existing epics | Needs a change-control design; v1 reports covered requirements and adds new epics only |
| Stop until the ARCH is amended whenever the PRD version changes | A priority-only PRD change would force an amendment with nothing to change, and a confirmed reuse, which writes nothing, would never clear it. A review record clears it instead |
| Validate with `devforgeai check` when on PATH | The CLI doesn't exist, and an unrelated `devforgeai` was found on PATH; self-check only |

## 13. Open questions

- None.

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft | all |
| 2 | 2026-09-24 | claude-code | Left-out reasons: `covered` now comes before `blocked`, and the next action is the first listed reason's, so both §4 examples follow from the rule (FR-005 takes later's action, FR-008 covered's). Found while building STORY-005 (R1-Q1), approved by Bryan | §4, BEH-05 |
