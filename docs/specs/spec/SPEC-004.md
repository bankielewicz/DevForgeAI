---
id: SPEC-004
type: spec
title: "Epic skill (MVP)"
status: approved
version: 4
created: 2026-09-24
updated: 2026-10-01
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "96018bc1-5ee7-423f-93a4-da37a8b6c392"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-10-01
upstream:
  - {id: STORY-005, relation: specifies, version: 2, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 10, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: epics come after the Architecture Definition step"}
  - {id: ADR-003, relation: informed_by, version: 2, hash: null, note: "A5: policy links carry the policy version, and the resolution line records each applied mandated platform (§4, bounded check)"}
  - {id: SPEC-003, relation: informed_by, version: 5, hash: null, note: "consumes the readiness rule (§4: a changed mandated platform reopens its question; the older-format record), which the bounded policy check tightens, and the downstream contract (§5). SPEC-003 v5 is approved but not yet on main: SKL-004 v4 is implemented only after it merges"}
  - {id: SPEC-002, relation: informed_by, version: 4, hash: null, note: "priority and release semantics, where null is undecided, and a later requirement's null priority (§5, BEH-05); re-read for version 2"}
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
  description, the ADRs' current status and the policy settings the ARCH applied (SPEC-003 §4, with the
  bounded policy check in §4), never from any skill's reply.
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
- **SPEC-003 v5 §4 and §5 (consumed):** the ARCH path, stable DEC IDs, the decision-specific readiness
  rule, and "epics may be written only for requirements that the readiness rule reports ready". SPEC-003 v5
  §4 counts an approved policy's active setting only while it still mandates the platform, for the
  capability, that the ARCH recorded for it: a changed mandate returns its question to open, and a record
  in the older format (no platform) is resolved by asking a user if one is present, and otherwise still
  counts. The bounded check in §4 follows that rule and keeps its own conditions (approved document,
  active mandate, an ARCH link, no contested mandate), because an epic must not rest on a mandate that
  another policy contests or that the ARCH never recorded.
- **SPEC-002 §5 (consumed):** PRD paths and stable IDs; `priority` (MoSCoW) and `release` (current or
  later) are independent, and `null` is undecided; `[NEEDS ADR]` markers; the PRD's `target_release`. A
  `later` requirement has `priority: null` by design (SPEC-002 BEH-05), so that null isn't undecided (§4).
- **ADR-003 A5 (consumed):** an ARCH records each applied policy setting as a link carrying the policy
  version, and each Change Log row's resolution line records every applied mandated platform as
  `architecture.mandated_platforms=<platform> for <capability> (POL-NNN#SET-NN)`; older ARCHs wrote
  `architecture.mandated_platforms=POL-NNN#SET-NN`, with no platform. A policy version newer than the link
  marks the link suspect; no skill relinks it.
- **Out of scope:**
  - writing stories, sprint planning, and modifying existing epics;
  - organizational policy resolution: PRD-001 FR-006 to FR-008 cover only prd and Architecture Definition,
    and FR-012 (release later) covers the rest. This skill doesn't resolve policy (no R1–R5, and it writes
    no resolution line) and copies neither `policy.md` nor `defaults.md`. It reads `docs/specs/policy/`
    only for the bounded resolver check in §4, and an ARCH's resolution line only for that check's
    check 3;
  - relinking policy links, or reopening a DEC when its mandated platform changes: that is the
    architecture step's (SPEC-003 v5). This skill only reports such a requirement blocked;
  - the `devforgeai check` CLI branch. The CLI doesn't exist, and anything named `devforgeai` on PATH
    can't be trusted by name. The skill validates with its own self-check list.

## 3. Architecture and components

```
src/claude/DevForgeAI/skills/epic/
├── SKILL.md                     # workflow checklist, selection and grouping rules, output contract
├── provenance.yaml              # SKL-004, implements SPEC-004
├── assets/
│   └── epic.md                  # THE epic template (moved from src/templates/)
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

**The current ARCH.** The skill uses the ARCH whose frontmatter `upstream` links cite this PRD, ignoring an
ARCH whose `status` is `superseded` or `deprecated`. It is **current** when that link's `version` equals
the PRD's `version`; a link version that differs, whether older or (after a hand edit) newer, is ERR-03.
The architecture skill records that link
when it creates or amends an ARCH and when the user confirms reuse against a
newer PRD version: a **review record**. The frontmatter PRD link moves to the reviewed version, `outcome`
becomes `reuse`, and one Change Log row is added; the ARCH's `version`, `status`, approval fields and every
item stay byte-identical. A second review against the same PRD version writes nothing. A version mismatch means a review is
due, not that the architecture must change. No such ARCH, or one not reviewed against the PRD's current
version, means the skill writes nothing and hands back to `/devforgeai:architecture PRD-NNN` (ERR-02, ERR-03).

**Readiness** (`references/selection.md`): SPEC-003 §4 applied to the ARCH file, with the bounded policy
check below for policy resolvers. A requirement R is **ready** when, for every active `DEC` with
`blocking: true` whose `upstream` cites R:
- `state` is `resolved`, and
- every `resolved_by` entry is an ADR whose file now has `status: accepted` and no `superseded_by`, or a
  policy setting that passes the bounded resolver check below.

The DEC's `state` is read first: an open DEC blocks R whatever its policy record says. This matters after
the architecture step reopens a DEC whose mandated platform changed: the ARCH's last resolution line then
records the new platform while the component's policy link keeps the old version, so check 3 alone would
pass (SPEC-003 v5).

A DEC **cites** R when its `upstream` has a link whose `id` is this PRD's ID and whose `item` is R. A link
to another PRD's item with the same number doesn't count: an amended ARCH can cover several PRDs. A DEC
blocks only the requirements its own `upstream` cites. Every PRD `[NEEDS ADR]` marker needs **its own
matching DEC**: one whose question answers the marker's decision and whose `upstream` cites every
requirement the marker names. A matching DEC answers the marker once it is resolved by an ADR that counts
or by a policy setting that passes the bounded check below. A mandated platform settles a decision as
much as an ADR does (SPEC-003 BEH-07), although SPEC-002 §5 names only an ADR. Only a DEC whose question
answers the marker's decision counts: neither a policy setting that resolves a different question nor the
resolution of another question clears the marker, even when that DEC cites the same requirement. When no
DEC clearly answers a marker, every requirement it names is blocked
("marker without a matching question"), even if other DECs citing them are resolved. When readiness can't
be established, R is `unknown`: never asserted ready or blocked. For example: a resolving ADR's file is
missing, a resolved DEC has an empty `resolved_by`, or a policy resolver fails the bounded check.

**Policy resolvers: a bounded check, not policy resolution.** A `POL-NNN#SET-NN` resolver counts only when
all four hold:
1. **Approved:** `docs/specs/policy/POL-NNN.md` exists and has `status: approved`.
2. **Active mandate:** setting `SET-NN` in it has `status: active` and `key: architecture.mandated_platforms`,
   the only kind of setting that resolves a DEC (SPEC-003 BEH-07).
