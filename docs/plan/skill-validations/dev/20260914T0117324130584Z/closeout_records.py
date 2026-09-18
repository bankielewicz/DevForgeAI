"""Assemble final records from completed observations; never assigns native outcomes."""
import collections
import hashlib
import json
from pathlib import Path
import shutil
import sys

RUN = Path(__file__).resolve().parent


def load(path):
    return json.loads(path.read_bytes())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def ref(path):
    return {'path': path.relative_to(RUN).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


def reduce(rows):
    selected = [r for r in rows if r['required'] and r['applicability'] != 'not_applicable']
    return {'outcome': 'FAIL' if any(r['result'] == 'FAIL' for r in selected) else 'INCOMPLETE' if any(r['result'] in ('NOT_RUN', 'ERROR') for r in selected) else 'PASS',
            'required_total': len(selected), 'required_evaluated': sum(r['result'] in ('PASS', 'FAIL') for r in selected),
            'incomplete_check_ids': [r['check_id'] for r in selected if r['result'] in ('NOT_RUN', 'ERROR')]}


def build():
    package = load(RUN / 'source-manifest.json')['package_digest']
    readback = load(RUN / 'commands/source-readback-final/stdout.txt')
    assert readback['status'] == 'MATCH' and readback['manifest']['package_digest'] == package
    save(RUN / 'source-after-manifest.json', readback['manifest'])
    original = RUN / 'origin-record.json'
    save(RUN / 'inputs/origin-record-before-readback.json', original.read_text(encoding='utf-8'))
    origin = load(original)
    origin['source_readback_state'] = 'UNCHANGED'
    original.write_text(json.dumps(origin, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for source, destination in [('case-observations-final.json', 'inputs/case-observations-final.json'), ('bundle/artifact-manifest.json', 'inputs/bundle-manifest-final.json')]:
        save(RUN / destination, (RUN / source).read_text(encoding='utf-8'))
    semantic = load(RUN / 'semantic-review-initial.json')
    for row in semantic['observations']:
        if row['rule_id'] == 'AV-E01':
            row.update(result='ERROR', reason='Current source/intake and bundle are digest-bound, and executed observations are retained. The unchanged schema1 full-run records checker returned MISMATCH because it interprets the separate bundle-relative reference family and raw snapshot envelope as schema1 run-relative references. Supported-family checks complement this result; the required full-run integrity command remains unresolved, not a dev instruction defect.',
                       evidence=[ref(RUN / 'commands/records-mixed-initial/stdout.txt'), ref(RUN / 'commands/source-readback-final/stdout.txt'), ref(RUN / 'inputs/bundle-manifest-final.json')])
    save(RUN / 'semantic-review-final.json', semantic)
    by_id = {row['rule_id']: row for row in semantic['observations']}
    cases = load(RUN / 'case-observations-final.json')['cases']
    by_id.update({row['case_id']: row for row in cases})
    rows = []
    for rule in load(RUN / 'rule-set.json')['rules']:
        ident = rule['rule_id']
        observation = by_id[ident]
        is_case = ident.startswith(('DV-', 'RV-'))
        dimension = 'behavior' if is_case else 'instructions' if ident.startswith(('AV-I', 'AV-C')) else 'workflow' if ident.startswith(('DEV-', 'REV-', 'AV-W')) else 'standards'
        evidence = [ref(RUN / 'inputs/case-observations-final.json')] if is_case else observation['evidence']
        rows.append({'schema_version': '1', 'run_id': RUN.name, 'check_id': 'CHECK-' + ident, 'rule_id': ident,
                     'subject_path': observation.get('subject_path', 'SKILL.md'), 'method': observation['method'],
                     'required': rule['required'], 'applicability': 'not_applicable' if observation['result'] == 'NOT_APPLICABLE' else 'applicable',
                     'result': observation['result'], 'reason': observation['reason'], 'evidence': evidence, 'dimension': dimension})
    assert len(rows) == 82
    save(RUN / 'checks.jsonl', ''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))
    dimensions = {name: reduce([row for row in rows if row['dimension'] == name]) for name in ('standards', 'workflow', 'instructions', 'behavior')}
    outcome = 'FAIL' if any(d['outcome'] == 'FAIL' for d in dimensions.values()) else 'INCOMPLETE' if any(d['outcome'] == 'INCOMPLETE' for d in dimensions.values()) else 'PASS'
    save(RUN / 'assessment.json', {'schema_version': '1', 'run_id': RUN.name, 'target_name': 'dev', 'assessment_completed': True,
                                 'overall_assessment': outcome, 'dimensions': dimensions, 'required_coverage': reduce(rows),
                                 'case_counts': dict(collections.Counter(row['result'] for row in cases)), 'unique_case_denominator': 23,
                                 'framework_acceptance': 'NOT_EVALUATED'})


def schema1_collection():
    suffix = sys.argv[2] if len(sys.argv) > 2 else ''
    destination = RUN.with_name(RUN.name + '-schema1-records' + suffix)
    destination.mkdir(exist_ok=False)
    names = ['source-manifest.json', 'source-after-manifest.json', 'origin-record.json', 'sources.json', 'rule-set.json',
             'workflow-map.json', 'checks.jsonl', 'findings.json', 'handoff.json', 'assessment.json']
    copied = set()
    def copy(name):
        if name in copied:
            return
        path = RUN / name
        assert path.is_file() and path.resolve().is_relative_to(RUN.resolve())
        output = destination / name
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, output)
        assert path.read_bytes() == output.read_bytes()
        copied.add(name)
        if name.startswith(('inputs/', 'source/', 'trials/')) or path.suffix not in ('.json', '.jsonl'):
            return
        documents = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()] if path.suffix == '.jsonl' else [load(path)]
        def walk(value):
            if isinstance(value, dict):
                if 'path' in value and 'sha256' in value and not (name.endswith('manifest.json') and 'bytes' in value):
                    copy(value['path'])
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        for document in documents:
            walk(document)
    for name in names:
        copy(name)
    if suffix:
        for row in load(RUN / 'source-manifest.json')['files']:
            copy('source/' + row['path'])
    save(RUN / ('inputs/schema1-collection-custody' + suffix + '.json'), {'scope': 'Exact-byte schema1 mandatory records, complete declared source snapshot and their direct/transitive supported references. This separate check does not replace the full mixed-family failure. The original collection omitted source files lacking individual check refs; its failure is preserved separately.',
                                                       'original_root': str(RUN), 'collection_root': str(destination),
                                                       'copied': [ref(RUN / name) for name in sorted(copied)]})


if __name__ == '__main__':
    {'build': build, 'schema1': schema1_collection}[sys.argv[1]]()
