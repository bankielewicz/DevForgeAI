---
name: devforgeai-development
description: Implement features using Test-Driven Development (TDD) while enforcing architectural constraints from context files. Use when implementing user stories, building features, or writing code that must comply with tech-stack.md, source-tree.md, and dependencies.md. Automatically invokes devforgeai-architecture skill if context files are missing.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Skill
---

# DevForgeAI Development Skill

Implement features using Test-Driven Development while enforcing architectural constraints to prevent technical debt.

## Purpose

This skill guides feature implementation with:
1. **Context-driven development** - Enforces tech-stack.md, source-tree.md, dependencies.md
2. **TDD workflow** - Red → Green → Refactor cycle with spec validation
3. **Ambiguity resolution** - Uses AskUserQuestion for all unclear implementation decisions
4. **Native tool efficiency** - Uses Read/Edit/Write/Glob/Grep (40-73% token savings vs Bash)
5. **Anti-pattern prevention** - Validates against anti-patterns.md during implementation

## When to Use This Skill

Activate this skill when:
- Implementing user stories or features
- Writing new code for existing projects
- Refactoring code while maintaining specs
- Converting requirements into tested code
- Ensuring code complies with architectural decisions

## Core Principle: Enforce Context, Ask When Ambiguous

**Context files are THE LAW:**
- tech-stack.md → Technology choices (NEVER substitute libraries)
- source-tree.md → File placement rules (NEVER violate structure)
- dependencies.md → Package versions (NEVER add unapproved packages)
- coding-standards.md → Code patterns (ALWAYS follow conventions)
- architecture-constraints.md → Design rules (NEVER cross layer boundaries)
- anti-patterns.md → Forbidden patterns (ALWAYS avoid)

**When context is ambiguous → STOP and use AskUserQuestion**

---

## TDD Workflow (6 Phases)

### Phase 0: Context Validation (CRITICAL)

Before ANY code is written, validate architectural context exists.

#### Step 1: Check for Context Files

```
Read all 6 context files in PARALLEL:
- Read(file_path=".devforgeai/context/tech-stack.md")
- Read(file_path=".devforgeai/context/source-tree.md")
- Read(file_path=".devforgeai/context/dependencies.md")
- Read(file_path=".devforgeai/context/coding-standards.md")
- Read(file_path=".devforgeai/context/architecture-constraints.md")
- Read(file_path=".devforgeai/context/anti-patterns.md")
```

**If ANY file is missing:**

```
Skill(command="devforgeai-architecture")
```

**STOP development until context files exist.** This prevents technical debt from ambiguous assumptions.

#### Step 2: Load Story/Feature Specification

```
Read(file_path=".ai_docs/Stories/[story-id].story.md")
# OR
Read(file_path="docs/specs/[feature-name].spec.md")
```

#### Step 3: Validate Spec Against Context

**If conflicts detected → Use AskUserQuestion:**

```
Question: "Spec requires [X], but tech-stack.md specifies [Y]. Which is correct?"
Header: "Spec conflict"
Options:
  - "Update spec to use [Y] from tech-stack.md (maintain consistency)"
  - "Update tech-stack.md to [X] and document in ADR (architecture change)"
multiSelect: false
```

#### Step 4: Extract Technology Configuration

**CRITICAL: Determine test and build commands from tech-stack.md**

From the tech-stack.md content (already read in Step 1), extract:

```
Programming Language: [Identify from tech-stack.md]
  - Node.js/JavaScript/TypeScript
  - Python
  - C# / .NET
  - Go
  - Java
  - Rust
  - Other

Test Framework: [Identify from tech-stack.md]
  - npm test / npm run test (Node.js)
  - pytest / python -m pytest (Python)
  - dotnet test (. NET)
  - go test ./... (Go)
  - mvn test / gradle test (Java)
  - cargo test (Rust)

Build Tool: [Identify from tech-stack.md]
  - npm / npm run build (Node.js)
  - pip / python setup.py (Python)
  - dotnet build / dotnet restore (.NET)
  - go build (Go)
  - mvn / gradle (Java)
  - cargo build (Rust)
```

