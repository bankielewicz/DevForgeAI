---
id: SPEC-003
type: spec
title: "Architecture Definition skill (MVP)"
status: draft
version: 5
created: 2026-09-23
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
  - {id: STORY-003, relation: specifies, version: 2, hash: null}
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 7, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 7, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 7, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: ADR-002, relation: constrains, version: 2, hash: null, note: "accepted: the Architecture Definition step"}
  - {id: ADR-003, relation: constrains, version: 2, hash: null, note: "accepted: configuration contract v1"}
  - {id: SPEC-002, relation: informed_by, version: 10, hash: null, note: "consumes the prd skill's downstream contract (SPEC-002 §5)"}
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
| `evidence` (`EVD-NN`) | Every project source consulted for architecture analysis, with its `kind` and, independently, a `classification`: observed, policy, decided or context |
| §7 | Requirement changes proposed to the PRD owner |

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
  devforgeai-version: "3"
```

- **The name must be exactly `architecture`.** The prd skill's handoff looks for `${CLAUDE_PLUGIN_ROOT}/skills/architecture/SKILL.md`.
- **Tools:**
  - code inspection: read-only, and every path read, listed or searched is inside the inspection scope. Read, Glob and Grep when available, otherwise read-only shell commands (ls, find, grep, cat, head) with explicit paths inside the scope; never a whole-repository listing or search. The project documents read by contract (docs/specs/prd/, arch/, adr/, policy/ and .claude/devforgeai.local.md) are outside this rule, and validation commands (devforgeai check) are separate from inspection;
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
    rule: "Inspect only the components or directories the user names (inspection_scope). Code inspection is read-only, and every path it reads, lists or searches is inside inspection_scope: use Read, Glob and Grep when available, otherwise read-only shell commands (ls, find, grep, cat, head) with explicit paths inside the scope, with no redirection, no writes and no running or building project code; never list or search the whole repository. The project documents read by contract (docs/specs/prd/, arch/, adr/ and policy/, and .claude/devforgeai.local.md) are outside this rule, and validation commands (devforgeai check) are separate from inspection. References such as imports and configuration may be followed only within that scope; ask before going outside it. Record every project source consulted for architecture analysis as an EVD item, with the version and status examined where applicable, classified independently of its kind as observed (code or configuration directly inspected within inspection_scope), policy (an approved, active, applicable setting), decided (an accepted, non-superseded ADR) or context (any other consulted input or historical material, including the input PRD, existing ARCHs, proposed, rejected or superseded ADRs, and documentation claims not corroborated by the implementation). Context establishes neither implemented behavior nor an accepted decision, and no classification resolves a DEC by itself. When evidence is insufficient, say so explicitly with a [NEEDS CLARIFICATION] marker, and never recommend reuse on assumption."
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
    handling: "Stop. Restore only what can't stand unvalidated: every status and approval field (approved_by, approved_on) this write changed, back to its value before the write (a new ARCH stays draft; a new ADR the user accepted becomes proposed with empty approval fields and is kept); the DEC state and resolved_by that depended on a restored ADR; and one matching audit record (Change Log row, and Status history row for an ADR). Keep the user's architectural choices and unrelated content. End with a validation-failure report; skip the readiness handoff and never present readiness as validated"
    user_result: "A validation-failure report: the file paths, the unresolved errors and what was restored; no readiness presented as validated"
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
| Behavioural (a): case thresholds | **Passed**, 2026-09-24, Claude Code 2.1.281, 3 runs per arm against the no-plugin baseline. The 12 architecture cases (VER-01 to VER-11, VER-14) each scored ≥ 0.8 in `results/2026-09-24T02-03-06-267Z` (`--tag architecture`: score 0.989, mean Δ +0.65). org-a-policy 1.00 (Δ +0.92, `results/2026-09-24T01-45-49-046Z`); org-b-policy 1.00 (Δ +0.58, `results/2026-09-24T01-55-07-371Z`). Full-plugin run `results/2026-09-24T02-25-22-717Z`: 40/40 cases, score 0.999, mean Δ +0.58 |
| Behavioural (b): individual grader failures (with-plugin arm) | Tag run: superseded-adr `names-superseded-adr`, 2 of 3 runs. Full-plugin run: brainstorm hands-off-to-prd `criteria` (llm judge), 1 of 3 runs. The org-a and org-b runs: none |
| Behavioural (c): manual checks done | VER-12 (f): `references/policy.md` and `defaults.md` byte-identical to the prd skill's. VER-12 (h): SKILL.md 249 lines, description 460 characters. VER-13: deployed-plugin SHA-256 `05a8356f2f857e553e2e252e00054f0b6e26bf3a94a6275de161b143587085e2` before org-a-policy, between the runs and after org-b-policy, with `git diff src/` empty each time. VER-12 (a), (c) to (e), (g) and an extra ERR-04 check (several ARCHs), 2026-09-24, one fixture copy per variant: **passed**. VER-12 (b): **partial** (row d). The build session supplied every answer on Bryan's instruction; decider names in the fixture ADRs are test data. VER-12 (c) passed against BEH-02; SKILL.md step 3.2's early warning did not appear before the handoff |
| Behavioural (d): manual checks partial | VER-12 (b): the scope held (content read only inside `services/auth`), `inspection_scope` was recorded, EVD kinds and classifications were correct (code `observed`; the README and the PRD `context`), and the two out-of-scope references were recorded as `[NEEDS CLARIFICATION]` markers naming their paths. The skill never asked before leaving the scope: it chose not to follow the references, so the "asks before leaving the scope" clause is unexercised. It also listed every file path in the project once, names only, before inspecting |
| Behavioural (e): ERR-05 | **Passed once, through the CLI path with a test stand-in** (a scratch `devforgeai` that always returns one unfixable error for `check --json`). With one decision accepted before validation, it stopped after 3 attempts (6 logged calls, 2 files each), listed the file and the error, kept ARCH-001 `draft`, left the new ADR `proposed` (not removed; DEC-01 back to open) and reported nothing ready. The self-check path is not exercised (deferred to STORY-004). During rollback it also rewrote text beyond statuses |
| Behavioural (f): superseded-adr diagnosis | `results/2026-09-24T11-45-56-054Z` (`--keep-temp --ablation none`, run without `--threshold`, so the default 1.0 marks the case not passed): score 0.94; `names-superseded-adr` failed in 1 of 3 runs. This diagnostic run's failing reply named ADR-002 and its successor but said "replaced", not "superseded": the one-line, 120-character grader, not an omission. The two failures in the tag run lost their transcripts, and their causes are unknown. All 3 ARCH files were correct. Separately, one passing run's reply misreported NFR-001 as blocked by DEC-01, which doesn't cite it; no grader checks that. No fix applied yet |
| Behavioural (g): SKL-003 v2 grader checks, offline | 2026-09-24, before any paid run. superseded-adr's regex graders, run through node RegExp: 84 checks against the 3 kept diagnostic replies and ARCH files and 12 independently written positive, negative, negated and reversed examples, all as expected. The llm readiness grader, applied by Haiku judges to 17 texts (the 3 kept replies and 14 independent examples): a first pass (17 of 17) had descriptive item IDs that could leak answers, so it was rerun blind: neutral IDs, a different shuffle per pass, answer files locked. Three blind passes gave 17 of 17 each, unanimous on every item. Each pass judged all items in one call, not one call per item |
| Behavioural (h): SKL-003 v2 manual reruns (commit feec61c) | 2026-09-24, driven by the build session on Bryan's instruction. VER-12 (b), the out-of-scope request in two fresh copies: the skill asked before reading shared/config.js; on yes it read only that file, added shared/config to inspection_scope and recorded an observed EVD; on no it read nothing outside the scope and recorded an explicit unknown naming the path. In both runs an early `ls -la …; ls services`, apparently during step-1 contract discovery, listed the project root and services/. Per Bryan's ruling, step-1 discovery is covered only for the named contract folders, so both runs **fail the command-path clause (minor)**: names only, one level, no code read, no evidence taken. The ask, yes and no parts pass. VER-12 (c) **failed**: the draft-PRD warning appeared only in the handoff, not when the PRD was read, and the run listed the whole repository with `find .`. VER-12 (i), ERR-05 through the stand-in CLI path: **passed** (3 attempts; only statuses, approval fields, DEC-01's state and audit rows restored; validation-failure report; step 11 skipped). The self-check failure path is not exercised. VER-12 (a), (d), (e), (g) and the ERR-04 check carry forward from build 469e984. The v2 full-plugin run and the Organization A/B checksum sequence have not run, pending Bryan's decision on these failures |
| Behavioural (i): SKL-003 v3 manual reruns (commit 36328fc) and a failed check | 2026-09-24, fresh copies, driven by the build session on Bryan's instruction. VER-12 (b), answer yes and answer no: **passed every clause**. Contract discovery used exact paths, the only listing was `find services/auth`, and there was no root or parent listing; the ask, yes and no behaviour was as in v2. VER-12 (c): the whole-repository listing is fixed, but **the warning is still late**. It appeared in the final handoff and in ARCH §1, not right after the PRD was read (the first text after the read came before the ARCH write and had no warning). VER-12 (c) therefore **fails** on v3 and is deferred to STORY-004 (Bryan's stop rule: v3 was the last wording round; the follow-up is deterministic enforcement, not wording) |
| Behavioural (j): SKL-003 v3 paid runs (build 36328fc, deployed hash a7105e76610fbc681a3f35080d01020de2c61c2eba395cb9e24abe5a2174cd39) | 2026-09-24, Claude Code 2.1.281, 3 runs per arm against the no-plugin baseline, threshold 0.8. **Full-plugin run** `results/2026-09-24T15-06-52-289Z`: 40/40 cases, score 0.998, mean Δ +0.58. All 12 architecture cases ≥ 0.8 (superseded-adr 0.97, the others 1.00), and no brainstorm or prd regression. Individual with-plugin grader failures: superseded-adr `readiness-mapping` (llm), 1 of 3 runs; brainstorm hands-off-to-prd `criteria` (llm), 1 of 3 runs. That superseded-adr reply lists FR-001 blocked by DEC-01 and FR-002 and NFR-001 ready, and three offline Haiku re-judges each returned PASS, so it is probably a judge false negative (not reproduced; the eval judge's reasons aren't recorded). The new superseded-adr regexes compiled and passed under the real eval engine. **Organization A/B checksum sequence, fresh on the same build:** org-a-policy `results/2026-09-24T16-03-11-734Z` 1.00 (Δ +0.96); org-b-policy `results/2026-09-24T16-11-56-752Z` 1.00 (Δ +0.83); no grader failures. Deployed-plugin SHA-256 `a7105e76610fbc681a3f35080d01020de2c61c2eba395cb9e24abe5a2174cd39` before org-a, between the runs and after org-b, with `git diff src/` empty each time. The v1 hashes in row (c) are historical |
| Demonstration vs ADR-003 | ADR-003's demonstration plan (its Organization A and B pass criteria) is refined by VER-02 and VER-03, not met literally. Under Organization A the identity-provider question resolves by `POL-001#SET-01` while session revocation stays open, with no reuse outcome (`outcome: null`). Under Organization B the identity-provider question is an open DEC, not a `[NEEDS ADR]` marker. ADR-003 is unchanged |

