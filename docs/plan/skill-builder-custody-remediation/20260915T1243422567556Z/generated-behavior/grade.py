"""Independent artifact checks supporting a separately recorded semantic review."""
import hashlib
import json
from pathlib import Path
import re

base = Path(__file__).resolve().parent
out = (base / 'chat-inline-001' / 'last-message.txt').read_text(encoding='utf-8')
blocks = {m.group(1): m.group(2) for m in re.finditer(r'### CASE (C[1-4])\s*(.*?)(?=### CASE|\Z)', out, re.S)}
checks = {}
for name, body in blocks.items():
    rows = [line for line in body.splitlines() if line.startswith('|')]
    checks[name + '_columns'] = rows[0] == '| Action | Owner | Due date |' and all(len(re.split(r'(?<!\\)\|', row)) == 5 for row in rows)
checks['C1_missing_values'] = '**Unassigned**' in blocks['C1'] and blocks['C1'].count('**Not specified**') == 2 and 'Robin' in blocks['C1']
checks['C1_no_discussion_task'] = 'cost' not in blocks['C1'].lower()
checks['C2_condition_uncertainty'] = all(s in blocks['C2'] for s in ['Possibly', 'if the director approves?', 'next Friday'])
checks['C2_no_invented_purchase'] = 'license' not in blocks['C2'].lower()
checks['C3_conflict_retained'] = all(s in blocks['C3'] for s in ['Kira', 'Omar', 'Tuesday', 'Thursday', 'unresolved', 'neither draft approved'])
checks['C4_literal_pipe_content'] = all(s in blocks['C4'] for s in [r'A \| B', r'Dev \| Ops', '2026-10-09'])
fixture = json.loads((base / 'fixture.json').read_text(encoding='utf-8'))
checks['selected_skill_unchanged'] = hashlib.sha256(Path(fixture['source']).read_bytes()).hexdigest() == fixture['source_sha256']
checks['input_unchanged_after_blocked_file_attempt'] = hashlib.sha256((Path(fixture['root']) / 'notes original.md').read_bytes()).hexdigest() == fixture['input_sha256']
result = {'artifact_checks': checks, 'all_artifact_checks_pass': all(checks.values()), 'case_status': {'C1': 'PASS', 'C2': 'PASS', 'C3': 'PASS', 'C4': 'PASS', 'F1': 'BLOCKED', 'F2': 'BLOCKED', 'F3': 'BLOCKED'}, 'overall': 'INCOMPLETE', 'required_case_count': 7, 'passing_case_count': 4, 'passing_percentage': 100 * 4 / 7, 'semantic_review': 'C1 preserves both supported tasks and missing fields. C2 preserves proposed participant, condition, question mark, and relative date without inventing an assigned asker. C3 preserves both unresolved alternatives without synthesizing a decision. C4 retains literal pipe content as valid three-cell Markdown. F1-F3 were not substantively exercised because the executor stopped before reading the skill; their unchanged fixtures are not passing behavior evidence.'}
(base / 'grading.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
