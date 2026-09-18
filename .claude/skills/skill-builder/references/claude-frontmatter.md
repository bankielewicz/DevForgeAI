# Claude Code skill frontmatter

Claude Code has no separate UI metadata file. Everything the host reads lives in the `SKILL.md` YAML frontmatter, so frontmatter authoring *is* metadata authoring — there is no `agents/openai.yaml` equivalent to write, and a converted package should not carry one.

## Fields

`name` and `description` are required. Everything else is optional and should be omitted rather than defaulted, because an absent key inherits host behavior while a written key asserts a decision the requirements may not support.

| Field | Purpose | Authoring rule |
| --- | --- | --- |
| `name` | Skill identity; matches the directory name | Preserve a valid existing name. Derive lowercase letters/digits with single hyphens, no leading or trailing hyphen, for a new skill. |
| `description` | The entire triggering mechanism | Describe what the skill does **and** the contexts that should invoke it. All "when to use" information belongs here, not in the body — the body is not in context at trigger time. |
| `allowed-tools` | Restricts the skill to named tools | Declare the capabilities the workflow actually needs. See below. |
| `model` | Model override | Set only when the task genuinely needs it. Omitting it inherits the configured session. |
| `effort` | Reasoning effort | Same rule as `model`. |
| `disable-model-invocation` | `true` makes the skill explicit-invocation only | Set only on explicit request. Implicit discovery is the default and should stay that way. |

Projects sometimes carry local bookkeeping keys such as `version`, `topics`, `last-updated` or a `metadata` block. Preserve them when editing; do not add them to a new skill without a requirement.

## Writing the description

The description is the only text the host sees when deciding whether to load the skill, so a description that documents the skill for a reader rather than advertising it to a dispatcher will under-trigger. State the capability, then the triggering contexts in the user's vocabulary — the words someone would actually type, including the cases where they describe the problem without naming the tool.

Be equally clear about what the skill does *not* cover when a neighbouring skill could plausibly claim the same request. A boundary sentence prevents two skills fighting over the same trigger, which is a more common failure than under-description.

## allowed-tools

`allowed-tools` is a real capability boundary, which makes it the right place to express constraints that would otherwise be prose asking the model to restrain itself. Declining to grant a tool is enforcement; a sentence saying "do not use subagents" is not.

Grant the minimum that the authored workflow needs. Two entries deserve deliberate thought because they widen scope more than they appear to:

- `Task` lets the skill spawn subagents. Omit it unless delegated work is part of the contract.
- `Skill` lets the skill invoke other skills. Omit it when the design requires the workflow to stop and hand off rather than continue into a downstream tool.

`Bash` accepts scoping patterns such as `Bash(git:*)` or `Bash(python:*)`. These constrain the command name, not its arguments, so a pattern that admits an interpreter admits everything that interpreter can run. Where the real constraint is narrower than the pattern can express, say so plainly in the skill body and record it as a contract obligation rather than implying the allowlist enforces it.

## Conversions

A source package from another host may carry metadata with no Claude Code equivalent. Record the substantive requirement in the authoring contract and drop the unsupported field rather than inventing a mapping — see [conversion-rules.md](conversion-rules.md) for the field-by-field treatment.
