# Build brief: prd skill (SKL-002)

**For a fresh Claude Code session.** Everything you need is in this repository. Don't assume any
context from earlier conversations. `CLAUDE.md` applies.

| | |
|---|---|
| Implements | `docs/specs/spec/SPEC-002.md` (version 1) |
| Story | `docs/specs/story/STORY-002.md` (version 1) |
| Build and validation process | `docs/specs/adr/ADR-001.md` (accepted, version 3) |
| Consumes | BRNs written by the brainstorm skill (SPEC-001 §5, downstream contract) |
| Branch / worktree | `story/STORY-002-prd` / `.claude/worktrees/story-002-prd` |
| Produces | Skill `prd` in plugin `devforgeai`, invoked as `/devforgeai:prd [BRN-NNN]` |

---

## 0. Before the session (done by the user in the main checkout)

The session checks these and **stops if any is missing**:

1. `main` includes this brief, SPEC-002, STORY-002, EPIC-002, PRD-001 v3, and the updated `src/schemas/prd.schema.json`.
2. The worktree exists, is deployed, and the session was started in it (ADR-001 steps 1–3):
   ```bash
   git worktree add .claude/worktrees/story-002-prd -b story/STORY-002-prd main
   W=.claude/worktrees/story-002-prd
   test -z "$(find $W/src/claude/DevForgeAI -type l)" \
     && mkdir -p $W/.claude/skills/devforgeai \
     && rsync -a --delete --exclude=/evals/results/ $W/src/claude/DevForgeAI/ $W/.claude/skills/devforgeai/
   claude --worktree story-002-prd -n story-002-prd
   ```
   The plugin already contains the brainstorm skill, so deploying **before** starting the session matters.
   Otherwise the session loads the main checkout's copy (ADR-001 step 2).

Opening prompt: *"Read docs/specs/handoffs/SKL-002-prd-build-brief.md and carry it out."*

## 1. Which creator skill to use

As with SKL-001, neither `/skill-creator:skill-creator` nor `/plugin-dev:create-plugin` drives this build:
SPEC-002 already settles the design, and both tools conflict with ADR-001. You may read
`plugin-dev:skill-development` as reference. At the end, run the `plugin-dev:skill-reviewer` and
`plugin-dev:plugin-validator` agents on the operational copy as advisory reviewers. SPEC-002 wins any conflict.

## 2. Read in this order

1. SPEC-002, which is authoritative: BEH-01…14, ERR-01…07, QR-01…03, VER-01…12, the data model and
   mapping in §4, and the frontmatter and downstream contract in §5.
2. STORY-002: AC-01…09.
3. ADR-001: the layout, commands and rules.
4. SPEC-001 §5 and the built brainstorm skill in `src/claude/DevForgeAI/skills/brainstorm/`. It shows
   what a BRN looks like, and how that skill structured `SKILL.md`, its references and its evals.
   Follow the same conventions.
5. `src/staging/templates/README.md` §1–§2, `src/staging/templates/prd.md`, and
   `src/schemas/prd.schema.json`, `brainstorm.schema.json` and `common.schema.json`.

**Precedence:** SPEC-002 > STORY-002 > ADR-001 > templates > anything else. If something is
contradictory or missing, **stop and ask the user**. Don't edit specs, stories, PRD-001, epics or ADRs
unless the user agrees. Propose changes in your report.

## 3. Deliverables

All deliverables go under `src/claude/DevForgeAI/`:

| Path | Content | Implements |
|---|---|---|
| `skills/prd/SKILL.md` | Frontmatter exactly as in SPEC-002 §5. The body follows the skill template: inputs, workflow checklist, steps, decisions that need the user, output contract, references. At most 500 lines, and no `<!-- -->` comments left | BEH-01…14, ERR-01…07, QR-01, QR-02 |
| `skills/prd/provenance.yaml` | `id: SKL-002`, `upstream: [{id: SPEC-002, relation: implements, version: 1, hash: null}]`, `skill_name: prd`, `packaging: plugin`, `plugin: devforgeai`, `eval_tag: prd`, `status: draft`, `generated_by` filled in | QR-02 |
| `skills/prd/assets/prd.md` | **Moved** with `git mv src/staging/templates/prd.md …`. Then update the prd row's link in `src/staging/templates/README.md` | BEH-11 |
| `skills/prd/references/brn-mapping.md` | The §4 mapping, with a short worked example: BRN items in, PRD items with `upstream` links out | BEH-02, BEH-04 |
| `skills/prd/references/interview.md` | The question bank for each round (framing, requirements, quality and constraints, metrics), which NFR categories each stage asks, the batching limits (4 per call, 5 calls), and the constraint-vs-design rule | BEH-03, BEH-05, BEH-07 |
| `skills/prd/references/output-rules.md` | PRD item-block rules, including `stage`, `priority` and `release` as `null` until decided, and the `constraint` category | BEH-12 |
| `evals/prd/<case>/` | One case per automated VER (table below), each with its fixture files and `case.yaml` scaffold | QR-03 |

Eval cases. Each is tagged `prd` plus the tag shown:

| Case | Tag | Verifies | Fixtures placed by scaffold |
|---|---|---|---|
| `writes-prd-from-brn` | `ver-01` | AC-02 | Converged BRN-001: IDEA-01 and IDEA-03 promoted, IDEA-02 parked, IDEA-04 rejected |
| `no-invented-decisions` | `ver-02` | AC-03 | Same BRN. The prompt gives `stage: prototype` only |
| `selects-unprocessed-brn` | `ver-03` | AC-01 | BRN-001 fully cited by PRD-001; BRN-002 not cited |
| `warns-unconverged` | `ver-04` | AC-05 | Draft BRN-001 with ideas still open |
| `stops-without-promoted` | `ver-05` | AC-05 | Converged BRN-001 with no promoted idea |
| `extend-or-new` | `ver-06` | AC-06 | PRD-001 (version 1) and an uncited BRN-002 |
| `hands-off-to-epic` | `ver-07` | AC-07 | Converged BRN-001 |
| `ignores-unrelated-request` | `ver-08` | AC-08 | None. The prompt asks to open a pull request |
| `records-provenance` | `ver-09` | AC-09 | Converged BRN-001 |
| `constraints-not-design` | `ver-10` | AC-04 | Converged BRN-001. The prompt names AWS, Stripe and "leaning towards microservices" |

**Fixtures.** Write every fixture BRN and PRD by hand. Check each one by reading it against its schema,
because no validator exists in the repository. The user hasn't yet decided whether the draft BRN from
STORY-001's manual test may be reused (SPEC-002 §13). Don't use it unless they say so.

**Eval constraints**, from ADR-001, the `claude plugin eval` documentation and STORY-001's experience:
- Runs are non-interactive and start in an empty workspace. Put every answer in the prompt, except
  in cases that test asking or stopping.
- File-content graders use `target: {source: file, path: <literal path>}`, and that path takes no glob.
  Outputs are deterministic, so name them: `docs/specs/prd/PRD-001.md`, or `PRD-002.md` when a PRD fixture exists.
- `file_exists` counts only files created during the run, not scaffold files.
- Prefer regex graders. llm judges are noisy on long files, and `focus: trace` shows only the first and last 12 messages.
- Write and Edit need `--allow-tools Write Edit`. Scaffolds need `--scaffold`.

## 4. Build loop

From the **worktree root**, as in ADR-001 steps 2, 4 and 5:

```bash
# deploy (after every change to src/)
test -z "$(find src/claude/DevForgeAI -type l)" \
  && mkdir -p .claude/skills/devforgeai \
  && rsync -a --delete --exclude=/evals/results/ src/claude/DevForgeAI/ .claude/skills/devforgeai/

# validate what ships
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai
for f in src/claude/DevForgeAI/skills/*/assets/*.schema.json; do [ -e "$f" ] || continue; cmp -s "$f" "src/schemas/$(basename "$f")" || echo "SCHEMA DRIFT: $f"; done
claude plugin validate .claude/skills/devforgeai --strict
```

**Evals run from a plain terminal in the worktree root, not from the session.** Claude Code worktree
sessions refuse any command containing `claude plugin eval`. The user runs them and the session reads
`.claude/skills/devforgeai/evals/results/<timestamp>/aggregate-result.json`:

```bash
# this skill's cases only, while iterating
claude plugin eval .claude/skills/devforgeai --tag prd --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
# single case, cheap
claude plugin eval .claude/skills/devforgeai --case <name> --runs 1 --ablation none --allow-tools Write Edit --scaffold --no-publish
# before the PR: the whole plugin, so the brainstorm suite shows no regression
claude plugin eval .claude/skills/devforgeai --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
```

- After each deploy, run `/reload-plugins`. A session keeps using the `SKILL.md` it loaded at the last reload.
- Run `/plugin` and `/skills` once to confirm that `/devforgeai:prd` and `/devforgeai:brainstorm` both load from the worktree path.
- Edit only `src/`.

## 5. Manual verifications

- **VER-11:** run an interactive session with a BRN that already names the users and a request that
  states the stage. Record:
  - that no question repeated those answers;
  - the size of each batch (at most 4);
  - which NFR categories were asked, compared with the stage rule in BEH-03;
  - that stopping mid-interview offers a draft save.
- **VER-12:** extend a PRD from a second BRN. Check:
  - the version rose by one, numbering continued, and existing items are byte-identical (`git diff`);
  - a Change Log entry was added and the suspect-epics warning appeared;
  - no BRN changed.

  Then try an unknown BRN ID (it must list the available BRNs) and a BRN with a malformed item block
  (it must stop and name the block). Finally, check that `SKILL.md` is within the NFR-001 limits.

## 6. Don't

- Don't write validator scripts into the repository, and don't start the `devforgeai` CLI.
- Don't create symlinks under `src/`. No skill file may reference `src/`, `docs/specs/` or `${CLAUDE_PROJECT_DIR}`.
- Don't modify the brainstorm skill, except to report a problem found through the handoff.
- Don't design architecture in the PRD skill. Constraints only (BEH-07).
- Don't build the epic skill.
- Don't push, open a PR or merge without asking the user first.

## 7. Done when

- [ ] Every deliverable in §3 exists, and `src/staging/templates/prd.md` has been moved rather than copied.
- [ ] `diff -r -x results` is clean, the schema-copy loop prints nothing, and `claude plugin validate --strict` passes.
- [ ] The `prd` eval cases each score at least 0.8 over 3 runs, with the baseline delta reported, and the full-plugin run shows no brainstorm regression.
- [ ] VER-11 and VER-12 are done by hand and recorded.
- [ ] Every commit message references `STORY-002`.

## 8. Report back

- A table of VER-01…12 with score and delta, or the manual result, and pass or fail.
- The paths of the eval reports.
- What `/plugin` and `/skills` showed.
- Deviations from SPEC-002 with reasons, proposed spec changes, and open questions.

## 9. After this build

The next workflow is the **`epic` skill** (`/devforgeai:epic PRD-NNN`). It consumes the PRD through
the downstream contract in SPEC-002 §5. The prd skill's handoff (BEH-13) detects it by checking for
`${CLAUDE_PLUGIN_ROOT}/skills/epic/SKILL.md`. SPEC-002 §13 has an open decision on whether an
architecture step comes first.
