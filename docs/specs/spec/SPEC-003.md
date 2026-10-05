---
id: SPEC-003
type: spec
title: "Architecture Definition skill (MVP)"
status: approved
version: 11
created: 2026-09-23
updated: 2026-10-04
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "388b2532-f519-4deb-b4ce-3e294d7e3b10"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-10-04
upstream:
  - {id: STORY-003, relation: specifies, version: 3, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 11, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 11, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: the Architecture Definition step"}
  - {id: ADR-003, relation: constrains, version: 2, hash: null, note: "accepted: configuration contract v1"}
  - {id: SPEC-002, relation: informed_by, version: 5, hash: null, note: "consumes the prd skill's downstream contract (SPEC-002 §5)"}
  - {id: SPEC-012, relation: constrains, version: 13, hash: null, note: "the task-list convention (§4) the workflow checklist follows"}
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

**Version 6** (2026-10-03) has the skill keep its workflow checklist in Claude Code's task list when the session
has one, as the progress tracker's task-list convention asks (SPEC-012 §4), so that each decision and the
outcome are credited to the step that asked for them (BEH-17). It also confirms the outcome at step 8, once the
change is known, before it writes to an existing ARCH: a reuse or amend chosen at step 4 picks the direction,
and step 8 approves the result (BEH-08).

**Version 7** (2026-10-03) applies the same to a confirmation typed into the request: it too comes before the change
is known, so with a user present step 8 still asks; only a request to proceed without questions keeps it (BEH-08).

**Version 8** (2026-10-03) tags each question with its step, as SPEC-012 version 9's convention asks: hidden in
AskUserQuestion's metadata, where the progress tracker checks it against the step marked in progress, and shown
in each question's header, where you see it (BEH-17).

**Version 9** (2026-10-04) asks the waiver (Bryan, 2026-10-04). When your request says to proceed without questions,
the skill first asks whether it should, in a question of its own with two fixed answers, "Proceed without questions"
and "Ask me as usual" (BEH-18). Your answer is recorded, so the progress tracker sees the choice your request made:
after "Proceed without questions", an outcome the request named is written at step 8 without asking, as BEH-08 says,
and the tracker counts your answer for step 8 instead of refusing the ARCH in enforce mode (SPEC-012 version 11,
BEH-19). Every other decision still needs your answer. Without the question tool, as in eval runs, nothing is asked
and the request is followed as before.

**Version 10** (2026-10-04) settles two follow-ups (Bryan, 2026-10-04). Step 8's question gains a third answer,
"Write nothing": the run then changes no file, lists the answers you gave so a later run can use them, and stops
(BEH-08). Before, an outcome you didn't confirm was still written, with `outcome: null`. And the waiver question no
longer counts against `interview.max_calls`: it asks how to run, not about the architecture (BEH-18).

**Version 11** (2026-10-04): when step 8 proposes reuse, it offers two answers, "Confirm reuse" and "Write
nothing": a reuse has no change to write with the outcome open (BEH-08).

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
  an approved policy's active setting that still mandates the platform, for the capability, that the
  ARCH recorded for it.

Otherwise R is **blocked**, and the report names the DEC IDs. A superseded ADR returns its
questions to open, until an accepted successor resolves them. So does a mandated platform that
changed, until the question is resolved again:
- **The record** is the setting's entry in the last resolution line of the ARCH's Change Log,
  `architecture.mandated_platforms=<platform> for <capability> (POL-NNN#SET-NN)`
  (`references/policy.md`). When the policy's `version` still equals the version of the ARCH's link
  to the setting, the setting is unchanged and there is nothing to compare.
- **No platform recorded** (a resolution line written in an older format): the report names the gap.
  With a user present, the skill asks whether the setting mandated the same platform when the
  question was resolved: if yes, it still counts; if no or unknown, the question is open. With no
  user, it still counts.

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
  - Bash only to run `python3` with the shared policy validation script (SPEC-002 §5), and to run the read-only commands ls, find, grep, cat, head and test -f with explicit paths in the documents read by contract, the skill's own files or the inspection scope: no writes, no redirection, and no running, installing or building project code. Claude Code may provide no Glob or Grep tool, so listing these folders can need Bash;
  - AskUserQuestion, with at most 4 questions per call;
  - when the session has them, the task-list tools (TaskCreate and TaskUpdate, or TodoWrite) for the workflow
    checklist (BEH-17).
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
    rule: "Take the PRD from $ARGUMENTS (PRD-NNN). With no argument, list the PRDs in docs/specs/prd/ with their titles and status, and ask. When docs/specs/prd/ holds no PRD, say that none exists yet, write nothing, and point to /devforgeai:prd. Never take a file path."
  - id: BEH-02
    status: active
    rule: "Read the PRD's requirements, constraints, stage, operating context and [NEEDS ADR] markers, and record its version in every link. If the PRD is a draft, warn that the result is a proposal. Never turn an unanswered product question (a null priority, a release or a [NEEDS CLARIFICATION] marker) into an architectural decision. Never edit the PRD."
  - id: BEH-03
    status: active
    rule: "Resolve policy exactly as the prd skill does (ADR-003 A3–A5, references/policy.md): the R1–R5 sequence, the SV rules, local preferences, the resolution line, and stopping on invalid policy. Approved policy documents are validated in full through the shared validation script, as SPEC-002 §5 and BEH-17 R1 specify; when the script can't run while approved policy exists, stop (ERR-02)."
  - id: BEH-04
    status: active
    rule: "Select the architecture description. Read docs/specs/arch/ARCH-*.md. If one covers the same system, propose reusing it or amending it (BEH-08), with reasons, and ask. Offer reuse only when that ARCH's frontmatter already links this PRD and no DEC in it is resolved by a mandated platform that changed (§4); otherwise propose amending it, or creating a new ARCH. When a user is present and a blocking DEC is open, recommend amending, since recording a decision on it is an amendment. Create a new ARCH, the next free ARCH-NNN.md, only when none covers the system or the user chooses to. Never create a second baseline automatically. Ask when several could apply."
  - id: BEH-05
    status: active
    rule: "Inspect only the components or directories the user names (inspection_scope). Code inspection is read-only, and every path it reads, lists or searches is inside inspection_scope: use Read, Glob and Grep when available, otherwise read-only shell commands (ls, find, grep, cat, head) with explicit paths inside the scope, with no redirection, no writes and no running or building project code; never list or search the whole repository. The project documents read by contract (docs/specs/prd/, arch/, adr/ and policy/, and .claude/devforgeai.local.md) are outside this rule, and validating the documents written (BEH-14) is separate from inspection. References such as imports and configuration may be followed only within that scope; ask before going outside it. Record every project source consulted for architecture analysis as an EVD item, with the version and status examined where applicable, classified independently of its kind as observed (code or configuration directly inspected within inspection_scope), policy (an approved, active, applicable setting), decided (an accepted, non-superseded ADR) or context (any other consulted input or historical material, including the input PRD, existing ARCHs, proposed, rejected or superseded ADRs, and documentation claims not corroborated by the implementation). Context establishes neither implemented behavior nor an accepted decision, and no classification resolves a DEC by itself. When evidence is insufficient, say so explicitly with a [NEEDS CLARIFICATION] marker, and never recommend reuse on assumption."
  - id: BEH-06
    status: active
    rule: "Identify the architectural questions that separate epics must share: component boundaries and responsibilities, data ownership, major interactions and interfaces, deployment, and how quality requirements are met. Every [NEEDS ADR] marker in the PRD becomes a DEC. Each DEC cites every affected requirement in its upstream links and is blocking unless the user says otherwise. Leave feature-level detail to specs."
  - id: BEH-07
    status: active
    rule: "Resolve each question only by one of three means. (1) An approved, active mandated-platform setting that answers exactly this question: resolved_by POL-NNN#SET-NN, applied as policy, not a user decision. (2) An existing accepted, non-superseded ADR that the user confirms answers exactly this question. (3) The user's explicit decision among the options presented with trade-offs, which is written as a new ADR with status accepted and approved_by the user. Anything else stays open. A deferred decision may be written as a proposed ADR that resolves nothing. When the user later decides a question that has a proposed ADR, the decision is a new accepted ADR that supersedes the proposed one; the user's decision is the approval. A DEC reopened because its mandated platform changed (§4) is resolved again by that setting only when the user confirms that the setting as it now stands answers it, as for an existing ADR in (2); with no user it stays open. While the DEC's most recent transition in the Change Log is that reopening (BEH-09), no run resolves it by that setting without the user's confirmation. An ADR or setting resolves only the question it answers, never every question that cites the same requirement."
  - id: BEH-08
    status: active
    rule: "Propose the outcome with reasons: reuse (the existing ARCH links this PRD and covers it unchanged, and this run changes no DEC), amend (the existing ARCH needs new or changed questions or components, or this run records a decision on an existing DEC or reopens one) or create (no ARCH covers the system). Offer reuse only as BEH-04 allows. Reusing one platform or component is not a reuse outcome. When any DEC's state or resolved_by changes in this run, the outcome is amend: if reuse was chosen earlier, say why and ask again. Write outcome only when the user confirms it, and keep it null otherwise. Confirming the outcome accepts no decision. When reuse is proposed, and in the handoff when it is confirmed, name every active requirement of the PRD that no active blocking DEC cites, and say that it is reported ready with no architectural question holding it back. When the user confirms reuse and the ARCH's frontmatter PRD link is older than the PRD's version, record the review (BEH-09); when that link already equals the PRD's version, confirming reuse writes nothing. A reuse or amend chosen at step 4 (BEH-04), in an answer or the request, picks the direction but doesn't confirm the outcome when the run will write to the existing ARCH (an amendment, or reuse's review record): step 8 then asks for confirmation once the change is known, naming what will change, such as the DEC, CMP and EVD items added, the DECs whose state or resolver changes, the ADRs accepted or superseded, the new version, and an approved ARCH's return to in-review. With a user present, step 8 asks even when the request confirmed the outcome: a confirmation given before the change is known picks the direction, as step 4's choice does (version 7). A request to proceed without questions keeps the request's confirmation and asks nothing at all (Bryan, 2026-10-03), once the waiver question (BEH-18) has been answered Proceed without questions or couldn't be asked; after any other answer, step 8 asks as with a user present (version 9). Step 8's question has three options, in this order: 'Confirm <outcome>' (Recommended), 'Write it with the outcome open' and 'Write nothing' (version 10; Bryan, 2026-10-04: 'Add Write nothing'); when the proposed outcome is reuse, only 'Confirm reuse' (Recommended) and 'Write nothing', since a reuse has no change to write with the outcome open (version 11; Bryan, 2026-10-04: 'Two answers for reuse'). Confirm writes the outcome; Write it with the outcome open writes the change with outcome null, as an unconfirmed outcome always was; Write nothing writes and edits no file, marks step 8 completed, lists in the reply each question asked in the run with its answer, says that nothing was written so a later run can reuse those answers, and ends the run's work there: steps 9 to 11 stay pending (BEH-17), since completing step 9 without a write would claim work not done. Text typed instead of an option is the user's answer, read as any typed answer is; a dismissal leaves the question unanswered, so nothing it affects is written (BEH-17's rule for a pending answer)."
  - id: BEH-09
    status: active
    rule: "Write or amend the ARCH. A new ARCH starts as draft. Amending bumps the version, continues item numbering, keeps existing items unchanged except for DEC state and resolved_by transitions (each logged in the Change Log), and returns an approved ARCH to in-review. Those transitions are a decision recorded on an existing DEC (BEH-07), and reopening a DEC whose resolver no longer counts: a superseded ADR, or a mandated platform that changed (§4). The Change Log row that reopens a DEC for a changed mandated platform names the DEC, the setting, and the platform recorded before and now. A review record, written when the user confirms reuse against a newer PRD version, makes exactly three changes: the frontmatter PRD link moves to the reviewed version, outcome becomes reuse, and one Change Log row is added, 'Reviewed against PRD-NNN vN: reuse confirmed, no architectural change', ending with the policy resolution line. Everything else stays byte-identical, including version, updated, status, the approval fields and every item with its links, which still show as suspect. It is a relink, not an amendment, so an approved ARCH stays approved. With no user, nothing is confirmed and nothing is written."
  - id: BEH-10
    status: active
    rule: "Describe the components that separate epics must share, as CMP items with a Mermaid overview. Link each to the quality drivers (NFR items) and constraints it serves, and to the POL setting when a mandated platform applies (relation constrains). Give each CMP its kinds (§4): one or more of user-interface, service, platform, api, relational-store, data-store and external. When a kind is uncertain, ask. With no user present, record only the kinds the PRD or the evidence states; when none is certain, leave kinds out and add [NEEDS CLARIFICATION: kinds of CMP-NN] to the open questions. When amending, existing components stay unchanged, with or without kinds."
  - id: BEH-11
    status: active
    rule: "Compute readiness with the §4 rule for every requirement cited by any DEC. Check each ADR's current status and superseded_by, and each mandated-platform setting against the platform the ARCH recorded for it (§4), at the time of writing; a question whose resolving ADR has been superseded, or whose mandated platform changed, is reported open."
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
  - id: BEH-17
    status: active
    rule: "When the session has task-list tools (TaskCreate and TaskUpdate, or TodoWrite; they may need loading through ToolSearch), keep the workflow checklist there, as SPEC-012 §4's task-list convention says. Before anything else, create one task per checklist step: its subject the step's checklist line without the box ('<N>. <title>'), its metadata devforgeai_step: N (with TodoWrite, the content '<N>. <title>'). Mark a step in_progress when its work starts. Before asking the user any question, mark the step the question belongs to in_progress: which PRD to step 2, reuse, amend or create to step 4, going outside the inspection scope to step 5, every decision question to step 7, and the outcome to step 8. So step 7 is completed and step 8 in progress before the outcome question is asked, alone in its own form. Never put two steps' questions in one question form. Tag each question form with its step: the AskUserQuestion call's metadata source 'devforgeai_step:N', which the user doesn't see and the progress tracker checks against the step marked in progress, and each of its questions' header 'Step N', which the user sees (SPEC-012 §4, version 9). Mark each step completed as soon as it is done, one at a time, a step with nothing to do included (step 5 with no scope, step 7 with no open question). After step 8's Write nothing (BEH-08), steps 9 to 11 stay pending: the run stops there (version 10). Without task-list tools, copy the checklist into the reply and tick items off as before. SKILL.md names the tag devforgeai_step, which tells the progress tracker that the skill follows the convention."
  - id: BEH-18
    status: active
    rule: "The waiver (version 9; Bryan, 2026-10-04). When the request says to proceed without questions (or 'don't ask me anything', 'proceed without asking me anything else', 'decide nothing') and the session has AskUserQuestion, ask it once, in step 1, right after the policy script has run (BEH-03) and before any other question, with step 1 marked in_progress (BEH-17): one question, alone in its form, the one question BEH-17's tag rule leaves out, with metadata source devforgeai_waiver (not devforgeai_step:1, so the progress tracker records it as the waiver and never as a step's answer), header 'Step 1', the question 'Your request says to proceed without questions. Should I?' and exactly two options, in this order: 'Proceed without questions' (description: 'I ask nothing more; decisions that need you stay open, except the outcome your request named.') and 'Ask me as usual' (description: 'I ask about each decision as it comes up.'). On Proceed without questions, follow the request's no-question rules (BEH-07, BEH-08). On Ask me as usual, on anything typed instead, or on a dismissal, ask as if the request hadn't said so, step 8's confirmation included. The questions BEH-01 and BEH-04 ask whatever the request says (which PRD, when none is named; reuse, amend or create, when an existing ARCH covers the system) are still asked when open. Ask the waiver at most once in a run. The waiver question doesn't count against interview.max_calls (version 10; Bryan, 2026-10-04: 'Doesn't count'). Without AskUserQuestion, ask nothing, in plain text or otherwise, and follow the request as before; when the request doesn't say to proceed without questions, never ask it."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The PRD ID given does not exist"
    handling: "List the available PRD IDs and write nothing; when no PRD exists, say so and point to /devforgeai:prd"
    user_result: "The list of PRDs, or that none exists yet"
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
    handling: "Stop. Keep the user's architectural choices and unrelated content, and never leave approved or accepted on content that failed validation. A new ARCH stays draft. An amended ARCH keeps the status BEH-09 gave it, so an approved ARCH whose content changed stays in-review with approved_by and approved_on cleared; a review record that fails validation is treated the same way. A new ADR the user accepted becomes proposed with empty approval fields and is kept, and the DEC state and resolved_by that depended on it return to open. When that ADR superseded an existing ADR in the same run, the supersession is rolled back: the older ADR is restored byte-for-byte to its state before the run; the replacement ADR is kept as proposed with approved_by, approved_on and supersedes cleared, and its prose and Status history still record the intended replacement and the user's decision; each DEC that depended on the replacement returns to open with resolved_by [] and is never reconnected to the older ADR; and the EVD item that recorded the older ADR for that supersession is kept, with status deprecated and its other fields unchanged, because item IDs are never deleted. Add one matching audit record (Change Log row, and Status history row for an ADR). End with a validation-failure report listing the checks, the repairs and the unresolved errors; skip the readiness handoff and never present readiness as validated"
    user_result: "A validation-failure report: the file paths, the checks and repairs made, the unresolved errors and the statuses left, including any supersession rolled back; no readiness presented as validated"
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
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 11, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version"
    measured_by: "Reading against skill-frontmatter.schema.json and skill.schema.json, and comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 11, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged architecture and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 11, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Versions 10 and 11 (SKL-003 v9) | Merged in PR #83 (`ab8301c`, 2026-10-04) and deployed as plugin 0.21.0 on 2026-10-04 (the deployed copy matches the source; `diff -rq` exit 0). Built on branch `docs/waiver-follow-ups` (draft PR #83) through `/plugin-dev:create-plugin` and `/plugin-dev:skill-development` (`9c091af`, reviews' fixes `8fe705f`, `0e12260`, reuse's two answers `ef0c104`); skill-reviewer and plugin-validator, no critical finding; `evaluate.py check` matched; SKILL.md 499 lines. VER-30: single-arm evals bound to `ef0c104` (`--runs 1 --ablation none`, judge sonnet, threshold 0.8; `tmp/eval-results/followups-suite1-20261004T220926-{brainstorm,architecture}`): brainstorm 9 of 9 and architecture 24 of 24, every case 1.00 ($18.02 for architecture). The two folders' plugin digests differ only by Claude Code's generated type files (`.claude-plugin/types/`, `tsconfig.json`, gitignored and not deployed), rewritten when the plugin loaded. VER-32 Live in Bryan's worker1 tab on 2026-10-04, Claude Code 2.1.289, enforce mode, `claude --plugin-dir` on a deploy-style copy of the build plus a probe mod that logged each turn.complete's reason: (a) `ws-arch-wn`, VER-28's request: step 8 asked 'Confirm amend (Recommended)', 'Write it with the outcome open', 'Write nothing' under 'Step 8'; Write nothing left `docs/` byte-identical to a fresh scaffold, no ADR, the reply listed the run's questions and answers, steps 9 to 11 stayed pending, and state.json showed step 8 done by the answer and no flag (in enforce mode); (b) `ws-arch-max`, `interview.max_calls: 2`, a waiving request answered 'Ask me as usual': after the waiver, one step-7 form (four questions) and step 8's question, two calls; Confirm amend wrote ARCH-001 with `outcome: amend` and ADR-002 and ADR-003. Pass. Not run live: reuse's two-answer form (version 11) |
| Version 9 (SKL-003 v8) | Merged in PR #77 (`8eb431a`, 2026-10-04 18:15 UTC) and deployed as plugin 0.20.0 on 2026-10-04 (the deployed copy matches the source; `diff -rq` exit 0). Built on branch `docs/waiver-menu-specs` (PR #77, `9366f46`, review fixes `505a4ba`); checklist unchanged, manifest matched. VER-30: `tmp/eval-results/waiver-suite1-20261004T120554-{brainstorm,architecture}` in the worktree, bound to `505a4ba`, 1 run, `--ablation none`: brainstorm 9 of 9 and architecture 24 of 24 at 0.8 or above ($4.65 and $17.74). VER-31 live, in Bryan's worker1 tab on 2026-10-04, enforce mode, `claude --plugin-dir` on a copy of `505a4ba`: (a) after the policy script the waiver menu; Proceed: no other question, ARCH-001 amended with outcome: amend and not refused; (b) Ask me as usual: step 7's questions and step 8's confirmation asked. Pass. The 3-run qualification was waived by Bryan on 2026-10-04, who approved SKL-003 v8 the same day |
| Versions 6 to 8 (SKL-003 v7) | Built on branch `feat/skl-001-v6-skl-003-v7` (worktree, draft PR #73) through `/plugin-dev:create-plugin`, 2026-10-03 and 2026-10-04: the eval cases first `1fe55f6` (`keeps-task-list`, `confirms-amend-at-step-8` and `request-confirm-still-asks`, generated by `make_evals.py`, the existing 21 unchanged), the skill `1d93c29`, the review fixes `aba1b04` and `7e6168d`, Bryan's review decisions `edee883` (step 8 asks for every outcome it writes once the change is known, create included), `max_turns` 90 in `f1654d8`, and step 1's change `ea3e2ce` and `a3e67ea` (§13: the policy script runs whatever the folder holds, as a command of its own). **Evals**, in Bryan's cmux tab on his word: a pilot bound to `7e6168d`, `tmp/eval-results/pilot-architecture-20261003T185015/` (keeps-task-list, confirms-amend-at-step-8, request-confirm-still-asks, superseded-adr, changed-platform-reopens, failed-amendment-stays-in-review: 6 of 6 at 1.00); one single-arm run of the suite bound to `f1654d8`, `tmp/eval-results/suite1single-architecture-20261003T201734/`: 24 of 24 at 1.00, $17.28, 22 to 51 turns of 90. Both ran before step 1's change. **Bryan waived the 3-run qualification with the baseline on 2026-10-04**, so no eval has run on step 1's final wording; the live run below covers it. Every eval run offered TaskCreate, TaskUpdate and ToolSearch and no AskUserQuestion. **VER-27: pass** on 2026-10-04, live in enforce mode with no policy folder, Claude Code 2.1.289 (session `8b03a4ed`, run `20261004T102529Z-architecture-339ec7bb`): step 1 ran `validate_policy.py` on its own (exit 0, strong evidence); 22 step events, every step started and done in order; two step-7 forms (DEC-01 to DEC-05, then the decider) and the outcome asked alone under step 8, each form tagged, with the header 'Step N'; ADR-001 to ADR-005 accepted and ARCH-001 created with `outcome: create`; no refusal, no flag, counts.unmarkedQuestions 0. An earlier live run on 2026-10-03 (session `3bb90ad9`, before step 1's change) passed on the task list, the tags and step 8, but enforce mode refused 5 ADR writes: four because step 1 skipped the script with no policy, one because the script ran joined to other commands. That run is why step 1 changed. SKL-003 v7 was approved by Bryan on 2026-10-04; merged in PR #73 (`2f99a01`, 2026-10-04) and deployed as plugin 0.18.0 the same day in Bryan's cmux tab, where the deployed copy matched the source (`diff -rq` printed nothing) |
| Version 5 | Claude: SKL-003 v6 implements it. Its automated VER items ran on 2026-10-01, 21 of 21 at 1.00 in every one of 3 runs (the SKL-003 v6 rows below); the manual VER-12 (a), (j), (k) and (l), VER-19 and VER-20 pass; VER-12 (i) passed within VER-19's run (ADR-003, accepted before validation, was restored to proposed), and VER-12 (f) by `src/tests/prd/test_shared_files.py` at `9796f22`; VER-12 (b) to (e), (g), (h) and VER-13 are not run. SKL-003 v6 was approved by Bryan on 2026-10-01, merged in PR #54 and deployed (plugin 0.10.0). Codex: not run. Changed: §4 (a mandated platform counts only while it is the one the ARCH recorded), §5 (Bash for scoped read-only commands), BEH-01, BEH-04, BEH-07, BEH-08, BEH-09, BEH-11, ERR-01, ERR-05 and VER-19; new: VER-20 (manual) and VER-21 to VER-25. The rows below record versions 1 to 4 |
| Version 4 | Claude: SKL-003 v4's automated VER items ran on 2026-09-29, 16 of 16 at 1.00 (the SKL-003 v4 row below); the manual VER-12, VER-13 and VER-19 are not run. SKL-003 v5, the shared-schema change (PR #25), still implements this version; its 3 policy cases were requalified on 2026-09-30, 3 of 3 at 1.00 (the SKL-003 v5 row below). Codex: not run; the Codex port of the shared-schema change (PR #26) has its own native evaluation (`src/codex/devforgeai/shared-schema-update-evidence/20260930/REPORT.md`). Changed: ERR-05 (a supersession recorded in a run that then fails validation is rolled back); new: VER-19 (manual regression case) |
| Version 3 | Not run. Changed: BEH-03, BEH-14, ERR-02, ERR-05, VER-12 (f) and (i); new: VER-17 and VER-18. The rows below record versions 1 and 2 |
| Structural: schemas, templates, fixtures and cross-document links | Fixtures: `src/tests/architecture/make_evals.py` validates all 15 against `src/schemas/` before it writes the cases. Schemas, templates and cross-document links: not run |
| Behavioural: automated VER items, one eval case each | Built as SKL-003 v1 and merged in PR #4; deployed. 14 eval cases (VER-01..11, 14, 15, 16). `claude plugin eval`, 3 runs with the no-plugin baseline, 2026-09-28, plugin 0.3.0: 14 of 14 at 1.00 in every run, mean Δ +0.67. That run checked VER-10's not-built branch; PR #5 switched `hands-off-to-epic` to the shipped branch, which scored 1.00 in 1 run with the baseline |
| Behavioural: SKL-003 v6, the five new cases on v5 and on v6, 2026-10-01 | One run each, no baseline, written before SKL-003 v6 (§11 step 1). On SKL-003 v5 (commit `cd892e0`; `tmp/eval-results/arch-v5-newcases-20261001T133751/`, written in the detached `arch-v5-check` worktree and kept in the main checkout's `tmp/eval-results/`): VER-21 1.00, VER-22 0.33, VER-23 1.00, VER-24 0.80, VER-25 0.57, $2.40. VER-21 and VER-23 already pass on v5 and stay as regression guards; on VER-22 v5 refused the confirmed reuse, on VER-24 it reported DEC-01 still resolved, and on VER-25 it didn't reopen DEC-01. On SKL-003 v6 (commit `dcbb024`; `tmp/eval-results/arch-v6-newcases-20261001T134913/`): 5 of 5 at 1.00, $2.21 |
| Behavioural: SKL-003 v6, architecture tag runs, 2026-10-01 | Claude Code 2.1.287; judge model sonnet; threshold 0.8; concurrency 4. **One run with the baseline:** `tmp/eval-results/arch-v6-1run-20261001T142042/`, commit `f663361`: 21 of 21 at 1.00, mean Δ +0.61, $17.81, 668 s. **Three runs with the baseline:** two folders, both bound by `src/tests/prd/record_revision.sh` to commit `0c93f9a` and plugin digest `51f246e666128e79ace08233314de74d4ece13fdb86a73866cd9a7e6c82791bd`: `tmp/eval-results/arch-v6-3run-20261001T143253/` (13 cases complete; a usage limit stopped the other 8, whose runs all errored and are discarded) and `tmp/eval-results/arch-v6-3run-rest-20261001T163700/` (those 8 rerun with `--tag architecture --case`). **All 21 cases scored 1.00 with the plugin in every run**; mean Δ +0.63; $53.04 for the runs kept. `policy-bad-date`'s baseline lost 2 of 3 runs to the limit, so its Δ rests on one baseline run. This qualifies SKL-003 v6 against SPEC-003 v5's automated items. The folders, and the one-run and v6 new-case folders above, are local and untracked: written in the build worktree `.claude/worktrees/spec-003-v5` and kept in the main checkout's `tmp/eval-results/` |
| Behavioural: manual VER items for SKL-003 v6, 2026-10-01 | `docs/runbooks/architecture-v6-checks.md` section 4, driven by Bryan with a copy of the v6 plugin loaded with `--plugin-dir`. **VER-20: pass** (sessions `797948c0` and `1228a170`). Each run also added and deferred a new shared question that cites FR-001 or NFR-001, so not every requirement that only DEC-02 blocked reports ready: VER-20 lacks VER-05's "unless the amendment adds a DEC that cites them" clause, a wording fix for the next version. **VER-12 (a) and (l): pass.** **VER-12 (j): pass.** **VER-12 (k): pass** (session `dff4dde7`). **VER-19: pass** (session `ffaafe1f`): ADR-001 byte-identical; the replacement proposed with approval and `supersedes` cleared; DEC-01 open; EVD-04 kept as `deprecated`. The skill flagged CMP-01's invalid status before writing. Its read-back used `sed -n` and `cat -A`, outside the allowed read-only commands (self-reported, nothing written). **VER-12 (i): pass** in the same run (ADR-003, accepted before validation, restored to proposed). **VER-12 (f)**: `src/tests/prd/test_shared_files.py` passes at `9796f22`. VER-12 (b) to (e), (g), (h) and VER-13: not run |
| Behavioural: SKL-003 v4, architecture tag run, 2026-09-29 | `tmp/eval-results/arch-v4-3run-20260929T141038/` (local, untracked). Started 14:10:39 EDT (18:10:39 UTC); Claude Code 2.1.284; plugin 0.6.0; 16 cases (VER-01 to VER-11, VER-14 to VER-18); 3 runs per arm against the no-plugin baseline; threshold 0.8; judge model sonnet; concurrency 4; $41.41; 1,661 s. **All 16 cases scored 1.00 with the plugin in every run**, with no errors; mean Δ +0.63. VER-17 `policy-bad-date` Δ +0.25 (the baseline also stops in most runs, so it shows the contract more than a gain); VER-18 `failed-amendment-stays-in-review` Δ +0.56. **Bound:** `src/tests/prd/record_revision.sh` wrote the commit `7e87cf4` (PR #16's merge), the plugin digest `dc301097547da60d3a3e0a319e61de14e781d487058b3661454cc3db03d22dbe` and a copy of the case files into the folder before the run. This qualifies SKL-003 v4 against SPEC-003 v4's automated items. SKL-003 v4 was approved by Bryan on 2026-09-29, after the manual VER-19 and VER-12 (i) runs |
| Behavioural: SKL-003 v5, policy-case requalification, 2026-09-30 | `tmp/eval-results/architecture-requal-20260930T135333-<case>/` (local, untracked), one folder per case, run by Bryan from a plain terminal with the shared-schema worktree's `tmp/requalify.sh`, after the prd cases. Started 15:00:32 EDT (19:00:32 UTC); Claude Code 2.1.286; plugin 0.7.0; the 3 policy cases (VER-02 `org-a-policy`, VER-03 `org-b-policy`, VER-17 `policy-bad-date`); 3 runs per arm against the no-plugin baseline; threshold 0.8; judge model sonnet; concurrency 1; $8.32; 1,401 s. **All 3 cases scored 1.00 with the plugin in every run**, with no errors; mean Δ +0.75 (VER-02 +1.00, VER-03 +1.00, VER-17 +0.25; VER-17's baseline again stops in most runs). **Bound:** `src/tests/prd/record_revision.sh` wrote the commit `a19949b` (PR #25's head; `src/` is identical at its merge `c2e6751`), the plugin digest `d4c23f78826894bbcdd2a29429b00689ba37601db3e8673ac78d29f2d43496b5` and a copy of the case files into each folder before its run. Every change from v4 is in policy validation and its reference text, so the other 13 cases last ran on v4 (the row above). **After the run:** the Codex port's evaluation found that `scripts/validate_policy.py` accepted `.nan` as `testing.coverage_threshold`; PR #27 (`4c01126`) made it a `schema` error, with no version bump. None of these 3 fixtures contains a NaN or a `testing.*` key, so the run wasn't repeated (Bryan, 2026-09-30). SKL-003 v5 was approved by Bryan on 2026-09-30 |
| Behavioural: SKL-003 v3, stopped run, 2026-09-29 | `tmp/eval-results/arch-v3-3run-20260929T134349/` in the build worktree (local, untracked). Commit `9bdb87a`, plugin digest `89919cc5e1e9e30a51e168fc2afbd923dd0ce7ddef0c92e66cfc9d531b00400c`, 16 cases, 3 runs per arm, concurrency 4. Stopped by Bryan after 1,108 s ($27.17), because version 4 changed the candidate; the aggregate is marked partial (interrupted). Ten cases had finished at 1.00 in all three plugin runs, including VER-17 and VER-18; `prd-change-handed-back` had one run at 1.00 before the stop cut the other two; five cases never started. It doesn't qualify SKL-003 v4 |
| Behavioural: SKL-003 v2 (component kinds), architecture tag run, 2026-09-29 | `tmp/eval-results/arch-stray-2026-09-29T15-14-40-867Z/` (local, untracked; moved from `src/claude/DevForgeAI/evals/results/` with version 5 and renamed with an `arch-stray-` prefix). Started 11:14:40 EDT (15:14:40 UTC); Claude Code 2.1.284; 14 cases; 3 runs per arm against the no-plugin baseline; threshold 0.8; concurrency 1; $34.92; 5,634 s. **All 14 cases scored 1.00 with the plugin**, with no failed grader in the with-plugin arm; mean Δ +0.64. `cmp-kinds` (VER-01's kinds clause) passed in all three `creates-arch` runs. **Revision:** commit `58647d3` at the start (PR #10 merged), then `5074a5b` from 11:16:17; `src/claude` is identical in both, and the plugin digest was `ebdb88382160091db135a78d3ae976727058bdb1aaf3037b899141b7eda5c92d` at 11:19 EDT. This qualifies SKL-003 v2 against SPEC-003 v2's automated items; version 3's changes (ERR-05, BEH-14, the shared policy script, VER-17, VER-18) aren't built yet |
| Behavioural: earlier run, mixed source, 2026-09-29 | `tmp/eval-results/arch-stray-2026-09-29T13-36-54-382Z/` (local, untracked; moved from `src/claude/DevForgeAI/evals/results/` with version 5 and renamed with an `arch-stray-` prefix). Started 09:36:54 EDT on PR #10's branch; the checkout switched to main at 10:05:04, 28 minutes into a 97-minute run, so its later cases tested the version-1 skill. 14/14 ≥ 0.8, mean Δ +0.66, $34.88; `hands-off-to-epic` 0.92, with the llm grader `handoff-quality` failing in one run (judge votes PASS FAIL FAIL). Not a qualification of either revision; kept as recorded. An interrupted third attempt (1 run, $0.40, `tmp/eval-results/arch-kinds-20260929T113839/`) is not a result |
| Behavioural: manual VER items (VER-12, VER-13, VER-19) | 2026-09-29 (Claude Code 2.1.285, a copy of the plugin at `7e87cf4` loaded with `--plugin-dir`, driven through the owner's cmux tab by session fdbef416-eebb-4053-95ce-624a311d72d5). **VER-19: pass**, in session `b17fd6d2-eaa9-4eec-9a30-e887ce30e3da` with the scaffold in `src/tests/architecture/manual/failed-supersession/`. The user approved superseding ADR-001 and chose built-in sign-in for DEC-01; validation found CMP-01's `status: current` and stopped after check 1. Afterwards: ADR-001 byte-identical to the fixture; ADR-002 proposed, with approved_by, approved_on and supersedes cleared, and its prose and Status history keeping the intended replacement and Priya Nair's decision; DEC-01 open with `resolved_by: []`; ARCH-001 in-review with the approval cleared, every existing item unchanged, and the audit row naming the rollback; a validation-failure report with no readiness. Notes: the operator cancelled the question form by mistake, so the answers came in a follow-up message; the EVD-04 that recorded the supersession was kept, deprecated, which ERR-05 doesn't specify. **VER-12 (i): pass** in the same run (a decision accepted before validation, then ERR-05). **VER-12 (f)**: `src/tests/prd/test_shared_files.py` passes at `7e87cf4`. The other VER-12 items and VER-13: not run |
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
  - id: VER-19
    status: active
    obligation: "Manual regression case, failed supersession: a fresh fixture copy where the approved ARCH-001's DEC-01 is resolved_by an accepted ADR-001, and its existing CMP-01 has a value the self-check rejects, which an amendment must leave unchanged. The user chooses to amend ARCH-001, confirms that outcome, and explicitly approves replacing ADR-001 with a new decision for DEC-01; the skill records the supersession, and validation then fails. Afterwards: ADR-001 is byte-identical to its state before the run (status accepted, superseded_by null, the same Status history); the replacement ADR is kept with status proposed, approved_by empty, approved_on null and supersedes [], and its prose and Status history record the intended replacement of ADR-001 and the user's decision; DEC-01 is open with resolved_by [], not reconnected to ADR-001; the EVD item the run added for ADR-001 is still present, with status deprecated and its other fields as written, and no EVD item is deleted; ARCH-001 is in-review with approved_by and approved_on cleared, with the audit record; and the reply is a validation-failure report that names the rollback and presents no readiness as validated. A run with no user never supersedes an ADR (BEH-07, BEH-16), so this case is run by hand."
    level: manual
    covers:
      - ERR-05
      - BEH-16
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 3, hash: null}
  - id: VER-20
    status: active
    obligation: "Manual, deciding an open question later: a fresh fixture copy where an approved ARCH-001 already links PRD-001 at its current version, its DEC-02 is open and blocking, and PRD-001 is unchanged. The user runs the skill for PRD-001 without naming an outcome. The skill recommends amending ARCH-001 because DEC-02 is open, presents DEC-02's options with their trade-offs, and the user picks one. Afterwards: a new ADR is accepted with approved_by the user; DEC-02 is resolved_by it; ARCH-001's version is one higher, it is in-review with approved_by and approved_on cleared, outcome is amend, and every existing item is byte-identical except DEC-02's state and resolved_by, logged in the Change Log; and the handoff reports ready each requirement that only DEC-02 blocked. In a second fresh copy where DEC-02's deferral is recorded as a proposed ADR, the new accepted ADR supersedes it, and the proposed ADR changes only status: superseded, superseded_by and one Status history row."
    level: manual
    covers:
      - BEH-04
      - BEH-07
      - BEH-08
      - BEH-09
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 3, hash: null}
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-21
    status: active
    obligation: "Reuse needs a link to this PRD: ARCH-001 covers the clinic system and its frontmatter links only PRD-001; PRD-002, for the same product, is linked by no ARCH. The prompt runs the skill for PRD-002, chooses to reuse ARCH-001, confirms the reuse outcome and says to proceed without questions. Nothing is written: ARCH-001 is byte-identical and no ARCH-002.md exists. The reply says that reuse needs an ARCH that links PRD-002, and offers amending ARCH-001 or creating a new ARCH. Eval case reuse-needs-prd-link: regex on the file and last_message, file_exists false for ARCH-002.md."
    level: e2e
    covers:
      - BEH-04
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
      - {id: STORY-005, item: AC-12, relation: verifies, version: 2, hash: null}
  - id: VER-22
    status: active
    obligation: "Reuse over a requirement no question cites: as VER-15, but PRD-001 version 2 also adds FR-003, which no DEC of ARCH-001 cites. The prompt chooses to reuse ARCH-001, confirms the reuse outcome and says to proceed without questions. The review record is written as in VER-15, and the reply names FR-003 as reported ready with no architectural question citing it. Eval case reuse-names-uncited: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-08
      - BEH-09
      - BEH-15
    upstream:
      - {id: STORY-003, item: AC-09, relation: verifies, version: 3, hash: null}
      - {id: STORY-005, item: AC-12, relation: verifies, version: 2, hash: null}
  - id: VER-23
    status: active
    obligation: "No PRD yet: docs/specs/prd/ holds no PRD, and the prompt runs the skill with no PRD ID. Nothing is written under docs/specs/, and the reply says that no PRD exists and points to /devforgeai:prd. Eval case no-prd-exists: file_exists false for docs/specs/arch/ARCH-001.md, regex on last_message."
    level: e2e
    covers:
      - BEH-01
      - ERR-01
    upstream:
      - {id: STORY-003, item: AC-01, relation: verifies, version: 3, hash: null}
  - id: VER-24
    status: active
    obligation: "A changed mandated platform blocks reuse: an approved ARCH-001 links PRD-001 at its current version; its DEC-01 is resolved_by POL-001#SET-01, and the last resolution line in its Change Log records platform A for identity and authentication. POL-001 is now at a newer version whose SET-01 mandates platform B for the same capability. The prompt chooses to reuse ARCH-001, confirms the reuse outcome and says to proceed without questions. Nothing is written: ARCH-001 is byte-identical. The reply says that DEC-01's mandated platform changed, naming POL-001#SET-01, and offers amending ARCH-001 instead of reuse. Eval case changed-platform-blocks-reuse: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 3, hash: null}
      - {id: STORY-003, item: AC-06, relation: verifies, version: 3, hash: null}
  - id: VER-25
    status: active
    obligation: "A changed mandated platform reopens its question: the fixture of VER-24, but the prompt chooses to amend ARCH-001, confirms that outcome and says to proceed without questions. In the amended ARCH-001, DEC-01 is open with resolved_by [], since no user confirmed SET-01 as it now stands; every other existing item is byte-identical; the new Change Log row logs DEC-01's transition, naming POL-001#SET-01 and both platforms. The handoff reports FR-001 blocked by DEC-01. Eval case changed-platform-reopens: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-07
      - BEH-09
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 3, hash: null}
      - {id: STORY-003, item: AC-06, relation: verifies, version: 3, hash: null}
  - id: VER-26
    status: active
    obligation: "With the task-list tools allowed, VER-01's fixture and prompt give a task list kept by the convention: at least 11 TaskCreate calls whose input carries devforgeai_step, one of them with the subject '8. Propose and confirm the outcome'; the first TaskCreate before the first Write; at least 11 TaskUpdate calls to completed; and ARCH-001 still written. Eval case keeps-task-list, generated by make_evals.py: allowed_tools adds TaskCreate, TaskUpdate, TaskList and TaskGet; tool_used graders with input_match, tool_order, file_exists. A TaskUpdate's input names only a task ID and a status, so which task is which step, and the marking before a question, are checked live by VER-27."
    level: e2e
    covers:
      - BEH-17
    upstream:
      - {id: STORY-003, item: AC-01, relation: verifies, version: 3, hash: null}
  - id: VER-27
    status: active
    obligation: "Live, in a session with the task tools, with SPEC-013's VER-22: an architecture run in which the user answers keeps its list, with step 7 in progress for every decision form, step 7 completed and step 8 in progress before the outcome question, asked alone, every question form tagged devforgeai_step:N for its step with each question's header 'Step N' (version 8), and each step completed in order; the tracker records step events for all 11 steps and flags no question gate (counts.unmarkedQuestions 0). Recorded in §9."
    level: manual
    covers:
      - BEH-17
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 3, hash: null}
  - id: VER-28
    status: active
    obligation: "Confirming an amendment at step 8: an approved ARCH-001 links PRD-001 version 1, and PRD-001 version 2 adds a requirement that raises a new question. The prompt runs the skill for PRD-001, chooses to amend ARCH-001 without confirming the outcome, and defers every new question (decide later). Nothing is written to ARCH-001 before the outcome is confirmed: it is byte-identical, and the final reply asks to confirm amend, naming what amending changes: at least the new DEC, the new version and ARCH-001's return to in-review. Eval case confirms-amend-at-step-8, generated by make_evals.py: regex on the file, llm grader on last_message."
    level: e2e
    covers:
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-29
    status: active
    obligation: "A confirmation in the request still asks at step 8: VER-28's fixture, but the prompt chooses to amend ARCH-001, says 'I confirm the amend outcome', defers every new question and doesn't say to proceed without questions. ARCH-001 is byte-identical, and the final reply asks to confirm amend, naming what amending changes. Eval case request-confirm-still-asks, generated by make_evals.py: regex on the file, llm grader on last_message. Every existing case whose prompt confirms an outcome also says to proceed without questions, so none changes."
    level: e2e
    covers:
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-30
    status: active
    obligation: "Without AskUserQuestion, no waiver question stops a run: every generated case whose prompt says to proceed without questions (or to proceed without asking anything else) still passes at 0.8 or above, with nothing asked; confirms-amend-at-step-8 and request-confirm-still-asks, whose prompts don't waive, still end by asking step 8's confirmation in the reply."
    level: e2e
    covers:
      - BEH-18
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-31
    status: active
    obligation: "Live, in enforce mode, with SPEC-013's VER-36: an architecture run whose request chooses to amend ARCH-001 and says to proceed without questions runs the policy script, then asks the waiver alone, tagged devforgeai_waiver with header 'Step 1' and the two labels; 'Proceed without questions' gives no other question, an ARCH written with outcome: amend that the tracker doesn't refuse, every new DEC open and no ADR; in a second run, 'Ask me as usual' gives step 7's questions and step 8's confirmation. A request that doesn't waive shows no waiver question. Recorded in §9."
    level: manual
    covers:
      - BEH-18
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
  - id: VER-32
    status: active
    obligation: "Live, in Bryan's worker1 tab (version 10): an architecture run on VER-28's fixture whose request chooses to amend ARCH-001 and doesn't waive questions reaches step 8, whose question offers 'Confirm amend' (Recommended), 'Write it with the outcome open' and 'Write nothing' in that order; 'Write nothing' leaves ARCH-001 byte-identical and no ADR written, the reply lists the run's questions with their answers and says nothing was written, and steps 9 to 11 stay pending in the task list. In observe mode, that run's state.json shows step 8 done and no flag. A second run on the same fixture whose request chooses to amend ARCH-001, leaves one new question undeferred and says to proceed without questions, answered 'Ask me as usual' at the waiver, with interview.max_calls: 2 in .claude/devforgeai.local.md, asks one step-7 question call and step 8's question after the waiver: two calls besides it. After 'Proceed without questions' step 8 asks nothing, so Write nothing isn't offered. Recorded in §9."
    level: manual
    covers:
      - BEH-08
      - BEH-18
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 3, hash: null}
```

## 10. Rollout, migration and rollback

The skill and the ARCH type are new; removing the skill directory rolls it back. The schema change is
additive: the `ARCH` document prefix and the `CMP`, `DEC` and `EVD` item prefixes.

Versions 6 to 8 (SKL-003 v7) ship in a plugin version no earlier than the one that builds SPEC-012 version 9 and
SPEC-013 version 8, so a session without the task tools is never held to a task list, and the tags it writes are
recorded and checked. The checklist's lines
don't change, so the tracker's architecture manifest stays matched. Rolling back is returning to SKL-003 v6; the
tracker then places the run's answers by its windows again (SPEC-012 BEH-09). The Codex architecture skill
isn't changed: the tracker's adapter is Claude Code's (SPEC-013).

Version 9 (SKL-003 v8) ships in the plugin version that builds SPEC-012 version 11 and SPEC-013 version 10 (0.20.0),
so the waiver's answer is recorded and counted for step 8. The checklist's lines don't change, so the architecture
manifest stays matched; its step 8 gains `waivable` (SPEC-012 DM-01). This spec's SPEC-012 link moves to version 11
when that is approved.

Version 10 (SKL-003 v9) ships with SPEC-001 version 15 and SPEC-013 version 11, in one plugin version. The checklist's
lines don't change, so the architecture manifest stays matched, and SPEC-012 doesn't change: a run that ends at
Write nothing reaches no step past 8, so the tracker flags nothing and reviews nothing (SPEC-013 BEH-26).

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

**Version 4** (after approval): the architecture skill's ERR-05 rules roll back a supersession recorded
in a run that fails validation (SKL-003 v4), and VER-19 is run by hand. The Codex architecture skill
follows the same contract.

**Version 5** (after approval): SKL-003 v6 implements the changed §4, §5, BEH and ERR items.
1. In `src/tests/architecture/make_evals.py`, add the cases for VER-21 to VER-25 and VER-20's
   fixtures, and move the hand-written `cmp-kinds` grader into the generator (regenerating must leave
   the existing cases unchanged). Run the new cases on SKL-003 v5 with `--runs 1 --ablation none`; a
   case that already passes stays as a regression guard.
2. Build SKL-003 v6, with the skill-only fixes of the 2026-10-01 review. Among them is decision D1: a
   request that names an accepted ADR while saying to proceed without questions leaves the DEC open,
   with the ADR recorded in its `notes`. The "proceed without questions" rule also gains the matching
   exception: a DEC reopened for a changed mandated platform is not resolved again by that setting
   (BEH-07).
3. Evaluate the whole suite, cheapest first, then run VER-12 (a), (j) and (k), VER-19 and VER-20 by
   hand. The Codex architecture skill follows the same contract, through a Codex session.

**Version 6** (after approval), through `/plugin-dev:create-plugin` and Anthropic's two skill guides:
1. In `src/tests/architecture/make_evals.py`, add the cases `keeps-task-list` (VER-26) and
   `confirms-amend-at-step-8` (VER-28) and `request-confirm-still-asks` (VER-29, version 7); regenerating must
   leave the existing cases unchanged. Run them on SKL-003
   v6 with `--runs 1 --ablation none`; they fail, since v6's text names no `devforgeai_step` and takes step 4's
   amend as the confirmation.
2. Build SKL-003 v7: the Workflow section takes BEH-17's wording and step 8 BEH-08's confirmation, `provenance.yaml` and
   `metadata.devforgeai-version` go to 7, skill-reviewer reviews it, and `evaluate.py check` (SPEC-012 IF-02)
   reports the architecture manifest matched.
3. Evaluate cheapest first: `keeps-task-list` with `--runs 1 --ablation none`, then the suite with `--runs 1`,
   then 3 runs with the baseline. A trace with no TaskCreate call means the case's `allowed_tools` didn't give
   the eval's model the task tools: record it in §9 and bring it to the owner before the full suite.
4. Once the plugin version that builds SPEC-012 version 9 and SPEC-013 version 8 is deployed, run VER-27 live.

**Version 9** (after approval), through `/plugin-dev:create-plugin` and `/plugin-dev:skill-development`:
1. Build SKL-003 v8: the waiver in step 1 after the policy script (BEH-18) and BEH-08's clause; `provenance.yaml` and
   `metadata.devforgeai-version` go to 8; skill-reviewer reviews it; `evaluate.py check` reports the manifest matched.
2. Evaluate cheapest first: a few waiving cases with `--runs 1 --ablation none`, then the suite with `--runs 1`
   (VER-30).
3. Once the plugin version that builds SPEC-012 version 11 and SPEC-013 version 10 is deployed, run VER-31 live.

**Version 10** (after approval), through `/plugin-dev:create-plugin` and `/plugin-dev:skill-development`:
1. Build SKL-003 v9: step 8's three options and Write nothing (BEH-08), the waiver outside `interview.max_calls` in
   "Asking" (BEH-18); `provenance.yaml` and `metadata.devforgeai-version` go to 9; skill-reviewer reviews it;
   `evaluate.py check` reports the manifest matched.
2. Evaluate the suite with `--runs 1` (eval runs have no question tool, so no case changes; every case must still
   pass).
3. Run VER-32 live in worker1, on Bryan's word.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| ADRs only, no ARCH document | Nothing citable for component boundaries, and nowhere to track questions and readiness |
| Unblock a requirement when any accepted ADR cites it | Unblocks FR-001 once the identity provider is chosen while session revocation is still open. Readiness is per question instead (§4) |
| Require the user to name every file to inspect | Too much friction. Named components or directories, with read-only discovery inside them, instead |
| Crawl the whole codebase | Unbounded cost, and it mixes observed practice with decisions. Bounded inspection and EVD classification instead |
| Require an approved PRD first | Makes architectural exploration expensive. Drafts are allowed with a warning, and product questions are never turned into decisions |
| Tick the checklist in the reply only | The tracker can't tell which step a question belongs to when Claude asks before it ticks: a live run asked step 7's and 8's questions under step 6 (SPEC-012 §9); ticks stay the fallback without a task list |
| Ask the waiver on every run, or in plain text without the question tool | Every run would open with a question, and eval runs, which have no question tool, would stop at it. Bryan chose to ask only when the request waives (2026-10-04) |
| Let the skill amend PRD requirements | Downstream never edits upstream, and the PRD's extension mode is append-only. Proposed changes go to the PRD owner (BEH-12) |

## 13. Open questions

- Recorded (Bryan, 2026-10-03, while building SKL-003 v7; accepted): a request that names amend or reuse and says
  to proceed without questions has the skill write that outcome without asking (BEH-08), but the progress tracker
  never sees the request's text, so it counts no answer for step 8. SPEC-012's architecture manifest then flags the
  ARCH write in observe mode and refuses it in enforce mode, whose refusal says to ask the user or leave the outcome
  open. Enforce mode needs an answer the tracker can see; a recorded waiver (a "proceed without questions" answer,
  specified next) is the planned way to make the user's choice visible.
- Resolved (Bryan, 2026-10-04, version 9 with SPEC-012 version 11 and SPEC-013 version 10): the waiver question
  (BEH-18) makes that choice visible, and a Proceed answer counts for step 8 only ("Step 8 only"). He accepted that the
  tracker then can't tell whether the request really named the outcome written. A dismissal or a typed answer means
  "Ask me as usual" (Resolved, Bryan, 2026-10-04, version 10: "Keep as is"; it keeps every decision asked).
- Resolved (Bryan, 2026-10-04, version 10: "Doesn't count"): the waiver question doesn't count against
  `interview.max_calls` (BEH-18).
- Recorded (Bryan, 2026-10-03, while building SKL-003 v7; his choice "A + live run"): step 1 runs the shared
  validation script whatever `docs/specs/policy/` holds, a missing folder included, as a command of its own.
  SPEC-012's architecture manifest takes a successful run of `validate_policy.py` as step 1's evidence, and in a live
  enforce-mode run with no policy folder the skill, which then skipped the script, had every ADR write refused, and
  once more when it ran the script joined to other commands. With no approved policy the script prints `No policy
  folder at …` or `OK: no approved policy document …` and exits 0, so the result is BEH-03's: the framework defaults
  apply. The mechanics now differ from the prd skill's, which still skips the script when no `POL-*.md` exists; the
  result is the same, and prd's step 1 takes the same change when prd gets a manifest. The shared `policy.md`,
  `defaults.md` and script are unchanged. Evals can't show the refusals gone, since the tracker records nothing in
  an eval's non-interactive runs (SPEC-013 BEH-01); a live enforce-mode run is the check.
- Accepted by Bryan (2026-10-04, from the skill-reviewer review of step 1's change): the shared `validate_policy.py`
  treats a `POL-*.md` with no readable `status` as a candidate for approval and validates it in full, rather than
  skipping it as not approved; a hand-written policy file missing `status:` fails validation (ERR-02), never passes
  silently. The script is byte-identical with the prd skill's (SPEC-002 §5), so any change is made in both.
- Resolved (Bryan, 2026-10-03, with SPEC-012 version 9): each question names its step, in AskUserQuestion's
  metadata, which the tracker checks against the step marked in progress when the question is asked, and in each
  question's header, which the user sees; an answer counts for a step only when the two agree.
- Resolved (Bryan, 2026-10-03): step 4's reuse-or-amend answer used to confirm the outcome for step 8 as well,
  but SPEC-012's architecture manifest lets `outcome` take a value only with an answer counted for step 8, so
  the tracker flagged such a run's ARCH write (refused in enforce mode). Step 8 now confirms the outcome once the
  change is known (BEH-08): the question guards an existing ARCH, and the tracker needs no change. Version 7
  (Bryan, 2026-10-03) closes the last case, a confirmation typed into the request, which the tracker can't see
  (a '/' prompt is no answer, SPEC-013 BEH-04): with a user present, step 8 asks then too.
- Resolved (Bryan, 2026-10-04, version 10: "Add 'Write nothing'"): declining at step 8 can leave the files untouched.
  Version 9 wrote an unconfirmed amendment with `outcome: null`, so the question showed the change but couldn't stop
  it; step 8 now offers Write nothing (BEH-08, VER-32), modelled on ERR-06's "Write it, or nothing, as the user
  chooses".
- Resolved (Bryan, 2026-10-04, version 11: "Two answers for reuse"): found by the skill review of SKL-003 v9, a
  reuse had nothing 'Write it with the outcome open' could write (reuse's review record sets outcome: reuse), so
  step 8 offers only Confirm reuse and Write nothing for it.
- Approved (Bryan, 2026-10-04): SKL-003 v9, its 3-run qualification waived; he accepted the end-of-workflow notes.
  Open, for later (from them): this skill's own Proceed description says "I ask nothing more" although BEH-01's
  and BEH-04's questions are still asked when open, the gap SPEC-001 version 15 closed for brainstorm; and reuse's
  two-answer step 8 (version 11) has not run live.
- Recorded for the next cycle (Bryan, 2026-10-04): a deliberate Write nothing should count as a finished run (or an
  ended session), not one stopped partway; with SPEC-013's next-cycle item, which has his words and his resume idea.
- Resolved (Bryan, 2026-10-03, with SPEC-012 version 5): tracked skills keep their checklist in the task list,
  and a question asked with no step in progress is refused in enforce mode; a skill whose runs don't keep the
  list is fixed through its spec (SPEC-012 §4).
- Resolved (decision D4, 2026-10-01): the description needs no "Not for…" clause. Bryan ran a
  near-miss trigger probe from a plain terminal (Claude Code 2.1.286, the plugin loaded with
  `--plugin-dir`, an empty folder). The skill didn't load for "monolith or microservices for my Flask
  app?", "how should I structure the backend of my side project?" or "draw the architecture of a
  typical e-commerce site", one run each. In the same session, the control prompt "define the
  architecture for PRD-001" did load it, so the plugin was loaded. §5 and the VER items are unchanged.
- Resolved: PRD-001 v8 records FR-013 as must/current, decided by Bryan on 2026-09-24.

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
| 3 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Record-only update, with no version bump: §9 records the 2026-09-29 architecture eval runs on SKL-003 v2 (component kinds). The re-test after PR #10 merged is bound to its commit and plugin digest (14/14 at 1.00); the earlier mixed-source run and an interrupted attempt are kept apart. No item changed | §9 |
| 4 | 2026-09-29 | claude-code (session fdbef416-eebb-4053-95ce-624a311d72d5) | Bryan's decision of 2026-09-29 on a failed supersession (ERR-05): when validation fails after an ADR accepted in the run superseded an existing ADR, the older ADR is restored byte-for-byte to its state before the run; the replacement is kept as proposed with approved_by, approved_on and supersedes cleared, its prose and Status history keeping the intended replacement and the user's decision; and the dependent DECs return to open with resolved_by [], never reconnected to the older ADR, with no readiness handoff. New VER-19, the regression case, is manual: a run with no user never supersedes an ADR (BEH-07, BEH-16). SPEC-004 and SPEC-009 relinked to version 4 (mechanical: the §4 and §5 they consume are unchanged). Awaiting Bryan's approval | ERR-05, VER-19, §9, §11, frontmatter, status |
| 4 | 2026-09-29 | Bryan | Approved | status |
| 4 | 2026-09-29 | claude-code (session fdbef416-eebb-4053-95ce-624a311d72d5) | Record-only update, with no version bump: §9 records SKL-003 v4's bound 3-run architecture eval (16 of 16 at 1.00) and the stopped SKL-003 v3 run, kept apart, and the manual runs: VER-19 pass, VER-12 (i) pass in the same run, VER-12 (f) by test; the other VER-12 items and VER-13 not run; and Bryan's approval of SKL-003 v4 on 2026-09-29. No item changed | §9 |
| 4 | 2026-09-30 | claude-code (session bd9e3bd9-6b79-4be2-b310-a8a29d143b92) | Record-only update, with no version bump: §9 records SKL-003 v5's bound requalification on its 3 policy cases (3 of 3 at 1.00), the NaN finding that PR #27 fixed after the run, and Bryan's approval of SKL-003 v5 on 2026-09-30. No item changed | §9 |
| 5 | 2026-10-01 | claude-code (session 388b2532-f519-4deb-b4ce-3e294d7e3b10) | Bryan's decisions of 2026-10-01 on the architecture skill review, and on issue #19. Deciding an existing question is an amendment: BEH-04 recommends amend when a user is present and a blocking DEC is open, BEH-08 makes the outcome amend whenever a DEC changes, and BEH-07 lets a later decision supersede a proposed ADR (D2; manual VER-20). Reuse is offered only for an ARCH that already links this PRD, and the reply names the requirements no DEC cites, which report ready (D3; VER-21, VER-22). A mandated platform counts only while it is the platform and capability the ARCH recorded; otherwise readiness reports its DEC open, reuse isn't offered, and an amendment reopens the DEC, logged in the Change Log row with both platforms, and it stays open until a user confirms the setting as it now stands, as for a superseded ADR (§4, BEH-04, BEH-07, BEH-09, BEH-11; VER-24, VER-25). SPEC-004's readiness check must follow this §4 rule. With no PRD at all the skill says so and points to /devforgeai:prd (BEH-01, ERR-01; VER-23). Bash may run scoped read-only commands, because Claude Code may provide no Glob or Grep tool (§5). Issue #19, Option A: the EVD item of a rolled-back supersession is kept and deprecated (ERR-05, VER-19). The two §9 runs stored in the plugin's evals/results/ moved to tmp/eval-results/. Unchanged by decision: D1 (a request that names an ADR while saying to proceed without questions leaves the DEC open, a skill-only clause) and D4 (the description stays: Bryan's trigger probe didn't load the skill on three near-miss prompts, §13). SPEC-009 and SPEC-011 relinked to version 5 (mechanical); SPEC-004's link moves with SPEC-004 v2. Awaiting Bryan's approval | §4, §5, BEH-01, BEH-04, BEH-07, BEH-08, BEH-09, BEH-11, ERR-01, ERR-05, VER-19 to VER-25, §9, §11, §13, frontmatter, status |
| 5 | 2026-10-01 | Bryan | Approved | status |
| 5 | 2026-10-01 | claude-code (session 388b2532-f519-4deb-b4ce-3e294d7e3b10) | Record-only update, with no version bump: §9 records SKL-003 v6's evaluation (the five new cases on v5 and on v6; one run 21 of 21 at 1.00; the 3-run qualification, 21 of 21 at 1.00, across two folders bound to one commit and digest), the manual VER-12 (a), (j), (k) and (l), VER-19 and VER-20 passes, and Bryan's approval of SKL-003 v6 on 2026-10-01. No item changed | §9 |
| 5 | 2026-10-01 | claude-code (session 388b2532-f519-4deb-b4ce-3e294d7e3b10) | Record-only update, with no version bump: §9 records SKL-003 v6's merge in PR #54 and deployment (plugin 0.10.0), and corrects the paths of the two 2026-09-29 runs, whose folders were renamed with an `arch-stray-` prefix when they were moved to `tmp/eval-results/`. No item changed | §9 |
| 6 | 2026-10-03 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | With SPEC-012 version 5's task-list convention (Bryan, 2026-10-03): BEH-17 keeps the workflow checklist in the session's task list, when it has one, with each question asked under its step and the outcome asked alone under step 8; new VER-26 (eval case keeps-task-list) and VER-27 (live); §5 lists the task tools; SPEC-012 link. Bryan's decision of 2026-10-03: BEH-08 confirms the outcome at step 8 once the change is known whenever the run writes to an existing ARCH, since step 4's choice picks only the direction (which also closes a gap in SPEC-012's outcome rule); new VER-28 (eval case confirms-amend-at-step-8); §13 | frontmatter, §1, §5, BEH-08, BEH-17, VER-26, VER-27, VER-28, §10, §11, §12, §13 |
| 6 | 2026-10-03 | Bryan | Approved, with step 8 confirming the outcome once the change is known (BEH-08) | status, BEH-08, §13 |
| 7 | 2026-10-03 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Bryan's decision of 2026-10-03 on a confirmation typed into the request: with a user present, step 8 asks even then, since it too comes before the change is known; a request to proceed without questions keeps it (BEH-08); new VER-29 (eval case request-confirm-still-asks); SPEC-012 link moved to version 7 | frontmatter, §1, BEH-08, VER-29, §10, §11, §13 |
| 7 | 2026-10-03 | Bryan | Approved | status |
| 8 | 2026-10-03 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | With SPEC-012 version 9 (Bryan, 2026-10-03): BEH-17 tags each question form with its step, AskUserQuestion's metadata source devforgeai_step:N, which the tracker checks against the step marked in progress, and each question's header 'Step N', which the user sees; VER-27 checks both live; SKL-003 v7 implements versions 6 to 8 and ships with SPEC-012 version 9 and SPEC-013 version 8; SPEC-012 link moved to version 9 | frontmatter, §1, BEH-17, VER-27, §10, §11, §13 |
| 8 | 2026-10-03 | Bryan | Approved, with the step shown in each question's header | status |
| 8 | 2026-10-03 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §13 records Bryan's acceptance of the tracker refusing an outcome named in a request to proceed without questions | §13 |
| 8 | 2026-10-03 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §13 records Bryan's choice that step 1 runs the policy script with no policy too, as a command of its own, so the progress tracker sees step 1's evidence; the result is unchanged, the mechanics now differ from the prd skill's | §13 |
| 8 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records SKL-003 v7's build, its single-arm evaluation before step 1's change, Bryan's waiver of the 3-run qualification, and the live VER-27 | §9 |
| 8 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records Bryan's approval of SKL-003 v7, and §13 his acceptance of the policy script's handling of a POL file with no readable status | §9, §13 |
| 8 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records plugin 0.18.0, set for the merge on Bryan's word | §9 |
| 8 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records PR #73's merge and the deploy of plugin 0.18.0 | §9 |
| 9 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Bryan's decisions of 2026-10-04: when the request says to proceed without questions, the skill asks the waiver once in step 1 after the policy script, with its own tag and two fixed labels, only with AskUserQuestion; after Proceed, step 8 writes the named outcome without asking and the tracker counts it (new BEH-18; BEH-08, VER-30, VER-31); status in-review | frontmatter, §1, BEH-08, BEH-18, VER-30, VER-31, §10, §11, §12, §13 |
| 9 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Before approval, the drafts review's fixes: the waiver is named as the one question the tag rule leaves out, and the questions BEH-01 and BEH-04 ask whatever the request says are cited | BEH-18 |
| 9 | 2026-10-04 | Bryan | Approved, with the waiver asked after the policy script and counted for step 8 | status |
| 9 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records the build, the tests, the evals and the live checks of version 9 | §9 |
| 9 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: Bryan approved SKL-003 v8 and waived its 3-run qualification; §13 records an open item from the build's review | §9, §13 |
| 9 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records PR #77's merge (`8eb431a`) and the deploy of plugin 0.20.0 | §9 |
| 10 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Bryan's decisions of 2026-10-04 (the waiver follow-ups): step 8 offers Confirm, Write it with the outcome open and Write nothing, which writes no file and stops (BEH-08); the waiver question doesn't count against interview.max_calls (BEH-18); a dismissed or typed waiver answer stays Ask me as usual; new VER-32 (live); status in-review | frontmatter, §1, BEH-08, BEH-18, VER-32, §10, §11, §13 |
| 10 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Before approval, the drafts review's fixes: step 8's typed answer and dismissal follow the existing rules, not new readings (BEH-08); steps 9 to 11 stay pending after Write nothing (BEH-17); VER-32's second run chooses amend and checks state.json | BEH-08, BEH-17, VER-32 |
| 10 | 2026-10-04 | Bryan | Approved | status |
| 11 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Found by the skill review of SKL-003 v9: for reuse, step 8 offers only 'Confirm reuse' and 'Write nothing' (BEH-08) | §1, BEH-08, §13 |
| 11 | 2026-10-04 | Bryan | Approved ('Two answers for reuse') | status |
| 11 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §13 records Bryan's decision for the next cycle that Write nothing counts as a finished run | §13 |
| 11 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records SKL-003 v9's build, evals and VER-32 | §9 |
| 11 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: Bryan approved SKL-003 v9 and waived its 3-run qualification; §13 records two items from the end-of-workflow notes | §13 |
| 11 | 2026-10-04 | claude-code (session a4f2ade8-0127-4b96-bc22-b3498b2ab3a9) | Record-only update, with no version bump: §9 records PR #83's merge (`ab8301c`) and the deploy of plugin 0.21.0 | §9 |
