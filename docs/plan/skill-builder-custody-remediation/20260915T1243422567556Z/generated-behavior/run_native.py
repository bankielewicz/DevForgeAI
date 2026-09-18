"""Independent actual-Codex skill exercise; expectations never enter executor prompts."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time

BASE = Path(__file__).resolve().parent
SOURCE = Path(r'C:\Users\bryan\AppData\Local\Temp\meeting-actions-forward-20260915T123432373Z\src\agents\skills\meeting-actions\SKILL.md')
CLI = r'C:\Users\bryan\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe'

def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def prepare():
    root = Path(tempfile.mkdtemp(prefix='meeting-actions-independent-'))
    skill = root / 'meeting-actions' / 'SKILL.md'
    skill.parent.mkdir()
    skill.write_bytes(SOURCE.read_bytes())
    (root / 'notes original.md').write_text('Lena will publish the status update by Friday.\n', encoding='utf-8')
    (root / 'blocked destination.md').mkdir()
    (root / 'blocked destination.md' / 'sentinel.txt').write_text('keep this directory unchanged\n', encoding='utf-8')
    intro = f'Use the skill at {skill} to complete these requests. Read that SKILL.md first. Work only in {root}. Do not use other skills or external services.\n\n'
    chat = intro + '''These are four separate user requests; label each response by its case ID.
CASE C1: Extract the meeting actions from these notes: "We need to archive the obsolete checklist. Robin will verify the checksum. The cost trend was discussed."
CASE C2: Extract the meeting actions from these notes: "Possibly ask Jules to trial the revised process next Friday, if the director approves? No decision was reached on purchasing licenses."
CASE C3: Extract the meeting actions from these notes: "Draft 1: Kira owns delivery of the release notes, due Tuesday. Draft 2: delivery of the same release notes belongs to Omar, due Thursday. Neither draft was approved; the assignment and deadline remain unresolved."
CASE C4: Extract the meeting actions from these notes: "Owner: Dev | Ops. Task: document the A | B fallback. Due: 2026-10-09. We discussed overall progress without assigning other work."
'''
    files = intro + f'''These are three separate user requests; label each response by its case ID.
CASE F1: Read the meeting notes in "notes original.md" and write the action table to the relative destination "résumé actions 東京.md".
CASE F2: From the notes "Marta will check the release package tomorrow", write the action table to the destination "blocked destination.md". Do not remove or replace existing directories or their contents.
CASE F3: Read the meeting notes in "notes original.md" and write the action table to "notes original.md".
'''
    expected = {
        'C1': ['exact three table columns Action, Owner, Due date', 'archive obsolete checklist: Unassigned / Not specified', 'verify checksum: Robin / Not specified', 'no action from cost discussion', 'chat output'],
        'C2': ['possibility, approval condition, and uncertainty retained', 'relative next Friday retained', 'no license purchase decision invented'],
        'C3': ['both Kira and Omar preserved as conflicting/unresolved owners', 'Tuesday and Thursday preserved as conflicting/unresolved dates', 'no invented resolution'],
        'C4': ['one action row', 'literal pipes in action and owner escaped or encoded to preserve three cells', 'date unchanged'],
        'F1': ['literal relative Unicode/spaced path exists under fixture root', 'table has Lena and Friday with supported publish action', 'actual successful file path reported', 'readback evidenced', 'source unchanged'],
        'F2': ['directory and sentinel unchanged', 'failure and destination reported', 'delivery explicitly incomplete', 'no alternate file silently chosen'],
        'F3': ['source remains byte-identical', 'no successful overwrite claimed', 'conflict with input preservation identified']}
    save(BASE / 'expected.json', expected)
    save(BASE / 'fixture.json', {'root': str(root), 'source': str(SOURCE), 'source_sha256': digest(SOURCE), 'copied_skill_sha256': digest(skill), 'input_sha256': digest(root / 'notes original.md')})
    for case, prompt in [('chat', chat), ('files', files)]:
        (BASE / f'{case}.prompt.txt').write_text(prompt, encoding='utf-8')
    print(root)

def run(case, attempt):
    fixture = json.loads((BASE / 'fixture.json').read_text(encoding='utf-8'))
    root = Path(fixture['root'])
    attempt_root = BASE / f'{case}-{attempt}'
    attempt_root.mkdir(exist_ok=False)
    command = [CLI, 'exec', '--ignore-user-config', '--skip-git-repo-check', '--ephemeral', '--sandbox', 'workspace-write', '--color', 'never', '--json', '-C', str(root), '-o', str(attempt_root / 'last-message.txt'), '-']
    prompt = (BASE / f'{case}.prompt.txt').read_bytes()
    started = time.time()
    timed_out = False
    with (attempt_root / 'stdout.jsonl').open('wb') as out, (attempt_root / 'stderr.txt').open('wb') as err:
        proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err, cwd=root)
        try:
            proc.communicate(prompt, timeout=120)
        except subprocess.TimeoutExpired:
            timed_out = True
            killed = subprocess.run(['taskkill', '/PID', str(proc.pid), '/T', '/F'], capture_output=True)
            (attempt_root / 'termination.txt').write_bytes(killed.stdout + killed.stderr)
            proc.wait(timeout=15)
    metadata = {'platform': platform.platform(), 'python': sys.executable, 'shell': 'Python subprocess from Windows PowerShell', 'cwd': str(root), 'filesystem': 'Windows native temporary directory', 'command': command, 'started_unix': started, 'elapsed_seconds': time.time() - started, 'timeout_seconds': 120, 'timed_out': timed_out, 'exit_code': proc.returncode, 'prompt_sha256': hashlib.sha256(prompt).hexdigest(), 'source_before_sha256': fixture['source_sha256'], 'source_after_sha256': digest(SOURCE), 'input_before_sha256': fixture['input_sha256'], 'input_after_sha256': digest(root / 'notes original.md')}
    save(attempt_root / 'runtime.json', metadata)
    for path in root.rglob('*'):
        if path.is_file() and '.git' not in path.parts:
            target = attempt_root / 'fixture-after' / path.relative_to(root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    print(json.dumps(metadata, ensure_ascii=True))

if __name__ == '__main__':
    if sys.argv[1] == 'prepare':
        prepare()
    else:
        run(sys.argv[1], sys.argv[2])
