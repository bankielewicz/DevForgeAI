# CMP-2: staged cost measurement proposal

Status: **Draft for review. No stage is approved, admitted or executed.** Replaces CMP-1 as the current proposal; the original ten-generation plan and packets remain in commit 5eaa7c0 and its custody records. A cost stage produces **no Routine PASS or Full qualification result**.

## Stage A: the smallest useful executable workload

Use the already available collaboration.spawn_agent interface (default agent, fork_turns=none, no model override) for two serial, fresh prompt contexts: a small instruction-paragraph revision, then an independent semantic review of that output against the raw request and original paragraph. Both tasks return text. They require no target skill invocation, local native client/profile, installation, authentication, interactive answer, nested child transport, proposed policy parser or new runtime implementation.

“Currently executable” means the task dispatch, fresh-context option and text-return interface are available in this session. It does not mean the run has occurred or that funding is available. Once explicitly funded, the operator can dispatch these two tasks with the existing interface; no infrastructure project is a prerequisite. If that interface or its existing authentication is unavailable at the time of allocation, stop and report that fact rather than silently moving Stage A to a native harness.

| Node | Work and inputs | Independent context / bound |
| --- | --- | --- |
| A1 | Revise a supplied paragraph so a missing adoption owner is recorded as an open question without blocking a draft; preserve local-only scope and no-adoption behavior. Raw before-text and change request are frozen in pilot-packets.json. Return the revised paragraph only; no tools or skill invocation requested. | Fresh task context, no inherited author conversation; one generation, at most 600 seconds. |
| A2 | Review A1's exact returned text against the original paragraph, raw request and frozen criteria. Judge each criterion with brief evidence and unavailable status where needed. No author's preferred outcome, commentary or previous verdict. | Different fresh reviewer context; one generation, at most 600 seconds. |

A2 measures both review overhead and whether the intended editing workload occurred. It is independent of A1 authorship, subject to recorded shared provider/system-context limits. A fresh task context is not a native filesystem/history sandbox. Both contexts receive the complete bounded raw task in their prompt and are instructed not to read files, use tools, activate a skill or delegate. The operator records any unexpected tool/context exposure as contamination/overhead; it does not become clean native evidence. No claim of independent review is made until A2 actually occurs with the required separation.

The 600-second task bound runs from dispatch through terminal settlement; an unfinished task is interrupted and retained as incomplete. Preparation and final record assembly have their separately listed overhead bounds. No live task deadline is paused or restarted.

One repetition; zero continuations and zero retries. A2 can assess an authentic partial/failure output, or record the absence of usable output. An A1 timeout remains a charged, censored observation. No extra repair or dispute-resolution model call is included. The operator captures exact raw input/output and usage metadata exposed by the interface, plus start/end events. Existing document/custody tooling is sufficient to record these facts; no evaluated helper is invoked.

Proposed Stage A bounds: two model generations × 600 seconds, plus 180 seconds packet/identity preparation, 180 seconds operator/capture overhead and 240 seconds closeout = **1,800 seconds (30 minutes)**. No new browser sign-in is planned; the selected interface uses the session's existing authentication without reading credentials. The two fresh prompt contexts are not two new authentication realms. These ceilings are not observed cost estimates.

Stage A measures initial prompt-edit generation and independent-review usage where exposed, actual elapsed times, active operator effort, waiting and capture overhead on this host interface. It cannot establish native skill execution, installed resource resolution, activation, paired utility performance, interactive latency, nested transport, native state isolation or subscription consumption from dispatch counts. Missing token/internal-request counters are NOT_OBSERVABLE, not zero. Even if those counters are absent, actual dispatch count, elapsed time and operator effort are useful first observations; token instrumentation becomes a specific later gap, not a reason to implement the whole framework first.

## Later stages require demonstrated measurement gaps

These are bounded **candidate designs**, not requested funding or automatically queued work. After Stage A, the owner may allocate one only if its named gap matters to a concrete future validation decision. Each decision freezes its exact identities, method, remaining prerequisites, counts and time. If no relevant gap remains, do not run it.

