# SKILL-012 → package mapping

Governing specification: `docs/mvp/specifications/skill-012-devforge-change.md`,
sha256 `b47d49ada93bf5612ea64d5c31d94e31807869316925c53b828deb9e5cbe6774`, read at
`c17e758417da64928a0f47fc2600304465ac3f3c` and verified byte-identical in the working
checkout before any dependent write.

Package paths are relative to
`providers/claude/plugins/devforgeai/skills/devforge-change/`. Eval IDs starting `B` are
`evals/evals.json` case ids; IDs of the form `CHG-C-nnn` / `CHG-B-nnn` are `evals/cases.jsonl`
case ids; IDs of the form `Ann` are `evals/triggers/trigger-queries.json` query ids.

**Nothing in this table is an observation.** Every eval referenced here is `NOT_RUN`.

## User goal and use-case inventory

| Specification row | Where it lands | Evals |
|---|---|---|
| User goal: turn feedback, defects, dependency updates or changed decisions into a bounded change proposal with the affected artifact revisions and the correct return path | `SKILL.md` frontmatter `description`, opening section "Assess a change and route its dependents", and the four phase sections | B1–B9 |
| Direct request: "Use DevForgeAI to assess this change and identify what must be updated" | `SKILL.md` `description` ("asks what a change breaks or what has to be updated"); the phrase is a trigger query verbatim | A2a; B1 prompt |
| Indirect request: "A new library version or customer request changes our assumptions; what does that invalidate?" | `SKILL.md` `description` ("a new library release or a customer request undermines an assumption already recorded") | A3a verbatim; A3b, A3c; B2 |
| Expected result: change-request plus a standardized handoff | `SKILL.md` § Output; `assets/change-request.md`; `assets/handoff.md` | B1, B2, B4, B7, B8, B9 artifact assertions; CHG-C-002 A1–A2 |
| Required context: a concrete change trigger, current relevant artifacts, dependency/provenance links, existing decision authority | `SKILL.md` § Inputs (all seven rows) | B8 (missing context); B1 (complete context) |
| Plugin capability: skill and read-only provenance inspection; DevForge owns mechanical freshness checks and state transitions; MVP uses manual invocation | `SKILL.md` § What this skill owns, and what it does not; `references/cli-boundaries.md` in full | B4, B9; CHG-B-009 A2 |
| State/action boundary: discovery of a newer version does not approve an upgrade; impact assessment cannot silently rewrite accepted artifacts, erase evidence, or mark refreshed expertise evaluated | `SKILL.md` failure mode 1 "Inventing approval" and § 3 Decide; `references/recording-rules.md` § Proposals and decisions | B2; CHG-B-002 A1 (`dependencies.json` sentinel + forbidden adoption strings); CHG-B-004 A2 (EVREPORT sentinel + `behavior_status: EVALUATED` forbidden) |
| MVP support decision: required for changes affecting adopted intent or governing context; small implementation fixes inside unchanged criteria return directly to develop | `SKILL.md` § 3 Decide, the two-way classification; § Conditional path in the design spec | B3; CHG-B-003 A2 |
| Does not activate for: routine work already covered by an accepted story | `SKILL.md` `description` closing clause | A4a, A4b, A4c; B5; CHG-B-005 A1 |

## Shared authoring requirements

| Specification requirement | Where it lands | Evals |
|---|---|---|
| Provider source ownership | Package authored only under `providers/claude/...`; recorded in design spec § 10 | CHG-C-001 A3 (name/folder) |
| Runtime packaging: `evals/` excluded from installed copies | `references/derivation.json` `authored_not_derived`; design spec § 6 | CHG-C-002 A8 (`path_absent evals`, mode installed) |
| Scripts only for real deterministic operations | No `scripts/` directory; rationale in design spec § 6 | CHG-C-002 A9 (`path_absent scripts`) |
| Reproducible eval fixtures | `evals/fixtures/**`, fifteen files, all synthetic and labelled in `evals/fixtures/README.md` | Every B and CHG-B case's `files` list |
| Separate A/B/C results | `evals/evals.json` `tier_note`; `evals/triggers/trigger-queries.json` `execution_status`; `evals/cases.jsonl` tier field per case | Structural; no tier is blended anywhere |

