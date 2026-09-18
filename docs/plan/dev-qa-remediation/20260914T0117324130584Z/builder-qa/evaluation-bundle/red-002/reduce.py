"""Reduce retained helper executions; this does not execute product or skill trials."""
import json
from pathlib import Path
import re


def grade_execution(receipt, stderr, expected_count):
    if receipt.get('exit_code') != 0:
        raise ValueError('execution failed')
    summary = re.search(r'^Ran (\d+) tests? in ', stderr, re.MULTILINE)
    if not summary or int(summary.group(1)) != expected_count:
        raise ValueError('test count mismatch')
    if not re.search(r'^OK\s*$', stderr, re.MULTILINE):
        raise ValueError('suite did not pass')
    rows = re.findall(r'^(test_\S+ \([^\r\n]+\)) \.\.\. ([^\r\n]+)', stderr, re.MULTILINE)
    if len({name for name, _ in rows}) != len(rows):
        raise ValueError('duplicate case identifiers')
    if len(rows) != expected_count or any(state != 'ok' for _, state in rows):
        raise ValueError('case outcomes incomplete')
    return {'passed': len(rows), 'required': expected_count}


def bound_bytes(reference):
    return Path(reference['path']).read_bytes()
