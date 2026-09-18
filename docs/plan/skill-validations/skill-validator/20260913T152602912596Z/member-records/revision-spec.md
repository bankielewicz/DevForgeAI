---
id: SKILL-VALIDATOR-QA-REVISION-20260913T152602912596Z
skill_name: skill-validator
target: codex
status: proposed
---

# Proposed complete validator revision contract

## Identity and retained governing behavior
This revision applies only to the 75-file development skill-validator package with SHA-256 d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1. It incorporates the complete frozen skill-validator-adaptive-enhancement-spec.md (f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42) and companion shared contract (8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59). Their copies are in inputs/. All unchanged inputs, outputs, schemas, roles, runtime interfaces, origin/legacy semantics, source protection, terminal operation, test obligations and failure reductions remain required. This proposal authorizes no mutation.

## Purpose, activation and inputs
Keep skill-validator's ordinary and explicit selected-set assessment triggers and all current exclusions. Inputs remain selected skill/specification, validation-request-v1, set-validation-request-v1 or explicit standalone set. Missing/ambiguous inputs remain unresolved; no set or origin history is invented. Ordinary skills acquire no adaptive metadata or operational-binding dependency. Exact specification and package identities must be checked before any later implementation.

## Outputs and workflow
Preserve snapshot/readback, source/rule/check/findings/workflow records, schema-1 references, separate supplemental records, reports and review-before-repair handoff. Helpers retain current public argv, strict JSON output shape, 0/1/2 exit semantics and read-only effects. Inputs are checked before dependent work; invalid records are rejected with specific evidence. Assessment completion remains distinct from PASS. Required failures dominate incomplete coverage, and optional recommendations cannot override failures.

## Mandatory revisions and independent acceptance
- REV-001 (QA-01): Maintain one canonical identity set across all member-check and integration-check artifact references. Reject reuse across roles before aggregating. Accept distinct valid artifacts; reject R06 unchanged. Count each applicable required row exactly once and keep unknown rows in total. A copied but intentionally separate record needs its own case identity; do not treat a byte-copy as new execution evidence.
- REV-002 (QA-02): Derive required handoff coverage from immutable input. A required handoff must have an applicable required observation, or an unknown/unperformed required row that keeps the set INCOMPLETE. Reject its exclusion as NOT_APPLICABLE. Optional absence follows its separately declared contract and must not fabricate a required producer success. Reject R07 unchanged; accept R01-R03 controls; preserve genuine N/A for genuinely inapplicable rules.
- REV-003 (QA-03): Extend contextual candidate extraction to exact protocol identifiers in structured text, including JSON schema_version strings. Emit exact byte/code-point locators and original/normalized forms as unresolved candidates. Detect P08 unchanged. Preserve P02, P04 and P14 behavior and legitimate multilingual prose. Never normalize source, blanket-fail Unicode, leak adjacent secrets, or claim exhaustive confusable detection.
- REV-004 (QA-04): Parse closing Markdown fences with allowed trailing whitespace only, same marker and adequate length. P07 must have no missing-resource failure, while P06 still fails and P05 retains supported anchors. Add backtick/tilde, nonclosing info text, empty closing tail, shorter fences and line-locator controls. Unsupported renderer details remain manual, not fabricated universal failures.

## Resource mapping and implementation responsibility
A later explicitly authorized implementation uses $skill-creator; this validator-only assessment performs no repair. REV-001/002 map to scripts/adaptive_observe.py and independent plus in-package regression cases. REV-003/004 map to scripts/text_resources.py and matching regression cases. Update explanatory references only where needed to document actual behavior. If executable/evaluation artifacts change, refresh the package's evaluation manifest through its documented maintenance procedure; retain every older manifest and failed attempt. Do not relax closed schemas merely to accept invalid records.

## Dependencies, effects and recovery
Use the existing Python 3.10+, PyYAML and declared local interfaces. No installs or guessed tokenizer conversions. Development package changes require a new explicit bounded authorization; operational .agents/.claude/.codex, companion source, original specifications, prior evidence, hooks/CI and Rust remain preserved. Interrupted attempts retain partial outputs; retries use fresh linked runs. Changed selected input invalidates dependent results and prior approval.

## Required verification and delivery
Follow repository red -> green -> refactor -> QA. Run unchanged external reproducers before fixes and preserve expected failures; then run all existing regression cases plus the new counterexamples. Run a fresh independent $skill-validator assessment of delivered bytes. Reconcile all 69 VA/AV/VAT obligations, complete the outstanding native whole workflow/resume and origin/relocation branches, test each needed caller rejection scenario and required producer-failure blocking, and measure coverage against a declared complete executable denominator. Existing Windows executed-line measurement is below 95%; no passing percentage may be guessed or rounded upward. Local encoding absence remains explicit; no download is authorized. Installation and Rust qualification are separate and unperformed.

## Review state and custody prerequisites
All four fixes are proposed, none selected by this report. No optional enhancement is bundled. The exact current maintenance identity and original baseline snapshots are verified, but no new authored/generated/adopted execution baseline is established by this QA run. Before a later repair, select the proposal digest and fixes and verify the applicable authoring/custody basis (or separately authorize observed scoped edit/adoption as required). Current package or proposal drift requires fresh selection. Missing execution custody is BLOCKED independently of the pending proposal review; the defect contract itself is reviewable.
