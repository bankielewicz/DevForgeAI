# Sources consulted while authoring this package

Each row records what was actually read and the specific claims relied on. A documentation claim is a fact about the documentation. It is not an observation of client behaviour for this package, and nothing here was verified by running this skill.

## Fetched during this authoring pass

| Source | Retrieved (UTC) | Claims relied on |
| --- | --- | --- |
| Claude Code skills documentation, https://code.claude.com/docs/en/skills | 2026-09-10 | A skill is a `SKILL.md` with YAML frontmatter; `description` is what Claude uses to decide when to apply the skill, and description text stays in context while the body loads only on use. Supporting files are referenced from `SKILL.md` by package-relative Markdown links and load only when followed. Skills load from a project `.claude/skills/<name>`, a personal `~/.claude/skills/<name>`, a nested `<subdir>/.claude/skills/<name>`, a plugin's `skills/<name>`, and a managed settings directory. Invocation is `/<skill-name>`, or `/<plugin-name>:<skill-name>` for a plugin skill. Keeping `SKILL.md` short and moving conditional detail into linked files is the documented guidance. |

Two details from that page are worth recording precisely, because a loose reading of either would be wrong.

**Tool permissions.** The page documents an `allowed-tools` frontmatter field that pre-approves listed tools for the turn that invokes the skill, and a `disallowed-tools` field that removes tools while the skill is active. This package uses neither: its frontmatter carries `name` and `description` only, per the DevForgeAI skill-authoring contract. So this package grants no tool permissions and removes none - which is a fact about this package, not a property of the client. Any statement that "a skill grants no tool permissions" is true here only because of what this frontmatter omits.

**Description budget.** The page states that `description` (combined with an optional `when_to_use`) is truncated at 1,536 characters. This package's description is a single plain scalar well inside that bound, with no colon-space sequence, no block scalar and no quoting that a restricted frontmatter reader would have to interpret.

## Carried from the builder, not re-verified here

| Source | Origin | Status |
| --- | --- | --- |
| Claude Code subagents documentation, https://code.claude.com/docs/en/sub-agents | Recorded in `devforge-project-expert-creator/references/sources.md` at commit 4999f3106565c5e320d1f1a7db066b437e4e94be, retrieved 2026-09-10 by that author | Not fetched during this pass. Nothing in this package depends on subagent behaviour; the row exists so a reader can see which of the builder's sources were and were not re-checked. |

## Framework sources

The governing specification, templates and contracts are DevForgeAI repository documents, not external sources. Their exact paths, revisions and SHA-256 digests are recorded in `derivation.json` rather than duplicated here, because that record is the one a refresh has to reconcile against.

## Not carried over

The Codex-side OpenAI documentation sources recorded in the Codex packages are not relied on by this Claude package. The Agent Skills specification is referenced through the framework's own authoring contract rather than fetched at this revision.

## Refresh conditions

Re-check the claims above and update the retrieval date when the Claude Code skills documentation changes materially - particularly the frontmatter field set, the description budget, the skill load locations or the invocation forms. A changed page invalidates the claims relied on, not merely the date.
