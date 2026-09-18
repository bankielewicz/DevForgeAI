"""Prepare immutable assessment inputs and cold trial fixtures; evidence only."""
import datetime, hashlib, json, os, pathlib, platform, re, shutil, sys
ROOT = pathlib.Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
VAL = PROJECT / ".agents/skills/skill-validator"
def write(path, data):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    if not isinstance(data,str): data=json.dumps(data,ensure_ascii=False,indent=2)+"\n"
    with p.open("x",encoding="utf-8",newline="\n") as f: f.write(data)
def ref(path):
    p=ROOT/path
    return {"path":path,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
def copy_input(src,name):
    p=ROOT/"inputs"/name;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,p)
for name in ["adaptive-validation.md","rules.md","trials.md","reporting.md","handoff.md","text-resource-checks.md"]:
    copy_input(VAL/"references"/name,name)
copy_input(VAL/"assets/rules-snapshot.json","rules-fallback.json")
copy_input(PROJECT/"AGENTS.md","project-AGENTS.md")
write("inputs/authorization.md","""# Selected request
Assess the installed skill-creator at C:/Users/bryan/.codex/skills/.system/skill-creator.
User requests structure, disposable helper tests, instruction review, and independent creation/update trials with output review.
Validation only. Preserve target bytes. Write only this evidence run and its synthetic trials.
No installation, operational updates, production changes or framework acceptance.
""")
# Exact bounded frontmatter lookup, excluding retained evidence and backup directories.
lookup=[]
base=PROJECT/"docs/plan"
pending=[base]
excluded=("skill-validations","skill-independent-qa","skill-adaptive-implementations","skill-set-validations","source","trials","inputs")
matches=[]
while pending:
    d=pending.pop()
    for p in sorted(d.iterdir()):
        if p.is_symlink() or (p.stat().st_file_attributes & 0x400): continue
        if p.is_dir():
            if p.name in excluded or "backup" in p.name.lower() or p.name=="devforgeai_cli": continue
            pending.append(p)
        elif p.suffix==".md":
            text=p.read_text(encoding="utf-8")
            m=re.match(r"\A---\r?\n(.*?)\r?\n---",text,re.S)
            if m:
                import yaml
                try: data=yaml.safe_load(m[1])
                except yaml.YAMLError: continue
                if isinstance(data,dict) and data.get("skill_name")=="skill-creator": matches.append(str(p))
            lookup.append(str(p.relative_to(PROJECT)))
