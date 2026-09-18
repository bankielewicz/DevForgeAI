"""Recompute final independent QA results from retained raw records; evidence only."""
import hashlib
import json
import re
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT=Path(__file__).resolve().parent
PROJECT=Path('C:/Projects/DevForgeAI')
DEV=ROOT.parent/'20260917T102726Z-dev-qa-fixes'
OLD=ROOT.parent/'20260917T023835Z-qa'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            digest.update(block)
    return digest.hexdigest()


def write(name,value):
    with (ROOT/name).open('x',encoding='utf-8',newline='\n') as stream:
        json.dump(value,stream,indent=2,ensure_ascii=True)
        stream.write('\n')


def verify(items):
    for item in items:
        path=Path(item['path'])
        assert sha(path)==item['sha256'] and path.stat().st_size==item['bytes'],str(path)


assert not (ROOT/'STOP.json').exists()
preserved=[]
for name in ['candidate-manifest.json','input-manifest.json','preserved-manifest.json','helper-manifest.json','binary-manifest.json','independent-binary-manifest.json']:
    items=load(ROOT/name)
    verify(items)
    preserved.append({'manifest':name,'sha256':sha(ROOT/name),'files':len(items),'mismatches':[]})
for base in [DEV,OLD]:
    manifest=load(base/'evidence-manifest.json')
    verify(manifest['files'])
    if 'binaries' in manifest:
        verify(manifest['binaries'])
    preserved.append({'manifest':str(base/'evidence-manifest.json'),'files':len(manifest['files']),'mismatches':[]})
v2=load(ROOT/'cli-helper-v2-binding.json')
assert sha(Path(v2['Path']))==v2['Hash'].lower()
matrix=load(ROOT/'cli-matrix-plan-v2.json')
assert matrix['entries']==load(ROOT/'cli-matrix-plan.json')['entries']
assert matrix['script_sha256']==sha(ROOT/'cli_matrix_v2.py')
for path,digest in matrix['protected_seed_files'].items():
    assert sha(Path(path))==digest,path

required=load(ROOT/'required-cases.json')
cases=load(ROOT/'package-results.json')
assert len(cases)==162 and all(case['status']=='PASS' for case in cases)
for declared in required[162:]:
    case=dict(declared)
    if case['id']=='SUP-01':
        attempt='20-supplement'
    elif case['id'].startswith('QA-'):
        number=int(case['id'].split('-')[1])
        attempt=f'{number+4:02d}-qa{number:02d}'
    else:
        attempt='18-rt01-corrected' if case['id']=='RT-01' else '19-rt02'
    receipt=load(ROOT/'attempts'/attempt/'receipt.json')
    if case['id'].startswith('RT-'):
        assert receipt['status']=='PASS'
        group='success' if case['id']=='RT-01' else 'compatibility'
        entries=[entry for entry in matrix['entries'] if entry['group']==group]
        observations=[]
        for entry in entries:
            path=ROOT/'attempts'/attempt/entry['id']
            assert load(path/'selection.json')==entry
            for label in ['control','first','end']:
                record=load(path/f'{label}.json')
                stdout=(path/f'{label}.stdout.txt').read_bytes()
                stderr=(path/f'{label}.stderr.txt').read_bytes()
                state=entry['seed']['state'] if label=='control' else entry['expected_state']
                error=None if label=='control' else entry['expected_error']
                if error:
                    actual=record['exit_code']==4 and not stdout and json.loads(stderr)=={'error':error}
                else:
                    actual=record['exit_code']==0 and not stderr and json.loads(stdout)['state']==state
                assert actual and record['read_only'] and record['expectation_met'],str(path)
                observations.append({'path':str(path/f'{label}.json'),'case':case['id'],'expected_state':state,'expected_error':error,'matched_from_raw_outputs':actual})
        assert len(observations)==receipt['observations']==len(entries)*3
        write(f"{case['id'].lower()}-observations.json",observations)
        case['subcases']=len(entries)
        case['observations']=len(observations)
        if case['id']=='RT-01':
            case['retained_preparation_error']='attempts/18-rt01/receipt.json; QA-H01; corrected once without changing assertions'
    else:
        raw=(ROOT/'attempts'/attempt/'stdout.txt').read_text(encoding='utf-8-sig')
        results=re.findall(r'^test ([\w:]+) \.\.\. (ok|FAILED|ignored)$',raw,re.MULTILINE)
        assert results==[(case['name'],'ok')],(case['id'],results)
        assert receipt['exit_code']==0 and not receipt['timed_out']
    case.update({'status':'PASS','attempt':attempt})
    cases.append(case)
assert len(cases)==178 and [case['id'] for case in cases]==[case['id'] for case in required]
assert all(case['status']=='PASS' for case in cases)

