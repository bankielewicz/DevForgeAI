import json
from pathlib import Path
from qa_harness import RUN,TARGET,execute,save,inventory,sha
from independent_probes import ref,write,js
base=RUN/'trials/budget-drift'; base.mkdir(parents=True,exist_ok=True)
results=[]
for cid,kind,expected in [('C01','token-null',0),('C02','token-false-pass',1),('C03','repeated-bytes',0),('C04','excerpt-bytes',0)]:
    root=base/cid; data=root/'inputs/excerpt.txt'; write(data,'é\n')
    budget={'unit':'tokens' if kind.startswith('token') else 'bytes','scope':'entrypoint' if kind.startswith('token') else 'observed_total_loads','maximum':5,'case_id':None if kind.startswith('token') else 'load-case','source':ref(data)}
    context={'tokenizer':None,'files':[{'path':'SKILL.md','bytes':3,'characters':2,'lines':1,'tokens':None}],'loads':[],'budget':budget,'budget_result':'PASS' if kind=='token-false-pass' else 'FAIL' if kind=='repeated-bytes' else 'NOT_RUN','reason':'Independent synthetic count oracle.'}
    if not kind.startswith('token'): context['loads']=[{'case_id':'load-case','path':'SKILL.md','occurrences':2,'basis':'observed_full_file' if kind=='repeated-bytes' else 'observed_excerpt','tokens':None,'evidence':[ref(data)]}]
    v={'schema_version':'adaptive-observations-v1','run_id':cid,'target_digest':'a'*64,'unicode_candidates':[],'resources':[],'edges':[],'context':context,'bindings':[],'limitations':['Synthetic arithmetic only; no measured host tokens.']}
    js(root/'adaptive-observations.json',v)
    save(root/'inputs/expectation.json',{'expected_exit':expected,'oracle':'null token budget NOT_RUN; repeated three-byte full files cost six bytes; excerpts cannot be substituted as full loads.'})
    r=execute(cid,['python','-B','-X','utf8',str(TARGET/'scripts/adaptive_observe.py'),'records','--run-root',str(root)])
    results.append({'id':cid,'expected_exit':expected,'actual_exit':r['exit_status'],'matched':expected==r['exit_status']})
source=base/'drift/source-skill'; write(source/'SKILL.md','---\nname: source-skill\ndescription: Return local input.\n---\nReturn it.\n')
execute('D01-snapshot',['python','-B','-X','utf8',str(TARGET/'scripts/observe.py'),'snapshot','--source',str(source),'--output',str(base/'drift/capture')])
save(base/'drift/expectation.json',{'expected':'SOURCE_CHANGED after a new file; old snapshot remains unchanged; changed-input resume must start fresh linked run','original':inventory(source)})
write(source/'changed.md','Late synthetic edit by harness.\n')
r=execute('D02-readback',['python','-B','-X','utf8',str(TARGET/'scripts/observe.py'),'readback','--source',str(source),'--manifest',str(base/'drift/capture/source-manifest.json')])
results.append({'id':'D02','expected_exit':1,'actual_exit':r['exit_status'],'matched':r['exit_status']==1})
save(base/'results.json',results)
print(results)
