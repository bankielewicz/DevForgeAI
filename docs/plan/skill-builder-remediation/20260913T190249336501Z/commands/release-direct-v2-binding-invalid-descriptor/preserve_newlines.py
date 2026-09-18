"""Restore original CRLF convention and refresh only the package artifact index."""
import json
from evidence import RUN, PACKAGE, identity, dump, sha

before=identity()
assert before['package_digest']=='464acfdce47c7784062c488ad75f6b31adf303ba1f3cb12143ef76842ff6a926'
snapshot=RUN/'source-interim-01'
for row in before['files']:
    path=snapshot/row['path']
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as stream:stream.write((PACKAGE/row['path']).read_bytes())
path=PACKAGE/'scripts/authoring.py'
data=path.read_bytes().replace(b'\r\n',b'\n').replace(b'\n',b'\r\n')
path.write_bytes(data)
path=PACKAGE/'package-manifest.json'
value=json.loads(path.read_text())
for name in value['artifacts']:
    value['artifacts'][name]=sha((PACKAGE/name).read_bytes())
path.write_bytes((json.dumps(value,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8'))
after=identity()
dump(RUN/'newline-refresh-receipt.json',{'before':before,'after':after,'reason':'Preserve original CRLF convention in authoring.py and package-manifest.json; no semantic edits.'})
print(after['package_digest'])