**Shared fixture:** one policy-neutral PRD (`PRD-001`) in which FR-001, "users sign in", is affected by two
architectural questions (a `[NEEDS ADR]` marker for the identity provider, and NFR-001 requiring session
revocation), with no identity ADR. It's written fresh and checked against `prd.schema.json`. Unless a case says
otherwise, the prompt says to proceed without questions, so evals exercise the no-user path.

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Shared fixture, no policy, no ARCH: writes docs/specs/arch/ARCH-001.md with a DEC for the identity provider and a DEC for session revocation, both open and citing PRD-001#FR-001; an EVD with kind prd and classification context records the PRD; outcome null; the handoff lists FR-001 as blocked. Eval case creates-arch: regex on the file and last_message."
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
      - {id: STORY-003, item: AC-01, relation: verifies, version: 2, hash: null}
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
      - {id: STORY-003, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-03
    status: active
    obligation: "Demonstration, Organization B: identical to VER-02 except for Organization B's policy. The identity-provider DEC stays open with an empty resolved_by. Eval case org-b-policy: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-04
    status: active
    obligation: "Unrelated ADR: the fixture adds an accepted ADR-001 about logging that cites PRD-001#FR-001. Both identity DECs stay open, nothing is resolved_by ADR-001, and FR-001 is blocked. Eval case unrelated-adr: regex on the file."
    level: e2e
    covers:
      - BEH-07
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-05
    status: active
    obligation: "Superseded ADR: an existing ARCH-001 has the provider DEC resolved_by ADR-002, which is superseded by ADR-003 (a different topic). The prompt chooses to amend ARCH-001 and confirms that outcome. The handoff names ADR-002 as the superseded resolver (equivalent wording such as 'replaced' is accepted; negated or reversed statements are not) and reports readiness derived from the amended ARCH: FR-001 blocked by DEC-01; FR-002 and NFR-001 ready, because DEC-02 stays resolved by the accepted ADR-001, unless the amendment adds a DEC (DEC-03 or higher) that cites them. Every requirement is listed, no summary contradicts the lists, and no requirement is attributed to a DEC that doesn't cite it. In the amended ARCH-001 the provider DEC is open with an empty resolved_by, DEC-02 is still resolved by ADR-001, and an EVD records ADR-002 with classification context. Eval case superseded-adr: regex on the file and last_message, plus an llm grader for the readiness mapping."
    level: e2e
    covers:
      - BEH-11
    upstream:
      - {id: STORY-003, item: AC-02, relation: verifies, version: 2, hash: null}
  - id: VER-06
    status: active
    obligation: "No user, no acceptance: in VER-01's run, no ADR in docs/specs/adr/ has status accepted, no DEC is resolved_by an ADR, and outcome is null. Eval case no-acceptance-without-user: regex not_contains on the written files."
    level: e2e
    covers:
      - BEH-07
      - BEH-08
    upstream:
      - {id: STORY-003, item: AC-03, relation: verifies, version: 2, hash: null}
  - id: VER-07
    status: active
    obligation: "Existing ARCH-001 for the same system: the skill proposes reuse or amend and asks; no ARCH-002.md is created. Eval case existing-arch-not-duplicated: file_exists false, regex on last_message."
    level: e2e
    covers:
      - BEH-04
      - ERR-04
    upstream:
      - {id: STORY-003, item: AC-04, relation: verifies, version: 2, hash: null}
  - id: VER-08
    status: active
    obligation: "Insufficient evidence: the prompt says 'reuse our current auth service' but names no inspection scope, and no code exists. The outcome is not reuse, and the file has a [NEEDS CLARIFICATION] marker about the missing evidence. Eval case insufficient-evidence: regex on the file."
    level: e2e
    covers:
      - BEH-05
    upstream:
      - {id: STORY-003, item: AC-05, relation: verifies, version: 2, hash: null}
  - id: VER-09
    status: active
    obligation: "Requirement handback: the fixture PRD has an NFR that conflicts with Organization A's mandated platform. ARCH §7 and the handoff propose a change for the PRD owner; PRD-001.md still has its original version line. Eval case prd-change-handed-back: regex on the ARCH and the PRD."
    level: e2e
    covers:
      - BEH-12
      - BEH-16
    upstream:
      - {id: STORY-003, item: AC-08, relation: verifies, version: 2, hash: null}
  - id: VER-10
    status: active
    obligation: "Handoff: the final reply lists ready and blocked requirements with DEC IDs, names the epic workflow and, since this plugin has no epic skill, says it is not built yet. Eval case hands-off-to-epic: regex on last_message."
    level: e2e
    covers:
      - BEH-15
    upstream:
      - {id: STORY-003, item: AC-09, relation: verifies, version: 2, hash: null}
  - id: VER-11
    status: active
    obligation: "A request such as 'explain the architecture of the Linux kernel' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
    upstream:
      - {id: STORY-003, item: AC-10, relation: verifies, version: 2, hash: null}
  - id: VER-12
    status: active
    obligation: "Manual, interactive: (a) each decision is presented with trade-offs and becomes an accepted ADR only after an explicit answer; confirming the outcome accepts nothing else. (b) Bounded inspection of a real directory records EVD items with their kind and classification (observed, policy, decided or context) and asks before leaving the scope; every inspection command in the transcript uses only paths inside the scope or the contract document folders, and none lists or searches the whole repository. A request that needs a file outside the scope (the session lifetime in shared/config.js) is run in two fresh fixture copies: the skill asks before reading it; answered yes, it reads the file, adds it to inspection_scope and records an observed EVD; answered no, it doesn't read it and records an explicit unknown naming the path. (c) A draft PRD shows the proposal warning when the PRD is read, before any question or write, and again in the handoff. (d) Stopping mid-session offers a draft save. (e) An invalid policy stops the skill with the rule named. (f) The architecture skill's references/policy.md and defaults.md are byte-identical to the prd skill's. (g) An unknown PRD ID lists the available PRDs. (h) SKILL.md is within the NFR-001 limits. (i) ERR-05, with a test stand-in for devforgeai that always reports an unfixable error and one decision accepted before validation: the skill stops after three attempts, keeps the choice as a proposed ADR, restores only statuses, approval fields, the dependent DEC state and the audit record, and ends with a validation-failure report without presenting readiness as validated. This exercises only the devforgeai check path; the self-check failure path is not exercised."
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
      - {id: STORY-003, item: AC-03, relation: verifies, version: 2, hash: null}
      - {id: STORY-003, item: AC-05, relation: verifies, version: 2, hash: null}
  - id: VER-13
    status: active
    obligation: "Operator check for the demonstration: run VER-02 and VER-03 with the same PRD, prompt and other fixtures, in fresh workspaces. A SHA-256 manifest of the deployed plugin (find .claude/skills/devforgeai -path '*/evals/results' -prune -o -type f -print0 | sort -z | xargs -0 sha256sum) is identical before VER-02, between the runs and after VER-03, and git diff src/ is empty. Record the three manifest hashes in the PR."
    level: manual
    covers:
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-07, relation: verifies, version: 2, hash: null}
  - id: VER-14
    status: active
    obligation: "Provenance and policy recording: in VER-01's run (no policy), the ARCH's generated_by has non-empty tool, model and session, reviewed_by is empty, every hash is null, the Change Log's 'Policy resolution:' line contains interview.max_calls=8 (default), architecture.mandated_platforms=none (default) and quality.required_categories=floor only (default), and the ARCH contains no 'id: POL-' link. Eval case records-provenance: one regex per check on the file, and a not_contains for 'id: POL-'."
    level: e2e
    covers:
      - BEH-13
      - BEH-03
    upstream:
      - {id: STORY-003, item: AC-11, relation: verifies, version: 2, hash: null}
      - {id: STORY-003, item: AC-06, relation: verifies, version: 2, hash: null}
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
| 2 | 2026-09-23 | claude-code | VER-14 checks the framework-default resolution-line entries that references/policy.md emits and the absence of a POL link, instead of the phrase 'no approved policy', which the unchanged policy.md never produces. SPEC-002 link re-reviewed at v10. Found while building STORY-003, approved by Bryan | VER-14, frontmatter |
| 3 | 2026-09-23 | claude-code | Evidence classification gains context (inputs and historical material: the input PRD, existing ARCHs, non-accepted ADRs, uncorroborated documentation), independent of kind, with the version and status examined; context establishes neither behavior nor a decision. VER-01 and VER-05 grade it; VER-12 (b) by hand; arch.schema.json enum and the ARCH template updated. STORY-003 links re-reviewed at v2. Found while building STORY-003, approved by Bryan | §4, BEH-05, VER-01, VER-05, VER-12, frontmatter |
| 4 | 2026-09-24 | claude-code | SKL-003 version 2 (§5 example). Code inspection defined as a property: read-only, every path inside the scope, tools when available, no whole-repository listing, contract documents and validation outside the rule (§5, BEH-05). ERR-05 restores only statuses, approval fields, the dependent DEC state and one audit record, keeps the user's choices, and ends with a validation-failure report. VER-05 readiness expectations derived from the amended ARCH. VER-12 (b) adds the out-of-scope request in two fixture copies and the command-path check, (c) warns when the PRD is read, (i) the ERR-05 stand-in check; VER-12 verifies AC-05. Found in VER-12 and the superseded-adr diagnosis, approved by Bryan | §5, BEH-05, ERR-05, VER-05, VER-12 |
| 5 | 2026-09-24 | claude-code | §5 skill-version example "3" for SKL-003 v3 (wording fixes: exact contract paths without Glob, no root or parent listing, the draft warning as its own line). Approved by Bryan | §5 |
