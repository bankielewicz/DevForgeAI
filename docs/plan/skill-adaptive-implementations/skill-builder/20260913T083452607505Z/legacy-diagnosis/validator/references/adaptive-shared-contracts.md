# Shared adaptive record definitions

Frozen project-policy contract. Semantic readers are validator-local. Read only the family needed for the selected input.

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

### 5.2 Project evidence and adaptation proposal

Store proposal runs at `<project>/docs/plan/skill-adaptations/<run-id>/`. Store captures in `inputs/`, followed by `project-evidence.json`, `adaptation-proposal.json`, and `adaptation-report.md`. These files are evidence outside source packages. Do not store a concrete `project_id` here.

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

Member IDs, requirement IDs, fact IDs, and handoff IDs are unique in their collections. All references resolve. `depends_on` identifies prerequisite authoring members; a dependency graph cycle is invalid. Handoffs are directed and acyclic in this version; a loop must be represented as a bounded internal workflow in a member, not an unbounded set cycle. A consumer MUST depend on every required producer. No automatic addition of unselected dependencies.

`retain` requires a verified existing package and a concrete target root; `revise` also requires the existing package. `create` requires `existing_package: null`. A missing destination may remain null in a proposal but blocks selected authoring. `project_variant` requires `parent_core`, a distinct name, and complete lineage rows. Other roles have null parent and empty lineage rows. An expertise member requires supporting domain or architecture facts or explicit user-supplied domain requirements; naming a persona is insufficient.

Use `NO_CHANGE` when all proposed actions are retain and there are no material gaps; use `BLOCKED` when any material unresolved gap prevents a complete recommendation; otherwise use `PROPOSED`. A blocked proposal may still contain independently actionable members; only their explicitly selected and fully resolved subset may be authored. The report lists selected-candidate versus unresolved entries without fabricating a complete recommendation.

### 5.3 Selection and sequential set authoring

| Record | Fields |
| --- | --- |
| `adaptation-selection-v1` | `schema_version` constant; `proposal: Ref`; `member_ids: Id[]` minimum 1 and unique; `destinations: Destination[]`; `authorization: Ref`; `permitted_effects: string[]`. |
| `Destination` | `member_id: Id`; `target_root: string`. Exactly one for each selected member. A different destination from the proposal is allowed only if the captured current instruction explicitly selects it; recheck collisions. |
| `set-authoring-v1` | `schema_version` constant; `run_id: Id`; `selection: Ref`; `ordered_member_ids: Id[]`; `members: MemberResult[]`; `state: AUTHORED\|PARTIAL\|BLOCKED\|NO_CHANGE`; `validation_status: NOT_PERFORMED`; `testing_status: NOT_PERFORMED`; `issues: Gap[]`. |
| `MemberResult` | `member_id: Id`; `status: AUTHORED\|RETAINED\|PARTIAL\|BLOCKED\|DEPENDENCY_BLOCKED`; `authoring_record: Ref?`; `validation_request: Ref?`; `package: PackageRef?`; `reason: string`; `applied_paths: RelPath[]`. |
| `set-validation-request-v1` | `schema_version` constant; `run_id: Id`; `selection: Ref`; `set_authoring: Ref`; `scope: full_set\|eligible_subset`; `members: AssessmentMember[]` minimum 1; `handoffs: Handoff[]`; `omitted_member_ids: Id[]`; `omitted_handoff_ids: Id[]`; `permission: string`. Permission states that the packet grants no external effects. |
| `AssessmentMember` | `member_id: Id`; `package: PackageRef`; `request: Ref?`; `adaptive_descriptor: Ref?`. `request` binds a `validation-request-v1` or is null for retained/standalone packages. Adaptive members require a descriptor Ref. |

Write selected-set runs to `<project>/docs/plan/skill-set-authorings/<run-id>/`. Retain selection before candidate generation. Per-member work stays in the existing `skill-authorings/<name>/<run-id>/` family; new envelopes reference those records. Produce no fake legacy COMPLETE record.

Sort selected members topologically with ASCII member ID as tie-breaker. Require dependency closure: dependencies must be selected or already represented by an explicitly retained, verified member included in the selection. Validate exact input digests and known history before any dependent authoring. Create/edit one member at a time. Preserve the existing B/C/N write rules; never edit parent core while creating a variant.

