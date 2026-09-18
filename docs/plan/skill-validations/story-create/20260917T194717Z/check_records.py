"""Run both record-integrity readers with separate retained outputs."""
import json
from pathlib import Path
import subprocess
import sys

RAW=Path(__file__).resolve().parent
PROJECT=RAW.parents[4]
VALIDATOR=PROJECT/'.agents/skills/skill-validator/scripts'
attempt=sys.argv[1] if len(sys.argv)>1 else '001'
assert attempt.isdecimal() and len(attempt)==3

for name,script,suffix in [('legacy','observe.py','-records'),('adaptive','adaptive_observe.py','-supplemental')]:
    argv=[sys.executable,'-B','-X','utf8',str(VALIDATOR/script),'records','--run-root',str(RAW.with_name(RAW.name+suffix))]
    result=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=120)
    for stream,data in [('stdout',result.stdout),('stderr',result.stderr)]:
        with (RAW/(name+'-records-'+attempt+'.'+stream+'.txt')).open('xb') as handle:handle.write(data)
    with (RAW/(name+'-records-'+attempt+'.execution.json')).open('x',encoding='utf-8') as handle:
        json.dump(dict(argv=argv,cwd=str(PROJECT),exit_code=result.returncode),handle,indent=2)
    print(name,result.returncode,result.stdout.decode('utf-8'),result.stderr.decode('utf-8'))
