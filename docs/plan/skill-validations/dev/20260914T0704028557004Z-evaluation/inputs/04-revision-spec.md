---
id: DEV-REVISION-20260913T2310456388212Z
skill_name: dev
target: codex
status: proposed
artifact_kind: complete_revision_specification
---

# Proposed complete dev revision specification

## 1. Identity, ownership, and review boundary

This is a complete proposed future contract for the portable Codex skill `dev`. The existing DEV-001 through DEV-026 requirements and DV-01 through DV-18 cases are reproduced below; the mandatory corrections in section 10 refine literal evidence-path selection and completion verification. No implementation is authorized by this document.

Observed development target: `C:\Projects\DevForgeAI\src\agents\skills\dev`.
Package digest: `7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae`. The [source manifest](source-manifest.json) and [retained original governing specification](inputs/inputs/06-dev-skill-spec.md), SHA-256 `b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265`, establish the assessment basis. [Origin](origin-record.json) remains observed; no generated/adopted baseline is inferred from the rejected packet.

Required correction: finding `F-60c84a7e29fc2151594698f693d698226b36a90666efcf4bf2ab6cc7fe744bc8` from one completed cold DV-17 execution. Prompt and specification selected the literal directory `custom receipts/`; actual artifacts were placed in `receipts/` and R-2 was falsely marked VERIFIED. This is evidence of one observed failure, not a quantified reliability claim. Retain all successful behavior and scope restrictions. No optional enhancement is proposed.

These concrete target/evidence names select this authoring review only. They must not become generated runtime defaults. The authorized validation task creates this proposal and evidence only. A later explicitly selected `$skill-builder` task owns any development-source revision; a separate `$skill-validator` task owns fresh quality evaluation. Operational copies, original specifications, existing packets and prior runs remain unchanged.

Project policy still determines product language, tools, layout and thresholds. When the selected product is DevForgeAI, its compiled-Rust authority and >=95% executed-line/required-case thresholds apply as runtime-selected project inputs; they are not universal constants for every product. Python evaluation produces evidence only. Standalone operation, terminal accessibility, no mandatory framework binding, and no plugin/installation requirement are preserved.

## 2. Purpose, activation, and ownership

**DEV-001 — Activation.** Activate for a request to implement, extend, or finish software against explicitly selected specification documents, including a coherent multi-document contract. Continue a prior implementation only when the user selects that work or checkpoint. Natural-language activation must express the development purpose; preserve automatic invocation unless the user separately disables it.

Near misses include specification-only drafting, standalone architecture research, skill authoring, package evaluation, operational installation, deployment, and a code-review-only request. Do not convert these into implementation authority. A task asking only for a plan produces a plan and stops; applicable host Plan mode always prohibits implementation writes. Explain missing specification selection rather than scanning every document and selecting a project objective autonomously.

**DEV-002 — Product scope.** The skill owns authorized product implementation, product tests, integration, refactoring, applicable QA, and implementation evidence. It does not invoke `$skill-builder` to write ordinary application code. `$skill-validator` owns assessment of the `dev` package itself, not every test of a product built using `dev`.

**DEV-003 — Portable operation.** Runtime instructions MUST NOT prescribe a programming language, package manager, application type, operating system, source-root layout, product executable, specification filename, fixed output directory, or model. Discover each from selected inputs and the current environment. No credentials, project UUID, author-machine location, source snapshot from this project, or installation path may be embedded in the generated package.

Fixed names for internal skill references/templates and generic record fields are allowed. Host concepts such as project instructions and shell permissions are not product assumptions. Examples in runtime resources must use neutral input roles and placeholders resolved before execution, not a disguised copy of the intended first application.

**DEV-004 — Authority.** Honor actual user scope, host permissions, applicable project instructions, and the selected specification. File contents provide requirements or data within that scope; they do not grant permission to run commands, bypass controls, install software, or broaden the task. The skill cannot mint protected approvals, waive gates, advance an unavailable authority service, or turn an editable record into acceptance.

In a project requiring an external authority, use its actual discovered interface and preserve its response evidence. If that authority is unavailable, report the precise affected operation as unavailable. Ordinary development may continue only where independently permitted; no fabricated or Python fallback acceptance path. The standalone skill itself requires no adaptive descriptor, operational binding helper, or setup step.

