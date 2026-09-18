# Shared adaptive record definitions

These frozen project-policy schemas are input contracts for read-only validation, not authoring or operational setup instructions. Read the relevant family only. Schema documents under ../schemas are local data; scripts/adaptive_contracts.py is an independent validator reader. Ordinary skills need no adaptive descriptor.

### 5.1 Type notation and common rules

The following tables are closed record schemas: every listed field is required unless explicitly marked optional; no unlisted fields are accepted. `T?` means either a T value or JSON null. Arrays may be empty unless a minimum is stated. All strings are nonempty unless expressly allowed empty. Integers exclude booleans. JSON is UTF-8, rejects duplicate keys/non-finite numbers, and uses no executable deserialization. Implement equivalent JSON Schema Draft 2020-12 documents and semantic cross-reference checks; the tables define requirements beyond JSON Schema expressiveness.

- `Digest`: 64 lowercase hexadecimal SHA-256 characters over actual raw bytes.
- `Name`: 1-64 ASCII lowercase letters/digits with single separating hyphens, matching `^[a-z0-9]+(?:-[a-z0-9]+)*$`. This is the adaptive project's naming policy, not a claim about all hosts.
- `Id`: nonempty ASCII string matching `^[A-Za-z0-9][A-Za-z0-9._-]*$`, unique within its declared record collection.
- `RelPath`: forward-slash package/project-relative path; no empty components, absolute root, drive, backslash, `.`/`..`, NUL, or link/junction traversal. Resolve under the declared base and inspect existing ancestors before access.
- `Ref`: `{path: string, sha256: Digest}`. In new external builder/set records, `path` is the resolved absolute path of an already retained file. Existing validator schema-1 run-relative references retain their existing base. Never silently reinterpret a reference between these families.
- `Locator`: `{ref: Ref, start_line: integer >= 1, end_line: integer >= start_line}` over saved UTF-8 text. It must locate a supporting passage, not just an existing file.
- `Requirement`: `{id: Id, origin: user|source|derived, statement: string, source_refs: Locator[], rationale: string?, verification: string}`. Source/user requirements need supporting retained input; derived requirements require rationale. No inferred requirement is presented as user authorization.
- `Capability`: `{id: Id, command: string, required: boolean, observed: available|unavailable|unknown, evidence: Ref?, limitation: string?}`. A command is a description, not shell text to execute automatically.
- `Gap`: `{code: Id, member_id: Id?, requirement_ids: Id[], description: string, resolution: string, evidence: Ref[]}`. Each resolution names an actual missing input, choice, capability, or scope change.

Package manifests are sorted arrays of `{path: RelPath, bytes: integer >= 0, sha256: Digest}` for every permitted regular package file. Compute `package_digest` as SHA-256 of compact JSON UTF-8 with unescaped Unicode; key order in each row is `path`, `bytes`, `sha256`; rows sort by path. Exclude timestamps and absolute roots from the digest. Omitted material makes capture incomplete; never use an incomplete digest as a complete runtime binding. Reject unexpected files during exact binding checks rather than treating them as harmless exclusions.

Use fresh UTC run IDs `YYYYMMDDTHHMMSSffffffZ`; on collision allocate a new timestamp, never overwrite. Timestamps use UTC RFC 3339 strings with `Z`. Record real source changes and retries; do not synthesize successful history.


## Project evidence and proposals

