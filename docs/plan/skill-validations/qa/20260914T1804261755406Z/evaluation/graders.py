"""Deterministic evidence graders; never framework acceptance.

These independently check arithmetic, case accounting and byte identity. They
do not certify the truth or semantic quality of a model-authored observation.
"""
from fractions import Fraction
import hashlib
from pathlib import Path, PurePosixPath

def metric(numerator, denominator, floor=95):
    if type(floor) is not int or not 95 <= floor <= 100:
        raise ValueError('Invalid floor')
    if numerator is None or denominator is None:
        return 'INCOMPLETE'
    if type(numerator) is not int or type(denominator) is not int or min(numerator,denominator)<0 or numerator>denominator:
        raise ValueError('Invalid metric counts')
    if denominator == 0:
        return 'INCOMPLETE'
    return 'PASS' if Fraction(100*numerator,denominator)>=floor else 'FAIL'

def unit_counts(inventory, attempts):
    keys=[(x['platform'],x['id']) for x in inventory]
    if len(keys)!=len(set(keys)):
        raise ValueError('Duplicate required case')
    latest={}
    for row in attempts:
        if row['category']!='unit':
            continue
        key=(row['platform'],row['id'])
        if key not in keys or row['status'] not in ('PASS','FAIL','ERROR','NOT_RUN'):
            raise ValueError('Unknown case or invalid status')
        latest[key]=row['status']
    passing=sum(value=='PASS' for value in latest.values())
    return {'passing':passing,'required':len(keys),'result':metric(passing,len(keys)),'attempts':len(attempts)}

def verify_reference(root, reference):
    root=Path(root).resolve()
    relative=reference['path']
    if not isinstance(relative,str) or not relative or '\\' in relative or ':' in relative or PurePosixPath(relative).is_absolute() or any(p in ('','..','.') for p in relative.split('/')):
        raise ValueError('Unsafe evidence reference')
    path=root/relative
    if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError('Linked evidence reference')
    resolved=path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError('Escaping evidence reference')
    return path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==reference['sha256']

def reduce_cases(cases, observations):
    ids=[case['case_id'] for case in cases]
    if len(ids)!=len(set(ids)):
        raise ValueError('Duplicate required case')
    observed={}
    for row in observations:
        key=row['case_id']
        if key in observed or key not in ids or row['result'] not in ('PASS','FAIL','NOT_RUN','ERROR'):
            raise ValueError('Duplicate/unknown case or invalid result')
        observed[key]=row['result']
    passing=sum(x=='PASS' for x in observed.values())
    failed=sum(x=='FAIL' for x in observed.values())
    pending=len(ids)-passing-failed
    return {'outcome':'FAIL' if failed else 'INCOMPLETE' if pending else 'PASS','passing':passing,'failed':failed,'unperformed':pending,'required':len(ids),'evaluated':passing+failed}
