# Anti-Pattern Scanner: Integration & Testing Guide

**Purpose:** QA skill integration patterns, invocation examples, and test suite documentation for the anti-pattern-scanner subagent.

**Loaded by:** `Read(file_path=".claude/agents/anti-pattern-scanner/references/integration-testing-guide.md")`

---

## Integration with spec-driven-qa Skill

### Invocation Point (Phase 2: Anti-Pattern Detection)

The anti-pattern-scanner is invoked by spec-driven-qa skill's Phase 2 anti-pattern detection workflow.

**Invocation Pattern (with Context Summary - RECOMMENDED):**
```python
anti_pattern_result = Task(
  subagent_type="anti-pattern-scanner",
  description="Scan for anti-patterns and architecture violations",
  prompt=f"""
  Scan story codebase for anti-patterns.

  **Context Summary (do not re-read files):**
  - tech-stack.md: Framework-agnostic, Markdown-based, no external deps
  - anti-patterns.md: No Bash for file ops, no monolithic components
  - architecture-constraints.md: Three-layer, single responsibility
  - source-tree.md: Skills in .claude/skills/, agents in .claude/agents/
  - dependencies.md: Zero external deps for core framework
  - coding-standards.md: Direct instructions, not prose; YAML frontmatter required

  Story ID: {story_id}
  Language: {language}
  Scan Mode: full (all 6 categories)

  Execute 9-phase workflow per anti-pattern-scanner specification.
  Return JSON with violations by severity, blocks_qa status, and remediation.
  """
)
```

**Invocation Pattern (without summary - legacy):**
```python
anti_pattern_result = Task(
  subagent_type="anti-pattern-scanner",
  description="Scan for anti-patterns and architecture violations",
  prompt=f"""
  Scan story codebase for anti-patterns using all 6 context files.

  Context Files (MANDATORY - enforce as law):
  {Read file_path="devforgeai/specs/context/tech-stack.md"}
  {Read file_path="devforgeai/specs/context/source-tree.md"}
  {Read file_path="devforgeai/specs/context/dependencies.md"}
  {Read file_path="devforgeai/specs/context/coding-standards.md"}
  {Read file_path="devforgeai/specs/context/architecture-constraints.md"}
  {Read file_path="devforgeai/specs/context/anti-patterns.md"}

  Story ID: {story_id}
  Language: {language}
  Scan Mode: full (all 6 categories)

  Execute 9-phase workflow per anti-pattern-scanner specification.
  Return JSON with violations by severity, blocks_qa status, and remediation.
  """
)
```

**Result Integration:**
```python
# Merge violations into QA report
violations.update(anti_pattern_result["violations"])

# Update blocking status (OR logic)
blocks_qa = blocks_qa OR anti_pattern_result["blocks_qa"]

# Add to blocking reasons if applicable
if anti_pattern_result["blocks_qa"]:
  blocking_reasons.extend(anti_pattern_result["blocking_reasons"])
```

**Token Efficiency:** Subagent approach uses ~3K tokens vs ~8K inline (73% reduction)

---

## Testing

Comprehensive test suite in `/tests/subagent_anti_pattern_scanner/test_anti_pattern_scanner.py`:

- **AC1:** Specification tests (8 tests) - PASSING
  - File exists, YAML frontmatter, 9-phase workflow, contracts, guardrails
- **AC2-AC6:** Category detection tests (27 tests) - PENDING implementation
  - Library substitution, structure, layers, code smells, security
- **AC7-AC8:** Blocking logic and evidence tests (13 tests) - PENDING
  - Blocking rules, evidence fields, recommendations
- **AC9-AC12:** Integration, templates, coverage, error handling (23 tests) - PENDING
  - QA integration, prompt templates, all categories, error scenarios
- **Integration & Edge Cases:** 12 tests - PENDING

**Test Framework:** pytest with comprehensive fixtures and parametrized test cases
