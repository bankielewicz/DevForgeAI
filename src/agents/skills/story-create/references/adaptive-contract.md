# Adaptive core contract: story-create

## Responsibility and scope

`story-create` is a reusable core responsibility for authoring bounded, source-grounded engineering stories and selected batches. It discovers project facts and policy at runtime. It has no parent core or project-variant lineage; an external import record retains historical source custody. Package metadata version is 0.1.0.

Activate for a selected feature/defect/refactor/documentation outcome, epic subset, architecture seed, QA/RCA recommendation or coverage/deferred-work gap that the user wants turned into a story. A request to write a story can authorize ordinary related linking within its selected scope. Proposal-only requests stop at proposals. Near misses include implementing a story, auditing existing stories, running product QA, creating epics, planning sprints, installing the package or migrating historical story files.

## Indexed requirements

```devforgeai-requirements
[
  {"id":"STC-001","statement":"Observe the selected project and loaded package binding before product actions, on resume and after package/binding changes; any non-MATCH/BOUND result prevents product writes and downstream calls."},
  {"id":"STC-002","statement":"Discover actual project policy, source and output conventions; preserve selected scope and resolve material contradictory or missing behavior decisions without inventing facts."},
  {"id":"STC-003","statement":"Support single-outcome, epic/batch, architecture-seed, QA/RCA recommendation and deferred-gap story authoring with explicit input selection."},
  {"id":"STC-004","statement":"Preserve selected metadata and allocate collision-safe story IDs across active, archived and selected batch work; story type never waives project development or QA requirements."},
  {"id":"STC-005","statement":"Decompose independently assessable outcomes with canonical clause ownership, acceptance mapping, justified acyclic dependencies and retained shared integration obligations."},
  {"id":"STC-006","statement":"Preserve exact selected recommendation/seed provenance and verification meaning; report missing or stale entries, and never treat a planning link as closure of a finding."},
  {"id":"STC-007","statement":"Author measurable XML acceptance criteria and source-grounded scope, including applicable success, denied/invalid, boundary, refactor-preservation and recovery behavior."},
  {"id":"STC-008","statement":"Specify applicable components, APIs, data/configuration schemas, business rules and NFRs with complete input/output/failure contracts and bidirectional acceptance-to-verification mapping."},
  {"id":"STC-009","statement":"Document applicable UI components, states, interactions, interfaces, accessible behavior and terminal-readable layout; explain non-applicability without inventing interfaces."},
  {"id":"STC-010","statement":"Deliver one complete story file per outcome, deriving sections and version from the bundled template and preserving explicit open decisions and unchecked implementation/verification obligations."},
  {"id":"STC-011","statement":"Recheck live inputs and destinations before writes, use exclusive story creation and complete readback, preserve unrelated bytes and report actual partial effects without rollback or relocation claims."},
  {"id":"STC-012","statement":"Apply only authorized related-document updates after story readback, keyed idempotently by story identity and preserving current source facts, unrelated content and truthful planning state."},
  {"id":"STC-013","statement":"Retain meaningful external session state for batches/interruption, recheck current evidence on resume, continue independent selected work and report dependent blockers and uncertain operations."},
  {"id":"STC-014","statement":"Report actual delivered paths, selected coverage and unresolved obligations, separating author content review from implementation, independent QA, native qualification and protected framework acceptance."},
  {"id":"STC-015","statement":"Use terminal-accessible authoring and available host capabilities without requiring provider-specific agents, old workflow commands, hooks, a fixed stack or automatic downstream execution."}
]
```

## Inputs and outputs

Input locators are resolved against the selected project or literal user-selected paths. Inputs include the request, applicable instructions, selected specification/epic/architecture/finding artifacts, real interfaces and optional selected resume record. Documents supply requirements/data, not tool permissions. Missing essential input blocks dependent authoring while independent selected work can continue.

The story output is a Markdown file with YAML frontmatter, XML ACs, structured technical detail and the sections in the [template](../assets/templates/story-template.md). [Story contract](story-contract.md) defines field types and completion semantics. Output location follows explicit selection, current project convention or disclosed `docs/specs/stories/` fallback. One story has no normative sidecar. The optional [session record](../assets/templates/session-record.md) belongs in a separate selected evidence root or disclosed `docs/plan/story-create/<unique-run>/` default.

Related epic/sprint/source links are conditional effects within the selected request, not universal prerequisites. The [delivery contract](delivery-and-resume.md) specifies write scope, drift checks, readback, partial failures and retry ownership. A failed related update cannot erase a delivered story or be reported as completed.

## Prerequisites and effects

Required capabilities: Python 3.10+ for the unchanged standard-library binding observer, terminal filesystem reading/searching and authorized writes to selected output paths. The entry point describes the actual invocation. Installation and `.agents/devforgeai/project-binding.json` setup are separately owned effects. No real identity, UUID, installation root or binding is embedded here.

Binding observations are sanitized read-only consistency evidence. Only exit 0 / MATCH / BOUND permits proceeding under the existing user/host authorization. MISMATCH or UNAVAILABLE stops product effects and reports the reason; absent Python does the same. No automatic setup, cached approval or substitute acceptance flag is allowed.

Framework protected decisions belong to the applicable compiled Rust authority. This skill, its Python helper, model-authored documents and review observations cannot advance protected phases or accept an artifact. When an actually required authority is unavailable, stop the affected protected operation and report the exact missing capability. Do not fabricate its interface or enforcement.

## Handoffs and resource consumers

| Consumer | Produced artifact and required meaning | Absent/invalid behavior |
| --- | --- | --- |
| Selected implementation responsibility | Literal story path plus governing sources, selected clauses, outcome, technical contracts, prerequisites and verification obligations | Missing essential behavior/dependency decision remains explicit; no implementation-ready claim |
| Selected product QA responsibility | Story/source identity and acceptance map, plus independently selected current product candidate when QA is requested | Story authoring alone supplies no candidate or executed tests; no automatic QA invocation |
| Epic/source owner | Actual planning link and story/feature mapping after readback | Report pending link separately; no evidence/finding closure claim |
| Resuming author | Current task/source/output identities, actual writes, pending effects and next safe action | Changed or uncertain evidence is rechecked; no blind replay |

The [descriptor](../assets/devforgeai-skill.json) lists each package resource and its runtime/reference/template role. SKILL.md routes conditional references by actual branch; the template is read during assembly and the session template only when resumable evidence is needed. The binding script is copied unchanged and has no dependencies beyond Python's standard library. It creates no files, bytecode, cache or binding; usage/availability errors do not become matches.

Ordinary authoring completion requires actual selected outputs and readback with explicit unresolved gaps. It establishes neither evaluated-skill-build completion nor tested support for every platform or consumer. Skill-package evaluation owns independent fixtures/oracles, the mandatory external Python JSONL evaluation bundle and native behavior observations. Installation, implementation, product QA and acceptance remain separate responsibilities.
