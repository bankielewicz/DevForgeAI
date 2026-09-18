---
id: DEVFORGEAI-SKILL-VALIDATOR-CLAUDE-CONVERSION-20260917
target: claude-code
status: observation
recorded: "2026-09-17"
---

# skill-validator — Codex to Claude Code conversion report

Complete source accounting for the conversion of `src/agents/skills/skill-validator` (89 files) into `src/claude/skills/skill-validator` (89 files).

Two linked authoring runs:

| Run | Operation | Result | Paths |
| --- | --- | --- | --- |
| `20260917T112416Z-claude-conversion` | `import` | **AUTHORED**, `PUBLISHED` | 89 applied |
| `20260917T115002Z-review-fixes` | `edit` (prior baseline `authored`) | **AUTHORED**, `PUBLISHED` | 4 applied |

- Inputs: the matching `...-inputs/` directory beside each run root
- Final package digest: `98580a1ad1318e21a0fb48911ef4ce819c214d039494938310a56f7b2f81ffe0`
- **Validation: NOT_PERFORMED - Testing: NOT_PERFORMED**

Run 002 exists because an independent review of the published run-001 bytes found a real defect. It is recorded in full under *Reviewer findings* below rather than folded silently into the run-001 narrative.

## The distinction that shaped this conversion

skill-validator is not an ordinary package to port, because it *assesses other packages*. Its Codex coupling splits into two categories that need opposite treatment, and conflating them produces a conversion that looks finished and is wrong:

**(a) The package's own host interface** — its frontmatter, its invocation syntax, its tool grants. Ordinary conversion.

**(b) The host semantics of the packages it inspects.** Here the question is not "what host am I running on" but "what host are my *targets* written for." A Claude-hosted validator inspects Claude Code packages, so the rules it applies change.

Category (b) is where a find-and-replace fails. `agents/openai.yaml` has no Claude analogue at all — both official sources state Claude Code reads no separate metadata file — so the optional-configuration check family could not be renamed onto an invented Claude path. It was migrated onto the optional frontmatter fields, which is where that surface actually lives here.

**The concrete defect that migration fixes:** the source's `metadata_checks` types table declared `allowed-tools: str`, because the Agent Skills specification defines only a space-separated string. Claude Code also accepts a YAML list, and all three Claude skills already in this repository — `advisor`, `dev`, `skill-builder` — use the list form. Carried forward unchanged, the converted validator would have failed its own siblings on a *required* check.

## File dispositions

89 source files in, 89 out: 66 preserved byte-identical, 22 rewritten, 1 omitted, 1 added.