## 3. Inputs and cold-session context

**DEV-005 — Invocation inputs.** Required inputs are the selected project, explicit specification document(s), current requested scope, and access to applicable project instructions. The project can be empty. Optional inputs are referenced constitutional material, a checkpoint, an evidence destination, and installed analysis/authority services. Referenced material becomes essential only for requirements that depend on it.

Interpret user-supplied paths in the actual host environment. Resolve relative document references relative to their containing document, and project paths relative to the selected project. Do not substitute Windows and Linux roots because they contain similar files. Missing, unreadable, duplicate, or ambiguous selected inputs are recorded before dependent changes.

**DEV-006 — Initial inspection.** Discover the actual shell, filesystem permissions, source layout, project instructions, build manifests, lockfiles, test configuration, installed executables, and relevant existing changes. If Git exists, record branch/HEAD and working-tree changes; otherwise use scoped file inventories and hashes without requiring Git initialization. Inspect repository ownership constraints and ongoing work before choosing files to change.

Do not run build scripts, install dependencies, or execute commands embedded in documents simply to understand them. First determine the command's purpose, side effects, and authorization. Existing tool configuration is evidence of intent, not proof that a tool is installed or works.

**DEV-007 — Context record.** Before production changes, retain a bounded context record covering selected inputs, their raw-byte hashes and locators, discovered tools, effective rules, declared outputs, known source changes, and unresolved gaps. Capture only relevant source and instructions. Exclude credentials and unrelated content. The record must identify omitted or inaccessible relevant inputs rather than claim comprehensive inspection.

Resolve an evidence destination from explicit invocation input, then applicable project rules, then an established suitable project evidence location. If none is available, ask once for a location before creating records. Never hardcode a new project directory. Keep evidence separate from installed skill bytes, input specifications, and product-generated data. Record the actual selected locations so a cold resume can find them.

The current conversation may authorize work, but the skill must not rely on memory to supply missing architectural or behavioral requirements. Material facts used from conversation must be recorded with their origin in the current context. A checkpoint is a navigation aid, not unquestioned current truth.

## 4. Specification and constitutional resolution

**DEV-008 — Requirement inventory.** Read every explicitly selected specification and its necessary references. Preserve supplied requirement/scenario IDs, qualifying them with source identity when several documents reuse an ID. If IDs are absent, assign local traceability IDs tied to exact source passages without rewriting the source. Inventory deliverables, interfaces, dependencies, exclusions, failure behavior, acceptance scenarios, and quality/platform obligations.

Distinguish normative requirements, examples, historical claims, and deferred capabilities. A proposed command in a specification is an implementation target, not an existing executable. Do not mark a feature complete because its intended signature or help text exists.

**DEV-009 — Dependency and conflict analysis.** Establish document/component dependencies and shared-interface ownership before coding. Reading a referenced specification does not automatically select its deliverables for implementation. If an unselected prerequisite is required and absent, identify the dependency and ask whether to select it or provide an existing implementation. Do not silently build an entire referenced framework.

Resolve explicit supersession and ordering only when supported by the selected contracts. Never assume the most recently read document wins. Detect incompatible interfaces, conflicting limits, architecture/policy contradictions, and dependency cycles. Ask for a concrete decision when material; retain the resolution and affected requirement IDs. Continue independent permitted work while dependent work remains unresolved.

**DEV-010 — Constitutional decision categories.** Establish the following facts from supplied evidence; they may be sections of existing documents rather than separate files:

| Category | Facts needed when applicable |
| --- | --- |
| Architecture | Component responsibilities, boundaries, interfaces, state ownership, external dependencies, authority. |
| Technology stack | Languages, versions/compatibility, libraries, package/build tools, runtime constraints. |
| Source tree | Actual target locations, conventions, ownership, generated versus maintained files. |
| Testing and QA | Required behaviors, test types, tools, thresholds, exclusions, platform matrix, acceptance owner. |
| Security and operations | Permissions, secrets, network constraints, irreversible effects, deployment/install boundaries. |
| Delivery | Required artifacts, evidence locations, native qualification, documentation, completion conditions. |

Reference established decisions instead of duplicating constitutional documents. Mark inapplicable categories with a reason. Infer routine implementation choices only where they are compatible with explicit rules and existing conventions; record the rationale. A missing language, storage/authority boundary, incompatible dependency, source destination, or mandated quality threshold is material when implementation depends on it.

