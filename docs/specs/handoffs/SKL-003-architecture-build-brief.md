# Build brief: architecture skill (SKL-003)

**For a fresh Claude Code session.** Everything you need is in this repository; `CLAUDE.md` applies.

| | |
|---|---|
| Implements | `docs/specs/spec/SPEC-003.md` (version 6) |
| Story | `docs/specs/story/STORY-003.md` (version 2) |
| Process | `docs/specs/adr/ADR-001.md` (accepted, v4); ADR-002 and ADR-003 (accepted) |
| Branch / worktree | `story/STORY-003-architecture` / `.claude/worktrees/story-003-architecture` |
| Produces | Skill `architecture` in plugin `devforgeai`, invoked as `/devforgeai:architecture PRD-NNN` |

## 0. Before the session (done by the user in the main checkout)

```bash
git worktree add .claude/worktrees/story-003-architecture -b story/STORY-003-architecture main
W=.claude/worktrees/story-003-architecture
[ -d "$W/src/claude/DevForgeAI" ] \
  && test -z "$(find "$W/src/claude/DevForgeAI" -type l)" \
  && mkdir -p "$W/.claude/skills/devforgeai" \
  && rsync -a --delete --exclude=/evals/results/ "$W/src/claude/DevForgeAI/" "$W/.claude/skills/devforgeai/" \
  && diff -r -x results "$W/src/claude/DevForgeAI" "$W/.claude/skills/devforgeai" && echo deployed
claude --worktree story-003-architecture -n story-003-architecture
```

Start the session only after the deploy prints `deployed`. Opening prompt: *"Read
docs/specs/handoffs/SKL-003-architecture-build-brief.md and carry it out. In your report back, list each
ambiguity you ran into: the question, what you checked, what depended on it, and whether it interrupted
work that could otherwise have continued."*

## 1. How to build

Build it the way SKL-001 and SKL-002 were built: follow the spec directly, not
`/skill-creator:skill-creator` or `/plugin-dev:create-plugin`. The `plugin-dev:skill-reviewer` and
`plugin-validator` agents may review the result, but SPEC-003 wins any conflict. Follow the conventions
of the built `brainstorm` and `prd` skills. Visual explanations are optional. If you make one, use a Claude Design artifact as supporting material,
store its approved export alongside, and keep ARCH, ADRs and Mermaid authoritative.

## 2. Read in this order

1. SPEC-003 (authoritative): BEH-01…16, ERR-01…06, QR-01…03, VER-01…14, the §4 readiness rule and the §5 contracts.
2. STORY-003: AC-01…11.
3. ADR-001 (process), ADR-002 (the step), ADR-003 (policy contract).
4. The built `prd` skill, especially `references/policy.md` and `defaults.md`, which you copy unchanged, and SPEC-002 §5.
5. `src/staging/templates/arch.md`, `adr.md` and README §1–§2; `src/schemas/arch.schema.json`, `adr.schema.json`, `prd.schema.json` and `policy.schema.json`.
6. `src/staging/examples/policy-two-orgs/`, the demonstration policies.

**Precedence:** SPEC-003 > STORY-003 > ADRs > templates. If something is contradictory or missing, stop and ask.
Don't edit specs, stories, the PRD, epics or ADRs without the user's explicit approval, and when you do,
apply the version and link updates in the same change.

## 3. Deliverables

All deliverables go under `src/claude/DevForgeAI/`:

| Path | Content |
|---|---|
| `skills/architecture/SKILL.md` | Frontmatter exactly as in SPEC-003 §5. The body follows the skill template. At most 500 lines, and no author comments left |
| `skills/architecture/provenance.yaml` | `SKL-003`, `implements` SPEC-003 v6, `skill_name: architecture`, `eval_tag: architecture`, `status: draft` |
| `skills/architecture/assets/arch.md`, `adr.md` | **Moved** with `git mv` from `src/staging/templates/`. Update the README rows |
| `skills/architecture/references/policy.md`, `defaults.md` | Copied unchanged from the prd skill |
| `skills/architecture/references/readiness.md`, `inspection.md`, `output-rules.md` | From SPEC-003 §4, BEH-05 to BEH-07 and BEH-11, and the schema |
| `evals/architecture/<case>/` | One case per automated VER. Cases are tagged `architecture` and `ver-NN` |

