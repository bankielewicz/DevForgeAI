# Sources and maintenance

Retrieved and inspected 2026-09-10 UTC. Framework files and package derivations are bound by path and digest in [derivation.json](derivation.json). The external references below support design choices in this package. None of them is evidence that this package has been installed, discovered, activated or evaluated.

## External documentation

| Source | Retrieved | Claims relied on here | Applicability and refresh |
| --- | --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | 2026-09-10 | All `SKILL.md` frontmatter fields are optional and `description` is the recommended one, because Claude uses it to decide when to apply the skill; the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing; explicit invocation is `/<skill-name>` for a project skill and `/<plugin-name>:<skill-name>` for a plugin skill, or bare when nothing collides; loading is progressive - descriptions are in context so Claude knows what is available, full skill content loads on invocation, and supporting files load only when a link is followed; skills load from a managed settings directory, `~/.claude/skills/`, `<project>/.claude/skills/`, a nested `<subdir>/.claude/skills/`, a plugin's `skills/` directory, an `--add-dir` directory, and synced account skills in cloud sessions; supporting files are referenced by relative Markdown links; keeping `SKILL.md` under 500 lines is advised because every line is a recurring token cost. | Claude Code. Recheck when the client's frontmatter fields, truncation limit, discovery locations or loading behaviour change. Verified against the published documentation only; no client behaviour was observed for this package, and nothing here establishes that this skill is discovered or activated. |
| The same page, `allowed-tools` field | 2026-09-10 | An `allowed-tools` grant lets Claude use the listed tools without prompting during the turn that invokes the skill, and the grant clears at the user's next message; every tool remains callable, and the user's permission settings still govern tools that are not listed. | Recorded because it is the one frontmatter field that changes what a skill can do without asking. **This package deliberately declares only `name` and `description`.** It therefore grants no tool permission of any kind, and every external action it describes runs under the user's existing permission settings. Recheck if that field's semantics change. |
| [Agent Skills specification](https://agentskills.io/specification) | 2026-09-10, fetched directly in repair pass 1 | A skill is a directory with a `SKILL.md` carrying YAML frontmatter; `scripts`, `references` and `assets` are optional and additional directories are permitted. The frontmatter table states `name` Required, "Max 64 characters", and **`description` Required, "Max 1024 characters. Non-empty."**, restated under the field's own heading as "Must be 1-1024 characters". `license`, `compatibility`, `metadata` and `allowed-tools` are optional. The specification names a reference validator, `skills-ref validate ./my-skill`, which "checks that your `SKILL.md` frontmatter is valid and follows all naming conventions". It also advises keeping `SKILL.md` under 500 lines. | The portable package shape, named as the base package standard by the framework authoring contract. **This package's `description` is held at or below 1,024 characters against this limit**, which is stricter than Claude Code's own documented behaviour - the client states no per-field maximum, only a 1,536-character listing truncation of `description` plus `when_to_use` combined. The stricter number is the one to keep: it satisfies both, and a spec-conformant non-Claude client or the reference validator would reject a longer one. Re-measure after any description edit. Provider-specific discovery behaviour still requires provider evidence. |

Framework evaluation evidence - the three separately reported tiers, the fixed result vocabulary, the run manifest - is a DevForgeAI release convention layered on that portable shape. It is not an additional requirement of the open standard.

## What is deliberately not carried here

This package is a Claude implementation and its claims about client behaviour come from Claude's own documentation. No hook event, model setting, authentication mode or per-provider metadata file is asserted for Claude on the strength of another provider's source, and no other provider's concepts appear in the instructions.

One exception is visible and deliberate: `assets/release-record.md` is a byte-exact copy of the framework's governing release-record template, and that template contains a line about a model-driven GitHub Action being deferred for the subscription-only MVP because its documented setup requires an API key. That template is governed outside this package's fence. Copying it byte-exact preserves its meaning and its derivation record; rewriting it from inside this fence would fork a shared template. Whether the shared wording should be provider-neutral is a decision for the template's owner, and it is recorded as an open item in this scaffold's authoring notes.

## Framework claims that are not documentation

Two facts in this package come from inspecting the built tooling rather than from any document, and they will go stale independently:

- The DevForge CLI's command surface, taken from its own `--help` on 2026-09-10: `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`. `verify`, `check` and `status` accept `--project`, `--policy`, `--state` and `--expert` at the leaf subcommand. No subcommand creates a pull request, pushes, merges, tags, publishes or deploys.
- `devforge-change`, which the roster names as the consumer of a release record, has no implementation in either provider's skill inventory as of that date.

Recheck both against the actual binary and the actual inventory rather than against this file. A capability that appears later does not make this file wrong; it makes it out of date, which is why the date is here.

## Refresh sequence

Select the source revision with the assignment owner. Preserve the old bytes and evidence. Update the affected package derivations in `derivation.json`. Regenerate only the authorized installed copies. Hand the changed identities to the evaluator for the checks they affect.

A web document changing does not by itself replace an already selected contract, and a refreshed provenance record is not evidence about behaviour. The framework references describe a local Linux/WSL POC with draft contracts; a package or hash check proves which inputs were referenced and never that the result is correct.
