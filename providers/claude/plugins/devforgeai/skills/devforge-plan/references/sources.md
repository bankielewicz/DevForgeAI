# Sources and maintenance

Retrieved and inspected 2026-09-10 UTC. Framework files and package derivations are bound by path and
digest in [derivation.json](derivation.json). The sources below support design choices in this package.
None of them is evidence that this package has been installed, activated or evaluated.

## External documentation

| Source | Retrieved | Claims relied on here | Applicability and refresh |
| --- | --- | --- | --- |
| [Claude Code skills documentation](https://code.claude.com/docs/en/skills) | 2026-09-10T19:39Z | `SKILL.md` carries YAML frontmatter, and `description` is what Claude uses to decide when to apply the skill; the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing; `name` is optional and defaults to the directory name; progressive disclosure runs in phases - the description is in context every turn, the full `SKILL.md` body enters the conversation when the skill is invoked and stays across turns, and supporting files load only when referenced; supporting files are referenced from `SKILL.md` by relative Markdown links; skills load from a project `.claude/skills/`, nested `<subdir>/.claude/skills/`, personal `~/.claude/skills/`, a plugin's `skills/`, a managed settings directory and an `--add-dir` directory, and a project skill entry may be a symlink; explicit invocation is `/<skill-name>`, and a plugin skill is namespaced `/<plugin-name>:<skill-name>`; the documentation recommends keeping `SKILL.md` under 500 lines because its content stays in context once loaded. | Claude Code. Recheck when the client's frontmatter fields, discovery behaviour, installation locations or invocation syntax change. Verified against the published documentation only; **no client behaviour was observed for this package**. |
| [Agent Skills specification](https://agentskills.io/specification) | Referenced through the framework authoring contract; **not fetched for this revision** | A skill is a directory with a `SKILL.md` carrying `name` and `description` frontmatter; `scripts`, `references` and `assets` are optional and additional directories are permitted. | The portable package shape. Provider-specific discovery behaviour still needs provider evidence. |

The frontmatter here is `name` and `description` only. Every other documented optional field -
`allowed-tools`, `model`, `paths`, `context`, `agent`, `hooks` and the rest - is deliberately unused: no
tool permission, model choice, activation restriction or hook registration is asserted by this package,
and the integration owner remains the only party who wires any of those.

## Observed local facts

| Observation | When | What it establishes | What it does not |
| --- | --- | --- | --- |
| `devforge --help` and `devforge check --help` against the companion DevForge repository's own debug build (`target/debug/devforge` in that checkout; the operator's absolute path is deliberately not recorded in this package) | 2026-09-10T19:37Z | The command surface is `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`. `check` takes `--project --policy --state --expert` and its own description says it "does not certify semantic behavior". **No subcommand accepts an epic, a story, a requirement graph or an artifact envelope.** | It does not establish that any command was run against a project during this authoring. None was. It is a statement about that build at that time, not about any other build. |
| Claude provider skill inventory at base `c17e758417da64928a0f47fc2600304465ac3f3c` | 2026-09-10T19:40Z | Four skills exist: `devforge-brainstorm`, `devforge-develop`, `devforge-project-expert-creator`, `devforge-review`. No `devforge-plan`. | It does not establish that no `devforge-plan` exists anywhere - personal, managed and consuming-project inventories were not searched. |

## What is deliberately not carried here

This is a Claude package. No Codex source, hook event, per-skill provider metadata file, model setting
or authentication mode is asserted for Claude on the strength of a Codex precedent. The Codex packages'
`agents/openai.yaml`, `.agents/skills` installation paths and `$skill` invocation syntax have no
counterpart here and are not restated.

No managed-runtime section is carried either. SKILL-006 requires no managed operation, so the
managed-session checkpoint, blocking-question and routed-handoff behaviour that a delivery-aware package
carries would be an unsupported claim in this one.

## Refresh sequence

Select the source revision with the assignment owner. Preserve the old bytes and evidence. Update the
affected entries in `derivation.json`. Regenerate only the authorised installed copies. Hand the changed
identities to the evaluator for the checks they affect.

A web document changing does not by itself replace an already selected contract, and a refreshed
provenance record is not evidence about behaviour. A package or hash check proves which inputs were
referenced and never that the result is correct.
