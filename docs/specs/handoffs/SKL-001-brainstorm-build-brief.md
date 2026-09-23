# Build brief: brainstorm skill (SKL-001)

**For a fresh Claude Code session.** Everything you need is in this repository. Don't assume any
context from earlier conversations.

| | |
|---|---|
| Implements | `docs/specs/spec/SPEC-001.md` (version 5) |
| Story | `docs/specs/story/STORY-001.md` (version 3) |
| Build and validation process | `docs/specs/adr/ADR-001.md` (accepted, version 2) |
| Branch / worktree | `story/STORY-001-brainstorm` / `.claude/worktrees/story-001-brainstorm` |
| Produces | Plugin `devforgeai` with skill `brainstorm`, invoked as `/devforgeai:brainstorm` |

---

## 0. Before the session (done by the user in the main checkout)

The session checks these and **stops if any is missing**. It doesn't create them itself.

1. The repository is a git repository with a `main` branch and at least one commit.
2. `main` has a committed `.gitignore` containing:
   ```gitignore
   .claude/worktrees/
   .claude/skills/devforgeai/
   src/claude/DevForgeAI/evals/results/
   ```
3. `main` has a committed `.claude/settings.json` containing:
   ```json
   { "permissions": { "deny": ["Edit(/.claude/skills/devforgeai/**)"] } }
   ```
4. The worktree exists, and the session was started in it (ADR-001 steps 1 and 3):
   ```bash
   git worktree add .claude/worktrees/story-001-brainstorm -b story/STORY-001-brainstorm main
   claude --worktree story-001-brainstorm -n story-001-brainstorm
   ```
   Nothing exists in `src/` yet, so there is nothing to deploy before this first session.

Opening prompt for the session: *"Read docs/specs/handoffs/SKL-001-brainstorm-build-brief.md and carry it out."*

## 1. Which creator skill to use

**Neither `/skill-creator:skill-creator` nor `/plugin-dev:create-plugin` drives this build.**
SPEC-001 has already made the design decisions those tools would interview for. Each also conflicts
with this repository's process:

| Tool | Conflict |
|---|---|
| `/skill-creator:skill-creator` | It uses its own `evals/evals.json` format, not `claude plugin eval` cases. It writes a `<skill>-workspace/` folder next to the skill, which would land inside `src/` and be deployed. Its description-optimization loop writes temporary files into `.claude/commands/`. It has no plugin manifest. |
| `/plugin-dev:create-plugin` | It has mandatory interview and confirmation gates that duplicate SPEC-001. It may `git init`. It has no eval mechanism. |

You may:
- read the `plugin-dev:skill-development` and `plugin-dev:plugin-structure` skills as reference;
- at the end, run the `plugin-dev:skill-reviewer` and `plugin-dev:plugin-validator` agents on the
  operational copy, if they're installed. Treat their findings as suggestions. When they conflict
  with SPEC-001, SPEC-001 wins, and you report the conflict.

## 2. Read in this order

1. SPEC-001, which is authoritative. It covers components, behavior (BEH-01…11), errors (ERR-01…05),
   quality responses (QR-01…03), verifications (VER-01…10), the frontmatter in §5 and the implementation plan in §11.
2. STORY-001, which has acceptance criteria AC-01…07.
3. ADR-001, which sets the layout, deploy and validate commands, and rules.
4. `src/staging/templates/skill/README.md` and every file under `src/staging/templates/skill/`.
5. `src/staging/templates/README.md` §1–§2: the item-block and provenance rules the BRN output must follow.
6. `src/staging/templates/brainstorm.md`, and `src/schemas/brainstorm.schema.json` with `common.schema.json`.

**Precedence when documents disagree:** SPEC-001 > STORY-001 > ADR-001 > templates > anything else.
If something is contradictory or missing, **stop and ask the user**. Don't invent requirements,
IDs or links. Don't edit SPEC-001, STORY-001, PRD-001, EPIC-001 or ADR-001. Propose changes in your report instead.

## 3. Deliverables

All deliverables go under `src/claude/DevForgeAI/`. The only other edit is one link in `src/staging/templates/README.md`, noted below.

