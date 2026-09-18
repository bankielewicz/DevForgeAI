# Skill builder operational assessment

Assessment completed: **true**. Overall: **FAIL**. Readiness: **BLOCKED**; proposal review: **pending**. This is one assessment agent using the selected operational validator snapshot. It is not a native builder activation or an independently executed builder model workflow, and the validator is not assessing itself.

Target: `C:\Projects\DevForgeAI\docs\plan\skill-authoring-enhancement\20260913T021452Z\operational-assessment\skill-builder`. Package digest: `df5204eb3ff53db0ff71d222bfab552170ca36950905ad9b49ea3fcbc9b6bb32`. Rule-set digest: `b1949a2fb4e690e8ff347ae3d552177590fa4cacdfd13f725a644960187dd9a5`.

## Preserved origin and evidence

The selected enhancement specification matched SHA-256 `43054bf9b3f97d48d479aeed2fe7b119629e6e717f0a55e1835714182844cb14`. Current request treats it as approved despite its retained proposed frontmatter. The snapshot captured 28 files with no exclusions. Final source readback is **MATCH**; original target bytes were not edited. History is observed/unknown because no baseline evidence was selected. Source and rule inputs were rehashed.

See [origin](origin-record.json), [source manifest](source-manifest.json), [exact source](source/), [readback](inputs/readback-stdout.json), [sources](sources.json), [pinned rules](rule-set.json) and [input readback](input-readback.json). A live read-only Agent Skills format refresh is retained. OpenAI Build skills retrieval was reachable, but its Markdown transport failed; no current broad OpenAI compliance claim is made. The operational fallback was preserved separately; its historic source locators were not treated as freshly read sources.

## Dimensions and required coverage

| Dimension | Outcome | Evaluated/required | NOT_RUN |
|---|---|---|---|
| standards | PASS | 1/1 | 0 |
| workflow | FAIL | 2/2 | 0 |
| instructions | FAIL | 2/2 | 0 |
| behavior | FAIL | 10/14 | 4 |

Enforcement is a fifth descriptive dimension: no new hook/CLI/CI mechanism is proposed. Existing guidance and ordinary input parsing/readback safeguards remain appropriate. See [enforcement recommendations](enforcement-recommendations.md).

## Findings

1. **Major — malformed input leaves writes without authoring record.** `scripts/authoring.py:244-245` checks field presence but not all types. With `known_issues:null`, begin exits 0; publish writes the synthetic target SKILL.md and baseline, then line 410 raises TypeError. It exits 2 with BLOCKED, no authoring-record.json and no publication-failure.json. Before/candidate/baseline/delivered evidence still exists. Fix pre-write parsing and retained post-write failure reporting. Finding `F-f0530cf3fcd3c232b753ab5684fa985f2f106828295172e93a8d70ec1fb21224`; [case](trials/malformed-contract/result.json), [stderr](trials/malformed-contract/attempt-002.stderr.txt), [after effect manifest](trials/malformed-contract/attempt-002.after.json).

2. **Minor — valid 64-character identity rejected.** `scripts/authoring.py:252` uses `>= 64`; begin exits 2 on a valid existing identity. The initializer permits 64 and the current [Agent Skills name contract](https://agentskills.io/specification#name-field) permits 1–64 characters. Fix the inclusive boundary without renaming existing skills. Finding `F-e937af0918a0b6660b11c9f49d60032ecf560ead6da77080256499cbb7935402`; [case](trials/name-64/result.json), [stderr](trials/name-64/attempt-001.stderr.txt).

3. **Minor — import preservation still depends on a structural checker.** `references/conversion-rules.md:18` tells the host to condition preservation on a required checker and move compatibility into prose if rejected. This conflicts with the package's authoring-only entrypoint and preservation requirement; the [format supports compatibility](https://agentskills.io/specification#compatibility-field). This is an instruction finding, not an observed model deleting metadata. Finding `F-65f77a3bc98cfc63f162cd1cbc0ca313ae81fb531b6e5754e0cb86e6ceb70a72`; [exact source](source/references/conversion-rules.md), [contextual review](ceremonial-review.json).

Stable machine findings and digest-bound locators are in [findings.json](findings.json). All three remain proposed, not approved or executed changes.

## Trials, positive evidence and limitations

Ten disposable cases ran: **8 PASS, 2 FAIL**, with command-level stdout/stderr, exit codes, timestamps and before/after manifests retained. No timeouts or retries occurred. Passing cases cover creation in a path with spaces and a second untested edit; observed first edit and divergent conflict; rejection of outside-scope candidate changes; source drift; metadata/policy/dependency preservation; occupied initializer destination; explicit adoption followed by adopted-origin editing; referenced-input drift. Normal successful runs retain NOT_PERFORMED validation/testing and publish exact request references. A source-drift case returned PARTIAL with no applied paths because the external fixture changed; the captured effects make the distinction visible.

See [trial results](trials/results.json), individual pre-execution `trials/*/plan.json`, [harness](assessment_trials.py), [command log](command-log.md), [workflow map](workflow-map.json), [applicability](applicability.md) and [checks](checks.jsonl). Fixtures are synthetic; package and operational validator remained read-only. Test-created instruction files are not examples authored by the builder model.

Structural observation passed its limited metadata/link checks. The personal installed checker was outside the selected local-input scope and was not run. Manual inspection found routed resources and concrete terminal outcomes except the cited failure. No grader import, quality-test subprocess or automatic validator invocation was found in the active authoring path. This static observation is not a full runtime trace for all future model choices.

Native implicit activation, independent cold workflow execution, full legacy schema-1/schema-2 lineage rejection regressions, interleaved per-path failures, publication fault injection, link/junction fixtures, alternate OS and missing-dependency runs were **NOT_RUN**. No subagents were authorized, so description-based independent classification was not substituted. Companion validator changes, its stale-packet detection and test relocation are outside the selected-builder assessment. Neither helper success nor report integrity establishes framework acceptance, native execution, Rust qualification or installation.

The harness records fixture identities and predeclared expectations before the first behavioral command. Some branch-specific fixture details are generated by the retained case code and appear in command-before manifests. All shell commands use 120-second subprocess timeouts. The wrapper command initially yielded a live session and completed normally. Early read commands are recorded in the log with their coverage; terminal transcript remains their exact raw output source.

## Proposed next action

[revision-spec.md](revision-spec.md) is the full proposed builder contract and mandatory correction scope. [handoff.json](handoff.json) binds it to the observed target. Review the three proposed findings and select the exact authorized development paths plus a valid baseline/custody prerequisite. The operational validator requires this prerequisite for an executable repair handoff; no verified baseline was supplied. Pending review and that missing execution prerequisite remain separate. No repair, builder invocation or installation was performed.
