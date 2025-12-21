# Technology Stack - DevForgeAI Framework

**Status**: LOCKED
**Last Updated**: 2025-12-21
**Version**: 1.1

## CRITICAL RULE: Framework-Agnostic Design

**LOCKED PRINCIPLE**: DevForgeAI is a **meta-framework** that works with ANY technology stack. This file documents the framework's own implementation constraints, NOT the constraints of projects using the framework.

---

## Framework Implementation Technologies

### Core Platform

**Platform**: Claude Code Terminal
- **Version**: 1.0+
- **Constraint**: Framework MUST work within Claude Code Terminal capabilities
- **Documentation**: https://docs.claude.com/en/docs/claude-code/

**CRITICAL**: Framework components are implemented as:
- **Skills** (`.claude/skills/[skill-name]/SKILL.md`) - Markdown with YAML frontmatter
- **Subagents** (`.claude/agents/[agent-name].md`) - Markdown with YAML frontmatter
- **Slash Commands** (`.claude/commands/[command-name].md`) - Markdown with YAML frontmatter

### Documentation Format

**Primary Format**: Markdown
- **ALL** skills, subagents, commands, context files, ADRs use Markdown
- **YAML frontmatter** for metadata only
- **JSON** only for structured data exchange (NOT documentation)

**PROHIBITED**:
❌ HTML files for framework documentation
❌ JSON/YAML files for instructions (Markdown only)
❌ Language-specific code in framework docs (must be framework-agnostic)

**Rationale**: Claude interprets natural language (Markdown) better than structured formats. Research shows 60-80% token savings with progressive disclosure in Markdown.

### Version Control

**System**: Git
- **Required**: All framework components version controlled
- **Branching**: Feature branches for development
- **Commits**: Conventional commit format

### Framework Validation Tools (EPIC-015)

**Epic Coverage Validation System**:
- **Language**: Bash scripting (Claude Code native)
- **Parsing**: Grep patterns for YAML frontmatter and markdown headers
- **Matching**: Exact `epic:` field matching via `grep "^epic: EPIC-XXX"`
- **Data Model**: JSON files or Bash associative arrays
- **Reporting**: Write tool for JSON/markdown generation
- **CLI**: Slash command `/validate-epic-coverage` in `.claude/commands/`

**Rationale** (ADR-005): Uses only Claude Code native tools (Grep, Read, Write, Bash) to achieve 95% coverage without external dependencies. Evidence: 60/63 stories (95%) have `epic:` field.

**PROHIBITED for framework validation**:
❌ External Python libraries (RapidFuzz, PyYAML, mistune)
❌ npm packages for framework tooling
❌ Any dependencies requiring `pip install` or `npm install`

---

## Static Analysis Tools (Code Quality & Security)

### REMOVED: ast-grep (ADR-007)

**Status**: ❌ REMOVED (2025-12-21)
**Decision**: ADR-007 - Remove ast-grep and Evaluate Tree-sitter

**Reason for Removal**: After comprehensive evaluation (EPIC-018, STORY-115-118), ast-grep was found to have fundamental limitations:

1. **Multi-line Pattern Matching Fails** - Patterns with comments/type annotations between statements don't match
2. **Cannot Count/Accumulate** - "Detect classes with >20 methods" impossible with pattern matching
3. **Whitespace Sensitivity** - Python indentation breaks pattern matching
4. **No Semantic Analysis** - Cannot detect duplicate code, unused variables, or cross-file issues
5. **C# AST Issues** - Access modifiers and catch blocks don't match expected patterns

**Evidence**: 52/59 tests passing (88.1%) despite comprehensive remediation - 6 tests failed due to tool limitations, NOT implementation issues.

**PROHIBITED**:
❌ ast-grep for static analysis (REMOVED)
❌ Pattern-based tools that cannot handle real-world code
❌ Tools without proper Python/C# AST support

---

### FUTURE: Tree-sitter Integration (PLANNED)

**Status**: 🔄 EVALUATION PLANNED
**Target**: DevForgeAI CLI enhancement

**Why Tree-sitter**:
- Direct AST access (traversal, not pattern matching)
- Python bindings available (`py-tree-sitter`)
- Can count, traverse, and analyze code
- Industry standard (GitHub, Neovim, Helix)
- Supports 100+ languages

**Planned Integration**:
```
devforgeai analyze --security /path/to/code
devforgeai analyze --antipatterns /path/to/code
```

**Implementation Approach**:
1. Add `py-tree-sitter` and language bindings to devforgeai CLI
2. Implement rule engine using AST traversal
3. Port security rules from ast-grep reference
4. Port anti-pattern rules from ast-grep reference

**Rationale**: Tree-sitter provides full AST access, enabling counting, traversal, and semantic analysis that ast-grep's pattern matching cannot achieve.

**Reference**: New epic to be created for tree-sitter evaluation

---

## Project Technology Stack Pattern

When creating context files for **projects using DevForgeAI**, the architecture skill MUST use AskUserQuestion to determine:

### Backend Technology Options

