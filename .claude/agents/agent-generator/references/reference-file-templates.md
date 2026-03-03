# Reference File Templates

**Purpose:** Templates for generating framework guardrail reference files that accompany subagents.

---

## When to Generate Reference Files

**MANDATORY for:**
- Command refactoring subagents (formatters, interpreters, orchestrators)
- Domain-specific subagents (qa, architecture, security, deployment)
- Decision-making subagents

**OPTIONAL for:**
- Simple validation subagents
- Single-purpose utilities

---

## Reference File Location

```
# Related skill exists
.claude/skills/[related-skill]/references/[subagent-topic]-guide.md

# No related skill
.claude/skills/devforgeai-subagent-creation/references/[subagent-name]-guide.md
```

---

## Standard Reference File Template

```markdown
# [Topic] Guide

**Purpose:** Framework guardrails for [subagent-name] subagent

**Prevents "bull in china shop" behavior by providing:**
- DevForgeAI workflow context (11 workflow states, 4 quality gates)
- Immutable constraints (thresholds, rules, patterns from context files)
- Decision boundaries (what's valid, what's not)
- Integration patterns (how to coordinate with other components)

**Reference Type:** [command-refactoring|domain-constraints|decision-guidance]

---

## DevForgeAI Context

### Workflow States (11-State Progression)

```
Backlog → Architecture → Ready for Dev → In Development → Dev Complete →
QA In Progress → [QA Approved | QA Failed] → Releasing → Released
```

**[subagent-name]'s role in workflow:**
[Describe at which states this subagent operates]
[Example: "Invoked during 'In Development' state, TDD Red phase"]

### Quality Gates (4 Gates)

**Gate 1: Context Validation** (Architecture → Ready for Dev)
- All 6 context files exist and validated
- No placeholder content (TODO, TBD)

**Gate 2: Test Passing** (Dev Complete → QA In Progress)
- Build succeeds
- All tests pass (100% pass rate)
- Light validation passed

**Gate 3: QA Approval** (QA Approved → Releasing)
- Deep validation PASSED
- Coverage meets thresholds (95%/85%/80%)
- Zero CRITICAL violations
- Zero HIGH violations (or approved exceptions)

**Gate 4: Release Readiness** (Releasing → Released)
- QA approved
- All workflow checkboxes complete
- No blocking dependencies

**[subagent-name]'s role in quality gates:**
[Describe which gates this subagent participates in]

### Domain-Specific Context

[CUSTOMIZE FOR SUBAGENT DOMAIN]

[For backend subagents:]
**Clean Architecture Layers:**
- Domain: Business logic (no external dependencies)
- Application: Use cases and orchestration
- Infrastructure: External integrations (DB, APIs)
- Presentation: Controllers, views, UI

**Layer dependencies:**
- Presentation → Application → Domain ✓
- Infrastructure → Domain (interfaces only) ✓
- Domain → Infrastructure ❌ (violates dependency inversion)

[For QA subagents:]
**Coverage Thresholds (Strict, Immutable):**
- Business Logic: 95% minimum
- Application Layer: 85% minimum
- Infrastructure Layer: 80% minimum

**Violation Severity:**
- CRITICAL: Blocks QA approval, must fix
- HIGH: Blocks QA approval (or requires exception)
- MEDIUM: Warning, should fix
- LOW: Informational, optional fix

[For architecture subagents:]
**Technology Decision Process:**
1. Check tech-stack.md for locked technologies
2. If not in tech-stack.md, use AskUserQuestion
3. Never substitute without user approval
4. Create ADR for all technology decisions
5. Update tech-stack.md and dependencies.md

---

## Framework Constraints

### 1. [Constraint Category 1] (Strict, Immutable)

[Define what CANNOT change - extract from relevant context files]

**Rules:**
- [Rule 1 from context files]
- [Rule 2 from context files]
- [Rule 3 from context files]

**Example:**
```
❌ WRONG: [Example of constraint violation]
✅ CORRECT: [Example following constraint]
```

**Never say:**
- "[Example of relaxing this constraint]"
- "This threshold is flexible"
- "Context files are guidelines"

**Always enforce:**
- "[Strict enforcement example]"
- "Technology must be in tech-stack.md"
- "Coverage below threshold blocks QA"

### 2. [Constraint Category 2] (Deterministic)

[Define classification/categorization rules - must be objective]

**Decision tree:**
```
IF [condition] THEN [outcome]
ELSE IF [condition] THEN [outcome]
ELSE [default outcome]
```

### 3. [Additional Constraints as needed]

---

## [Subagent Task] Guidelines

### Task Execution Within Constraints

**How to perform task while respecting framework:**

1. **[Step 1] with Constraint Reference**
   - Check: [Which context file to validate against]
   - Action: [What to do]
   - Constraint: [Which rule applies]
   - Output: [Expected result]

2. **[Step 2] with Constraint Reference**
   - [Similar structure]

**Output Template:**

```markdown
## [Subagent Output Section]

**[Field 1]:** [value following constraint X]
**[Field 2]:** [value following constraint Y]

