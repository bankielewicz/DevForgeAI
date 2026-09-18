"""Bind actual maintenance changes and check preservation/local links."""
import ast
import difflib
import hashlib
import json
from pathlib import Path
import re
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'
sys.path.insert(0, str(PACKAGE / 'scripts'))
import authoring as a

def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

before = json.loads((RUN / 'before-manifest.json').read_bytes())
manifest_path = PACKAGE / 'package-manifest.json'
manifest = json.loads(manifest_path.read_bytes())
manifest['artifacts'] = {p: h for p, h in inventory(PACKAGE).items() if p != 'package-manifest.json'}
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
after = inventory(PACKAGE)
changes = {p: {'before': before.get(p), 'after': after.get(p)}
           for p in sorted(set(before) | set(after)) if before.get(p) != after.get(p)}
allowed = {'SKILL.md', 'scripts/authoring.py', 'package-manifest.json',
    'assets/authoring-design-template.json', 'assets/build-report-template.md',
    'schemas/authoring-design.schema.json', 'references/workflow-design.md',
    'references/authoring.md', 'references/spec-build.md', 'references/evidence-format.md',
    'references/regeneration.md', 'references/validation-handoff.md'}
assert set(changes) <= allowed, set(changes) - allowed
protected = json.loads((RUN / 'preservation-before.json').read_bytes())
preserved = {path: inventory(Path(path)) == expected for path, expected in protected.items()}
assert all(preserved.values()), preserved
links = []
for path in PACKAGE.rglob('*.md'):
    for match in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        target = match.group(1).split('#')[0]
        if not target or '://' in target or target.startswith('mailto:'):
            continue
        destination = path.parent / target
        assert destination.exists(), (path, target)
        links.append({'source': str(path.relative_to(PACKAGE)), 'target': target})
python_files = list(PACKAGE.rglob('*.py'))
for path in python_files:
    ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
json_files = list(PACKAGE.rglob('*.json'))
for path in json_files:
    a.parse(path.read_bytes())
patch = []
for name in changes:
    old_path, new_path = RUN / 'before/skill-builder' / name, PACKAGE / name
    old = old_path.read_text(encoding='utf-8').splitlines(keepends=True) if old_path.exists() else []
    new = new_path.read_text(encoding='utf-8').splitlines(keepends=True) if new_path.exists() else []
    patch.extend(difflib.unified_diff(old, new, fromfile='before/' + name, tofile='after/' + name))
(RUN / 'changes.patch').write_text(''.join(patch), encoding='utf-8')
(RUN / 'changes.json').write_text(json.dumps(changes, indent=2), encoding='utf-8')
(RUN / 'delivered-manifest.json').write_text(json.dumps(a.manifest(a.files(PACKAGE)), indent=2), encoding='utf-8')
result = {'changed_files': len(changes), 'preserved': preserved, 'local_links': len(links),
    'python_syntax_files': len(python_files), 'strict_json_files': len(json_files),
    'manifest_matches_bytes': manifest['artifacts'] == {p: h for p, h in after.items() if p != 'package-manifest.json'},
    'unchanged_existing_files': sum(before.get(p) == h for p, h in after.items()),
    'package_digest': a.manifest(a.files(PACKAGE))['package_digest']}
(RUN / 'static-checks.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
