# VPI-01: bounded implementation proposal

Status: **Implementation proposal only. No additional execution approved or started.** The user has accepted [VPR-2](../validation-policy-v1-20260908/policy-revision.md) at **8ede26450ae737a5e928c5f70a945aa995969b30 as the design specification**. This current acceptance supersedes the frozen proposal's historical “not accepted” label; it does not rewrite those bytes or grant funding, runtime adoption, operational installation or qualification.

The continuation source is [/home/bryan/Projects/DevForge/tmp/skill-validation-policy-r2-review-stage-a-20260908T135135757276Z/review-and-stage-a-report.md](/home/bryan/Projects/DevForge/tmp/skill-validation-policy-r2-review-stage-a-20260908T135135757276Z/review-and-stage-a-report.md), SHA-256 `a11ddd75b4602dbd193c76db429bf291eeff176670352312bae7fe27ca2c9695`. Stage A is **complete**, with its recorded closeout deviation. Any earlier recap that calls it pending is stale and must not drive execution. The source review/report/results/ledgers and terminal exception are frozen inputs in [source-inventory.json](source-inventory.json).

## Preserved decisions and evidence

The independent VPR-2 review passed with no unresolved blockers. Preserve its advisory: uninstrumented human active and waiting time stays NOT_OBSERVABLE; automated event intervals are not person-time. Stage A used exactly two separate initial contexts, and its independent text reviewer marked all five criteria satisfied. A1 capture was 58.009610 UTC / 63.874450166 monotonic seconds; A2 was 73.338876 / 82.130952796 seconds. These intervals include dispatch/detection/capture overhead and do not measure model service time.

At artifact freeze, Stage A elapsed was 383.847663 UTC / 421.967209522 monotonic seconds. Closeout took 223.255054 UTC / 243.785463266 monotonic seconds against a planned 240-second sublimit: **3.785463266 monotonic seconds over**. The final check failed and was not retried. The complete task observations remain valid as bounded text observations; closeout was not fully conformant. The minimal terminal exception record is retained separately. Preserve both clock series; no historical clock or result is recalculated to erase that deviation.

Input/cached-input/output usage, internal requests/retries/compaction, model service time, human active/waiting person-time, subscription consumption and complete child tool telemetry were unavailable. They remain NOT_OBSERVABLE, not zero. Stage A neither measured native skills/transport nor established **subscription affordability**. The proposed nine-generation/six-hour ceiling is a scheduling bound, not an affordability or completion estimate. No Stage A repetition or later cost-measurement stage is a prerequisite of this proposal.

The historical ledgers remain separate and exhausted: original **24 approved / 24 charged / 0 remaining**, R2-REVIEW **1/1/0**, CMP-2.A **2/2/0**. Aggregate external units are 27, without altering any old ledger. Present root proposal authoring is requested work; its provider usage is unmeasured, not free or zero. No agent/reviewer/model task has been additionally dispatched for this proposal.

## Deliverable and admission boundary

Request one bounded engineering tranche that produces an isolated, independently reviewed implementation candidate, actual deterministic TDD/verification evidence, staged installation/export evidence, and a precise handoff for qualification planning. Its terminal success label is **IMPLEMENTED_AND_INDEPENDENTLY_REVIEWED_FOR_QUALIFICATION_PLANNING**. If a required check or review remains unresolved, return the frozen partial candidate and the specific blockers. Neither label implies native qualification or operational readiness.

This implementation changes enforcement and evidence-admission semantics; **CI-05 selects Full before adopting the changed runtime/validator contract**. CI-06 also applies if implementation changes receiving semantics. Do not bootstrap the new runtime into accepting itself through its new Routine route. Deterministic fixture PASS, the earlier design review and Stage A are not substitutes for the required independent Full evidence. Full still means complete applicable assertion coverage, not automatic execution of all 1,099 historical design units.

No native evaluation, new authentication, token bridge, interactive/nested transport project, general installer redesign, operational refresh, shared-main merge or later measurement stage is included in this engineering request. These boundaries allow useful implementation to finish while native qualification prerequisites remain unresolved.

## Source selection, ownership and dependency order

