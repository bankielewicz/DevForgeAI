# Experiment constraints supplied by the operator

Synthetic fixture.

- Session: SESSION-208@1, worktree `wt/ferrymap-xplan-006`, branch `experiment/fanout-latency`
- Permitted prototype path: `experiments/XPLAN-006/` only
- Allowed tools and services: local PostgreSQL 16 container, the repository's own test
  harness, local load generation. No cloud services, no production data, no new
  dependencies added to the project manifest.
- Time bound: 4 hours of work, and no single measurement run longer than 10 minutes
- Observable success measure: p95 end-to-end update latency at or under 250 ms with 400
  simulated concurrent viewers on one route
- Observable failure measure: p95 above 250 ms, or the run not sustaining 400 viewers
- Stop conditions: the time bound; anything needing production data or a credential; any
  change required outside `experiments/XPLAN-006/`
