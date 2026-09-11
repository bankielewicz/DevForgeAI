# Authoring notes — devforge-prototype (SKILL-004), Claude scaffold

Date: 2026-09-10 UTC. Worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-prototype-20260910`, branch `author/claude-devforge-prototype-scaffold-20260910`, base `c17e758417da64928a0f47fc2600304465ac3f3c` (HEAD verified equal to base and the tree clean before any write).

Authored only. No installation, export, binding, activation or evaluation was performed. Validation status: Not performed. Behavioural status: `NOT_EVALUATED`. Tiers A, B and C: `NOT_RUN`.

## The builder that was followed

The Claude `devforge-project-expert-creator` package was **source-loaded** — read read-only by absolute path and followed as instructions. It was not installed, not discovered, not invoked as a skill, and not run. Files loaded:

- `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md`
- `.../references/framework-context.md`
- `.../references/existing-skill-selection.md`
- `.../references/interview-guide.md`
- `.../references/manual-operation.md`
- `.../assets/skill-design-spec.md`
- `.../assets/handoff.md`
- `.../references/derivation.json` and `.../references/sources.md` (read for record shape)

**Identity of the loaded bytes.** That worktree's HEAD at authoring time was `8c0bdd0d86c7330d2f7910d63b3511e8df43d20b`, not the assigned `4999f3106565c5e320d1f1a7db066b437e4e94be`. `git diff --stat 4999f31 8c0bdd0` shows eight files changed, all under `docs/skill-authoring/history/.../validation/`, and no file under `providers/`. The package bytes read are therefore the bytes at `4999f31`. The per-file digests recorded in the candidate's `references/derivation.json` were taken from `git show 4999f31:...` rather than from the working tree, so they are pinned to the assigned commit regardless.

**Status of the builder.** It is itself a draft under independent review. An E1 bootstrap review of its predecessor candidate `69b6090` was revise-bounded; findings F-001 through F-004 were applied as repair pass 1 at `4999f31`, and F-005/F-006 were declined as evaluation gaps rather than target defects. No native evaluation of the builder has been performed — its own tiers are unobserved. Following it is an authoring method. It certifies nothing about either package.

**Builder files deliberately not loaded:** `assets/expert-spec.md`, `assets/expert-package.md`, `assets/expert-skill.md`, `assets/evaluation-cases.md` (all govern the builder's own XSPEC/XPKG outputs, which this skill does not produce) and `references/validator-handoff.md` (evaluator-repair intake; there are no findings to intake on a first scaffold).

## Workflow actually run

**Intake.** Read SKILL-004 (digest verified against the packet), both output templates, the shared handoff template, the two authoring templates, the skill-authoring contract, the relevant sections of the artifact and execution contracts, the language policy, bounded-delivery, the roster's provenance flow, and both repository `CLAUDE.md` files. Recorded every digest in the candidate's `references/derivation.json`.

**Selection.** Searched `providers/claude/plugins/devforgeai/skills/` and `providers/codex/plugins/devforgeai/skills/` at base, plus `docs/mvp/roster.md`. Claude has brainstorm, develop, project-expert-creator and review; Codex additionally has evaluate-expert. **No `devforge-prototype` exists in either provider**, so there is no port source and creation is justified. The roster records SKILL-004 as "Proposed". The destination directory did not exist at base; nothing was overwritten.

*Search limits, stated as limits:* `~/.claude/skills`, any managed settings directory, any `--add-dir` directory and project-local `.claude/skills` installations were not searched and are not visible from this worktree. What this establishes is "no suitable skill found in the searched inventory". It does not establish that no such skill exists anywhere.

**Design.** Populated the working design document at `design/skill-design-spec.md` from the specification, templates and contracts. **No questions were asked**, per the assignment. Every decision the specification leaves silent is recorded there as a labelled proposal, not as a requirement.

**Authoring.** Wrote the package. **PreparedTransfer.** Wrote `spec-mapping.md`, `file-manifest.json`, these notes and `handoff.md`.

## Proposed defaults recorded

None of these comes from SKILL-004. Each is labelled a proposal in `SKILL.md`, in `references/derivation.json` under `proposed_defaults`, and in the design spec §9.

| Proposal | Value | Basis |
|---|---|---|
| XPLAN / XREPORT destination when none is selected | `docs/devforge/experiments/` | The installed `devforge-brainstorm` precedent of a `docs/devforge/<kind>/` map |
| Handoff destination when none is selected | `docs/devforge/handoffs/` | Same precedent, so a project does not acquire two handoff locations |
| Experiment fence path when the user supplies none | `experiments/<XPLAN-ID>/` | Keeps the prototype identifiable and outside a policy source root; SKILL-004 requires a declared fence but names no path |
| A missing time or resource bound | Not a default — a missing required input that stops the experiment | SKILL-004's Required context makes the bound part of the required constraints |
| Near-miss exclusions beyond develop | design, change, brainstorm named in the description | SKILL-004's "Does not activate for" row names only develop; the other three come from the roster's skill boundaries |
| Three distilled references rather than shipped contract copies | `framework-context`, `recording-rules`, `experiment-boundaries` | Progressive-disclosure guidance in the authoring contract; the builder's own precedent |

## Rust authority and the missing integrations

The only DevForge command named anywhere in the package is `devforge isolate`, and it is named with its actual limit: it mounts `/` read-only and rebinds only `--project` writable, which bounds the whole project and therefore **does not implement an experiment fence**. `devforge check` and the `init/red/green/accept/verify/status` gate are described as belonging to other workflows.

`devforge --help` was run once, against `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge`, to confirm the command surface before naming anything. Output listed: `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`. **No DevForge command was run against any project**, and no gate, policy, test or pin in the companion repository was read for modification or modified.

Four integrations this workflow would need are recorded as open requirements in `references/framework-context.md` and as routes R1–R3 in the design spec, with owner "integration owner", feasibility "unknown" and status "requirement recorded; no gate implemented":

1. A sub-project experiment fence.
2. A pre-execution plan freeze held outside the evaluated agent's write access.
3. A promotion check tying a hardening disposition to actual hardening.
4. Threshold immutability between a frozen plan and its report.

Nothing in the package presents any of these as active enforcement, and `evals/cases.jsonl` case `XP-B-001` demonstrates gap 4 deliberately: every deterministic assertion matches on a report that moved its own threshold, and the defect is routed to independent review with a null grader rather than approximated by one.

No Python or shell was added to the package. There is no `scripts/` directory. The JSONL runner and deterministic graders the eval cases target belong to the Claude `devforge-evaluate-expert` package and were not duplicated.

## Evaluation runner dependency

`evals/cases.jsonl` is authored against the runner and graders in the Claude `devforge-evaluate-expert` package at commit **`e52ac596cbf790dfa156d883852d392c512fdbcc`**. Read at that commit:

- `scripts/run_cases.py` — `--help` output read; sha256 `d1fb18689eeea31f8facde4e3de1507320e74ffb349f547f9db2201395bb132d`
- `scripts/graders.py` — the ten graders and their argument shapes; sha256 `7c03e7b2137787035c995787b232a7bf8d801c88672675bacf4359a8cdb38c13`
- `references/runner-interface.md` — the interface contract and the gate-versus-evidence boundary; sha256 `a58c35dab0fdb68d3a7dea92bf761a1e4ac25bee89fb49320fb09e247557170b`
- `evals/cases.jsonl` — case-shape precedent; sha256 `b4b0c9314f43aa4aebaeee7f25c4d5e4b81fc2b0e628d98e3505c91679cb1f83`

That package is source-only, under independent review, not installed anywhere, and its own evaluation is `NOT_RUN`. Nothing about its state transfers to this package. The dependency is recorded in `evals/evals.json` under `runner_dependency`.

## Commands actually run

Every command below is authoring hygiene against files this author wrote. **None of it is an evaluation of `devforge-prototype`, and no row of any output may be cited as evidence about this skill's behaviour.**

| Command | Purpose | Result |
|---|---|---|
| `git -C <worktree> rev-parse HEAD` / `branch --show-current` / `status --short` | Verify assignment before writing | HEAD `c17e758…` equals base; branch correct; tree clean |
| `git -C <builder worktree> merge-base --is-ancestor 4999f31 HEAD` and `git diff --stat 4999f31 HEAD` | Establish the identity of the builder bytes read | ancestor; 8 files changed, all under `docs/skill-authoring/.../validation/` |
| `git show 4999f31:… \| sha256sum` (7 files) | Pin builder digests to the assigned commit | recorded in `references/derivation.json` |
| `sha256sum` over the governing inputs and templates | Verify the packet's stated digests and record sources | SKILL-004 matched `e4f61c35…`; both output templates and the shared handoff matched the packet |
| `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help` | Confirm the command surface before naming any command | 10 subcommands listed: `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`. Nothing run against a project |
| `… devforge isolate --help` | Confirm the exact flag shape before naming it in the package | `--project`, `--runtime` with possible values `codex` and `claude`, `--policy`, `--state`, `--expert`, and a trailing `-- <COMMAND>...`. Its own summary line is "Run with only the project writable; no unconfined fallback", which is the project-wide bound the package states |
| `… devforge expert --help` | Confirm the subcommands named in `references/framework-context.md` | `prepare`, `bind`, `status` |
| `graders.read_frontmatter` (evaluate-expert `e52ac59`) against this package's `SKILL.md` | Confirm the frontmatter parses under the restricted top-level scalar subset an evaluator's structural case will use, rather than only under a full YAML parser | `parsed`; fields `name` and `description` both populated; description 1,129 characters, inside the client's documented 1,536-character budget. Authoring hygiene over this author's own file; it establishes nothing about behaviour |
| `python3 scripts/run_cases.py --help` (evaluate-expert, `e52ac59`) | Read the runner interface | usage and exit-status contract recorded |
| `python3 <runner> --cases <this package>/evals/cases.jsonl --candidate <this package>/evals/fixtures --out <scratchpad>/observations.jsonl --mode source` | **Case-file loadability and fixture-discrimination check.** Confirms the case file parses, every grader name exists, every `candidate_subpath` resolves, and each fixture is discriminated as its case intends | exit 0; 9 case records. XP-C-001/002/003 and XP-A-001 all MATCH; XP-C-004/005/006 MISMATCH as authored; XP-A-002 COULD_NOT_RUN with no terminal completion; XP-B-001 MATCH on structure plus INDETERMINATE on the routed assertion. Output written to the scratchpad, outside the package. **This tests the fixtures and the case file. It evaluates nothing about this skill, and tiers A/B/C stay `NOT_RUN`.** |
| Link check over every package `*.md` | Confirm package-relative links resolve inside the package | 7 local links resolve; 0 broken; 0 escape the package |
| Fixture-path check over `evals.json` and `cases.jsonl` | Confirm every declared `files` path exists and stays within `evals/` | none unresolved |
| `grep -rn "/home/bryan" <package>` | Confirm no developer home path ships | 3 found and removed; rescan clean |
| Trigger-file stratification check | Confirm ids unique and every category has both splits | 22 queries, 10 positive / 12 negative, 6 negative categories, 12 train / 10 validation |

`WebFetch` of `https://code.claude.com/docs/en/skills`, 2026-09-10 — claims relied on are recorded in `references/sources.md`. The builder's second source (the subagents page) was **not** re-fetched and is recorded as carried-but-not-re-verified rather than restated as this pass's own retrieval.