The current proposal author is root. Its assigned worktree is `/home/bryan/Projects/DevForge/worktrees/skill-validation-policy-20260908T114822309238Z`, branch `proposal/skill-validation-policy-20260908T114822309238Z`, starting clean at the accepted design commit. This task adds only the five files in this new proposal directory. The accepted eight-file directory is immutable.

Future implementation bases proposed here are DevForgeAI **8ede26450ae737a5e928c5f70a945aa995969b30** and DevForge **c7b2a62696c7f3764fdea3313182b9e896339a2a**. The shared DevForgeAI checkout has 14 changed file entries, including contracts; the shared runtime checkout has five, including delivery_core.py. Their exact current preimages are retained. They are neither adopted nor rolled back. Work from committed bases in separate worktrees. Any later integration onto a different shared baseline needs its owner's explicit reconciliation, refreshed pins and checks of the resulting combined bytes; it is not a license to overwrite the dirty checkouts.

[implementation-allocation.json](implementation-allocation.json) fixes per-node file ownership, proposed fresh worktree/branch/output destinations, predecessor bindings and limits. At most **nine new worktrees**, including two conditional repair trees, and at most **three concurrent writers** are proposed. None has been created. Reviewers use fresh prompt contexts and read frozen trees without writes; this does not claim native filesystem/history isolation. Before each writer starts, bind the actual predecessor commit, branch, clean/new destination, allowed paths and output root. An unavailable or changed predecessor stops dependent work; never silently repin.

The dependency order is G1 shared contracts; then G2 runtime core and G5 builder can proceed independently. G3 runtime scheduling and G4 validator follow the frozen G2 test/runtime output; the operator records the package-helper RED before G4. After all focused GREEN evidence exists, G6 combines their frozen commits in two isolated integration worktrees. The operator runs the complete deterministic block and freezes source/binary/output identities before G7's independent combined review.

| Node | Responsible owner | Maximum task window | Output and scope |
| --- | --- | ---: | --- |
| G1 | shared contract owner | 20 min | Transcribe accepted VPR-2 into scoped shared contracts and freeze v2 record rules plus independent requirement-derived test expectations; no redesign or runtime execution. |
| G2 | runtime policy owner | 30 min | Implement protected policy/coverage/lineage parsing and typed task/gate dispositions with discriminating RED/GREEN; preserve every legacy v1 predicate. |
| G3 | runtime schedule owner | 30 min | Implement policy-bound schedule dependencies, complete typed call allocation and distinct funded v2 limits through actual collector/router/capability consumers; retain original v1 24/600/14400 limits. |
| G4 | canonical validator owner | 30 min | Update only canonical Codex validator instructions/references/templates and evidence reducer for Routine/Full and versioned selection, preserving source oracles. Runtime/operator performs helper RED/GREEN. |
| G5 | canonical builder owner | 20 min | Update canonical Codex builder intake, design/handoff/results language and derived shared references to preserve Routine acceptance versus qualification and a nonrecursive prepared handoff; no evaluation. |
| G6 | integration owner | 30 min | Combine only frozen owner commits in isolated integration trees; reconcile capability/installer/helper pins and fixture compatibility; prepare combined candidate and qualification-planning handoff without native execution. |
| G7 | independent combined reviewer | 20 min | One fresh read-only review of exact combined diffs, accepted spec, frozen expectations, original catalogs, actual RED/GREEN and complete check outputs. Review both utility packages, runtime and integration; no self-review or native claim. |
| G8 (conditional) | bounded remediation owner | 30 min | Optional single repair task within existing scope against actual failing evidence. Cannot change accepted policy/oracles, implement native transport, or broaden installation. One repair opportunity across the entire tranche. |
| G9 (conditional) | fresh independent reviewer | 20 min | Optional one fresh read-only re-review when G7 already reviewed a candidate changed by G8; no recursive grader or further repair. If G8 was used before G7, G7 is the independent final review and G9 remains unspent. |

Each row is one initial externally dispatched task, not permission for child delegation or uncounted continuations. Every writer owns only the listed paths in its own tree. G3 may change overlapping runtime files only after G2's ownership has ended and its exact commit is selected. G6 owns the combined integration trees and importer/installer/helper-policy reconciliation; individual workers never mutate shared main. G8 receives only actual finding paths within the union of the existing scopes. No role may edit the accepted policy or an oracle merely to make its change pass.

