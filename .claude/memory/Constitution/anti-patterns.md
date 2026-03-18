# Anti-Patterns - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2026-02-05
**Version**: 1.1

## Framework Anti-Patterns

### Category 1: Tool Usage Violations (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Using Bash for File Operations**

**Wrong**:
```markdown
Bash(command="cat story.md")
Bash(command="echo 'content' > file.md")
Bash(command="find . -name '*.md'")
```

**Correct**:
```markdown
Read(file_path="story.md")
Write(file_path="file.md", content="content")
Glob(pattern="**/*.md")
```

**Rationale**: 40-73% token efficiency gain with native tools.

### Category 2: Monolithic Components (SEVERITY: HIGH)

❌ **FORBIDDEN: All-in-One Skill**

**Wrong**:
```
.claude/skills/devforgeai-everything/
└── SKILL.md (5,000 lines doing ideation + architecture + dev + qa + release)
```

**Correct**:
```
.claude/skills/
├── spec-driven-ideation/
├── designing-architecture/
├── spec-driven-dev/
├── validating-quality/
└── releasing-stories/
```

**Rationale**: Modularity enables independent updates and token efficiency.

### Category 3: Making Assumptions (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Assuming Technology Choices**

**Wrong**:
```markdown
# AI sees "need caching" and adds Redis without asking
Install Redis for caching layer
```

**Correct**:
```markdown
Question: "Spec requires caching. Which technology?"
Header: "Caching"
Options:
  - "Redis (in-memory, distributed)"
  - "Memcached (simple, fast)"
  - "In-memory (no external service)"
multiSelect: false
```

**Rationale**: Assumptions cause technical debt.

### Category 4: Size Violations (SEVERITY: HIGH)

❌ **FORBIDDEN: Exceeding Component Size Limits**

**Wrong**:
```markdown
# SKILL.md with 2,000 lines of inline documentation
```

**Correct**:
```markdown
# SKILL.md with 500 lines + references/ for deep docs
For detailed scoring rubric, see references/complexity-assessment-matrix.md
```

**Rationale**: Character budget constraints (15K for commands).

### Category 5: Language-Specific Framework Code (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Python/C#/JavaScript in Framework**

**Wrong**:
```
.claude/skills/spec-driven-dev/
├── SKILL.md
└── scripts/
    └── implement.py    # Python implementation
```

**Correct**:
```
.claude/skills/spec-driven-dev/
├── SKILL.md
└── references/
    └── tdd-workflow-guide.md    # Documentation only
```

**Rationale**: Framework must be language-agnostic.

### Category 6: Context File Violations (SEVERITY: CRITICAL)

❌ **FORBIDDEN: Proceeding Without Context Files**

**Wrong**:
```markdown
# Development skill starts implementation without reading context
Implement feature X using EF Core
```

**Correct**:
```markdown
## Phase 1: Context Validation
Read all 6 context files
HALT if missing: "Run /create-context first"
Check tech-stack.md for ORM choice
```

**Rationale**: Context files prevent architectural violations.

### Category 7: Circular Dependencies (SEVERITY: HIGH)

❌ **FORBIDDEN: Skills Calling Each Other in Loops**

**Wrong**:
```
spec-driven-dev calls validating-quality
  ↓
validating-quality calls spec-driven-dev
  ↓
Infinite loop
```

**Correct**:
```
spec-driven-dev calls validating-quality (one-way)
validating-quality returns results
spec-driven-dev continues
```

**Rationale**: Prevents infinite loops and context overflow.

### Category 8: Narrative Documentation (SEVERITY: MEDIUM)

❌ **FORBIDDEN: Prose Instead of Instructions**

**Wrong**:
```markdown
The system should first analyze the codebase, and then it might want to consider generating tests...
```

**Correct**:
```markdown
1. Analyze codebase:
   - Grep(pattern="class.*Test", glob="**/*.cs")
2. Generate tests:
   - Use test-automator subagent
```

