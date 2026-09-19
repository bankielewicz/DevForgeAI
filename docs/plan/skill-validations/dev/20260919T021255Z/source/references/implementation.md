# Product implementation, TDD, and QA

Apply this to authorized product work. Product tests are part of this workflow, independent of assessment of the installed skill package.

## Inspect for reuse, then plan

Before adding a substantial method, class, module, or service, inspect existing code and tests for the same responsibility. Search behavior terms, names, comments/documentation, interfaces, dependencies, and call sites. Inspect plausible candidates even when names differ. Optional structural/semantic/index tools can help; record freshness and coverage limitations and inspect current source. No search match is not proof of absence.

For candidates record reuse, extension, composition, or new implementation with source/test references and compatibility/ownership reasons in the [slice plan](../assets/slice-plan.md). Do not force reuse when required behavior or ownership makes it unsuitable. Scope this assessment to the proposed responsibility.

Plan dependency-ordered slices identifying requirement IDs, existing components/additions, consumed/provided contracts, dependencies, owned change scope, expected behavior, and verification. Establish shared schemas/protocol ownership before consumers. Favor observable end-to-end slices over disconnected scaffolding. Every selected requirement needs a verification method or a precise gap. File counts or completed slice percentages cannot establish delivery.

The entire workflow can run in one session. Delegation is not required; separately authorized delegation must preserve ownership and evidence.

## Resolve commands before execution

Derive build, test, formatting, static-analysis, integration, and coverage commands from actual manifests, scripts, and documentation. Inspect effects, required dependencies, installed executable resolution/version, shell, platform, and working directory. Preserve argument data using native argument handling, especially paths with spaces, Unicode, or shell metacharacters. Avoid string interpolation that could execute data. Choose bounded noninteractive execution with an appropriate recorded timeout.

If tooling is absent, use the project-prescribed toolchain or resolve the material decision. Minimum build/test scaffolding is allowed within product scope. Dependency installation, network, or elevated privileges follow existing authorization and host approvals. Do not replace the target language to evade missing tools. Keep native host and filesystem identity visible; another checkout needs separate identity and scope verification.

Use [execution records](../assets/execution-record.jsonl) following [evidence-resume.md](evidence-resume.md). Record each actual attempt, even setup failures and timeouts.

## Red

For each behavioral slice, write focused tests with concrete expected behavior before changing production behavior. Execute them and preserve the failure. Explain why it demonstrates absent/incorrect required behavior. An unavailable executable, broken test syntax/setup, invalid environment, or unrelated dependency error is a prerequisite failure, not a valid red result.

In a new project establish the minimum runnable harness first; record setup separately. Existing behavior characterization tests may initially pass: retain them as regression evidence and add a distinct failing case for the requested change. Never break correct production code to manufacture red. A compilation failure counts only when an intentionally missing contract is the expected failure and the test/harness otherwise establishes that fact.

For documentation-only work, retain the applicable factual, link, requirement, and consistency review instead of inventing behavioral red/green evidence.

## Green

Implement the minimum real required behavior and rerun the same focused tests. Preserve expected assertions. Do not stub out the integration under test, hardcode fixture answers, suppress errors, or weaken assertions to obtain success. Document mocks at external boundaries and perform real integration when required. If the intended expectation is contradictory, stop the dependent change and resolve the requirement rather than silently rewriting it.

## Refactor and integration

Improve structure without changing tested behavior or public contracts. Rerun affected tests after refactoring; when no refactor is needed, record the reason without artificial churn. Keep broader architecture work within scope or propose it separately. Integrate dependency-ordered components and verify actual interactions, failure behavior, and shared-contract compatibility.

## QA and metrics

On the integrated candidate run applicable regression, integration, negative-path, formatting, static-analysis, coverage, and platform checks derived from contracts and changed paths. Include recovery, concurrency, invalid-input, and denied-operation cases where specified. Retain all attempts. Once sufficient checks pass, broaden/repeat only for new changes, failures, or unresolved concerns.

Before measurement declare the candidate, required-case set, tools, metric definitions, source denominator, exclusions, thresholds, and required platforms. Derive these from project policy; resolve missing needed acceptance metrics instead of choosing universal defaults. Keep executed-line and branch coverage distinct when available. Never exclude uncovered owned behavior to improve a result.

Count each declared required case once. Preserve failed, errored, skipped, blocked, and unexecuted required cases as nonpasses under the applicable policy; show their counts. When required-case pass rate is used, compute passing required cases divided by all declared required cases, multiplied by 100. Do not round a below-threshold metric up, remove required skips, or mix revisions. Preserve earlier attempts as history; they neither enlarge nor shrink the case denominator. Use a coherent final candidate for final qualification and disclose unresolved flakiness even after a later pass. Numeric floors do not waive mandatory failures or regressions.

Record raw measurements, tool/report locators, counts, exclusions, and per-platform results in the [delivery template](../assets/delivery.md). Missing measurement is unperformed, never an estimated pass.

## Native and external behavior

Compilation, mocks, static inspection, and command help do not prove native service behavior. Run required native checks on their declared host when authorized and available. Otherwise name exact unperformed cases and retain a partial result; do not infer another platform passed or install operational components merely to erase a gap.

Keep builds and behavioral verification operable through the Claude Code terminal. A GUI product may need separate native/human visual evidence: request it or report the case unperformed. Terminal success cannot certify rendered visuals. No browser or MCP is mandatory for this skill.

Finish with [failure-delivery.md](failure-delivery.md), even when implementation succeeded but QA or authority responses remain unavailable.

