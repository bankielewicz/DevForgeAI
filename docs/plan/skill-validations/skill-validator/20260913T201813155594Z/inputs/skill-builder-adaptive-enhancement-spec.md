---
id: DEVFORGEAI-SKILL-BUILDER-ADAPTIVE-001
target: codex-cli
status: proposed
specification_version: "1.0"
recorded: "2026-09-12"
---

# Skill Builder: Adaptive Framework Enhancement Specification

## 1. Contract, baseline, and authority

This is the complete enhancement contract for the development `skill-builder` package. Implement it through `$skill-creator`. Its companion is [Skill Validator: Adaptive Framework Enhancement Specification](skill-validator-adaptive-enhancement-spec.md). This document authorizes no installation or implementation by itself. A current implementation request must select it explicitly. Frontmatter deliberately omits `skill_name`: this is maintenance of an existing skill, not another candidate for ordinary name-based specification lookup.

The baseline is [the development builder](../../src/agents/skills/skill-builder/SKILL.md), including [authoring](../../src/agents/skills/skill-builder/references/authoring.md), [custody records](../../src/agents/skills/skill-builder/references/evidence-format.md), [revision handling](../../src/agents/skills/skill-builder/references/regeneration.md), and [manual validation handoff](../../src/agents/skills/skill-builder/references/validation-handoff.md). Preserve the behavior introduced by [the authoring enhancement](skill-builder-authoring-enhancement-spec.md). Where older builder documents assign testing to builder, the current authoring-only contract governs this enhancement.

Observed baseline: 28 permitted development files; package SHA-256 `65e5513cdb531cbfb1d9ef3eb9a1665f4221b1993ea0e5fbd1eb8e20fa6cc680`; entrypoint SHA-256 `17539f04d7b64db2540cdde06e41c1c3ad78a5d0223a59f478ad79926335a82a`. Package hashing follows section 5. Reinspect current bytes before implementation; a changed baseline requires a documented compatibility review before dependent edits, not automatic restoration of this snapshot.

Normative language: MUST and MUST NOT identify required behavior; MAY identifies a permitted alternative whose selection rules are stated. An absent required input produces the specified unresolved result. No implementer may fill a material requirement gap with guessed product facts, a pretend command, a TODO, or an advisory substitute for required behavior.

### 1.1 Scope and ownership

- Builder authors and edits skills, captures write custody, proposes adaptation, and returns manual validator requests. It MUST NOT run quality checkers, graders, generated scripts as samples, or workflow trials during ordinary authoring; it MUST NOT invoke validator automatically.
- Validator owns skill-quality validation, testing, and set integration assessment. Its findings do not authorize repairs. A later current request may authorize a selected revision.
- `$skill-creator` maintenance of these tools may execute their implementation tests. That is distinct from giving the resulting builder permission to test generated skills.
- The framework's future compiled-Rust CLI owns planned hooks, gates, protected phase transitions, and framework acceptance. It does not exist as a required runtime in this specification. Do not implement, invoke, simulate, or name hypothetical control commands. Local checks and model decisions are development observations.
- Both tools stop at development source. Operational binding creation, installation, plugin assembly, MCP integration, hook/CI configuration, Rust implementation, and remote publication are outside these enhancements.
- Existing conversational creation, explicit specifications, Claude import, focused editing without prior generated history, explicit adoption, and legacy provenance reading MUST continue to work without adaptive metadata.

## 2. Definition of adaptation

Adaptation means recommending and authoring a project-appropriate set of skills, not merely changing the number of workflow steps. It uses these roles:

| Role | Meaning | Required distinction |
| --- | --- | --- |
| `core` | Reusable engineering workflow that discovers applicable project conventions. | No fabricated language, architecture, development-style, or product assumptions. |
| `project_variant` | Separately named specialization of one selected core package. | Preserve core bytes; record exact parent lineage and each retained, changed, or removed parent requirement. |
| `expertise` | Product-specific responsibility grounded in observed product evidence. | State what this role owns, what it does not own, and how it exchanges artifacts with other roles. |

