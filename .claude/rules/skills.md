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
  - prd, architecture and context share `validate_policy.py` (SPEC-002 §5, D-09; SPEC-003 §3;
    SPEC-011 §3), byte-identical across the three skills with `references/policy.md`, `defaults.md`
    and the policy and common schema copies in `references/schemas/` (unchanged copies of
    `src/schemas/`). Change them in all three skills together; `src/tests/prd/test_shared_files.py`
    checks it. The script validates approved policy in full with jsonschema and a format checker,
    so an impossible date such as `2026-13-45` and a YAML `.nan` are schema errors, then applies
    SV-01..06, and exits 0, 1 (invalid) or 2 (can't run). It must also
    work on the system's jsonschema 4.10 (no `referencing` module), which loads whenever the user
    site-packages are hidden, for example under another HOME, as eval workspaces use. Its tests, run
    under both, are in `src/tests/prd/`.
  - context's `context_check.py` snapshots, checks and restores the context documents and ambiguity
    logs against its copies of `context.schema.json` and `ambiguities.schema.json` (SPEC-011 §5); its
    tests are in `src/tests/context/`.
  - spec-lookup's `find_spec.py` (standard library only) searches a project's `docs/specs/` and prints
    citations (SPEC-014 IF-01); its tests are in `src/tests/spec-lookup/`.
  - prd, architecture and epic have no document validator: prd's step 9 reads the PRD back against
    the self-check list, as architecture's step 10 does for the ARCH and each ADR, and epic's step 8
    for each epic.
  - documents-updater's `check_docs.py` checks Markdown structure and links at step 6; its tests live
    in `src/tests/documents-updater/` so they don't deploy.
  - git's `repo_state.py`, `scan_staged.py` and `qa_state.py` are read-only and offline; their tests
    live in `src/tests/git/`. `repo_state.py` must never refresh the index: a plain `git diff`
    rewrites `.git/index` even with `GIT_OPTIONAL_LOCKS=0`, and `check-ignore` fails under
    `GIT_LITERAL_PATHSPECS`.
- `skills/<name>/assets/<type>.md`: the canonical document template; architecture holds two, `arch.md`
  and `adr.md`, epic holds `epic.md`, and context holds one per context document plus `detail.md`. `src/templates/brainstorm.md` is a leftover identical copy;
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
- epic's `hands-off-to-story` graders accept both branches, with a story skill installed or without
  one, so the case needs no change when one is built (SPEC-004 VER-10). The epic skill checks for it at `${CLAUDE_SKILL_DIR}/../story/SKILL.md`,
  the form verified here, which SPEC-004 v2 BEH-11 also names.
- The rule for handing off to documents-updater is in CLAUDE.md, "Rules a change must not break".

## GitHub posts (`src/templates/github/`)

The github-post skill (SKL-009, SPEC-010) is not built. A session posting from these templates checks
the post by hand:
- **Quotes:** verify every quote against the pinned commit (`git show <sha>:<path>`), as SPEC-010
  BEH-09 specifies.
- **Angle brackets:** GitHub strips bare `<word>` text outside code as HTML. `"<file>: <part>"`
  renders as `": "` (checked with `gh api markdown`, 2026-09-30). Put such text in a code span or a
  fence, including inside `>` quotes. No script checks this.
- **Checking what was posted:** `gh issue edit N --body-file F` stores the file byte for byte, and
  `gh issue view N --json body` returns it exactly, so compare the two for equality.
