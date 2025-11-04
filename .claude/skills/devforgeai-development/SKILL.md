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

---

## CRITICAL: Extracting Parameters from Conversation Context

**IMPORTANT:** Skills CANNOT accept runtime parameters. All information must be extracted from conversation context.

### How Slash Commands Pass "Parameters" to Skills

When a slash command invokes this skill, it:
1. Loads story file via @file reference: `@.ai_docs/Stories/STORY-XXX.story.md`
2. States context explicitly: "Story ID: STORY-XXX"
3. Invokes skill WITHOUT arguments: `Skill(command="devforgeai-development")`

**You must extract story ID from the conversation.**

### Story ID Extraction

The slash command loads the story file via @file reference, making story content available in conversation.

**Extract story ID from conversation:**

**Method 1: Read YAML frontmatter**
```
Look for YAML frontmatter in conversation:
  ---
  id: STORY-XXX
  title: ...
  status: ...
  ---

Extract: id field = Story ID
```

**Method 2: Search for file reference**
```
Search conversation for pattern:
  ".ai_docs/Stories/STORY-XXX"

Extract STORY-XXX from file path
```

**Method 3: Search for explicit statement**
```
Search conversation for:
  "Story ID: STORY-XXX"
  "Story: STORY-XXX"

Extract STORY-XXX
```

**Method 4: Grep loaded content**
```
If methods 1-3 fail:
  Grep conversation for "STORY-[0-9]+" pattern
  Use first match found
```

### Validation Before Proceeding

Before starting TDD workflow, verify:
- [ ] Story ID extracted successfully
- [ ] Story content available in conversation (via @file load)
- [ ] Acceptance criteria accessible from story content
- [ ] Technical specification present

**If extraction fails:**
```
HALT with error:
"Cannot extract story ID from conversation context.

Expected to find:
  - YAML frontmatter with 'id: STORY-XXX' field
  - OR file reference like '.ai_docs/Stories/STORY-XXX.story.md'
  - OR explicit statement like 'Story ID: STORY-XXX'

Please ensure story is loaded via slash command or provide story ID explicitly."
```

---

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

**For EACH DoD item, validate completion status:**

<deferral_enforcement>
  <policy>ZERO autonomous deferrals allowed</policy>
  <mechanism>AskUserQuestion MANDATORY for all incomplete items</mechanism>
  <violation_consequence>Git commit BLOCKED until user approval obtained</violation_consequence>
</deferral_enforcement>

