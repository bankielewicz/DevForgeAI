# QA post-MVP authoring delivery

Authoring: AUTHORED. Destination: `C:\Projects\DevForgeAI\src\agents\skills\qa`.

Updated the existing nine resources for ordinary QA `run` intent, same-invocation planning/preparation/execution, dependency-aware readiness, integrity-first inspection, evidence-based stop classification, complete-collection metric decisions, report/fix ownership and retained resume/retest state. Explicit planning-only, >=95% floors, stricter project policy, independent oracles and platform qualifications remain required. No runtime helper was added.

## Bound inputs and history

- Extension: `C:\Projects\DevForgeAI\docs\specs\qa-skill-postmvp-spec.md`; SHA-256 `855cfca3a95d45efb7acb62593a473fe5043450b61cf912af8ea9839edb69b4a`.
- Companion MVP: `C:\Projects\DevForgeAI\docs\specs\qa-skill-spec.md`; SHA-256 `6378025552bbbc4bfdaff8f1d3d14443cfacf44986f51f98845797b116b53e03`.
- Precedence: extension only supersedes its listed MVP clauses; all unamended requirements and applicable QV scenarios remain selected.
- Prior authored baseline: `20260914T1748018341005Z`; original package digest `2ba0d049f58360a0360031789bce5c9045153540e200d363c8caa4f5c7be2db7`. Its published record and baseline snapshot were verified by the custody helper; prior files remain in place.
- Delivered package: 9 files, 79946 bytes; SHA-256 package digest `bb9b461276a959fe5278117b6687b3edce1342149ae2dd1b5ea82fb03e1d38ed`.
- All nine paths changed; no additions/removals. See [applied.diff](applied.diff) and [authoring record](authoring-record.json).
- The operational `.agents/skills/qa` manifest matches its pre-authoring capture. Both supplied specifications and all bound source inputs still match their recorded bytes.

## Requirement-to-resource mapping

| Requirement | Changed or retained resources |
| --- | --- |
| QAP-001 | `SKILL.md`, `references/intake-planning.md`, `agents/openai.yaml` |
| QAP-002 | `SKILL.md`, `references/intake-planning.md` |
| QAP-003 | `references/intake-planning.md`, `assets/test-plan-template.md` |
| QAP-004 | `SKILL.md`, `references/intake-planning.md`, `references/execution-integrity.md` |
| QAP-005 | `references/execution-integrity.md` |
| QAP-006 | `references/execution-integrity.md`, `assets/qa-report-template.md`, `assets/qa-fix-template.md` |
| QAP-007 | `references/assessment.md`, `assets/test-plan-template.md`, `assets/qa-report-template.md` |
| QAP-008 | `SKILL.md`, `references/execution-integrity.md`, `assets/test-plan-template.md`, `assets/qa-report-template.md`, `assets/qa-fix-template.md` |
| QAP-009 | `references/execution-integrity.md`, `references/intake-planning.md` |
| QAP-010 | `SKILL.md`, `references/assessment.md`, `assets/qa-report-template.md`, `assets/test-plan-template.md` |
| QAP-011 | `references/reporting-handoff.md`, `assets/test-plan-template.md`, `assets/qa-report-template.md`, `assets/qa-fix-template.md` |
| QAP-012 | `SKILL.md`, `references/reporting-handoff.md` |
| QAP-013 | `references/reporting-handoff.md`, `assets/test-plan-template.md` |
| QAP-014 | `SKILL.md`, `references/reporting-handoff.md`, `manual-evaluation-obligations.md (external authoring input)` |

QA-001 through QA-026 remain the companion contract; unchanged criterion inventory/oracles, source bindings, test-integrity definitions, execution categories, numerical floors, manual dev ownership and independent retest lifecycle remain in their existing references. The bound [manual evaluation obligations](../20260914T193851Z-inputs/manual-evaluation-obligations.md) preserve QV-01 through QV-21 with compatibility amendments and require QPV-01 through QPV-21. These are future evaluation requirements, not executed cases.

## Authoring review and custody

Read the entry instructions, four phase references, all three templates and UI metadata before editing and after staging. Reviewed mode routing, stop versus continuation decisions, complete versus partial metrics, explicit plan non-verdict, artifact-delivery failures, literal path preservation and legacy-plan resume. Existing package-relative links still name the same consumed resources; no new runtime dependency or concrete authoring path was introduced. A requested `rg` prose search found old broad patterns only in ordinary-run lines mentioning planning; those lines were inspected directly. This was authoring text review, not a structural checker or behavioral test.

The publication helper rechecked original input and current package bytes, compared baseline/current/candidate, rechecked each written path and read back the complete delivery before publishing the next baseline. [Delivery readback](delivery-readback.json) independently records byte correspondence and operational preservation. [Command receipts](authoring-command-receipts.json) record exact custody commands, host, interpreter and outcomes.

Validation: NOT_PERFORMED. Testing: NOT_PERFORMED. Framework acceptance: NOT_EVALUATED. No red/green, native-behavior, coverage or skill-acceptance result is claimed. No structural checker, grader, test suite, generated skill sample, cold trial or product QA was executed. No authoring conflict remains. Evaluated-build completeness remains unproven until the separate validator produces and executes the required exact-byte-bound Python bundle.

## Manual validator handoff

Request: `C:\Projects\DevForgeAI\docs\plan\skill-authorings\qa\20260914T193851Z\validation-request.json`

Request SHA-256: `40ac8bd62b6e0d8b1216acef54d487f38e5708655dc7cfe5ca5dde6cac3aaa2f`

Use [the generated manual request](validator-request.md), or paste this into a Codex conversation in `C:\Projects\DevForgeAI`:

```text
$skill-validator Validate and test C:\Projects\DevForgeAI\src\agents\skills\qa using C:\Projects\DevForgeAI\docs\plan\skill-authorings\qa\20260914T193851Z\validation-request.json (SHA-256 40ac8bd62b6e0d8b1216acef54d487f38e5708655dc7cfe5ca5dde6cac3aaa2f). Bind the exact delivered package and both selected specifications. Apply qa-skill-postmvp-spec.md precedence over qa-skill-spec.md only where amended; retain applicable QV-01 through QV-21 and add QPV-01 through QPV-21. Read the bound manual-evaluation-obligations.md input. Produce and execute the mandatory Python JSONL runner, deterministic graders, independent fixtures/expected results, schema, runtime/dependency information and digests/manifests in fresh evidence. Observe actual continuation and stop ordering with test-launch markers. Preserve old evidence and source; do not repair or install the skill. Report unavailable coverage honestly and retain compiled-Rust authority boundaries.
```

The request is a manual assessment proposal; the builder has not invoked it. Existing historical validation results do not qualify these edited bytes.