| Source path | Disposition | Reason |
| --- | --- | --- |
| `SKILL.md` | rewrite | Claude Code frontmatter added (`name`, `description`, `allowed-tools`); "Codex development skill" → "Claude Code development skill"; new structural-boundary paragraph; routing added to the new frontmatter asset. |
| `assets/openai-yaml-guidance.md` | **omit** | Documents `agents/openai.yaml`, a file Claude Code never reads. `interface.icon_small`, `icon_large`, `brand_color` and `default_prompt` have no equivalent and are recorded here as unreproduced source metadata. `policy.allow_implicit_invocation: false` survives as `disable-model-invocation: true`. |
| `assets/claude-frontmatter-guidance.md` | **add** | Its replacement: the Claude Code field table with value domains, the recorded source divergences, invocation and discovery semantics, and the Codex-metadata mapping. Mirrors what the skill-builder conversion did with `references/claude-frontmatter.md`. |
| `assets/rules-snapshot.json` | rewrite | Revision `2026-09-17.1`. Sources re-pinned; see *Rule re-pinning* below. |
| `assets/enforcement-register-template.md` | rewrite | Enforcement destination `codex_hook` → `claude_hook`. |
| `assets/origin-spec-template.md`, `assets/revision-spec-template.md` | rewrite | `target: codex` → `target: claude-code`. |
| `scripts/skill_format.py` | rewrite | The core (b) change. See *Metadata profile* below. |
| `scripts/observe.py` | rewrite | Shares the field table from `skill_format` instead of duplicating it; emits advisory divergence rows; the `agents/openai.yaml` configuration block is replaced by a `foreign_host_configuration` NOT_RUN observation. |
| `scripts/text_resources.py` | rewrite | AV-F04 migrated from `agents/openai.yaml` to the optional frontmatter fields; known-field set shared; reachability roots reduced to `SKILL.md`, which is the only entrypoint Claude Code reads. |
| `scripts/adaptive_contracts.py` | rewrite | The installed-binding path rule is now host-neutral. See *Installation roots* below. |
| `references/rules.md` | rewrite | 5 replacements: "universal Codex requirement"; `.agents/skills` → a host discovery location such as `.claude/skills`; `codex_hook` → `claude_hook`; the source-compilation paragraph; the `agents/openai.yaml` optionality sentence. |
| `references/set-trials.md` | rewrite | 3 replacements: the native CLI trial section; the sandbox-flag caution; the discovery-trial fixture location, which becomes `.claude/skills/<name>` because that is the path the host actually scans. |
| `references/adaptive-validation.md` | rewrite | 3 replacements including the AV-F04 catalog row. |
| `references/trials.md` | rewrite | 2 replacements: the task runner and independent-reviewer paragraphs, now naming `Task` and stating what a subagent does and does not guarantee. |
| `references/handoff.md` | rewrite | 2 replacements: `target Codex` → `target claude-code`; `$skill-builder` → a statement that the builder is unreachable because `Skill` is absent from `allowed-tools`. |
| `references/reliable-evaluation.md` | rewrite | The `allowed-tools` string-only claim and the "Codex-compatible profile" label. |
| `references/text-resource-checks.md` | rewrite | Link retargeted to the new frontmatter asset. |
| `references/adaptive-shared-contracts.md` | rewrite | `InstalledBinding` path contract matched to the code change. |
| `tests/test_postmvp.py` | rewrite | `allowed-tools: [Read]` moved out of the rejected set; genuinely invalid values (`[1]`, `effort: ultra`, `shell: fish`, `disable-model-invocation: maybe`) put in its place; a new test asserts the full Claude optional-field set parses and that the list form is reported as a portability divergence. |
| `tests/test_postmvp_resource_quality.py` | rewrite | `{'allowed-tools': ['Read']}` moved out of the failure list; the three `agents/openai.yaml` tests became frontmatter tests; two new tests assert a foreign host's configuration file is reported unread rather than failed. |
| `tests/test_authoring.py` | rewrite | Two cases invoked `skill-builder/scripts/generate_openai_yaml.py`, which **does not exist in the Claude skill-builder** — it was dropped in that package's own conversion. They now assert metadata preservation through an ordinary frontmatter text edit, which is what focused metadata editing is on this host. |
| `tests/test_observe.py` | rewrite | Docstring note: the specification ID is preserved verbatim as origin identity; the host these checks target is Claude Code. |
| `evals/build-manifest.json` | rewrite | 88 artifact rows regenerated against the delivered bytes. Required: it tracked `assets/openai-yaml-guidance.md`, which no longer exists. |
| `schemas/` (20 files) | preserve | Host-neutral closed schemas; unchanged so existing records stay valid. |
| `evals/` (16 other files) | preserve | Cases, fixtures, profiles, runtime, schemas, README — verified free of host-specific content. |
| `scripts/` (10 other files) | preserve | `graders.py`, `run_evaluation.py`, `trial_runner.py`, `trial_worker.py`, `windows_trial.py`, `standards_observe.py`, `adaptive_observe.py`, `authoring_intake.py`, `build_evidence.py`, `custody.py` — no host coupling found. |
| `tests/` (13 other files), `references/` (6 other files), `assets/` (2 other files) | preserve | Verified free of host-specific content. |

Verified: the only source file absent from the target is `assets/openai-yaml-guidance.md`, and the only added file is its Claude replacement.

## Metadata profile

`scripts/skill_format.py` now separates two kinds of row, because the two official sources disagree and promoting either one to a required rule fails packages the other calls valid.