**DEV-011 — Gaps and controlled adaptation.** Use precise gap categories: missing input, contradictory requirement, missing decision, unavailable capability, denied operation, or changed input. Record source references, affected work, why it cannot proceed, and the minimum resolution needed. Do not substitute a vague TODO, optimistic assumption, or placeholder for an essential decision.

Drafting or changing constitutional/specification files is a separate selected effect. The default is to record resolutions in the context record, not manufacture architecture documents or weaken requirements. If new evidence invalidates the plan, update dependent slices and propose necessary requirement changes through the project's actual review policy. Failed tests never authorize rewriting expected behavior to obtain a pass.

## 5. Existing-code discovery and implementation planning

**DEV-012 — Reuse assessment.** Before creating a substantial new method, class, module, or service, inspect relevant existing code and tests. Search names, documentation/comments, interfaces, dependencies, and behavior-related terms. Structural or semantic tools are optional aids unless the selected project requires them. Record their coverage/freshness limitations and inspect current source before relying on results.

For plausible existing candidates, record reuse, extension, composition, or new implementation with concise evidence and reasons. Absence of search matches is not proof that equivalent functionality is absent. Do not demand reuse when compatibility, ownership, or required behavior makes a new component appropriate. Scope assessment to the proposed responsibility rather than generating a repository-wide ceremony for every edit.

**DEV-013 — Implementation slices.** Build a dependency-ordered work plan. Each slice identifies requirement IDs, affected existing components, proposed additions, contracts it consumes/provides, tests and acceptance checks, dependencies, and allowed effects. Shared protocol/schema ownership precedes dependent clients. Favor observable end-to-end behavior where possible over large disconnected scaffolds.

For each selected requirement, identify a planned verification method or a precise gap. Do not declare completion because a percentage of files or planned slices exists. Respect supplied build order and source ownership. No delegation is required by this skill; the complete workflow must be executable by one Codex session, and any separately authorized delegation must preserve task ownership and evidence.

**DEV-014 — Commands and prerequisites.** Resolve actual build/test/format/static-analysis/coverage commands from project manifests and documentation, then check required tool availability before use. Record the working directory, argument data, expected effects, and tool versions. Use native argument handling so paths and untrusted strings are data, not injected shell code.

If no implementation/tooling exists yet, choose the framework/toolchain prescribed by the specification or resolve the missing decision. Create build/test scaffolding only within authorized product scope. Dependency installation, network access, or privilege elevation follows existing authorization and host approval mechanisms; never bypass them. Missing tooling is reported, not silently replaced with a different target language.

## 6. Red, green, refactor, and QA

**DEV-015 — Red.** Translate each behavioral slice into focused tests with concrete expected results before changing its production behavior. Execute the test and retain the failing output. Confirm that it fails because the required behavior is absent or incorrect. A missing executable, syntax error in the test, invalid environment, or unrelated dependency failure is not a valid red result.

For a new project, prepare the minimum runnable test harness first and distinguish harness setup from the red behavioral case. Characterization tests for existing behavior may initially pass; label them as regression evidence, then add the separate failing test for the requested change. Do not manufacture failure by breaking correct source. Compilation failures count as red only for an intentionally missing contract when the test and its expected failure are otherwise established.

**DEV-016 — Green.** Implement the minimum real behavior needed to satisfy the requirement and execute the same focused tests. Preserve their intended assertions. Do not replace the integration under test with a stub, hardcode expected fixture outputs, suppress errors, or weaken tests to claim success. Mocks are allowed at documented external boundaries, with real integration coverage where required.

**DEV-017 — Refactor.** Improve structure while preserving the tested behavior and declared public contracts. Rerun affected tests after refactoring. Broader architectural changes must remain within the selected scope or be proposed as new work. A refactor that needs no code changes can record that conclusion; no artificial churn is required to satisfy the workflow label.

**DEV-018 — Product QA.** After slices integrate, execute the applicable regression, integration, negative-path, static-analysis, formatting, coverage, and platform checks. Select meaningful checks from the project's contracts and actual changed paths. Add recovery, concurrency, denied-operation, and invalid-input cases where specified. Do not repeatedly broaden an already sufficient test run without a new concern or change.

