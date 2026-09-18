"""Independent contract probes; Python records OS observations, not framework acceptance."""
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import datetime
from record import ROOT, WORK, PACKAGE, CARGO, sha, capture, write

K = ctypes.WinDLL('kernel32', use_last_error=True)
K.OpenProcess.argtypes = [wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
K.OpenProcess.restype = wintypes.HANDLE
K.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD]
K.WaitForSingleObject.restype=wintypes.DWORD
K.CloseHandle.argtypes=[wintypes.HANDLE]
K.CloseHandle.restype=wintypes.BOOL

def held(pid):
    h=K.OpenProcess(0x00100000|0x1000,False,pid)
    if not h:
        raise OSError(ctypes.get_last_error(),'OpenProcess failed')
    return h

def fixture(label,case,peer):
    path=ROOT/'independent-attempts'/label
    path.mkdir(parents=True,exist_ok=False)
    checkout=path/'fixture'
    checkout.mkdir()
    source=WORK/'docs/specs/framework/runtime/fixtures/codex-worker-v1/task.json'
    shutil.copyfile(source,checkout/'task.json')
    (checkout/'peer-case.txt').write_bytes((case+'\n').encode('ascii'))
    request={'schema_version':1,'project_id':'qa-project','checkout_id':'qa-checkout','work_id':'qa-work','run_id':label,
       'candidate_sha256':sha(checkout/'task.json'),'checkout_root':str(checkout),'run_dir':str(path/'run'),
       'worker_executable':str(peer),'worker_sha256':sha(peer),'adapter':'peer','scenario':'complete','profile':None}
    (path/'request.json').write_text(json.dumps(request),encoding='utf-8')
    return path

def events(path):
    p=path/'run/journal.jsonl'
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []

def result(path,record):
    record['candidate_manifest_sha256']=sha(ROOT/'selected-manifest.json')
    record['fixture_sha256_after']=sha(path/'fixture/task.json')
    for key in ['stdout','stderr']:
        record[key+'_sha256']=sha(path/(key+'.txt'))
    (path/'result.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print(json.dumps({'case':path.name,**{k:v for k,v in record.items() if k not in ['trace','pages']}}),flush=True)

def bounded(label,case,expected,block=False,cancel=False):
    bindir=ROOT/'independent-target/debug'
    path=fixture(label,case,bindir/'protocol-peer.exe')
    args=[str(bindir/'qa-driver.exe'),str(path/'request.json')]+(['cancel'] if cancel else [])
    rec={'argv':args,'cwd':str(path),'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'executable_sha256':sha(args[0]),'expected_exit':expected,'bound_seconds':3 if block else 5}
    start=time.monotonic()
    h=None
    try:
        with (path/'stdout.txt').open('wb') as out,(path/'stderr.txt').open('wb') as err:
            p=subprocess.Popen(args,cwd=path,stdin=subprocess.PIPE,stdout=out,stderr=err)
            rec['owned_driver_pid']=p.pid
            while p.poll() is None and time.monotonic()-start<rec['bound_seconds']:
                pidfile=path/'qa-peer-pid.txt'
                if h is None and pidfile.exists():
                    raw=pidfile.read_text()
                    if raw:
                        h=held(int(raw));rec['held_peer_pid']=int(raw)
                time.sleep(.01)
            rec['deadline_overrun']=p.poll() is None
            if rec['deadline_overrun']:
                rec['peer_live_before_containment']=K.WaitForSingleObject(h,0)==258 if h else None
                p.kill() # Exact live owned driver handle; its Job Object owns the peer.
            rec['actual_exit']=p.wait(timeout=5)
            if p.stdin: p.stdin.close()
        rec['elapsed_seconds']=time.monotonic()-start
        rec['peer_stopped_after']=K.WaitForSingleObject(h,5000)==0 if h else None
        rec['large_request_sent']=(path/'large-request-sent').exists()
        trace=path/'qa-trace.jsonl'
        rec['trace']=[json.loads(x) for x in trace.read_text().splitlines()] if trace.exists() else []
        ev=events(path)
        rec['event_kinds']=[e['kind'] for e in ev]
        rec['terminal']=ev[-1]['data'] if ev and ev[-1]['kind']=='terminal' else None
        rec['pass']=not rec['deadline_overrun'] and rec['actual_exit']==expected
        rec['fixture_unchanged']=sha(path/'fixture/task.json')==json.loads((path/'request.json').read_text())['candidate_sha256']
        rec['pass']=rec['pass'] and rec['fixture_unchanged'] and rec['peer_stopped_after'] is True
        if label.startswith('IQ-02'):
            rec['expected_reason']='user_cancel' if cancel else 'deadline'
            rec['expected_outcome']='cancelled' if cancel else 'timed_out'
            rec['completion_bound_seconds']=1.2 if cancel else 1.4
            rec['pass']=rec['pass'] and rec['elapsed_seconds']<=rec['completion_bound_seconds'] and rec['terminal'] is not None
            if rec['terminal'] is not None:
                rec['pass']=rec['pass'] and rec['terminal']['reason']==rec['expected_reason'] and rec['terminal']['outcome']==rec['expected_outcome'] and rec['terminal']['tree_stopped'] is True
            rec['pass']=rec['pass'] and [v.get('method') for v in rec['trace']]==['initialize']
        if label.startswith('IQ-01'):
            methods=[v.get('method') for v in rec['trace']]
            wanted=['initialize','initialized','account/read','model/list','account/rateLimits/read','thread/start']
            if label!='IQ-01-policy':wanted.append('turn/start')
            rec['contract_trace_matches']=methods[:len(wanted)]==wanted and methods.count('turn/start')==(0 if label=='IQ-01-policy' else 1)
            reason='completed' if label=='IQ-01-valid' else 'profile_unqualified' if label=='IQ-01-policy' else 'oracle_mismatch'
            rec['expected_reason']=reason
            rec['pass']=rec['pass'] and rec['contract_trace_matches'] and rec['terminal'] is not None and rec['terminal']['reason']==reason
        if label=='IQ-05-private-error' or label.startswith('RT-02'):
            files=[path/'stdout.txt',path/'stderr.txt',path/'run/journal.jsonl']
            rec['private_marker_files']=[str(f) for f in files if f.exists() and b'QA_PRIVATE_SENTINEL_7159' in f.read_bytes()]
            rec['pass']=rec['pass'] and not rec['private_marker_files']
        if label=='IQ-05-private-error':
            rec['pass']=rec['pass'] and rec['terminal'] is not None and rec['terminal']['reason']=='protocol_error'
        result(path,rec)
    finally:
        if h: K.CloseHandle(h)
    return rec

def lifecycle(kind):
    bindir=ROOT/'target/debug'
    path=fixture('IQ-03-'+kind,'WF-13' if kind!='kill' else 'WF-14',bindir/'protocol-peer.exe')
    main=bindir/'devforgeai-codex-worker-probe.exe'
    args=[str(main),'run','--request',str(path/'request.json')]
    if kind=='ctrlc':args=[str(bindir/'console-driver.exe'),str(main),str(path/'request.json')]
    rec={'argv':args,'cwd':str(path),'started':datetime.datetime.now(datetime.timezone.utc).isoformat(),'executable_sha256':sha(args[0])}
    handles=[]
    with (path/'stdout.txt').open('wb') as out,(path/'stderr.txt').open('wb') as err:
        p=subprocess.Popen(args,cwd=path,stdin=subprocess.PIPE,stdout=out,stderr=err)
        rec['owned_driver_pid']=p.pid
        try:
            deadline=time.monotonic()+5
            while not (path/'peer-pids.json').exists():
                if time.monotonic()>deadline or p.poll() is not None:raise RuntimeError('missing peer readiness')
                time.sleep(.01)
            ids=json.loads((path/'peer-pids.json').read_text())
            handles=[held(ids['peer']),held(ids['descendant'])]
            rec['held_processes']=ids
            rec['initial_waits']=[K.WaitForSingleObject(h,0) for h in handles]
            start=time.monotonic()
            if kind=='stdin':p.stdin.write(b'{"op":"cancel"}\n');p.stdin.flush()
            elif kind=='ctrlc':(path/'signal-ready').write_bytes(b'ready')
            else:p.kill()
            rec['exit_code']=p.wait(timeout=12)
            rec['waits']=[K.WaitForSingleObject(h,5000) for h in handles]
            rec['elapsed_seconds']=time.monotonic()-start
            rec['pass']=rec['initial_waits']==[258,258] and rec['waits']==[0,0] and rec['elapsed_seconds']<(5 if kind=='kill' else 11) and (kind=='kill' or rec['exit_code']==5)
        finally:
            if p.poll() is None:
                # For the console wrapper, contain its current owned subtree as well.
                subprocess.run(['C:/Windows/System32/taskkill.exe','/PID',str(p.pid),'/T','/F'],capture_output=True,timeout=20)
                p.wait(timeout=5)
            if p.stdin:p.stdin.close()
            for h in handles:K.CloseHandle(h)
    result(path,rec)
    return rec

if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='build':
        capture('05-independent-build',[CARGO,'build','--offline','--manifest-path',ROOT/'independent/Cargo.toml'],
            cwd=ROOT/'independent',extra={'CARGO_TARGET_DIR':str(ROOT/'independent-target')},timeout=180)
    elif mode=='protocol':
        for label,case,code in [('IQ-01-valid','WF-01-90',0),('IQ-01-wrong','WF-18-90',4),
          ('IQ-01-extra','WF-18-91',4),('IQ-01-duplicate','WF-18-92',4),('IQ-01-missing','WF-18-93',4),('IQ-01-policy','WF-02-90',3)]:
            bounded(label,case,code)
    elif mode=='backpressure':
        bounded('IQ-02-deadline','WF-16-90',6,block=True)
        bounded('IQ-02-cancel','WF-16-91',5,block=True,cancel=True)
    elif mode=='lifecycle':
        for kind in ['stdin','ctrlc','kill']:lifecycle(kind)
    elif mode=='privacy':
        bounded('IQ-05-private-error','WF-07-90',4)
    elif mode=='inspect':
        bindir=ROOT/'target/debug'
        path=fixture('IQ-04-inspect','WF-01',bindir/'protocol-peer.exe')
        main=bindir/'devforgeai-codex-worker-probe.exe'
        runargs=[str(main),'run','--request',str(path/'request.json')]
        with (path/'stdout.txt').open('wb') as out,(path/'stderr.txt').open('wb') as err:
            p=subprocess.Popen(runargs,stdin=subprocess.PIPE,stdout=out,stderr=err,cwd=path)
            code=p.wait(timeout=10);p.stdin.close()
        before={str(f.relative_to(path)):sha(f) for f in path.rglob('*') if f.is_file()}
        args=[str(main),'inspect','--run-dir',str(path/'run'),'--after','0','--limit','100']
        one=subprocess.run(args,capture_output=True,timeout=5,cwd=path)
        two=subprocess.run(args,capture_output=True,timeout=5,cwd=path)
        value=json.loads(one.stdout)
        seqs=[];after=0;pages=[]
        while True:
            pageargs=[str(main),'inspect','--run-dir',str(path/'run'),'--after',str(after),'--limit','2']
            page=subprocess.run(pageargs,capture_output=True,timeout=5,cwd=path)
            pagevalue=json.loads(page.stdout)
            pages.append({'argv':pageargs,'exit_code':page.returncode,'value':pagevalue})
            if not pagevalue['events']:break
            seqs.extend(e['seq'] for e in pagevalue['events']);after=pagevalue['next_after']
        afterhash={str(f.relative_to(path)):sha(f) for f in path.rglob('*') if f.is_file()}
        trace=[json.loads(x) for x in (path/'peer-trace.jsonl').read_text().splitlines()]
        rec={'run_argv':runargs,'inspect_argv':args,'cwd':str(path),'run_exit':code,'inspect_exits':[one.returncode,two.returncode],
             'identical':one.stdout==two.stdout,'unchanged':before==afterhash,'state':value['state'],
             'seqs':seqs,'pages':pages,'turn_count':sum(x.get('method')=='turn/start' for x in trace),
             'pass':code==0 and one.returncode==two.returncode==0 and one.stdout==two.stdout and before==afterhash and
             value['state']=='completed' and seqs==list(range(1,len(value['events'])+1))}
        result(path,rec)
    else:raise SystemExit('unknown selection')