## Decisions worth flagging to the reviewer

- **The `allowed-tools` nuance.** The Claude documentation does describe frontmatter fields that grant tool permissions. The builder's flat statement that "a skill grants no tool permissions" is therefore true of a package that omits them, not of the client. `references/sources.md` states this precisely rather than repeating the flat claim.
- **The good fixture reports a *missed* threshold.** The exemplar of a well-run experiment is one that failed, because SKILL-004's hardest requirement is preserving a failure rather than renegotiating it.
- **Several tier-B prompts carry pressure.** XB-4, XB-7, XB-8, XB-9 and XB-11 each embed a plausible-sounding request to move a threshold, adopt a newer revision, declare a draft ready, close out early, or reach outside the fence. That is deliberate: the specification's boundaries are only observable under pressure. A grader must not mark a correct refusal as a failure to be helpful.
- **`baseline_comparison` on XB-8 says `old_skill`** because a prior report artifact is the fixture. If no earlier candidate exists at evaluation time, that arm is `NOT_APPLICABLE` with the reason recorded — not a silent substitution of `without_skill`.
- **No managed-runtime section** was carried from `devforge-brainstorm`. SKILL-004 describes no managed operation, and importing the concept would add a runtime claim the specification does not make.

## Unresolved items

1. Every proposed default above awaits a decision. Silence is not approval.
2. `docs/mvp/package-index.json` and `docs/mvp/roster.md` still record SKILL-004 as Proposed / not-implemented. Updating them was explicitly outside this fence and is the integration owner's action.
3. Tiers A, B and C are `NOT_RUN`. The deterministic arm additionally depends on `devforge-evaluate-expert` at `e52ac59`, which is itself unevaluated and not installed.
4. The four missing CLI integrations are open. Until they exist, the fence, the plan freeze, the promotion boundary and threshold immutability are observed by whoever does the work, not enforced.
5. No client was observed loading this package, so tier A is unobserved rather than negative, and no claim of discovery or activation appears anywhere in the package or this record.

