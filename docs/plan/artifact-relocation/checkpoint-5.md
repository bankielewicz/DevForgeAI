# Checkpoint 5: relocation outcome and review handoff

The selected [five-checkpoint plan](plan.md) is complete within its explicit hold
boundaries. All 64 original collections are accounted for. The final batch moved
32 collections; the earlier pilot moved two. No collection or cache was deleted.

| Disposition | Collections | Regular files | Logical bytes |
| --- | ---: | ---: | ---: |
| Relocated and verified | 34 | 30,359 | 346,517,223 |
| Retained with named holds | 30 | 452,097 | 39,727,172,615 |
| Total inventoried | 64 | 482,456 | 40,073,689,838 |

Moved evidence is under `C:\Projects\DevForgeAI\artifacts\evidence\`.
Held collections remain under `C:\Projects\DevForgeAI\worktrees\`.
Registered working checkouts remain under `worktrees/git/`; the parent directory
was not renamed. Held counts are the original no-follow inventory observations,
not a fresh full-tree qualification. Their source presence and destination absence
were checked at handoff. The 37 reparse points were not followed or relocated.

## Verification

The rollout used the unchanged checkpoint-3 utility and tests. Their source
bindings, together with all other checkpoint-3 source bindings, were checked before
execution and finalization. Native Windows PowerShell 7.6.6 ran each collection's
fresh admission and `New-RelocationPlan`, compared its complete tree digest to
the earlier preview, then ran `Invoke-EvidenceRelocation -Approve` and an additional
`Test-EvidenceRelocation` readback. Both enclosing live commands exited 0.

All 34 complete manifests matched before and after movement: relative paths,
file SHA256/length, directory layout including empty directories, and attributes.
Each final plan and success receipt was read back and bound by SHA256 in
[checkpoint-5-results.json](checkpoint-5-results.json). No blocked live move or
unaccounted collection remains. Preserved source/destination state was checked
again during final accounting; no uncertain operation was replayed.

All **76 retrieval targets** match their recorded SHA256 and lengths. Nine catalog
locators changed in this checkpoint, in addition to the two pilot locators.
The [catalog](retrieval-catalog.md) preserves original paths, stable IDs and
historical Git URLs. Its 56 published historical targets and 20 local-only targets
retain their availability distinction. Historical sealed reports were not edited.

Primary HEAD remains `164b652572cbb349e2c44eb3270f4d653bac05e5` on `main`, with a
clean Git status. Its three protected root files (`AGENTS.md`, `.gitignore`,
`.gitattributes`) match their before hashes. No root-level PowerShell helper exists
in that primary checkout; the existing operator-console worktree remains at
`bf4c3324285e0202a72d37bd9cc54e3de7a627a7` with clean status. The existing
docs-worktree-pr-delivery worktree also remains clean at its recorded commit.
Registered paths and branches were unchanged during the live batch.

The primary artifact root's local ignore marker keeps raw payloads ignored until
the policy PR is merged. No operational skills, configuration, installed components,
native diagnostic or framework authority implementation was changed by this task.

The unchanged tool's developer checks remain those in
[checkpoint-3.md](checkpoint-3.md): **37/37 required cases (100%)**, executed-line
coverage **148/148 (100%)**, command coverage **293/300 (97.666667%)**, no executable
source exclusions. PSScriptAnalyzer reported zero errors and two reviewed warnings.
Branch coverage is NOT_MEASURED. Those tests were not rerun merely for these record
changes; live relocation supplies additional observations. Independent QA is
**NOT_RUN** and framework acceptance is **NOT_EVALUATED**.

## Holds and cleanup candidates

The [final results](checkpoint-5-results.json) enumerate every collection, including
each held collection's reasons, owner and explicit unset next-review date. Holds
cover reparse-dependent trees, literal runtime/configuration consumers, unresolved
native-diagnostic evidence, and advisor-run lease/consumer review. Bryan is the
migration reviewer; original producer ownership is not inferred. No hold expires
automatically. Releasing one requires inspection of that collection and a new
current admission, not reuse of today's expiring operation inputs.

The original inventory found **24,203,450,051 logical bytes** beneath names associated
with build/cache material. This is a discovery list, not proven reclaimable space.
Per-collection candidate sizes remain in [inventory.json](inventory.json); none is
approved for disposal. A later selected cleanup must identify exact subpaths,
bound executables and reproduction dependencies, active writers, retention/holds,
and required retrievable archives before proposing deletion. No disk savings are
claimed: this operation moved about 330 MiB on the same disk, and about 37 GiB remains
held. Physical allocation and reclaimed space were not measured.

## Publication and evidence access

Each checkpoint has its own actual Git worktree, branch and stacked draft PR.
Review and merge in dependency order; this task does not merge them:

| Checkpoint | Branch | Parent / published review |
| --- | --- | --- |
| 1: inventory | `docs/artifact-inventory` | `main`; [PR 4](https://github.com/bankielewicz/DevForgeAI/pull/4) |
| 2: policy and retrieval | `docs/artifact-policy` | checkpoint 1; [PR 5](https://github.com/bankielewicz/DevForgeAI/pull/5) |
| 3: tested utility | `feat/artifact-relocation-tool` | checkpoint 2; [PR 6](https://github.com/bankielewicz/DevForgeAI/pull/6) |
| 4: pilot | `chore/artifact-relocation-pilot` | checkpoint 3; [PR 7](https://github.com/bankielewicz/DevForgeAI/pull/7) |
| 5: rollout | `chore/artifact-relocation-rollout` | checkpoint 4; this branch's draft PR |

Checkpoint commits 1-4 are respectively
`16bfaefc2b8c3567d5b053c576581acb83e38860`,
`d54b2d6f9aee78a97bf5d8f3aee2f954102d23a6`,
`4684a6486b8c226e38fc27b1ec696cee0a6f30d0`, and
`a321db391b97eb28e6169eb6cef3cd9fbd9fce82`.
The checkpoint-5 manifest binds this report, results, catalog and local finalization
evidence; Git supplies the final candidate commit identity without a self-hash cycle.
Current primary-main navigation gains the repairs only after the PRs are integrated.
After each merge, verify the next PR's base and diff before merging it.

Raw evidence remains local, deliberately absent from the PR payloads:

- Tool tests, coverage and original previews: `worktrees/git/artifact-relocation-tool/tmp/relocation-tool-001/`.
- Pilot plans, admissions and receipts: `worktrees/git/artifact-relocation-pilot/tmp/relocation-pilot-001/`.
- Final batch plans, admissions, progress and receipts: `worktrees/git/artifact-relocation-rollout/tmp/relocation-rollout-001/`.
- Final accounting command: from the rollout worktree, `& .\tmp\finalize-checkpoint-5.ps1` (exit 0). It reads evidence and updates task records; it performs no collection move.

Bryan can access these locations on this machine. Remote independent retest needs
access arranged with Bryan; raw evidence has not been uploaded or remotely backed
up by this task. No retention expiry is selected. Preserve these task worktrees and
raw inputs until their evidence dependencies have been addressed by a separately
selected retention/relocation action. Published compact manifests are not a backup
of the underlying files.

The next owner is Bryan for PR review and hold/retention decisions. A future cleanup
or remaining-collection migration is separate work; it should start from these
recorded dispositions and recheck current state rather than repeat completed moves.