**If tech-stack.md doesn't specify test framework explicitly:**

Detect via project markers using Glob:
```
Glob(pattern="package.json") → Node.js → TEST_COMMAND="npm test"
Glob(pattern="*.csproj") → .NET → TEST_COMMAND="dotnet test"
Glob(pattern="pyproject.toml") → Python → TEST_COMMAND="pytest"
Glob(pattern="requirements.txt") → Python → TEST_COMMAND="pytest"
Glob(pattern="go.mod") → Go → TEST_COMMAND="go test ./..."
Glob(pattern="pom.xml") → Java/Maven → TEST_COMMAND="mvn test"
Glob(pattern="build.gradle*") → Java/Gradle → TEST_COMMAND="gradle test"
Glob(pattern="Cargo.toml") → Rust → TEST_COMMAND="cargo test"
```

**If detection fails (no tech-stack.md AND no project markers):**

Use AskUserQuestion:
```
Question: "Unable to detect project technology. What command runs tests?"
Header: "Test command"
Options:
  - "npm test (Node.js/JavaScript/TypeScript)"
  - "pytest (Python)"
  - "dotnet test (.NET/C#)"
  - "go test ./... (Go)"
  - "mvn test (Java/Maven)"
  - "gradle test (Java/Gradle)"
  - "cargo test (Rust)"
  - "Other (specify custom command)"
multiSelect: false
```

**Store commands as variables:**
```
TEST_COMMAND = [detected test command]
BUILD_COMMAND = [detected build command if applicable]
PACKAGE_MANAGER = [detected package manager]
```

**Validation:**
- [ ] Technology detected successfully
- [ ] TEST_COMMAND variable set
- [ ] BUILD_COMMAND variable set (if needed)
- [ ] Ready to proceed to Phase 1

**Example outputs:**
- Node.js project: TEST_COMMAND="npm test", BUILD_COMMAND="npm run build"
- .NET project: TEST_COMMAND="dotnet test", BUILD_COMMAND="dotnet build"
- Python project: TEST_COMMAND="pytest", BUILD_COMMAND=null

---

### Phase 1: Test-First Design (Red Phase)

Write failing tests BEFORE implementation following TDD principles.

#### Step 1: Analyze Acceptance Criteria

From story/spec, identify:
- **Functional requirements** (what the code must do)
- **Non-functional requirements** (performance, security, etc.)
- **Edge cases** (error conditions, validation failures)
- **Integration points** (APIs, databases, external services)

#### Step 2: Design Test Cases

For TDD patterns and test design, see `references/tdd-patterns.md`

**Test levels:**
- **Unit Tests** - Business logic, calculations, validation
- **Integration Tests** - Database, API, file I/O
- **Contract Tests** - API request/response validation
- **E2E Tests** - Complete user workflows

#### Step 3: Determine Test File Location

Consult source-tree.md for test organization.

**If location is ambiguous → Use AskUserQuestion:**

```
Question: "Where should tests for [ComponentName] be placed?"
Header: "Test location"
Options:
  - "tests/Unit/[ComponentName]Tests.[ext] (separate by type)"
  - "src/[Component]/[Component].Tests/[Component]Tests.[ext] (co-located)"
  - "tests/[SourcePath]/[ComponentName]Tests.[ext] (mirror source)"
multiSelect: false
```

#### Step 4: Write Failing Tests

Use native tools (NOT Bash):

```
Read existing test file (if exists)
Edit or Write test file with new failing tests
```

Follow coding-standards.md patterns (AAA format, naming conventions).

**Run tests to verify they fail:**

```
# Use TEST_COMMAND variable from Phase 0 Step 4
Bash(command=TEST_COMMAND)

# Example: If Node.js detected, executes: npm test
# Example: If .NET detected, executes: dotnet test
# Example: If Python detected, executes: pytest
```

**Expected: RED (test fails) ✓**