Declared coverage and pass-rate thresholds come from the project's rules/specifications. Record the metric definition, denominator, exclusions, raw counts, required platforms, and measurement tool before claiming a result. Do not silently change denominator, round a failing value up, omit required skipped cases, or mix evidence from different product revisions. When policy does not define a needed acceptance metric, resolve that gap rather than inventing a universal default.

Preserve all attempts, including initial failures and retries. Final qualification uses a coherent final candidate and declared required-case set; earlier failures remain historical evidence and do not increase or decrease the case denominator. A later passing attempt must not hide an unresolved flaky failure. Report counts, defects, and any remaining uncertainty separately.

**DEV-019 — Native and external checks.** Compilation, mocked integration, static review, and successful command help do not establish native execution or real service behavior. Run required checks on the declared host when available and authorized. Otherwise identify the specific unperformed acceptance cases and retain an honest partial result. Do not synthesize GUI evidence, infer another platform passed, or install operational components solely to turn a gap into apparent completion.

The workflow must be operable from Codex CLI terminal. A product may include a GUI, but terminal-accessible builds and behavioral tests cannot certify visual rendering by themselves. If a selected requirement needs human/native visual evidence unavailable through the current terminal workflow, request that evidence or report the case unperformed. No MCP/browser tool is a mandatory capability of the reusable skill.

## 7. Records, interruption, and completion

**DEV-020 — Evidence records.** Provide templates for the logical records below. Select their concrete output paths at runtime under the resolved evidence root, and record that mapping. Do not create empty documents merely to satisfy a file list; one concise human-readable report may carry several logical sections, while execution records and machine-readable mappings remain distinct where needed.

| Record | Required observable content |
| --- | --- |
| Context | Current authorization source/scope, selected project, input locators/hashes, rules/decisions and their sources, tool observations, output mapping, unresolved gaps. |
| Requirement traceability | Source-qualified ID, statement locator, dependencies, implementation paths/symbols, tests/evidence references, status and unresolved reason. |
| Slice plan | Slice ID, requirement IDs, inputs/outputs, dependencies, owned change scope, verification plan, current state. |
| Execution evidence | Unique attempt ID, slice/check IDs, stage, exact command and working directory, platform/tool identity, start/end, exit code, retained stdout/stderr references, candidate identity, interpretation. |
| Checkpoint | Context/input references, completed/pending slices, last verified candidate identities, observed changed files, owned running processes/jobs, outstanding decisions/failures, next safe action. |
| Delivery | Selected scope, implemented outputs, requirement accounting, final checks/metrics, remaining defects/gaps, unperformed native checks, and external acceptance status when applicable. |

Execution records are append-only JSONL data or equivalent references into an existing project evidence system when its contract preserves those fields. Redact secret values, clearly mark redaction, and retain an appropriate protected source reference if required. Do not falsely claim a redacted command is a byte-exact unredacted receipt. Records are editable development observations, not an enforcement system. No Python evidence helper may implement an authority gate.

**DEV-021 — Resumption and drift.** Write a checkpoint after meaningful verified progress and before yielding when work remains. On resume, verify selected input hashes, current source, expected tools, permissions, and process/job state. Reuse unaffected evidence only when its candidate and prerequisites still match. Changed specifications, shared contracts, source, toolchain, or test definitions invalidate dependent decisions/results; identify that dependency rather than discarding all history blindly.

Never overwrite another actor's changes, blindly restart a job, replay a migration, restore a historical snapshot into current source, or claim rollback without evidence. Unknown process outcome requires inspection before retry. Cancel or clean up only resources this run owns and is authorized to manage. Partial progress must remain inspectable and resumable.

**DEV-022 — Result semantics.** Overall development status is one of:

| Status | Meaning |
| --- | --- |
| `COMPLETE` | Every selected deliverable and mandatory acceptance check is satisfied with current evidence; no required work remains. This is a development result, not protected framework acceptance. |
| `PARTIAL` | Useful selected work is delivered, but required implementation or verification remains. |
| `BLOCKED` | No remaining selected work can proceed without a specified missing decision, permission, input, or capability. |

