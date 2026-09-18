---
parent: session-miner
topic: anti-pattern-mining
description: STORY-231 anti-pattern detection and violation tracking
---

# Anti-Pattern Mining (STORY-231)

**Purpose:** Detect, categorize, and track anti-pattern violations from session history.

---

## Purpose

Extract and analyze anti-pattern violations from SessionEntry data with:
- Pattern matching against anti-patterns.md rules (10 categories)
- Violation counting with AP-XXX codes and severity distribution
- Consequence tracking with error correlation analysis

---

## When Invoked

**Proactive triggers:**
- When analyzing anti-pattern frequency for EPIC-034
- When monitoring framework compliance
- When identifying high-risk patterns causing errors

**Explicit invocation:**
- "Mine anti-patterns from history.jsonl"
- "Detect framework violations from sessions"
- "Build anti-pattern violation registry"

---

## Data Model: AntiPatternViolation

Extends SessionEntry with anti-pattern-specific fields:

```yaml
AntiPatternViolation:
  # Inherited from SessionEntry
  timestamp: DateTime (ISO8601)
  session_id: UUID
  command: String
  user_input: String
  project: String

  # Anti-pattern-specific fields
  category:
    type: Enum
    values:
      - bash_for_file_ops
      - monolithic_components
      - making_assumptions
      - size_violations
      - language_specific_code
      - context_file_violations
      - circular_dependencies
      - narrative_documentation
      - missing_frontmatter
      - hardcoded_paths
    description: Classified anti-pattern category from anti-patterns.md

  category_id:
    type: Integer (1-10)
    description: Numeric category identifier matching anti-patterns.md

  severity:
    type: Enum (critical|high|medium|low)
    description: Impact severity level per category
    derived: true

  pattern_matched:
    type: String
    description: The specific pattern text that triggered detection
    extraction: Substring of user_input matching rule

  violation_code:
    type: String (AP-XXX format)
    description: Unique violation code for tracking
    derived: true
```

---

## AC#1: Anti-Pattern Matching

### Category Definition Reference (from anti-patterns.md)

| ID | Category | Severity | Primary Patterns | Exception Rules |
|----|----------|----------|---------|-----------------|
| 1 | bash_for_file_ops | critical | `cat`, `echo >`, `find`, `grep`, `sed` | npm test, git, docker, build, install |
| 2 | monolithic_components | high | `everything`, `all-in-one`, `ideation + architecture + dev` | None |
| 3 | making_assumptions | critical | `Install Redis`, `Use PostgreSQL`, `Build with React`, `Using EF Core` | Must check AskUserQuestion context |
| 4 | size_violations | high | `>1000 lines`, `>500 lines`, `2000 lines` | None |
| 5 | language_specific_code | critical | `.py` in skills/, `executable code` in docs | None |
| 6 | context_file_violations | critical | `without context`, `Proceeding without`, `skip context` | None |
| 7 | circular_dependencies | high | `A -> B -> A` invocation chains | None |
| 8 | narrative_documentation | medium | `should first`, `might want to`, `The system should` | None |
| 9 | missing_frontmatter | high | `no frontmatter`, `no YAML`, `missing ---` | None |
| 10 | hardcoded_paths | medium | `/home/user/`, `/Users/`, `C:\Users\` | None |

### Pattern Matching Algorithm

```
FUNCTION match_anti_patterns(user_input):
  violations = []
  input_normalized = normalize_input(user_input)

  FOR category_id in [1..10]:
    FOR pattern in PATTERNS[category_id]:
      IF pattern_matches(input_normalized, pattern):
        IF NOT is_legitimate_exception(user_input, category_id):
          violations.append({
            category: CATEGORY_NAME[category_id],
            category_id: category_id,
            severity: SEVERITY_MAP[category_id],
            pattern_matched: extract_matched_text(user_input, pattern)
          })

  RETURN violations

FUNCTION normalize_input(user_input):
  normalized = user_input.lower()
  IF len(normalized) > 10000:
    normalized = normalized[:10000]
  RETURN normalized
