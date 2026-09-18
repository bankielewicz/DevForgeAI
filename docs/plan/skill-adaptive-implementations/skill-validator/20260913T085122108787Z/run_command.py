"""Terminal evidence runner. argv input; retains every attempt including timeout."""
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys
from capture import ROOT, RUN

if __name__ == '__main__':
    name, *command = sys.argv[1:]
    folder = RUN / 'commands' / name
    folder.mkdir(parents=True, exist_ok=False)
    start = dt.datetime.now(dt.timezone.utc).isoformat()
    (folder / 'plan.json').write_text(json.dumps({'argv':command,'cwd':str(ROOT),'timeout_seconds':120,'start':start}), encoding='utf-8')
    with (folder / 'stdout.txt').open('wb') as out, (folder / 'stderr.txt').open('wb') as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err)
        try:
            code = process.wait(timeout=120)
            termination = 'exited'
        except subprocess.TimeoutExpired:
            killed = subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'], stdout=err, stderr=err, timeout=15)
            if killed.returncode:
                process.kill()
            process.wait(timeout=15)
            code, termination = None, 'timeout-tree-terminated' if not killed.returncode else 'timeout-parent-killed-tree-unverified'
    (folder / 'result.json').write_text(json.dumps({'exit_code':code,'termination':termination,'end':dt.datetime.now(dt.timezone.utc).isoformat()}), encoding='utf-8')
    print(json.dumps({'command':command,'exit_code':code,'termination':termination,'evidence':str(folder)}))
    print((folder / 'stdout.txt').read_text(encoding='utf-8',errors='replace')[-2000:])
    print((folder / 'stderr.txt').read_text(encoding='utf-8',errors='replace')[-2000:])
