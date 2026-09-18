---
id: DEVFORGEAI-SKILL-BUILDER-REVIEW-20260916
target: codex-cli
status: observation
recorded: "2026-09-16"
---

# skill-builder review findings

Read-only review of `src/agents/skills/skill-builder/` against its operational copy, its three governing specifications, and the assessor package that owns its evaluation. No package file was created, edited or removed. Frontmatter deliberately omits `skill_name`: this is an observation record, not a build input for `build_evidence.py resolve-spec` name lookup.

## Method

Commands actually run on this host (Windows 11, Git Bash, Python 3.10.11):

- SHA-256 of every tracked artifact recompared against `package-manifest.json`, for both copies.
- `diff -rq` between `src/agents/skills/skill-builder` and `.agents/skills/skill-builder`.
- Per-file SHA-256 comparison of the delta set against `src/agents/skills/skill-validator`.
- `--help` on all seven bundled scripts, to establish the real CLI surface.
- One bounded evaluation probe (F8), output written outside both roots.

## F1 — Package integrity is clean

`package-manifest.json` tracks 46 artifacts. All 46 exist, all 46 digests match raw bytes, and nothing on disk is untracked (47 files on disk = 46 + the manifest itself). Same result for the operational copy. No drift, no missing artifact, no stale digest.

## F2 — The `src` / `.agents` delta is exactly the evaluation harness

`diff -rq` reports no differing file. The two copies differ only by files present in `.agents` and absent from `src`:

```
evals/                          (15 files, incl. fixtures/portable/)
tests/                          (7 files)
scripts/graders.py
scripts/run_evaluation.py
references/evaluation.md
references/evaluator-contracts.md
```

26 files. Every artifact the two copies share is byte-identical.

## F3 — Those files are copies of the validator's, not builder-specific work

Compared against `src/agents/skills/skill-validator/`:

| File | Result |
| --- | --- |
| `scripts/run_evaluation.py` | byte-identical (`f538b80a4119…`, 11 106 bytes) |
| `scripts/graders.py` | byte-identical (`d21e43c151c4…`, 55 913 bytes) |
| `evals/builder-cases.jsonl`, `cases.jsonl`, `profiles.json`, `runtime.json` | byte-identical |
| `evals/*.schema.json` (3) | byte-identical |
| all 7 `tests/*.py` | byte-identical |
| `evals/build-manifest.json` | differs (legitimately per-package) |
| `references/evaluation.md` | differs — older text |
| `references/evaluator-contracts.md` | differs — older text |

The delta is also a strict *subset* of the validator's harness: `evals/README.md` and `evals/validator-cases.jsonl` are present in the validator and absent from the builder. A pre-migration snapshot looks like a subset; a deliberately builder-owned harness would not.

The builder's `references/evaluation.md` is the superseded version: titled "Required terminal evaluation", it resolves its commands against `<builder>` and instructs running the harness for "maintenance of the builder". The validator's same-named file is titled "Validator-owned deterministic assessment" and states **"Keep this harness in validator."**

## F4 — The operational copy's own manifest does not know about its harness

`package-manifest.json` is byte-identical in both copies. It tracks the 46-artifact, no-harness shape. So in `.agents/skills/skill-builder` those 26 files are untracked by the package manifest — they are covered only by `evals/build-manifest.json`, which the residual harness brought with it.

The timestamps rule out staleness as the explanation. Both copies of `package-manifest.json` carry mtime `2026-09-15 08:59:59.359769600 -0400`, identical to the nanosecond. The harness files they omit date from `2026-09-11 23:59` through `2026-09-12 11:35`; `SKILL.md` dates from `2026-09-14 17:14`. The manifest was therefore written three days *after* the harness already existed in `.agents`, and excludes it anyway.

The package manifest shipped with the operational copy describes the `src` shape, and was written while the harness was sitting next to it. That is the operational copy's own evidence that `src` is current and `.agents` is behind, not the reverse.

## F5 — The specification chain assigns evaluation to the validator

Three specs govern this package. They disagree, and they say which one wins.

