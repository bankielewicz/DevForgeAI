"""Run the three required fault cases with observed triggers and guaranteed ACL restoration."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import threading
import time
import sys
from faults import observes_selected_epic
from prepare_continuation import RUN,put,ref
from run_trials import execute

def clock():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def watch_epic(stop):
    case=RUN/'trials/G01';stream=case/'attempt-001/stdout.txt';epic=case/'project/input/epic.md'
    deadline=time.monotonic()+1810
    while not stop.is_set() and time.monotonic()<deadline:
        if stream.exists():
            for number,line in enumerate(stream.read_text(encoding='utf-8').splitlines(),1):
                try:event=json.loads(line)
                except ValueError:continue
                if observes_selected_epic(event,'Copper owl 73.'):
                    before=epic.read_bytes()
                    note=b'\nConcurrent operator note: preserve violet kestrel 86.\n'
                    assert note not in before
                    with epic.open('ab') as handle:handle.write(note)
                    after=epic.read_bytes()
                    put(case/'fault-execution.json',{'timestamp':clock(),'trigger_event_line':number,'trigger_event_sha256':hashlib.sha256(line.encode('utf-8')).hexdigest(),'trigger_event_id':event['item']['id'],'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'append_only':after==before+note,'effect':'One unrelated note appended after completed source-read output while native process is active.','status':'EXECUTED'})
                    return
        stop.wait(0.2)
    put(case/'fault-execution.json',{'timestamp':clock(),'status':'NOT_TRIGGERED','reason':'Selected completed source read not observed before native completion or deadline.'})

def acl(action):
    case=RUN/'trials/G02';target=case/'project/backlog'
    argv=['C:/Program Files/PowerShell/7/pwsh.exe','-NoProfile','-File',str(RUN/'fault_controls.ps1'),'-Action',action,'-Target',str(target),'-StatePath',str(case/'acl-original.json')]
    result=subprocess.run(argv,capture_output=True,timeout=120)
    put(case/(action.lower()+'-acl.execution.json'),{'timestamp':clock(),'argv':argv,'exit_code':result.returncode,'stdout':result.stdout.decode('utf-8'),'stderr':result.stderr.decode('utf-8')})
    if result.returncode:raise RuntimeError('Synthetic ACL '+action+' failed')

def main():
    schedule=json.loads((RUN/'scheduling-amendment.json').read_bytes())
    assert schedule['global_native_concurrency_maximum']==3
    # The replay process has two workers; this sequential process adds one worker.
    selected=sys.argv[1:]
    if not selected or len(selected)!=len(set(selected)) or not set(selected)<={'G01','G02','G03'}:raise ValueError('Select required adverse cases once')
    for ident in selected:
        active=[p for p in (RUN/'trials').glob('*/attempt-*/started.json') if not (p.parent/'result.json').exists()]
        if len(active)>=3:raise ValueError('Declared global native concurrency would be exceeded')
        if ident=='G01':
            stop=threading.Event();watcher=threading.Thread(target=watch_epic,args=(stop,),daemon=False);watcher.start()
            try:value=execute(ident)
            finally:stop.set();watcher.join(timeout=10)
            assert not watcher.is_alive()
        elif ident=='G02':
            case=RUN/'trials/G02'
            try:
                acl('Deny')
                try:
                    (case/'project/backlog/denial-probe.txt').write_bytes(b'This must be denied.')
                except PermissionError:
                    put(case/'denial-probe.json',{'timestamp':clock(),'result':'PermissionError','created':False})
                else:raise RuntimeError('Selected directory is not write-denied')
                value=execute(ident)
            finally:
                if (case/'acl-original.json').exists():acl('Restore')
        else:value=execute(ident)
        print(json.dumps(value),flush=True)

if __name__=='__main__':main()
