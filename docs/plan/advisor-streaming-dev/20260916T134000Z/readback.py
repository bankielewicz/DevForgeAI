"""Read back publication and preservation boundaries without mutating source."""
import hashlib
import json
from pathlib import Path

ROOT = Path('C:/Projects/DevForgeAI')
HERE = Path(__file__).resolve().parent
def rows(root):
    return sorted([{'path':p.relative_to(root).as_posix(),'bytes':len(p.read_bytes()),
        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in root.rglob('*') if p.is_file()],
        key=lambda row:row['path'])
source = rows(ROOT/'src/agents/skills/advisor')
frozen = json.loads((HERE/'candidate-freeze.json').read_text())
assert source == sorted(frozen['files'],key=lambda row:row['path'])
canonical = hashlib.sha256(json.dumps(source,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
publication = json.loads((ROOT/'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming/publication-readback.json').read_text())
assert canonical == publication['package_digest']
before = json.loads((ROOT/'docs/plan/skill-authorings/advisor/20260916T134000Z-streaming-intake/preservation-before.json').read_text())
assert {r['path']:r['sha256'] for r in rows(ROOT/'.agents/skills/advisor')} == before['operational']
assert hashlib.sha256((ROOT/'advisor-test.ps1').read_bytes()).hexdigest() == before['example']['sha256']
value = {'source':str(ROOT/'src/agents/skills/advisor'),'files':source,'package_digest':canonical,
 'candidate_files_equal_publication':True,'operational_unchanged':True,'user_example_unchanged':True,
 'digest_algorithm':'SHA256 compact UTF8 JSON of path/bytes/sha256 rows sorted by case-sensitive relative POSIX path',
 'developer_freeze_ordering_note':'candidate-freeze.json used host Path sorting; its differently ordered digest is preserved. File maps match exactly; this digest uses the builder canonical ordering.'}
with (HERE/'final-readback.json').open('x',encoding='utf-8') as stream:
    json.dump(value,stream,indent=2)
    stream.write('\n')
print(json.dumps({'status':'PASS','files':len(source),'package_digest':canonical}))
