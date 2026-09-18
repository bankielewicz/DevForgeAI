"""Independent disposable regression probes; no target execution or builder imports."""
import copy
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[5]
HELPER = PROJECT / 'src/agents/skills/skill-validator/scripts/adaptive_observe.py'
EXPECTED = json.loads((ROOT / 'expectations.json').read_text(encoding='utf-8'))
RESULTS = []

def digest(data):
    return hashlib.sha256(data).hexdigest()

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(value if isinstance(value, bytes) else value.encode('utf-8'))
    return {'path':str(path), 'sha256':digest(path.read_bytes())}

def record(path, value):
    return write(path,json.dumps(value,ensure_ascii=False,indent=2))

def execute(ident, arguments):
    command = [sys.executable,'-B','-X','utf8',str(HELPER),*arguments]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(command,cwd=ROOT,capture_output=True,timeout=120)
    out = ROOT / 'results' / ident
    write(out / 'stdout.json',result.stdout)
    write(out / 'stderr.txt',result.stderr)
    row = {'id':ident,'command':command,'started':started,'exit_code':result.returncode,
           'expected':next(x for x in EXPECTED['cases'] if x['id']==ident)['expect']}
    row['observation'] = json.loads(result.stdout.decode('utf-8'))
    record(out / 'receipt.json',row)
    RESULTS.append(row)

def package(ident, body, extra=None):
    root = ROOT / 'fixtures' / ident / 'example-skill'
    write(root / 'SKILL.md', '---\nname: example-skill\ndescription: Draft concise incident summaries from supplied event notes.\n---\n\n'+body)
    for path,data in (extra or {}).items():
        write(root/path,data)
    execute(ident,['package','--source',str(root)])

def helper(ident, value, nested=False):
    root = ROOT / 'fixtures' / ident / 'run'
    record(root / 'helper.json',value)
    if nested:
        write(root/'trials/fixture/findings.json','{ BROKEN TARGET DATA')
    execute(ident,['records','--run-root',str(root)])

def check(result):
    return {'schema_version':'1','run_id':'helper','check_id':'check-1','rule_id':'AV-E01','subject_path':'records','method':'deterministic','required':True,'applicability':'applicable','result':result,'reason':'Independent synthetic record for integrity review.','evidence':[]}

def main():
    if (ROOT/'results').exists():
        raise RuntimeError('Fresh attempts required; refusing result overwrite')
    record(ROOT/'candidate-hashes.json',{str(p.relative_to(HELPER.parents[1])):digest(p.read_bytes()) for p in HELPER.parent.glob('*.py')})
    package('IR-01','[Guide](references/guide.md#alpha)\n[Again][guide]\n![Image](assets/image.svg)\n\n[guide]: references/guide.md#alpha-1\n',{'references/guide.md':'# Alpha\n# Alpha\n','assets/image.svg':'<svg/>'})
    package('IR-02','Document a Markdown link using the literal syntax `[Example](absent-example.md)`.\n')
    package('IR-03','[Guide](references/guide(v1).md)\n',{'references/guide(v1).md':'# Guide\n'})
    package('IR-04','[Required guide](references/absent.md)\n')
    package('IR-05','日本語 العربية עברית. Preserve the symbol ♥\ufe0f in summaries.\n')
    package('IR-06','[Guide](references/invalid.md)\n',{'references/invalid.md':b'\xffinvalid'})
    valid = {'schema_version':'adaptive-check-observation-v1','command':'records','status':'OBSERVED','checks':[check('PASS')],'observations':{'checked_records':['assessment.json'],'errors':[]},'limitations':['Shape evidence only.']}
    helper('IR-07',valid)
    bad = copy.deepcopy(valid)
    bad['checks'][0]['result']='FAIL'
    bad['observations']['errors']=['assessment.json: totals mismatch']
    helper('IR-08',bad)
    context={'tokenizer':None,'files':[{'path':'SKILL.md','bytes':20,'characters':20,'lines':1,'tokens':None}],'loads':[],'budget':None,'budget_result':'NOT_APPLICABLE','reason':'No selected budget.'}
    candidate={'path':'SKILL.md','start_byte':10,'end_byte':1,'line':1,'column':1,'codepoint':'U+200B','unicode_name':'ZERO WIDTH SPACE','escaped_excerpt':'\\u200b','context':'prose','disposition':'defect','reason':'Raw deterministic candidate improperly finalized.'}
    badpackage={'schema_version':'adaptive-check-observation-v1','command':'package','status':'OBSERVED','checks':[],'observations':{'unicode_candidates':[candidate],'resources':[],'edges':[],'context':context},'limitations':[]}
    helper('IR-09',badpackage)
    helper('IR-10',valid,True)
    selected_root=ROOT/'fixtures/selected'
    members=[]
    for ident,name in [('A','draft-card'),('B','review-card')]:
        root=selected_root/name
        write(root/'SKILL.md','---\nname: '+name+'\ndescription: Process a supplied card.\n---\nRead supplied data and write the requested result.\n')
        data=(root/'SKILL.md').read_bytes()
        rows=[{'path':'SKILL.md','bytes':len(data),'sha256':digest(data)}]
        manifest=record(selected_root/(ident+'-manifest.json'),rows)
        compact=json.dumps(rows,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode('utf-8')
        members.append({'member_id':ident,'package':{'name':name,'root':str(root),'package_digest':digest(compact),'manifest':manifest},'specifications':[],'adaptive_descriptor':None,'depends_on':[] if ident=='A' else ['A']})
    auth=write(selected_root/'authorization.txt','Assess exactly draft-card as A and review-card as B in this synthetic project.\n')
    base={'schema_version':'standalone-set-input-v1','run_id':'independent-review','authorization':auth,'members':members,'handoffs':[],'requirements':[],'gaps':[]}
    for ident in ['IR-11','IR-12','IR-13','IR-14','IR-15']:
        value=copy.deepcopy(base)
        if ident=='IR-12': value['members'].append(copy.deepcopy(members[0]))
        if ident=='IR-13': value['members'][1]['depends_on']=['C']
        if ident=='IR-14': value['unknown']=True
        if ident=='IR-15': value['members'][0]['package']['package_digest']='0'*64
        ref=record(ROOT/'fixtures'/ident/'request.json',value)
        execute(ident,['intake-set','--request',ref['path'],'--request-sha256',ref['sha256']])
    record(ROOT/'results-summary.json',RESULTS)
    print(json.dumps([{'id':r['id'],'exit_code':r['exit_code'],'status':r['observation']['status']} for r in RESULTS],indent=2))

if __name__=='__main__':
    main()