| Stage | Gap that warrants allocation | Proposed workload / maximum demand | What it cannot establish |
| --- | --- | --- | --- |
| B: paired native authoring | Stage A does not measure installed utility/resource overhead, candidate/baseline output size or native usage capture needed for a selected maintenance plan. | Candidate and preserved baseline each perform one fully specified authoring task; one independent reviewer grades both separately and then compares. 3 initial generations, 3 fresh evidence contexts, 0 continuations, 0 retries; candidate ceiling 3,600 seconds including setup/auth/capture/closeout. | No spontaneous-question or interactive continuation cost, nested review, broad activation accuracy, Routine PASS or qualification. |
| C: interactive authoring | A/B leave operator-answer turnaround, continuation cost or parent wall-time impact unknown for a required interactive workload. | Fresh candidate/baseline parents each ask one deliberately withheld input and receive at most one matched literal answer; one paired grader. 5 generations = 3 initial contexts + 2 same-parent continuations; 0 retries; candidate ceiling 4,500 seconds including all overhead. | No rate of spontaneous clarification success, arbitrary dialogue cost, nested validator behavior or qualification. This is a controlled one-question cost sample. |
| D: nested validator review | Earlier observations do not measure a real independent inner review, authenticated result return, parent resumption and resulting report cost needed by a selected native plan. | One native validator parent, one actual fresh independent child review, one counted parent return, one independent report grader. 4 generations = 3 initial contexts + 1 continuation; 0 retries; candidate ceiling 3,600 seconds including overhead. | No complete inner C/B/A campaign, recursive qualification, arbitrary nesting, routine validation result or Full qualification. |

B–D keep the preserved candidate/baseline source references for continuity; a changed selection needs a newly reviewed stage allocation. The old-skill baseline a78b9bff83c090153952b31b84b0584ef1650f02 already includes workspace-allocation work. Compare actual changed package resources, not Git labels alone. Do not claim causal improvement from unrelated earlier changes. Exact future native installation/output/state paths are intentionally not allocated now; no unused profile or workspace was created for this specification revision.

A Stage C parent retains one 600-second whole-attempt deadline: up to 240 seconds initial work + 180 seconds continuation + 180 seconds total actual waiting, interpretation, transport and settlement. A Stage D parent retains one 600-second bound: 150 initial + 150 child review + 150 return + 150 transport/settlement. The child inherits the earlier parent deadline. The independent final graders retain their own at-most-600-second bounds. Stage ceilings include all setup/auth/operator/capture/closeout and never extend an individual or parent deadline. If the actual required overhead cannot fit, do not admit that stage under the proposed bound.

B–D require a demonstrated appropriate native method and actual state/process/filesystem separation. C/D additionally require supported question or child-return transport. They cannot smuggle implementation calls, extra probes, token instrumentation models, graders or controller decisions into “setup.” Such work is separately proposed and approved if it becomes necessary. These gaps do not block Stage A.

## Authentication lifecycle and practical burden