**Rationale**: Direct instructions are clearer for Claude.

### Category 9: Missing Frontmatter (SEVERITY: HIGH)

❌ **FORBIDDEN: Skills/Subagents/Commands Without Frontmatter**

**Wrong**:
```markdown
# My Skill
Instructions go here...
```

**Correct**:
```markdown
---
name: my-skill
description: Brief description of when to use
tools: Read, Write
---

# My Skill
Instructions go here...
```

**Rationale**: Frontmatter required for discovery.

### Category 10: Hardcoded Paths (SEVERITY: MEDIUM)

❌ **FORBIDDEN: Hardcoded File Paths**

**Wrong**:
```markdown
Read(file_path="/home/user/project/story.md")
```

**Correct**:
```markdown
Read(file_path="devforgeai/specs/Stories/$STORY_ID.md")
```

**Rationale**: Relative paths work across environments.

### Category 11: Code Search Tool Selection (SEVERITY: MEDIUM)

**Treelint-Supported Languages:** Python (`.py`), TypeScript (`.ts`, `.tsx`), JavaScript (`.js`, `.jsx`), Rust (`.rs`), Markdown (`.md`)

**Grep is Correct for:** Unsupported languages, simple text-pattern searches (TODOs, string literals), fallback when Treelint is unavailable.

❌ **FORBIDDEN: Using Treelint for Unsupported File Types**

**Wrong**:
```markdown
# Treelint does not support C#, Java, Go, SQL - returns errors
Bash(command="treelint search --type function myfile.cs")
Bash(command="treelint search --type class MyClass.java")
Bash(command="treelint deps --calls project.go")
```

**Correct**:
```markdown
# Use Grep for unsupported languages
Grep(pattern="class\\s+\\w+", glob="**/*.cs")
Grep(pattern="public\\s+void", glob="**/*.java")
Grep(pattern="func\\s+\\w+", glob="**/*.go")
```

**Rationale**: Treelint returns errors for unsupported file types, wasting tokens on error responses instead of useful results.

❌ **FORBIDDEN: Using Grep When Treelint Available for Supported Languages**

**Wrong**:
```markdown
# Using Grep for semantic code search in Treelint-supported languages
Grep(pattern="def\\s+validate", glob="**/*.py")
Grep(pattern="function\\s+handle", glob="**/*.ts")
Grep(pattern="class\\s+Service", glob="**/*.js")
```

**Correct**:
```markdown
# Use Treelint for semantic AST-aware search
Bash(command="treelint search --type function --name 'validate*' --format json")
Bash(command="treelint search --type class --name 'Service*' --format json")
Bash(command="treelint deps --calls --format json")
```

**Rationale**: Treelint provides 99.93% token reduction vs Grep for semantic code search (Source: ADR-013, RESEARCH-007). AST-aware search eliminates false positives from comments, strings, and partial matches. Grep remains valid for simple text patterns (TODOs, string literals) even in supported languages, and as fallback when Treelint is unavailable.

## Anti-Pattern Detection Protocol

When framework components detect anti-patterns:

1. **HALT immediately**
2. **Report specific violation** with file:line reference
3. **Provide correction example**
4. **Request user confirmation** before proceeding

## Enforcement Checklist

Before committing framework changes:
- [ ] No Bash for file operations (use Read/Write/Edit/Glob/Grep)
- [ ] Components within size limits (skills <1000, commands <500)
- [ ] No language-specific code in framework
- [ ] All ambiguities use AskUserQuestion
- [ ] Context files read before development
- [ ] No circular dependencies
- [ ] Direct instructions, not narrative prose
- [ ] All components have frontmatter
- [ ] No hardcoded absolute paths
- [ ] Code search tool selection correct (Treelint for supported languages, Grep for unsupported)

---

**REMEMBER**: Projects using DevForgeAI will have their own anti-patterns.md with project-specific forbidden patterns (SQL injection, N+1 queries, God objects, etc.).
