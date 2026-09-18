# Independent adoption task trial — final

Status: PASSED for the bounded development trial. All final-chain deterministic
observations bind builder manifest `11457297985c7768faaec1846e54e0bcf4538fd8e064fb0d1099f9da6c7e8620`. This is actual execution against
a new disposable TEMP development project, not fabricated successful evidence.

Project: `C:\Users\bryan\AppData\Local\Temp\skill-builder-adoption-trial-my5s7hbx`

Development target: `C:\Users\bryan\AppData\Local\Temp\skill-builder-adoption-trial-my5s7hbx\src\agents\skills\receipt-totals`

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

The adoption origin digest is `814a61bc213f9f8bccda8f4b8abc66fa26d50e72ccb3da15721a571469764e4d`.
The first generated origin digest is `01f8e5b59ac1ced4acbb2fda825de99fb0879bef9fc58edc9cc0778385ab93eb`.
The later generated origin digest is `8a97f9103185418ff706d5b26c64498e0eafd36a7744083d579d441d5c3f2b8a`.

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

No source defect was observed in these exercised builder interfaces. The helper
reason now says 'verified prior baseline' and the typed ownership and origin
fields correctly identify adoption. Python observations and
ordinary pointer files confer no protected authority. Rust implementation and
qualification: NOT_PERFORMED. Native implicit routing: NOT_PERFORMED. Operational
installation: NOT_PERFORMED. Publication-failure and partial-write recovery were
not injected in this final chain. No stronger reliability claim is made.

## Earlier retained chain

The adjacent original independent-adoption-trial directory preserves the first chain. It
contains a rejected unsorted manifest attempt, a correctly recaptured adoption,
successful conflict/resolution/later execution, and a self-authored authorization
resolved_path metadata defect in the first revision. That defect was disclosed;
the raw bounded instruction bytes were correct but the informational original
locator pointed at the first instruction rather than the combined instruction.
Its old-manifest provenance also predictably failed an optional current-manifest
re-evaluation with 'builder manifest digest differs from running evaluator'. Those
results are preserved, not relabeled. The controller requested this fresh chain
to obtain current-manifest observations with exact original locators. This report
uses this new -final2 chain as its completed trial evidence. The intervening -final
chain remains retained with its own 60522daa manifest and completed 530-candidate /
19-case emitted-digest audit. No earlier evidence has been rewritten for this run.

## Complete direct emitted-input readback

[measured-input-readback-audit.json](measured-input-readback-audit.json) verifies
every emitted measurement: 530 candidate_digests entries and 19 cases_sha256
values across eight result files / 19 records. All passed. Eight complete candidate
input trees and eight case files were copied before their corresponding evaluator
calls, with full file-set/hash equality readback before execution. The actual
command receipts identify each original root, preserved snapshot, capture manifest,
case-file path and digest. The audit rechecks all eight full snapshot manifests
and reads every emitted digest directly from those preserved input bytes.

There are zero fallback per-file locator mappings and zero unavailable or mismatched
measurements. Every source-relative measured path retains the same path inside
its explicitly recorded snapshot root. The audit separately records files outside
each measured union, files added after the preserved snapshot, and later replacements
such as pointer-advancement plans. Those later files are not represented as part
of the earlier evaluator's measured input set. Original source roots, published
pointers, replaced-plan byte copies, raw results and preceding reports remain retained.
