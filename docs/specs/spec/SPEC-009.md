---
id: SPEC-009
type: spec
title: "Story skill (MVP)"
status: draft          # draft | in-review | approved | superseded | deprecated
version: 2
created: 2026-09-29
updated: 2026-09-29
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
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 10, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "stories follow epics; detailed feature design stays in specs"}
  - {id: ADR-004, relation: constrains, version: 2, hash: null, note: "accepted: the project context documents this skill reads"}
  - {id: PRD-001, item: FR-016, relation: informed_by, version: 10, hash: null, note: "the requirement this skill implements; no story specifies it yet"}
  - {id: SPEC-004, relation: informed_by, version: 1, hash: null, note: "consumes the epic skill's downstream contract (SPEC-004 §5)"}
  - {id: SPEC-003, relation: informed_by, version: 3, hash: null, note: "reads the ARCH's components (CMP) and deployment units (SPEC-003 §4, §5)"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/story"]
---

# SPEC-009 — Story skill (MVP)

> **Draft, from Bryan's decisions of 2026-09-29.** It builds on ADR-004 (project context documents,
> accepted 2026-09-29). It can't be built before the prerequisites in §11: the context templates, the
> component kind, and the story template and schema changes.

## 1. Overview

The `story` skill ships in the `devforgeai` plugin and is invoked as `/devforgeai:story EPIC-NNN`. The
epic skill's handoff already names that command (epic `SKILL.md`, "It exists" branch). The skill turns
one epic into story documents:
- it reads the epic, the PRD items the epic refines, the architecture description (ARCH) the epic
  relied on, and the project context documents (ADR-004), loading only what each story needs;
- it proposes **vertical slices**: stories that each deliver observable behaviour through every
  component they need;
- it writes the stories once the user confirms the slicing;
- it flags every story that needs a design before it can be `ready`;
- it hands off to the spec step.

Four rules shape everything else:
- **Stories are vertical slices** (Bryan, 2026-09-29). A story is "the unit of delivery" (story
  template). Front-end, middle-tier, back-end and database work for one behaviour belong to the same
  story. Its spec carries each layer's design, and the context documents carry each layer's
  conventions. The skill never writes one story per layer or per component.
- **Nothing the epic promises is lost.** Every requirement the epic refines, and every done-when (DW)
  item, is satisfied by at least one acceptance criterion (AC) across the epic's stories. Any gap is
  reported.
- **Design comes first for user-facing work** (Bryan, 2026-09-29). A story that needs a screen or a CLI
  flow can't become `ready` until its design is approved. The skill writes the `/design` brief and the
  marker, and the user runs `/design`.
- **The user decides the slicing.** The skill proposes it; the user confirms or changes it. Everything
  the skill can't confirm stays marked.

The skill is recorded as `SKL-008` in its `provenance.yaml`.

## 2. Constraints

- **PRD-001 NFR-001 to NFR-003:** a `SKILL.md` of at most 500 lines, spec-only frontmatter with
  provenance in the sidecar, and an eval suite (§9).
- **ADR-001:** built from `src/`, deployed with rsync by the owner, evaluated from a plain terminal.
- **ADR-002:** stories come after epics. Detailed feature design (API contracts, data structures,
  migrations) belongs in each story's spec, not in the story.
- **ADR-004:**
  - the project context documents in `docs/specs/context/`, read through `index.md`;
  - progressive disclosure: only the documents for the components a story touches;
  - read-only;
  - the ambiguities log as the pressure relief valve (ADR-004 D8).
- **SPEC-004 §5 (consumed):**
  - the epic path and stable `DW-NN` IDs, which stories cite with `satisfies` links;
  - the epic's `refines` links, which name the requirements its stories must satisfy;
  - the epic's single `informed_by` link to the ARCH, at the ARCH's version;
  - epics start as drafts.