Framework supports (but does not mandate) any of:
- C# with .NET 6.0+
- Python 3.9+ with FastAPI/Django/Flask
- Node.js 18+ with Express/Nest.js
- Java 11+ with Spring Boot
- Go 1.20+ with Gin/Echo
- Rust 1.70+ with Actix/Rocket

**Pattern**: devforgeai-architecture skill asks user to select backend technology, then LOCKS it in project's tech-stack.md.

### Frontend Framework Options

Framework supports (but does not mandate) any of:
- React 18+ with TypeScript
- Vue.js 3+ with TypeScript
- Angular 15+
- Svelte 4+
- Solid.js
- Next.js 14+ (React meta-framework)

**Pattern**: devforgeai-architecture skill asks user to select frontend framework, then LOCKS it in project's tech-stack.md.

### Database Options

Framework supports (but does not mandate) any of:
- PostgreSQL 13+
- MySQL 8+
- Microsoft SQL Server 2019+
- MongoDB 6+
- SQLite 3+
- Oracle Database 19c+

**Pattern**: devforgeai-architecture skill asks user to select database, then LOCKS it in project's tech-stack.md.

### Testing Framework Options

Framework supports (but does not mandate) any of:

**For .NET**:
- xUnit
- NUnit
- MSTest

**For Node.js/TypeScript**:
- Jest
- Vitest
- Mocha + Chai

**For Python**:
- pytest
- unittest
- nose2

**For Java**:
- JUnit 5
- TestNG

**For Go**:
- testing (standard library)
- Testify

**Pattern**: devforgeai-architecture skill asks user to select testing framework for their language, then LOCKS it in project's tech-stack.md.

---

## Framework Constraint Enforcement

### LOCKED: Claude Code Terminal Tools

Framework skills and subagents MUST use Claude Code native tools:

**File Operations**:
- ✅ `Read(file_path="...")` - Reading files
- ✅ `Write(file_path="...")` - Creating files
- ✅ `Edit(file_path="...", old_string="...", new_string="...")` - Modifying files
- ✅ `Glob(pattern="...")` - Finding files by pattern
- ✅ `Grep(pattern="...")` - Searching file contents

**PROHIBITED**:
❌ `Bash(command="cat file.txt")` - Use Read() instead
❌ `Bash(command="echo 'content' > file.txt")` - Use Write() instead
❌ `Bash(command="find . -name *.md")` - Use Glob() instead
❌ `Bash(command="grep 'pattern' file.txt")` - Use Grep() instead
❌ `Bash(command="sed -i 's/old/new/' file.txt")` - Use Edit() instead

**Rationale**: Native tools are 40-73% more token-efficient than Bash commands.

**Exception**: Bash MUST be used for:
- Running tests: `Bash(command="npm test")`, `Bash(command="dotnet test")`
- Running builds: `Bash(command="npm run build")`, `Bash(command="dotnet build")`
- Git operations: `Bash(command="git status")`, `Bash(command="git commit")`
- Package managers: `Bash(command="npm install")`, `Bash(command="pip install")`

### LOCKED: Skill Invocation Pattern

**Skills invoke other skills**:
```markdown
Skill(command="devforgeai-qa --mode=light --story=STORY-001")
```

**Skills invoke subagents**:
```markdown
Task(subagent_type="test-automator",
     prompt="Generate tests for acceptance criteria in STORY-001.md")
```

**PROHIBITED**:
❌ Skills directly calling Bash to invoke other skills
❌ Circular skill dependencies (Skill A calls Skill B calls Skill A)

### LOCKED: Context File Format

All project context files MUST follow this structure:

```markdown
# [Context File Title]

**Status**: LOCKED
**Last Updated**: YYYY-MM-DD
**Version**: X.Y

## [Section 1]
Content with ✅ CORRECT and ❌ FORBIDDEN examples

## [Section 2]
...

## Ambiguity Resolution Protocol
When ambiguity is encountered, AI agents MUST use AskUserQuestion...
```

**PROHIBITED**:
❌ Context files in JSON format
❌ Context files in YAML format (except frontmatter)
❌ Context files without "LOCKED" status marker
❌ Context files without version and date

---

## Token Budget Constraints

### LOCKED: Component Size Limits

These limits enforce Claude Code Terminal's character budget constraint:

**Skills**:
- Target: 500-800 lines (~20,000-30,000 characters)
- Maximum: 1,000 lines (~40,000 characters)
- Rationale: Skills have separate context windows

**Slash Commands**:
- Target: 200-400 lines (~8,000-15,000 characters)
- Maximum: 500 lines (~20,000 characters)
- Rationale: 15,000 character budget for command context

**Subagents**:
- Target: 100-300 lines (~4,000-12,000 characters)
- Maximum: 500 lines (~20,000 characters)
- Rationale: Separate context window per subagent

**Context Files**:
- Target: 200-400 lines (~8,000-15,000 characters)
- Maximum: 600 lines (~24,000 characters)
- Rationale: Read into development skill context

**ENFORCEMENT**:
When components exceed targets:
1. Extract reference documentation to separate files
2. Use progressive disclosure (load references on demand)
3. Split into sub-components if necessary

---

## Framework Extension Pattern