| Path | Content | Implements |
|---|---|---|
| `.claude-plugin/plugin.json` | `name: devforgeai`, `version: 0.1.0`, `description`, `author: {name: "Bryan"}` | ADR-001 |
| `skills/brainstorm/SKILL.md` | Frontmatter exactly as in SPEC-001 §5. The body follows the skill template: inputs, workflow checklist, steps, decisions that need the user, output contract, references. At most 500 lines, and no `<!-- -->` comments left | BEH-01…11, ERR-01…05, QR-01, QR-02 |
| `skills/brainstorm/provenance.yaml` | From the template: `id: SKL-001`, `upstream: [{id: SPEC-001, relation: implements, version: 5, hash: null}]`, `skill_name: brainstorm`, `packaging: plugin`, `plugin: devforgeai`, `eval_tag: brainstorm`, `status: draft`, `generated_by` filled in | QR-02 |
| `skills/brainstorm/assets/brainstorm.md` | **Moved** with `git mv src/staging/templates/brainstorm.md …`. Then update the brainstorm row's link in `src/staging/templates/README.md` to the new path | BEH-08 |
| `skills/brainstorm/references/output-rules.md` | The rules the skill self-checks against when `devforgeai` isn't installed: frontmatter keys, ID patterns, quoting, one top-level key per `yaml items` block, allowed collections and fields, no leftover placeholders. Taken from templates README §1.1–§1.2 and `brainstorm.schema.json` | BEH-09 |
| `skills/brainstorm/references/frameworks/INDEX.md` | Table with columns *framework, file, use when, avoid when*, and one row: diverge-converge | BEH-03 |
| `skills/brainstorm/references/frameworks/diverge-converge.md` | The sections from SPEC-001 §4, in order | BEH-03, BEH-04 |
| `evals/brainstorm/<case>/` | One case per automated VER (table below), built from the skill template's `evals/` | QR-03 |
| (no schema) | The canonical schemas are already in `src/schemas/`. The skill ships **no** schema copy | ADR-001 |

Eval cases. Each is tagged `brainstorm` plus the tag shown:

| Case | Tag | Verifies | Notes |
|---|---|---|---|
| `writes-valid-brn` | `ver-01` | AC-01 | The prompt gives the topic, trigger, users and constraints, and says to proceed without questions |
| `no-unconfirmed-dispositions` | `ver-02` | AC-02 | Regex `not_contains` on the written file for `disposition: promoted`, `parked` and `rejected` |
| `records-provenance` | `ver-03` | AC-03 | Regex on the file for `generated_by`, `reviewed_by: []` and `hash: null` |
| `uses-named-framework` | `ver-04` | AC-04 | The prompt names diverge-converge. An llm grader checks the reply. On `docs/specs/brainstorm/BRN-001.md`: regex graders (partial structural checks, not schema validation) and an llm grader given the complete document and each collection's allowed fields. CLI validation is NOT_RUN until `devforgeai check` exists |
| `ignores-unrelated-request` | `ver-06` | AC-05 | `tool_used: Skill`, `min: 0`, `max: 0`, `arm: both` |
| `asks-for-topic` | `ver-07` | AC-06 | No topic given; `file_exists` with `exists: false`; llm grader |
| `existing-brn` | `ver-08` | AC-01 | `case.yaml` scaffold creates `docs/specs/brainstorm/BRN-001.md` on the same topic; the skill must ask, not overwrite |
| `hands-off-to-prd` | `ver-10` | AC-07 | This plugin has no `prd` skill, so the reply must say the PRD step isn't available yet and give the BRN path |

**Amended 2026-09-22 (SPEC-001 v5, STORY-001 v3):** BRN documents are written to `docs/specs/brainstorm/BRN-NNN.md`. The skill allocates the ID itself and never asks for or accepts a file name, so eval prompts name no file and graders read `docs/specs/brainstorm/BRN-001.md` directly.

**Eval constraints** (from the `claude plugin eval` documentation):
- Each run is non-interactive and starts in an empty workspace. No user answers questions, so put
  every answer in the prompt, except in the two cases that test questioning (`asks-for-topic`, `existing-brn`).
