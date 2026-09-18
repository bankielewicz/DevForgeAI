# Adaptive records and portable package contracts

These are project-policy interfaces, not additional required Codex metadata. All new JSON schemas are closed Draft 2020-12 records. Read the schema for the selected mode; ordinary authoring requirements and legacy schemas retain their existing meanings.

| Input/output | Schema |
| --- | --- |
| Captured project facts, exclusions, capabilities and gaps | [project-evidence-v1](../schemas/project-evidence-v1.schema.json) |
| Proposal/update review with requirements, members and handoffs | [adaptation-proposal-v1](../schemas/adaptation-proposal-v1.schema.json) |
| Exact authorized selected members/destinations | [adaptation-selection-v1](../schemas/adaptation-selection-v1.schema.json) |
| Per-member results and aggregate state | [set-authoring-v1](../schemas/set-authoring-v1.schema.json) |
| Full set or explicit eligible subset manual request | [set-validation-request-v1](../schemas/set-validation-request-v1.schema.json) |
| Portable role descriptor | [adaptive-skill-v1](../schemas/adaptive-skill-v1.schema.json) |
| Separately owned operational binding | [project-binding-v1](../schemas/project-binding-v1.schema.json) |
| Read-only input observation | [adaptive-observation-v1](../schemas/adaptive-observation-v1.schema.json) |
| Runtime binding observation | [binding-observation-v1](../schemas/binding-observation-v1.schema.json) |

Use strict UTF-8 JSON: reject duplicate keys, nonfinite numbers, unsupported versions and unlisted fields. Strings are nonempty; integers exclude booleans. Names are 1–64 ASCII lowercase alphanumeric components with single separating hyphens. IDs are nonempty ASCII alphanumeric-leading strings using letters, digits, dot, underscore and hyphen. IDs are unique in their declared collections. Relative paths use forward slashes with no absolute root, drive, backslash, NUL, empty/dot/traversal component or link/junction traversal.

New external Ref paths are resolved absolute locators of already retained files; SHA-256 binds raw bytes. Locators use inclusive one-based line spans in saved UTF-8 text and must support their claim. Derived requirements need rationale; source/user requirements need supporting retained input. No inferred requirement supplies authorization. Capabilities record observed availability separately from declared toolchain intent. Gaps name an actual missing input, choice, capability or scope resolution.

PackageRef manifests are complete sorted arrays of `{path, bytes, sha256}`. Hash compact UTF-8 JSON with unescaped Unicode and row keys in that exact order. Timestamps/roots are outside the digest. New arrays may be copied from an existing authoring manifest's `files`, retained as a new external file; do not modify or reinterpret the legacy manifest. Unexpected files and incomplete capture invalidate exact package binding. Capture mutable existing/parent packages before editing, preserving their named directory; PackageRef.root may locate those immutable bytes while Member.target_root selects the live destination. Retention verifies live bytes against the same snapshot. No source locator becomes a runtime constant.

## Core lineage and requirements

Core packages express reusable workflow with project convention discovery; no invented product/toolchain assumptions. Variants preserve core bytes and record a non-null exact parent PackageRef, distinct identity, and one disposition for every parent requirement. Retained requirements have equivalent child statements; modified requirements identify replacements; removed requirements identify the current explicit authorization and reason. Cite that current instruction in a user Requirement that names the removed parent ID. Inspect the cited meaning: the helper cannot grant consent from a matching ID. Expertise and core have null parent and empty lineage arrays.

For newly authored adaptive contracts, include a fenced `devforgeai-requirements` JSON array of `{id, statement}` rows as an unambiguous requirement locator. The read-only helper uses that index for full parent accounting. Existing cores may instead have an unambiguous Markdown requirement table with ID/Requirement or Requirement/Required behavior columns anywhere in their bounded captured Markdown resources; they need no adaptive descriptor or particular contract filename. If the selected core's requirement inventory cannot be resolved, retain a precise mapping gap rather than editing core, inventing origin or treating a missing convenience file as absence. Semantic equivalence, current authorization and domain support still need source inspection.

## Generated adaptive package

Author `assets/devforgeai-skill.json` and `references/adaptive-contract.md`. Descriptor name matches directory/frontmatter; role is core, project_variant or expertise, binding_required is true, contract_path is exactly `references/adaptive-contract.md`, and required_capabilities includes Python 3.10+. The parent field is null except for variants, which carry only parent name, digest and full requirement IDs. No own digest (self-reference), absolute source locator, installation root, project UUID or copied binding is permitted. Relative domain facts/paths and role names are permitted.

The linked contract defines responsibilities/exclusions, activation and near misses, relative input/output contracts with concrete observable fields, effects, recovery, dependencies, requirement IDs and parent dispositions. Include observable completion and failure behavior, not a quality adjective. Unknown essential behavior blocks authoring. Domain evidence locators here are project-relative; retain machine-absolute custody references only in external evidence. Resource roles identify actual runtime/template/reference/fixture/license paths with reasons; each resolves, and its consumer still needs inspection. Do not create empty scaffolds or a generated-skill test campaign.

Link the descriptor and contract from generated SKILL.md, and expose the runtime prerequisite there before product actions. Copy [check_project_binding.py](../assets/adaptive-runtime/check_project_binding.py) unchanged into generated `scripts/`, declare its runtime role, and author the [binding instructions](project-binding.md). Ordinary non-adaptive skills and builder/validator themselves need no descriptor or installed binding.

## Read-only helper limits

`adaptive.py inspect --record` accepts only the new record families and prints VALID/INVALID/UNAVAILABLE (exit 0/1/2), errors and an empty order. `plan-set --selection` also verifies pre-authoring destinations/capabilities and returns deterministic ASCII-ID topology. Neither writes, executes described commands, runs quality checks or publishes members. CLI usage errors exit 2 on stderr. Retained refs and complete package bytes are reread; references, cycles, collection IDs, subset omissions and reductions are checked. Supporting passage semantics, redundancy, authorization and claimed absence still require author inspection; VALID is not semantic approval. Existing custody helpers are the only per-member publication interface.
