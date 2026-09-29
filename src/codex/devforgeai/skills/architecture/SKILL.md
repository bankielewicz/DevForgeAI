---
name: architecture
description: "Performs DevForgeAI Architecture Definition for a PRD. It identifies the architectural questions separate epics must share, settles each only by an explicit decision, an accepted ADR or approved policy, and writes an architecture description (ARCH) with ADRs and a report of which requirements are ready for epic work. Use after a PRD is written, when deciding system architecture, components, data ownership or deployment, or when resolving NEEDS ADR markers. Load this skill before any repository discovery. Before loading, access only contract document paths or user-approved inspection scope; never list or search the repository root."
metadata:
  devforgeai-id: "SKL-003"
  devforgeai-version: "5"
---

# Architecture

Perform the Architecture Definition step for one PRD. Identify the architectural questions that
separate epics must share, settle each one only by policy, an accepted ADR or the user's explicit
decision, and write `docs/specs/arch/ARCH-NNN.md` plus any ADRs. The epic workflow reads the ARCH
mechanically and writes epics only for requirements the readiness rule reports ready. A question
marked resolved without a real decision lets separate epics build conflicting foundations.

Three rules shape everything below:
- **Readiness is decision-specific.** A requirement is ready only when every blocking question that
  cites it is resolved. An ADR or policy setting resolves the question it answers, never "the
  requirement".
- **Decisions are accepted one by one.** Confirming the outcome (reuse, amend or create) accepts
  none of the decisions inside it.
- **Evidence is honest.** Inspection is bounded and recorded; observed practice isn't policy; missing
  evidence is stated as unknown.

## Inputs

- A PRD ID such as `PRD-002`, supplied with the DevForgeAI Architecture skill mention
  (for example `$devforgeai:architecture PRD-002` in Codex CLI), or in the conversation. If absent, follow
  step 2. Never accept a file path; if given one, ask for the ID.
- Read by contract: PRDs in `docs/specs/prd/` (read-only), ARCHs in `docs/specs/arch/`, ADRs in
  `docs/specs/adr/`, policy in `docs/specs/policy/` and `.codex/devforgeai.local.md`. Reach them by
  these paths; the local preference file is read-only during Architecture and is never created or
  edited. Never list the working directory or the repository root to find them.
- Code and configuration: only inside the inspection scope the user names
  ([references/inspection.md](references/inspection.md)).
- Templates: `assets/arch.md` and `assets/adr.md`.

Resolve assets and references from the actual directory containing this loaded `SKILL.md`.
Resolve `docs/specs/` and `.codex/devforgeai.local.md` from the consuming project root. Use the
host file and shell tools for scoped reads, searches and edits; no tool approvals are granted by
this skill.

Never run a `devforgeai` command: that CLI doesn't exist, and a program with that name on PATH can't
be trusted.

## Decisions that belong to the user

The ARCH records decisions; it never makes them. These are the user's:

- **Which PRD**, when no ID was given.
- **Which ARCH**: reuse or amend an existing one that covers the system, or create another.
- **The inspection scope**, and any read outside it.
- **The answer to each architectural question**: an option you presented, or confirming that an
  existing accepted ADR answers it. Also whether a question is non-blocking.
- **The outcome**: reuse, amend or create.
- **Superseding an accepted ADR.**
- **Saving a draft** when the user stops mid-session.
- **Changes to the PRD**: you only propose them; the PRD owner decides.

Write a decision only when the user made it explicitly, in an answer or in the request. The request
can answer only these:
- which PRD;
- which ARCH, and the outcome, but only by naming the outcome for that ARCH ("amend ARCH-001",
  "reuse ARCH-001; I confirm reuse", "create a new ARCH"). Asking to define or update the
  architecture, or to reuse a component or service, confirms no outcome;
- the inspection scope, and that a question is non-blocking;
- that a named accepted ADR answers a named question ("ADR-004 settles the identity provider").

