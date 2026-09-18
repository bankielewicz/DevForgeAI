# Preparation observation

The first compiled `profile-sources` observation exited 0 in 0.094 seconds and
produced 137 entries with 36 physical file bindings. No Codex process was launched.
The subsequent Python evidence preparation stopped at its path equality check:
Rust emitted the standard Windows extended path prefix `\\?\`, while the fixture
constant used the ordinary absolute spelling. This was an evidence-helper
assertion, not a product defect or native attempt.

The originally executed helper is retained as `diagnostic-preparation-001.py`;
its exact digest is in `sources-001/started.json`. The helper now normalizes only
the standard prefix for that comparison. The initial binding step consumes the
same successful source observation without running the collector again. The
compiled Rust source, binary, predicates, inventory bytes and fixture are unchanged.

The supervisor also preserves the prior successful supervisor's inherited-console
launch behavior. Window handling for the native worker remains in unchanged Rust.
No native invocation had occurred at the time of either recorder adjustment.
