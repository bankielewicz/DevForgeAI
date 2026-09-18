# Artifact purpose, retrieval and retention

Read this procedure when creating execution evidence, planning a relocation or
considering cleanup. It applies around the selected workflow; it does not expand
skill scope or grant framework acceptance.

## Four storage classes

| Class | Contents | Treatment |
| --- | --- | --- |
| Project records | Source, tests, specifications, decisions, concise verification summaries | Version in Git. |
| Retained evidence | Required results, failure reproductions, necessary candidate/input snapshots | Store outside ordinary Git history with identity, ownership and retrieval metadata. |
| Working checkouts | Registered Git worktrees and unpublished work | Preserve while needed; remove only after publication, ownership and dependency checks. |
| Rebuildable material | Compiler outputs, downloaded dependencies, disposable fixtures and indexes | Review preferentially for reclamation once no active work depends on them. |

A directory can contain several classes. A `target` directory may contain a bound
executable; its name does not make it disposable. An old checkout may contain the
only unpublished source. An ignored directory is neither a backup nor shared storage.

For this migration, keep registered checkouts under `worktrees/git/` and retained
collections under `artifacts/evidence/` in the primary checkout. Keep their internal
layout intact, even when a retained collection contains build outputs. Do not split
or delete those outputs merely to make the class names match the directory tree.
The primary artifact root is explicitly selected; it is not inferred from whichever
task worktree runs a tool. Raw evidence remains local-only unless a record identifies
a verified shared location. Detailed manifests stay local; small summaries and their
digests are tracked. Do not publish credentials or unnecessary private data.

## Identity and availability

Record an artifact's stable identifier, digest, size, project/run ownership,
producing candidate and current locator. Keep identity separate from location.
Retain a versioned relocation record when a locator changes. Preserve sealed
reports and the historical paths inside them rather than editing them to simulate
an unchanged run. Do not add fields to an existing closed record schema.

When exact bytes exist in published Git history, a verified immutable commit link
provides a portable locator without recommitting another copy. Git commits do not
capture dirty files, ignored inputs, external prerequisites or missing execution
results. A rerun is a new observation, not reconstruction of the old result.

Every handoff states who can retrieve the required evidence and for how long.
Local-only evidence has a remote-review limitation. A hash verifies a retrieved
artifact; it cannot reconstruct missing bytes. Missing, expired or inaccessible
required evidence blocks the dependent assessment or claim, not unrelated work.
Historical results keep their original attribution but are not fresh qualification.

## Retention eligibility and holds

Retention is a project-selected policy, not a universal 90-day timer. Project rules
distinguish active investigations, supported releases, expensive reproductions,
sensitive material and disposable outputs. An unset duration is a visible decision
gap; do not invent expiry or automatic deletion.

Elapsed retention makes material eligible for review only. Active investigations,
release dependencies, unpublished work and explicit holds prevent disposal. Each hold
records its reason, owner and next review date or the explicit missing-owner/date
gap. For the current migration, Bryan is the migration reviewer; that does not
invent the original producer's ownership. There is no selected disposal deadline.

Measure storage by class, project and run. Report logical bytes separately from
physical allocation. Reclaim eligible caches first. If required evidence exceeds a
budget, report the conflict; do not omit capture or discard evidence silently.

## Relocation and cleanup

Inventory and preview exact sources/destinations before effects. Recheck ownership,
dependencies, known active processes, worktree registration, untracked/ignored work,
reparse points, collisions and archive accessibility immediately before mutation.
Verify complete before/after identities; do not follow links into other locations.
Use Git operations for registered worktrees. Moving a folder does not register it.

For the selected same-volume migration, move one admitted collection at a time into
a new destination. Preserve partial outcomes and stop on drift; never overwrite a
destination or blindly replay an uncertain move. Receipts live outside the collection.
The [execution contract](../plan/artifact-relocation/plan.md) defines checkpoint
delivery, pilot validation and final accounting.

Until the policy PR is merged, a directory-local `.gitignore` containing `*` inside
the newly created primary artifact root keeps payloads ignored without editing the
primary tracked `.gitignore`. Verify with `git check-ignore` before storing data.
The policy PR also adds `/artifacts/` to the tracked root ignore file.

Cleanup is a separate selected action: preview exact candidates and estimated space,
verify any necessary archive and holds, recheck current state, then perform only the
selected effects and retain a small receipt. This migration does not delete caches,
remove worktrees or rewrite Git history. Deleting a tracked file later does not remove
its earlier Git history; history reduction requires a separate coordinated decision.

## Responsibility

DFF-04 owns selected project policy, DFF-08 owns evidence obligations and DFF-10 owns
retrieval, continuity and retention behavior. A later qualified Rust implementation
may enforce protected decisions. Operator scripts perform selected maintenance and
produce observations; they cannot issue framework acceptance or silently waive holds.
