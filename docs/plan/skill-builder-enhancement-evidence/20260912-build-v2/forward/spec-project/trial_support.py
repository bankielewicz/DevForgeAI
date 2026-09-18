"""Disposable trial evidence support; not part of the generated skill."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import stat
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
BUILDER = Path(r'C:\Projects\DevForgeAI\src\agents\skills\skill-builder')
INPUTS = ROOT.parents[1] / 'forward-inputs'
SPEC = INPUTS / 'decimal-ledger-spec.md'
RUN = '20260912T123744Z-spec'
NAME = 'decimal-ledger-spec'
EVIDENCE = ROOT / 'docs/plan/skill-builds' / NAME / RUN
SNAP = EVIDENCE / 'snapshot'
CANDIDATE = EVIDENCE / 'candidate'
DEST = ROOT / 'src/agents/skills' / NAME
CHECKER = Path(r'C:\Users\bryan\.codex\skills\.system\skill-creator\scripts\quick_validate.py')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def log(value):
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    with (EVIDENCE / 'command-log.jsonl').open('a', encoding='utf-8') as stream:
        stream.write(json.dumps(dict(timestamp_utc=stamp(), **value), ensure_ascii=False) + '\n')
    with (EVIDENCE / 'command-log.md').open('a', encoding='utf-8') as stream:
        stream.write('\n```json\n' + json.dumps(value, indent=2, ensure_ascii=False) + '\n```\n')

def command(argv, purpose, expected=0):
    argv = [str(item) for item in argv]
    result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
    row = dict(cwd=str(ROOT), argv=argv, exact_powershell_command='& ' + ' '.join("'" + part.replace("'", "''") + "'" for part in argv), purpose=purpose, exit_code=result.returncode, stdout=result.stdout, stderr=result.stderr, interpretation='Expected exit observed' if result.returncode == expected else 'UNEXPECTED EXIT; retained without retry')
    log(row)
    print(json.dumps(row, ensure_ascii=False))
    return result

def check_boundary(path):
    for item in [path.absolute(), *path.absolute().parents]:
        if item.exists():
            info = item.lstat()
            assert not stat.S_ISLNK(info.st_mode) and not (getattr(info, 'st_file_attributes', 0) & 0x400), str(item)

def manifest(folder):
    files = []
    for path in sorted(folder.rglob('*')):
        check_boundary(path)
        if path.is_file():
            data = path.read_bytes()
            files.append(dict(path=path.relative_to(folder).as_posix(), bytes=len(data), sha256=sha(data)))
    return dict(schema_version='1', root=str(folder.resolve()), captured_at_utc=stamp(), files=files, excluded_boundaries=[])

def outputs(folder):
    return [dict(path=row['path'], sha256=row['sha256']) for row in manifest(folder)['files']]

def initialize():
    assert not DEST.exists(), 'Destination collision'
    assert not (EVIDENCE / 'build-contract.json').exists(), 'Run occupied'
    for path in (ROOT, SPEC, EVIDENCE, DEST, BUILDER, CHECKER):
        check_boundary(path)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    log(dict(cwd=str(ROOT), tool='apply_patch', action='Created trial_support.py only; exact patch retained in agent transcript', returned_result='Done', interpretation='Evidence helper authoring, not skill execution'))
    log(dict(cwd=r'C:\Projects\DevForgeAI', phase='pre-log discovery', operations=['Get-Content for builder SKILL.md, six referenced documentation/templates, selected spec, sample.csv and invalid.csv', 'Get-ChildItem builder root and scripts directory (names only)', 'Get-Content for build_evidence.py, run_evaluation.py, installed quick_validate.py', 'rg package_links and build_traceability definitions in scripts/graders.py', 'rg memory registry for skill-builder history; historical author-only guidance not applied to current mandatory checks', 'New-Item disposable root; Get-Date; python --version; Get-Command codex; $PSVersionTable'], exit_codes=[0,0,0,0,0,0], stream='combined', observed='Selected target decimal-ledger-spec; destination absent; sample rows 0.10,0.20,3.45,-1.10; invalid row NaN. Python 3.10.11, Windows 10.0.26200, PowerShell 7.6.6. No codex executable returned. One documentation batch output was truncated; evaluation.md was subsequently reread in full.', limitation='Pre-log command tool transcript retains exact commands/output; this entry is explicitly a summary, not a fabricated full stream. Subsequent subprocess operations retain exact arguments and separate stdout/stderr.'))
    command(['pwsh', '-NoProfile', '-Command', "$PSVersionTable | ConvertTo-Json; if (Get-Command codex -ErrorAction SilentlyContinue) { codex --version } else { Write-Output 'Codex CLI unavailable on PATH; identity NOT_OBSERVED' }"], 'Identify terminal and CLI availability')
    command([sys.executable, '-B', '-X', 'utf8', '-c', 'import platform,sys,yaml; print(sys.version); print(platform.platform()); print("PyYAML",yaml.__version__)'], 'Identify Python and checker/resolver dependency')
    resolution = command([sys.executable, '-B', '-X', 'utf8', BUILDER/'scripts/build_evidence.py', 'resolve-spec', '--project-root', ROOT, '--spec', SPEC], 'Resolve explicitly selected specification')
    assert resolution.returncode == 0
    write_json(EVIDENCE/'selection.json', json.loads(resolution.stdout))
    data = SPEC.read_bytes()
    record = command([sys.executable, '-B', '-X', 'utf8', BUILDER/'scripts/build_evidence.py', 'input-record', '--file', SPEC, '--id', 'selected-spec', '--snapshot-path', 'inputs/decimal-ledger-spec.md', '--role', 'spec', '--start-byte', '0', '--end-byte', str(len(data))], 'Bind original specification raw bytes')
    assert record.returncode == 0
    selected = json.loads(record.stdout)['input']
    (SNAP/'inputs').mkdir(parents=True)
    (SNAP/'inputs/decimal-ledger-spec.md').write_bytes(data)
    assert (SNAP/'inputs/decimal-ledger-spec.md').read_bytes() == data
    write_json(EVIDENCE/'original-inputs-before.json', dict(schema_version='1', files=[dict(path=str(path.resolve()), bytes=len(path.read_bytes()), sha256=sha(path.read_bytes())) for path in (SPEC, INPUTS/'sample.csv', INPUTS/'invalid.csv')]))
    mapping = {
        'REQ-01': ['SKILL.md', 'scripts/sum_amounts.py'],
        'REQ-02': ['SKILL.md', 'scripts/sum_amounts.py', 'assets/result.schema.json'],
        'REQ-03': ['SKILL.md', 'scripts/sum_amounts.py', 'assets/result.schema.json', 'references/workers/result-review.md'],
        'REQ-04': ['SKILL.md', 'scripts/sum_amounts.py'],
        'REQ-05': ['SKILL.md', 'references/workers/result-review.md'],
        'REQ-06': ['SKILL.md', 'scripts/sum_amounts.py'],
    }
    expectations = {
        'REQ-01': 'Execute BOM, quoted fields, negative amounts, missing header, empty/nonfinite/overprecision values.',
        'REQ-02': 'Observe exact count/total fields and decimal result 2.65; header-only CSV gives 0 and 0.00; large decimal total remains exact.',
        'REQ-03': 'Structural checker and resource links pass; required args, success stdout, stderr diagnostics, exit 2 and no-overwrite cases executed; inspect schema.',
        'REQ-04': 'Input raw-byte digests match before/after; invalid input and output conflicts preserve previous output; inspect standard-library-only helper.',
        'REQ-05': 'Run sequential read-only result review against produced JSON and before/after original input digests.',
        'REQ-06': 'Observe Python >=3.10 and PowerShell; inspect imports and frontmatter; no install or runtime config changes.',
    }
    requirements = []
    for rid, paths in mapping.items():
        start = data.index((rid + ' ').encode())
        end = data.find(b'\n\n', start)
        if end == -1:
            end = len(data)
        excerpt = data[start:end]
        requirements.append(dict(id=rid, origin='source', text=excerpt.decode('utf-8').strip(), source_refs=[dict(input_id='selected-spec', start_byte=start, end_byte=end, sha256=sha(excerpt))], artifact_paths=paths, verification=[dict(method='bounded script exercises plus editorial readback', expected=expectations[rid])]))
    artifacts = [dict(path=path, role=role, requirement_ids=[rid for rid, paths in mapping.items() if path in paths], purpose=purpose) for path, role, purpose in [('SKILL.md','entrypoint','Select CSV-total tasks and route invocation/resources/review'),('scripts/sum_amounts.py','supporting script','Exact decimal CSV sum and exclusive JSON creation'),('assets/result.schema.json','schema','Exact count and two-place total output contract'),('references/workers/result-review.md','reference','Advisory read-only output and input-preservation review')]]
    contract = dict(schema_version='1', mode='spec_build', target_name=NAME, inputs=[selected], authorization=dict(instruction='Explicit independent forward trial: build from the selected approved specification in this disposable project; bounded local exercises authorized; no installation or writes outside project.', inputs=[dict(id=selected['id'], sha256=selected['sha256'])]), purpose='Summarize the amount column of a supplied local CSV using exact decimal arithmetic.', activation=dict(positive=["Total the amount column in this local CSV into a new JSON file."], excluded=['explanation alone','transaction categorization','network data retrieval','editing the original CSV']), requirements=requirements, artifacts=artifacts, workers=[dict(role='result-review', requirement_ids=['REQ-05'], inputs=['actual produced JSON path','original input path and pre-run SHA-256'], output='findings and inspected paths with observed input digest comparison', assigned_write_paths=[], tools=['Python standard library or PowerShell read-only terminal'], independent_execution='optional; sequential main-agent execution explicitly allowed', isolation='none required', failure_behavior='Report mismatch or missing evidence; no repair or acceptance decision')], dependencies=[dict(name='Python', requirement='3.10+ standard library only', availability=platform.python_version(), digest_verification='Runtime identity observed; binary digest qualification not claimed'),dict(name='Windows PowerShell terminal', requirement='terminal execution', availability='PowerShell 7.6.6 on Windows, observed', digest_verification='Not required by source contract')])
    write_json(EVIDENCE/'build-contract.json', contract)
    write_json(SNAP/'evidence/build-contract.json', contract)
    write_json(EVIDENCE/'spec-gaps.json', dict(schema_version='1', gaps=[]))
    write_json(EVIDENCE/'boundary.json', dict(project=str(ROOT), input=str(SPEC), destination=str(DEST), evidence=str(EVIDENCE), original_paths_checked_for_reparse_points=True, exclusions=['source Claude package','tests contents','deterministic-candidate','other trials','implementation logs','backup directories','legacy CLI/hook folders'], note='No excluded contents inspected. Required evaluator will internally hash its own complete bound builder package; this is its mandatory integrity check, not a manual fixture inspection.'))
    log(dict(cwd=str(ROOT), action='Captured specification snapshot, raw byte requirement slices, contract and empty gaps before candidate generation', output=str(EVIDENCE/'build-contract.json'), contract_sha256=sha((EVIDENCE/'build-contract.json').read_bytes()), interpretation='No essential contract gaps found; authoring can proceed'))
    print(str(EVIDENCE))

if __name__ == '__main__':
    assert len(sys.argv) == 2 and sys.argv[1] == 'init'
    initialize()
