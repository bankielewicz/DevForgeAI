# Semantic and test-integrity review

This is validator self-review. A cold subagent received only the skill, synthetic task, specification and permitted effects; no expected answer or historical finding was supplied.

## Structure, text and resources

The selected entrypoint is 12,181 bytes, 12,181 Unicode characters and 75 physical lines. The manifest binds its original directory name skill-validator; the temporary name source is not an identity defect. The 61 parsed Markdown resource edges resolve. The only Unicode candidate is fullwidth p in tests/test_adaptive.py:102, an intentional confusable-command fixture whose assertions check detection and redaction. Placeholder candidates in references/set-trials.md:81 and references/text-resource-checks.md:18 describe positive/negative fixtures, not unfinished instructions. No optional agents/openai.yaml is present or required. No token budget was selected; no tokenizer was run.

Referenced instructions supply actual input, output, continuation and failure branches. scripts modules are consumed by entrypoint commands or local imports; schemas/assets and evals have reference/runner consumers; tests are intentionally reachable through unittest discovery documented by evals/README.md. Package graph reachability alone does not establish executable imports; cited source inspection and executed regression evidence supply that context. Remote guidance and renderer-specific behavior are not comprehensively crawled.

## Contextual wording

SKILL.md requires fresh capture and readback: useful actionable instructions preserving evidence, not ceremonial scoring. Its statement that Python observations are not framework acceptance accurately limits authority. references/reliable-evaluation.md separates timeouts from product defects and bounds retries; this provides concrete recovery behavior. These safeguards remain in the proposal. Long paragraphs and cross-references can cost context, but no universal length failure or destructive rewrite is justified by these measurements. Native user-correction and adversarial prompt handling were not exercised.

## Test integrity and confirmed integration mismatch

331 standalone/regression cases pass. Two modules initially failed to import without their documented AUTHORING_BUILDER_ROOT dependency. Their 71 real cases were then executed once with captured current development builder bytes; 68 pass, two fail, one errors. The initial loader errors remain in the first log; they are not counted as extra test cases. Total: 399/402, no skipped methods.

Three test assumptions are incompatible with that captured dependency:

- tests/test_authoring.py:139 requires result['issues']. Current builder recheck_stage failure returns a nonempty error, BLOCKED and zero applied paths before entering its legacy issues-return branch. The test errors before its preservation assertions.
- tests/test_authoring_safeguards.py:200 writes into a target that the create fixture has not created. The current before_write callback occurs before target.mkdir, so the callback cannot install a competing file. BLOCKED does not prove a preservation defect; the intended competing-write scenario was not reached.
- tests/test_authoring_safeguards.py:264-273 makes files(target) fail after interruption but does not create the target. Recovery tests target.exists() before calling files, so the planned read failure is not exercised.

This establishes broken integration test expectations/fixtures against the selected dependency, not a product mutation defect or permission to repair builder. No failing test was weakened or rerun. Mock usage reviewed includes bounded limit overrides, simulated links and targeted filesystem fault injection; those do not prove actual OS races or Windows symlink capability. The test suite contains substantive negative assertions, not only metadata checks.

## Coverage and evaluator limitations

Measured line coverage is 3424/3802 (90.05786428195686%); branch coverage is 1593/1908 (83.49056603773585%). No first-party lines were excluded. The denominator includes all 14 captured scripts, including migrated custody/build fixture-support modules. The measurement configuration instruments the captured source path. Tests that copy the evaluator to disposable locations can execute identical code outside that configured source path; those copied-path executions are not credited here. Consequently this measurement does not establish a precise package-wide deficit, but it does not prove the required 95% floor. Correct byte-bound copied-path instrumentation before deciding what extra tests are needed; never discard source from the denominator.

The first coverage aggregation with a changed data basename found no data. Its logs are preserved. Corrected aggregation of the existing chunks succeeded; no tests were repeated for that correction.

Independent CLI probes: seven of eight match the frozen expected exit code. The quoted-inline-link probe incorrectly expected exit 2 although its clean metadata, exact directory identity and absence of Unicode justify exit 0. Its useful no-false-missing-link predicate holds, but the frozen case remains an evaluator ERROR, not a retroactive PASS or target defect. Its plan/results are unchanged.

Description-only routing passed 6/6. The cold workflow detected the seeded credit defect and delivered useful artifacts; its exact sample-specific obligation was not exercised. Native CLI activation, adversarial host input, user correction and other platforms remain NOT_RUN. No comparison, installation or compiled-Rust acceptance was performed.
