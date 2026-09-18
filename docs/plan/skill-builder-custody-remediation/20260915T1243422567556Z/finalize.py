"""Readback and static maintenance evidence; no acceptance authority."""
import ast
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
PACKAGE = ROOT / 'src/agents/skills/skill-builder'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def inventory(root):
    rows = []
    pending = [root]
    while pending:
        for path in pending.pop().iterdir():
            info = path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                rows.append({'path': path.relative_to(root).as_posix(), 'skipped': 'link_or_junction'})
            elif path.is_dir():
                pending.append(path)
            elif path.is_file():
                data = path.read_bytes()
                rows.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': sha(data)})
    return sorted(rows, key=lambda row: row['path'])


def save(name, value):
    path = RUN / name
    if path.exists():
        raise ValueError('fresh output required: ' + str(path))
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


before = inventory(RUN / 'before')
after = inventory(PACKAGE)
shutil.copytree(PACKAGE, RUN / 'delivered')
if inventory(RUN / 'delivered') != after:
    raise ValueError('delivered snapshot differs from selected source')
save('source-before-manifest.json', before)
save('source-after-manifest.json', after)
old = {row['path']: row['sha256'] for row in before}
new = {row['path']: row['sha256'] for row in after}
changed = sorted(path for path in set(old) | set(new) if old.get(path) != new.get(path))
allowed = {'scripts/authoring.py', 'references/authoring.md', 'references/evidence-format.md',
           'references/regeneration.md', 'package-manifest.json'}
patch = []
for path in changed:
    patch.extend(difflib.unified_diff((RUN / 'before' / path).read_text(encoding='utf-8').splitlines(True),
        (PACKAGE / path).read_text(encoding='utf-8').splitlines(True), fromfile='before/' + path,
        tofile='after/' + path))
(RUN / 'changes.patch').write_text(''.join(patch), encoding='utf-8')
save('changes.json', {'changed_paths': changed, 'allowed_paths': sorted(allowed),
    'scope_preserved': set(changed) <= allowed,
    'package_digest': sha(json.dumps(after, ensure_ascii=False, separators=(',', ':')).encode())})
manifest = json.loads((PACKAGE / 'package-manifest.json').read_bytes())['artifacts']
actual = {k: v for k, v in new.items() if k != 'package-manifest.json'}
links = []
for path in PACKAGE.rglob('*.md'):
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
        local = target.split('#')[0]
        if local and '://' not in local and not (path.parent / local).exists():
            links.append({'source': str(path), 'target': target})
syntax = []
for path in PACKAGE.rglob('*.py'):
    try:
        ast.parse(path.read_text(encoding='utf-8'))
    except SyntaxError as exc:
        syntax.append({'path': str(path), 'error': str(exc)})
command = [sys.executable, '-B', '-X', 'utf8',
    r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py', str(PACKAGE)]
result = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=120)
save('static-checks.json', {'manifest_exact': manifest == actual, 'missing_links': links,
    'python_syntax_errors': syntax, 'quick_validate': {'argv': command, 'cwd': str(ROOT),
    'exit_code': result.returncode, 'stdout': result.stdout.decode('utf-8'),
    'stderr': result.stderr.decode('utf-8')}})
prior = ROOT / 'docs/plan/skill-creator-reviews/skill-builder/20260915T1233215519782Z'
op_before = json.loads((prior / 'operational-before.json').read_bytes())['files']
save('preservation.json', {
    'operational_matches_pre_repair_review': inventory(ROOT / '.agents/skills/skill-builder') == op_before,
    'selected_revision_spec_unchanged': (RUN / 'revision-spec.md').read_bytes() ==
        (ROOT / 'docs/plan/skill-validations/skill-builder/20260914T2131571597777Z/revision-spec.md').read_bytes(),
    'only_selected_development_paths_changed': set(changed) <= allowed})
save('readback.json', {'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'source_files': len(after), 'changed_paths': changed, 'static_pass': manifest == actual and not links and not syntax and result.returncode == 0})
save('artifact-manifest.json', inventory(RUN))
print(json.dumps({'changed_paths': changed, 'source_files': len(after), 'static_pass': manifest == actual and not links and not syntax and result.returncode == 0}))
