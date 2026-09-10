# Authoring notes — devforge-change (SKILL-012), Claude package

Authoring session 2026-09-10 UTC. Worktree
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-change-20260910`, branch
`author/claude-devforge-change-scaffold-20260910`, HEAD verified
`c17e758417da64928a0f47fc2600304465ac3f3c` before any write.

Times below are actual `date -u` readings, not placeholders: the session's first reading was
`2026-09-10T20:04:04Z` and the pre-manifest reading was `2026-09-10T20:23:16Z`.

## The builder that was followed

The Claude `devforge-project-expert-creator` package at commit
`4999f3106565c5e320d1f1a7db066b437e4e94be` was **source-loaded, not installed**. Its bytes
were read out of git object storage with
`git show 4999f3106565c5e320d1f1a7db066b437e4e94be:<path>` from the worktree
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910`,
whose HEAD is ahead of `4999f31` by coordinator evidence commits only. Pinning by object
hash rather than reading the working tree is deliberate: the working tree is not the frozen
builder.

Files loaded, by absolute path at that revision:

| Absolute path (at `4999f31`) | Used for |
|---|---|
| `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910/providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | The five-phase workflow actually followed: Intake, Selection, Design, Authoring, Prepared transfer |
| `.../devforge-project-expert-creator/references/framework-context.md` | Ownership split, roles that stay separate, two roots, the artifact envelope, package shape and packaging rules, result vocabulary, bounded delivery |
| `.../devforge-project-expert-creator/references/existing-skill-selection.md` | Where to look in a Claude environment, how to compare candidates, how to record search scope and its limits |
| `.../devforge-project-expert-creator/references/interview-guide.md` | The specification content checklist, and how to record an enforcement requirement without claiming enforcement exists |
| `.../devforge-project-expert-creator/references/manual-operation.md` | Command boundaries, artifact mapping, what a concise handoff is and is not |
| `.../devforge-project-expert-creator/assets/skill-design-spec.md` | The template for `design/skill-design-spec.md`; copied to this artifact location and filled here, never in place |
| `.../devforge-project-expert-creator/assets/handoff.md` (sha256 `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790`) | The template for `handoff.md` in this directory |

**Builder status.** The builder is itself a draft under independent review. Its E1 bootstrap
review was revise-bounded and its repairs are applied at `4999f31`; it has had **no native
evaluation**. Following it is a recorded dependency of this work, not a validation of either
package. Nothing about this scaffold is stronger because the builder was followed.

Two builder assets were deliberately **not** used: `assets/expert-spec.md`,
`assets/expert-package.md` and `assets/evaluation-cases.md` are shapes for a *project expert*
package. This assignment authors a *framework roster skill*, whose specification (SKILL-012)
already states the requirements those documents would otherwise capture, and whose acceptance
cases go into `evals/` rather than into an XSPEC. The design spec plus this package's own
`references/derivation.json` and `evals/` carry the same facts in the shapes this package
actually has.

## The builder's workflow, as actually run

**Intake.** Recovered before asking anything: the packet, the governing specification, both
output templates, the four contracts, the roster, the two authoring templates, the
`devforge-brainstorm` exemplar, and the Claude client documentation. All eleven governing
inputs were hashed in the working checkout and compared against the same paths at
`c17e758417da64928a0f47fc2600304465ac3f3c`; every pair matched, and every value matched the
packet's stated digest where the packet gave one (the skill-authoring contract's full digest
is `371462385b4e32d1b347f959abb779f4be4251e357c5720a9aef039113eb4b53`; the packet truncated
it).

**Selection.** Searched `providers/claude/plugins/devforgeai/skills/` at base: four entries —
`devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator`,
`devforge-review`. **No `devforge-change` exists.** Also checked
`docs/skill-authoring/history/claude-scaffolding-20260910/` for a destination collision: the
`devforge-change` directory existed and contained no files.

Creation is justified, and the justification is a distinction of activation and scope rather
than of subject matter: nothing installed activates on "what does this change invalidate", and
nothing installed owns the impact graph or the routing decision. The four candidates and their
boundaries are compared in design spec § 9.

Search limits, recorded because a bounded search cannot support a global claim: personal
`~/.claude/skills/`, enterprise managed settings, claude.ai account-synced skills and any
`--add-dir` directory were **not searched** — they are runtime discovery locations for a
consuming session, outside this assignment's fence. The Codex inventory was not compared;
provider sources have distinct ownership. The honest result is "no suitable skill found in
the searched inventory".

**Design.** `design/skill-design-spec.md` was populated from the specification, the templates
and the contracts. **No questions were asked**, per the assignment. Where a source is silent,
a proposed default is recorded and labelled **PROPOSAL** — see the list below. Silence is not
approval and a default invented here is not a requirement anyone gave.

**Authoring.** The package was written against the design spec, in the order: `SKILL.md`,
assets, references, fixtures, evals, then `references/derivation.json` last so its destination
digests describe final bytes.

**Prepared transfer.** `file-manifest.json` and `handoff.md` in this directory. The next owner
is an independent evaluator. Validation status: not performed.

## Decisions and proposed defaults

Settled by the specification or the assignment — not proposals:

- Four phases (Capture, Trace impact, Decide, Route and verify) and their exit conditions.
- One output artifact, `CHG` prefix, from the governing template, plus a handoff.
- Nine acceptance cases: five specification rows plus four common cases.
- Two-field frontmatter, `name` and `description` only.
- `without_skill` as every tier-B baseline, because no previous revision of this skill exists.

Proposed defaults, each recorded as **PROPOSAL** in design spec § 9:

| Proposal | Why | What would settle it |
|---|---|---|
| No `scripts/` | Nothing in this workflow is a repeated deterministic operation. A helper would either read project artifacts (judgement) or restate a check the Rust CLI owns | An owner identifying a genuinely deterministic evaluation-only need |
| Four references (`impact-tracing`, `recording-rules`, `cli-boundaries`, `sources`) | Derived from what the four phases actually need at the point they need it | Review of whether any is unused or any phase is under-served |
| Invocation policy: automatic when relevant and explicit by name | The Claude default; the specification restricts model invocation nowhere | An owner choosing `disable-model-invocation` or `user-invocable` |
| No hard-coded default output destination | The specification names none. Inventing a path would be a constraint nobody set, and a wrong default is worse than deferring to the project's own map | A project artifact map convention being accepted |
| All workflow items classified required | The specification states them as required behaviour; that is the basis for proposing it, not a user's answer | A user classifying W1/P1–P4/T1–T6 |
| Trigger split fixed and stratified, roughly 60/40 train/validation | The authoring contract requires a fixed split; the ratio is unspecified | An owner setting a ratio |
| Synthetic fixture project "tidepool", invented package `tidepool-sync` | Fixtures must be reproducible and must not imply a real project or a real vendor release | Nothing; this is an authoring choice recorded for transparency |
| Enforcement routes R1 and R2 as recorded requirements with feasibility unknown | The specification's "affected work remains stale or blocked" is a real blocking requirement, and nothing implements it | The integration owner confirming or refusing feasibility |

## Commands actually run

Only these. No command was run against any consuming project, and no evaluation was executed.

```text
git -C <assigned worktree> rev-parse HEAD                 # verified c17e758…
git -C <assigned worktree> status --porcelain             # scope check, before and after
git show 4999f31…:<builder path>                          # builder bytes, source-loaded
git show e641797…:<evaluate-expert path>                  # runner interface, graders, cases
git show c17e758…:<governing input path> | sha256sum      # pin verification, eleven inputs
sha256sum <governing input path>                          # working-copy comparison
date -u                                                   # actual timestamps
/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help
                              devforge expert --help, delivery --help,
                              expert prepare --help, expert status --help,
                              check --help, status --help, verify --help
