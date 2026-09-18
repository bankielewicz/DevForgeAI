"""Names and digests only; observation is not launch or acceptance authority."""
import datetime as dt
import json
import os
from pathlib import Path
import record

ROOT = Path(__file__).resolve().parent
DEV = record.WORKSPACE / 'docs/plan/framework-worker-source-identity/20260916T021843Z-dev'
manifest = json.loads((DEV / 'candidate-manifest.json').read_text())
candidate_errors = [r['path'] for r in manifest if record.sha256(record.PACKAGE/r['path']) != r['sha256']]
inputs = json.loads((DEV / 'selected-inputs-final.json').read_text())
readback = [{'path': r['path'], 'expected_sha256': r['sha256'],
             'actual_sha256': record.sha256(record.WORKSPACE/r['path'])} for r in inputs]
prior = json.loads((ROOT/'source-observation-001/stdout.bin').read_bytes())
source_changes = []
for entry in prior['entries']:
    if entry['state'] == 'file':
        actual = record.sha256(Path(entry['path']))
        if actual != entry['sha256']:
            source_changes.append({'path': entry['path'], 'expected_sha256': entry['sha256'], 'actual_sha256': actual})
names = sorted(k for k in os.environ if 'API_KEY' in k.upper() or 'ACCESS_TOKEN' in k.upper() or k.upper() == 'OPENAI_BASE_URL')
value = {'observed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
         'candidate_files': len(manifest), 'candidate_mismatches': candidate_errors,
         'selected_input_readback': readback,
         'selected_input_changes': [r for r in readback if r['expected_sha256'] != r['actual_sha256']],
         'prior_inventory_file_changes': source_changes,
         'environment_names_matched_by_rust_guard': names,
         'environment_values_read_or_recorded': False,
         'parent_environment_changed': False,
         'native_preflight_executed': False,
         'inherited_environment_expected_result': 'profile_unqualified (static inference; not yet executed)',
         'advisor_briefing_citation_correction': 'AGENTS.md:88 is now advisor guidance; Follow the user selected scope is present later in the current file. Initial briefing line anchor was stale. Preserve original briefing.'}
with (ROOT/'state-observation-001.json').open('x',encoding='utf-8') as stream:
    json.dump(value,stream,indent=2); stream.write('\n')
print(json.dumps(value))
