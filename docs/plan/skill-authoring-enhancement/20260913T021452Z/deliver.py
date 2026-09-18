"""Apply the verified enhancement using the new custody workflow."""
import json
from pathlib import Path
import sys
RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
sys.dont_write_bytecode = True
sys.path.insert(0,str(RUN / 'candidate/skill-builder/scripts'))
import authoring as a
result = json.loads((RUN / 'checks-004/result.json').read_text())
assert result['successful'] and result['skipped']==0
structural = json.loads((RUN / 'structural-002/result.json').read_text())
assert all(r['exit_code']==0 for r in structural)
for name in ('skill-builder','skill-validator'):
    current = a.files(RUN / 'candidate' / name)
    assert current == a.files(RUN / 'checks-004/input-packages' / name)
    assert current == a.files(RUN / 'structural-002/input-packages' / name)
    delivery = RUN / 'authoring' / name
    candidate = delivery / 'candidate'
    for p in a.files(candidate):
        if p not in current:
            a.child(candidate,p).unlink()
    for p,d in current.items():
        path = a.child(candidate,p)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(d)
    assert a.files(candidate)==current
    a.save(RUN / (name+'-delivery-command.json'),{'command':[sys.executable,'-B','-X','utf8',str(RUN / 'candidate/skill-builder/scripts/authoring.py'),'publish','--run-root',str(delivery)],'executor':'skill-creator enhancement author using custody helper','input_manifest':a.manifest(current),'expected':'Exact authorized staged changes; actual applied delta and publication readback; authoring-only provenance'})
    observed = a.publish(delivery)
    a.save(RUN / (name+'-delivery-result.json'),observed)
    print(json.dumps({'target':name,**observed}))
    if observed['state']!='AUTHORED':
        sys.exit(1)
    actual = a.files(ROOT / 'src/agents/skills' / name)
    assert actual==current
    a.save(RUN / (name+'-actual-delivered-manifest.json'),a.manifest(actual))
print('Both development packages delivered; exact delivered bytes match tested snapshots.')
