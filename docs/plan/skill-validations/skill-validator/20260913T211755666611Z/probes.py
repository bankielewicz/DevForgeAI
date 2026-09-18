"""Fresh contract cases: predeclared expectations, public interfaces only."""
import json
import os
from pathlib import Path
import sys
import unicodedata
from harness import RUN, ROOT, TARGET, PRIOR, read, write, save, ref, sha, compact, inventory, execute

# Independently transcribed from the frozen catalog, not imported from candidate.
RULES = ['AV-F01','AV-F02','AV-F03','AV-F04','AV-F05','AV-U01','AV-R01','AV-R02','AV-R03',
         'AV-I01','AV-I02','AV-I03','AV-I04','AV-C01','AV-S01','AV-S02','AV-W01','AV-W02','AV-E01'] + ['AV-A%02d'%i for i in range(1,11)]

def package(root, name):
    p=root/name
    write(p/'SKILL.md',f'---\nname: {name}\ndescription: Describe supplied local text.\n---\nReturn a description of the supplied text.\n')
    return p

def row(rule, cid, subject, run='set-review', result='PASS', app='applicable', required=True, evidence=None):
    return dict(schema_version='1',run_id=run,check_id=cid,rule_id=rule,subject_path=subject,method='deterministic',required=required,applicability=app,result=result,reason='Controlled synthetic record observation; not an actual skill-quality result.',evidence=evidence or [])

def jsonl(p, rows):
    write(p,b'\n'.join(compact(r) for r in rows)+b'\n')
    return ref(p)

def record_fixture(cid, kind):
    root=RUN/'trials'/cid
    pkgs=[]
    for name in ('alpha','beta'):
        p=package(root/'packages',name)
        write(p/'members/A','Local source resource, also a permissible logical integration subject.\n')
        m=inventory(p)
        mf=save(root/'inputs'/f'{name}-manifest.json',m['files'])
        pkgs.append(dict(name=name,root=str(p),manifest=ref(mf),package_digest=m['package_digest']))
    auth=write(root/'inputs/authorization.txt','Synthetic records only; no product effects.\n')
    handoff=dict(id='transfer',producer='A',consumer='B',artifact_role='text',format='text',schema_ref=None,
                 contract='The producer supplies nonempty text; required absence blocks consumer.',required=True,failure_behavior='block_consumer')
    no_handoff=kind in ('no-handoff','same-artifact','case-alias','copied-rows','unique-similar','shared-citation','na-ordinary')
    optional=kind=='optional-absence'
    if optional:
        handoff.update(required=False,failure_behavior='report_optional_absence',contract='Absent text is reported as OPTIONAL_INPUT_ABSENT; no invented success.')
    inp=dict(schema_version='standalone-set-input-v1',run_id='selection',authorization=ref(auth),
             members=[dict(member_id=k,package=p,specifications=[],adaptive_descriptor=None,depends_on=[] if k=='A' or no_handoff or optional else ['A']) for k,p in zip(('A','B'),pkgs)],
             handoffs=[] if no_handoff else [handoff],requirements=[],gaps=[])
    inputpath=save(root/'inputs/selection.json',inp)
    members=[]
    all_rows=[]
    for k,p in zip(('A','B'),pkgs):
        mroot=root/'member-evidence'/k
        shared=write(mroot/'evidence.txt','One observation may support distinct obligations.\n')
        evid=[ref(shared,mroot)] if kind=='shared-citation' else []
        rows=[row(rule,f'{k}-{rule}','members/A' if k=='A' and kind in ('same-artifact','case-alias','copied-rows') else 'SKILL.md',evidence=evid) for rule in RULES]
        if kind=='na-ordinary':
            for r in rows:
                if r['rule_id'].startswith('AV-A'):
                    r.update(applicability='not_applicable',result='NOT_APPLICABLE',reason='Ordinary member has no selected adaptive obligations.')
        checks=jsonl(mroot/'checks.jsonl',rows)
        report=write(mroot/'report.md','Controlled reducer fixture; not a claim of executed skill quality.\n')
        members.append(dict(member_id=k,package_digest=p['package_digest'],report=ref(report),checks=checks,outcome='PASS',source_state='UNCHANGED',reason='Synthetic record case.'))
        all_rows+=rows
    integ=[] if no_handoff else [row('AV-A09','transfer-observation','handoffs/transfer')]
    if kind=='required-na':
        integ[0].update(applicability='not_applicable',result='NOT_APPLICABLE',reason='No transfer assessed, despite the required declaration.')
    elif kind in ('not-run','unknown'):
        integ[0].update(result='NOT_RUN',applicability='unknown' if kind=='unknown' else 'applicable')
    elif kind=='failure':
        integ[0]['result']='FAIL'
    elif kind=='failure-unknown':
        integ[0]['result']='FAIL'
        integ.append(row('AV-A10','dependent-observation','handoffs/transfer',result='NOT_RUN',app='unknown'))
    elif kind=='missing-observation':
        integ=[]
    elif kind=='optional-absence':
        integ[0]['reason']='Observed OPTIONAL_INPUT_ABSENT according to the optional contract.'
    if kind in ('same-artifact','case-alias','copied-rows'):
        integ=[json.loads(b) for b in read(Path(members[0]['checks']['path'])).splitlines()]
    if kind in ('unique-similar','shared-citation'):
        # Same content evidence, new execution identities and valid integration locators.
        path=write(root/'integration/evidence.txt','One observation may support distinct obligations.\n')
        integ=[row('AV-A09','independent-routing','members/A',evidence=[ref(path,path.parent)]),row('AV-A10','independent-recovery','members/B',evidence=[ref(path,path.parent)])]
    integref=jsonl(root/'integration/checks.jsonl',integ)
    if kind in ('same-artifact','case-alias'):
        integref=dict(members[0]['checks'])
        if kind=='case-alias':
            integref['path']=integref['path'].replace('member-evidence','MEMBER-EVIDENCE')
    # Straight arithmetic over supplied rows, not candidate reduction. Deliberately
    # dishonest totals for duplicate/NA cases are inputs the candidate must reject.
    counted=[r for r in all_rows+integ if r['required'] and r['applicability']!='not_applicable']
    evaluated=sum(r['applicability']=='applicable' and r['result'] in ('PASS','FAIL') for r in counted)
    unknown=sum(r['applicability']=='unknown' for r in counted)
    outcome='FAIL' if any(r['result']=='FAIL' for r in counted) else 'INCOMPLETE' if evaluated<len(counted) else 'PASS'
    assessment=dict(schema_version='set-assessment-v1',run_id='set-review',input=ref(inputpath),scope='full_set',omitted_member_ids=[],omitted_handoff_ids=[],members=members,integration_checks=integref,outcome=outcome,assessment_completed=True,required_evaluated=evaluated,required_total=len(counted),unknown_applicability=unknown,limitations=['Synthetic record-integrity case only.'],prior_assessment=None)
    save(root/'records/set-assessment.json',assessment)
    return root, root/'records', dict(outcome=outcome,required_evaluated=evaluated,required_total=len(counted),unknown_applicability=unknown)

