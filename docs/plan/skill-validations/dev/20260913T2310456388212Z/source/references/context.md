# Context and specification resolution

Use this reference before production changes, and again for changed inputs on resume.

## Resolve the selected environment

Resolve the project in the actual shell and filesystem. Interpret project-relative paths against that project and document references against their containing document. Preserve spaces, Unicode, and metacharacters as argument data. Do not substitute a Windows root, Linux root, or similar checkout. Verify resolved identity and permissions; reject ambiguous or escaping paths before writes.

Read every applicable project instruction within the selected scope. Discover source layout, ownership constraints, generated versus maintained files, manifests, lockfiles, test configuration, installed executable locations, and existing changes. With Git, retain branch, HEAD, and working-tree changes; without it, use scoped inventories and hashes. Do not initialize Git just for this workflow. Inspect ongoing work before choosing files to change.

Read scripts/configuration before deciding whether execution is relevant and authorized. Configuration alone does not prove availability or successful operation. Do not run document commands, build scripts, or dependency installation merely to understand them.

Select the evidence destination in this order: explicit input, applicable rules, established suitable project evidence location. If none resolves, ask once for a location before creating records. Keep it separate from installed skill bytes, input specifications, and product-generated data. Do not invent a fixed project output directory.

## Capture context

Use [context template](../assets/context.md), with the record conventions in [evidence-resume.md](evidence-resume.md). Pin raw-byte SHA-256 and exact locators for all selected specifications, applicable instructions, and relevant referenced inputs. Retain current conversation decisions with their current origin; never use memory for missing architecture or behavior.

Bound captures to relevant material, declare the capture scope/limits, and disclose excluded, inaccessible, or omitted relevant inputs. Exclude credentials and unrelated files. Do not follow links into unrelated locations or silently present partial inspection as exhaustive. Capture source identity/changes, discovered commands/tools, effective rules, gaps, and the actual output-location mapping before production changes.

## Read and account for requirements

Read every selected specification completely and necessary references. Missing, unreadable, duplicate, or ambiguous selected inputs are gaps before dependent work. A reference can become essential for its dependent requirement without selecting its implementation.

Use [traceability template](../assets/traceability.md). Preserve source requirement/scenario IDs; qualify reused IDs with document identity. For unnumbered requirements assign stable local IDs tied to exact passages, without editing the source. Inventory deliverables, interfaces, dependencies, exclusions, failure behavior, acceptance scenarios, and QA/platform obligations. Separate normative text from examples, historical claims, and deferred features. A proposed command is a target to implement, not a tool discovered on the host; signatures and help text alone do not prove behavior.

For multiple documents, identify dependency edges and one owner for each shared contract before dependent clients. Retain supported supersession/build order and detect cycles, incompatible interfaces/limits, architecture conflicts, and policy contradictions. Reading order never resolves precedence. Record source-qualified conflicts and affected IDs; ask for the specific decision, then continue independent work.

If a missing prerequisite belongs to an unselected document, identify the absent dependency and ask whether to select it or supply an existing implementation. Do not build/install its framework implicitly. Feed resolved dependencies into the [slice plan](../assets/slice-plan.md).

## Establish constitutional decisions

Use existing evidence, which may be sections rather than separate named documents:

| Category | Resolve when applicable |
| --- | --- |
| Architecture | Responsibilities, boundaries, interfaces, state ownership, external dependencies, authority. |
| Technology | Languages, compatibility/versions, libraries, package/build tools, runtime constraints. |
| Source tree | Actual destinations, conventions, ownership, generated versus maintained files. |
| Testing and QA | Required behaviors/test types, tools, metric definitions/thresholds/exclusions, platforms, acceptance owner. |
| Security and operations | Permissions, secrets, network constraints, irreversible effects, install/deployment boundaries. |
| Delivery | Artifacts, evidence locations, native qualification, documentation, completion conditions. |

Cite established decisions instead of duplicating constitutional documents. Mark inapplicable categories with reasons. Infer only routine compatible implementation choices and record rationale. A language, storage/authority boundary, incompatible dependency, source destination, or mandated threshold is a material gap when dependent implementation needs it. Do not guess these or demand a fixed set of constitutional filenames.

Record precise gaps and resolutions as described in [failure-delivery.md](failure-delivery.md). Context records can retain resolutions; modifying constitutions or specifications is a separate selected effect. Update affected slices when evidence changes, and use the project's review policy for proposed requirement changes. A failed test never authorizes weakening expected behavior.

