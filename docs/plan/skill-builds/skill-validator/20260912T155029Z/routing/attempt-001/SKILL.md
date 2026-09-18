---
name: skill-validator
description: >-
  Validate one Codex skill's structure, instructions, workflow, and bounded
  behavior against applicable OpenAI guidance and its specification. Establish
  an origin specification when missing, report evidence-backed findings, and
  prepare a revision specification for skill-builder. Use when asked to validate
  or audit a skill, check its steps or resources, review ceremonial instructions,
  or assess a generated or edited skill before adoption. Do not use to repair or
  install a skill, audit project source code generally, or build the future
  DevForgeAI enforcement framework.
---

# Skill Validator

Assess one explicitly selected Codex development skill. Preserve its bytes and exact origin, inspect its workflow, execute authorized disposable trials, and return findings plus a proposed full revision specification for review. This is a development assessment: Python observations and model conclusions are not DevForgeAI admission, enforcement or mutation authority. Compiled Rust remains the separate future enforcement design.

## Intake and boundaries

Use the explicit target and unambiguous project root. A name must resolve uniquely within user-selected discovery locations; relevant duplicates are an input decision, not permission to audit the repository. Resolve bundled resources relative to this loaded package, and work products relative to the project. Do not install, repair, adopt, configure hooks/CI, invoke skill-builder, or operate on production data during validation.

Create a fresh UTC run directory at `docs/plan/skill-validations/<target-name>/<run-id>/`, disjoint from target, source specifications and this package. Establish boundaries before writes. Enumerate directories before recursion; omit backup directories and `devforgeai_cli` before reading/hashing. Do not follow links/junctions; reject escaping roots, traversal and special files. The default capture ceiling is 2,000 files and 32 MiB. An omission is disclosed; material omissions prevent complete restoration or assessment. Never silently truncate or raise a ceiling.

Record OS, shell, Python/PyYAML availability, installed checker identity, host task capability, user requirements and authorized effects. Python 3.10+ and PyYAML are the helper defaults; check without installation. If unavailable, continue manual independent checks and mark affected observations NOT_RUN. No future CLI is required.

## Establish the origin before assessment

Read [origin.md](references/origin.md). An explicit specification path governs; missing explicit input or ambiguous provenance/lookup remains unresolved while independent package checks continue. Otherwise verify matching provenance, then perform bounded exact `skill_name` lookup in `docs/plan` and `docs/design/specs` without precedence. Only actual absence permits reconstructing [origin-spec-template.md](assets/origin-spec-template.md). Capture existing specification bytes under `inputs/`.

Inspect [observe.py](scripts/observe.py) before executing its documented interface. `snapshot --source <target> --output <new-dir>` creates `<new-dir>/source/` and `<new-dir>/source-manifest.json`; choose the fresh run directory itself as the new-dir, with its parent existing, or capture to a disjoint fresh staging directory and transfer the exact files with verified readback. Do not precreate the snapshot output. Snapshot is the only helper command that writes. Retain partial output after errors and never treat it as complete.

Record origin kind, honest history, original absolute target, source manifest, specification reference, exclusions and uncertainties in `origin-record.json`. An observed origin is not an adopted/generated baseline; prose is not an exact backup.

## Select rules and inspect

Read [rules.md](references/rules.md); use [rules-snapshot.json](assets/rules-snapshot.json) as the dated fallback. Refresh official guidance through available read-only tools when possible, retain the retrieved content and source identity, and pin `sources.json` plus `rule-set.json` before results. Distinguish mandatory format requirements, official recommendations and project policies. Model/API advice is conditional. Unsupported assertions remain unresolved; a checker restriction is not automatically a universal format rule.

Plan applicability and required/advisory classification before checks. Run `structure --source <run>/source` and the actual installed Skill Creator checker when available, recording their limited coverage separately. Inspect unsupported links/anchors manually. Trace each real workflow step from its cited entrypoint, inputs and executor to outputs, next branches, completion evidence, failure/recovery route and terminal user result in `workflow-map.json`. Do not demand a phase registry, fixed headings or separate scripts/workers.

Review the assessment families, actual tool calls, resource routing, examples, contradictions and citation support. For ceremonial passages, retain exact contextual excerpts and intended safeguards; classify semantically rather than by keyword. Preserve useful MUST/checklists and user review boundaries. Recommendations for future mechanisms go only into the enforcement register.

## Exercise bounded behavior

Read [trials.md](references/trials.md), then plan cases before execution with independent expected outcomes, fixture digests, exact command/task prompt, executor, timeout and permitted write root. Use disposable synthetic projects under `trials/`. Inspect commands and dependencies first. Use the actual host task runner for minimal-input workflow trials when available; preserve its prompt, input package snapshot and final artifacts. Do not put intended corrections into a cold task prompt.

The default command timeout is 120 seconds. Retain each real attempt, output streams, exit/timeout, timestamps, side effects and recovery; retry as a new attempt. Do not run network/credential/external-write fixtures without adequate authority and containment. Continue static assessment when a required behavioral check cannot run; report NOT_RUN rather than PASS. Separate description classification from native implicit activation. Label validator self-review explicitly; optional independent reviews do not gain enforced isolation through task prose.

## Synthesize and deliver for review

Read [reporting.md](references/reporting.md). Write schema-1 checks, stable findings, workflow map, sources/rules and [validation-report-template.md](assets/validation-report-template.md). Produce [enforcement-register-template.md](assets/enforcement-register-template.md), or an explicit no-candidates result. Reference only already observed bytes with their actual digests and locators.

Reduce standards, workflow, instructions and behavior separately: required FAIL precedes INCOMPLETE; retain unperformed coverage even under FAIL. Report enforcement recommendations as a fifth descriptive dimension, not an implemented acceptance gate. `assessment_completed` is separate from PASS/FAIL/INCOMPLETE and builder readiness. Missing target completes intake without a package assessment.

Run `readback --source <original-target> --manifest <run>/source-manifest.json`; save stdout as `source-after-manifest.json` or retain its full observation with the contained current manifest in that file. Recheck original specification and rule-source digests. SOURCE_CHANGED limits conclusions to the retained snapshot and blocks current-byte readiness; start a fresh linked run for changed inputs. Run `records --run-root <run>` after all references exist. It checks record integrity, not semantic citation support or complete assessment quality.

Read [handoff.md](references/handoff.md). If changes are justified, use [revision-spec-template.md](assets/revision-spec-template.md) to write a complete proposed future contract; preserve origin and distinguish fixes from optional enhancements. Record missing decisions precisely. Write `handoff.json` with target/proposal digests, review state, selected/deferred findings and verified baseline/adoption prerequisites. Pending review alone is REVIEW_REQUIRED; a missing material prerequisite is BLOCKED. Never invoke the builder from this workflow. Return the report, evidence and proposal paths and exact review decisions needed.

## Revalidation and recovery

After a later authorized build, start a fresh run, compare actual delivered bytes with builder evidence, and classify prior findings as resolved, persistent, new or unverified with supporting cases. Never overwrite previous findings or reuse approval for changed proposal/target bytes. Resume an interrupted assessment only after its input identities and hashes match; preserve completed work and name the next unfinished action.

For package maintenance and bounded acceptance cases, read [evals/README.md](evals/README.md). Do not run builder-enhancement campaigns during ordinary validation.