python3 -B <scratchpad>/run_cases.py --help               # the frozen runner's own help
python3 -B  (author-side schema check of evals/cases.jsonl; stdlib only)
python3 -B  (author-side link-resolution and package-hygiene checks; stdlib only)
```

The `devforge` help output came from a locally built development binary reporting
`devforge 0.1.0`, sha256 `835c32639c0a7df270fe1b9182580f14fc7d0874d3aad1b4037ba7cf420b2b07`.
Reading `--help` establishes which subcommands that build exposes. It is not evidence that
any command was run against a project, nor that any consuming project has that binary.

**The frozen case runner was not executed against this package's cases.** Producing
observations is the independent evaluator's work, and a run by the author would be exactly
the self-grading the builder forbids. `evals/cases.jsonl` was checked for *schema* only, by an
author-side stdlib script that reproduces the runner's documented rules: one JSON object per
line, no duplicate JSON keys, no duplicate `case_id`, only the ten permitted case keys and
seven permitted assertion keys, a non-empty `assertions` list per case, only the ten known
grader names or `null` with a `routed_to`, and every `files` entry existing inside `evals/`.
Twelve cases, no schema errors. That check establishes the file would be accepted as input; it
establishes nothing about the candidate.

## Evaluation dependency

`evals/cases.jsonl` is authored against the schema of the Claude `devforge-evaluate-expert`
package at commit `e641797eebf04cd1e8eb9f711549e038e7745407` in
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910`. Read at
that revision: `scripts/run_cases.py` (its `--help`, and its case and assertion key
validation), `scripts/graders.py` (the ten grader names and their argument shapes),
`references/runner-interface.md`, and `evals/cases.jsonl` as a worked example.

