# Sources and maintenance

External sources retrieved 2026-09-10 UTC. Framework files and package derivations are bound in [derivation.json](derivation.json). These sources support design choices; none of them is evidence that this package has been evaluated.

| Source | Claims used here | Applicability and refresh |
| --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | Model-invoked discovery from the `description` field, with `description` (plus `when_to_use` where present) loaded every turn and truncated at 1,536 characters; explicit invocation as `/skill-directory-name`, and `/plugin-name:skill-directory-name` for a plugin skill, with the bare form available when no other command collides; the discovery locations and their precedence (managed/enterprise settings, `~/.claude/skills/`, the project's `.claude/skills/`, nested `<subdir>/.claude/skills/`, plugin `skills/`, `--add-dir`, and claude.ai-synced skills); the directory name determining the slash command while frontmatter `name` sets the display label and, for a plugin skill, the last command segment; supporting files referenced by Markdown link loading on demand at roughly zero context cost until read; `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PLUGIN_ROOT}`; the guidance to keep `SKILL.md` under 500 lines; and the exclamation-prefixed shell-injection syntax - both the inline form and the fenced block form - which executes on the user's machine before the skill content reaches Claude and aborts the whole invocation on a non-zero exit. | Claude Code. Recheck when the client, its discovery configuration or the packaging format changes. Documentation describes the client; it is not consultation evidence for the version actually run. |

Retrieved via a single fetch of that page on 2026-09-10 UTC. No observation of a running client was made, and nothing in this package establishes that this skill is discovered, loaded or activated by any client.

## What the provider documentation does not settle

Three things are deliberately not taken from that source.

The frontmatter here carries `name` and `description` only. Claude supports many more fields - `when_to_use`, `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable`, `paths`, `model`, `effort`, `context: fork`, `agent`, `hooks` among them - and this package deliberately uses none of them, because the DevForgeAI authoring rule for these packages is the two-field form. Adding one is an authoring decision for the integration owner, not an inference from the field existing.

No shell-injection placeholder appears anywhere in this package, in either the inline or the fenced block form. Command examples are inert text in `text` fences. That is deliberate: those placeholders run before the skill is seen and abort the invocation on failure, which is not a property an authoring package should acquire by accident.

Claude's naming rules make a difference between the frontmatter `name` and the directory name legitimate. DevForgeAI packages keep them equal by convention, which is a convention and not a provider conformance rule.

## Framework sources

The governing specification, the shared templates copied into `assets/`, and the contracts this package's references were distilled from are recorded with their paths, revisions and digests in [derivation.json](derivation.json). The installed skill does not need any of them present at runtime.

## Refresh sequence

Select the source revision with the assignment owner; preserve the old bytes and evidence; update the affected package derivations; regenerate only authorised installed copies; and route changed identities into a new evaluation iteration for the affected checks. A web document changing does not by itself replace an already-selected contract, and a newer revision applies to a new iteration rather than to a closed one.
