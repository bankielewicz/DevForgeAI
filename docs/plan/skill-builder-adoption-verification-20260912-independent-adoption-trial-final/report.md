# Independent adoption task trial — final

Status: PASSED for the bounded development trial. All final-chain deterministic
observations bind builder manifest `60522daaff9000367beacb7b5a6fb03cd90caeb93ac829bc13bba98c2d3b31a9`. This is actual execution against
a new disposable TEMP development project, not fabricated successful evidence.

Project: `C:\Users\bryan\AppData\Local\Temp\skill-builder-adoption-trial-dana9h_x`

Development target: `C:\Users\bryan\AppData\Local\Temp\skill-builder-adoption-trial-dana9h_x\src\agents\skills\receipt-totals`

## Results and receipts

| Stage | Actual result | Retained evidence |
| --- | --- | --- |
| Original script | Executed; numeric 0.30000000000000004 demonstrated the known defect | commands/origin-known-defect.json |
| Adoption | Helper exit 0; adoption-v1 one PASS; unchanged target/spec | retained/adopt-01-published/ |
| Adoption publication | External pointer written then read back; no prior pointer | retained/adopt-01-published/publication-readback.json |
| First candidate | Structural PASS; 15 behavior cases PASS; spec-v1 two PASS | retained/revision-01-conflict/ |
| Injected user edit | Script comment appended after adoption publication | user-edit-observation.json |
| Conflict | Helper exit 1, CONFLICT; applied_paths empty; live destination equals C | retained/revision-01-conflict/post-plan-live-manifest.json |
| Distinct resolution | Edited script retained; only script restored to exact adopted bytes; origin unchanged | resolution-edit-readback.json and prompts/04-conflict-resolution.txt |
| Resolved first revision | Fresh candidate/delivered checks; 15 delivered cases PASS; delivered and published revision-spec-v2 each three PASS | retained/revision-02-resolved-successful/ |
| Later revision | Selected last successful generated N; adds exact total_quantity; 16 fresh candidate and delivered cases PASS; delivered and published revision-spec-v2 each three PASS | retained/later-revision-03-successful/ |
| Original input locators | All six selected original-input and captured-input digest/size comparisons PASS | original-input-locator-audit.json |
| User notes and origin spec | Byte-identical after the complete chain | final-target-manifest.json |

Eight evaluator result files contain 19 PASS records; [evaluation-index.json](evaluation-index.json)
records exact paths, profiles, hashes and counts. The helper's expected conflict
exit 1 is retained independently from these successful evaluations. Candidate
spec-v1 checks are candidate observations; delivered/published revision-spec-v2
checks are separately executed on real after snapshots. Publication pointers are
outside the target; their original absolute paths and readback hashes are retained.

## Authorization and custody

The trial controller authorized a new disposable chain with the same raw receipt
task and separate adoption, first-revision, conflict-resolution and later-revision
instructions. Raw directions are in prompts/. Original managed scope is exactly
SKILL.md and scripts/receipt_totals.py. notes.txt is retained_user throughout.
Adoption historical_origin remains unknown. The first generated origin comes from
the adopted managed snapshot; the later revision selects the successful first N,
not current files or the conflict attempt. [origin-chain.json](origin-chain.json)
retains all three pointer objects, while raw published pointers and readback
receipts remain in each retained run directory.

The adoption origin digest is `44f43530ca0892328a54353c3eed07758f5c2626f09c87b208530970eb4f1083`.
The first generated origin digest is `a73ea957abc875ed7b073dac228221d5fcb098d64e35afc542580325bd69eb40`.
The later generated origin digest is `8caea788b6079e253a001d3929afb29675088233bd3aa654ce6f5d33d4bcdfcc`.

## Verification scope and limitations

The worker read current SKILL.md, references, schemas and the documented legacy
package_links case interface. It did not read builder implementation, implementation
tests or other agents' conclusions. No builder source was edited. The independent
trial used one worker and real subprocesses; raw commands, streams, scripts,
inputs, snapshots, conflicts, resolution edits and pointer receipts are retained.
The controller's explicit fresh-chain instruction authorized reuse of the reviewed
behavior proposals in the new project; it did not erase the earlier attempt.

The checks cover exact decimal aggregation and wide values, single grand-total
rounding/half-up ties, fractional quantities, empty and quoted receipts, exact
successful JSON schema, invalid header/cell counts, blank items, invalid text,
negative/nonfinite inputs, and receipt preservation. The later checks also inspect
the exact total_quantity schema and values, including zero for an empty receipt.

No source defect was observed in these exercised builder interfaces. One cosmetic
helper reason says 'previous generated baseline' for an adopted row; the typed
ownership and origin fields correctly identify adoption. Python observations and
ordinary pointer files confer no protected authority. Rust implementation and
qualification: NOT_PERFORMED. Native implicit routing: NOT_PERFORMED. Operational
installation: NOT_PERFORMED. Publication-failure and partial-write recovery were
not injected in this final chain. No stronger reliability claim is made.

## Earlier retained chain

The adjacent directory without the -final suffix preserves the first chain. It
contains a rejected unsorted manifest attempt, a correctly recaptured adoption,
successful conflict/resolution/later execution, and a self-authored authorization
resolved_path metadata defect in the first revision. That defect was disclosed;
the raw bounded instruction bytes were correct but the informational original
locator pointed at the first instruction rather than the combined instruction.
Its old-manifest provenance also predictably failed an optional current-manifest
re-evaluation with 'builder manifest digest differs from running evaluator'. Those
results are preserved, not relabeled. The controller requested this fresh chain
to obtain current-manifest observations with exact original locators. This report
uses the new final chain as its completed trial evidence.

## Complete emitted-input readback audit

[measured-input-readback-audit.json](measured-input-readback-audit.json) verifies
all 530 candidate_digests entries and all 19 cases_sha256 values emitted in the
eight result files against retained bytes. All checks passed; no measured bytes
were unavailable. Four recorded measurements (two graders in each of two delivered
evaluations) explicitly map revision-plan.json to the retained sibling
revision-plan-before-publication.json whose exact SHA-256 matches the emitted
digest. This is two distinct retained byte copies; no record or input was rewritten.

The audit lists every current retained-root file outside each result file's measured
input union. The known later publication pointer/plan-copy additions are identified
from the executed driver sequence; other unmeasured files receive no chronology
claim. Thus digest readback covers the exact emitted measurements, not every byte
later present in a reused root. The prior report bytes remain in
report-before-measured-input-audit.md. A subsequent source wording-only manifest
change is being tested in a separate new -final2 chain; this report retains its
actual 60522daa manifest identity.
