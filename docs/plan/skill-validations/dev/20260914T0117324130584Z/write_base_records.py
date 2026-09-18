"""Persist source provenance, workflow map and supplemental manual dispositions."""
import json
from pathlib import Path
import hashlib

RUN = Path(__file__).resolve().parent


def ref(path, absolute=False):
    return {'path': str(path) if absolute else path.relative_to(RUN).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def main():
    manifest = json.loads((RUN / 'source-manifest.json').read_bytes())
    index = json.loads((RUN / 'inputs/input-index.json').read_bytes())
    revision = next(row for row in index if row['original_path'].endswith('revision-spec.md'))
    authoring = next(row for row in index if row['original_path'].endswith('authoring-record.json'))
    save(RUN / 'origin-record.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev',
                                    'original_source_root': manifest['root'], 'manifest': ref(RUN / 'source-manifest.json'),
                                    'specification': revision['snapshot'], 'origin_kind': 'existing_spec', 'history_kind': 'observed',
                                    'prior_evidence': authoring['snapshot'], 'completeness': 'complete',
                                    'uncertainties': ['Schema1 observed field does not encode authoring-v1 lineage; separately captured current authored custody is verified by BOUND intake.'],
                                    'source_readback_state': 'NOT_RUN', 'historical_origin': 'authored lineage retained in separate authoring-family supplement; not fabricated legacy generated/adopted history'})
    rows = [
        ('context', 'SKILL.md:Workflow1 / references/context.md', ['selected project/specs/scope/instructions'], 'Resolve identity, read complete inputs, inspect current tools/source, bind literal original destination and output paths before writes.', ['context and exact input/output map'], 'Observed context and original-source path comparison precede production changes.', ['requirements'], 'Missing/ambiguous/unavailable inputs stop dependent writes; independent work continues.'),
        ('requirements', 'SKILL.md:Workflow2 / references/context.md', ['context', 'selected specifications'], 'Inventory source-qualified requirements, contracts, dependency owners, constitutional decisions and gaps.', ['traceability', 'resolved dependency order or precise gaps'], 'Every selected normative requirement has source, owner and verification/gap.', ['slices'], 'Conflicts/cycles/missing unselected prerequisites require a precise decision.'),
        ('slices', 'SKILL.md:Workflow3 / references/implementation.md', ['requirements', 'existing source/tests'], 'Inspect reuse candidates by responsibility, retain decision, plan observable dependency slices and real commands.', ['reuse assessment', 'slice plan', 'declared checks'], 'Each slice binds input/output contracts, ownership and concrete expected behavior.', ['tdd-qa'], 'Missing tools or material architecture decisions block only dependent slices.'),
        ('tdd-qa', 'SKILL.md:Workflow4 / references/implementation.md', ['slice plan', 'tool availability', 'authorized source/test roots'], 'Execute focused valid red, minimum green, justified refactor, integration and project-derived QA/native checks.', ['product source/tests', 'actual receipts and metrics'], 'Real candidate-bound passing checks; no stubbed integration, weakened assertions or denominator manipulation.', ['checkpoint', 'delivery'], 'Setup errors are not red; unavailable required native checks remain NOT_RUN; preserve failures.'),
        ('checkpoint', 'SKILL.md:Workflow5 / references/evidence-resume.md', ['current inputs/candidate', 'job outcomes', 'execution evidence'], 'Retain checkpoint and recheck hashes, destination identity, job state and ownership before resumption.', ['fresh checkpoint', 'drift/gap record', 'new attempt evidence'], 'Changed prerequisites invalidate dependent prior claims; old work stays retained.', ['context', 'tdd-qa', 'delivery'], 'Unknown jobs inspected before retry; changed destination rebinds permitted future records without overwriting old output.'),
        ('delivery', 'SKILL.md:Workflow6 / references/failure-delivery.md', ['traceability', 'actual checks', 'original destination selection'], 'Read back all promised files at exact selected paths, reduce every selected requirement, report COMPLETE/PARTIAL/BLOCKED and separate acceptance.', ['delivery report', 'usable outputs or precise next gap'], 'Actual-versus-required path and current candidate evidence; passing tests alone cannot verify wrong locations.', [], 'Wrong/missing outputs prevent VERIFIED/COMPLETE; external authority unavailable remains NOT_EVALUATED.'),
    ]
    steps = []
    for ident, entry, inputs, action, outputs, completion, next_steps, failure in rows:
        steps.append({'step_id': ident, 'entrypoint': entry, 'entry_conditions': inputs, 'inputs': inputs,
                      'executor': 'Codex CLI skill-following session using terminal/file operations', 'action': action,
                      'outputs': outputs, 'completion_evidence': completion, 'next_branches': next_steps, 'failure_route': failure,
                      'terminal_user_outcome': 'Selected usable product/evidence or precise material gap; implementation/QA/native/acceptance distinctly reported.'})
    save(RUN / 'workflow-map.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev', 'steps': steps})
    supplementary = RUN.with_name(RUN.name + '-supplemental')
    supplementary.mkdir(exist_ok=False)
    raw = json.loads((RUN / 'commands/adaptive-token-count/stdout.txt').read_bytes())['observations']
    for node in raw['resources']:
        node['role'] = 'runtime' if node['path'] == 'SKILL.md' else 'reference' if node['path'].startswith('references/') else 'template'
        node['usage'] = 'used'
        node['reason'] = 'Manually read actual entrypoint/reference consumer and template role; resource is reachable through local instructions.'
        node['evidence'] = [ref(RUN / 'source' / node['path'], True), ref(RUN / 'source/references/evidence-resume.md', True)]
    save(supplementary / 'adaptive-observations.json', {'schema_version': 'adaptive-observations-v1', 'run_id': RUN.name,
                                                      'target_digest': manifest['package_digest'], **raw, 'bindings': [],
                                                      'limitations': ['Explicit native invocation is not implicit discovery.', 'Ordinary skill; adaptive bindings and set contracts not applicable.', 'Actual token consumption/load count is unmeasured; named local tokenizer availability is reported in raw helper observation.']})
    save(RUN / 'inputs/authoring-family-supplement.json', {'schema_version': 'authoring-family-assessment-v1',
                                                       'basis': 'Independently BOUND current authoring-v1 request and exact target readback; prior authored baseline retained.',
                                                       'authoring_record': authoring['snapshot'], 'intake': ref(RUN / 'commands/intake/stdout.txt'),
                                                       'package_digest': manifest['package_digest'], 'adoption_required': False,
                                                       'authority': 'Custody evidence only, not prior evaluated build or framework acceptance.'})
    save(RUN / 'enforcement-recommendations.md', '# Enforcement recommendations\n\nNo new implementation is authorized by this assessment. Destination identity/readback remains skill guidance plus editable execution evidence. A future separately selected protected acceptance service could validate original selection, allowed roots, delivered-file digests and completeness before accepting a project result. Such authority would belong to compiled Rust under DevForgeAI policy; no hook, service, plugin, or gate is claimed implemented here. Bypass/coverage limitation: model-written records and Python observers alone cannot enforce custody against hostile or concurrent mutation. Verification would require denied mismatched paths, stale/missing outputs and provenance tests against an actual implemented authority.\n')


if __name__ == '__main__':
    main()
