"""Final evidence audit; only assessment-owned artifacts are updated."""
import json
import re
import shutil
from pathlib import Path
from qa_harness import RUN, ROOT, TARGET, LOADED, PRIOR, inventory, save, sha, now

def read(p): return json.loads(p.read_bytes())
def write(p, s): p.write_text(s, encoding='utf-8')

def amend():
    old = RUN/'report-drafts'/'001'
    old.mkdir(parents=True, exist_ok=False)
    paths = ['qa-report.md','coverage-matrix.json','coverage-matrix.md','coverage-summary.json','stable-findings.json','final-receipt.json','member-records/validation-report.md','member-records/handoff.json','member-records/inputs/coverage-matrix.json','member-records/checks.jsonl','supplemental-records/adaptive-observations.json']
    for name in paths:
        dst=old/name; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(RUN/name,dst)
    matrix=read(RUN/'coverage-matrix.json')
    for row in matrix:
        if row['id']=='VAT-25':
            row['result']='INCOMPLETE'
            row['remaining_limitation']+=' Static boundary review only: no direct cold request for nonexistent Rust acceptance or universal certification was executed.'
        if row['id']=='VAT-03':
            row['result']='INCOMPLETE'
            row['remaining_limitation']+=' Duplicate/injected members and closure have executed controls; unrelated C actually installed alongside a complete cold selected-set assessment was not separately exercised.'
    save(RUN/'coverage-matrix.json',matrix)
    md=(RUN/'coverage-matrix.md').read_text(encoding='utf-8')
    for ident in ('VAT-03','VAT-25'):
        row=next(x for x in matrix if x['id']==ident)
        md=re.sub(r'^\| '+ident+r' / .*$', '| '+ident+' / '+str(row['line'])+' | '+row['result']+' | '+row['implementation_locations']+' | '+row['evidence']+' | '+row['remaining_limitation']+' |',md,flags=re.M)
    write(RUN/'coverage-matrix.md',md)
    summary=read(RUN/'coverage-summary.json');summary.update(VAT={'PASS':12,'FAIL':5,'INCOMPLETE':8},VAT_required_pass_rate=48.0);save(RUN/'coverage-summary.json',summary)
    mem=RUN/'member-records';shutil.copyfile(RUN/'coverage-matrix.json',mem/'inputs/coverage-matrix.json')
    checks=[json.loads(l) for l in (mem/'checks.jsonl').read_text().splitlines()]
    for row in checks:
        for ref in row['evidence']:
            if ref['path']=='inputs/coverage-matrix.json':ref['sha256']=sha((mem/ref['path']).read_bytes())
    write(mem/'checks.jsonl',''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in checks))
    report=(RUN/'qa-report.md').read_text(encoding='utf-8').replace('14 PASS, 5 FAIL, 6 INCOMPLETE','12 PASS, 5 FAIL, 8 INCOMPLETE').replace('56.00%','48.00%')
    report += '\nFinal citation review conservatively marks VAT-03 and VAT-25 INCOMPLETE: no whole selected-set trial with unrelated C installed, and no direct unsupported-certification request trial. The earlier draft and successful record checks remain retained. The target Unicode candidate at tests/test_adaptive.py:102 is a deliberate fullwidth-command test string, passed as data to the candidate scanner; it is legitimate fixture content, not a production command. New legacy and adaptive records are checked separately through supported interfaces; final results are in final-receipt.json.\n'
    write(RUN/'qa-report.md',report)
    # This copy lives one directory below the report; preserve working links.
    member_report=re.sub(r'\]\((?!https?://)([^)]+)\)',lambda m:'](../'+m.group(1)+')',report)
    write(mem/'validation-report.md',member_report)
    handoff=read(mem/'handoff.json');handoff['report']['sha256']=sha((mem/'validation-report.md').read_bytes());save(mem/'handoff.json',handoff)
    supp=read(RUN/'supplemental-records/adaptive-observations.json')
    for c in supp['unicode_candidates']:
        if c['path']=='tests/test_adaptive.py' and c['line']==102:
            c.update(disposition='legitimate',reason='Captured tests/test_adaptive.py:101-104 passes a deliberately fullwidth command literal as data into text.candidates and asserts NFKC detection. The 229-case executed suite includes this test. This is intentionally defective fixture content, not a production command.')
    save(RUN/'supplemental-records/adaptive-observations.json',supp)
    findings=read(RUN/'stable-findings.json')
    for finding in findings['findings']:
        for field in ('source_refs','observation_refs'):
            for ref in finding[field]:
                p=mem/ref['path'];assert p.is_file() and sha(p.read_bytes())==ref['sha256'];ref['path']=str(p.resolve())
    save(RUN/'stable-findings.json',findings)
    save(RUN/'report-reconciliation.json',{'time_utc':now(),'draft_preserved':'report-drafts/001','changes':['VAT-03 and VAT-25 conservatively incomplete','member report links and bound matrix hashes refreshed','legitimate target fixture Unicode adjudicated','top-level finding reference bases made absolute'],'effect_scope':'assessment artifacts only'})