## Canonical skill and shared-contract changes

**G1 — Shared contract owner.** Update the selected `docs/skill-authoring/skill-validator-design.md`, `docs/mvp/skill-authoring-contract.md`, scoped utility clauses of `docs/mvp/execution-contract.md`, and existing run-manifest, evaluation-report and shared-handoff templates where their fields/claims change. Preserve brainstorm and other-provider obligations. Define opt-in VPR-2 applicability; do not globally waive the old C/B/A convention for unrelated assignments. Pin accepted policy, requested claim, owner-accepted scope/base, immediate/cumulative impact, selected assertions, compatibility evidence, review selection, outcome/disposition and qualification lineage in the existing records. Freeze exact v2 schemas and the requirement-derived expectations before implementation. Envelope and producer authority remain separate from semantic judgment.

**G4 — Canonical validator owner.** The only skill source is `providers/codex/plugins/devforgeai/skills/skill-validator/`. Update SKILL.md, its managed/native/worktree/evidence/enforcement references, plan/results/grade/handoff/report templates and `scripts/assess_evidence.py` for policy selection and honest reduction. Retain all S001–S013 checks and R01–R10 invariant meanings. W1, all P1–P6 and T01–T12 remain Enforced. A task can satisfy its versioned selection obligation while its unselected native observation remains NOT_RUN; selection is not PASS or a invented NOT_APPLICABLE. Native selection, P4 dependencies, current evidence and cumulative lineage determine Routine versus Full disposition. The helper remains an advisory mechanical reducer; it cannot issue protected runtime authority, owner acceptance or a receipt.

Preserve the original `evals/evals.json` bytes and all source cases/assertions. Add only a versioned policy-regression supplement at `evals/validation-policy-cases.json`; use it to exercise the new implementation, not retroactively rewrite original outcomes. Refresh package-local contract copies and `references/derivation.json` from the G1 commit with exact source/destination hashes. Change other listed resources only when affected; a file fence is not an instruction to rewrite every file.

**G5 — Canonical builder owner.** Update `providers/codex/plugins/devforgeai/skills/skill-builder/` only: distinguish scope acceptance, qualification and release claims in intake, design, repair results and prepared handoffs; preserve settled decisions and existing enforced authoring groups. Refresh derived contracts/templates and provenance. A validator's prepared T12 handoff does not demand another Full campaign. Actual target receiving evidence, when required for qualification, still must exist before T09. Builder authoring does not execute a validator or mark a runtime transition complete.

Installed `.agents/skills` copies and exported plugins are generated outputs. No installed resource is an authoring source. Claude skill/hook sources and the other ten application skills are outside the change fence. Shared changes must explicitly retain their current behavior.

## Protected runtime and integration changes

**G2 — Policy and state.** Add the bounded protected parser/reducer `runtime/delivery/validation_policy.py`; connect it to `utility_state.py`, `utility_evidence.py` and the embedded Rust package in `src/delivery.rs`. Reuse existing external assignment, plan/results, task/gate, journal and receipt mechanisms. The model supplies impact/meaning judgments and a real independently selected T04 review; protected runtime validates policy version, authority/freshness, required evidence bindings, classifications, dependency dispositions and final claims. Exact source hashes do not establish semantic adequacy.

Keep `devforge.utility-session/v1` and transport framing unchanged where their shape/meaning is unchanged. Introduce explicit v2 delivery/gate/result/schedule or allocation schemas wherever selection semantics or fields change; never interpret an unknown version as permissive v1 or silently append fields to strict v1 records. Existing v1 sessions, journals and receipts retain their old semantics and replay paths. G1 fixes the concrete schema inventory, allowed fields and cross-version matrix before G2 writes behavior; a consumer change outside the listed fence is a scoped blocker, not implicit authority to broaden it.

Retain separate outcome, selection, report-completion, validation-disposition, current routine acceptance and last qualified identity fields. Missing required evidence blocks suitability; accurate failure reporting may still finish P5/P6. A Routine decision never moves the qualified anchor or substitutes for an owner's adoption decision. New evidence cannot retroactively satisfy an earlier admission gate.