**If TEST_COMMAND not set:**
```
ERROR: Technology detection failed in Phase 0 Step 4
Unable to determine test command
Review Phase 0 logs for technology detection issues
```

---

### Phase 2: Implementation (Green Phase)

Write minimal code to make tests pass while enforcing constraints.

#### Step 1: Determine Implementation File Location

Consult source-tree.md for file placement.

**If location is ambiguous → Use AskUserQuestion**

#### Step 2: Validate Dependencies

```
Read(file_path=".devforgeai/context/dependencies.md")
```

**If implementation needs package NOT in dependencies.md → STOP and use AskUserQuestion:**

```
Question: "Implementation requires package '[PackageName]' for [functionality]. Should I add it?"
Header: "New dependency"
Options:
  - "Yes, add [PackageName] version [X.Y.Z]"
  - "No, use existing dependency [AlternativeName] from dependencies.md"
  - "No, implement manually without external dependency"
multiSelect: false
```

After approval:
1. Update dependencies.md
2. Create ADR documenting decision
3. Install package
4. Proceed with implementation

#### Step 3: Implement Following Coding Standards

```
Read(file_path=".devforgeai/context/coding-standards.md")
```

Enforce patterns during implementation:
- Async/await patterns
- Dependency injection
- Error handling (Result Pattern, exceptions, etc.)
- Naming conventions
- Logging patterns

#### Step 4: Validate Architecture Constraints

```
Read(file_path=".devforgeai/context/architecture-constraints.md")
```

Enforce layer boundaries (e.g., Domain NEVER references Infrastructure).

**If architecture decision is ambiguous → Use AskUserQuestion**

#### Step 5: Use Native Tools for File Operations

**CRITICAL: Use native tools for 40-73% token savings**

✅ CORRECT:
- `Read(file_path="...")`
- `Edit(file_path="...", old_string="...", new_string="...")`
- `Write(file_path="...", content="...")`
- `Glob(pattern="...")`
- `Grep(pattern="...", type="...")`

❌ FORBIDDEN:
- Bash for cat, sed, find, grep, echo > (use native tools instead)

Reserve Bash ONLY for: tests, builds, git, package managers

#### Step 6: Run Tests

```
# Use TEST_COMMAND variable from Phase 0 Step 4
Bash(command=TEST_COMMAND)
```

**Expected: GREEN (test passes) ✓**

---

### Phase 3: Refactor (Refactor Phase)

Improve code quality while keeping tests green.

For detailed refactoring techniques, see `references/refactoring-patterns.md`

#### Step 1: Check Anti-Patterns

```
Read(file_path=".devforgeai/context/anti-patterns.md")
```

Validate implementation doesn't violate:
- Library substitution (locked in tech-stack.md)
- Structure violation (defined in source-tree.md)
- Cross-layer dependencies (enforced by architecture-constraints.md)
- Framework mixing
- Magic numbers/strings
- God objects (>500 lines)
- Tight coupling (use dependency injection)
- Security anti-patterns (SQL injection, XSS, hardcoded secrets)

**If anti-pattern detected → Refactor immediately**

#### Step 2: Apply Refactoring Techniques

Common refactorings:
- Extract Method (methods >50 lines)
- Extract Class (classes >500 lines)
- Introduce Parameter Object (>4 parameters)
- Replace Magic Numbers with Constants
- Remove Duplication (DRY principle)

See `references/refactoring-patterns.md` for complete catalog.

#### Step 3: Keep Tests Green

```
# Refactor implementation
Edit(file_path="...", old_string="...", new_string="...")

# Verify tests still pass (use TEST_COMMAND from Phase 0)
Bash(command=TEST_COMMAND)
```

**HALT if tests break during refactoring**

**Expected: Tests remain GREEN ✓**

---

### Phase 4: Integration & Validation

Ensure implementation integrates correctly with existing codebase.

#### Step 1: Run Full Test Suite

