"""Seal final maintenance evidence and write the separate evaluation handoff."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'
sys.path.insert(0, str(PACKAGE / 'scripts'))
import authoring as a

def write(name, value):
    path = RUN / name
    data = (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    with path.open('xb') as stream:
        stream.write(data)
    assert path.read_bytes() == data

grade = json.loads((RUN / 'qa-03/grade.json').read_bytes())
assert grade['passing'] == grade['required'] and not grade['nonpasses']
coverage = json.loads((RUN / 'qa-03-coverage.json').read_bytes())
totals = coverage['totals']
line_percent = 100 * totals['covered_lines'] / totals['num_statements']
branch_percent = 100 * totals['covered_branches'] / totals['num_branches']
assert line_percent >= 95
runtime = json.loads((RUN / 'qa-03/runtime.json').read_bytes())
for rel, expected in runtime['source'].items():
    assert a.digest((ROOT / rel).read_bytes()) == expected, rel
protected = json.loads((RUN / 'preservation-before.json').read_bytes())
for path, expected in protected.items():
    root = Path(path)
    observed = {p.relative_to(root).as_posix(): a.digest(p.read_bytes()) for p in root.rglob('*') if p.is_file()}
    assert expected == observed, path
shutil.copytree(PACKAGE, RUN / 'delivered/skill-builder')
assert a.files(PACKAGE) == a.files(RUN / 'delivered/skill-builder')
snapshot = a.manifest(a.files(PACKAGE))
assert snapshot == json.loads((RUN / 'delivered-manifest.json').read_bytes())
requirements = [ROOT / 'docs/specs/skill-builder-postmvp-spec.md',
    ROOT / 'docs/plan/skill-builder-authoring-enhancement-spec.md',
    ROOT / 'docs/plan/skill-builder-adaptive-enhancement-spec.md', ROOT / 'AGENTS.md',
    ROOT / 'docs/plan/devforgeai-codex-rust-enforcement-design.md']
refs = [a.reference(path) for path in requirements]
dependencies = {name: importlib.metadata.version(name) for name in ('coverage', 'PyYAML', 'jsonschema')}
write('runtime-dependencies.json', {'python': sys.version, 'executable': sys.executable,
    'maintenance_dependencies': dependencies, 'builder_design_dependencies': 'Python standard library and existing local record_schema only; no added dependency'})
write('result.schema.json', {'type': 'object', 'required': ['case', 'status', 'seconds', 'detail'],
    'additionalProperties': False, 'properties': {'case': {'type': 'string'},
        'status': {'enum': ['PASS', 'FAIL', 'ERROR', 'SKIP']}, 'seconds': {'type': 'number', 'minimum': 0}, 'detail': {'type': 'string'}}})
write('requirement-refs.json', refs)
readback = {'source_action': 'edited', 'maintenance_status': 'COMPLETE',
    'required_cases': grade['required'], 'passing_cases': grade['passing'],
    'line_coverage': {'covered': totals['covered_lines'], 'statements': totals['num_statements'], 'percent': line_percent, 'excluded_lines': totals['excluded_lines']},
    'branch_coverage': {'covered': totals['covered_branches'], 'branches': totals['num_branches'], 'percent': branch_percent},
    'package_digest': snapshot['package_digest'], 'target': str(PACKAGE),
    'validation': 'NOT_PERFORMED', 'generated_skill_testing': 'NOT_PERFORMED',
    'linux_maintenance': 'NOT_RUN', 'framework_acceptance': 'NOT_PERFORMED'}
write('final-result.json', readback)
handoff = f'''# Independent validator handoff

Use $skill-validator to independently validate the development skill-builder at
`{PACKAGE}` against the original selected specifications in
`{RUN / 'requirement-refs.json'}` (SHA-256 `{a.reference(RUN / 'requirement-refs.json')['sha256']}`).

Expected current package digest: `{snapshot['package_digest']}`.
Bind and reread `{RUN / 'delivered-manifest.json'}`
(SHA-256 `{a.reference(RUN / 'delivered-manifest.json')['sha256']}`) and reject stale source.
The digest includes package-manifest.json; that file's artifacts map excludes itself.

This standalone maintenance handoff does not fabricate a builder authoring-record
or change validation-request-v1. The enhanced builder's actual packet was exercised
through unchanged validator intake in maintenance fixtures.

Independently derive fixtures and oracles from original requirements. Builder design
artifacts and adverse-condition descriptions are authored expectations, not executed
results or waivers. Maintenance helper results do not qualify a cold workflow.

Assess all SBPV-01 through SBPV-18 from the post-MVP specification, retaining applicable
legacy/adaptive regressions. For SBPV-18 cold-invoke the enhanced builder, then separately
exercise two actual generated skills: a simple transformation and a branching workflow
with file delivery and a relevant failure path. Use different layouts and literal paths
with spaces/Unicode. Verify outputs, failed delivery, interruption/recovery, unchanged
source reporting, native obligations and independent oracle construction.

Prepare the mandatory external Python JSONL runner, deterministic graders, fixtures,
expected results, schema, runtime/dependencies and artifact byte bindings. The present
maintenance bundle is supporting evidence, not a replacement for your independent bundle.
Predeclare commands, permitted effects, output paths, case budgets and retry policy.
Preserve all attempts. No silent timeout increase or automatic repair cycle.

Unresolved implementation decisions: none identified. Unperformed qualification:
all cold builder/generator and generated-skill SBPV behavioral scenarios, Linux coverage,
full-package coverage outside the declared custody scope, and framework acceptance.
Maintenance: {grade['passing']}/{grade['required']} Windows cases pass;
line coverage {totals['covered_lines']}/{totals['num_statements']} = {line_percent:.6f}%
for authoring.py and record_schema.py only, no excluded lines. Branch coverage is separate.

Validation: NOT_PERFORMED. Generated-skill Testing: NOT_PERFORMED.
An unchanged or AUTHORED skill is not an evaluated build. Preserve operational copies,
validator source, original specs, existing generated skills and historical evidence.
This file grants no evaluation, installation, network, external-effect or repair permission;
the later user invocation determines assessment authorization. Next owner: skill-validator;
next action: bind current source and propose the independent assessment under that invocation.
'''
(RUN / 'validator-handoff.md').write_text(handoff, encoding='utf-8')
report = f'''# Skill-builder post-MVP maintenance

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
Package digest: `{snapshot['package_digest']}`.
Final source bytes exactly match the hashes captured before qa-03, including the manifest.

## Executed maintenance evidence

Native Windows, Python {sys.version.split()[0]}, coverage.py {dependencies['coverage']}.
Final QA: **{grade['passing']}/{grade['required']} required cases passed (100%)**, no skips/nonpasses.
Elapsed final suite: see qa-03.txt. Required inventory and outcomes are in
[expected cases](qa-03/expected.json), [JSONL observations](qa-03/results.jsonl),
[deterministic reduction](qa-03/grade.json) and [coverage](qa-03-coverage.json).

Executed-line denominator, declared before collection: all first-party statements in
scripts/authoring.py and scripts/record_schema.py, no excluded lines.
**{totals['covered_lines']}/{totals['num_statements']} = {line_percent:.6f}%** line coverage.
Branch coverage: **{totals['covered_branches']}/{totals['num_branches']} = {branch_percent:.6f}%**.
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
| qa-03 | {grade['passing']}/{grade['required']} after explicit internal mode fix and compatibility cases. |

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
'''
(RUN / 'maintenance-report.md').write_text(report, encoding='utf-8')
write('command-receipts.json', {
    'cwd': str(ROOT), 'platform': runtime['platform'],
    'commands': [
        {'command': f'python -B -X utf8 -m coverage run --branch --include=\"*/skill-builder/scripts/authoring.py,*/skill-builder/scripts/record_schema.py\" {RUN.relative_to(ROOT).as_posix()}/run_maintenance.py qa-03', 'environment': {'COVERAGE_FILE': str(RUN / 'coverage-qa-03')}, 'exit': int((RUN / 'qa-03-exit.txt').read_text(encoding='utf-8-sig').strip())},
        {'command': f'python -B -m coverage json -o {RUN.relative_to(ROOT).as_posix()}/qa-03-coverage.json', 'exit': 0},
        {'command': f'python -B {RUN.relative_to(ROOT).as_posix()}/grade_maintenance.py {RUN.relative_to(ROOT).as_posix()}/qa-03', 'exit': 0},
        {'command': f'python -B -X utf8 {RUN.relative_to(ROOT).as_posix()}/finalize_artifacts.py', 'exit': 0},
        {'command': 'python -B -X utf8 C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py src/agents/skills/skill-builder', 'exit': int((RUN / 'quick-validate-final-exit.txt').read_text(encoding='utf-8-sig').strip())} ]})
bundle = [RUN / name for name in ('test_design.py', 'test_builder_adaptive.py', 'run_maintenance.py', 'grade_maintenance.py',
    'result.schema.json', 'runtime-dependencies.json', 'builder-before.json', 'qa-03/expected.json', 'qa-03/results.jsonl',
    'qa-03/grade.json', 'qa-03/runtime.json', 'qa-03-coverage.json', 'plan.md', 'regression-adaptation.md',
    'command-receipts.json', 'maintenance-report.md', 'validator-handoff.md', 'delivered-manifest.json')]
bundle.extend(ROOT / 'src/agents/skills/skill-validator/tests' / name for name in ('test_authoring.py', 'test_authoring_safeguards.py'))
write('maintenance-bundle-manifest.json', {'kind': 'external-maintenance-evidence', 'files': [a.reference(path) for path in bundle]})
for path in (RUN / 'maintenance-report.md', RUN / 'validator-handoff.md'):
    assert path.read_text(encoding='utf-8')
print(json.dumps(readback, indent=2))
