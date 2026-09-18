"""Retain read-only helper execution and actual environment; no acceptance authority."""
import datetime, hashlib, json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
PROJECT=ROOT.parents[4]
VAL=PROJECT/".agents/skills/skill-validator/scripts"
def run(case,argv):
    folder=ROOT/"observations"/case;folder.mkdir(parents=True,exist_ok=False)
    plan={"argv":argv,"cwd":str(PROJECT),"timeout_seconds":120,"effects":"stdout/stderr and evidence only; selected target read-only","start_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (folder/"plan.json").write_text(json.dumps(plan,indent=2),encoding="utf-8")
    start=datetime.datetime.now(datetime.timezone.utc)
    try:
        p=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=120)
        out,err,code=p.stdout,p.stderr,p.returncode;timed=False
    except subprocess.TimeoutExpired as e:
        out,err,code=e.stdout or b"",e.stderr or b"",None;timed=True
    (folder/"stdout.txt").write_bytes(out);(folder/"stderr.txt").write_bytes(err)
    result={**plan,"end_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"elapsed_seconds":(datetime.datetime.now(datetime.timezone.utc)-start).total_seconds(),"exit_code":code,"timed_out":timed}
    (folder/"attempt-001.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(case,code,out[:160].decode("utf-8","replace"))
    return out
prefix=[sys.executable,"-B","-X","utf8"]
run("structure",prefix+[str(VAL/"observe.py"),"structure","--source",str(ROOT/"source")])
run("installed-quick-validate",prefix+[r"C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py",str(ROOT/"source")])
run("text-resources",prefix+[str(VAL/"adaptive_observe.py"),"package","--source",str(ROOT/"source")])
# Readback at this stage establishes current preservation; final readback follows all trials.
run("initial-readback",prefix+[str(VAL/"observe.py"),"readback","--source",r"C:\Users\bryan\.codex\skills\.system\skill-creator","--manifest",str(ROOT/"source-manifest.json")])

