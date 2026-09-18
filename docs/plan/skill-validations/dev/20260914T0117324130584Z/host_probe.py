"""Capture nonsecret installed runtime identity; do not access credentials."""
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

RUN = Path(__file__).resolve().parent
data = {'platform': platform.platform(), 'shell': 'Windows PowerShell process orchestration; native children use installed Codex-selected terminal',
        'python': sys.version, 'python_executable': sys.executable, 'codex_executable': shutil.which('codex'),
        'config_fields': [], 'config_limit': 'Only explicit nonsecret model/sandbox/approval and hook-section labels inspected; no auth/credential files read.',
        'isolation_limit': 'Native child workspace-write policy plus assigned disposable roots; shared existing user config. No independent OS-isolation proof.'}
for package in ('PyYAML', 'tiktoken'):
    try:
        data[package] = importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        data[package] = None
config = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'config.toml'
data['user_config_present'] = config.is_file()
if config.is_file():
    for line in config.read_text(encoding='utf-8').splitlines():
        if re.match(r'^(model|model_reasoning_effort|sandbox_mode|approval_policy)\s*=', line) or re.match(r'^\[.*hooks.*\]', line):
            data['config_fields'].append(line)
for arg in (['--version'], ['exec', '--help']):
    command = [shutil.which('codex'), *arg]
    result = subprocess.run(command, capture_output=True, timeout=20)
    data[' '.join(arg)] = {'command': command, 'exit_code': result.returncode, 'stdout': result.stdout.decode('utf-8', errors='replace'), 'stderr': result.stderr.decode('utf-8', errors='replace')}
print(json.dumps(data, ensure_ascii=False, indent=2))