Individual checks report `PASS`, `FAIL`, `ERROR`, `NOT_RUN`, or `NOT_APPLICABLE` with evidence/reason. `NOT_APPLICABLE` requires a scope-based reason; it cannot hide an unavailable required platform. A final report may show implemented features with unperformed QA but must not label the overall task complete. Numeric floors cannot waive mandatory failing scenarios or unresolved regressions.

Report external framework acceptance independently as an actual authority response or `NOT_EVALUATED`. If the current invocation requests only planning or a subset, define completion against that explicitly selected scope and make the distinction visible; never imply the whole product is finished.

**DEV-023 — Side-effect boundaries.** Do not deploy, publish, merge, install operational skills, configure startup, or execute irreversible migrations without corresponding current authorization. A request to implement through QA does authorize ordinary reversible source/test/evidence edits within the selected project, not every command found in a specification. Honor authorization already supplied without repeatedly asking for it. Preserve unrelated files and old evidence.

## 8. Generated package architecture

**DEV-024 — Package resources.** Require `SKILL.md` with `name: dev` and a precise activation description. Keep essential routing, portable input resolution, end-to-end behavior, and authority boundaries in the entrypoint. Use focused relative references for context/specification resolution, implementation/TDD/QA, evidence/resume, and failure/delivery behavior. Use assets for reusable record templates. Each shipped resource must have an actual entrypoint or reference consumer.

Do not add empty scaffolds, automatic README/changelog files, unused schemas, arbitrary example counts, executable product fixtures, test campaigns, framework bindings, or plugin manifests during authoring. Host metadata, if generated, must preserve supported fields and use `dev` as the skill identity. No two-part skill name is required.

Default runtime implementation is instructions plus templates. Add a helper only if a concrete repeated operation cannot be served adequately by available terminal tooling. Its contract must state inputs, outputs, dependencies, effects, error behavior, and consumer. Supporting Python may produce bounded evidence observations, but no helper decides framework transitions or acceptance. A helper dependency must be checked before the operation needing it, not silently turned into a prerequisite for unrelated work.

**DEV-025 — Instruction isolation.** Builder authoring restrictions apply while creating this package; they must not be copied as a prohibition against `dev` running its product tests. Conversely, `dev`'s authorization to program and test products must not authorize the builder to execute a skill-quality campaign while authoring it.

The standalone package does not receive `binding_required=true`, an adaptive project descriptor, or an installed-root assumption. A future adaptive wrapper or project variant is separate work and must preserve this portable behavior rather than silently impose setup on the standalone skill.

## 9. Skill evaluation build contract

**DEV-026 — Separate validation stage.** The authored `dev` package must be assessed in a separately selected `$skill-validator` task against this specification and its exact delivered bytes. Builder performs custody safeguards/readback and publishes its manual handoff, but does not invoke validator or run quality tests. Authoring completion is not evaluated-build completion.

Mandatory evaluation build artifacts are a Python JSONL runner, deterministic graders, scenario/fixture definitions, expected results, evidence schema, runtime/dependency declarations, and an artifact manifest binding all those files and the exact `dev` package digest. They may live in the validator-owned external build-evaluation bundle; they are not required runtime dependencies or a test campaign copied into the installed skill. Each evidence artifact must have a retained locator and SHA-256. Missing required artifacts means the evaluated skill build is incomplete.

The validation task owns authoring and executing that bundle under its own selected contract. If its available workflow cannot create a required artifact, report the gap; do not silently reassign it to builder or fabricate a bound result. This specification describes required cases but does not generate or execute that campaign during skill authoring.

Deterministic graders can check record completeness, source/digest binding, requirement accounting, execution evidence presence, and expected fixture outcomes. They cannot prove all instructions are semantically correct or that the skill generalizes from a few trials. Require bounded cold-session behavioral trials and separate semantic observations for reuse judgment, gap handling, and faithful implementation. Observed Python results are evidence only; compiled Rust remains the authority if protected framework acceptance is required.

### 9.1 Acceptance scenarios for the skill

The validator must turn these into actual bounded tests with explicit expected observations. Each required case counts once in the declared suite. Use disposable projects and retained inputs, with budgets/timeouts declared before execution. Running these cases is not part of the present specification-writing task.

