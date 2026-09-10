# Sources and maintenance

External sources retrieved 2026-09-10 UTC. Framework files and package derivations are bound in [derivation.json](derivation.json). These sources support authoring decisions; none of them is evidence that this package has been evaluated, installed, or activated.

| Source | Claims used here | Applicability and refresh |
| --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | The `description` field is what Claude uses to decide when to apply a skill, and the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing - which is why this package puts the activating conditions and the sibling exclusions in `description` and keeps it inside that bound. Explicit invocation is `/skill-name` for a project skill and `/plugin-name:skill-name` for a plugin skill, with a nested project skill addressed as `/path:skill-name`. Discovery locations in precedence order: enterprise, personal `~/.claude/skills/`, project `.claude/skills/` and each parent to the repository root, nested `<subdir>/.claude/skills/`, plugin `<plugin>/skills/`, then claude.ai account-synced skills. Supporting files referenced from `SKILL.md` load on demand rather than every turn, which is why the four references here are linked at the phase that needs them. `${CLAUDE_SKILL_DIR}` names the directory holding the loaded `SKILL.md`. The shell-injection forms - an exclamation mark immediately followed by a backtick-quoted command, and a fenced block whose info string is a bare exclamation mark - run before Claude sees the skill content, and a failed command aborts the whole invocation rather than only its own placeholder. | Claude Code. Recheck when the client, its discovery configuration, or the packaging format changes. Documentation describes the client; it is not consultation evidence for the version actually run, and this package has not been loaded by any client. |
| [Agent Skills specification](https://agentskills.io/specification) | The portable package shape: a skill directory with `SKILL.md` carrying `name` and `description`, with `scripts`, `references` and `assets` optional. | Provider-neutral. Provider-specific discovery behaviour still needs provider evidence. |

## What the provider documentation does not settle

The frontmatter here carries `name` and `description` only. Claude supports many more fields - `when_to_use`, `allowed-tools`, `disable-model-invocation`, `user-invocable`, `context: fork`, `argument-hint` and `arguments` among them - and this package deliberately uses none of them, because the DevForgeAI authoring rule for these packages is the two-field form. Adding one is an authoring decision for the integration owner, not an inference from the field existing.

No shell-injection line appears anywhere in this package, deliberately, and this file describes that syntax in words rather than reproducing the token. It executes before the skill content is read and a non-zero exit aborts the invocation, so it would make this skill's availability depend on a command succeeding on someone else's machine. Command examples appear as inline code identifiers in tables and, where a whole invocation is shown, inside a ```` ```text ```` fence. They illustrate what an operator would run; nothing in this package executes them.

Claude sets the slash command from the directory name for a project skill and from the frontmatter `name` for a plugin skill, so a difference between the two is legitimate for the client. DevForgeAI packages keep them equal by convention, and this package does; that is a convention, not a provider conformance rule.

Nothing in these pages establishes discovery, activation or quality for this package. Tiers A, B and C are separately reported observations and every one of them is `NOT_RUN` for these bytes.

## Framework inputs

The governing specification (SKILL-012), the shared templates copied into `assets/`, and the contracts distilled into the other references are bound by path, revision and digest in [derivation.json](derivation.json). Those are project files, not external sources, and they are selected by the assignment owner rather than retrieved.

## Refresh sequence

Select the source revision with the assignment owner; preserve the old bytes and evidence; update the affected package derivations; regenerate only authorised installed copies; and route the changed identities into a new evaluation iteration for the affected checks. A web document changing does not by itself replace an already-selected contract, and a newer revision applies to a new iteration rather than to a closed one.