**G3 — Scheduling, native allocation and consumers.** Update `utility_schedule.py` and its `native_schedule.py` kernel adapter so a v2 reviewed selection can require C and A while B is explicitly unselected; selected C failure still blocks its dependents. Keep the v1 all-earlier-tier rule. Native-prerequisite, C, B and A task/gate records remain present with their precise meanings, including a typed no-native selection path that does not fabricate a native plan, boundary evidence or successful launch.

Bind the full original assertion catalog, reviewed evidence-selection map and complete typed call graph independently of the convenient native-attempt projection. Native workers, static reviewers, graders, meaningful parent returns and continuations stay explicit where required. One admissible raw observation may cover several compatible assertions; every assertion retains its own result. Opposite arms, incompatible variants, implicit prompts and earlier temporal prerequisites cannot be collapsed. Do not force every static reviewer into a native installation, and do not invent an optimized Full total before the final observation map exists.

The current v1 24-unit/600-second/14,400-second ceilings occur in both allocation validation and collector checks. Preserve them for v1 and all exhausted historical records. A new v2 allocation must bind distinct external owner authority and explicit total/per-unit/time limits; it cannot borrow from or reset any old grant. Use a complete charged call/continuation inventory, exclusive reservation and journal replay. Propagate the selected limits consistently to `native_process.py`, the scheduler, state reducer and capability reporting. A higher numeric cap alone is not the implementation. No new funded native allocation is created by this proposal.

Adapt only affected strict-version consumers in the listed supervisor/runtime/router paths and advertise support truthfully. Preserve collector authenticity, launch/import/grade separation, one-use claims, owned-process settlement, callback-origin limits and unsupported-method refusal. No arbitrary native launcher, authentication reuse implementation or nested broker is added. Actual native compatibility remains unobserved until a separately funded and admitted qualification campaign.

**G6 — Integration owner.** Reconcile the compiled runtime capability, installer/runtime-requirement consumer, framework structural checker, fixture helper hashes and both source packages. `policies/notes-json.json` and `policies/notes-sqlite.json` pin helper bytes; only this external policy owner may refresh those pins to the independently reviewed selected helper. Do not weaken gate assertions or make tooling worker-editable. Preserve strict existing six-field runtime requirement schemas and existing hook events; any necessary capability metadata must be explicitly versioned and verified, never silently added to a strict v1 shape. No hook registration change or global-state access is part of this tranche.

## TDD, independent review and verification

The frozen policy regression map is [requirement-map.json](requirement-map.json). Its 17 discriminators come from the accepted requirements; expected values must be hand-derived and fixed before implementation, not computed by the new reducer. D means deterministic fixture/CLI checks, S means independent semantic review, and N means actual native evidence required later. A D test of an N evidence predicate does not supply the N observation.

| ID | Discriminating boundary | Evidence required |
| --- | --- | --- |
| VPI-01 | Legacy v1 remains strict | D |
| VPI-02 | Routine no-native reporting | D, S |
| VPI-03 | Authority and version cannot be supplied by worker | D |
| VPI-04 | Selected native prerequisites cannot be removed | D, N |
| VPI-05 | Cumulative lineage cannot reset | D, S |
| VPI-06 | Compatibility is evidenced | D, S, N |
| VPI-07 | Baseline and candidate outcomes remain separate | D, S |
| VPI-08 | Assertion coverage is complete | D, S |
| VPI-09 | Shared evidence is bound to the same conditions | D, S |
| VPI-10 | Batched grades retain independent judgments | D, S |
| VPI-11 | Synthetic data proves only mechanical handling | D, S, N |
| VPI-12 | Target receiving transfer is distinct from evaluator handoff | D, S, N |
| VPI-13 | New funding cannot reopen old ledgers | D |
| VPI-14 | Receipt and replay stay honest | D |
| VPI-15 | Installation preserves evidence identities | D, N |
| VPI-16 | Owner acceptance and qualification differ | D, S, N |
| VPI-17 | Failure reporting can complete without passing | D, S |

For runtime/Rust/helper changes: (1) freeze the contract and failing example; (2) add the meaningful regression; (3) rebuild the current CLI and observe the intended assertion RED; (4) implement minimally; (5) rebuild and run the unchanged expectation to observe GREEN; then refactor if needed. Setup failures, missing binaries, skipped tests and environment errors are not RED. Assert exit, structured stdout, relevant stderr and permitted/forbidden state writes, including failure atomicity. Retain RED test/source identities and raw outputs so G7 can inspect chronology. Runtime authors run their focused tests; the operator/companion test owner runs frozen package-helper tests so canonical skill authoring does not silently become validator execution.