| Case | VER | Fixtures |
|---|---|---|
| `creates-arch` | ver-01 | The shared fixture PRD (SPEC-003 §9) |
| `org-a-policy` | ver-02 | Shared PRD, plus Organization A's `POL-001.md` in `docs/specs/policy/` |
| `org-b-policy` | ver-03 | Shared PRD, plus Organization B's `POL-001.md`. Everything else identical to `org-a-policy` |
| `unrelated-adr` | ver-04 | Shared PRD, plus an accepted logging ADR-001 citing FR-001 |
| `superseded-adr` | ver-05 | Shared PRD, an ARCH-001 with a DEC resolved by ADR-002, and ADR-002 superseded by ADR-003 |
| `no-acceptance-without-user` | ver-06 | As `creates-arch` |
| `existing-arch-not-duplicated` | ver-07 | Shared PRD, plus an ARCH-001 for the same system |
| `insufficient-evidence` | ver-08 | Shared PRD. The prompt says to reuse the current auth service, and names no scope |
| `prd-change-handed-back` | ver-09 | A PRD whose NFR conflicts with Organization A's mandate, plus Organization A's policy |
| `hands-off-to-epic` | ver-10 | As `creates-arch` |
| `ignores-unrelated-request` | ver-11 | None |
| `records-provenance` | ver-14 | As `creates-arch` |

Write every fixture fresh and check it against its schema. Runs are non-interactive: put every answer in the
prompt, and file graders need literal paths. See `plugin-eval-quirks` in memory.

## 4. Build loop

Deploy after every change to `src/` (step 0's snippet, run from the worktree root with `W=.`), run
`/reload-plugins`, then validate:

```bash
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai
for f in src/claude/DevForgeAI/skills/*/assets/*.schema.json; do [ -e "$f" ] || continue; cmp -s "$f" "src/schemas/$(basename "$f")" || echo "SCHEMA DRIFT: $f"; done
claude plugin validate .claude/skills/devforgeai --strict
```

The user runs evals from a **plain terminal** in the worktree root:

```bash
claude plugin eval .claude/skills/devforgeai --tag architecture --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
claude plugin eval .claude/skills/devforgeai --allow-tools Write Edit --scaffold --no-publish --threshold 0.8   # before the PR: no brainstorm/prd regression
```

## 5. Manual checks

- **VER-12:** by hand, in a scratch project with `claude --plugin-dir <worktree>/.claude/skills/devforgeai`. Each fixture project is a git repo with an initial commit, and fixtures are checked against their schemas.
- **VER-13, the demonstration operator check:** before `org-a-policy`, between the two runs, and after `org-b-policy`:
  ```bash
  find .claude/skills/devforgeai -path '*/evals/results' -prune -o -type f -print0 | sort -z | xargs -0 sha256sum | sha256sum
  git diff --stat src/
  ```
  All three hashes must be identical, and `git diff` empty. Record them in the PR.

## 6. Don't

- Don't build experts, index the whole codebase, add detailed feature design, or build the epic skill.
- Don't write validator scripts into the repository, and don't start the `devforgeai` CLI.
- Don't modify the brainstorm or prd skills.
- Don't create symlinks under `src/`. Skill resources resolve inside the skill or plugin.
- Don't push, open a PR or merge without asking the user.

## 7. Done when

- [ ] The deliverables exist, and the templates were moved, not copied.
- [ ] `diff` is clean, the schema-copy loop prints nothing, and `validate --strict` passes.
- [ ] Every architecture case scores at least 0.8 over 3 runs, with its delta reported, and the full-plugin run shows no regression.
- [ ] VER-12 and VER-13 are done and recorded.
- [ ] Every commit references `STORY-003`.

## 8. Report back

- A table of VER-01…14 with the score and delta, or the manual result.
- The eval report paths.
- The VER-13 hashes.
- Deviations from the spec, proposed spec changes, and open questions.
- The ambiguity list.

## 9. After this build

Next is the **epic** workflow, `/devforgeai:epic PRD-NNN`. It consumes the readiness rule (SPEC-003 §4) and
writes epics only for ready requirements.
