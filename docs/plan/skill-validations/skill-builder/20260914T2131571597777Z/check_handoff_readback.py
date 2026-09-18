"""Correct the escaped-path oracle on already observed positive fixture bytes."""
import json
from prepare_validation import ROOT,put,sha
base=ROOT/'trials/independent/test_valid_capture_and_publication'
prompt=base/'docs/plan/authoring/run1/validator-request.md'
text=prompt.read_text(encoding='utf-8')
prefix='Original selected requirement sources: '
line=next(x for x in text.splitlines() if x.startswith(prefix))
sources=json.loads(line[len(prefix):])
expected={'path':str(base/'input/requirements.txt'),'sha256':sha(base/'input/requirements.txt')}
plan={'original_case':'test_valid_capture_and_publication','expected_reference':expected,'method':'Decode the JSON source reference then compare raw path and digest; no production re-execution','reason':'Original assertion compared JSON-escaped Windows path to unescaped text.'}
put('observations/handoff-readback/plan.json',plan)
assert sources==[expected]
for value in [sha(base/'input/design.json'),'NOT_PERFORMED','Independently derive','not observed behavior','Source action: created']: assert value in text,value
put('observations/handoff-readback/result.json',{'result':'PASS','sources':sources,'evidence':{'path':str(prompt),'sha256':sha(prompt)},'original_attempt_retained':True})
print('PASS: exact parsed source path and digest; original assertion failure retained.')