| Record | Fields |
| --- | --- |
| `project-evidence-v1` | `schema_version` constant; `run_id: Id`; `project_root: string`; `scope_roots: string[]` minimum 1; `inputs: Ref[]`; `facts: Fact[]`; `exclusions: Exclusion[]`; `complete: boolean`; `capabilities: Capability[]`; `gaps: Gap[]`. |
| `Fact` | `id: Id`; `category: architecture\|domain\|language\|toolchain\|development_style\|requirements\|existing_skills\|constraint`; `statement: string`; `basis: observed\|user_supplied\|unknown`; `sources: Locator[]`. Unknown facts have no asserted conclusion and explain what is unknown. Other facts require sources. |
| `Exclusion` | `path: string`; `reason: string`; `material: boolean`. |
| `adaptation-proposal-v1` | `schema_version` constant; `run_id: Id`; `mode: propose\|review_updates`; `project_evidence: Ref`; `prior_proposal: Ref?`; `requirements: Requirement[]`; `members: Member[]`; `handoffs: Handoff[]`; `gaps: Gap[]`; `state: PROPOSED\|BLOCKED\|NO_CHANGE`. |
| `Member` | `id: Id`; `name: Name`; `role: core\|project_variant\|expertise`; `action: retain\|create\|revise`; `target_root: string?`; `existing_package: PackageRef?`; `parent_core: PackageRef?`; `responsibility: string`; `exclusions: string[]`; `triggers: string[]` minimum 1; `near_misses: string[]` minimum 1; `requirement_ids: Id[]` minimum 1; `fact_ids: Id[]`; `rationale: string`; `depends_on: Id[]`; `capabilities: Capability[]`; `lineage_delta: LineageRow[]`. |
| `PackageRef` | `name: Name`; `root: string`; `manifest: Ref`; `package_digest: Digest`. Root is a development/evidence locator, never copied into runtime metadata. Manifest binds complete captured bytes. |
| `LineageRow` | `requirement_id: Id`; `disposition: retained\|modified\|removed`; `reason: string`; `replacement_requirement_ids: Id[]`. Every parent requirement occurs once; modified rows require replacements; retained rows refer to the equivalent child requirement; removed rows require a current authorized reason. |
| `Handoff` | `id: Id`; `producer: Id`; `consumer: Id`; `artifact_role: Id`; `format: json\|text\|file_set`; `schema_ref: Ref?`; `contract: string`; `required: boolean`; `failure_behavior: block_consumer\|report_optional_absence`. JSON requires a local schema Ref; other formats require concrete observable fields/content rules in `contract`. |
## Selection and set envelopes

| Record | Fields |
| --- | --- |
| `adaptation-selection-v1` | `schema_version` constant; `proposal: Ref`; `member_ids: Id[]` minimum 1 and unique; `destinations: Destination[]`; `authorization: Ref`; `permitted_effects: string[]`. |
| `Destination` | `member_id: Id`; `target_root: string`. Exactly one for each selected member. A different destination from the proposal is allowed only if the captured current instruction explicitly selects it; recheck collisions. |
| `set-authoring-v1` | `schema_version` constant; `run_id: Id`; `selection: Ref`; `ordered_member_ids: Id[]`; `members: MemberResult[]`; `state: AUTHORED\|PARTIAL\|BLOCKED\|NO_CHANGE`; `validation_status: NOT_PERFORMED`; `testing_status: NOT_PERFORMED`; `issues: Gap[]`. |
| `MemberResult` | `member_id: Id`; `status: AUTHORED\|RETAINED\|PARTIAL\|BLOCKED\|DEPENDENCY_BLOCKED`; `authoring_record: Ref?`; `validation_request: Ref?`; `package: PackageRef?`; `reason: string`; `applied_paths: RelPath[]`. |
| `set-validation-request-v1` | `schema_version` constant; `run_id: Id`; `selection: Ref`; `set_authoring: Ref`; `scope: full_set\|eligible_subset`; `members: AssessmentMember[]` minimum 1; `handoffs: Handoff[]`; `omitted_member_ids: Id[]`; `omitted_handoff_ids: Id[]`; `permission: string`. Permission states that the packet grants no external effects. |
| `AssessmentMember` | `member_id: Id`; `package: PackageRef`; `request: Ref?`; `adaptive_descriptor: Ref?`. `request` binds a `validation-request-v1` or is null for retained/standalone packages. Adaptive members require a descriptor Ref. |
## Portable descriptors

| Record | Fields |
| --- | --- |
| `adaptive-skill-v1` | `schema_version` constant; `name: Name`; `role: core\|project_variant\|expertise`; `binding_required: true`; `parent_core: CoreLineage?`; `contract_path: RelPath`; `required_capabilities: string[]`; `resource_roles: ResourceRole[]`. |
| `CoreLineage` | `name: Name`; `package_digest: Digest`; `requirement_ids: Id[]` minimum 1. No absolute source locator or project identifier. |
| `ResourceRole` | `path: RelPath`; `role: runtime\|template\|reference\|fixture\|license`; `reason: string`. Entries are unique and resolve. Declaring a role alone does not prove a resource is used. |
## Operational binding shape