```

### Legitimate Bash Exceptions (NOT violations)

Category 1 (bash_for_file_ops) does NOT apply when Bash is used for:

| Pattern | Reason | Exception Rule |
|---------|--------|----------------|
| `Bash(command="npm test")` | Test execution | Contains `test` or `pytest` or `dotnet test` |
| `Bash(command="npm run build")` | Build execution | Contains `build` or `compile` |
| `Bash(command="git")` | Git operations | Starts with `git ` |
| `Bash(command="npm install")` | Package management | Contains `install` or `pip install` |
| `Bash(command="docker")` | Container operations | Starts with `docker ` |

### Exception Checking

```
FUNCTION is_legitimate_exception(user_input, category_id):
  # Only Category 1 has exceptions
  IF category_id != 1:
    RETURN false

  command = extract_bash_command(user_input).lower()

  # Allowed prefixes
  allowed_prefixes = ["git ", "docker ", "kubectl ", "npm ", "yarn ", "pnpm "]
  IF any(command.starts_with(prefix) for prefix in allowed_prefixes):
    RETURN true

  # Allowed keywords
  allowed_keywords = ["test", "build", "install", "publish", "deploy"]
  IF any(keyword in command for keyword in allowed_keywords):
    RETURN true

  RETURN false
```

### Multi-Violation Detection

A single entry can trigger multiple violations:

```
Example: Bash(command="cat /home/user/file.md")

Violations detected:
  1. Category 1 (bash_for_file_ops) - Bash cat command
  2. Category 10 (hardcoded_paths) - /home/user/ absolute path

Both violations counted separately with unique entries.
```

---

## AC#2: Violation Counting

### Severity Distribution

Map categories to severity levels:

```
Severity Mapping:
  critical = Categories: 1, 3, 5, 6
  high = Categories: 2, 4, 7, 9
  medium = Categories: 8, 10
  low = (none)
```

### Violation Code (AP-XXX) Assignment

```
violation_code = "AP-" + sprintf("%03d", category_id)

Code Mapping:
  AP-001 = bash_for_file_ops (critical)
  AP-002 = monolithic_components (high)
  AP-003 = making_assumptions (critical)
  AP-004 = size_violations (high)
  AP-005 = language_specific_code (critical)
  AP-006 = context_file_violations (critical)
  AP-007 = circular_dependencies (high)
  AP-008 = narrative_documentation (medium)
  AP-009 = missing_frontmatter (high)
  AP-010 = hardcoded_paths (medium)
```

### Violation Rate Calculation

```
violation_rate = total_violations / total_entries

Example:
  total_entries = 8
  total_violations = 7
  violation_rate = 7 / 8 = 0.875
```

---

## AC#3: Consequence Tracking

### Correlation Analysis Workflow

```
Input: AntiPatternViolation[] + ErrorEntry[] (from STORY-229)
  |
Group both by session_id
  |
For each session:
  Sort violations and errors by timestamp
  |
  For each violation:
    Find subsequent error in same session
    Check temporal proximity (<10 minutes)
    |
    If found: Mark as correlated
  |
Calculate correlation_rate
  |
Identify high_risk_patterns (>50% correlation)
  |
Output: ConsequenceCorrelation report
```

### Session-Scoped Correlation

Correlations are ONLY detected within the same session:

```
RULE: Violation in session A does NOT correlate with error in session B

Example (CORRELATED):
  Session abc123:
    Entry 1: Violation (Bash cat) at 10:30:00
    Entry 2: Error (File not found) at 10:31:00
  -> Correlation detected

Example (NOT CORRELATED):
  Session abc123:
    Entry 1: Violation (Bash cat) at 10:30:00
  Session def456:
    Entry 2: Error (File not found) at 10:31:00
  -> No correlation (different sessions)
```

### Temporal Proximity Check

```
FUNCTION check_temporal_proximity(violation, error):
  # Violation must precede error
  IF violation.timestamp >= error.timestamp:
    RETURN false

  # Within 10-minute window (600000ms)
  time_delta_ms = error.timestamp - violation.timestamp
  IF time_delta_ms > 600000:
    RETURN false

  RETURN true
```

### Correlation Detection Algorithm

```
FUNCTION find_correlations(violations, errors):
  correlations = []

  sessions_violations = group_by_session_id(violations)
  sessions_errors = group_by_session_id(errors)

  FOR session_id, violations_in_session in sessions_violations:
    errors_in_session = sessions_errors.get(session_id, [])
    IF len(errors_in_session) == 0:
      CONTINUE

    violations_in_session.sort(by="timestamp")
    errors_in_session.sort(by="timestamp")

    FOR violation in violations_in_session:
      FOR error in errors_in_session:
        IF error.timestamp > violation.timestamp AND
           (error.timestamp - violation.timestamp) <= 600000:
          correlations.append({
            violation: violation,
            error: error,
            time_delta_ms: error.timestamp - violation.timestamp,
            session_id: session_id
          })
          BREAK

  RETURN correlations
