# Development context template

Populate from observed inputs before production changes. Choose concrete output paths at runtime; consolidate with other human-readable records when useful. Bracketed fields are instructions to fill, not facts.

- Record identity/time: [unique identity and UTC timestamp]
- Selected project: [original locator, resolved root, host/filesystem identity]
- Current scope/authorization: [current request locator or retained text; authorized effects; exclusions; plan/subset/implementation]
- selected_evidence_value: [complete literal path value from the original input, preserving all words and characters]
- selection_source: [original request text/locator or source-qualified rule; not a paraphrased decision]
- resolved_evidence_root: [actual host-resolved absolute directory]
- Path normalization and pre-write comparison: [normalization if used; actual components compared with original selection; result or precise gap]
- Capture bounds/omissions: [relevant scope, limits, omitted/inaccessible inputs and impact]
- Existing source state: [scoped inventory/manifest locator and SHA-256; Git branch/HEAD/changes if present; ownership and ongoing work]

| Input role | Exact locator | Raw-byte SHA-256 | Relevance and availability |
| --- | --- | --- | --- |
| [selected spec, instructions, necessary reference, checkpoint] | [path] | [observed digest] | [selected versus reference-only; gaps] |

| Decision category | Effective decision or inapplicable reason | Source/locator | Supplied or inferred rationale |
| --- | --- | --- | --- |
| [architecture, technology, source tree, QA, security/operations, delivery] | [decision] | [evidence] | [origin] |

| Tool/command role | Resolved executable/version and host | Exact command/arguments and working directory | Effects, authority and availability |
| --- | --- | --- | --- |
| [build/test/format/static/coverage/native] | [observed identity] | [project-derived command] | [prerequisites/permission] |

| Logical record/output | Required concrete location | Original selection reference | Owner and purpose |
| --- | --- | --- | --- |
| [context/traceability/slices/executions/checkpoints/delivery or product output] | [resolved path beneath selected root] | [original input locator] | [owner] |

| Gap ID/category | Source and affected requirements/slices | Why dependent work stops | Minimum resolution and independent work |
| --- | --- | --- | --- |
| [ID and precise category] | [locators and IDs] | [reason] | [decision/input/capability needed] |