| Record | Fields |
| --- | --- |
| `project-binding-v1` | `schema_version` constant; `project_id: string` canonical lowercase UUID; `project_root: string` resolved absolute local project root; `revision: integer >= 1`; `bindings: InstalledBinding[]` minimum 1; `updated_at_utc: string` RFC 3339 UTC. |
| `InstalledBinding` | `name: Name`; `package_path: RelPath`; `package_digest: Digest`; `role: core\|project_variant\|expertise`; `selected: boolean`. Names and paths unique. Path is a normalized relative locator whose final segment is `<name>`; the installation root is a deployment fact carried by the binding, not a constant this package asserts. |

## Cross-record review

Verify IDs are unique and references resolve to exact retained bytes. Source/user requirements need supporting locators; derived requirements need rationale. Unknown facts do not assert observed conclusions. Expertise needs domain/architecture evidence or current user domain requirements; names/personas alone do not ground a role. Missing evidence remains a gap.

For a proposal, create actions have no existing package; retain/revise actions require one; retention also requires a concrete destination. Core/expertise have no parent lineage. Variants require a distinct parent identity, exact digest, one disposition per parent requirement and equivalent retained child statements. Modified requirements identify replacements; removal needs current user support and semantic review. No reader grants authorization from a keyword or matching ID. Parent/current bytes are read-only.

Selected destinations correspond exactly to selected members without overlap with each other or parent roots. Dependencies and directed handoffs are acyclic, with ASCII-ID topological tie breaking. Required handoff producers occur in consumer depends_on. Missing dependencies do not authorize adding packages.

Validate set-authoring per-member custody, partial applied paths, transitive DEPENDENCY_BLOCKED outcomes and aggregate state: all RETAINED means NO_CHANGE; at least one AUTHORED and all others AUTHORED/RETAINED means AUTHORED; delivered changes plus unresolved members means PARTIAL; otherwise BLOCKED. Authoring validation/testing fields remain NOT_PERFORMED and do not establish quality.

Full-set requests contain the complete original selection with no omissions. Eligible subsets partition the selected IDs, include at least one omission, contain only complete AUTHORED/RETAINED package bindings, and are dependency-closed. Handoffs equal original selected handoffs whose endpoints are requested; omitted IDs identify all others. Copy scope/omissions into the assessment unchanged. Later narrowing requires a new captured input.

Descriptors carry no own digest, framework project UUID, author-machine root or binding record. Parent digest/name and product-relative facts are allowed. Contract path is references/adaptive-contract.md and defines responsibilities/exclusions, triggers/near misses, input/output/effect/recovery/dependency contracts, parent dispositions and observable completion. Resource roles resolve but do not prove usage. The Python 3.10+ binding capability and actual helper/contract routes must be reachable before adaptive product actions.

## Binding observations and portability

Only disposable synthetic operational .agents/devforgeai/project-binding.json fixtures may be created by validation. Real bindings remain read-only; retain sanitized observations and digest, never UUID/content in generic evidence. Call the selected inspected target helper through an argument vector:

```text
python -B -X utf8 <loaded-package>/scripts/check_project_binding.py --project-root <selected-root> --skill-root <loaded-package>
```

Inspect exact loaded package/root/name/role/selection bindings, complete bytes and related selected core/variant descriptors. A core's responsibility group is its name; a variant's group is parent_core.name. At most one selected implementation occupies a group, including two variants sharing a parent. The parent need not be installed solely to preserve lineage. Compare resolved roots using native case normalization; no Windows/WSL path substitution.

The closed binding-observation-v1 object contains status, reason_code, nullable binding_sha256/package_digest and details. MATCH/BOUND exits 0. MISMATCH exits 1 for MISSING_BINDING, INVALID_BINDING, ROOT_MISMATCH, UNBOUND_SKILL, PACKAGE_CHANGED, ROLE_MISMATCH, NOT_SELECTED, AMBIGUOUS_ROLE or UNSAFE_PATH. UNAVAILABLE exits 2 for CAPTURE_LIMIT or IO_ERROR. CLI usage errors use stderr and exit 2. Output must not disclose concrete identity or secrets.

On non-MATCH, the target reports the prerequisite and performs no product writes or downstream calls. A resumed invocation or changed binding/package requires a fresh check; a cached observation grants no authority. Relocation requires separately authorized setup/rebinding, never automatic initialization. This editable applicability check is not protected identity enforcement or Rust qualification. See [set-trials](set-trials.md) for actual effects and two-host fixture evidence requirements.
