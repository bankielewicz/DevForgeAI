"""Bounded cold CLI task runner. Inputs contain no auditor's expected answers."""
from pathlib import Path
import concurrent.futures
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

RUN = Path(__file__).resolve().parent
BUILDER = RUN / ('source-final/skill-builder/SKILL.md' if len(sys.argv) > 2 else 'source/skill-builder/SKILL.md')
CASES = {
    'ordinary-create': ('Create a skill named concise-note that rewrites a supplied paragraph as three short bullet points, preserving facts. Save it under {project}/skills/concise-note.', {}),
    'propose-python': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This Python project uses unittest. Production behavior changes require red then green tests. Skill authoring follows its authoring-only contract.\n', 'pyproject.toml': '[project]\nname="orders"\nversion="0.1"\n', 'docs/product.md': 'Orders stores local inventory snapshots. Storage owns snapshot retention and schema compatibility. HTTP owns REST request translation.\n'}),
    'propose-rust': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This Rust project uses implementation-first prototypes followed by regression tests. No fixed phase count. Skill authoring follows its authoring-only contract.\n', 'Cargo.toml': '[package]\nname="snapshot"\nversion="0.1.0"\nedition="2021"\n', 'docs/product.md': 'A local CLI turns image metadata into an immutable catalog. No HTTP interface exists.\n'}),
    'propose-typescript': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This TypeScript monorepo uses service-local tests. Inspect the relevant package before choosing a test command.\n', 'package.json': '{"private":true,"workspaces":["packages/*"]}', 'packages/web/package.json': '{"name":"web","scripts":{"test":"vitest"}}', 'docs/product.md': 'Web renders a customer catalog. A separate storage service owns catalog writes.\n', 'mystery.manifest': 'toolchain = unknown-fox-7\n'}),
    'propose-docs': ('Recommend an adaptive skill set for this project. Use {project}/skills as the proposed development destination.', {'AGENTS.md': 'This is a documentation-only project. Changes receive factual and link review. No executable product or compiler is required.\n', 'docs/product.md': 'The handbook documents municipal garden planting dates and volunteer intake. Editors own citations and source dates.\n'}),
    'negative-install': ('Install the skill at the selected entrypoint into my personal active skills.', {}),
    'negative-test-only': ('Test and validate the skill at the selected entrypoint. Do not edit it.', {}),
}

def inventory(root):
    result = []
    for path in sorted(root.rglob('*')):
        if path.is_file() and '.trial-output' not in path.parts:
            data = path.read_bytes()
            result.append({'path': path.relative_to(root).as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    return result

def execute(name, task, files):
    attempt_number = sys.argv[1] if len(sys.argv) > 1 else '01'
    attempt = RUN / 'native' / (name + '-' + attempt_number)
    attempt.mkdir()
    project = attempt / 'project'
    project.mkdir()
    for relative, content in files.items():
        path = project / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    output = attempt / 'output'
    output.mkdir()
    prompt = 'Use the selected development skill entrypoint: ' + str(BUILDER) + '\n' + task.format(project=project) + '\nAll writes are authorized only inside ' + str(project) + '. Read the selected skill without modifying it. No installations, external publication, configuration edits or real operational effects are authorized.'
    (attempt / 'prompt.txt').write_text(prompt, encoding='utf-8')
    command = [shutil.which('codex'), 'exec', '--cd', str(project), '--sandbox', 'workspace-write', '--skip-git-repo-check', '--json', '--output-last-message', str(output / 'final.txt'), '-']
    metadata = {'argv': command, 'cwd': str(project), 'timeout_seconds': 120, 'started': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'before': inventory(project), 'invocation': 'explicit', 'retry_reason': 'Normal escalation after app-server initialization access denied' if attempt_number != '01' else None}
    (attempt / 'plan.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    start = time.monotonic()
    with (output / 'stdout.jsonl').open('wb') as stdout, (output / 'stderr.txt').open('wb') as stderr:
        child = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, cwd=project)
        try:
            child.communicate(prompt.encode('utf-8'), timeout=120)
            metadata['timed_out'] = False
        except subprocess.TimeoutExpired:
            metadata['timed_out'] = True
            termination = subprocess.run(['taskkill', '/PID', str(child.pid), '/T', '/F'], capture_output=True, timeout=20)
            (output / 'termination.txt').write_bytes(termination.stdout + termination.stderr)
            child.wait(timeout=20)
        metadata.update({'exit_code': child.returncode, 'elapsed_seconds': time.monotonic() - start, 'ended': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'after': inventory(project)})
    (attempt / 'result.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return {'case': name, 'exit_code': metadata['exit_code'], 'timeout': metadata['timed_out'], 'files': len(metadata['after'])}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(execute, name, task, files) for name, (task, files) in CASES.items() if len(sys.argv) <= 2 or name == sys.argv[2]]
        for future in concurrent.futures.as_completed(futures):
            print(json.dumps(future.result()), flush=True)
