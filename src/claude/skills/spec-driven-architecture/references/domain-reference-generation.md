# Domain Reference Generation

**Purpose:** Detection Heuristic Engine and Reference File Template for generating project-specific domain references for subagents.

**Status:** LOCKED
**Version:** 1.0
**Story:** STORY-477 (EPIC-082)

---

## Detection Heuristic Engine

The Detection Heuristic Engine evaluates project context files to determine which subagents need project-specific domain references. The engine is **read-only** — it uses only Read() and Grep operations during evaluation. No Write or Edit operations are permitted against context files. Read and Grep only.

### Engine Behavior

- Evaluates exactly 4 heuristics: DH-01, DH-02, DH-03, DH-04
- Each heuristic is evaluated independently
- Heuristic evaluation is idempotent (same input = same output)
- Missing context files cause graceful skip with warning (no halt)
- Maximum 20 Read/Grep calls total across all 4 heuristics

### Structured Output Format

For each triggered heuristic, the engine returns:

| Field | Description |
|-------|-------------|
| Heuristic ID | DH-01 through DH-04 |
| Target Agent | Name of the subagent receiving the reference |
| Output File | Path: `.claude/agents/{agent-name}/references/project-{type}.md` |
| Source Files | List of context files used as content sources |

When no heuristics trigger, the engine returns an empty list and reports: **"No domain references needed"** for this project. This enables Phase 5.7 to be skipped entirely.

---

## Heuristic Definitions

### DH-01: Hardware/Platform Domain Detection

**Target Agent:** backend-architect
**Output File:** `.claude/agents/backend-architect/references/project-domain.md`

**Trigger Condition:** `architecture-constraints.md` contains one or more hardware/platform keywords:

| Keywords |
|----------|
| GPU, CUDA, FPGA, embedded, driver, kernel, DMA, interrupt, register, hardware, sensor, actuator, firmware |

**Matching:** Case-insensitive word boundaries to prevent false matches on common English words.

**Content Sources:**
1. `architecture-constraints.md` — hardware layer rules, platform constraints
2. `anti-patterns.md` — hardware-specific anti-patterns
3. `coding-standards.md` — platform-specific coding patterns

**Evaluation:**
```
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Grep(pattern="GPU|CUDA|FPGA|embedded|driver|kernel|DMA|interrupt|register|hardware|sensor|actuator|firmware", -i=true)

IF any keyword match found:
    TRIGGERED = true
    Return { heuristic_id: "DH-01", target_agent: "backend-architect", output_file: ".claude/agents/backend-architect/references/project-domain.md", source_files: ["architecture-constraints.md", "anti-patterns.md", "coding-standards.md"] }
ELSE:
    TRIGGERED = false
```

---

### DH-02: Multi-Language/Build-System Detection

**Target Agent:** test-automator
**Output File:** `.claude/agents/test-automator/references/project-testing.md`

**Trigger Condition:** `tech-stack.md` defines more than 1 distinct language or build system (Multi-Language/Build-System detection).

**Content Sources:**
1. `tech-stack.md` — language versions, build tool configurations
2. `source-tree.md` — test directory structure per language
3. `coding-standards.md` — language-specific test patterns

**Evaluation:**
```
Read(file_path="devforgeai/specs/context/tech-stack.md")

Count distinct languages/build systems defined.

IF count > 1:
    TRIGGERED = true
    Return { heuristic_id: "DH-02", target_agent: "test-automator", output_file: ".claude/agents/test-automator/references/project-testing.md", source_files: ["tech-stack.md", "source-tree.md", "coding-standards.md"] }
ELSE:
    TRIGGERED = false
```

---

### DH-03: Domain Anti-Pattern Density Detection

**Target Agent:** security-auditor
**Output File:** `.claude/agents/security-auditor/references/project-security.md`

**Trigger Condition:** `anti-patterns.md` contains more than 5 level-2 (`##`) headings. The threshold is strictly greater than (>5, NOT >=5). Exactly 5 headings does NOT trigger.

**Content Sources:**
1. `anti-patterns.md` — domain-specific anti-patterns and forbidden patterns
2. `architecture-constraints.md` — security-relevant architectural rules
3. `coding-standards.md` — secure coding patterns

**Evaluation:**
```
Read(file_path="devforgeai/specs/context/anti-patterns.md")
Grep(pattern="^## ", output_mode="count")

heading_count = count of level-2 headings

IF heading_count > 5:
    TRIGGERED = true
    Return { heuristic_id: "DH-03", target_agent: "security-auditor", output_file: ".claude/agents/security-auditor/references/project-security.md", source_files: ["anti-patterns.md", "architecture-constraints.md", "coding-standards.md"] }
ELSE:
    TRIGGERED = false
```

