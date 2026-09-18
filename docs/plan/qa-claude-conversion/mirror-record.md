# ADR-073 mirror record — qa

Date: 2026-09-17
Action: copied the delivered `qa` skill package from the authoring destination to the operational mirror.

- Source: `C:\Projects\DevForgeAI\src\claude\skills\qa`
- Mirror: `C:\Projects\DevForgeAI\.claude\skills\qa`
- Files: 8 (`SKILL.md`, 4 references, 3 assets)
- Package digest at time of mirroring: `947ceb2e4713b478c32df28ea4546d0595264b5cae0c08dcfa081131ff3eb31c`
- Verification: `diff -rq src/claude/skills/qa .claude/skills/qa` reports no differences.

## Why this is recorded outside the authoring runs

`skill-builder` scopes authoring to the selected `target_root`; writing elsewhere to make a
skill operate is installation and stays outside the authoring workflow. Both `qa` authoring
runs therefore bind `target_root` `src\claude\skills\qa` only, and neither record claims the
mirror. The same is true of the `dev` conversion: run
`docs/plan/skill-authorings/dev/20260917T103904Z-claude-conversion` applied package-relative
paths under `src/claude/skills/dev` and its `.claude/` copy was made outside the run.

The mirror itself is the ADR-073 dual-path contract stated in `CLAUDE.md`: `.claude/` and
`src/claude/` are independent byte-identical copies, and every sibling skill (`advisor`,
`dev`, `skill-builder`, `skill-validator`) satisfies it. The maintainer authorized this copy
explicitly on 2026-09-17 after the conversion was delivered.

## Open question this does not resolve

Design open question Q4 asked whether the mirror obligation applies to this package. The
maintainer answered yes for `qa`. Whether the ADR-073 rule should continue to govern the
current (non-legacy) skills generally remains a maintainer decision; `CLAUDE.md` scopes the
rule's stated rationale to the legacy framework while observed practice applies it to all
skills.

## Unrelated pre-existing divergence

`diff -rq .claude src/claude` also reports `agents/legacy` and `commands/legacy` present only
under `src/claude`. That divergence predates this work and was present before the conversion
began; it was not introduced or changed here.
