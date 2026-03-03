# Scoring Methodology

**Purpose:** Determine confidence levels and evidence scoring for AC verification.

---

## Confidence Level Determination

**Confidence Enum Values:**

| Level | Definition | Criteria |
|-------|------------|----------|
| `HIGH` | Strong evidence of correct implementation | All Given/When/Then matched with DIRECT match_type; source_files hints used |
| `MEDIUM` | Moderate evidence with some inference | Mix of DIRECT and INFERRED matches; OR discovery-based with good coverage |
| `LOW` | Weak evidence requiring manual review | Mostly PARTIAL/INFERRED matches; OR discovery-based with sparse coverage |

**BR-002 Enforcement:** When verification uses discovery fallback (no source_files hints), confidence MUST be MEDIUM or LOW, never HIGH.

---

## Confidence Calculation Rules

```
IF all match_types == DIRECT AND hints_provided:
  confidence = HIGH
ELIF hints_provided AND majority DIRECT:
  confidence = HIGH
ELIF discovery_based AND all match_types == DIRECT:
  confidence = MEDIUM  # BR-002: discovery limits max confidence
ELIF any match_type == PARTIAL:
  confidence = LOW
ELSE:
  confidence = MEDIUM
```

---

## Match Type Classification

| Match Type | Definition | Confidence Impact |
|------------|------------|-------------------|
| `DIRECT` | Exact keyword/pattern match found | HIGH |
| `INFERRED` | Related pattern suggests implementation | MEDIUM |
| `PARTIAL` | Some elements found, others missing | LOW |

---

## Anti-Pattern Detection Scoring

### Severity Hierarchy

| Severity | Impact | AC Status |
|----------|--------|-----------|
| `CRITICAL` | Blocks AC verification | AC marked FAIL |
| `HIGH` | Blocks AC verification | AC marked FAIL |
| `MEDIUM` | Warning only | AC continues (warning logged) |

**CRITICAL and HIGH violations both cause AC to fail verification.**

### Flagging Decision Logic

```
IF severity == "CRITICAL" THEN:
  flag_ac_as_failing = true

IF severity == "HIGH" THEN:
  flag_ac_as_failing = true

IF severity == "MEDIUM" THEN:
  add_warning_only = true
```

### Detailed Flagging Decision Logic

```
violations = collect_all_violations(source_files)

critical_count = count(violations WHERE severity == "CRITICAL")
high_count = count(violations WHERE severity == "HIGH")
medium_count = count(violations WHERE severity == "MEDIUM")

IF critical_count > 0 OR high_count > 0:
  ac_status = "POTENTIALLY_FAILING"
  blocking_violations = filter(violations, severity IN ["CRITICAL", "HIGH"])
  flag_message = f"AC flagged: {critical_count} CRITICAL, {high_count} HIGH violations"
ELSE:
  ac_status = "CLEAN" (or previous status)
  IF medium_count > 0:
    warnings = filter(violations, severity == "MEDIUM")
    warning_message = f"Non-blocking: {medium_count} MEDIUM severity issues"
```

### Aggregation Logic

```
# Aggregate violations from all inspected files
anti_pattern_results = {
  "total_violations": len(violations),
  "by_severity": {
    "CRITICAL": critical_count,
    "HIGH": high_count,
    "MEDIUM": medium_count
  },
  "blocking": critical_count + high_count > 0,
  "violations": violations
}
```

---

## Anti-Pattern Categories

The anti-patterns.md file defines 10 categories to check:

| # | Category | Severity | Detection Method |
|---|----------|----------|------------------|
| 1 | Tool Usage Violations | CRITICAL | Check for Bash file operations instead of native tools |
| 2 | Monolithic Components | HIGH | Check for files exceeding size limits |
| 3 | Assumptions | CRITICAL | Check for technology choices without AskUserQuestion |
| 4 | Size Violations | HIGH | Check component line counts against limits |
| 5 | Language-Specific Code | CRITICAL | Check for executable code in framework files |
| 6 | Context File Violations | CRITICAL | Check for proceeding without reading context files |
| 7 | Circular Dependencies | HIGH | Check for skills calling each other in loops |
| 8 | Narrative Documentation | MEDIUM | Check for prose instead of direct instructions |
| 9 | Missing Frontmatter | HIGH | Check for missing YAML frontmatter in components |
| 10 | Hardcoded Paths | MEDIUM | Check for absolute paths instead of relative |

---

## Detection Patterns by Category

**Category 1: Tool Usage Violations (CRITICAL)**
```
# Detect Bash for file operations
Grep(pattern="Bash\(command.*cat |Bash\(command.*echo.*>|Bash\(command.*find ", path="{source_file}")
```

**Category 2: Monolithic Components (HIGH)**
```
# Check file size (>1000 lines for skills, >500 for commands)
line_count = count_lines(source_file)
IF line_count > threshold: flag_violation
```

**Category 3: Assumptions (CRITICAL)**
```
# Detect technology assumptions without AskUserQuestion
Grep(pattern="[Ii]nstall.*Redis|[Uu]se.*EF Core|[Aa]dd.*npm", path="{source_file}")
# Then verify AskUserQuestion was used
```

**Category 4: Size Violations (HIGH)**
```
# Check against tech-stack.md limits
# Skills: max 1000 lines
# Commands: max 500 lines
# Subagents: max 500 lines
```

**Category 5: Language-Specific Code (CRITICAL)**
```
# Detect executable code in framework components
Grep(pattern="def |function |class .*\{|import .* from", path="{source_file}")
# In .claude/skills/ or .claude/agents/ directories
```

**Category 6: Context File Violations (CRITICAL)**
```
# Detect implementation without reading context files
Grep(pattern="Read\(file_path.*context/tech-stack\.md", path="{source_file}")
# If missing in development workflow files
```

**Category 7: Circular Dependencies (HIGH)**
```
# Detect skill A calling skill B calling skill A
Grep(pattern="Skill\(command=", path="{source_file}")
# Build dependency graph, check for cycles
```

**Category 8: Narrative Documentation (MEDIUM)**
```
# Detect prose instead of instructions
Grep(pattern="should first|might want to|could consider", path="{source_file}")
```

**Category 9: Missing Frontmatter (HIGH)**
```
# Check for YAML frontmatter in skills/subagents/commands
Grep(pattern="^---$", path="{source_file}")
# First line should start frontmatter
```

**Category 10: Hardcoded Paths (MEDIUM)**
```
# Detect absolute paths
Grep(pattern="/home/|/Users/|C:\\\\|/mnt/c/", path="{source_file}")
```

---

## AntiPatternViolation Data Model

```json
{
  "category": "Tool Usage Violations",
  "severity": "CRITICAL",
  "file_path": ".claude/skills/implementing-stories/SKILL.md",
  "line_number": 145,
  "description": "Using Bash(command='cat file.txt') instead of Read() tool",
  "remediation": "Replace with Read(file_path='file.txt')"
}
```

**Field Specifications:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `category` | String | **Yes** | Must match one of 10 defined categories |
| `severity` | Enum | **Yes** | One of: `CRITICAL`, `HIGH`, `MEDIUM` |
| `file_path` | String | **Yes** | Relative path from project root |
| `line_number` | Integer | No | Positive integer if detected |
| `description` | String | **Yes** | Human-readable violation description |
| `remediation` | String | No | Suggested fix if available |

---

**Version:** 1.0
**Extracted from:** ac-compliance-verifier.md (STORY-334)