---

# Repair pass 1 — from the independent scaffold review

Recorded 2026-09-10T21:46:05Z UTC. Supersedes candidate `e199230858d871926fff2d55de8b015fa0ce335e`.

Input: `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-prototype/validation/scaffold-review/` — disposition **revise**, 0 BLOCKER / 1 MAJOR / 4 MINOR / 1 ADVISORY. Read-only untrusted evidence. The review directory was not modified. Every finding was verified against the actual candidate bytes at `e199230` before its change was applied; the verification command and its result are in the table below.

One consolidated pass, authorised by the coordinator. The next-owner substitution — this scaffold's author under coordinator dispatch, rather than the validator's default `devforge-project-expert-creator` — is confirmed and is recorded here so it stays visible.

## F → CHG → disposition

| Finding | Sev | CHG | Verified at `e199230` (file:line) | Disposition | Files changed |
|---|---|---|---|---|---|
| F-001 | MINOR | CHG-001 | `evals/cases.jsonl` — all 9 cases set `candidate_subpath` into `evals/fixtures/`; none reads the package. `--mode installed` was byte-identical because no case declared a mode. | **applied** | `evals/cases.jsonl` |
| F-002 | MAJOR | CHG-002 | `evals/evals.json` `evals[7]` (id 8) `baseline_comparison: "old_skill"`; the other ten say `without_skill`. `git ls-tree c17e758 providers/claude/plugins/devforgeai/skills/` returns four skills and no `devforge-prototype`. | **applied** | `evals/evals.json` |
| F-003 | MINOR | CHG-003 | `SKILL.md:50` claimed the freeze exists "so that a later reader can tell the plan preceded the evidence"; `references/framework-context.md:33` denies exactly that; grep of `references/experiment-boundaries.md` for `preced` / `does not establish` / `self-recorded` / `outside the evaluated` returned **no match**, so the routed file did not carry the limit. | **applied** | `SKILL.md`, `references/experiment-boundaries.md` |
| F-004 | MINOR | CHG-004 | `evals/evals.json` `runner_dependency.commit = e52ac59…`. `git log e52ac59..e641797` shows `b6a4bf7` → `e101e76` → `6916b60` → `e641797`; both scripts changed. | **applied** | `evals/evals.json`, `references/derivation.json` |
| F-005 | MINOR | CHG-005 | `grep -rn -- "--candidate" evals/` returned **no match**. Reproduced the failure mode: `--candidate <package root>` exits 0 with all nine cases `COULD_NOT_RUN` and zero assertions observed. | **applied** | `evals/evals.json`, `evals/cases.jsonl`, `evals/fixtures/README.md` |
| F-006 | ADVISORY | CHG-006 | Line 3 of each: `XPLAN-001.md` → `XPLAN-006`, `XREPORT-001.md` → `XREPORT-006`, `XPLAN-004.md` → `XPLAN-010`, `XREPORT-004.md` → `XREPORT-010`. Demonstrated. | **applied — README option** | `evals/fixtures/README.md` |

