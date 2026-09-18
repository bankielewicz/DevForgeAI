"""Windows native-path exclusion edge, with only synthetic environment text."""
from pathlib import Path
import json
import os
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_independent as base
assert os.name=='nt'
root=base.RUN/'fixtures/windows-env-case'
root.mkdir()
plan={'case':'Windows .ENV exclusion alias','expected':'UNSAFE_PATH','basis':'Governing section 4.2 excludes .env files; section 6.2 rejects excluded files. Windows resolves .ENV and .env to the same file.','permitted_root':str(root),'fixture':'synthetic environment marker only'}
base.save(base.RUN/'reports/env-case-plan.json',plan)
fixture=base.Independent('test_binding_secret_excluded'); fixture.root=root
skill,_=fixture.skill()
(skill/'.ENV').write_text('SYNTHETIC_TOKEN=not-a-real-secret\n',encoding='utf-8')
lowercase_alias_exists=(skill/'.env').exists()
fixture.binding(skill)
code,observation=base.runtime.observe(str(root),str(skill))
result={'case':plan['case'],'target_digest':'ecb5f8056f18e1d9889de0c829a7e8e48a6feafe1b8f29bc09718d226eb20099','lowercase_alias_exists':lowercase_alias_exists,'exit_code':code,'observation':observation,'expected_reason':'UNSAFE_PATH','status':'PASS' if observation['reason_code']=='UNSAFE_PATH' else 'FAIL'}
base.save(base.RUN/'reports/env-case-result.json',result)
print(json.dumps(result))
