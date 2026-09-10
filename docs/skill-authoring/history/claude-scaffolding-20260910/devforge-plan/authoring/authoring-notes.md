# Authoring notes — devforge-plan (SKILL-006), Claude scaffold

Author: an AI assistant working under the coordinator packet
`/home/bryan/Projects/DevForge/tmp/claude-remaining-skills-scaffolding-20260910/packets/author-devforge-plan.md`.
Session window observed with `date -u`: first timestamp `2026-09-10T19:34:37Z`, package manifest recorded
at `2026-09-10T20:03:26Z`. Every timestamp in this pass is an observed `date -u` value; none is a
date-only placeholder.

Worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-plan-20260910`, branch
`author/claude-devforge-plan-scaffold-20260910`. `git rev-parse HEAD` returned
`c17e758417da64928a0f47fc2600304465ac3f3c` and `git status --porcelain` was empty before any write.

## The builder, and what following it actually means

The assignment named a frozen builder and it was **source-loaded**: read by absolute path from its own
worktree at a pinned commit, and followed as instructions. It was not installed, not discovered, and not
invoked as a skill. Nothing in this pass is evidence that the builder works.

Files loaded, all via
`git -C /home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910 show 4999f31:<path>`
so that the committed bytes were read rather than a working tree that may still be moving:

| Absolute source | Package-relative path at 4999f31 | SHA-256 |
| --- | --- | --- |
| `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910` @ `4999f3106565c5e320d1f1a7db066b437e4e94be` | `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` |
| same | `.../references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| same | `.../references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| same | `.../references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| same | `.../references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| same | `.../assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| same | `.../assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |

**The builder is a draft under independent review.** Its E1 bootstrap review was revise-bounded against
its candidate-1 bytes, and repairs F-001 through F-004 were applied at `4999f31`. It has had no native
evaluation. Its own `derivation.json` records the superseded candidate-1 SKILL.md digest
`1e9929a5713de1df05e2b0bbafdc49de388e74104e584f4ec77c237c35362a0e` preserved at commit `69b6090`, and
notes that findings recorded against those bytes do not transfer to the changed ones.

The builder's own package assets were **not** shipped into `devforge-plan`. `assets/skill-design-spec.md`
is the builder's authoring template; it was copied to this authoring directory and filled there, per its
own instruction never to fill it in place. `devforge-plan` ships only the resources its own workflow
needs.

Its five phases were run for a framework skill rather than a project expert:

| Builder phase | What was actually done |
| --- | --- |
| Intake | Recovered SKILL-006, the two output templates, the shared handoff template, the four contracts, the roster, the package index and the observed CLI surface before writing anything |
| Selection | Searched the assigned Claude inventory and, read-only, the Codex inventory at base. No `devforge-plan` in either. Result recorded as **create**, with the searched and unsearched locations both named |
| Design | Filled `design/skill-design-spec.md` from the governing sources. **No questions were asked** — the assignment prohibits them — so every gap the sources leave is a labelled proposed default |
| Authoring | Wrote `SKILL.md`, three references, three assets, and the evals |
| PreparedTransfer | `file-manifest.json`, this note, `spec-mapping.md` and `handoff.md`; no receiver invoked |

## Selection: what was searched, and what was not

Searched at base `c17e758417da64928a0f47fc2600304465ac3f3c` by reading directory names and `SKILL.md`
frontmatter, then the plausible candidates' instructions. Nothing was executed or installed.

- `providers/claude/plugins/devforgeai/skills/` — `devforge-brainstorm`, `devforge-develop`,
  `devforge-project-expert-creator`, `devforge-review`. No `devforge-plan`.
- `providers/codex/plugins/devforgeai/skills/` (read-only, lineage only) — the same four plus
  `devforge-evaluate-expert`. No `devforge-plan` to port.
- `docs/mvp/package-index.json` SKILL-006 entry — `implementations.claude.source: null`,
  `status: NOT_IMPLEMENTED`, `native_behavior: NOT_EVALUATED`; Codex identical. Read-only; not modified.
- Destination `providers/claude/plugins/devforgeai/skills/devforge-plan/` — did not exist. No collision.

**Not searched, and therefore not claimed empty:** `~/.claude/skills/`, any managed settings directory,
any `--add-dir` directory, any consuming project's `.claude/skills/`, any exported plugin outside this
repository, and the `.agents/skills` Codex installation tree. The comparison covered instructions and
metadata only. The honest result is *no suitable skill found in the searched inventory* — not that none
exists.

## Decisions, and the proposed defaults where the sources are silent

The design spec §9 table carries all of these. The ones a reviewer should look at first:

| Decision | What was chosen | Basis | Status |
| --- | --- | --- | --- |
| Workflow item classification (W1, P1–P4, T1–T5 required; T4 and T6 optional) | Derived from SKILL-006's phase-exit table and its statement that sprint grouping is optional | Specification | **Proposed** — no user answered the optional-or-required question |
| Default output destinations | `docs/devforge/epics/`, `docs/devforge/stories/`, `docs/devforge/handoffs/` when nothing was selected | Artifact contract's suggested map | **Proposed default** |
| Invocation policy | Automatic when relevant plus explicit by name; no `paths` restriction, no `disable-model-invocation` | SKILL-006 requires an indirect-activation observation, which a restricted package could not produce | **Proposed default** |
| Three references, no more | `recording-rules`, `upstream-resolution`, `readiness-check` — one per conditional body of detail the phases need | Authoring judgement against the progressive-loading rule | **Proposed** |
| No `scripts/` | None authored | No deterministic operation in this workflow justifies one; the runner belongs to `devforge-evaluate-expert` | **Proposed** |
| No managed-runtime section | Omitted deliberately | SKILL-006 requires no managed operation; the brainstorm package's managed section would be an unsupported claim here | Settled by specification |
| Baseline label | `without_skill` on every tier-B case | No `devforge-plan` existed in either provider at base, so `old_skill` has no referent | Settled by observation |
| Templates copied byte-for-byte | `assets/epic.md` and `assets/story.md` are exact copies, verified by digest equality | Keeps refresh mechanical and verification trivial; filling guidance lives in `references/recording-rules.md` instead | Settled |

## The missing integration, stated once and not softened

`devforge --help` (observed `2026-09-10T19:37Z`) lists `delivery`, `expert`, `check`, `init`, `red`,
`green`, `accept`, `verify`, `status`, `isolate`. `devforge check --help` shows `--project --policy
--state --expert` and its own description says it "does not certify semantic behavior".

**No subcommand accepts an epic, a story, a requirement graph or a `devforge.artifact/v1` envelope.**
SKILL-006 assigns deterministic graph and provenance checks to DevForge; that capability does not exist.
So the package names no DevForge command as a planning gate. The requirement is recorded three times, in
the form the builder's interview guide prescribes — as enforcement routes R1, R2 and R3 in the design
spec §6, each with the protected action, the observable evidence, the intended allow/refuse behaviour,
the recovery message, the integration owner, feasibility unknown, and the status **"Enforcement
requested; not confirmed available."**

No command was executed against any project during this authoring. Naming one is not evidence of
running it.

## Commands actually run

Read-only inspection, plus writes inside the fence. Nothing was installed, exported, bound, evaluated or
committed outside the assigned worktree.

| Command | Purpose |
| --- | --- |
| `date -u +%Y-%m-%dT%H:%M:%SZ` | Every recorded timestamp |
| `git -C <plan-worktree> rev-parse HEAD` / `status --porcelain` / `branch --show-current` | Verify the assignment before writing |
| `git -C <expert-creator-worktree> show 4999f31:<path>` | Read the frozen builder's committed bytes |
| `git -C <evaluate-expert-worktree> log --oneline` / `ls-tree` / `show e52ac59:<path>` | Read the runner dependency's committed bytes |
| `git -C <DevForgeAI> ls-tree -d --name-only c17e758 <provider skill dirs>` | Selection search at base |
| `sha256sum` on the governing specification, templates and contracts | Verify the digests the packet supplied and record the rest |
| `python3 <extracted run_cases.py> --help` | Read the runner's real interface rather than inferring it |
| `/home/bryan/Projects/DevForge/framework/DevForge/target/debug/devforge --help`, `check --help`, `expert --help` | Establish the real command surface |
| WebFetch `https://code.claude.com/docs/en/skills` | Client facts recorded in `references/sources.md` |
| `python3` one-liners over the authored package | The static self-checks below |