F-006 was ADVISORY and conditional on being demonstrated. It is: the four filenames and their `artifact_id` values genuinely diverge. The review offered renaming or a README statement and named the README the lower-risk option; renaming would touch every `files` entry, every `args.file`/`args.path` and would churn the XP-C-002 and XP-C-006 sentinel digests for a readability gain no assertion depends on. The divergence is deliberate — stable fixture slots versus realistic project allocations — and is now stated with a mapping table rather than left to be inferred.

## What was deliberately not copied

The review's `evaluator-structural-cases.jsonl` was copied **in substance** as the starting point for CHG-001 and is not referenced by the package: it is evaluation evidence and must not become a package dependency.

Its `EV-S-007` asserted `required_report_fields` against `assets/experiment-plan.md` and `assets/prototype-report.md` and observed `MISMATCH placeholder`. Those are unfilled templates; placeholders in them are correct. Authoring that case would record a healthy package as defective. `XP-PKG-003` asserts their presence instead, and its `notes` says why — placeholder detection belongs on a produced artifact, which is what `XP-C-004` covers.

## Verification of this pass

| Check | Result |
|---|---|
| Nine existing cases unchanged | Field-level comparison against the pre-repair file: only `tier` and `notes` differ; `assertions`, `candidate_subpath` and `expectations` byte-identical |
| Nine existing rows still reproduce | Re-ran with `--candidate <package>/evals/fixtures --mode source` against the `e641797` runner: all nine rows identical to the review's `candidate-cases.observations.jsonl` in `execution_status`, `result` and `observed` text |
| New cases observe what they claim | `--candidate <package> --mode source`: XP-PKG-001..004 all MATCH; XP-PKG-005 all INDETERMINATE with reason `mode=source`, which is the honest result with no installed copy allocated |
| CHG-003 acceptance | `grep -rn "preceded the evidence"` over the package returns exactly two occurrences, both of which **deny** the claim (`framework-context.md:33`, `experiment-boundaries.md:21`) |
| CHG-004 acceptance | `run_cases.py` at `e641797` hashes to `95ca2abf…` and `graders.py` to `1b7a27a3…`, matching the values recorded beside the pin and those the coordinator supplied |
| Links | 9 local links resolve inside the package; 0 broken; 0 escape |
| Frontmatter | `parsed` under the restricted top-level scalar reader; `name` and `description` populated; description 1,129 characters |
| Digest chain | 31 manifest entries match the package on disk; 30 derivation destination digests match the manifest; no package file lacks a derivation entry; superseded digests preserved with their `e199230` locator |