```
FOR each DoD item in story acceptance criteria:
    IF item is complete:
        Mark: [x] {item} - Completed: {brief_completion_note}

    ELSE:
        # Item not complete - MUST get user approval to defer

        <halt_condition>
          <trigger>Incomplete DoD item detected</trigger>
          <item>'{item}'</item>
          <action>MANDATORY AskUserQuestion - CANNOT SKIP</action>
        </halt_condition>

        AskUserQuestion:
            Question: "DoD item not complete: '{item}'. How should we proceed?"
            Header: "Incomplete DoD"
            Options:
                - "Complete it now (continue development to finish item)"
                - "Defer to follow-up story (create STORY-XXX for tracking)"
                - "Scope change (requirements changed - requires ADR)"
                - "External blocker (document dependency with ETA)"
            multiSelect: false

        BASED ON USER SELECTION:

        **Option 1: "Complete it now"**
        ```
        Return to Phase 2-4 (TDD cycle)
        Implement the DoD item
        Run tests
        Mark: [x] {item} - Completed: {note}
        ```

        **Option 2: "Defer to follow-up story"**
        ```
        AskUserQuestion:
            Question: "Create follow-up story for '{item}' now or later?"
            Header: "Follow-up"
            Options:
                - "Create now (I'll approve story details)"
                - "I'll create manually later (provide story ID)"
            multiSelect: false

        IF "Create now":
            Task(
                subagent_type="requirements-analyst",
                description="Create follow-up story",
                prompt="Create follow-up story for deferred work:

                        Original Story: {current_story_id}
                        Deferred DoD Item: '{item}'

                        Extract acceptance criteria from original item.
                        Set dependency: prerequisite_stories: [{current_story_id}]
                        Set epic: {current_epic}
                        Set status: Backlog

                        Return new story ID."
            )

            new_story_id = {result from subagent}

            Mark: [ ] {item} - Deferred to {new_story_id}: Work split for focused implementation

        ELSE:
            AskUserQuestion:
                Question: "What is the follow-up story ID?"
                Header: "Story ID"
                (User must provide STORY-XXX ID)

            Verify story exists:
            Glob(pattern=".ai_docs/Stories/{user_provided_id}*.md")
            IF not found:
                WARN: "Story doesn't exist yet. You must create it."

            Mark: [ ] {item} - Deferred to {user_provided_id}: {get reason from user}
        ```

        **Option 3: "Scope change (requires ADR)"**
        ```
        AskUserQuestion:
            Question: "Create ADR documenting scope change now or later?"
            Header: "ADR creation"
            Options:
                - "Create now (I'll provide justification)"
                - "I'll create manually later (provide ADR number)"
            multiSelect: false

        IF "Create now":
            Task(
                subagent_type="architect-reviewer",
                description="Create scope change ADR",
                prompt="Create ADR for scope change:

                        Story: {current_story_id}
                        Descoped Item: '{item}'

                        Document:
                        - Why requirement changed
                        - Business justification
                        - Impact on system
                        - Alternatives considered

                        Return ADR number."
            )

            adr_number = {result from subagent}

            Mark: [ ] {item} - Out of scope: ADR-{adr_number} documents scope change

        ELSE:
            AskUserQuestion:
                Question: "What is the ADR number?"
                Header: "ADR number"
                (User must provide ADR-XXX number)

            Mark: [ ] {item} - Out of scope: ADR-{user_provided_adr}
        ```

        **Option 4: "External blocker"**
        ```
        AskUserQuestion:
            Question: "Describe the external blocker for '{item}'"
            Header: "Blocker details"
            (Free-form: "Example: Payment API v2 not available until 2025-12-01")

        blocker_description = {user input}

        Validate blocker is external:
        IF blocker_description contains internal terms (our code, our API, our module):
            AskUserQuestion:
                Question: "This seems like an internal blocker. Is it truly external (outside our control)?"
                Header: "Blocker type"
                Options: ["Yes - external dependency", "No - I can resolve it now"]
                multiSelect: false

            IF "No":
                Return to "Complete it now" path

        Mark: [ ] {item} - Blocked by: {blocker_description}

        # Log to technical debt register

        # Auto-create from template if doesn't exist
        Check if .devforgeai/technical-debt-register.md exists
        IF not found:
            Read template: .claude/skills/devforgeai-orchestration/assets/templates/technical-debt-register-template.md
            Write(.devforgeai/technical-debt-register.md, content=template)
            Display: "Created technical debt register from template"

        Read .devforgeai/technical-debt-register.md
        Append to "Open Debt Items" section:
            "- {item} (from {story_id}): Blocked by {blocker_description} | Date: {date} | Status: Open"
        ```
```

**After ALL DoD items processed, validate and display summary:**

<validation_checkpoint>
  <requirement>Every incomplete DoD item MUST have user-approved justification</requirement>
  <check>Verify AskUserQuestion was invoked for each deferral</check>
  <action_on_failure>HALT git commit - return to deferral resolution</action_on_failure>
</validation_checkpoint>

