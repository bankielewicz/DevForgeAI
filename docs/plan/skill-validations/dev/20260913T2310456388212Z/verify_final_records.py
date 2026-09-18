"""Run the installed schema-1 evidence checker with retained actual streams."""
import json
import sys
import native_trials as n
n.h.RUN = n.RUN / 'verification'
attempt = sys.argv[1]
record = n.h.execute('records-' + attempt, [sys.executable, '-B', '-X', 'utf8', str(n.PROJECT / '.agents/skills/skill-validator/scripts/observe.py'), 'records', '--run-root', str(n.RUN)], cwd=n.PROJECT)
output = n.RUN / 'verification/commands' / ('records-' + attempt) / 'stdout.txt'
print(output.read_text(encoding='utf-8'))
raise SystemExit(record['exit_status'] or 0)
