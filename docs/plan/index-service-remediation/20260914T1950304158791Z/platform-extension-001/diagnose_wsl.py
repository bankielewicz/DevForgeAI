import datetime
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent
code = '''import hashlib,json,os
from pathlib import Path
root=Path("/home/bryan/Projects/devforgeai-remediation-20260914T1950304158791Z")
fixture=Path("/tmp/dfr-wsl-20260914T1950304158791Z/bin")
expected=json.loads((root/"expected.json").read_text())["files"]
drift=[r["path"] for r in expected if not (root/"devforgeai"/r["path"]).is_file() or hashlib.sha256((root/"devforgeai"/r["path"]).read_bytes()).hexdigest()!=r["sha256"]]
owned=[]
for p in Path("/proc").iterdir():
 if p.name.isdigit():
  try:
   exe=os.readlink(p/"exe")
   if str(root) in exe or str(fixture.parent) in exe: owned.append({"pid":int(p.name),"executable":exe})
  except (FileNotFoundError,PermissionError,ProcessLookupError): pass
print(json.dumps({"source_drift":drift,"fixture_directory_exists":fixture.is_dir(),"fixture_executable_exists":(fixture/"examples/wsl_fixture").is_file(),"remaining_owned_processes":owned,"retained_builds":[{"path":str(root/"devforgeai/target/release"/n),"sha256":hashlib.sha256((root/"devforgeai/target/release"/n).read_bytes()).hexdigest()} for n in ["devforgeai","devforgeai-indexd","examples/wsl_fixture"]]}))
'''
args = ["wsl","--distribution","Ubuntu","--user","bryan","--cd","/home/bryan","--exec","python3","-c",code]
result = subprocess.run(args,capture_output=True,timeout=30)
receipt = {"argv":args,"recorded_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"exit_code":result.returncode,"stdout":result.stdout.decode("utf-8",errors="replace"),"stderr":result.stderr.decode("utf-8",errors="replace")}
(root / "wsl-final-readback.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
