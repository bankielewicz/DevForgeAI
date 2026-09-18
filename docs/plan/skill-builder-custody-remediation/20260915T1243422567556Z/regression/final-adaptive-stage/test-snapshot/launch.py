"""One bounded suite attempt with exact command and retained process output."""
import datetime
import json
from pathlib import Path
import subprocess
import sys
import time
RUN=Path(__file__).resolve().parent
ROOT=RUN.parents[4]
attempt=sys.argv[1]
receipt=RUN/(attempt+'-process.json')
assert not receipt.exists()
command=[sys.executable,'-B','-X','utf8',str(RUN/'run_suite.py'),*sys.argv[1:]]
start=time.monotonic()
value={'command':command,'cwd':str(ROOT),'shell':'Native Windows Python subprocess argument vector; launched from PowerShell','filesystem':'Windows C:','start':datetime.datetime.now(datetime.timezone.utc).isoformat(),'timeout_seconds':120}
receipt.write_text(json.dumps(value,indent=2),encoding='utf-8')
try:
    result=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
    code=result.returncode;stdout=result.stdout;stderr=result.stderr
except subprocess.TimeoutExpired as exc:
    code=None;stdout=exc.stdout or b'';stderr=exc.stderr or b''
(RUN/(attempt+'-stdout.txt')).write_bytes(stdout)
(RUN/(attempt+'-stderr.txt')).write_bytes(stderr)
value.update(exit_code=code,elapsed_seconds=time.monotonic()-start,timeout=code is None)
receipt.write_text(json.dumps(value,indent=2),encoding='utf-8')
print(json.dumps(value));print(stdout.decode('utf-8',errors='replace')[-3000:]);print(stderr.decode('utf-8',errors='replace')[-5500:])
sys.exit(code if code is not None else 124)