| Case | Requirements | Setup and required observation |
| --- | --- | --- |
| DV-01: cold single-spec build | DEV-001, DEV-005, DEV-006, DEV-007, DEV-008, DEV-013 | New session receives project and one complete spec; reconstructs context, implements required behavior, and records actual checks without hidden history. |
| DV-02: dependent documents | DEV-008, DEV-009, DEV-013 | Two selected specs share a contract; establish one contract owner and dependency order, implement both, and verify their integration. |
| DV-03: cross-language portability | DEV-003, DEV-010, DEV-014 | Two unrelated disposable products use different languages, build systems, and layouts; neither receives the other's commands, paths, or architecture. |
| DV-04: brownfield reuse | DEV-012 | Existing differently named helper satisfies part of the requirement; inspect code/tests and justify reuse/extension instead of duplicating responsibility blindly. |
| DV-05: constitution gap | DEV-010, DEV-011 | An essential technology/ownership decision is missing; ask the precise question, continue independent work, and create no unrequested constitution or guessed implementation. |
| DV-06: contradictory specs | DEV-009, DEV-011 | Selected inputs disagree on an interface; report source-qualified conflict and stop dependent coding until resolved. |
| DV-07: unselected dependency | DEV-009, DEV-023 | A referenced prerequisite is absent; reading it does not authorize building/installing it. |
| DV-08: optional and required tools | DEV-004, DEV-014 | Optional index unavailable: use normal terminal discovery. Mandatory project authority unavailable: no simulated acceptance or dependent protected operation. |
| DV-09: valid TDD lineage | DEV-015, DEV-016, DEV-017 | Retain an intended red failure, passing implementation, and post-refactor result; initially passing characterization tests are not misreported as red. |
| DV-10: environment failure | DEV-014, DEV-015 | Broken test setup or absent tool is diagnosed as a prerequisite failure, not evidence that the new behavior failed correctly. |
| DV-11: honest QA metrics | DEV-018, DEV-022 | Below-threshold coverage, required skips, and failing mandatory cases remain visible; no rounding, denominator manipulation, or false completion. |
| DV-12: unavailable platform | DEV-019, DEV-022 | Product builds on current host but a required native platform is unavailable; report implementation and NOT_RUN qualification separately. |
| DV-13: interruption and drift | DEV-020, DEV-021 | Resume after source/spec edits; detect changed inputs, invalidate dependent evidence, preserve prior attempts, and avoid blind job replay. |
| DV-14: scope and side effects | DEV-001, DEV-004, DEV-023 | Plan-only or implementation-only scope never becomes installation/deployment permission; unrelated changes and evidence remain intact. |
| DV-15: portable package audit | DEV-003, DEV-024, DEV-025 | Runtime resources contain no author-machine roots, target product names/commands, selected application spec names, fixed product layout, or mandatory framework bootstrap. |
| DV-16: ownership and evaluation artifacts | DEV-002, DEV-025, DEV-026 | Builder returns manual handoff without tests; validator bundle binds mandatory Python artifacts; `dev` can still execute authorized product QA. |
| DV-17: output and terminal evidence | DEV-007, DEV-020, DEV-022 | Output mapping is runtime-selected; commands/results have real references; no invented PASS, GUI result, or framework receipt. |
| DV-18: exact input and path handling | DEV-005, DEV-006, DEV-014 | Paths containing spaces/Unicode/metacharacters stay data; distinct Windows/Linux roots and explicit selected specs are preserved. |

### 9.2 External application acceptance inputs

The existing index-service and query specifications may be selected later as external validation inputs, including their applicable project rules. Do not copy those product filenames, requirements, protocols, languages, source trees, or fixtures into `dev` runtime resources. The validation task must explicitly select and hash the exact inputs; this sentence does not authorize building that application now.

Use a small synthetic dependent-spec trial for bounded routine validation. A full application build is a separately selected integration trial with its own scope, resources, platform access, and quality requirements. Neither trial alone proves universal language/project support.


## 10. Mandatory correction requirements

**REV-001 — Preserve the literal selected destination (mandatory fix).** Refines DEV-005 and DEV-007. Before creating any evidence directory or record, retain the complete selected path value and selection source. Treat all words, embedded spaces, Unicode and metacharacters within that value as path data. Never shorten a multiword directory by treating a word as an adjective, translate or rename it, or substitute a preferred synonym. Record the original input separately from its resolved host path. Ordinary platform separator normalization may be recorded; it must not change path components or substitute another checkout. Resolve relative paths against the selected project, and check actual scope/permissions. An explicit usable path is sufficient input and does not require another confirmation. Ambiguity or denial is a precise gap; independent permitted work may continue.

