import datetime, hashlib, json, os, platform, re, shutil, stat, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT = Path('C:/Projects/DevForgeAI')
def digest(data): return hashlib.sha256(data).hexdigest()
def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
def inventory(root):
    rows, excluded = [], []
    def walk(folder):
        for p in sorted(folder.iterdir()):
            rel = p.relative_to(root).as_posix()
            s = p.lstat()
            if p.is_symlink() or getattr(s, 'st_file_attributes', 0) & 1024:
                excluded.append({'path':rel,'kind':'link','reason':'no following links'}); continue
            if p.is_dir():
                if 'backup' in p.name.lower() or p.name in ('devforgeai_cli', '.git', '__pycache__'):
                    excluded.append({'path':rel,'kind':'directory','reason':'excluded boundary'}); continue
                walk(p)
            elif stat.S_ISREG(s.st_mode):
                if len(rows)>=2000 or sum(r['bytes'] for r in rows)+s.st_size>32*1024*1024: raise ValueError('inventory ceiling')
                b=p.read_bytes(); rows.append({'path':rel,'bytes':len(b),'sha256':digest(b)})
            else: raise ValueError('special file '+str(p))
    walk(root)
    rows.sort(key=lambda r:r['path'])
    return {'schema_version':'1','root':str(root.resolve()),'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':rows,'excluded_boundaries':excluded}

