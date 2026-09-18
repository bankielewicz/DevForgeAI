import datetime, hashlib, json, pathlib
R=pathlib.Path(__file__).resolve().parent
def write(p,v):
    dest=R/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def ref(p):return {'path':p,'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest()}
base={'schema_version':'1','run_id':R.name,'target_name':'skill-builder'}
sources=json.loads((R/'guidance-sources-selected.json').read_text())['sources']
for name in ['skill-builder-adoption-spec.md','skill-builder-enhancement-spec.md','claude-to-codex-skill-import-spec.md']:
    p='inputs/specs/'+name;sources.append({'source_id':name.removesuffix('.md'),'original_path':'C:/Projects/DevForgeAI/docs/plan/'+name,'retrieved_at_utc':None,'snapshot_path':p,'sha256':ref(p)['sha256'],'sections':['complete selected project specification'],'freshness':'snapshot_only'})
write('sources.json',{**base,'sources':sources})
rules=[]
for rid,title,authority,method,required,source,expected in [
 ('SB-FORMAT','Portable entrypoint and supported metadata','format_requirement','deterministic',True,'agent-skills','Parse valid name/description; supported optional fields; correct directory identity.'),
 ('SB-DISCLOSURE','Clear scope and resource routing','official_recommendation','semantic',True,'openai-skills','Core operation choices and conditional references are explicit; real links resolve.'),
 ('SB-WORKFLOW','Complete preserved operation paths','project_policy','semantic',True,'skill-builder-adoption-spec','Import/specification/regeneration/adoption branches have concrete inputs, effects, recovery and terminal results.'),
 ('SB-CONSISTENCY','Consistent completion instructions','project_policy','semantic',True,'skill-builder-adoption-spec','Completion guidance preserves every required forward-trial family, including adoption lineage.'),
 ('SB-CUSTODY','Evidence and history remain distinct','project_policy','deterministic',True,'skill-builder-adoption-spec','Actual current hashes match selected prior bytes; enhancement evidence is not generated/adopted history.'),
 ('SB-BEHAVIOR','Bounded independent behavioral evidence','project_policy','behavioral',True,'skill-builder-adoption-spec','Verified retained evaluator inputs/cases/results support declared tested behaviors; unexecuted current task coverage remains explicit.'),
 ('SB-COLD','Fresh minimal-input task execution','project_policy','behavioral',True,'skill-builder-adoption-spec','Execute selected target workflow from minimal inputs only when authorized; otherwise NOT_RUN.'),
 ('SB-AUTONOMY','Preserve authority and actual permissions','project_policy','semantic',True,'skill-builder-enhancement-spec','No forced repeated permission ritual, fictitious task isolation, Python authority, installation or unavailable execution.'),
 ('SB-NATIVE','Native implicit activation','official_recommendation','behavioral',False,'openai-skills','Observe actual host selection, distinct from independent classification; outside this task.'),
 ('SB-MODEL','Model/API conditional advice','official_recommendation','semantic',False,'openai-skills','No API-specific constraint is imposed on this instruction-only orchestrating skill.')]:
    s=next(x for x in sources if x['source_id']==source)
    rules.append({'rule_id':rid,'revision':'2026-09-12.1','title':title,'source_refs':[{'path':s['snapshot_path'],'sha256':s['sha256'],'source_id':source,'locator':'Complete selected specification' if authority=='project_policy' else 'Frontmatter and progressive disclosure'}],'authority_class':authority,'applicability':'not_applicable' if rid=='SB-MODEL' else 'applicable','method':method,'expected_observation':expected,'required':required,'limitation':'Selected dated snapshot and bounded development observations only; no universal current-live or enforcement claim.'})
write('rule-set.json',{**base,'selected_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selection_timing':'Pinned before deterministic execution and final results; initial semantic intake had already read the selected contracts. No prior expectation file was retained for the independent classification; it is exploratory evidence only.','rules':rules})
for cid,argv,expected in [
 ('structure',['python','-B','-X','utf8',str(R/'inputs/validator/scripts/observe.py'),'structure','--source',str(R/'source')],'exit 0; supported metadata and local links observed without required mismatches'),
 ('installed-checker',['python','-B','-X','utf8','C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py',str(R/'source')],'exit 0; installed checker reports Skill is valid; limited structural coverage')]:
    write('trials/'+cid+'/plan.json',{**base,'case_id':cid,'requirement_ids':['SB-FORMAT','SB-DISCLOSURE'],'fixture_references':[ref('source-manifest.json'),ref('inputs/validator-manifest.json'),ref('inputs/quick_validate.py')],'expected_outputs':expected,'expected_effects':'No source/checker/package changes; stdout/stderr and attempt records only under run','executor':'Python subprocess launched by assessment task','command':argv,'timeout_seconds':120,'permitted_write_root':str(R)})
write('trials/cold-task/plan.json',{**base,'case_id':'cold-task','requirement_ids':['SB-COLD'],'fixture_references':[ref('source-manifest.json')],'expected_outputs':'NOT_RUN: user prohibits invoking skill-builder workflows','executor':'Host Codex task runner is available; required target execution excluded by authorization','command':None,'timeout_seconds':120,'permitted_write_root':str(R)})
print('Rule set, source records and deterministic plans pinned.')
