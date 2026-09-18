"""Final delivery readback and non-self-referential evidence seal."""
import json
import sys
from bootstrap import RUN,ROOT,VALIDATOR,write,ref,command
sys.path.insert(0,str(VALIDATOR/'scripts'))
import observe

def main():
    report=(RUN/'validation-report.md').read_text()
    records=json.loads((RUN/'observations/records-002.stdout').read_bytes())
    assert records['status']=='OBSERVED' and not records['errors']
    report+='\nFinal integrity verification: schema-1 records attempt 002 returned OBSERVED with zero errors; the supplemental adaptive records check also returned OBSERVED with zero errors. Record checking validates shape, references and reductions, not semantic truth or framework acceptance.\n'
    (RUN/'validation-report.md').write_text(report,encoding='utf-8')
    handoff=json.loads((RUN/'handoff.json').read_text());handoff['report']=ref('validation-report.md');write('handoff.json',handoff)
    with (RUN/'command-log.md').open('a',encoding='utf-8') as stream:
        stream.write('\nFinal evidence repairs and checks: inputs/final_checks.py executed both schema-family checks; adaptive exit 0, schema-1 attempt 001 exit 1 with eight retained errors. inputs/repair_records.py retained the complete pre-repair hierarchy and corrected derived locators only; evaluation-002 exit 0 (21/21), records-002 exit 0 (zero errors). inputs/seal_delivery.py binds final report/handoff bytes, repeats final source/record readback and writes the evidence seal. Exact argv/cwd/timing/exit for each helper are in observations/*.receipt.json.\n')
    p=command('source-readback-final',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'readback','--source',str(ROOT/'src/agents/skills/qa'),'--manifest',str(RUN/'source-manifest.json')])
    assert p.returncode==0 and json.loads(p.stdout)['status']=='MATCH'
    p=command('records-003',[sys.executable,'-B','-X','utf8',str(VALIDATOR/'scripts/observe.py'),'records','--run-root',str(RUN)])
    value=json.loads(p.stdout);assert p.returncode==0 and not value['errors']
    files,excluded=observe.inventory(RUN);assert not excluded
    rows=[]
    for relative,path,info in files:
        data=observe.read_stable(path,info)
        rows.append({'path':relative,'bytes':len(data),'sha256':observe.sha256(data)})
    digest=observe.sha256(observe.compact(rows))
    write('final-evidence-manifest.json',{'schema_version':'qa-validation-evidence-seal-v1','target_package_digest':json.loads((RUN/'source-manifest.json').read_text())['package_digest'],'files':rows,'evidence_digest':digest,'excluded_from_own_digest':['final-evidence-manifest.json'],'record_integrity':ref('observations/records-003.stdout'),'framework_acceptance':'NOT_EVALUATED'})
    for row in rows:
        assert observe.sha256(observe.read_stable(RUN/row['path']))==row['sha256']
    seal=json.loads((RUN/'final-evidence-manifest.json').read_text())
    assert observe.sha256(observe.compact(seal['files']))==seal['evidence_digest']
    print(json.dumps({'status':'VERIFIED','sealed_files':len(rows),'report':ref('validation-report.md'),'bundle':ref('evaluation/bundle-manifest.json'),'seal':ref('final-evidence-manifest.json'),'required_checks':value['required_coverage']},indent=2))

if __name__=='__main__':main()