After isolated integration, required commands are run once against the exact candidate; repeat only what actual repair or new findings require. From the **DevForge integration worktree**, retain its default `target/` directory because some Python tests hardcode `target/debug/devforge`:

```text
cargo fmt --check
cargo clippy --locked --all-targets -- -D warnings
cargo build --locked
cargo test --locked --all-targets
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_framework.py --framework <absolute-DevForgeAI-integration-worktree>
python3 scripts/validate_mvp.py --mvp <absolute-DevForgeAI-integration-worktree>/docs/mvp
python3 scripts/demo.py --framework <absolute-DevForgeAI-integration-worktree>
```

These are future command templates, not commands executed for this proposal. Always rebuild after changes to embedded Python. The demo's runtime `.poc` output and framework `.poc` candidates must be in the two owned integration trees; it exercises both providers' synthetic project fixtures and does not launch a model. Bound at most one initial and one justified post-repair verification pass within the shared deterministic allowance. The wrapper `verify_poc.py` omits cargo test and is not substituted for the explicit complete check set. No unrelated fixture or policy is altered to hide failures.

G7 receives exact combined commits/diffs, accepted design, raw requirement/oracle inputs, test expectations and observed evidence, without an author-preferred verdict. Review the change semantics, denial boundaries, v1 compatibility, coverage/correlation, state replay, packaging, ownership and actual test sufficiency. G7 does not independently observe native behavior by reading synthetic logs. A single review covers the relevant combined implementation; no review per requirement or nested reviewer chain is added.

One optional G8 repair can be spent either on a real pre-review check failure or on G7's blockers. If used before G7, G7 examines the repaired final candidate and G9 remains unused. If G7's reviewed candidate changes through G8, run required affected checks and use G9 for one fresh independent review of the resulting exact bytes. Further failure stops this tranche with the remaining work identified. Unused conditional units remain unspent under their distinct proposal; they are not reassigned to measurement or native execution.

## Requested additional allowance

Request **VPI-01: at most nine initial generations and six hours total**, explicitly separate from all exhausted ledgers. Seven normal nodes total 180 minutes of generation windows; G8/G9 add at most 50 minutes. Every node has the 20- or 30-minute bound in the table, including its tools, compilation/tests and settlement. These are newly proposed engineering bounds, not extensions of any historical 600-second native attempt.

The conservative serial allocation is **230 minutes generation windows + 30 preparation + 60 deterministic verification/staging + 30 custody/closeout + 10 non-model contingency = 360 minutes**. The last ten minutes cannot fund another model call. Parallel work may finish sooner, but neither observed Stage A latency nor parallelism is used to promise affordability or success. Do not count a command twice when it runs inside a node window; active person-time, automated intervals, waiting and total elapsed union remain distinct.

All nine calls require explicit new approval; current additional approval and dispatch counts are zero. If all nine are eventually used, aggregate historical-plus-new external charges would be **36**, while the three old ledgers stay 24/24/0, 1/1/0 and 2/2/0. No retry, child model, automatic continuation or unlisted control turn is included. G8/G9 are the only explicitly proposed additional repair/re-review tasks, not an unbounded retry loop. If a chosen authoring method would require another model call, stop that dependent task and report it rather than hiding it in setup.

Start one allocation clock before preparation; include workspace setup, native-free fixture processes, testing, waiting, staging and report assembly. Reserve the full closeout allowance and stop new work before it is consumed. Retain available UTC and monotonic readings and their source; until clock disagreement is resolved, apply the more conservative observed elapsed bound and report discrepancy. No historical or live deadline is reset. Timeouts/censored tasks retain charges and owned processes must be settled. A minimal terminal exception record records a failed deadline; it does not legalize an overrun or authorize another task.

Capture externally dispatched initial/continuation counts separately from actually exposed internal requests, raw token categories, deterministic execution and operator effort. Missing counters stay unavailable. Cached input is not added again to its inclusive input total, cumulative totals are not added to their deltas, and no time/attempt/byte conversion is presented as subscription consumption.