if __name__ == '__main__':
    assert not (PROJECT/'src/agents/skills/skill-validator').exists()
    assert not (ROOT/'build-contract.json').exists()
    spec=PROJECT/'docs/plan/skill-validator-spec.md'; raw=spec.read_bytes()
    inp=ROOT/'inputs/skill-validator-spec.md'; inp.parent.mkdir(exist_ok=True); inp.write_bytes(raw)
    auth='User explicitly requests skill-validator generation from docs/plan/skill-validator-spec.md to src/agents/skills/skill-validator, authorizes required disposable trials and independent held-out task/routing agents; preserves old specification, evidence, operational copies and existing project skills; after successful build separately assess skill-builder without mutation, adoption or invoking builder.'
    (ROOT/'inputs/authorization.txt').write_text(auth+'\n',encoding='utf-8')
    paths={
      'SKILL.md':list(range(1,15)),
      'references/origin.md':[1,2,14], 'references/rules.md':[3,4,5,6,7,13],
      'references/trials.md':[8,14], 'references/reporting.md':[9], 'references/handoff.md':[10,11],
      'assets/origin-spec-template.md':[1], 'assets/revision-spec-template.md':[10],
      'assets/validation-report-template.md':[7,9], 'assets/enforcement-register-template.md':[7,9],
      'assets/rules-snapshot.json':[3], 'scripts/observe.py':[2,4,9,11],
      'tests/test_observe.py':[2,4,9,11,14], 'evals/cases.jsonl':list(range(1,15)),
      'evals/README.md':[8,12,13,14]}
    artifacts=[{'path':p,'role':('entrypoint' if p=='SKILL.md' else p.split('/')[0]),'requirement_ids':[f'SV-{i:03d}' for i in ids],'purpose':p} for p,ids in paths.items()]
    reqs=[]
    for m in re.finditer(rb'^\| (SV-\d{3}) \| (.*?) \| (.*?) \|\r?$',raw,re.M):
        ident=m[1].decode(); reqs.append({'id':ident,'origin':'source','text':m[2].decode(),'source_refs':[{'input_id':'approved-spec','start_byte':m.start(),'end_byte':m.end(),'sha256':digest(raw[m.start():m.end()])}], 'artifact_paths':[a['path'] for a in artifacts if ident in a['requirement_ids']], 'verification':[{'method':m[3].decode(),'expected':'Specified observation retained in V01-V20 trials; inspect full source sections for complete behavior.'}]})
    assert len(reqs)==14
    inputs=[]
    for ident,p,original,role in [('approved-spec',inp,spec,'spec'),('current-authorization',ROOT/'inputs/authorization.txt',ROOT/'inputs/authorization.txt','clarification')]:
        b=p.read_bytes(); inputs.append({'id':ident,'path':p.relative_to(ROOT).as_posix(),'resolved_path':str(original.resolve()),'role':role,'bytes':len(b),'sha256':digest(b)})
    contract={'schema_version':'1','mode':'spec_build','target_name':'skill-validator','inputs':inputs,'authorization':{'instruction':auth,'inputs':[{'id':i['id'],'sha256':i['sha256']} for i in inputs]},'purpose':'Read-only one-skill development assessment with reconstructable origin, pinned applicable rules, bounded trials, findings and review-first full revision proposal. Full sections 1-12 of digest-bound approved specification govern schemas, capability, recovery and effects.','activation':{'positive':['Validate this named Codex skill','Audit workflow entrypoints','Review a hand-edited skill'], 'excluded':['repair','install','general source audit','framework enforcement']},'requirements':reqs,'artifacts':artifacts,'workers':[{'role':'held-out task trial executor','independence':'essential for build trials; separate Codex agents with minimal raw fixtures and no answer key','assigned_candidate_paths':[],'outputs':'external task artifacts, commands, findings and limitations','failure':'preserve failed attempts; required unexecuted trial prevents completed build'}, {'role':'routing classification reviewer','independence':'essential; classify blinded prompts from delivered description','assigned_candidate_paths':[],'outputs':'external observed classifications; native activation NOT_RUN'}],'dependencies':[{'name':'Python','available':True,'observed_version':sys.version,'role':'3.10+ helper/evaluator'}, {'name':'PyYAML','available':True,'observed_version':__import__('yaml').__version__,'role':'YAML parsing'}, {'name':'installed Skill Creator checker','available':True,'path':'C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py','sha256':digest(Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py').read_bytes())}, {'name':'Codex subagents','available':True,'role':'independent build trials; host-provided capability, no separate filesystem isolation claimed'}, {'name':'official docs connector','available':True,'role':'optional freshness transport; retain fallback'}, {'name':'Rust enforcement','available':False,'role':'outside scope, no dependency'}]}
    write(ROOT/'build-contract.json',contract)
    write(ROOT/'spec-gaps.json',{'schema_version':'1','gaps':[]})
    builder=PROJECT/'.agents/skills/skill-builder'; write(ROOT/'builder-before-manifest.json',inventory(builder))
    write(ROOT/'development-builder-before-manifest.json',inventory(PROJECT/'src/agents/skills/skill-builder'))
    old=PROJECT/'docs/plan/skill-builds/skill-validator/20260912T140148003Z'; write(ROOT/'preserved-blocked-build-manifest.json',inventory(old))
    write(ROOT/'environment.json',{'timestamp':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'python':sys.version,'shell':'PowerShell 7','codex_cli':'Get-Command codex returned no command; host subagents available','checker_path':contract['dependencies'][2]['path'],'builder_manifest_sha256':digest((builder/'evals/build-manifest.json').read_bytes())})
    write(ROOT/'contract-created.json',{'created_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'contract_sha256':digest((ROOT/'build-contract.json').read_bytes()),'candidate_absent':not (ROOT/'candidate').exists(),'destination_absent':not (PROJECT/'src/agents/skills/skill-validator').exists(),'requirements':[r['id'] for r in reqs],'acceptance_scenarios':[f'V{i:02d}' for i in range(1,21)]})
    (ROOT/'command-log.md').write_text('# Command and tool log\n\nInitial read-only intake commands and complete outputs are retained in the host conversation tool transcript. They read the selected specification, loaded builder references, repository AGENTS.md, installed checker and memory registry; no target writes occurred. One exploratory read of scripts/deterministic_graders.py failed (file absent); actual scripts are graders.py, build_evidence.py and run_evaluation.py. Some tool displays were truncated; specification sections were reread in bounded slices.\n\nBootstrap: python -B -X utf8 docs/plan/skill-builds/skill-validator/20260912T155029Z/bootstrap.py. Writes digest-bound contract and inventories before candidate generation. Subsequent commands retain per-attempt receipts.\n',encoding='utf-8')
    print(json.dumps({'run_root':str(ROOT),'contract_sha256':digest((ROOT/'build-contract.json').read_bytes()),'requirements':len(reqs),'artifacts':len(artifacts)}))
