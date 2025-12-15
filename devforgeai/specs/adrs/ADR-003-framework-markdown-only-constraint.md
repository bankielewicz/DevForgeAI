# ADR-003: Framework Must Remain Markdown-Only (No Executable Code)

**Date:** 2025-11-18
**Status:** ACCEPTED
**Context:** STORY-040 Implementation Review
**Related Issues:** None
**Affected Stories:** STORY-040 (devforgeai-documentation skill)

---

## Decision

**The DevForgeAI framework must remain 100% Markdown-based with zero executable code.**

Executable Python/JavaScript/C# code must NOT be added to the framework repository. All functionality must be implemented as:
- **Skills** (Markdown files in `.claude/skills/`)
- **Subagents** (Markdown files in `.claude/agents/`)
- **Commands** (Markdown files in `.claude/commands/`)
- **Reference files** (Markdown documentation in skill `references/` directories)

---

## Context

During STORY-040 (DevForgeAI Documentation Skill) implementation, a Python module (`devforgeai_documentation/`) was created containing 1,912 lines of executable code across 4 Python files.

**Context-validator identified 7 constraint violations:**

1. **CRITICAL**: `anti-patterns.md` § 5 - "Language-specific code in Framework forbidden"
2. **CRITICAL**: `source-tree.md` § .claude/ - "Framework files are Markdown only"
3. **CRITICAL**: `tech-stack.md` § Documentation Format - "Markdown only, no executable code"
4. **MAJOR**: `dependencies.md` - "Framework has zero external dependencies"
5. **MAJOR**: `architecture-constraints.md` - "Skills-based architecture, not code-based"
6. **MINOR**: `coding-standards.md` - Missing documentation of purpose
7. **MINOR**: `architecture-constraints.md` - No test verification

---

## Rationale

### 1. Framework Design Principle: Documentation-as-Code

DevForgeAI framework operates as **metadata and instructions for Claude Code Terminal**, not as executable code. This design has critical benefits:

**Benefit 1: Language Agnostic**
- Framework works with Python, Node.js, C#, Go, Java, Rust, etc.
- Adding Python code breaks language agnosticism
- Projects using DevForgeAI specify their own technology stack
- Framework must not impose a language

**Benefit 2: Terminal-Native Execution**
- Skills execute in Claude Code Terminal (not as separate Python processes)
- Terminal calls tools (bash, Read, Write, Edit, Glob, Grep)
- Terminal doesn't execute embedded Python
- Architecture violates if Python runs independently of terminal

**Benefit 3: Maintainability**
- Markdown is version-control friendly (clear diffs, merge strategies)
- Code requires testing framework, CI/CD, dependencies management
- Framework growth becomes unbounded (each skill adds code + tests + deps)
- Markdown scales to 100+ skills without infrastructure overhead

**Benefit 4: Security**
- Framework code is visible to user (no black boxes)
- Users can read and audit instructions (Markdown is human-readable)
- Executable code creates trust questions (what does it actually do?)
- Transparency builds confidence in framework

### 2. Architecture Pattern: Skills-Based Execution

DevForgeAI follows **skills-based architecture**:

```
User → Command → Skill (Markdown) → Subagents (Markdown) → Terminal Tools
                      ↓
                  No executable code
                  Instructions only
```

**Why no executable code at skill level:**

1. **Skill responsibility**: Orchestrate workflow phases
2. **Subagent responsibility**: Specialized domain tasks
3. **Terminal responsibility**: Execute tools (bash, Read, Write, etc.)

Adding Python code at the skill level breaks this separation.

### 3. Immutability Principle

Context files are immutable constraints (`tech-stack.md`, `source-tree.md`, etc.).

`tech-stack.md` line 27-39 states clearly:
```markdown
### Documentation Format

**Primary Format**: Markdown
- **ALL** skills, subagents, commands, context files, ADRs use Markdown
- **YAML frontmatter** for metadata only
- **JSON** only for structured data exchange (NOT documentation)

**PROHIBITED**:
❌ HTML files for framework documentation
❌ JSON/YAML files for instructions (Markdown only)
❌ Language-specific code in framework docs (must be framework-agnostic)

**Rationale**: Claude interprets natural language (Markdown) better than structured formats.
```

This constraint is not aspirational—it's an immutable design decision.

---

## Consequences

### Positive

1. **Framework remains language-agnostic** - Works with any tech stack
2. **Zero dependencies** - No installation overhead, no version conflicts
3. **Transparent execution** - Users see exactly what's happening (Markdown)
4. **Maintainable** - Scales to 100+ skills without infrastructure burden
5. **Secure** - No hidden code execution, full transparency
6. **Version control friendly** - Clean diffs, easy merges