```

### High-Risk Pattern Identification

```
FUNCTION identify_high_risk_patterns(violations, correlations):
  category_total = {}
  category_correlated = {}

  FOR violation in violations:
    category = violation.category
    category_total[category] = category_total.get(category, 0) + 1
    category_correlated[category] = category_correlated.get(category, 0)

  FOR correlation in correlations:
    category = correlation.violation.category
    category_correlated[category] += 1

  high_risk = []
  FOR category, total in category_total:
    correlated = category_correlated[category]
    rate = correlated / total
    IF rate > 0.50:
      high_risk.append({
        category: category,
        violation_code: violation_code_for_category(category),
        correlation_rate: rate,
        sample_size: total
      })

  RETURN high_risk.sort_by("correlation_rate", descending=true)
```

---

## Anti-Pattern Analysis Pipeline

**Complete Workflow (7 Steps):**

```
Input: SessionEntry[] from history.jsonl
  |
[1] Filter entries with user_input field
[2] Apply anti-pattern matching rules (AC#1 - 10 categories)
[3] Aggregate violation counts and codes (AC#2)
[4] Load error entries (from STORY-229 ErrorEntry[])
[5] Correlate violations with errors (AC#3 - session-scoped)
[6] Identify high-risk patterns (>50% correlation)
[7] Generate AntiPatternAnalysisReport
  |
Output: Violations, distributions, correlations, registry
```

---

## Edge Case Handling

| Case | Handling |
|------|----------|
| Empty session file | Return empty violations array, totals at 0 |
| All entries have violations | Process all, violation_rate approaches 1.00 |
| No errors in session | correlation_rate = 0.00, empty high_risk_patterns |
| Legitimate Bash usage | Apply exception rules, NOT flagged as violation |
| Multiple violations per entry | Each violation counted separately |
| Very long user_input (>10000) | Truncate before pattern matching |
| Unicode content | Preserve encoding, case-insensitive matching |
| Bash in quotes (documentation) | Context-aware matching, NOT flagged |
| Missing user_input field | Skip entry for anti-pattern analysis |

---

## Core Helper Functions

```
FUNCTION group_by_session_id(entries):
  # Partition entries into groups by session_id
  # Entries with null session_id grouped together
  RETURN Map<session_id, Entry[]>

FUNCTION extract_bash_command(user_input):
  # Extract command text from Bash(command="...") pattern
  RETURN command_string

FUNCTION extract_matched_text(user_input, pattern):
  # Return substring of user_input that matched pattern
  RETURN matched_substring

FUNCTION violation_code_for_category(category_name):
  # Map category name to AP-XXX code
  RETURN "AP-" + sprintf("%03d", category_id)
```

---

## Invocation Template

```markdown
Task(
  subagent_type="session-miner",
  description="Analyze anti-patterns from session history",
  prompt="""
  Perform anti-pattern analysis on history.jsonl:

  1. Parse history with session-miner (offset=0, limit=1000)
  2. Apply anti-pattern matching rules (10 categories)
  3. Aggregate violation counts and codes
  4. Load error entries (STORY-229)
  5. Correlate violations with subsequent errors
  6. Identify high-risk patterns (>50% correlation)
  7. Generate anti-pattern analysis report

  Return AntiPatternAnalysisReport with recommendations.
  """
)
```

---

## Success Criteria (STORY-231)

**Functional Requirements:**
- [ ] Match all 10 anti-pattern categories
- [ ] Apply legitimate Bash exceptions (npm test, git, docker, build, install)
- [ ] Count violations per category with category_distribution
- [ ] Assign AP-XXX codes using formula
- [ ] Calculate violation_rate and severity_distribution
- [ ] Correlate violations with errors within 10-minute window
- [ ] Identify high-risk patterns with >50% error correlation
- [ ] Session-scoped correlation (no cross-session)

**Non-Functional Requirements:**
- [ ] Case-insensitive pattern matching
- [ ] Handle multiple violations per entry
- [ ] Truncate inputs >10000 chars
- [ ] Context-aware matching (avoid false positives)
- [ ] Preserve Unicode content
- [ ] Graceful error handling

**Integration Requirements:**
- [ ] Reuse ErrorEntry from STORY-229 for correlation
- [ ] Use same session_id grouping logic
- [ ] Compatible JSON output format
- [ ] Extends session-miner pipeline
