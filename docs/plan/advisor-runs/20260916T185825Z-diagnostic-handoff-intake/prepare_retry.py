from pathlib import Path
import hashlib
import json
root = Path(__file__).resolve().parent
repo = Path('C:/Projects/DevForgeAI')
run = root.with_name('20260916T185825Z-diagnostic-handoff')
receipt = run/'attempt-001/execution.json'
execution = json.loads(receipt.read_text())
assert execution['execution_status'] == 'FAILED'
assert execution['transport']['cleanup'] == {'child_exited':True,'pipes_closed':True}
assert execution['exit_code'] == 1
result = json.loads((run/'attempt-001/result.json').read_text())
assert result['terminal_reason'] == 'api_error'
assert 'ConnectionRefused' in result['result']
text = (root/'briefing.md').read_text()
text = text.replace('No reviewer attempt has run yet.',
    'Attempt 1 has completed unsuccessfully; this is the sole remaining attempt, reason=retry, using normal host escalation for the observed connection refusal. The immutable ask, auth, model, budget, read-only restrictions and timeout remain unchanged.')
note = f'''\nAttempt-001 authoritative outcome: execution_status=FAILED, response_status=NOT_EVALUATED, exit_code=1, verdict=null, no response.md. result.json says exactly: "{result['result']}". terminal_reason=api_error, zero model tokens reported, reported_cost_usd=0. The direct process exited and both pipes closed, with no timeout or interruption. stderr is empty. This is an observed connection failure, not evidence of bad credentials, unavailable model or a handoff defect. Prior receipt: {receipt}; SHA256 {hashlib.sha256(receipt.read_bytes()).hexdigest()}. Prior result: {run/'attempt-001/result.json'}. The first USD 1.00 allocation remains consumed; do not reclaim it. This remaining attempt requests host escalation to address a likely sandbox network restriction; do not switch authentication or weaken reviewer restrictions.\n'''
text = text.replace('## CURRENT PLAN',note+'\n## CURRENT PLAN')
with (root/'briefing-retry.md').open('x',encoding='utf-8',newline='\n') as stream:
    stream.write(text)
for line in (root/'citation-readback.txt').read_text().splitlines():
    path,number,anchor = line.split(':',2)
    actual = (repo/path).read_text().splitlines()[int(number)-1]
    assert actual == anchor[1:], (path,number)
    print(f'{path}:{number}: {actual}')
manifest = repo/'docs/plan/framework-worker-diagnostics/20260916T181820Z-dev/candidate-v2-manifest.json'
for item in json.loads(manifest.read_text()):
    candidate = repo/'devforgeai/experiments/codex-worker-probe'/item['path']
    assert hashlib.sha256(candidate.read_bytes()).hexdigest() == item['sha256']
for i,line in enumerate((run/'attempt-001/result.json').read_text().splitlines(),1):
    if 'ConnectionRefused' in line or 'terminal_reason' in line:
        print(f'{run.relative_to(repo).as_posix()}/attempt-001/result.json:{i}: {line}')
print('All original citations and 58 current source bindings reverified immediately before retry.')
