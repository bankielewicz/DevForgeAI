# Validation Matrix — Configuration Layer Alignment Protocol (CLAP)

**Version:** 1.0
**Status:** Active
**Last Updated:** 2026-02-23
**Checks:** 15 total (10 Contradiction, 4 Completeness, 1 ADR Propagation)

---

## Required Fields Per Check

Every check definition includes these 8 fields:

| Field | Description |
|-------|-------------|
| id | Unique check identifier (CC-NN, CMP-NN, ADR-NN) |
| category | CC (Contradiction), CMP (Completeness), ADR (ADR Propagation) |
| severity | HIGH, MEDIUM, or LOW |
| layer_a | Source/authoritative layer for the check |
| layer_b | Target layer being validated against layer_a |
| description | What the check validates |
| method | How to execute the check using Grep/Read with exact text matching |
| example_finding | A concrete example of what a finding looks like |

---

## Contradiction Checks (CC-01 through CC-10)

### CC-01

- **id:** CC-01
- **category:** CC
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/anti-patterns.md`
- **layer_b:** `CLAUDE.md`
- **description:** Pattern names in CLAUDE.md that appear in anti-patterns.md forbidden list
- **method:** Extract all pattern names from anti-patterns.md `## Category` and `❌ FORBIDDEN` sections using Grep. For each forbidden pattern name, search CLAUDE.md for that exact pattern name string. If found in a non-warning context (not preceded by "FORBIDDEN" or "❌"), flag as contradiction.
- **example_finding:** CLAUDE.md says "installs CUDA hooks via std::call_once" but anti-patterns.md Category 1 forbids "std::call_once for CUDA hook initialization"

### CC-02

- **id:** CC-02
- **category:** CC
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/tech-stack.md`
- **layer_b:** `CLAUDE.md`
- **description:** Technologies, versions, build commands, and platform consistency between tech-stack.md and CLAUDE.md
- **method:** Extract technology names and version numbers from tech-stack.md tables and LOCKED sections using Grep. Search CLAUDE.md for each technology name. If version differs or a PROHIBITED technology is mentioned positively, flag as contradiction.
- **example_finding:** CLAUDE.md lists "npm install" as build command but tech-stack.md prohibits npm for framework validation

### CC-03

- **id:** CC-03
- **category:** CC
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/architecture-constraints.md`
- **layer_b:** `CLAUDE.md`
- **description:** Architecture description accuracy — layer boundaries, IPC protocol, component relationships
- **method:** Extract architecture section headings and key values (protocol constants, layer names) from architecture-constraints.md. Search CLAUDE.md for the same terms. If values differ (e.g., "16-byte header" vs "24-byte header"), flag as contradiction.
- **example_finding:** CLAUDE.md says "16-byte header" but architecture-constraints.md says "24-byte header"

### CC-04

- **id:** CC-04
- **category:** CC
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/source-tree.md`
- **layer_b:** `CLAUDE.md`
- **description:** File paths and component locations consistency
- **method:** Extract file paths mentioned in CLAUDE.md using Grep for path-like patterns (containing `/`). Verify each path exists in source-tree.md directory listing. If a path is referenced in CLAUDE.md but absent from source-tree.md, flag.
- **example_finding:** CLAUDE.md references "src/hook/" but source-tree.md defines the path as "native/hook/"

### CC-05

- **id:** CC-05
- **category:** CC
- **severity:** LOW
- **layer_a:** `devforgeai/specs/context/coding-standards.md`
- **layer_b:** `CLAUDE.md`
- **description:** Code examples in CLAUDE.md follow coding-standards.md patterns
- **method:** If CLAUDE.md contains code examples (detected by ``` blocks), extract function/method call patterns. Compare against coding-standards.md approved patterns. Flag if example uses a deprecated or forbidden pattern.
- **example_finding:** CLAUDE.md shows println!() in code example but coding-standards.md requires tracing::info!()

### CC-06

- **id:** CC-06
- **category:** CC
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/dependencies.md`
- **layer_b:** `CLAUDE.md`
- **description:** Listed dependencies and versions consistency
- **method:** Extract dependency names and version pins from dependencies.md LOCKED sections using Grep. Search CLAUDE.md for each dependency name. If version differs or dependency is listed as FORBIDDEN in dependencies.md but mentioned in CLAUDE.md, flag.
- **example_finding:** CLAUDE.md mentions "Detours 3.0" but dependencies.md pins "Detours 4.0.1"

### CC-07

- **id:** CC-07
- **category:** CC
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/tech-stack.md`
- **layer_b:** `.claude/system-prompt-core.md`
- **description:** Platform constraint and technology references in system prompt
- **method:** Extract platform section from tech-stack.md (OS, architecture, required versions). Check system prompt for platform awareness statements. Extract PROHIBITED technologies and verify system prompt doesn't recommend them.
- **example_finding:** tech-stack.md says "Windows 11 x64 only" but system prompt has no platform guard

### CC-08

- **id:** CC-08
- **category:** CC
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/architecture-constraints.md`
- **layer_b:** `.claude/system-prompt-core.md`
- **description:** Layer boundaries and build system understanding in system prompt
- **method:** Extract build system sections and component layer definitions from architecture-constraints.md. Check system prompt for build routing awareness. Verify subagent routing covers all component types listed in architecture.
- **example_finding:** architecture-constraints.md defines 3 build systems but system prompt only routes for Cargo

### CC-09

- **id:** CC-09
- **category:** CC
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/*.md` (6 context files)
- **layer_b:** `.claude/rules/**/*.md`
- **description:** Rule file references match context file constraints
- **method:** Read each rule file. Extract technology/pattern name references. For each reference, verify it exists in the corresponding context file. If a rule references a technology not in tech-stack.md or a pattern not in coding-standards.md, flag.
- **example_finding:** Rule references "TypeScript strict mode" but tech-stack.md doesn't list TypeScript

