# Authoring notes — devforge-release (Claude), SKILL-011 scaffold

Session: 2026-09-10 UTC, 19:40 to 20:05 observed via `date -u`. Worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-release-20260910`, branch `author/claude-devforge-release-scaffold-20260910`, HEAD verified at `c17e758417da64928a0f47fc2600304465ac3f3c` with a clean working tree before any write.

Write fence observed: `providers/claude/plugins/devforgeai/skills/devforge-release/**` and `docs/skill-authoring/history/claude-scaffolding-20260910/devforge-release/authoring/**`. Nothing outside it was created, edited or deleted.

**Validation status: Not performed.** Tiers A, B and C are all `NOT_RUN`. Nothing was installed, exported, bound, activated or evaluated.

## The builder that was followed

The Claude `devforge-project-expert-creator` package was **source-loaded**: its bytes were read by absolute path from Git at a pinned commit and its process was followed by this author. It was not installed, not invoked as a skill, and no builder or evaluator agent was called.

Read from the sibling worktree `/home/bryan/Projects/DevForge/worktrees/claude-scaffold-project-expert-creator-20260910` at commit `4999f3106565c5e320d1f1a7db066b437e4e94be`, under `providers/claude/plugins/devforgeai/skills/devforge-project-expert-creator/`:

| File | sha256 at that commit |
| --- | --- |
| `SKILL.md` | `342b82923e64cef0c2ab77fdb8fc11b92fc68ea145642c486d2a937c5363f3d9` |
| `references/framework-context.md` | `884d915f6b65f11540283ee3ed241d2e33cd54c24d22d93e51e3496d49501c66` |
| `references/existing-skill-selection.md` | `89a070c3fbee10a8bce513101a0dd50bbfaec431fd3056fddc8d3113e5b933df` |
| `references/interview-guide.md` | `0157e51472cbf206b73d818e0243708906496ab8d72a9b1cbefd7cfab3134d76` |
| `references/manual-operation.md` | `3b3eb092033239bd8f20f0eb1d087b810cbd87fd641225531b15abc02b3b572c` |
| `assets/skill-design-spec.md` | `715ef3bdf9082ace4c3b3eeda27e8bf9e4663355bcebed2f5d997fefc5a26ef9` |
| `assets/handoff.md` | `d741d4dfadbb37353f5542dbb825ab7df9bbdb7be10e4380e262f54e0f663790` |

That worktree's HEAD is ahead of the pinned commit by coordinator evidence commits (`b7e7152`, `8c0bdd0`). Every byte above was read with `git show 4999f31:<path>` rather than from the working tree, so the drift did not reach this authoring.

**The builder is itself a draft under independent review.** Its E1 bootstrap review was revise-bounded and its repairs F-001 through F-004 were applied at the pinned commit; a focused recheck of the same commit exists at `8c0bdd0`. It has had no native evaluation. Following its process establishes that its process was used - nothing about whether it, or this package, works.

Its five phases were run in order:

- **Intake** — recovered the specification, both templates, four contracts, the roster, the sibling specifications, the Claude conventions exemplar, the built CLI's command surface, and the pinned evaluation runner. No user was asked to restate anything already on disk.
- **Selection** — searched the Claude provider inventory at base and in the worktree; recorded the result, the scope and the limits (below, and in the design document section 9). Decision: **create**.
- **Design** — `assets/skill-design-spec.md` copied out and filled at `design/skill-design-spec.md`, never in place inside the builder package. **No questions were asked**, per this assignment: every material decision was recovered from the specification, templates and contracts, and every silence was recorded as a labelled proposed default.
- **Authoring** — the package, written against the design document rather than the other way round.
- **PreparedTransfer** — `file-manifest.json`, this file, `spec-mapping.md`, and `handoff.md` to an independent evaluator.

## Selection: what was searched, and what that does not establish

Searched by direct listing, both at base commit `c17e758` and in the worktree:

- `providers/claude/plugins/devforgeai/skills/` — `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator`, `devforge-review`. No `devforge-release`.
- `providers/codex/plugins/devforgeai/skills/` — those four plus `devforge-evaluate-expert`. No `devforge-release`, so there was no Codex package to port from. This is original authoring, not a port.
- The destination directory, for a collision: absent.

Not searched, and therefore **not** claimed empty: `~/.claude/skills`, any managed settings directory, any `--add-dir` directory, any exported plugin tree, any consuming project's `.claude/skills`. Inspection was of names, descriptions and instructions only; nothing was run, installed or tested.

The honest result: **no suitable skill found in the searched inventory.** Not "no such skill exists".

## Decisions recovered from the sources

Settled by the specification or by an observed fact, not by this author: the four workflow phases and their exit conditions; the four-row input table and its consume-only restriction; the `REL` prefix and the release-record template; the five acceptance cases and the four common cases; the near-miss owners (`devforge-review`, `devforge-develop`, `devforge-change`); the fixed result vocabulary; the fixed train/validation trigger split; which CLI commands may be named.

## Proposed defaults, where the sources were silent

Every one of these is a **proposal**. None was approved, and silence is not approval.

| Item | Proposed default | Why |
| --- | --- | --- |
| Artifact destination | `docs/devforge/releases/`, handoffs `docs/devforge/handoffs/` | The artifact contract's suggested project directories. A selected destination or a project's own accepted map outranks it, and `SKILL.md` says so. |
| Description length | ~1,000 characters, no `when_to_use` | Claude Code truncates `description` plus `when_to_use` at 1,536 characters combined. Authored length: **1,027**. |
| Invocation policy | Automatically when relevant, and explicitly by name | The specification is silent; both are ordinary for a Claude skill. |
| `scripts/` | None | Nothing in this workflow is a repeated deterministic operation, and the language policy confines framework logic to Rust. The permitted Python exception already exists in the evaluate-expert package as an evaluation input. |
| Reference layout | Two workflow references (`recording-rules.md`, `delivery-actions.md`) plus `derivation.json` and `sources.md` | The specification names no layout. Kept to what the four phases actually need. |
| Tier-B baseline | `without_skill` | No prior Claude `devforge-release` exists, so nothing can serve as `old_skill`. |
| Fixture project | Synthetic "Foldbench" | Fixtures must be reproducible from source and must not describe a real project. Every fixture is labelled synthetic and no digest inside one was computed from anything. |
| Codex line in the copied template | Kept byte-exact; not rewritten | The template is governed outside this fence. Open item for its owner, below. |

## Deviations from the builder, and why

- **No Q&A round.** The builder's Design phase expects one to three questions per round for material gaps. This assignment directed the author to ask none and to record proposed defaults instead. Every gap that would have been a question is a labelled proposal in the table above and in the design document's section 9.
- **No expert-specification (XSPEC) or expert-package record (XPKG).** Those are the builder's own outputs for a *project expert*. The artifact this assignment produces is a framework skill package, whose identity record is `file-manifest.json` and whose design record is the filled design document. Maintaining an XSPEC alongside them would be the second independent design the builder's artifact mapping prohibits.
- **`references/validator-handoff.md` not consulted for content.** It governs a bounded repair from an evaluator's findings. There are no findings; section 11 of the design document is `NOT_APPLICABLE`.

## Commands actually run

Read-only inspection, plus the writes inside the fence. Nothing was installed, exported, bound, activated or deployed, and no external action of any kind was performed.

```text
git -C <release worktree> rev-parse HEAD                 -> c17e758417da64928a0f47fc2600304465ac3f3c, clean
git -C <builder worktree> show 4999f31:<path>            -> builder bytes, seven files
git -C <evaluate-expert worktree> show e52ac59:<path>    -> runner, graders, cases.jsonl, runner-interface.md
git ls-tree c17e758 providers/claude/.../skills/         -> the four-entry inventory
sha256sum <governing inputs>                             -> digests, verified against the same paths at base
framework/DevForge/target/debug/devforge --help          -> the command surface
framework/DevForge/target/debug/devforge {verify,status,check,accept} --help  -> leaf flags
python3 <pinned runner> --help                           -> the runner interface
```

### The only execution: a schema-load check, run twice

```text
python3 <scratchpad>/ee/scripts/run_cases.py \
  --cases    <package>/evals/cases.jsonl \
  --candidate <package> \
  --out      <scratchpad>/observations.jsonl
```

Run twice against the runner and graders committed at `e52ac596cbf790dfa156d883852d392c512fdbcc`, extracted read-only into a scratchpad outside both repositories: at 2026-09-10T20:02:30Z, and again at 2026-09-10T20:15:25Z after `references/derivation.json` was corrected, to confirm the final bytes still load. Both runs: exit status **0**, ten case records written, identical rows. The observations files stay in the scratchpad and are not evidence for anything beyond the load check.

**What this was for, and what it was not.** It checks that the authored case file loads: valid JSONL, no duplicate `case_id`, no unknown grader, every `candidate_subpath` resolving. Exit 1 would have meant the deliverable is malformed. That is the whole claim.

It is **not an evaluation**, and none of its rows is adopted here as an outcome. The vocabulary is deliberately disjoint from PASS/FAIL, there is no aggregate record, and the exit status describes the program rather than the package. Tier C stays `NOT_RUN`, because a source-mode run against the authoring tree is not an installed-resource observation. For the record, and as observations only: the seven deterministic cases completed; REL-C-005 and REL-C-007 returned `MISMATCH`, which is the observation those two fixtures were authored to produce; REL-C-002 returned `INDETERMINATE` because it declares `installed` mode and the run was `source`; the three routed cases returned `INDETERMINATE` with their routing, which is the honest answer.

### Scans

```text
grep -rn "/home/"     <package>   -> none (see the correction below)
grep -n  "^!"         SKILL.md    -> none
grep -n  '`!'         SKILL.md    -> none
grep -rn "docs/mvp"   SKILL.md assets/ references/{recording-rules,delivery-actions}.md -> none
wc -l SKILL.md                    -> 121 lines, against the documented 500-line guidance
python3 -c "json.load(...)"       -> derivation.json, evals.json, trigger-queries.json all parse
```

The first scan initially found four developer home paths in `references/derivation.json`, recorded there as provenance for the builder worktree, the framework checkout, the CLI binary and the evaluate-expert worktree. They were rewritten as workspace-relative paths with a `path_convention` note, because a package must carry no developer home directory. The absolute paths survive in this file, which sits outside the package.

## Unresolved items for the coordinator

1. **The Codex line in the shared release-record template.** `docs/mvp/templates/devforge-release/release-record.md` carries "Model-driven Codex GitHub Action: deferred for the subscription-only MVP; its documented setup requires an API key." The assignment says no Codex-only concepts; the same assignment says copy the governing template. Resolution taken: copy byte-exact, record `transformation: none` in `derivation.json`, raise it here. The template's owner decides whether the shared wording should be provider-neutral. It is echoed once more, in the `good/REL-008.md` fixture, for fidelity to the template it fills.
2. **The runner dependency is pending.** `evals/cases.jsonl` is written to the schema of the runner and graders at `e52ac596cbf790dfa156d883852d392c512fdbcc`. That package is a draft; an independent E2 bootstrap review of that same commit exists at `b6a4bf7` in its worktree and a repair pass is in progress on that branch. A repair that changes the case schema, the grader names or the `expect` handling would invalidate this case file. It is installed nowhere.
3. **Four enforcement requirements with no implementation.** R1 (candidate-to-review identity binding), R2 (authority per external action), R3 (no outcome row without a readback), R4 (no dependent write into another writer's fence). Recorded in the design document section 5 with owner, evidence, intended allow/refuse behaviour and feasibility. No DevForge predicate covers any of them, and none is described in the package as active enforcement.
4. **`devforge-change` is named as a routing owner and does not exist.** The specification's consumer edge is `release-record -> change`. `SKILL.md` names it as a capability gap rather than as an installed target, and instructs a plain-language next task where it is absent.
5. **Two acceptance behaviours have no eval case**: interruption-and-resume, and post-release operational failure. Both are covered in `SKILL.md`; neither can be staged honestly in a single-turn case. Recorded in `spec-mapping.md` under "Gaps in this mapping".
6. **Nothing observed about the client.** No Claude Code version was queried and no client behaviour was observed. The invocation and discovery claims in `references/sources.md` come from the published documentation, retrieved 2026-09-10, and are labelled as such.
7. **The CLI binary's digest was not pinned.** `references/delivery-actions.md` describes the command surface of the build at `framework/DevForge/target/debug/devforge` as observed on 2026-09-10. The binary's own digest was not recorded, so that observation binds a path and a date rather than exact bytes.
