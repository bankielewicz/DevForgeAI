# Operator-selected evidence relocation

This one-shot Windows PowerShell 7.2+ utility implements the selected
[relocation contract](../plan/artifact-relocation/plan.md). It is not a protected
framework validator, cleanup service or acceptance authority. Read the
[retention procedure](artifact-retention.md) first.

The script is `scripts/artifact-relocation/Move-EvidenceCollection.ps1` in its task
checkout. Explicitly select the **primary** project root; task worktrees are authoring
locations, not interchangeable data roots. Git and readable Windows process metadata
are required. Do not change permissions, policy or operational configuration merely
to force a blocked collection through admission.

## Inputs and modes

- `Inventory`: `-ProjectRoot`, `-Collection`; returns a complete sorted file/directory
  manifest, including SHA256, bytes and attributes. Refuses reparse points.
- `Preview`: the same inputs plus `-OutputDirectory` and `-AdmissionPath`; writes a
  unique plan outside the collection and returns its path and SHA256. It does not move
  payloads or initialize the artifact destination.
- `Relocate`: `-PlanPath`, `-ExpectedPlanSha256`, `-Approve`; checks the selected plan,
  original admission and current source/process/path conditions before one same-volume
  directory move. Returns a receipt only after complete destination verification.
- `Verify`: plan path and expected SHA256; checks the destination independently of
  receipt existence. Source must be absent. It never replays a move.

Admission is a separately reviewed JSON document with `Version: 1`, the exact `Root`
and `Collection`, `Owner`, UTC `ReviewedUtc`, a nonempty `DependencyReview`, and `Holds`.
Any hold, missing decision, mismatched identity or review older than 24 hours blocks
execution. This freshness window is for the immediate maintenance operation, not a
retention or deletion timer. Select a new reviewed input after investigating drift;
do not edit an already-bound record to manufacture success.

Example, using already prepared and reviewed inputs:

```powershell
$tool = 'C:\Projects\DevForgeAI\worktrees\git\artifact-relocation-tool\scripts\artifact-relocation\Move-EvidenceCollection.ps1'
$preview = & $tool -Mode Preview -ProjectRoot 'C:\Projects\DevForgeAI' `
    -Collection 'framework-foundation' `
    -AdmissionPath 'C:\Projects\DevForgeAI\tmp\selected-admission.json' `
    -OutputDirectory 'C:\Projects\DevForgeAI\tmp\selected-relocation'

# Inspect the exact generated plan before selecting the effect.
Get-Content -LiteralPath $preview.PlanPath
& $tool -Mode Relocate -PlanPath $preview.PlanPath `
    -ExpectedPlanSha256 $preview.SHA256 -Approve
& $tool -Mode Verify -PlanPath $preview.PlanPath `
    -ExpectedPlanSha256 $preview.SHA256
```

The example admission file is not supplied or implicitly approved. The selected
checkpoint supplies actual admissions and unique local output paths.

## Safety, failure and recovery

Only literal collection names directly beneath primary/worktrees are admitted;
`git` is reserved. Destinations are primary/artifacts/evidence with the same name.
Registered worktrees inside a collection, protected receipt directories, cross-root
plans, path escapes, collisions and reparse points are refused. Full per-file
manifests, including empty directory layout and attributes, are compared before and
after movement. Each inventory pass has a 15-minute deadline. A collection exceeding
it is blocked, not partially qualified.

Process inspection checks visible command lines for current, destination and
original collection paths. It is not a complete open-handle/cwd detector. The
operator must stop other writers and review dependencies; exact byte checks detect
drift but cannot prevent every concurrent external write. Hashing refuses a file
already opened incompatibly by a writer. No workers are launched or terminated.

Storage initialization creates the selected local artifact root and a new `.gitignore`
marker only when missing. Existing marker contents are not overwritten; Git must
confirm that destination payloads are ignored before movement.

A selected plan gets an exclusive, retained `.attempt.lock` before mutation. An
existing attempt is not automatically repeated. On post-move failure, source may
already be absent and destination present: inspect the retained BLOCKED receipt and
both locations, then use Verify to establish actual state. Never infer rollback.
If receipt writing itself fails, the missing receipt is an explicit incomplete
observation; the plan and filesystem must be inspected independently.

Keep plans, admissions, receipts and their digests outside payload directories.
Never delete them as a side effect of this utility. Checkpoints identify their
precise local evidence roots; remote reviewers receive small summaries with explicit
local-only limitations. No cache deletion, history rewrite or remote upload occurs.

## Verification

The native Pester suite is `tests/artifact-relocation/Relocation.Tests.ps1`. Run
Pester 5.7.1 with coverage over the entire production `.ps1`; tests/fixtures are
excluded, no executable production lines are excluded. Record JaCoCo line counters
separately from command coverage; this collector does not measure branch coverage.
The checkpoint-3 report records actual runs, source digests and known limitations.