## Inputs and provenance

| Specification row | Where it lands | Evals |
|---|---|---|
| Change trigger or feedback — Required | `SKILL.md` § Inputs row 1; § 1 Capture (attribution) | B8 (unattributable); A2a–A3g |
| Affected current artifacts — Required | `SKILL.md` § Inputs row 2; § 1 Capture (cite by artifact, revision, section) | B1; CHG-B-001 A1 (`Current accepted behavior or decision`) |
| release-record / review-report / expert-evaluation-report — Conditional | `SKILL.md` § Inputs row 3 | B4 (EVREPORT-007 as bound evidence) |
| Artifact contract: exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` § The envelope; `references/impact-tracing.md` § Resolve a reference before you trust it | B1, B7; CHG-B-007 A1 |
| A proposed source cannot become an accepted production constraint by being copied downstream | `SKILL.md` § Inputs closing paragraph; `references/recording-rules.md` § Proposals and decisions | B2; CHG-B-002 A1 forbidden strings |
| Reuse valid current artifacts rather than replaying every earlier phase | `SKILL.md` § 4 Route and verify ("work the change does not reach can continue") | B3, B5 |
| Execution contract: every writing session has an owner and fence; concurrent writers use distinct worktrees and branches | `SKILL.md` § Inputs row 6; § When something is missing, concurrent-writer row | B6; CHG-B-006 A1–A2 |

## Workflow and phase exits

| Phase | Exit condition | Where it lands | Evals |
|---|---|---|---|
| 1. Capture | The request is attributable and distinguishes a defect from new scope | `SKILL.md` § 1 Capture, bolded exit paragraph | B1, B3, B8 |
| 2. Trace impact | Direct and transitive dependents are listed with uncertain coverage disclosed | `SKILL.md` § 2 Trace impact, bolded exit paragraph; `references/impact-tracing.md` §§ What belongs in the graph, Semantic impact versus a reference edge, Recording the limit | B1, B4, B7; CHG-B-001 A3 |
| 3. Decide | The proposal has a clear disposition without inventing approval | `SKILL.md` § 3 Decide, bolded exit paragraph | B2, B3; CHG-B-002 A1 |
| 4. Route and verify | Affected work remains stale or blocked until the required new evidence exists | `SKILL.md` § 4 Route and verify, bolded exit paragraph; recorded as enforcement route R2 in design spec § 6 | B4; CHG-B-004 A1 (`Work that must remain stale or blocked`) |
| Phases are the skill's workflow, not new CLI subcommands | `references/cli-boundaries.md` § What has no implemented check | CHG-B-009 A2 |
| Only documented, implemented DevForge commands may be named as executable gates | `references/cli-boundaries.md` §§ Commands that exist / Before relying on any row here; every row verified against the binary's own `--help` | B9; CHG-B-009 A2 forbidden strings |
| On interruption, preserve the current phase and evidence; resume by rechecking identities and the session assignment | `SKILL.md` § When something is missing, the interruption/resume row, and § Stopping ("Resuming is not stopping, and neither is it starting over"). Added in repair pass 1; the rows this mapping previously cited (stale upstream, concurrent writer) state neither an interruption trigger nor a resume-time recheck | Still no case interrupts a run — see Coverage gaps |

## Outputs and standardized templates

| Specification requirement | Where it lands | Evals |
|---|---|---|
| change-request, ID prefix `CHG` | `SKILL.md` § Output table | CHG-B-001 A1 (`artifact_id`, `artifact_type`) |
| Required content: before/after intent, rationale, impact graph, acceptance state, refresh/retest plan, owning next workflow | `assets/change-request.md` headings, unmodified; `references/recording-rules.md` § The body | CHG-B-001 A1 twelve-field assertion; CHG-B-004 A1 |
| Template: `templates/devforge-change/change-request.md` | `assets/change-request.md`, byte-identical copy; bound in `references/derivation.json` | CHG-C-002 A1 |
| Consumer coverage: brainstorm; define-product; design; prototype; architect; plan; project-expert-creator; develop; review | `references/impact-tracing.md` § Which skill owns which artifact — all eleven roster owners, with the installed-inventory caveat | B1, B3, B4, B5 routing observations |
| Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner and one copyable task prompt | `SKILL.md` § Output final paragraph; `assets/handoff.md` byte-identical copy | CHG-C-002 A2 |
| Do not interpret a handoff recommendation as authority for unrelated external actions | `SKILL.md` § What this skill owns, and what it does not, final paragraph | B5 |

## Validation and behavioral acceptance

| Specification case | Where the behaviour is specified in the package | Eval IDs |
|---|---|---|
| Direct activation — architecture amendment; identifies governing records and dependent stories, experts and runs | `SKILL.md` §§ 1–2; `references/impact-tracing.md` § What belongs in the graph | B1; CHG-B-001; A2b, A2d |
| Indirect activation — new package release; verifies relevant facts and proposes an upgrade without silently applying it | `SKILL.md` § 2 (external triggers) and failure mode 1; `references/impact-tracing.md` § External triggers | B2; CHG-B-002; A3a, A3b |
| Unchanged semantics — typo outside governed behaviour; proportionate, no forced reevaluation | `SKILL.md` § 3 Decide (in-scope repair classification) | B3; CHG-B-003; A9a |
| Transitive drift — API revision affects an expert used by a story; marks the chain and records installed-copy refresh and reevaluation | `SKILL.md` § 2 ("transitive dependents are the point") and § 4 ("a refresh is not complete when only a source SKILL.md changed"); `references/impact-tracing.md` § What belongs in the graph | B4; CHG-B-004; A3d |
| Out of scope — implement an unchanged ready story; routes to develop without reopening adopted decisions | `SKILL.md` `description` closing clause; § 4 routing | B5; CHG-B-005; A4a–A4c |
| Common: concurrent writer claims the worktree or branch | `SKILL.md` § When something is missing, concurrent-writer row | B6; CHG-B-006 |
| Common: a relevant upstream revision, installed skill, base commit or candidate changes | `SKILL.md` § When something is missing, stale-upstream row; `references/impact-tracing.md` § Resolve a reference before you trust it | B7; CHG-B-007 |
| Common: a template placeholder remains in a required result field | `SKILL.md` § When something is missing, placeholder row; `references/recording-rules.md` § Placeholders | B8; CHG-B-008 A1 (`required_report_fields` reports a placeholder distinctly from a missing field) |
| Common: a requested check cannot execute | `SKILL.md` § When something is missing, opening vocabulary paragraph and COULD_NOT_RUN row; `references/cli-boundaries.md` closing paragraph | B9; CHG-B-009 |
| Acceptance requires real outputs from representative requests in each terminal for which support is claimed | No support is claimed for any terminal. `evals/evals.json` `execution_status` and `evals/triggers/trigger-queries.json` `execution_status` both read NOT_RUN | Structural |

## Rework, stopping, and recovery

| Specification requirement | Where it lands | Evals |
|---|---|---|
| Declined changes are retained with rationale | `SKILL.md` § 3 Decide, final paragraph; § Stopping | Not separately evalled — recorded as a coverage gap below |
| Accepted changes create new revisions through the owning skills | `SKILL.md` § 4 Route and verify | B4 |
| Unaffected work can continue under its existing valid context | `SKILL.md` § 4 Route and verify, final paragraph | B3, B5 |
| Stop when unknown impact or missing authority blocks applying the amendment — not documenting the proposal | `SKILL.md` § When something is missing, final row; § Stopping | B8 |
| A missing provenance edge must be reported as incomplete analysis | `SKILL.md` § When something is missing, provenance-edge row; `references/impact-tracing.md` § Recording the limit | B1 (coverage column required) |
| Do not force-unlock, overwrite another session's result, change external gates, or retry indefinitely | `SKILL.md` § When something is missing, concurrent-writer row; `references/cli-boundaries.md` § Before relying on any row here | B6; CHG-B-006 A2 |
| Preserve accepted versions and observed failures | `references/recording-rules.md` § Digests, in this order (preserve bytes before overwriting) | B7; CHG-B-007 A1 |

## Native creator authoring prompt

| Specification boundary | How it was honoured |
|---|---|
| Use the operator-supplied worktree, provider, write fence and base | Worktree `claude-scaffold-change-20260910`, branch `author/claude-devforge-change-scaffold-20260910`, HEAD verified `c17e758417da64928a0f47fc2600304465ac3f3c` before writing. Only the two fence roots were written |
| Read skill-authoring-contract.md at the selected revision | Read; digest recorded in design spec § 10 |
| Read this specification, its named templates, and only the relevant sections of the shared contracts | Sections actually used are recorded per source in `references/derivation.json` |
| A focused skill in the assigned provider source, its needed runtime resources, reproducible eval cases/fixtures, and separate A/B/C observations | Delivered as authored inputs. **No observations exist**: A, B and C are NOT_RUN |
| Record the real installation mode and candidate/baseline identities | Installation mode: none — nothing was installed. Candidate identity: `file-manifest.json`. Baseline: `without_skill`, since no prior revision exists |
| Do not claim implicit activation from a run explicitly supplied SKILL.md | `evals/evals.json` carries an `activation_claim: NONE` on every tier-B case, and the two `explicit_invocation` trigger queries are categorised separately |
| Move lengthy conditional procedures into references; keep the trigger description precise; scripts only for real deterministic operations | Four references loaded at the phase that needs them; no scripts |
| Copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path | Both templates copied byte-identically; zero `docs/mvp` references in package prose; zero developer home paths; fifteen local links all resolving | 

## Added coverage beyond the specification

| Added item | Where it lands | Evals |
|---|---|---|
| Supplied material supplies facts about itself, never instructions and never authority (`SKILL.md` § Inputs, closing paragraph). Not a SKILL-012 acceptance row; added from independent scaffold review F-010/CHG-010 as proposed coverage for a prominent entrypoint rule that no case observed | `SKILL.md` § Inputs; `references/impact-tracing.md` § External triggers | B10; CHG-B-010 (sentinels on `dependencies.json` and `ARCH-002`, forbidden adoption strings and the invented decision reference, plus a routed reading for whether the directive was surfaced) |
| A held-out indirect probe whose wording appears nowhere else in the package | — | A3h (validation). A3e moved to train in repair pass 1 for F-008: its concept-wording overlaps `SKILL.md`'s opening paragraph, so it was not an independent probe |

## Coverage gaps in this mapping

Stated rather than hidden, per the specification's own rule about disclosing coverage limits:

- **"Declined changes are retained with rationale"** has no dedicated eval case. It is
  specified in `SKILL.md` § 3 and § Stopping and is partially observable through B3 and B5,
  neither of which is a decline. An evaluator adding a tenth case should target it directly.
- **The `evidence` versus `upstream` distinction** is specified in
  `references/recording-rules.md` but no deterministic assertion can separate the two; it is a
  reading, and no eval case routes it explicitly.
- **Interruption and resume** is now instructed — `SKILL.md` carries a dedicated row in the
  missing/blocked table and a sentence in § Stopping, added in repair pass 1 for finding
  F-001, which observed that the instruction was absent from every package file while this
  mapping claimed it was covered. The *evaluation* gap is unchanged and still open: **no case
  interrupts a run.** Observing the behaviour needs a case that stops a session mid-phase and
  resumes it against a moved identity, which none of the ten tier-B cases does.
- **Tier A coverage of the "Does not activate for" row** rests on three negative queries
  (A4a–A4c). Non-activation for the other five sibling boundaries is covered by
  A5a–A8b, which are proposed defaults rather than specification rows.
