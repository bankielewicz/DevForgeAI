# Retained adaptive tests

Copied the prior 20260913T083452607505Z test_adaptive.py, preserved at its source.
Changed only project ancestry for this new evidence location and the byte-preservation
test to exclude scripts/authoring.py, whose changes SBP-010/011 explicitly require.
The byte baseline is the captured pre-maintenance package, never historical bytes.
All previous schemas and other scripts remain in its preservation assertion.
ADAPTIVE_TEST_ROOT selects a new per-attempt fixture root. All functional cases remain.
This is maintenance regression evidence, not independent skill-validator evaluation.
