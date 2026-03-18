# Spec-Driven Architecture — Shared Reference Loading Map

This skill does NOT duplicate reference files. All references are loaded via `Read()` from the `designing-systems` skill directory at runtime.

**Source directory:** `.claude/skills/designing-systems/`

**Why shared reads:** Single source of truth prevents drift between the legacy skill and this replacement. If a reference file is updated in `designing-systems/`, this skill automatically picks up the change.

**Dependency:** The `designing-systems/` skill directory MUST remain intact. It serves as the reference library even though it is deprecated for direct invocation.

---

## Phase-to-Reference Loading Map

| Phase | Reference Files (loaded via Read from `.claude/skills/designing-systems/`) |
|---|---|
| 01 | `references/context-discovery-workflow.md`, `references/user-input-guidance.md`, `references/architecture-user-input-integration.md` |
| 02 | `references/context-file-creation-workflow.md`, `assets/context-templates/tech-stack.md`, `assets/context-templates/source-tree.md`, `assets/context-templates/dependencies.md`, `assets/context-templates/coding-standards.md`, `assets/context-templates/architecture-constraints.md`, `assets/context-templates/anti-patterns.md` |
| 03 | `references/adr-creation-workflow.md`, `references/adr-policy.md`, `references/adr-template.md`, `assets/adr-examples/ADR-EXAMPLE-001-database-selection.md` (+ others as needed) |
| 04 | `references/technical-specification-workflow.md`, `references/system-design-patterns.md` |
| 05 | `references/architecture-validation.md` |
| 06 | `references/prompt-alignment-workflow.md` |
| 07 | `references/domain-reference-generation.md` |
| 08 | `references/architecture-review-workflow.md` |
| 09 | `assets/context-templates/design-system.md` |
| 10 | `references/post-creation-validation.md` |
| 11 | `references/epic-management.md`, `references/feature-decomposition.md`, `references/feature-analyzer.md`, `references/complexity-assessment-workflow.md`, `references/complexity-assessment-matrix.md`, `references/artifact-generation.md`, `references/epic-validation-checklist.md`, `references/epic-validation-hook.md`, `references/technical-assessment-guide.md` |

## On-Demand References (loaded when relevant context detected)

| Reference | Trigger |
|---|---|
| `references/ambiguity-detection-guide.md` | Ambiguity detected during any phase |
| `references/brownfield-integration.md` | Project mode detected as brownfield |
| `references/brownfield-map-integration.md` | Brownfield with treelint available |
| `references/dependency-graph.md` | Complex dependency analysis needed |
| `references/skill-output-schemas.yaml` | Schema validation for epic creation input |

---

## Pattern: How References Are Loaded

Each phase file begins with a **Reference Loading** section that uses explicit `Read()` calls:

```
Read(file_path=".claude/skills/designing-systems/references/{reference-name}.md")
```

References are loaded FRESH at the start of each phase. They are NOT consolidated or cached across phases. This prevents the "already covered" rationalization that enables token optimization bias.
