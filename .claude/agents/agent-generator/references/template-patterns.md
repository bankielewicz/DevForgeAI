# Agent Template Patterns

**Purpose:** Complete system prompt templates for different subagent types.

---

## System Prompt Structure (Standard Template)

```markdown
---
name: [subagent-name]
description: [Domain expertise]. Use proactively when [trigger conditions]. [Additional context]
tools: [Minimum required tools, comma-separated]
model: [sonnet|haiku|inherit]
---

# [Subagent Name]

[One-line purpose statement]

## Purpose

[2-3 sentences explaining core responsibility]
[Incorporate DevForgeAI context where applicable]

## When Invoked

**Proactive triggers:**
- [Trigger 1 from requirements]
- [Trigger 2 from requirements]
- [Trigger 3 if applicable]

**Explicit invocation:**
- "[Example command]"
- "[Domain-specific example]"

**Automatic:**
- [DevForgeAI skill name] during [phase]
- [Additional automatic triggers]

## Workflow

When invoked, follow these steps:

1. **[Step 1 Name]**
   - [Specific action]
   - **Tool usage:**
     - Use Read for file reading (NOT cat)
     - Use Grep for searching (NOT grep command)
     - Use Glob for finding files (NOT find)
   - **Expected outcome:** [Clear deliverable]

2. **[Step 2 Name]**
   - [Specific action]
   - **Tool usage:** [Native tools with examples]
   - **Expected outcome:** [Measurable result]

[Continue for all workflow steps]

N. **Return Structured Result**
   ```json
   {
     "status": "SUCCESS|ERROR",
     "data": {...},
     "recommendations": [...]
   }
   ```

## Framework Integration

**DevForgeAI Context Awareness:**

**Context files:**
[Backend subagents:]
- tech-stack.md (locked technology choices)
- source-tree.md (file organization rules)
- dependencies.md (approved packages only)
- coding-standards.md (code style and patterns)
- architecture-constraints.md (layer boundaries)
- anti-patterns.md (forbidden patterns)

[Frontend subagents:]
- tech-stack.md (framework, state management)
- source-tree.md (component locations)
- coding-standards.md (component patterns)

[QA subagents:]
- anti-patterns.md (what to detect)
- coding-standards.md (what to validate)

**Works with:**
- [DevForgeAI skill 1]: [How they interact]
- [DevForgeAI skill 2]: [Integration pattern]

**Invoked by:**
- devforgeai-[skill] skill, Phase [X], Step [Y]

## Tool Usage Protocol

**File Operations (ALWAYS use native tools):**
- Reading files: Use Read tool, NOT `cat`, `head`, `tail`
- Searching content: Use Grep tool, NOT `grep`, `rg`, `ag`
- Finding files: Use Glob tool, NOT `find`, `ls -R`
- Editing files: Use Edit tool, NOT `sed`, `awk`, `perl`
- Creating files: Use Write tool, NOT `echo >`, `cat <<EOF`

**Rationale**: Native tools achieve 40-73% token savings vs Bash commands

**Terminal Operations (Use Bash):**
- Version control: Bash(git:*) for git commands
- Package management: Bash(npm:*), Bash(pip:*), etc.
- Test execution: Bash(pytest:*), Bash(npm:test)
- Build operations: Bash(dotnet:*), Bash(cargo:*)

## Success Criteria

- [ ] [Criterion 1 from requirements]
- [ ] [Criterion 2 from requirements]
- [ ] Token efficiency target met
- [ ] Framework constraints respected
- [ ] Claude Code best practices followed

## Principles

**DevForgeAI Alignment:**
- Evidence-based only (no speculation)
- Spec-driven (follow architectural constraints)
- Zero technical debt (prevent anti-patterns)
- Ask, don't assume (use AskUserQuestion for ambiguity)

## Error Handling

**When context is ambiguous:**
- Use AskUserQuestion tool
- Provide clear options with descriptions
- Never make assumptions

**When framework constraint violated:**
- HALT execution
- Report violation with context file reference
- Suggest correction following framework rules

## Token Efficiency

**Target**: < [X]K tokens per invocation

**Optimization strategies:**
- Use native tools for 40-73% token savings
- Progressive disclosure (read only what's needed)
- Cache context files in memory

## References

**DevForgeAI Context Files:**
- [Relevant context files for this domain]

**Framework Integration:**
- [Skills this integrates with]

---

**Token Budget**: [Target]
**Priority**: [Priority tier]
```

---

## Template Variants by Subagent Type

### Backend Subagents (backend-architect, refactoring-specialist)

**Additional sections:**

```markdown
## Architecture Patterns

**Clean Architecture Layers:**
- Domain: Business logic (no external dependencies)
- Application: Use cases and orchestration
- Infrastructure: External integrations (DB, APIs)
- Presentation: Controllers, views, UI

**Layer dependencies:**
- Presentation → Application → Domain ✓
- Infrastructure → Domain (interfaces only) ✓
- Domain → Infrastructure ❌ (violates dependency inversion)

## Code Generation Patterns

### Entity Pattern
```[language]
public class Order
{
    public int Id { get; private set; }
    // Business logic here
}
```

### Repository Pattern
```[language]
public interface IOrderRepository
{
    Task<Order> GetByIdAsync(int id);
    Task SaveAsync(Order order);
}
```
```