```
# Use TEST_COMMAND from Phase 0 with coverage flags (if supported)
# Technology-specific coverage commands:
# - Node.js: npm test -- --coverage
# - Python: pytest --cov=src --cov-report=term
# - .NET: dotnet test --collect:"XPlat Code Coverage"
# - Go: go test -coverprofile=coverage.out ./...
# - Rust: cargo test -- --test-threads=1

Bash(command=TEST_COMMAND_WITH_COVERAGE)

# Or if simple test command:
Bash(command=TEST_COMMAND)
```

Validate:
- [ ] All existing tests still pass (no regressions)
- [ ] New tests pass
- [ ] Code coverage meets requirements (95%/85%/80%)

#### Step 2: Static Analysis

If configured:

```
Bash(command="[linter command]")
```

Fix violations using Edit tool.

#### Step 3: Build Validation

```
Bash(command="[build command]")
```

**Expected: Build succeeds ✓**

#### Step 4: Update Documentation

If implementation affects:
- API contracts → Update docs/api/
- Database schema → Update context files
- New dependencies → Update dependencies.md (already done in Phase 2)

---

### Phase 5: Git Workflow

Prepare implementation for review and merge.

For detailed git conventions, see `references/git-workflow-conventions.md`

#### Step 1: Review Changes

```
Bash(command="git status")
Bash(command="git diff")
```

Validate:
- [ ] Only relevant files modified
- [ ] No debug code or commented-out code
- [ ] No secrets or credentials in code
- [ ] All new files in correct locations (per source-tree.md)

#### Step 1b: Update Story File with Implementation Notes

**CRITICAL: Document implementation details in story file BEFORE committing**

This step is MANDATORY - it transforms the story from requirements-only into a complete record of what was done and how it was verified.

**Read story file:**
```
Read(file_path=".ai_docs/Stories/[story-id].story.md")
```

**Generate Implementation Notes section:**

Use Edit tool to add "## Implementation Notes" section (before "## Related Stories" or at end of file):

```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** [current date and time]
**Commit:** [will update with hash after commit]

### Definition of Done Status

[Copy each Definition of Done item from story file above, marking completion status]

- [x] Unit tests written and passing - Completed: Created X unit tests in tests/[module]/, all passing
- [x] Integration tests for API endpoints - Completed: Created Y integration tests, verified with cargo test
- [x] Code follows coding-standards.md - Completed: Applied cargo fmt, followed naming conventions
- [ ] Performance benchmarks created - Not completed: Deferred to STORY-XXX (performance optimization epic)

**If ALL items completed:** Mark all with [x] and brief completion note
**If ANY items NOT completed:** Mark with [ ] and provide reason:
  - "Deferred to STORY-XXX" (planned for future story)
  - "Out of scope" (requirement changed, documented in ADR)
  - "Blocked by [dependency]" (cannot complete until X resolved)

### Key Implementation Decisions

[Document significant technical decisions made during implementation]

- **Decision 1:** Used [Technology/Pattern] instead of [Alternative]
  - **Rationale:** tech-stack.md specifies [X], architecture-constraints.md requires [Y]
  - **Alternatives considered:** [List alternatives and why rejected]

- **Decision 2:** Placed files in [Location]
  - **Rationale:** source-tree.md specifies [structure rule]

[Include 2-5 key decisions that affect maintainability, performance, or architecture]

### Files Created/Modified

[List files organized by layer from source-tree.md]

**Layer: [Presentation/Application/Domain/Infrastructure]**
- `path/to/file1.ext` - [Purpose, what it does]
- `path/to/file2.ext` - [Purpose, what it does]

**Tests:**
- `tests/unit/test_module.ext` - Unit tests for [component]
- `tests/integration/test_api.ext` - Integration tests for [feature]

### Test Results

- **Unit tests:** X passing / Y total
- **Integration tests:** X passing / Y total
- **E2E tests:** X passing / Y total (if applicable)
- **Coverage:** Z% (target: 95% business logic, 85% application, 80% infrastructure)
- **All tests passing:** YES/NO

**Coverage by layer:**
- Business logic: X%
- Application: Y%
- Infrastructure: Z%

### Acceptance Criteria Verification

[For each acceptance criterion from story, document HOW it was verified]

**Given/When/Then Scenario 1:**
- [x] **Verified:** cargo test::test_scenario_1 passes - validates [specific behavior]
- **Method:** Unit test validates [input] → [expected output]

**Given/When/Then Scenario 2:**
- [x] **Verified:** Manual testing - ran `cargo run -- [args]`, confirmed [expected result]
- **Method:** Integration test + manual verification

**Scenario 3 (if any not verified):**
- [ ] **Not verified:** Deferred to QA - requires [specific test environment/data]

### Notes

[Optional: Any additional context]
- Blockers encountered: [None / List blockers and resolutions]
- Workarounds applied: [None / List workarounds]
- Technical debt introduced: [None / List debt with plan to address]
- Future improvements: [Suggestions for v2.0, optimization opportunities]
```

