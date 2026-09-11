# Sources and maintenance

External sources retrieved 2026-09-10 UTC. Framework files and package derivations are bound in [derivation.json](derivation.json). These sources support design choices; none of them is evidence that this package has been evaluated.

| Source | Claims used here | Applicability and refresh |
| --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | Model-invoked discovery from the `description` field; explicit invocation as `/skill-name`, and `/plugin-name:skill-name` for a plugin skill; the eight discovery locations and their override precedence, highest first: enterprise managed settings, personal `~/.claude/skills/`, the project's `.claude/skills/` and each parent to the repository root, nested `<subdir>/.claude/skills/`, an `--add-dir` additional directory, plugin `<plugin>/skills/`, claude.ai account-synced skills, then bundled skills; the directory name determining the slash command while frontmatter `name` sets the display label for a personal or project skill and the command segment for a plugin skill; supporting files referenced from `SKILL.md` loading on demand; `${CLAUDE_SKILL_DIR}` and `${CLAUDE_PLUGIN_ROOT}`; and the exclamation-prefixed shell-injection syntax that executes before the skill is seen and aborts it on a non-zero exit. | Claude Code. Recheck when the client, its discovery configuration or the packaging format changes. Documentation describes the client; it is not consultation evidence for the version actually run. |
| [Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents) | Subagent files live in `.claude/agents/`, `~/.claude/agents/` or a plugin's `agents/` directory with a defined precedence; frontmatter fields including `name`, `description`, `tools`, `model` and `skills`; the `skills` field preloading full skill content at startup; each subagent running in its own context window with its own system prompt. | Used only for the independence discussion in the review rubric and the isolation caution in native evaluation. This package defines no subagent; a plugin `agents/` file is outside its fence. |
| [Agent Skills specification](https://agentskills.io/specification) | The portable package shape: a skill directory with `SKILL.md` carrying `name` and `description`, with `scripts`, `references` and `assets` optional. | Provider-neutral. Provider-specific discovery behaviour still needs provider evidence. |

## What the provider documentation does not settle

Three things are deliberately not taken from these sources.

The frontmatter here carries `name` and `description` only. Claude supports many more fields - `allowed-tools`, `disable-model-invocation`, `user-invocable`, `context: fork`, `agent`, `model`, `effort`, `paths` among them - and this package deliberately uses none of them, because the DevForgeAI authoring rule for these packages is the two-field form. Adding one is an authoring decision for the integration owner, not an inference from the field existing.

Claude's naming rules make a difference between the frontmatter `name` and the folder name legitimate. DevForgeAI packages keep them equal by convention, which is a convention and not a provider conformance rule; see [missing DevForge CLI capabilities](missing-rust-capabilities.md).

Nothing in these pages establishes an isolation boundary. A separate context window separates a prompt. Filesystem, process, credential and memory boundaries are observed per attempt or recorded as unavailable.

## Refresh sequence

Select the source revision with the assignment owner; preserve the old bytes and evidence; update the affected package derivations; regenerate only authorised installed copies; and route changed identities into a new evaluation iteration for the affected checks. A web document changing does not by itself replace an already-selected contract, and a newer revision applies to a new iteration rather than to a closed one.
