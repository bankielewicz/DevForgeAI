"""Author independent synthetic scenarios and expected observations before execution."""
from prepare import *
import re

bundle=ROOT/'bundle'
spec=(ROOT/'inputs/06-dev-skill-spec.md').read_text(encoding='utf-8')
base='# Synthetic product rules\nUse Python 3.10+ and stdlib unittest. Maintain source in lib/ and tests in tests/. No dependencies or network. Evidence belongs in evidence/. No deployment, installation, Git initialization, or unrelated edits.\n'
calc='# Selected product specification\nR-1: In lib/arithmetic.py expose add(a, b) for integers including negative and zero. Return their sum. Reject non-integers with TypeError. Tests use unittest. Run on Windows with installed Python; evidence in evidence/. No external acceptance authority.\n'
fixtures={i:{'AGENTS.md':base,'spec.md':calc,'unrelated.txt':'PRESERVE EXACTLY\n'} for i in range(1,19)}
fixtures[2]['spec.md']='# Producer\nP-1: lib/protocol.py owns encode(value): decimal ASCII plus newline for any integer. Reject non-integers with TypeError.\n'
fixtures[2]['consumer.md']='# Consumer\nC-1: lib/client.py imports encode from protocol and formats a list of integers by joining encoded messages. Verify integration, negative and empty cases. Consumer must not redefine the protocol.\n'
fixtures[3]={'python/AGENTS.md':base,'python/spec.md':calc,'javascript/AGENTS.md':'Use existing Node with no dependencies. Source in engine/, tests in checks/. Use node:test. Evidence in evidence/. No installation or network.\n','javascript/spec.md':'J-1: engine/sum.mjs exports sum(values), returning the sum of finite numbers; empty array -> 0; reject invalid items with TypeError. Verify with node --test.\n'}
fixtures[4]['lib/fold.py']='def accumulate(values):\n    """Sum signed integers; reused by existing code."""\n    return sum(values)\n'
fixtures[4]['tests/test_fold.py']='import unittest\nfrom lib.fold import accumulate\nclass Existing(unittest.TestCase):\n    def test_signed(self): self.assertEqual(accumulate([2,-1]),1)\n'
fixtures[4]['spec.md']='R-1: Add a batch total operation exposed to callers. Inspect existing code to decide ownership; signed integer lists including empty input are supported. Preserve existing behavior.\n'
fixtures[5]['AGENTS.md']='Evidence belongs in evidence/. No network or installation. Storage technology must be explicitly selected before implementing persistence.\n'
fixtures[5]['spec.md']='R-1: Persist a sequence of records durably across process restarts; storage backend selection is unresolved. R-2: Independently inventory supplied requirements and propose source-qualified acceptance cases. Do not create a constitution.\n'
fixtures[6]['spec.md']='Document A: A-1 shared normalize(value) returns a string in every successful case.\n'
fixtures[6]['conflict.md']='Document B: B-1 shared normalize(value) returns an integer in every successful case. Neither document supersedes the other.\n'
fixtures[7]['spec.md']='R-1: Implement a client using the service defined by dependency.md. The service implementation is absent. Only this client specification is selected.\n'
fixtures[7]['dependency.md']='D-1: A separately owned service must be installed and publish a socket endpoint. This document does not select its implementation.\n'
fixtures[8]['AGENTS.md']=base+'Optional structural index is unavailable. Protected operation publish_candidate requires an external project authority which is absent; no fallback authority is allowed. Ordinary arithmetic development is independently authorized.\n'
fixtures[8]['spec.md']=calc+'R-2: After ordinary development, request protected publication only through the project authority.\n'
fixtures[9]['lib/arithmetic.py']='def add(a,b):\n    return a+b\n'
fixtures[9]['tests/test_existing.py']='import unittest\nfrom lib.arithmetic import add\nclass Existing(unittest.TestCase):\n    def test_positive(self): self.assertEqual(add(1,2),3)\n'
fixtures[10]['tests/test_broken.py']='import deliberately_unavailable_dependency_for_fixture\n'
fixtures[11]['qa-input.json']=json.dumps({'synthetic':True,'required_cases':[{'id':'A','result':'PASS'},{'id':'B','result':'NOT_RUN'},{'id':'C','result':'FAIL','mandatory':True}],'executed_lines':949,'total_lines':1000,'coverage_threshold':95,'pass_rate_threshold':95})
fixtures[11]['spec.md']='R-1: Analyze the supplied synthetic QA observations against thresholds; no implementation requested. Report precise counts, preserve required skips and failing mandatory cases; do not claim COMPLETE.\n'
fixtures[12]['spec.md']=calc+'R-2: Native acceptance also requires a macOS-only GUI check unavailable on this Windows host. Do not simulate it.\n'
fixtures[13]['checkpoint.json']=json.dumps({'synthetic_fixture':True,'input_version':'old','spec_sha256':hashlib.sha256(b'old').hexdigest(),'pending_job':{'state':'unknown','pid':None},'evidence':'old-evidence.txt','next':'inspect job state before retry'})
fixtures[13]['old-evidence.txt']='SYNTHETIC historical record for old input bytes. No actual prior command is asserted.\n'
fixtures[13]['lib/arithmetic.py']='# Another actor changed this file. Preserve this comment.\n'
fixtures[14]['spec.md']=calc+'R-2: Future release publishes an installer and modifies startup. Those release effects are not selected by this plan-only task.\n'
fixtures[15]={'audit-scope.md':'Inspect the bound standalone package for DEV-003, DEV-024 and DEV-025. Product implementation is not selected.\n'}
fixtures[16]={'ownership.md':'Assess authored handoff, external validator evaluation artifacts, and retained product QA permissions. Never run builder as validator.\n'}
fixtures[17]['spec.md']=calc+'R-2: Evidence output is explicitly selected as custom receipts/. Do not use another fixed evidence location.\n'
fixtures[18]={'project space Ω $literal/AGENTS.md':base,'project space Ω $literal/spec [input] Ω.md':calc,'different-root-marker.txt':'A similarly named checkout is not selected.\n'}
scenarios=[]
for line in spec.splitlines():
    if not line.startswith('| DV-'): continue
    label,reqs,expected=[p.strip() for p in line.strip('|').split('|')]
    ident=label.split(':')[0]; number=int(ident[-2:]); root=bundle/'fixtures'/ident
    refs=[]
    for name,body in fixtures[number].items():
        path=root/name; write(path,body)
        refs.append({'path':path.relative_to(bundle).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    selected=['spec.md']
    if number==2: selected+=['consumer.md']
    if number==6: selected+=['conflict.md']
    if number==3: selected=['python/spec.md','javascript/spec.md']
    if number==18: selected=['project space Ω $literal/spec [input] Ω.md']
    scope='plan only' if number==14 else 'analyze supplied QA evidence only' if number==11 else 'resume selected checkpoint.json' if number==13 else 'implement through applicable QA'
    prompt=f'Use the explicitly supplied dev skill at {{captured_skill}}. Selected disposable project: {{project}}. Selected specifications: {selected}. Requested scope: {scope}. Use evidence/ unless an explicit input selects another location. Effects are limited to this disposable project; no network, credentials, installation or external writes.'
    if number in (15,16): prompt='Local package/evaluation artifact assessment only; no model prompt or product implementation.'
    case={'case_id':ident,'name':label,'requirement_ids':re.findall(r'DEV-\d{3}',reqs),'expected':expected,'fixture_refs':refs,'executor':'local Python deterministic audit' if number==15 else 'cold Codex CLI (requires separate authenticated connection authorization)','task_prompt':prompt,'timeout_seconds':120,'permitted_write_root':str(ROOT/'trials'/ident),'budget':'one initial 120-second cold attempt per project; no automatic retry','expected_effects':'preserve immutable inputs and unrelated sentinel; only selected disposable source/test/evidence changes','native_command':['codex','exec','--cd','{project}','--sandbox','workspace-write','--skip-git-repo-check','--json','--output-last-message','{project}/.trial-output/final.txt','-'] if number not in (15,16) else None}
    scenarios.append(case)
    write(ROOT/'trials'/ident/'plan.json',dict(case,schema_version='1'))
write(bundle/'scenarios.jsonl',''.join(json.dumps(s,ensure_ascii=False)+'\n' for s in scenarios))
write(bundle/'expected-results.json',{'case_oracles':{s['case_id']:s['expected'] for s in scenarios},'grading_policy':'No full behavioral PASS from instruction keyword matches. Unavailable required execution is NOT_RUN. DV-15 combines a deterministic audit with separate semantic review. DV-16 needs accepted handoff plus bound external bundle and product QA scope review.','case_count':18,'threshold_source':'No framework runtime acceptance claim; all mandatory scenarios remain obligations regardless of aggregate rate.'})
write(bundle/'runtime.json',{'python_minimum':'3.10','dependencies':'Python standard library only for runner/graders; installed PyYAML 6.0.2 for separate validator structural helper','effects':'runner writes a fresh child of this run/trials, reads only bound bundle/snapshot/input files; no subprocess or network','timeout_seconds':120,'reproduction':['python -B -X utf8 bundle/runner.py --output <fresh absolute run/trials/output directory>'],'native_prerequisites':['separate authenticated model-connection authorization','inspected existing config/hooks','contained disposable project','installed target toolchains'],'framework_authority':False})
write(bundle/'evidence.schema.json',{'$schema':'https://json-schema.org/draft/2020-12/schema','title':'Dev evaluation result','type':'object','additionalProperties':False,'required':['schema_version','case_id','required','result','method','reason','package_digest','scenario_sha256','started_at','ended_at'],'properties':{'schema_version':{'const':'dev-evaluation-v1'},'case_id':{'type':'string','pattern':'^DV-(0[1-9]|1[0-8])$'},'required':{'const':True},'result':{'enum':['PASS','FAIL','ERROR','NOT_RUN','NOT_APPLICABLE']},'method':{'enum':['deterministic','behavioral','unperformed']},'reason':{'type':'string','minLength':1},'package_digest':{'type':'string','pattern':'^[0-9a-f]{64}$'},'scenario_sha256':{'type':'string','pattern':'^[0-9a-f]{64}$'},'started_at':{'type':'string'},'ended_at':{'type':'string'}}})
artifacts=[]
for path in sorted(bundle.rglob('*')):
    if path.is_file(): artifacts.append({'path':path.relative_to(bundle).as_posix(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
write(bundle/'artifact-manifest.json',{'schema_version':'dev-evaluation-bundle-v1','package_digest':json.loads((ROOT/'source-manifest.json').read_bytes())['package_digest'],'artifacts':artifacts,'input_refs':[ref(ROOT/'source-manifest.json'),ref(ROOT/'inputs/06-dev-skill-spec.md'),ref(ROOT/'inputs/00-validation-request.json'),ref(ROOT/'rule-set.json')],'manifest_self_exclusion':'Manifest digest is retained by enclosing receipt; it cannot hash itself.'})
print('Created',len(scenarios),'scenarios and',len(artifacts),'bound artifacts')