## Static self-checks, and exactly what they are not

These confirm that my own writes landed and parse. They are authoring operations. **None of them is a
tier result, and no observations file exists.**

| Check | Result |
| --- | --- |
| `SKILL.md` frontmatter parses under the restricted reader from `graders.py` @ `e52ac59`; keys are exactly `name` and `description` | parsed; `name=devforge-plan`; description 897 characters, well inside the documented 1,536-character listing cap |
| `SKILL.md` body length against the documented 500-line recommendation | 248 lines |
| Every Markdown link in the package resolves inside the package | 7 local links in `SKILL.md`, 1 in `references/sources.md`; all resolve. Only two external URLs, both in `sources.md` |
| No developer home path anywhere in the package | `grep -rn '/home/' <package>` returns nothing |
| No `docs/mvp` runtime dependency | `grep -rn 'docs/mvp' <package> --include='*.md'` returns nothing |
| No `!`-prefixed shell-injection syntax in Markdown | none; the two command examples are in ```text fences |
| `evals/evals.json`, `evals/triggers/trigger-queries.json`, `references/derivation.json` parse as JSON | all parse |
| `evals/cases.jsonl` — every line parses, no duplicate `case_id`, every grader name is in the `GRADERS` registry at `e52ac59` | 17 cases, all valid |
| Fixture field lists match the fixtures | `required_report_fields` was called directly on each fixture the cases name. The conforming fixtures return complete; `draft-placeholder/STORY-009.md` returns the placeholder observation the case expects, naming the field and line |

The last row deserves a boundary statement. `graders.py` was imported and its functions called directly
on files I had just written, to confirm a field list I authored actually matches a fixture I authored.
`run_cases.py` was **not** run: it produces observations, and producing observations about this candidate
is the evaluator's work, not the author's. A `MATCH` from a grader is an observation about one assertion.
It is not `PASS` for a required check, it is not tier C, and it is not recorded as either anywhere in
this package.

## Dependency: the case runner and graders

`evals/cases.jsonl` is written to the schema of the Claude `devforge-evaluate-expert` package at
**commit `e52ac596cbf790dfa156d883852d392c512fdbcc`**, in worktree
`/home/bryan/Projects/DevForge/worktrees/claude-scaffold-evaluate-expert-20260910`.

| File at e52ac59 | SHA-256 |
| --- | --- |
| `.../devforge-evaluate-expert/scripts/run_cases.py` | `d1fb18689eeea31f8facde4e3de1507320e74ffb349f547f9db2201395bb132d` |
| `.../devforge-evaluate-expert/scripts/graders.py` | `7c03e7b2137787035c995787b232a7bf8d801c88672675bacf4359a8cdb38c13` |
| `.../devforge-evaluate-expert/references/runner-interface.md` | `a58c35dab0fdb68d3a7dea92bf761a1e4ac25bee89fb49320fb09e247557170b` |
| `.../devforge-evaluate-expert/evals/cases.jsonl` | `b4b0c9314f43aa4aebaeee7f25c4d5e4b81fc2b0e628d98e3505c91679cb1f83` |

**Status: pending and unmerged.** That package is a candidate on branch
`author/claude-devforge-evaluate-expert-scaffold`; commit `b6a4bf7` on the same branch records an E2
independent bootstrap review of the `e52ac59` bytes, and a repair pass was in progress while this was
authored. The committed `e52ac59` bytes were read deliberately rather than the moving working tree. **If
those scripts change, `evals/cases.jsonl` must be rechecked against the new grader registry and case
schema before anyone runs it.**

Ten graders exist at that revision: `frontmatter_present`, `frontmatter_fields`, `name_folder_relation`,
`package_relative_links`, `path_present`, `path_absent`, `required_report_fields`,
`claim_evidence_binding`, `transcript_completion`, `artifact_side_effect`. Only the eight that fit a
planning package are used; `claim_evidence_binding` and `transcript_completion` are shaped for
evaluation-report and activation-transcript fixtures this package does not produce.

**Two invocation groups, because `--candidate` takes one root.** Running everything in one invocation is
not possible and a partial run is visible in the output, since unselected cases appear as `SKIPPED`:

```text
group 1 - the installed package itself
  --candidate <installed devforge-plan root>  --mode installed
  --case-id PL-PKG-001 --case-id PL-PKG-002