3. **Still the mandate the ARCH recorded.** The ARCH has a link to the setting (`id: POL-NNN`,
   `item: SET-NN`; ADR-003 A5); with no link, R is `unknown`. If the link's `version` equals the policy
   document's `version`, the setting is unchanged and check 3 passes with nothing more read: a policy
   version bump alone never blocks R. Otherwise read the ARCH's **current resolution line**: the one in its
   last Change Log row that carries a `Policy resolution:` line (create, amend and the reuse review write
   one; approval rows don't). Never fall back to an older row. Build the entry from the setting's current
   value, `architecture.mandated_platforms=<platform> for <capability> (POL-NNN#SET-NN)`, and compare it as
   exact text, after trimming outer whitespace from the platform and the capability (the architecture step
   copies both verbatim). Exactly one outcome applies:
   - **Unchanged:** the line contains the entry. The setting counts, and the report notes the newer policy
     version.
   - **Changed:** the line names `POL-NNN#SET-NN` in that form with a different platform or capability. The
     mandate changed since the ARCH applied it, so its question is open again (SPEC-003 v5 §4): R is
     **blocked** by that DEC, naming the change, and the next action hands back to the architecture step.
   - **No platform recorded:** the line names the setting only in the older form
     `architecture.mandated_platforms=POL-NNN#SET-NN`, with no platform and capability. Only that exact form
     qualifies. The report names the evidence gap. With a user present, ask whether the setting mandated
     the platform it now names, for its capability, when the question was resolved: yes, the setting
     counts; no or don't know, treat it as changed (blocked). With no user, including a request to proceed
     without questions, the setting still counts (SPEC-003 v5 §4).
   - **No record:** the line doesn't name `POL-NNN#SET-NN` at all, or no Change Log row carries a
     `Policy resolution:` line. A missing record is never treated as the older form: R is `unknown`.
4. **No contested mandate.** No other approved document in `docs/specs/policy/` has an active
   `architecture.mandated_platforms` setting for the same capability. Capabilities are compared as the
   policy script compares them: outer whitespace trimmed and case ignored, while inner spaces count; no
   other normalization. The one exception is a permitted override (SV-04): the resolver is the project
   policy's setting, and the organization setting for that capability has `overridable_by` including
   `project`. An organization setting replaced by a permitted override fails this check. Settings for
   different capabilities never conflict, so an organization and a project policy can each mandate
   platforms.

A changed mandate makes R **blocked**, for example
`blocked by DEC-07 (POL-001#SET-01 now mandates "<platform> for <capability>"; ARCH-001 recorded "<platform> for <capability>")`.
Every other failed check makes R `unknown`, naming the resolver and the failed condition, for example:
- `POL-001#SET-01 fails the policy check: setting deprecated (check 2)`;
- `POL-001#SET-01 fails the policy check: ARCH-001 has no link to it (check 3)`;
- `POL-001#SET-01 fails the policy check: ARCH-001's latest resolution doesn't record it (check 3)`;
- `POL-001#SET-01 fails the policy check: POL-002#SET-01 also mandates "<capability>" (check 4)`.

Both hand back to the architecture step, `/devforgeai:architecture PRD-NNN`, which re-resolves policy and,
for a changed mandate, reopens the question. Check 4 compares capabilities the way SPEC-002's policy script
does; check 3 compares entries as exact text, because they are copies. SPEC-003 v5 closes the earlier known
limit: the architecture step offers no reuse while a resolved DEC relies on a changed platform, so a reuse
review can no longer record a new platform over an unchanged question.

**The selection rule.** A requirement R of the PRD (an FR or an NFR) is **eligible** when all hold:
1. R is `status: active`;
2. R is ready;
3. `release: current`;
4. `priority` is `must`, `should` or `could`;
5. for an FR only: no active existing epic (not `superseded` or `deprecated`) has a `refines` link to this
   PRD's R (the PRD ID and the item both match), at any version. NFRs are never "covered": an eligible NFR
   is attached to new epics by the grouping, even when an existing epic already refines it (Grouping).

Every other requirement is **left out**. The report gives each one **one compact row with every reason that
applies**, in the order below, and **one next action: the first listed reason's**. Several reasons never mean
several questions.

| Reason | When | Next action |
|---|---|---|
| `deprecated` | R is not active | none |
| `wont` | `priority: wont` | none for this release |
| `later` | `release: later` | none for the current release |
| `undecided` | `release` is `null`, or `priority` is `null` with `release: current`. A `later` requirement's null priority is SPEC-002's normal form, not undecided | the PRD owner decides |
| `covered` (an FR) or `refined` (an NFR) | an FR: an active existing epic refines this PRD's FR. An NFR: R is blocked or unknown, and an active existing epic refines this PRD's NFR. Names every such epic | an FR that isn't blocked or unknown: none. Otherwise review those epics' work before continuing |
| `blocked` | R is not ready; names the blocking DEC IDs, any superseded resolver, a mandated platform that changed, or the marker without a matching question | resolve it with `/devforgeai:architecture` |
| `unknown` | readiness can't be established: a missing or unreadable input, or a policy resolver that fails the bounded check; names it | fix that input, or review the architecture, then run again |

**The NFR review signal.** When an NFR is blocked or unknown, every active existing epic whose
`upstream` has a `refines` link to this PRD's NFR (the PRD ID and the item both match, at any version)
rests on a question that is no longer settled, just as a covered FR's epic does. The row then lists the
reason **refined by EPIC-NNN** (every such epic), and when that reason comes first among those that give a
next action, the next action is **Review EPIC-NNN's work before continuing.** This is still not `covered`:
a covered FR gets no new epic, while an NFR that becomes eligible again can be attached to new epics as
usual. The existing epics are read-only either way.

**Precedence.** The order of reasons and the one-next-action rule don't change: the next action is the
first listed reason's. So when `wont`, `later` or `undecided` also applies, that reason comes first and
its action wins, but the row still lists `covered by …` or `refined by …`, so the reader sees which epics
rest on the unsettled question. A deprecated requirement gets only `deprecated`.

For example:
- `FR-005: later (release later); blocked by DEC-06 (open). No action for the current release.`
- `FR-008: covered by EPIC-002; blocked by DEC-03 (ADR-002 superseded by ADR-003). Review EPIC-002's work before continuing.`
- `NFR-001: refined by EPIC-001; blocked by DEC-08 (open). Review EPIC-001's work before continuing.`
- `NFR-003: later (release later); refined by EPIC-001; blocked by DEC-08 (open). No action for the current release.`

An eligible NFR that no new epic attaches also gets a row, because it is in no new epic. It is always
refined by an active existing epic, since otherwise a standalone NFR epic is written (Grouping). Its row
reads **already refined by EPIC-NNN**, with no action, for example `NFR-001: already refined by EPIC-001.
No action.` It is never called `covered`, since NFRs are never covered.

**The report** lists each new epic with the requirements it refines, then the rows. Together they name
**every FR exactly once** (in one epic line or one row) and **every NFR at least once**: an NFR attached to
several new epics appears in each of their lines.

**Grouping.** Each eligible FR is refined by exactly one new epic. Each eligible NFR is **attached** to at
least one new epic, unless an active existing epic already refines it, with `note: "partial: <which part>"`
when more than one active epic refines it; attaching it never creates a second deliverable. Which new epics
it is attached to is the grouping's choice. The skill's own proposal attaches it to every new epic whose
capability it constrains, while a grouping the user states or changes decides otherwise (VER-04). A
**standalone NFR epic** is written only for an eligible NFR that no active epic, existing or new in this
run, refines. So rerunning with unchanged inputs writes nothing (ERR-05).
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
    rule: "Find the ARCH whose frontmatter upstream links cite this PRD, ignoring a superseded or deprecated ARCH, and check that its PRD link version equals the PRD's version (§4), which the architecture skill records on create, amend or a confirmed reuse review. Use it only then; otherwise stop as ERR-02, ERR-03 (the link version differs, older or newer) or ERR-04."
  - id: BEH-04
    status: active
    rule: "Compute readiness for every active FR and NFR of the PRD from the ARCH file and the ADR files, as SPEC-003 §4 with the bounded policy check in §4, reading each resolving ADR's current status and superseded_by now. A DEC cites a requirement only through a link with this PRD's ID and that item, and blocks only the requirements its own upstream cites. Read a DEC's state first: an open DEC blocks whatever its policy record says. A policy resolver counts only if it passes the bounded check in §4: an approved document; an active architecture.mandated_platforms setting; an ARCH link to it; still the mandate the ARCH recorded (the link's version equals the policy's, or else the ARCH's latest resolution line holds the setting's current platform and capability); and no other approved document mandating the same capability, unless it is a permitted project override. A policy version bump alone never blocks. A changed platform or capability makes the requirement blocked by that DEC, naming the change, and hands back to the architecture step. A record in the older form architecture.mandated_platforms=POL-NNN#SET-NN (no platform) is an evidence gap the report names: with a user present, ask, one question per such resolver showing the setting's current platform and capability, whether the setting mandated that platform when the question was resolved (yes: it counts; no or don't know: blocked, as changed); with no user, it counts. A missing record (no link, or no resolution line naming the setting) is unknown, never the older form. Resolve no policy beyond that. When a resolver counts at a newer policy version, say so in the report. Match every PRD [NEEDS ADR] marker to its own DEC (one whose question answers the marker's decision; a policy setting resolving a different question, or the resolution of another question, never clears it); when none clearly does, every requirement the marker names is blocked, even if other DECs citing it are resolved. When readiness can't be established, report the requirement as unknown, naming the missing input or failed check; a resolved DEC with an empty resolved_by is unknown. Never use a skill's reply as the source."
  - id: BEH-05
    status: active
    rule: "Apply the selection rule (§4): a requirement is eligible only when it is active, ready, release current, priority must, should or could, and, for an FR, not already refined by an active existing epic. NFRs are never covered. Give every other requirement one compact row with every reason that applies (deprecated, wont, later, undecided, covered (an FR) or refined (a blocked or unknown NFR) with every such epic's ID, blocked with the DEC IDs, a changed mandate or the unmatched marker, unknown), in the §4 order, and one next action, the first listed reason's: a covered FR or a refined NFR that is blocked or unknown gets 'Review EPIC-NNN's work before continuing' unless an earlier reason (wont, later, undecided) already gives the next action, and the row still names the epics. Undecided means release null, or priority null with release current; a later requirement's null priority isn't undecided. An eligible NFR that no new epic attaches gets the row 'already refined by EPIC-NNN' with no action."
  - id: BEH-06
    status: active
    rule: "Read every existing epic in docs/specs/epic/. An FR of this PRD that an active existing epic (not superseded or deprecated) refines, at any version and matching both the PRD ID and the item, is covered; if it is also blocked or unknown now, say so. NFRs are never covered: an NFR of this PRD that an active existing epic refines (both the PRD ID and the item match) and that is blocked or unknown now gets the NFR review signal (§4), naming every such epic; an eligible one is still attached to new epics as usual. Never modify, renumber or duplicate an existing epic."
  - id: BEH-07
    status: active
    rule: "Propose how to group the eligible requirements into epics: each a deliverable capability, each eligible FR in exactly one epic, each eligible NFR attached to every new epic it constrains, and a standalone NFR epic only for an eligible NFR that no active epic, existing or new, refines (§4). Show each proposed epic's title, requirements and priority, and ask the user to confirm or change the grouping; write nothing until they do. A grouping stated in the request counts as confirmed. A stated or changed grouping is applied as given, limited only by §4's rules: only eligible requirements, each eligible FR in exactly one new epic, each eligible NFR in at least one new epic unless an active existing epic already refines it, and the standalone-NFR, priority and numbering rules. If no one can confirm (the request says to proceed without questions and gives no grouping), write the proposal and add to §8 of each epic: [NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]. If a stated grouping leaves an eligible FR unplaced or places one twice and no one can be asked, place that FR by the proposal, keep the rest of the stated grouping, and add the same marker to every epic written."
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
    rule: "Hand off with each epic written (path, title, priority and the requirements it refines), then the left-out rows (§4: every reason that applies and one next action per requirement, with no extra questions), and the proposal warning if an input is a draft. Epic lines and rows together name every FR exactly once and every NFR at least once (§4, the report). Then name the next step, the story step, with the new epic IDs as its input: if ${CLAUDE_SKILL_DIR}/../story/SKILL.md exists, tell the user to run /devforgeai:story with an epic ID; otherwise say stories are written by hand from the story template for now and that, once the story skill (planned as /devforgeai:story) is built, it runs with an epic ID. After ERR-05 the story step names the epics that already refine the requirements; after ERR-08 there is no story step (ERR-08 names the next step). The next step comes last in the final reply, as its own paragraph outside any code block, starting with the words Next step; nothing follows it. Never write a story."
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
    condition: "No active ARCH (not superseded or deprecated) cites the PRD"
    handling: "Write nothing. Say that readiness comes from the architecture description, and tell the user to run /devforgeai:architecture with the PRD ID first"
    user_result: "A handback to the architecture step; no epic written"
  - id: ERR-03
    status: active
    condition: "The ARCH that cites the PRD hasn't been reviewed against the PRD's current version: its PRD link version differs, usually older, or newer after a hand edit"
    handling: "Write nothing. Name both versions, and tell the user to review the architecture against this PRD version with /devforgeai:architecture and the PRD ID; confirming reuse there records the review, and changes are made only if the review finds them"
    user_result: "A handback to review the architecture; no epic written"
  - id: ERR-04
    status: active
    condition: "Several active ARCH documents cite the PRD"
    handling: "List them with their systems and PRD link versions, and ask; never pick one silently"
    user_result: "A choice of ARCH"
  - id: ERR-05
    status: active
    condition: "Nothing new to write, because everything eligible already has an epic: no FR is eligible, every eligible NFR is already refined by an active epic, and at least one requirement is active, ready, release current and must, should or could (for example, a rerun with unchanged inputs)"
    handling: "Write nothing, say that no requirement needs a new epic, report every row (§4, including 'already refined' for each eligible NFR), and name the story step for the epics that already refine the requirements"
    user_result: "The report; no epic written"
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
  - id: ERR-08
    status: active
    condition: "Nothing is eligible yet: no requirement of the PRD is active, ready, release current and must, should or could (for example, an open DEC blocks every current-release requirement)"
    handling: "Write nothing. Say that no requirement is eligible for an epic yet, never that none needs one, and report every requirement's row. Name no story step. The next step is /devforgeai:architecture with the PRD ID when any row is blocked or unknown; otherwise the PRD owner's decision on the undecided rows; otherwise say that nothing remains for the current release"
    user_result: "The report and the step that unblocks it; no epic written"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the selection and grouping rules and the output contract; the ARCH lookup, readiness and output rules live in references/"
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
    response: "One eval case per automated VER item, tagged epic and ver-NN, run against the no-plugin baseline"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 10, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Structural: schemas, templates, fixtures and cross-document links | Version 1: `src/tests/epic/make_evals.py` validates all 11 fixtures against `src/schemas/`, and checks the shared fixture against the table below, before it writes the cases. The skill's `SKILL.md` frontmatter and `provenance.yaml` pass `skill-frontmatter.schema.json` and `skill.schema.json`. Templates and cross-document links: not run. Version 2 (SKL-004 v2): `make_evals.py` validates all 18 fixtures against `src/schemas/` with the format checker, checks the shared fixture against the table below, and checks each variant's premise (both resolution entries present, the two policies' capabilities distinct, POL-001 v2's SET-01 unchanged, DEC-08's citations) before it writes the 18 cases. Its regex and file graders were checked offline (`src/tests/epic/grade_evals.mjs`) against scripted v2-correct and v1-like results: 16 of 16 scenarios as expected. `SKILL.md` (306 lines, 2,916 words) and `provenance.yaml` pass their schemas, and both record version 2. plugin-dev's validation phase (`plugin-validator`, `skill-reviewer`, 2026-10-01): no defects, with eight polish items left for a later version. Templates and cross-document links: not run |
| Behavioural: automated VER items, one eval case each | Version 1: built as SKL-004 v1 and merged in PR #5; deployed. 14 eval cases (VER-01..12, 14, 15). `claude plugin eval`, 3 runs with the no-plugin baseline, 2026-09-28, plugin 0.4.0: 14 of 14 at 0.8 or above, 13 at 1.00, mean Δ +0.51. `no-arch-hands-back` (VER-05) scored 0.89; after `SKILL.md` step 3 stated ERR-02's reason and its readiness grader became an llm grader, it scored 1.00 over 3 runs. PR #5 records the results |
| Behavioural (v2-a): the new and changed cases on SKL-004 v1, 2026-10-01 | `tmp/eval-results/epic-v2-on-v1-20261001T122340-<case>/` (local, untracked), one folder per case, run by Bryan from a plain terminal. Bound to `96f94b3` (the v2 cases, SKL-004 v1 unchanged); Claude Code 2.1.286; plugin 0.7.0; `--runs 1 --ablation none`; judge model sonnet; $3.24. **Four of the five predicted failures reproduced, with v1's own wording:** VER-16 0.67 (FR-001 and FR-012 unknown: "same key … (check 4)"); VER-17 0.67 (FR-012 unknown: "POL-001 is now v2 but ARCH-001 links it at v1 (check 3)"); VER-19 0.71 ("No requirement needs a new epic." with every requirement blocked); VER-03 0.80 (FR-005 "later; undecided (priority null)"). VER-14 and VER-18 passed on v1: the model improvised the right row and read "cites" correctly, so their graders stay as guards. VER-01 passed (control) |
| Behavioural (v2-b): SKL-004 v2, epic tag, one run, 2026-10-01 | `tmp/eval-results/epic-v2-runs1-20261001T124457/` (local, untracked). Bound to `6da48fe` (SKL-004 v2), plugin digest `f849c869a7dce1e5bd6a85d14caeb1b10e76c181b6190e8b195460ebaf682e1c`; Claude Code 2.1.286; plugin 0.7.0; 18 cases; `--runs 1 --ablation none`; judge model sonnet; concurrency 4; $8.33; 257 s. **18 of 18 at 1.00**, with no errors |
| Behavioural (v2-c): SKL-004 v2, epic tag, 3 runs with the baseline, 2026-10-01 | `tmp/eval-results/epic-v2-3run-20261001T132651/` (local, untracked), run by Bryan from a plain terminal. Bound to `6da48fe`, the same plugin digest as (v2-b); Claude Code 2.1.286; plugin 0.7.0; 18 cases; 3 runs per arm against the no-plugin baseline; threshold 0.8; judge model sonnet; concurrency 4; $43.21; 1,541 s. **All 18 cases at 0.8 or above, 16 at 1.00; mean Δ +0.52**, with no errors. VER-15 (`policy-resolver-revoked`) 0.89: in one run, EPIC-001 was right (no FR-012 link), but the reply's FR-012 row didn't match the regex, and a failed regex grader keeps no reply. VER-03 (`reports-left-out`) 0.93: in one run, the llm grader voted FAIL FAIL PASS on a reply whose four rows and notes meet every clause (judge disagreement). Δ: VER-01 +0.69, VER-02 +0.63, VER-03 +0.73, VER-04 +0.30, VER-05 +1.00, VER-06 +1.00, VER-07 +0.33, VER-08 +0.67, VER-09 +0.33, VER-10 +0.67, VER-11 0.00 (the negative trigger), VER-12 +0.40, VER-14 +0.60, VER-15 +0.22, VER-16 +0.40, VER-17 +0.53, VER-18 +0.17, VER-19 +0.61 |
| Behavioural (v3-a): SKL-004 v3, epic tag, one run, 2026-10-01 | `tmp/eval-results/epic-v3-runs1-20261001T144103/` (local, untracked), run by Bryan from a plain terminal. Bound to `823b06e` (SKL-004 v3 after its skill-review polish); Claude Code 2.1.287; plugin 0.8.0; 18 cases, unchanged from version 2; `--runs 1 --ablation none`; judge model sonnet; concurrency 4; $8.42; 258 s. 17 of 18 at 1.00, with no errors. VER-03 (`reports-left-out`) 0.80: all three judges failed its llm grader on a reply correct on every clause. The grader written for version 2 forbade asking "the PRD owner to decide" FR-005's priority while requiring "the PRD owner decides" for FR-007 and NFR-002 |
| Behavioural (v3-b): VER-03's grader fix, one case, 2026-10-01 | The grader now says "The PRD owner decides" is the expected next action, not a question (`329ff27`; VER-03's obligation unchanged; only that grader file regenerated). `tmp/eval-results/epic-v3-ver03-20261001T144953/` (local, untracked), bound to `329ff27`; Claude Code 2.1.287; `--runs 1 --ablation none`; $0.53. **1.00**, judge votes PASS PASS PASS. Then `dbeef9f` named the "No action …" rows as next actions and said a row may list several reasons, from the grader's review |
| Behavioural (v3-c): SKL-004 v3, epic tag, 3 runs with the baseline, 2026-10-01 | `tmp/eval-results/epic-v3-3run-20261001T163508/` (local, untracked), run by Bryan from a plain terminal. Bound to `dbeef9f`, plugin digest `554e69443eee04f69a8f67e25379b970bab71634e76d6e38c095a8b4648316fa`; Claude Code 2.1.287; plugin 0.8.0; 18 cases; 3 runs per arm against the no-plugin baseline; threshold 0.8; judge model sonnet; concurrency 4; $43.02; 1,526 s. **All 18 cases at 1.00 in every run; mean Δ +0.51**, with no errors; VER-03's llm grader passed 9 of 9 votes. An earlier attempt on `dbeef9f`, `tmp/eval-results/epic-v3-3run-20261001T145309/` (started 18:53 UTC), is not a result: all 108 runs failed with the account's session limit ("You've hit your session limit"; score 0.19, $1.29), and the run above followed the reset. Δ: VER-01 +0.69, VER-02 +0.62, VER-03 +0.80, VER-04 +0.30, VER-05 +1.00, VER-06 +1.00, VER-07 +0.33, VER-08 +0.67, VER-09 +0.33, VER-10 +0.67, VER-11 0.00 (the negative trigger), VER-12 +0.40, VER-14 +0.53, VER-15 +0.33, VER-16 +0.40, VER-17 +0.47, VER-18 +0.17, VER-19 +0.50 |
| Behavioural (v4): SKL-004 v4, epic tag | Not run. Version 4 is implemented only after SPEC-003 v5 is on main. It adds VER-20 to VER-26 (25 cases) and keeps VER-17, the unchanged mandate, as a regression case |
| Behavioural: manual VER items (VER-13) | Not run, for version 1, 2 or 3; deferred by Bryan (2026-10-01) |
| Qualification | SKL-004 v2 approved by Bryan on 2026-10-01, after its automated items passed in a bound 3-run (v2-c). Merged in PR #43 (`eeedd5c`) and deployed in plugin 0.8.0. SKL-004 v3 approved by Bryan on 2026-10-01, after its automated items passed in a bound 3-run (v3-c); merged in PR #47 (`3cf7033`) and deployed in plugin 0.8.1, which the context skill's PR #45 set; the v3 runs above used 0.8.0. Open: VER-13 |

**Shared fixture (version 2).** One approved PRD, `PRD-001` v2 with `target_release: "Spring launch"`, and
one approved `ARCH-001` whose frontmatter cites PRD-001 v2. Both have the shape the current prd (SKL-002
v3) and architecture (SKL-003 v5) skills write: a constraint NFR for the mandated platform, carrying its
policy link; components with `kinds`; and resolution lines in the ADR-003 A5 format. Each is written fresh
and checked against its schema. The shared PRD is approved although FR-005, FR-007 and NFR-002 keep `null`
values that SPEC-002 §4 would block at approval. That is deliberate: the skill doesn't enforce the PRD's
approval gate and must handle whatever lands. The ADRs are `ADR-001` (accepted, answers DEC-02), `ADR-002`
(superseded by `ADR-003`) and `ADR-003` (accepted, a different topic: it answers DEC-04, audit storage).
`docs/specs/policy/POL-001.md` is an approved organization policy at version 1. Its `SET-01` mandates
"Regional network mail relay (SMTP)" for "transactional email" and resolves DEC-07. The ARCH links it at
version 1 on the mail-relay component, and the ARCH's resolution line reads
`architecture.mandated_platforms=Regional network mail relay (SMTP) for transactional email (POL-001#SET-01)`.

| Requirement | Priority / release | ARCH | Expected |
|---|---|---|---|
| FR-001 | must / current | DEC-01 open, cites only FR-001; a PRD `[NEEDS ADR]` marker names FR-001 | left out: blocked by DEC-01 |
| FR-002 | must / current | DEC-02 resolved by ADR-001, cites FR-002 and NFR-001 | eligible |
| FR-003 | should / current | no DEC | eligible |
| FR-004 | could / current | no DEC | eligible |
| FR-005 | null / later, as prd writes a later requirement | DEC-06 open, cites FR-005 | left out: later; DEC-06 open; no action for the current release; not undecided |
| FR-006 | wont / current | no DEC | left out: wont |
| FR-007 | null / current | no DEC | left out: undecided |
| FR-008 | must / current | DEC-03 resolved by ADR-002, superseded | left out: blocked by DEC-03 |
| FR-009 | must / current | no DEC; a PRD `[NEEDS ADR]` marker names FR-009 | left out: blocked (marker without a matching question) |
| FR-010 | must / current | DEC-04 (audit storage) resolved by ADR-003, cites FR-010; a PRD `[NEEDS ADR]` marker for a different decision (payment provider) names FR-010, and no DEC answers it | left out: blocked (marker without a matching question) |
| FR-011 | must / current | DEC-05 resolved by ADR-004, whose file doesn't exist | left out: unknown (ADR-004 not found) |
| FR-012 | must / current | DEC-07 resolved by `POL-001#SET-01`: approved, an active mandate, POL-001 v1 equals the ARCH's link version, and no other policy mandates "transactional email" | eligible |
| NFR-001 | must / current | DEC-02 | eligible |
| NFR-002 | null / null: the constraint NFR for `POL-001#SET-01`, as prd v3 writes policy and quality-round NFRs | no DEC | left out: undecided (priority and release null); the PRD owner decides |

So the eligible set is FR-002, FR-003, FR-004, FR-012 and NFR-001. FR-001 shows that DEC-01 blocks only what it
cites (FR-002 stays eligible), FR-008 shows that a superseded resolver blocks again, and FR-009 shows that
a `[NEEDS ADR]` marker with no question still blocks, and FR-010 shows that one resolved DEC doesn't
answer a different marker. FR-005 shows that a later requirement's null priority isn't undecided, and
NFR-002 that an NFR prd left undecided is never attached (Bryan's decision of 2026-10-01). File graders
check the written epics, not the reply, because a wrong epic is worse than a wrong sentence. Unless a
case says otherwise, the prompt states the grouping, so the run is non-interactive and confirmed.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture; the prompt asks for one epic covering everything eligible. docs/specs/epic/EPIC-001.md refines FR-002, FR-003, FR-004, FR-012 and NFR-001 at PRD-001 version 2, and contains no refines link to FR-001, FR-005 to FR-011 or NFR-002. Eval case selects-ready-current: regex on the file."
    level: e2e
    covers:
      - BEH-02
      - BEH-03
      - BEH-04
      - BEH-05
      - BEH-08
      - BEH-10
    upstream:
      - {id: STORY-005, item: AC-01, relation: verifies, version: 2, hash: null}
  - id: VER-02
    status: active
    obligation: "In VER-01's setup, no epic refines FR-001, FR-008, FR-009, FR-010 or FR-011, and the reply reports FR-001 blocked by DEC-01, FR-008 blocked by DEC-03 (naming ADR-002 as superseded), FR-009 and FR-010 blocked by a [NEEDS ADR] marker without a matching question, and FR-011 as unknown because ADR-004 isn't found; FR-002 and FR-012 are not reported blocked or unknown. Eval case blocked-not-included: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-03
    status: active
    obligation: "In VER-01's setup, the reply gives one row each for FR-005 (later, with DEC-06 open and no action for the current release; the row doesn't say undecided), FR-006 (won't have), FR-007 (undecided, for the PRD owner) and NFR-002 (undecided, for the PRD owner), each with a next action, and asks no question about them. Eval case reports-left-out: regex on last_message."
    level: e2e
    covers:
      - BEH-05
      - BEH-11
    upstream:
      - {id: STORY-005, item: AC-03, relation: verifies, version: 2, hash: null}
  - id: VER-04
    status: active
    obligation: "Shared fixture; the prompt asks for one epic per priority level, with NFR-001 only in the Must epic. EPIC-001.md has priority must and refines FR-002, FR-012 and NFR-001; EPIC-002.md has priority should and refines FR-003; EPIC-003.md has priority could and refines FR-004. Eval case orders-by-priority: regex on the three files."
    level: e2e
    covers:
      - BEH-07
      - BEH-08
    upstream:
      - {id: STORY-005, item: AC-06, relation: verifies, version: 2, hash: null}
  - id: VER-05
    status: active
    obligation: "The shared PRD and ADRs with no ARCH: no docs/specs/epic/EPIC-001.md is written, and the reply tells the user to run /devforgeai:architecture PRD-001 first. Eval case no-arch-hands-back: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-02
    upstream:
      - {id: STORY-005, item: AC-04, relation: verifies, version: 2, hash: null}
  - id: VER-06
    status: active
    obligation: "The shared fixture with the ARCH's PRD link at version 1 while PRD-001 is at version 2: no EPIC-001.md is written, and the reply names both versions and tells the user to review the architecture with /devforgeai:architecture PRD-001. Eval case stale-arch-stops: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-03
      - ERR-03
    upstream:
      - {id: STORY-005, item: AC-04, relation: verifies, version: 2, hash: null}
  - id: VER-07
    status: active
    obligation: "The shared fixture plus an existing EPIC-001.md (version 1, a unique sentinel line) that refines FR-002, FR-008 and NFR-001 (partial). The prompt asks for one epic covering everything eligible, with NFR-001 applying to it. EPIC-001.md still has version 1 and the sentinel; the new EPIC-002.md refines FR-003, FR-004, FR-012 and NFR-001 and not FR-002; the reply reports FR-002 as covered by EPIC-001, reports FR-008 as covered by EPIC-001 and now blocked by DEC-03, and doesn't report NFR-001 as covered. Eval case existing-epic-not-duplicated: regex on both files and last_message."
    level: e2e
    covers:
      - BEH-06
      - BEH-12
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-08
    status: active
    obligation: "The shared fixture with PRD-001 at status draft: EPIC-001.md and the reply say the epics are proposals because the PRD is a draft. Eval case draft-inputs: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-02
    upstream:
      - {id: STORY-005, item: AC-08, relation: verifies, version: 2, hash: null}
  - id: VER-09
    status: active
    obligation: "Shared fixture; the prompt says to proceed without questions and gives no grouping. EPIC-001.md exists, has status draft, and carries a [NEEDS CLARIFICATION] marker saying the grouping is unconfirmed. Eval case unconfirmed-grouping: regex on the file."
    level: e2e
    covers:
      - BEH-07
    upstream:
      - {id: STORY-005, item: AC-05, relation: verifies, version: 2, hash: null}
  - id: VER-10
    status: active
    obligation: "In VER-01's setup, the final reply names the story step as next with EPIC-001 as its input, and no file is written under docs/specs/story/. The grader doesn't check whether the story skill exists, so shipping it won't break this case. Eval case hands-off-to-story: regex on last_message and file_exists false."
    level: e2e
    covers:
      - BEH-11
    upstream:
      - {id: STORY-005, item: AC-09, relation: verifies, version: 2, hash: null}
  - id: VER-11
    status: active
    obligation: "A request such as 'write an epic poem about the sea' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
    upstream:
      - {id: STORY-005, item: AC-10, relation: verifies, version: 2, hash: null}
  - id: VER-12
    status: active
    obligation: "In VER-01's run, EPIC-001.md has non-empty generated_by tool, model and session, reviewed_by empty, every hash null, status draft, approved_by empty, target_release 'Spring launch', and an informed_by link to ARCH-001. Eval case records-provenance: regex on the file."
    level: e2e
    covers:
      - BEH-09
    upstream:
      - {id: STORY-005, item: AC-11, relation: verifies, version: 2, hash: null}
  - id: VER-13
    status: active
    obligation: "Manual, interactive, one fixture copy per check: (a) the skill proposes a grouping, the user changes it, and the epics written follow the changed grouping; (b) an unknown PRD ID lists the available PRDs and writes nothing; (c) two active ARCHs citing the PRD are listed and the skill asks; (d) automated since version 2 by VER-19 (ERR-08) and VER-14 (ERR-05), so not run by hand; (e) stopping before confirming writes nothing; (f) SKILL.md is within the NFR-001 limits, and metadata.devforgeai-version equals provenance.yaml's version; (g) run on this repository's own PRD-001, which has no ARCH, it writes nothing and hands back to the architecture step; (h) by reading only: SKILL.md states the three-attempt limit and the ERR-06 failure report; (i) the review loop: PRD-001 gets a priority-only change to version 3, the skill stops (ERR-03), /devforgeai:architecture PRD-001 with reuse confirmed moves the ARCH's frontmatter PRD link to version 3, sets outcome reuse and adds one Change Log row, with the ARCH's version, status, approval fields and items unchanged, and the skill then writes epics; confirming reuse again at version 3 changes nothing in the ARCH; (j) a superseded ARCH-001 and an approved ARCH-002 both cite the PRD at its version: the skill uses ARCH-002 without asking; (k) automated since version 4 by VER-20 (a changed platform now makes FR-012 blocked, not unknown), so not run by hand. ERR-06 can't be forced without a CLI, so (h) is a reading check, not an exercise."
    level: manual
    covers:
      - BEH-01
      - BEH-07
      - ERR-01
      - ERR-04
      - ERR-06
      - ERR-07
      - QR-01
      - BEH-03
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-05, relation: verifies, version: 2, hash: null}
      - {id: STORY-005, item: AC-12, relation: verifies, version: 2, hash: null}
  - id: VER-14
    status: active
    obligation: "The shared fixture plus an existing EPIC-001.md (version 1, a unique sentinel line) that already refines FR-002, FR-003, FR-004, FR-012 and NFR-001, as a first run would have written. No docs/specs/epic/EPIC-002.md is written, EPIC-001.md still has version 1 and the sentinel, and the reply says no requirement needs a new epic, gives NFR-001 a row saying it is already refined by EPIC-001, and doesn't call NFR-001 covered. Eval case rerun-writes-nothing: file_exists false, regex on the file and last_message."
    level: e2e
    covers:
      - BEH-05
      - BEH-06
      - BEH-07
      - BEH-11
      - ERR-05
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-15
    status: active
    obligation: "The shared fixture with POL-001's SET-01 at status deprecated: EPIC-001.md contains no refines link to FR-012, and the reply reports FR-012 as unknown, naming POL-001#SET-01 and the failed check. Eval case policy-resolver-revoked: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-16
    status: active
    obligation: "Two policy layers: the shared fixture plus an approved project policy POL-002 v1 whose active SET-01 mandates 'Riverside council sign-in (OIDC)' for 'volunteer sign-in'. In ARCH-001, DEC-01 is resolved by POL-002#SET-01, the identity-provider component links it at version 1, and the resolution line names both mandated platforms. The prompt asks for one epic covering everything eligible. EPIC-001.md refines FR-001 and FR-012 as well as FR-002, FR-003, FR-004 and NFR-001, and the reply reports neither FR-001 nor FR-012 as unknown. Eval case epic-two-policy-layers: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-17
    status: active
    obligation: "Policy bumped, mandate unchanged: the shared fixture with POL-001 at version 2, which adds an active testing.coverage_threshold setting SET-02 and leaves SET-01 as it was; ARCH-001 still links SET-01 at version 1, and its resolution line holds SET-01's entry. The prompt asks for one epic covering everything eligible. EPIC-001.md refines FR-012, the reply doesn't report FR-012 as unknown, and the reply notes that POL-001 is newer than the version ARCH-001 linked. Eval case epic-policy-bump-unchanged: regex on the file and last_message, plus an llm grader on last_message for the version note."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-18
    status: active
    obligation: "A second PRD with colliding numbers: the shared fixture plus an approved PRD-002 v1, with ARCH-001 at version 2 (amended and approved again). Its frontmatter also cites PRD-002 v1, and it has an open DEC-08 that cites only PRD-002#FR-003. The prompt asks for one epic covering everything eligible. EPIC-001.md refines PRD-001's FR-003, and the reply doesn't report FR-003 as blocked by DEC-08. Eval case epic-second-prd-same-number: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-19
    status: active
    obligation: "Nothing eligible: the shared fixture, with ARCH-001 adding an open DEC-08 ('Which hosting provider runs the system?') that cites FR-002, FR-003, FR-004, FR-012 and NFR-001. The prompt asks for one epic covering everything eligible. No file is written under docs/specs/epic/. The reply says no requirement is eligible yet and doesn't say that no requirement needs a new epic. Its next step names /devforgeai:architecture PRD-001, and the reply doesn't name /devforgeai:story. Eval case epic-nothing-eligible: file_exists false and regex on last_message."
    level: e2e
    covers:
      - BEH-11
      - ERR-08
    upstream:
      - {id: STORY-005, item: AC-03, relation: verifies, version: 2, hash: null}
      - {id: STORY-005, item: AC-09, relation: verifies, version: 2, hash: null}
  - id: VER-20
    status: active
    obligation: "A changed mandate is blocked: the shared fixture with POL-001 at version 2, whose SET-01 now mandates 'Network-hosted mail service (HTTPS API)' for 'transactional email', while ARCH-001 still links SET-01 at version 1 and its resolution line records the regional network mail relay. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md contains no refines link to FR-012. The reply reports FR-012 as blocked by DEC-07, naming the new platform, and not as unknown or ready; its next action is /devforgeai:architecture PRD-001. Eval case epic-mandate-changed-blocked: regex on the file and last_message, plus an llm grader for the blocked row."
    level: e2e
    covers:
      - BEH-04
      - BEH-05
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-21
    status: active
    obligation: "No platform recorded, no user: the shared fixture with POL-001 at version 2 (SET-02 added, SET-01 unchanged) and an ARCH-001 whose resolution line records the setting only as architecture.mandated_platforms=POL-001#SET-01. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md refines FR-012, and the reply names the gap: ARCH-001 recorded no platform for POL-001#SET-01. Eval case epic-legacy-record-no-user: regex on the file, plus an llm grader on last_message for the gap."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-22
    status: active
    obligation: "No platform recorded, a user present: VER-21's fixture, but the prompt states the grouping (one epic for everything eligible) and doesn't say to proceed without questions. No file is written under docs/specs/epic/ before the answer, and the reply asks whether POL-001#SET-01 mandated the regional network mail relay for transactional email when DEC-07 was resolved. Eval case epic-legacy-record-asks: file_exists false, plus an llm grader on last_message for the question."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-23
    status: active
    obligation: "A missing record is not the older form: the shared fixture with POL-001 at version 2 (SET-01 unchanged) and an ARCH-001 whose Change Log has no Policy resolution: line in any row. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md contains no refines link to FR-012, and the reply reports FR-012 as unknown, naming POL-001#SET-01 and the missing record. Eval case epic-missing-record-unknown: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-24
    status: active
    obligation: "Blocked NFRs with an existing epic: the shared fixture plus NFR-003 (release later, priority null) in PRD-001, an open DEC-08 in ARCH-001 citing NFR-001 and NFR-003, and an existing active EPIC-001 (a unique sentinel line) that refines FR-003, NFR-001 and NFR-003. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md is unchanged; no new epic refines NFR-001 or NFR-003. The reply gives NFR-001 the row 'refined by EPIC-001; blocked by DEC-08 (open)' with the next action to review EPIC-001's work, never calls NFR-001 covered, and gives NFR-003 'later … refined by EPIC-001 … blocked by DEC-08' with no action for the current release (precedence). Eval case epic-nfr-blocked-review: regex on the files and last_message, plus an llm grader for the two rows."
    level: e2e
    covers:
      - BEH-05
      - BEH-06
      - BEH-12
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-25
    status: active
    obligation: "An unknown NFR with an existing epic: the shared fixture plus an existing active EPIC-001 (a unique sentinel line) that refines FR-003 and NFR-001, and a resolved DEC-08 in ARCH-001 citing NFR-001 whose resolver ADR-005 doesn't exist. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md is unchanged and no new epic refines NFR-001. The reply gives NFR-001 the row 'refined by EPIC-001; unknown: ADR-005 not found' with the next action to review EPIC-001's work, and doesn't call it covered. Eval case epic-nfr-unknown-review: regex on the files and last_message."
    level: e2e
    covers:
      - BEH-05
      - BEH-06
    upstream:
      - {id: STORY-005, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-26
    status: active
    obligation: "Exact-question marker matching: the shared fixture with ARCH-001 adding DEC-08 ('Which email service sends membership payment receipts?'), resolved by POL-001#SET-01, which passes the bounded check and cites FR-010. FR-010's payment-provider marker still has no matching question. The prompt asks for one epic covering everything eligible and says to proceed without questions. EPIC-001.md contains no refines link to FR-010, and the reply reports FR-010 blocked by the payment-provider marker without a matching question. Eval case epic-unrelated-policy-marker: regex on the file and last_message."
    level: e2e
    covers:
      - BEH-04
    upstream:
      - {id: STORY-005, item: AC-02, relation: verifies, version: 2, hash: null}
```

## 10. Rollout, migration and rollback

The skill is new; removing its directory rolls it back. No schema changes: `epic.schema.json` already
covers the epic document. It depends on two parts of the architecture skill (SPEC-003):
- **The review record** (SPEC-003 BEH-08, BEH-09): a confirmed reuse against a newer PRD version records
  the review (§4). Without it, a reuse writes nothing and this skill's current-ARCH check would reject the
  ARCH forever.
- **SPEC-003 VER-10:** the architecture skill's `hands-off-to-epic` case must match whether this skill
  ships. The change that ships this skill updates that case if it no longer matches.

**Version 2** changes no schema. It changes the bounded policy check, the left-out rows and the report,
and splits ERR-05 from the new ERR-08. Roll it out by regenerating every case from the new §9, since the
generator asserts the shared fixture against the table. Then requalify the whole suite, because the shared
fixture changed under every case. Rolling back restores SKL-004 v1 and the v1 cases together.

**Version 4 depends on SPEC-003 v5.** SPEC-003 v5 (approved 2026-10-01, on
`feat/spec-003-v5-architecture`) reopens a DEC whose mandated platform changed and defines the
older-format record; this version follows it. SKL-004 v4 is implemented, evaluated and merged only after
SPEC-003 v5 is on main. Rolling back restores SKL-004 v3 and the v3 cases together.

**Backlog for the architecture step (SPEC-003), not part of this change:** relink a policy link when the
policy's `version` changes and the setting doesn't. Until then, check 3's resolution-line comparison
carries that case. (Reopening a DEC whose mandated platform changed is part of SPEC-003 v5.)

## 11. Implementation plan

1. Create a worktree for STORY-005 per ADR-001 v4, using the hardened deploy snippet.
2. `git mv src/templates/epic.md` into `skills/epic/assets/`, and update the templates README rows.
3. Write `references/selection.md` and `references/output-rules.md` from §4, BEH-03 to BEH-10 and the epic schema.
4. Write `SKILL.md` from §5–§7, and `provenance.yaml` as SKL-004 implementing SPEC-004.
5. Write the shared fixture and the case variants, checking each file against its schema, then the eval cases for VER-01 to VER-12, VER-14 and VER-15.
6. Update the architecture skill's `hands-off-to-epic` case if it no longer matches now that this skill ships (§10).
7. Deploy and validate per ADR-001, iterating until every case scores at least 0.8. Do VER-13 by hand.

**Version 2**, on the worktree branch `feat/epic-spec-004-v2`:
1. Bryan approves this version.
2. In `src/tests/epic/make_evals.py`:
   - write the new §9 shared fixture and the variants for VER-16 to VER-19;
   - change the cases for VER-01, VER-03 and VER-14;
   - extend the shared-fixture check to the NFRs, then regenerate.
   New case names start with `epic-`, because `--case` matches across skills.
3. Run only the new and changed cases on SKL-004 v1 (`--runs 1 --ablation none`, from a plain terminal),
   and confirm the new ones fail.
4. Write SKL-004 v2: `references/selection.md` and `SKILL.md` per §4, §6 and §7. Also make these fixes
   within this spec:
   - a stated grouping and a changed grouping are both limited only by the invariants (only eligible
     requirements, each eligible FR in exactly one epic, NFR attachment), and the unconfirmed-grouping
     marker goes on every epic of the run;
   - the template's `blocked_by` comment no longer contradicts the output rules;
   - prd's `target_release` placeholder is treated as no target release;
   - a DEC that asks a marker's question but cites only some of its requirements gets an accurate reason.
   Bump `provenance.yaml` and `metadata.devforgeai-version` together, and move the `implements` link to
   SPEC-004 v2.
5. Run the whole suite with `--runs 1`, then 3 runs with the baseline, after `record_revision.sh`. Record
   the results in §9, then open the PR. In the same PR:
   - update CLAUDE.md's skill-table row for `epic` to SKL-004 v2 and SPEC-004 v2;
   - remove `.claude/rules/skills.md`'s note that SPEC-004 BEH-11 names a different story-skill path,
     since BEH-11 now names the verified form.

**Version 3** (wording only), on `feat/epic-skl-004-v3`:
1. Bryan approves this version.
2. Write SKL-004 v3 through `/plugin-dev:create-plugin`, matching §4, BEH-07, BEH-11 and ERR-05, plus the
   skill-text polish from PR #43's skill review:
   - "covered" kept for FRs only;
   - one rule for an unconfirmed placement;
   - "the report" kept for SKILL.md step 9's report;
   - check 4 names the policy `scope` field;
   - the story-skill check uses Read or Glob;
   - text with no behavioral effect trimmed.
   Bump `provenance.yaml` and `metadata.devforgeai-version` together; `status` returns to `draft`.
3. Validate (`plugin-validator`, `skill-reviewer`), then run the 18 unchanged cases: the whole suite once,
   then 3 runs with the baseline, each bound by `record_revision.sh`. Record the results in §9, then open
   the PR.

**Version 4** (gated on SPEC-003 v5 merging), on a new branch from main:
1. Bryan approves this version; SPEC-003 v5 is on main.
2. In `src/tests/epic/make_evals.py`, add the variants for VER-20 to VER-26:
   - a POL-001 v2 whose SET-01 platform changed (VER-20);
   - an ARCH-001 whose resolution line uses the older form, with a POL-001 v2 whose SET-01 is unchanged
     (VER-21, VER-22): pass the raw entry `architecture.mandated_platforms=POL-001#SET-01` to `resolution()`;
   - an ARCH-001 with no `Policy resolution:` line in any row (VER-23);
   - NFR-003 in PRD-001, DEC-08 citing NFR-001 and NFR-003, and an existing EPIC-001 refining FR-003,
     NFR-001 and NFR-003 (VER-24); DEC-08 resolved by a missing ADR-005 (VER-25);
   - DEC-08 about payment receipts, resolved by POL-001#SET-01 and citing FR-010 (VER-26).
   Check each variant's premise, regenerate, and check the graders offline with scripted good and bad results.
   New case names start with `epic-`.
3. Run the new cases on SKL-004 v3 (`--runs 1 --ablation none`) and confirm the new behavior fails.
4. Write SKL-004 v4 through `/plugin-dev:create-plugin`: `references/selection.md` (check 3, the NFR review
   signal, precedence), `SKILL.md` (step 4, the legacy question in "Decisions that belong to the user", step 9).
   Bump `provenance.yaml` and `metadata.devforgeai-version` together. Update VER-13 (k) in
   `docs/runbooks/epic-ver-13-checks.md` to "automated by VER-20".
5. Validate (`plugin-validator`, `skill-reviewer`), then the whole suite once and 3 runs with the baseline,
   each bound by `record_revision.sh`. Record the results in §9, then open the PR.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| Epics for every current-release requirement | Starts delivery on unsettled foundations; ADR-002 puts architecture first |
| Read readiness from the architecture skill's reply | The reply misreported readiness once in three runs; the ARCH file was right every time |
| Treat a PRD with no ARCH as "nothing blocking" | Every requirement would look ready without anyone having looked. The skill hands back instead |
| Drop policy check 4, matching SPEC-003 §4 exactly (version 2) | Loses detection of two approved policies mandating platforms for the same capability. Narrowing it to the same capability, as SV-04 does, keeps that detection and allows normal layering (Bryan, 2026-10-01) |
| Drop policy check 3 and only warn on a version mismatch (version 2) | Loses detection of a changed mandated platform. The resolution-line fallback keeps it, and costs nothing when the versions match (Bryan, 2026-10-01) |
| Attach NFRs whose priority or release is null anyway (version 2) | Decides what belongs to the PRD owner. prd writes quality-round and policy NFRs as null, so that is upstream's to change, and the epic skill reports them as undecided (Bryan, 2026-10-01) |
| A changed mandate reported as unknown, as in version 3 (version 4) | SPEC-003 v5 reopens the question, so the requirement is blocked like any open question. Unknown is kept for inputs the skill can't establish (Bryan, 2026-10-01) |
| A record in the older form treated as unknown, or as changed (version 4) | SPEC-003 v5 asks a user if one is present and otherwise counts it; the epic skill follows, so the two skills agree on readiness. The exception is limited to that exact form; a missing record stays unknown (Bryan, 2026-10-01) |
| The NFR review signal ahead of `later`, `wont` or `undecided` (version 4) | Breaks the one-next-action rule. The row still lists the epics, so the reader sees them (Bryan, 2026-10-01) |
| A read-only selection script now (version 2) | It would make readiness and the rows deterministic and unit-testable. But it changes §5's no-shell rule and overlaps PRD-001 FR-018 (`devforgeai check`), so it is deferred to FR-018 (Bryan, 2026-10-01) |
| Select by priority (Musts only) | MoSCoW keeps Shoulds and Coulds in the release as contingency; priority orders, release selects |
| Extend or rewrite existing epics | Needs a change-control design; v1 reports covered requirements and adds new epics only |
| Stop until the ARCH is amended whenever the PRD version changes | A priority-only PRD change would force an amendment with nothing to change, and a confirmed reuse, which writes nothing, would never clear it. A review record clears it instead |
| Validate with `devforgeai check` when on PATH | The CLI doesn't exist, and an unrelated `devforgeai` was found on PATH; self-check only |

## 13. Open questions

- None. The NFR review signal deferred in version 3 is part of version 4 (§4).

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-27 | claude-code (session a2b1015f-3340-4c70-80ed-b674d486fadd) | Baseline for this workspace, reset from SPEC-004 v4 on Bryan's decision, since nothing has been built from it here. Versions 1–2 are in DevForgeAI-SDF2's git history (docs/specs/spec/SPEC-004.md, main at ef78b83); v4, with its Change Log for v3–v4, is kept at docs/archive/2026-09-27-spec-reset/SPEC-004-v4.md. Removed as DevForgeAI-SDF2 history: §9's run records (now not run; the shared fixture is kept), the SKL-003 v5 and SPEC-003 v7 references in §4, §10 and §11 (the review record is part of SPEC-003 from v1), and PR #10. §10 and §11 step 6 now say the change that ships this skill updates the architecture skill's hands-off-to-epic case if needed. Links: SPEC-003 and SPEC-002 at v1. Awaiting Bryan's approval | frontmatter, §4, §9, §10, §11 |
| 1 | 2026-09-27 | Bryan | Approved | status |
| 1 | 2026-09-28 | claude-code (session 383de882-2b59-4b3b-808b-83bb1ab93b9b) | Status update only, at Bryan's instruction, with no version bump: §9 records that the skill is built (SKL-004 v1, PR #5) and deployed, and its fixture checks and eval results. No requirement, behavior or VER item changed | §9 |
| 2 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Bryan's decisions of 2026-10-01 on the epic skill's validation findings (D1–D5). D2: policy check 4 fails only when another approved policy mandates the same capability, unless it is a permitted project override. D3: check 3 passes on an equal link version, and otherwise only when the ARCH's latest resolution line still holds the setting's current platform and capability; the known limit is stated. D1: a null priority or release stays undecided, and the shared fixture gains NFR-002 at null/null. D4: no selection script; deferred to FR-018. D5: one combined cycle with SKL-004 v2. Also: a DEC cites a requirement only through this PRD's ID; a matching DEC resolved by a policy setting that passes the check answers a `[NEEDS ADR]` marker (SPEC-003 BEH-07); superseded and deprecated ARCHs are ignored; a link version newer than the PRD's is ERR-03; an empty resolved_by is unknown; a later requirement's null priority isn't undecided; an eligible NFR that no new epic attaches gets an "already refined" row; the report names every FR once and every NFR at least once; ERR-05 is now "everything eligible is covered", and the new ERR-08, "nothing eligible yet", names no story step; BEH-11 checks for the story skill at `${CLAUDE_SKILL_DIR}/../story/SKILL.md`, the form verified with the shipped skill. §9: the shared fixture takes the current prd and architecture output shape; VER-01, VER-03, VER-13 and VER-14 changed; VER-16 to VER-19 added. Links: SPEC-003 v4 and SPEC-002 v3 re-read, and ADR-003 v2 added. Awaiting Bryan's approval | frontmatter, §1, §2, §4, BEH-03, BEH-04, BEH-05, BEH-11, ERR-02 to ERR-05, ERR-08, §9, VER-01, VER-03, VER-13, VER-14, VER-16 to VER-19, §10, §11, §12 |
| 2 | 2026-10-01 | Bryan | Approved | status |
| 2 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Record-only update, with no version bump: §9 records SKL-004 v2's structural checks and plugin-dev validation, the new and changed cases run on SKL-004 v1 (four of five predicted failures reproduced), the one-run suite (18 of 18 at 1.00) and the bound 3-run (18 of 18 at 0.8 or above, mean Δ +0.52). No item changed | §9 |
| 2 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Record-only update, with no version bump: §9 records Bryan's approval of SKL-004 v2 (2026-10-01), its merge in PR #43 and deployment in plugin 0.8.0, and that the run folders moved from the worktree to the main checkout's `tmp/eval-results/`. No item changed | §9 |
| 3 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Wording only, from PR #43's skill review and Bryan's decisions of 2026-10-01 (spec v3 for wording; no new NFR review signal, recorded in §13; one run, then a 3-run). §4 Grouping and BEH-07: attaching an eligible NFR to every new epic it constrains is the proposal's default; the rule is at least one new epic unless an active epic already refines it, and a stated or changed grouping is limited only by §4's rules. BEH-07 also states what happens when a stated grouping leaves an eligible FR unplaced and no one can be asked. ERR-05 and BEH-11: "already has an epic" and "already refine" replace "covered", which is kept for FRs. §4 check 3: an ARCH with no resolution line at all is treated as one that no longer applies the setting. No VER item or fixture changed. Awaiting Bryan's approval | frontmatter, §4, BEH-07, BEH-11, ERR-05, §9, §11, §13 |
| 3 | 2026-10-01 | Bryan | Approved | status |
| 3 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Record-only update, with no version bump: §9 records SKL-004 v3's one run (17 of 18 at 1.00; VER-03 0.80 from a grader conflict written for version 2), the grader fix and its one-case check (1.00), and the bound 3-run (18 of 18 at 1.00, mean Δ +0.51). No item changed | §9 |
| 3 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Record-only update, with no version bump: §9 records Bryan's approval of SKL-004 v3 (2026-10-01), its merge in PR #47 and deployment in plugin 0.8.1, and the 3-run attempt that the account's session limit stopped. No item changed | §9 |
| 4 | 2026-10-01 | claude-code (session 96018bc1-5ee7-423f-93a4-da37a8b6c392) | Bryan's decisions of 2026-10-01, following SPEC-003 v5 §4. Check 3: a policy version bump alone never blocks; a changed platform or capability makes the requirement blocked by its DEC and hands back to the architecture step; a record in the older form `architecture.mandated_platforms=POL-NNN#SET-NN` is an evidence gap (ask a user if present, one question per resolver; no user: it counts), limited to that exact form; a missing record stays unknown; checks 1, 2 and 4 and the ARCH link are kept. A DEC's state is read before its resolver. A policy setting resolving a different question never clears a marker. The NFR review signal: a blocked or unknown NFR that an active existing epic refines lists `refined by EPIC-NNN` and, as the first reason with an action, asks to review that epic's work; precedence follows the existing reason order. VER-13 (k) automated by VER-20; VER-20 to VER-26 added; the known limit and the reopen backlog item removed (SPEC-003 v5). SPEC-003 link moved to v5, gated on its merge. Awaiting Bryan's approval | frontmatter, §2, §4, BEH-04, BEH-05, BEH-06, §9, VER-13, VER-20 to VER-26, §10, §11, §12, §13 |
| 4 | 2026-10-01 | Bryan | Approved | status |
