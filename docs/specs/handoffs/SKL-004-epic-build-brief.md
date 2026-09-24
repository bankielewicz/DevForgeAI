# Build brief: epic skill (SKL-004)

**For a fresh Claude Code session.** Everything you need is in this repository; `CLAUDE.md` applies.

| | |
|---|---|
| Implements | `docs/specs/spec/SPEC-004.md` (version 1) |
| Story | `docs/specs/story/STORY-005.md` (version 1) |
| Process | `docs/specs/adr/ADR-001.md` (accepted, v4); ADR-002 (accepted) |
| Consumes | SPEC-003 §4 (readiness) and §5 (downstream contract); SPEC-002 §5 (priority and release) |
| Branch / worktree | `story/STORY-005-epic` / `.claude/worktrees/story-005-epic` |
| Produces | Skill `epic` in plugin `devforgeai`, invoked as `/devforgeai:epic PRD-NNN` |

## 0. Before the session (done by the user in the main checkout)

```bash
git pull --ff-only
git worktree add .claude/worktrees/story-005-epic -b story/STORY-005-epic main
W=.claude/worktrees/story-005-epic
[ -d "$W/src/claude/DevForgeAI" ] \
  && test -z "$(find "$W/src/claude/DevForgeAI" -type l)" \
  && mkdir -p "$W/.claude/skills/devforgeai" \
  && rsync -a --delete --exclude=/evals/results/ "$W/src/claude/DevForgeAI/" "$W/.claude/skills/devforgeai/" \
  && diff -r -x results "$W/src/claude/DevForgeAI" "$W/.claude/skills/devforgeai" && echo deployed
claude --worktree story-005-epic -n story-005-epic
```

Start the session only after the deploy prints `deployed`.

## 1. How to build

Build it the way SKL-001 to SKL-003 were built: follow the spec directly, not `/skill-creator:skill-creator`
or `/plugin-dev:create-plugin`. The `plugin-dev:skill-reviewer` and `plugin-validator` agents may review
the result, but SPEC-004 wins any conflict. Follow the conventions of the built `brainstorm`, `prd` and
`architecture` skills.

## 2. Read in this order

1. SPEC-004 (authoritative): the §4 current-ARCH, readiness and selection rules, BEH-01…12, ERR-01…07,
   QR-01…03, VER-01…13, and the §9 shared fixture table.
2. STORY-005: AC-01…11.
3. SPEC-003 §4 and §5, and the architecture skill's `references/readiness.md`: the readiness rule you consume.
4. ADR-001 (process) and ADR-002 (the step).
5. `src/staging/templates/epic.md` and README §1–§2; `src/schemas/epic.schema.json`, `arch.schema.json`,
   `adr.schema.json` and `prd.schema.json`.
6. Memory: `project-status`, `skill-build-learnings`, `plugin-eval-quirks`, `verification-evidence-discipline`,
   `doc-editing-lessons`, `decisions-vs-mechanics`, `moscow-priority-vs-release` and `cmux-read-other-panes`.

**Precedence:** SPEC-004 > STORY-005 > ADRs > templates. If something is contradictory or missing, stop and
ask with a recommended fix. Don't edit specs, stories, the PRD, epics or ADRs without the user's explicit
approval, and when you do, apply the version and link updates in the same change.

## 3. Deliverables

All deliverables go under `src/claude/DevForgeAI/`:

| Path | Content |
|---|---|
| `skills/epic/SKILL.md` | Frontmatter as in SPEC-004 §5, with `metadata.devforgeai-version` equal to `provenance.yaml`'s `version`. The body follows the skill template. At most 500 lines, and no author comments left |
| `skills/epic/provenance.yaml` | `SKL-004`, `version: 1`, `implements` SPEC-004 v1, `skill_name: epic`, `eval_tag: epic`, `status: draft` |
| `skills/epic/assets/epic.md` | **Moved** with `git mv` from `src/staging/templates/`. Update the README rows |
| `skills/epic/references/selection.md`, `output-rules.md` | From SPEC-004 §4, BEH-03 to BEH-10, and the epic schema |
| `evals/epic/<case>/` | One case per automated VER. Cases are tagged `epic` and `ver-NN` |
| `plugin.json` | Version raised to 0.4.0 |

| Case | VER | Fixtures |
|---|---|---|
| `selects-ready-current` | ver-01 | The shared fixture (SPEC-004 §9). The prompt asks for one epic covering everything eligible |
| `blocked-not-included` | ver-02 | As `selects-ready-current` |
| `reports-left-out` | ver-03 | As `selects-ready-current` |
| `orders-by-priority` | ver-04 | Shared fixture. The prompt asks for one epic per priority level |
| `no-arch-hands-back` | ver-05 | Shared PRD and ADRs, no ARCH |
| `stale-arch-stops` | ver-06 | Shared fixture with the ARCH's PRD link at version 1 |
| `existing-epic-not-duplicated` | ver-07 | Shared fixture plus an existing EPIC-001 (version 1, a sentinel line) refining FR-002 |
| `draft-inputs` | ver-08 | Shared fixture with PRD-001 at status draft |
| `unconfirmed-grouping` | ver-09 | Shared fixture. The prompt says to proceed without questions and gives no grouping |
| `hands-off-to-story` | ver-10 | As `selects-ready-current` |
| `ignores-unrelated-request` | ver-11 | None |
| `records-provenance` | ver-12 | As `selects-ready-current` |

