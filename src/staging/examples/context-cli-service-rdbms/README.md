# Example: context documents for a CLI, a service and a relational store

A filled set of project context documents (DevForgeAI ADR-004), for a small command-line tool,
`shiftlog`. It mirrors a project's `docs/specs/` folder so it can be copied into a fixture as-is.

- `arch/ARCH-001.md`: three components, one per kind the set covers: `user-interface` (CMP-01),
  `service` (CMP-02) and `relational-store` (CMP-03).
- `context/`: the documents those kinds need, validated against `src/schemas/context.schema.json`:
  - the five core documents: `index.md`, `architecture.md`, `tech-stack.md`, `source-tree.md` and
    `testing.md`;
  - `front-end.md` and `ui-mockups.md` (user-interface), `middle-tier.md` (service) and `rdbms.md`
    (relational-store);
  - one detail file, `rdbms/migrations.md`.
- `adr/ADR-001.md` and `adr/ADR-002.md`: the example project's two accepted decisions.
- `ambiguities/AMB-001.md`: a log with one accepted entry that names CTX-003 (a change within TEC-02's
  allowed range, a convention) and one open entry,
  validated against `src/schemas/ambiguities.schema.json`.

Every `basis` appears at least once. `source-tree.md` is a draft because it still holds a proposed root
(SRC-10); the other documents are approved. `ui-mockups.md` indexes one approved design, recorded in
STORY-001. `testing.md` cites only DevForgeAI defaults, because no
policy key for testing exists until the testing-policy schema change. The project's ADR-001 and ADR-002
are the example project's own decisions, not DevForgeAI's ADRs; they are included, minimal, so that each
`decision` statement resolves. PRD-001 and STORY-001 are cited but not included: a fixture generator seeds
them. `freshness_days: 90` is an example value only.
