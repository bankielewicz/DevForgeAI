# Limit CLI specification

The selected candidate is `src/limit_cli.py`.

## Requirements

- `LIM-01`: Read `LIMIT` from the environment. Accept only the canonical decimal strings `1` through `100`; surrounding whitespace, signs, decimals, leading zeroes, and non-digits are invalid.
- `LIM-02`: For valid input, write exactly `limit=<N>` plus one newline to stdout, write nothing to stderr, and exit 0.
- `LIM-03`: For missing or invalid input, write exactly `error: invalid limit` plus one newline to stderr, write nothing to stdout, and exit 2.
- `LIM-04`: Do not create, edit, or delete files.

## Acceptance examples

- `LIMIT=7` produces stdout `limit=7\n` and exit 0.
- `LIMIT= 7` produces stderr `error: invalid limit\n` and exit 2.
- `LIMIT=007` produces stderr `error: invalid limit\n` and exit 2.
- Missing `LIMIT` produces stderr `error: invalid limit\n` and exit 2.
