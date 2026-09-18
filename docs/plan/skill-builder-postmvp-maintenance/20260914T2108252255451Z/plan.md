# Maintenance scope declared before changes

Implement SBP-001 through SBP-016 in development skill-builder only. No installation,
validator modification, generated-skill campaign, or Rust authority change.

Executable coverage denominator: all executed-line statements in authoring.py and
record_schema.py, the changed custody implementation and its schema dependency;
no excluded lines. Branch coverage reported separately. Other unchanged builder
modules are exercised by applicable retained regression tests but are not claimed
as fully covered by this focused maintenance measurement. Platform: native Windows.
Linux and cold native skill qualification remain separate NOT_RUN obligations.

Required maintenance inventory: every unittest case in test_design.py plus retained
test_authoring.py and test_authoring_safeguards.py; adaptive regression inventory
will be frozen before execution after reviewing current fixture setup. Expected
red failures are retained as TDD evidence; green/QA case counts are separate, and
failed attempts are never deleted or averaged away. 95% line coverage and case pass
rate are independently required for the declared maintenance scope.

Use disposable local fixtures with spaces/Unicode, file-delivery/readback assertions,
invalid input and mutation probes, legacy calls and unchanged validator intake.
Each maintenance command has a 120-second execution ceiling, no product timeout
claim, no automatic retry. No network, native agent invocation, or external effect.
The separate validator task owns SBPV-01 through SBPV-18 behavioral qualification,
including two end-to-end generated skills and independent oracles.
