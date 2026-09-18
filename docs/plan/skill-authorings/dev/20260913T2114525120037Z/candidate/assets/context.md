# Development context template

Populate from observed inputs before production changes. Choose concrete output paths at runtime; consolidate with other human-readable records when useful. Bracketed fields are instructions to fill, not facts.

- Record identity/time: [unique identity and UTC timestamp]
- Selected project: [original locator, resolved root, host/filesystem identity]
- Current scope/authorization: [current request locator or retained text; authorized effects; exclusions; plan/subset/implementation]
- Evidence root and selection source: [explicit input, project rule, or established location]
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

| Logical record/output | Concrete location | Owner and purpose |
| --- | --- | --- |
| [context/traceability/slices/executions/checkpoints/delivery or product output] | [resolved path] | [owner] |

| Gap ID/category | Source and affected requirements/slices | Why dependent work stops | Minimum resolution and independent work |
| --- | --- | --- | --- |
| [ID and precise category] | [locators and IDs] | [reason] | [decision/input/capability needed] |

