# Context File Validation Reference

**Purpose:** Centralized validation logic for story content against 6 constitutional context files. This reference is the Single Source of Truth (SSOT) for context validation, reused by:
- Phase 3.6 (during tech spec generation)
- Phase 5.1 (before file write)
- Phase 7.7 (final validation)
- `/validate-stories` command (post-hoc validation)

---

## Overview

Validates story content against 6 constitutional context files to prevent technical debt at specification stage.

**Context Files (Read-Only Reference):**

| File | Path | Validates |
|------|------|-----------|
| tech-stack.md | `devforgeai/specs/context/tech-stack.md` | Technology choices |
| source-tree.md | `devforgeai/specs/context/source-tree.md` | File paths and directories |
| dependencies.md | `devforgeai/specs/context/dependencies.md` | Package dependencies |
| coding-standards.md | `devforgeai/specs/context/coding-standards.md` | Coverage thresholds, patterns |
| architecture-constraints.md | `devforgeai/specs/context/architecture-constraints.md` | Layer boundaries |
| anti-patterns.md | `devforgeai/specs/context/anti-patterns.md` | Forbidden patterns |

---

## Greenfield Mode

**Check for context files before validation:**

```
context_dir = "devforgeai/specs/context/"
context_files = Glob(pattern=f"{context_dir}*.md")

if len(context_files) == 0:
    # Greenfield mode: no context files exist
    Display: """
    ℹ️ Greenfield Mode: Context validation skipped

    No context files found in devforgeai/specs/context/
    Story creation will proceed without framework validation.

    Recommendation: Run /create-context to enable validation
    """
    SKIP validation functions
    RETURN { greenfield: true, violations: [] }
```

**If context files exist:** Proceed with validation functions below.

---

## Validation Functions

### 1. validate_technologies(tech_spec_content)

**Purpose:** Validate technologies in technical specification against tech-stack.md

**Severity:** HIGH

**Input:** Technical specification text from story

**Process:**
```
1. Read tech-stack.md:
   tech_stack = Read(file_path="devforgeai/specs/context/tech-stack.md")

2. Extract LOCKED technologies from tech-stack.md:
   - Parse sections for "LOCKED" markers
   - Build approved_technologies list
   - Note PROHIBITED technologies

3. Extract technology mentions from tech_spec_content:
   - Scan for framework names (React, Vue, Angular, etc.)
   - Scan for language names (Python, TypeScript, C#, etc.)
   - Scan for database names (PostgreSQL, MongoDB, Redis, etc.)
   - Scan for library mentions

4. Compare:
   FOR each technology in tech_spec:
     IF technology in PROHIBITED list:
       violations.append({
         type: "PROHIBITED_TECHNOLOGY",
         technology: technology,
         severity: "CRITICAL",
         source: "tech-stack.md",
         remediation: "Remove or replace with approved alternative"
       })
     ELIF technology NOT in approved_technologies AND not generic:
       violations.append({
         type: "UNAPPROVED_TECHNOLOGY",
         technology: technology,
         severity: "HIGH",
         source: "tech-stack.md",
         remediation: "Add to tech-stack.md (requires ADR) or remove"
       })

5. Return violations list
```

---

### 2. validate_file_paths(tech_spec_content)

**Purpose:** Validate file paths in technical specification against source-tree.md

**Severity:** HIGH

**Input:** Technical specification text from story

**Process:**
```
1. Read source-tree.md:
   source_tree = Read(file_path="devforgeai/specs/context/source-tree.md")

2. Extract allowed directory patterns from source-tree.md:
   - Parse directory structure tree
   - Build allowed_paths list (e.g., "devforgeai/specs/Stories/", ".claude/skills/")
   - Note FORBIDDEN paths

3. Extract file paths from tech_spec_content:
   - Scan for patterns like "src/...", "devforgeai/...", etc.
   - Scan for file_path fields in YAML
   - Extract proposed implementation locations

4. Compare:
   FOR each path in proposed_paths:
     IF path matches FORBIDDEN pattern:
       violations.append({
         type: "FORBIDDEN_PATH",
         path: path,
         severity: "CRITICAL",
         source: "source-tree.md",
         remediation: f"Use approved path from source-tree.md"
       })
     ELIF path NOT in allowed_paths structure:
       # Find closest match
       suggested_path = find_closest_allowed_path(path)
       violations.append({
         type: "INVALID_PATH",
         path: path,
         suggested: suggested_path,
         severity: "HIGH",
         source: "source-tree.md",
         remediation: f"Change to: {suggested_path}"
       })

5. Return violations list
```

**Special Case - Story Output Directory:**
```
# CRITICAL: Stories MUST go in devforgeai/specs/Stories/
IF story_output_path != "devforgeai/specs/Stories/":
    violations.append({
      type: "WRONG_STORY_DIRECTORY",
      path: story_output_path,
      correct: "devforgeai/specs/Stories/",
      severity: "CRITICAL",
      remediation: "Stories MUST be in devforgeai/specs/Stories/"
    })
```

---

### 3. validate_dependencies(dependencies_section)

**Purpose:** Validate package dependencies against dependencies.md

**Severity:** HIGH

**Input:** Dependencies section from story technical specification