def text_fixture(cid, files):
    root=RUN/'trials'/cid
    p=package(root,'sample')
    for name,text in files.items(): write(p/name,text)
    return root,p

def unicode_expected(path,text,char):
    i=text.index(char)
    prefix=text[:i]
    line=prefix.count('\n')+1
    col=len(prefix.rsplit('\n',1)[-1])+1
    return dict(path=path,start_byte=len(prefix.encode('utf-8')),end_byte=len((prefix+char).encode('utf-8')),line=line,column=col,codepoint=f'U+{ord(char):04X}',disposition='unresolved')

def prepare():
    cases=[]
    def add(cid,finding,root,args,exit,detail,**expect):
        cases.append(dict(case_id=cid,finding=finding,fixture_root=str(root),argv=[sys.executable,'-B','-X','utf8',str(TARGET/'scripts/adaptive_observe.py'),*map(str,args)],expected_exit=exit,oracle=detail,expected=expect,manifest=inventory(root)))
    for cid,kind,code,desc in [
        ('D01','same-artifact',1,'Reject member file reused for integration; 58 unique rows cannot become 87.'),
        ('D02','case-alias',1,'Windows path case alias still refers to the same member evidence.'),
        ('D03','copied-rows',1,'Copied identical run/check identities do not establish new check executions.'),
        ('D04','unique-similar',0,'Distinct checks and obligations may share supporting bytes.'),
        ('D05','shared-citation',0,'Many distinct member checks may cite a shared observation.'),
        ('H01','required-na',1,'Required immutable handoff cannot be excluded as not applicable.'),
        ('H02','pass',0,'Required PASS is counted once: 59/59.'),
        ('H03','failure',0,'Valid assessment FAIL is accepted as a record; 59/59.'),
        ('H04','not-run',0,'Valid assessment INCOMPLETE preserves unperformed required row: 58/59.'),
        ('H05','unknown',0,'Unknown applicability remains INCOMPLETE: 58/59, unknown 1.'),
        ('H06','missing-observation',1,'A selected required handoff needs an observation row.'),
        ('H07','no-handoff',0,'No handoffs declared; empty integration is valid: 58/58.'),
        ('H08','optional-absence',0,'Observed optional-absence branch counts as applicable PASS.'),
        ('H09','na-ordinary',0,'Justified adaptive-only N/A on ordinary members remains legal: 38/38.'),
        ('H10','failure-unknown',0,'Required FAIL wins while unknown stays counted: 59/60, unknown 1.')]:
        root,record,counts=record_fixture(cid,kind)
        add(cid,'QA-01' if cid.startswith('D') else 'QA-02',root,['records','--run-root',record],code,desc,counts=counts)
    specs=[
        ('U01',{'protocol.json':'{"schema_version": "ｔask-card-v1"}\n'},2,'protocol.json','ｔ'),
        ('U02',{'protocol.json':'{\r\n  "description": "café 中文",\r\n  "schema_version":\r\n    "ｔask-card-v1"\r\n}\r\n'},2,'protocol.json','ｔ'),
        ('U03',{'protocol.json':'{"password":"SYNTHETIC_ONLY_123", "schema_version":"ｔask-card-v1"}\n'},2,'protocol.json','ｔ'),
        ('U04',{'protocol.json':'{"schema_version":"task-card-v1"}\n'},0,None,None),
        ('U05',{'notes.md':'中文 العربية café Ａ typographic prose.\n'},0,None,None),
        ('U06',{'notes.md':'A legitimate joining sequence: 👩\u200d💻.\n'},2,'notes.md','\u200d'),
        ('U07',{'notes.md':'Run `ｐython` only as an illustrated command.\n'},2,'notes.md','ｐ')]
    for cid,files,code,path,char in specs:
        root,p=text_fixture(cid,files)
        candidates=[] if path is None else [unicode_expected(path,files[path],char)]
        add(cid,'QA-03',root,['package','--source',p],code,'Exact protocol/command candidates are unresolved; legitimate prose preserved; original bytes stay unchanged.',candidates=candidates,secret='SYNTHETIC_ONLY_123')
    fences=[
        ('F01','```text\n```not-close\n[example](absent.md)\n```\n',0,[]),
        ('F02','~~~text\n~~~not-close\n[example](absent.md)\n~~~\n',0,[]),
        ('F03','````text\n```\n[example](absent.md)\n````\n',0,[]),
        ('F04','```text\n~~~\n[example](absent.md)\n```\n',0,[]),
        ('F05','```text\n[example](absent.md)\n``` \t\n[real](absent.md)\n',1,[4]),
        ('F06','~~~text\n[example](absent.md)\n~~~~\n[real](absent.md)\n',1,[4]),
        ('F07','[real](absent.md)\n',1,[1]),
        ('F08','```text\n```not-close\n[example](absent.md)\n```\n[real](absent.md)\n',1,[5]),
        ('F09','   ```text\n   ```not-close\n[example](absent.md)\n   ```\n',0,[]),
        ('F10','[A](guide.md#one) [B](guide.md#two) [C](guide.md#explicit)\n',0,[])]
    for cid,text,code,missing in fences:
        files={'example.md':text}
        if cid=='F10': files['guide.md']='# One\nTwo\n---\n<span id="explicit"></span>\n'
        root,p=text_fixture(cid,files)
        add(cid,'QA-04',root,['package','--source',p],code,'CommonMark 0.31.2 section 4.5: code contents literal; only valid closing fences restore links.',missing_lines=missing)
    for cid,mode,code in [('R06','records',1),('R07','records',1),('P07','package',0),('P08','package',2)]:
        root=PRIOR/'trials/independent'/cid
        arg=root/'sample' if mode=='package' else root
        extra={}
        if cid=='P07': extra['missing_lines']=[]
        if cid=='P08': extra['candidates']=[unicode_expected('protocol.json',read(arg/'protocol.json').decode(),'ｔ')]
        add('REPLAY-'+cid,{'R06':'QA-01','R07':'QA-02','P08':'QA-03','P07':'QA-04'}[cid],root,[mode,'--source' if mode=='package' else '--run-root',arg],code,'Original retained fixture byte replay; no relocation or rewriting.',**extra)
    save(RUN/'expectations-before-execution.json',cases)
    print('Prepared',len(cases),'cases, no candidate executed.')