```
# Final enforcement check
IF any deferred item lacks user interaction approval:
    <error_condition>
      <type>PROTOCOL_VIOLATION</type>
      <message>Cannot proceed to git commit: Deferrals require user approval via AskUserQuestion</message>
      <resolution>Return to Phase 5 Step 1b and execute AskUserQuestion for each incomplete item</resolution>
    </error_condition>

    HALT development
    Display: "❌ ERROR: Autonomous deferrals detected. User approval required for all incomplete DoD items."
    DO NOT proceed to Step 1.5 (deferral validation)

ELSE:
    Display:
    "Definition of Done Status:
     - Complete: {complete_count}/{total_count}
     - Deferred: {deferred_count}
       - Story splits: {story_split_count} (follow-up stories created/referenced)
       - Scope changes: {scope_change_count} (ADRs created/referenced)
       - External blockers: {blocker_count} (tracked in tech debt register)

    All deferrals have user approval and proper justification ✓
    Proceeding to automated deferral validation..."

# Story Size Detection (RCA-006 Rec 4)
IF deferred_count > 3:
    <story_size_warning>
      <trigger>More than 3 deferred DoD items detected</trigger>
      <threshold>Maximum recommended: 3 deferrals per story</threshold>
      <implication>Excessive deferrals suggest story scope too large or poorly defined</implication>
      <action>Recommend story splitting for better focus and reduced technical debt</action>
    </story_size_warning>

    Display:
    "⚠️  STORY SIZE WARNING

     This story has {deferred_count} deferred DoD items.
     Recommended maximum: 3 deferrals

     Excessive deferrals indicate:
     - Story scope may be too large
     - Work is fragmented across multiple follow-up stories
     - Risk of deferral chains (A→B→C)

     Consider splitting into focused stories to reduce technical debt."

    AskUserQuestion:
        Question: "Story has {deferred_count} deferrals (max 3 recommended). How should we proceed?"
        Header: "Story Size"
        Options:
            - "Complete more items now (reduce deferrals by implementing additional work)"
            - "Split story (AI will analyze and suggest focused splits)"
            - "Accept as-is (I'll document reason: legacy refactor, infrastructure, etc.)"
        multiSelect: false

    BASED ON USER SELECTION:

    **Option 1: "Complete more items now"**
    ```
    Display: "Returning to implementation to complete additional DoD items..."

    AskUserQuestion:
        Question: "Which deferred items should we complete now?"
        Header: "Items to complete"
        Options:
            [List each deferred item as option]
        multiSelect: true  # Allow selecting multiple

    selected_items = user_response

    FOR each selected_item:
        Display: "Implementing: {selected_item}"
        # Return to Phase 2 (Implementation) for this item
        # After implementation, return to DoD validation

    # After implementing selected items:
    Display: "✓ Additional items complete. Reduced deferrals from {original_count} to {new_count}"

    # Re-run DoD validation to update counts
    ```

    **Option 2: "Split story (AI will analyze)"**
    ```
    Display: "Analyzing story for split opportunities..."

    Task(
        subagent_type="requirements-analyst",
        description="Suggest story split",
        prompt="Analyze current story for splitting recommendations:

                Story ID: {current_story_id}
                Story Points: {story_points}
                Total DoD Items: {total_count}
                Complete: {complete_count}
                Deferred: {deferred_count}

                Deferred items:
                {list each deferred item with justification}

                Analyze and suggest:
                1. Natural groupings of deferred work
                2. Core story (keep in current) vs extensions (move to child stories)
                3. Recommended split: 2-3 focused child stories
                4. Story points distribution

                Use splitting techniques:
                - By operations (CRUD splits)
                - By quality attributes (functionality vs performance)
                - By testing scope (unit vs integration vs platform)

                Return:
                - Recommended split approach
                - Child story titles and scope
                - Acceptance criteria distribution
                - Story points for each child"
    )

    split_recommendations = extract from subagent response

    Display:
    "Split Recommendations:

     {format split recommendations from subagent}

     Option A: {approach_1}
       - STORY-{current}: {core_work} ({points} points) - KEEP
       - STORY-{new_1}: {extension_1} ({points} points) - NEW
       - STORY-{new_2}: {extension_2} ({points} points) - NEW

     Option B: {approach_2}
       [Alternative split...]"

    AskUserQuestion:
        Question: "Which split approach should we use?"
        Header: "Split Strategy"
        Options:
            - "Option A ({count} stories)"
            - "Option B ({count} stories)"
            - "Custom (I'll specify different split)"
            - "Cancel (keep original story)"
        multiSelect: false

    IF user approves split:
        FOR each child story in approved split:
            Task(
                subagent_type="requirements-analyst",
                description="Create child story from split",
                prompt="Create focused child story:

                        Parent Story: {current_story_id}
                        Child Title: {child_title}
                        Acceptance Criteria: {subset_criteria}
                        Story Points: {child_points}

                        Set:
                        - prerequisite_stories: [{current_story_id}]
                        - epic: {current_epic}
                        - sprint: Backlog (for future sprint)
                        - status: Backlog
                        - priority: {inherit from parent}

                        Return new story ID and file path."
            )

            new_story_id = extract from subagent
            Display: "✓ Created {new_story_id}: {child_title}"

        # Update current story with split references
        Edit current story Implementation Notes:
        Add: "Story split on {date} due to size ({deferred_count} deferrals)

              Child stories:
              - {new_story_1}: {title} ({points} points)
              - {new_story_2}: {title} ({points} points)

              Rationale: Reduce deferral chains, create focused stories"

        Display: "✓ Story split complete. Current story focused, {count} child stories created."

    ELSE:
        Display: "Split cancelled. Continuing with original story."
    ```

    **Option 3: "Accept as-is (document reason)"**
    ```
    AskUserQuestion:
        Question: "Provide reason for accepting {deferred_count} deferrals (>3 max):"
        Header: "Justification"
        # User provides free-form text
        # Example: "Legacy code refactor - inherently large scope"
        # Example: "Infrastructure story - many system touchpoints required"

    reason = user_input

    Edit current story Implementation Notes:
    Add: "## Story Size Exception

          Deferrals: {deferred_count} (exceeds recommended maximum of 3)

          Justification: {reason}

          Acknowledged: Story size accepted with documented reason"

    Display: "✓ Story size exception documented. Proceeding with {deferred_count} deferrals."
    ```

ENDIF (deferred_count > 3 check)
```

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

