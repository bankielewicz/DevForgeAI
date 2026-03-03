# Tool Access Restrictions

**Purpose:** Tool selection patterns and principle of least privilege enforcement.

---

## Core Principle: Minimum Required Tools

Every subagent should have the **minimum tools necessary** to complete its task. This follows the principle of least privilege:

- **Reduces attack surface** - Fewer tools = fewer potential misuses
- **Improves token efficiency** - Less tool documentation loaded
- **Clarifies responsibility** - Clear boundaries on what subagent can do

---

## Tool Categories

### 1. File Operations (Native Tools - MANDATORY)

**ALWAYS use native tools for file operations:**

| Operation | Use This | NEVER Use |
|-----------|----------|-----------|
| Read files | `Read` | `cat`, `head`, `tail`, `less` |
| Search content | `Grep` | `grep`, `rg`, `ag`, `ack` |
| Find files | `Glob` | `find`, `ls -R`, `locate` |
| Edit files | `Edit` | `sed`, `awk`, `perl -i` |
| Create files | `Write` | `echo >`, `cat <<EOF`, `touch` |

**Rationale:** Native tools achieve **40-73% token savings** vs Bash commands:
- File read: 40% savings
- File search: 60% savings
- File find: 73% savings

### 2. Terminal Operations (Bash with Scope)

**Use Bash ONLY for terminal operations:**

| Operation | Bash Scope Pattern |
|-----------|-------------------|
| Git commands | `Bash(git:*)` |
| npm/Node.js | `Bash(npm:*)` |
| Python/pip | `Bash(pip:*)`, `Bash(pytest:*)` |
| .NET | `Bash(dotnet:*)` |
| Docker | `Bash(docker:*)` |
| Kubernetes | `Bash(kubectl:*)` |
| Terraform | `Bash(terraform:*)` |

**Invalid (no scope):**
```yaml
tools: Bash  # Wrong - no scope pattern
```

**Valid (with scope):**
```yaml
tools: Bash(git:*), Bash(npm:*)
```

### 3. AI Tools

| Tool | Purpose | When to Include |
|------|---------|-----------------|
| `Skill` | Invoke DevForgeAI skills | Orchestration subagents only |
| `AskUserQuestion` | Clarify ambiguity | All decision-making subagents |
| `Task` | Invoke other subagents | Orchestration subagents only |

### 4. Web Tools

| Tool | Purpose | When to Include |
|------|---------|-----------------|
| `WebFetch` | Fetch documentation | Research, architecture review |
| `WebSearch` | Search internet | Research, competitive analysis |

---

## Tool Access by Subagent Type

### Validation/Analysis Subagents (View-Only)

```yaml
tools: Read, Grep, Glob
```

**Examples:** context-validator, coverage-analyzer, anti-pattern-scanner

**Why:** Only needs to read and analyze, never modify

### Code Generation Subagents

```yaml
tools: Read, Write, Edit, Grep, Glob
```

**Examples:** backend-architect, frontend-developer, test-automator

**Why:** Needs to read existing code, write new code, edit files

### Testing Subagents

```yaml
tools: Read, Write, Edit, Grep, Glob, Bash(pytest:*|npm:test|dotnet:test)
```

**Examples:** test-automator, integration-tester

**Why:** Needs file operations plus test execution

### Deployment Subagents

```yaml
tools: Read, Write, Edit, Bash(docker:*), Bash(kubectl:*), Bash(terraform:*)
```

**Examples:** deployment-engineer

**Why:** Needs infrastructure command access

### Review Subagents

```yaml
tools: Read, Grep, Glob, Bash(git:*)
```

**Examples:** code-reviewer

**Why:** Needs read access plus git history

### Research Subagents

```yaml
tools: Read, Write, Edit, Grep, Glob, WebFetch, WebSearch
```

**Examples:** internet-sleuth, architect-reviewer

**Why:** Needs web access for research

---

## Forbidden Patterns

### 1. Bash for File Operations

**WRONG:**
```yaml
tools: Read, Bash(cat:*), Bash(grep:*)  # FORBIDDEN
```

**RIGHT:**
```yaml
tools: Read, Grep, Glob
```

### 2. Wildcard Bash Access

**WRONG:**
```yaml
tools: Bash  # No scope = unrestricted access
```

**RIGHT:**
```yaml
tools: Bash(git:*)  # Scoped access
```

### 3. Unnecessary Tools

**WRONG:**
```yaml
# Validator that only reads but has Write access
name: context-validator
tools: Read, Write, Edit, Grep, Glob  # Over-provisioned
```

**RIGHT:**
```yaml
name: context-validator
tools: Read, Grep, Glob  # Minimum required
```

### 4. Missing Required Tools

**WRONG:**
```yaml
# Code generator without Edit
name: backend-architect
tools: Read, Glob  # Can't modify code!
```

**RIGHT:**
```yaml
name: backend-architect
tools: Read, Write, Edit, Grep, Glob
```

---

## Tool Validation Checklist

Before finalizing tool list:

- [ ] All file operations use native tools (Read/Write/Edit/Grep/Glob)
- [ ] No Bash commands for file operations
- [ ] Bash has scope patterns (e.g., `Bash(git:*)`)
- [ ] Tools match subagent's responsibilities
- [ ] No unnecessary tools (principle of least privilege)
- [ ] AskUserQuestion included if decisions required
- [ ] Web tools only if research needed

---

## Common Tool Selection Mistakes

### Mistake 1: Over-Provisioning

**Problem:** Including tools "just in case"

**Example:**
```yaml
# Security auditor with Write access (shouldn't modify code)
tools: Read, Write, Edit, Grep, Glob  # Over-provisioned
```

**Fix:** Remove Write and Edit - auditor only reads and reports

### Mistake 2: Missing AskUserQuestion

**Problem:** Subagent makes autonomous decisions without user input

**Example:**
```yaml
# Architect makes decisions without asking
tools: Read, Write, Grep, Glob
```

**Fix:** Add AskUserQuestion for decision points

### Mistake 3: Using Bash for Portability

**Problem:** Thinking Bash commands are "more portable"

**Example:**
```yaml
tools: Bash(cat:*), Bash(grep:*)  # "Works on any system"
```

**Fix:** Native tools ARE the portable solution - use Read, Grep, Glob

---

## Tool Documentation Loading

Each tool in the frontmatter causes Claude to load its documentation. More tools = more tokens consumed before the subagent even starts working.

**Token Impact:**
- Each tool adds ~500-2000 tokens of documentation
- 10 tools = ~5-20K tokens just for tool docs
- Minimizing tools saves context window space

**Optimization:**
- List only required tools
- Group related Bash scopes: `Bash(git:*|npm:*)`
- Remove unused tools from older subagents
