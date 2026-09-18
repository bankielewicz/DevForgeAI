from pathlib import Path
import hashlib,json,re
p=Path(r'C:\Projects\DevForgeAI\devforgeai\experiments\codex-worker-probe-logging')
f=p/'src/restrictive-launch-policy.json'; old=json.loads(f.read_bytes()); new=json.loads(f.read_bytes())
new['policy_id']='codex-0.154.0-readonly-no-external-tools-v3'
count=0
for i,s in enumerate(new['argv']):
    updated,n=re.subn(r'^(mcp_servers|plugins|apps)\."([A-Za-z0-9_@-]+)"\.enabled=false$',r'\1.\2.enabled=false',s)
    count+=n; new['argv'][i]=updated
assert count==15 and len(new['argv'])==116
data=(json.dumps(new,indent=2)+'\n').encode(); f.write_bytes(data); sha=hashlib.sha256(data).hexdigest()
for name in ['tests/launch_policy.rs','tests/runtime_edges.rs']:
    f=p/name; s=f.read_text().replace('readonly-no-external-tools-v2','readonly-no-external-tools-v3').replace('1dbc48c4a3627f7c5fc7a996935ec507426e4cd90adac058eb81100ac9b526b5',sha)
    s=re.sub(r'(mcp_servers|plugins|apps)\.\\"([A-Za-z0-9_@-]+)\\"\.enabled=false',r'\1.\2.enabled=false',s)
    if name=='tests/launch_policy.rs': s=s.replace('("codex-0.154.0-stdio", 3, id, sha.as_str()),','("codex-0.154.0-stdio", 4, id, sha.as_str()),')
    f.write_text(s,encoding='utf-8',newline='\n')
print(json.dumps({'corrections':count,'new_policy_sha256':sha}))