Continue independent members after one failure; mark transitive dependents `DEPENDENCY_BLOCKED`. Runtime handoff failure is validator evidence, not something builder tests. If a member's bytes were partly applied, record `PARTIAL` and all applied paths. Do not roll back successful members or advance a failed member's baseline.

Set state is `NO_CHANGE` if all members are RETAINED; `AUTHORED` if at least one is AUTHORED and all others are AUTHORED/RETAINED; `PARTIAL` if any changes were delivered and at least one member is unresolved; otherwise `BLOCKED`. Retention alone is not an authored change. Full-set validation requests contain all selected members only when complete package bindings exist. For a partial set, return a clearly identified request for the eligible subset and report omitted members/handoffs; it cannot claim full-set coverage.

For `scope: full_set`, member IDs equal the selected IDs and both omission arrays are empty. For `eligible_subset`, member IDs and omitted IDs partition the original selection, without duplicates, and at least one selected member is omitted. Every requested member is AUTHORED/RETAINED with a complete package binding, and all of its required dependencies are in the request. Handoffs equal the proposal handoffs whose endpoints are requested; omitted handoff IDs equal the other selected-set handoffs. Handoffs outside the original selection are not assessed. If no dependency-closed eligible subset exists, publish no set-validation request and list the missing members in the result/report. Keep the full selection reference so a subset cannot be mistaken for the original set.

After authoring, publish the set result and manual request. Do not call validator or start a repair cycle. Existing direct single-skill requests remain valid without any set envelope.

### 5.4 Portable adaptive descriptor

Each newly authored adaptive package includes `assets/devforgeai-skill.json` and a linked `references/adaptive-contract.md`. Ordinary non-adaptive authoring does not add them. These are framework project-policy resources, not extra required Codex frontmatter.

| Record | Fields |
| --- | --- |
| `adaptive-skill-v1` | `schema_version` constant; `name: Name`; `role: core\|project_variant\|expertise`; `binding_required: true`; `parent_core: CoreLineage?`; `contract_path: RelPath`; `required_capabilities: string[]`; `resource_roles: ResourceRole[]`. |
| `CoreLineage` | `name: Name`; `package_digest: Digest`; `requirement_ids: Id[]` minimum 1. No absolute source locator or project identifier. |
| `ResourceRole` | `path: RelPath`; `role: runtime\|template\|reference\|fixture\|license`; `reason: string`. Entries are unique and resolve. Declaring a role alone does not prove a resource is used. |

`contract_path` is `references/adaptive-contract.md`. Its content specifies responsibilities, exclusions, activation/near-miss cases, relative input/output contracts, effects, recovery, dependencies, requirement IDs, and parent requirement dispositions where applicable. It must contain an executable or observable definition of completion. Unknown essential requirements block authoring; no fixed headings are required beyond clear locators for those properties.

For descriptors, project_variant requires a non-null parent_core; core and expertise require null. Descriptor name must match frontmatter and directory identity. Every parent requirement ID must be represented in the linked contract's disposition map. Required capabilities include Python 3.10+ for the copied binding helper; optional tool names do not become mandatory runtime dependencies by being mentioned as examples.

Do not include the package's own digest in its descriptor: that creates a self-reference. External manifests and operational records bind the completed package. Parent digest is permitted and is not self-referential. The descriptor references only package-relative files; domain evidence locators in the contract are project-relative, never author-machine absolute paths.

## 6. Operational project binding contract

### 6.1 Record and setup boundary

The separate future terminal setup step owns `<project>/.agents/devforgeai/project-binding.json`. These enhancements specify its interface and consumers but do not implement an installer or mutate that real operational path. Validator may create it only inside disposable synthetic project fixtures.

| Record | Fields |
| --- | --- |
| `project-binding-v1` | `schema_version` constant; `project_id: string` canonical lowercase UUID; `project_root: string` resolved absolute local project root; `revision: integer >= 1`; `bindings: InstalledBinding[]` minimum 1; `updated_at_utc: string` RFC 3339 UTC. |
| `InstalledBinding` | `name: Name`; `package_path: RelPath`; `package_digest: Digest`; `role: core\|project_variant\|expertise`; `selected: boolean`. Names and paths unique. Path is exactly `.agents/skills/<name>`. |

