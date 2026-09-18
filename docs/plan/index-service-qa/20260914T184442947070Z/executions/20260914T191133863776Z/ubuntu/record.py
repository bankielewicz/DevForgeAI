"""QA evidence recorder only; no framework authority or product repair."""
import pathlib, os, sys, subprocess, json, time, hashlib, datetime
HERE=pathlib.Path(__file__).resolve().parent
SCRATCH=pathlib.Path(os.environ.get("QA_SCRATCH",str(HERE/"scratch")))
CANDIDATE=SCRATCH/"candidate"
def run(case,argv,timeout=1800):
    attempt=HERE/"attempts"/case
    attempt.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy()
    for name in ["TEMP","TMP","TMPDIR"]:env[name]=os.environ.get("QA_TEMP",str(SCRATCH/"temp"))
    env.update(CARGO_TARGET_DIR=str(SCRATCH/"target"),CARGO_LLVM_COV_TARGET_DIR=str(SCRATCH/"coverage-target"),DEVFORGEAI_INDEX_DATA=str(SCRATCH/"default-data"),DEVFORGEAI_GUI_EVIDENCE=str(attempt/"gui"),CARGO_TERM_COLOR="never",RUST_BACKTRACE="1")
    start=datetime.datetime.now(datetime.timezone.utc).isoformat(); tick=time.monotonic()
    receipt={"case_id":case,"argv":argv,"cwd":str(CANDIDATE),"platform":sys.platform,"start":start,"environment_overrides":{k:env[k] for k in ["TEMP","TMP","TMPDIR","CARGO_TARGET_DIR","CARGO_LLVM_COV_TARGET_DIR","DEVFORGEAI_INDEX_DATA","DEVFORGEAI_GUI_EVIDENCE"]},"timeout_seconds":timeout}
    (attempt/"started.json").write_text(json.dumps(receipt,indent=2))
    with (attempt/"stdout.txt").open("wb") as out,(attempt/"stderr.txt").open("wb") as err:
        p=subprocess.Popen(argv,cwd=CANDIDATE,env=env,stdin=subprocess.DEVNULL,stdout=out,stderr=err)
        receipt["pid"]=p.pid
        try:receipt["exit_code"]=p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            receipt["timeout"]=True;receipt["exit_code"]=None
            # No uncertain child replay/kill. Leave state for explicit observation.
    receipt.update(end=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick)
    for name in ["stdout.txt","stderr.txt"]:receipt[name+"_sha256"]=hashlib.sha256((attempt/name).read_bytes()).hexdigest()
    (attempt/"receipt.json").write_text(json.dumps(receipt,indent=2))
    print(json.dumps(receipt),flush=True)
    return receipt
if __name__=="__main__":
    name=sys.argv[1]
    if name=="fmt":args=["cargo","fmt","--all","--","--check"]
    elif name=="clippy":args=["cargo","clippy","--locked","--offline","--all-targets","--","-D","warnings"]
    elif name=="build":args=["cargo","build","--locked","--offline","--release"]
    elif name=="list":args=["cargo","test","--locked","--offline","--all-targets","--","--list"]
    elif name=="coverage":args=["cargo","llvm-cov","--locked","--offline","--all-targets","--ignore-run-fail","--json","--output-path",str(HERE/"coverage.json"),"--fail-under-lines","95","--ignore-filename-regex",r"[/\\](tests|examples|fixtures)[/\\]","--","--test-threads=1"]
    elif name=="benchmark":args=["cargo","run","--locked","--offline","--release","--example","benchmark","--",str(HERE/"benchmark-fixtures.json")]
    elif name=="collector-env":args=["cargo","llvm-cov","show-env"]
    else:raise SystemExit("Unknown task")
    run(os.environ.get("QA_ATTEMPT",name),args)

