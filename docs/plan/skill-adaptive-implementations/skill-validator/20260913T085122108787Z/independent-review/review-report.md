# Independent forward review of adaptive validator candidate

The inspected candidate has four reproduced defects: two unsupported missing-resource findings and two accepted invalid raw-helper records. This is an independent subagent review of the maintenance candidate, separate from the parent's validator self-review. It is a bounded terminal/helper review, not native CLI activation, operational binding qualification, or acceptance of all VA/VAT requirements.

## Grounding and retained evidence

The installed skill-creator instructions and validator entrypoint were read. Review expectations derive from validator specification sections 3.2, 4.2, 6 and 7 and the read-only builder shared contract section 5.1. Live specification hashes match the user's frozen hashes:

- Validator: `f08a5f745235e969c8186731c187bdc5150d8f92cc8d140d0deb6812e7ecaf42`
- Builder: `8fa6fae0625c5edd41cf8bca539a07e9d5fb1f1b90998feaf0be48814fa40a59`

`expectations.json` was written before candidate execution. `candidate-hashes.json` records all validator script bytes at review start. Each probe retains actual command arguments, exit code, stdout/stderr and parsed observation under `results/<IR-id>/`. Probe source and fixtures are retained. No source package, specification, operational copy, builder package or previous evidence was edited by this reviewer. All reviewer writes are under this independent-review directory.

## Supported findings

1. **F-IR01 / IR-02 / VAT-08 / VA-005 / AV-R01:** `text_resources.py:132` parses Markdown link-like text inside an inline code span as an actual link. The ordinary prose `Document a Markdown link using the literal syntax \`[Example](absent-example.md)\`.` contains no active Markdown resource consumer. The helper returns exit 1, MISMATCH, and AV-R01 FAIL for `absent-example.md`. This is an unsupported defect finding on a quoted syntax example. Resolve Markdown inline-code context before treating a target as a consumer, or leave ambiguous syntax unresolved.

2. **F-IR02 / IR-03 / VAT-08 / VA-005 / AV-R01:** `text_resources.py:132` stops the inline destination at the first closing parenthesis. The existing file `references/guide(v1).md` is linked with `[Guide](references/guide(v1).md)`. The helper instead checks nonexistent `references/guide(v1`, returns exit 1/MISMATCH and required AV-R01 FAIL. Balanced-parentheses paths must resolve correctly or be explicitly unsupported, rather than falsely reported absent.

3. **F-IR03 / IR-08 / VAT-24 / VA-014 / AV-E01:** `adaptive_observe.py:190` accepts a raw `adaptive-check-observation-v1` with `command: records`, `status: OBSERVED`, a required FAIL check and a nonempty `observations.errors` array. The enclosing records invocation returns exit 0/OBSERVED with no errors and says supported record reductions were verified. The persisted helper's declared status contradicts its own required checks and command observations. The reader needs a command-specific status consistency check; checking shape alone does not verify this integrity.

4. **F-IR04 / IR-09 / VAT-24 / VA-014 / AV-E01 and AV-U01:** the same raw-helper dispatch accepts a package Unicode candidate with `start_byte: 10`, `end_byte: 1`, `disposition: defect`, an empty resource inventory, and OBSERVED status. This violates the strict interval and section 7's required unresolved deterministic disposition. The records helper returns exit 0/OBSERVED and no errors. The finalized supplemental reader already checks part of the interval semantics; raw helper observations need their specified semantic integrity constraints too, without treating a helper candidate as final adjudication.

Reproduction for each finding uses the exact command in its `results/IR-XX/receipt.json`. For example, from the project root:

```powershell
python -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py package --source docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/fixtures/IR-02/example-skill
python -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py package --source docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/fixtures/IR-03/example-skill
python -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py records --run-root docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/fixtures/IR-08/run
python -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py records --run-root docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/fixtures/IR-09/run
```

## Results and preserved harness correction

The 15 independently specified probes yielded 11 expected outcomes after correcting one review-fixture serialization error. The candidate false-positive count is 2 (IR-02, IR-03); missed seeded-integrity-defect count is 2 (IR-08, IR-09). These results are not an aggregate acceptance score.

Known-good supported observations: IR-01 ordinary inline/reference links, duplicate-heading anchor and image resolve; IR-05 preserves multilingual text, emits an unresolved legitimate U+FE0F candidate at bytes 162..165, line 6, column 41, and reports null tokens without claiming tokenizer execution; IR-07 reads an honest helper record; IR-10 ignores a nested malformed fixture `findings.json`; IR-11 validates a standalone A/B set in order A,B. Seeded defects correctly rejected: IR-04 absent resource; IR-06 malformed declared UTF-8; IR-12 duplicate member; IR-13 missing selected dependency; IR-14 unknown field; IR-15 stale package digest.

The first IR-11 fixture incorrectly calculated package digests with `sort_keys=True`. The existing manifest contract preserves the `path,bytes,sha256` field order. Its failed output and original fixture remain under `results/IR-11` and `fixtures/IR-11`; it is a harness error, not a candidate finding. `retry_intake.py` creates fresh corrected IR-11 through IR-15 inputs and results under `attempt-02`, with a retained explanation. It does not edit the original fixture or repair a producer artifact. The corrected IR-11 returns 0/OBSERVED; corrected IR-12 through IR-15 return 1/MISMATCH.

Executed harness commands, both exit 0:

```powershell
python -B -X utf8 docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/run_review.py
python -B -X utf8 docs/plan/skill-adaptive-implementations/skill-validator/20260913T085122108787Z/independent-review/retry_intake.py
```

Both harnesses inspect the candidate through its public command surface and use argument vectors, a 120-second subprocess timeout and disposable fixture inputs. The review did not execute target-skill scripts. No native child model task or child process timeout scenario was attempted. Fixture creation and outputs are retained; this review did not capture native-process containment or native effects manifests and does not claim such coverage.

## Limits

This review covers selected deterministic text parsing, raw-helper record integrity and standalone-set intake behavior on Windows/Python. Parent work on guidance/tests was still ongoing; findings apply to recorded candidate script hashes. Full regression, installed creator quick-validation, adaptive operational binding, full shared-builder record agreement, semantic paraphrase trials, native explicit behavior, implicit host activation, producer/consumer task integration, Linux execution and final package readback remain parent-owned or NOT_RUN here. No repair, install, Rust enforcement or certification claim is made.
