# Execution and test integrity

In plan mode, use these procedures for read-only inspection and test design only. Execution actions require the selected plan, candidate and permitted effects.

**QA-010 — Mock-decorator prohibition.** Any mock decorator in selected first-party implementation, tests, or QA helpers causes FAIL, including unused declarations and aliases/wrappers confirmed to apply mocking. Inspect the syntax and imports appropriate to the actual language; analogous mock-generating attributes/annotations are covered. Do not assume a Python-only spelling or equate every decorator/attribute with mocking.

Inventory relevant first-party code and resolve aliases, re-exports, and decorator factories where inspectable. Text search is an initial locator, not sufficient proof of absence. Non-executable examples/comments and vendored dependency internals do not count as first-party mock decorators, but their scope treatment must be explicit. A first-party use of a dependency's mock decorator is covered. When dynamic behavior or unavailable code prevents resolution, record incomplete inspection; never manufacture a clean result.

This specific prohibition applies regardless of claimed test usefulness or passing metrics. Broader test doubles without decorators are not automatically prohibited by that spelling rule, but must satisfy the independent integrity rules and cannot replace required real integration behavior.

**QA-011 — Result-gaming prohibition.** Confirmed tests or evidence processing that game results cause FAIL. Inspect for:

- Vacuous/constant assertions, missing assertions, or tests that never exercise the claimed product behavior.
- Hardcoded/fabricated successful output or expected values computed from the same defective logic without an independent oracle.
- Exceptions swallowed as success, early returns bypassing verification, or timeouts treated as passes.
- Skipped/ignored cases credited as passed, retries counted as new cases, or denominator changes that hide failures.
- Unjustified coverage suppression, omitted first-party files, or helper/setup tests credited as product acceptance.
- Substituting a fake/mock implementation for a required real boundary while claiming integration or native coverage.
- Altering expectations, fixtures, reports, or scope simply to manufacture a passing result.

For each confirmed finding, show the relevant source/evidence and why it cannot establish its claimed behavior. Do not infer deception or developer intent from a defect. Legitimate test setup, ordinary fixtures, dependency isolation permitted by the contract, and language constructs that merely share suspicious names are not automatically gaming. Unresolved candidates remain explicit incomplete investigations; they do not justify a clean integrity result.

## Execute the selected plan

**QA-013 — Admission and isolation.** Before executing, reread the selected plan, candidate, rules, and evidence paths. Stop affected checks when identities drift; do not silently rebind an approved plan to changed source. Reuse valid unaffected evidence only with explicit binding and a recorded reason, never from a summary claiming PASS alone.

Execution may create independent tests, fixtures, and evidence in its authorized QA locations and operate disposable product state. These writes are not repairs to product source or developer tests. Preserve candidate bytes and prior attempts. Builds/instrumentation use declared output locations or disposable copies, with candidate identity verified before and after. No installation, startup configuration, destructive production data operations, permissions changes, network access, or migrations beyond current authorization.

**QA-014 — Build, function, and contracts.** Verify applicable build instructions, dependency locks, artifact contents, and source-to-artifact correspondence. Execute functional normal/negative/boundary acceptance cases and real integration checks specified at component boundaries. Validate serialization, version behavior, state transitions, persistence, and error propagation where relevant. A help command or compiled artifact is not evidence of full behavior.

**QA-015 — Regression and platform coverage.** Execute relevant unit and regression suites, impacted consumer checks, backward compatibility, configuration changes, and required platform cases. Derive actual platform obligations from selected inputs. Keep each platform's results and limitations distinct. A Windows process reading Linux files is not a Linux-native test, and a Linux build does not qualify Windows GUI behavior.

**QA-016 — Reliability, security, performance, and usability.** Execute relevant specification-driven recovery, interruption, cancellation, timeout, concurrency, resource-exhaustion, authorization, isolation, unsafe-input, path/data-protection, and dependency-risk checks. Scope the assessment; do not label a bounded QA security check as an exhaustive security audit.

Measure performance against explicit budgets on a declared workload and host. If no threshold exists, report measurements as observations and identify any required missing acceptance decision. Assess CLI/API diagnostics, documentation accuracy, accessibility, and user workflows where required. Native UI/visual checks need actual evidence; terminal/static results cannot establish rendered behavior. If such evidence is unavailable, leave the required case NOT_RUN and explain the needed handoff. Browser/MCP access is not a prerequisite of the portable skill.

**QA-017 — Execution evidence.** Retain case and attempt IDs, criterion references, exact commands/actions, working directory, platform/tool versions, fixture identity, timestamps, exit codes, output references/hashes, expected and actual observations, cleanup, and interpretation. Preserve failed attempts and uncertainty after timeout. Retry only within current authorization and plan budgets; do not silently repeat consumed or irreversible actions.

Results are PASS, FAIL, ERROR, NOT_RUN, or NOT_APPLICABLE at the case level. NOT_APPLICABLE needs a specification/scope reason and must not hide an unavailable required check. Redact credentials while indicating redactions; do not falsely claim redacted text is a byte-exact unredacted command. Existing developer evidence and independently executed evidence remain labeled separately.

## Record a case and its attempts

Use the stable case ID from the plan and unique attempt IDs. Record category (unit, integration, acceptance, native or setup), required platform, execution provenance (developer-supplied, independent QA or manual native), candidate/plan/specification references, and status alongside the QA-017 receipt fields. Separate observed exit success from the expected behavioral assertions. Retain raw tool reports and capture their interpretation without rewriting them as passing evidence.

For uncertain timeouts/interruption, checkpoint the owned processes, fixtures, last observed state and next safe observation. Do not delete unrelated state or rerun a consumed action blindly. Track authorized retry budgets independently of case counts. A skipped or blocked required case uses NOT_RUN with its reason; it stays in the required inventory.

Before accepting an integrity absence claim, enumerate in-scope first-party files, inspect language-appropriate syntax/imports and follow resolvable aliases, re-exports, wrappers and factories. Record uninspectable/dynamic regions as omissions. Include QA-authored helpers in that inspection. If a suspected pattern is ordinary fixture setup, explain its limited claim rather than assigning product acceptance credit or alleging gaming. If confirmed, cite exact source and the assertion/boundary it fails to establish.

Feed valid raw evidence to [assessment](assessment.md), then use [reporting and handoff](reporting-handoff.md). QA source observations and evidence processing do not authorize protected phase transitions.