✅ Passes: [list]
❌ Violations: [list with severity and context file reference]
⚠️ Warnings: [list with suggestions]
```

**Anti-patterns to avoid:**
- ❌ [Anti-pattern 1]: [Why forbidden]
- ❌ [Anti-pattern 2]: [Why forbidden]

**Correct patterns:**
- ✅ [Pattern 1]: [Why required]
- ✅ [Pattern 2]: [Why required]

---

## Framework Integration Points

### Context Files to Reference

**When to check each context file:**

- **tech-stack.md:** Before suggesting any technology
- **source-tree.md:** Before creating/suggesting file locations
- **dependencies.md:** Before adding package dependencies
- **coding-standards.md:** When generating/reviewing code
- **architecture-constraints.md:** When validating layer boundaries
- **anti-patterns.md:** When detecting violations

**How to reference:**
```
Read(file_path="devforgeai/specs/context/[file].md")
# Extract relevant rules
# Apply to current analysis
# Report violations with specific reference
```

### Related Skills/Subagents

**Coordination patterns:**

- **[Skill/Subagent 1]:**
  - When: [Phase/step/condition]
  - Expects: [Input contract]
  - Returns: [Output contract]
  - Error handling: [What to do if fails]

### Tool Usage Patterns

**Mandated by DevForgeAI:**

**File operations:** ALWAYS native tools
- Read(file_path="...") NOT cat
- Grep(pattern="...") NOT grep command
- Glob(pattern="...") NOT find
- Edit(...) NOT sed/awk
- Write(...) NOT echo >

**Rationale:** 40-73% token savings (evidence-based)

---

## Output Format

[If subagent returns structured data]

```json
{
  "status": "SUCCESS|ERROR|PARTIAL",
  "result_type": "[specific_type]",
  "display": {
    "template": "[markdown]",
    "title": "...",
    "sections": [...]
  },
  "data": {...},
  "validation": {
    "passes": [...],
    "warnings": [...],
    "failures": [...]
  },
  "recommendations": {...},
  "metadata": {...}
}
```

**Contract guarantees:**
- ✅ Always valid JSON
- ✅ status always present
- ✅ display.template never empty
- ✅ No interpretation needed by caller

---

## Error Scenarios

### [Error Type 1]

**Detection:**
```
IF [condition]:
  ERROR_TYPE = "[type]"
```

**Response:**
```json
{
  "status": "ERROR",
  "data": {
    "error_type": "[type]",
    "error_message": "[description]"
  },
  "recommendations": {
    "remediation": ["[step 1]", "[step 2]"],
    "priority": "HIGH"
  }
}
```

**Caller guidance:**
- Display error to user
- Apply remediation OR ask user

### Framework Constraint Violation

**Detection:**
```
IF violates context_file rules:
  CONSTRAINT_VIOLATION = true
```

**Response:**
```json
{
  "status": "ERROR",
  "result_type": "constraint_violation",
  "data": {
    "violated_constraint": "[file].md - [rule]",
    "violation_details": "[what violated]"
  },
  "recommendations": {
    "remediation": [
      "Review [file].md section [X]",
      "Correct to follow [rule]"
    ],
    "priority": "HIGH"
  }
}
```

**Caller guidance:**
- HALT execution
- Display violation details
- Do NOT proceed until resolved

---

## Testing Checklist

**Validate subagent against framework:**

- [ ] Respects constraint 1: [name]
- [ ] Respects constraint 2: [name]
- [ ] Output format matches schema
- [ ] Framework-aware (not siloed)
- [ ] Integration with [related] tested
- [ ] Error handling comprehensive
- [ ] Context file references accurate
- [ ] Token efficiency target met
- [ ] No autonomous decisions

**Test scenarios:**
1. Happy path: Expected outputs
2. Constraint violation: Detects and reports
3. Missing context: Handles gracefully
4. Integration: Coordinates correctly
5. Error conditions: All handled

---

**Target size:** 200-600 lines
**Update frequency:** When framework constraints change
**Purpose:** Prevent autonomous behavior, enforce compliance
```

---

## Domain-Specific Templates

### QA Domain Reference File

Add these sections:

```markdown
## Coverage Thresholds (Immutable)

| Layer | Threshold | No Exceptions |
|-------|-----------|---------------|
| Business Logic | 95% | CRITICAL if below |
| Application | 85% | CRITICAL if below |
| Infrastructure | 80% | CRITICAL if below |

**Coverage below threshold = QA FAILED**
(Not PASS WITH WARNINGS)

## Violation Severity Classification

| Severity | Definition | QA Impact |
|----------|------------|-----------|
| CRITICAL | Security, data loss | Blocks approval |
| HIGH | Functionality broken | Blocks approval |
| MEDIUM | Code quality | Warning |
| LOW | Style, minor | Informational |
```

### Architecture Domain Reference File

Add these sections:

```markdown
## Technology Decision Rules

1. **Locked technologies** (tech-stack.md)
   - Cannot change without ADR
   - No substitution allowed

2. **New technology requests**
   - HALT + AskUserQuestion
   - Require explicit approval
   - Create ADR if approved
   - Update tech-stack.md and dependencies.md

## Layer Boundary Rules

```
Allowed:
- Presentation → Application → Domain ✓
- Infrastructure → Domain (interfaces) ✓

Forbidden:
- Domain → Infrastructure ❌
- Application → Presentation ❌
- Cross-layer direct dependencies ❌
```
```

### Security Domain Reference File

Add these sections:

```markdown
## OWASP Top 10 Detection

| Vulnerability | Detection Pattern | Severity |
|---------------|-------------------|----------|
| SQL Injection | String concat in queries | CRITICAL |
| XSS | Unescaped output | CRITICAL |
| Broken Auth | Missing validation | CRITICAL |
| Sensitive Data | Hardcoded secrets | CRITICAL |

## Secret Detection Patterns

```regex
password\s*=\s*['"][^'"]+['"]
api[_-]?key\s*=\s*['"][^'"]+['"]
-----BEGIN.*PRIVATE KEY-----
```
```
