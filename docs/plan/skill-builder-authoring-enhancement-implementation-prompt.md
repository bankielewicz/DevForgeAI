# Codex prompt: Implement the Skill Builder authoring enhancement

Copy the prompt below into Codex to authorize and perform the implementation.

```text
Use $skill-creator at:
C:\Users\bryan\.codex\skills\.system\skill-creator\SKILL.md

Apply its authoring guidance to update both development packages according to the approved enhancement specification:
C:\Projects\DevForgeAI\docs\plan\skill-builder-authoring-enhancement-spec.md

Specification SHA-256:
43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14

Project root:
C:\Projects\DevForgeAI

Development targets:
- C:\Projects\DevForgeAI\src\agents\skills\skill-builder
- C:\Projects\DevForgeAI\src\agents\skills\skill-validator

Use $skill-validator for testing and validation of the delivered changes. Read its operational instructions at:
C:\Projects\DevForgeAI\.agents\skills\skill-validator\SKILL.md

AUTHORIZATION AND SCOPE

This authorizes implementation of the specification in both development packages, supporting evidence capture, and validator-owned testing and validation. It is an implementation request, not another specification-writing task.

Read the actual specification, applicable AGENTS.md files, both development skill packages, the installed skill-creator instructions and relevant helpers, and the referenced documents under docs\codex.

Verify the specification digest before mutation. If it differs, preserve and report the discrepancy and stop dependent changes. Capture the current target manifests and inspect their known history before making edits.

Implement all requirements AB-001 through AB-014, including:
- Conversational skill creation without requiring a separate approved specification.
- Focused editing, including existing skills without builder history.
- Portable destination selection.
- Bundled scaffolding and UI metadata authoring.
- Proportionate instruction and resource design.
- Distinct authoring records and baselines.
- An explicit, digest-bound manual handoff to skill-validator.

Transfer testing and validation responsibilities to skill-validator as specified. The resulting builder must not automatically invoke validator, run quality checks, or execute generated skills as tests. Preserve its custody, ownership, conflict detection, safe-write, and readback safeguards.

The authoring-only restriction applies to the resulting skill-builder workflow. It does not prohibit testing the implementation during this enhancement task. Use skill-creator to author the changes and skill-validator to assess them.

COMPATIBILITY AND BOUNDARIES

Preserve historical evidence and the meanings of legacy records. Inspect existing origins and baselines before editing; do not fabricate provenance, silently adopt around conflicting history, or reinterpret previous successful builds. Using skill-creator does not authorize bypassing applicable provenance, ownership, or safe-write requirements.

Implement a coherent migration across instructions, references, scripts, schemas, templates, profiles, fixtures, and tests where required. Keep changes limited to this enhancement. Introduce the new versioned authoring records without changing the meaning of legacy schema-1 or schema-2 records.

Update only the two development packages and create new task evidence under docs\plan. Do not modify operational .agents, .claude, .codex, installed caches, personal skill copies, historical evidence, or the supplied documentation. Do not install dependencies or skills, configure hooks or CI, or implement Rust enforcement.

Treat installed skill-creator resources as read-only reference material. Bundle any adapted helpers in the appropriate development package without depending on this machine's personal installation path, and preserve applicable source notices.

VERIFICATION AND DELIVERY

Retain new evidence in fresh directories under docs\plan. Preserve exact evaluator input snapshots and case files before execution, commands, outputs, failures, retries, and relevant digests.

Use skill-validator for implementation assessment and execute the applicable checks and behavioral trials covering AC-01 through AC-14. Include skill-creator's structural checker for both delivered packages, meaningful execution of new or changed scripts, and applicable independent behavioral trials.

This instruction authorizes bounded independent subagents for those trials. Give evaluators realistic requests and the minimum raw artifacts they need, without supplying intended answers, suspected defects, or prior conclusions unless the case requires them. Use synthetic inputs and disposable workspaces under fresh evidence directories. Do not modify other existing project skills or perform unauthorized external actions.

This authorization permits validator assessment for this implementation; it does not change the enhanced builder's manual-handoff behavior. Retain the exact validator implementation used for assessment. Distinguish assessment using the existing operational validator from trials of the enhanced development validator, and do not treat the latter's self-review as independent evidence.

Run meaningful regression checks for the changed behavior and migration, including rejection paths, ownership conflicts, stale handoffs, and legacy-record compatibility. Avoid tests that merely match wording or headings. Keep assessment proportionate to the implementation and its acceptance scenarios.

Reassess actual delivered bytes and complete readback before reporting successful delivery or publishing successful provenance. Verify that package changes are confined to the authorized development targets and that protected copies and historical evidence remain unchanged.

Distinguish structural checks, deterministic tests, routing classification, native activation, independent behavioral execution, and self-review. Do not claim success for unperformed checks or use historical evidence as a substitute for required fresh execution.

Complete the authorized implementation without requesting the same authorization again. Stop only for a concrete unresolved prerequisite, changed approved input, conflicting requirement, or actual permission restriction. If blocked, preserve completed work and explain the exact blocker.

Return:
- Actual changes to each development package.
- Migration and compatibility details.
- Authoring/provenance and evidence paths.
- Verification results mapped to AC-01 through AC-14.
- Remaining failures, unperformed coverage, and limitations.
```