**Process:**
```
1. Read dependencies.md:
   deps = Read(file_path="devforgeai/specs/context/dependencies.md")

2. Extract approved packages from dependencies.md:
   - Parse LOCKED packages with versions
   - Note FORBIDDEN alternatives

3. Extract proposed packages from dependencies_section:
   - Scan for package names (npm, pip, nuget patterns)
   - Extract version constraints if present

4. Compare:
   FOR each package in proposed_packages:
     IF package in FORBIDDEN list:
       approved_alternative = get_approved_alternative(package)
       violations.append({
         type: "FORBIDDEN_DEPENDENCY",
         package: package,
         alternative: approved_alternative,
         severity: "HIGH",
         source: "dependencies.md",
         remediation: f"Use {approved_alternative} instead"
       })
     ELIF package NOT in approved_packages:
       violations.append({
         type: "UNAPPROVED_DEPENDENCY",
         package: package,
         severity: "HIGH",
         source: "dependencies.md",
         remediation: "Add to dependencies.md (requires ADR) or remove"
       })

5. Return violations list
```

---

### 4. validate_coverage_thresholds(dod_content, file_paths)

**Purpose:** Validate test coverage thresholds match architectural layer

**Severity:** MEDIUM

**Input:** Definition of Done content, file paths from technical specification

**Process:**
```
1. Read coding-standards.md:
   standards = Read(file_path="devforgeai/specs/context/coding-standards.md")

2. Extract coverage thresholds by layer:
   thresholds = {
     "business_logic": 95,  # Core domain, services
     "application": 85,      # Controllers, handlers
     "infrastructure": 80    # Repositories, external integrations
   }

3. Determine layer from file_paths:
   FOR each path in file_paths:
     layer = classify_layer(path)
     # src/domain/, src/services/ → business_logic
     # src/controllers/, src/handlers/ → application
     # src/repositories/, src/integrations/ → infrastructure

4. Extract coverage mentioned in DoD:
   - Scan for patterns like "95% coverage", "85%", etc.
   - Extract stated threshold

5. Compare:
   IF stated_threshold != thresholds[layer]:
     violations.append({
       type: "INCORRECT_COVERAGE_THRESHOLD",
       stated: stated_threshold,
       correct: thresholds[layer],
       layer: layer,
       severity: "MEDIUM",
       source: "coding-standards.md",
       remediation: f"Update coverage to {thresholds[layer]}% for {layer} layer"
     })

6. Return violations list
```

---

### 5. validate_architecture(tech_spec_content)

**Purpose:** Validate technical specification against architecture constraints

**Severity:** HIGH

**Input:** Technical specification text from story

**Process:**
```
1. Read architecture-constraints.md:
   arch = Read(file_path="devforgeai/specs/context/architecture-constraints.md")

2. Extract layer dependency rules:
   - Parse dependency matrix (which layers can call which)
   - Extract FORBIDDEN cross-layer dependencies

3. Analyze tech_spec for layer violations:
   - Check if proposed design has controllers calling repositories directly
   - Check if infrastructure depends on domain
   - Check for circular dependencies

4. Compare:
   FOR each proposed_dependency in tech_spec:
     IF violates_layer_rules(proposed_dependency):
       violations.append({
         type: "LAYER_VIOLATION",
         from_layer: source_layer,
         to_layer: target_layer,
         severity: "HIGH",
         source: "architecture-constraints.md",
         remediation: "Insert application layer between {source} and {target}"
       })

5. Return violations list
```

---

### 6. validate_anti_patterns(tech_spec_content)

**Purpose:** Detect forbidden patterns in technical specification

**Severity:** CRITICAL

**Input:** Technical specification text from story

**Process:**
```
1. Read anti-patterns.md:
   patterns = Read(file_path="devforgeai/specs/context/anti-patterns.md")

2. Extract forbidden patterns:
   anti_patterns = [
     "God Object",           # Classes >500 lines or >20 methods
     "SQL concatenation",    # String-based SQL queries
     "Hardcoded secrets",    # API keys, passwords in code
     "Bash for file ops",    # Using cat/echo instead of Read/Write
     "Monolithic skills",    # Single skill doing everything
     "Direct instantiation"  # Not using dependency injection
   ]

3. Scan tech_spec_content for pattern matches:
   FOR each pattern in anti_patterns:
     IF pattern_detected(tech_spec_content, pattern):
       violations.append({
         type: "ANTI_PATTERN_DETECTED",
         pattern: pattern,
         severity: "CRITICAL",
         source: "anti-patterns.md",
         remediation: get_remediation_for_pattern(pattern)
       })

4. Return violations list
```

---

### 7. validate_dual_path(tech_spec_content, story_content)

**Purpose:** Detect stories specifying `.claude/` operational paths as development targets instead of `src/claude/` source-of-truth paths

**Severity:** CRITICAL

**Constitutional Rule:** source-tree.md lines 13-15: "Do not modify operational files. Only modify src/, tests/ files."

**Input:**
- `tech_spec_content` — Technical Specification section text
- `story_content` — Full story file content (for scanning AC `<file>` verification blocks)

