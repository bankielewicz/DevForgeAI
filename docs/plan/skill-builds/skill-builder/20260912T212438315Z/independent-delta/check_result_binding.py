import json
from pathlib import Path

root = Path(__file__).resolve().parent
run = root.parent
observation = json.loads((root / 'observation.json').read_bytes())
expected = {'revision/N/' + row['path']: row['sha256'] for row in observation['candidate_rows']}
delta = json.loads((run / 'candidate-delta.json').read_bytes())
assert delta['candidate'] == observation['candidate_rows']
results = [json.loads(line) for line in (run / 'candidate-results.jsonl').read_bytes().splitlines()]
for row in results:
    actual = {key: value for key, value in row['candidate_digests'].items() if key.startswith('revision/N/')}
    assert actual == expected, row['case_id']
print(json.dumps({'candidate_rows_match_recorded_delta': True, 'all_three_results_bind_all_36_N_file_digests': True, 'result_cases': [row['case_id'] for row in results]}, indent=2))
