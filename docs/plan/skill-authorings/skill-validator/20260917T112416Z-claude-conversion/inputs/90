# Retrieved: Claude Code skills reference

- source_id: `claude-code-skills`
- url: https://code.claude.com/docs/en/skills
- retrieved_at_utc: 2026-09-17
- representation: documentation extraction via the host `WebFetch` tool (model-rendered Markdown answer over the fetched page); NOT raw HTTP bytes.
- limitation: digests bind this retained extraction, not the original transport bytes. A later run must re-retrieve to claim current-live coverage.

## Frontmatter fields (all optional; `---` must be the file's first line)

| Field | Type | Constraints |
| --- | --- | --- |
| `name` | String | No length limit stated on this page. Defaults to the directory name. For plugin skills, sets the command name segment. |
| `description` | String | "truncated at 1,536 characters in the skill listing" (shared cap with `when_to_use`). Recommended. If omitted, the first non-empty markdown line is used. |
| `when_to_use` | String | Part of the 1,536-character cap with `description`. |
| `argument-hint` | String | Autocomplete hint. |
| `arguments` | String or YAML list | Named positional arguments for `$name` substitution. "Names map to argument positions in order." |
| `disable-model-invocation` | Boolean | Default `false`. Prevents automatic invocation; `/name` still works. |
| `user-invocable` | Boolean | Default `true`. `false` makes the skill model-only background knowledge. |
| `allowed-tools` | String or YAML list | "Space- or comma-separated string, or YAML list". Grant clears on the next message. Supports Bash rules with variable substitution. |
| `disallowed-tools` | String or YAML list | Removed from the tool pool while active. Cannot remove `EndConversation` if other tools remain. |
| `model` | String | Same values as `/model`; accepts `inherit`. Subject to the org `availableModels` allowlist. |
| `effort` | String | `low`, `medium`, `high`, `xhigh`, `max`. Inherits from session by default. |
| `context` | String | `fork` — runs the skill in a forked subagent context. |
| `agent` | String | Subagent type when `context: fork`. `Explore`, `Plan`, `general-purpose`, or a custom agent. |
| `background` | Boolean | With `context: fork`. Default `true`. |
| `paths` | String or YAML list | Glob patterns limiting automatic activation. |
| `shell` | String | `bash` or `powershell`. Default `bash`. |
| `hooks` | YAML map | Hooks registered on invocation, kept for the session. |
| `metadata` | YAML map | "Free-form YAML map for your own key-value data". Claude Code ignores it. |
| `license` | String | Agent Skills standard; accepted, not acted on. |
| `compatibility` | String | "Up to 500 characters". Accepted, not acted on. |

Booleans: "Boolean fields accept `yes`, `no`, `on`, `off`, `1`, and `0` in any letter case, in addition to `true` and `false`. Before v2.1.218, Claude Code recognized only `true` and `false`."

Parsing: "Claude Code reads the frontmatter only when the opening `---` is the file's first line. Otherwise it treats the whole file, `---` markers included, as skill content."

## Discovery locations

`.claude/skills/<skill-name>/SKILL.md` in the managed-settings directory (enterprise), `~/.claude/skills/...` (personal), `.claude/skills/...` (project), `<subdir>/.claude/skills/...` (nested), the same path under an `--add-dir` directory, `<plugin>/skills/<skill-name>/SKILL.md` (plugin), and claude.ai account skills.

## Invocation

`/<command-name>` or `/command-name argument1 argument2`. Command name comes from the directory name for personal/project skills; a nested clash uses the subdirectory path with `/` replaced by `:`; a plugin skill is `/plugin-name:skill-name`.

## Separate configuration files

"**No separate metadata files are read.**" / "**No other config files are read.** All configuration is in `SKILL.md` frontmatter and markdown content only."