**Process:**
```
1. Extract ALL file paths from BOTH inputs:
   proposed_paths = []

   # From tech_spec_content:
   - Extract paths from: **Target File:** `{path}` lines
   - Extract paths from: file_path: "{path}" in YAML blocks
   - Extract paths from: <file hint="...">{path}</file> elements

   # From story_content (AC verification blocks):
   - Extract paths from: <file hint="...">{path}</file> elements
   - Extract paths from: <file>{path}</file> elements

   # Deduplicate
   proposed_paths = unique(proposed_paths)

2. Define exempt prefixes (paths that are NOT subject to dual-path rule):
   exempt_prefixes = [
     "devforgeai/",     # Framework specs, RCA, qa, config, feedback, workflows
     "tests/",          # Test tree (allowed target)
     "src/",            # Already in source tree (correct)
     "installer/",      # Installer code
     ".github/",        # GitHub config
     "docs/",           # Documentation
     "CLAUDE.md",       # Root config (no src/ mirror)
     "README.md",       # Root doc
     "package.json",    # Root config
     "node_modules/",   # Dependencies
     "dist/",           # Build output
     "tmp/",            # Temporary files
   ]

3. Define operational prefixes (paths that MUST use src/ equivalent):
   operational_prefixes = [".claude/"]

4. violations = []

   FOR each path in proposed_paths:
     # Skip exempt paths
     IF path starts with any exempt_prefix:
       CONTINUE

     # Check for operational path violations
     IF path starts with any operational_prefix:
       src_equivalent = path.replace(".claude/", "src/claude/", 1)

       violations.append({
         "type": "DUAL_PATH_OPERATIONAL_TARGET",
         "path": path,
         "severity": "CRITICAL",
         "source": "source-tree.md lines 13-15",
         "src_equivalent": src_equivalent,
         "remediation": f"Replace '{path}' with '{src_equivalent}' — /dev workflow must only modify src/ tree, not operational .claude/ files"
       })

5. Return violations list
```

**Rationale for CRITICAL severity:**
- The /dev workflow will modify operational files if the story is implemented as written
- This violates an IMMUTABLE constitutional rule (source-tree.md is LOCKED)
- Previous severity of HIGH allowed violations to be missed during audits (see custody-chain-audit-stories-566-570.md Rev 2)

---

## Resolution Protocol

**For each violation found:**

```
1. Categorize by severity:
   CRITICAL > HIGH > MEDIUM > LOW

2. If CRITICAL or HIGH violations exist:
   HALT workflow

   Use AskUserQuestion:
   Question: "Context validation found {count} violation(s). How to proceed?"
   Header: "Validation"
   Options:
     - "Fix in story"
       Description: "I'll provide the correct value"
     - "Update context file"
       Description: "Requires ADR - the constraint should change"
     - "Defer to manual review"
       Description: "Flag for later review, proceed with warning"

   IF user selects "Fix in story":
     AskUserQuestion for correct value
     Apply fix to story content
     Re-validate

   IF user selects "Update context file":
     HALT: "Create ADR first, then update context file, then retry"

   IF user selects "Defer to manual review":
     Add warning note to story
     Log deferral
     Continue with warning

3. If only MEDIUM or LOW violations:
   Display warnings
   Embed note in story: "⚠️ {count} validation warnings - see below"
   Continue workflow
```

---

## Validation Report Format

**Generate report after all validation functions run:**

```markdown
## Context Validation Report

**Story:** {story_id}
**Validated At:** {timestamp}
**Context Files Checked:** {count}/6

### Summary

| Severity | Count | Blocking |
|----------|-------|----------|
| CRITICAL | {n}   | Yes      |
| HIGH     | {n}   | Yes      |
| MEDIUM   | {n}   | No       |
| LOW      | {n}   | No       |

**Status:** {COMPLIANT | FAILED | WARNINGS}

### Violations

{for each violation}
#### {severity}: {type}
- **Location:** {where in story}
- **Issue:** {description}
- **Context File:** {source} (line {line_number})
- **Remediation:** {how to fix}
{/for}

### Compliance Score

{percentage}% compliant ({passed}/{total} checks)
```

---

## Integration Points

### Phase 3.6: Technology Validation

**Trigger:** After technical specification generated
**Functions called:** `validate_technologies()`, `validate_dependencies()`, `validate_architecture()`
**On violation:** HALT + AskUserQuestion

### Phase 5.1: Directory Validation

**Trigger:** Before story file write
**Functions called:** `validate_file_paths()` (specifically story output directory)
**On violation:** Auto-correct to `devforgeai/specs/Stories/`

### Phase 7.7: Comprehensive Validation

**Trigger:** Final validation before completion
**Functions called:** All 6 validation functions
**On violation:** HALT + AskUserQuestion for CRITICAL/HIGH, warn for MEDIUM/LOW

### /validate-stories Command

**Trigger:** User invokes command on existing stories
**Functions called:** All 6 validation functions
**On violation:** Report + AskUserQuestion for fixes

---

## Error Handling

**Context file missing:**
```
IF Read() fails for context file:
  Log: "Warning: {file} not found, skipping {validation_type}"
  SKIP that validation function
  Continue with remaining validations
```

**Malformed context file:**
```
IF parsing fails:
  Log: "Warning: {file} has invalid format, skipping validation"
  SKIP that validation function
  Continue with remaining validations
```

**All context files missing:**
```
IF no context files exist:
  Greenfield mode (documented above)
  SKIP all validation
  Return success with greenfield flag
```

---

## Performance Considerations

