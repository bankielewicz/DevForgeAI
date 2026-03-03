# YAML Frontmatter Specification

**Purpose:** Validation rules and patterns for subagent YAML frontmatter.

---

## Required Fields

### 1. name (REQUIRED)

**Format:** `lowercase-with-hyphens`

**Rules:**
- Must be lowercase
- Words separated by hyphens (not underscores)
- Must match filename (without .md extension)
- Pattern: `[domain]-[role]`

**Valid Examples:**
- `test-automator`
- `backend-architect`
- `deployment-engineer`
- `code-reviewer`

**Invalid Examples:**
- `TestAutomator` (CamelCase not allowed)
- `test_automator` (underscores not allowed)
- `BACKEND-ARCHITECT` (uppercase not allowed)

### 2. description (REQUIRED)

**Format:** Natural language, 50-200 characters

**Pattern:** `[Domain expertise]. Use proactively when [trigger conditions]. [Additional context]`

**Rules:**
- Must include "proactively" for auto-invoked subagents
- Should include invocation triggers
- Should describe domain expertise
- Must be concise (fit on one line)

**Valid Examples:**
```yaml
description: Test generation expert specializing in Test-Driven Development (TDD). Use proactively when implementing features requiring test coverage.

description: Backend implementation expert specializing in clean architecture. Use proactively when implementing service layers, repositories, or domain logic.

description: QA validation specialist for anti-pattern detection. Use proactively during code review and QA validation phases.
```

**Invalid Examples:**
```yaml
description: This subagent handles testing.  # Too vague, no triggers

description: Use this for tests.  # No domain expertise, too short
```

### 3. tools (REQUIRED)

**Format:** Comma-separated list of tool names

**Available Tools:**
- **File Operations:** Read, Write, Edit, Glob, Grep
- **Terminal:** Bash (with scope patterns)
- **AI:** Skill, AskUserQuestion
- **Web:** WebFetch, WebSearch

**Rules:**
- Use principle of least privilege (minimum required tools)
- NEVER use Bash for file operations
- Bash must include scope patterns: `Bash(git:*)`, `Bash(npm:*)`

**Valid Examples:**
```yaml
tools: Read, Write, Edit, Grep, Glob

tools: Read, Grep, Glob, Bash(git:*)

tools: Read, Write, Bash(pytest:*), Bash(npm:test)
```

**Invalid Examples:**
```yaml
tools: Read, cat, grep  # cat and grep are Bash commands

tools: Bash  # No scope pattern

tools: *  # Wildcard not allowed
```

### 4. model (REQUIRED)

**Format:** One of `haiku`, `sonnet`, `opus`, or `inherit`

**Selection Guidelines:**

| Model | Use When | Token Estimate |
|-------|----------|---------------|
| `haiku` | Simple, deterministic tasks | < 10K tokens |
| `sonnet` | Complex reasoning, code generation | 10-50K tokens |
| `opus` | Maximum capability, extremely complex | > 50K tokens |
| `inherit` | Match main conversation model | Varies |

**Valid Examples:**
```yaml
model: haiku    # For validation, formatting, simple parsing
model: sonnet   # For code generation, architecture review
model: inherit  # For adaptive behavior
```

---

## Optional Fields

### color (OPTIONAL)

**Format:** Valid CSS color name

**Purpose:** Visual distinction in UI

**Examples:**
```yaml
color: green
color: blue
color: orange
```

---

## Complete Frontmatter Examples

### Simple Validator Subagent
```yaml
---
name: context-validator
description: Context file constraint enforcement expert. Use proactively before every git commit and during QA validation.
tools: Read, Grep, Glob
model: haiku
---
```

### Complex Code Generator
```yaml
---
name: backend-architect
description: Backend implementation expert specializing in clean architecture, domain-driven design, and layered architecture patterns. Use proactively during TDD Green phase.
tools: Read, Write, Edit, Grep, Glob, Bash(git:*)
model: sonnet
---
```

### Decision-Making Subagent
```yaml
---
name: architect-reviewer
description: Software architecture review specialist. Use proactively after ADRs created, when architecture decisions need validation.
tools: Read, Grep, Glob, WebFetch, AskUserQuestion
model: sonnet
---
```

---

## Validation Checklist

Before writing subagent file, verify:

- [ ] `name` field present and matches filename
- [ ] `name` uses lowercase-with-hyphens format
- [ ] `description` includes domain expertise
- [ ] `description` includes "proactively" if auto-invoked
- [ ] `tools` lists only required tools (minimum access)
- [ ] `tools` uses native tools for file operations
- [ ] `model` appropriate for task complexity
- [ ] YAML frontmatter properly delimited with `---`
- [ ] No syntax errors in YAML

---

## Common Validation Errors

### Error: Invalid YAML Syntax

**Symptoms:**
- Parser errors when loading subagent
- Missing frontmatter in Claude Code

**Common Causes:**
```yaml
# Wrong: Missing closing delimiter
---
name: test-automator
description: Test expert

# Wrong: Unescaped special characters
---
name: test-automator
description: Use for "complex" tests  # Quotes need escaping

# Wrong: Inconsistent indentation
---
name: test-automator
  description: Test expert  # Unexpected indent
```

**Correct Format:**
```yaml
---
name: test-automator
description: Use for complex tests or \"quoted\" content
tools: Read, Write
model: sonnet
---
```

### Error: Name Mismatch

**Symptoms:**
- Subagent not found when invoked
- Different name in `/agents` list

**Fix:**
- Ensure `name` field exactly matches filename (without .md)
- Example: `test-automator.md` must have `name: test-automator`

### Error: Missing Proactive Trigger

**Symptoms:**
- Subagent not auto-invoked when expected

**Fix:**
- Include "proactively" in description
- Document trigger conditions clearly
- Example: "Use proactively when [condition]"
