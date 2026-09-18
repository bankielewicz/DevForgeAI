# Validator-only QA assessment

**FAIL — the enhanced skill-validator does not meet its governing acceptance criteria.** Four independently reproduced required failures remain. The review reached reporting; this does not mean every native or capability-dependent case completed.

## Confirmed findings first

- **QA-01: Duplicate member/integration evidence inflates required coverage.** A member check file is reused as integration_checks. All 29 A rows are counted twice; the helper accepts 87/87 instead of rejecting the shared artifact. Location: `scripts/adaptive_observe.py:112`. Reproducer/evidence: [commands/R06](commands/R06/stdout.txt). Stable ID: `F-0b5c4676e917c304c39f8339e6536ba54a08ec05f7d410ab6c4c83a12791ddba`.
- **QA-02: Required handoff can disappear through NOT_APPLICABLE.** A full set declares a required A-to-B handoff, but its only integration row claims NOT_APPLICABLE. records accepts PASS at 58/58, omitting the required integration obligation. Location: `scripts/adaptive_observe.py:119`. Reproducer/evidence: [commands/R07](commands/R07/stdout.txt). Stable ID: `F-451f9ac54c52d553ee8d83d14dd69b0487d7a66ed6da8003b8eebe25af0ff720`.
- **QA-03: Exact protocol identifier escapes NFKC candidate scanning.** protocol.json contains schema_version with U+FF54 FULLWIDTH LATIN SMALL LETTER T in task-card-v1. The helper reports OBSERVED with no Unicode candidates. The exact protocol string differs, although normalization would change it. Location: `scripts/text_resources.py:84`. Reproducer/evidence: [commands/P08](commands/P08/stdout.txt). Stable ID: `F-423b36f0fa4378d0d426892377bea79335327a3b1507d05d7c5459de655252aa`.
- **QA-04: Valid fenced example produces a false missing-resource failure.** A backtick line with trailing nonspace text is treated as a closing fence. The literal link on the following code-content line is then reported as a missing local resource, producing MISMATCH for a valid example. Location: `scripts/text_resources.py:107`. Reproducer/evidence: [commands/P07](commands/P07/stdout.txt). Stable ID: `F-fb4a957d8ef5cf9a369515aa9a44ca736024f52c57fa25f06bdb25248953af48`.

All four are major required defects. Their full identity arrays, exact locators, expected/observed behavior, impact, preserved requirements and proposed corrections are in [stable-findings.json](stable-findings.json). Their modules were added by the enhancement relative to the verified 51-file baseline; no later target drift was observed. The fenced-code expectation is supported by [CommonMark 0.31.2 section 4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks): closing fences permit only trailing spaces/tabs; code content remains literal. This clarifies the already selected resource-parsing obligation rather than replacing the contract.

## Identity, authority and preservation

Target: `C:\Projects\DevForgeAI\src\agents\skills\skill-validator`. Current, reported delivered, retained delivered and loaded evaluator all have **75 permitted files**, **672,043 bytes**, package SHA-256 `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`. The loaded operational evaluator is `.agents/skills/skill-validator`; it is a separate location with identical bytes. Its helpers assessing this target are **self-review**, including legacy/new record integrity. Independent expectations and terminal harnesses are outside both packages; fresh child tasks alone are not treated as independent oracles.

Both selected specification hashes match exactly before and after assessment. The original 51-file baseline digest `77f0eec091cb41559074296ec8b0cd7dad76329ca6647b969f0e76b49cea51a4` and retained delivered snapshot were independently recalculated. The delivery adds 24 files, modifies SKILL.md and evals/build-manifest.json, removes none, and preserves all preexisting scripts/tests/schemas. No provenance was reconstructed or adoption inferred. [Identity/readback](selected-input-readback.json), [baseline compatibility](baseline-compatibility.json), [retained snapshots](retained-snapshot-verification.json).

The companion's current captured digest is `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2` (43 files). It differs from the implementation report's older companion identity but was unchanged throughout this assessment. This is a preexisting difference, not an observed concurrent edit or an attributed implementation-session mutation. Target, installed evaluator, companion and the bounded prior-evidence inventory match before/after. Whole operational homes and all historical evidence trees were not captured; no whole-tree preservation claim is made. No package, specification, operational copy, real binding, plugin, hook, CI, or Rust implementation was edited by this review.

## Executed evidence and limits