**Load context files in parallel:**
```
# Parallel reads for efficiency
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/dependencies.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")
Read(file_path="devforgeai/specs/context/architecture-constraints.md")
Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

**Cache context files within skill execution:**
- Load once at start of validation
- Reuse across all validation functions
- Don't reload for each function call

---

## Custody Chain Validation Functions

**Purpose:** Validate inter-document traceability across the spec-driven development chain: brainstorm -> requirements -> epic -> sprint -> story. These functions complement the 6 context file validation functions above.

**Used by:**
- `/validate-stories` command (Phase 3: --chain mode)
- Future CI pipeline integration (custody chain gate)

---

### 7. validate_provenance_chain(story_meta, chain_docs)

**Purpose:** Verify each story traces back to its parent epic, requirements doc, and brainstorm

**Severity:** HIGH (broken chain) or MEDIUM (partial chain)

**Input:** story_meta dict (frontmatter from stories), chain_docs dict (Glob results for all spec layers)

**Process:**

1. Group stories by epic_id from frontmatter

2. FOR each epic_id in scope:
   a. Verify epic file exists on disk
      IF missing: CRITICAL finding ("Epic file not found")

   b. Read epic frontmatter
      Extract: brainstorm_ref, requirements_ref, research_ref

   c. Verify brainstorm back-reference:
      IF brainstorm_ref missing: HIGH finding ("no brainstorm back-reference")
      IF brainstorm_ref file not found: HIGH finding ("broken brainstorm reference")

   d. Verify requirements back-reference:
      IF requirements_ref path not found: MEDIUM finding ("broken requirements reference")

   e. Verify research ID consistency across chain:
      Extract research IDs from brainstorm, requirements, and epic
      IF mismatched IDs: HIGH finding ("research ID mismatch")
      IF path case mismatch (specs/research/ vs specs/Research/): MEDIUM finding

3. Return findings list

---

### 8. validate_dependency_graph(story_meta)

**Purpose:** Validate inter-story dependency DAGs for cycles, missing deps, stale labels, undeclared coupling

**Severity:** CRITICAL (cycles), HIGH (missing deps, undeclared coupling), MEDIUM (stale labels)

**Input:** story_meta dict with depends_on arrays

**Process:**

1. Build adjacency list: { story_id: [depends_on_ids] }

2. Cycle detection (BFS/DFS):
   FOR each story_id:
     Walk dependency chain tracking visited set
     IF revisit detected: CRITICAL finding ("circular dependency: A -> B -> C -> A")

3. Missing dependency detection:
   FOR each depends_on entry:
     IF target story_id has no file on disk: HIGH finding ("depends on non-existent story")

4. Stale status label detection:
   FOR each story's dependency table:
     Compare listed_status against target story's actual frontmatter status
     IF mismatch: MEDIUM finding ("lists DEP as 'Backlog' but actual is 'Ready for Dev'")

5. Undeclared mutual dependency detection:
   FOR each pair of stories (A, B) in scope:
     IF A's ACs/spec text references B's types/structs/interfaces
     AND A does NOT list B in depends_on:
       HIGH finding ("A references B but doesn't declare depends_on")

6. Return findings list

---

### 9. validate_adr_references(story_meta, chain_docs)

**Purpose:** Verify ADR references in stories are valid and accepted

**Severity:** CRITICAL (ADR TBD blocking implementation), HIGH (broken/unaccepted ADR)

**Input:** story_meta dict, chain_docs.adrs list

**Process:**

1. FOR each story in scope:

   a. Scan for "ADR TBD" or "ADR-TBD" text:
      IF found: CRITICAL finding ("unresolved ADR TBD - implementation blocked")

   b. Extract all ADR-NNN references via regex:
      FOR each unique ADR reference:
        Verify file exists in adrs/ directory
        IF missing: HIGH finding ("references ADR-NNN which has no file")

        IF file exists:
          Read ADR file, extract status field
          IF status == "proposed": HIGH finding ("ADR not yet accepted")
          IF status == "superseded":
            Extract superseded_by field
            MEDIUM finding ("references superseded ADR - update to successor")

2. Return findings list

---

### 10. validate_story_quality(story_meta)

**Purpose:** Detect ambiguity, broken file references, and internal inconsistency within story documents

**Severity:** HIGH (ambiguous ACs, internal contradiction), MEDIUM (broken refs, path issues)

**Input:** story_meta dict

**Process:**

1. FOR each story:

   a. Ambiguous AC detection:
      Grep for "(or {word})" patterns in AC text
      IF found: HIGH finding ("ambiguous AC text - pick one definitive answer")

   b. Internal inconsistency:
      Compare AC assertions against Design Decisions section
      IF contradiction found (e.g., AC says "Variable or Constant" but Design says "Variable"):
        HIGH finding ("AC contradicts design decision")

   c. Broken file path references:
      Extract all src/ file paths from tech spec
      FOR each concrete path (not wildcard):
        IF file does not exist AND story does not mark it as "new file to create":
          MEDIUM finding ("references non-existent file")

   d. Path case sensitivity:
      Grep for "specs/research/" (lowercase)
      IF found: MEDIUM finding ("wrong case - should be 'specs/Research/'")

   e. Unresolved TL items:
      Grep for "TL-\d{3}" items marked as "unresolved" or "pending"
      Count per story
      IF count > 2: MEDIUM finding ("N unresolved technical limitations - high implementation risk")

2. Return findings list

---

### Custody Chain Finding Format

Each finding uses this structure for consistency with the audit report:

  finding_id:   "F-NNN"              # Sequential, assigned during report generation
  severity:     "CRITICAL|HIGH|MEDIUM|LOW"
  type:         "category/specific"  # e.g., "provenance/broken_brainstorm_ref"
  affected:     ["STORY-XXX"]        # List of affected story/epic IDs
  summary:      "One-line description"
  evidence:     "Quoted text from source file (optional)"
  remediation:  "Numbered steps to fix"
  verification: "grep command to confirm fix (optional)"
  phase:        "3a|3b|3c|3d"        # Which sub-phase detected it

---

### Severity Decision Rules

| Severity | Trigger | Examples |
|----------|---------|---------|
| CRITICAL | Blocks TDD Red phase; no workaround | Missing ADR prerequisite, circular dependency, epic file missing |
| HIGH | Context loss causing likely rework (>30% story point risk) | Broken provenance chain, undeclared dependency, ambiguous AC, research ID mismatch |
| MEDIUM | Documentation gap or stale data; no implementation risk | Stale status label, path case mismatch, broken file reference |
| LOW | Known tradeoff, explicitly documented in ADR or design decision | ADR-006 field to Variable mapping, grammar maturity risk |

---

## Plan-Story Coherence Validation Functions

**Purpose:** Validate that stories generated from a plan are internally consistent, match their source plan, and agree on shared specifications across sibling stories in the same epic.

**Used by:**
- `/validate-stories` command (Phase 3e: --chain mode, 2+ stories from same epic)

**Trigger:** Chain mode only. Requires 2+ stories from same epic in scope.

---

### 11. validate_cross_story_schema(stories_in_epic)

**Purpose:** Detect schema mismatches between sibling stories referencing shared data structures

**Severity:** HIGH (incompatible schemas cause runtime failures when stories are implemented)

**Input:** List of story content dicts from the same epic

**Process:**
```
shared_schemas = {}

