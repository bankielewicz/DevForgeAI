"""Retain evaluator-control outputs without altering target code."""
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parent
stage=sys.argv[1]
assert stage in ('red','green')
argv=[sys.executable,'-B','-X','utf8',str(ROOT/'test_graders.py')]
result=subprocess.run(argv,capture_output=True,timeout=120)
for stream,data in [('stdout',result.stdout),('stderr',result.stderr)]:
    with (ROOT/(stage+'.'+stream+'.txt')).open('xb') as handle:handle.write(data)
with (ROOT/(stage+'.execution.json')).open('x',encoding='utf-8') as handle:json.dump({'argv':argv,'exit_code':result.returncode},handle,indent=2)
print(result.stderr.decode('utf-8'))
raise SystemExit(result.returncode)
