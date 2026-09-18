# Claude Code SKILL.md frontmatter (fields, domains, divergences)

Claude Code reads **no separate metadata or configuration file**. Everything the host reads is in the `SKILL.md` YAML frontmatter, so a package that still carries `agents/openai.yaml` or any other host's configuration document is carrying bytes this host never reads. Report that as a disposition question, not as a parsed contract.

The frontmatter is only read when the opening `---` is the file's first line. Otherwise the whole file, `---` markers included, is skill content — a leading BOM or blank line silently turns metadata into prose.

## Fields

`name` and `description` are the fields a package should carry. Claude Code will fall back to the directory name and the first non-empty markdown line, but a skill that relies on that fallback has no stated trigger.

| Field | Accepted shape | Notes |
| --- | --- | --- |
| `name` | string | 1-64 characters, lowercase letters/digits and single separating hyphens, matching the parent directory name. |
| `description` | string | Non-empty, at most 1024 characters. Carries the entire trigger: the body is not in context when the host decides whether to load the skill. |
| `when_to_use` | string | Additional triggering context; shares the listing cap with `description`. |
| `allowed-tools` | string **or YAML list** | Space- or comma-separated string, or a list of tool names. Scoped `Bash(...)` entries are preserved intact. |
| `disallowed-tools` | string or YAML list | Removed from the pool while the skill is active. |
| `model` | string | Same values as `/model`, including `inherit`. |
| `effort` | string | `low`, `medium`, `high`, `xhigh`, `max`. |
| `disable-model-invocation` | boolean | `true` makes the skill explicit-invocation only. |
| `user-invocable` | boolean | `false` makes the skill model-only background knowledge. |
| `context` | string | `fork` runs the skill in a forked subagent context. |
| `agent` | string | Subagent type; meaningful only with `context: fork`. |
| `background` | boolean | Used with `context: fork`. |
| `paths` | string or YAML list | Glob patterns limiting automatic activation. |
| `shell` | string | `bash` or `powershell`. |
| `hooks` | YAML map | Hooks registered on invocation and kept for the session. |
| `argument-hint` | string | Autocomplete hint. |
| `arguments` | string or YAML list | Named positional arguments for `$name` substitution. |
| `metadata` | YAML map | Free-form string-to-string data the host ignores. |
| `license` | string | Agent Skills field; accepted, not acted on. |
| `compatibility` | string | 1-500 characters. Accepted, not acted on. |

Boolean fields accept `yes`, `no`, `on`, `off`, `1` and `0` in any case as well as `true` and `false`. A YAML safe load already converts most of these to a Python bool; an unquoted `1` or `0` arrives as an integer.

A field outside this table is an applicability question, not a defect. Record it `NOT_RUN` against selected-source guidance.

## Recorded source divergences

These are the places where the two official sources disagree. Neither side may be promoted to a required format rule, because doing so fails packages the other source calls valid.

| Subject | Claude Code skills reference | Agent Skills specification / Anthropic authoring guidance |
| --- | --- | --- |
| `allowed-tools` shape | "Space- or comma-separated string, or YAML list" | "A space-separated string of tools that are pre-approved to run", marked experimental |
| `description` length | truncated at 1,536 characters in the skill listing, shared with `when_to_use` | "Must be 1-1024 characters" |
| `name` length | no limit stated | "Max 64 characters" / "Maximum 64 characters" |
| `name` content | no reserved-word or XML-tag rule stated | authoring guidance prohibits XML tags and the reserved words `anthropic` and `claude` |

The required rows in `scripts/skill_format.py` carry only what both sides support. The divergences are emitted by `advisory_checks` and are never defects on their own — they tell a reviewer that a package is valid here and non-portable elsewhere, or valid here and outside a recommendation there.

The YAML-list `allowed-tools` case is the one that matters in practice: it is idiomatic Claude Code and non-conformant to the portable specification, and a validator that treated the specification as universal would fail ordinary Claude Code packages on a required check.

## Invocation and discovery

A skill is invoked explicitly as `/<skill-name>`, or `/skill-name argument1 argument2`. A nested skill whose name clashes uses its subdirectory path with `/` replaced by `:`; a plugin skill is `/plugin-name:skill-name`. There is no `$skill-name` substitution — a converted package that still carries that syntax carries a string the host will not expand.

Discovery locations are the managed-settings directory, `~/.claude/skills/`, the project's `.claude/skills/`, a nested `<subdir>/.claude/skills/`, an `--add-dir` directory, a plugin's `skills/` directory, and claude.ai account skills. Development source held outside any of these is not a defect; installation is separately scoped.

## Unreproduced source metadata on conversion

A Codex package's `interface.icon_small`, `icon_large`, `brand_color` and `default_prompt` have no Claude Code equivalent. Record them as unreproduced source metadata in the conversion evidence. Do not invent frontmatter keys to hold them, and do not retain `$skill-name` prompt syntax.

`policy.allow_implicit_invocation: false` maps onto `disable-model-invocation: true`. `dependencies.tools` (MCP) has no in-package equivalent: Claude Code configures MCP at project or user level, so the dependency becomes a documented prerequisite rather than a declaration the package can make.

## Sources

Pinned in [rules-snapshot.json](rules-snapshot.json) with retrieval dates and representation honesty:

- `claude-code-skills` — https://code.claude.com/docs/en/skills
- `agent-skills` — https://agentskills.io/specification
- `claude-skill-best-practices` — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

Refresh them through available read-only retrieval before treating a field table as current; a snapshot establishes compliance with that identified snapshot only.
