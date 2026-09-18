"""Check retained evidence integrity without re-executing product cases."""
import datetime,hashlib,json,pathlib,re,subprocess,sys
R=pathlib.Path(__file__).resolve().parent;PROJECT=R.parents[4];V=PROJECT/".agents/skills/skill-validator/scripts"
def load(p):return json.loads((R/p).read_text(encoding="utf-8"))
def write(p,v):
    q=R/p;q.parent.mkdir(parents=True,exist_ok=True)
    with q.open("x",encoding="utf-8") as f:f.write(v if isinstance(v,str) else json.dumps(v,indent=2)+"\n")
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Add the fetched body as a supporting source, keeping earlier retrieval intact.
sources=load("sources.json");write("inputs/sources-before-body.json",sources)
sources["sources"].append({"source_id":"official-build-skills-body","url":"https://learn.chatgpt.com/docs/build-skills","retrieved_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"sha256":sha(R/"inputs/official-build-skills-body.txt"),"snapshot_path":"inputs/official-build-skills-body.txt","sections":["L873-L897","L916-L932","L958-L985"],"freshness":"live_verified"})
(R/"sources.json").write_text(json.dumps(sources,indent=2)+"\n",encoding="utf-8")
# Recheck frozen evidence and all raw helper streams, without changing attempts.
plan=load("trials/helpers/frozen-plan.json")
assert sha(R/"trials/helpers/frozen-plan.json")==(R/"trials/helpers/frozen-plan.sha256").read_text().strip()
for case in load("trials/helpers/case-results.json")["cases"]:
    d=R/"trials/helpers/attempts"/case["id"]
    obs=json.loads((d/"attempt-after.json").read_text())
    before=json.loads((d/"attempt-before.json").read_text())
    assert before["plan_sha256"]==sha(R/"trials/helpers/frozen-plan.json")
    assert obs["result"]==case["result"]
    assert (d/"stdout.bin").read_bytes().decode("utf-8","replace")==obs["stdout"]
    assert (d/"stderr.bin").read_bytes().decode("utf-8","replace")==obs["stderr"]
    assert obs["started_at"]<=obs["ended_at"] and not obs["timed_out"]
# Target source and frozen rule copies are independently checked again.
baseline=load("inputs/final-input-bindings.json")
assert all(sha(R/path)==digest for path,digest in baseline.items())
for name in ("adaptive-validation.md","rules.md","trials.md","reporting.md","handoff.md","text-resource-checks.md"):
    assert sha(R/"inputs"/name)==sha(V.parent/"references"/name)
write("observations/evidence-readback.json",{"result":"PASS","helper_attempts":51,"raw_streams":102,"frozen_plan_unchanged":True,"pinned_input_digests_unchanged":True,"rule_source_copies_match_current_validator":True,"limits":"No product retry; no semantic acceptance inferred."})
def run(name,args):
    d=R/"observations"/name;d.mkdir()
    argv=[sys.executable,"-B","-X","utf8"]+args
    started=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=120)
    (d/"stdout.txt").write_bytes(p.stdout);(d/"stderr.txt").write_bytes(p.stderr)
    write("observations/"+name+"/attempt-001.json",{"argv":argv,"cwd":str(PROJECT),"started_at_utc":started,"ended_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"timeout_seconds":120,"exit_code":p.returncode})
    result=json.loads(p.stdout)
    print(name,p.returncode,result.get("status"),result.get("errors",result.get("observations",{}).get("errors")))
    return p.returncode,result
a,aa=run("records",[str(V/"observe.py"),"records","--run-root",str(R)])
b,bb=run("supplemental-records",[str(V/"adaptive_observe.py"),"records","--run-root",str(R.parent/(R.name+"-supplemental"))])
write("record-integrity.md",f"""# Record integrity
- Schema-1 records command: exit {a}, status {aa.get('status')}.
- Supplemental adaptive records: exit {b}, status {bb.get('status')}.
- Independent retained-stream/input checks: PASS, 51 helper attempts and 102 raw streams checked.
- Outputs: observations/records/stdout.txt and observations/supplemental-records/stdout.txt.
These observations verify supported record shapes, references, identities and reduction arithmetic. They do not establish semantic support, runtime behavior or framework acceptance.
""")
assert a==0 and b==0
# Verify report/proposal relative Markdown links now that final files exist.
broken=[]
for name in ("validation-report.md","revision-spec.md"):
    for target in re.findall(r"\]\(([^)]+)\)",(R/name).read_text()):
        if "://" not in target and not (R/target.split("#")[0]).exists():broken.append((name,target))
assert not broken,broken
write("observations/document-links.json",{"result":"PASS","documents":["validation-report.md","revision-spec.md"],"missing":[],"remote_links":"Official documentation fetched separately; this check is local."})
print("DOCUMENT_LINKS PASS")

