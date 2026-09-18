"""Retest unchanged findings and independent set-reduction probes in fresh attempt."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'attempt-03'
HELPER=ROOT.parents[5]/'src/agents/skills/skill-validator/scripts/adaptive_observe.py'
RULES=['AV-F01','AV-F02','AV-F03','AV-F04','AV-F05','AV-U01','AV-R01','AV-R02','AV-R03','AV-I01','AV-I02','AV-I03','AV-I04','AV-C01','AV-S01','AV-S02','AV-W01','AV-W02','AV-E01']+['AV-A%02d'%i for i in range(1,11)]

def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data if isinstance(data,bytes) else data.encode('utf-8'))
    return {'path':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}

def record(path,value):
    return write(path,json.dumps(value,ensure_ascii=False,indent=2))

def run(ident,args):
    case=OUT/ident
    command=[sys.executable,'-B','-X','utf8',str(HELPER),*args]
    result=subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
    write(case/'stdout.json',result.stdout)
    write(case/'stderr.txt',result.stderr)
    record(case/'receipt.json',{'command':command,'exit_code':result.returncode})
    print(ident,result.returncode,json.loads(result.stdout)['status'])

def main():
    OUT.mkdir(exist_ok=False)
    record(OUT/'script-hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in HELPER.parent.glob('*.py')})
    for ident in ['IR-02','IR-03']:
        run(ident,['package','--source',str(ROOT/'fixtures'/ident/'example-skill')])
    for ident in ['IR-08','IR-09']:
        run(ident,['records','--run-root',str(ROOT/'fixtures'/ident/'run')])
    selected=json.loads((ROOT/'attempt-02/IR-11/request.json').read_text(encoding='utf-8'))
    selected['members']=selected['members'][:1]
    selected['authorization']=write(OUT/'input/authorization.txt','Assess exactly selected member A, draft-card, using this synthetic set review.\n')
    selected['run_id']='set-review'
    input_ref=record(OUT/'input/input.json',selected)
    for ident in ['IR-16','IR-17','IR-18','IR-19','IR-20','IR-21','IR-22']:
        case=OUT/ident
        checks=[]
        for rule in RULES:
            adaptive=rule.startswith('AV-A')
            dimension='instructions' if rule.startswith(('AV-I','AV-S')) else 'behavior' if rule=='AV-W02' else 'workflow' if rule.startswith(('AV-W','AV-A')) else 'standards'
            checks.append({'schema_version':'1','run_id':'member-review','check_id':rule,'rule_id':rule,'subject_path':'SKILL.md','method':'deterministic','required':True,'applicability':'not_applicable' if adaptive else 'applicable','result':'NOT_APPLICABLE' if adaptive else 'PASS','reason':'Ordinary skill has no adaptive contract.' if adaptive else 'Synthetic record-integrity fixture; semantic assessment is outside this probe.','evidence':[],'dimension':dimension})
        member_outcome='PASS'
        outcome='PASS'
        total,evaluated,unknown=19,19,0
        if ident in ('IR-17','IR-18'):
            checks[1].update(applicability='unknown',result='NOT_RUN',reason='Applicable host-specific requirement unresolved.')
            member_outcome=outcome='INCOMPLETE'
            evaluated,unknown=18,1
        if ident=='IR-18':
            checks[0]['result']='FAIL'
            member_outcome=outcome='FAIL'
            advisory=copy.deepcopy(checks[2])
            advisory.update(check_id='advisory',required=False,result='FAIL')
            checks.append(advisory)
        if ident=='IR-19': total=20
        if ident=='IR-20':
            aliases={'standards':'standards_compliance','workflow':'workflow_correctness','instructions':'instruction_quality','behavior':'behavioral_evaluation'}
            for row in checks: row['dimension']=aliases[row['dimension']]
        if ident=='IR-21':
            for row in checks:
                row.update(applicability='not_applicable',result='NOT_APPLICABLE',reason='Explicit isolated source-coverage fixture; this check is not applicable.')
            checks[0].update(applicability='applicable',result='FAIL',reason='Required entrypoint parsing failed; retained despite absent human report.')
            member_outcome='INCOMPLETE'
            outcome='FAIL'
            total,evaluated,unknown=1,1,0
        if ident=='IR-22': checks[0]['subject_path']='../outside.md'
        check_ref=write(case/'member/checks.jsonl','\n'.join(json.dumps(row) for row in checks)+'\n')
        report=write(case/'member/report.md','Synthetic member record integrity probe. No native behavior claim.\n')
        integration=write(case/'set/integration.jsonl','')
        assessment={'schema_version':'set-assessment-v1','run_id':'set-review','input':input_ref,'scope':'full_set','omitted_member_ids':[],'omitted_handoff_ids':[],'members':[{'member_id':'A','package_digest':selected['members'][0]['package']['package_digest'],'report':None if ident=='IR-21' else report,'checks':check_ref,'outcome':member_outcome,'source_state':'UNCHANGED','reason':'Synthetic retained member observation.'}],'integration_checks':integration,'outcome':outcome,'assessment_completed':True,'required_evaluated':evaluated,'required_total':total,'unknown_applicability':unknown,'limitations':['No handoffs are declared; record integrity only.'],'prior_assessment':None}
        record(case/'set/assessment.json',assessment)
        run(ident,['records','--run-root',str(case/'set')])

if __name__=='__main__':
    main()
