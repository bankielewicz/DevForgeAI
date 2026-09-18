"""Independent specification-derived QA ledger; never imports either skill."""
from pathlib import Path
import datetime
import hashlib
import json
import platform
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[4]
SUBCASES = {
    '01': ['cold-create', 'focused-edit', 'manual-handoff-byte-binding', 'no-quality-process'],
    '02': ['two-languages', 'unknown-manifest', 'dependency-exclusion', 'junction-exclusion', 'no-project-script'],
    '03': ['2000-file-boundary', '2001-file-limit', '32MiB-boundary', '32MiB-plus-one-limit', 'missing-python', 'missing-rust-enforcement', 'independent-proposal-retained'],
    '04': ['http-retained', 'storage-evidence', 'no-redundant-persona', 'supporting-locators'],
    '05': ['missing-disposition', 'unauthorized-removal', 'complete-three-row-lineage', 'core-preserved'],
    '06': ['adaptive-authoring', 'relocation', 'no-concrete-identity', 'relative-runtime-paths'],
    '07': ['bound', 'missing', 'invalid', 'root-mismatch', 'unbound', 'package-changed', 'role-mismatch', 'not-selected', 'ambiguous-role', 'unsafe-path', 'capture-limit', 'io-error', 'duplicate-name', 'no-product-effects'],
    '08': ['all-valid-record-families', 'duplicate-key', 'extra-field', 'unknown-version', 'malformed-reference', 'malformed-digest', 'unresolved-id', 'boolean-integer', 'nonfinite-number', 'misleading-lineage-text'],
    '09': ['legacy-authoring-contract', 'legacy-validation-request', 'closed-top-level', 'legacy-reference-base'],
    '10': ['a-fails', 'b-dependency-blocked', 'c-authored', 'aggregate-partial', 'eligible-subset', 'subset-dependency-closure'],
    '11': ['cycle', 'missing-dependency', 'occupied-target', 'user-edited-obsolete', 'concurrent-drift', 'partial-paths'],
    '12': ['positive-propose', 'positive-author-set', 'positive-review-updates', 'negative-install', 'negative-test-only', 'explicit-native', 'implicit-discovery'],
    '13': ['no-change', 'equal-semantics-changed-bytes', 'removed-required-contract', 'missing-parent', 'no-auto-rebase'],
    '14': ['python-tdd', 'rust-implementation-first', 'typescript-monorepo', 'documentation-only'],
    '15': ['spaces', 'non-ascii', 'shell-significant', 'missing-interpreter', 'offline', 'no-install'],
    '16': ['evidence-drift', 'fresh-linked-proposal', 'no-stale-approval'],
    '17': ['claude-import', 'observed-first-edit', 'authored-baseline', 'legacy-generated', 'legacy-adopted', 'corrupt-history', 'no-fake-complete'],
}

def write(name, value):
    (ROOT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    for name in ('inputs', 'commands', 'source', 'fixtures', 'native', 'reports'):
        (ROOT / name).mkdir(exist_ok=True)
    inputs = []
    for filename in ('AGENTS.md', 'docs/plan/skill-builder-independent-qa-prompt.md', 'docs/plan/skill-builder-adaptive-enhancement-spec.md', 'docs/plan/skill-validator-adaptive-enhancement-spec.md'):
        path = PROJECT / filename
        data = path.read_bytes()
        (ROOT / 'inputs' / path.name).write_bytes(data)
        inputs.append({'path': filename, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    write('inputs/manifest.json', inputs)
    spec = (ROOT / 'inputs/skill-builder-adaptive-enhancement-spec.md').read_text(encoding='utf-8')
    rows = []
    for line_no, line in enumerate(spec.splitlines(), 1):
        if re.match(r'\| BA-\d{3} \|', line):
            fields = [x.strip() for x in line.split('|')[1:-1]]
            rows.append({'requirement': fields[0], 'oracle': fields[1], 'cases': fields[2], 'spec_line': line_no, 'status': 'NOT_RUN', 'source_locations': [], 'evidence': []})
    write('requirements.json', rows)
    cases = []
    for line_no, line in enumerate(spec.splitlines(), 1):
        match = re.match(r'\| BAT-(\d\d) \|', line)
        if match:
            fields = [x.strip() for x in line.split('|')[1:-1]]
            for suffix in SUBCASES[match[1]]:
                cases.append({'id': fields[0] + '-' + suffix, 'fixture': fields[1], 'oracle': fields[2], 'spec_line': line_no, 'status': 'NOT_RUN', 'platforms': ['Windows/PowerShell', 'Linux/POSIX'], 'timeout_seconds': 120, 'effects_root': str(ROOT), 'evidence': []})
    write('cases.json', cases)
    clauses = []
    section = ''
    for number, line in enumerate(spec.splitlines(), 1):
        if line.startswith('#'):
            section = line
        elif line.strip() and not line.startswith('| BA-') and not line.startswith('| BAT-'):
            clauses.append({'id': f'SPEC-L{number}', 'section': section, 'text': line, 'status': 'NOT_RUN', 'source_locations': [], 'evidence': []})
    write('complete-clause-inventory.json', clauses)
    write('host.json', {'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat(), 'platform': platform.platform(), 'python': sys.version, 'python_path': sys.executable, 'codex': shutil.which('codex'), 'wsl': shutil.which('wsl'), 'timeout_seconds': 120})
    for title, command in [('python-version', [sys.executable, '--version']), ('codex-version', [shutil.which('codex'), '--version']), ('codex-exec-help', [shutil.which('codex'), 'exec', '--help'])]:
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        result = subprocess.run(command, capture_output=True, timeout=120)
        (ROOT / 'commands' / (title + '.stdout')).write_bytes(result.stdout)
        (ROOT / 'commands' / (title + '.stderr')).write_bytes(result.stderr)
        write('commands/' + title + '.json', {'argv': command, 'cwd': str(PROJECT), 'started': start, 'exit_code': result.returncode, 'timeout_seconds': 120})
    print(json.dumps({'root': str(ROOT), 'requirements': len(rows), 'subcases': len(cases), 'clauses': len(clauses)}))

if __name__ == '__main__':
    main()
