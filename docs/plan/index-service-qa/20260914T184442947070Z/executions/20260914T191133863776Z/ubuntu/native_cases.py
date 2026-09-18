"""Independent native QA observations; operates only owned synthetic state."""
import pathlib,os,sys,json,subprocess,time,hashlib,sqlite3,datetime
HERE=pathlib.Path(__file__).resolve().parent
SCRATCH=pathlib.Path(os.environ.get("QA_SCRATCH",str(HERE/"scratch")))
TEMP=pathlib.Path(os.environ.get("QA_TEMP",str(SCRATCH/"temp")))
ROOT=TEMP/"native-acceptance";ROOT.mkdir(exist_ok=False)
DATA=ROOT/"data";SOURCE=ROOT/"source";SOURCE.mkdir()
EXE=SCRATCH/"target/release"/("devforgeai.exe" if os.name=="nt" else "devforgeai")
OUT=HERE/"native-acceptance";OUT.mkdir(exist_ok=False)
env=os.environ.copy();env["DEVFORGEAI_INDEX_DATA"]=str(DATA)
records=[]; results=[];seq=0
def cli(args,input=None):
    global seq
    seq+=1;start=time.time()
    p=subprocess.run([str(EXE),*args,"--json"],input=input,capture_output=True,env=env,timeout=130)
    stem=f"{seq:03}";(OUT/(stem+".stdout")).write_bytes(p.stdout);(OUT/(stem+".stderr")).write_bytes(p.stderr)
    value=json.loads(p.stdout);assert isinstance(value,dict)
    records.append({"sequence":seq,"argv":[str(EXE),*args,"--json"],"input":input.decode() if input else None,"start":start,"end":time.time(),"exit":p.returncode,"stdout":stem+".stdout","stderr":stem+".stderr"})
    return p.returncode,value
def ok(args):c,v=cli(args);assert c==0,(c,v);assert v["ok"] is True,v;return v["data"]
def waitjob(j):
    end=time.monotonic()+30
    while time.monotonic()<end:
        d=ok(["job","status","--job",j])
        if d["outcome"] not in ["queued","running"]:assert d["outcome"]=="succeeded",d;return d
        time.sleep(.05)
    raise AssertionError("job did not finish within harness30s")
def check(name,fn):
    start=time.time()
    try:detail=fn();results.append({"id":name,"status":"PASS","detail":detail,"start":start,"end":time.time()})
    except Exception as e:results.append({"id":name,"status":"FAIL" if isinstance(e,AssertionError) else "ERROR","detail":repr(e),"start":start,"end":time.time()})
def manifest():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SOURCE.iterdir() if p.is_file()}
def start():
    assert ok(["daemon","status"])["daemon_state"]=="stopped"
    ok(["daemon","start"]);assert ok(["daemon","start"])["already_running"] is True
    return "stopped -> started -> already_running"
check("N01",start)
project=None
def setup():
    global project
    ok(["daemon","pause"])
    for n,b in {"good.py":b"def before(): return 1\n","readme.md":b"documentation\n",".env":b"NEVER_INDEX_SECRET","utf16.txt":b"\xff\xfeA\x00","binary.txt":b"\x00\x01"}.items():(SOURCE/n).write_bytes(b)
    d=ok(["project","add","--root",str(SOURCE),"--name","Independent QA"]);project=d["project_id"]
    j=ok(["index","rescan","--project",project]);assert j["waiting_for_resume"] is True
    assert ok(["daemon","status"])["indexing_mode"]=="paused"
    ok(["daemon","resume"]);waitjob(j["job_id"])
    d=ok(["index","status","--project",project]);assert d["text_count"]==2,d;assert d["structural_count"]==1,d;assert d["skipped_count"]==2,d;assert d["excluded_count"]==1,d;assert d["coverage"]=="partial",d
    return d
