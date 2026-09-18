"""Independent artifact readback; authors' self-verdicts are not the oracle."""
import datetime, hashlib, json, pathlib, re, yaml
ROOT=pathlib.Path(__file__).resolve().parent
def dump(path,value):
    with (ROOT/path).open("x",encoding="utf-8") as f:json.dump(value,f,indent=2)
def manifest(root):
    return [{"path":p.relative_to(root).as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(root.rglob("*")) if p.is_file()]
results=[]
source=json.loads((ROOT/"source-manifest.json").read_text())["files"]
for case in ("create","update"):
    trial=ROOT/"trials"/case
    before=json.loads((trial/"before-manifest.json").read_text())
    after=manifest(trial/"workspace")
    dump("trials/"+case+"/after-manifest.json",after)
    maps={r["path"]:r for r in after}
    preserved=[]
    for row in before:
        relative=row["path"].removeprefix("workspace/")
        if relative=="draft-note/agents/openai.yaml":continue
        actual=maps.get(relative)
        preserved.append(actual is not None and actual["sha256"]==row["sha256"])
    snapshot=manifest(trial/"skill-creator")
    checks={"preexisting_unrelated_bytes_unchanged":all(preserved),"skill_creator_snapshot_unchanged":snapshot==source}
    if case=="create":
        skill=trial/"workspace/release-note-draft"
        text=(skill/"SKILL.md").read_text(encoding="utf-8")
        data=yaml.safe_load(re.match(r"---\n(.*?)\n---",text,re.S)[1])
        checks["name"]=data["name"]=="release-note-draft"
        checks["only_instruction_file"]=sorted(p.relative_to(skill).as_posix() for p in skill.rglob("*") if p.is_file())==["SKILL.md"]
        checks["ordinary_invocation_default"]=not (skill/"agents/openai.yaml").exists()
        manual={"reviewer":"primary; independent of author","result":"PASS","observations":["Explicit Added/Changed/Fixed order with empty groups omitted.","Unknown version/date remain unspecified; no current-date inference.","Preserves issue identifiers with correct changes; does not invent benefits or publish.","Missing notes/meaning-changing ambiguity route to material clarification.","Deliverable has actual instructions, no unfinished scaffold; optional helper/reference files omitted as requested."],"limit":"This tests skill creation; it is not a downstream live release/publication trial."}
    else:
        target=trial/"workspace/draft-note/agents/openai.yaml"
        data=yaml.safe_load(target.read_text())
        checks["requested_display_name"]=data["interface"]["display_name"]=="Incident Note"
        checks["requested_description"]=data["interface"]["short_description"] in ("Draft clear incident notes from supplied facts","Draft clear incident notes from supplied facts.")
        checks["policy_preserved"]=data["policy"]=={"allow_implicit_invocation":False}
        checks["dependency_preserved"]=data["dependencies"]=={"tools":[{"type":"mcp","value":"synthetic-notes","description":"Synthetic fixture only; do not connect","transport":"streamable_http","url":"https://example.invalid/mcp"}]}
        restored=target.read_bytes().replace(b'display_name: "Incident Note"',b'display_name: "Draft Note"').replace(b'short_description: "Draft clear incident notes from supplied facts."',b'short_description: "Draft incident notes from supplied facts"').replace(b'short_description: "Draft clear incident notes from supplied facts"',b'short_description: "Draft incident notes from supplied facts"')
        old=next(r for r in before if r["path"]=="workspace/draft-note/agents/openai.yaml")
        checks["all_other_yaml_bytes_preserved"]=hashlib.sha256(restored).hexdigest()==old["sha256"]
        manual={"reviewer":"primary; independent of author","result":"PASS","observations":["Only requested scalar values changed; byte-restoration hash equals original.","In-place edit used; policy/dependencies/default prompt/icon/comment preserved.","Sentence-ending period in unquoted request interpreted as part of requested description; both punctuation readings admitted explicitly."],"limit":"No native UI rendering or service connection tested."}
    result={"case_id":"SC-"+case.upper(),"result":"PASS" if all(checks.values()) else "FAIL","checks":checks,"manual_review":manual,"reviewed_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"evidence":["before-manifest.json","after-manifest.json","workspace/execution-log.json","workspace/delivered-summary.md"],"execution_limitation":"Agent task messages/command combined output retained; exact per-command UTC start/end not exposed in author logs. Measured command elapsed times and exits retained. OS-level isolation not claimed."}
    dump("trials/"+case+"/primary-review.json",result);results.append(result)
p=json.loads((ROOT/"trials/routing/plan.json").read_text());answers=json.loads((ROOT/"trials/routing/response.json").read_text())
routing={"case_id":"SC-ROUTING","result":"PASS" if all(a["applies"]==p["expected"][a["id"]] for a in answers) and len(answers)==6 else "FAIL","passing":sum(a["applies"]==p["expected"][a["id"]] for a in answers),"required":6,"limitation":"Description-only independent classification; native implicit discovery NOT_RUN."}
dump("trials/routing/primary-review.json",routing)
print(json.dumps({"authoring":[(r["case_id"],r["result"],r["checks"]) for r in results],"routing":routing},indent=2))