A role is a skill responsibility, not a native Codex agent profile, employee persona, privileged principal, or permanently running worker. No fixed role count, organizational chart, phase count, worker count, language adapter tree, or universal development style is required.

For every proposed role, identify an actual unmet need or justified specialization. A role with no distinct responsibility is rejected as redundant. Prefer retaining an existing skill where it already meets the selected requirements. Core changes are authored as variants; updating a reusable core itself remains a separately selected ordinary edit.

"Any project" means the authoring mechanism does not require a particular project language or layout. It does not establish verified support for untested environments or make every workflow applicable to every project. A database workflow may require a database; its contract must say so.

### 2.1 Source versus operational identity

`src/` and all generated development packages MUST contain no concrete framework project identifier, installation-root literal, binding-record copy, or embedded expected project UUID. Product-domain facts, relative product paths, and descriptive role names are permitted: these express expertise, not a machine binding. A UUID intentionally used as product test data is not a framework identity; it must be identified as fixture data.

Generic field names such as `project_id` and the relative binding path are permitted in schemas and helpers. Actual project identity values exist only under operational `.agents/devforgeai/` locations, including the operational subtree of a disposable trial project. Authoring evidence may reference a real binding file by path and digest but MUST NOT copy its project identity into reports or snapshots. Do not capture a binding in general source discovery.

Generated adaptive packages carry a portable role descriptor and a generic local binding check. Their product work requires the operational binding in section 6. Existing ordinary skills and these two authoring/validation tools are not retroactively required to carry that descriptor or to have an installed framework before authoring can run.

## 3. Terminal capability contract

The supported execution surface is Codex CLI plus local terminal tools and files. Discover the actual shell, project root, Python executable, and CLI capabilities before constructing commands. Python 3.10+ is required for deterministic custody and the portable binding helper; PyYAML remains required where existing YAML helpers use it. This requirement does not make Python the destination project's programming language.

Do not install dependencies, contact package registries, initialize Git, use GUI/browser automation, add MCP servers, change CLI configuration, or create native agent profiles to obtain a missing capability. Standard read-only documentation retrieval through terminal tools is permitted when available and authorized; retain source date and use the named local fallback when unavailable. No live documentation lookup is an essential authoring dependency.

When an essential authoring/custody dependency is unavailable, complete independent proposal work and mark dependent authoring BLOCKED. An unavailable runtime dependency of a proposed skill becomes a named gap. If the selected contract requires actual Rust gate enforcement, that member is BLOCKED; a documentation or design artifact that explicitly requires no enforcement may still be authored.

Do not assume `npm test`, `cargo test`, a particular build manifest, a `src` directory, or Unix paths. Read repository instructions and tool configuration. File names suggest where to inspect; they do not authorize executing project scripts or prove a toolchain is available.

## 4. Invocation, discovery, and modes

Keep the name `skill-builder`. Update its description to include project-adaptation proposals and selected skill sets while retaining ordinary creation/editing and the separation from testing, installation, and standalone specification writing. Preserve current automatic invocation policy and unrelated optional metadata.

### 4.1 Mode selection

| Current request | Mode | Authorized output |
| --- | --- | --- |
| Assess a project and recommend a framework skill set | `propose` | Project evidence, proposal, and human-readable decisions; no candidate skills. |
| Build explicitly selected members of an identified proposal | `author_set` | Sequential per-member development authorings plus aggregate custody and manual validation request. |
| Check a selected variant against a specified changed core or changed project evidence | `review_updates` | Change-impact proposal; no automatic authoring. |
| Create/edit/import/adopt one ordinary or adaptive skill | Existing operation | Existing per-skill flow, with adaptive descriptor obligations only if the selected task is adaptive. |

If a single current request explicitly authorizes proposing and creating a set, capture that authorization, prepare the concrete proposal first, and create only members that fit its stated scope and resolved destinations. New material choices outside that authorization remain unresolved. Do not require approval a second time for an already selected, unchanged member.

### 4.2 Bounded project discovery

