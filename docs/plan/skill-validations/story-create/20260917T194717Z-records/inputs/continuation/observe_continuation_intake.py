"""Recheck the existing authored intake without rewriting authoring history."""
import json
from pathlib import Path
import subprocess
import sys
from prepare_continuation import RUN,PROJECT,put,ref
request=PROJECT/'docs/plan/skill-authorings/story-create/20260917T182711Z-02/validation-request.json'
argv=[sys.executable,'-B','-X','utf8',str(PROJECT/'.agents/skills/skill-validator/scripts/authoring_intake.py'),'--request',str(request),'--request-sha256','ab83db7725bd07ed97210a7f5d1032922813ac94433210a1651e23f45d5bab27']
result=subprocess.run(argv,capture_output=True,timeout=120)
put(RUN/'intake.stdout.txt',result.stdout.decode('utf-8'))
put(RUN/'intake.stderr.txt',result.stderr.decode('utf-8'))
put(RUN/'intake.execution.json',{'argv':argv,'exit_code':result.returncode,'request':ref(request)})
print(result.stdout.decode('utf-8'))
raise SystemExit(result.returncode)
