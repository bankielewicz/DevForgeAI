import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
VALIDATOR = PROJECT / '.agents/skills/skill-validator'
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def put(path, value):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
def ref(path): return {'path': path, 'sha256': sha(ROOT/path)}
def copy(src, dst):
    path=ROOT/dst
    path.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(src,path)
def command(name, argv):
    folder=ROOT/'observations'/name
    folder.mkdir(parents=True,exist_ok=False)
    started=dt.datetime.now(dt.timezone.utc).isoformat()
    result=subprocess.run(argv,cwd=PROJECT,capture_output=True,timeout=120)
    (folder/'stdout.txt').write_bytes(result.stdout)
    (folder/'stderr.txt').write_bytes(result.stderr)
    put(folder/'receipt.json',dict(command=argv,cwd=str(PROJECT),started_at_utc=started,ended_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),exit_code=result.returncode,timeout_seconds=120))
    print(name,result.returncode)
    return result

if __name__ == '__main__':
    assert PROJECT == Path('C:/Projects/DevForgeAI')
    sources=[]
    selected=[('postmvp','docs/specs/skill-builder-postmvp-spec.md'),('authoring','docs/plan/skill-builder-authoring-enhancement-spec.md'),('adaptive','docs/plan/skill-builder-adaptive-enhancement-spec.md'),('repository','AGENTS.md'),('rust-authority','docs/plan/devforgeai-codex-rust-enforcement-design.md')]
    for ident, path in selected:
        dst='inputs/'+Path(path).name
        copy(PROJECT/path,dst)
        sources.append(dict(source_id=ident,original_path=str(PROJECT/path),retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sha256=sha(ROOT/dst),snapshot_path=dst,sections=['Full selected contract'],freshness='live_verified'))
    for path in ['adaptive-validation.md','rules.md','reporting.md','trials.md','set-trials.md','handoff.md','text-resource-checks.md']:
        copy(VALIDATOR/'references'/path,'guidance/'+path)
    copy(VALIDATOR/'assets/rules-snapshot.json','guidance/rules-fallback.json')
    sources.extend([dict(source_id='av-catalog',original_path=str(VALIDATOR/'references/adaptive-validation.md'),retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sha256=sha(ROOT/'guidance/adaptive-validation.md'),snapshot_path='guidance/adaptive-validation.md',sections=['3.1 Core rule catalog','4.1 Adaptive rules'],freshness='live_verified'),dict(source_id='openai-skills',url='https://learn.chatgpt.com/docs/build-skills',retrieved_at_utc=dt.datetime.now(dt.timezone.utc).isoformat(),sha256=sha(ROOT/'guidance/openai-build-skills.md'),snapshot_path='guidance/openai-build-skills.md',sections=['Best practices','Optional metadata','How ChatGPT and Codex use skills'],freshness='live_verified')])
    put('sources.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',sources=sources))
    rules=[]
    for line in (ROOT/'guidance/adaptive-validation.md').read_text(encoding='utf-8').splitlines():
        if not line.startswith('| AV-'): continue
        _,ident,method,expect,_=line.split('|',4)
        ident=ident.strip()
        na=ident in ['AV-F04','AV-A01','AV-A02','AV-A03','AV-A04','AV-A05','AV-A09','AV-A10']
        rules.append(dict(rule_id=ident,revision='2026-09-12',title=ident,source_refs=[dict(**ref('guidance/adaptive-validation.md'),source_id='av-catalog',locator='3.1 Core rule catalog; 4.1 Adaptive rules')],authority_class='project_policy',applicability='not_applicable' if na else 'applicable',method='semantic' if 'Semantic' in method or 'semantic' in method else 'behavioral' if 'Behavioral' in method else 'deterministic',expected_observation=expect.strip(),required=True,limitation='Standalone ordinary builder; optional UI metadata absent. Adaptive authoring capability is assessed, not an inferred runtime member/set.'))
    text=(ROOT/'inputs/skill-builder-postmvp-spec.md').read_text(encoding='utf-8')
    import re
    for match in re.finditer(r'\*\*(SBP-\d{3}) — (.*?)\*\*',text):
        rules.append(dict(rule_id=match[1],revision='1.0',title=match[2],source_refs=[dict(**ref('inputs/skill-builder-postmvp-spec.md'),source_id='postmvp',locator=match[1])],authority_class='project_policy',applicability='applicable',method='semantic',expected_observation=match[2],required=True,limitation='Full SBPV scenario results separate from static source review.'))
    put('rule-set.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',rules=rules))
    put('origin-record.json',dict(schema_version='1',run_id=ROOT.name,target_name='skill-builder',original_source_root=str(PROJECT/'src/agents/skills/skill-builder'),manifest=ref('source-manifest.json'),specification=ref('inputs/skill-builder-postmvp-spec.md'),origin_kind='existing_spec',history_kind='observed',prior_evidence=None,completeness='complete',uncertainties=['Maintenance delivery inspected separately; no adopted/generated baseline asserted.'],source_readback_state='NOT_RUN',historical_origin='unknown'))
    put('capabilities.json',dict(os=platform.platform(),python=sys.version,python_executable=sys.executable,shell='PowerShell 7',host='Codex desktop primary agent; installed codex-cli cold tasks',git_metadata=False,target_scope='development skill-builder only',effects='Fresh validation run and disposable children only; no production/operational writes, repairs, installation or external messaging.',snapshot_limits={'files':2000,'bytes':33554432},native_budget_seconds=120,retry_policy='No automatic retry; failed attempts retained.'))
    put('campaign-plan.json',dict(required_scenarios=['SBPV-%02d'%i for i in range(1,19)],coverage={'denominator':'All first-party executable Python in captured scripts/*.py plus assets/adaptive-runtime/check_project_binding.py','exclusions':'No first-party exclusions; fixtures and validator harness excluded; named-tokenizer optional.','line_floor':95,'branch':'reported separately','required_platforms':['Windows native','Linux/POSIX path compatibility'],'pass_rate':'passing required cases / all required cases, each counted once; NOT_RUN not passes'},native_cases=['simple transformation with Unicode literal destination','branching file-delivery with success/missing-input/failure-report behavior'],oracles='Independently authored from selected SBP/SBPV requirements before each attempt.',assessment='Read-only development validation, not framework acceptance.'))
    command('structure',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'structure','--source',str(ROOT/'source')])
    checker=Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
    if checker.exists():
        copy(checker,'inputs/quick_validate.py')
        command('installed-checker',[sys.executable,'-B','-X','utf8',str(checker),str(ROOT/'source')])
    command('text-resources',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/adaptive_observe.py'),'package','--source',str(ROOT/'source')])
    command('codex-version',[shutil.which('codex'),'--version'])
    command('codex-help',[shutil.which('codex'),'exec','--help'])