### Negative

1. **Limits some functionality** - Cannot use language-specific optimizations
2. **Requires skill-based design** - More workflow orchestration, less direct code
3. **Subagent delegation** - Heavy functionality must go to subagents, not skills
4. **Not directly testable** - Framework itself is tested through skills, not unit tests

---

## Implications for STORY-040

**STORY-040 (DevForgeAI Documentation Skill) must be implemented as:**

### NOT This (Violates Constraint):
```
❌ devforgeai_documentation/ (Python module)
   ├── __init__.py
   ├── greenfield_generator.py
   ├── brownfield_analyzer.py
   └── diagram_generator.py
```

### But This (Compliant):
```
✅ .claude/skills/devforgeai-documentation/
   ├── SKILL.md (workflow phases, step-by-step instructions)
   ├── references/
   │   ├── documentation-standards.md
   │   ├── greenfield-workflow.md
   │   ├── brownfield-analysis.md
   │   ├── diagram-generation-guide.md
   │   └── template-customization.md
   ├── assets/
   │   ├── templates/
   │   │   ├── readme-template.md
   │   │   ├── developer-guide-template.md
   │   │   └── ...
   └── [no Python code]
```

**How functionality is implemented:**

1. **Skill Phase 1**: Mode detection (greenfield vs brownfield)
2. **Skill Phase 2**: Discovery (read stories or analyze codebase)
3. **Skill Phase 3**: Content generation (invoke subagents)
   - `documentation-writer` subagent (Markdown prose)
   - `code-analyzer` subagent (codebase analysis)
4. **Skill Phase 4**: Template application
5. **Skill Phase 5**: Validation and output

**All logic is delegated to:**
- Subagents (specialized domain work)
- Terminal tools (file operations via Read/Write/Edit)
- AI analysis (Claude's built-in capabilities)

---

## Acceptance Criteria

✅ **This decision is accepted when:**

1. Python module `devforgeai_documentation/` is deleted
2. `devforgeai-documentation` skill is created as Markdown in `.claude/skills/`
3. All reference files are Markdown in skill `references/` directory
4. Skill workflow phases are defined, no executable code
5. Tests validate skill behavior through subagent invocation (not Python unit tests)
6. STORY-040 completion uses skill, not Python module
7. Documentation quality gate integrated into `/release` command via skill, not code

---

## Alternatives Considered

### Alternative 1: Create Python Module in Project Root (REJECTED)
**Why rejected**: Violates framework design—framework must be Markdown-only

### Alternative 2: Create Skill + Keep Python Module for Internal Use (REJECTED)
**Why rejected**: Still violates framework design—framework repository must not contain executable code

### Alternative 3: Modify Context Files to Allow Python Code (REJECTED)
**Why rejected**: Would require ADR to override immutable constraints. Better to follow existing design.

### Alternative 4: Implement as Skill Using Markdown Instructions (ACCEPTED)
**Why accepted**: Complies with all constraints, follows established patterns (like /dev, /qa, /orchestrate)

---

## Related Standards

**References:**
- `tech-stack.md` § Documentation Format (line 27-39)
- `source-tree.md` § .claude/ Directory (line 152-162)
- `anti-patterns.md` § Category 5 (line 91-111) - "Language-Specific Code in Framework"
- `architecture-constraints.md` § Skills-Based Architecture (line 82-100)
- `coding-standards.md` § Documentation Structure (line 121-130)

---

## Implementation Notes

### For STORY-040:

1. **Remove violation**: Delete `devforgeai_documentation/` Python module ✅ DONE
2. **Create skill**: Implement `.claude/skills/devforgeai-documentation/SKILL.md`
3. **Create references**: 5 Markdown reference files in `references/`
4. **Create templates**: 7 Markdown templates in `assets/templates/`
5. **Create command**: `/document` slash command in `.claude/commands/`
6. **Test via skill**: Verify through skill workflow, not Python unit tests
7. **Integrate gates**: Add documentation quality gate to `/release` via skill logic

### For Future Stories:

This ADR establishes the principle: **Executable code in the DevForgeAI framework repository is forbidden.**

All future functionality must be implemented as:
- Skills (Markdown instructions)
- Subagents (specialized domain work)
- Not as Python/JavaScript/C# modules

---

**Decision Made:** ACCEPTED
**Implementation Status:** PENDING (STORY-040 awaiting correction)
**Last Updated:** 2025-11-18

---

**Approval Chain:**
- [x] Architecture Review: Constraint-validator confirmed violations
- [x] Decision: Skill-based implementation required
- [x] Documentation: This ADR

