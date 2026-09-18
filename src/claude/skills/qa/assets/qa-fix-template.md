# QA Remediation Handoff to dev

## Selected candidate and authority
- QA run and FAIL report: [actual reference and hash]
- Source/build candidate: [actual manifest/artifact references and hashes]
- Governing specifications/stories: [exact inputs and hashes]
- Applicable rules and quality floors: [references and resolved values]
- Project/environment and current evidence destination: [actual values]
- Remediation owner: dev
- Selected confirmed defect IDs: [complete list]
- Authorized repair scope: [product/test paths or responsibilities, allowed effects]
- Excluded effects: [installation/deployment/etc. outside current authorization]

## Defect [stable ID]
- Violated criterion or mandatory QA policy: [exact clause and source locator]
- Issue classification and terminal/nonterminal disposition: [INTEGRITY_FAILURE/METRIC_FAILURE/CRITICAL_PRODUCT_DEFECT/MANDATORY_PRODUCT_DEFECT; trigger evidence and ordered decision]
- Severity and demonstrated impact: [facts, governing requirement; no unsupported critical label]
- Exact defective artifact ownership: [application/developer-test/QA-created helper or evidence processing, verified path and scoped remediation responsibility]
- Verified affected files/symbols/interfaces: [references; otherwise explicitly unknown]
- Preconditions and environment: [versions, state, permissions]
- Test data: [fixture identity and required inputs]
- Reproduction procedure: [ordered exact commands/actions with working directories]
- Expected behavior: [specification-derived observable result]
- Actual behavior: [observed output/state]
- Evidence: [case/attempt IDs, logs, source ranges, artifacts, hashes]
- Reproduction status: [reproduced or confirmed static finding; do not fabricate a run]
- Root cause: [confirmed explanation or not established]
- Required correction: [behavior/invariant to restore, not speculative implementation]
- Compatibility and preservation constraints: [existing behavior/data/interfaces]
- Regression requirements: [specific missing/incorrect cases and test oracles]
- QA retest conditions: [explicit corrected-candidate retest selection, exact independent observations, affected regressions and invalidated integrity/metric collections to reestablish; no automatic repair/retest]
- Tests stopped and still required: [case/attempt IDs, preserved FAIL/ERROR, remaining NOT_RUN with trigger IDs and partial metric obligations]
- Containment and safe cleanup state: [owned operations and actual disposition; no further reproductions after terminal stop]
- Dependencies on other defects/decisions: [IDs and ordering or none]

## Return contract from dev
- Corrected candidate source/build identity and changed-file manifest.
- Per-defect correction and evidence references; no self-issued QA closure.
- Recorded red/green/refactor and regression results.
- Current coverage and required unit-test counts, denominators, and raw reports.
- Compatibility checks and remaining gaps.
- Exact artifacts and environments needed by QA for retesting.

## Pending prerequisite or specification decisions
- [Separate unresolved decisions/QA prerequisites with owner and affected cases; not invented fixes.]

## End-user remediation invocation
- Required project/environment to open in Claude Code: [resolved value]
- dev availability: [verified selection mechanism or missing prerequisite]
- Paste into the Claude Code session input: [complete resolved dev prompt]