### Adding New Skills

**Process**:
1. Create `.claude/skills/[skill-name]/` directory
2. Create `SKILL.md` with YAML frontmatter
3. Add `references/` subdirectory for deep documentation
4. Update CLAUDE.md with skill description
5. Test skill invocation

**PROHIBITED**:
❌ Adding skills without SKILL.md file
❌ Hardcoding logic in skills (use AskUserQuestion for decisions)
❌ Skills that work only for specific languages

### Adding New Subagents

**Process**:
1. Create `.claude/agents/[agent-name].md`
2. Add YAML frontmatter with name, description, tools, model
3. Write system prompt focused on single responsibility
4. Test subagent in isolation and with skills
5. Update documentation

**PROHIBITED**:
❌ Subagents with multiple responsibilities
❌ Subagents that overlap with existing agents
❌ Subagents without tool restrictions (use principle of least privilege)

### Adding New Slash Commands

**Process**:
1. Create `.claude/commands/[command-name].md`
2. Add YAML frontmatter with description, argument-hint
3. Write command instructions with $ARGUMENTS placeholder
4. Keep under 500 lines (<20K characters)
5. Test with real arguments

**PROHIBITED**:
❌ Commands exceeding 500 lines (extract to skills)
❌ Commands without argument hints
❌ Commands that duplicate skill functionality

---

## Ambiguity Resolution Protocol

**CRITICAL**: When framework implementation encounters ambiguity:

1. **Check this file** for LOCKED decisions
2. **Check other context files** for related constraints
3. **If still ambiguous** → STOP and use AskUserQuestion
4. **After resolution** → Update context file or create ADR

**Example Ambiguity**:
"Should the development skill invoke QA skill automatically or wait for user command?"

**Resolution**:
```
Question: "Should development skill invoke QA skill automatically after implementation?"
Header: "QA invocation"
Options:
  - "Automatic - Always invoke light QA after each phase"
  - "Manual - Wait for user to run /qa command"
  - "Configurable - Allow user to set preference"
multiSelect: false
```

After resolution → Document decision in this file or create ADR.

---

## Migration and Versioning

### Framework Version Upgrades

**Semantic Versioning**: MAJOR.MINOR.PATCH

**MAJOR** (Breaking changes):
- Context file format changes
- Skill/subagent interface changes
- Tool usage pattern changes
- Requires project migration

**MINOR** (New features):
- New skills added
- New subagents added
- New slash commands added
- Backward compatible

**PATCH** (Bug fixes):
- Documentation corrections
- Reference file updates
- Minor optimizations
- Fully compatible

### Project Migration Strategy

When upgrading projects to new framework version:
1. Check CHANGELOG for breaking changes
2. Update context files if format changed
3. Regenerate context files with new architecture skill
4. Test with sample story before full migration

---

## Installer/Distribution Technologies

### NPM Package Distribution (EPIC-012)

**Status**: LOCKED (as of 2025-11-25)

**Purpose**: DevForgeAI installer is distributed as an NPM package for easy installation.

**Package Distribution**:
- **Registry**: NPM (public)
- **Package Name**: `devforgeai` (or `@devforgeai/installer` if scoped)
- **Installation**: `npm install -g devforgeai`
- **Entry Point**: `devforgeai` command available globally

**CLI Framework (Node.js wrapper)**:
- **Commander.js 11+** OR **Yargs 17+** - LOCKED (command-line argument parsing)
- **Inquirer.js 9+** - LOCKED (interactive wizard prompts)
- **Ora 7+** - LOCKED (spinner/progress indicators)
- **Chalk 5+** - LOCKED (terminal colors/formatting)
- **Semver 7+** - LOCKED (semantic version parsing/comparison)
- **Boxen 7+** - LOCKED (bordered message boxes)

**Core Installer (Python - existing)**:
- Reuses existing `installer/install.py` and related modules
- Node.js CLI wrapper invokes Python subprocess
- Python 3.10+ required for CLI tools (devforgeai validators)

**Integration Points**:
- **NPM Registry**: Package publishing via `npm publish` with provenance
- **GitHub API**: Version checking, release notes (optional, online mode)
- **PyPI**: devforgeai CLI installed via pip (optional dependency)

**PROHIBITED**:
❌ Replacing Python installer with pure Node.js (reuse existing code)
❌ Bundling alternative CLI frameworks (one choice only)
❌ External network calls during installation (offline mode required)

**Rationale**: NPM provides widest reach for Node.js developers (primary target audience). Python installer core already exists and is well-tested.

---

## References

- [Claude Code Documentation](https://docs.claude.com/en/docs/claude-code/)
- [Native Tools Best Practices](.claude/skills/claude-code-terminal-expert/references/best-practices.md) - Token efficiency guidelines
- [Claude Code Terminal Expert Skill](.claude/skills/claude-code-terminal-expert/SKILL.md) - Complete terminal feature reference
- [Framework Design Rationale](README.md)

---

**REMEMBER**: This tech-stack.md defines the **framework's own constraints**. Projects using DevForgeAI will have their own tech-stack.md files created by the devforgeai-architecture skill based on user technology choices.
