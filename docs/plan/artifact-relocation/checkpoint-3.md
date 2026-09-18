# Checkpoint 3: tested relocation utility and preview

Candidate: `feat/artifact-relocation-tool`; primary data root:
`C:\Projects\DevForgeAI`. Authoring root:
`C:\Projects\DevForgeAI\worktrees\git\artifact-relocation-tool`.
The selected contract is [plan.md](plan.md); the
[operator guide](../../workflows/evidence-relocation-tool.md) describes the interface.

## Results

- Native Windows / PowerShell 7.6.6, Pester 5.7.1: **37/37 required cases passed
  (100%)**, none skipped, blocked or unexecuted in the final campaign.
- Executed-line coverage: **148/148 (100%)**; command coverage:
  **293/300 (97.666667%)**. Denominator: the complete production
  `scripts/artifact-relocation/Move-EvidenceCollection.ps1`; no executable source
  exclusions. Only tests/fixtures/tooling are excluded. Branch coverage is
  NOT_MEASURED. A covered line does not prove every conditional on it executed.
- PSScriptAnalyzer 1.25.0: zero errors, two reviewed warnings (plural helper name
  and explicit operator confirmation instead of ShouldProcess), one informational
  positional-call finding. No warnings were silently suppressed.
- All **34** eligible collections previewed and their plans read back by SHA256:
  **30,359 files / 346,517,223 logical bytes**. Complete manifests include empty
  directories and attributes in addition to files. No payload moved.
- **30** collections retained on hold: reparse points, literal runtime/configuration
  dependencies, the unresolved native-diagnostic chain, or advisor-run lease review.
  See [admission-review.json](admission-review.json). Owner/review-date gaps remain
  explicit; no hold expires automatically.

## TDD and retained attempts

Raw records are local-only in `tmp/relocation-tool-001` under this authoring root.
The checkpoint manifest supplies exact filenames, byte counts and SHA256 values.
Access for a remote reviewer must be arranged with Bryan; digests are not a substitute
for those bytes. Source/tests and this compact summary are published, not raw trees.

1. `red.xml`: focused missing relocation behavior, 0/1 passed, exit 1. A runnable
   helper deliberately reported unimplemented behavior; this was not setup failure.
2. `green-focused.xml`: UTC admission parsing defect, 0/1, exit 1. Corrected conversion
   of JSON-deserialized DateTime values without losing their time-zone identity.
3. `green-focused-002.xml`: focused actual fixture move, 1/1, exit 0.
4. `regression-001.xml`: 35/35, exit 0, coverage retained as coverage-001.xml.
5. `receipt-boundary-red.xml`: 0/2 selected regression cases, exit 1; 35 other cases
   intentionally outside that focused run. An externally placed plan could write
   receipts in Git metadata or outside the selected project.
6. Extracted shared receipt-location checking for both preview and plan consumption;
   `regression-002.xml`: 37/37, exit 0, coverage-002.xml. Original failures remain.
7. Live preview completed all 34 plans. Its enclosing display command then exited 1
   on a strict-mode XML-property formatting error, after saving preview-results.json.
   A fresh readback verified all 34 plan hashes and parsed coverage using XPath.
   No payload was moved or operation blindly repeated because of that display error.

Final Pester invocation used New-PesterConfiguration with Run.Path set to the
relocation test file, Run.PassThru true, TestResult enabled at regression-002.xml,
CodeCoverage enabled for the whole production script, JaCoCo output at coverage-002.xml,
and CoveragePercentTarget 95. Invoke-Pester returned Passed; a non-Passed result
exits 1. Native Pester needed normal host access to its disposable registry, fixture
repositories and Windows process metadata. No tools were installed.

## Requirement traceability

| Contract obligation | Implementation / observation |
| --- | --- |
| Explicit primary root, scope and worktree exclusion | Get-RelocationPaths; actual nested-worktree refusal fixtures. |
| Identity, ownership, holds and freshness | Bound plan SHA256, Read-RelocationAdmission, source manifest and pre-move rechecks. |
| No overwrite, reparse traversal or protected receipt writes | Literal collection admission, destination refusal, Assert-PlainRelocationPath, shared receipt-location checks. |
| Complete preservation | Get-RelocationTree includes byte hashes, attributes and directory layout; binary/Unicode/hidden/read-only/empty-directory cases. |
| Drift, failure and interruption | Stale inputs, incompatible file locks, missing process visibility, final-recheck consumer appearance, blocked receipts, independent Verify, retained attempt locks. |
| Operator terminal interface | Inventory/Preview/Relocate/Verify exercised through the public script; ignored destination checked by Git. |
| Evidence/authority separation | New standalone plan/receipt format only; no protected acceptance, historic schema edits, cleanup or installed runtime changes. |
| Actual output placement | Source, tests, local evidence and all preview plans read back at their declared locations. |

Process checks inspect visible command lines; they are not a complete open-handle or
cwd detector. Stop other writers before live mutation. Post-move drift produces a
blocked observation and retained bytes, never a fabricated rollback. Cross-platform
qualification is NOT_RUN; this tool targets native Windows. Independent QA is NOT_RUN;
framework acceptance is NOT_EVALUATED.

## Next checkpoint

Use the unchanged tested utility in a new pilot worktree, generate fresh admissions
and plans there, compare their tree identities to [preview-summary.json](preview-summary.json),
and relocate only foundation/MVP planning after live rechecks. Existing checkpoint-3
inputs and raw evidence remain unchanged. Any mismatch blocks that collection.