#### Step 1.5: Validate Deferrals (CRITICAL - Automated Quality Gate)

<automated_validation>
  <purpose>Prevent technical debt from unjustified deferrals</purpose>
  <trigger>Any DoD items marked [ ] (incomplete)</trigger>
  <enforcement>BLOCKS git commit on CRITICAL/HIGH violations</enforcement>
</automated_validation>

**Purpose:** Automated validation of deferral justifications before git commit

**IF any DoD items marked [ ] (incomplete):**

```
Task(
    subagent_type="deferral-validator",
    description="Validate deferral justifications",
    prompt="Validate all deferred Definition of Done items.

            Story already loaded in conversation.

            Check for:
            - Valid deferral reasons (format validation)
            - Technical blockers documented and verified
            - ADR for scope changes (exists and documents item)
            - Circular deferrals (story chains)
            - Referenced stories exist and include work
            - Implementation feasibility (could be done now?)

            Return JSON validation report with violations."
)

Parse validation results from subagent

IF validation returns CRITICAL or HIGH violations:
    <failure_condition>
      <severity>BLOCKING</severity>
      <action>HALT development - git commit forbidden</action>
      <resolution>Fix violations OR complete deferred work</resolution>
    </failure_condition>

    Display:
    "❌ Deferral Validation FAILED

    Violations detected:
    {list each CRITICAL and HIGH violation}

    You must fix these issues before git commit:
    1. Complete the work now (if feasible), OR
    2. Create proper justifications:
       - Create follow-up story (STORY-XXX)
       - Create ADR for scope change (ADR-XXX)
       - Document external blocker with ETA

    Run /dev {story_id} again to resolve deferral issues."

    HALT development
    DO NOT proceed to git commit
    User must fix deferrals first

ELSE IF validation returns only MEDIUM violations:
    <warning_condition>
      <severity>NON_BLOCKING</severity>
      <action>Warn user, allow commit to proceed</action>
    </warning_condition>

    Display:
    "⚠️ Deferral Validation WARNINGS

    Minor issues detected:
    {list MEDIUM violations}

    These won't block commit but should be addressed in future."

    Proceed to Step 2 (commit allowed)

ELSE:
    <success_condition>
      <result>All deferrals properly justified</result>
      <action>Proceed to git commit</action>
    </success_condition>

    Display: "✓ All deferrals validated - properly justified"
    Proceed to Step 2
```

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