Resolve a unique project root from current user selection or unambiguous workspace context. Do not select another repository because it has more convenient tooling. Obtain development destination selection using existing authoring rules; a supplied destination answers the question.

Default discovery covers root instructions/manifests, project documentation, and source/test areas relevant to the requested engineering work. Enumerate before descending. Exclude `.git`, dependency/cache/build output trees (`node_modules`, `.venv`, `venv`, `target`, `dist`, `build`, `__pycache__`), backups, `devforgeai_cli`, private key files, `.env` files, and operational binding contents before reading/hashing. Explicitly selected core packages and operational skill inventories are separate bounded inputs. Do not follow links, junctions, traversal, or special files. Respect applicable repository instructions about additional exclusions.

Default discovery and source capture ceiling: 2,000 regular files and 32 MiB total captured bytes across selected project evidence and core packages for one proposal. Do not copy the whole repository to obtain a few facts. Count each captured original file once. Exceeding a ceiling produces `DISCOVERY_LIMIT`; identify the uninspected roots and obtain a narrower scope or explicit new ceiling. Never silently truncate or raise it. Existing per-member custody ceilings remain unchanged.

Capture evidence needed for architecture, product boundaries, requirements/specifications, languages/toolchains, testing/build conventions, contribution style, relevant security constraints, and existing skill coverage. Missing facts are unknown, not proof of absence. Existing documentation outranked by a current user correction remains retained as conflicting historical input; capture the correction separately.

Do not execute tests or application scripts during discovery. Tool `--help`/version identification is permitted after inspecting the command's nature. Do not run configuration files to parse them. Secrets accidentally observed must not be copied into proposal excerpts; redact values and identify only the affected source path and exclusion reason.

## 5. Shared record and package interfaces

This section is authoritative for interfaces shared with validator. Validator section 4 consumes them without changing their definitions. All interfaces below are new; preserve legacy JSON schemas and records byte-for-byte unless a focused, separately specified migration requires otherwise.

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

## 7. Update review and conflict behavior

`review_updates` requires selected existing variants, their retained parent references, and explicit current core/evidence inputs. No registry, network update check, background poll, or automatic source selection is added.

Compare exact recorded parent digest to selected current core digest, then compare requirement statements and referenced project evidence. Report `NO_CHANGE` only when relevant bytes and requirements are unchanged. A changed digest alone establishes changed input, not a semantic defect. Map affected responsibilities, tests, resource routes, and handoffs. Produce an adaptation proposal whose `prior_proposal` references the earlier proposal when available.

Missing parent bytes, unresolved parent identity, absent requirement mapping, or contradictory evidence produce a specific gap; never reconstruct successful parent history from current files. A later explicit selection authorizes revision of the variant through existing custody rules. It never authorizes modifying upstream core or carrying forward validation from older bytes.

## 8. Requirement register and acceptance cases

All requirements below are required project policies for this enhancement. Test cases are maintenance obligations of the implementation task, executed by validator or a bounded terminal test harness; they do not become ordinary builder responsibilities.

| Requirement | Required behavior | Acceptance cases |
| --- | --- | --- |
| BA-001 | Preserve authoring-only and manual handoff boundaries. | BAT-01, BAT-12 |
| BA-002 | Discover project evidence within scope and limits without executing project code. | BAT-02, BAT-03 |
| BA-003 | Propose evidence-grounded roles and identify unresolved requirements. | BAT-04, BAT-05 |
| BA-004 | Preserve source/operational project identity separation. | BAT-06, BAT-07 |
| BA-005 | Implement exact shared record schemas, digests, and references. | BAT-08, BAT-09 |
| BA-006 | Author selected sets sequentially with dependencies and per-member results. | BAT-10, BAT-11 |
| BA-007 | Preserve core and record complete variant lineage. | BAT-05, BAT-13 |
| BA-008 | Ground expertise and preserve project development conventions. | BAT-04, BAT-14 |
| BA-009 | Produce portable descriptors and binding helper. | BAT-06, BAT-07, BAT-15 |
| BA-010 | Propose explicit updates without automatic rebasing/repair. | BAT-13, BAT-16 |
| BA-011 | Preserve legacy history, existing schemas, and custody conflict behavior. | BAT-09, BAT-11, BAT-17 |
| BA-012 | Keep all authoring terminal-local with honest capability failures. | BAT-03, BAT-15 |
| BA-013 | Deliver discriminating routing and progressive resources. | BAT-12, BAT-14 |
| BA-014 | Report exact authoring state without testing or enforcement claims. | BAT-01, BAT-10, BAT-17 |

