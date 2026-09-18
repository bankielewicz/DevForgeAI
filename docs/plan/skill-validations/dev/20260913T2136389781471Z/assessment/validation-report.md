# Dev skill validation assessment

**Assessment: INCOMPLETE. Selected manual packet: REJECTED.** Assessment completed as a standalone review of the explicitly selected package and specification. No runtime skill defect was confirmed by performed semantic/structural checks; unperformed behavior prevents a passing overall result.

Package: `7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae`. Request: `7ebe47919c03b654614dcfa5ff288c0e58a3870615582e798780c74e8cfa15d6` (verified). Specification: `b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265` (verified). [Source manifest](source-manifest.json), [origin](origin-record.json), [binding audit](input-binding-audit.json), [pinned rules](rule-set.json).

## Input rejection and scope

The actual installed validator intake exited 1: `authoring contract/request mismatch`. Contract target_root uses forward slashes; request and authoring record use backslashes. They resolve to the same Windows directory, but the installed helper compares strings exactly. Every separately audited reference digest matched. This is a reproducible handoff compatibility failure, not evidence that package bytes changed. The rejection is retained; no binding was normalized or silently accepted. See [finding](findings.json) and [correction decision](handoff-correction.md).

The assessment records live here; original run preparation, trial plans, execution bundle and raw attempts remain unchanged in the parent directory. Exact copies of necessary execution inputs are under inputs/ so the legacy schema-1 checker does not interpret external evaluator schemas as its own records. This is one selected package assessment, not duplicate case counting.

## Results

| Dimension | Outcome | Required evaluated/applicable |
| --- | --- | --- |
| standards | INCOMPLETE | 13/14 |
| workflow | INCOMPLETE | 10/11 |
| instructions | PASS | 18/18 |
| behavior | INCOMPLETE | 1/19 |

All DEV-001 through DEV-026 and all 29 AV catalog entries are accounted in [checks](checks.jsonl). Semantic conformance: DEV-001–DEV-025 passed instruction review; DEV-026 remains incomplete. Ordinary-skill adaptive rules and absent optional host metadata are justified NOT_APPLICABLE. [Requirement observations](semantic-observations.json) and [workflow map](workflow-map.json) retain source locations.

Structural observation and installed Skill Creator checker both exited 0. The package helper exited 2: source-named snapshot identity and contextual placeholder candidates required manual review. Original directory identity resolves the former; intentional template slots and prose rejecting vague TODOs resolve the latter. Raw helper output is unchanged. All 11 files are reachable; no specified Unicode candidates, broken local links, unresolved anchors, hidden fixed product paths or required bootstrap found. Token counts are NOT_RUN because the installed tokenizer lacks the selected local encoding cache; no download was attempted. Exact text size: 34045 bytes, 11 files; entrypoint 4,462 bytes and 34 lines. No token budget was selected.

The official [Build skills guidance](https://learn.chatgpt.com/docs/build-skills) was retrieved read-only and retained. It corroborates required name/description, optional resources and description-based routing. The pinned AV/project rules are the assessment contract; this is not a claim of exhaustive current standards coverage.

## Mandatory external evaluation bundle

Created and executed: Python JSONL runner, deterministic graders, 18 scenario definitions, synthetic Python and JavaScript fixtures with distinct layouts, independent expected observations, evidence schema, runtime/dependencies, and SHA-256 artifact manifest bound to the exact package and governing inputs. [Bundle manifest](inputs/bundle/artifact-manifest.json), [scenario definitions](inputs/bundle/scenarios.jsonl), [execution summary](inputs/bundle-attempt-001/summary.json).

The runner verified 69 artifact hashes plus package/input bindings, then exited 2 for incomplete coverage. DV-15 portable audit passed. DV-01–DV-14 and DV-17–DV-18 are NOT_RUN because cold authenticated model execution was not authorized under the packet's network/credential restrictions. DV-16's artifact subcheck passed, but the full scenario is NOT_RUN because the manual handoff was rejected and product QA behavior was not executed. **Required DV cases: 1/18 passed (5.555555555555555%), 17 NOT_RUN.** This misses the 95% required-case minimum and leaves mandatory scenarios unsatisfied. No cold workflow, native implicit activation, independent description-classification agent, cross-language build, interruption behavior, native visual check or full example application was executed. Semantic routing self-review is separate.

The bundle contract was tested red before creation (two expected missing-artifact/scenario assertion failures), then green (2/2 tests). Deterministic grader regression/negative tests passed 21/21, including stale bytes, duplicate records, paths, false PASS and denominator handling. These 23 evaluator tests are separate from the 18 skill cases and do not inflate their denominator. No production refactor was needed. Framework executable-line/branch coverage, formatting/Clippy/platform qualification are NOT_RUN: no executable framework implementation was selected. Evaluator test success is not framework acceptance or general skill behavior.

## Preservation and next action

Complete capture: 11 files, no exclusions, within 2,000-file/32 MiB ceiling; no links followed. Final source readback matched the selected package. Original specification and retained rule-source/input hashes were rechecked. Development target, operational skills, authoring packet and prior evidence were not repaired or installed. No plugin or example application was built.

Builder readiness: **BLOCKED** by rejected handoff and incomplete behavioral evidence. No dev revision-spec.md is proposed because no runtime change is justified by performed checks. Review the separate handoff compatibility decision; a newly bound packet and authorized cold trials require fresh evidence. Installation: **NOT_PERFORMED**. Framework acceptance: **NOT_EVALUATED**.
