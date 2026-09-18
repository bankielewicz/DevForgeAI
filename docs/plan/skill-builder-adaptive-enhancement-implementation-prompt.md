# Implementation Prompt: Skill Builder Adaptive Enhancement

Use this prompt in a Codex CLI terminal session rooted at `C:\Projects\DevForgeAI`. It implements only the builder enhancement. Run the validator implementation with its [separate prompt](skill-validator-adaptive-enhancement-implementation-prompt.md); neither prompt installs the resulting skills. The supplied specifications are proposed until a current user request selects their implementation. Submitting the prompt below is that explicit selection for its bounded scope.

Governing document: [builder specification](skill-builder-adaptive-enhancement-spec.md). Shared assessment contract: [validator specification](skill-validator-adaptive-enhancement-spec.md). The digests below bind the exact document bytes delivered with this prompt. A later specification edit requires a reviewed, updated prompt; do not silently substitute it.

```text
Use $skill-creator to implement this enhancement of the existing skill-builder development package.

Load the actual skill-creator instructions at:
C:\Users\bryan\.codex\skills\.system\skill-creator\SKILL.md

If that installation path is unavailable in this CLI session, resolve the installed skill-creator from the current skill catalog. Do not install or create a replacement. If the skill is unavailable, report that prerequisite and stop implementation.

PROJECT ROOT
C:\Projects\DevForgeAI

ONLY SKILL PACKAGE YOU MAY MODIFY
C:\Projects\DevForgeAI\src\agents\skills\skill-builder

GOVERNING SPECIFICATION
C:\Projects\DevForgeAI\docs\plan\skill-builder-adaptive-enhancement-spec.md
SHA-256: 8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59

COMPANION SPECIFICATION — READ-ONLY INTERFACE AND ASSESSMENT INPUT
C:\Projects\DevForgeAI\docs\plan\skill-validator-adaptive-enhancement-spec.md
SHA-256: f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42

READ-ONLY COMPANION PACKAGE
C:\Projects\DevForgeAI\src\agents\skills\skill-validator

AUTHORIZATION

Implement BA-001 through BA-014 and all behavior defined by the governing specification. Use skill-creator for the maintenance edits, not skill-builder to modify itself. Use skill-validator for assessment and testing where its existing interface applies, supplemented by the governing specification's explicit cases and an independent terminal test harness for new interfaces.

This request authorizes development-source edits in the one package above, fresh implementation evidence, and bounded synthetic testing. It does not authorize modifying the companion package, operational skill copies, personal skills, the skill-creator installation, either governing specification, old evidence, hooks, CI, plugin packaging, installation, remote publication, or Rust enforcement.

The resulting builder remains authoring-only. That runtime restriction does not prohibit testing the builder implementation during this explicitly authorized maintenance task. Do not add automatic validator calls or generated-skill quality execution to normal authoring.

1. GROUND AND PRESERVE

Read applicable AGENTS.md files, skill-creator, both complete specifications, the current builder package and its referenced custody/schema interfaces. Inspect the companion interfaces needed for compatibility without changing them. Verify both specification digests before mutation; a mismatch stops dependent implementation and must be reported with actual hashes.

Recheck the real development package rather than relying on an attached or operational copy. The specification recorded builder package digest 65e5513cdb531cbfb1d9ef3eb9a1665f4221b1993ea0e5fbd1eb8e20fa6cc680. If current bytes differ, preserve them, inspect the differences and record compatibility before dependent edits. Do not reset another session's work, resurrect removed files, or infer missing history from a missing convenient pointer. A conflicting material requirement or corrupt known origin is a concrete blocker; compatible maintenance changes may be preserved without asking again for already-authorized work.

Create a fresh UTC evidence run under:
C:\Projects\DevForgeAI\docs\plan\skill-adaptive-implementations\skill-builder\<run-id>\

Capture bounded target bytes/manifests, input document hashes, the current request, environment/tool identity and an implementation log there. Enumerate before recursion; preserve existing exclusions/no-follow rules and capture ceilings. No actual project UUID or operational binding contents may enter source or generic evidence. Inspect commands before executing them.

Map each BA requirement and BAT case to the planned instructions, scripts, schemas, fixtures and evidence. Resolve discoverable facts locally. Do not add a generic framework dispatcher or substitute advice for a required implemented behavior.

2. IMPLEMENT THE BUILDER CONTRACT

Preserve existing conversational create/edit/import/adopt/specification modes, portable destination selection, baseline/current/candidate write protection, observed-first-edit behavior, legacy meanings, and manual validation-request-v1 handoff.

Implement the specified propose, author_set and review_updates behavior. Ground proposed responsibilities in captured project evidence; retain existing coverage instead of generating duplicate expert personas. A project-specific core change becomes a separately identified variant with full parent requirement dispositions, preserving core bytes. Expertise roles require actual domain evidence and explicit inputs, outputs, effects and handoffs.

Implement the closed new schemas and read-only adaptive.py inspect/plan-set interfaces. Existing closed legacy schemas must retain their fields and meanings. Set envelopes reference existing per-member authoring/validation records. Implement dependency closure, deterministic topological order, independent continuation after failures, truthful per-member/aggregate states, and explicit full_set versus eligible_subset validation requests with complete omissions.

Author portable adaptive descriptors, linked contracts and the generic check_project_binding.py runtime template. Keep concrete project identity outside src and generated development packages. Operational binding setup remains separate; only disposable trial projects may receive synthetic .agents/devforgeai/project-binding.json records. Detect absent, mismatched, stale, inactive and ambiguous bindings with the specified exit codes and sanitized observations. Do not expose the UUID in helper output.

Support Codex CLI and local terminal tools. Do not invent an available DevForgeAI Rust CLI, transition command, hook, privileged gate or acceptance receipt. Missing essential capabilities produce the specified failure. Never require GUI, browser, MCP, plugin packaging or an external application service.

Keep mode-specific procedures and schemas in the routed resources defined by the specification. Preserve supported metadata and automatic invocation. Inspect consumers before removing resources; avoid duplicated manuals, empty scaffolds, fabricated context metrics and ceremonial instructions.

3. TEST AND ASSESS THE MAINTENANCE CHANGE

Use the existing skill-validator as the maintenance assessment owner by explicitly reading its selected entrypoint. Keep that invocation bounded to the builder development package and disposable tests. It is acceptable that the old validator cannot yet implement every new automatic check; execute the independently specified missing cases with the local test harness and label their methods/results accurately. Do not claim the validator itself has already been enhanced.

Exercise BAT-01 through BAT-17, including positive and negative record cases, source identity separation, runtime binding behavior, hostile path characters, core preservation, stale evidence, dependency failures and existing custody/history compatibility. Retain oracles before execution. Builder maintenance test files may live in this fresh evidence run; do not put a test campaign in ordinary generated skills or modify validator to host these tests.

Run skill-creator's actual installed quick_validate.py against delivered builder bytes as a limited structural observation. Run meaningful new/changed helper tests with Python -B -X utf8. Discover existing relevant regression tests before selecting commands; do not assume a builder tests directory still exists or equate an empty unittest discovery with success. Inspect any new script before its disposable execution.

Use bounded Codex CLI cold tasks for applicable behavior cases when the existing host can run them. Keep intended fixes, expected answers and grader labels out of cold prompts. Use the actual supported CLI flags, existing authentication/model and contained fixture roots. Do not bypass sandbox/approval or hook-trust controls. Default timeout is 120 seconds per attempt; retain each failure/retry separately. Missing host/tool/native coverage stays NOT_RUN and cannot support a completed verification claim.

An actual builder-to-enhanced-validator integration test is separate from shared schema fixtures. If the companion implementation is not present, mark that integration NOT_RUN and provide a concrete later test request; do not broaden this task by implementing validator.

4. READ BACK AND DELIVER

Recheck target bytes, applicable input/spec hashes, linked resources and every requirement/case mapping. Verify that source contains no concrete project identity, original installation-root constants or copied binding records. Confirm the companion package, operational packages and old evidence were not changed by this task.

Preserve partial work and failed attempts. A failed/unavailable required check cannot become PASS; distinguish authored implementation from verified implementation, current static evidence from native behavior, and development testing from future Rust qualification.

Return the changed development paths, exact package digest, implementation log and assessment evidence, per-requirement coverage, actual commands/results, unresolved gaps and any specific remaining native/integration tests. Do not install, update .agents, modify the specification, invoke an automatic repair loop, or start another enhancement after this deliverable.
```