---

### DH-04: Multi-Language Coding Standards Detection

**Target Agent:** code-reviewer
**Output File:** `.claude/agents/code-reviewer/references/project-review.md`

**Trigger Condition:** `coding-standards.md` contains language-specific pattern sections for 2 or more distinct languages (2+ languages).

**Content Sources:**
1. `anti-patterns.md` — language-specific anti-patterns
2. `coding-standards.md` — language-specific coding patterns and conventions
3. `dependencies.md` — language-specific package constraints
4. `architecture-constraints.md` — cross-language architectural rules

**Evaluation:**
```
Read(file_path="devforgeai/specs/context/coding-standards.md")

Identify language-specific sections (e.g., "Python", "TypeScript", "C#", "Java", "Go", "Rust").

IF distinct_language_count >= 2:
    TRIGGERED = true
    Return { heuristic_id: "DH-04", target_agent: "code-reviewer", output_file: ".claude/agents/code-reviewer/references/project-review.md", source_files: ["anti-patterns.md", "coding-standards.md", "dependencies.md", "architecture-constraints.md"] }
ELSE:
    TRIGGERED = false
```

---

## Heuristic Summary Table

| ID | Target Agent | Trigger | Threshold | Output File |
|----|-------------|---------|-----------|-------------|
| DH-01 | backend-architect | Hardware/platform keywords in architecture-constraints.md | Any keyword match | project-domain.md |
| DH-02 | test-automator | Multi-Language/Build-System in tech-stack.md | >1 language/build system | project-testing.md |
| DH-03 | security-auditor | Anti-pattern heading count in anti-patterns.md | >5 headings (strictly) | project-security.md |
| DH-04 | code-reviewer | Language-specific sections in coding-standards.md | 2+ languages | project-review.md |

---

## Reference File Template

### Auto-Generation Header

Every generated reference file MUST include this header:

```markdown
<!-- AUTO-GENERATED FILE - DO NOT EDIT MANUALLY -->
<!-- Generated from: {list of source context files} -->
<!-- Generation Date: {YYYY-MM-DD} -->
<!-- Regeneration command: /audit-alignment --generate-refs -->
<!-- Source Files: {comma-separated list of context files used} -->
```

### Required Template Sections

Generated reference files contain the following 5 sections. Sections with no extractable content from source context files are omitted (not populated with placeholders).

#### 1. When to Load This Reference

Describes the conditions under which the subagent should load this reference file. Derived from the heuristic trigger condition and target agent role.

#### 2. Domain Constraints

Also referred to as Domain-Specific Constraints. Extracts architectural constraints, platform rules, and domain boundaries from source context files. Content is 100% context-derived.

#### 3. Forbidden Patterns (Project-Specific)

Extracts project-specific anti-patterns and forbidden coding practices from anti-patterns.md and related context files. No hardcoded content — purely derived from context files only.

#### 4. Language Patterns

Also referred to as Language-Specific Patterns. Extracts language-specific coding patterns, naming conventions, and idioms from coding-standards.md. Only populated when the project has language-specific standards.

#### 5. Build Commands

Also referred to as Build and Test Commands. Extracts build commands, test commands, and CI/CD patterns from tech-stack.md and source-tree.md. Provides the subagent with project-specific execution commands.

---

## Derivation Purity

**CRITICAL CONSTRAINT:** All generated reference file content must maintain 100% derivation purity.

- Every piece of content MUST be directly extractable from or traceable to a specific section of a source context file
- No hardcoded domain knowledge is permitted in generated files
- No synthesized or hallucinated content — only context-derived content
- Derivation purity ensures references remain accurate as context files evolve
- Validation: Compare each generated section against source context file content

---

## Naming Convention

Generated reference files follow the `project-*.md` naming pattern:

| Target Agent | File Name | Full Path |
|-------------|-----------|-----------|
| backend-architect | project-domain.md | `.claude/agents/backend-architect/references/project-domain.md` |
| test-automator | project-testing.md | `.claude/agents/test-automator/references/project-testing.md` |
| security-auditor | project-security.md | `.claude/agents/security-auditor/references/project-security.md` |
| code-reviewer | project-review.md | `.claude/agents/code-reviewer/references/project-review.md` |

**Pattern:** `.claude/agents/{agent-name}/references/project-{type}.md`

---

## Engine Integration

The Detection Heuristic Engine is invoked during Phase 5.7 of the spec-driven-architecture skill workflow. The engine:

1. Reads all 6 context files (read-only evaluation)
2. Evaluates DH-01 through DH-04 in sequence
3. Collects triggered heuristics into a results list
4. If results list is empty: reports "No domain references needed" and skips Phase 5.7
5. If results list is non-empty: generates reference files using the template for each triggered heuristic

