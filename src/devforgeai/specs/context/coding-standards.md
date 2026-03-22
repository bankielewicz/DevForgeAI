# Coding Standards - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2026-01-19
**Version**: 1.2 (Added: Phase 04.5 and Phase 05.5 for AC Compliance Verification - EPIC-046)

## Framework Coding Standards

### Markdown Documentation Style

**All framework components use Markdown with specific patterns**:

✅ **CORRECT Style**:
```markdown
## Phase 1: Context Validation

Read context files in PARALLEL:
- Read(file_path="devforgeai/context/tech-stack.md")
- Read(file_path="devforgeai/context/source-tree.md")

HALT if ANY file missing: "Context files incomplete"
```

❌ **FORBIDDEN Style**:
```markdown
## Phase 1: Context Validation

The system should read context files. First it validates...
[Narrative prose instead of direct instructions]
```

**Rationale**: Claude interprets direct instructions better than prose.

### Tool Usage Standards

**LOCKED: Use Native Tools Over Bash**

✅ **CORRECT**:
```markdown
Read(file_path="story.md")
Edit(file_path="config.md", old_string="v1.0", new_string="v1.1")
Glob(pattern="**/*.md")
Grep(pattern="LOCKED", glob="**/*.md")
```

❌ **FORBIDDEN**:
```markdown
Bash(command="cat story.md")
Bash(command="sed -i 's/v1.0/v1.1/' config.md")
Bash(command="find . -name '*.md'")
Bash(command="grep 'LOCKED' **/*.md")
```

**Exception**: Bash required for tests, builds, git, package managers.

### Skill Naming Convention (ADR-017)

**Skills use gerund naming (verb + -ing) without framework prefix**:
- ✅ `designing-systems` (gerund form, no prefix)
- ✅ `implementing-stories` (gerund form, no prefix)
- ❌ `devforgeai-[name]` (old convention: framework prefix, non-gerund)

### YAML Frontmatter Standards

**All skills, subagents, commands MUST have frontmatter**:

```yaml
---
name: skill-name
description: Brief description of when to use this
tools: Read, Write, Edit, Bash   # Optional, comma-separated
model: inherit                   # Optional: sonnet, haiku, opus, inherit
---
```

### Progressive Disclosure Pattern

✅ **CORRECT**:
```markdown
# SKILL.md (main file - concise)
## Phase 3: Complexity Assessment
Score complexity on 0-60 scale.
For detailed scoring rubric, see references/complexity-assessment-matrix.md

# references/complexity-assessment-matrix.md (deep details)
[1000 lines of detailed scoring criteria]
```

❌ **FORBIDDEN**:
```markdown
# SKILL.md (monolithic - verbose)
## Phase 3: Complexity Assessment
[1000 lines of detailed scoring criteria inline]
```

### AskUserQuestion Pattern

**LOCKED: Use for ALL ambiguities**:

```markdown
Question: "Which [technology/pattern/approach] should be used?"
Header: "[Category]"
Description: "This decision will be locked in [context-file]"
Options:
  - "[Option 1] (recommended for [reason])"
  - "[Option 2] (better for [use-case])"
  - "[Option 3] ([tradeoff])"
multiSelect: false
```

### File Size Standards

**LOCKED Component Size Limits**:
- Skills: Target 500-800 lines, Max 1,000 lines
- Commands: Target 200-400 lines, Max 500 lines
- Subagents: Target 100-300 lines, Max 500 lines
- Context Files: Target 200-400 lines, Max 600 lines

**Enforcement**: Extract to references/ when exceeding target.

### Naming Conventions

**Files**: lowercase-with-hyphens.md
**Skills**: [gerund-phrase] (e.g., `implementing-stories`, `validating-quality`) — see ADR-017
**Subagents**: [domain]-[role]
**Commands**: [action] or [action]-[object]

### Documentation Structure Pattern

**Standard Section Order**:
1. YAML frontmatter
2. Purpose statement
3. When to Use
4. Workflow/Process (numbered phases)
5. Reference files
6. Success criteria

---

## Story Type Classification

Story types (`feature`, `documentation`, `bugfix`, `refactor`) define TDD phase skipping behavior.

**See:** `.claude/skills/devforgeai-story-creation/references/story-type-classification.md`

---

## Phase Naming Convention (STORY-126)

All development workflow phases use standardized naming:

### Phase Numbering