**Validation before proceeding to Step 2:**
- [ ] Implementation Notes section added to story file
- [ ] All DoD items have status ([x] or [ ] with reason)
- [ ] Key decisions documented
- [ ] Files listed
- [ ] Test results recorded
- [ ] Acceptance criteria verification documented

**If any validation fails:** HALT - Complete Implementation Notes before committing

---

#### Step 2: Stage Implementation Files and Story File

**CRITICAL: Story file MUST be included in commit**

```
# Stage implementation files
Bash(command="git add [relevant_implementation_files]")

# Stage updated story file (includes Implementation Notes from Step 1b)
Bash(command="git add .ai_docs/Stories/[story-id].story.md")
```

**Validation:**
- [ ] Implementation files staged
- [ ] Story file staged (with Implementation Notes)
- [ ] Ready for commit

---

#### Step 3: Create Commit

**Commit message format (Conventional Commits):**

```
Bash(command='git commit -m "$(cat <<'\''EOF'\''
[type]: [brief description]

- Implemented [feature] following TDD
- Tests: [test description]
- Compliance: tech-stack.md, coding-standards.md
- Coverage: [percentage]

Closes #[issue-number]
EOF
)"')
```

**Commit types:** feat, fix, refactor, test, docs, chore, perf, style

**Example:**

```
feat: Implement order discount calculation

- Implemented CalculateDiscount method following TDD
- Tests: Unit tests for valid coupon, expired coupon, invalid code
- Compliance: tech-stack.md (Dapper), coding-standards.md (Result Pattern)
- Coverage: 95% for OrderService

Closes #STORY-001
```

See `references/git-workflow-conventions.md` for:
- Branch naming conventions
- Commit timing strategies
- Staging strategies
- Push best practices
- Git hooks integration

#### Step 4: Push to Remote

```
Bash(command="git push origin [branch-name]")
```

---

## Ambiguity Resolution Protocol

**CRITICAL: Use AskUserQuestion for ALL ambiguities**

### Common Ambiguity Scenarios

#### Scenario 1: Technology Choice Ambiguous

Spec requires functionality not explicitly covered in tech-stack.md.

**Response:**

```
Question: "Spec requires [technology/feature], but tech-stack.md doesn't specify. Which should be used?"
Header: "[Category]"
Description: "This will be added to tech-stack.md as a LOCKED choice"
Options:
  - "[Option 1] (benefits: ...)"
  - "[Option 2] (benefits: ...)"
  - "[Option 3] (benefits: ...)"
multiSelect: false
```

After answer:
1. Update tech-stack.md
2. Create ADR documenting decision
3. Update dependencies.md if needed
4. Proceed with implementation

#### Scenario 2: Pattern Not Specified

Implementation needs pattern not in coding-standards.md or architecture-constraints.md.

**Use AskUserQuestion to clarify which pattern to use**

#### Scenario 3: File Location Unclear

New file type not covered in source-tree.md.

**Use AskUserQuestion to determine correct location**

#### Scenario 4: Conflicting Requirements

