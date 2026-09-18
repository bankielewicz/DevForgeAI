"""Fresh bounded CLI fixtures; source is read-only, outputs are retained per attempt."""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import signal
import subprocess
import time

def put(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

def manifest(root):
    return [{'path':p.relative_to(root).as_posix(), 'bytes':p.stat().st_size,
             'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]

def run(args):
    folder = Path(args.root) / args.case
    folder.mkdir(parents=True, exist_ok=False)
    project = folder / 'Project space'
    project.mkdir()
    simple = '-simple' in args.case
    package = project / ('builder-source' if simple else '.agents/skills') / 'skill-builder'
    source = Path(args.source)
    original = manifest(source)
    shutil.copytree(source, package, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    copied = manifest(package)
    if copied != original:
        raise RuntimeError('Source copy mismatch')
    put(folder/'source-manifest.json', original)
    output = project/'result-skill'/('sort-lines' if simple else 'count-lines')
    if simple:
        request = f'Use the skill-builder instructions at {package / "SKILL.md"}. Create a skill named sort-lines. It accepts newline-separated text supplied in the user message, removes empty lines, sorts remaining lines by Unicode code-point order, preserves duplicates, and returns only sorted lines. Runtime reads/writes of files are unnecessary. '
    else:
        request = 'Create a Codex development skill named count-lines. It accepts a user-selected UTF-8 input file and literal output directory. Mode count writes count.json with {"nonempty_lines": integer}; mode list writes lines.txt with nonempty lines in original order, duplicates retained, LF separators. Load only the instructions needed by the chosen mode. Preserve the input. Missing input or invalid UTF-8 writes failure.json with {"status":"FAILED","reason":string,"input":string}; if that cannot be delivered report incomplete delivery. Refuse to overwrite any existing result or failure.json. A reusable deterministic helper is appropriate. '
    prompt = request + f'Save the development package at {output}. Selected project: {project}. Complete authoring and its manual validation handoff. All authoring writes are authorized only inside this synthetic project. The copied builder-source and .agents fixture are read-only inputs; do not install or alter active skills. No external messaging or network operations. Do not execute the generated skill or run its tests; an independent evaluator owns that step.'
    (folder/'prompt.txt').write_text(prompt, encoding='utf-8')
    (project/'AGENTS.md').write_text('# Synthetic authoring project\nAll generated artifacts must stay inside this project. The provided builder-source or .agents/skills package is an immutable test input. Use development result-skill destinations. Do not install anything.\n', encoding='utf-8')
    command = [args.codex or shutil.which('codex'), 'exec', '--cd', str(project), '--sandbox', 'workspace-write', '--skip-git-repo-check', '--json', '--output-last-message', str(project/'final.txt'), '-']
    put(folder/'plan.json', {'case':args.case, 'platform':platform.platform(), 'python':platform.python_version(), 'executable':command[0], 'command':command, 'cwd':str(project), 'source':str(source.resolve()), 'discovery':'explicit source load' if simple else 'implicit project skill discovery', 'timeout_seconds':120, 'retry_policy':'No automatic retry of native timeout', 'expected':['selected package read', 'original requirements and design captured', 'authored destination with publication/baseline and manual validator request', 'source fixture unchanged'], 'filesystem':'Windows NTFS' if os.name=='nt' else 'Linux native /tmp, source read over /mnt/c'})
    put(folder/'before.json', manifest(project))
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    timeout = False
    cleanup = None
    with (folder/'stdout.jsonl').open('xb') as stdout, (folder/'stderr.txt').open('xb') as stderr:
        options = {'creationflags':subprocess.CREATE_NO_WINDOW} if os.name=='nt' else {'start_new_session':True}
        process = subprocess.Popen(command, cwd=project, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, **options)
        try:
            process.communicate(prompt.encode('utf-8'), timeout=120)
        except subprocess.TimeoutExpired:
            timeout = True
            if os.name=='nt':
                result = subprocess.run(['taskkill','/PID',str(process.pid),'/T','/F'],capture_output=True,timeout=15,creationflags=subprocess.CREATE_NO_WINDOW)
                cleanup = {'method':'taskkill /T /F', 'exit_code':result.returncode, 'stdout':result.stdout.decode(errors='replace'), 'stderr':result.stderr.decode(errors='replace')}
            else:
                os.killpg(process.pid, signal.SIGKILL)
                cleanup = {'method':'killpg SIGKILL', 'process_group':process.pid}
            process.wait(timeout=15)
    put(folder/'after.json', manifest(project))
    receipt = {'started_at_utc':started, 'elapsed_seconds':time.monotonic()-clock, 'exit_code':process.returncode, 'timed_out':timeout, 'pid':process.pid, 'cleanup':cleanup, 'source_fixture_unchanged':manifest(package)==original, 'source_unchanged':manifest(source)==original, 'destination_exists':output.exists(), 'status':'INCOMPLETE' if timeout or process.returncode else 'REQUIRES_ARTIFACT_REVIEW'}
    put(folder/'attempt-001.json', receipt)
    print(json.dumps(receipt))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--case', required=True)
    parser.add_argument('--codex')
    run(parser.parse_args())