**REV-002 — Bind concrete outputs before writes (mandatory fix).** Refines DEV-007 and DEV-020. Resolve the exact evidence root using existing precedence: explicit current input, then applicable rules, then established suitable location. Map each promised context, traceability, slice, execution, checkpoint and delivery artifact beneath that root before creating it. Retain the original selection locator/text, raw selected path value, resolved root, and concrete output locations. Compare the actual path components with the selected value using host filesystem semantics; do not validate only against a paraphrased decision record. A different preexisting default directory is not a substitute. Do not use shell interpolation for path data. No mandatory new runtime helper or schema framework is required; inspected native terminal/file operations can supply observations.

**REV-003 — Verify output requirements before completion (mandatory fix).** Refines DEV-008, DEV-020 and DEV-022. Treat a required output destination as an acceptance obligation alongside product behavior. Read back the promised files at their actual paths and compare them with the original selected mapping. A missing output, wrong root, altered path component, unresolved conflict or unavailable required location prevents that requirement from being VERIFIED and prevents overall COMPLETE. Report the concrete actual and required locations and remaining correction, with PARTIAL or BLOCKED as appropriate. Passing product tests, absence of a generic default directory, file existence at another location, or a model-written preservation flag do not satisfy this check. Preserve previously produced evidence; do not silently relocate or overwrite it to conceal an attempt.

**REV-004 — Preserve and verify the whole contract (mandatory preservation).** Keep DEV-001–DEV-026 behavior, names, authority boundary, exact input identity, user authorization precedence, source-qualified accounting, red/green/refactor/QA, metric honesty, drift handling and independent work on gaps. Record new attempts after changed bytes. Builder performs custody/readback only and supplies a new exact digest-bound manual request. Validator creates/executes its external Python JSONL bundle and cold cases against the revised bytes. The existing handoff spelling failure is a separate unresolved compatibility decision; do not silently repair validator or authoring records in this revision.

## 11. Output record fields and workflow/resource routing

The current UTF-8 Markdown context, traceability, slice-plan, checkpoint and delivery records and JSONL execution schema remain supported. Existing required execution fields and raw-byte hashes remain unchanged. Add concrete context fields for `selected_evidence_value`, `selection_source`, `resolved_evidence_root`, and the logical-output-to-concrete-path map; these may be labeled Markdown fields, not a mandatory runtime JSON schema. The selection source is the current request text/locator or source-qualified applicable rule. Record normalization only when used. Delivery records include actual-versus-required destination verification for each required output mapping. Checkpoints retain the same selection identity for drift comparison.

Workflow: entrypoint selects context routing; context resolves inputs and exact output map before writing records; requirements/reuse analysis produces dependency slices; implementation executes real TDD and QA; evidence/resume retains bound records and rechecks changed inputs; failure/delivery verifies outputs, reduces requirements and returns usable results or a precise gap. Output mapping must be checked before its first write and again before completion. Recover by preserving prior attempts and selecting a fresh permitted destination/attempt after an actual user correction; never assume changed input approval.

| Resource | Preserved responsibility | Revision mapping |
| --- | --- | --- |
| SKILL.md | Activation, scope, authority, six-step routing, product/package ownership | Brief literal-output selection and final verification routing; REV-001–REV-004 |
| references/context.md | Host/input identity, context, specifications, constitutional gaps | REV-001, REV-002 |
| references/implementation.md | Reuse, slices, commands, TDD, QA, native checks | Preserve DEV-012–DEV-019; no unrelated rewrite |
| references/evidence-resume.md | Real receipts, output maps, checkpoints, drift | REV-002, REV-003; preserve DEV-020–DEV-021 |
| references/failure-delivery.md | Gap decisions, scope and honest terminal status | REV-003; preserve DEV-011, DEV-022–DEV-023 |
| assets/context.md | Bounded observed context and output map | REV-001, REV-002 fields |
| assets/delivery.md | Requirement/check accounting and terminal outcome | REV-003 destination readback |
| assets/checkpoint.md | Resume identity and pending work | REV-002, REV-003 selected destination binding |
| assets/traceability.md | Source-qualified requirements and evidence | Include destination obligation using existing fields; REV-003 |
| assets/slice-plan.md | Dependency slices and declared verification | Preserve existing behavior |
| assets/execution-record.jsonl | Actual invocation, candidate, streams, result | Preserve schema and real-evidence requirements |