| Phase | Name | Reference File |
|-------|------|----------------|
| Phase 01 | Pre-Flight Validation | `preflight-validation.md` |
| Phase 02 | Test-First Design | `tdd-red-phase.md` |
| Phase 03 | Implementation | `tdd-green-phase.md` |
| Phase 04 | Refactoring | `tdd-refactor-phase.md` |
| Phase 04.5 | AC Compliance Verification (Post-Refactor) | `ac-verification-workflow.md` |
| Phase 05 | Integration & Validation | `integration-testing.md` |
| Phase 05.5 | AC Compliance Verification (Post-Integration) | `ac-verification-workflow.md` |
| Phase 06 | Deferral Challenge | `phase-06-deferral-challenge.md` |
| Phase 07 | DoD Update | `dod-update-workflow.md` |
| Phase 08 | Git Workflow | `git-workflow-conventions.md` |
| Phase 09 | Feedback Hook | (inline in SKILL.md) |
| Phase 10 | Result Interpretation | (inline in SKILL.md) |

### Sub-Step Naming (Phase 01 Only)

Phase 01 has granular sub-steps: `Phase 01.X` or `Phase 01.X.Y`

Examples:
- `Phase 01.0` - Project root validation
- `Phase 01.1` - Git repository validation
- `Phase 01.1.5` - User consent (conditional)
- `Phase 01.6.5` - Story type detection

### Documentation Standards

- **Headings:** Use `Phase NN: Full Name` format (no color suffixes)
- **References:** Use `Phase 01.X` in prose (not "Step 0.X")
- **TDD Patterns:** RED/GREEN/REFACTOR appear in body text, not headings

**See:** `.claude/skills/implementing-stories/` for workflow implementation

---

## Markdown Command Testing Pattern

For `.claude/commands/*.md` specification files, test via three levels:

### Structural Tests

Verify required sections exist using Grep for section headers:

```bash
# Verify required section exists in command file
grep -qE "^## Required Section" target_file.md
```

### Pattern Tests

Verify code blocks contain expected tool references:

```bash
# Validate tool patterns appear in code examples
grep -qE "Read\(|Edit\(|Grep\(" target_file.md
```

### Integration Tests

Invoke command and verify output matches expected behavior:

```bash
# Execute command and validate output
output=$(invoke_command)
if [[ "$output" == *"expected_pattern"* ]]; then
  echo "PASS: Output validation"
fi
```

### Coverage Calculation

Coverage = (found patterns / required patterns) × 100%

Where patterns are the assertions documented in acceptance criteria.

---

## Documentation Cross-Reference Format (LOCKED)

When referencing other documentation files, use this standardized format for consistency and navigation.

### Standard Format

```
For full details, see: [filename.md](filename.md) (Section Name)
```

### Required Elements

| Element | Description | Example |
|---------|-------------|---------|
| Introductory phrase | Always use "For full details, see:" | `For full details, see:` |
| Markdown link | Standard `[text](url)` format | `[complexity-assessment-matrix.md](complexity-assessment-matrix.md)` |
| Context hint | Actual section header in parentheses | `(Scoring Rubric)` |

### Examples

✅ **CORRECT**:
```markdown
For full details, see: [story-type-classification.md](story-type-classification.md) (Type Definitions)

For full details, see: [preflight-validation.md](preflight-validation.md) (Phase 01.0 Validation)
```

❌ **DEPRECATED** (do not use):
```markdown
See: story-type-classification.md, lines 45-60
Reference: story-type-classification.md#type-definitions
Details in story-type-classification.md (lines 45-60)
```

### Context Hint Requirements

- Use actual section header text, not line numbers
- Match the heading exactly as it appears in the target file
- If no specific section, omit the context hint entirely

**Rationale**: Section headers are stable identifiers; line numbers change with edits.

---

## WSL Test Execution

### Path Handling

**Use `/mnt/c/` paths in WSL, not `C:\`**

When running tests on Windows Subsystem for Linux (WSL), always reference files using Unix-style paths with the `/mnt/c/` prefix. pytest discovers tests from Unix-style paths, and coverage reports use Unix paths.

✅ **Correct**:
```
/mnt/c/Projects/DevForgeAI2/tests/
/mnt/c/Projects/DevForgeAI2/src/
```

❌ **Incorrect**:
```
C:\Projects\DevForgeAI2\tests\
C:\Projects\DevForgeAI2\src\
```

**Rationale**: WSL mount points may not preserve file metadata or execute permissions when using Windows-style paths. Unix paths work consistently across WSL and native Linux.

---

### Environment Setup

**Set Python path and navigate to project root**

Before running tests, configure your WSL environment with these commands:

```bash
cd /mnt/c/Projects/DevForgeAI2
export PYTHONPATH=".:$PYTHONPATH"
```

**Why**: `PYTHONPATH` tells Python where to find module imports. This export adds the current directory (`.`) to the search path, allowing pytest to discover project modules. Without this, you'll get "ModuleNotFoundError" when running tests.

For full details, see: [INSTALL.md](../../../installer/INSTALL.md) (PYTHONPATH Configuration)

---

### Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Module not found | PYTHONPATH not set | `export PYTHONPATH=".:$PYTHONPATH"` |
| Permission denied on .sh | Windows file locks | Close file in other programs, or `chmod +x script.sh` |
| Line ending errors (`$'\r': command not found`) | CRLF in shell scripts | `dos2unix script.sh` or `sed -i 's/\r$//' script.sh` |
| Slow file operations | Windows filesystem overhead | Run tests from WSL native filesystem if possible |
| pytest not found | Virtual env not activated | `source venv/bin/activate` or `pip install pytest` |

---

### Test Commands

**Run pytest with these commands**:

```bash
pytest tests/ -v                                          # Run all tests

