"""Independent behavioral trial authoring and retained terminal evidence.

All generated skill packages reside in a new disposable TEMP project. This is
trial orchestration, not a builder runtime helper or protected acceptance gate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BUILDER = HERE.parents[2] / 'src/agents/skills/skill-builder'
CHECKER = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
STATE = HERE / 'trial-state.json'
LOG = HERE / 'commands.jsonl'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode('utf-8') if isinstance(data, str) else data)

def dump(path, obj):
    write(path, json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def inv(root):
    return {p.relative_to(root).as_posix(): digest(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}

def manifest(root):
    return {'schema_version': '1', 'root': str(root.resolve()), 'captured_at_utc': datetime.now(timezone.utc).isoformat(), 'files': [{'path': p, 'bytes': (root / p).stat().st_size, 'sha256': h} for p,h in inv(root).items()], 'excluded_boundaries': []}

def run(args, cwd, purpose, expected=0):
    start = datetime.now(timezone.utc).isoformat()
    result = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    row = {'at_utc': start, 'cwd': str(cwd), 'argv': [str(a) for a in args], 'command_windows': subprocess.list2cmdline([str(a) for a in args]), 'purpose': purpose, 'exit_code': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr, 'expected_exit_code': expected}
    with LOG.open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(row) + '\n')
    if result.returncode != expected:
        raise RuntimeError(f'{purpose}: expected exit {expected}, got {result.returncode}: {result.stderr}\n{result.stdout}')
    return row

PY = [sys.executable, '-B', '-X', 'utf8']
SOURCE_SKILL = '''---
name: receipt-summary
description: Summarize receipt CSV files as exact decimal JSON totals by category.
model: sonnet
---

# Receipt summary

On a request to summarize receipts, read a supplied UTF-8 CSV with exactly
`category,amount` columns. Use [scripts/summarize.py](scripts/summarize.py).
Resolve its path relative to the loaded skill. Call Python with the CSV path.
Do not edit the CSV or write a report file; return the script's JSON stdout.
The response has schema_version "1", row_count (integer), total (two decimal
string), and categories (alphabetically sorted object of two decimal strings).
Amounts are nonnegative base-10 numbers with at most two fractional digits;
reject missing categories, invalid amounts, nonfinite values, and malformed
columns with exit 2 and no stdout. Empty CSV with a valid header returns zeros.
This capability does not recommend purchases, initiate payments, or install tools.
'''
TARGET_SKILL = '''---
name: receipt-summary
description: Summarize a supplied receipt CSV as exact decimal JSON totals by category.
---

# Receipt summary

Use [scripts/summarize.py](scripts/summarize.py) for receipt aggregation.
Resolve the script relative to this loaded skill and the supplied CSV relative to
the identified project root. Execute `python -B -X utf8 <script> <csv>`.

Require UTF-8 CSV with exactly `category,amount` columns. Amounts are nonnegative
base-10 numbers with at most two fractional digits. The script rejects invalid,
nonfinite or missing amounts, blank categories, and malformed columns with exit
2 and no stdout. A valid header with no rows produces zero totals.

Return its JSON stdout unchanged: schema_version "1", row_count integer, total
as a two decimal string, and categories as an alphabetically sorted object of
two decimal strings. Do not edit the CSV or create report files. Do not initiate
payments, recommend purchases, or install tools.
'''
SCRIPT = '''"""Aggregate receipt amounts using exact decimal arithmetic."""
import csv
from decimal import Decimal
import json
from pathlib import Path
import re
import sys

def summarize(path):
    categories = {}
    count = 0
    with Path(path).open(encoding="utf-8", newline="") as stream:
        rows = csv.DictReader(stream)
        if rows.fieldnames != ["category", "amount"]:
            raise ValueError("expected exactly category,amount columns")
        for row in rows:
            category = (row.get("category") or "").strip()
            amount = row.get("amount") or ""
            if None in row or not category or not re.fullmatch(r"[0-9]+(?:\\.[0-9]{1,2})?", amount):
                raise ValueError("invalid category or amount")
            # Integer cents avoid Decimal context precision limits on long inputs.
            whole, _, fraction = amount.partition(".")
            cents = int(whole) * 100 + int(fraction.ljust(2, "0") or "0")
            categories[category] = categories.get(category, 0) + cents
            count += 1
    def money(cents):
        return str(cents // 100) + "." + str(cents % 100).zfill(2)
    return {"schema_version": "1", "row_count": count, "total": money(sum(categories.values())), "categories": {key: money(categories[key]) for key in sorted(categories)}}

def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError("usage: summarize.py CSV")
        result = summarize(sys.argv[1])
    except (OSError, UnicodeError, ValueError, csv.Error) as exc:
        print(str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
'''
SPEC = '''---
skill_name: receipt-summary-spec
status: approved-for-this-disposable-trial
---

# Receipt summarizer development specification

R1. Build the receipt-summary-spec Codex skill. Activate when the user requests
receipt CSV aggregation. Exclude payment initiation, recommendations, installation,
and unrelated edits. No workers or external dependencies are required.

R2. Accept one UTF-8 CSV path relative to the identified project root. Require
exactly category,amount header columns. Require a nonempty trimmed category and
a nonnegative base-10 amount with at most two fractional digits. Reject invalid,
nonfinite or missing amounts and malformed columns with exit 2 and no stdout.

R3. Implement scripts/summarize.py using exact decimal aggregation; no float
rounding. Return JSON stdout with exactly schema_version "1", row_count integer,
total two decimal string, and categories alphabetically sorted object mapping
names to two decimal strings. A header-only CSV produces zero totals.

R4. SKILL.md must route to the script relative to the loaded skill. Use existing
Python standard library only. Do not edit input files, write report files, call
services, install software, or initiate payments. Retrying corrected CSV is safe
because errors produce no output artifacts. Preserve these limits in instructions.
'''

def exercise(project, skill, evidence, run_id, target):
    fixture = evidence / 'task-inputs'
    fixture.mkdir(exist_ok=True)
    valid = fixture / 'receipts.csv'
    write(valid, 'category,amount\ntravel,0.10\nfood,12.34\ntravel,0.20\nfood,0.66\n')
    empty = fixture / 'empty.csv'
    write(empty, 'category,amount\n')
    original = inv(fixture)
    commands = [run(PY + [CHECKER, skill], project, 'Skill Creator structural check')]
    output = run(PY + [skill / 'scripts/summarize.py', valid], project, 'Execute decimal totals and JSON contract')
    commands.append(output)
    actual = json.loads(output['stdout'])
    expected = {'schema_version':'1','row_count':4,'total':'13.30','categories':{'food':'13.00','travel':'0.30'}}
    assert actual == expected and list(actual['categories']) == ['food','travel']
    output = run(PY + [skill / 'scripts/summarize.py', empty], project, 'Execute header-only recovery contract')
    commands.append(output)
    assert json.loads(output['stdout']) == {'schema_version':'1','row_count':0,'total':'0.00','categories':{}}
    for label, data in [('nonfinite','category,amount\nfood,NaN\n'),('missing','category,amount\nfood,\n'),('precision','category,amount\nfood,1.234\n'),('columns','category,amount\nfood,1.00,extra\n'),('blank','category,amount\n ,1.00\n')]:
        path = fixture / (label + '.csv')
        write(path, data)
        original[path.name] = digest(path.read_bytes())
        output = run(PY + [skill / 'scripts/summarize.py', path], project, 'Reject ' + label + ' CSV without JSON output', 2)
        commands.append(output)
        assert not output['stdout'] and output['stderr']
    assert inv(fixture) == original
    observation = {'schema_version':'1','run_id':run_id,'target_name':target,'outputs':[{'path':p,'sha256':h} for p,h in inv(skill).items()], 'commands':commands, 'assertions':{'exact_decimal_total':'13.30','travel_decimal_total':'0.30','header_only':'0.00','rejections':5,'input_preservation':True}}
    dump(evidence / 'checks.json', observation)
    return observation

def build_contract(snapshot, originals, mode, target, request):
    inputs=[]
    requirements=[]
    paths=['SKILL.md','scripts/summarize.py']
    for index,(source,relative) in enumerate(originals):
        data=source.read_bytes()
        write(snapshot / relative,data)
        ident=f'input-{index+1}'
        inputs.append({'id':ident,'path':relative,'resolved_path':str(source.resolve()),'role':'source' if mode=='import' else 'spec','bytes':len(data),'sha256':digest(data)})
        requirements.append({'id':f'req-{index+1:04d}','origin':'source','text':'Preserve the input capability, activation, complete decimal CSV and JSON contract, side effects and error recovery described in this input.','source_refs':[{'input_id':ident,'start_byte':0,'end_byte':len(data),'sha256':digest(data)}],'artifact_paths':paths,'verification':[{'method':'Execute valid/empty/malformed CSV tasks and manually inspect full generated instructions and script','expected':'Exact decimal totals, strict schema/error behavior, no input mutation, resources resolve and permissions unchanged'}]})
    obj={'schema_version':'1','mode':mode,'target_name':target,'inputs':inputs,'authorization':{'instruction':request,'inputs':[{'id':row['id'],'sha256':row['sha256']} for row in inputs]},'purpose':'Produce exact receipt CSV aggregation as JSON without mutating input or invoking services.','activation':{'positive':['Summarize this receipt CSV'],'excluded':['payment initiation','purchase recommendations','installation','unrelated edits']},'requirements':requirements,'artifacts':[{'path':p,'role':'entrypoint' if p=='SKILL.md' else 'script','requirement_ids':[r['id'] for r in requirements],'purpose':'Route safe receipt task' if p=='SKILL.md' else 'Execute exact decimal CSV to JSON aggregation'} for p in paths],'workers':[],'dependencies':[]}
    dump(snapshot/'evidence/build-contract.json',obj)
    return obj

def provenance(snapshot, run_id, target, mode, prior=None, complete=False):
    contract=json.loads((snapshot/'evidence/build-contract.json').read_text())
    baseline=inv(snapshot/'baseline')
    outputs=[]
    for path,h in inv(snapshot/'destination').items():
        owned=path in baseline
        outputs.append({'path':path,'sha256':h,'ownership':'generated' if owned else 'retained_user','baseline_path':'baseline/'+path if owned else None,'baseline_sha256':baseline.get(path)})
    obj={'schema_version':'1','run_id':run_id,'mode':mode,'target_name':target,'builder_manifest_sha256':digest((BUILDER/'evals/build-manifest.json').read_bytes()),'contract_sha256':digest((snapshot/'evidence/build-contract.json').read_bytes()),'inputs':[{'id':r['id'],'sha256':r['sha256']} for r in contract['inputs']],'dependencies':[],'outputs':outputs,'mappings':[{'requirement_id':r['id'],'artifact_paths':r['artifact_paths'],'evidence_ids':['checks']} for r in contract['requirements']],'evidence':[{'id':'checks','path':'evidence/checks.json','sha256':digest((snapshot/'evidence/checks.json').read_bytes())}],'prior_build':prior,'result':'COMPLETE' if complete else 'INCOMPLETE'}
    dump(snapshot/'evidence/build-provenance.json',obj)
    return obj

def cases(runroot, imported=False, revision=False):
    rows=[{'case_id':'task-package-links','grader_id':'package_links','params':{'path':'destination'},'expected':'PASS'},{'case_id':'task-traceability','grader_id':'build_traceability','params':{'evidence':'evidence','destination':'destination'},'expected':'PASS'}]
    if imported:
        rows.append({'case_id':'task-import-accounting','grader_id':'manifest_accounting','params':{'source':'source','destination':'destination','evidence':'evidence'},'expected':'PASS'})
    if revision:
        rows.append({'case_id':'task-revision','grader_id':'revision_consistency','params':{'path':'evidence/revision-plan.json'},'expected':'PASS'})
    write(runroot/'evaluation-cases.jsonl',''.join(json.dumps(row)+'\n' for row in rows))

def evaluate(project, runroot, profile, suffix):
    # Preserve each exact evaluator input before later provenance/readback edits.
    bounded=runroot/'evaluation-snapshots'/suffix
    shutil.copytree(runroot/'snapshot',bounded)
    archived_cases=runroot/('evaluation-cases-'+suffix+'.jsonl')
    write(archived_cases,(runroot/'evaluation-cases.jsonl').read_bytes())
    return run(PY+[BUILDER/'scripts/run_evaluation.py','--package-root',BUILDER,'--candidate-root',bounded,'--cases',archived_cases,'--output',runroot/(suffix+'.jsonl'),'--run-id',runroot.name+'-'+suffix,'--profile',profile], project, 'Evaluate '+profile+' '+suffix)

def prepare():
    if STATE.exists():
        raise RuntimeError('trial-state already exists; retain it and choose a new directory for new trials')
    project=Path(tempfile.mkdtemp(prefix='skill-builder-forward-independent-'))
    source=project/'raw/claude-receipt-summary'
    write(source/'SKILL.md',SOURCE_SKILL)
    write(source/'scripts/summarize.py',SCRIPT)
    spec=project/'docs/plan/receipt-summary-spec.md'
    write(spec,SPEC)
    dump(STATE,{'project':str(project),'phase':'prepared','created_at':datetime.now(timezone.utc).isoformat()})
    write(HERE/'raw-task-prompts.md','# Independent requests\n\nThe evaluating agent received the builder and synthetic-task request, without an intended answer or suspected defect.\n\n1. Import the synthetic Claude receipt-summary package into the disposable project. Preserve its JSON contract and decimal CSV aggregation behavior; run the generated script and required checks.\n\n2. Build receipt-summary-spec from the reviewed Markdown specification in the disposable project. Execute the result and preserve requirement and output traceability.\n\n3. Revise receipt-summary-spec after an owned user edit while retaining an unrelated user file. First request a competing instruction revision, retain conflict evidence, then explicitly resolve the conflict by preserving the edited entrypoint and putting the additional approved clarification in the script. Recompute against the last successful baseline and apply only the resulting proposal.\n')
    commands=[run(PY+['--version'],project,'Identify Python'), run(['codex','--version'],project,'Identify available Codex CLI')]
    dump(HERE/'host.json',{'at_utc':datetime.now(timezone.utc).isoformat(),'platform':platform.platform(),'shell':'PowerShell invoking Python subprocess argv; no shell expansion','cli_identification':commands,'capabilities':{'terminal':True,'python_standard_library':True,'worker_independence':'separate delegated agent; no model profile claimed'},'qualification':'NOT_PERFORMED'})
    for mode,target in [('import','receipt-summary'),('spec_build','receipt-summary-spec')]:
        root=project/('docs/plan/skill-imports' if mode=='import' else 'docs/plan/skill-builds')/target/'initial'
        snapshot=root/'snapshot'
        (snapshot/'evidence').mkdir(parents=True)
        originals=[(source/'SKILL.md','source/SKILL.md'),(source/'scripts/summarize.py','source/scripts/summarize.py')] if mode=='import' else [(spec,'inputs/specification.md')]
        request=('Import '+str(source) if mode=='import' else 'Build from reviewed '+str(spec))+' into this disposable project and execute required checks.'
        build_contract(snapshot,originals,mode,target,request)
        candidate=snapshot/'destination'
        write(candidate/'SKILL.md',TARGET_SKILL.replace('name: receipt-summary\n','name: '+target+'\n'))
        write(candidate/'scripts/summarize.py',SCRIPT)
        shutil.copytree(candidate,snapshot/'baseline')
        exercise(project,candidate,snapshot/'evidence','initial',target)
        for original,relative in originals:
            assert original.read_bytes()==(snapshot/relative).read_bytes()
        if mode=='import':
            dump(snapshot/'evidence/source-manifest.json',manifest(source))
            dump(snapshot/'evidence/source-after-manifest.json',manifest(source))
            dump(snapshot/'evidence/destination-manifest.json',manifest(candidate))
            dump(snapshot/'evidence/file-dispositions.json',{'schema_version':'1','files':[{'source_path':p,'source_sha256':h,'role':'entrypoint' if p=='SKILL.md' else 'supporting script','disposition':'REWRITE' if p=='SKILL.md' else 'PRESERVE','target_paths':[p],'rationale':'Remove source-host model override; preserve task permissions and output interface.' if p=='SKILL.md' else 'Standard-library Python is host-neutral and executable unchanged.','behavior_preserved_or_changed':'Decimal CSV and JSON contract retained.','dependencies':[],'planned_verification':'Execute script valid/invalid fixtures and inspect output','performed_review':'checks.json records actual runs; full entrypoint and script reviewed.'} for p,h in inv(source).items()]})
        provenance(snapshot,'initial',target,mode)
        cases(root,mode=='import')
        write(root/'semantic-review.md','Manually read source/specification and generated SKILL.md/script. Exact JSON fields, decimals, errors, source-relative script route and project-relative input resolution are retained. Source model override removed from imported entrypoint; source Python preserved byte-for-byte. No external capabilities, profiles, installations, workers or output report files are introduced.\n')
    print(json.dumps({'project':str(project),'phase':'prepared','next':'Wait for builder manifest stability before final evaluations and regeneration.'}))

def finish_initial(project,target,mode):
    root=project/('docs/plan/skill-imports' if mode=='import' else 'docs/plan/skill-builds')/target/'initial'
    snapshot=root/'snapshot'
    contract=json.loads((snapshot/'evidence/build-contract.json').read_text())
    input_readback=[]
    for row in contract['inputs']:
        data=Path(row['resolved_path']).read_bytes()
        assert len(data)==row['bytes'] and digest(data)==row['sha256']
        input_readback.append({'path':row['resolved_path'],'sha256':digest(data),'matches_contract':True})
    dump(root/'input-readback.json',{'at_utc':datetime.now(timezone.utc).isoformat(),'inputs':input_readback})
    provenance(snapshot,'initial',target,mode)
    profile='import-v2' if mode=='import' else 'spec-v1'
    evaluate(project,root,profile,'candidate-evaluation')
    destination=project/'src/agents/skills'/target
    if destination.exists():
        raise RuntimeError('destination collision')
    shutil.copytree(snapshot/'destination',destination)
    exercise(project,destination,snapshot/'evidence','initial',target)
    assert inv(destination)==inv(snapshot/'destination')
    provenance(snapshot,'initial',target,mode)
    evaluate(project,root,profile,'delivered-evaluation')
    provenance(snapshot,'initial',target,mode,complete=True)
    evaluate(project,root,profile,'completed-evaluation')
    dump(root/'active-baseline.json',{'run_id':'initial','baseline':[{'path':p,'sha256':h} for p,h in inv(snapshot/'baseline').items()]})
    write(root/('conversion-report.md' if mode=='import' else 'build-report.md'),'# '+target+' independent forward trial\n\nAuthoring COMPLETE. Skill Creator structural PASSED. Deterministic '+profile+' PASSED in candidate, delivered, and completed evaluations. Supporting-script and behavioral checks PASSED: exact totals, JSON fields, header-only input, five rejection paths and unchanged task inputs. Manual semantic review: semantic-review.md. Original selected inputs were rehashed against snapshots before candidate completion. Delivery was new and absent before copy, then byte-equal readback completed before active-baseline publication. Outputs: snapshot/destination; generated baseline: snapshot/baseline; contract, provenance and actual command observations: snapshot/evidence. Exact terminal argv, cwd, stdout, stderr and status are retained in the outer commands.jsonl. Framework enforcement NOT_IMPLEMENTED; Rust qualification NOT_PERFORMED; operational installation NOT_PERFORMED; native implicit activation NOT_PERFORMED.\n')
    return root

def revision(project, priorroot):
    target='receipt-summary-spec'
    destination=project/'src/agents/skills'/target
    edited=destination/'SKILL.md'
    write(edited,edited.read_text(encoding='utf-8')+'\nUser note: report totals only; keep finance review outside this skill.\n')
    write(destination/'personal-note.txt','USER OWNED: September bookkeeping notes. Preserve this unrelated file exactly.\n')
    user_before=inv(destination)
    parent=priorroot.parent
    spec=project/'docs/plan/receipt-summary-spec.md'
    initial_baseline=priorroot/'snapshot/baseline'
    prior_bytes=(priorroot/'snapshot/evidence/build-provenance.json').read_bytes()
    old_pointer=(priorroot/'active-baseline.json').read_bytes()

    def setup(name,resolved):
        root=parent/name
        snap=root/'snapshot'
        (snap/'evidence').mkdir(parents=True)
        instruction='Revise the generated script docstring to clarify that sums use exact integer cents; preserve the user-edited SKILL.md and unrelated personal-note.txt. This explicitly resolves the preceding entrypoint conflict by withdrawing the competing generated entrypoint change.' if resolved else 'Revise SKILL.md to clarify that the script aggregates exact integer cents, while retaining all current user edits and the unrelated personal-note.txt.'
        revision_input=root/'revision-request.md'
        write(revision_input,instruction+'\n')
        build_contract(snap,[(spec,'inputs/specification.md'),(revision_input,'inputs/revision-request.md')],'spec_build',target,instruction)
        for label,folder in [('B',initial_baseline),('C',destination),('N',initial_baseline),('after',destination),('destination',destination)]:
            shutil.copytree(folder,snap/label)
        if resolved:
            script=snap/'N/scripts/summarize.py'
            write(script,script.read_text(encoding='utf-8').replace('exact decimal arithmetic.','exact integer-cent arithmetic, avoiding binary float rounding.'))
        else:
            entry=snap/'N/SKILL.md'
            write(entry,entry.read_text(encoding='utf-8')+'\nImplementation clarification: the script aggregates exact integer cents.\n')
        shutil.copytree(snap/'N',snap/'baseline')
        write(snap/'evidence/prior-provenance.json',prior_bytes)
        projection={'run_id':'initial','result':'COMPLETE','baseline':[{'path':p,'sha256':h} for p,h in inv(snap/'B').items()],'provenance':{'path':'evidence/prior-provenance.json','sha256':digest(prior_bytes)}}
        dump(snap/'evidence/prior-projection.json',projection)
        write(snap/'evidence/baseline-before.json',old_pointer)
        write(snap/'evidence/baseline-after.json',old_pointer)
        request={'schema_version':'1','run_id':name,'baseline':'B','current':'C','candidate':'N','after':'after','required_paths':['SKILL.md','scripts/summarize.py'],'owned_paths':sorted(inv(snap/'B')),'prior_build':{'path':'evidence/prior-projection.json','sha256':digest((snap/'evidence/prior-projection.json').read_bytes())},'baseline_before':{'path':'evidence/baseline-before.json','sha256':digest(old_pointer)},'baseline_after':{'path':'evidence/baseline-after.json','sha256':digest(old_pointer)}}
        dump(snap/'evidence/revision-request.json',request)
        command=run(PY+[BUILDER/'scripts/build_evidence.py','revision-plan','--snapshot-root',snap,'--request','evidence/revision-request.json'],project,'Compute '+name+' B/C/N proposal',0 if resolved else 1)
        plan=json.loads(command['stdout'])
        dump(snap/'evidence/revision-plan.json',plan)
        # Candidate N is exercised and evaluated separately from the current
        # destination snapshot; a preview must not confuse those byte sets.
        assessment=root/'candidate-assessment'
        candidate_snap=assessment/'snapshot'
        for label in ['B','C','N','after','baseline','inputs','evidence']:
            shutil.copytree(snap/label,candidate_snap/label)
        shutil.copytree(snap/'N',candidate_snap/'destination')
        exercise(project,candidate_snap/'destination',candidate_snap/'evidence',name,target)
        provenance(candidate_snap,name,target,'spec_build',prior={'path':'evidence/prior-provenance.json','sha256':digest(prior_bytes)})
        cases(assessment,revision=True)
        evaluate(project,assessment,'revision-spec-v1','candidate-evaluation')
        exercise(project,snap/'destination',snap/'evidence',name,target)
        provenance(snap,name,target,'spec_build',prior={'path':'evidence/prior-provenance.json','sha256':digest(prior_bytes)})
        cases(root,revision=True)
        evaluate(project,root,'revision-spec-v1','preview-evaluation')
        return root,snap,plan

    root,snap,plan=setup('conflict',False)
    assert plan['status']=='CONFLICT' and inv(destination)==user_before
    assert (priorroot/'active-baseline.json').read_bytes()==old_pointer
    write(root/'conflict-report.md','Conflict observed in owned SKILL.md. No destination mutations occurred. Current destination and active-baseline bytes are unchanged. Candidate and result retained. The next trial resolves this conflict through a distinct recorded instruction, withdrawing the competing entrypoint proposal and changing only a generated script clarification.\n')
    root,snap,plan=setup('resolved-retry',True)
    assert plan['status']=='PLANNED'
    rechecks=[]
    assert inv(destination)==inv(snap/'C')
    rechecks.append({'at_utc':datetime.now(timezone.utc).isoformat(),'phase':'before_first_mutation','destination':inv(destination),'matches_C':True})
    applied=[]
    for row in plan['rows']:
        if row['action']!='USE_NEW' or row['c_sha256']==row['n_sha256']:
            continue
        path=destination/row['path']
        assert path.resolve().is_relative_to(destination.resolve())
        assert not path.is_symlink() and (digest(path.read_bytes()) if path.exists() else None)==row['c_sha256']
        rechecks.append({'at_utc':datetime.now(timezone.utc).isoformat(),'phase':'immediately_before_mutation','path':row['path'],'current_sha256':row['c_sha256'],'matches_C':True})
        if row['n_sha256'] is None:
            raise RuntimeError('this trial does not require deletions')
        write(path,(snap/'N'/row['path']).read_bytes())
        applied.append(row['path'])
    for path in inv(destination):
        write(snap/'after'/path,(destination/path).read_bytes())
        write(snap/'destination'/path,(destination/path).read_bytes())
    assert (destination/'personal-note.txt').read_bytes()==(snap/'C/personal-note.txt').read_bytes()
    assert (destination/'SKILL.md').read_bytes()==(snap/'C/SKILL.md').read_bytes()
    assert applied==['scripts/summarize.py']
    dump(root/'mutation-log.json',{'rechecks':rechecks,'applied_paths':applied,'after':inv(destination),'readback_equal':inv(destination)==inv(snap/'after'),'unrelated_file_retained':True,'edited_entrypoint_retained':True,'authorization':'snapshot/inputs/revision-request.md'})
    exercise(project,destination,snap/'evidence','resolved-retry',target)
    # Run the delivered task's non-revision graders before claiming evaluation
    # success in the APPLIED observation, then evaluate the full revision profile.
    provenance(snap,'resolved-retry',target,'spec_build',prior={'path':'evidence/prior-provenance.json','sha256':digest(prior_bytes)})
    full_cases=(root/'evaluation-cases.jsonl').read_bytes()
    cases(root)
    evaluate(project,root,'spec-v1','delivered-task-evaluation')
    write(root/'evaluation-cases.jsonl',full_cases)
    plan.update(status='APPLIED',applied_paths=applied,readback_passed=True,evaluation_passed=True)
    dump(snap/'evidence/revision-plan.json',plan)
    evaluate(project,root,'revision-spec-v1','applied-evaluation')
    pointer={'run_id':'resolved-retry','baseline':[{'path':p,'sha256':h} for p,h in inv(snap/'N').items()]}
    dump(root/'active-baseline.json',pointer)
    pointer_bytes=(root/'active-baseline.json').read_bytes()
    write(snap/'evidence/baseline-after.json',pointer_bytes)
    plan.update(baseline_advanced=True,baseline_after={'path':'evidence/baseline-after.json','sha256':digest(pointer_bytes)})
    dump(snap/'evidence/revision-plan.json',plan)
    provenance(snap,'resolved-retry',target,'spec_build',prior={'path':'evidence/prior-provenance.json','sha256':digest(prior_bytes)},complete=True)
    evaluate(project,root,'revision-spec-v1','published-evaluation')
    write(root/'build-report.md','# Independent regeneration trial\n\nAuthoring COMPLETE after an actual retained CONFLICT and distinct explicit resolution. Conflict left destination and baseline unchanged. Retry used the original last-successful B, retained the edited SKILL.md through N=B, retained personal-note.txt as retained_user, and changed only scripts/summarize.py after package and per-path rechecks. Mutation-log.json captures actual delta/readback. Structural and script checks PASSED; exact decimals, JSON schema, five invalid-input cases and input preservation were executed. Deterministic revision-spec-v1 preview/applied/published observations PASSED; delivered task spec-v1 PASSED before evaluation success was set. Development baseline advanced only after successful delivered evaluation and readback. Generated N remains distinct from delivered edited SKILL.md. Framework enforcement NOT_IMPLEMENTED, Rust qualification NOT_PERFORMED, operational installation NOT_PERFORMED, native implicit activation NOT_PERFORMED.\n')

def finalize():
    state=json.loads(STATE.read_text())
    if state['phase']!='prepared':
        raise RuntimeError('finalization not repeatable; retain runs and use separate retry evidence')
    project=Path(state['project'])
    finish_initial(project,'receipt-summary','import')
    prior=finish_initial(project,'receipt-summary-spec','spec_build')
    revision(project,prior)
    shutil.copytree(project,HERE/'retained-project')
    dump(HERE/'retained-project-manifest.json',manifest(HERE/'retained-project'))
    state.update(phase='complete',completed_at=datetime.now(timezone.utc).isoformat(),builder_manifest_sha256=digest((BUILDER/'evals/build-manifest.json').read_bytes()))
    dump(STATE,state)
    print(json.dumps(state))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['prepare','finalize'])
    args=parser.parse_args()
    (prepare if args.phase=='prepare' else finalize)()