**`metadata_checks` (required)** carries only constraints both sides support: `name` 1-64 lowercase/hyphen matching the directory; `description` non-empty and ≤1024. It gains the Claude Code optional fields with their value domains — `allowed-tools`/`disallowed-tools`/`paths`/`arguments` as a string *or* a non-empty list of strings; `metadata`/`hooks` as mappings; `disable-model-invocation`/`user-invocable`/`background` as booleans accepting `true/false`, `yes/no`, `on/off` and `1/0` in any case; `effort` in `low|medium|high|xhigh|max`; `shell` in `bash|powershell`; `context` equal to `fork`; `agent` only meaningful with `context: fork`.

**`advisory_checks` (new, never required)** reports the divergences: a YAML-list tool grant is valid here and non-portable; `description` + `when_to_use` past 1,536 characters is truncated in the Claude Code listing; the reserved words `anthropic`/`claude` and XML tags in `name` are prohibited by the Anthropic authoring guidance but not by the Claude Code reference.

## Rule re-pinning

`assets/rules-snapshot.json` moved to revision `2026-09-17.1`, `host: claude-code`. Three sources were retrieved live on 2026-09-17 and their extractions retained in the run inputs with digests: the Claude Code skills reference, the Agent Skills specification, and the Anthropic skill-authoring best-practices page. Each is labelled `representation: documentation extraction produced by the host WebFetch tool … not raw HTTP bytes`, because that is what was actually obtained. Five in-repository Anthropic guidance copies under `docs/Agentskills/` are pinned `snapshot_only`. The project specification carries forward with its digest re-verified unchanged.

Seven superseded sources — OpenAI Build skills, prompt engineering, model guidance, citation formatting, and their three local snapshots — are retained by identity and digest in a new `supersedes` block rather than reinterpreted against a host they do not describe.

**REC-006 changed authority class.** No Anthropic or Claude Code citation-formatting source was retrieved, so the rule survives as `project_policy` sourced to the project specification, with its official-host freshness recorded `unavailable` and flagged as an open sourcing question. It was not re-pointed at a plausible-looking Claude URL.

## Design decisions worth review

**`Skill` is deliberately absent from `allowed-tools`.** The source says "Never invoke the builder from this workflow" in several places. On this host that can be a capability boundary instead of a sentence, so it is one — including against an instruction embedded in a package being assessed.

**`Task` is granted.** This is the one grant that widens scope, and it was not automatic. `references/trials.md` already required "the actual host task runner for minimal-input workflow trials when available", and the source repeatedly notes that an optional independent review "does not gain enforced isolation through task prose." In Claude Code the host task runner *is* `Task`, and it supplies the fresh context that makes an independent review independent. The converted text now says plainly that a subagent shares this session's authentication and budget and is not an enforced permission boundary.

**The Bash grants are narrower than the trials may need, on purpose.** `Bash(python:*)`, `Bash(python3:*)`, `Bash(pwsh:*)` and `Bash(powershell:*)` cover the bundled helpers and the Windows trial adapter. A trial that runs some *other* target's command is not pre-approved and surfaces as a permission decision. For a skill whose job includes executing other packages' commands, that prompt is a feature. `SKILL.md` states this rather than implying the allowlist is narrower than it is.

**`WebFetch` is granted** so the live rule refresh the workflow describes can actually happen. Without it the skill could only ever report `snapshot_only`.

**`model` and `effort` are omitted**, consistent with the source declaring neither.

**Native CLI trial shape re-verified, not translated.** The source carried a `codex exec …` command "verified as present in CLI 0.154.0". Rather than invent a Claude equivalent, `claude --version` and `claude --help` were run: the replacement shape uses `--print`, `--output-format json`, `--add-dir` and `--permission-mode acceptEdits`, all verified present in Claude Code 2.1.274, and the text notes there is no `--cd` equivalent and warns against the permission-bypass flags.

## Open questions — maintainer decisions required

All three are in the authoring design and the handoff packet.

**Q1 — installed binding path.** `adaptive_contracts.py` required `package_path == '.agents/skills/' + name`. Swapping in `.claude/skills/` would hardcode an installation root into a package that may be loaded from a different location, which `conversion-rules.md` forbids and which this project has already been bitten by. The rule is now host-neutral: the path must be a normalized relative locator whose final segment is the binding's name. If DevForgeAI wants the Claude constant enforced, that is a maintainer call. Affects `B4-inspect-package`.

