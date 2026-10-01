---
paths:
  - "src/claude/DevForgeAI/skills/**"
  - "src/claude/DevForgeAI/.claude-plugin/**"
  - "src/templates/**"
---

# Skill anatomy and building a skill

## Anatomy (under `src/claude/DevForgeAI/`)

- `skills/<name>/SKILL.md`: the only file loaded on trigger; at most 500 lines. It holds a copyable
  checklist, the decisions that belong to the user, an output contract, and direct links to references.
- `skills/<name>/provenance.yaml`: the SKL record with an `implements` link to the spec; Claude never
  loads it. Directory name = `SKILL.md` `name` = `skill_name`. `metadata.devforgeai-id` and
  `devforgeai-version` mirror provenance `id` and `version`: bump both on any change to `SKILL.md` or
  its references.
- `skills/<name>/references/`: loaded on demand, one level deep. `output-rules.md` defines keys, ID
  patterns and allowed fields, and ends with the self-check list used in place of `devforgeai check`.
- `skills/<name>/scripts/`: executed, not loaded. Keep `__pycache__/` out of the deployed copy.
  - Brainstorm's `validate_brn.py` applies the output rules at step 7. It can't check what the user
    confirmed, so step 7 also reads the file back. It stays standard-library only (BEH-09), with
    PyYAML as an optional syntax check, and must give the same verdict without PyYAML: its tests in
    `src/tests/brainstorm/` run every case both ways. The Codex port keeps a fork of it (D-03).
  - prd and architecture share `validate_policy.py` (SPEC-002 §5, D-09), byte-identical with
    `references/policy.md`, `defaults.md` and `references/schemas/` (unchanged copies of
    `src/schemas/`); change them in both skills together, and `src/tests/prd/test_shared_files.py`
    checks it. The script validates approved policy in full with jsonschema, then checks dates against
    the calendar (additional semantic validation labelled `calendar check`: the unchanged schema
    accepts `2026-13-45`), then SV-01..06, and exits 0, 1 (invalid) or 2 (can't run). It must also
    work on the system's jsonschema 4.10 (no `referencing` module), which loads whenever the user
    site-packages are hidden, for example under another HOME, as eval workspaces use. Its tests, run
    under both, are in `src/tests/prd/`.
  - Neither prd nor architecture has a document validator: prd's step 9 reads the PRD back against the
    self-check list, as architecture's step 10 does for the ARCH and each ADR, and epic's step 8 for
    each epic.
  - documents-updater's `check_docs.py` checks Markdown structure and links at step 6; its tests live
    in `src/tests/documents-updater/` so they don't deploy.
  - git's `repo_state.py`, `scan_staged.py` and `qa_state.py` are read-only and offline; their tests
    live in `src/tests/git/`. `repo_state.py` must never refresh the index: a plain `git diff`
    rewrites `.git/index` even with `GIT_OPTIONAL_LOCKS=0`, and `check-ignore` fails under
    `GIT_LITERAL_PATHSPECS`.
- `skills/<name>/assets/<type>.md`: the canonical document template; architecture holds two, `arch.md`
  and `adr.md`, and epic holds `epic.md`. `src/templates/brainstorm.md` is a leftover identical copy;
  edit the asset. documents-updater's `assets/` holds its twelve fallback templates instead.
- `evals/<name>/<case>/`: `prompt.md`, `graders/*.md`, optional `case.yaml` + `scaffold.sh`; one case
  per automated VER item, tagged `<name>` and `ver-NN`.
- Never put a `CLAUDE.md` anywhere under `src/claude/DevForgeAI/`: the deploy would copy it into the
  plugin.

The architecture skill copies the prd skill's `references/policy.md` and `defaults.md` byte-identical
(SPEC-003 §3), so both are written skill-neutral.

Brainstorm frameworks are an extension point: add a file with the six sections that
`references/frameworks/INDEX.md` requires, plus one index row. `SKILL.md` never changes.

## Building the next skill

Follow the implementing spec's §11, translating paths per `.claude/rules/spec-paths.md`:

1. Copy `src/templates/skill/` and fill it in before it reaches a loaded skills directory.
2. Write `SKILL.md` from spec §5–§7, and `provenance.yaml` with the next SKL ID (reserved IDs are in
   CLAUDE.md's skill table).
3. Move the document template from `src/templates/` into `assets/`, and update the templates README row.
4. Write `references/output-rules.md`.
5. Write one eval case per automated VER item (every skill since documents-updater generates its cases
   with `src/tests/<name>/make_evals.py`).
6. Evaluate the source directly (no deploy needed) until every case scores ≥ 0.8, cheapest first
   (CLAUDE.md, "Evaluating a skill"). Then deploy, and do the manual VER items by hand.

## Hand-offs between skills

- The architecture `hands-off-to-epic` case was flipped to the shipped branch (`/devforgeai:epic
  PRD-001`) in the change that added `epic`, as the prd `hands-off-to-architecture` case was when
  `architecture` shipped.
- When a story skill ships, epic's `hands-off-to-story` case needs no flip: its graders accept both
  branches (SPEC-004 VER-10). The epic skill checks for it at `${CLAUDE_SKILL_DIR}/../story/SKILL.md`,
  the form verified here, where SPEC-004 BEH-11 writes `${CLAUDE_PLUGIN_ROOT}/skills/story/SKILL.md`.
- The rule for handing off to documents-updater is in CLAUDE.md, "Rules a change must not break".