check("N02",setup)
def source_read():
    d=ok(["index","status","--project",project]);generation=d["current_generation"]
    con=sqlite3.connect("file:"+str(DATA/"index.sqlite3")+"?mode=ro",uri=True)
    try:
        data=con.execute("select s.bytes from snapshots s join files f on s.hash=f.hash where generation=? and path='good.py'",(generation,)).fetchone()[0]
        assert data==(SOURCE/"good.py").read_bytes()
        assert con.execute("select count(*) from snapshots where instr(bytes,?)>0",(b"NEVER_INDEX_SECRET",)).fetchone()[0]==0
    finally:con.close()
    return {"generation":generation,"snapshot_sha256":hashlib.sha256(data).hexdigest(),"secret_snapshots":0}
if project:check("N03",source_read)
def changed():
    ok(["daemon","pause"]);f=SOURCE/"good.py";stat=f.stat();f.write_bytes(b"def after_(): return 2\n");os.utime(f,ns=(stat.st_atime_ns,stat.st_mtime_ns))
    old=ok(["index","status","--project",project])["current_generation"]
    assert ok(["daemon","status"])["indexing_mode"]=="paused"
    ok(["daemon","resume"])
    waitjob(ok(["index","rescan","--project",project])["job_id"])
    actual=source_read();assert actual["generation"]!=old
    return actual
if project:check("N04",changed)
def atomic_readers():
    c=sqlite3.connect("file:"+str(DATA/"index.sqlite3")+"?mode=ro",uri=True);c.execute("BEGIN")
    try:
        g=c.execute("select current from projects where id=?",(project,)).fetchone()[0]
        before=c.execute("select s.bytes from snapshots s join files f on s.hash=f.hash where generation=? and path='good.py'",(g,)).fetchone()[0]
        for _ in range(2):waitjob(ok(["index","reindex","--project",project])["job_id"])
        assert c.execute("select current from projects where id=?",(project,)).fetchone()[0]==g
        assert c.execute("select s.bytes from snapshots s join files f on s.hash=f.hash where generation=? and path='good.py'",(g,)).fetchone()[0]==before
    finally:c.close()
    return "real SQLite read transaction retained one generation across two daemon publications"
if project:check("N05",atomic_readers)
def rename_delete():
    old=ok(["index","status","--project",project])["current_generation"]
    (SOURCE/"good.py").rename(SOURCE/"renamed.py");(SOURCE/"readme.md").unlink()
    end=time.monotonic()+10
    while time.monotonic()<end:
        d=ok(["index","status","--project",project])
        if d["current_generation"]!=old and not d["dirty"]:break
        time.sleep(.1)
    else:raise AssertionError("watcher did not reconcile in10s harness")
    c=sqlite3.connect("file:"+str(DATA/"index.sqlite3")+"?mode=ro",uri=True)
    try:paths={r[0] for r in c.execute("select path from files where generation=?",(d["current_generation"],))}
    finally:c.close()
    assert "renamed.py" in paths and "good.py" not in paths and "readme.md" not in paths,paths
    return sorted(paths)
if project:check("N06",rename_delete)
def remove():
    before=manifest();code,v=cli(["project","remove","--project",project]);assert code==2,(code,v)
    ok(["project","remove","--project",project,"--yes"]);assert manifest()==before
    assert ok(["project","list"])["projects"]==[]
    return {"source_after":before}
if project:check("N07",remove)
def invalid_bridge():
    req={"protocol_version":2,"request_id":"550e8400-e29b-41d4-a716-446655440000","operation":"arbitrary.shell","timeout_ms":10000,"params":{}}
    code,value=cli(["bridge","request"],json.dumps(req).encode())
    assert code==4,(code,value);assert value["error"]["code"]=="PROTOCOL_INCOMPATIBLE";return value
check("N08",invalid_bridge)
def shutdown():
    ok(["daemon","stop"]);assert ok(["daemon","status"])["daemon_state"]=="stopped";assert ok(["daemon","stop"])["already_stopped"] is True
    return "owned daemon stopped and endpoint unavailable"
check("N09",shutdown)
(OUT/"commands.json").write_text(json.dumps(records,indent=2));(OUT/"results.json").write_text(json.dumps(results,indent=2))
print(json.dumps(results),flush=True)

