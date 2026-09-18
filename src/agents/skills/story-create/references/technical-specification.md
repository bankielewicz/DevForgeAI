# Technical specification and verification mapping

## Ground the design

Inspect applicable interfaces, selected architecture decisions, approved dependencies and actual source layout before describing changes. Reuse an existing owner when it already has the responsibility. Mark proposed new interfaces/paths as planned. Do not infer an HTTP endpoint from words such as “GET” or “API host”; route to API-specific detail only when the selected contract actually has that interface.

Specify inputs, outputs, constraints, state changes, ownership, dependency interfaces, failure behavior, recovery and observable tests. Keep necessary detail inside the story while referencing canonical shared requirements. A documentation-only story can have empty component arrays with an explicit reason and document/link verification obligations; do not invent executable components to satisfy a template.

## Structured technical block

Retain `technical_specification.format_version: "2.0"` for the nested structured vocabulary. It is separate from the story's 0.1.0 format. Use `components`, `business_rules` and `non_functional_requirements` arrays. Component kinds are Service, Worker, Configuration, Logging, Repository, API and DataModel. Use them only where semantically appropriate; otherwise explain the actual project contract in prose without disguising it as an unrelated kind.

For each applicable component record its name/type, purpose, real or planned project-relative path, interfaces/dependencies and requirements. Give component and requirement identities unique within the story; `id: COMP-001` can name the component, and `SVC-001`, `API-001`, `BR-001`, `NFR-001` can name obligations. Retain `implements_ac` arrays on applicable technical requirements and corresponding XML `implements` references on ACs; verify their semantic relationship explicitly rather than inferring correctness from a keyword score. No requirement may be left as a disconnected component declaration.

| Kind | Required applicable detail |
| --- | --- |
| Service | Interface/operation, lifecycle or ownership, dependencies, inputs/results, state invariants and failures |
| Worker | Trigger/schedule, concurrency, idempotency, cancellation, retry/timeout limits, restart recovery and observability |
| Configuration | Key names/types, required/default behavior, validation, safe example values, missing/invalid handling and secret boundaries |
| Logging | Events/sinks, severity, correlation, permitted/redacted fields, delivery/rotation/failure behavior where required |
| Repository | Data access interface, entity/store, operations, transaction/concurrency boundary, constraints and failure recovery |
| API | Protocol/operation, authentication/authorization, request/response/error shape, versioning and relevant idempotency/rate/size behavior |
| DataModel | Named fields/types, constraints/nullability, identity, relationships, indexes and storage mapping if applicable |

Embed complete applicable data/configuration schemas and a concrete safe example. A relational DataModel names its table and field constraints; a nonrelational model explicitly states its storage/mapping instead of inventing a SQL table. Every component requirement, configuration key, logging sink and data field has a specific `test_requirement` beginning `Test: `, or a documented verification relationship in the adjacent traceability table. Use source-defined priorities and values, not template examples as defaults.

Business rules have `id`, `rule`, `trigger`, `validation`, `error_handling`, `test_requirement` and priority where known. NFRs have `id`, `category`, `requirement`, `metric`, `test_requirement` and applicable priority. A metric specifies workload, unit/boundary and observation method, not just a number. If a mandatory value is unresolved, keep the question explicit and do not label the dependent specification ready.

## Protocol detail

**REST:** define method/path, path/query/header parameters, authentication and authorization, request media type and schema, success/error status and schema, validation order where material, pagination/filter/sort contracts, idempotency and concurrency semantics. Include realistic request/response examples, including a denial or invalid request. If the selected project requires OpenAPI, embed an appropriate version from its actual contract with `info`, `paths`, schemas and security definitions. Local internal schema references resolve within the embedded document; canonical external specifications can remain explicit governing references. Do not create a separate per-story API specification as a sidecar or claim OpenAPI validation without execution evidence.

**GraphQL:** define the selected schema/types/scalars, field nullability, queries/mutations/subscriptions, arguments, result/error behavior, authentication and field/object authorization. Specify pagination and relevant batching/cost constraints from project policy. Include an operation/variables/result example and an error example. Clarify partial data versus error behavior and subscription lifecycle when applicable.

**gRPC:** define package/service/RPC names, protobuf request/response messages, field numbers/types, enum/default semantics, unary/streaming behavior, metadata/authentication, status/error details, deadlines/cancellation and retry/idempotency rules. Include success/failure exchanges and compatibility constraints for changed fields. Do not invent field numbers or alter an existing wire contract without source authorization.

**Terminal or other interfaces:** specify the actual command/operation contract when the selected product has one: arguments, stdin/stdout/stderr, output schema, exit codes, effects, cancellation and invalid usage. Distinguish a specified future interface from an executable observed now. Documentation examples must not imply an unavailable command already exists.

## Implementation guidance

Include Implementation Guide when cross-cutting decisions or nontrivial coordination need explanation, including feature stories estimated at five or more points on the default scale. Other stories may include it when useful. Keep its Architecture Decisions, Cross-Cutting Concerns, Implementation Sequence, Task Prompt Templates, Anti-Patterns, and Patterns and References subsections. Explain concrete alternatives/rationale, data/error flow, dependency order, review/test focus and relevant existing examples. Task prompts are optional handoff text with named inputs/outputs and exclusions; they do not require an agent per phase or grant tool permissions.

## Traceability and limitations

Show both directions: every AC resolves to technical/document obligations and planned tests, and each declared component/rule/NFR resolves to selected ACs or a cited shared requirement. Resolve dangling IDs and unowned obligations. Do not fabricate dependencies simply to fill arrays.

Record known limitations under `technical_limitations` with `id`, component, limitation, decision, discovered_phase and impact. `pending` retains the unresolved decision; a proposed `defer:STORY-ID`, `descope:ADR-ID` or workaround requires actual current authorization before it changes scope. Cite that decision. A limitation cannot quietly remove an acceptance scenario.

State applicable regression, integration, negative-path, platform and recovery verification, plus source-derived measurement boundaries. The author describes these tests; development and independent QA execute and assess them in separately selected work. No generated test stub, self-score or status flag proves technical adequacy.
