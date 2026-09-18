"""Independent, read-only CLI interpretation checks over fresh copied QA evidence."""
import argparse
import copy
import hashlib
import json
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path('C:/Projects/DevForgeAI')
EXE = ROOT / 'build-target/debug/devforgeai-codex-worker-probe.exe'
FIXTURES = ROOT / 'attempts/03-coverage/fixtures'


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')


def bindings(root):
    return {str(path): sha(path) for path in sorted(root.rglob('*')) if path.is_file()}


def identities():
    assert not (ROOT / 'STOP.json').exists(), 'Whole-run stop already recorded'
    for name in ['candidate-manifest.json','input-manifest.json','preserved-manifest.json','binary-manifest.json']:
        for item in load(ROOT / name):
            assert sha(Path(item['path'])) == item['sha256'], item['path']


def events_write(run, events):
    (run / 'journal.jsonl').write_bytes(b''.join(json.dumps(event, separators=(',',':')).encode() + b'\n' for event in events))


def seed_catalog():
    candidates = []
    for path in sorted(FIXTURES.glob('*/control-observation.json')):
        observed = load(path)
        if set(['expected','library','cli_exit_code','read_only','expectation_met']) - observed.keys():
            continue
        state = observed['expected']
        if state not in ['completed','preflight_checked','failed','blocked','cancelled','timed_out','cleanup_uncertain']:
            continue
        root = path.parent
        run = root / 'run'
        request = load(run / 'request.json')
        inputs = load(run / 'inputs.json')
        if inputs.get('capture_schema') != 1:
            continue
        raw = load(root / 'control-stdout.txt')
        assert raw['state'] == state and raw['next_after'] == len(raw['events'])
        assert raw['events'][-1]['kind'] == 'terminal'
        assert observed['expectation_met'] and observed['cli_exit_code'] == 0
        level = (inputs.get('diagnostics') or {}).get('level','off')
        candidates.append({'root':str(root),'run':str(run),'state':state,'schema':request['schema_version'],'level':level,'control':str(root/'control-stdout.txt'),'control_sha256':sha(root/'control-stdout.txt')})
    return candidates


def selected(catalog, state, schema, level=None):
    matches = [seed for seed in catalog if seed['state']==state and seed['schema']==schema and (level is None or seed['level']==level)]
    assert matches, (state,schema,level)
    # Lexical first content-qualified control, independent of a new inspector observation.
    return matches[0]


def prepare():
    identities()
    assert load(ROOT / 'coverage-analysis.json')['package_passed'] == 162
    catalog = seed_catalog()
    entries = []
    capture_mutations = ['drain','stdout-eof','stderr-eof','stdout-error','stderr-error','stdout-overflow','stderr-overflow','missing-capture']
    exit_mutations = ['missing-post','null-post','nonzero-post','string-post','negative-post','large-post','boolean-post','terminal-nonzero','both-nonzero','duplicate-exit']
    success_seeds = [selected(catalog,'completed',3,level) for level in ['off','minimal','verbose','debug']]
    success_seeds += [selected(catalog,'preflight_checked',schema) for schema in [2,3]]
    for seed in success_seeds:
        for mutation in capture_mutations + exit_mutations + ['missing-status']:
            entries.append({'group':'success','seed':seed,'mutation':mutation,'expected_error':'evidence_incomplete' if mutation=='missing-status' else 'evidence_corrupt','expected_state':None,'views':'first-and-end'})
        if seed['level'] != 'off':
            entries.append({'group':'success','seed':seed,'mutation':'bad-log','expected_error':'evidence_corrupt','expected_state':None,'views':'first-and-end'})
    for state in ['blocked','failed','cancelled','timed_out','cleanup_uncertain']:
        seed = selected(catalog,state,3,'off')
        for mutation in ['failure-stdout','failure-stderr','failure-null','missing-post']:
            entries.append({'group':'compatibility','seed':seed,'mutation':mutation,'expected_error':'evidence_corrupt' if mutation=='missing-post' else None,'expected_state':None if mutation=='missing-post' else state,'views':'first-and-end'})
    peer_legacy = selected(catalog,'completed',1)
    native_legacy = selected(catalog,'preflight_checked',2)
    for seed in [peer_legacy,native_legacy]:
        entries.append({'group':'compatibility','seed':seed,'mutation':'historical','expected_error':None,'expected_state':seed['state'],'views':'first-and-end'})
    for mutation in ['drain','missing-post','nonzero-post']:
        entries.append({'group':'compatibility','seed':peer_legacy,'mutation':mutation,'expected_error':'evidence_corrupt','expected_state':None,'views':'first-and-end'})
    peer_debug = selected(catalog,'completed',3,'debug')
    for mutation,state,error in [('interrupted','interrupted_unknown',None),('detail-only','completed',None),('no-capture-schema',None,'evidence_corrupt')]:
        entries.append({'group':'compatibility','seed':peer_debug,'mutation':mutation,'expected_error':error,'expected_state':state,'views':'first-and-end'})
    for number,entry in enumerate(entries,1):
        entry['id'] = f'M-{number:03d}'
    protected_roots = sorted({entry['seed']['root'] for entry in entries})
    protected = {path:digest for root in protected_roots for path,digest in bindings(Path(root)).items()}
    plan = {'script_sha256':sha(Path(__file__)),'executable_sha256':sha(EXE),'candidate_manifest_sha256':sha(ROOT/'candidate-manifest.json'),'seed_catalog':catalog,'protected_seed_files':protected,'entries':entries,'scope':'Copied record interpretation only; actual prior peer controls and explicitly synthetic preflight records; no worker launch or native qualification.'}
    assert not (ROOT / 'cli-matrix-plan.json').exists()
    save(ROOT/'cli-matrix-plan.json',plan)
    print(json.dumps({'catalog':len(catalog),'subcases':len(entries),'success':sum(e['group']=='success' for e in entries),'compatibility':sum(e['group']=='compatibility' for e in entries),'plan_sha256':sha(ROOT/'cli-matrix-plan.json')},indent=2))


