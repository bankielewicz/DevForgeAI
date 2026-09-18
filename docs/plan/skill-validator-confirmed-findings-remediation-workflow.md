# Skill-validator confirmed-findings remediation workflow

## 1. Select the repair scope and establish identity

Repair QA-01 through QA-04 in the development skill-validator package according to [the focused remediation specification](https://github.com/bankielewicz/DevForgeAI/blob/87fd32de0b35793f4891ec9139d50764bdddd568/docs/plan/skill-validations/skill-validator/20260913T201813155594Z/revision-spec.md).

- Proposal SHA-256: `832de4a0d2512f9f50481aeb822645c3830bfd005da954a0a10070dc69b92c25`.
- Expected pre-edit target: 75 files; package SHA-256 `d51703237abb4d015fbed30f8f03ef93040603a4ea0ec57a623db61e3c71f4b1`.
- Verify both governing specification hashes and current package bytes before dependent edits.
- Preserve original and independent reproducers from assessment `20260913T201813155594Z`.

Read applicable instructions. Verify package inventory using the specified hashing procedure. Preserve changed inputs; do not reset them. Inspect known provenance and use the supported maintenance basis. An exact observed scoped-edit capture is not generated/adopted history; corrupt known history must not be treated as absent.

Create separate UTC implementation and QA evidence runs. Use Windows-native tools on the selected C: checkout, with temporary storage inside each run. No operational installation, companion changes, WSL relocation, dependency installation, or historical-evidence edits.

## 2. Implement through skill-creator: red -> green -> refactor

Maintenance owns implementation and TDD. Independent quality assessment remains skill-validator's responsibility.

1. QA-01: reject repeated check artifacts across member/integration roles and copied execution identities. Normalize Windows path-case aliases for identity comparison; preserve distinct checks sharing citations or evidence bytes.
2. QA-02: reconcile integration coverage with immutable selected handoffs. Reject unjustified required N/A and missing observations. Preserve FAIL precedence, unknown/unperformed counts, optional absence, and valid subset omissions.
3. QA-04: terminate fences only with the correct marker, sufficient length, permitted indentation, and space/tab-only tail. Preserve literal examples and real links following the closer.
4. QA-03: recognize NFKC-changing characters in literal JSON/JSONL schema_version values, including multiline layouts. Emit precisely located unresolved candidates; do not modify source, leak neighboring secrets, or blanket-fail Unicode.

For each correction, execute new focused tests before production edits and retain actual requirement failures. Setup errors are not red evidence. Implement the minimum change, rerun positive/negative controls, then refactor only where useful and rerun affected tests.

Concentrate production changes in scripts/adaptive_observe.py and scripts/text_resources.py, with focused tests and required evaluation metadata. Preserve public CLI arguments, exit meanings, closed schemas, legacy behavior, and ordinary-skill applicability.

Refresh evals/build-manifest.json from actual package bytes, preserving schema, grader/profile definitions, and complete artifact membership. Recalculate artifact digests; the manifest does not list itself. Do not weaken runner binding checks.

## 3. Fresh skill-validator QA

Use fresh retained expectations and independent assessment context; a helper assessing itself remains self-review. Do not execute old harnesses in place: their run paths are fixed. Use new wrappers and disposable fixtures, retain original expectations, and document necessary path/reference rebinding against the delivered target digest.

Required checks:

- Four original reproducers and all 33 independent probes.
- Additional FV-001 through FV-004 acceptance cases.
- Complete regression discovery: `python -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -v`.
- Installed quick_validate.py on exact captured delivery.
- Actual legacy/new record interfaces, required evaluation binding and applicable compatibility profiles.

Compare output contents, locations, counts, applicability, and effects, not only exit status. F08 must report only the real line-5 link, excluding the line-3 literal example. Preserve exact commands, tool identity, stdout/stderr, timing, timeout/termination, input digests and before/after effects. Default attempts to 120 seconds; retain failures and allocate fresh linked retries.

Declare all first-party executable support scripts as the package line-coverage denominator before measurement; report branch coverage separately. Keep the repository's 95% coverage/pass-rate requirements without rounding, hidden source exclusions, or pooling repeated executions.

## 4. Delivery and closure

Deliver implementation report, exact changed-file inventory and package digest, evaluation manifest, red/green/refactor evidence, independent QA, stable-finding resolution map, final readbacks and remaining gaps.

A finding is resolved only when its original and independent reproductions and required controls pass against delivered bytes. Report repair success separately from overall package acceptance. Missing verification remains INCOMPLETE and demonstrated required failures remain FAIL; percentages cannot waive mandatory failures.

Native activation/resume, broader lifecycle integration, tokenizer setup, installation and Rust qualification remain separate. Closing these four findings does not close those historical gaps.