def run():
    cases=json.loads(read(RUN/'expectations-before-execution.json'))
    result=[]
    for case in cases:
        cid=case['case_id']
        assert inventory(Path(case['fixture_root']))['files']==case['manifest']['files'], 'Fixture drift'
        receipt=execute(cid,case['argv'],Path(case['fixture_root']))
        raw=read(RUN/'commands'/cid/'stdout.txt')
        try: obs=json.loads(raw)
        except (ValueError,UnicodeError): obs={}
        checks={'exit':receipt['exit']==case['expected_exit'],'completed':not receipt['timed_out'],'preserved':receipt['fixture_unchanged']}
        ex=case['expected']
        if 'candidates' in ex:
            actual=obs.get('observations',{}).get('unicode_candidates',[])
            checks['candidate_count']=len(actual)==len(ex['candidates'])
            checks['candidate_locations']=all(any(all(a.get(k)==v for k,v in e.items()) for a in actual) for e in ex['candidates'])
            checks['no_automatic_fail']=not any(r.get('result')=='FAIL' for r in obs.get('checks',[]))
            if ex.get('secret'): checks['redacted']=ex['secret'] not in raw.decode(errors='replace')
        if 'missing_lines' in ex:
            actual=[e['line'] for e in obs.get('observations',{}).get('edges',[]) if e['resolution']=='missing']
            checks['missing_lines']=actual==ex['missing_lines']
        result.append(dict(case_id=cid,finding=case['finding'],expected_exit=case['expected_exit'],actual_exit=receipt['exit'],matched=all(checks.values()),checks=checks,evidence=ref(RUN/'commands'/cid/'receipt.json',RUN)))
        save(RUN/'results'/f'{cid}.json',result[-1])
        print(cid, 'MATCH' if result[-1]['matched'] else 'MISMATCH',flush=True)
    save(RUN/'probe-results.json',result)

if __name__=='__main__':
    {'prepare':prepare,'run':run}[sys.argv[1]]()