### Scalability

- Adding a 5th heuristic requires only editing this reference file (no SKILL.md changes)
- Engine supports up to 10 target agents without architectural changes
- Heuristic definitions are self-contained in this file (NFR-003)

---

## Phase 5.7 Workflow: Domain Reference Generation

This 5-step workflow integrates the Detection Heuristic Engine into the spec-driven-architecture skill as Phase 5.7. It executes after Phase 5.5 (Prompt Alignment) and before Phase 6 (Epic Creation). The workflow is **non-blocking** — failure does not halt the spec-driven-architecture skill.

### Step 1: Run Detection Heuristics

Load all 6 context files in read-only mode and evaluate each heuristic:

```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")

Evaluate DH-01 through DH-04 using the Detection Heuristic Engine defined above.
Collect triggered heuristics into a results list.

IF results list is empty:
    Display: "No domain references needed for this project."
    Skip Steps 2-5.
    Proceed to Phase 6 (non-blocking).
```

- Missing context files cause graceful skip with warning (no halt)
- Maximum 20 Read/Grep calls total across all 4 heuristics
- Each heuristic is evaluated independently

### Step 2: Present Recommendations via AskUserQuestion

Display triggered heuristic count and target agent names to the user:

```
Display: "{N} domain reference(s) recommended:"
FOR each triggered heuristic:
    Display: "  - {heuristic_id}: {target_agent} → {output_file}"

AskUserQuestion with 3 options:
    Option 1: "Generate all" — Generate references for all triggered heuristics
    Option 2: "Select individually" — Present each triggered heuristic for individual approval
    Option 3: "Skip" — Skip generation entirely, proceed to Phase 6
```

- If user selects "Generate all": all triggered heuristics are approved
- If user selects "Select individually": present each heuristic with Accept/Skip choice
- If user selects "Skip": proceed directly to Phase 6 (non-blocking)
- Generation proceeds only for approved references

### Step 3: Generate Reference Files

For each approved heuristic, generate the corresponding reference file:

```
FOR each approved heuristic:
    1. Read source context files listed in heuristic definition (source_files array)
    2. Extract domain-relevant content from each source file
    3. Apply reference file template:
       - Auto-generation header (5-line comment block)
       - Section 1: When to Load This Reference
       - Section 2: Domain Constraints
       - Section 3: Forbidden Patterns (Project-Specific)
       - Section 4: Language Patterns
       - Section 5: Build Commands
    4. Create agent references/ subdirectory if it doesn't exist:
       Bash(command="mkdir -p .claude/agents/{agent-name}/references/")
    5. Write to output path:
       Write(file_path=".claude/agents/{agent-name}/references/project-{type}.md")
    6. Overwrite existing project-*.md files with fresh content
```

- Sections with no extractable content from source context files are omitted (not populated with placeholders)
- Content is 100% derived from source context files (derivation purity)
- No hardcoded domain knowledge permitted in generated files

### Step 4: Verify No Contradictions (Derivation Purity)

For each generated reference file, verify content derivation:

```
FOR each generated reference file:
    1. Read the generated file
    2. FOR each section in the generated file:
        - Identify the source context file(s) for that section
        - Read the source context file(s)
        - Verify every statement in the section is traceable to source content
    3. IF verification fails for any section:
        - Display WARNING: "Derivation purity failed for {output_file}, section {section_name}"
        - Halt generation for THAT file only (do not delete partial file)
        - Continue verification for remaining files
    4. IF verification passes:
        - Mark file as verified
        - Display: "Verified: {output_file}"
```

- Partial generation failure (one agent) does not block remaining agents
- Verification checks every section against its declared source files
- No synthesized or hallucinated content permitted

### Step 5: Report

Display a summary of the generation results:

```
Display: "=== Domain Reference Generation Summary ==="
Display: "Files generated: {count_generated} / {count_approved}"

FOR each generated file:
    Display: "  - {output_file}"
    Display: "    Sources: {comma-separated source files}"

IF any files failed verification:
    Display: "  ⚠ Failed verification: {list of failed files}"

Display: "Regeneration command: /audit-alignment --generate-refs"
```

- Report includes count of files generated vs approved
- Each file lists its source context files
- Failed verifications are listed with warnings
- Regeneration command provided for future updates

---

## References

- [EPIC-082](devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md) — Domain Reference Generation
- [ADR-012](devforgeai/specs/adrs/ADR-012-subagent-progressive-disclosure.md) — Progressive Disclosure Pattern
- [Requirements Specification](devforgeai/specs/requirements/domain-reference-generation-requirements.md) — FR-001, FR-002

---

**Version:** 1.0 | **Created:** 2026-02-23 | **Story:** STORY-477