group 2 - the fixtures
  --candidate <skill source>/evals/fixtures
  every case except PL-PKG-001 and PL-PKG-002
```

Nine of the seventeen cases carry `grader: null` with a `routed_to` value. The runner reports those as
`INDETERMINATE` with the routing, which is the honest answer: no deterministic check establishes whether
a partition is sound, whether a criterion is falsifiable, or whether a collision was handled. Those are
the independent reviewer's readings.

## Unresolved items and open questions

1. **No planning-artifact capability in the CLI.** R1, R2 and R3 are recorded requirements with
   feasibility unknown. Integration owner.
2. **Seven of eight named siblings do not exist for Claude.** `define-product`, `design`, `prototype`,
   `architect`, `release` and `change` have no source; `evaluate-expert` is an unmerged candidate. The
   skill therefore treats producers and consumers as artifact types and instructs checking what is
   installed before naming any receiver.
3. **Runner dependency unmerged**, as above.
4. **Workflow classifications are proposals.** No user answered the optional-or-required question,
   because the assignment prohibited asking.
5. **`package-index.json` still records SKILL-006 as `NOT_IMPLEMENTED` with a null Claude source.**
   Updating it is outside this fence and is a coordinator item.
6. **`evals/fixtures/README.md` will not survive installation** — `evals/` is stripped from installed
   copies and exports. The synthetic labelling therefore lives where the fixtures live, in source, which
   is where anyone reading them will be.
7. **Nothing behavioural is known.** Tiers A, B and C are `NOT_RUN`. No installation exists, no baseline
   arm was run, and no independent evaluator has seen these bytes.

## What was deliberately not touched

`docs/mvp/**` (specifications, templates, contracts, roster, package index), every sibling Claude skill,
every Codex source, the plugin manifest, `hooks/`, `agents/`, and the companion DevForge repository's
gates, policies, tests and tooling pins. Two worktrees were read at pinned commits and neither was
modified: the builder's, and the evaluate-expert candidate's. No branch was created, switched, reset,
rebased, stashed or cleaned.

**Validation status: Not performed.** **Behavioural status: NOT_EVALUATED.** **Enforcement status:
requirements recorded; no gate implemented by this skill.**