FOR each story in stories_in_epic:
  tech_spec = extract_section(story.content, "Technical Specification")

  # Extract all defined schemas (JSON keys, YAML keys from required_keys sections)
  schemas = extract_schema_definitions(tech_spec)
  # Each schema: { target_file: str, fields: {name: type}, story_id: str }

  FOR each schema in schemas:
    key = schema.target_file  # e.g., "phase-steps-registry.json", "phase-state.json"
    IF key in shared_schemas:
      existing = shared_schemas[key]

      # Compare field names
      existing_names = set(existing.fields.keys())
      current_names = set(schema.fields.keys())
      mismatched = existing_names.symmetric_difference(current_names)

      IF mismatched:
        findings.append({
          type: "coherence/schema_mismatch",
          severity: "HIGH",
          affected: [existing.story_id, story.story_id],
          summary: f"Field name mismatch for shared schema '{key}'",
          evidence: f"{existing.story_id} uses {sorted(existing_names)}, {story.story_id} uses {sorted(current_names)}. Difference: {sorted(mismatched)}",
          remediation: "Align field names across stories. Check plan file for canonical schema.",
          phase: "3e"
        })

      # Compare types for shared fields
      shared_fields = existing_names.intersection(current_names)
      FOR field in shared_fields:
        IF existing.fields[field] != schema.fields[field]:
          findings.append({
            type: "coherence/schema_mismatch",
            severity: "HIGH",
            affected: [existing.story_id, story.story_id],
            summary: f"Type mismatch for field '{field}' in '{key}'",
            evidence: f"{existing.story_id} types '{field}' as {existing.fields[field]}, {story.story_id} types it as {schema.fields[field]}",
            remediation: "Align field type to plan specification.",
            phase: "3e"
          })
    ELSE:
      shared_schemas[key] = schema

RETURN findings
```

**Extraction heuristic for `extract_schema_definitions()`:**
```
Look for:
- YAML `required_keys:` sections with `key:` and `type:` fields
- JSON examples in code blocks with field definitions
- `schema:` blocks within technical_specification YAML
- References to shared files (*.json, *.yaml) in file_path fields

Build schema dict: { target_file, fields: {name: type_string}, story_id }
```

---

### 12. validate_api_contracts(story)

**Purpose:** Verify external API field names and schemas match actual APIs

**Severity:** CRITICAL (wrong field names cause silent hook failures)

**Input:** Single story content dict

**Known API schemas (hardcoded reference — update when APIs change):**
```
CLAUDE_HOOKS_INPUT_SCHEMAS = {
  "SubagentStop": {
    "agent_type": "string",       # NOT subagent_type
    "agent_id": "string",
    "agent_transcript_path": "string",
    "last_assistant_message": "string",
    "stop_hook_active": "boolean"
  },
  "SubagentStart": {
    "agent_type": "string",
    "agent_id": "string"
  },
  "TaskCompleted": {
    "task_id": "string",
    "task_subject": "string",
    "task_description": "string",   # Optional
    "teammate_name": "string",      # Optional
    "team_name": "string"           # Optional
  },
  "Stop": {
    "stop_hook_active": "boolean",
    "last_assistant_message": "string"
  },
  "SessionStart": {
    "source": "string",            # startup|resume|clear|compact
    "model": "string",
    "agent_type": "string"          # Optional
  },
  "PreToolUse": {
    "tool_name": "string",
    "tool_input": "object",
    "tool_use_id": "string"
  },
  "PostToolUse": {
    "tool_name": "string",
    "tool_input": "object",
    "tool_response": "object",
    "tool_use_id": "string"
  },
  "UserPromptSubmit": {
    "prompt": "string"
  }
}
# Common fields on ALL hook events: session_id, transcript_path, cwd, permission_mode, hook_event_name