| Scope | Actual result |
| --- | --- |
| Exact requested unittest discovery | **229/229 pass**, no empty discovery or discrepancy; 50.278 seconds. Coverage repeat also 229/229, 70.834 seconds. Retries are not extra passing cases. |
| Installed skill-creator quick_validate.py on exact capture | Exit 0, limited structural check; installed checker identity retained. |
| Legacy structure helper | Exit 0, limited self-review. |
| New package helper on retained source | Exit 2 INCOMPLETE: original directory identity, placeholder and Unicode adjudication need caller review; raw stdout preserved unchanged. No helper output is counted twice. |
| Independent Windows terminal corpus | **36/40 match**, 1 false positive (P07), 3 missed required defects (P08/R06/R07). |
| Shared contract/lineage controls | **8/8 fixtures agree and match**, both current captured readers. Sixteen reader executions are eight paired cases. |
| Binding helper | **9/9 Windows and 9/9 WSL/Linux**, correct reasons, no emitted identity or helper writes. These are companion-template/helper evidence. |
| Native binding caller | MATCH writes exactly `sample`; missing binding creates no product output. Other reject reasons are not individually qualified as native caller behavior. |
| Semantic paraphrases | **18/18 match**, 10 seeded defects and 8 legitimate examples; **0 false positives, 0 misses**. Two independent agent presentations for VAT-07/10/21; same model family, no enforced independence claim. |
| Project conventions | Five fresh CLI focused reviews preserve Python/TDD, Rust implementation-first permission, service-local scope, docs-only constraints and unresolved equal-scope conflict. No language compiler/test execution is claimed. |
| Native task-card/receipt integration | Five scenarios satisfy actual contents/write sets: real v1 accepted unchanged, real v2 rejected unchanged, separate missing-verification rejection, required absence no receipt, optional absence exact reason. |
| Full validator/native discovery | Both time out at 120 seconds; partial events retained, tree termination exit 0. No reliable host selection signal, so implicit activation remains **NOT_RUN**. |
| Native resume | Unchanged selected inputs verified before resume; the fresh attempt also times out at 120 seconds. Full completion remains **INCOMPLETE**. |
| Tokenizers | Installed tiktoken 0.9.0; cl100k_base, r50k_base, p50k_base, o200k_base and gpt2 data unavailable locally. No download/estimated token conversion. Exact non-token counts and four budget/excerpt controls pass. |
| Source drift and records | Synthetic late edit detected as SOURCE_CHANGED. Prior legacy and adaptive records both exit 0 through current supported interfaces; their shape validity does not override new defects. |

The cold native host uses existing `gpt-6-astra` / high reasoning configuration, Codex CLI 0.154.0 and explicit workspace-write, no additional real-project writable roots or bypass flags. The initial native app-server access denial and initial WSL denial remain retained; separately approved fresh attempts use the same child policy. Prompt restrictions and before/after observations are not OS isolation certification. Host runtime session files are incidental CLI effects, not installed-skill edits. Exact argv, stdout/stderr, start/end, timeout and termination are in [command-log.md](command-log.md) and [command-log.json](command-log.json).

## Coverage and reduction

The declared required acceptance suite is **25 VAT cases**, counted once per complete case: **12 PASS, 5 FAIL, 8 INCOMPLETE**. Required-case pass rate is **48.00%**; partial, unavailable and failed cases are not passes. This does not meet the 95% minimum. This denominator is separate from the regression suite's 229/229 and the independent probe subcorpora; they must not be summed to average away a failed mandatory scenario.

The 29-row capability rule ledger has **23/29 evaluated**, **0 unknown applicability**, **0 N/A exclusions**. Unavailable required verification is represented as NOT_RUN, not unknown applicability or N/A. These AV rows assess the enhancement's required assessment capabilities; they do not require an adaptive descriptor or real binding on this ordinary tool. VA/AV/VAT are three views, not three added sets of executions. Full matrix: [coverage-matrix.md](coverage-matrix.md), with exact obligations and independent pre-execution expectations in [coverage-matrix.json](coverage-matrix.json).

Executed-line coverage of all nine first-party Python support scripts at the original target paths is **2322/3426 = 67.7758%**. Branches: **1038/1802 = 57.6027%**. Installed coverage.py 7.9.0 collected original-path subprocesses. No first-party source exclusions were used; altered temporary copies were not aliased to pristine paths. This is a measured bounded suite, below 95%, not complete campaign coverage or Rust framework coverage. The denominator was declared before execution. [Coverage data](coverage/coverage.json), [denominator](coverage/denominator-before-run.json).

## Separate conclusions and remaining work

- **Implementation conformity: FAIL.** QA-01 through QA-04 violate required behavior.
- **Deterministic regression: PASS for 229 preserved cases; independent deterministic corpus: FAIL.**
- **Semantic findings: supported for retained corpora.** No generalized model reliability or security-certification claim.
- **Native whole workflow/resume: INCOMPLETE; implicit activation: NOT_RUN.** Focused native tasks completed separately.
- **Shared readers and fixed synthetic handoffs: PASS in bounded cases. Full builder-authoring-to-validator lifecycle: NOT_RUN.** The request forbids automatic builder invocation; paired readers/fixtures do not substitute for that lifecycle.
- **Installation: NOT_PERFORMED. Rust qualification/acceptance: NOT_RUN.** The designated devforgeai directory was empty at inspection; no proposed command is presented as implemented.

Remaining work is to select and implement the four proposed fixes in a separate authorized maintenance task, preserve and rerun the unchanged reproducers, then perform fresh validator-only QA. Required verification still includes complete ordinary/origin workflows, resume completion, full adaptive relocation and caller rejection coverage, required-producer failure propagation and the separately authorized builder lifecycle. Positive exact-token counts require already available named encoding data. Numeric thresholds cannot waive any failed invariant.

The [revision specification](revision-spec.md) is a complete proposed amendment incorporating both frozen contracts, with requirements, cases, resources, effects, recovery and custody prerequisites. It has **not been applied**. Proposed findings are unselected; handoff is reviewable, while execution custody remains BLOCKED until a later current authorization and verified appropriate baseline/scoped-edit basis. This assessment grants no repair or installation authority.

Final citation review conservatively marks VAT-03 and VAT-25 INCOMPLETE: no whole selected-set trial with unrelated C installed, and no direct unsupported-certification request trial. The earlier draft and successful record checks remain retained. The target Unicode candidate at tests/test_adaptive.py:102 is a deliberate fullwidth-command test string, passed as data to the candidate scanner; it is legitimate fixture content, not a production command. New legacy and adaptive records are checked separately through supported interfaces; final results are in final-receipt.json.
