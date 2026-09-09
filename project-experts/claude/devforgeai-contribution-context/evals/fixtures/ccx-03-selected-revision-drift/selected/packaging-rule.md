# Packaging rule (synthetic fixture) — revision 2

Status: revision 2. This is the revision selected by the active assignment.

RULE-PK-001: Authored evaluation inputs stay in the authored source and are omitted from the
runtime export. A runtime export carries SKILL.md, references, assets and scripts only.

RULE-PK-002: A package-local copy of a shared template records its source locator, revision and
digest, its destination digest, any transformation, and its refresh conditions.

RULE-PK-003: Changed package bytes receive a new package identity, and the affected prior
evaluation becomes stale.
