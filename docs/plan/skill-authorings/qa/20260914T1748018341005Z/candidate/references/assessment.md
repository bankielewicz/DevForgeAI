# Metrics and verdict

**QA-018 — Mandatory numerical floors.** Require first-party executable-line coverage >=95% and required unit-test pass rate >=95%, independently for each required platform and the declared overall scope. Use stricter project thresholds where specified. Lower project values do not waive these selected QA floors; record that mismatch rather than adopting the lower value.

Coverage is `100 * executed eligible first-party lines / all eligible first-party executable lines`. Declare the denominator, tool, scope, and exclusions before claiming a result. Exclude declared third-party/generated dependency code and fixture data, not uncovered first-party functionality. Report branch coverage separately when available. If a selected language/tool cannot establish executed-line coverage, that measurement remains unavailable, not an inferred pass.

Unit-test pass rate is `100 * passing required unit cases / all required unit cases`. Do not mix integration, GUI, setup, or acceptance-case counts into it. Enumerate the declared required unit-case inventory from project policy, inspected suites, and the QA plan. Missing required unit tests are gaps; existing suite size is not proof that this inventory is complete. Required skipped, blocked, errored, failed, and unexecuted unit cases are not passes. A zero or unresolved denominator cannot yield 100%.

Count each case once for the final candidate; retain all retry attempts separately. Recalculate aggregates from raw records, not rounded dashboard values. Do not round subthreshold metrics upward, drop failing cases, or reuse coverage from different source bytes. Report values such as 94.99% as below threshold. Report test integrity, criterion coverage, and unit/code metrics separately.

**QA-019 — Verdict.** Execution produces one product QA verdict:

| Verdict | Rule |
| --- | --- |
| FAIL | At least one confirmed mandatory conformance failure, below-threshold measured metric, mock decorator, result-gaming finding, or unresolved confirmed regression. Remaining incomplete checks must also be disclosed. |
| INCOMPLETE | No confirmed failure establishes FAIL, but required tests, measurement, candidate identity, inspection coverage, or prerequisites remain unresolved/unperformed. |
| PASS | All selected mandatory criteria and applicable integrity checks are satisfied with valid candidate-bound evidence; both floors and stricter applicable policies pass; no required work or confirmed defect remains unresolved. |

Failure takes precedence over incompleteness. Passing percentages cannot waive a failed mandatory acceptance scenario or an integrity finding. Unknown or missing evidence is not a measured failure percentage, but it prevents PASS. Advisory suggestions outside the agreed requirements do not become mandatory repair scope.

The verdict is an evidence-backed QA recommendation. Protected framework acceptance, human release decisions, installation, deployment, and publication remain separate. Do not emit an invented authority receipt or call a Python grading result an authorized phase transition.

## Apply the decision to raw records

Before execution, declare eligible source inventory/exclusions and the unique required unit-case inventory for each platform. Preserve the plan's aggregate policy; identify cross-platform executions distinctly, and aggregate compatible line counts without treating a line executed on one platform as executed on another. Do not average rounded percentages or mix different candidate identities. If compatible overall evidence cannot be established, report that measurement unavailable. A later justified scope correction must be documented against requirements; never silently reduce the denominator to hide failures.

For every platform and overall scope, report integer numerator/denominator, the exact ratio and an unrounded decision. Apply thresholds by comparing the counts at full precision. A display-rounded value cannot qualify a result. For example, 9,499 of 10,000 eligible lines or required unit cases is 94.99% and fails independently of the other metric. Missing measurement has no estimated ratio. Required unit skips/errors/blocked/unexecuted cases remain nonpassing cases in the denominator; retries are attempts of the same case, never extra cases or erased evidence. Missing inventory completeness prevents PASS even if the observed suite passed.

Keep acceptance-criterion coverage, integrity inspection coverage and product metrics separate. Confirmed FAIL has priority while remaining gaps are still listed. An unresolved dynamic decorator investigation with no confirmed failure yields INCOMPLETE, not a clean inspection. A measured 99% cannot waive even one failed mandatory acceptance criterion. Use [the report template](../assets/qa-report-template.md) and route the result through [the user handoff](reporting-handoff.md).