| Case | Fixture/action | Expected observable result |
| --- | --- | --- |
| BAT-01 | Cold ordinary create then focused edit; validator absent. | Both can author under current authorization; no checker/test/validator process; manual requests bind delivered bytes; quality NOT_PERFORMED. |
| BAT-02 | Synthetic monorepo with root instructions, two languages, an unknown manifest, ignored dependency tree, and a junction. | Facts cite inspected sources; unknown toolchain remains unknown; excluded tree/link not read; no project script runs. |
| BAT-03 | Exceed each capture ceiling separately; remove Python; require nonexistent Rust enforcement in one member. | Exact scope/capability gaps; independent prose proposal work retained; dependent authoring BLOCKED; no installs or substitute enforcement. |
| BAT-04 | Product docs define storage ownership and HTTP ownership; an existing skill covers HTTP. | Proposal retains HTTP coverage and justifies storage expertise; no redundant catchall persona; each assertion cites evidence. |
| BAT-05 | Core has three requirement IDs; proposed variant changes one and drops one without authorization. | Core unchanged; missing authorized disposition blocks variant; resolved proposal accounts for all three requirements. |
| BAT-06 | Generate adaptive skill, relocate its development package, inspect all source bytes. | No concrete project UUID, binding copy, or original absolute runtime root; helper/template paths remain package-relative; development authoring needs no installed identity. |
| BAT-07 | Synthetic operational binding: correct root/package, absent record, wrong root, inactive member, altered package, duplicate name, core and variant both selected. | Respectively MATCH and named non-MATCH results; no UUID emitted; no product writes after rejection. |
| BAT-08 | Valid records plus duplicate keys, extra fields, unknown versions, malformed references/digests and unresolved IDs. | Deterministic readers accept valid shapes and reject each invalid shape without mutating source or reinterpreting versions. |
| BAT-09 | Existing authoring-contract-v1 and validation-request-v1 fixtures with unchanged bytes. | Existing readers retain behavior; new data exists only in separate envelopes; legacy interpretation unchanged. |
| BAT-10 | Three selected members: A fails, B depends on A, C is independent and succeeds. | A BLOCKED/PARTIAL as actually observed; B DEPENDENCY_BLOCKED; C AUTHORED; aggregate state follows delivered effects; no rollback or false full-set request. |
| BAT-11 | Cycle, missing dependency, occupied destination, user-edited obsolete file, and concurrent input drift. | Each rejected before dependent changes; preserve user/core bytes and previous evidence; disclose actual partial writes. |
| BAT-12 | Positive proposal/create-set/update-review prompts and negative install/test-only prompts. | Description classification distinguishes modes; returned handoff does not invoke validator; native activation separately labeled. |
| BAT-13 | Parent digest changes but semantics are equal, then parent removes a required contract. | First reports input change without invented defect; second proposes affected variant revision; neither auto-rebases. |
| BAT-14 | Python/TDD project, Rust implementation-first project, TypeScript monorepo, and documentation-only project. | Follow fixture conventions and relevant task requirements; no forced uniform tool or ceremony; unsupported facts explicitly identified. |
| BAT-15 | Binding helper run with paths containing spaces/non-ASCII characters and shell-significant characters; missing interpreter; network disabled. | Safe argument handling and offline local operation where Python exists; unavailable runtime clearly reported; no shell injection/dependency installation. |
| BAT-16 | Resume after selected evidence changes; old proposal otherwise intact. | Stale references identified; fresh linked proposal or explicit current selection needed; no silent old approval reuse. |
| BAT-17 | Existing import, observed first edit, authored baseline, legacy generated/adopted baseline, and corrupt known history. | Preserve each old interpretation; corrupt known history blocks; new authoring never rewrites historical COMPLETE or asserts adoption. |