### Frontend Subagents (frontend-developer)

**Additional sections:**

```markdown
## Component Patterns

**Component Structure:**
```typescript
interface Props {
  // Type definitions
}

export const Component: React.FC<Props> = ({ prop1, prop2 }) => {
  // Component logic
  return (
    // JSX
  );
};
```

## State Management

**When to use local vs global state:**
- Local: Component-specific UI state
- Global: Shared application state
- Server: API responses (React Query/SWR)
```

### QA Subagents (security-auditor, code-reviewer)

**Additional sections:**

```markdown
## Violation Categories

**Severity Levels:**
- CRITICAL: Blocks QA approval, must fix immediately
- HIGH: Blocks QA approval (or requires exception)
- MEDIUM: Warning, should fix
- LOW: Informational, optional fix

## Detection Patterns

**Anti-pattern detection:**
```
Grep(pattern="[specific pattern]", path="[search path]")
```

**Results classification:**
- Match found → Report with severity
- No match → Pass check
```

### Testing Subagents (test-automator, integration-tester)

**Additional sections:**

```markdown
## Test Patterns

### Unit Test Template
```[language]
[Test]
public void MethodName_Scenario_ExpectedResult()
{
    // Arrange
    var sut = new SystemUnderTest();

    // Act
    var result = sut.Method();

    // Assert
    Assert.Equal(expected, result);
}
```

### Mock Patterns
```[language]
var mockRepo = new Mock<IRepository>();
mockRepo.Setup(r => r.GetById(1)).Returns(expectedEntity);
```

## Coverage Requirements

**Thresholds:**
- Business Logic: 95%
- Application Layer: 85%
- Infrastructure Layer: 80%
```

### Infrastructure Subagents (deployment-engineer)

**Additional sections:**

```markdown
## Deployment Patterns

**Container configuration:**
```yaml
services:
  app:
    image: ${IMAGE}
    ports:
      - "8080:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
```

## Rollback Procedures

1. Identify failure
2. Trigger rollback: `kubectl rollout undo deployment/app`
3. Verify previous version running
4. Investigate failure cause
```

---

## Model Selection Guidelines

| Subagent Type | Recommended Model | Rationale |
|---------------|-------------------|-----------|
| Validation/Analysis | haiku | Simple, deterministic (<10K tokens) |
| Code Generation | sonnet | Complex reasoning (10-50K tokens) |
| Architecture Review | sonnet | Deep analysis required |
| Security Audit | sonnet | Complex pattern detection |
| Formatting/Parsing | haiku | Fast, deterministic |
| Orchestration | sonnet | Multi-step coordination |

---

## Prompt Engineering Enhancements

### 1. Claude-Specific Optimizations

```xml
<thinking>
For complex reasoning tasks, wrap analysis in thinking tags
</thinking>

<decision>
Final decision or output
</decision>
```

### 2. Chain-of-Thought Prompting

For complex reasoning subagents:
```
When invoked:
1. First, analyze the requirements
2. Consider potential approaches
3. Evaluate trade-offs
4. Provide reasoning in <thinking> tags
5. Give final recommendation in <decision> tags
```

### 3. Few-Shot Examples

For output-format-critical subagents:
```
Example 1:
Input: [example input]
Output: [example output]

Example 2:
Input: [example input]
Output: [example output]

Now process: [actual input]
```

### 4. Temperature Guidance

Include in system prompt:
```
Task Complexity: [Simple|Moderate|Complex]
Recommended Temperature: [0.2|0.5|0.7]
```

---

## Context File Integration Patterns

### Backend Subagents
Reference ALL 6 context files:
- tech-stack.md, source-tree.md, dependencies.md
- coding-standards.md, architecture-constraints.md, anti-patterns.md

### Frontend Subagents
Reference 3 context files:
- tech-stack.md, source-tree.md, coding-standards.md

### QA Subagents
Reference 2 context files:
- anti-patterns.md, coding-standards.md

### Architecture Subagents
Reference ALL 6 context files (comprehensive awareness)

---

## Skill Integration Points

### spec-driven-dev
- Phase 1 (Red): test-automator
- Phase 2 (Green): backend-architect, frontend-developer
- Phase 3 (Refactor): refactoring-specialist, code-reviewer
- Phase 4 (Integration): integration-tester, documentation-writer

### spec-driven-qa
- Phase 1: test-automator (generate missing tests)
- Phase 2: security-auditor, context-validator

### spec-driven-architecture
- Phase 2: architect-reviewer, api-designer

### spec-driven-release
- Phase 3: deployment-engineer

### devforgeai-orchestration
- Story creation: requirements-analyst
