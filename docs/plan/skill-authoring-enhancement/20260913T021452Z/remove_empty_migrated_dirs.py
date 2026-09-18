from pathlib import Path
import json
RUN = Path(__file__).resolve().parent
target = (RUN.parents[3] / 'src/agents/skills/skill-builder').resolve()
removed=[]
for name in ('evals','tests'):
    root=(target/name).resolve()
    assert root.is_relative_to(target) and root != target
    if not root.exists():
        continue
    dirs=[p for p in root.rglob('*') if p.is_dir()] + [root]
    for p in sorted(dirs,key=lambda p:len(p.parts),reverse=True):
        assert p.resolve().is_relative_to(target)
        if p.is_symlink() or any(p.iterdir()):
            raise ValueError('not a plain empty migrated directory: '+str(p))
        p.rmdir()
        removed.append(str(p))
(RUN/'removed-empty-migrated-directories.json').write_text(json.dumps({'removed':removed,'method':'Nonrecursive rmdir after resolved descendant and empty checks; file manifests unchanged.'},indent=2))
print(json.dumps({'removed_empty_directories':len(removed)}))
