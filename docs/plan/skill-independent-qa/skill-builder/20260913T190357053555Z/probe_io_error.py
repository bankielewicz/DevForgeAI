"""Independent deterministic I/O failure injection; no OS permission claim."""
from pathlib import Path
import json
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_independent as base
from capture import manifest
expected='7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a'
assert manifest(base.BUILDER)['package_digest']==expected
root=base.RUN/'fixtures/windows-final04-io-error'; root.mkdir()
fixture=base.Independent('test_binding_bound'); fixture.root=root
skill,_=fixture.skill(); fixture.binding(skill)
before=base.package(root)
base.save(base.RUN/'reports/io-error-plan.json',{'target_digest':expected,'expected_exit':2,'expected_status':'UNAVAILABLE','expected_reason':'IO_ERROR','method':'Inject OSError at the runtime capture read boundary; no simulated successful result','fixture_root':str(root)})
with patch.object(base.runtime.Capture,'read',side_effect=OSError('synthetic I/O failure')):
    code,result=base.runtime.observe(str(root),str(skill))
assert (code,result['status'],result['reason_code'])==(2,'UNAVAILABLE','IO_ERROR')
assert before==base.package(root)
base.save(base.RUN/'reports/io-error-result.json',{'target_digest':expected,'status':'PASS','exit_code':code,'observation':result,'unchanged':True,'limitation':'Fault injection covers error propagation; it does not qualify native host permission isolation.'})
print('PASS deterministic I/O error propagation')
