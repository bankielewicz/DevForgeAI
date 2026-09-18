# Retrieved: Agent Skills specification

- source_id: `agent-skills`
- url: https://agentskills.io/specification
- retrieved_at_utc: 2026-09-17
- representation: documentation extraction via the host `WebFetch` tool; NOT raw HTTP bytes.
- limitation: digests bind this retained extraction, not the original transport bytes.

## Directory structure

"A skill is a directory containing, at minimum, a `SKILL.md` file." `scripts/`, `references/`, `assets/` are optional; "A skill directory may contain any files and directories beyond the required `SKILL.md`."

## Frontmatter

| Field | Required | Constraints (verbatim) |
| --- | --- | --- |
| `name` | Yes | "Max 64 characters. Lowercase letters, numbers, and hyphens only. Must not start or end with a hyphen." |
| `description` | Yes | "Max 1024 characters. Non-empty. Describes what the skill does and when to use it." |
| `license` | No | "License name or reference to a bundled license file." |
| `compatibility` | No | "Max 500 characters." |
| `metadata` | No | "Arbitrary key-value mapping for additional metadata (a map from string keys to string values)." |
| `allowed-tools` | No | "Space-separated string of pre-approved tools the skill may use. (Experimental)" |

`name` field, verbatim: "Must be 1-64 characters"; "May only contain unicode lowercase alphanumeric characters (`a-z`, `0-9`) and hyphens (`-`)"; "Must not start or end with a hyphen (`-`)"; "Must not contain consecutive hyphens (`--`)"; "Must match the parent directory name".

`description` field, verbatim: "Must be 1-1024 characters"; "Should describe both what the skill does and when to use it"; "Should include specific keywords that help agents identify relevant tasks".

`compatibility`: "Must be 1-500 characters if provided".

`allowed-tools`: "A space-separated string of tools that are pre-approved to run"; "Experimental. Support for this field may vary between agent implementations". Example: `allowed-tools: Bash(git:*) Bash(jq:*) Read`.

## Progressive disclosure

"Metadata (~100 tokens): The `name` and `description` fields are loaded at startup for all skills"; "Instructions (< 5000 tokens recommended)"; "Resources (as needed)". "Keep your main `SKILL.md` under 500 lines."

## File references

"use relative paths from the skill root"; "Keep file references one level deep from `SKILL.md`. Avoid deeply nested reference chains."

## Validation

`skills-ref validate ./my-skill` — "This checks that your `SKILL.md` frontmatter is valid and follows all naming conventions."

## Divergence recorded against Claude Code

`allowed-tools` is a space-separated **string** here; Claude Code additionally accepts a YAML list. A YAML-list value is valid for Claude Code and non-conformant to this specification. The description cap is 1024 here; Claude Code states a 1,536-character *listing truncation*, not a rejection.