**Q2 — operational binding directory.** `.agents/devforgeai/project-binding.json` is carried over unchanged. Renaming a live operational contract unilaterally would break existing bindings and fixtures for a cosmetic gain. Affects `B4-inspect-package`, `B5-exercise-behavior`.

**Q3 — which frontmatter authority governs.** The Claude Code reference and the Anthropic best-practices page disagree on `name` length, reserved words, XML tags and the `description` cap. Only the constraints both support are required; the rest are advisory with the conflict recorded. Affects `B3-select-rules`, `B4-inspect-package`.

## Verification performed

| Check | Result |
| --- | --- |
| Design validated against `authoring-design-v1` | accepted by `authoring.py begin` (8 behaviors, 30 resources, 93 source refs) |
| Design capture bound | `design-capture.json` + `origin.design_capture_ref` + `stage-integrity.json`, source and snapshot digests equal |
| `change_paths` vs candidate contents | 89 = 89, no file outside authorized scope, none declared but absent |
| Every prose replacement | asserted to hit exactly once (21 in references/assets, 10 in tests) |
| Python syntax across the package | all files parse |
| Internal Markdown links | 0 unresolved across every `.md` in the package |
| Residual host coupling | none outside deliberate provenance: the `supersedes` block, the Codex→Claude mapping section of the new asset, the preserved origin specification ID, and the new tests that write a foreign `agents/openai.yaml` as the artifact under detection |
| Frontmatter parses as YAML | valid; `name: skill-validator`, description 702 chars, `Skill` absent, `Task` present |
| `evals/build-manifest.json` self-consistency | 88 tracked paths regenerated: 1 added, 1 removed, 21 changed |
| Delivered bytes vs candidate | identical (`diff -rq` empty) |
| Publication (run 001) | `AUTHORED`, `publication-readback.json` `PUBLISHED`, 89 applied paths, no unresolved write issues |
| Publication (run 002) | `AUTHORED`, `PUBLISHED`, 4 applied paths, prior origin `authored` against the run-001 baseline |
| `NOT_APPLICABLE` result/applicability pairing | matches the `adaptive_observe.py` line 34/36 contract and the `adaptive-check-observation-v1` result enum |
| Dual-path mirror | `src/claude/skills` and `.claude/skills` `diff -rq` clean (skills subtree only - see below) |
| Host discovery | Claude Code loaded `/skill-validator` from the mirrored copy in-session |

These are build-integrity and write-custody observations. **No test suite, eval campaign, grader, structural checker or trial was executed**, per the authoring-only contract. The 16 carried-over test files — including the 4 that were rewritten — remain unexecuted against the converted bytes.

## Reviewer findings on the run-001 bytes

An independent review of the published package raised four items. Two were confirmed against the code and fixed in run 002; two were checked and did not hold.

**F1 (confirmed, blocking) - the portability divergence reduced every sibling package to INCOMPLETE.** `text_resources.check()` defaults `required=True`, and run 001 emitted the YAML-list `allowed-tools` divergence as `check('AV-F04','SKILL.md','NOT_RUN', ..., 'unknown')`. `observe.reduce_checks` puts any required row with `applicability == 'unknown'` or `result == 'NOT_RUN'` into `incomplete`, which reduces to INCOMPLETE - and `adaptive_observe.reduction()` calls exactly that function over the AV rows. So `advisor`, `dev`, `skill-builder` and the converted `skill-validator` itself would all have reduced to INCOMPLETE.

This is the same defect the conversion set out to remove, moved from *required FAIL* to *required NOT_RUN to INCOMPLETE*. A validator that can never report PASS on this repository's own skills is still the bug. The shipped test asserted the row's `result` and never the reduction, so it passed while the reduction was broken.

