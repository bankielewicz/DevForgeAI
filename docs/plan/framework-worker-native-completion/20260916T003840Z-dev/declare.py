"""Declare the frozen candidate's executable case denominator before full execution."""
import json
from pathlib import Path
import record

root = Path(__file__).resolve().parent
names = [line.removesuffix(': test') for line in (root/'enumerate-final/stdout.bin').read_text().splitlines() if line.endswith(': test')]
assert len(names) == len(set(names)), 'Use target-qualified IDs if names overlap'
assert len(names) == 114, len(names)
wf = [name for name in names if name.startswith('wf_')]
assert len(wf) == 20
record.atomic_json(root/'required-cases.json', {
    'platform': 'Windows x64', 'configuration': 'default; no optional package features',
    'candidate_manifest_sha256': record.sha256(root/'candidate-manifest.json'),
    'enumeration_receipt': 'enumerate-final/receipt.json',
    'required_function_count': len(names), 'unit_function_count': 28,
    'mandatory_wf_parent_count': len(wf),
    'counting_rule': 'Each function counted once; WF cases and defect tests are subsets, not additive. All subfixture assertions must pass. Coverage execution is a separate instrumented attempt and is not added to the pass denominator.',
    'required_functions': names, 'mandatory_wf_parents': wf,
    'native_trials': {'required_in_native_readiness':2, 'selected_coverage_retest_scope':False, 'status':'BLOCKED_PENDING_SEPARATE_PREREQUISITES', 'attempts':0},
    'first_party_coverage_exclusions': [],
})
print(json.dumps({'required_functions':len(names), 'unit_functions':28, 'mandatory_wf_parents':len(wf)}))
