# Conversational requirement capture — skill-validator Codex → Claude Code conversion

Recorded 2026-09-17. Supplied requirements are marked **user**; everything else is a labelled inferred default.

## R1 — user

"convert the C:\Projects\DevForgeAI\src\agents\skills\skill-validator codex skill-validator skill into a Claude skill here: C:\Projects\DevForgeAI\src\claude\skills named skill-validator."

Destination supplied outright: `C:\Projects\DevForgeAI\src\claude\skills\skill-validator`. Identity supplied: `skill-validator`. No destination question is open.

## R2 — source

Every one of the 89 source files gets an explicit disposition (preserve, rewrite, omit, add). No file is silently dropped and nothing is added that the source did not imply.

## R3 — derived

The package's **own** host interface becomes Claude Code: SKILL.md frontmatter carries all host-read metadata, `$skill-validator` invocation syntax becomes `/skill-validator`, and `allowed-tools` is derived from the declared capabilities.

## R4 — derived (the load-bearing one)

skill-validator assesses *other skill packages*. Its Codex coupling therefore splits in two and the halves need opposite treatment:

- **(a) its own host interface** — ordinary conversion, as R3.
- **(b) the host semantics of the packages it inspects** — a Claude-hosted validator inspects Claude Code packages, so the *rules it applies* change. `agents/openai.yaml` has no Claude analogue at all (both official sources state no separate metadata file is read), so the optional-configuration check family migrates onto the optional frontmatter fields rather than being find-and-replaced onto an invented path.

Concretely, the converted `skill_format.metadata_checks` must accept a YAML-list `allowed-tools`, because Claude Code documents that form and all three Claude skills already in this repository (`advisor`, `dev`, `skill-builder`) use it. Carrying the Codex string-only rule forward would make the converted validator fail its own siblings on a required check.

## R5 — derived

No operator-specific or host-specific installation root is baked into the package. `.agents/skills/<name>` must not simply become `.claude/skills/<name>`; where the source asserted an installed-path constant, the converted rule derives the path from the binding input instead.

## R6 — derived

`assets/rules-snapshot.json` is re-pinned against actually retrieved Claude Code / Agent Skills / Anthropic authoring sources, with retrieval dates, representation honesty and recorded source conflicts. No rule text, URL or digest is authored from memory. Where no equivalent Claude source was retrieved, the affected rule is marked rather than invented.

## R7 — derived

`evals/build-manifest.json` binds package paths to digests. Its rows are regenerated against the delivered bytes because one tracked path is removed and one added; a stale manifest would reference a file that no longer exists.

## R8 — project policy (CLAUDE.md, ADR-073 dual-path contract)

`src/claude/` and `.claude/` are independent byte-identical copies; an edit to either without the other silently desynchronizes the framework. The mirror is a repository layout invariant, not host configuration, and is performed and reported as a distinct step after publication.

## Explicit non-goals

No installation, hooks, settings registration, CI wiring or plugin assembly. No execution of the carried-over test suite, eval campaign or graders — authoring custody only. Validation and testing remain NOT_PERFORMED.
