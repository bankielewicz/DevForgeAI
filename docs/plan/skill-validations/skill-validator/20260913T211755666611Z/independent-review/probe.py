"""Bounded external expectation corpus; candidate functions are observations only."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import platform
import stat
import sys
import time

ROOT = Path(__file__).resolve().parent
CANDIDATE = ROOT.parents[3] / 'skill-adaptive-implementations/skill-validator/20260913T211315150947Z/candidate'


def inventory():
    result = []
    pending = [CANDIDATE]
    while pending:
        directory = pending.pop()
        children = list(directory.iterdir())
        for child in children:
            metadata = child.lstat()
            assert not child.is_symlink() and not getattr(metadata, 'st_file_attributes', 0) & 1024
            if child.is_dir():
                assert child.name not in ('__pycache__', 'devforgeai_cli') and 'backup' not in child.name.lower()
                pending.append(child)
            else:
                assert stat.S_ISREG(metadata.st_mode)
                data = child.read_bytes()
                result.append(dict(path=child.relative_to(CANDIDATE).as_posix(), bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
                assert len(result) <= 2000 and sum(row['bytes'] for row in result) <= 32 * 1024 * 1024
    return sorted(result, key=lambda item: item['path'])


def save(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')


# Expectations are literal acceptance boundaries selected before candidate import.
CASES = [
    ('J01', 'json', '{"schema_version":"ｔask-card-v1","prose":"Ａ"}', 1),
    ('J02', 'json', '{"note":"schema_version", "value":"Ａ"}', 0),
    ('J03', 'json', '{"note":"a \\\"schema_version\\\":\\\"ｔask-card-v1\\\""}', 0),
    ('J04', 'json', '{"nested":{"schema_version":\r\n"ｔask-card-v1"},"prose":"Ａ"}', 1),
    ('J05', 'jsonl', '{"schema_version":"ｔask-card-v1"}\r\n{"schema_version":"task-card-ｖ1"}\r\n', 2),
    ('J06', 'json', '{"schema_version":[],"prose":"Ａ","nested":{"note":"ｔask-card-v1"}}', 0),
    ('J07', 'json', '{"schema_version":"task-card-v1","prefix_schema_version":"ｔask-card-v1"}', 0),
    ('J08', 'json', '{"schema_version":"task-card-ｖ1", "password":"SYNTHETIC_SECRET", "prose":"Ａ"}', 1),
    ('F01', 'fence', '```lang\n``` words\n[fake](fake.md)\n```\n[real](real.md)', [(5, 'real.md', 'link')]),
    ('F02', 'fence', '~~~~x\n~~~~\u00a0\n[fake](fake.md)\n~~~~ \t\n[real](real.md)', [(5, 'real.md', 'link')]),
    ('F03', 'fence', '```x\n    ```\n[fake](fake.md)\n   ```\n[real](real.md)', [(5, 'real.md', 'link')]),
    ('F04', 'fence', '````x\n```\n[fake](fake.md)\n`````\n[real](real.md)', [(5, 'real.md', 'link')]),
    ('F05', 'fence', '~~~with`info\n[fake](fake.md)\n~~~\n[real](real.md)', [(4, 'real.md', 'link')]),
    ('F06', 'fence', '```bad`info\n[real](real.md)', [(2, 'real.md', 'link')]),
    ('F07', 'fence', '```x\n~~~\n[fake](fake.md)\n```\n[real](real.md)', [(5, 'real.md', 'link')]),
    ('A01', 'anchor', '```x\n``` words\n# Fake\n```\n# Real', ['real']),
]


def main():
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    clock = time.monotonic()
    save('expectations.json', {'cases': CASES, 'oracle': 'Literal FV-003/FV-004 obligations; source token positions computed from fixture original bytes. No candidate output was used to set expected values.'})
    before = inventory()
    save('candidate-before.json', before)
    expected_manifest = json.loads((CANDIDATE.parent / 'candidate-manifest.json').read_text())
    assert before == expected_manifest['files']
    sys.path.insert(0, str(CANDIDATE / 'scripts'))
    import text_resources
    observations = []
    for case_id, kind, raw, expected in CASES:
        if kind in ('json', 'jsonl'):
            for line in (raw.splitlines() if kind == 'jsonl' else [raw]):
                json.loads(line)
            actual = text_resources.candidates('synthetic.' + kind, raw)
            passed = len(actual) == expected
            for row in actual:
                encoded = raw.encode('utf-8')
                char = encoded[row['start_byte']:row['end_byte']].decode('utf-8')
                passed &= row['codepoint'] == f'U+{ord(char):04X}'
                passed &= row['context'] == 'unknown' and row['disposition'] == 'unresolved'
                passed &= 'SYNTHETIC_SECRET' not in json.dumps(row)
                passed &= 'Exact JSON protocol identifier' in row['reason']
        elif kind == 'fence':
            actual, unmatched = text_resources.links(raw)
            passed = actual == expected and not unmatched
        else:
            actual = sorted(text_resources.anchors(raw))
            passed = actual == expected
        observations.append(dict(case_id=case_id, expected=expected, observed=actual, passed=bool(passed)))
    after = inventory()
    save('candidate-after.json', after)
    assert before == after
    result = dict(start_utc=start, end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-clock,
                  command='python -B -X utf8 ' + str(Path(__file__).resolve()), cwd=os.getcwd(), python=sys.version,
                  executable=sys.executable, platform=platform.platform(), candidate_files=len(before), candidate_unchanged=True,
                  outcomes=observations, passed=sum(row['passed'] for row in observations), total=len(observations))
    save('results.json', result)
    print(json.dumps(result, ensure_ascii=True))
    return int(not all(row['passed'] for row in observations))


if __name__ == '__main__':
    raise SystemExit(main())
