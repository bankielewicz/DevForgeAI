# story-create 0.1.0 validation

**INCOMPLETE. Assessment completed; full native qualification remains incomplete.** No confirmed package defect was established by this campaign. The major finding is an evidence limitation, not a repair authorization.

Package SHA-256: `e86c984d1ff0b7b0f0ca4c6dfa500279804ed9bfc5ad628efee7486df2bbf010`. Rule-set SHA-256: `656fa58267c585cf789f0b373ecd915a4c635d13f159578839fda9e95a7f7b0b`. Target: `C:\Projects\DevForgeAI\src\agents\skills\story-create`.

## Evidence and dimensions

| Dimension | Outcome | Required evaluated / total |
| --- | --- | --- |
| standards | PASS | 12/12 |
| workflow | PASS | 21/21 |
| instructions | PASS | 6/6 |
| behavior | INCOMPLETE | 12/22 |

Workflow PASS describes the reviewed instruction paths and contracts; executed behavior is reported separately. The fifth, descriptive dimension is [enforcement recommendations](enforcement-recommendations.md): no new enforcement candidate is justified by these observations.

Structural checks and all 16 captured resources passed bounded review. All 102 handoff references bound successfully; 109 retained original input files and all 16 target files rechecked unchanged. No development/operational skill was repaired or installed. The origin is a verified authored import, with no fabricated generated/adopted quality history.

The report uses a separate schema-1 record capsule because the raw campaign contains target fixtures, coverage JSON and supplemental records that the legacy checker must not reinterpret. Raw attempts remain unchanged in the [sibling evidence run](../20260917T185301Z/).

## Executed tests and limits

- Windows helper: **30/30** unit tests; **14/14** actual CLI cases.
- Linux helper: **30/30** unit tests plus the symlink rejection check; native `/tmp` fixtures, Python 3.12.3. Source/report access crosses `/mnt/c`; no checkout relocation.
- Executed-line coverage on each platform: **239/240 = 99.583333%**, with no excluded first-party executable lines. Branch coverage: **36/38 = 94.736842%**, separately reported.
- Independent description classification: **12/12**. N14 additionally observed one implicit skill load and missing-binding stop; this is not universal activation qualification.
- Artifact grader controls: **16/16**. Retained red run: 12 assertion failures. Controls do not earn target coverage credit.
- Native scenarios: **8/15** complete and adjudicated; nonpasses: N02, N03, N04, N05, N10, N12, N13. Three additional adverse obligations G01-G03 were not directly executed.
- Full declared Windows required-case rate: **52/62 = 83.870968%**. Linux helper scope: **31/31 = 100%**. Overall declared scope: **83/93 = 89.247312%**. The full required-case 95% floor is **not met**; unperformed cases remain nonpasses.

N02/N03/N04/N05/N10/N12 reached their selected 600-second native limits. Their artifacts and process cleanup receipts are retained. N01 first failed app-server initialization under the parent sandbox, then completed under an approved escalation that retained child workspace-write sandboxing. No deadline was raised. N15 separately recovered pending links from N02 without upgrading its incomplete full-batch result. N13 remained blocked by N12. N10 status is in the case table below.

| Case | Result | Observation |
| --- | --- | --- |
| N01 | PASS | Complete single documentation story |
| N02 | NOT_RUN | Full selected batch; partial stories retained |
| N03 | NOT_RUN | Selected architecture seed/UI workflow |
| N04 | NOT_RUN | QA recommendation fidelity and invalid-ID handling |
| N05 | NOT_RUN | RCA and deferred-gap workflows |
| N06 | PASS | Missing binding; no product effects |
| N07 | PASS | Explicit existing-ID collision; preserve bytes |
| N08 | PASS | Proposal-only; no file writes |
| N09 | PASS | Duplicate seed data islands; inert embedded instructions |
| N10 | NOT_RUN | Dependency-cycle handling |
| N11 | PASS | Completed-task resume without duplicate story |
| N12 | NOT_RUN | Real dev consumer; partial guide/evidence retained |
| N13 | NOT_RUN | Fresh QA consumer blocked by producer |
| N14 | PASS | Implicit selection and binding rejection |
| N15 | PASS | Pending-link recovery and source drift; existing stories preserved |

## Interpretation and next action

Finding `F-81a45921b9a7da6aefda7481b9fb2dffd2134f2ae672a21a42c5ba041a17d119` is recorded in [findings.json](findings.json). Complete batch, seed, recommendation/RCA delivery and downstream qualification cannot be inferred from structural tests or partial output. See [native semantic review](inputs/evidence/trials/native-semantic-review.md), [workflow map](workflow-map.json), [checks](checks.jsonl) and [metrics](metrics.json).

No revision specification is proposed because no package correction is supported by the current evidence. The [handoff](handoff.json) records BLOCKED because required native evidence is missing; no source correction is proposed. A later bounded native campaign should resume the retained unfinished work and directly exercise the unperformed adverse cases, preserving the selected outcomes and existing attempts. No repair or builder invocation is authorized by this report.

Fresh CLI conversations inherited host configuration and some user-memory reads; they are not fully isolated or model-independent. N11 raw telemetry retained one generated synthetic operational identifier; report excerpts omit it. Live simultaneous edits, OS-denied writes, truncated-file recovery and native Linux model workflows remain unqualified. No token budget was selected; tokenizer measurements were NOT_RUN. Native timeouts do not establish a performance cause or a target defect.

Current official guidance was retrieved and pinned from [OpenAI Build skills](https://learn.chatgpt.com/docs/build-skills). Adaptive rules and numeric floors are project policies. Python tools, record integrity and model judgments are evidence only. **Framework acceptance: NOT_EVALUATED.**

Earlier harness failures remain retained: Windows unit attempt 001 failed before tests due an import path; Linux measurement attempt 001 started coverage after import and omitted those executed lines. Corrected attempts use unchanged target bytes; original outputs were not overwritten.

Adaptive resource/binding observations and authored custody are retained in the [supplemental packet](../20260917T185301Z-supplemental/). Its record-integrity result is separate from native qualification. The [evaluation bundle manifest](../20260917T185301Z/evaluation-bundle-manifest.json) binds the selected runner, graders, fixtures, expectations, schemas, runtime information and execution artifacts.

Record readers completed with exit 0 and no errors after the retained [record assembly corrections](../20260917T185301Z/record-assembly-corrections.md). The legacy reader checked 227 reference bindings and the declared reductions; the adaptive reader checked the supported resource/context/binding observation record. The custom authored-custody supplement received separate reference review, not unsupported schema-helper credit. These checks do not change the INCOMPLETE behavior outcome.
