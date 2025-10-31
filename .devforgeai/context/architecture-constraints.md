# Architecture Constraints - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-10-30
**Version**: 1.0

## Framework Architecture Patterns

### Three-Layer Architecture (LOCKED)

```
Layer 1: Skills (Framework Implementation)
   ↓ invokes
Layer 2: Subagents (Parallel Execution)
   ↓ uses
Layer 3: Slash Commands (User Workflows)
```

**Dependency Rules**:
- ✅ Commands can invoke Skills
- ✅ Commands can invoke Subagents via Task tool
- ✅ Skills can invoke other Skills
- ✅ Skills can invoke Subagents via Task tool
- ❌ Skills CANNOT invoke Commands
- ❌ Subagents CANNOT invoke Skills or Commands
- ❌ Circular dependencies forbidden (Skill A → Skill B → Skill A)

### Skill Design Constraints (LOCKED)

**Single Responsibility Principle**:
- Each skill handles ONE phase of development lifecycle
- ✅ devforgeai-development: TDD implementation only
- ✅ devforgeai-qa: Quality validation only
- ❌ devforgeai-dev-and-qa: Multiple responsibilities

**Context Isolation**:
- Each skill invocation has separate context window
- Skills MUST NOT assume state from previous invocations
- Skills MUST read context files explicitly

**Progressive Disclosure**:
- Main SKILL.md: Core instructions (<1000 lines)
- references/: Deep documentation (loaded on demand)
- MUST use "see references/[file].md" pattern

### Subagent Design Constraints (LOCKED)

**Domain Specialization**:
- Each subagent specialized in single domain
- ✅ test-automator: Test generation only
- ✅ backend-architect: Backend implementation only
- ❌ full-stack-developer: Too broad

**Tool Restrictions**:
- Principle of least privilege
- Only grant tools needed for subagent's domain
- Example: test-automator gets Read, Write, Edit, Bash (for running tests)
- Example: code-reviewer gets Read, Grep, Glob only (read-only)

**Parallel Execution Support**:
- Subagents MUST be designed for parallel invocation
- No shared state between subagents
- No dependencies between parallel subagents

### Command Design Constraints (LOCKED)

**User-Facing Workflows**:
- Commands orchestrate skills and subagents
- Commands provide user-friendly parameters
- Commands handle user ambiguity via AskUserQuestion

**Size Constraints**:
- Keep under 500 lines (<20K characters)
- If exceeding 500 lines → extract to skill

**Parameter Handling**:
- Use $ARGUMENTS for user input
- Provide argument-hint in frontmatter
- Validate parameters before processing

### Context File Enforcement (LOCKED)

**Immutability Principle**:
- Context files are THE LAW
- Development skill MUST read ALL 6 context files
- AI agents MUST follow constraints or HALT

**Validation Pattern**:
```markdown
## Phase 1: Context Validation
Read context files in PARALLEL:
- Read(file_path=".devforgeai/context/tech-stack.md")
- Read(file_path=".devforgeai/context/source-tree.md")
- Read(file_path=".devforgeai/context/dependencies.md")
- Read(file_path=".devforgeai/context/coding-standards.md")
- Read(file_path=".devforgeai/context/architecture-constraints.md")
- Read(file_path=".devforgeai/context/anti-patterns.md")

HALT if ANY file missing: "Context incomplete. Run /create-context"
```

### Quality Gate Pattern (LOCKED)

**Gate Enforcement**:
- Quality gates MUST block progression on violations
- Gates validated in sequence (no skipping)
- HALT pattern for gate failures

**Example**:
```markdown
HALT if tests fail: "Tests must pass before proceeding"
HALT if coverage < threshold: "Coverage below 95%/85%/80%"
HALT if CRITICAL violations: "Fix critical issues before release"
```

### Error Handling Pattern (LOCKED)

**AskUserQuestion for Ambiguity**:
```markdown
IF ambiguity detected:
  Use AskUserQuestion with specific options
  Document decision in context file or ADR
  Proceed with chosen option
```

**HALT for Constraint Violations**:
```markdown
IF constraint violated:
  HALT with clear error message
  Provide resolution steps
  Request user confirmation before retry
```

### Token Efficiency Pattern (LOCKED)

**Parallel Tool Invocation**:
```markdown
✅ CORRECT: Parallel reads
Read(file_path="file1.md")
Read(file_path="file2.md")
Read(file_path="file3.md")

❌ WRONG: Sequential narrative
First read file1, then read file2, then read file3...
```

**Native Tools Over Bash**:
- 40-73% token savings documented
- MUST use Read/Write/Edit/Glob/Grep instead of Bash equivalents

---

**REMEMBER**: Projects using DevForgeAI will have their own architecture-constraints.md defining layer boundaries, patterns, and design rules specific to their architecture (Clean Architecture, N-Tier, etc.).
