# Rules and semantic inspection

### SV-003: rule records

Each rule has `rule_id`, revision, title, source references, authority class (`format_requirement`, `official_recommendation`, `project_policy`), applicability, method (`deterministic`, `semantic`, `behavioral`), expected observation, required/advisory classification, and limitation. Pin the selected rule-set digest for each run. Do not let a mid-run refresh silently change expectations.

Mandatory format rules need an applicable authoritative source. Do not promote an example, API recommendation, local checker restriction, historical note, or preferred folder arrangement into a universal Codex requirement. Unsupported mandatory claims produce an unresolved standards question. When source documents conflict, record both and scope the uncertainty; no automatic newest-wins rule resolves a substantive contradiction.

Live refresh uses an available official documentation connector or normal authorized read-only retrieval. It is optional transport, not a required MCP/plugin installation. Bundle dated rule summaries and citations so offline operation remains possible. Record whether freshness is `live_verified`, `snapshot_only`, or `unavailable`. A snapshot-only result may establish compliance with that identified snapshot, but cannot claim current-live compliance.

### Required assessment families

| Family | Checks and limits |
| --- | --- |
| Format and identity | Required `SKILL.md`, parseable metadata, required name/description, supported fields and configuration types under the selected source version; identity consistency and scope/trigger clarity. Preserve supported optional fields. Do not require exactly six populated fields or create empty folders. |
| Discovery and invocation | Explicit and implicit trigger behavior, near-misses, applicable invocation policy, and relevant duplicate names. Development source outside `.agents/skills` is not a defect. Installation is separately scoped. |
| Progressive disclosure | Essential decisions in the entrypoint, conditional details loaded when needed, explicit resource routing, and no unread resource carrying an essential hidden condition. Length, nesting, or duplication is evidence for review rather than an invented universal line/token cap. |
| Resources | Existing links and anchors where supported, correct relative roots, meaningful scripts/templates/references, call sites, dependencies, and unused/missing material. Do not mark custom folders or extra files defective without a relevant requirement or demonstrated harm. |
| Workflow and outcome | Traceable steps, branch coverage, coherent inputs/outputs, concrete completion conditions, useful result delivery, bounded retries, and recoverable partial work. |
| Instructions | Imperative actions, consistent terminology, separation of data from instructions, examples consistent with rules, appropriate detail, explicit side effects, and no instructions pretending to override higher-priority host controls. |
| Autonomy and permissions | Honor current user direction, avoid repeated permission requests for already-authorized work, prepare reviewable output before required approval, and identify the actual instruction causing a pause. Retain user-selected review boundaries and real permission restrictions. |
| Tools and portability | Actual command/tool interfaces, shell and path correctness, required capability availability, declared effects, safe disposable execution, and honest unsupported-environment reporting. |
| Prompt grounding | Relevant context, observed source references, examples representing ordinary and failure cases, appropriate output contracts, and no invented input facts. API guidance applies only to API-backed components. |
| Model-specific guidance | Apply behavior tuning only to the identified model/host when relevant. Do not require a fixed model, obsolete parameter, or API feature for an ordinary skill. |
| Citations | References resolve to observed sources; source identity is distinct from a locator; supporting passages actually support findings; conflicting sources remain visible. Valid citation syntax alone does not establish support. |
| Verification proportionality | Required checks and useful regressions execute; tests are not repetitions of the implementation or ritual counts. Stop repeating successful checks unless changes or unresolved concerns justify repetition. |

The installed Skill Creator structural checker is a useful named observation when available, not the entire standards definition. Its absence is not a defect in the inspected skill. During package maintenance, validator owns required structural and deterministic checks; authoring completion has separate semantics.

### SV-007: ceremonial and enforcement review

For each candidate passage, retain file/line or byte span, exact bounded excerpt, context, intended behavioral effect, classification, evidence, proposed disposition, preserved requirement, and any enforcement-register reference. Candidate classification is semantic and requires context; keyword matching may suggest review locations but cannot establish a finding by itself.

Use `useful_instruction`, `redundant_wording`, `ambiguous_requirement`, `unbounded_ritual`, or `unenforced_control_claim`. Useful guidance produces no defect solely for emphasis, repetition, a checklist, XML, capitalized MUST, or imperative tone. Do not claim that LLMs universally ignore a wording style.

Examples: checking computed totals is actionable; repeating a self-score until perfection has no observable stopping criterion; announcing COMPLETE does not enforce a state transition; a real user review requirement remains meaningful. Preserve the substantive safety or correctness property when recommending edits. Do not remove the only safeguard and call the workflow improved; retain actionable guidance and document residual enforcement needs until a replacement exists.

The enforcement register uses proposed destinations `codex_hook`, `git_hook`, `github_check`, `ci_workflow`, `devforgeai_cli`, or `guidance_only`. For each, describe trigger, invariant, inputs, intended observation/action, current evidence, failure behavior, bypass/coverage limits, dependencies, and a future verification scenario. Distinguish local Git hooks from GitHub-hosted checks. These are candidates for later design, not claims that a hook event or CLI command exists. Unsupported mappings remain recommendations requiring investigation.

## Workflow mapping

