# Retained test adaptations

Historical test files remain unchanged at their source. Copies adjust repository ancestry to this evidence directory; `retained-test-receipts.json` records the original and initial copied hashes.

The historical `test_old_stage_without_mode_remains_publishable` test began a new no-design stage, deleted its `design_capture_requested` field and expected publication. The selected origin-digest binding makes this a changed-stage rejection case. The copied test is renamed `test_changed_stage_without_mode_blocks_publication` and requires BLOCKED, absent destination, and absent successful baseline. Existing genuine no-design cases continue to require AUTHORED. This adapts the explicit new contract, not a failing implementation.

The adaptive preservation baseline is the parent's pre-repair package in `../before`, captured in `builder-before.json`. Its existing exception for `scripts/authoring.py` remains because that is the selected repair target; all other selected schema/script paths retain exact byte assertions.

Additional runtime-original tests execute the original shipped asset against retained fixture oracles; the original suite still exercises copied installation fixtures separately. CLI coverage instrumentation executes actual Python scripts with their original arguments and inspects their real returned outputs.

After qa-01, two retained design tests that mutate origin/design inside `before_write` are updated to require BLOCKED with no applied files; the new pre-write boundary catches their injected mutation before writing. They formerly expected PARTIAL after the write. The old-noncanonical-stage diagnostic assertion now checks the fresh-run instruction across the returned failure record, because stage-integrity rejection occurs before the previous conflict `issues` field. Rejection and input/destination preservation assertions remain.

qa-01 exposed a coverage harness import error: coverage execution did not preserve direct-script sys.path[0]. coverage_driver.py restores the target script directory and uses runpy to execute its unchanged bytes with its original arguments. This fixes instrumentation only.

V3 defers destination creation until after the before_write callback and stage check. Two retained fault callbacks previously assumed the destination directory already existed. After preserving v3-authoring's two failures, each callback now explicitly creates its target before simulating the external writer or making that destination unreadable. All original state, applied-path, other-writer byte, and unavailable-capture assertions remain unchanged. This establishes the same intended competing-writer/unreadable-filesystem scenario at the corrected earlier callback boundary.
