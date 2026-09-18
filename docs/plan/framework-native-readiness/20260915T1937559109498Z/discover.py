"""Read-only native-readiness discovery; emits allowlisted settings, never credentials."""
import datetime,hashlib,json,os,platform,subprocess,sys,time,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
WORK=Path('C:/Projects/DevForgeAI')
HOME=Path('C:/Users/bryan/.codex')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=True)+'\n',encoding='utf-8')
def identity(p):return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
known=WORK/'docs/plan/framework-worker-qa/20260915T1901023951559Z-retest/selected-manifest.json'
rows=json.loads(known.read_text(encoding='utf-8-sig'))
write('candidate-before.json',[{**r,'matches':sha(r['path'])==r['sha256']} for r in rows])
assert all(sha(r['path'])==r['sha256'] for r in rows),'candidate drift'
config=HOME/'config.toml'
data=tomllib.loads(config.read_text(encoding='utf-8-sig'))
allowed=['model','model_provider','model_reasoning_effort','approval_policy','sandbox_mode','profile','forced_login_method','web_search','project_doc_fallback_filenames','project_root_markers']
safe={k:data[k] for k in allowed if k in data}
safe.update(config_identity=identity(config),top_level_keys=sorted(data),features=data.get('features',{}),windows=data.get('windows',{}))
safe['projects']={k:v for k,v in data.get('projects',{}).items() if 'devforgeai' in k.lower()}
safe['mcp_servers']={k:{'enabled':v.get('enabled','default'),'transport':'command' if 'command' in v else 'url' if 'url' in v else 'unknown','keys':sorted(v)} for k,v in data.get('mcp_servers',{}).items()}
safe['plugins']={k:{'enabled':v.get('enabled','default')} for k,v in data.get('plugins',{}).items() if isinstance(v,dict)}
safe['apps']={'keys':sorted(data.get('apps',{}))}
safe['profiles']={k:{a:b for a,b in v.items() if a in allowed or a in ['features','windows']} for k,v in data.get('profiles',{}).items()}
safe['additional_effect_keys']=[k for k in data if any(s in k for s in ['hook','notify','instruction','provider','permission','tool','exec','sandbox','credential','auth'])]
write('config-observations.json',safe)
paths=[HOME/'AGENTS.md',HOME/'AGENTS.override.md',config,HOME/'hooks.json',HOME/'requirements.toml',HOME/'managed_config.toml']
for base in [WORK,*WORK.parents,WORK/'docs',WORK/'docs/plan',WORK/'docs/plan/framework-native-readiness',ROOT,WORK/'docs/plan/framework-worker-trials']:
    paths += [base/'AGENTS.md',base/'AGENTS.override.md',base/'.codex/config.toml',base/'.codex/hooks.json',base/'.codex/requirements.toml']
for base in [HOME/'rules',WORK/'.codex/rules']:
    if base.exists():paths+=list(base.glob('*.rules'))
paths += [Path('C:/ProgramData/OpenAI/Codex')/f for f in ['config.toml','requirements.toml','hooks.json']]
write('profile-source-inventory.json',[identity(p) if p.is_file() else {'path':str(p),'exists':p.exists()} for p in dict.fromkeys(paths)])
captured=WORK/'devforgeai/experiments/codex-worker-probe/tests/fixtures/schema-command.json'
alias=Path(json.loads(captured.read_text())['executable']);physical=alias.resolve(strict=True)
chain=[]
for p in [alias,*alias.parents]:
    if p.is_junction() or p.is_symlink():chain.append({'path':str(p),'target':os.readlink(p),'resolved':str(p.resolve())})
current=HOME/'packages/standalone/current'
if current.is_junction() or current.is_symlink():chain.append({'path':str(current),'target':os.readlink(current),'resolved':str(current.resolve())})
write('launcher-identity.json',{'captured_alias':str(alias),'physical':identity(physical),'alias_sha256':sha(alias),'chain':chain})
write('environment.json',{'platform':platform.platform(),'python':sys.version,'python_executable':sys.executable,'cwd':str(Path.cwd()),'code_root':str(WORK),'credential_env_names_present':[k for k in os.environ if k in ['OPENAI_API_KEY','CODEX_API_KEY','AZURE_OPENAI_API_KEY','OPENAI_BASE_URL','OPENAI_API_BASE','CODEX_HOME']],'secret_values_retained':False,'git_metadata':(WORK/'.git').exists()})
for name,args in [('codex-version',['--version']),('codex-help',['--help']),('app-server-help',['app-server','--help'])]:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    p=subprocess.run([str(physical),*args],cwd=WORK,capture_output=True,timeout=20)
    (ROOT/(name+'.stdout.txt')).write_bytes(p.stdout);(ROOT/(name+'.stderr.txt')).write_bytes(p.stderr)
    write(name+'.receipt.json',{'argv':[str(physical),*args],'cwd':str(WORK),'start':start,'seconds':time.monotonic()-t,'exit':p.returncode,'executable_sha256':sha(physical),'stdout_sha256':sha(ROOT/(name+'.stdout.txt')),'stderr_sha256':sha(ROOT/(name+'.stderr.txt'))})
write('input-identities.json',[identity(WORK/p) for p in ['AGENTS.md','docs/specs/framework/runtime/codex-worker-feasibility-v1.md','docs/specs/framework/roadmap-and-decisions.md','docs/specs/framework/guardrails-and-rust-runtime.md','docs/plan/devforgeai-codex-rust-enforcement-design.md','docs/specs/framework/mvp/acceptance.md','devforgeai/experiments/codex-worker-probe/tests/fixtures/schema-command.json']])
print(json.dumps({'root':str(ROOT),'physical':str(physical),'settings':safe,'native_trial_launched':False},indent=2))
