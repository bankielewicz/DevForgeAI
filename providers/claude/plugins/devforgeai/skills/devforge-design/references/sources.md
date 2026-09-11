# Sources consulted while authoring this package

Each entry records what was actually read, when, and the specific claim it supports. Retrieval dates are the authoring date; a later reader should re-check anything marked as a client behaviour, because client documentation changes without notice.

## Claude Code client facts

Source: <https://code.claude.com/docs/en/skills>, retrieved 2026-09-10 UTC via an automated fetch that converts the page to Markdown. The fetch summarised the page rather than returning it verbatim; the claims below are what that summary stated, and none of them was separately observed in a running client by this author.

| Claim used | How it shaped this package |
| --- | --- |
| A skill is a directory containing `SKILL.md`; frontmatter is read only when the opening `---` is the file's first line. | `SKILL.md` opens with `---` on line 1. |
| The `description` is what Claude uses to decide when to apply the skill; the combined description text is truncated at 1,536 characters in the skill listing. | The description states the job, the direct and indirect activating conditions, and the near-miss exclusions by sibling skill name, and is kept well inside that limit. |
| Skills load from enterprise, personal (`~/.claude/skills/<name>/`), project (`.claude/skills/<name>/`), nested subdirectory, and plugin (`<plugin>/skills/<name>/`) locations. | The package resolves its own resources against the loaded `SKILL.md` directory rather than any fixed path, so it works from any of these. |
| Plugin skills are invoked as `/plugin-name:skill-name`; for a plugin skill the frontmatter `name` sets the command's final segment. | `name: devforge-design` matches the directory name, so the invocation form is stable whichever installation mode is used. This package still does not assert an invocation form in a handoff without confirming what is installed. |
| Progressive disclosure: linked reference files are loaded when the link is followed, so large reference material does not enter context every turn. | Conditional detail lives in `references/`, linked at the phase that needs it. |
| Recommended size: keep `SKILL.md` under 500 lines. | `SKILL.md` is well inside that. |
| `allowed-tools` grants time-limited tool permission for the invoking turn; `disallowed-tools` removes tools. | Neither is used. This skill needs no elevated permission, and the DevForgeAI authoring assignment restricts frontmatter to `name` and `description`. |
| Claude Code supports a dynamic-context-injection syntax that runs a shell command at skill-load time and substitutes its output into the skill content. | Deliberately not used, and the syntax is not reproduced anywhere in this package. Every command example is inside a `text` fence so nothing executes when the skill is loaded. |
| A skill folder must not be named `synced`. | Not applicable; the folder is `devforge-design`. |

The DevForgeAI authoring contract restricts this package's frontmatter to `name` and `description` regardless of what the client additionally supports. Where the client offers a capability the contract does not select, the contract governs.

## Governing DevForgeAI inputs

Read from the DevForgeAI checkout at base revision `c17e758417da64928a0f47fc2600304465ac3f3c`. Exact paths and digests are in `derivation.json`. These are repository-relative provenance records of what was read while authoring this package. They are not runtime lookups: nothing in this package reads them at load time, and the package works with no DevForgeAI checkout present.

| Source | What it settled |
| --- | --- |
| `docs/mvp/specifications/skill-003-devforge-design.md` | The governing specification: user goal, use-case inventory, inputs and provenance, the four workflow phases and their exits, the output artifact and its template, the acceptance cases and common cases, rework and stopping conditions. |
| `docs/mvp/templates/devforge-design/design-spec.md` | The design-spec output shape, copied unchanged into `assets/`. |
| `docs/mvp/templates/shared/handoff.md` | The handoff shape, copied unchanged into `assets/`. |
| `docs/mvp/skill-authoring-contract.md` | Package structure, the `evals/` packaging decision, derivation records, the three separately reported evaluation tiers and their vocabulary. |
| `docs/mvp/artifact-contract.md` | The `devforge.artifact/v1` envelope, upstream reference resolution, the no-self-digest rule, and the separation of document status from readiness and behavioural evaluation. |
| `docs/mvp/execution-contract.md` | Worktree and ownership behaviour on a concurrent-writer collision, and the rule that a handoff names an actual installed skill or a plain-language task. |
| `docs/mvp/roster.md` | The provenance flow: this skill consumes the product-brief (and optionally the architecture-contract, an existing design-spec, and a prototype-report or change-request), and its design-spec is read by prototype, architect, plan, review and change. |
| `docs/development-language-policy.md` | Rust owns phase state, transitions and gate checks; skills own the reasoning inside a phase; ceremonial enforcement in skill content is prohibited. |
| `docs/learned-behaviors/bounded-delivery.md` | The finite stopping condition, and the rule that a prepared result with honest unknowns is a finished result. |

## Rust command surface

Observed 2026-09-10 by running the compiled DevForge binary's own help at the debug build path in the authoring environment:

```text
<devforge-binary> --help
```

It listed exactly these subcommands: `delivery`, `expert`, `check`, `init`, `red`, `green`, `accept`, `verify`, `status` and `isolate`. None of them reads a design-spec, resolves its upstream references, or verifies a mockup digest. `SKILL.md` states that gap as a missing integration owned by the integration owner rather than naming a command that does not exist.

This is an observation of one build at one moment. Re-check the installed binary's own help before relying on it; a subcommand added later does not make this record wrong, it makes it old.