For OS coverage, run deterministic helper cases on the current supported host and retain exact observations. Windows/PowerShell and Linux/POSIX-shell fixtures must both be specified; an unavailable host remains NOT_RUN, and cross-platform verification remains incomplete. Fixture inspection alone is not native execution. The validator companion defines held-out behavior and set-integration evidence.

## 9. Implementation placement and compatibility

Keep shared mode routing in `SKILL.md`; add focused `references/adaptation.md`, `references/adaptive-contracts.md`, and `references/project-binding.md`. Implement deterministic record/topology/lineage observations in `scripts/adaptive.py`, new schemas under `schemas/`, and the portable runtime template under `assets/adaptive-runtime/`. These paths support concrete contracts; do not add empty folders or unrelated manuals.

`adaptive.py` public interface after implementation:

```text
python -B -X utf8 <builder>/scripts/adaptive.py inspect --record <json-file>
python -B -X utf8 <builder>/scripts/adaptive.py plan-set --selection <json-file>
```

Both commands are read-only and print `{schema_version: "adaptive-observation-v1", status: "VALID"|"INVALID"|"UNAVAILABLE", errors: string[], ordered_member_ids: Id[]}`. `inspect` returns an empty order; `plan-set` resolves referenced proposal and returns valid selected topology. Exit 0/1/2 corresponds to VALID/INVALID/UNAVAILABLE. Invalid CLI usage exits 2 with stderr. These commands validate input shape/custody, not skill quality. Existing authoring helpers remain the only ordinary per-member publication path; the model writes proposal/selection records as captured work products, not through a new universal dispatcher.

All new schema versions reject unsupported versions explicitly. Never inject extra fields into closed legacy schemas. Existing non-adaptive operations do not require project evidence, role descriptors, set records, or binding metadata. Adaptive metadata is required only for the adaptive members selected under this contract.

Existing arbitrary conversational requirement shapes remain valid within authoring-contract-v1. For adaptive members, embed the new Requirement rows as its requirements array and add retained adaptive proposal/descriptor references through existing inputs; do not add new top-level legacy fields. Validator must recognize the adaptive shape by the selected proposal/specification, not reinterpret all old requirement objects as the new type.

Maintenance tests for builder may live in the fresh implementation evidence directory; they are not copied into ordinary generated skill packages. The installed Skill Creator checker is a named structural observation only, and validator remains responsible for skill-quality verdicts. Shared record readers are tested by exact fixture agreement; the builder's read-only input validation does not become a second semantic assessment workflow.

## 10. Sources, verification, and completion

OpenAI's [Build skills guidance](https://learn.chatgpt.com/docs/build-skills), read on 2026-09-12, supports skill metadata discovery, conditional resource loading, and separate plugin distribution. The framework's descriptor, role binding, record versions, and naming policy in this document are project choices, not claimed OpenAI requirements. Runtime behavior must use the available CLI's actual help, not inferred interfaces.

Local `codex --version` reported `codex-cli 0.154.0`; `codex exec --help` exposed terminal task execution, `--cd`, `--sandbox`, `--json`, and `--output-last-message`. Both commands exited 0 with warnings about inaccessible Codex temporary aliases. This establishes interface availability only; no native task trial or sandbox qualification was performed while authoring this specification.

Implementation completion requires all BA requirements traced to delivered files and BAT evidence, no unimplemented required branch, and exact delivered readback. Distinguish implementation, structural checks, helper execution, semantic review, native task trials, operational installation, and Rust qualification. A failed/unavailable required trial leaves the relevant verification incomplete; do not rename it PASS. Follow the companion validator specification for test ownership and independent expected outcomes.

Document-delivery verification checks this specification's record definitions, cross-document agreement, requirement/case references, local links, baseline identities, and absence of unresolved normative placeholders. It does not establish that any enhancement has been implemented or installed.
