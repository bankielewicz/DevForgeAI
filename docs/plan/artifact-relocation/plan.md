# Evidence relocation execution contract

Selected by Bryan on 2026-09-18. This is the implementation contract for the
approved five-checkpoint plan, not a framework acceptance record.

## Objective and selected decisions

Separate project records, retained evidence, working Git checkouts and rebuildable
material. Preserve bytes and evidence provenance while repairing retrieval.
Keep bulky evidence local, move eligible collections on the same volume, and use
one dedicated worktree/branch/stacked draft PR per checkpoint. No automatic merge.

Existing registered worktrees stay under the primary checkout's `worktrees/git/`.
Approved evidence destinations are under its `artifacts/evidence/`. Do not rename
the parent `worktrees` directory or restore all moved material into Git.

## Checkpoints

1. **Inventory:** classify all 64 non-Git collections; record counts, logical sizes,
   skipped reparse points, read errors, references, initial holds and limitations.
   Publish this contract and a compact inventory. No collection moves.
2. **Policy and retrieval:** define the four storage classes, ownership, holds,
   retention eligibility and local-only access limits in DFF-04/08/10. Add an
   AGENTS.md progressive-disclosure pointer, storage procedure and relocation
   catalog. Repair current navigation using verified immutable Git references
   where available. Keep historical sealed documents unchanged.
3. **Tool:** implement bounded native PowerShell Inventory/Preview/Relocate/Verify
   operations. Explicit root, selected plan and expected plan digest govern each
   operator-selected relocation. Publish tests and a preview, never raw collections.
4. **Pilot:** relocate framework-foundation and framework-mvp-planning if admitted;
   verify complete file manifests, retrieval and preservation; publish receipts.
5. **Rollout:** relocate other eligible collections one at a time. Publish final
   accounting, named holds, retrieval results and cleanup candidates. A collection
   may remain held; it must never disappear from the accounting.

The initial branch starts at verified origin/main. Each later branch starts from
the preceding checkpoint's exact committed head and its draft PR targets that
branch. Commit/push/verify each checkpoint; never force-push or merge automatically.
Keep changes to existing operator-console worktrees and PRs out of this task.

## Inventory, identity and retrieval

Record source/original/proposed locations, collection identity, purpose, owner,
dependency references, holds, file counts, logical bytes and classification status.
Unknown ownership or a location-dependent consumer is a hold, not permission.
Classify mixed collections conservatively; a build-directory name alone never
establishes disposability. Skip reparse points and record their presence.

Keep detailed inventories, per-file hashes and raw receipts local; publish compact
summaries and digests. A hash is not a replacement for the underlying evidence.
Link to an immutable historical Git object only after verifying matching bytes and
that its commit is on published history. Otherwise disclose local-only retrieval.
Do not edit sealed reports, historical paths inside reports, or closed schemas.
Relocation records are a separate versioned format, not framework authority.

## Relocation behavior

- Restrict sources to selected non-Git collections directly under primary/worktrees
  and destinations to primary/artifacts/evidence. Exclude registered checkouts,
  Git metadata, operational configuration and unrelated paths.
- Require explicit selection of the exact plan and SHA256. Before each move,
  recheck paths, ownership/dependencies, known active use, same volume, collisions,
  reparse points, source identity and any holds. Stop affected operations on gaps.
- Capture the complete relative-path, byte-count and SHA256 manifest before moving;
  move one collection without overwriting; verify every file afterward. Keep
  receipts outside the moved collection. Preserve directory layout and attributes.
- On failure/interruption, retain observations and inspect both paths on resume.
  Never replay blindly, replace existing destinations or claim an automatic rollback.
- Until the policy PR reaches primary/main, a new directory-local ignore marker
  protects artifacts. Check its actual Git ignore behavior before storing payloads.
  Do not edit the primary checkout's tracked ignore file to bypass PR delivery.

## Verification and completion

Documentation-only checkpoints verify facts, links, identity and consistency.
Do not invent runtime tests or coverage for them.

Tool behavior follows red -> green -> refactor -> developer QA. Test successful
binary/Unicode/hidden/read-only relocation, collision and path escape, reparse and
worktree exclusion, stale source/plan, permission/locked-file failures, interrupted
and repeated operations, mismatches, ignored storage and unrelated preservation.
Declare all first-party executable utility files as the coverage denominator;
exclude only tests/fixtures/vendor tooling. Executed-line coverage and required-case
pass rate must each be >=95%, with no failed mandatory case. Report raw counts,
platform, commands, versions, exit codes, retained failures and limitations.

Live relocation requires complete before/after hashes and updated catalog readback.
Every original collection must end relocated-and-verified, retained-with-hold, or
blocked-with-reason. Report logical sizes separately from disk allocation/free space.

No cache deletion, worktree removal, Git history rewrite, native Codex execution,
historical diagnostic rerun, installation, remote archive provisioning or framework
acceptance is selected. No universal retention timer is introduced. Cleanup remains
a separate reviewed action after dependency and ownership checks.
