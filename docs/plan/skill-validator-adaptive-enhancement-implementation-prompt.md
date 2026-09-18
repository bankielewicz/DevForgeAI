# Implementation Prompt: Skill Validator Adaptive Enhancement

Use this prompt in a Codex CLI terminal session rooted at `C:\Projects\DevForgeAI`. It implements only the validator enhancement. The builder has a [separate implementation prompt](skill-builder-adaptive-enhancement-implementation-prompt.md). Either implementation may be developed against the frozen shared contracts; only an actual later run with both delivered packages establishes their integration behavior.

Governing document: [validator specification](skill-validator-adaptive-enhancement-spec.md). Shared input contracts: [builder specification](skill-builder-adaptive-enhancement-spec.md). The hashes below bind the exact specification bytes. Submitting the prompt explicitly selects their validator-scoped implementation; their proposed status alone authorizes nothing.

```text
Use $skill-creator to implement this enhancement of the existing skill-validator development package.

Load the actual skill-creator instructions at:
C:\Users\bryan\.codex\skills\.system\skill-creator\SKILL.md

If that installation path is unavailable in this CLI session, resolve installed skill-creator from the current skill catalog. Do not install or create a replacement. If it is unavailable, report that prerequisite and stop implementation.

PROJECT ROOT
C:\Projects\DevForgeAI

ONLY SKILL PACKAGE YOU MAY MODIFY
C:\Projects\DevForgeAI\src\agents\skills\skill-validator

GOVERNING SPECIFICATION
C:\Projects\DevForgeAI\docs\plan\skill-validator-adaptive-enhancement-spec.md
SHA-256: f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42

COMPANION SPECIFICATION — READ-ONLY SHARED CONTRACT
C:\Projects\DevForgeAI\docs\plan\skill-builder-adaptive-enhancement-spec.md
SHA-256: 8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59

READ-ONLY COMPANION PACKAGE
C:\Projects\DevForgeAI\src\agents\skills\skill-builder

AUTHORIZATION

Implement VA-001 through VA-015, the AV rule catalog and all required behavior in the governing specification. Use skill-creator to edit validator; do not treat an ordinary validator invocation as repair authority. Use validator guidance and a separately retained terminal test harness to assess the maintenance change, identifying validator self-review explicitly.

This authorizes the one development package's implementation, fresh evidence, and bounded synthetic tests. Do not modify builder, operational .agents/.claude/.codex copies, personal skills, installed skill-creator, specifications, previous evidence, hook/CI configuration, plugin packages or Rust implementation. Do not install dependencies, publish remotely or create a real project binding. Operational binding fixtures may exist only inside disposable synthetic projects.

1. GROUND AND CAPTURE

Read applicable AGENTS.md files, skill-creator, both complete specifications, current validator instructions/scripts/schemas/tests and the builder interfaces needed for compatibility. Verify both specification hashes before mutation. If a hash differs, report actual versus expected bytes and stop dependent implementation rather than silently selecting the edited contract.

Reinspect the actual development package. The specification recorded validator package digest 77f0eec091cb41559074296ec8b0cd7dad76329ca6647b969f0e76b49cea51a4. If the current package differs, preserve it and record a compatibility review; do not reset or overwrite another session's work. Preserve known history and baseline semantics. Material contradictions or corrupt known origins are specific blockers; compatible current changes remain preserved.

Create a fresh UTC evidence run under:
C:\Projects\DevForgeAI\docs\plan\skill-adaptive-implementations\skill-validator\<run-id>\

Retain bounded target manifests/snapshots, selected specification hashes, this authorization, environment identity, an implementation map and exact command log. Enumerate before recursion and honor existing exclusions, no-follow paths, disjoint roots and capture ceilings. Do not copy real operational project UUIDs or binding contents into source or general evidence.

2. IMPLEMENT THE VALIDATOR CONTRACT

Preserve standalone single-skill assessment, validation-request-v1 intake, source readback, origins, authoring-family supplements, legacy records, stable findings, existing required-failure precedence, and review-before-repair handoff. Existing ordinary skills do not acquire mandatory adaptive metadata.

Implement explicit selected-set intake, independent readers for shared builder contracts, complete membership/omission verification, standalone-set-input-v1, set-assessment-v1 and supplemental adaptive observations. Do not import runtime logic from builder or require its installation. Shared golden fixtures must verify agreement without loosening legacy schemas or accepting unknown versions.

Implement adaptive_observe.py package/intake-set/records as specified and preserve existing observer commands. Schema-1 helper observations and new set records must retain their declared path bases; do not reinterpret absolute versus run-relative references. Validate new evidence integrity without treating target fixtures as evaluator authority.

Implement the complete AV-F/U/R/I/C/S/W/E and AV-A catalogs: structural metadata, optional configuration, Unicode candidates, placeholders, link/anchor/resource graph analysis, contextual anti-slop, output/workflow contracts, measured context, effects/security review, adaptive role evidence, lineage, binding, portability, set handoffs and recovery. Deterministic candidate matches must remain separate from semantic defect adjudication. Preserve legitimate Unicode, useful MUST/checklists, intentional non-runtime resources and supported optional fields.

Token measurement must name an already installed tokenizer and local encoding. No automatic downloads or fabricated token conversion. Unsupported renderer anchors, dynamic resource use, unknown applicability, missing tools and unperformed native behavior must retain their actual statuses rather than produce PASS.

Test runtime project binding using only synthetic operational .agents/devforgeai records. Keep concrete identity out of src, fixture source templates, generic reports and helper output. Verify exact package/root/selection bindings, core-variant conflict, missing/stale records and absence of product effects after rejection. The editable binding is an applicability check, not Rust enforcement.

Preserve terminal-only behavior. The future Rust CLI, hooks, phase gates and protected acceptance are not available dependencies. Do not implement plugin assembly, MCP conformance, WCAG/enterprise/OWASP certification, L0-L3 scores or repository-maturity grading as substitutes for the actual specified checks.

3. VERIFY WITH INDEPENDENT ORACLES

Create expectations before executing candidates. Exercise VAT-01 through VAT-25 and cross-reference every VA requirement and applicable AV rule to retained evidence. Use known-good and seeded-defect fixtures; report false positives and misses with case IDs. Retain context-sensitive paraphrase cases required by the specification. A matching heading or model-written PASS is not test evidence.

Run installed skill-creator quick_validate.py against delivered validator bytes as a limited structural check. Run the existing validator regression suite and new meaningful tests with:
python -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -v

Inspect the suite first and preserve its existing cases. Missing/empty discovery is not a passing suite. Retain failed attempts and fixes as new attempts; do not delete failing cases to obtain a green result. Execute new or changed scripts only after inspection and within disposable roots.

Use the exact synthetic project and task-card/receipt contracts from specification section 5.4. For a positive handoff, feed the consumer the producer's real unchanged output in a fresh task. Negative malformed-input tests remain separately identified. Do not repair the producer artifact between steps or include intended corrections/labels in cold prompts.

Use actual Codex CLI task execution when host authentication, supported flags and containment permit it. Keep existing model/auth selection; no sandbox/approval/hook-trust bypass or additional real-project writable roots. Default timeout is 120 seconds per attempt. Record stdout/stderr, events, final artifacts, effects, termination and before/after manifests. Explicit loading, description classification, implicit host activation, child-task execution and self-review are distinct evidence categories.

If a host, language toolchain, native selection signal or companion implementation is unavailable, mark dependent coverage NOT_RUN and keep independent supported checks running. Do not claim a cross-platform or end-to-end integration pass from static fixtures. The companion builder may be read/tested in disposable copies when present, but it may not be edited by this task.

4. FINAL READBACK AND REPORT

Recheck delivered package bytes and selected input/specification hashes. Validate new and legacy record integrity using their actual supported interfaces, then manually assess citation support and semantic completeness. Reconcile required evaluated/total counts, unknown applicability, member outcomes, full_set/eligible_subset scope and omissions.

Confirm that the builder, operational skills and historical evidence remain unchanged by this task. Preserve interrupted or partially implemented work and identify any unfinished requirement. Do not claim implemented, tested, natively verified, installed or Rust-qualified states interchangeably.

Return changed development paths, exact package digest, requirement/rule/case coverage, actual commands/results, evidence and report paths, limitations and any specific remaining native/integration work. Do not automatically repair assessed target skills, invoke builder, refresh .agents, install anything or continue into another enhancement.
```
