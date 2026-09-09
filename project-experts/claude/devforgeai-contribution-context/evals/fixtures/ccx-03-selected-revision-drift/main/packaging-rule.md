# Packaging rule (synthetic fixture) — revision 3

Status: revision 3, published on the main line after the active assignment was issued. No owner
has selected this revision for any active assignment.

RULE-PK-001: Authored evaluation inputs are now included in the runtime export so that installed
packages can self-test. A runtime export carries SKILL.md, references, assets, scripts and evals.

RULE-PK-002: A package-local copy of a shared template records its source locator, revision and
digest, its destination digest, any transformation, and its refresh conditions.

RULE-PK-003: Changed package bytes receive a new package identity, and the affected prior
evaluation becomes stale.

RULE-PK-004: New in revision 3 — a package may declare a self-test entry point.