Spec requirement conflicts with existing context files.

**Use AskUserQuestion to resolve conflict**

#### Scenario 5: Version Ambiguity

Package version not specified in dependencies.md.

**Use AskUserQuestion to determine version**

---

## Tool Usage Protocol

**MANDATORY: Use native tools for file operations**

### File Operations (ALWAYS use native tools):
- **Reading**: Read tool, NOT `cat`, `head`, `tail`
- **Searching**: Grep tool, NOT `grep`, `rg`, `ag`
- **Finding**: Glob tool, NOT `find`, `ls -R`
- **Editing**: Edit tool, NOT `sed`, `awk`, `perl`
- **Creating**: Write tool, NOT `echo >`, `cat > <<EOF`

### Terminal Operations (Use Bash):
- **Version control**: git commands
- **Package management**: npm, pip, cargo, dotnet, maven, gradle
- **Test execution**: pytest, npm test, dotnet test, cargo test, mvn test
- **Build processes**: make, cmake, gradle, dotnet build, npm run build
- **Containers**: docker, kubectl, podman

### Communication (Use text output):
- Explain steps to user
- Provide analysis results
- Ask clarifying questions
- NOT `echo` or `printf` for communication

### Efficiency Target

**Token budget per feature implementation: <80,000 tokens**

Breakdown:
- Context validation: ~5,000 tokens
- Test design & writing: ~15,000 tokens
- Implementation: ~30,000 tokens
- Refactoring & validation: ~20,000 tokens
- Documentation updates: ~10,000 tokens

**Using native tools saves 40-73% vs Bash commands**

---

## Integration with Other Skills

### devforgeai-architecture

Auto-invoke if context files missing:

```
if context_files_missing:
    Skill(command="devforgeai-architecture")
    # Wait for completion, then reload context files and continue
```

### devforgeai-qa

Invoke light QA after each phase, deep QA at end:

```
# Light QA during development (automatic or manual)
Skill(command="devforgeai-qa --mode=light --story={story_id}")

# Deep QA after implementation complete
Skill(command="devforgeai-qa --mode=deep --story={story_id}")
```

### devforgeai-release

After QA approval, ready for release:

```
Skill(command="devforgeai-release --story={story_id}")
```

---

## Reference Materials

Load these on demand during development:

### TDD Guidance
**`./references/tdd-patterns.md`** (1,013 lines)
- Complete TDD workflow patterns
- Red → Green → Refactor cycle
- Test structure patterns (AAA, Given-When-Then)
- Test types (unit, integration, contract, E2E)
- Mocking patterns
- Test data builders
- Edge case testing
- Code coverage guidance
- TDD anti-patterns to avoid

### Refactoring
**`./references/refactoring-patterns.md`** (797 lines)
- Common refactoring techniques (Extract Method, Extract Class, etc.)
- Code smell identification patterns
- Refactoring safety procedures
- Language-specific refactoring patterns
- Refactoring decision trees
- Refactoring anti-patterns

### Version Control
**`./references/git-workflow-conventions.md`** (885 lines)
- Branch naming conventions
- Commit message format (Conventional Commits)
- Commit timing strategies (single vs multiple commits per story)
- Staging strategies
- Push timing and best practices
- Git hooks integration
- Multi-file commit organization

---

## Success Criteria

This skill succeeds when:

- [ ] Context files validated before development starts
- [ ] All ambiguities resolved via AskUserQuestion (no assumptions)
- [ ] Tests written BEFORE implementation (TDD followed)
- [ ] Implementation follows ALL context file constraints
- [ ] No anti-patterns introduced
- [ ] All tests pass (including new and existing)
- [ ] Code coverage meets requirements (95%/85%/80%)
- [ ] Build succeeds
- [ ] Native tools used for file operations (achieving token efficiency)
- [ ] Documentation updated for any API/schema changes
- [ ] Git commits created with proper conventional format

**The goal: Zero technical debt from wrong assumptions, fully tested features that comply with architectural decisions.**