- Only read-only tools come from `allowed_tools`. Write and Edit come from `--allow-tools` on the
  command line (ADR-001 step 5). Bash isn't granted, so in evals the skill takes the BEH-09 fallback path,
  validating against `output-rules.md`.
- `prompt.md` rejects unknown frontmatter keys. Link cases to VER items only through `tags`.

## 4. Build loop

Run everything from the **worktree root**, as in ADR-001 steps 2, 4 and 5:

```bash
# deploy (after every change to src/)
test -z "$(find src/claude/DevForgeAI -type l)" \
  && mkdir -p .claude/skills/devforgeai \
  && rsync -a --delete --exclude=/evals/results/ src/claude/DevForgeAI/ .claude/skills/devforgeai/

# validate what ships
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai
for f in src/claude/DevForgeAI/skills/*/assets/*.schema.json; do [ -e "$f" ] || continue; cmp -s "$f" "src/schemas/$(basename "$f")" || echo "SCHEMA DRIFT: $f"; done
claude plugin validate .claude/skills/devforgeai --strict
claude plugin eval .claude/skills/devforgeai --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
```

- After the first deploy, run `/reload-plugins`. Then run `/plugin` and `/skills` to confirm that
  `devforgeai@skills-dir` and `/devforgeai:brainstorm` load from the worktree path. Report what you see.
  ADR-001 lists this as not yet confirmed.
- Edit only `src/`. The operational copy is overwritten on every deploy, and the deny rule blocks editing it.
- `claude plugin eval` makes model calls. Iterate on one case at a time with
  `--case <name> --runs 1 --ablation none` before running the full suite.

## 5. Manual verifications

Do these by hand in the worktree session and record the results:

- **VER-05:** add a test framework file and an `INDEX.md` row, leaving `SKILL.md` unchanged. Confirm the
  skill selects it. Delete the file, and confirm the skill falls back to diverge-converge and says so.
  Remove the test framework before committing.
- **VER-09:** stop a session mid-brainstorm and confirm the skill offers to save a draft. Check that
  `SKILL.md` is at most 500 lines. Check its frontmatter by reading it against
  `src/schemas/skill-frontmatter.schema.json`, since no validator for that schema exists in the repository.

## 6. Don't

- Don't write validator scripts (Python or otherwise) into the repository, and don't start the `devforgeai` Rust CLI.
- Don't create symlinks anywhere under `src/`.
- Don't reference `src/` (including `src/staging/` and `src/schemas/`), `docs/specs/` or `${CLAUDE_PROJECT_DIR}` from any skill file. Every
  path a skill uses resolves inside the skill or plugin (`${CLAUDE_SKILL_DIR}`, `${CLAUDE_PLUGIN_ROOT}`).
- Don't add brainstorming frameworks beyond diverge-converge; the catalog is deferred (PRD-001 §12).
- Don't build the PRD skill.
- Don't push, open a PR or merge without asking the user first.

## 7. Done when

- [ ] Every deliverable in §3 exists, and `src/staging/templates/brainstorm.md` has been moved rather than copied.
- [ ] The schema-copy loop prints nothing.
- [ ] `diff -r -x results` is clean and `claude plugin validate --strict` passes.
- [ ] `claude plugin eval` passes with every case at 0.8 or above over 3 runs, with the baseline delta reported.
- [ ] VER-05 and VER-09 are done by hand and their results recorded.
- [ ] Every commit message references `STORY-001`.

## 8. Report back

End the session with:
- a table of VER-01…10 showing, for each, the eval score and delta (or the manual result) and pass or fail;
- the path of the eval report;
- what `/plugin` and `/skills` showed;
- every deviation from SPEC-001, with the reason;
- proposed changes to SPEC-001, STORY-001 or ADR-001;
- open questions.

## 9. After this build

The next workflow is the **`prd` skill** in the same plugin (`/devforgeai:prd`). It consumes a BRN
document and writes a PRD whose requirements cite BRN items through `upstream` links (SPEC-001 §5,
downstream contract). It isn't specified yet. Once this skill is built, its handoff (BEH-10) detects the
`prd` skill by checking for `${CLAUDE_PLUGIN_ROOT}/skills/prd/SKILL.md`, so the handoff wording needs no change.
