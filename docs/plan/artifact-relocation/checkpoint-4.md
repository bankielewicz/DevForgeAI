# Checkpoint 4: verified pilot relocation

The exact tested utility from checkpoint 3 relocated both admitted pilot collections
on the same volume. Its published source/test bindings were verified before use.
Fresh admissions and full plans were written in this worktree; checkpoint-3 inputs
and receipts were not changed.

| Collection | Files | Logical bytes | Result |
| --- | ---: | ---: | --- |
| framework-foundation | 6 | 23,083 | VERIFIED |
| framework-mvp-planning | 20 | 135,096 | VERIFIED |

Before moving, both fresh complete manifests matched checkpoint-3 preview tree
digests. After movement, every file's SHA256/length and directory/file attributes
matched; independent Verify readback also passed. Total: 26 files / 158,179 bytes.
Original worktrees/<collection> paths are absent; destinations exist beneath
C:\Projects\DevForgeAI\artifacts\evidence. Neither collection was deleted or copied
into ordinary Git history. Their internal paths and sealed report bytes are unchanged.

The catalog now resolves both relocated reports at their verified destinations.
Their published historical Git links remain usable. All other catalog locators
remain unchanged for this checkpoint.

The primary artifact root contains a new local .gitignore marker; Git confirms its
payloads are ignored. The primary tracked ignore file, AGENTS, .gitattributes and
all root PowerShell helpers match their before hashes. Primary HEAD remains
164b652572cbb349e2c44eb3270f4d653bac05e5 and its tracked/untracked status is clean.
Existing registered worktrees remain in place. No operational files were modified.

Raw plans, admission inputs, result receipts and primary-before observations are
local-only under tmp/relocation-pilot-001 in this checkpoint worktree. The compact
checkpoint-4-results.json binds the plans, receipt hashes and verified tree digests.
The original raw files are required for a full remote retest; arrange access with
Bryan. These observations do not establish prior framework/native acceptance.
Independent QA is NOT_RUN; framework acceptance remains NOT_EVALUATED.

Execution used native Windows PowerShell 7.6.6 and the unchanged
New-RelocationPlan -> Invoke-EvidenceRelocation -Approve -> Test-EvidenceRelocation
sequence for each named collection, with the actual plan path and SHA256 returned
by Preview. The enclosing pilot command exited 0. No test suite rerun was needed
because production/test bytes remained identical to checkpoint 3; this checkpoint
adds live pilot verification rather than claiming a new unit campaign.
