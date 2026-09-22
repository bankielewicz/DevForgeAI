# Skill template

A DevForgeAI skill is an [Agent Skills](https://agentskills.io/specification) directory that
Claude Code loads, plus a provenance sidecar that ties it into the planning chain. Each skill
**implements** a specification (`SPEC-NNN`), and its eval cases verify that spec's `VER-` items.

> **Never copy this folder into a `skills/` or `.claude/skills/` directory as-is.** Anything
> under those paths loads as a live skill. Copy it, rename it, and fill it in first.

## Layout

```
<plugin>/                         # DevForgeAI packages skills as a Claude Code plugin
├── skills/
│   └── <skill-name>/             # directory name MUST equal SKILL.md `name`
│       ├── SKILL.md              # loaded when the skill triggers; keep it short
│       ├── provenance.yaml       # DevForgeAI record; never loaded by Claude unless read
│       ├── references/           # loaded on demand, one level deep from SKILL.md
│       ├── scripts/              # executed, not loaded
│       └── assets/               # templates and data the skill copies or fills
└── evals/
    └── <skill-name>/             # this skill's eval cases (from evals/ here)
        └── <case>/prompt.md, graders/*.md, case.yaml
```

| File here | Becomes | Purpose |
|---|---|---|
| [SKILL.md](SKILL.md) | `skills/<skill-name>/SKILL.md` | Instructions Claude follows |
| [provenance.yaml](provenance.yaml) | `skills/<skill-name>/provenance.yaml` | ID, status, version, `implements` link to the SPEC |
| [references/reference.md](references/reference.md) | `skills/<skill-name>/references/<topic>.md` | Shape for an on-demand reference file |
| [evals/](evals/) | `evals/<skill-name>/<case>/` | Eval case shapes for `claude plugin eval` |

## Why provenance lives in a sidecar

The Agent Skills spec defines `metadata` as a map of **strings to strings**, so link records
(lists of objects) can't live in `SKILL.md` portably. `SKILL.md` carries only two metadata keys,
`devforgeai-id` and `devforgeai-version`, always quoted. `provenance.yaml` holds the full
record, uses the common frontmatter keys from [../README.md](../README.md) §2.2, and is
validated against `schemas/skill.schema.json`.

`devforgeai check` also verifies:
- `SKILL.md` frontmatter against `schemas/skill-frontmatter.schema.json`. Unknown keys are
  **errors** there, because Claude Code silently ignores a misspelled field such as
  `disable-model-invokation`. If the YAML doesn't parse at all, Claude Code loads the skill
  with no fields, and nothing warns you.
- that the directory name equals `name`, which equals `provenance.yaml` `skill_name`;
- that `devforgeai-id` and `devforgeai-version` match `provenance.yaml` `id` and `version`;
- that every `VER-` item of the implemented SPEC has an eval case tagged with it.

## Authoring rules

These rules follow the Agent Skills specification and Anthropic's skill authoring best practices.

**Frontmatter**
- `name`: lowercase letters, digits and single hyphens, at most 64 characters, and never containing
  `anthropic` or `claude`. Prefer a short verb or gerund. In a plugin, the command is namespaced
  (`/devforgeai:<name>`), so the name itself needn't repeat "devforgeai".
- `description`: third person, stating **what it does and when to use it**, with the words users
  actually say. 1–1024 characters, no `<` or `>`. This is the only text Claude sees before it
  decides to load the skill, so it matters more than anything in the body.
- Set `disable-model-invocation: true` only for workflows a person must start deliberately.

**Body**
- At most 500 lines, and ideally well under 5,000 tokens. Claude already knows general
  concepts, so write only what it wouldn't know or do by default.
- Give a copyable checklist for multi-step workflows, and a validate → fix → repeat loop
  wherever output can be checked.
- Give one default approach, with an escape hatch. Don't list many alternatives.
- Link every reference file directly from `SKILL.md`: one level deep, never chained.
  Reference files over 100 lines start with a table of contents.
- Use one term per concept throughout. Use forward slashes in paths. Use `${CLAUDE_SKILL_DIR}`
  for files inside the skill.
- Don't put time-sensitive statements in the body.
- **Delete every `<!-- -->` comment when filling in `SKILL.md`.** Whatever remains ships
  into Claude's context on every invocation.
- Don't use `` !`command` `` context injection for commands that can fail. A non-zero exit
  aborts the whole skill before Claude sees it.

**Judgment boundaries**
- State explicitly which decisions the skill may make and which need the user's confirmation.
  The implementing SPEC should have an AC or BEH item for each boundary, and an eval case for it.

## Evals

Evals use the case format of `claude plugin eval`, which targets plugins only. That is one
reason DevForgeAI packages skills as a plugin.
- Every skill needs **at least three cases**: one that should trigger it, one unrelated request
  that must not trigger it, and one per critical `VER-` item.
- Link a case to its VER item through `tags` (for example `ver-01`) and to the skill through
  the tag in `provenance.yaml` `eval_tag`. `prompt.md` rejects unknown frontmatter keys, so
  tags are the only way to attach IDs.
- Each run starts in an **empty workspace** with no project `.claude/`, `CLAUDE.md` or project
  files. If the skill reads project files, seed them with `case.yaml` `context.scaffold_script`
  and run with `--scaffold`.
- Compare against the no-plugin baseline (the default). A case that scores the same with and
  without the skill doesn't show that the skill helps.
