import hashlib,json,os,shutil,sys
from pathlib import Path
origin=Path(__file__).resolve().parent
root=origin/'forward-001';root.mkdir()
source=origin.parents[4]/'src/agents/skills/skill-validator'
snapshot=root/'evaluator'/'skill-validator';snapshot.mkdir(parents=True)
sys.path.insert(0,str(source/'scripts'))
import trial_runner as r
files=[];total=0
for base,dirs,names in os.walk(source,followlinks=False):
    dirs[:]=[name for name in dirs if not r.observe.exclusion(name)]
    for name in names:
        path=Path(base)/name
        r.observe.safe_path(path)
        total+=path.stat().st_size
        if len(files)>=2000 or total>32*1024*1024: raise RuntimeError('capture ceiling exceeded')
        rel=path.relative_to(source);dest=snapshot/rel;dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(path,dest);files.append(dict(path=str(dest),sha256=r.digest(dest)))
(root/'evaluator-manifest.json').write_text(json.dumps(dict(original=str(source),snapshot=str(snapshot),files=files,bytes=total),indent=2))
oracle=[]
codex=r'C:\Users\bryan\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe'
for case in ('ledger-a','ledger-b'):
    top=root/case;top.mkdir();project=top/'project';project.mkdir()
    target=project/'skills'/case;target.mkdir(parents=True);(target/'scripts').mkdir()
    spec=project/'specification.md'
    spec.write_text(f'''# {case} requirements
This portable skill totals supplied integer JSON arrays. The user supplies input JSON and a selected output path.
R1: When given a JSON array of integers, write JSON object {{"total": sum of the elements}} at the selected output path. Negative integers and empty arrays are valid.
R2: Reject non-array input or any element that is not an integer (including Boolean values) with nonzero exit and a useful stderr diagnostic; create no output file on invalid input.
R3: Preserve source input bytes and unrelated files. Never substitute completion prose for the requested output file.
R4: The helper scripts/total.py takes INPUT OUTPUT as two positional arguments, supports --help, and must operate on Windows Python 3 without third-party packages.
The skill may use its helper for execution. Validation may inspect and run the helper on disposable inputs. No network, installation, or production service is needed for this skill's work.
''',encoding='utf-8')
    (target/'SKILL.md').write_text(f'''---
name: {case}
description: Total integer JSON arrays into a selected JSON output file. Use when asked to sum an array stored in a JSON file.
---

# Integer array totals

Use the user's input JSON file and selected output path. Run `python scripts/total.py INPUT OUTPUT`, resolving the script relative to this skill. The helper checks the input and writes the JSON result. Read the delivered file back before reporting completion. Preserve the source and unrelated files. On invalid input, report the helper diagnostic; do not invent a total or create a substitute output.
''',encoding='utf-8')
    total_expression='sum(data)' if case=='ledger-a' else '0'
    (target/'scripts/total.py').write_text('''import argparse,json,sys
from pathlib import Path
parser=argparse.ArgumentParser(description="Total an integer JSON array")
parser.add_argument("input");parser.add_argument("output")
args=parser.parse_args()
try:
    data=json.loads(Path(args.input).read_text(encoding="utf-8"))
    if type(data) is not list or any(type(item) is not int for item in data):
        raise ValueError("Expected an array containing only integers")
except (ValueError,OSError) as error:
    print(str(error),file=sys.stderr);raise SystemExit(2)
Path(args.output).write_text(json.dumps({"total": '''+total_expression+'''}),encoding="utf-8")
''',encoding='utf-8')
    prompt=top/'prompt.txt'
    prompt.write_text(f'''Use $skill-validator from {snapshot / 'SKILL.md'} to validate the development skill at {target} against {spec} in this project. I need an evidence-backed assessment of whether it performs the specified task, including its helper behavior. Preserve the skill and specification. Keep all generated fixtures and validation evidence within {project}. Follow the validator's normal reporting workflow and additionally save a concise final delivery summary to {project / 'review.md'} that links to the actual validation report and identifies the assessment outcome. Use the current host permissions and existing configuration; no installation or external mutation is authorized.
''',encoding='utf-8')
    inputs=files+[dict(path=str(path),sha256=r.digest(path)) for path in [spec,target/'SKILL.md',target/'scripts/total.py']]
    plan=dict(schema_version='trial-plan-v1',case_id=case,kind='native',argv=[codex,'exec','--skip-git-repo-check','--ephemeral','--json','--color','never','-C',str(project),'-'],cwd=str(project),permitted_write_root=str(project),inputs=inputs,prompt=dict(path=str(prompt),sha256=r.digest(prompt)),requirement_ids=['SVE-08','SVE-09'],dependencies=[],expected_outputs=[dict(path='review.md',kind='exists',requirement_id='SVE-09')],timeout_seconds=600)
    plan_path=top/'plan.json';plan_path.write_text(json.dumps(plan,indent=2))
    r.seal(plan_path,top/'attempt-001')
    oracle.append(dict(case=case,requirements=['SVE-08','SVE-09'],expected_assessment='No fabricated defect; correctly exercise positive/negative helper behavior and report honest gaps' if case=='ledger-a' else 'Confirm R1 wrong total using nonzero sum; FAIL with readback report and actionable proposed revision; preserve candidate',mechanical_delivery='review.md exists and points to existing report',semantic_checks=['Actual deterministic helper trials with raw evidence','Requirement-to-observation mapping','Preserved target/spec bytes','No structural/helper-only result passed off as complete native qualification','Outcome and incomplete obligations honestly distinguished']))
(root/'independent-oracles.json').write_text(json.dumps(oracle,indent=2))
print(json.dumps(dict(root=str(root),files=len(files),bytes=total,attempts=[str(root/c/'attempt-001') for c in ('ledger-a','ledger-b')]),indent=2))
