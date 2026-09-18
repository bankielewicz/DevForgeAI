# Skill-builder post-MVP maintenance

Implemented the selected specification in development source. Source action: **edited**.
Maintenance delivery is complete; independent skill validation and generated-skill
testing are **NOT_PERFORMED**. No framework acceptance or operational installation is claimed.

## Delivered change

Added the external design template, closed design schema and workflow-design reference;
added optional `begin --design`, bounded input capture/readback, origin binding and
publication rechecks; extended the manual prompt with original requirements, design
identity, open questions, unperformed helper/native obligations and explicit source action.
Updated authoring, specification, regeneration, custody and handoff guidance and report asset.
Existing contract/request schemas, metadata and invocation behavior remain unchanged.

The internal boolean design_capture_requested distinguishes a legacy call that carries
design JSON as ordinary input from explicit --design selection. It is internal custody
metadata, not a new contract/request field or protected authority. Legacy no-design stages
and adaptive member/set boundaries retain their meanings.

12 package paths changed, including 3 additions; 35 existing files are byte-identical.
See [exact changes](changes.json), [patch](changes.patch), [manifest](delivered-manifest.json)
and the retained [delivered snapshot](delivered/skill-builder/SKILL.md).
Package digest: `ecb01ece2c38443e58fe7a5b307e9d0de22a1fa9b9ec1f726b79cfa328cb9c9e`.
Final source bytes exactly match the hashes captured before qa-03, including the manifest.

## Executed maintenance evidence

Native Windows, Python 3.10.11, coverage.py 7.9.0.
Final QA: **154/154 required cases passed (100%)**, no skips/nonpasses.
Elapsed final suite: see qa-03.txt. Required inventory and outcomes are in
[expected cases](qa-03/expected.json), [JSONL observations](qa-03/results.jsonl),
[deterministic reduction](qa-03/grade.json) and [coverage](qa-03-coverage.json).

Executed-line denominator, declared before collection: all first-party statements in
scripts/authoring.py and scripts/record_schema.py, no excluded lines.
**596/615 = 96.910569%** line coverage.
Branch coverage: **333/354 = 94.067797%**.
Both mandatory maintenance numeric floors are met. This focused scope is not full-package
coverage or native skill qualification. Linux and broader qualification remain NOT_RUN.

Retained progression:

| Attempt | Observation |
| --- | --- |
| red.txt | New CLI contract rejected --design before implementation; functional red. |
| green-01.txt | 9/10; subprocess fixture omitted -X utf8 and failed encoding output. Harness failure retained. |
| green-02 | 81/81 initial design plus retained authoring/custody regressions. |
| qa-01 | 148/149; junction fixture quoting failed before product behavior. Retained. |
| red-report.txt | Real unchanged publication succeeded but prompt omitted explicit unchanged action. |
| qa-02 | 150/150 after fixture and source-action corrections. |
| red-legacy-input.txt | No-design call with design-shaped ordinary input incorrectly blocked. |
| qa-03 | 154/154 after explicit internal mode fix and compatibility cases. |

Earlier attempts remain evidence; final counts use each final required case once.
No timeout was raised. Each completed suite stayed below the declared 120-second ceiling.
Refactor decision: isolate design input checking, rechecking and prompt composition in
the existing authoring helper; reuse record_schema, with no new service or dependency.
No unrelated structural rewrite was needed. Final regressions ran after the changes.

Skill Creator quick_validate exited 0. Local checks resolved 41 Markdown links,
parsed 8 Python files and 20 JSON files, and confirmed the package manifest against bytes.
These are structural/custody observations only. See [static checks](static-checks.json).
Unchanged validator intake bound a valid packet and rejected stale design bytes in
test_capture_and_unchanged_validator_packet; this is bounded interface evidence only.

## Requirement coverage and remaining owner

| Requirements | Delivered behavior / evidence |
| --- | --- |
| SBP-001, 014 | Authoring-only scope retained; narrow source changes, old schemas and adaptive regression preserved. |
| SBP-002–008 | Observable workflow, resource, helper, delivery, recovery and adverse-condition instructions in workflow-design.md; cold behavior NOT_RUN. |
| SBP-009–011 | Design shape/path/ref checks, single normal input snapshot, bounded capture and publication custody; positive/negative maintenance cases executed. |
| SBP-012 | Unchanged packet schema/intake; original source/design references and independent-oracle obligations in manual prompt. |
| SBP-013 | Created/edited/unchanged reporting and qualification separation; real unchanged edit exercised. |
| SBP-015–016 | Retained TDD/QA evidence, byte manifests and manual independent handoff; separate behavioral evaluation remains required. |

No unresolved implementation decision was found. **SBPV-01–18 are not claimed passed**
by this maintenance run. Independent cold builder trials, two actual generated-skill
workflows, their own Python evaluation bundle, other required platforms and broader
coverage belong to the separately invoked validator. Numeric helper results cannot
substitute for these obligations.

Operational .agents/skills/skill-builder, development skill-validator and docs/specs
were rehashed against the pre-maintenance capture and are unchanged. Prior evidence
was read or copied; new attempts stayed in this fresh directory. No installation,
hooks, CI, existing generated skill or Rust implementation was changed.

Next owner: skill-validator. Use the [manual handoff](validator-handoff.md) to bind the
delivered package and independently assess it under a later user-selected task.
