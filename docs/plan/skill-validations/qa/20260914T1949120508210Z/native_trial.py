"""One retained, bounded cold CLI attempt. Never retries automatically."""
from bootstrap import ROOT, write, observe
import datetime
import json
import subprocess
import sys

case=ROOT/'trials'/sys.argv[1]
attempt=sys.argv[2]
record=case/f'attempt-{attempt}.json'
assert not record.exists()
plan=json.loads((case/'plan.json').read_bytes())
project=case/'project'
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
stdout=case/f'attempt-{attempt}.stdout.jsonl'
stderr=case/f'attempt-{attempt}.stderr.txt'
assert not stdout.exists() and not stderr.exists()
timed_out=False
with stdout.open('wb') as out, stderr.open('wb') as err:
    process=subprocess.Popen(plan['command'],cwd=project,stdin=subprocess.PIPE,stdout=out,stderr=err)
    try:
        process.communicate((case/'prompt.txt').read_bytes(),timeout=plan['timeout_seconds'])
    except subprocess.TimeoutExpired:
        timed_out=True
        # PID comes only from this still-running owned child. No name-based kill.
        if process.poll() is None:
            cleanup=subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=15)
            (case/f'attempt-{attempt}.cleanup.stdout').write_bytes(cleanup.stdout)
            (case/f'attempt-{attempt}.cleanup.stderr').write_bytes(cleanup.stderr)
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
write(record,dict(schema_version='1',case_id=plan['case_id'],attempt_id=attempt,command=plan['command'],cwd=str(project),started_at_utc=start,ended_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=process.poll(),timeout=timed_out,timeout_seconds=plan['timeout_seconds'],stdout=stdout.name,stderr=stderr.name,limitations=['CLI workspace sandbox is host-controlled; task prompt is not proof of OS isolation.']))
write(case/f'attempt-{attempt}.after.json',observe.make_manifest(project))
print(json.dumps(json.loads(record.read_bytes()),indent=2))
print(stderr.read_text(encoding='utf-8',errors='replace')[-2500:])
sys.exit(124 if timed_out else process.returncode)