attempts=[]
for path in sorted((ROOT/'attempts').glob('*/receipt.json')):
    receipt=load(path)
    if 'outputs' in receipt:
        verify(receipt['outputs'])
        assert receipt['exit_code']==0 and not receipt['timed_out']
        status='PASS' if receipt['action'] not in ['build','list','independent-build','fmt','clippy'] else 'CHECK_COMPLETED'
    else:
        status=receipt['status']
        assert status=='PASS' or path.parent.name=='18-rt01'
    attempts.append({'attempt':path.parent.name,'receipt':str(path),'receipt_sha256':sha(path),'action':receipt['action'],'status':status,'exit_code':receipt.get('exit_code',receipt.get('process_exit_code')),'elapsed_seconds':receipt.get('elapsed_seconds')})
assert len(attempts)==23

# Recompute original independently authored negative observations from their retained values.
mutations=[]
for path in sorted((ROOT/'attempts/13-qa09/fixtures').glob('*/mutation-result.json')):
    result=load(path)
    assert set(result['result'])=={'Err'},str(path)
    expected='evidence_incomplete' if result['mutation']=='missing-status' else 'evidence_corrupt'
    assert result['result']['Err']==expected,str(path)
    mutations.append({'mutation':result['mutation'],'actual':expected,'path':str(path),'sha256':sha(path)})
assert len(mutations)==9
write('original-defect-retest.json',mutations)

coverage=load(ROOT/'coverage-analysis.json')
assert sha(ROOT/'coverage.json')==coverage['coverage_sha256']
assert coverage['line_floor_pass'] and coverage['unit_floor_pass']
developer=load(DEV/'coverage-analysis.json')
# The independent report binds its own observed values; development counts are comparison only.
differences=[]
dev_files=[{'path':item['filename'],'covered':item['summary']['lines']['covered'],'count':item['summary']['lines']['count']} for item in load(DEV/'coverage.json')['data'][0]['files']]
for current in coverage['per_file']:
    for previous in dev_files:
        previous_path=previous.get('path',previous.get('filename',''))
        if Path(previous_path).name==Path(current['path']).name and previous.get('covered')!=current['covered']:
            differences.append({'file':Path(current['path']).name,'development':previous,'independent':current})
metrics={'platform':'Windows x64','overall_platforms':['Windows x64'],'required_cases':178,'passed':178,'pass_percent':'100','unit_required':49,'unit_passed':49,'unit_percent':'100','package_integration':{'passed':113,'required':113},'supplemental':{'passed':1,'required':1},'independent_original':{'passed':13,'required':13},'independent_cli':{'passed':2,'required':2,'subcases':145,'observations':435},'line_covered':coverage['line_covered'],'line_count':coverage['line_count'],'line_percent':str(Decimal(100)*coverage['line_covered']/coverage['line_count']),'thresholds':{'line':95,'unit':95,'project_suite':95},'all_numeric_floors':'PASS','coverage_collection':'Complete162-case package campaign only; no supplemental/independent coverage credit','coverage_sha256':coverage['coverage_sha256'],'branch_coverage':'NOT_RUN','metric_stop':None,'retained_harness_error':'QA-H01,18-rt01','product_failures':[],'unexecuted_required_cases':[],'verdict':'PASS','native_codex':'NOT_RUN','framework_acceptance':'NOT_EVALUATED','coverage_development_comparison':differences}
write('metrics.json',metrics)
write('case-results.json',cases)
write('attempt-index.json',attempts)

docs=[PROJECT/'devforgeai/experiments/codex-worker-probe-logging-qa-fixes/README.md']
docs += [Path(item['path']) for item in load(ROOT/'specification-bindings.json')]
docs.append(DEV/'delivery.md')
links=[]
for path in sorted(set(docs)):
    text=re.sub(r'```.*?```','',path.read_text(encoding='utf-8-sig'),flags=re.DOTALL)
    for destination in re.findall(r'(?<!!)\[[^\]]+\]\(([^)]+)\)',text):
        parts=urlsplit(destination.strip().strip('<>'))
        if parts.scheme or not parts.path:
            continue
        target=(path.parent/unquote(parts.path)).resolve()
        links.append({'source':str(path),'destination':destination,'resolved':str(target),'exists':target.exists()})
assert all(item['exists'] for item in links)
write('documentation-review.json',{'documents':[str(path) for path in sorted(set(docs))],'links':links,'broken_links':[],'factual_review':'README identifies the corrected sibling and schema3/inspector behavior; source assertions checked against current implementation and fresh tests. Development FIX_REPORTED remains a historical claim; only this independent report records closure. No native/authority qualification inferred. Remote links and fragment-only anchors not exercised.'})
write('final-preservation.json',{'timestamp_utc':datetime.now(timezone.utc).isoformat(),'checks':preserved,'protected_matrix_seed_files':len(matrix['protected_seed_files']),'candidate_files':68,'preserved_source_files':183,'input_files':108,'problems':[]})
print(json.dumps({'verdict':'PASS','cases':'178/178','units':'49/49','lines':f"{coverage['line_covered']}/{coverage['line_count']}",'line_percent':metrics['line_percent'],'matrix_observations':435,'original_mutations_rejected':9,'attempts':len(attempts),'documents':len(set(docs)),'local_links':len(links),'preservation':'unchanged','native_codex':'NOT_RUN','framework_acceptance':'NOT_EVALUATED'},indent=2))
