"""Read-only display of retained native evidence; does not assign case verdicts."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

for folder in sorted((ROOT / 'commands').iterdir()):
    if len(sys.argv) > 1 and not any(folder.name.startswith(x) for x in sys.argv[1:]):
        continue
    command = json.loads((folder / 'command.json').read_bytes())
    if command['termination'] == 'not-started':
        print(folder.name, 'RUNNING')
        continue
    print('\nATTEMPT', folder.name, command['termination'], command.get('exit_status'))
    project = Path(command['cwd'])
    final = project / '.trial-output/final-001.txt'
    print('FINAL', final.read_text(encoding='utf-8') if final.is_file() else 'ABSENT')
    for line in (folder / 'stdout.txt').read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        item = row.get('item', {})
        if row.get('type') == 'item.completed' and item.get('type') == 'command_execution':
            print('COMMAND', item['command'][:350], 'EXIT', item.get('exit_code'))
            print(item.get('aggregated_output', '')[-600:])
        elif row.get('type') == 'item.completed' and item.get('type') not in ('agent_message', 'reasoning', 'file_change'):
            print('OTHER_EVENT', json.dumps(row, ensure_ascii=False))