- **SPEC-003 §4 and §5 (consumed):** CMP items (responsibility, owned data, interactions, deployment
  unit). The epic carries no CMP links (epic `references/output-rules.md`: one ARCH link, "No other
  link"), so the skill reads the ARCH itself. SPEC-003 §5 says epics cite CMP items, which contradicts
  the shipped epic skill. That is recorded as follow-up M8; this skill works whichever way it's settled.
- **Out of scope:**
  - writing specs, including embedded ones (the spec step does that);
  - resolving policy (PRD-001 FR-012 is `later`; SPEC-004 §2 is the precedent). The Definition of Done
    cites the testing policy without resolving it;
  - calling `/design`: no documented interface lets a skill drive Claude Design;
  - initializing git or creating source folders: the git skill's `connect` (SPEC-007 BEH-04) and the
    walking-skeleton story's delivery do that;
  - sprint planning and estimates the user didn't give;
  - editing any upstream document (BEH-18).

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/story/
├── SKILL.md                     # workflow checklist, slicing and coverage rules, output contract
├── provenance.yaml              # SKL-008, implements SPEC-009
├── assets/
│   ├── story.md                 # THE story template (moved from src/templates/)
│   └── design-brief.md          # the /design brief template (BEH-11)
└── references/
    ├── slicing.md               # vertical slicing patterns, the walking-skeleton rule, spec_mode criteria
    ├── context.md               # which context documents to open for which component kinds (ADR-004 D2, D4)
    └── output-rules.md          # story frontmatter, links, AC rules, Definition of Done, the self-check list
src/claude/DevForgeAI/evals/story/<case>/   # one case per automated VER item (§9)
```

```mermaid
flowchart LR
    E[Select epic BEH-01] --> R[Read epic and PRD items BEH-02]
    R --> A[Read the ARCH BEH-03]
    A --> C[Read context index, then only what applies BEH-04]
    C --> X[Existing stories and coverage BEH-05]
    X --> G[Greenfield check BEH-06]
    G --> S[Propose vertical slices, confirm BEH-07]
    S --> W[Write stories BEH-08 BEH-10 BEH-13 BEH-15]
    W --> D[Design gate BEH-11]
    D --> V[Validate BEH-16]
    V --> H[Coverage report and handoff BEH-09 BEH-17]
```

## 4. Data model

**Inputs** (all read-only):
- `docs/specs/epic/EPIC-NNN.md`: the `refines` links (requirements at the PRD version), the DW items, the
  ARCH link and the status;
- the PRD at the version the epic links: each refined FR or NFR's statement, priority and release;
- the ARCH the epic links: CMP items with their `kinds` (SPEC-003 §4), DEC state, deployment;
- accepted ADRs the ARCH or the context documents cite, when a story needs the decision's detail;
- the context documents (ADR-004): `docs/specs/context/index.md` first, then only the documents BEH-04
  selects;
- existing stories: `docs/specs/story/STORY-*.md`;
- approved design exports under `docs/specs/story/design/STORY-NNN/`.

**Outputs:**
- new stories at `docs/specs/story/STORY-NNN.md` from `assets/story.md`, valid against
  `story.schema.json`;
- for a story that needs a design, a brief at `docs/specs/story/design/STORY-NNN/brief.md`;
- entries in the ambiguities log of the story concerned (ADR-004 D8), when BEH-14 allows one.

**Coverage.** An item the epic promises is **covered** when an existing, non-cancelled story that refines
this epic has an AC with a `satisfies` link to it, at any version. The items are each refined FR, each
refined NFR and each DW item. The skill writes new stories only for uncovered items, so rerunning with
unchanged inputs writes nothing (ERR-05).

**Story forms** (story template §1):
- **User story:** "As a <role>, I want <capability>, so that <benefit>." Most stories use it.
- **Enabler story:** "To enable <capability>, <component> needs <change>, because <reason>." Used for
  work that no user sees but a user story needs, such as the walking skeleton.

**The walking skeleton.** An established practice (Alistair Cockburn): the first story of a greenfield
project delivers the thinnest end-to-end path through each deployment unit it needs, with the build, the
test harness and CI in place. It creates the source tree that `source-tree.md` describes.
- Its title starts with `Walking skeleton:` so later runs can find it.
- Other stories of that project list it in `blocked_by`.
- A project is **greenfield** when none of the code roots `source-tree.md` names exists yet. The check
  lists only those roots, never the whole repository.

**`spec_mode`.**
- `embedded` is proposed only when all of these hold:
  - the story touches one component;
  - it changes no data model;
  - it adds or changes no interface;
  - it has at most three ACs;
  - it needs no design.
- Every other story is `separate`. The user confirms the proposal with the slicing.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: story
description: Turns a DevForgeAI epic into story documents, proposing vertical slices that each deliver observable behaviour through every component they need, with acceptance criteria that cover every requirement and done-when item of the epic. It reads the architecture description and the project context documents, flags stories that need a design first, and writes the stories once the user confirms. Use after the epic step, when splitting an epic into stories or planning delivery work.
argument-hint: "EPIC-NNN"
metadata:
  devforgeai-id: "SKL-008"
  devforgeai-version: "<SKL-008's provenance.yaml version, quoted>"
```

- **The name must be exactly `story`.** The epic skill's handoff looks for it next to itself.
- **The version isn't fixed here.** `metadata.devforgeai-version` must equal `provenance.yaml`'s `version`,
  so a skill fix bumps the skill, not this spec.
- **Arguments:** `$ARGUMENTS` is one epic ID (`EPIC-NNN`) or empty (BEH-01). File paths aren't accepted.
- **Tools:**
  - reading: Read, plus Glob and Grep when available; otherwise `ls` and `cat`, read-only, on
    `docs/specs/` and on the code roots named in `source-tree.md`;
  - writing: Write for new stories and briefs, and Edit only on stories written in this run and for
    BEH-12's design record;
  - AskUserQuestion, with at most 4 questions per call;
  - no other shell command, and no code inspection beyond the root check.
- **The story document** (template and schema changes M7, which must land before the build):
  - `upstream` holds exactly one `refines` link to the epic, at the epic's version, plus `constrains`
    links to the context documents and ADRs the story relies on, at their versions. This settles the
    template's conflict between "exactly one parent epic" and embedded `constrains` links;
  - an optional `components:` list of `ARCH-NNN#CMP-NN` IDs, with the details in §3 Scope (Bryan,
    2026-09-29);
  - `spec_mode`, `blocked_by` and `estimate` as in the template.
- **Downstream contract (consumed by the spec step):**
  - the story path and stable `AC-NN` IDs;
  - the epic `refines` link, and each AC's `satisfies` links;
  - `components:`, which the spec's `components` and §3 detail;
  - `spec_mode`. `separate`: a SPEC cites the story with `specifies`. `embedded`: the spec step fills the
    story's §5;
  - approved design paths, which become the spec's UI contract;
  - the Claude Design handoff-bundle link, when one was recorded, which dev uses when it implements
    (the dev skill comes later, M12);
  - the `constrains` links to context documents, which the spec obeys;
  - `blocked_by` order;
  - stories start as `draft`. Only the user moves one to `ready`, and not while any marker remains
    (templates README).
- **Delivery contract (consumed later):**
  - story IDs name the branches (SPEC-007 BEH-05: `story/STORY-NNN-<slug>`) and appear in commits
    (SPEC-007 BEH-10) and in the PR body (SPEC-007 BEH-12);
  - QA's verdict names them in its Scope line (SPEC-008 §4).

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Take the epic from $ARGUMENTS (EPIC-NNN). With no argument, list the epics in docs/specs/epic/ that still have uncovered items (§4), with their titles, status and the number of uncovered items, and ask. Never take a file path."
  - id: BEH-02
    status: active
    rule: "Read the epic's refines links, DW items, ARCH link and status, and the PRD items it refines at the linked version. If the epic, the PRD, the ARCH or a context document it relies on is a draft, say in the handoff and in each story's section 2 that the stories are proposals because an input is a draft. Never edit an input."
  - id: BEH-03
    status: active
    rule: "Read the ARCH that the epic's informed_by link names: its components (responsibility, kinds, owned data, interactions and deployment unit) and the state of the decisions that cite the epic's requirements. When the ARCH's version is newer than the epic's link, apply ERR-03. When the ARCH gives no kinds for a component a story needs, as in an ARCH written before SPEC-003 version 2, ask the user which kinds it has (ERR-08)."
  - id: BEH-04
    status: active
    rule: "Read docs/specs/context/index.md first. For each story being proposed, open only the context documents for the kinds of the components it touches, plus tech-stack.md, source-tree.md and testing.md when the story needs them, following references/context.md. Open a detail file only when its one-line description in the parent document applies to the story. Never open every context document by default. Record each context document a story relies on as a constrains link at its version."
  - id: BEH-05
    status: active
    rule: "Read every existing story whose upstream refines this epic, and compute coverage (§4): which refined FRs and NFRs and which DW items an AC already satisfies. Never modify, renumber or duplicate an existing story, except for the design record in BEH-12."
  - id: BEH-06
    status: active
    rule: "Check whether the project is greenfield (§4) by listing only the code roots that source-tree.md names. If it is, and no story in docs/specs/story/ has a title starting 'Walking skeleton:', propose a walking-skeleton enabler story first: the thinnest end-to-end path through each deployment unit the epic's first slice needs, with ACs for a clean build, one end-to-end request through those components, a running test harness with at least one passing test per deployment unit, and CI running the build and tests. Every other story proposed in this run lists it in blocked_by."
  - id: BEH-07
    status: active
    rule: "Propose vertical slices for the uncovered items with the patterns in references/slicing.md (paths, interfaces, data, rules, and a spike when an unknown blocks estimation). Each story delivers observable behaviour (user form) or a necessary enabler (enabler form). Never propose one story per layer, component or team; when the request asks for layer stories, explain why they are sliced vertically and propose vertical slices. For each proposed story show its title, form, the items its ACs will satisfy, its components, the proposed spec_mode, whether it needs a design, and blocked_by. Ask the user to confirm or change the slicing, and write nothing until they do. A slicing stated in the request counts as confirmed. If no one can confirm (the request says to proceed without questions and gives no slicing), write the proposal and add to section 7 of each story: [NEEDS CLARIFICATION: slicing proposed by the skill; not confirmed by the user]."
  - id: BEH-08
    status: active
    rule: "Write ACs that are observable and testable, with given, when and then as lists. Each story covers its happy path, its key edge cases and at least one failure path. Every AC has at least one satisfies link: to an FR or NFR at the PRD version the epic links, or to a DW item at the epic's version. Never write an AC that no refined item or DW supports: behaviour the skill thinks is missing becomes an open question in section 7, not an AC."
  - id: BEH-09
    status: active
    rule: "After the slicing is confirmed, check that every refined FR, every refined NFR and every DW item is covered by at least one AC across the epic's existing and new stories. Report each uncovered item as a gap in the handoff, with the reason (the user deferred it, or no confirmed slice covers it) and its next action. Never add an AC without the user's confirmation just to close a gap."
  - id: BEH-10
    status: active
    rule: "Write each confirmed story to the next free docs/specs/story/STORY-NNN.md, creating the folder if it is missing, from ${CLAUDE_SKILL_DIR}/assets/story.md. Number the walking skeleton first, then the rest in the confirmed order. Frontmatter: status draft; estimate null unless the user gave one; spec_mode as confirmed; components as ARCH-NNN#CMP-NN IDs; blocked_by as confirmed; upstream with one refines link to the epic at its version and constrains links to the context documents and ADRs the story relies on (BEH-04). Fill sections 1 to 4 and 6 to 7. In section 3 Scope, name each component with what the story changes in it. Section 5 keeps the template's GENERATED line when spec_mode is separate; when it is embedded, section 5 says the spec step writes the embedded specification."
  - id: BEH-11
    status: active
    rule: "Design gate. For a story that touches a user-facing component (web, desktop, mobile or CLI) and whose ACs describe a screen, flow or output that no approved design covers (neither one indexed in docs/specs/context/ui-mockups.md nor one recorded in an existing story under BEH-12): write a brief to docs/specs/story/design/STORY-NNN/brief.md from ${CLAUDE_SKILL_DIR}/assets/design-brief.md (the goal, the users, the flows and states to show, the ACs it illustrates, and the constraints from front-end.md and the design system), and add to section 7 [NEEDS CLARIFICATION: approved design for <screen or flow>; brief at <path>]. The marker keeps the story from becoming ready. Never call /design, and never describe a design as approved."
  - id: BEH-12
    status: active
    rule: "Design record. When run again for an epic, and a story's design folder holds an exported PNG or PDF that the user confirms in this run as approved: add to section 3 the export's path, the approval date and, when the user gives it, the link to the design's Claude Design handoff bundle; remove that design marker; raise the story's version by one, update the date and add one Change Log row. Say in the handoff that the context step indexes the design in ui-mockups.md on its next run. This is the only change the skill makes to an existing story. Without the user's confirmation it changes nothing."
  - id: BEH-13
    status: active
    rule: "Write the Definition of Done from the template and add, as they apply: 'Required tests pass 100%, or each failure is a named, approved exception; coverage meets the testing policy (testing.md and the policy settings it cites)'; for a story with a design, 'The implementation matches the approved design at <path>'; and 'The ambiguities log entries for this story are reviewed'. Never state a policy value that the story skill did not read from a document; cite the document."
  - id: BEH-14
    status: active
    rule: "Record in the ambiguities log of the story the choice concerns (ADR-004 D8: docs/specs/ambiguities/AMB-NNN.md with that story in work_item, created when the story has none and reused across sessions), and continue, only a small choice that changes no AC, scope, component, interface or permission: for example, a context document that is silent about a convention the story only mentions (such as the test folder for a new component). Name the context document the entry is for. Ask, never log, about anything the user decides: the slicing, an AC's behaviour, a component's kind, a design, a spec_mode or blocked_by. Logging never authorizes contradicting a spec or an input."
  - id: BEH-15
    status: active
    rule: "Fill provenance on every story written: generated_by with the tool, model and session; authors; reviewed_by empty; every hash null; today's dates; approved_by empty. Delete every template author comment."
  - id: BEH-16
    status: active
    rule: "Validate every story written against the self-check list in references/output-rules.md, reading each file back. Fix and check again, at most three attempts. Never run a devforgeai command."
  - id: BEH-17
    status: active
    rule: "Hand off with each story written (path, title, form, components, spec_mode, design needed, blocked_by), the coverage report with every gap and its reason (BEH-09), the context documents opened, the ambiguities logged, and the proposal warning if an input is a draft. Then name the next step, the spec step, with the story IDs in blocked_by order: if ${CLAUDE_SKILL_DIR}/../spec/SKILL.md exists, tell the user to run /devforgeai:spec with a story ID; otherwise say specs are written by hand from the spec template for now and that, once the spec skill (planned as /devforgeai:spec) is built, it runs with a story ID. Name the stories that wait for a design, and say /design is run with their brief first. The next step comes last in the final reply, as its own paragraph outside any code block, starting with the words Next step; nothing follows it. Never start the spec step."
  - id: BEH-18
    status: active
    rule: "Never modify a PRD, BRN, ARCH, ADR, policy document, context document or epic; never write a spec; never resolve policy; never call /design; never run git or create source folders."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The epic ID given does not exist"
    handling: "List the available epics with titles and status, and write nothing"
    user_result: "The list of epics"
  - id: ERR-02
    status: active
    condition: "The epic has no ARCH link, or the ARCH it links doesn't exist"
    handling: "Write nothing. Say that stories need the architecture description, and tell the user to run /devforgeai:architecture with the epic's PRD ID first"
    user_result: "A handback to the architecture step; no story written"
  - id: ERR-03
    status: active
    condition: "The ARCH's version is newer than the version the epic links"
    handling: "Say the epic's architecture link is suspect, name both versions and the components the epic's requirements depend on, and ask whether to slice against the current ARCH. With no confirmation, write nothing"
    user_result: "A question; no story written without confirmation"
  - id: ERR-04
    status: active
    condition: "docs/specs/context/index.md is missing, or a context document it lists that a story needs is missing"
    handling: "Write nothing. Say which context document is missing, and tell the user that the context step writes the project context documents (ADR-004), naming /devforgeai:context when that skill exists"
    user_result: "A handback to the context step; no story written"
  - id: ERR-05
    status: active
    condition: "Nothing to write: every refined FR and NFR and every DW item is already covered by an existing story (for example, a rerun with unchanged inputs)"
    handling: "Write nothing, say that no item needs a new story, and report the coverage"
    user_result: "The coverage report; no story written"
  - id: ERR-06
    status: active
    condition: "Validation still fails after three fix attempts"
    handling: "Stop. Keep the stories written as draft, report the file paths and the unresolved errors, and don't present them as ready for the spec step"
    user_result: "A validation-failure report"
  - id: ERR-07
    status: active
    condition: "The user stops before confirming the slicing"
    handling: "Write nothing, and say how to resume: run the skill again with the epic ID"
    user_result: "No story written"
  - id: ERR-08
    status: active
    condition: "The ARCH gives no kinds for a component a proposed story touches (an ARCH written before SPEC-003 version 2), so the skill can't tell which context documents apply"
    handling: "Ask which kinds the component has (user-interface, service, platform, api, relational-store, data-store or external), use the answer for this run only, and say in the handoff that the ARCH should record them when it is next amended"
    user_result: "A question; the answer applies to this run"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the slicing, coverage and design rules and the output contract; slicing patterns, context selection and output rules live in references/"
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
    response: "One eval case per automated VER item, tagged story and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 10, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: frontmatter and item blocks against `spec.schema.json` | See the Change Log row for the check at drafting |
| Behavioural: automated VER items, one eval case each | Not run: the skill isn't built |
| Behavioural: manual VER items (VER-16, VER-17) | Not run |

**Shared fixture.** Nothing upstream exists in this repository, so each case's scaffold seeds its own
documents, each checked against its schema:
- a PRD with FR-001 to FR-003 and NFR-001;
- an ARCH with three components: a CLI (user-facing), a service, and a relational store;
- EPIC-001, which refines FR-001 to FR-003 and NFR-001, with DW-01 and DW-02, and links the ARCH;
- the context documents `index.md`, `architecture.md`, `tech-stack.md`, `source-tree.md`, `testing.md`,
  `front-end.md`, `middle-tier.md` and `rdbms.md`.

Unless a case says otherwise, the code roots in `source-tree.md` exist (not greenfield), and the prompt
states the slicing, so the run is non-interactive and confirmed.

No story specifies this skill, so the VER items have no `upstream` link. `spec.schema.json` requires one
only in a spec that specifies a story.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture; the prompt states a two-story slicing. docs/specs/story/STORY-001.md and STORY-002.md exist, each refines EPIC-001 at its version, each AC has at least one satisfies link to FR-001, FR-002, FR-003, NFR-001, DW-01 or DW-02, and each story's components lists ARCH CMP IDs. Eval case writes-stories: file_exists and regex on the files."
    level: e2e
    covers:
      - BEH-02
      - BEH-03
      - BEH-08
      - BEH-10
      - BEH-15
      - BEH-16
  - id: VER-02
    status: active
    obligation: "In VER-01's run, the ACs across the two stories satisfy every one of FR-001, FR-002, FR-003, NFR-001, DW-01 and DW-02, and the reply's coverage report lists no gap. Eval case covers-every-item: regex on the files and last_message."
    level: e2e
    covers:
      - BEH-09
  - id: VER-03
    status: active
    obligation: "Shared fixture; the prompt asks for one story for the CLI, one for the service and one for the database, and to proceed without questions. No story's components holds only one layer's component while its ACs describe behaviour needing others; the reply explains vertical slicing; each story carries the unconfirmed-slicing marker. Eval case vertical-not-layered: llm on last_message and the files, regex for the marker."
    level: e2e
    covers:
      - BEH-07
  - id: VER-04
    status: active
    obligation: "Shared fixture with the code roots in source-tree.md absent and no existing story. STORY-001.md has a title starting 'Walking skeleton:' in the enabler form, with ACs for a clean build, an end-to-end request, a passing test per deployment unit and CI; every other story written lists STORY-001 in blocked_by. Eval case walking-skeleton-first: regex on the files."
    level: e2e
    covers:
      - BEH-06
  - id: VER-05
    status: active
    obligation: "In VER-01's setup (code roots present), no story written has a title starting 'Walking skeleton:'. Eval case no-skeleton-when-code-exists: regex not_contains on the files."
    level: e2e
    covers:
      - BEH-06
  - id: VER-06
    status: active
    obligation: "Shared fixture; the slicing gives one story a new CLI output that ui-mockups.md doesn't list. That story has a brief at docs/specs/story/design/STORY-NNN/brief.md, a [NEEDS CLARIFICATION: approved design …] marker in section 7 and status draft; the reply says /design is run with the brief first and doesn't call the design approved. Eval case design-gate: file_exists and regex on the files and last_message."
    level: e2e
    covers:
      - BEH-11
      - BEH-17
  - id: VER-07
    status: active
    obligation: "An existing STORY-001.md (version 1) with a design marker, and an exported design.png in its design folder; the prompt says the user approves that design. STORY-001.md is at version 2, section 3 names the export's path, the design marker is gone, and the Change Log has one new row; no other story file changed. Eval case design-record: regex on the file."
    level: e2e
    covers:
      - BEH-12
  - id: VER-08
    status: active
    obligation: "Shared fixture; the slicing gives one story that touches only the CLI component. Its frontmatter has constrains links to front-end.md and to no rdbms.md or middle-tier.md, and the run's trace shows no Read of rdbms.md. Eval case context-progressive-loading: regex on the file. The trace check is manual (kept with --keep-temp): no shipped grader checks Read calls."
    level: e2e
    covers:
      - BEH-04
  - id: VER-09
    status: active
    obligation: "The shared fixture without docs/specs/context/: no story is written, and the reply names the context step. Eval case no-context-hands-back: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-04
  - id: VER-10
    status: active
    obligation: "The shared PRD and EPIC-001 with no ARCH file: no story is written, and the reply tells the user to run /devforgeai:architecture first. Eval case no-arch-hands-back: file_exists false and regex on last_message."
    level: e2e
    covers:
      - ERR-02
  - id: VER-11
    status: active
    obligation: "The shared fixture plus existing stories (each version 1 with a unique sentinel line) whose ACs already satisfy every refined item and DW. No new story file is written, the existing files are unchanged, and the reply says no item needs a new story. Eval case rerun-writes-nothing: file_exists false, regex on the files and last_message."
    level: e2e
    covers:
      - BEH-05
      - ERR-05
  - id: VER-12
    status: active
    obligation: "Shared fixture; the prompt says to proceed without questions and gives no slicing. At least one story exists, with status draft and the unconfirmed-slicing marker in section 7. Eval case unconfirmed-slicing: regex on the file."
    level: e2e
    covers:
      - BEH-07
  - id: VER-13
    status: active
    obligation: "In VER-01's run, each story has non-empty generated_by tool, model and session, reviewed_by empty, every hash null, status draft, approved_by empty, estimate null, and a Definition of Done that cites testing.md. Eval case records-provenance: regex on the files."
    level: e2e
    covers:
      - BEH-13
      - BEH-15
  - id: VER-14
    status: active
    obligation: "In VER-01's run, the final reply ends with the handoff to the spec step: the last paragraph, outside any code block, starts with Next step and nothing follows it; it names the story IDs; without a spec skill it says specs are written by hand for now and names the planned /devforgeai:spec with a story ID; no file is written under docs/specs/spec/. The graders read the reply, never whether the spec skill exists. Eval case hands-off-to-spec: regex on last_message and file_exists false."
    level: e2e
    covers:
      - BEH-17
      - BEH-18
  - id: VER-15
    status: active
    obligation: "A request such as 'tell me a story about a dragon' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
  - id: VER-16
    status: active
    obligation: "Manual, interactive, one fixture copy per check: (a) the skill proposes a slicing, the user changes it, and the stories written follow the change; (b) an unknown epic ID lists the available epics and writes nothing; (c) an ARCH newer than the epic's link asks before writing (ERR-03); (d) an ARCH without component kinds asks for the kind (ERR-08); (e) stopping before confirming writes nothing; (f) spec_mode: a one-component, three-AC change with no data, interface or design change is proposed embedded, and a multi-component story separate; (g) SKILL.md is within the NFR-001 limits and metadata.devforgeai-version equals provenance.yaml's version; (h) by reading only: SKILL.md states the three-attempt limit and the ERR-06 report."
    level: manual
    covers:
      - BEH-01
      - BEH-07
      - ERR-01
      - ERR-03
      - ERR-06
      - ERR-07
      - ERR-08
      - QR-01
  - id: VER-17
    status: active
    obligation: "Manual: in a run where source-tree.md names no test folder for a component a story touches, the skill writes the story, records one ambiguities-log entry naming source-tree.md, and doesn't ask; in the same run it still asks the user to confirm the slicing. A brief written under VER-06 is usable as-is with /design, checked by running /design with it."
    level: manual
    covers:
      - BEH-14
      - BEH-11
```

## 10. Rollout, migration and rollback

The skill is new; removing its directory rolls it back. It moves `src/templates/story.md` into
`skills/story/assets/`, and needs the story template and schema changes (M7): the `components:` field,
and the `upstream` rule in §5.
- The epic skill needs no change. Its handoff already names `/devforgeai:story EPIC-NNN`, and its
  `hands-off-to-story` grader accepts both branches.
- When this skill ships, nothing else's eval case needs flipping. No other skill's handoff names the
  story step.

## 11. Implementation plan

**Prerequisites, before the build. Each needs Bryan's yes; the TASKS.md numbers are given:**
- ADR-004 accepted (M1);
- context templates (M2);
- component kinds in the ARCH (M4): specified in SPEC-003 version 2 and written by the architecture skill from SKL-003 version 2; ERR-08 covers older ARCH files;
- story template and schema changes (M7);
- the design-brief format and the approved-export location (M9);
- the ambiguities template's schema (the `AMB` and `ENT` prefixes, M13);
- PRD-001 FR-016 names this skill (M6, done in PRD-001 version 10).

**Build steps:**
1. Create a worktree for the story skill's story, following ADR-001.
2. `git mv src/templates/story.md` into `skills/story/assets/`, update the templates README row, and add
   `assets/design-brief.md`.
3. Write `references/slicing.md`, `references/context.md` and `references/output-rules.md` from §4,
   BEH-04 to BEH-14 and the story schema.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-008 implementing SPEC-009.
5. Write the shared fixture and the case variants, checking each file against its schema. Then write the
   eval cases for VER-01 to VER-15.
6. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Do VER-16 and VER-17
   by hand.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| One story per layer (front end, middle tier, database) | No such story is observable alone, and its ACs are only proven when every layer is done. Bryan chose vertical slices (2026-09-29), matching the epic skill's "never group by layer" |
| One story per epic (SDF2's practice) | It worked for skills built one at a time, but a product epic is too large to specify, build and review as one PR |
| One story per ARCH component | The same problem as layers, and it couples delivery to the component list |
| The story skill writes the spec too, always embedded | Mixes what with how. Embedded is for small changes only (story template) |
| The story skill calls `/design` | No documented interface lets a skill drive Claude Design; the user runs it with the brief |
| The story skill resolves the testing policy | PRD-001 FR-012 is `later`. The spec, dev and QA steps apply the testing values; the story cites them |
| Read every context document every run | Past a certain length Claude doesn't follow content reliably (ADR-004 D4). The index plus relevant documents stay small |

## 13. Open questions

- Resolved (Bryan, 2026-09-29): components record `kinds` in the ARCH (SPEC-003 version 2), and ADR-004 version 2 D2 maps them to context documents.
- [NEEDS CLARIFICATION: whether refined NFRs must each be satisfied by a story AC, or may instead be met through a spec's quality responses (QR items)]
- [NEEDS CLARIFICATION: how a later run finds the walking skeleton: the title prefix proposed in §4, or a frontmatter field]
- [NEEDS CLARIFICATION: where approved design exports live (proposed docs/specs/story/design/STORY-NNN/) and the brief's format (M9)]
- Resolved (Bryan, 2026-09-29): each story's ambiguities log is docs/specs/ambiguities/AMB-NNN.md, with the story in `work_item`, reused across sessions (ADR-004 D8).
- [NEEDS CLARIFICATION: whether a story must be approved before the spec step runs on it]

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Initial draft from Bryan's decisions of 2026-09-29: vertical slices, design first for user-facing work, components in the frontmatter, context documents per ADR-004 (proposed), testing values cited, not resolved, and the ambiguities log. Revised after an independent review the same day: the design gate also counts designs recorded in stories, BEH-12 records the handoff-bundle link, the downstream contract names it, the SPEC-003 §5 contradiction is noted (M8), and VER-08's trace check is manual. Awaiting Bryan's review; it can't be approved before ADR-004 is accepted | all |
| 1 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | ADR-004 accepted by Bryan: its link is now constrains, blocked_by is empty, and the "(proposed)" labels are removed. No item changed | frontmatter, §2 |
| 2 | 2026-09-29 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Aligned with Bryan's decisions of 2026-09-29: component kinds from SPEC-003 version 2 (BEH-03, §4; ERR-08 kept for ARCH files written before it); the ambiguities log per story (BEH-14, §4, §13); PRD-001 FR-016 names this skill (informed_by link); §11 and §13 updated. Links re-reviewed: PRD-001 v10, ADR-004 v2, SPEC-003 v2 | frontmatter, §4, BEH-03, BEH-14, ERR-08, §11, §13 |