Stages are instructions followed by the host, not protected DevForgeAI phase transitions. One primary agent can complete the workflow. No fixed worker count or essential independent subagent capability is required. Optional reviewers may inspect evidence when the host and user scope permit; their task prose does not establish isolation. Record whether review was self-review or independent review.

| Stage and entrypoint | Entry condition and inputs | Action and output | Exit and recovery |
| --- | --- | --- | --- |
| 1. Establish origin; `origin.md` | Invocation identifies a readable skill and project. | Resolve specification, inventory files, preserve snapshot and source manifest, record origin and user intent. Reconstruct specification when absent. | Continue with known requirements. Ambiguous origins are recorded as unresolved; do not fabricate a replacement origin. Missing target ends the assessment without invented findings about its contents. |
| 2. Establish rules; `rules.md` | Target identity and available origin observations exist. | Retrieve applicable guidance, preserve source records, select rule set and applicability, record baseline capabilities and a trial plan. | Continue using dated fallback when live retrieval fails. Unsupported assertions remain unknown; source conflicts affect only dependent rules. |
| 3. Inspect package; `rules.md` | Stable source snapshot and applicable rules exist. | Run structural observations, inspect resources and metadata, and check instruction and workflow contracts. Produce check records, workflow map, and findings. | Continue other checks after individual errors. Changes to source invalidate claims against the current target. |
| 4. Exercise behavior; `trials.md` | Expected outcomes and inspected, bounded trial procedures exist. | Execute safe disposable trials, capture outputs and side effects, and compare with expected results. | Record pass/fail/unperformed per case; do not install software or use live services merely to force completion. |
| 5. Synthesize; `reporting.md` | All attempted checks have final observations or explicit unperformed reasons. | Produce report, findings, enforcement register, and proposed revision specification if changes are justified. | Check evidence links, rule coverage, contradictions, and status reductions. Missing information remains explicit and does not become guessed behavior. |
| 6. Handoff; `handoff.md` | Report and proposed revision have been read back. | Identify builder readiness, exact target, specification path/digest, required review decisions, and provenance/adoption prerequisites. | Stop at review. Do not invoke builder or mutate target as part of a validation-only request. |
| 7. Revalidate; `handoff.md` | A later authorized builder run delivered a selected result. | Start a fresh validation run over actual delivered bytes; compare prior findings and exercise affected plus still-required checks. | Report resolved/persistent/new/unverified findings. Link prior evidence; never rewrite earlier outcomes. |

The workflow map uses one row per actual step, with `step_id`, entrypoint location, entry conditions, inputs, executor, action, outputs, completion evidence, next/branch targets, failure route, and terminal user outcome. A clear linked instruction or heading is a valid entrypoint. A script, explicit phase registry, fixed seven-stage anatomy, and separate worker are not required for every step. Implicit simple steps may be mapped from prose; explain the supporting text rather than failing missing headings mechanically.

Every path must end in a usable outcome, an explicit request for a material decision, or a concrete failure with retained evidence. Inspect success, missing input, partial output, cancellation, retry, and recovery paths where applicable. Separate creation of an output from delivery, installation, publication, or promotion; require each only if it belongs to the selected skill's contract.

## Source selection and discrepancy handling

The bundled rule summaries were compiled on 2026-09-12 from the live OpenAI Build skills page, the linked Agent Skills specification, and the selected project specification. Their source digests identify the extracted representations retained in the build evidence; URLs permit a new refresh. Copy fallback summaries into the run, record snapshot_only for unavailable original content, and do not cite a passage you have not read. A live retrieval must be saved before its digest is recorded. Preserve prior expected rules when refresh changes them mid-run.

Agent Skills permits `compatibility`; the installed Skill Creator checker observed during construction does not list that field. Report its rejection as a named checker limitation where the pinned applicable standard supports the field. Optional directories and `agents/openai.yaml` are not mandatory. Keep unknown extension metadata as an applicability question unless an authoritative selected rule resolves it. No model override or fixed model is required.

For each Markdown link, inspect supported helper observations then manually review reference-style links, HTML, unusual heading anchors or escaped destinations beyond its parser. A resolving file is not evidence its passage supports a finding. Cite source IDs and a section/line or exact byte interval against saved source content. Length/nesting guidance is a recommendation; demonstrate workflow or retrieval harm before proposing a fix.

Map simple prose steps faithfully. A success branch with a file created but no promised delivery, an input with no producer, unreachable next step, inconsistent schema between example and script, or missing failure exit merits a cited workflow/instruction observation. An unresolved contradiction belongs in the report and proposal decision list, not an arbitrarily selected implementation.

For source-backed autonomy review, honor current authorized scope and actual host controls. Do not apply API parameters to instruction-only skills. Treat model guidance as conditional, time-specific advice. Require observed effects for an enforcement claim; future hook/CLI mappings are design recommendations requiring later investigation.


## Authoring-family compatibility

For authoring-v1 inbound requests use [authoring-intake.md](authoring-intake.md). Preserve legacy record meanings. An authored baseline or observed scoped edit base may support a future authorized edit without explicit adoption; known conflicting history still blocks. Record that newer basis in a separate authoring-family assessment supplement rather than falsifying a schema-1 generated/adopted baseline or rewriting history. Testing remains validator-owned.
