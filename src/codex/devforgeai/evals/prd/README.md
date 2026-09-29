# PRD evaluations for Codex

This suite is a mechanical port of the current Claude PRD suite: **20 cases**, **3
repetitions**, **plugin and no-plugin arms**, **120 trials**, plus all **23 mandatory
SPEC-002 VER obligations** and explicit manual/supplemental branches. Native behavioral
qualification is NOT_RUN. Static schema checks and discovery are separate evidence.

`../../tests/make_prd_evals.py` is the generator. From the repository root:

```bash
python3 -B src/codex/devforgeai/tests/make_prd_evals.py --check
```

Omit `--check` only when intentionally regenerating from changed source. Keep prior
evidence and bind a new candidate/plan; never rewrite a frozen campaign. Original
prompts, fixtures and graders remain under `src/claude/DevForgeAI/evals/prd`.
`provider-mapping.json` binds each original and adapted file by SHA-256.

## Mechanical adaptations

- Natural-language task bodies and all fixture scaffolds remain byte-identical.
- Remove Claude `allowed_tools` runner metadata from prompt frontmatter. This grants
  no Codex permissions; the native runner must set its actual tool/sandbox policy.
- Map Claude Skill-call graders to `codex_skill_read`: a successful native read of
  the exact loaded PRD `SKILL.md`, bound to the selected catalog entry. Retain min/max
  and arm semantics; presence in the catalog alone is not activation. Resolve relative
  read paths against the event cwd and do not credit failed/ambiguous command reads.
- Translate slash-command handoff assertions to `$devforgeai:...`, escaping the dollar
  only in regex bodies. Keep handoff placement, ID-only argument and no-work rules.
- Change `claude-code` to `codex` only in the two new-record provenance graders. Never
  rewrite historical fixture authorship. Non-empty strings are insufficient evidence
  of current identity; supplemental provenance assessment must verify actual identity.

The custom `codex_skill_read` grader is an adapter contract, not a built-in Codex or
Claude grader. No turnkey PRD native runner is shipped by this import. Reusing another
skill's runner requires a reviewed PRD adapter; do not run Claude evaluations as Codex
qualification. Regex and semantic grader meanings and the 0.8 threshold are unchanged.

## Execution and acceptance

The immutable [evaluation plan](../../prd-import-evidence/evaluation-plan.json) maps
every BEH/ERR/QR/VER item and contains the complete trial denominator. Freeze the exact
native executable/version, runner, graders, prompts, fixture bytes and schedule before
launch. Preserve raw protocol/stdout/stderr, catalog, final responses, before/after
files and candidate hashes. Independently assess semantic results against sealed artifacts.

Use isolated consuming projects and a runtime-only package containing the actual four
skills for the shipped handoff branch. Baselines get no plugin, skill hints or answers.
Do not expose evaluator files or inject model/session identity that production cannot
obtain. Include implicit activation and unrelated-request non-activation. No installation
or marketplace changes are required for disposable evaluation.

Resolve the SPEC-002 failure-lifecycle/attempt ambiguity before qualifying those manual
branches. Preserve every failure, blocked case and NOT_RUN result. No case averaging or
successful helper command establishes full PRD, combined-package or owner acceptance.
