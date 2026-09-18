"""Capture selected immutable inputs and freeze the assessment catalog."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent
PROJECT = RUN.parents[4]
VALIDATOR = PROJECT / '.agents/skills/skill-validator'
sys.path.insert(0, str(VALIDATOR / 'scripts'))
import observe

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False, allow_nan=False)
        stream.write('\n')

def ref(path):
    return {'path': path.relative_to(RUN).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def capture(original, relative):
    data = observe.read_stable(observe.safe_path(original))
    destination = RUN / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as stream:
        stream.write(data)
    assert destination.read_bytes() == data
    return dict(original_path=str(original), **ref(destination))

def main():
    packet = PROJECT / 'docs/plan/skill-authorings/story-create/20260917T182711Z-02/validation-request.json'
    request = json.loads(packet.read_bytes())
    author = Path(request['authoring_record']['path'])
    record = json.loads(author.read_bytes())
    paths = [packet, author, Path(request['target_manifest']['path']), Path(record['contract']['path'])]
    paths += [Path(v['path']) for v in request['specification_refs']]
    paths += [author.parent / n for n in ['authoring-baseline.json','import-report.md','author-review.md']]
    paths += [author.parent.parent / '20260917T182711Z-intake/authoring-design.json']
    paths = list(dict.fromkeys(paths))
    assert len(paths) <= 2000 and sum(p.stat().st_size for p in paths) <= 32*1024*1024
    index = []
    for path in paths:
        index.append(capture(path, 'inputs/repository/' + path.relative_to(PROJECT).as_posix()))
    write(RUN/'inputs/index.json', index)
    for directory in ['scripts', 'references', 'schemas', 'assets']:
        root = VALIDATOR / directory
        files, excluded = observe.inventory(root)
        for relative, original, info in files:
            capture(original, 'evaluator/' + directory + '/' + relative)
    capture(VALIDATOR/'SKILL.md', 'evaluator/SKILL.md')
    creator = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    if creator.exists():
        capture(creator, 'evaluator/installed-creator-quick_validate.py')
    rules_text = (RUN/'evaluator/references/adaptive-validation.md').read_text(encoding='utf-8')
    sources = []
    def source(source_id, path, locator, url=None, original=None, freshness='snapshot_only'):
        source_ref = dict(ref(path), source_id=source_id, locator=locator)
        sources.append(dict(source_id=source_id, url=url, original_path=original,
                            retrieved_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            sha256=source_ref['sha256'], snapshot_path=source_ref['path'],
                            sections=[locator], freshness=freshness))
        return source_ref
    av = source('adaptive-project-policy', RUN/'evaluator/references/adaptive-validation.md', '3.1 Core rule catalog; 4.1 Adaptive rules', original=str(VALIDATOR/'references/adaptive-validation.md'))
    official = source('openai-skills', RUN/'guidance/openai-build-skills.md', 'How ChatGPT and Codex use skills; Best practices', url='https://learn.chatgpt.com/docs/build-skills', freshness='live_verified')
    req_path = RUN/'inputs/repository/docs/plan/skill-authorings/story-create/20260917T182711Z-intake/requirements.json'
    contract = source('authoring-requirements', req_path, 'SC-001 through SC-016', original=str(PROJECT/req_path.relative_to(RUN/'inputs/repository')))
    nonapp = {'AV-F04': 'Optional agents/openai.yaml is absent.', 'AV-A03':'Core, not a project variant.', 'AV-A06':'No update-review workflow in selected authoring skill.', 'AV-A08':'No set authoring output selected.', 'AV-A09':'Single member assessment; consumer handoffs separately tested.', 'AV-A10':'No selected multi-skill set; required dependency failures covered by SC-007.'}
    rules = []
    for line in rules_text.splitlines():
        if not line.startswith('| AV-'):
            continue
        fields = [s.strip() for s in line.strip('|').split('|')]
        ident = fields[0]
        method = 'deterministic' if ident.startswith(('AV-F01','AV-F04','AV-U','AV-C','AV-E')) else 'behavioral' if ident in ('AV-W02','AV-A05','AV-A10') else 'semantic'
        rules.append(dict(rule_id=ident, revision='2026-09-12', title=fields[1], source_refs=[av], authority_class='project_policy', applicability='not_applicable' if ident in nonapp else 'applicable', method=method, expected_observation=fields[2], required=True, limitation=nonapp.get(ident,'Helper output alone does not prove semantic or native behavior.')))
    for req in json.loads(req_path.read_bytes()):
        rules.append(dict(rule_id=req['id'], revision='0.1.0', title=req['outcome'], source_refs=[contract], authority_class='project_policy', applicability='applicable', method='semantic' if req['id'] in ('SC-001','SC-002') else 'behavioral', expected_observation=req['outcome'], required=True, limitation='Windows native assessment; other platforms reported separately.'))
    rules.append(dict(rule_id='OAI-001', revision='live-20260917', title='Required skill metadata', source_refs=[official], authority_class='format_requirement', applicability='applicable', method='deterministic', expected_observation='SKILL.md contains name and description.', required=True, limitation='Does not establish activation or behavior.'))
    write(RUN/'sources.json', dict(schema_version='1', run_id=RUN.name, target_name='story-create', sources=sources))
    write(RUN/'rule-set.json', dict(schema_version='1', run_id=RUN.name, target_name='story-create', rules=rules))
    write(RUN/'preflight.json', dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), cwd=str(PROJECT), platform=platform.platform(), python=sys.version, python_executable=sys.executable, shell='PowerShell 7 native Windows', git_metadata=(PROJECT/'.git').exists(), selected_target=str(PROJECT/'src/agents/skills/story-create'), input_count=len(paths), input_bytes=sum(p.stat().st_size for p in paths), authorization='Validation and disposable synthetic execution only; source and operational copies read-only.', timeouts={'utility_seconds':120,'native_seconds':600}, coverage_denominator='All executable lines in captured scripts/check_project_binding.py; no first-party exclusions. External evaluator code reported separately.', rule_set=ref(RUN/'rule-set.json')))
    for name, argv in [('codex-version',['codex','--version']),('codex-help',['codex','exec','--help']),('python-dependencies',[sys.executable,'-B','-X','utf8','-c',"import importlib.metadata as m; print({p:m.version(p) for p in ['PyYAML','coverage']})"])]:
        result = subprocess.run(argv, cwd=PROJECT, capture_output=True, timeout=120)
        (RUN/(name+'.stdout.txt')).write_bytes(result.stdout)
        (RUN/(name+'.stderr.txt')).write_bytes(result.stderr)
        write(RUN/(name+'.execution.json'),dict(argv=argv,cwd=str(PROJECT),exit_code=result.returncode))
    print(json.dumps({'run':str(RUN),'inputs':len(index),'rules':len(rules),'package':json.loads((RUN/'source-manifest.json').read_bytes())['package_digest']}))

if __name__ == '__main__':
    main()
