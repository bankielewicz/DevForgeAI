"""Prepare non-runnable trial proposals and unqualified review records; no launch."""
import hashlib,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Projects/DevForgeAI')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2)+'\n')
identity=read(ROOT/'launcher-identity.json');settings=read(ROOT/'config-observations.json')
args=['app-server','--listen','stdio://','--strict-config']
overrides={'model_provider':'openai','forced_login_method':'chatgpt','web_search':'disabled','features.memories':False,'apps._default.enabled':False}
for k in settings['mcp_servers']:overrides['mcp_servers.'+json.dumps(k)+'.enabled']=False
for k in settings['plugins']:overrides['plugins.'+json.dumps(k)+'.enabled']=False
for k in settings['apps']['keys']:overrides['apps.'+json.dumps(k)+'.enabled']=False
for k,v in overrides.items():args+=['-c',k+'='+json.dumps(v)]
policy={'policy_id':'codex-0.154.0-readonly-no-external-tools-v1','status':'PROPOSED_NOT_VERSION_QUALIFIED','executable':identity['physical']['path'],'argv':args,'persistent_config_writes':False,'unknown_keys':'reject; --strict-config','remaining':'Verify per-key pinned-version support and effective disablement; unresolved hook/managed sources block launch.'}
write(ROOT/'restrictive-launch-policy.proposed.json',policy)
source=[{'path':x['path'],'sha256':x['sha256']} for x in read(ROOT/'profile-source-inventory.json') if 'sha256' in x]
for plugin in read(ROOT/'extension-observations.json')['plugins']:
    for version in plugin['cached_versions']:
        source += [{'path':x['path'],'sha256':x['sha256']} for x in version['identities']]
source=list({x['path']:x for x in source}.values())
fixed=WORK/'docs/specs/framework/runtime/fixtures/codex-worker-v1'
records=[]
for code,scenario in [('WN-01','complete'),('WN-02','cancel')]:
    base=ROOT/'trials'/code;base.mkdir(parents=True,exist_ok=True)
    destination=WORK/'docs/plan/framework-worker-trials'/(ROOT.name+'-'+code)
    review={'schema_version':1,'reviewer':'Codex static readiness preparation; NOT a qualified operator review','trial_selection_ref':str(ROOT/'trial-selection.proposed.md'),'codex_sha256':identity['physical']['sha256'],'checkout_root':str(destination/'fixture'),'model':settings['model'],'effort':settings['model_reasoning_effort'],'profile_sources':source,'findings':{'native_read_only_available':False,'no_external_tool_or_hook_effects':False,'codex_managed_chatgpt':False,'no_custom_provider':False}}
    write(base/'profile-review.unqualified.json',review)
    request={'schema_version':1,'project_id':'DevForgeAI','checkout_id':'worker-native-'+code,'work_id':'worker-feasibility-'+code,'run_id':ROOT.name+'-'+code,'candidate_sha256':sha(fixed/'task.json'),'checkout_root':str(destination/'fixture'),'run_dir':str(destination/'run'),'worker_executable':identity['physical']['path'],'worker_sha256':identity['physical']['sha256'],'adapter':'codex-0.154.0-stdio','scenario':scenario,'profile':{'model':settings['model'],'effort':settings['model_reasoning_effort'],'review_ref':str(base/'profile-review.unqualified.json'),'review_sha256':sha(base/'profile-review.unqualified.json')}}
    write(base/'request.draft.json',request)
    for name in ['task.json','prompt.txt','expected.json','output-schema.json']:shutil.copyfile(fixed/name,base/name)
    records.append({'id':code,'status':'BLOCKED_NOT_RUN','request':str(base/'request.draft.json'),'profile':'UNQUALIFIED','proposed_fixture':str(destination/'fixture'),'proposed_run':str(destination/'run'),'dispatch_seconds':120,'rpc_seconds':10,'grace_seconds':5,'teardown_seconds':5,'external_safety_seconds':145,'turns':1,'automatic_retries':0,'selected_model':settings['model'],'selected_effort':settings['model_reasoning_effort'],'model_selection_status':'PROPOSED_FROM_CURRENT_CONFIG; user selection and protocol availability not observed'})
write(ROOT/'native-trial-inventory.json',records)
print(json.dumps({'drafts':len(records),'native_launched':False,'override_count':len(overrides),'profile_sources':len(source)}))
