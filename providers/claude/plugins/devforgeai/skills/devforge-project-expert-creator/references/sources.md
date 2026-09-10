# Sources and maintenance

Retrieved and inspected 2026-09-10 UTC. Framework files and package derivations are bound by path and digest in [derivation.json](derivation.json). The external references below support design choices in this package. None of them is evidence that this package has been installed, activated or evaluated.

## External documentation

| Source | Retrieved | Claims relied on here | Applicability and refresh |
| --- | --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | 2026-09-10 | `SKILL.md` carries YAML frontmatter, with `description` used for automatic invocation decisions and truncated at 1,536 characters combined with `when_to_use`; explicit user invocation is `/<skill-name>`, and a plugin skill is namespaced `/<plugin-name>:<skill-name>` or bare when no name collides; progressive loading in three phases - description in context every turn, body on invocation, supporting files only when a link is followed; skills load from `<project>/.claude/skills/`, nested `.claude/skills/`, `~/.claude/skills/`, a plugin's `skills/` directory, a managed settings directory and an `--add-dir` directory; supporting files are referenced by relative markdown links; a `SKILL.md` body is recommended to stay under 500 lines because it persists in context after invocation. | Claude Code. Recheck when the client's frontmatter fields, discovery behaviour or installation locations change. Verified against the published documentation only; no client behaviour was observed for this package. |
| [Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents) | 2026-09-10 | A subagent is defined by YAML frontmatter plus a Markdown system prompt, with `name` and `description` required and `tools`, `model` and `skills` among the optional fields; the `skills` field preloads full skill content into a subagent at startup rather than only its description; `model` accepts an alias, a full model ID or `inherit`; subagent definitions live in `.claude/agents/`, `~/.claude/agents/` and a plugin's `agents/` directory, resolved by priority. | Claude Code. Relevant only because an expert package may be preloaded by an integration owner's subagent; this skill authors no subagent and registers nothing. Recheck when the subagent frontmatter or resolution order changes. |
| [Agent Skills specification](https://agentskills.io/specification) | Referenced through the framework authoring contract, not fetched for this revision | A skill is a directory with a `SKILL.md` carrying `name` and `description` frontmatter; `scripts`, `references` and `assets` are optional and additional directories are permitted. | The portable package shape. Provider-specific discovery behaviour still requires provider evidence. |

Framework evaluation evidence is a DevForgeAI release convention layered on that portable shape; it is not an additional requirement of the open standard.

## What is deliberately not carried here

This package is a Claude implementation. The Codex creator's sources - the OpenAI skill, hook, prompt-engineering and evaluation-practice pages - support that provider's design decisions and are not repeated as though they governed Claude behaviour. No hook event, model setting, authentication mode or per-skill provider metadata file is asserted for Claude on the strength of a Codex source.

## Refresh sequence

Select the source revision with the assignment owner. Preserve the old bytes and evidence. Update the affected package derivations in `derivation.json`. Regenerate only the authorised installed copies. Hand the changed identities to the evaluator for the checks they affect.

A web document changing does not by itself replace an already selected contract, and a refreshed provenance record is not evidence about behaviour. The framework references describe a local Linux/WSL POC with draft contracts; a package or hash check proves which inputs were referenced and never that the result is correct.
