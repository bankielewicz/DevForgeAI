"""Independent focused evidence harness. No candidate imports; no repairs."""
import datetime as dt
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import stat
import subprocess
import sys
import time

RUN = Path(__file__).absolute().parent
ROOT = Path('C:/Projects/DevForgeAI')
TARGET = ROOT / 'src/agents/skills/skill-validator'
LOADED = ROOT / '.agents/skills/skill-validator'
PRIOR = ROOT / 'docs/plan/skill-validations/skill-validator/20260913T152602912596Z'
CHECKER = Path('C:/Users/bryan/.codex/skills/.system/skill-creator/scripts/quick_validate.py')
EXPECTED = 'd51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1'
SPECS = {'skill-validator-adaptive-enhancement-spec.md': 'f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42', 'skill-builder-adaptive-enhancement-spec.md': '8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59'}

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')

def compact(v):
    return json.dumps(v, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def safe(p):
    p = Path(os.path.abspath(p))
    if '..' in p.parts:
        raise ValueError('Traversal')
    for a in reversed((p, *p.parents)):
        if os.path.lexists(a):
            s = a.lstat()
            if stat.S_ISLNK(s.st_mode) or getattr(s, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Link/reparse boundary: ' + str(a))
    return p

def read(p):
    p = safe(p)
    before = p.stat()
    if not stat.S_ISREG(before.st_mode) or before.st_size > 32 * 1024 * 1024:
        raise ValueError('Special/oversize file')
    b = p.read_bytes()
    after = p.stat()
    if (before.st_size, before.st_mtime_ns, before.st_ino) != (after.st_size, after.st_mtime_ns, after.st_ino):
        raise ValueError('Read drift')
    return b

def write(p, b):
    p = safe(p)
    p.relative_to(RUN)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open('xb') as f:
        f.write(b.encode('utf-8') if isinstance(b, str) else b)
    return p

def save(p, v):
    return write(p, json.dumps(v, ensure_ascii=False, indent=2, allow_nan=False) + '\n')

def ref(p, base=None):
    return {'path': p.relative_to(base).as_posix() if base else str(p), 'sha256': sha(read(p))}

def excluded(name):
    s = name.lower()
    return (s in {'devforgeai_cli', '.git', '__pycache__', 'node_modules', '.venv', 'venv', 'target', 'dist', 'build'}
            or re.search(r'(?:^|[-_.])backups?(?:$|[-_.])', s)
            or s.endswith(('.bak', '.backup', '~')))

def inventory(root):
    root = safe(root)
    pending, rows, omissions, total = [root], [], [], 0
    while pending:
        entries = sorted(pending.pop().iterdir(), key=lambda p: p.name)
        for p in entries:
            rel = p.relative_to(root).as_posix()
            if excluded(p.name):
                omissions.append(rel)
                continue
            safe(p)
            s = p.lstat()
            if stat.S_ISDIR(s.st_mode):
                pending.append(p)
            elif stat.S_ISREG(s.st_mode):
                if any(x in ('', '.', '..') for x in rel.split('/')) or ':' in rel or '\\' in rel:
                    raise ValueError('Invalid package path')
                total += s.st_size
                if len(rows) >= 2000 or total > 32 * 1024 * 1024:
                    raise ValueError('Capture ceiling exceeded')
                b = read(p)
                rows.append({'path': rel, 'bytes': len(b), 'sha256': sha(b)})
            else:
                raise ValueError('Special file')
    rows.sort(key=lambda r: r['path'])
    return {'schema_version': '1', 'root': str(root), 'captured_at_utc': now(), 'files': rows,
            'excluded_boundaries': omissions, 'complete': not omissions, 'package_digest': sha(compact(rows))}

def execute(cid, argv, fixture=None, timeout=120):
    dest = RUN / 'commands' / cid
    dest.mkdir(parents=True, exist_ok=False)
    before = inventory(fixture) if fixture else None
    temp = RUN / 'temporary' / cid
    temp.mkdir(parents=True, exist_ok=False)
    env = os.environ.copy()
    env.update(TMP=str(temp), TEMP=str(temp), PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    start, tick = now(), time.monotonic()
    save(dest / 'plan.json', {'argv': list(map(str, argv)), 'cwd': str(ROOT), 'started_at': start,
         'timeout_seconds': timeout, 'fixture_before': before, 'permitted_effects': [str(temp), str(dest)],
         'environment_overrides': {k: env[k] for k in ('TMP','TEMP','PYTHONDONTWRITEBYTECODE','PYTHONUTF8')}})
    timed_out, termination = False, None
    with (dest / 'stdout.txt').open('xb') as out, (dest / 'stderr.txt').open('xb') as err:
        proc = subprocess.Popen(list(map(str, argv)), cwd=ROOT, env=env, stdout=out, stderr=err, shell=False)
        try:
            code = proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            killed = subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True, timeout=15)
            termination = {'exit': killed.returncode, 'stdout': killed.stdout.decode(errors='replace'), 'stderr': killed.stderr.decode(errors='replace')}
            code = proc.wait(timeout=15)
    after = inventory(fixture) if fixture else None
    rec = {'case_id': cid, 'argv': list(map(str, argv)), 'cwd': str(ROOT), 'start': start, 'end': now(),
           'elapsed_seconds': time.monotonic()-tick, 'exit': code, 'timed_out': timed_out, 'termination': termination,
           'stdout': ref(dest/'stdout.txt', RUN), 'stderr': ref(dest/'stderr.txt', RUN),
           'fixture_after': after, 'fixture_unchanged': None if not fixture else before['files']==after['files']}
    save(dest / 'receipt.json', rec)
    return rec

def setup():
    inputs = RUN / 'inputs'
    for name, expected in SPECS.items():
        p = ROOT / 'docs/plan' / name
        b = read(p)
        save(inputs / (name + '.identity.json'), {'original_path':str(p), 'expected':expected, 'actual':sha(b)})
        if sha(b) != expected:
            raise ValueError('SPECIFICATION MISMATCH; contract-dependent work stopped')
        write(inputs / name, b)
    for name, path in [('target', TARGET), ('loaded-evaluator', LOADED), ('companion', ROOT/'src/agents/skills/skill-builder')]:
        m = inventory(path)
        save(inputs/(name+'-before.json'), m)
        if name == 'target':
            old = json.loads(read(PRIOR/'target-before.json'))
            save(inputs/'delivery-comparison.json', {'expected':EXPECTED, 'actual':m['package_digest'], 'matches':m['package_digest']==EXPECTED, 'prior_files_equal':old['files']==m['files']})
            if m['package_digest'] != EXPECTED or len(m['files']) != 75:
                raise ValueError('Target drift: separately select current/snapshot')
            for row in m['files']:
                write(RUN/'source'/row['path'], read(path/row['path']))
            save(RUN/'source-manifest.json', m)
            assert inventory(RUN/'source')['files'] == m['files']
    prior_names = ['qa-report.md','revision-spec.md','stable-findings.json','target-before.json','target-after.json',
                   'expectations-before-execution.json','independent_probes.py','qa_harness.py','command-log.md',
                   'final-receipt.json','baseline-compatibility.json']
    selected = []
    for n in prior_names:
        p = PRIOR/n
        write(inputs/'prior'/n, read(p)); selected.append(ref(p))
    for cid in ('R06','R07','P07','P08'):
        for n in ('stdout.txt','stderr.txt','command.json'):
            p=PRIOR/'commands'/cid/n
            write(inputs/'prior/commands'/cid/n, read(p)); selected.append(ref(p))
        root=PRIOR/'trials/independent'/cid
        m=inventory(root)
        save(inputs/'prior'/f'{cid}-manifest.json',m)
        selected.extend(ref(root/r['path']) for r in m['files'])
    save(inputs/'prior-selected-before.json', selected)
    instructions=[]
    for base in (ROOT,TARGET,LOADED,RUN,ROOT/'src/agents/skills/skill-builder'):
        for parent in (base,*base.parents):
            if parent == ROOT.parent: break
            p=parent/'AGENTS.md'
            if p.exists() and str(p) not in [x['path'] for x in instructions]:
                instructions.append(ref(p))
    for root in (TARGET, LOADED):
        for r in inventory(root)['files']:
            if Path(r['path']).name=='AGENTS.md': instructions.append(ref(root/r['path']))
    save(inputs/'applicable-instructions.json', instructions)
    write(inputs/'AGENTS.md',read(ROOT/'AGENTS.md'))
    save(inputs/'checker-identity.json',ref(CHECKER))
    versions={}
    for name in ('PyYAML','coverage','jsonschema'):
        try: versions[name]=importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError: versions[name]=None
    save(inputs/'environment.json',{'time':now(),'platform':platform.platform(),'python':sys.version,'executable':sys.executable,'packages':versions,'execution':'Native Windows; selected C: checkout; no WSL','git_present':(ROOT/'.git').exists()})
    print(json.dumps({'run':str(RUN),'target_digest':EXPECTED,'target_files':75,'environment':versions}))

if __name__ == '__main__':
    setup()
