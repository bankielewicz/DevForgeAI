"""Expected byte identities from independently specified literal stimuli."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
pairs={
 'silent':(b'',b''),
 'config':(b'',b'Error: qa-settings:7:3: unknown configuration field `QA_CANARY_config_7391`\n'),
 'mcp':(b'',b'Error: invalid transport\nin `mcp_servers.QA_CANARY_transport_7391`\n'),
 'negative':(b'',b'NotError: invalid transport\nin `mcp_servers.QA_CANARY_negative_7391`\n'),
 'utf8':(b'\xff\nqa-last-line\xe2\x82',b'\xfe\n'),
 'flood':(b'',b'q'*700001),
 'argv':(json.dumps(['with space','quote"inside','trailing\\','日本語'],ensure_ascii=False,separators=(',',':')).encode()+b'\n',b''),
 'inherited-canary':(b'',b'Bearer sk-CANARY_SECRET_29417 arbitrary account/path/prompt CANARY_SECRET_29417'),
}
for n in [1048576,1048577]:pairs['line-'+str(n)]=(b'z'*n+b'\n',b'')
for n in [128,129]:pairs['queue-'+str(n)]=(b'\n'*n,b'')
for n in [8388608,8388609]:pairs['bytes-'+str(n)]=(b'',b'b'*n)
result={name:{stream:{'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for stream,b in zip(['stdout','stderr'],values)} for name,values in pairs.items()}
with (root/'expected.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({'oracles':len(result),'expected_sha256':hashlib.sha256((root/'expected.json').read_bytes()).hexdigest()}))

