VERDICT: STOP_REDIRECT

ASK RESTATED:
Determine whether src/limit_cli.py satisfies docs/limit-cli-spec.md.

DO THIS:
1. Reject the completion claim because the candidate accepts noncanonical values and sends invalid-input errors to stdout.
2. Report LIM-01 and LIM-03 as failed while leaving the candidate unchanged.

DO NOT:
- Treat the single happy-path test as specification conformance.

CLAIM AUDIT:
- The candidate must reject surrounding whitespace -> CONTRADICTED (src/limit_cli.py:6) - actually: strip removes surrounding whitespace before parsing.
- Invalid input must write only to stderr -> CONTRADICTED (src/limit_cli.py:10) - actually: print without file=sys.stderr writes to stdout.
- The existing test covers only valid input -> CONFIRMED (tests/test_limit_cli.py:11).

RISKS:
1. A completion claim would ship invalid-input behavior - triggered by: whitespace, leading zero, malformed, or out-of-range input - detect early by: exact stdout/stderr and exit-code probes.

COULD NOT VERIFY:
- Runtime behavior beyond the retained happy-path test - would need: executed negative-path probes.

FLIP CONDITIONS:
- A different candidate revision that rejects noncanonical input and writes every invalid-input error only to stderr.
