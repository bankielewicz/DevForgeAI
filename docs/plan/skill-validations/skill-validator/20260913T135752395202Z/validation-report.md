# skill-validator compatibility assessment

Outcome: **FAIL**. Exact package digest: `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`. This is validator self-assessment with independent differential CLI fixtures and a bounded independent static review.

229 updated-validator regression tests pass. Fourteen shared schemas match. All 13 public-interface differential cases are retained in inputs; the builder agrees with its independently defined expected outcomes. The validator disagrees in eight cases, grouped into five findings. Valid full-set and actual prior partial-set/single-skill handoffs are accepted.

| Finding | Evidence-backed gap |
| --- | --- |
| F-af18464dbd66 | Changed-equivalent PROPOSED is rejected while false NO_CHANGE and a nonvariant review are accepted. |
| F-d4737aa0c58e | The reader rejects an ordinary core whose full explicit requirement table is in SKILL.md because references/adaptive-contract.md is absent. |
| F-c46ff9dd2c0e | The same valid fenced parent inventory is accepted with LF and rejected with CRLF. Raw decode preserves CRLF and the closing-fence expression excludes CR. |
| F-74e5f1f773e3 | Intake accepts self-consistent delivered descriptors with the wrong selected role or parent digest; builder rejects both. |
| F-556ad77ff0f1 | Descriptor lists R3 but its contract has no R3 disposition; validator records accepts it and builder rejects it. |

Cold validator trial: Timed out at 120 seconds. Partial agent message independently identified expertise versus project_variant mismatch; no completed final report. Native implicit discovery remains NOT_RUN. Product producer-to-consumer execution and prior builder convention/author_set/update cold timeouts remain distinct; successful intake does not close them.

The validator package text observer emitted INCOMPLETE because it leaves fixture/placeholder candidate adjudication to the assessor. Manual review treats its one fullwidth-p character in a negative parser fixture as legitimate. Resource dynamic-use coverage remains NOT_RUN. Exact counts are retained; tokens were not guessed.

The initial differential fixture round had a harness manifest-sort error (Windows path ordering instead of ASCII row paths). It is preserved; round2 uses new fixture roots and correct sorted manifests. No package fix or test result replacement occurred.

Readback: UNCHANGED. Both specifications remain at selected hashes. Live OpenAI standards were not refreshed; this compatibility conclusion uses the pinned local project contracts. No installation, adoption, repair, operational binding change or Rust qualification.

See the coordinator compatibility-report.md, revision-spec.md, exact command-log.md and checks.jsonl for evidence and proposed next work.
