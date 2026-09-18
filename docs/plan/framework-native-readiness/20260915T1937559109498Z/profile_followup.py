"""Sanitized static profile extension inventory. Does not activate extensions."""
import hashlib,json,tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parent
HOME=Path('C:/Users/bryan/.codex')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cfg=tomllib.loads((HOME/'config.toml').read_text(encoding='utf-8-sig'))
out=[]
for label,settings in cfg.get('plugins',{}).items():
    if not settings.get('enabled',True):continue
    name,market=label.split('@',1)
    base=HOME/'plugins/cache'/market/name
    roots=sorted(base.iterdir()) if base.exists() else []
    entries=[]
    for root in roots:
        manifest=root/'.codex-plugin/plugin.json'
        if not manifest.is_file():continue
        data=json.loads(manifest.read_text(encoding='utf-8-sig'))
        hooks=data.get('hooks')
        default=root/'hooks/hooks.json'
        files=[manifest]+([default] if default.exists() else [])
        for value in hooks if isinstance(hooks,list) else [hooks]:
            if isinstance(value,str) and value.startswith('./'):
                p=(root/value).resolve()
                if p.is_relative_to(root.resolve()) and p.is_file():files.append(p)
        entries.append({'root':str(root),'manifest_keys':sorted(data),'declares_hooks':hooks is not None,'default_hook_exists':default.exists(),'declares_mcp':'mcpServers' in data,'declares_apps':'apps' in data,'identities':[{'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size} for p in dict.fromkeys(files)]})
    out.append({'plugin':label,'cached_versions':entries,'effective_version':'NOT_OBSERVED; no app-server started'})
def rule_summary():
    p=HOME/'rules/default.rules';t=p.read_text()
    return {'path':str(p),'sha256':sha(p),'bytes':p.stat().st_size,'prefix_rule_lines':sum('prefix_rule(' in x for x in t.splitlines()),'allow_lines':sum('decision="allow"' in x or "decision='allow'" in x for x in t.splitlines()),'scope':'Existing exec permissions; not proof MCP or hooks are contained. Full source not copied.'}
result={'plugins':out,'rules':rule_summary(),'mcp':{k:{'command':v.get('command'),'argument_count':len(v.get('args',[])),'argument_file_paths':[a for a in v.get('args',[]) if isinstance(a,str) and Path(a).is_absolute() and Path(a).is_file()],'environment_names':sorted(v.get('env',{})),'enabled':v.get('enabled',True)} for k,v in cfg.get('mcp_servers',{}).items()},'shell_environment_policy_keys':sorted(cfg.get('shell_environment_policy',{})),'credential_contents_read':False}
(ROOT/'extension-observations.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'plugins':len(out),'cached_versions':sum(len(x['cached_versions']) for x in out),'hook_bundles':sum(x['declares_hooks'] or x['default_hook_exists'] for p in out for x in p['cached_versions']),'mcp':result['mcp'],'rules':result['rules']},indent=2))