An answer to an architectural question stated in the request ("use Keycloak", "reuse our current
auth service") is a preference: record it in the DEC's `notes` and recommend it when you ask. It
never becomes an ADR until the user picks it. The one exception to all of this is policy: an
approved mandated platform that answers exactly a question resolves it without asking.

**Asking.** Use `request_user_input` when it is available and permitted by the active mode and tool
instructions. Ask at most 3 questions per batch, within any stricter host limit, with 2–3 mutually
exclusive options per question. Put the recommended option first and mark it "(Recommended)".
If `request_user_input` is unavailable or not permitted, ask one concise plain-text question with
the full choices and end your turn; an unanswered gate stays open. When the full choice set cannot
fit the tool, ask with a numbered plain-text list and end your turn. For an
asynchronous tool, its return is not the user's answer: wait before dependent work. Silence,
timeout, preselected options and a pending question are never confirmation. Use at most
`interview.max_calls` calls (step 1; default 8) unless the user asks for more; questions left when
the budget runs out stay open. Write nothing that a pending answer affects until the answer arrives.

**"Proceed without questions."** When the request says to proceed without questions (or "don't ask
me anything", "decide nothing"), ask no decision questions:
- no question is newly resolved except by a mandated platform. Resolutions already in an ARCH being
  amended follow [readiness.md](references/readiness.md), "State changes when amending";
- `outcome` stays `null` unless the request names it for this ARCH (above);
- write no ADR at all;
- read nothing outside the inspection scope, and record the gap as an unknown.

Every other step still runs, and a new ARCH is still written when none covers the system. This
never answers the two gates: **which PRD**, and **reuse, amend or create when an existing ARCH covers
the system**. A gate is answered only by an explicit answer to that gate, in the request ("amend
ARCH-001") or in reply to your question; name where the answer came from. If a gate is open, ask it
and write nothing.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Resolve policy (R1, R2)
- [ ] 2. Select the PRD
- [ ] 3. Read the PRD; apply R3 and R4
- [ ] 4. Select or create the ARCH
- [ ] 5. Inspect within the scope
- [ ] 6. Identify the architectural questions and components
- [ ] 7. Resolve each question explicitly
- [ ] 8. Propose and confirm the outcome
- [ ] 9. Write the ARCH and ADRs
- [ ] 10. Validate every file written
- [ ] 11. Compute readiness, report and hand off
```

### 1. Resolve policy (R1, R2)

Follow [references/policy.md](references/policy.md) with the framework defaults in
[references/defaults.md](references/defaults.md). This step comes first, before any question.
1. Read `docs/specs/policy/POL-*.md`. If the folder is missing, use the framework defaults.
2. Check every approved document against the checklist in policy.md. Skip draft and in-review
   documents, and report them.
3. **Any violation stops the skill (ERR-02).** Before writing anything, name the policy file, the
   setting (`SET-NN` and its key) and the rule broken, and say nothing was written. Never fall back
   silently.
4. Resolve `interview.max_calls` and `architecture.mandated_platforms`, and read local preferences.

### 2. Select the PRD

- **An ID was given.** Read `docs/specs/prd/<ID>.md`. If it doesn't exist (ERR-01), list the PRD IDs
  that do exist with their titles and status, write nothing, and stop.
- **No ID.** List every PRD with its ID, title and status, and ask which one to use. Never guess,
  even when only one exists. With no answer, write nothing.

### 3. Read the PRD; apply R3 and R4

Read its frontmatter (`status`, `version`, `owner`, `stage`, `operating_context`), its functional and
non-functional requirements (constraints included), and every `[NEEDS ADR]` and
`[NEEDS CLARIFICATION]` marker. Every PRD link you add uses the version you read here; links on
existing items keep theirs. Never edit the PRD.
- **Draft PRD** (`status` other than `approved`): warn now, before any question or write, that the
  result is a proposal because the PRD may still change. Repeat the warning in the handoff.
- **R3 and R4:** the operating context is the one the request states, otherwise the PRD's
  `operating_context` (policy.md R3). If it is still unknown, evaluate policy as `production`. Note
  the required quality categories for section 2.
- **Product questions stay the PRD owner's.** A `null` priority or release, or a
  `[NEEDS CLARIFICATION]` marker, never becomes an architectural question
  ([references/readiness.md](references/readiness.md)).

### 4. Select or create the ARCH

Read the frontmatter of each `docs/specs/arch/ARCH-*.md`: `system`, `status`, `version`, `outcome` and
its PRD links. An ARCH **covers this system** when its frontmatter links this PRD, or its `system`
names the product this PRD's title names.
- **None covers this system:** a new ARCH is created at step 9, with the next free ID. No question.
- **One covers it:** compare what it was defined against with the PRD now: the PRD version it cites,
  new or changed requirements and `[NEEDS ADR]` markers, and resolvers that were superseded.
  Recommend **reuse** (it covers the PRD unchanged) or **amend** (it needs new or changed questions
  or components), with those reasons, and ask. Offer a separate new ARCH only as a
  non-recommended option. Never create a second baseline automatically, and write nothing until the
  user answers.
- **Several could apply** (ERR-04): list them with their systems and ask. Never pick one silently.

A choice of reuse or amend, in the request or an answer, also confirms that outcome for step 8,
unless step 8 finds another outcome is needed: then say why and ask again.

### 5. Inspect within the scope

Follow [references/inspection.md](references/inspection.md). The scope is what the user named; if
nothing was named, it is `[]` and no code is read. Every path you read, list or search is inside the
scope, apart from the documents read by contract. Ask before going outside it (ERR-03); with no user
or a "no", record the unknown.

Record an EVD for every project source you consult (inspection.md, "Recording evidence"): the PRD
(`kind: prd`, `classification: context`), each other existing ARCH, each ADR that bears on this PRD's
questions, each applied policy setting, and each code or configuration source. When the evidence is insufficient, write a `[NEEDS CLARIFICATION]`
marker and never recommend reuse on assumption.

### 6. Identify the architectural questions and components

Follow [readiness.md](references/readiness.md):
- Record a DEC for each question separate epics must share: component boundaries and
  responsibilities, data ownership, major interactions and interfaces, deployment, and how quality
  requirements are met. Every `[NEEDS ADR]` marker becomes a DEC.
- Each DEC cites **every** affected requirement, at the PRD version examined, and is blocking unless
  the user says otherwise. Leave feature-level detail (API fields, migrations, class structures) to
  specs.
- Describe the components separate epics must share as CMP items, with a Mermaid overview: at least
  one, even with no user. They show the proposed shape; where a boundary is a choice rather than a
  given, a DEC records that choice (readiness.md). Link each CMP to the NFRs and constraints it
  serves. Each mandated platform (step 1) appears as the CMP that provides that capability, carrying
  the setting's `constrains` link: the one place R5 allows.
- Give each new CMP its `kinds` from output-rules.md: one or more of `user-interface`, `service`,
  `platform`, `api`, `relational-store`, `data-store` and `external`. A component can have several
  (a service that also exposes an API has `service` and `api`). When a kind is uncertain, ask
  using the **Asking** rules above: `request_user_input` when permitted, otherwise a plain-text
  question and wait. With no user, record only kinds the PRD or the evidence states; if none is
  certain, leave `kinds` out and add `[NEEDS CLARIFICATION: kinds of CMP-NN]` to section 8.
  When amending, existing components stay unchanged, with or without `kinds`.
- **When amending**, add new items after the existing ones, leave existing items unchanged, reopen
  any DEC whose resolver no longer counts, and give a new requirement that an existing question
  affects a new DEC of its own (readiness.md, "State changes when amending").

### 7. Resolve each question explicitly

Use only the three means in [readiness.md](references/readiness.md), in this order:
1. **Mandated platforms:** a setting that answers exactly a question resolves it as policy, with no
   question and no ADR.
2. **Existing accepted ADRs:** when one may answer a question, ask the user to confirm it answers
   exactly that question.
3. **The user's decision:** for each remaining question, present 2 architecture options with
   trade-offs plus *Decide later* when using `request_user_input`. If a faithful choice requires 3
   architecture options plus *Decide later*, use a numbered plain-text list and end your turn; do
   not drop or merge an option to fit the tool. Each explicit pick becomes a new ADR with
   `status: accepted`. *Decide later* keeps the question open; write a proposed ADR only if the user
   asks to record the deferral.

`approved_by` on an accepted ADR is the deciding user's name. If the conversation hasn't named them,
ask who is deciding, offering the PRD owner as the first option. A preference stated in the request
is recorded in the DEC's `notes` and made the recommended option; it is not a decision until picked.
With no user, only means 1 applies.

- **PRD conflicts (BEH-12):** when architecture shows a requirement is infeasible, too costly or in
  conflict (for example with a mandated platform), write the proposed change in section 7 and in the
  handoff, addressed to the PRD owner. Never edit the PRD: the owner amends it.
- **Superseding an accepted ADR** only on the user's explicit approval (output-rules.md).
- **Stopping mid-session** (ERR-06): offer to save a draft ARCH with every unanswered question open
  and `outcome: null`. Write it, or nothing, as the user chooses.

### 8. Propose and confirm the outcome

Propose one outcome, with reasons:
- **reuse:** the existing ARCH covers the PRD unchanged;
- **amend:** the existing ARCH needs new or changed questions or components;
- **create:** no ARCH covers the system.

Using a mandated or existing platform or component is not a reuse outcome. Ask the user to confirm,
unless the request or step 4 already did. Write `outcome` only when it is confirmed; otherwise it
stays `null`. Confirming the outcome accepts no decision.
- **Reuse confirmed and the ARCH's PRD link is older than the PRD's version:** write the review record
  (output-rules.md), and nothing else.
- **Reuse confirmed and the link already equals the PRD's version:** write nothing; go to step 11.

### 9. Write the ARCH and ADRs

Read [references/output-rules.md](references/output-rules.md) before writing.

**New ARCH.**
1. **ID and path:** the highest `NNN` among `docs/specs/arch/ARCH-NNN.md` plus one, or `ARCH-001`.
   Create the folder if it is missing. Never ask for or accept a file name.
2. **Template:** build from `assets/arch.md`. Keep every heading, replace every
   placeholder and example item, and delete every `<!-- -->` comment.
3. **Frontmatter:** `status: draft`, `version: 1`, `created` and `updated` today; `owner` from the
   request, otherwise the PRD's owner; `authors` the owner and `"codex"`; `generated_by` with
   `tool: "codex"`, `model:` the exact model ID exposed by the host and `session:` the actual host
   session/thread ID. Never infer a model from a family name or copy the source author's identity.
   If a value is unavailable, use `"unknown"`, add `[NEEDS CLARIFICATION: host model/session identity unavailable]` in section 8,
   disclose incomplete provenance in the reply, and leave validation unresolved; placeholder text does not satisfy BEH-13 or
   VER-14;
   `reviewed_by: []`, `approved_by: ""`, `approved_on: null`; every `hash: null`. `upstream` holds
   the PRD link at the version read in step 3, plus the `informed_by` policy links R5 puts in
   frontmatter. Set `system` (the product this PRD's title names), `outcome` and
   `inspection_scope`.
4. **Change Log:** one row, author `codex (session <value>)`, where `<value>` is exactly
   `generated_by.session` (the actual host session/thread ID, or `unknown` when unavailable), and whose change text
   ends with the policy resolution line, for example `Initial draft for PRD-001 v1. Policy
   resolution: interview.max_calls=8 (default); …`.

**Amending** and **the review record** follow output-rules.md exactly.

**ADRs.** One per explicit decision (`accepted`), and one per deferral the user asked to record
(`proposed`), from `assets/adr.md` (output-rules.md, "ADRs"). Write the ADR before
the DEC that it resolves.

Never modify a PRD, BRN or policy document, and never modify an existing ADR except to record a
supersession the user explicitly approved.

### 10. Validate every file written

Read each written file back and check it against the **Self-check list** in
[output-rules.md](references/output-rules.md), item by item. Fix each problem and check again, at
most three attempts. If errors remain (ERR-05), restore what output-rules.md says, end with a
validation-failure report (the file paths, the unresolved errors, what was restored), and skip the
readiness handoff. Never present readiness as validated.

### 11. Compute readiness, report and hand off

Compute readiness with the rule in [readiness.md](references/readiness.md) from the ARCH as written
(or as it stands, when nothing was written), reading each resolving ADR's current `status` and
`superseded_by` now.

Write the final reply in this order:

1. This block, filled in. It opens the reply: nothing comes before it, not even the checklist.

   ```
   ARCH-NNN written to docs/specs/arch/ARCH-NNN.md (for PRD-NNN vN; new | amended to version N | review recorded | unchanged)
   Outcome: create | amend | reuse | unconfirmed (proposed: <outcome>)
   ADRs written: ADR-NNN (accepted | proposed), … | none
   Ready for epic work: FR-NNN, NFR-NNN, … | none
   Blocked: FR-NNN (DEC-NN, DEC-NN); NFR-NNN (DEC-NN) | none
   Proposed PRD changes: <requirement: change, for the PRD owner> | none
   Policy resolution: <the resolution line's entries>
   ```

   Ready and Blocked together list every active FR and NFR of the PRD exactly once.

2. Then, briefly: the draft-PRD warning if it applies; each open question with its DEC ID; any
   resolver that no longer counts and why; each proposed PRD change, addressed to the PRD owner; and
   any finding labelled "observed practice".
3. The next step, as its own paragraph outside any code block. It starts with the words
   **Next step**, names the PRD by its ID and never by its path, and nothing follows it.

For the next step, check whether `../epic/SKILL.md`, relative to this skill, exists and is available
as the DevForgeAI Epic skill in Codex:
- **It exists and is available:** tell the user to select that skill with the PRD ID (for example
  `$devforgeai:epic PRD-NNN` in Codex CLI) for the ready requirements.
- **It is absent or unavailable:** say the DevForgeAI Codex Epic skill is unavailable and that,
  once supplied and available, the user can select it with the PRD ID. Do not imply an unrelated
  skill or a Claude command supplies the missing Codex workflow.

For example: "Next step: the DevForgeAI Codex Epic skill is unavailable. Once it is available,
select it with PRD-001 (for example `$devforgeai:epic PRD-001` in Codex CLI) for the ready requirements;
FR-001 waits for DEC-01 and DEC-02."

Never start epic work, and never write an epic.

When the skill stops without writing (a gate is open, ERR-01, ERR-02, ERR-04), the reply says why and
what the user can do, and leaves out the report block. After ERR-05, the validation-failure report
replaces both the block and the next step.

## Output contract

- **Paths:** `docs/specs/arch/ARCH-NNN.md` and `docs/specs/adr/ADR-NNN.md` in the current project;
  each name is the ID only.
- **Shape:** the two templates, with every heading kept and no author comments.
- **Data:** the ARCH holds only the `components`, `decisions` and `evidence` collections, with their
  defined fields ([output-rules.md](references/output-rules.md)).
- **Decisions:** `outcome` is non-null only when the user confirmed it. A DEC is resolved only by an
  applied mandated platform, an accepted ADR the user confirmed, or a new ADR the user accepted. An
  ARCH is never written `approved`, and no ADR is accepted without the user.
- **Traceability:** every DEC cites the requirements it affects at the PRD version examined; every
  applied policy setting is linked once; every project source consulted is an EVD.
- **Readiness:** reported per requirement by the rule, never stored and never guessed.

## Examples

**No user, no ARCH yet.** "Do the architecture for PRD-002. Proceed without questions." The skill
resolves policy (none, so defaults) and reads PRD-002 (approved, version 3, with
`[NEEDS ADR: calendar integration; affects FR-004]`). No ARCH exists, so it will create one. No scope
was named, so no code is read. It records a DEC per shared question, each citing the requirements it
affects, all open; writes no ADR; leaves `outcome: null`; validates; and reports FR-004 as blocked by
its DEC, then the next step.

**An ARCH already covers the system.** "Run architecture for PRD-002." ARCH-001 covers the same
clinic system and cites PRD-002 version 2; version 3 adds a `[NEEDS ADR]` marker. The skill
recommends amending ARCH-001, with that reason, asks, and writes nothing until the user answers.

**A decision made interactively.** For "Which identity provider handles sign-in?" the skill offers
three providers with trade-offs against the security NFRs, recommending one. The user picks it, so
the skill writes ADR-004 (`accepted`, `approved_by` the user) and sets the DEC's
`resolved_by: [ADR-004]`. The user then confirms `create`; that resolves nothing else, so the
session-revocation question stays open.

## References

- [references/policy.md](references/policy.md): read at step 1. Policy checks, precedence, R3 to R5,
  and the resolution line. Kept byte-identical with the Codex PRD port's corresponding source file.
- [references/defaults.md](references/defaults.md): read at step 1. Framework defaults and the quality
  floor per operating context. Kept byte-identical with the Codex PRD port's corresponding source file.
- [references/inspection.md](references/inspection.md): read at step 5. The inspection scope, allowed
  commands, leaving the scope, and evidence classification.
- [references/readiness.md](references/readiness.md): read at steps 6, 7 and 11. Which questions to
  record, the three means of resolution, and the readiness rule.
- [references/output-rules.md](references/output-rules.md): read before step 9. Keys, fields, links,
  amendment, the review record, ADRs, ERR-05, and the self-check list used at step 10.
