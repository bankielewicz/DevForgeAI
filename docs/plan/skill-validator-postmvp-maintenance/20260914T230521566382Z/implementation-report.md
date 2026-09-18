# Skill-validator enhancement: delivered; native delivery qualification incomplete

Development changes are implemented in `src/agents/skills/skill-validator`. Final deterministic Windows verification passed **402/402 required unittest cases (100%)**, with **3626/3802 executable lines covered (95.37085744345082%)**. Branch coverage is **1724/1908 (90.35639412997904%)**, reported separately. The 95% line and deterministic-case floors pass. Final-source native delivery qualified **1/2 trials (50%)**, below the native required-case floor; the adverse report/handoff obligation remains unperformed after timeout. Full qualification is **INCOMPLETE**. These results do not establish full skill or protected framework acceptance.

## Delivered behavior

- One shared metadata parser now validates required fields, optional field types and limits, string metadata mappings, duplicate keys and malformed YAML keys. Both format consumers use the same checks; existing record families remain compatible.
- A digest-bound catalog maps all eight supplied Agent Skills documents to mandatory format, host-specific behavior, advisory measurements, semantic evaluation and host-only integration guidance. Optional folders, recommended size and host tolerance are not universal failure rules.
- Supplemental resource observations report entrypoint size, traversal depths and cycles as advisories. A confirmed false positive for inline-code Markdown links was repaired. Unicode remains intact; both new CLIs emit portable JSON on legacy Windows pipe encodings.
- The reusable trial runner seals plans before execution, checks exact inputs, preserves every attempt, grades delivered content and rejects incomplete or altered evidence. Native sessions default to 600 seconds; utilities to 120 seconds, with explicit positive finite overrides. Windows Job Objects own worker/descendant lifetime and report cleanup. Dependencies, unrelated ready cases, partial output, interruptions and zero-exit/missing-delivery cases have executable tests.
- Workflow references and the report template now lead with actual completion, separate mechanical from semantic qualification, require held-out expectations and explain optional matched baseline comparisons. Python evidence never replaces compiled-Rust authority.

The selected implementation contract is [skill-validator-postmvp-spec.md](../../../specs/skill-validator-postmvp-spec.md). [The delivered snapshot](delivery-003/source/) and [change inventory](delivery-003/checks.json) bind the final source. Nineteen package files changed or were added; none were removed. The new specification is outside the package. Operational skill copies were not installed or edited.

## Verification

| Check | Observed result | Evidence |
|---|---|---|
| Full Windows regression | PASS: 402/402, 112.070 seconds, exit 0 | [JSONL](regression-005/results.jsonl), [frozen expectations](regression-005/expected-results.json), [grader](regression-005-grading.json), [log](regression-005.log) |
| Full first-party executed-line coverage | PASS: 3626/3802 = 95.37085744345082% | [Measurement](coverage-final-003/measurement.json), [line/branch detail](coverage-final-003/coverage.json) |
| Changed/new script-module line coverage | 1297/1337 = 97.00822737471952% | Same coverage report; denominator is every line in the seven changed/new script modules |
| Branch coverage | 1724/1908 = 90.35639412997904%; no substitution for line coverage | Same coverage report |
| Creator compatibility checker | PASS, exit 0 | [Raw output](creator-check-delivery-003.txt) |
| Structural/resource checks | OBSERVED, exit 0 | [Raw observations](structure-delivery-003.json) |
| Python syntax / catalog / source manifest | PASS: 14 scripts, eight document digests, exact artifact inventory | [Delivery checks](delivery-003/checks.json) |
| Protected-file readback | PASS: all 96 originally captured files unchanged | [Original identities](preservation.json), [readback](delivery-003/checks.json) |
| Real process exceeding old 120-second ceiling | PASS: 121.188 seconds, configured 600 seconds, cleanup VERIFIED | [Receipt](long-budget/runner-output.json) |
| Independent adaptive/resource tests | PASS: 28 adaptive and 40 resource cases, included in full 402 denominator | [Adaptive review](adaptive-quality/RESULT.md), [resource review](resource-quality/REPORT.md), [resource supplement](resource-quality/SUPPLEMENT-004.md) |
| Final-source cold native workflow/report delivery | INCOMPLETE: 1/2 complete delivered workflows (50%); adverse trial timed out | [Final independent adjudication](independent/forward-002/adjudication.md) |
| Earlier cold trials | INCOMPLETE: 0/2 delivery; inherited read-only actor settings | [Retained earlier adjudication](independent/forward-001/adjudication.md) |
| Linux native / implicit discovery / optional comparisons | NOT_RUN | Not qualified by Windows helper or explicit-activation results |
| Installation / protected framework acceptance | NOT_PERFORMED / NOT_EVALUATED | Outside selected source maintenance scope |

Coverage includes all first-party Python under `scripts/`, including legacy custody and evaluation code. Fixtures/tests are excluded from the executable-source denominator, not from the required-case suite. Subprocess fixture copies count only when their captured source digest equals the final declared source. Missing or mismatched execution identities earn no credit. The text coverage table combines lines and branches; its rounded total is not the executed-line percentage above. Several individual modules remain below 95%; the declared whole-source floor passes without changing its denominator.

