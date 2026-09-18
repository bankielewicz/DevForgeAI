"""Reproduce the unexpected regression on unchanged pre-repair validator bytes."""
import json
import os
import sys
from harness import RUN, ROOT, read, save, inventory, execute

before=ROOT/'docs/plan/skill-adaptive-implementations/skill-validator/20260913T211315150947Z/source'
builder=ROOT/'src/agents/skills/skill-builder'
assert inventory(before)['package_digest']=='d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1'
os.environ['AUTHORING_BUILDER_ROOT']=str(builder)
save(RUN/'baseline-failure-plan.json',{'target':str(before),'target_digest':'d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1','companion':inventory(builder),'expected':'Determine whether the same seven error-message subtest failures occur before repairs; do not change assertions or companion.','environment_override':{'AUTHORING_BUILDER_ROOT':str(builder)}})
rec=execute('PRE-REPAIR-FAILURE-CONTROL',[sys.executable,'-B','-X','utf8','-m','unittest','discover','-s',str(before/'tests'),'-p','test_authoring.py','-k','malformed_contract','-v'])
print(rec['exit'])
