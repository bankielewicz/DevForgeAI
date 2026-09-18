"""Create only the fixed disposable fixture and record compiled source inspection."""
import json
from pathlib import Path
import record

trial = record.WORK / 'docs/plan/framework-worker-trials/20260915T2306060954875Z-preflight'
trial.mkdir(exist_ok=False)
fixture = trial / 'fixture'
fixture.mkdir()
(fixture/'task.json').write_bytes((record.PACKAGE/'tests/fixtures/task.json').read_bytes())
record.write('native-fixture-binding.json', {
    'trial':str(trial), 'fixture':str(fixture), 'fixture_sha256':record.sha(fixture/'task.json'),
    'operation':'profile-sources only; no Codex process or model trial',
    'worker_version':'0.154.0', 'model':'gpt-6-astra', 'effort':'high',
    'native_trials':'WN-01/WN-02 remain selected once after prerequisites; zero automatic retries'
})
record.capture('native-source-inspection-001', [record.ROOT/'target/debug/devforgeai-codex-worker-probe.exe', 'profile-sources','--checkout-root',fixture], timeout=30)
