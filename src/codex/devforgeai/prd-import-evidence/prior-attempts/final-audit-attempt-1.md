# Retained final-audit attempt 1

The original final audit exited 1 at the assertion that primary Git status was unchanged.
Tool output reported primary_authority_or_source_changes=[], primary_unrelated_dirty_file_changes=[], worktree_readonly_input_or_unrelated_skill_changes=[] and runtime_candidate_changes_after_freeze=[]. Both SPEC-002 hashes remained 90b539a7a4ebdc57da1343c3e11099946872768d97bb66a50af6ab50e5e84e6c.

Before: src/templates/README.md modified; ADR-004.md, SPEC-009.md, the ambiguities template and the handoff prompt untracked. After: only the handoff prompt untracked.

Read-only follow-up found primary HEAD 1dacff87546230f400bb969e0bd5c1e2b43e7043, merging PR 9 for the four previously dirty documentation/template files. Their bytes still match the original baseline. The task worktree stayed on 073a2f2f498a5ebfc88dcf46d75a40bdee8e2216.

This is an overbroad audit expectation, not a source preservation failure. Retain this failed attempt and helper. Audit input bytes and report the concurrent Git-history/status movement separately; do not reset or restore primary state. No final-preservation or delivery manifest was written by attempt 1.