Write every fixture fresh and check it against its schema. Runs are non-interactive: put every answer in the
prompt, and file graders need literal paths. Grade selection on the **written epic files**; the reply is
secondary. Prefer regex graders; if you need an llm judge, test it blind offline first (neutral IDs, shuffled
order, answers hidden).

**The one permitted change outside the new skill.** Shipping this skill makes the architecture skill's
`hands-off-to-epic` case (SPEC-003 VER-10) fail, because it expects "not built yet". SPEC-003 is approved,
so propose the change and get Bryan's explicit approval before making it: SPEC-003 v7 changes VER-10 so the
handoff names `/devforgeai:epic PRD-001`, and a grader that doesn't depend on whether the skill exists; the
graders in `evals/architecture/hands-off-to-epic/` are updated; SKL-003's `provenance.yaml` link moves to
v7 (SKL-003 keeps its version, since SKILL.md is unchanged). Don't change the architecture skill otherwise.

## 4. Build loop

Deploy after every change to `src/` (step 0's snippet, run from the worktree root with `W=.`), run
`/reload-plugins`, then validate:

```bash
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai
for f in src/claude/DevForgeAI/skills/*/assets/*.schema.json; do [ -e "$f" ] || continue; cmp -s "$f" "src/schemas/$(basename "$f")" || echo "SCHEMA DRIFT: $f"; done
claude plugin validate .claude/skills/devforgeai --strict
```

The user runs evals from a **plain terminal** in the worktree root. **State the estimated cost before each
paid run**: roughly $27 for the `epic` tag run (12 cases × 3 runs × 2 arms) and roughly $95 for the
full-plugin run (52 cases).

```bash
claude plugin eval .claude/skills/devforgeai --tag epic --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
claude plugin eval .claude/skills/devforgeai --allow-tools Write Edit --scaffold --no-publish --threshold 0.8   # before the PR: no regression
```

To iterate cheaply on one case: `--case <name> --runs 1 --ablation none`. To diagnose a failure, add
`--keep-temp`, which keeps the reply in `/tmp/claude-eval-*/out/trace.jsonl`.

## 5. Manual checks (VER-13)

- Run each check in its own scratch fixture copy (a git repo with an initial commit, fixtures schema-checked
  first) with `claude --plugin-dir <worktree>/.claude/skills/devforgeai`. Never run them in the worktree, and
  never reset a copy between checks.
- After each check, save the transcript, `git status --porcelain --untracked-files=all` and `git diff`.
  Confirm the plugin path from the transcript's "Base directory for this skill" line; `/skills` doesn't show it.
- Record who answered the questions. If the build session drives the checks on Bryan's instruction, say so;
  names in the fixtures are test data.
- (g) runs on this repository's own PRD-001, in a copy of the repository, not in the main checkout.

## 6. Evidence discipline (lessons from STORY-003)

- **A failure stays a failure.** If wording can't fix a behavior after two rounds, stop, record it as failed,
  and propose deferring it to a named story. Never relabel it a "known limit" or a pass.
- Keep confirmed causes apart from unknown ones. A passing rerun doesn't erase an earlier failure.
- Record the Claude Code version with every run.
- Keep an evidence archive outside the repository, `~/devforgeai-evidence/STORY-005/`, with the result
  folders, transcripts and reports, and write its `MANIFEST.sha256` last.
- Delete eval sandboxes only by exact path, never with a wildcard; they hold the account profile.
- Don't use `git stash`. Before writing records, check `git log` for commits the lead session made.

## 7. Don't

- Don't write stories, plan sprints, modify existing epics, resolve policy, or call any `devforgeai` command.
- Don't write validator scripts into the repository, and don't start the `devforgeai` CLI.
- Don't modify the brainstorm, prd or architecture skills, except the approved SPEC-003 VER-10 change above.
- Don't create symlinks under `src/`. Skill resources resolve inside the skill or plugin.
- Don't push, open a PR or merge without asking the user.

## 8. Done when

- [ ] The deliverables exist, and the template was moved, not copied.
- [ ] `diff` is clean, the schema-copy loop prints nothing, and `validate --strict` passes.
- [ ] Every epic case scores at least 0.8 over 3 runs, with its delta reported, and the full-plugin run shows
      no regression, including the updated `hands-off-to-epic` case.
- [ ] VER-13 is done and recorded, with (h) marked as a reading check.
- [ ] Every commit references `STORY-005`.

## 9. Report back

- A table of VER-01…13 with the score and delta, or the manual result, and the Claude Code version.
- The eval report paths, and every individual grader failure.
- Deviations from the spec, proposed spec changes, and open questions.
- The ambiguity list: the question, what you checked, what depended on it, and whether it interrupted work.

## 10. After this build

Next is the **story** workflow, `/devforgeai:story EPIC-NNN`. It consumes SPEC-004 §5's downstream contract:
the epic's `DW-NN` IDs and `refines` links.
