"""Final readback, syntax, local links, schema preservation and artifact hashes."""
import ast
import difflib
import json
import re
import sys
from urllib.parse import unquote
from evidence import RUN, ROOT, PACKAGE, identity, dump, sha

label = sys.argv[1]
folder = RUN / label
folder.mkdir(exist_ok=False)
current = identity()
original = json.loads((RUN/'initial-receipt.json').read_text())
assert current['specifications'] == original['specifications']
old = {r['path']:r for r in original['files']}
new = {r['path']:r for r in current['files']}
changed = sorted(n for n in new if old.get(n) != new[n])
assert not set(old)-set(new)
assert set(changed) == {'scripts/adaptive.py','scripts/authoring.py','scripts/record_schema.py','assets/adaptive-runtime/check_project_binding.py','references/project-binding.md','package-manifest.json'}
assert all(new[n] == old[n] for n in old if n.startswith('schemas/'))
missing = []
parsed = {'python':[], 'json':[]}
for name in new:
    path=PACKAGE/name
    if name.endswith('.py'):
        ast.parse(path.read_text(encoding='utf-8'), filename=name)
        parsed['python'].append(name)
    if name.endswith('.json'):
        json.loads(path.read_text(encoding='utf-8'))
        parsed['json'].append(name)
    if name.endswith('.md'):
        for target in re.findall(r'\]\(([^\s)]+)\)', path.read_text(encoding='utf-8')):
            if target.startswith(('https:','http:','#','mailto:')):continue
            rel=unquote(target.split('#')[0])
            if rel and not (path.parent/rel).exists():missing.append({'source':name,'target':target})
assert not missing,missing
package_manifest=json.loads((PACKAGE/'package-manifest.json').read_text())
assert set(package_manifest['artifacts'])==set(new)-{'package-manifest.json'}
assert all(package_manifest['artifacts'][n]==new[n]['sha256'] for n in package_manifest['artifacts'])
for name in changed:
    prior=(RUN/'source-before'/name).read_text(encoding='utf-8') if name in old else ''
    now=(PACKAGE/name).read_text(encoding='utf-8')
    diff=''.join(difflib.unified_diff(prior.splitlines(keepends=True),now.splitlines(keepends=True),fromfile='before/'+name,tofile='after/'+name))
    target=folder/'diffs'/(name+'.diff')
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(diff,encoding='utf-8')
dump(folder/'receipt.json', dict(current,changed_files=changed,removed_files=[],schemas_unchanged=True,syntax=parsed,missing_local_links=missing,artifact_hashes='MATCH',scope='Development builder only; no installation or Rust qualification'))
print(json.dumps({'digest':current['package_digest'],'files':len(new),'changed':changed,'python_parsed':len(parsed['python']),'json_parsed':len(parsed['json']),'local_links':'PASS','artifact_hashes':'MATCH','specifications':'UNCHANGED'}))