DEVFORGEAI_CLI_COMMANDS = {
  "phase-record": {
    "positional": ["story_id"],
    "flags": ["--subagent", "--project-root"]
  },
  "phase-record-step": {
    "positional": ["story_id"],
    "flags": ["--phase", "--step", "--project-root"]
  },
  "phase-init": {
    "positional": ["story_id"],
    "flags": ["--project-root"]
  },
  "phase-complete": {
    "positional": ["story_id"],
    "flags": ["--phase", "--checkpoint-passed"]
  },
  "phase-check": {
    "positional": ["story_id"],
    "flags": ["--from", "--to"]
  },
  "phase-status": {
    "positional": ["story_id"],
    "flags": ["--project-root", "--format"]
  }
}
```

**Process:**
```
findings = []

# Extract all JSON field references from ACs and Tech Spec
ac_content = extract_section(story.content, "Acceptance Criteria")
tech_spec = extract_section(story.content, "Technical Specification")
full_text = ac_content + tech_spec

# Check Claude hooks API references
FOR hook_event in CLAUDE_HOOKS_INPUT_SCHEMAS:
  IF hook_event mentioned in full_text (case-sensitive):
    expected_fields = CLAUDE_HOOKS_INPUT_SCHEMAS[hook_event]

    # Extract field names story uses for this hook event
    referenced_fields = extract_json_field_references(full_text, context=hook_event)

    FOR ref in referenced_fields:
      IF ref.field_name NOT in expected_fields AND ref.field_name NOT in COMMON_FIELDS:
        # Find closest match for helpful remediation
        closest = find_closest_string(ref.field_name, expected_fields.keys())
        findings.append({
          type: "coherence/api_contract_error",
          severity: "CRITICAL",
          affected: [story.story_id],
          summary: f"Wrong API field name for {hook_event} hook event",
          evidence: f"Story references '{ref.field_name}' but {hook_event} API uses '{closest}'",
          remediation: f"Replace all occurrences of '{ref.field_name}' with '{closest}'",
          phase: "3e"
        })

# Check devforgeai-validate CLI references
FOR cmd_name in DEVFORGEAI_CLI_COMMANDS:
  IF cmd_name mentioned in full_text:
    expected = DEVFORGEAI_CLI_COMMANDS[cmd_name]

    # Check if story uses positional args where flags are expected (or vice versa)
    cli_usages = extract_cli_invocations(full_text, cmd_name)
    FOR usage in cli_usages:
      FOR flag in expected["flags"]:
        IF flag_name_without_dashes(flag) appears as positional arg in usage:
          findings.append({
            type: "coherence/api_contract_error",
            severity: "HIGH",
            affected: [story.story_id],
            summary: f"CLI argument format mismatch for {cmd_name}",
            evidence: f"Story uses positional arg for '{flag}' but CLI expects flag syntax",
            remediation: f"Use '{flag}' flag syntax instead of positional argument",
            phase: "3e"
          })

RETURN findings
```

**Extraction heuristic for `extract_json_field_references()`:**
```
Look for:
- Patterns like: .field_name, ['field_name'], jq -r '.field_name'
- JSON examples in code blocks with quoted keys
- YAML schema definitions with key: names
- Prose references like "the agent_type field" or "receives agent_type"
```

---

### 13. validate_plan_story_drift(story, plan_file)

**Purpose:** Detect specification drift between plan and generated stories

**Severity:** HIGH (drift causes implementation confusion across sessions)

**Input:** Single story content dict, plan_file path (or None)

**Process:**
```
IF plan_file is None:
  RETURN []  # No plan to compare against

plan_content = Read(plan_file)
findings = []

# --- Compare file/script names ---
plan_filenames = extract_filenames_from_prose(plan_content)  # e.g., "track-subagent-invocation.sh"
story_filenames = extract_filenames_from_prose(story.content)

# Match by semantic role (both reference "SubagentStop hook script")
FOR each semantic_role that appears in both:
  plan_name = plan_filenames[semantic_role]
  story_name = story_filenames[semantic_role]
  IF plan_name != story_name:
    findings.append({
      type: "coherence/plan_story_drift",
      severity: "HIGH",
      affected: [story.story_id],
      summary: f"Script name drift: plan vs story",
      evidence: f"Plan specifies '{plan_name}', story specifies '{story_name}'",
      remediation: f"Update story to use '{plan_name}' (from plan)",
      phase: "3e"
    })

# --- Compare timeout values ---
plan_timeouts = extract_timeout_values(plan_content)  # {hook_event: seconds}
story_timeouts = extract_timeout_values(story.content)

FOR event in set(plan_timeouts.keys()) & set(story_timeouts.keys()):
  IF plan_timeouts[event] != story_timeouts[event]:
    findings.append({
      type: "coherence/plan_story_drift",
      severity: "MEDIUM",
      affected: [story.story_id],
      summary: f"Timeout drift for {event}",
      evidence: f"Plan: {plan_timeouts[event]}s, Story: {story_timeouts[event]}s",
      remediation: f"Update story timeout to {plan_timeouts[event]}s",
      phase: "3e"
    })

# --- Compare field name conventions ---
plan_fields = extract_field_definitions(plan_content)  # {schema_target: {field: type}}
story_fields = extract_field_definitions(story.content)

FOR target in set(plan_fields.keys()) & set(story_fields.keys()):
  plan_f = set(plan_fields[target].keys())
  story_f = set(story_fields[target].keys())
  diff = plan_f.symmetric_difference(story_f)
  IF diff:
    findings.append({
      type: "coherence/plan_story_drift",
      severity: "HIGH",
      affected: [story.story_id],
      summary: f"Field name drift for '{target}'",
      evidence: f"Plan fields: {sorted(plan_f)}, Story fields: {sorted(story_f)}",
      remediation: "Align story fields to plan specification",
      phase: "3e"
    })

