# Bundled scaffolding and metadata authoring

The adapted init_skill.py is bundled; resolve it relative to this loaded builder. No personal installation path is a dependency. The helper originates from OpenAI Skill Creator; see [source notice](../assets/skill-creator-notice.md) and its preserved license.

For a new staged package only:

```text
python -B -X utf8 <builder>/scripts/init_skill.py selected-name --path <staging-parent> --resources references --allowed-tools Read,Grep,Glob
```

Choose only useful resource directories, omit `--resources` for a small instruction-only skill, and request `--examples` only when placeholders help actual authoring. `--allowed-tools` takes a comma-separated list and preserves scoped `Bash(...)` entries intact. `--model` and `--effort` are available but should stay omitted unless the task needs an override; an absent key inherits the configured session, while a written key asserts a decision.

Initialization refuses an occupied directory and never silently selects a different name. Complete or remove placeholders and empty unused resources before delivery. This authoring review is not a quality checker or sample-task run.

For metadata, read the included [frontmatter reference](claude-frontmatter.md). Claude Code keeps all host-read metadata in the SKILL.md frontmatter, so there is no separate UI file to generate or update — focused metadata edits are ordinary text edits to that frontmatter, which also means exact surrounding bytes survive an edit without a helper normalizing them.

Preserve existing fields not selected for editing, including any project-local bookkeeping keys. Keep automatic invocation for new skills unless the user explicitly requests otherwise; `disable-model-invocation: true` is an explicit request, not a default.
