# Synthetic framework authority

Synthetic fixture. Operator-authored for an evaluation case. It describes no
real framework and creates no authority.

## What this fixture supplies

Accepted requirements, the governing contract extract, and the provider
conventions for a synthetic conversational framework called Ledgerworks. There
is deliberately no production application, no deployed service and no
application architecture document here: a framework workflow skill does not
need one.

## Accepted requirements

- REQ-101: a release check reads the accepted ledger, compares it against the
  candidate manifest, and reports the differences. It never edits either.
- REQ-102: every check result uses the fixed vocabulary `PASS`, `FAIL`,
  `NOT_RUN`, `COULD_NOT_RUN`, `NOT_APPLICABLE`. Results are never blended into
  a score.
- REQ-103: the workflow stops and reports when the accepted ledger cannot be
  resolved. It does not substitute a newer ledger.
- REQ-104: the closing response is short. Full inventories stay in the saved
  report.
- REQ-105: the skill authors nothing executable and grants no tool permission.
  Any requirement that must block a dependent action is recorded and routed to
  the integration owner.

## Governing contract extract

Skill packages are a `SKILL.md` with `name` and `description` frontmatter, plus
optional resource directories. Installed copies and exported plugins are
generated; the provider source directory is the only editable source. Authored
evaluation inputs stay in the source package and are excluded from installed
copies.

Compiled runtime code owns phase state, transitions, gates and acceptance.
Skill markdown owns the reasoning inside a phase. Enforcement content written
into skill text that blocks nothing is prohibited.

## Provider conventions in scope

Claude packages live under `providers/claude/plugins/ledgerworks/skills/<name>`.
Codex packages live under `providers/codex/plugins/ledgerworks/skills/<name>`.
The two are separate provider implementations with separately tracked
behaviour. This assignment covers the Claude provider only.

## What is not supplied

No accepted decision exists yet about what the release check does when the
candidate manifest is missing entirely, as opposed to empty. Treat that as an
open decision rather than inventing one.