RETURN findings
```

**Plan file discovery (called by Sub-Phase 3e orchestration):**
```
FOR epic_id in epics_in_scope:
  # Search .claude/plans/ for files referencing this epic or its stories
  plan_files = Glob(pattern=".claude/plans/*.md")
  FOR plan_file in plan_files:
    content_preview = Read(plan_file, limit=50)  # Check header only
    IF epic_id in content_preview:
      RETURN plan_file
    FOR story_id in stories_in_epic:
      IF story_id in content_preview:
        RETURN plan_file

  # Fallback: check brainstorm for plan reference
  brainstorm = find_brainstorm_for_epic(epic_id)
  IF brainstorm:
    plan_ref = extract_field(brainstorm.content, "Feeds Into")
    IF plan_ref and ".claude/plans/" in plan_ref:
      RETURN plan_ref

  RETURN None
```

---

### 14. validate_naming_consistency(stories_in_epic)

**Purpose:** Verify artifact naming conventions are consistent across sibling stories

**Severity:** MEDIUM (confusing but not functionally blocking)

**Input:** List of story content dicts from the same epic

**Process:**
```
findings = []
artifact_names = {}  # {story_id: [file_names]}

FOR story in stories_in_epic:
  dod = extract_section(story.content, "Definition of Done")
  tech_spec = extract_section(story.content, "Technical Specification")
  combined = dod + "\n" + tech_spec

  # Extract file paths being created (not existing files being modified)
  created_files = extract_created_file_paths(combined)
  artifact_names[story.story_id] = created_files

# Classify naming patterns for script files
all_scripts = []
FOR story_id, files in artifact_names.items():
  FOR f in files:
    IF f.endswith('.sh') OR f.endswith('.py') OR f.endswith('.json'):
      all_scripts.append({"name": basename(f), "story": story_id})

IF len(all_scripts) >= 2:
  # Check: are names descriptive (contain action/purpose) or generic (contain event name)?
  descriptive_count = 0
  generic_count = 0
  FOR script in all_scripts:
    IF contains_action_word(script.name):  # e.g., "track-", "validate-", "inject-"
      descriptive_count += 1
    ELSE:  # e.g., "stop-hook.sh", "session-start-hook.sh"
      generic_count += 1

  IF descriptive_count > 0 AND generic_count > 0:
    findings.append({
      type: "coherence/naming_inconsistency",
      severity: "MEDIUM",
      affected: [s["story"] for s in all_scripts],
      summary: "Mixed naming conventions for created artifacts",
      evidence: f"Descriptive: {[s['name'] for s in all_scripts if contains_action_word(s['name'])]}, Generic: {[s['name'] for s in all_scripts if not contains_action_word(s['name'])]}",
      remediation: "Standardize all artifact names to use descriptive naming (action-object pattern)",
      phase: "3e"
    })

RETURN findings
```

---

### 15. validate_format_consistency(stories_in_epic)

**Purpose:** Verify shared format patterns (IDs, regexes, task subject formats) are consistent across stories

**Severity:** HIGH (incompatible formats break cross-story integration)

**Input:** List of story content dicts from the same epic

**Process:**
```
findings = []
format_specs = {}  # {semantic_type: {value: str, story_id: str, evidence: str}}

FOR story in stories_in_epic:
  ac_content = extract_section(story.content, "Acceptance Criteria")
  tech_spec = extract_section(story.content, "Technical Specification")
  combined = ac_content + "\n" + tech_spec

  # Extract format patterns
  patterns = extract_format_patterns(combined)
  # Each pattern: { semantic_type: str, value: str, evidence: str }
  # Examples:
  #   { semantic_type: "step_id_format", value: "NN.M", evidence: "'02.2'" }
  #   { semantic_type: "step_id_format", value: "PHASE-NN-STEP-MM", evidence: "'PHASE-02-STEP-01'" }
  #   { semantic_type: "task_subject_format", value: "Step NN.M:", evidence: "'Step 02.2: ...'" }
  #   { semantic_type: "task_subject_format", value: "PHASE-NN-STEP-MM:", evidence: "'PHASE-02-STEP-01: ...'" }

  FOR pattern in patterns:
    key = pattern.semantic_type
    IF key in format_specs:
      IF format_specs[key].value != pattern.value:
        findings.append({
          type: "coherence/format_inconsistency",
          severity: "HIGH",
          affected: [format_specs[key].story_id, story.story_id],
          summary: f"Format inconsistency for '{key}'",
          evidence: f"{format_specs[key].story_id} uses '{format_specs[key].value}' (e.g., {format_specs[key].evidence}), {story.story_id} uses '{pattern.value}' (e.g., {pattern.evidence})",
          remediation: "Align format to plan specification. All stories must use the same ID/pattern format.",
          phase: "3e"
        })
    ELSE:
      format_specs[key] = {"value": pattern.value, "story_id": story.story_id, "evidence": pattern.evidence}

