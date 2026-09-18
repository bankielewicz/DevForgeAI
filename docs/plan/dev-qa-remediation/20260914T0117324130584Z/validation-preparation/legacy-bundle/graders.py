"""Deterministic evidence observations only; no policy or acceptance authority."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat

def sha(data):
    return hashlib.sha256(data).hexdigest()

def compact(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')

def unique(pairs):
    answer={}
    for key,value in pairs:
        if key in answer: raise ValueError('duplicate JSON key')
        answer[key]=value
    return answer

def load(data):
    return json.loads(data,object_pairs_hook=unique,parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def safe_file(root, name):
    if not isinstance(name,str) or not name or '\\' in name or ':' in name or '\x00' in name:
        raise ValueError('unsafe relative path')
    parts=PurePosixPath(name).parts
    if name.startswith('/') or any(p in ('','.','..') for p in name.split('/')):
        raise ValueError('unsafe relative path')
    path=root
    for part in parts:
        path=path/part
        info=path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400:
            raise ValueError('link boundary')
    if not path.is_file(): raise ValueError('not a regular file')
    if path.stat().st_size>32*1024*1024: raise ValueError('read ceiling')
    return path

def verify_refs(root, rows):
    seen=set()
    for row in rows:
        if set(row)!={'path','sha256'} or row['path'] in seen: raise ValueError('duplicate or malformed reference')
        seen.add(row['path'])
        if not re.fullmatch('[0-9a-f]{64}',row['sha256']): raise ValueError('invalid SHA-256')
        if sha(safe_file(root,row['path']).read_bytes())!=row['sha256']: raise ValueError('STALE_BINDING: '+row['path'])
    return len(seen)

def verify_package(root, manifest):
    rows=manifest['files']
    if not manifest['complete'] or manifest['excluded_boundaries']: raise ValueError('incomplete package')
    if [r['path'] for r in rows]!=sorted(set(r['path'] for r in rows)): raise ValueError('noncanonical manifest')
    canonical=[]
    for row in rows:
        data=safe_file(root,row['path']).read_bytes()
        if len(data)!=row['bytes'] or sha(data)!=row['sha256']: raise ValueError('STALE_PACKAGE')
        canonical.append({'path':row['path'],'bytes':row['bytes'],'sha256':row['sha256']})
    pending=[root]; actual=[]
    while pending:
        for path in sorted(pending.pop().iterdir()):
            info=path.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info,'st_file_attributes',0)&0x400: raise ValueError('link boundary')
            if path.is_dir(): pending.append(path)
            elif path.is_file(): actual.append(path.relative_to(root).as_posix())
            else: raise ValueError('special file')
            if len(actual)>2000: raise ValueError('file ceiling')
    if sorted(actual)!=[r['path'] for r in rows]: raise ValueError('package file-set drift')
    if sha(compact(canonical))!=manifest['package_digest']: raise ValueError('package digest mismatch')
    return manifest['package_digest']

def portable_scan(root, manifest):
    forbidden=re.compile(r'[A-Za-z]:[\\/]|/home/|binding_required\s*[:=]\s*true|devforgeai_cli|dev-skill-spec\.md|index-service|query-cli',re.I)
    return [{'file':r['path'],'match':m.group(0)} for r in manifest['files'] for m in forbidden.finditer(safe_file(root,r['path']).read_text(encoding='utf-8'))]

def check_execution(row, root):
    needed={'attempt_id','command','working_directory','started_at','ended_at','exit_code','stdout','stderr','candidate','result'}
    if not needed<=row.keys(): raise ValueError('incomplete receipt')
    if row['result']=='PASS' and (type(row['exit_code']) is not int or row['exit_code']!=0 or not row['ended_at']): raise ValueError('unsupported PASS')
    verify_refs(root,[row['stdout'],row['stderr'],row['candidate']])
    return True

def metrics(cases):
    if len({c['case_id'] for c in cases})!=len(cases): raise ValueError('duplicate case')
    allowed={'PASS','FAIL','ERROR','NOT_RUN','NOT_APPLICABLE'}
    if any(c['result'] not in allowed for c in cases): raise ValueError('invalid outcome')
    required=[c for c in cases if c['required']]
    passes=sum(c['result']=='PASS' for c in required)
    return {'passing':passes,'required':len(required),'pass_rate':100*passes/len(required) if required else None,'counts':{s:sum(c['result']==s for c in required) for s in sorted(allowed)}}
