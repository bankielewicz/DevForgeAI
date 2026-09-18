# Earlier adoption trial — retained, superseded for final verification

This directory preserves actual attempts against TEMP project
skill-builder-adoption-trial-kto8d8pr. It is not the final current-manifest trial.
The adjacent directory with the -final suffix contains the fresh complete chain.

- Initial adoption helper exit 2: `ValueError: observed rows must be sorted`.
  The worker had used Windows Path ordering rather than explicit normalized-string
  ordering. The attempt remains under retained/adopt-01-helper-error/; its raw
  command output remains commands/adoption-plan-01.json. No target bytes changed.
- Adoption was recaptured in a new adopt-02 run with sorted rows. Helper/grader
  succeeded and external pointer publication/readback succeeded.
- First candidate passed structural, 15 behavior cases, and spec-v1 evaluation.
  An injected user comment caused actual exit 1 CONFLICT with unchanged target.
  Separate controller direction authorized retaining the edit and restoring only
  the script to exact adopted bytes. Retry used the same adopted origin.
- First delivery and generated publication passed revision-spec-v2 under manifest
  fcef77def723a1fc2f2fc5e49285830eb9f79cc6cf832beb7861a17522c965cc.
- Self-audit found an informational authorization resolved_path defect: combined
  first-revision and resolution bytes were correctly retained and digest-bound,
  but their original locator incorrectly named the first authorization file. The
  worker disclosed this; no historical contract, provenance or pointer was rewritten.
- An optional current-manifest re-evaluation of that old-provenance first revision
  returned one FAIL, `builder manifest digest differs from running evaluator`.
  package_links and revision_consistency_v2 remained PASS. This is retained in
  revision-02-resolved-latest-60522daa-results.jsonl. It is not relabeled successful.
- The separately authorized later revision selected the successful first N and
  passed 16 fresh behavior cases plus delivered/published revision-spec-v2 on
  manifest 60522daaff9000367beacb7b5a6fb03cd90caeb93ac829bc13bba98c2d3b31a9.
  This later success does not repair the earlier locator defect.

The controller then requested an entirely new disposable chain with exact original
locators and current-manifest checks. It did not authorize re-adopting this already
governed target. All old project bytes, attempts, commands, outputs, edits and
evidence remain retained. No operational installation or Rust qualification occurred.