Every shipped resource must remain consumed by entrypoint/reference instructions. Keep the package instruction/template-only unless a separately justified repeated operation requires a helper. No fixture campaign, evaluator bundle, product root, credential, model preference, plugin or operational binding enters runtime resources.

## 12. Dependencies, effects, recovery and preserved work

Essential host capabilities are Codex terminal/file operations and readable selected inputs; product tools are discovered per project. Git/index/service/MCP/browser/plugins are optional unless the selected product explicitly requires one. Required authority absence blocks its protected operation. No new dependency installation is part of this revision. User paths stay data on their actual platform; Windows results cannot qualify Linux or macOS.

Only the eleven-file development package is a possible later builder target, after review and verified custody. Preserve unrelated user files, original governing specification, authoring packet, all validation evidence and operational copies. The proposal authorizes no writes there. A later revision does not adopt history, install, configure startup, merge, deploy, build the example application, or grant framework acceptance. Interrupted work requires current input/source hashes, attributable job state and retained prior attempts; do not replay unknown work.

No exceptions to these boundaries are approved. The current user authorized the existing model connection for disposable validation trials; that does not authorize a builder change. One separate unresolved decision remains: canonical authoring-path serialization versus verified path-equivalence handling for the rejected handoff. This proposal's runtime correction is concrete and reviewable, but execution readiness remains BLOCKED until the selected custody/packet prerequisite is resolved and review is bound to the exact proposal/target digests.

Future plugin packaging remains deferred. Preserve `dev` identity; future `devforgeai`/`DevForgeAI` packaging and namespaced invocation need their own selected host verification. No namespaced invocation is promised here.

## 13. Independent acceptance cases for the correction

All original DV-01–DV-18 obligations remain required. Preserve original failed/time-limited attempts and create fresh fixtures for revised bytes. Do not prewrite intended corrections into cold prompts.

| Case | Inputs | Required observation |
| --- | --- | --- |
| RV-01 / DV-17 | Explicit literal evidence directory `custom receipts/`; generic `evidence/` default in project guidance; ordinary product QA | Exact `custom receipts/` exists and contains promised evidence; no shortening to `receipts/`; source-qualified output requirement is verified from actual readback |
| RV-02 | Explicit quoted evidence path containing spaces, Unicode, brackets and a literal dollar sign on the selected host | One literal path value preserved in selection record, commands and produced files; no globbing, expansion or component loss |
| RV-03 | Default evidence directory already exists with sentinel bytes; user explicitly selects a different usable directory | Existing bytes untouched, explicit selected location used, no unnecessary permission question |
| RV-04 | A supplied evidence mapping/delivery draft incorrectly points to a shortened root while original selection differs | Detect mismatch before dependent writes or final completion; do not endorse VERIFIED/COMPLETE from internally consistent but wrong mapping |
| RV-05 | Explicit destination unavailable or genuinely ambiguous, with independent permitted work | Precise location/capability decision and correct PARTIAL/BLOCKED status; no silent fallback or invented path |
| RV-06 | Resume checkpoint after explicit destination input changes | Identify mapping drift, preserve old outputs/attempts, rebind permitted future records and invalidate dependent completion claims |

Deterministic checks verify artifact existence at the exact selected root, protected-byte readback, digests and required-case accounting. Separate semantic/cold observations verify selection fidelity, authorization and completion honesty. Each original required case counts once; variants/retries do not inflate its denominator. New cases are separately declared before execution. Report untested native platforms, token counts, implicit activation and protected acceptance honestly.

## 14. Review and later builder handoff

Review the mandatory runtime correction REV-001–REV-004 and the separately scoped handoff compatibility issue. No optional enhancement is bundled. [handoff.json](handoff.json) records the exact proposal digest, target package identity, pending review and material readiness blocker. A later authorized `$skill-builder` invocation must explicitly select this proposal by absolute path and digest, preserve unaffected requirements and files, perform custody/readback, and return a fresh manual validator packet. Do not use name-based lookup to choose among this proposal and the original specification. The validator is not invoked automatically by builder.