Setup must explicitly select a project, generate a new project UUID for a new project, inspect exact installed package bytes, choose active roles, and write/read back the record under separate authorization. Updating bindings preserves identity and increments revision; intentional reuse for a different product requires a new identity. Relocation of the same project requires an explicit root update and recheck. No silent first-use initialization by a skill is permitted.

Setup may bind only complete packages with matching descriptors. It selects at most one active implementation of a core responsibility: a core and a variant of that core may both be installed, but only one is selected for the same responsibility. Distinct expertise roles may be selected together. Tool consumers verify this relation from installed descriptors.

The implementation group of a core is its name; the group of a project_variant is its parent_core.name. At most one selected core/variant binding may occupy a group, including two variants with the same parent. Expertise roles use their own distinct names; semantic responsibility overlap is assessed by validator, not inferred by the binding helper. Read the descriptors of selected core/variant bindings to compute these groups; missing/invalid descriptors yield INVALID_BINDING. A variant's parent need not be installed merely to preserve recorded lineage. Compare roots after absolute resolution and native platform case normalization, with no Windows/WSL path substitution. A matching project UUID alone never overrides a different root or package digest.

The record is editable operational data. Copying both a binding and a package is not a protected identity mechanism. `project_root` catches ordinary accidental relocation; no claim of resistance to a malicious user editing all fields is permitted. Future Rust authority remains separate.

### 6.2 Runtime helper and outcome

Implement a portable generic `check_project_binding.py` template under builder `assets/adaptive-runtime/`, copied to each adaptive package's `scripts/`. It uses Python standard library only, creates no bytecode/cache/output files, and never stores concrete project identity in its own source. Runtime invocation:

```text
python -B -X utf8 <loaded-package>/scripts/check_project_binding.py --project-root <selected-root> --skill-root <loaded-package>
```

Pass arguments as an argument vector with native shell quoting, never interpolated shell code. The helper resolves and checks both roots, reads the exact binding and descriptor, inventories the loaded package without following links, checks the manifest digest against the unique installed binding, verifies the bound root, role, selected state, and active core/variant exclusion, then prints one JSON object. Maximum capture is 2,000 files / 32 MiB for the selected package and required related descriptors; refuse links, special files, excluded/generated files, invalid paths, and incomplete capture.

Output closed object: `{schema_version: "binding-observation-v1", status: "MATCH"|"MISMATCH"|"UNAVAILABLE", reason_code: Id, binding_sha256: Digest?, package_digest: Digest?, details: string[]}`. Do not output project UUID, secrets, or binding contents. Exit 0 means MATCH; 1 means MISMATCH; 2 means unavailable capability/I/O/limit; argparse usage errors also exit 2 but have stderr and no claimed JSON observation.

Reason codes: `BOUND`, `MISSING_BINDING`, `INVALID_BINDING`, `ROOT_MISMATCH`, `UNBOUND_SKILL`, `PACKAGE_CHANGED`, `ROLE_MISMATCH`, `NOT_SELECTED`, `AMBIGUOUS_ROLE`, `UNSAFE_PATH`, `CAPTURE_LIMIT`, `IO_ERROR`. Missing binding is MISMATCH; limits/I/O failures are UNAVAILABLE; other listed failures are MISMATCH. Invalid descriptor is INVALID_BINDING. Unknown schema versions fail closed as INVALID_BINDING.

Generated instructions MUST run this check before product-specific operations and after a detected binding/package change or resumed invocation. On non-MATCH, report the reason and request separately authorized setup/rebinding; perform no product writes or downstream workflow calls. Read-only explanation and reporting the missing prerequisite remain allowed. A helper result is an observation, not an immutable authorization token; no cached match survives changed bytes.

Builder copies/authors this helper but does not test it in ordinary authoring. Validator owns synthetic runtime checks. The maintenance implementation of builder must test the template under `$skill-creator` before reporting the enhancement verified.


An ordinary validation does not perform setup or authoring actions described as ownership above. Test operational consumers solely under disposable synthetic roots.