Both runner invocations are **authoring hygiene over this author's own files**. They establish that the case file loads, that the nine prior rows are unchanged, and that the new cases observe what they claim. They are not an evaluation of this skill.

## Status after repair pass 1

**Validation status:** Not performed. **Behavioural status:** `NOT_EVALUATED`. **Tiers A, B and C:** `NOT_RUN`. **Enforcement status:** requirements recorded; no gate implemented by this skill. **Finding status:** source changes recorded; reevaluation required.

Applying a change means the source was edited. It closes no finding. F-001 through F-006 keep their original IDs and severities, were observed against `e199230`, and do not transfer to these bytes.

## Corrections to earlier entries in this file

- The fallback proposed above under "Decisions worth flagging" — that XB-8's arm becomes `NOT_APPLICABLE` if no earlier candidate exists — is **withdrawn**. F-002 is right that this misuses the fixed vocabulary: `NOT_APPLICABLE` is reserved for a stated scope exclusion and an absent baseline is not one. The arm is `without_skill`.
- The runner dependency recorded above as `e52ac59` is superseded by `e641797`; see CHG-004. The earlier entry is left in place rather than rewritten, because it records what was true when it was written.

## Still open after this pass

Unchanged from the list above, plus: the `--candidate` convention remains undocumented in the `devforge-evaluate-expert` package's own cases. That is a defect in a sibling package, reported to its owner and not edited around. Its one open MINOR (F-R01) also remains that package's own.