def mutate(run, events, mutation):
    exit_event = next(e for e in events if e['kind']=='process_exit')
    data = exit_event['data']
    terminal = events[-1]['data']
    if mutation == 'drain':
        data['capture']['drain_complete'] = False
    elif mutation in ['stdout-eof','stderr-eof','stdout-error','stderr-error','stdout-overflow','stderr-overflow']:
        stream,kind = mutation.split('-')
        if kind=='eof':
            data['capture'][stream]['eof'] = False
            data['capture']['drain_complete'] = False
        elif kind=='error':
            data['capture'][stream]['read_error'] = 'pipe_read_failed'
            data['capture']['drain_complete'] = False
        else:
            data['capture'][stream]['byte_overflow'] = True
    elif mutation=='missing-capture':
        del data['capture']
    elif mutation=='missing-post':
        del data['worker_exit_code']
    elif mutation.endswith('-post'):
        data['worker_exit_code'] = {'null':None,'nonzero':29,'string':'0','negative':-1,'large':2**32,'boolean':False}[mutation[:-5]]
    elif mutation in ['terminal-nonzero','both-nonzero']:
        terminal['worker_exit_code'] = 29
        if mutation=='both-nonzero':
            data['worker_exit_code'] = 29
    elif mutation=='duplicate-exit':
        events.insert(events.index(exit_event)+1,copy.deepcopy(exit_event))
    elif mutation=='missing-status':
        for event in events:
            if event['data'].get('method')=='diagnostics_status':
                event['data']['method']='unrelated'
    elif mutation=='bad-log':
        (run/'diagnostics.jsonl').write_bytes(b'{}\n')
    elif mutation.startswith('failure-'):
        stream='stderr' if mutation=='failure-stderr' else 'stdout'
        data['capture']['drain_complete']=False
        data['capture'][stream].update({'eof':False,'read_error':'pipe_read_failed','byte_overflow':True})
        if mutation=='failure-null':
            data['worker_exit_code']=None
            terminal['worker_exit_code']=None
    elif mutation=='historical':
        inputs=load(run/'inputs.json')
        del inputs['capture_schema']
        save(run/'inputs.json',inputs)
        exit_event['data']={'worker_exit_code':0,'tree_stopped':True}
        events[:]=[event for event in events if event['data'].get('method')!='diagnostics_status']
    elif mutation=='interrupted':
        data['capture']['drain_complete']=False
        data['capture']['stderr'].update({'eof':False,'read_error':'pipe_read_failed'})
        events.pop()
    elif mutation=='detail-only':
        data['observed_before_stop']=False
        data['pre_stop_exit_code']=None
        for stream in ['stdout','stderr']:
            data['capture'][stream].update({'detail_dropped':99,'classification_truncated':True})
    elif mutation=='no-capture-schema':
        inputs=load(run/'inputs.json')
        del inputs['capture_schema']
        save(run/'inputs.json',inputs)
    else:
        raise AssertionError(mutation)
    for number,event in enumerate(events,1):
        event['seq']=number
    events_write(run,events)
    if mutation=='interrupted':
        with (run/'journal.jsonl').open('ab') as stream:
            stream.write(b'{unfinished')


