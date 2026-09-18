import json
import re
from pathlib import Path
from record import ROOT, PACKAGE, write, sha

summary={}
inventory=json.loads((ROOT/'test-inventory.json').read_text())
for name in ['01-tests','04-coverage']:
    text=(ROOT/name/'stdout.txt').read_text()
    observed=dict(re.findall(r'^test (\w+) \.\.\. (ok|FAILED|ignored)$',text,re.M))
    entries=[{**x,'result':observed.get(x['name'],'NOT_RUN')} for x in inventory]
    summary[name]={'entries':entries,'passed':sum(x['result']=='ok' for x in entries),'total':len(entries),
       'mandatory_passed':sum(x['result']=='ok' and x['category']=='mandatory' for x in entries),
       'supplemental_passed':sum(x['result']=='ok' and x['category']=='supplemental' for x in entries),
       'unit_passed':sum(x['result']=='ok' and x['level']=='unit' for x in entries)}
coverage=json.loads((ROOT/'coverage.json').read_text())
selected=[]
outside=[]
prefix=str(PACKAGE/'src').replace('\\','/').lower()+'/'
for data in coverage['data']:
    for f in data['files']:
        filename=f['filename'].replace('\\','/')
        if filename.lower().startswith(prefix):
            selected.append({'file':filename,'lines':f['summary']['lines'],'branches':f['summary'].get('branches'),
               'sha256':sha(filename),'uncovered_segments':[s for s in f['segments'] if s[2]==0 and s[3]]})
        else:outside.append(filename)
covered=sum(x['lines']['covered'] for x in selected)
count=sum(x['lines']['count'] for x in selected)
summary['coverage']={'covered':covered,'count':count,'percentage':100*covered/count,'meets_floor':covered*100>=count*95,
                    'files':selected,'outside_denominator':outside,'branches':'NOT_RUN (unstable collector option; not selected)'}
write('metrics.json',summary)
print(json.dumps({k:{a:b for a,b in v.items() if a not in ['entries','files','outside_denominator']} for k,v in summary.items()}))
