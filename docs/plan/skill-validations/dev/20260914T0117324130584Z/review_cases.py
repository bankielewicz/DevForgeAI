"""Display bounded completed native artifacts for manual assessment, no verdicts."""
import json
from pathlib import Path
import sys
RUN = Path(__file__).resolve().parent
for name in sys.argv[1:]:
    base = RUN / 'trials' / name
    attempts = sorted(base.glob('attempt-*/result.json'))
    if not attempts:
        print(name, 'IN_PROGRESS_OR_NOT_RUN')
        continue
    record = json.loads(attempts[-1].read_bytes())
    project = Path(record['cwd'])
    number = attempts[-1].parent.name.split('-')[-1]
    final = project / '.trial-output' / ('final-' + number + '.txt')
    print('\nTRIAL', name, record['termination'], record.get('exit_status'), record['elapsed_seconds'])
    print('FINAL', final.read_text(encoding='utf-8') if final.exists() else 'ABSENT')
    print('EFFECTS', (attempts[-1].parent / 'effects.json').read_text(encoding='utf-8'))
    for line in (RUN / 'commands' / (name + '-' + number) / 'stdout.txt').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        item = row.get('item', {})
        if row.get('type') in ('error', 'turn.failed'):
            print('ERROR', row)
        if row.get('type') == 'item.completed' and item.get('type') == 'command_execution':
            print('COMMAND', item.get('command', '')[:220], 'EXIT', item.get('exit_code'))
            print('OUTPUT_TAIL', item.get('aggregated_output', '')[-500:])