def observe(run, destination, label, expected_state, expected_error, after, limit):
    before=bindings(run)
    argv=[str(EXE),'inspect','--run-dir',str(run),'--after',str(after),'--limit',str(limit)]
    start=time.monotonic()
    result=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
    (destination/f'{label}.stdout.txt').write_bytes(result.stdout)
    (destination/f'{label}.stderr.txt').write_bytes(result.stderr)
    after_bytes=bindings(run)
    if before!=after_bytes:
        save(ROOT/'STOP.json',{'class':'EXECUTION_SAFETY_BLOCKER','case':label,'reason':'unexpected mutation by read-only inspector','before':before,'after':after_bytes})
        raise AssertionError('Inspector mutated QA record')
    output=json.loads(result.stdout) if result.stdout else None
    error=json.loads(result.stderr) if result.stderr else None
    if expected_error:
        met=result.returncode==4 and output is None and error=={'error':expected_error}
    else:
        met=result.returncode==0 and error is None and output['state']==expected_state
        met=met and len(output['events'])<=limit and output['next_after']>=after
    record={'label':label,'argv':argv,'cwd':str(PROJECT),'exit_code':result.returncode,'expected_state':expected_state,'expected_error':expected_error,'state':output.get('state') if output else None,'error':error,'read_only':True,'expectation_met':met,'elapsed_seconds':time.monotonic()-start,'before_sha256':before}
    save(destination/f'{label}.json',record)
    return record


def execute(group):
    identities()
    plan=load(ROOT/'cli-matrix-plan.json')
    assert sha(Path(__file__))==plan['script_sha256'] and sha(EXE)==plan['executable_sha256']
    for path,digest in plan['protected_seed_files'].items():
        assert sha(Path(path))==digest,path
    attempt=ROOT/'attempts'/('18-rt01' if group=='success' else '19-rt02')
    attempt.mkdir(exist_ok=False)
    save(attempt/'launch.json',{'action':'CLI matrix '+group,'started_utc':datetime.now(timezone.utc).isoformat(),'plan_sha256':sha(ROOT/'cli-matrix-plan.json'),'script_sha256':sha(Path(__file__)),'executable_sha256':sha(EXE)})
    records=[]
    start=time.monotonic()
    for entry in [entry for entry in plan['entries'] if entry['group']==group]:
        identities_stop=(ROOT/'STOP.json').exists()
        assert not identities_stop
        target=attempt/entry['id']
        target.mkdir()
        run=target/'run'
        shutil.copytree(Path(entry['seed']['run']),run)
        request=load(run/'request.json')
        request['run_dir']=str(run)
        save(run/'request.json',request)
        inputs=load(run/'inputs.json')
        inputs['request_sha256']=sha(run/'request.json')
        save(run/'inputs.json',inputs)
        assert sha(Path(entry['seed']['control']))==entry['seed']['control_sha256']
        events=load(Path(entry['seed']['control']))['events']
        events_write(run,events)
        control=observe(run,target,'control',entry['seed']['state'],None,0,100)
        records.append(control)
        assert control['expectation_met'], ('invalid constructed control',entry)
        (target/'journal-before.jsonl').write_bytes((run/'journal.jsonl').read_bytes())
        mutate(run,events,entry['mutation'])
        save(target/'selection.json',entry)
        for label,after,limit in [('first',0,1),('end',len(events),1)]:
            records.append(observe(run,target,label,entry['expected_state'],entry['expected_error'],after,limit))
    for path,digest in plan['protected_seed_files'].items():
        assert sha(Path(path))==digest,path
    identities()
    summary={'case':'RT-01' if group=='success' else 'RT-02','action':'CLI matrix '+group,'status':'PASS' if all(record['expectation_met'] for record in records) else 'FAIL','observations':len(records),'passed_observations':sum(record['expectation_met'] for record in records),'failed':[record for record in records if not record['expectation_met']],'elapsed_seconds':time.monotonic()-start,'ended_utc':datetime.now(timezone.utc).isoformat(),'read_only':True,'native_codex':'NOT_RUN'}
    save(attempt/'receipt.json',summary)
    print(json.dumps(summary,indent=2))
    raise SystemExit(0 if summary['status']=='PASS' else 1)


parser=argparse.ArgumentParser()
parser.add_argument('action',choices=['prepare','success','compatibility'])
action=parser.parse_args().action
prepare() if action=='prepare' else execute(action)