## Handling QA Deferral Failures

**When invoked after QA failure due to deferrals:**

### Step 1: Detect QA Failure Context

**Check for QA report:**

```
Glob(pattern=".devforgeai/qa/reports/{story-id}-qa-report*.md")

IF multiple reports found (multiple QA attempts):
    Read most recent report

IF report status is "FAILED":
    Parse failure reasons

    IF failure includes "Deferral Validation FAILED":
        # This is a deferral-specific failure
        Extract deferral violations from report

        Display to user:
        "Previous QA attempt failed due to deferral issues:

         Unjustified Deferrals:
         1. '{item}': {violation_type}
            Current reason: '{reason}'
            Required: {required_action}

         2. '{item}': {violation_type}
            Current reason: '{reason}'
            Required: {required_action}

         Proceeding to resolve each deferral issue..."
```

### Step 2: Resolve Each Deferral Issue

```
FOR each deferral violation from QA report:
    AskUserQuestion:
        Question: "QA flagged deferral for '{item}'. How to resolve?"
        Header: "Deferral issue"
        Options:
            - "Complete the work now (implement {item})"
            - "Create follow-up story (proper tracking)"
            - "Create ADR (document scope change)"
            - "Document external blocker (with ETA)"
        multiSelect: false

    Based on user selection:
        Execute appropriate resolution (same as Phase 6 Step 1 logic)
        Update Implementation Notes with proper justification
```

### Step 3: Run Light QA to Verify Fixes

```
After resolving all deferral issues:
    Display: "Deferral issues resolved. Running light QA validation..."

    # Don't need full deep QA, just validate deferrals fixed
    Read updated Implementation Notes
    Verify all incomplete items now have valid justifications

    IF validation passes:
        Display: "Deferral issues resolved ✓ Ready for QA re-evaluation"
        Update story status remains "Dev Complete"

    ELSE:
        Display: "Some deferral issues remain. Please review."
        List remaining issues
```

**Trigger Conditions:**

This workflow triggered when:
- Story status is "Dev Complete" or "QA Failed"
- Previous QA report shows "Deferral Validation FAILED"
- User runs /dev {story-id} after QA failure

**Exit Criteria:**
- All deferral violations from QA report resolved
- Implementation Notes updated with valid justifications
- Ready for QA re-validation

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
- Documentation updates: ~5,000 tokens
- **DoD User Interaction: ~5,000 tokens** ← NEW (RCA-006 Rec 4)
  - Budgeted for AskUserQuestion dialogs (up to 3 deferrals)
  - Includes user response processing and justification documentation
  - Includes follow-up story/ADR creation via subagents

**Story Size Guideline (RCA-006 Rec 4):**

<story_size_constraint>
  <threshold>3 incomplete DoD items (deferrals)</threshold>
  <recommendation>If >3 deferrals detected, suggest story splitting</recommendation>
  <rationale>Excessive deferrals indicate story scope too large or poorly defined</rationale>
</story_size_constraint>

**If >3 deferrals:** Story likely too large, recommend splitting via requirements-analyst subagent

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