## Integration and operational-installation sequence

1. **Isolated combination and fixture staging — within proposed VPI-01 only after funding.** G6 selects owner commits into fresh integration trees, binds the source pair and built binary, runs the complete checks, and stages a project-local Codex install and fresh runtime-only export. Use the existing installer with absolute reviewed paths:

   ```text
   python3 scripts/install_framework.py --framework <AI-integration> --project <new-owned-staging-project> --provider codex --runtime <CLI-integration>/target/debug/devforge
   python3 scripts/install_framework.py --framework <AI-integration> --provider codex --export-plugin <new-owned-export-parent>/devforgeai
   ```

   Snapshot planned destination files, enforce collisions before writes, read back installed/exported bytes and compare their manifest to selected canonical runtime resources; evals remain source-only. These commands stage fixtures, not the operational project. The current installer enumerates the **entire Codex provider**, not just these two skills: inventory every planned source/destination and require unchanged identities for unrelated packages. It has no assumed per-skill flag. Any unreviewed unrelated change blocks the dependent refresh; do not silently replace another session's installed skill or add a general selector project.

2. **Qualification allocation — distinct subsequent decision.** Preserve all original cases and compute the final assertion-to-observation/grade/dependency map for the exact integrated candidate/environment. Reuse only admissible observations, with distinct per-assertion judgments and sampling limits. G6 supplies the implementation/evidence handoff and known gaps; it does not invent the final reduced Full count. Freeze a concrete complete allocation, supported client/method, separate evidence state, authentication lifecycle and operator burden before requesting native execution funding. Unknown auth isolation or required interactive/nested transport remains a blocker for that dependent qualification, not proof or an automatic engineering task. Do not reuse the exhausted original campaign or launch the 1,099-unit historical design by default. No repeat Stage A or later measurement stage is queued.

3. **Required Full evidence and independent assessment — not funded here.** Run the separately approved campaign against exact frozen bytes, including required C/B/A, candidate/baseline judgments, representative enforcement failures and actual eligible target-to-receiver transfer. Installed manifests or synthetic transcripts cannot satisfy native requirements. Complete Full evidence for the changed enforcement contract is required before operational use. Funding for this step must be concrete and separately approved after its allocation exists; no open-ended allowance is requested here.

4. **Shared integration and operational installation — final owner-controlled step.** Resolve the existing dirty/shared-baseline ownership before any merge; preserve a precise before/after reviewed source pair and binary. If integration changes the qualified bytes or effective environment, refresh affected evidence before adoption instead of silently repinning. The owner may issue one concrete conditional decision for merge, acceptance and the exact project-local installation when their scope is known; do not add per-file approval rounds. Use the installer from the reviewed runtime candidate, verify destination/runtime capability and full planned write set, preserve an exact preimage/installation inventory, then compare post-install identities and required resource/control observations before enabling v2 assignments. Global Codex state or credentials are outside this path.

5. **Recovery and claims.** On an installation mismatch or incomplete post-install check, leave the affected use disabled. Restore only recorded owned preimages or reinstall the pinned last accepted compatible package/runtime pair after collision checks; never reset shared source trees or reuse a stale qualified label. A rollback record identifies actual restored bytes and remaining observations. Record design acceptance, engineering review, qualification, owner adoption and installation as distinct facts. The historical qualified identity and Routine lineage survive all updates.

## Remaining decisions and present checks

The design is accepted; the implementation allowance is not. The concrete worktree/owner model and nine-generation/six-hour request above are ready for a funding decision. Shared-main reconciliation and operational destination/write-set approval wait for an exact reviewed implementation candidate. Final Full observation count, supported native isolation/authentication/transport and measured subscription affordability remain unresolved. None is inferred from Stage A or silently added to this request.

This proposal was authored without additional delegated calls, implementation, test/helper execution, authentication, installation or new native workspace creation. Present checks are limited to current guidance/identity inspection, committed-source and retained-evidence hashes, JSON/arithmetic/path/link checks, full readback and Git diff review. No independent review of this implementation proposal is claimed. [Prepared handoff](prepared-handoff.md) transfers this proposal for the user's allocation decision only.
