"""Assemble evidence-backed validation records. Does not repair the target."""
import datetime, hashlib, json, pathlib, re, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
PROJECT=ROOT.parents[4]
VAL=PROJECT/".agents/skills/skill-validator/scripts"
sys.path.insert(0,str(VAL))
import observe
RUN=ROOT.name
def read(p):return json.loads((ROOT/p).read_text(encoding="utf-8"))
def write(p,v):
    path=ROOT/p;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("x",encoding="utf-8",newline="\n") as f:
        f.write(v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)+"\n")
def replace(p,v):
    (ROOT/p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def ref(p):return {"path":p,"sha256":hashlib.sha256((ROOT/p).read_bytes()).hexdigest()}
def src(p,sid,anchor):
    text=(ROOT/p).read_text(encoding="utf-8")
    offset=text.index(anchor)
    line=text[:offset].count("\n")+1
    return {**ref(p),"source_id":sid,"locator":{"line_start":line,"line_end":line+anchor.count("\n")}}
helper=read("trials/helpers/case-results.json")
# Retain command-level readback and exact stdout before deriving current state.
d=ROOT/"observations/final-readback";d.mkdir()
argv=[sys.executable,"-B","-X","utf8",str(VAL/"observe.py"),"readback","--source",r"C:\Users\bryan\.codex\skills\.system\skill-creator","--manifest",str(ROOT/"source-manifest.json")]
start=datetime.datetime.now(datetime.timezone.utc).isoformat()
p=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=120)
(d/"stdout.txt").write_bytes(p.stdout);(d/"stderr.txt").write_bytes(p.stderr)
write("observations/final-readback/attempt-001.json",{"argv":argv,"cwd":str(PROJECT),"started_at_utc":start,"ended_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"timeout_seconds":120,"exit_code":p.returncode})
rb=json.loads(p.stdout)
assert p.returncode==0 and rb["status"]=="MATCH"
write("source-after-manifest.json",rb["manifest"])
original_origin=(ROOT/"origin-record.json").read_bytes()
write("inputs/origin-record-before-readback.json",original_origin.decode("utf-8"))
origin=read("origin-record.json");origin["source_readback_state"]="UNCHANGED";replace("origin-record.json",origin)
sources=read("sources.json")
for sid,pth in [("quick-validator","source/scripts/quick_validate.py"),("initializer","source/scripts/init_skill.py"),("ui-generator","source/scripts/generate_openai_yaml.py"),("installed-ui","source/agents/openai.yaml")]:
    sources["sources"].append({"source_id":sid,"url":None,"original_path":str(ROOT/pth),"retrieved_at_utc":start,"sha256":ref(pth)["sha256"],"snapshot_path":pth,"sections":["complete captured source"],"freshness":"live_verified"})
sources["sources"].append({"source_id":"official-build-skills","url":"https://learn.chatgpt.com/docs/build-skills","original_path":None,"retrieved_at_utc":"2026-09-15T12:08:47Z","sha256":ref("inputs/official-web-response.json")["sha256"],"snapshot_path":"inputs/official-web-response.json","sections":["Build skills","Optional metadata","Where Codex loads local skills"],"freshness":"live_verified"})
# Record original selected source list before supplementing supporting observed sources.
write("inputs/sources-initial.json",(ROOT/"sources.json").read_text())
replace("sources.json",sources)
# Primary findings are deduplicated by source location/defect, not number of failed tests.
findings=[]
def finding(short,rule,category,severity,path,sid,anchor,cases,description,impact,correction,preserved):
    fid,identity=observe.finding_identity(rule,path,anchor,0)
    evidence=[ref("trials/helpers/attempts/"+c+"/attempt-after.json") for c in cases]
    if not cases:evidence=[ref("observations/ui-length.json")]
    f={"finding_id":fid,"label":short,"identity":identity,"rule_id":rule,"category":category,"severity":severity,"subject_path":path,"locator":src("source/"+path,sid,anchor)["locator"],"source_refs":[src("source/"+path,sid,anchor)],"observation_refs":evidence,"description":description,"user_impact":impact,"proposed_correction":correction,"preserved_requirements":preserved,"verification_cases":cases or ["UI-LENGTH"],"disposition":"proposed"}
    findings.append(f)
finding("SC-F01","AV-R03","resource_tool_issue","major","scripts/quick_validate.py","quick-validator","if name:",["V08-blank-name","V09-blank-description"],"Blank name and whitespace-only description both return success.","Incomplete discovery metadata is reported valid.","Require nonempty trimmed strings for both required fields before content checks.","Keep valid optional metadata and ordinary completed skills accepted.")
finding("SC-F02","AV-R03","resource_tool_issue","major","scripts/quick_validate.py","quick-validator",'r"[ ]{0,3}\\[TODO:[^\\n]*\\][ \\t]*", line',["V16-scaffold-bullet"],"A standalone unfinished TODO expressed as a Markdown list item returns success.","Unfinished scaffold instructions can be delivered with a passing check.","Recognize standalone list-item scaffold placeholders outside code examples.","Continue accepting literal fenced examples and meaningful prose mentioning TODO.")
finding("SC-F03","AV-R03","resource_tool_issue","major","scripts/quick_validate.py","quick-validator",'match = re.match(r"^---\\n(.*?)\\n---", content, re.DOTALL)',["V17-closing-delimiter"],"Closing marker ---trailing is accepted as a frontmatter delimiter.","Malformed skill frontmatter receives success.","Require a complete delimiter line with supported line ending or EOF.","Preserve CRLF/LF and valid complete frontmatter.")
finding("SC-F04","AV-R03","resource_tool_issue","minor","scripts/quick_validate.py","quick-validator",'unexpected = ", ".join(sorted(unexpected_keys))',["V20-mixed-yaml-keys"],"Mixed numeric and string YAML keys raise uncaught TypeError while sorting.","Malformed input produces a traceback instead of an actionable validation result.","Reject non-string keys explicitly before sorting/reporting.","Remain read-only and retain nonzero rejection of unsupported keys.")
finding("SC-F05","AV-R03","resource_tool_issue","minor","scripts/generate_openai_yaml.py","ui-generator",'def yaml_quote(value):',["G15-carriage-return"],"An accepted internal carriage return is written literally; YAML parsing changes it to a space.","Requested metadata strings can be silently changed.","Serialize supported strings with complete YAML-safe escaping and exact parse round trip.","Preserve caller-provided quotes, backslashes, Unicode and supported whitespace.")
finding("SC-F06","AV-I01","instruction_issue","minor","SKILL.md","skill-contract","- Keep names under 64 characters and prefer short action-oriented names.",["I10-name-64","V11-name-64"],"Prose requires fewer than 64 characters; both helpers accept exactly 64.","Boundary behavior disagrees with the local authoring contract.","Align prose to the existing inclusive 64-character helper boundary after explicit proposed review.","Do not tighten names to 63 or recast local prose as a universal standard.")
finding("SC-F07","AV-R03","resource_tool_issue","minor","scripts/generate_openai_yaml.py","ui-generator",'for key in optional_order:',["G14-invalid-prompt"],"Generator accepts a default_prompt lacking $skill-name, contrary to bundled UI guidance.","Generated optional metadata can violate the package's own output constraint.","When default_prompt is explicitly supplied, validate the required selected skill invocation and reject invalid input before writing.","Do not create an optional prompt when none was requested; do not silently rewrite supplied text.")
finding("SC-F08","AV-F04","instruction_issue","minor","agents/openai.yaml","installed-ui",'short_description: "Create or update a skill"',[],"Bundled short_description has 24 characters; its UI guidance and generator require 25–64.","The package's own UI metadata fails its stated constraint; rendered UI harm was not observed.","Use a meaningful 25–64 character description without changing other metadata.","Preserve display name, both icon paths and current implicit invocation default.")
write("findings.json",{"schema_version":"1","run_id":RUN,"target_name":"skill-creator","findings":findings})
# Every mandatory AV catalog row gets a run-bound adjudication.
checks=[]
def check(cid,rid,subject,dimension,result,reason,evidence,method="semantic",required=True,app="applicable"):
    checks.append({"schema_version":"1","run_id":RUN,"check_id":cid,"rule_id":rid,"subject_path":subject,"method":method,"required":required,"applicability":app,"result":result,"reason":reason,"evidence":[ref(x) for x in evidence],"dimension":dimension})
manual=["semantic-review.md"]
raw=["observations/text-resources/stdout.txt","observations/structure/stdout.txt"]
catalog=[
("AV-F01","standards","PASS","Unique-key required YAML fields and UTF-8 confirmed on actual target.",raw),
("AV-F02","standards","PASS","Original folder name and skill identity agree; snapshot root name is not a defect.",raw+["source-manifest.json"]),
("AV-F03","standards","PASS","Scoped description and independent routing classifications pass; native activation separate.",["trials/routing/primary-review.json"]+manual),
("AV-F04","standards","FAIL","Supported YAML types/icons resolve, but bundled 24-character UI blurb contradicts 25–64 local constraint.",["observations/ui-length.json"]+manual),
("AV-F05","standards","PASS","No unfinished installed instructions or broken fences; helper templates are intentionally unfinished fixtures.",manual+raw),
("AV-U01","standards","PASS","All captured text scanned; no specified Unicode candidates.",raw),
("AV-R01","standards","PASS","Actual link and icon destinations resolve; fenced illustrative paths are not dependencies.",raw+manual),
("AV-R02","workflow","PASS","Every file has a reviewed role, including command-linked helpers and intentional license.",manual),
("AV-R03","workflow","FAIL","Executable helper contract failures independently reproduced and output artifacts reviewed.",["trials/helpers/case-results.json","trials/helpers/helper-report.md"]),
("AV-I01","instructions","FAIL","Local name boundary is inconsistent: under 64 versus inclusive 64.",manual+["trials/helpers/case-results.json"]),
("AV-I02","instructions","PASS","Contextual ceremony review found actionable guidance; no hollow acceptance controls.",manual),
("AV-I03","instructions","PASS","Conditional UI guidance is linked before metadata edits; helpers are explicitly routed.",manual),
("AV-I04","instructions","PASS","Cold creation/update honor selected outputs and preserve policy/dependencies; no redundant approval pause.",["trials/create/primary-review-002.json","trials/update/primary-review-002.json"]),
("AV-C01","instructions","PASS","All text byte/character/line counts recorded; token measurement optional NOT_RUN.",raw),
("AV-S01","instructions","PASS","Static source-to-effect review: no retrieved instructions/network/tool execution; safe YAML loading. Not adversarial prompt-injection certification.",manual),
("AV-S02","workflow","PASS","Inspected local effects and tested preserving existing/invalid targets; no shell/network/credential operations.",manual+["trials/helpers/case-results.json"]),
("AV-W01","workflow","PASS","Creation/update paths executed by separate agents and independently reviewed; limitations disclosed.",["trials/create/primary-review-002.json","trials/update/primary-review-002.json"]),
("AV-W02","workflow","PASS","Existing/partial target reinitialization rejected preserving bytes; update preserves unrelated data. Forced process cancellation not exercised.",["trials/helpers/attempts/I14-partial-retry/attempt-after.json","trials/update/primary-review-002.json"]),
("AV-E01","standards","PASS","Frozen expectations, exact attempts, snapshot/output readback and unchanged original bytes retained; all limitations disclosed.",["trials/helpers/frozen-plan.json","observations/final-readback/stdout.txt","source-manifest.json"])]
for rid,dim,res,reason,ev in catalog:check(rid+"-review",rid,"SKILL.md",dim,res,reason,ev)
for i in range(1,11):
    rid=f"AV-A{i:02}"
    check(rid+"-scope",rid,"SKILL.md","standards","NOT_APPLICABLE","Ordinary system skill; no selected adaptive descriptor, binding, variant or multi-member set contract.",["origin-spec.md"],app="not_applicable")
for c in helper["cases"]:
    case=c["id"];check(case,"SC-HELPERS","scripts/"+c["helper"],"behavior",c["result"] if c["result"]!="INCOMPLETE" else "NOT_RUN",c["expected"]["reason"]+" Observed: "+("; ".join(c["observed"]["errors"]) or "expected outcome and file-effect assertions satisfied."),["trials/helpers/attempts/"+case+"/attempt-before.json","trials/helpers/attempts/"+case+"/attempt-after.json"],method="behavioral")
for case in ("create","update"):
    rr=read("trials/"+case+"/primary-review-002.json")
    check("SC-"+case.upper(),"SC-"+case.upper(),"SKILL.md","behavior",rr["result"],"Independent explicit host task; actual artifacts reviewed and source/sentinel byte preservation confirmed.",["trials/"+case+"/primary-review-002.json","trials/"+case+"/workspace/execution-log.json"],method="behavioral")
routing=read("trials/routing/response.json");expected=read("trials/routing/plan.json")["expected"]
for row in routing:check(row["id"],"SC-ROUTING","SKILL.md","behavior","PASS" if row["applies"]==expected[row["id"]] else "FAIL",row["reason"],["trials/routing/plan.json","trials/routing/response.json"],method="behavioral")
check("NATIVE-DISCOVERY","SC-DISCOVERY","SKILL.md","behavior","NOT_RUN","Native implicit invocation was not exercised; explicit task loading is not discovery.",["trial-plan.md"],method="behavioral",required=False)
write("checks.jsonl","".join(json.dumps(c,ensure_ascii=False)+"\n" for c in checks))
# Workflow rows map instructions, not fictional protected phases.
stages=[
("select","Create or Update a Skill","User asks for authoring or selected edit","User outcome/current skill","Choose relevant workflow and resolve only material unknowns","Selected output location and resource choice",["initialize","edit"],"Ask a concrete material question or identify missing input"),
("initialize","Initialize a New Skill","New output skill selected","Name/path/resource/interface arguments","Optionally invoke initializer","Starter files or retained diagnostic",["edit"],"Existing directory rejected; partial initialization retained"),
("edit","Write the Instructions","Selected new/existing skill inspected","Current bytes and requested behavior","Write focused instructions and required resources; preserve other data","Reviewable completed skill",["validate"],"Preserve partial work and report unresolved input"),
("metadata","UI Metadata and Invocation Policy","UI metadata requested","Current YAML and conditional UI reference","Generate new/interface-only YAML or edit in place when preserving policy/dependencies","Requested fields with unrelated data preserved",["validate"],"Reject invalid arguments; do not retry overwrite blindly"),
("validate","Validate and Iterate","Completed candidate exists","Candidate and helper","Run limited validator, inspect resource/instruction quality and scripts","Executed observations and limitations",["forward","deliver"],"Report failed check; narrow observed correction only if authoring authorized"),
("forward","Independent Forward-Testing","Complexity/risk or explicit requested trial","Minimal prompt, skill snapshot and raw artifacts","Independent bounded disposable task and output review","Retained artifacts and realistic behavior evidence",["deliver"],"Keep errors/timeouts; no fabricated native PASS"),
("deliver","Validate and Iterate","Work and checks have usable outcome","Candidate paths, observations and limits","Return actual artifact location and status","Usable result or concrete limitation",[],"Retain partial result and next unresolved action")]
steps=[]
for ident,anchor,entry,inputs,action,outputs,nxt,failure in stages:
    loc=src("source/SKILL.md","skill-contract",anchor)
    steps.append({"step_id":ident,"entrypoint":loc,"entry_conditions":entry,"inputs":[inputs],"executor":"Codex host; named Python helper when selected","action":action,"outputs":[outputs],"completion_evidence":["trials/create/workspace/execution-log.json","trials/update/workspace/execution-log.json","trials/helpers/case-results.json"],"next":nxt,"failure_route":failure,"terminal_user_outcome":outputs})
write("workflow-map.json",{"schema_version":"1","run_id":RUN,"target_name":"skill-creator","steps":steps})
# A separate supplemental family retains semantic graph dispositions.
rawobs=read("observations/text-resources/stdout.txt")["observations"]
supp=ROOT.parent/(RUN+"-supplemental");supp.mkdir()
nodes=rawobs["resources"]
for n in nodes:
    pth=n["path"]
    n["role"]="license" if pth=="license.txt" else "reference" if pth.startswith("references/") else "template" if pth.startswith("assets/") else "runtime"
    n["reachable"]=pth!="license.txt"
    n["usage"]="intentional_nonruntime" if pth=="license.txt" else "used"
    n["reason"]="Reviewed concrete consumer in semantic-review.md; license intentionally nonruntime."
    n["evidence"]=[{"path":str(ROOT/"semantic-review.md"),"sha256":ref("semantic-review.md")["sha256"]}]
edges=rawobs["edges"]
skill=(ROOT/"source/SKILL.md").read_text()
for script in ("init_skill.py","generate_openai_yaml.py","quick_validate.py"):
    line=skill[:skill.index("scripts/"+script)].count("\n")+1
    edges.append({"source":"SKILL.md","line":line,"target":"scripts/"+script,"kind":"script_call","resolution":"resolved"})
edges.append({"source":"scripts/init_skill.py","line":19,"target":"generate_openai_yaml.py","kind":"script_call","resolution":"resolved"})
sup={"schema_version":"adaptive-observations-v1","run_id":RUN,"target_digest":read("source-manifest.json")["package_digest"],"unicode_candidates":rawobs["unicode_candidates"],"resources":nodes,"edges":edges,"context":rawobs["context"],"bindings":[],"limitations":["No OS-enforced task isolation, token consumption measurement, native implicit invocation or security certification.","Whole package captured; actual role and link adjudication primary-authored, distinct from raw helper output."]}
(supp/"adaptive-observations.json").write_text(json.dumps(sup,ensure_ascii=False,indent=2),encoding="utf-8")
# Required check accounting is separate from case pass rate.
dims={d:observe.reduce_checks([c for c in checks if c["dimension"]==d]) for d in observe.DIMENSIONS}
overall="FAIL" if any(d["outcome"]=="FAIL" for d in dims.values()) else "INCOMPLETE" if any(d["outcome"]=="INCOMPLETE" for d in dims.values()) else "PASS"
allreq=observe.reduce_checks(checks)
assessment={"schema_version":"1","run_id":RUN,"target_name":"skill-creator","assessment_completed":True,"overall_assessment":overall,"dimensions":dims,"package_digest":read("source-manifest.json")["package_digest"],"rule_set_digest":ref("rule-set.json")["sha256"],"required_coverage":allreq,"unknown_applicability":0,"helper_cases":{"pass":42,"fail":9,"total":51},"independent_authoring_cases":{"pass":2,"total":2},"description_classification_cases":{"pass":6,"total":6},"framework_acceptance":"NOT_EVALUATED"}
write("assessment.json",assessment)
write("enforcement-recommendations.md","""# Enforcement recommendations
No new framework hooks, CLI gates or deployment controls are proposed. The observed failures are in local skill guidance and supporting Python utilities. Narrow helper tests and source corrections are sufficient proposed destinations (guidance_only).
Python evidence and this assessment cannot authorize mutations or establish protected framework acceptance. Preserve host permission checks and user-selected scope. No enforcement mechanism was installed or claimed.
""")
binding={p:ref(p)["sha256"] for p in ["source-manifest.json","rule-set.json","inputs/adaptive-validation.md","source/SKILL.md","source/references/openai_yaml.md","trials/helpers/frozen-plan.json"]}
write("inputs/final-input-bindings.json",binding)
write("command-log.md","""# Executed commands and custody
Host: native Windows, PowerShell; Python C:/Program Files/Python310/python.exe 3.10.11, PyYAML 6.0.2. Working root C:/Projects/DevForgeAI on Windows C:; .git absent.
- observe.py snapshot --source C:/Users/bryan/.codex/skills/.system/skill-creator --output this run: exit 0, complete 9 files, no exclusions. Source manifest retains capture time/hashes.
- prepare.py: exit 0; bounded origin search found no matching frontmatter specification. docs/design/specs absent. An earlier rg query named that absent root and exited 2; not a product defect.
- run_observations.py: exit 0. Retained per-command argv/cwd/timestamps/stdout/stderr under observations. structure=0, installed quick_validate=0, adaptive package=2 (snapshot directory identity requires manual binding), initial readback=0.
- trials/helpers/helper_evidence.py freeze and run: separate freeze and execution, 51 cases. Raw stdout.bin/stderr.bin, inputs/outputs and start/end UTC retained per case. Source unchanged.
- Independent create/update subagents: fork_turns=none, no solution/expected results supplied; commands and combined tool outputs retained in workspace/execution-log.json. Task artifacts independently read back. Exact per-command UTC timestamps not exposed; measured shell durations/exits retained.
- review_trials.py: exit 0, but artifact grading initially falsely flagged snapshot drift because Windows Path ordering differed from manifest ordering. Original primary-review.json failures and script preserved.
- review_snapshot_order.py: exit 0, canonical relative-path comparisons confirm identical bytes. primary-review-002.json corrects the reviewer error without rerunning or modifying either product task.
- Description-only independent subagent: 6 responses retained, 6 match predeclared expected labels; no file/tool use. Native implicit discovery remains NOT_RUN.
- synthesize.py: final original target readback exit 0; exact stdout and extracted manifest retained.
Further record-check commands are retained under observations after report assembly. Readback checks evidence integrity only.
""")
print(json.dumps({"assessment":assessment,"findings":[(f["label"],f["severity"],f["description"]) for f in findings]},indent=2))