Consequences recorded in `references/derivation.json`:

- The runner is invoked as
  `python3 -B <installed-skill-root>/scripts/run_cases.py --cases … --candidate … --out …`,
  all paths absolute, `--out` must not exist and must sit outside `--candidate`.
- `--mode installed` is required for the three tier-C cases; they declare `mode`, and an
  assertion in a case whose declared mode differs from the run's is reported
  `INDETERMINATE` rather than silently skipped.
- What `--candidate` must point at differs per tier and is not expressible in the schema, so
  each case carries it in `notes`: the installed skill root for C rows, the run workspace root
  (holding a flat `inputs/` copy and `outputs/`) for B rows.
- Six assertions carry `"grader": null` with a `routed_to` value. Those record expectations no
  deterministic check can establish; the runner emits `INDETERMINATE` with the routing, which
  is the honest answer and is deliberately visible.
- That package is itself an unevaluated scaffold. A change to its runner interface, permitted
  keys or grader names invalidates `evals/cases.jsonl` until it is re-authored.

## Corrections made during authoring

Recorded because a clean-looking record that hides its own repairs is less useful than one
that shows them:

- **Resource mentions were converted to markdown links.** The first `SKILL.md` draft named its
  references in backtick code spans, which is not the progressive-disclosure mechanism the
  client documents — supporting files load on demand when referenced by a markdown link. Six
  links in `SKILL.md` and five in `references/recording-rules.md` now resolve; two more were
  added to `references/impact-tracing.md`, which otherwise linked nothing.
- **A literal shell-injection token was removed from `references/sources.md`.** That file
  documents the syntax; the first draft reproduced the exclamation-plus-backtick token inside a
  code span. Since a reference is loaded as skill content when its link is followed, the token
  is now described in words instead. No such token exists anywhere in the package.
- **A fenced `text` command example was added to `references/cli-boundaries.md`.** Commands
  otherwise appear only as inline code identifiers inside table cells, which cannot carry a
  fence.

## Unresolved items for the coordinator

1. **Two enforcement requirements have no implemented check.** R1 (a change-request may not be
   consumed as the basis for a revision while a required field is empty, holds a placeholder,
   or declares an unresolvable upstream entry) and R2 (affected work stays stale or blocked
   until the required new evidence exists). Five specific missing integrations are enumerated
   in `references/cli-boundaries.md`. Both are routed to the integration owner with feasibility
   **unknown**; R2 is recorded as "Enforcement requested; not confirmed available", since
   `devforge expert status` covers one bound expert and its scope does not reach stories,
   contracts, reports, candidates or installed skill copies.
2. **Six of the nine consumers the specification names are not implemented** in this provider:
   define-product, design, prototype, architect, plan, release. Their absence is handled as a
   capability gap in `references/impact-tracing.md` rather than by installing a stub. The
   dated installed-inventory statement in that file goes stale as soon as another Claude skill
   is added.
3. **The runner dependency is a moving target.** `e641797` is the pinned revision; that package
   is under active authoring in its own worktree and is itself unevaluated.
4. **Three coverage gaps in the spec mapping are stated rather than closed:** declined-change
   retention has no dedicated eval case; the `evidence` versus `upstream` distinction has no
   deterministic assertion; interruption and resume is covered only indirectly. See
   `spec-mapping.md` § Coverage gaps.
5. **No upstream artifact was mutated and no refresh was performed.** This is a change skill
   that routes to owning skills; nothing in `docs/mvp`, `package-index.json`, the roster, the
   sibling skills, the manifests, the hooks or the agents was touched, and no claim is made
   that any of them was refreshed.
6. **Every tier is NOT_RUN.** Tier C needs an actual installed copy in a project where
   `docs/mvp` is unreachable; tier B needs a run workspace and a `without_skill` arm; tier A
   needs a fresh terminal. None was arranged. Behavioural status: `NOT_EVALUATED`.