### CC-10

- **id:** CC-10
- **category:** CC
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/*.md` (cross-reference)
- **layer_b:** `devforgeai/specs/context/*.md` (cross-reference)
- **description:** Cross-references between the 6 context files agree with each other
- **method:** Check: dependencies.md packages vs tech-stack.md approved technologies; source-tree.md paths vs coding-standards.md naming conventions; architecture-constraints.md layers vs source-tree.md directory structure. Flag any mismatches.
- **example_finding:** dependencies.md lists "express" package but tech-stack.md prohibits Node.js

---

## Completeness Checks (CMP-01 through CMP-04)

### CMP-01

- **id:** CMP-01
- **category:** CMP
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/tech-stack.md`
- **layer_b:** `.claude/system-prompt-core.md`
- **description:** Platform constraint from tech-stack.md present in system prompt
- **method:** Read tech-stack.md Platform or OS section. Search system prompt for a platform guard statement matching the platform name. If no match found, report as gap.
- **example_finding:** tech-stack.md declares "Windows 11 x64, CUDA 13+" but system prompt has no platform constraint section

### CMP-02

- **id:** CMP-02
- **category:** CMP
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/tech-stack.md` + `devforgeai/specs/context/source-tree.md`
- **layer_b:** `CLAUDE.md`
- **description:** All build systems and commands documented in CLAUDE.md
- **method:** Extract all build system sections from tech-stack.md (Cargo, CMake, pnpm, npm, pip, etc.). For each, verify CLAUDE.md has a corresponding build command section or entry. If any build system lacks CLAUDE.md documentation, report as gap.
- **example_finding:** tech-stack.md lists CMake build system but CLAUDE.md has no CMake build commands section

### CMP-03

- **id:** CMP-03
- **category:** CMP
- **severity:** HIGH
- **layer_a:** `devforgeai/specs/context/architecture-constraints.md`
- **layer_b:** `.claude/system-prompt-core.md`
- **description:** Subagent routing for all component types defined in architecture
- **method:** Extract component/layer types from architecture-constraints.md dependency table or layer definitions. Check system prompt for explicit routing of each component type to an appropriate subagent. If any component type lacks routing, report as gap.
- **example_finding:** architecture-constraints.md defines C++ native layer but system prompt doesn't route native code to any subagent

### CMP-04

- **id:** CMP-04
- **category:** CMP
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/context/architecture-constraints.md`
- **layer_b:** `.claude/system-prompt-core.md`
- **description:** Sprint/phase awareness matching current project state
- **method:** Search architecture-constraints.md for sprint annotations or phase markers (e.g., "Sprint 2", "Phase: Implementation"). If present, check system prompt for corresponding state awareness. If architecture has sprint annotations but system prompt has none, report as gap.
- **example_finding:** architecture-constraints.md annotates Sprint 2 modules but system prompt has no sprint awareness

---

## ADR Propagation Check (ADR-01)

### ADR-01

- **id:** ADR-01
- **category:** ADR
- **severity:** MEDIUM
- **layer_a:** `devforgeai/specs/adrs/ADR-*.md` (all accepted ADRs)
- **layer_b:** `devforgeai/specs/context/*.md` (6 context files)
- **description:** Every accepted ADR decision is reflected in relevant context file(s)
- **method:** Read each ADR file. Check YAML frontmatter or Status line for "Accepted" status. Skip ADRs with status "Superseded" or "Deprecated". Extract the Decision section text. Search all 6 context files for evidence that the decision was incorporated (key terms from the decision appearing in the relevant context file). If no evidence found, flag as propagation drift. Report propagation_status as FULLY_PROPAGATED, PARTIALLY_PROPAGATED, or NOT_PROPAGATED.
- **example_finding:** ADR-003 accepted "Use Redis for caching" but tech-stack.md has no Redis entry and dependencies.md has no Redis package

---

## Check Summary Table

| Check ID | Category | Severity | Layer A | Layer B |
|----------|----------|----------|---------|---------|
| CC-01 | CC | HIGH | anti-patterns.md | CLAUDE.md |
| CC-02 | CC | HIGH | tech-stack.md | CLAUDE.md |
| CC-03 | CC | MEDIUM | architecture-constraints.md | CLAUDE.md |
| CC-04 | CC | MEDIUM | source-tree.md | CLAUDE.md |
| CC-05 | CC | LOW | coding-standards.md | CLAUDE.md |
| CC-06 | CC | MEDIUM | dependencies.md | CLAUDE.md |
| CC-07 | CC | HIGH | tech-stack.md | system-prompt-core.md |
| CC-08 | CC | HIGH | architecture-constraints.md | system-prompt-core.md |
| CC-09 | CC | MEDIUM | context files | rules |
| CC-10 | CC | MEDIUM | context files | context files |
| CMP-01 | CMP | HIGH | tech-stack.md | system-prompt-core.md |
| CMP-02 | CMP | MEDIUM | tech-stack.md + source-tree.md | CLAUDE.md |
| CMP-03 | CMP | HIGH | architecture-constraints.md | system-prompt-core.md |
| CMP-04 | CMP | MEDIUM | architecture-constraints.md | system-prompt-core.md |
| ADR-01 | ADR | MEDIUM | ADRs (accepted) | context files |

---

## References

- CLAP Requirements: `devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md`
- ADR-021: `devforgeai/specs/adrs/ADR-021-configuration-layer-alignment-protocol.md`
- Context Validator Pattern: `.claude/agents/context-validator.md`
