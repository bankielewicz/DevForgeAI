# Sources consulted while authoring this package

This records what was read and when, so a later reader can tell a checked claim from an assumption about the client. It is an authoring record. It establishes nothing about this package's behaviour, which is `NOT_EVALUATED`.

## Claude Code Agent Skills documentation

- **Source:** https://code.claude.com/docs/en/skills
- **Retrieved:** 2026-09-10 (UTC date of this authoring session)
- **Method:** fetched and read as rendered documentation text. Not exercised against a running client; no discovery, activation or loading behaviour was observed.

Claims taken from it and what each was used for:

| Claim as stated by the documentation | Used for |
| --- | --- |
| A skill is a directory containing `SKILL.md`, with optional supporting files loaded only when the instructions link to them. | The package shape: `SKILL.md` plus `assets/` and `references/` linked at the point that needs them. |
| The `description` field is what Claude uses to decide when to apply the skill. | Writing the description as a trigger statement rather than a summary. |
| "Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing to reduce context usage." | Keeping the description well inside that bound and leading with what the skill does. |
| Installation locations differ in scope: `~/.claude/skills/<name>/`, `<project>/.claude/skills/<name>/`, a nested `<subdir>/.claude/skills/<name>/`, a managed settings directory, and a plugin's `skills/<name>/`. A plugin skill is invoked as `/plugin-name:skill-name`. | The two-roots rule, and the instruction to confirm what is actually installed before naming an invocation form in a handoff. |
| "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files." | Splitting the conditional detail into `references/recording-rules.md` and `references/evidence-and-scope.md`. |
| Dynamic context injection exists: a line beginning `!` followed by a backticked command is executed and replaced with its output before Claude sees the content. | Deliberately **not used**. This package contains no `!`-prefixed injection; command examples appear in fenced `text` blocks so nothing executes on load. |
| The rendered `SKILL.md` enters the conversation once and stays across later turns; Claude Code does not re-read the file on later turns. | Keeping the body short enough to be worth carrying, with detail behind links. |

**Discrepancy worth recording.** The client documentation states that no frontmatter field is required and that `name` defaults to the directory name. The DevForgeAI skill-authoring contract (identity recorded in `derivation.json`) and the Agent Skills specification it cites require `name` and `description`. This package follows the stricter framework requirement: frontmatter carries exactly `name` and `description`. That is a deliberate choice, not an inference that the client rejects a missing field.

**Not used.** The documentation also describes `allowed-tools`, `disallowed-tools`, `disable-model-invocation`, `user-invocable`, `context: fork`, `agent`, `background`, `model`, `effort`, `argument-hint`, `arguments`, `when_to_use`, `paths`, `shell`, `hooks` and `metadata`. None appears in this package's frontmatter. The framework contract fixes the frontmatter at `name` and `description`, and a skill grants no tool permissions here.

## Framework sources

The governing specification, templates and contracts are recorded with their exact identities in `derivation.json` rather than repeated here. Hook declarations and runtime requirements are integration-owner scope and are not part of this package.

## DevForge CLI command surface

- **Source:** `devforge --help` from the compiled binary at `framework/DevForge/target/debug/devforge`.
- **Observed:** 2026-09-10, during authoring.
- **Observed subcommands:** `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status`, `isolate`, `help`.
- **Also observed:** `devforge check --help`, which prints exactly one description line: "Check structural policy and provenance; does not certify semantic behavior".
- **Used for:** the statement in `SKILL.md` and `references/recording-rules.md` that no command in this surface resolves an artifact's upstream reference, validates a product brief, or gates its adoption - so that gap is named as a missing integration rather than implied to exist.
- **Limit:** a `--help` listing establishes which subcommands the binary exposes. It says nothing about their behaviour, and this authoring session executed none of them.

## DevForge external policy schema

- **Source:** the companion DevForge repository's `policies/*.json`, observed through `policies/notes-sqlite.json` at sha256 `5da0f2075b1246cb86d9e3b2f3125ab793f8abfc2349069dd39bf18f8e3d1649`.
- **Observed:** 2026-09-10, read-only.
- **Observed top-level keys:** `schema`, `project_id`, `goal`, `story_id`, `upstream`, `dependencies`, `dependency_file`, `source_roots`, `test_root`, `expert_dirs`, `forbidden_tokens`, `tooling_files`.
- **Used for:** the more specific half of the `devforge check` sentence in `SKILL.md` and `references/recording-rules.md` - that it checks a project candidate's dependencies, layout, tooling pins and expert provenance. `check --help` alone would support only the generic wording, so the specific claim is sourced here rather than left unsupported.
- **Limit:** this is the shape of the external policy that drives the check, read from one project's policy file. It is not an observation of the check running, and neither the binary nor this policy file was digest-pinned by an authority outside this session. The companion repository owns both; nothing in this package resolves either at runtime.