write("inputs/origin-lookup.json",{"scope":"Markdown frontmatter only; no filename inference","files_considered":lookup,"matches":matches,"second_root_exists":(PROJECT/"docs/design/specs").exists(),"excluded_directory_names":list(excluded),"history":"unknown"})
assert not matches, matches
write("origin-spec.md","""---
id: OBSERVED-SKILL-CREATOR-20260915T120847Z
skill_name: skill-creator
target: codex
status: observed
---
# Observed origin
Current package observed on 2026-09-15; historical origin unknown. Exact restoration uses source/ and source-manifest.json, complete with no exclusions. This is not a generated or adopted baseline.

## Purpose and triggers
Create/update Codex skills when the user asks for reusable skill authoring. Ordinary task execution, installation and independent audits are separate capabilities. Metadata in source/SKILL.md lines 1-6 governs discovery.

## Inputs and defaults
User task, intended name/location, existing package for updates, optional resources and interface fields. Entry instructions choose CODEX_HOME/skills or ~/.codex/skills absent a destination; preserve explicit destinations and current invocation policy. Hosts and current discovery paths may differ and require verification.

## Outputs and schemas
A folder containing UTF-8 SKILL.md with YAML name/description and Markdown instructions; only needed resources. Optional agents/openai.yaml contains interface strings, dependency records and boolean invocation policy. UI guidance is source/references/openai_yaml.md. Python helpers initialize files, generate UI metadata, and perform limited validation.

## Workflow and recovery
Understand the selected outcome and material unknowns; select resources; initialize only a new directory when helpful; author concise instructions; preserve unrelated existing bytes; validate and review observable results; deliver paths and limits. Existing directory initialization is rejected. Generator replaces openai.yaml, so policy/dependency-bearing updates must be edited in place. Retry and partial-work preservation are reviewed against actual helper behavior. Independent forward tests are conditional on complexity, authorization and availability.

## Resources, dependencies and environments
Three Python helpers (init_skill.py imports generate_openai_yaml.py; both and quick_validate.py use standard library and PyYAML). SKILL.md routes metadata changes to references/openai_yaml.md. agents/openai.yaml consumes two icons; license is intentional nonruntime material. Windows Python 3.10.11/PyYAML 6.0.2 available. Other platforms not qualified.

## Effects and boundaries
Write only user-selected skill destinations and disposable trial locations. No installation or external service mutation implied. The assessment retains original system package unchanged.

## Known uncertainty
Observed helper limitations are not approved future requirements. Current source is the baseline; no separate matching project specification was found in the bounded lookup. Native implicit selection and default user-location discovery require distinct runtime evidence.

## Cases and reconstruction
Cover new minimal skill, resource initialization, invalid inputs, existing destination, metadata generation/update, malformed frontmatter/placeholders, and independent create/update tasks. Reconstruct functionally using these inputs and cited source resources; restore exact bytes only from captured source/ and manifest.
""")
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
manifest=json.loads((ROOT/"source-manifest.json").read_text())
write("origin-record.json",{"schema_version":"1","run_id":ROOT.name,"target_name":"skill-creator","original_source_root":manifest["root"],"manifest":ref("source-manifest.json"),"specification":ref("origin-spec.md"),"origin_kind":"reconstructed","history_kind":"observed","prior_evidence":None,"completeness":"complete","uncertainties":["Historical origin unknown; no matching project specification in bounded search."],"source_readback_state":"NOT_RUN","historical_origin":"unknown"})
write("inputs/environment.json",{"os":platform.platform(),"python":sys.version,"executable":sys.executable,"cwd":str(PROJECT),"shell":"PowerShell","filesystem":"Windows-native C:","git_metadata_present":(PROJECT/".git").exists(),"task_runner":"collaboration.spawn_agent; shared workspace; task boundaries not OS-enforced","python_bytecode_disabled":True})
catalog=(ROOT/"inputs/adaptive-validation.md").read_text()
rules=[]
for line in catalog.splitlines():
    m=re.match(r"\| (AV-[A-Z]\d\d) \| (.*?) \| (.*?) \|",line)
    if not m: continue
    rid,method,expected=m.groups()
    rules.append({"rule_id":rid,"revision":"2026-09-12","title":rid,"source_refs":[{**ref("inputs/adaptive-validation.md"),"source_id":"validator-catalog","locator":rid}],"authority_class":"project_policy","applicability":"not_applicable" if rid.startswith("AV-A") else "applicable","method":"behavioral" if rid in ("AV-W02",) else "semantic" if rid.startswith("AV-I") or rid in ("AV-W01","AV-S01") else "deterministic","expected_observation":expected,"required":True,"limitation":"Ordinary system skill; adaptive-only rules not applicable. Local conventions are not universal Codex standards."})
for rid,title,expected in [
("SC-HELPERS","Helper contract","Independent positive and negative cases honor declared formats and write behavior."),
("SC-CREATE","Independent creation","Deliver a focused reusable skill at requested path with correct scope and no unrequested extras."),
("SC-UPDATE","Independent update","Change requested UI fields only, preserve invocation policy, dependencies, assets and instructions."),
("SC-ROUTING","Description routing","Positive authoring prompts match; ordinary task execution and installation do not."),
("SC-DISCOVERY","Native implicit discovery","Record unperformed unless host selection is actually observed.")]:
    rules.append({"rule_id":rid,"revision":"1","title":title,"source_refs":[{**ref("inputs/authorization.md"),"source_id":"user-request","locator":"Selected request"}],"authority_class":"project_policy","applicability":"applicable","method":"behavioral","expected_observation":expected,"required":rid!="SC-DISCOVERY","limitation":"No implicit activation inferred from explicit file loading."})
write("rule-set.json",{"schema_version":"1","run_id":ROOT.name,"target_name":"skill-creator","rules":rules})
sources=[]
for sid,p,sections,fresh in [("validator-catalog","inputs/adaptive-validation.md",["3.1","4.1"],"snapshot_only"),("user-request","inputs/authorization.md",["Selected request"],"live_verified"),("skill-contract","source/SKILL.md",["Core Principles","Create or Update a Skill","Independent Forward-Testing"],"live_verified"),("ui-contract","source/references/openai_yaml.md",["Field descriptions and constraints"],"live_verified")]:
    sources.append({"source_id":sid,"url":None,"original_path":str(ROOT/p),"retrieved_at_utc":now,**{"sha256":ref(p)["sha256"]},"snapshot_path":p,"sections":sections,"freshness":fresh})