def finish():
    results={}
    for name,p in [('target',TARGET),('loaded-evaluator',LOADED),('companion',ROOT/'src/agents/skills/skill-builder'),('prior-evidence',PRIOR)]:
        current=inventory(p);before=read(RUN/(name+'-before.json'))
        results[name]={'digest':current['package_digest'],'file_count':current['file_count'],'unchanged':current['files']==before['files']};assert results[name]['unchanged']
    for name,expected in read(RUN/'contract-hashes.json').items():
        actual=sha((ROOT/'docs/plan'/name).read_bytes());results[name]={'actual':actual,'expected':expected['expected'],'unchanged':actual==expected['expected']};assert results[name]['unchanged']
    save(RUN/'final-integrity.json',{'checked_at_utc':now(),'bounded_inputs':results,'scope':'Exact permitted inventories only; not all historical or operational trees.'})
    commands=[]
    for d in sorted((RUN/'commands').iterdir()):
        if (d/'command.json').is_file():
            commands.append({'attempt':d.name,**read(d/'command.json'),'stdout':{'path':str(d/'stdout.txt'),'sha256':sha((d/'stdout.txt').read_bytes())},'stderr':{'path':str(d/'stderr.txt'),'sha256':sha((d/'stderr.txt').read_bytes())}})
    save(RUN/'command-log.json',commands)
    write(RUN/'command-log.md','# Exact commands and results\n\nArgument vectors were executed without shell interpolation. Full streams, timing and termination receipts are linked. Repeated attempts are not additional passing cases. Early exploratory reads remain in the session transcript.\n\n'+''.join('## '+c['attempt']+'\n\n```json\n'+json.dumps(c['argv'],ensure_ascii=False)+'\n```\n\nCwd: `'+c['cwd']+'`. Start '+c['started_at_utc']+'; end '+c.get('ended_at_utc','unrecorded')+'; exit '+str(c.get('exit_status'))+'; '+c['termination']+'. [stdout](commands/'+c['attempt']+'/stdout.txt), [stderr](commands/'+c['attempt']+'/stderr.txt), [receipt](commands/'+c['attempt']+'/command.json).\n\n' for c in commands))
    validation={}
    for name in ('new-legacy-records-002','new-adaptive-records-002'):
        c=read(RUN/'commands'/name/'command.json');assert c['exit_status']==0
        validation[name]={'exit_status':c['exit_status'],'receipt':'commands/'+name+'/command.json','scope':'Record integrity only; self-review, not semantic acceptance'}
    receipt=read(RUN/'final-receipt.json');receipt.update(records_validation=validation,final_integrity='final-integrity.json',coverage_summary='coverage-summary.json',completed_at_utc=now())
    receipt['report']['sha256']=sha((RUN/'qa-report.md').read_bytes());save(RUN/'final-receipt.json',receipt)
    # Verify every local Markdown link in the delivered report and its member copy.
    link_checks=[]
    for p in (RUN/'qa-report.md',RUN/'member-records/validation-report.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if link.startswith('http'):continue
            target=(p.parent/link.split('#')[0]).resolve();link_checks.append({'report':str(p.relative_to(RUN)),'link':link,'exists':target.exists()});assert target.exists()
    save(RUN/'final-link-audit.json',link_checks)
    print(json.dumps({'outcome':'FAIL','findings':4,'VAT':{'PASS':12,'FAIL':5,'INCOMPLETE':8},'record_checks':validation,'identity':results['target']},ensure_ascii=False))

if __name__=='__main__':
    import sys
    amend() if sys.argv[1]=='amend' else finish()