- `claude-to-codex-skill-import-spec.md` (recorded 2026-09-11): "The authorized deliverable is the development skill `skill-builder` and its required evaluation artifacts." This is the sentence `CLAUDE.md` relies on.
- `skill-builder-authoring-enhancement-spec.md` (2026-09-12) §1: "Make skill-builder an **authoring-only workflow**; skill-validator owns both validation and testing."
- `skill-builder-adaptive-enhancement-spec.md` (2026-09-12) §1: "**Where older builder documents assign testing to builder, the current authoring-only contract governs this enhancement.**" §1.1: "Validator owns skill-quality validation, testing, and set integration assessment."

The 2026-09-12 pair supersedes the 2026-09-11 sentence, in the 2026-09-12 spec's own words.

## F6 — The validator states the migration already happened

`src/agents/skills/skill-validator/evals/README.md`:

> "The migrated profiles.json, cases, portable fixtures, scripts/run_evaluation.py, graders.py and regression tests retain legacy import/specification/regeneration/adoption expectations. […] All testing belongs here; builder contains no quality campaign."

The validator holds `builder-cases.jsonl` and the `builder-v2` profile (`PROFILES` in `run_evaluation.py`, all five graders). The campaign for skill-builder exists and is validator-owned.

## F7 — Absent `builder-v2` fixture directories are not a defect

`builder-cases.jsonl` references `trace/`, `revision/` and `routing/` paths that exist in neither package's `evals/fixtures/`. This is by design: `run_evaluation.py` resolves case `params` against `--candidate-root`, not against the package. Those fixtures appear as supplied per-run inputs under `docs/plan/skill-authoring-enhancement/20260913T021452Z/checks-001/commands/*/input-*/`. Recorded here so it is not re-reported as a gap.

## F8 — Harness probe: PASS

```
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/run_evaluation.py \
  --package-root src/agents/skills/skill-validator \
  --candidate-root src/agents/skills/skill-validator \
  --cases src/agents/skills/skill-validator/evals/cases.jsonl \
  --output <new-file-outside-both-roots> \
  --run-id review-probe-001 --profile legacy-import-v1
```

Output retained in this directory as [`review-probe-001.jsonl`](review-probe-001.jsonl) (2 records, SHA-256 `c63a8b33dde99199…`). It was written to a session scratchpad outside both roots as the runner requires, then copied here for preservation.

Exit 0. `{"records": 2, "exit_code": 0, "authority": "NONE"}`. Both cases `"status": "PASS"`, `"expectation_met": true`, on Python 3.10.11 / Windows-10-10.0.26200-SP0. The runner self-labels its authority as NONE, consistent with AGENTS.md: Python produces evidence only.

This probe exercised the validator package against itself. It is **not** an assessment of skill-builder. `builder-v2` was not run.

## Assessment

`src/agents/skills/skill-builder` is internally complete and consistent as an authoring-only skill: manifest clean, CLI surface real, routing coherent, separation of duties held throughout `SKILL.md` and every reference.

The evidence points the opposite way from `CLAUDE.md`'s "incomplete build" framing. `CLAUDE.md` reads the `src` copy as missing required artifacts; F3–F6 indicate `src` is the post-migration shape and the `.agents` harness is pre-migration residue, carried by an operational copy installed before the migration and not refreshed since. `CLAUDE.md` itself flags this as "a reported observation, not an acceptance decision" and asks for maintainer confirmation — this review supplies the evidence for that decision and does not make it.

## Open question — maintainer decision required

**OQ-1. Is the `.agents/skills/skill-builder` evaluation harness residue to be removed, or a deliverable to be added to `src`?**

- Evidence for *residue*: F3 (byte-identical validator copies), F4 (operational package manifest excludes them), F5 (2026-09-12 specs supersede), F6 ("Keep this harness in validator"; "builder contains no quality campaign").
- Evidence for *deliverable*: the 2026-09-11 import spec sentence quoted in F5, plus AGENTS.md's requirement that a skill build carry bound evaluation artifacts — if that requirement means *inside the built package* rather than *owned by the assessor*.

Decision owner: maintainer. Blocked on it: whether `CLAUDE.md`'s "Package shapes differ" section needs correcting, and whether `dev` (no eval artifacts at all) is a third instance of the same question or a genuinely separate gap.

Until OQ-1 resolves, no file under `.agents/` should be added or removed — AGENTS.md requires explicit authorization for that path either way.

**Evaluation status for skill-builder: NOT_PERFORMED. Testing status: NOT_RUN.** No campaign bound to the current `src` bytes was executed in this review.
