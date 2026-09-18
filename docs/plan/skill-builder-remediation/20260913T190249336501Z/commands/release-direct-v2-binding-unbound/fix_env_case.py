"""Apply independently reproduced F05 and retain exact before/after identity."""
import json
from evidence import RUN, PACKAGE, identity, dump, sha

before = identity()
assert before['package_digest'] == 'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099'
for row in before['files']:
    destination = RUN / 'source-before-env-fix' / row['path']
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('xb') as stream:
        stream.write((PACKAGE / row['path']).read_bytes())
path = PACKAGE / 'assets/adaptive-runtime/check_project_binding.py'
data = path.read_bytes()
assert data.count(b"p.startswith('.env')") == 1
path.write_bytes(data.replace(b"p.startswith('.env')", b"p.casefold().startswith('.env')"))
path = PACKAGE / 'references/project-binding.md'
data = path.read_bytes()
needle = b'This filename policy does not claim comprehensive secret detection.'
assert data.count(needle) == 1
path.write_bytes(data.replace(needle, b'Environment-file prefixes such as `.env`, `.ENV`, and `.Env.local` are also excluded case-insensitively before reads. ' + needle))
path = PACKAGE / 'package-manifest.json'
value = json.loads(path.read_text())
for name in value['artifacts']:
    value['artifacts'][name] = sha((PACKAGE / name).read_bytes())
path.write_bytes((json.dumps(value, ensure_ascii=False, indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
after = identity()
dump(RUN / 'env-fix-receipt.json', {'before':before, 'after':after, 'reason':'F05: reject native Windows case aliases of excluded environment-file prefixes before content reads.'})
print(after['package_digest'])
