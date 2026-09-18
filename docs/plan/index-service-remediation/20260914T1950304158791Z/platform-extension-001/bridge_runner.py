import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent
PROJECT = Path(r"C:\Projects\DevForgeAI\devforgeai")
OUT = ROOT / "bridge"
OUT.mkdir(exist_ok=False)
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
manifest = json.loads((ROOT.parent / "source-manifest.json").read_text())
assert all(digest(Path(row["path"])) == row["sha256"] for row in manifest["files"])
env = os.environ.copy()
overrides = {"DEVFORGEAI_WSL_FIXTURE":"/tmp/dfr-wsl-20260914T1950304158791Z/bin/examples/wsl_fixture", "DEVFORGEAI_INDEX_DATA":str(ROOT / "bridge-data")}
env.update(overrides)
args = ["cargo","test","--locked","--offline","--test","wsl_bridge","--","--ignored","--test-threads=1"]
receipt = {"argv":args,"cwd":str(PROJECT),"environment_overrides":overrides,"candidate_manifest_sha256":digest(ROOT.parent / "source-manifest.json"),"runner_sha256":digest(Path(__file__)),"started_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"timeout_seconds":180}
start = time.monotonic()
with (OUT / "stdout.txt").open("wb") as stdout, (OUT / "stderr.txt").open("wb") as stderr:
    try:
        result = subprocess.run(args,cwd=PROJECT,env=env,stdout=stdout,stderr=stderr,timeout=180)
        receipt.update(exit_code=result.returncode,outcome="observed_exit")
    except subprocess.TimeoutExpired:
        receipt.update(exit_code=None,outcome="timeout")
receipt.update(elapsed_seconds=time.monotonic()-start,ended_at=datetime.datetime.now(datetime.timezone.utc).isoformat())
for name in ["stdout.txt","stderr.txt"]:
    receipt[name+"_sha256"] = digest(OUT / name)
(OUT / "receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt,indent=2))
print((OUT / "stdout.txt").read_text())
print((OUT / "stderr.txt").read_text())
