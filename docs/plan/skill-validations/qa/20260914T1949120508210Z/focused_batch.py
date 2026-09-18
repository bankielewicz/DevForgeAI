"""Two independent preplanned cases; each once; no retries or bypass flags."""
from pathlib import Path
import subprocess
import sys
root=Path(__file__).resolve().parent
for case in ['QPV-02','QPV-06']:
    result=subprocess.run([sys.executable,'-B','-X','utf8',str(root/'native_trial.py'),case,sys.argv[1]],cwd=root.parents[4])
    print(case, result.returncode,flush=True)