write("sources.json",{"schema_version":"1","run_id":ROOT.name,"target_name":"skill-creator","sources":sources})
# Cold cases: evaluator expectations never passed to task agents.
create=ROOT/"trials/create"; update=ROOT/"trials/update"
create.mkdir(parents=True);update.mkdir(parents=True)
write("trials/create/workspace/keep.txt","sentinel: preserve unrelated file\n")
write("trials/update/workspace/draft-note/SKILL.md","""---
name: draft-note
description: Draft a short incident note from user-supplied facts.
metadata:
  owner: synthetic-evaluation
---
# Draft Note
Use only supplied facts. Ask about missing incident times rather than inventing them.
Produce a draft in the conversation; publishing requires a separate request.
""")
write("trials/update/workspace/draft-note/agents/openai.yaml",'''# Existing hand-maintained metadata
interface:
  display_name: "Draft Note"
  short_description: "Draft incident notes from supplied facts"
  icon_small: "./assets/note.svg"
  default_prompt: "Use $draft-note to draft an incident note."
policy:
  allow_implicit_invocation: false
dependencies:
  tools:
    - type: "mcp"
      value: "synthetic-notes"
      description: "Synthetic fixture only; do not connect"
      transport: "streamable_http"
      url: "https://example.invalid/mcp"
''')
write("trials/update/workspace/draft-note/assets/note.svg",'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"><rect width="16" height="16"/></svg>\n')
write("trials/update/workspace/keep.txt","sentinel: preserve sibling\n")
for case in ("create","update"):
    d=ROOT/"trials"/case
    files=[{"path":p.relative_to(d).as_posix(),"bytes":p.stat().st_size,"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted((d/"workspace").rglob("*")) if p.is_file()]
    write("trials/"+case+"/before-manifest.json",files)
    shutil.copytree(ROOT/"source",d/"skill-creator")
    if case=="create":
        prompt=f"""Use $skill-creator at {d/'skill-creator/SKILL.md'} to create a skill named release-note-draft in {d/'workspace/release-note-draft'}.
It should turn user-supplied change notes into a concise release-note draft grouped into Added, Changed, and Fixed, omitting empty groups. Preserve issue identifiers, mark unknown version/date as unspecified, and never invent changes or publish the draft. This is a simple instruction-only workflow; no scripts or extra reference files are needed. Keep ordinary automatic discovery.
All writes must stay under {d/'workspace'}. The skill-creator package is read-only. Do not install anything or use external services. Complete the authoring work and report the result and checks performed."""
        expected=["valid named skill created at selected path","all requested draft behaviors preserved","no scripts/references or unrequested optional UI fields","implicit policy absent or true","keep.txt unchanged","actual validation and honest delivery"]
    else:
        prompt=f"""Use $skill-creator at {d/'skill-creator/SKILL.md'} to update {d/'workspace/draft-note'}.
Change its UI display name to Incident Note and its UI short description to Draft clear incident notes from supplied facts. Preserve everything else, including its existing invocation policy and dependencies. This is an interface-only edit.
All writes must stay under {d/'workspace'}. The skill-creator package is read-only. Do not connect to any service or install anything. Complete the edit and report the result and checks performed."""
        expected=["only requested interface strings changed","policy false preserved","dependency subtree preserved","default_prompt and icon preserved","SKILL.md/icon/sibling byte identical","actual validation and honest delivery"]
    write("trials/"+case+"/prompt.txt",prompt)
    write("trials/"+case+"/plan.json",{"schema_version":"1","case_id":"SC-"+case.upper(),"requirement_ids":["SC-"+case.upper(),"AV-I04","AV-W01","AV-W02"],"fixtures":ref("trials/"+case+"/before-manifest.json"),"skill_snapshot":ref("source-manifest.json"),"expected_outputs_and_effects":expected,"executor":"independent collaboration agent; fork_turns=none","task_prompt":ref("trials/"+case+"/prompt.txt"),"timeout_seconds":600,"timeout_rationale":"Small complete authoring task; bounded host supervision. Local shell commands 120 seconds.","permitted_write_root":str(d/"workspace")})
write("trial-plan.md","""# Declared assessment scope
Required: whole-package structure/text/resource review; all three helpers with positive and negative disposable cases; independent creation and metadata-only update tasks; description-only positive/near-miss classification; source preservation and records integrity.
Adaptive AV-A01..A10: not applicable to this ordinary system skill.
Native implicit discovery: advisory NOT_RUN unless actually observed. Explicit host subagent execution is distinct from CLI implicit activation.
Platforms: native Windows only. Linux/macOS not selected. No runtime coverage percentage promised; evidence harness is not framework implementation.
Helper agent must freeze its case oracle and fixtures before execution, retain each attempt and both stdout/stderr, and use content/file-effect assertions.
Cold task agents receive only prompt and their own raw fixture/snapshot, not expectations.
""")
print(str(ROOT))
print(manifest["package_digest"])

