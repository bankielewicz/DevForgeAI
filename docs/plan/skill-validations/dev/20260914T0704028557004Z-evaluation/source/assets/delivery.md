# Development delivery template

- Selected scope: [implementation/plan/subset, explicit documents and source-qualified requirements]
- Overall development status: [COMPLETE/PARTIAL/BLOCKED and evidence-based reason]
- Final candidate identity: [source/test/config manifest locators and hashes, tools/platforms, Git when applicable]
- Implemented outputs/changed paths: [actual deliverables and purpose]
- Requirement accounting: [traceability locator; selected count and verified/pending/blocked counts; exclusions]
- Plan-only/subset limitation: [what selected completion covers, where applicable]

## Checks and metrics

### Required output destination readback

Original selection: [complete selected_evidence_value, selection_source and resolved_evidence_root, reread from original input].

| Required output | Required actual path | Observed actual path | Readback evidence | Result or missing correction |
| --- | --- | --- | --- | --- |
| [promised file/record] | [path derived from original selection] | [observed path, or absent] | [command/observation locator and file digest] | [verified or precise mismatch/gap] |

A missing or wrongly placed required output prevents VERIFIED/COMPLETE even when product tests pass. Preserve misplaced attempts and report their locations.

| Required check/platform | Candidate and attempt/report references | Result | Counts/measurement or unperformed reason |
| --- | --- | --- | --- |
| [behavior, integration, regression, negative, recovery, format, static, coverage, native/visual] | [locators/digests] | [PASS/FAIL/ERROR/NOT_RUN/NOT_APPLICABLE] | [observed details] |

- Declared required-case set and policy: [source, exact denominator, classification]
- Pass-rate accounting: [passing/all required; failed/errored/skipped/blocked/unexecuted counts; exact percentage and project threshold]
- Coverage: [metric definition; source denominator/exclusions; raw counts; measurement tool/report; executed-line and branch separately if available; project threshold]
- Per-platform qualification: [each required host; unavailable required cases are NOT_RUN]
- Earlier attempts and flakiness: [retained history and unresolved issues; no denominator inflation]
- Remaining defects/gaps: [affected requirements, minimum resolution]
- Native/visual checks unperformed: [exact cases and needed evidence]

## Acceptance and continuation

- External framework acceptance: [actual authority response locator/digest or NOT_EVALUATED; identify if outside scope]
- Checkpoint: [locator/hash when work remains]
- Next safe action: [remaining selected work or concrete missing input/capability/authorization]

Development completion does not grant protected acceptance. Do not label overall COMPLETE while selected mandatory implementation or verification remains.
