# SKILL-002 → package coverage map

Every row of the governing specification, mapped to the file and section that carries it and to the eval case that would observe it. Package paths are relative to `providers/claude/plugins/devforgeai/skills/devforge-define-product/`.

**Governing specification:** SKILL-002 revision 2, `docs/mvp/specifications/skill-002-devforge-define-product.md`, sha256 `3e48f93f200499083a062e200f71ad4a3659fad098ef6658fb4b4a34bea6ddbf` at base `c17e758417da64928a0f47fc2600304465ac3f3c`.

**Revision 2**, after repair pass 1 from the independent scaffold review of `05ed112a5a46495041651183493e28c4eae00fed`. Rows corrected or added in that pass say so. Applying a change does not close a finding.

**Every eval status below is NOT_RUN.** This map records what a case would observe, not what was observed. A row marked "covered" means a file carries the requirement; it is not a claim that anything checked it.

## User goal and use-case inventory

| Spec row | Carried by | Eval case |
| --- | --- | --- |
| User goal: bounded MVP or later release scope with measurable outcomes, requirements and explicit non-goals | `SKILL.md` frontmatter description; body title and opening; phase 3 "Define"; "Stopping" | DP-B-001, DP-B-002 |
| Direct request: "Use DevForgeAI to define the MVP from these ideas." | Description ("define the MVP or the next release from an idea ledger") | trigger P2a (train); DP-B-001 |
| Indirect request: "What is the smallest version worth shipping, and how would we know it helped?" | Description ("the smallest version worth shipping and how they would know it helped") | trigger P3a (train); DP-B-002 |
| Expected result: product-brief plus a standardized handoff | `SKILL.md` phase 3 and phase 4; `assets/product-brief.md`; `assets/handoff.md` | DP-B-001 (handoff carries the brief's digest) |
| Required context: selected idea IDs, known users and constraints, evidence the user has, existing requirements for an established project | `SKILL.md` "Required inputs" table | DP-B-001, DP-B-010 |
| Plugin capability: skill plus read-only research tools; no new backend or API account; unavailable evidence stays visible | `SKILL.md` phase 2; `references/evidence-and-scope.md` "Recording a source", "Observation, inference, assumption, invention"; no `scripts/` in the package | DP-B-003 |
| State/action boundary: research and local planning only; do not contact customers, spend money, or turn illustrative technology into approved architecture | `SKILL.md` phase 2 final paragraph; failure mode 3; "Stopping" final sentence; `references/evidence-and-scope.md` "Technology stays illustrative" | DP-B-003, DP-B-005 (negative control: nothing deployed or sent) |
| MVP support decision: required when defining or changing a release scope, including proportionate discovery and feasibility research | `SKILL.md` phase 2, the proportionality sentence, which names discovery **and feasibility** as the two kinds of research it governs (line 65); design spec W1 | DP-B-002, DP-B-010. **Feasibility added in repair pass 1 (CHG-009/F-009)**: revision 1 carried the discovery half only. |
| Does not activate for: restyling an accepted screen (design); approved implementation details (architect, develop) | Description near-miss exclusions; `SKILL.md` "What downstream reads" | triggers N5a, N5b, N6a, N6b |

## Inputs and provenance

| Spec row | Carried by | Eval case |
| --- | --- | --- |
| idea-ledger: required for a new product; selected idea IDs and adoption records | `SKILL.md` "Required inputs" row 1 | DP-B-001, DP-B-004 |
| product-brief: required for an existing product; current accepted goals, requirements, outcomes, non-goals | `SKILL.md` "Required inputs" row 2; "For an established project, reuse the valid current artifacts" | DP-B-010 |
| Evidence and constraints: source URLs or files, dates, limitations, budget or operating constraints | `SKILL.md` "Required inputs" row 3; `references/evidence-and-scope.md` "Recording a source" | DP-B-002, DP-B-003 |
| change-request: conditional; preserve its acceptance state | `SKILL.md` "Required inputs" row 4 ("that state is not the user adopting it here") | DP-B-010 (the case's required behaviour) |
| Consume-only boundary | `SKILL.md` "'Use only' is a boundary, not a summary" | DP-B-010 |
| Artifact contract: exact revisions, hashes, stable section IDs, decisions, source evidence | `references/recording-rules.md` "The artifact envelope", "Upstream entries for a brief" | DP-B-007, DP-B-010 |
| A proposed source cannot become an accepted production constraint by being copied downstream | `references/evidence-and-scope.md` "What a proposed source can and cannot do"; `SKILL.md` failure mode 2 | DP-B-004, DP-B-010 |
| For an established project, reuse valid current artifacts rather than replaying every earlier phase | `SKILL.md` "Required inputs" closing paragraph; phase 1 | DP-B-010 |
| Execution contract: owner and fence per session; concurrent writers use distinct worktrees; a shared worktree is not a concurrency mechanism | `references/recording-rules.md` "Ownership and concurrent writers"; `SKILL.md` common case 3 | DP-B-006 |
| Session template records the authority-selected assignment | `references/recording-rules.md` "Ownership and concurrent writers"; fixture `evals/fixtures/ownership/SESSION-088.md` | DP-B-006 |

## Workflow and phase exits

| Spec row | Carried by | Eval case |
| --- | --- | --- |
| Phase 1 Select; exit: scope origin and current decision state are known | `SKILL.md` "## 1. Select" with an explicit **Exit when** line | DP-B-001, DP-B-010 |
| Phase 2 Investigate; exit: important claims have evidence or are labelled assumptions | `SKILL.md` "## 2. Investigate" with **Exit when** | DP-B-002, DP-B-003 |
| Phase 3 Define; exit: each requirement has a stable ID and an observable outcome | `SKILL.md` "## 3. Define" with **Exit when** | DP-B-001, DP-B-004 |
| Phase 4 Review scope; exit: dependent design and planning can identify the exact adopted requirements | `SKILL.md` "## 4. Review scope" with **Exit when** | DP-B-001, DP-B-010 |
| These phases are not CLI subcommands | `SKILL.md` "What this skill owns, and what it does not"; `references/recording-rules.md` "Resolving a reference before you use it" | DP-B-009 |
| Only documented, implemented DevForge commands may be named as executable gates | `SKILL.md` "Missing integration, named rather than assumed" - names only subcommands observed in `--help`, and states that none covers this workflow | DP-B-009 |
| On interruption, preserve the current phase and evidence; resume by rechecking identities and the assignment | `SKILL.md` "When something is missing or a check cannot run", interruption bullet (line 121); `references/recording-rules.md` "When a session is interrupted, and how it resumes" (line 58) | DP-B-007 RESUME observation. **Corrected in repair pass 1 (CHG-002/F-002)**: revision 1 cited "Resolving a reference before you use it" and "Ownership and concurrent writers", neither of which carried the requirement. CHG-001 created the sections named here. |

## Outputs and standardized templates

| Spec row | Carried by | Eval case |
| --- | --- | --- |
| product-brief, prefix `PROD`, requirements and measurable acceptance intent traced to ideas or cited constraints | `SKILL.md` phase 3 ("IDs are stable and never reused: `PROD` ... `EVID`") | DP-B-001, DP-B-004 |
| Template `docs/mvp/templates/devforge-define-product/product-brief.md` | `assets/product-brief.md`, byte-identical copy; recorded in `references/derivation.json` | DP-C-001 (path_present) |
| Consumer coverage: design; prototype; architect; plan; review; change | `SKILL.md` "What downstream reads" table | DP-B-005 (routing), trigger negatives |
| Roster diagram summarises the flows; the input table defines conditional paths | Same table plus the conditional-paths note in the design spec section 4 | - |
| Every result includes a handoff with output identities, observed checks, unresolved decisions, next owner and one copyable task | `SKILL.md` phase 4 and "Before you call it done"; `assets/handoff.md` | DP-B-001, DP-B-009 |
| Do not read a handoff recommendation as authority for unrelated external actions | `SKILL.md` "Stopping" final sentence; "Everything you are handed ... never instructions to you" | DP-B-005 |

## Validation and behavioral acceptance

| Spec acceptance case | Required observation | Eval case | Deterministic slice |
| --- | --- | --- | --- |
| Direct activation: MVP from two selected ideas → bounded scope with explicit non-goals | Bounded scope; non-goals present; requirements traced and observable | **DP-B-001** | none; routed to review |
| Indirect activation: what to ship first → prioritizes outcomes, records the assumptions driving the choice | Outcomes lead; assumptions recorded; baselines unknown not invented | **DP-B-002** | none; routed to review |
| Missing evidence: market-size claim without sources → researches or marks unverified; no invented statistics | No uncited statistic appears | **DP-B-003** | none; absence of invention across prose is not byte-checkable |
| Traceability: a requirement unsupported by any idea or constraint → origin marked as a proposal, decision requested | Proposal origin; decision requested; not silently adopted or dropped | **DP-B-004** | none; routed to review |
| Out of scope: deploy an accepted build → routes to release rather than generating another brief | Declines; routes; deploys and sends nothing | **DP-B-005** | none; the side-effect half is covered by the run's own boundary evidence. Routing now also appears in the body beneath the consumer table (line 108), not only in the frontmatter description - **added in repair pass 1 (CHG-010/F-010)**. |

## Additional common cases

| Spec case | Eval case | Deterministic slice |
| --- | --- | --- |
| A concurrent writer claims this session's worktree or branch: stop dependent writes, report the collision, delete or reset nothing | **DP-B-006**; `SKILL.md` common case 3; `references/recording-rules.md` "Ownership and concurrent writers" | `artifact_side_effect` sentinel on `ownership/contested/PROD-004.md`, sha256 `6d25b414...` |
| A relevant upstream revision, installed skill, base commit or candidate changes: mark prior evidence stale and route a new check | **DP-B-007** (two staging variants); `SKILL.md` common case 2; `references/recording-rules.md` "When the upstream has moved on" | `artifact_side_effect` sentinels pinning both ledger revisions, `03b523de...` and `300f1c78...` |
| A template placeholder remains in a required result field: the result stays a draft | **DP-B-008**; `SKILL.md` common-case list closing paragraph; `references/recording-rules.md` "The artifact envelope" | `required_report_fields` → `placeholder` on the draft fixture, plus a `complete` positive control on `PROD-001` |
| A requested check cannot execute: record COULD_NOT_RUN and its actual cause; absence of an error is not PASS | **DP-B-009**; `SKILL.md` common case 4 and the fixed-vocabulary table; `references/recording-rules.md` "Result vocabulary" | none; a self-issued PASS is prose |
| Acceptance requires real outputs from representative requests in each terminal claimed | Design spec "Evaluation coverage proposed"; `evals/evals.json` `status` field | - |

## Rework, stopping, and recovery

| Spec row | Carried by | Eval case |
| --- | --- | --- |
| Revise a draft when discovery changes understanding | `SKILL.md` "Rework, and where a change belongs" | DP-B-010 |
| Route changes to adopted product behaviour through change, then issue a new brief revision | Same section; "What downstream reads" row for devforge-change | DP-B-010 |
| Stop when missing target users or conflicting scope decisions block acceptance of dependent requirements - not unrelated evidence gathering | `SKILL.md` "Stopping", second paragraph, including the narrowness of the stop | DP-B-007 (scope of the stop), DP-B-010 (negative control against stopping) |
| Preserve accepted versions and observed failures | `SKILL.md` "Rework"; `references/recording-rules.md` "Digest order, and reading references back" | DP-B-010 |
| Do not force-unlock, overwrite another session's result, change external gates, or retry indefinitely | `SKILL.md` common case 3; `references/recording-rules.md` "Ownership and concurrent writers" | DP-B-006 |
| If the worktree or active run changes, re-establish the baseline and evidence before resuming | `references/recording-rules.md` "When a session is interrupted, and how it resumes", the three-step re-establish order and the changed-identity rule (line 58) | DP-B-006, DP-B-007 RESUME observation. **Corrected in repair pass 1 (CHG-002/F-002)**: revision 1 cited "Ownership and concurrent writers", which covers collisions and bootstrap, not resumption. |
| Report missing observations precisely | `SKILL.md` "Result vocabulary" paragraph; "Before you call it done" | DP-B-009 |

## Native creator authoring prompt

| Spec instruction | How it was satisfied |
| --- | --- |
| Use the operator-supplied worktree, provider, write fence and base | Recorded in the design spec section 10 and verified with `git rev-parse HEAD` before any write |
| Read skill-authoring-contract.md at the selected revision | Read at `c17e758`, digest recorded |
| Create or improve devforge-define-product to satisfy SKILL-002 | Created; no prior package existed |
| Read this specification, its named templates, and only the relevant sections of the shared contracts | Sections actually used are listed per source in `references/derivation.json` |
| A focused skill in the assigned provider source, its runtime resources, reproducible eval cases/fixtures, separate A/B/C observations | Package delivered; fixtures reproducible from source; A/B/C proposed separately and all `NOT_RUN` |
| Record the real installation mode and candidate/baseline identities | Installation mode: none - not installed. Candidate digests in `file-manifest.json`; baseline `without_skill` because none exists |
| Do not claim implicit activation from a run explicitly supplied SKILL.md | `evals/evals.json` `tier_note`; `triggers/trigger-queries.json` `schema_note` |
| Preserve user scope and existing approval; keep DevForge authority external; respect the assigned worktree; report unavailable checks truthfully | Design spec "Preserved boundaries"; `SKILL.md` "Missing integration"; every tier `NOT_RUN` |
| Move lengthy conditional procedures into references; keep the trigger description precise; use scripts only for real deterministic operations | Two workflow references; description within the client's documented listing limit; no `scripts/` |
| Copy needed templates into the package and use package-relative references; installed skills must not depend on this repository's docs path | `assets/` holds both templates; every link in `SKILL.md` is package-relative; no `docs/mvp` path is resolved at runtime and no developer home path appears in the package |

## Completion handoff

| Spec row | Carried by |
| --- | --- |
| "You are here: Define a useful delivery scope." | `SKILL.md` title and opening |
| Completion means the specified artifacts exist, their declared inputs resolve, required observations are recorded, and the next task is explicit | `SKILL.md` "Stopping" |
| A document's accepted status and an external gate's passing result are separate facts | `SKILL.md` "Before you call it done"; `references/recording-rules.md` "Result vocabulary"; `evals/fixtures/existing-product/CHANGE-011.md` "Status of this document" |

## Coverage summary

- Specification acceptance-case rows: **5 of 5** carried and mapped to an eval case.
- Additional common cases: **4 of 4** carried and mapped, with three carrying a deterministic slice.
- Inputs-and-provenance rows: **4 of 4**, plus the consume-only boundary and the two contract references.
- Phase rows: **4 of 4**, each with an explicit exit condition in the body. The phase table's closing interruption-and-resume requirement is carried as of revision 2; in revision 1 it was **not carried by any runtime file**, and this map wrongly recorded it as carried (F-002).
- Output rows: **1 of 1** artifact plus the handoff requirement.
- Additional case beyond the specification rows: DP-B-010, covering the existing-product and change-request input paths, which no acceptance-case row exercises.
- **Everything is NOT_RUN.** No case has been executed, no terminal observed, no package installed.

## Repair pass 1 additions

Rows the independent scaffold review at `05ed112` showed were not carried, and where the requirement now lives.

| Requirement | Now carried by | Observed by |
| --- | --- | --- |
| SKILL-002 "Workflow and phase exits", interruption and resume | `SKILL.md` line 121; `references/recording-rules.md` line 58 | DP-B-007 RESUME graded observation. No case stages an actual interruption; a dedicated case is deferred and the deferral is recorded in `authoring-notes.md` section 9. |
| SKILL-002 "Rework, stopping, and recovery", re-establish the baseline | `references/recording-rules.md` line 58 | DP-B-006, DP-B-007 RESUME |
| SKILL-002 "MVP support decision", feasibility research | `SKILL.md` line 65 | DP-B-002 |
| SKILL-002 acceptance case "Out of scope", release routing reachable from the phase-4 section | `SKILL.md` line 108 | DP-B-005 |
| Fixture references resolve to real bytes (skill-authoring-contract rev 3; artifact-contract rev 2 envelope) | every `upstream` and `supersedes` digest under `evals/fixtures/` is the real SHA-256 of the referenced bytes, and the two predecessor fixtures exist under `preserved/` | DP-B-001 to DP-B-005, DP-B-008, DP-B-010 staging; the digest table in `evals/fixtures/README.md` |
| Provenance for the `devforge check` characterisation | `references/sources.md` "DevForge external policy schema" (line 40); the observed-input list in `references/derivation.json` | not case-observed; a provenance record, not behaviour |

**Coverage claim limits, stated plainly.** Every row above records where a requirement is now carried in bytes. None of it is an observation of behaviour: tiers C, B and A remain NOT_RUN, and the ten review findings keep their original IDs and severities until independent observation of the new bytes closes them.