pytest tests/test_validators.py -v                        # Run specific test file

pytest tests/ --cov=src --cov-report=term-missing        # Run with coverage report

pytest tests/test_validators.py::test_dod_validation -v  # Run single test
```

---

### Shell Script Testing

**Always run shell scripts with `bash`, not direct execution**

When executing shell scripts on WSL, use explicit `bash` invocation instead of direct execution.

✅ **Correct**:
```bash
bash path/to/test.sh
bash tests/run_story_tests.sh
```

❌ **Incorrect**:
```bash
./path/to/test.sh
./tests/run_story_tests.sh
```

**Why**: WSL mount points (especially when accessing Windows filesystem) may not preserve execute permissions correctly. Explicit `bash` invocation bypasses permission issues.

**Fix line endings first**: Before running, ensure scripts have Unix line endings:
```bash
dos2unix path/to/test.sh && bash path/to/test.sh
```

---

## XML Acceptance Criteria Schema

**Purpose:** Define XML schema for machine-readable acceptance criteria in story files.

**Reference:** STORY-279, EPIC-046 AC Compliance Verification System

### Root Element

```xml
<acceptance_criteria id="ACN" implements="COMP-XXX,COMP-YYY">
  <!-- Child elements -->
</acceptance_criteria>
```

**Root Element: `<acceptance_criteria>`**

| Attribute | Required | Format | Description |
|-----------|----------|--------|-------------|
| `id` attribute | **Required** | `AC1`, `AC2`, `AC3`, etc. | Unique identifier matching pattern `^AC\d+$` |
| `implements` attribute | **Optional** | Comma-separated `COMP-XXX` | Links to technical specification components |

### Mandatory Child Elements

The following child elements are **required** inside `<acceptance_criteria>`:

| Element | Required | Description |
|---------|----------|-------------|
| `<given>` | **Mandatory** | Initial context or precondition |
| `<when>` | **Mandatory** | Action or event being tested |
| `<then>` | **Mandatory** | Expected outcome or result |

### Optional Verification Element

The `<verification>` element is **optional** and provides hints for automated verification:

```xml
<verification>
  <source_files>
    <file>path/to/source.py</file>
  </source_files>
  <test_file>path/to/test.py</test_file>
  <coverage_threshold>95</coverage_threshold>
</verification>
```

| Element | Parent | Description |
|---------|--------|-------------|
| `<verification>` | `<acceptance_criteria>` | Optional container for verification hints |
| `<source_files>` | `<verification>` | Contains `<file>` elements listing source files |
| `<test_file>` | `<verification>` | Expected test file path |
| `<coverage_threshold>` | `<verification>` | Coverage percentage target (0-100) |

### Examples

**Example 1: Minimal AC (Required Elements Only)**

```xml
<acceptance_criteria id="AC1">
  <given>User is on the login page</given>
  <when>User enters valid credentials and clicks submit</when>
  <then>User is redirected to dashboard</then>
</acceptance_criteria>
```

**Example 2: AC with Implements Attribute**

```xml
<acceptance_criteria id="AC2" implements="COMP-001,COMP-002">
  <given>API endpoint /users exists</given>
  <when>GET request is sent with valid auth token</when>
  <then>Response returns 200 with user list</then>
</acceptance_criteria>
```

**Example 3: Complete AC with Verification Block**

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>Shopping cart has items</given>
  <when>User clicks checkout button</when>
  <then>Order is created with correct total</then>
  <verification>
    <source_files>
      <file>src/cart/checkout.py</file>
      <file>src/orders/service.py</file>
    </source_files>
    <test_file>tests/STORY-XXX/test_ac3_checkout.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

### Validation Rules

1. **ID Format**: Must match regex `^AC\d+$` (e.g., AC1, AC2, AC10)
2. **Mandatory Children**: Reject AC blocks missing `<given>`, `<when>`, or `<then>`
3. **Implements Format**: If present, must be comma-separated COMP-XXX identifiers
4. **Coverage Threshold**: If present, must be integer 0-100

---

> **Note**: Projects using DevForgeAI will have their own coding-standards.md with language-specific patterns (CSharp, Python, JavaScript, etc.).
