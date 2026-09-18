"""Bounded forward exercises against the generated package, with real outputs."""
import json
import re
import sys
from trial_support import *

def main():
    phase = sys.argv[1]
    package = CANDIDATE if phase == 'candidate' else DEST
    work = EVIDENCE / ('exercises-' + phase)
    work.mkdir()
    measured = outputs(package)
    log(dict(cwd=str(ROOT), tool='apply_patch', affected_paths=[str(package/row['path']) for row in measured], action='Created the four requirement-bound candidate resources; tightened schema end-of-string assertion before execution', returned_result='Success (empty structured result)', readback=measured, interpretation='Authored candidate bytes; no builder edit'))
    structural = command([sys.executable,'-B','-X','utf8',CHECKER,package], 'Installed Skill Creator structural check for '+phase)
    assert structural.returncode == 0
    script = package/'scripts/sum_amounts.py'
    prefix = [sys.executable,'-B','-X','utf8',script]
    cases = []

    def run_case(ident, source, expected_result=None, expected_code=0, existing=None, arguments=None):
        target = work/(ident+'.json')
        if existing is not None:
            target.write_bytes(existing)
        before = source.read_bytes() if source.exists() else None
        args = arguments if arguments is not None else ['--input',source,'--output',target]
        observed = command(prefix+args, 'Execute '+phase+' case '+ident, expected_code)
        assert observed.returncode == expected_code, ident
        assert (source.read_bytes() if source.exists() else None) == before, ident+' input changed'
        if expected_code == 0:
            result = json.loads(target.read_bytes())
            assert result == expected_result and json.loads(observed.stdout) == expected_result, ident
            assert type(result['count']) is int and set(result) == {'count','total'}
            assert observed.stderr == '', ident
        else:
            assert observed.stderr and not observed.stdout, ident
            assert target.read_bytes() == existing if existing is not None else not target.exists(), ident
        cases.append(dict(case_id=ident,input_path=str(source),output_path=str(target),input_sha256_before=sha(before) if before is not None else None,input_sha256_after=sha(source.read_bytes()) if source.exists() else None,exit_code=observed.returncode,stdout=observed.stdout,stderr=observed.stderr,expected=expected_result,observation='PASSED',output_sha256=sha(target.read_bytes()) if target.exists() else None))

    run_case('supplied-sample',INPUTS/'sample.csv',dict(count=4,total='2.65'))
    run_case('supplied-invalid',INPUTS/'invalid.csv',expected_code=2)
    run_case('output-conflict',INPUTS/'sample.csv',expected_code=2,existing=b'USER OUTPUT MUST REMAIN\r\n')
    run_case('invalid-output-conflict',INPUTS/'invalid.csv',expected_code=2,existing=b'USER INVALID OUTPUT MUST REMAIN\n')
    fixtures = [
        ('quoted-bom',b'\xef\xbb\xbfdescription,amount\r\n"quoted, field",0.10\r\n"two\r\nlines",0.20\r\n',dict(count=2,total='0.30'),0),
        ('header-only',b'description,amount\n',dict(count=0,total='0.00'),0),
        ('large-decimals',b'amount\n99999999999999999999999999999.99\n0.02\n-0.01\n',dict(count=3,total='100000000000000000000000000000.00'),0),
        ('negative-zero',b'amount\n-0.00\n',dict(count=1,total='0.00'),0),
        ('missing-header',b'value\n1.00\n',None,2),
        ('missing-amount',b'description,amount\nbad,\n',None,2),
        ('short-row',b'description,amount\nbad\n',None,2),
        ('infinite',b'amount\nInfinity\n',None,2),
        ('precision',b'amount\n1.001\n',None,2),
        ('trailing-precision',b'amount\n1.000\n',None,2),
        ('malformed-quote',b'amount\n"1.00\n',None,2),
        ('invalid-utf8',b'amount\n\xff\n',None,2),
    ]
    for ident,data,expected,code in fixtures:
        source=work/(ident+'.csv')
        source.write_bytes(data)
        run_case(ident,source,expected,code)
    run_case('missing-input-file',work/'absent.csv',expected_code=2)
    run_case('required-arguments',INPUTS/'sample.csv',expected_code=2,arguments=[])
    schema=json.loads((package/'assets/result.schema.json').read_bytes())
    assert schema['type']=='object' and set(schema['required'])=={'count','total'} and schema['additionalProperties'] is False
    assert schema['properties']['count']=={'type':'integer','minimum':0}
    assert schema['properties']['total']['type']=='string'
    pattern=schema['properties']['total']['pattern']
    valid_strings=['0.00','-1.10','100000000000000000000000000000.00']
    invalid_strings=['1','1.0','1.000','1.00\n','1.00\r\n','NaN','Infinity','01.00','+1.00','1e2']
    assert all(re.search(pattern,value) for value in valid_strings)
    assert all(not re.search(pattern,value) for value in invalid_strings)
    review=cases[0]
    produced=json.loads(Path(review['output_path']).read_bytes())
    assert set(produced)=={'count','total'} and type(produced['count']) is int and produced['count']>=0 and type(produced['total']) is str and re.search(pattern,produced['total'])
    assert review['input_sha256_before']==review['input_sha256_after']
    # Actual read-only task return, rather than a claim that a worker profile ran.
    worker=dict(schema_version='1',run_id=RUN,target_name=NAME,outputs=measured,execution='sequential main-agent task using Python standard library',assigned_write_paths=[],inspected_input_path=review['input_path'],inspected_output_path=review['output_path'],input_sha256_before=review['input_sha256_before'],input_sha256_after=review['input_sha256_after'],observed_json=produced,findings=[],interpretation='Actual JSON fields and string pattern checked; input bytes unchanged; no framework acceptance')
    write_json(EVIDENCE/('worker-review-'+phase+'.json'),worker)
    write_json(EVIDENCE/('observations-'+phase+'.json'),dict(schema_version='1',run_id=RUN,target_name=NAME,outputs=measured,structural=dict(exit_code=structural.returncode,stdout=structural.stdout,stderr=structural.stderr),behavioral_cases=cases,schema_observation=dict(exact_fields_types=True,valid_pattern_examples=valid_strings,rejected_pattern_examples=invalid_strings,limitation='Schema shape and pattern exercised directly; no external JSON Schema engine dependency installed'),worker_review='worker-review-'+phase+'.json'))
    write_json(EVIDENCE/('manifest-'+phase+'.json'),manifest(package))
    log(dict(cwd=str(ROOT),action='Completed '+phase+' script exercises and sequential worker review',cases=len(cases),outputs=measured,interpretation='All expected results and input/output preservation assertions passed; schema was inspected and its pattern exercised without external packages'))
    print(json.dumps(dict(phase=phase,cases=len(cases),structural='PASSED',behavioral='PASSED',worker='PASSED')))

if __name__=='__main__':
    main()
