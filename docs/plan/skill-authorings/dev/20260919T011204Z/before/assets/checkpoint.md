# Checkpoint template

Write after meaningful verified progress and before yielding unfinished work. Preserve older checkpoints.

- Checkpoint identity/time: [unique ID, UTC timestamp]
- Selected project/scope: [resolved identity and current authorization reference]
- Context and selected inputs: [locators and raw-byte hashes]
- Evidence destination identity: [complete selected_evidence_value, original selection_source, resolved_evidence_root and concrete output mapping]
- Traceability/slice/execution records: [actual locations and identities]
- Last verified candidate(s): [source/test/config manifest references and hashes; check IDs; tools/platform]
- Observed changed files and ownership: [current paths/hashes, own edits versus other actors]
- Completed slices: [IDs and current evidence]
- Pending/blocked slices: [IDs, dependencies, exact gaps]
- Outstanding failures/decisions: [references, minimum resolution]
- Owned processes/jobs: [observed identity, command, start time, output locations, known/unknown state, authority to cancel/clean]
- Resume comparison: [changed specs/contracts/evidence-destination selection/source/tests/tools/permissions/jobs; invalidated dependent evidence and placement/completion claims; unaffected retained evidence with reasons; preserved prior outputs]
- Next safe action: [concrete action after required identity/job checks]

A checkpoint is not permission to restore source, replay jobs/migrations, discard changes, or claim a prior result applies to new bytes.