RETURN findings
```

**Extraction heuristic for `extract_format_patterns()`:**
```
Look for:
- Regex patterns in validation fields: "^PHASE-[\d.]+-STEP-\d+$" or "^\d+\.\d+$"
- ID examples in AC text: 'PHASE-02-STEP-01' or '02.2'
- Task subject format examples: "Step 02.2: ..." or "PHASE-02-STEP-01: ..."
- Classify by semantic type based on surrounding context (step ID, task subject, etc.)
```

---

### 16. validate_instruction_consistency(stories_in_epic, plan_file)

**Purpose:** Detect contradictory placement/ordering instructions across stories

**Severity:** HIGH (contradictions cause implementation ambiguity)

**Input:** List of story content dicts, plan_file path (or None)

**Process:**
```
findings = []
instructions = {}  # {subject: {placement: str, story_id: str}}

FOR story in stories_in_epic:
  notes = extract_section(story.content, "Notes")
  design_decisions = extract_subsection(notes, "Design Decisions")

  IF design_decisions:
    # Extract placement/ordering instructions
    # Look for patterns like: "Section added after X, before Y"
    #                         "Added between X and Y"
    #                         "Placed after X"
    placements = extract_placement_instructions(design_decisions)

    FOR instruction in placements:
      key = instruction.subject  # e.g., "Progressive Task Disclosure section"
      IF key in instructions:
        IF instructions[key].placement != instruction.placement:
          findings.append({
            type: "coherence/instruction_contradiction",
            severity: "HIGH",
            affected: [instructions[key].story_id, story.story_id],
            summary: f"Contradictory placement for '{key}'",
            evidence: f"{instructions[key].story_id} says '{instructions[key].placement}', {story.story_id} says '{instruction.placement}'",
            remediation: "Check plan file for authoritative placement instruction and align both stories.",
            phase: "3e"
          })
      ELSE:
        instructions[key] = {"placement": instruction.placement, "story_id": story.story_id}

# Cross-check against plan if available
IF plan_file:
  plan_content = Read(plan_file)
  plan_instructions = extract_placement_instructions(plan_content)

  FOR instruction in plan_instructions:
    key = instruction.subject
    IF key in instructions AND instructions[key].placement != instruction.placement:
      findings.append({
        type: "coherence/instruction_contradiction",
        severity: "HIGH",
        affected: [instructions[key].story_id],
        summary: f"Story contradicts plan placement for '{key}'",
        evidence: f"Plan says '{instruction.placement}', story says '{instructions[key].placement}'",
        remediation: f"Update story to match plan: '{instruction.placement}'",
        phase: "3e"
      })

RETURN findings
```

---

### 17. validate_dependency_assumptions(stories_in_epic)

**Purpose:** Verify dependent stories' assumptions about their dependencies match actual specifications

**Severity:** HIGH (incorrect assumptions cause integration failures)

**Input:** List of story content dicts from the same epic

**Process:**
```
findings = []

# Build output specification map: what does each story produce?
story_outputs = {}
FOR story in stories_in_epic:
  tech_spec = extract_section(story.content, "Technical Specification")
  dod = extract_section(story.content, "Definition of Done")

  outputs = {
    "file_names": extract_created_file_paths(tech_spec + dod),
    "field_names": extract_field_definitions(tech_spec),
    "cli_commands": extract_cli_definitions(tech_spec),
    "data_formats": extract_format_patterns(tech_spec),
  }
  story_outputs[story.story_id] = outputs

# Check each dependency relationship
FOR story in stories_in_epic:
  depends_on = story.frontmatter.get("depends_on", [])

  FOR dep_id in depends_on:
    IF dep_id NOT in story_outputs:
      CONTINUE  # Dependency not in scope

    dep_outputs = story_outputs[dep_id]

    # Extract what this story ASSUMES about the dependency
    ac_content = extract_section(story.content, "Acceptance Criteria")
    tech_spec = extract_section(story.content, "Technical Specification")

    # Check field name assumptions
    referenced_fields = extract_dependency_field_references(tech_spec, dep_id)
    FOR ref in referenced_fields:
      # Does the dependency actually define this field?
      dep_fields = dep_outputs.get("field_names", {})
      FOR target_file, fields in dep_fields.items():
        IF ref.target_file == target_file AND ref.field_name NOT in fields:
          closest = find_closest_string(ref.field_name, fields.keys())
          findings.append({
            type: "coherence/dependency_assumption_mismatch",
            severity: "HIGH",
            affected: [story.story_id, dep_id],
            summary: f"{story.story_id} assumes wrong field name from {dep_id}",
            evidence: f"{story.story_id} references '{ref.field_name}' from {dep_id}'s '{ref.target_file}', but {dep_id} defines '{closest}'",
            remediation: f"Update {story.story_id} to use '{closest}' instead of '{ref.field_name}'",
            phase: "3e"
          })

    # Check data format assumptions
    story_formats = extract_format_patterns(ac_content + tech_spec)
    dep_formats = dep_outputs.get("data_formats", [])
    FOR sf in story_formats:
      FOR df in dep_formats:
        IF sf.semantic_type == df.semantic_type AND sf.value != df.value:
          findings.append({
            type: "coherence/dependency_assumption_mismatch",
            severity: "HIGH",
            affected: [story.story_id, dep_id],
            summary: f"{story.story_id} assumes wrong format from {dep_id}",
            evidence: f"{story.story_id} assumes '{sf.semantic_type}' format '{sf.value}', but {dep_id} specifies '{df.value}'",
            remediation: f"Update {story.story_id} to use format '{df.value}' from {dep_id}",
            phase: "3e"
          })

RETURN findings
```