## Independent findings and retained attempts

Independent adversarial probes found unsupported receipt mutations, omitted dependency inventory, incomplete side-effect accounting, empty native output obligations, reused preexisting output and Boolean/numeric JSON confusion. Each confirmed behavior has retained counterexamples and repaired regression coverage. The separate resource reviewer found RQ-01, the inline-code link false positive; its original test passed unchanged after repair. Final regression also exposed a Unicode console failure in the trial CLI; a corresponding advisory-CLI failure was then reproduced and repaired. Both have retained red/green logs.

Earlier suite and fixture failures remain in this directory. Initial test setup failures and stale-manifest failures are not valid behavioral red results. The advisory organization helper lacks a retained pre-implementation red run; later tests do not retroactively supply one. [The evidence guide](README.md) identifies these limitations and the final qualifying attempts.

## Native delivery results and remaining gap

Both first cold actors completed before the selected 600-second ceilings: **141.797 seconds** and **146.937 seconds**. Cleanup was VERIFIED, and all bound inputs stayed unchanged. Initial attempt-001 launches had failed before actor startup with Windows access-denied errors. The separately approved attempt-002 continuations retained the same budgets and did not erase those failures.

The actors inherited a **read-only Codex sandbox**, so they correctly refused report writes. Their zero exits did not pass the delivery oracle: required `review.md`, normal report, record bundle and applicable revision proposal remained absent. The outer runner's write permission was not proof of the inner actor's effective write capability. This is a harness prerequisite gap, not a confirmed validator refusal to perform authorized writable work.

The nominal positive fixture also contained an independently discovered input/output-alias preservation defect. It cannot be counted as a clean positive control. The adverse fixture's seeded wrong-total defect was detected. The actors clearly labeled their substituted-I/O probes; those do not qualify real-file/native execution. Their behavior applies to the captured evaluator snapshot, which predates the final source fixes; differences are retained with that trial.

The user explicitly authorized two fresh final-source trials under `independent/forward-002`, with corrected alias handling, independently frozen oracles, new disposable roots and explicitly selected supported `--sandbox workspace-write`. A delegated host-approval request was canceled before either process started; the root then obtained direct host approvals and launched the same guarded, previously unstarted attempt directories. This did not replay an executed attempt.

**Ledger-c qualified the bounded validator-delivery oracle.** It completed in **582.328 seconds**, without timeout, with exit 0, VERIFIED cleanup and unchanged bound inputs. It delivered the review summary, normal validation report, evidence/check records and handoff. Independent readback checked 26 report links, 24/24 real-file helper checks and record integrity. The target skill's own assessment correctly remained INCOMPLETE for unperformed nested native/discovery cases. Passing the validator's delivery trial does not promote those target checks to PASS.

**Ledger-d did not qualify delivery.** It reached its **600-second limit** (602.891 seconds including cleanup), with timeout recorded, owned worker exit 124, VERIFIED cleanup, unchanged inputs and runner outcome NOT_RUN. Nineteen real-file helper checks completed: 15 passed and four reproduced the seeded wrong-total defect. Three description-routing observations were separate from implicit activation. The required final validation report, review summary and revision handoff were absent. These intermediate findings cannot substitute for delivery. Timeout alone does not confirm a validator source defect.

The two final-source trials are a distinct, user-selected campaign; the earlier snapshot trials and their failed delivery remain unchanged. Native outcomes are not pooled with the 402 unit cases to conceal the 50% native completion rate. No additional retry or budget increase was performed. The remaining qualification work is the adverse report/revision-delivery path; it needs a separately selected follow-up with explicit delivery milestones and budget. This campaign cannot claim that a longer default by itself eliminates unfinished native evaluations.

The QA skill's historical 42-scenario campaign was not replayed. This maintenance does not convert that campaign's incomplete result into PASS or a confirmed QA source defect.

## Commands and runtime

Root verification commands ran from `C:\Projects\DevForgeAI` using native Windows Python 3.10.11; cold actors used their separately recorded disposable working directories. No WSL or cross-filesystem execution was used. The final campaign command was `python -B -X utf8 docs/plan/skill-validator-postmvp-maintenance/20260914T230521566382Z/campaign.py regression-005` with the per-process coverage settings documented in [README.md](README.md). Runtime, exact source identities and arguments are in [runtime.json](regression-005/runtime.json); the retained exit is [0](regression-005.exit.txt).

`measure.py combine coverage-final-003` and `grade_campaign.py` both exited 0. `check_delivery.py delivery-003`, the creator's installed `quick_validate.py`, and `observe.py structure --source src/agents/skills/skill-validator` also exited 0. The bundle includes the Python JSONL runner, deterministic grader, schemas, expected results, fixture sources, source snapshots, exact document inputs and coverage data. All of it remains supporting evidence, with no mutation or framework acceptance authority.