Fixed: one required AV-F04 row carries the outcome; each divergence is a separate **non-required** row with its own discriminator so several cannot collide on one `check_id`. The reviewer's suggested `applicability='not_applicable'` pairing was not used - `adaptive_observe.py` requires `(applicability == 'not_applicable') == (result == 'NOT_APPLICABLE')`, so that row would have been rejected by the package's own contract. The divergence rows stay `applicable`/`NOT_RUN` and are excluded from the reduction by `required=False` alone. The unknown-*extension* row stays required, because an unrecognised field genuinely needs adjudication.

**F2 (confirmed) - one malformed optional field produced two required FAIL rows.** AV-F01 and the new AV-F04 block each called `frontmatter()` and each failed on the same exception, against the same bytes, which collides with "counts each member and integration check once". Fixed: the entrypoint is parsed once; when it does not resolve, AV-F01 carries the failure and AV-F04 is `not_applicable` / `NOT_APPLICABLE` with a reason.

**F3 (checked, does not hold).** The reviewer asked whether `skill-builder/scripts/init_skill.py` still scaffolds `agents/openai.yaml`, which would falsify the rewritten assertion in `tests/test_authoring.py`. It contains no `agents/` scaffolding at all. The assertion stands and is a useful regression guard.

**F4 (checked, does not hold).** The conversion deleted the `configuration_yaml`, `configuration_policy` and `invocation_policy_type` check identifiers. Nothing in `evals/` or `tests/` references any of them. `evals/runtime.json` pins a Python version and capture limits only - no package digest - so it is not stale.

Run 002 changed four paths: `scripts/text_resources.py`, `scripts/observe.py`, `tests/test_postmvp_resource_quality.py` and the regenerated `evals/build-manifest.json`. Two tests now assert the **reduction outcome**, not just the presence of a row, so this defect class cannot pass unnoticed again; a third asserts that several divergences produce distinct check identities.

**Worth the assessor's attention:** these fixes were reasoned from the code and could not be executed, because authoring may not run the package's own checkers. F1 in particular was invisible to the test that was supposed to cover it. The first independent check should be running `text_resources.package` against this repository's four Claude skills and confirming each AV-F04 reduction is PASS.

## Pre-existing repository drift found, not touched

`diff -rq src/claude .claude` is *not* clean, but the only differences are `src/claude/agents/legacy/` (203 files) and `src/claude/commands/legacy/` (87 files), which exist in the source tree and not in the operational copy. This predates the conversion, matches the `skills/legacy/` reorganization already visible in the tree, and is outside this task's scope. `CLAUDE.md`'s statement that the pair is "896 files each, currently `diff -rq`-clean" is stale — the counts are now 1063 and 773.

## Next owner and action

Independent assessment, using the converted package itself.

- Packet: `docs/plan/skill-authorings/skill-validator/20260917T112416Z-claude-conversion/validation-request.json` (SHA-256 `820f37bbfbb9d262fae6c7078552a4c96a0e6be2529ecb88d9b598a7b0779965`)
- Invocation: `docs/plan/skill-authorings/skill-validator/20260917T112416Z-claude-conversion/validator-request.md`

The packet names the authored design, 93 original requirement sources with digests, the three open questions, and unperformed helper-testing obligations for seven scripts. The highest-value first checks are the ones authoring was not permitted to run: the test suite against the converted bytes, and whether the AV-F04 reduction is PASS for this repository's own `advisor`, `dev`, `skill-builder` and `skill-validator` packages - the exact property that run 001 got wrong and whose fix in run 002 is reasoned, not executed.

The package is at `src/claude/skills/skill-validator/` and was copied to `.claude/skills/skill-validator/`.

Two things about that copy should be stated rather than left to the reader. First, it is a mirror of the `skills/` subtree, not evidence that the ADR-073 dual-path contract is being upheld - it demonstrably is not, elsewhere in the same tree (see *Pre-existing repository drift*). Second, the copy had a real effect: `.claude/skills/` is a live discovery location, so `/skill-validator` became invocable in this session. That is discovery, not installation - no hooks, settings registration, CI wiring or plugin assembly was performed, and none is implied by the copy. If the maintainer wants the package staged in `src/claude/` only, deleting `.claude/skills/skill-validator/` reverses it completely.