Keep evidence-context/workspace/history independence separate from account authentication. Supported cached login reuse and automatic refresh can avoid repeated browser flows. That does not prove isolated state. [OpenAI authentication](https://learn.chatgpt.com/docs/auth#login-caching). CODEX_HOME includes more than credentials, and an OS credential-store option alone does not establish safe cross-root reuse. [State locations](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations).

- Stage A proposes **zero new sign-ins** using the currently available authenticated task service. No ordinary global directory, keyring or auth file is read or exposed. It measures host-context costs, not native isolation.
- For native stages, a dedicated operator-owned authenticated host with fresh separated evidence state, or supported credential-store reuse across separated state roots, may reduce sign-ins. The selected client's cross-root lookup/refresh and host/worker state boundaries remain **unresolved**, not implemented or verified. No credential bytes may be copied, symlinked into workspaces, exported into prompts or passed through an unsupported token bridge.
- If each native context needs a distinct credential realm because supported reuse cannot meet the required isolation, explain that concrete dependency. B/C/D each propose three fresh evidence contexts; a continuation retains its parent's authentication lifecycle. Budget zero to three sign-ins according to the actually selected supported arrangement, not one per generation. An expired/revoked session adds an actual auth event and stops if no allocated time/authority remains.

For planning sensitivity only, at an assumed 5–10 minutes of operator involvement per fresh sign-in, the historical 907-sign-in choice would consume **75.6–151.2 operator hours**; CMP-1's seven would consume **35–70 minutes**. These are unmeasured assumptions, not observed sign-in times. Three sign-ins in a later stage would cost **15–30 minutes** under the same assumption; this may dominate the model workload. A supported shared lifecycle could reduce auth events, but no saving is claimed without observation. The owner should decline or redesign a native stage if its isolation/authentication overhead makes the intended measurement impractical.

We read public documentation and retained protocol schemas only. No account status, credentials, authentication flow, profile setup or live reuse test was inspected/executed.

## Funding: exhausted history and separate proposals

The original ledger remains **24 approved / 24 charged / 0 remaining**. It cannot fund any new stage, and no spent slot is reclaimed. The user-authorized root specification revision does not silently authorize delegated review or evaluation calls. Its provider usage is unmeasured, not zero; the existing attempt ledger is retained without inventing subscription-consumption entries.

| Separate proposal | New maximum demand | Time ceiling | Approval status |
| --- | ---: | ---: | --- |
| R2-REVIEW | 1 independent review generation of the completed policy/audit/stage design; zero retries | 1,200 seconds total: 600 model + 300 preparation + 300 closeout | Proposed; not approved or run |
| CMP-2.A | 2 generations (A1 task + A2 independent review); zero retries | 1,800 seconds total | Proposed; not approved or run |
| CMP-2.B / C / D | 3 / 5 / 4 candidate units, each subject to a later gap-based allocation | 3,600 / 4,500 / 3,600 seconds candidate bounds | Future options; no funding requested now |

R2-REVIEW and Stage A are independently selectable proposals. If both are expressly approved and fully consumed, the aggregate historical-plus-new charged count would be **27**, consisting of the intact original 24 plus three new charges under linked new authority. No approval, cap amendment or new charge has occurred. Approval of documentation, R2-REVIEW, or one pilot stage does not authorize another. No runtime implementation tranche or 1,099-unit campaign is requested by this revision.

## Usage and time accounting

Use the existing plan/result record and ordinary raw transcript/custody storage; do not add a bespoke approval artifact for each metric. The allocation JSON declares fields, stage nodes and proposed bounds. The operator/collector can generate record identities, hashes, joins and arithmetic mechanically. Model-produced explanations are not a usage meter.

| Quantity | Measurement and limitation |
| --- | --- |
| External generations/continuations | Count each actual task/turn/resumption dispatched; identify initial versus continuation and parent. Include charged failures and unplanned requests in actual accounting. Unlaunched slots are not executed. |
| Internal model requests | Record only actual provider/client-observed requests, automatic retries or compaction calls, with source and scope. One external generation may contain multiple internal requests; absence of a counter is NOT_OBSERVABLE. |
| Reported token usage | Preserve reported input, cached-input, output and other token fields with their exact meanings and whether turn/session cumulative. Cached input may be a subset of input; do not sum it again. Never add cumulative totals to their own turn deltas. No invented token estimate from character length or time. |
| Deterministic execution | Count/measure commands, helpers, capture/parsing and mechanical checks separately from model dispatch; record actual exit, wall duration and purpose. Model invocations hidden behind a command still count as model work. |
| Active operator time | Record preparation, interpreting/sending answers, authentication, intervention, grade review and closeout intervals per person. Distinguish active involvement from time waiting for a model/browser. |
| Waiting and elapsed time | Keep actual waiting intervals and total start-to-closeout elapsed time. Use a union of intervals: parent spans overlap children, and active operator/model work can overlap. Sum person-time separately; do not double-count elapsed time or pause deadlines. |

Use UTC and monotonic timestamps where available; otherwise retain the actual clock source and resolution. “Model service time” is available only if directly reported; generation wall time includes visible and invisible overhead. Raw usage counters do not establish subscription-balance consumption unless the provider exposes that meaning. Attempt counts and time ceilings are scheduling controls, not reliable subscription-consumption or dollar estimates.

The stage report records actual observations, sample count, limits, independent-review status, failure/censoring, operator burden and unobserved fields. A small Stage A report can be measurement-complete for dispatch/time/operator costs while token/internal-request consumption stays unobserved. Do not call the missing measures zero or claim the pilot fully estimates subscription cost.

Use observations only for a future explicitly selected workload: distinguish fixed setup/auth costs, task size and stratum, initial/continuation/grading work, and unsampled native/interactive/nested effects. With one specimen per condition, report individual values and limits, not percentiles, failure probabilities or an unjustified extrapolation across all 1,099 historical units. Each later stage must name the gap it would resolve and why that matters to a practical allocation decision.
