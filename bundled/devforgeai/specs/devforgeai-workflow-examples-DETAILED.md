# DevForgeAI Workflow Examples: THE COMPLETE, DETAILED REALITY

**Document Purpose:** Show the ACTUAL detailed questioning and specification process - NOT "vibe coding"
**Date:** 2025-10-31
**Version:** 3.0 - COMPREHENSIVE DETAIL
**Replaces:** devforgeai-workflow-examples-CORRECTED.md (partial)

---

## ⚠️ CRITICAL: This Shows REALITY, Not Simplified Examples

**What users think DevForgeAI does (WRONG):**
```
User: "I want a todo app"
Claude: *makes tech stack assumptions*
Claude: *generates generic templates*
Result: "Vibe coding" with ambiguities
```

**What DevForgeAI ACTUALLY does (CORRECT):**
```
User: "I want a todo app"
Claude: *asks 23+ detailed questions*
Claude: *documents every decision*
Claude: *generates 3,000+ lines of specifications*
Result: ZERO ambiguity, fully specified system
```

**This document shows:**
- ✅ **EVERY AskUserQuestion invocation** (complete blocks, not summaries)
- ✅ **COMPLETE context file content** (full 500-800 line files, not excerpts)
- ✅ **FULL flowcharts** with every question as a decision node
- ✅ **ACTUAL time investment** (30 minutes to 5 hours of specification)
- ✅ **ACTUAL output volume** (3,000-12,000 lines of specifications)

**Document Length:** ~10,000 lines (necessary to show complete reality)

---

## Table of Contents

1. [Example 1: Simple CLI App - Todo List](#example-1-simple-cli-app---todo-list)
2. [Example 2: Mid-Size Desktop GUI - Expense Tracker](#example-2-mid-size-desktop-gui---expense-tracker)
3. [Example 3: Complex SaaS Platform - Project Management](#example-3-complex-saas-platform---project-management)
4. [Example 4: MVP Development - Meal Planning App](#example-4-mvp-development---meal-planning-app)
5. [Example 5: Post-MVP Enhancements - Adding Features After Launch](#example-5-post-mvp-enhancements---adding-features-after-launch)
6. [Comparison: "Vibe Coding" vs DevForgeAI Reality](#comparison-vibe-coding-vs-devforgeai-reality)
7. [Statistics & Analysis](#statistics--analysis)

---

# Example 1: Simple CLI App - Todo List

## Overview

**Project:** Command-line todo list application
**Complexity Score:** 8/60 (Simple Tier)
**Total Questions Asked:** 23 (10 ideation + 13 architecture)
**Context Files Generated:** 6 files, ~3,000 total lines
**Time Investment:** ~30-40 minutes of specification
**Development Time:** 2-3 hours (3 stories)
**Key Point:** Even "simple" apps get rigorous specification - NO guessing

---

## Phase 0: Ideation (devforgeai-ideation)

**User Input:**
```bash
/ideate CLI todo list app for personal productivity
```

### Question 1: Project Type

```javascript
AskUserQuestion(
  question: "What type of project is this?",
  header: "Project type",
  description: "Understanding project context helps determine appropriate architecture and patterns.",
  multiSelect: false,
  options: [
    {
      label: "Greenfield - New project/product from scratch",
      description: "Starting fresh with no existing codebase. Full freedom in technology choices."
    },
    {
      label: "Brownfield - Adding features to existing system",
      description: "Enhancing current application. Must work within existing architecture."
    },
    {
      label: "Modernization - Replacing/upgrading legacy system",
      description: "Migrating from old technology. May need to maintain compatibility."
    },
    {
      label: "Problem-solving - Fixing issues in current system",
      description: "Addressing technical debt or bugs in production system."
    }
  ]
)
```

**User Answer:** `"Greenfield - New project from scratch"`

**Rationale:** Starting fresh allows us to choose optimal tech stack without legacy constraints.

---

### Question 2: Business Problem

```javascript
AskUserQuestion(
  question: "What business problem are you trying to solve?",
  header: "Problem space",
  description: "Understanding the core problem helps scope features appropriately.",
  multiSelect: false,
  options: [
    {
      label: "Personal productivity",
      description: "Tool for individual use to improve personal efficiency and organization"
    },
    {
      label: "Team collaboration",
      description: "Multiple users working together, sharing resources and communicating"
    },
    {
      label: "Business process automation",
      description: "Streamline organizational workflows, reduce manual work"
    },
    {
      label: "Customer-facing solution",
      description: "Product for external users/customers, revenue-generating"
    }
  ]
)
```

**User Answer:** `"Personal productivity"`

**Rationale:** Single-user tool means simpler architecture (no multi-user, no authentication complexity).

---

### Question 3: Primary Users

```javascript
AskUserQuestion(
  question: "Who are the primary users or beneficiaries?",
  header: "User personas",
  description: "Identifying users helps determine features, UX patterns, and security requirements.",
  multiSelect: true,
  options: [
    {
      label: "End customers/consumers",
      description: "External paying customers using the product"
    },
    {
      label: "Internal employees",
      description: "Company staff members using for business operations"
    },
    {
      label: "Business partners/vendors",
      description: "External collaborators with controlled access"
    },
    {
      label: "Administrators/operators",
      description: "System administrators managing the platform"
    },
    {
      label: "Self (personal tool)",
      description: "Just for my own use, not shared"
    }
  ]
)
```

**User Answer:** `["Self (personal tool)"]`

**Rationale:** Single user = no user management, no permissions, no authentication needed.

---

### Question 4: Success Metrics

```javascript
AskUserQuestion(
  question: "What is the primary goal or success metric?",
  header: "Success criteria",
  description: "Clear success metrics help prioritize features and measure progress.",
  multiSelect: true,
  options: [
    {
      label: "Increase revenue/conversions",
      description: "Business growth focused, sales-driven metrics"
    },
    {
      label: "Reduce costs/inefficiency",
      description: "Operational efficiency, cost savings"
    },
    {
      label: "Improve user experience",
      description: "User satisfaction, engagement, retention"
    },
    {
      label: "Enable new capabilities",
      description: "Feature enablement, new workflows possible"
    },
    {
      label: "Compliance/regulatory requirement",
      description: "Legal/regulatory necessity, must-have for business"
    },
    {
      label: "Personal learning/productivity",
      description: "Individual benefit, skill development"
    }
  ]
)
```

**User Answer:** `["Personal learning/productivity"]`

**Rationale:** Success = improved personal task management, learning Python/CLI development.

---

### Question 5: MVP Scope

```javascript
AskUserQuestion(
  question: "What is the initial scope for the MVP or first release?",
  header: "Scope definition",
  description: "Defining MVP helps focus on core value and avoid scope creep.",
  multiSelect: false,
  options: [
    {
      label: "Core feature only (single user flow)",
      description: "Minimal viable functionality - e.g., add tasks, list tasks. ~1-2 weeks."
    },
    {
      label: "Core + 2-3 secondary features",
      description: "Basic feature set - e.g., add, list, edit, delete, search. ~4-6 weeks."
    },
    {
      label: "Full feature set (comprehensive solution)",
      description: "Complete functionality from start - all features. ~3-6 months."
    },
    {
      label: "Not sure - need help defining MVP",
      description: "Require guidance on scope and prioritization"
    }
  ]
)
```

**User Answer:** `"Core feature only (single user flow)"`

**Rationale:** MVP = add, list, complete tasks. Defer edit/delete/search to v2.

---

### Question 6: Core Capabilities (Domain-Specific)

```javascript
AskUserQuestion(
  question: "What core task management capabilities should the tool support?",
  header: "Feature selection",
  description: "Select all features needed for MVP. Additional features can be added later.",
  multiSelect: true,
  options: [
    {
      label: "Add tasks",
      description: "Create new tasks with description"
    },
    {
      label: "List tasks",
      description: "View all tasks (or filter by status)"
    },
    {
      label: "Complete tasks",
      description: "Mark tasks as done"
    },
    {
      label: "Edit tasks",
      description: "Modify existing task descriptions"
    },
    {
      label: "Delete tasks",
      description: "Remove tasks permanently"
    },
    {
      label: "Prioritize tasks",
      description: "Set priority levels (high, medium, low)"
    },
    {
      label: "Due dates",
      description: "Assign deadlines to tasks"
    },
    {
      label: "Categories/tags",
      description: "Organize tasks by category"
    },
    {
      label: "Search tasks",
      description: "Find tasks by keyword"
    }
  ]
)
```

**User Answer:** `["Add tasks", "List tasks", "Complete tasks"]`

**Rationale:** Core workflow = add → list → complete. Other features deferred to maintain MVP focus.

---

### Question 7: Data Persistence

```javascript
AskUserQuestion(
  question: "What data storage approach should be used?",
  header: "Storage mechanism",
  description: "Storage choice impacts performance, portability, and complexity.",
  multiSelect: false,
  options: [
    {
      label: "JSON file (local filesystem)",
      description: "Simple, portable, human-readable. No database needed. Best for <10k records."
    },
    {
      label: "SQLite (local database)",
      description: "SQL database, more query capabilities. Good for 10k-1M records."
    },
    {
      label: "PostgreSQL/MySQL (server database)",
      description: "Client-server, multi-user support. Requires database server installation."
    },
    {
      label: "Cloud database (Firebase, Supabase)",
      description: "Hosted, sync across devices. Requires internet connection."
    }
  ]
)
```

**User Answer:** `"JSON file (local filesystem)"`

**Rationale:** Simple CLI, <1000 tasks expected. JSON is portable, no database setup required.

---

### Question 8: Platform/Deployment

```javascript
AskUserQuestion(
  question: "What platform(s) should this CLI tool support?",
  header: "Target platforms",
  description: "Platform support affects language choice and testing requirements.",
  multiSelect: true,
  options: [
    {
      label: "Linux",
      description: "Linux distributions (Ubuntu, Fedora, Arch, etc.)"
    },
    {
      label: "macOS",
      description: "Apple macOS (Intel and Apple Silicon)"
    },
    {
      label: "Windows",
      description: "Windows 10/11"
    },
    {
      label: "WSL (Windows Subsystem for Linux)",
      description: "Linux environment on Windows (developers)"
    }
  ]
)
```

**User Answer:** `["Linux", "macOS", "Windows"]`

**Rationale:** Cross-platform support = wider usability. Python enables this easily.

---

### Question 9: Performance Requirements

```javascript
AskUserQuestion(
  question: "What are the performance requirements?",
  header: "Performance targets",
  description: "Performance requirements drive architecture decisions and optimization needs.",
  multiSelect: false,
  options: [
    {
      label: "High performance (<100ms response, >10k concurrent users)",
      description: "Real-time, high-traffic applications. Requires optimization, caching, load balancing."
    },
    {
      label: "Standard performance (<500ms response, 1k-10k users)",
      description: "Typical web application. Database indexing, basic caching."
    },
    {
      label: "Moderate performance (<2s response, <1k users)",
      description: "Internal tools, low traffic. Basic optimization sufficient."
    },
    {
      label: "Performance not critical (internal tool, low usage)",
      description: "Single-user or infrequent use. Simplicity over performance."
    }
  ]
)
```

**User Answer:** `"Performance not critical (single-user CLI)"`

**Rationale:** Single-user CLI, <1000 tasks. Any performance is acceptable (<100ms).

---

### Question 10: Security Requirements

```javascript
AskUserQuestion(
  question: "What security requirements apply?",
  header: "Security needs",
  description: "Security requirements determine authentication, encryption, and compliance measures.",
  multiSelect: true,
  options: [
    {
      label: "Authentication required (user login)",
      description: "Users must authenticate to access. Username/password, OAuth, SSO."
    },
    {
      label: "Authorization/role-based access control",
      description: "Different user permissions (admin, user, guest)"
    },
    {
      label: "Data encryption (at rest and in transit)",
      description: "Encrypted storage and transmission (TLS, AES-256)"
    },
    {
      label: "Compliance (GDPR, HIPAA, SOC2, PCI-DSS)",
      description: "Regulatory requirements with audit trails"
    },
    {
      label: "Audit logging",
      description: "Track all user actions for compliance/debugging"
    },
    {
      label: "Standard security practices",
      description: "Basic security hygiene (input validation, parameterized queries)"
    },
    {
      label: "No special security (personal tool)",
      description: "Minimal security requirements, local use only"
    }
  ]
)
```

**User Answer:** `["No special security (personal tool)"]`

**Rationale:** Local file storage, single user, no network access. Security not a concern.

---

### Complexity Assessment

**Ideation skill calculates complexity score:**

```markdown
## Complexity Assessment

### Functional Complexity (0-20 points)
- User roles: 1 (single user) = **2 points**
- Core entities: 1 (Task) = **2 points**
- Integrations: 0 (no external APIs) = **0 points**
- Workflow: Linear (add → list → complete) = **2 points**
**Subtotal: 6/20**

### Technical Complexity (0-20 points)
- Data volume: <1,000 tasks = **2 points**
- Concurrent users: 1 user = **2 points**
- Real-time: None (batch operations) = **0 points**
**Subtotal: 4/20**

### Team/Organizational Complexity (0-10 points)
- Team size: 1 developer = **1 point**
- Team distribution: N/A = **0 points**
**Subtotal: 1/10**

### Non-Functional Complexity (0-10 points)
- Performance: Not critical = **1 point**
- Compliance: None = **0 points**
**Subtotal: 1/10**

---

**TOTAL COMPLEXITY SCORE:** 12/60

**RECOMMENDED TIER:** Tier 1: Simple Application

**RATIONALE:**
- Single user, single entity, no integrations
- Linear workflow, minimal data volume
- Solo developer, no compliance
- Simple architecture appropriate: Single file, no layers, JSON storage
```

---

### Epic Generation

**Ideation skill generates epic:**

```markdown
# EPIC-001: Personal Todo CLI

**ID:** EPIC-001
**Title:** Personal Todo CLI Tool
**Status:** DRAFT
**Created:** 2025-10-31
**Estimated Points:** 8

## Business Goal

Enable personal task management through simple, cross-platform command-line interface.

## Success Metrics

- **Primary:** Can add, list, and complete tasks in <100ms per operation
- **Secondary:** Works on Linux, macOS, Windows without installation complexity
- **Learning:** Understand CLI patterns, file I/O, testing in Python

## Features Breakdown

### Feature 1: Add Tasks (STORY-001)
- CLI command: `todo add "Buy milk"`
- Assigns unique ID to each task
- Stores in JSON file
- **Estimated:** 3 points

### Feature 2: List Tasks (STORY-002)
- CLI command: `todo list`
- Shows all tasks (or filter by status)
- Format: ID, Description, Status
- **Estimated:** 2 points

### Feature 3: Complete Tasks (STORY-003)
- CLI command: `todo complete 1`
- Marks task as done
- Updates JSON file
- **Estimated:** 3 points

## Technical Considerations

- **Architecture:** Simple (Tier 1) - single file
- **Storage:** JSON file in user's home directory
- **Platform:** Cross-platform Python 3.11+
- **Testing:** pytest with >90% coverage

## Risks

- None (simple project)

## Next Steps

1. Create architecture context files (tech-stack.md, etc.)
2. Generate stories with detailed acceptance criteria
3. Begin development with TDD approach
```

**Epic document location:** `devforgeai/specs/Epics/EPIC-001-todo-cli.epic.md`

---

### Requirements Specification

**Ideation skill generates requirements document:**

```markdown
# Requirements Specification: Todo CLI

**Project:** Todo CLI Tool
**Date:** 2025-10-31
**Status:** APPROVED
**Complexity:** 12/60 (Simple Tier)

## 1. Project Context

### 1.1 Project Type
**Greenfield** - New project from scratch

### 1.2 Business Problem
Personal productivity tool for managing daily tasks via command line.

### 1.3 User Personas
- **Primary:** Solo developer/power user comfortable with terminal
- **Age:** 25-45
- **Technical skill:** Intermediate to advanced (uses CLI tools daily)

### 1.4 Success Criteria
- Add/list/complete tasks in <100ms
- Cross-platform (Linux, macOS, Windows)
- Zero setup complexity (single executable)
- Learning Python CLI development patterns

## 2. Functional Requirements

### FR-001: Add Tasks
**Priority:** MUST-HAVE (MVP)
**Description:** User can add task with description

**Acceptance Criteria:**
- Given user runs `todo add "Buy milk"`
- When command executes
- Then task is created with unique ID
- And task is stored in JSON file
- And success message shown: "✅ Added task #1: Buy milk"

**Business Rules:**
- Description is required (min 1 character, max 500 characters)
- Duplicate descriptions are allowed (different IDs)
- Task auto-assigned status "pending"
- Task auto-assigned creation timestamp

### FR-002: List Tasks
**Priority:** MUST-HAVE (MVP)
**Description:** User can view all tasks

**Acceptance Criteria:**
- Given user runs `todo list`
- When command executes
- Then all tasks displayed in table format:
  ```
  ID | Description        | Status    | Created
  ---|--------------------|-----------|---------
  1  | Buy milk           | pending   | 2025-10-31
  2  | Walk dog           | complete  | 2025-10-31
  ```
- And tasks sorted by ID (oldest first)

**Business Rules:**
- Empty list shows message: "No tasks yet. Use 'todo add' to create one."
- Completed tasks shown with strikethrough (if terminal supports)

### FR-003: Complete Tasks
**Priority:** MUST-HAVE (MVP)
**Description:** User can mark task as complete

**Acceptance Criteria:**
- Given user runs `todo complete 1`
- When task ID exists
- Then task status updated to "complete"
- And JSON file updated
- And success message: "✅ Completed task #1: Buy milk"

- Given user runs `todo complete 999` (non-existent ID)
- When task ID doesn't exist
- Then error message: "❌ Task #999 not found"
- And exit code 1

**Business Rules:**
- Can complete same task multiple times (idempotent)
- Completing completed task shows: "Task #1 already complete"

### FR-004: Edit Tasks (DEFERRED to v2)
**Priority:** SHOULD-HAVE (post-MVP)
### FR-005: Delete Tasks (DEFERRED to v2)
**Priority:** SHOULD-HAVE (post-MVP)
### FR-006: Search Tasks (DEFERRED to v2)
**Priority:** COULD-HAVE (post-MVP)

## 3. Non-Functional Requirements

### NFR-001: Performance
- **Target:** <100ms per command execution
- **Rationale:** CLI commands should feel instant
- **Measurement:** pytest benchmark tests

### NFR-002: Portability
- **Target:** Works on Linux, macOS, Windows without code changes
- **Rationale:** Cross-platform usability
- **Verification:** CI/CD tests on all 3 platforms

### NFR-003: Reliability
- **Target:** Zero data loss, even if command interrupted
- **Strategy:** Atomic file writes (write to temp, then rename)
- **Verification:** Kill-signal tests in pytest

### NFR-004: Usability
- **Target:** Clear error messages, helpful --help output
- **Strategy:** Use Click framework's built-in help generation
- **Verification:** Manual UX review

### NFR-005: Maintainability
- **Target:** >90% test coverage, <10 cyclomatic complexity per function
- **Strategy:** TDD with pytest, Ruff linting
- **Verification:** Coverage reports in CI/CD

## 4. Data Requirements

### 4.1 Data Entities

**Task Entity:**
```json
{
  "id": 1,
  "description": "Buy milk",
  "status": "pending",
  "created_at": "2025-10-31T10:30:00Z"
}
```

**Field Specifications:**
- `id`: Integer, auto-increment, primary key
- `description`: String, required, 1-500 characters
- `status`: Enum ["pending", "complete"], default "pending"
- `created_at`: ISO 8601 timestamp (UTC)

### 4.2 Data Storage

**Format:** JSON file
**Location:** `~/.local/share/todo/todo.json` (XDG Base Directory spec)
**Structure:**
```json
{
  "next_id": 3,
  "tasks": [
    { "id": 1, "description": "...", "status": "...", "created_at": "..." },
    { "id": 2, "description": "...", "status": "...", "created_at": "..." }
  ]
}
```

**Concurrency:** Not applicable (single-user)
**Backup:** User responsibility (file is in standard location)

## 5. Integration Requirements

**None** - Fully self-contained application

## 6. Constraints

- **Technology:** Python 3.11+ (must support type hints)
- **Dependencies:** Minimize external dependencies (Click framework only)
- **Installation:** Single command: `pip install todo-cli`
- **File size:** <1 MB executable

## 7. Assumptions

- User has Python 3.11+ installed
- User comfortable with command-line interface
- User manages <10,000 tasks (JSON file performance sufficient)
- User's filesystem supports POSIX file locking (Windows/Mac/Linux)

## 8. Architecture Recommendation

**Tier 1: Simple Application**
- **Pattern:** Single file (todo.py)
- **Layers:** None (functions organized logically)
- **Storage:** JSON file with atomic writes
- **Testing:** pytest with >90% coverage

**Rationale:** Complexity score 12/60 = Simple tier. Over-engineering would add unnecessary complexity.

## 9. Next Steps

1. **Invoke devforgeai-architecture:** Create 6 context files
2. **Invoke devforgeai-orchestration:** Generate Sprint 1, create 3 stories
3. **Begin development:** STORY-001 (Add tasks) with TDD
```

**Requirements document location:** `devforgeai/specs/requirements/todo-cli-requirements.md`

---

### Ideation Phase Complete

**Output Artifacts:**
- 📄 `devforgeai/specs/Epics/EPIC-001-todo-cli.epic.md` (Epic document)
- 📄 `devforgeai/specs/requirements/todo-cli-requirements.md` (Requirements spec)

**Questions Asked:** 10
**Time Taken:** ~15-20 minutes
**Ambiguities Remaining:** 0 (all resolved via questioning)

**Next Step:** Invoke devforgeai-architecture skill to create context files

---

## Phase 1: Architecture (devforgeai-architecture)

**User Input:**
```bash
/create-context todo-cli
```

**Architecture skill reads requirements:**
```
Read(file_path="devforgeai/specs/requirements/todo-cli-requirements.md")
```

**Architecture skill begins technology decisions...**

---

### Question 11: Backend Language

```javascript
AskUserQuestion(
  question: "What backend technology stack should this project use?",
  header: "Backend language",
  description: "Language choice is LOCKED once selected. Cannot be changed without ADR.",
  multiSelect: false,
  options: [
    {
      label: "C# with .NET 8.0",
      description: "Strongly typed, mature ecosystem, cross-platform. Best for: Enterprise apps, Windows-first."
    },
    {
      label: "Python with FastAPI",
      description: "Fast, modern, type hints, async support. Best for: Web APIs, data science integration."
    },
    {
      label: "Python (CLI only, no web framework)",
      description: "Simple scripts, standard library focused. Best for: CLI tools, automation."
    },
    {
      label: "Node.js with Express",
      description: "JavaScript, large ecosystem, async by default. Best for: Full-stack JS, real-time."
    },
    {
      label: "Go",
      description: "Compiled, fast, simple concurrency. Best for: Microservices, CLI tools."
    },
    {
      label: "Rust",
      description: "Memory safe, blazing fast, steep learning curve. Best for: Systems programming, performance-critical."
    }
  ]
)
```

**User Answer:** `"Python (CLI only, no web framework)"`

**Rationale:** CLI tool, no web server needed. Python = cross-platform, simple deployment, rich CLI libraries.

---

### Question 12: CLI Framework

```javascript
AskUserQuestion(
  question: "Which CLI framework should be used for command-line interface?",
  header: "CLI framework",
  description: "⚠️ CRITICAL: This choice will be LOCKED in tech-stack.md. AI agents cannot use alternatives without ADR approval.",
  multiSelect: false,
  options: [
    {
      label: "Click",
      description: "Composable, decorator-based, popular choice. Mature, well-documented. ~12k GitHub stars."
    },
    {
      label: "Typer",
      description: "Type-hint based, built on Click, modern. Better type safety. ~15k GitHub stars."
    },
    {
      label: "argparse",
      description: "Python standard library, no dependencies. More boilerplate, less ergonomic."
    },
    {
      label: "Fire",
      description: "Auto-generates CLI from code, minimal boilerplate. Less explicit control."
    }
  ]
)
```

**User Answer:** `"Click"`

**Rationale:** Mature, decorator-based (clean syntax), composable commands, excellent documentation.

---

### Question 13: Path Library

```javascript
AskUserQuestion(
  question: "Which approach for file path handling?",
  header: "Path library",
  description: "Path handling affects cross-platform compatibility and code readability.",
  multiSelect: false,
  options: [
    {
      label: "pathlib (modern, OOP, Python 3.4+)",
      description: "Recommended modern approach. Object-oriented, cross-platform, type-safe."
    },
    {
      label: "os.path (classic, functional)",
      description: "Traditional Python approach. Functional API, more verbose."
    }
  ]
)
```

**User Answer:** `"pathlib (modern)"`

**Rationale:** Modern Python standard, OOP approach, handles Windows/Unix differences automatically.

---

### Question 14: JSON Library

```javascript
AskUserQuestion(
  question: "For JSON file handling, which library?",
  header: "JSON library",
  description: "JSON library affects performance and feature set.",
  multiSelect: false,
  options: [
    {
      label: "json (standard library)",
      description: "Built-in, no dependencies, sufficient for simple use. ~1x speed baseline."
    },
    {
      label: "orjson (faster, more features)",
      description: "3-5x faster, handles more data types (datetime, UUID). Requires C extension."
    },
    {
      label: "ujson (ultra-fast)",
      description: "C-based, very fast. Less feature-complete than orjson."
    }
  ]
)
```

**User Answer:** `"json (standard library)"`

**Rationale:** No performance concerns (<1000 tasks), avoid unnecessary dependencies.

---

### Question 15: Testing Framework

```javascript
AskUserQuestion(
  question: "Which testing framework should be used?",
  header: "Test framework",
  description: "⚠️ LOCKED: All tests must use chosen framework for consistency.",
  multiSelect: false,
  options: [
    {
      label: "pytest",
      description: "Most popular, fixture-based, rich plugin ecosystem. Simple assert statements. Industry standard."
    },
    {
      label: "unittest",
      description: "Python standard library, no dependencies. More verbose (self.assertEqual). xUnit style."
    },
    {
      label: "nose2",
      description: "Extends unittest, more features. Less popular, smaller ecosystem."
    }
  ]
)
```

**User Answer:** `"pytest"`

**Rationale:** Industry standard, simple syntax (`assert x == y`), fixture system, rich plugins.

---

### Question 16: Code Formatter

```javascript
AskUserQuestion(
  question: "Which code formatter should be enforced?",
  header: "Formatter",
  description: "Formatter will be enforced via pre-commit hooks. Non-negotiable once selected.",
  multiSelect: false,
  options: [
    {
      label: "Black (opinionated, zero config)",
      description: "Automatic formatting, no debates. 88-char lines. Industry standard. 'Any color as long as it's black.'"
    },
    {
      label: "autopep8 (PEP 8 compliant)",
      description: "Follows PEP 8 style guide. More configurable than Black."
    },
    {
      label: "YAPF (Google style)",
      description: "Configurable, Google's formatter. More knobs to tune."
    },
    {
      label: "None (manual formatting)",
      description: "No automatic formatting. Rely on developer discipline."
    }
  ]
)
```

**User Answer:** `"Black"`

**Rationale:** Zero configuration, no formatting debates, widely adopted, enforced via pre-commit.

---

### Question 17: Linting

```javascript
AskUserQuestion(
  question: "Which linting tool should be used?",
  header: "Linter",
  description: "Linter will catch bugs, style issues, and enforce conventions.",
  multiSelect: false,
  options: [
    {
      label: "Ruff (fast, modern, replaces many tools)",
      description: "10-100x faster than alternatives. Replaces Flake8, isort, pydocstyle. Rust-based, very fast."
    },
    {
      label: "Pylint (comprehensive, strict)",
      description: "Thorough code analysis, many rules. Slower. More opinionated."
    },
    {
      label: "Flake8 (popular, extensible)",
      description: "Plugin-based, widely used. Moderate speed. Combines PyFlakes, pycodestyle, mccabe."
    },
    {
      label: "None (no linting)",
      description: "Skip linting step. Not recommended."
    }
  ]
)
```

**User Answer:** `"Ruff"`

**Rationale:** 10-100x faster than alternatives, replaces multiple tools (Flake8+isort), modern Rust-based.

---

### Question 18: Type Checking

```javascript
AskUserQuestion(
  question: "Should type checking be enforced?",
  header: "Type checking",
  description: "Type checking catches bugs at development time, improves code documentation.",
  multiSelect: false,
  options: [
    {
      label: "mypy (strict type checking)",
      description: "Enforces type hints, catches type errors. Industry standard. Strict mode = zero ambiguity."
    },
    {
      label: "pyright (Microsoft's type checker)",
      description: "Fast, comprehensive. Used by VS Code. More aggressive than mypy."
    },
    {
      label: "No type checking",
      description: "Type hints for documentation only. Not enforced."
    }
  ]
)
```

**User Answer:** `"mypy (strict type checking)"`

**Rationale:** Catch type errors early, enforce type hints on all functions, improve maintainability.

---

### Question 19: Dependency Management

```javascript
AskUserQuestion(
  question: "Which dependency management approach?",
  header: "Dependencies",
  description: "Dependency management affects installation, reproducibility, and packaging.",
  multiSelect: false,
  options: [
    {
      label: "pyproject.toml (modern Python standard)",
      description: "PEP 518, single config file, future-proof. Used by Poetry, PDM, Hatch. Recommended."
    },
    {
      label: "requirements.txt (traditional)",
      description: "Simple, widely supported. No dev dependencies separation. Legacy approach."
    },
    {
      label: "Poetry (advanced dependency management)",
      description: "Dependency resolution, virtual envs, packaging. More complex, slower."
    },
    {
      label: "Pipenv (pipfile-based)",
      description: "Virtual envs, Pipfile + Pipfile.lock. Less popular now."
    }
  ]
)
```

**User Answer:** `"pyproject.toml (modern standard)"`

**Rationale:** Modern Python standard (PEP 518), single config file, works with pip, future-proof.

---

### Question 20: Architecture Pattern

```javascript
AskUserQuestion(
  question: "Which backend architecture pattern should be used?",
  header: "Architecture",
  description: "Architecture pattern determines code organization and complexity.",
  multiSelect: false,
  options: [
    {
      label: "Clean Architecture (Domain/Application/Infrastructure)",
      description: "Complex layering, dependency inversion. Best for: Large teams, complex domains. Overkill for simple CLI."
    },
    {
      label: "N-Tier (Presentation/Business/Data)",
      description: "Traditional layering. Best for: Medium apps, web applications."
    },
    {
      label: "Simple layered (minimal structure)",
      description: "Basic organization, suitable for simple apps. Functions grouped by purpose."
    },
    {
      label: "Single file (no layers)",
      description: "Everything in one file, appropriate for CLIs <500 lines. Simplest approach."
    }
  ]
)
```

**User Answer:** `"Single file (no layers)"`

**Rationale:** Simple CLI, ~300 lines of code expected. Single file keeps it simple, easy to understand.

---

### Question 21: Test Organization

```javascript
AskUserQuestion(
  question: "How should tests be organized?",
  header: "Test structure",
  description: "Test organization affects discoverability and maintainability.",
  multiSelect: false,
  options: [
    {
      label: "Mirror source structure (tests/test_todo.py mirrors todo.py)",
      description: "Test structure matches source structure. Easy to find tests."
    },
    {
      label: "Separate by test type (tests/unit/, tests/integration/)",
      description: "Organized by test level. Run unit tests separately."
    },
    {
      label: "Co-located with source (same directory as code)",
      description: "Tests next to implementation. Less common in Python."
    }
  ]
)
```

**User Answer:** `"Mirror source structure"`

**Rationale:** Single file app → single test file. Simple 1:1 mapping.

---

### Question 22: Documentation Style

```javascript
AskUserQuestion(
  question: "What documentation style should be used for docstrings?",
  header: "Docstrings",
  description: "Docstring style affects readability and tool compatibility (Sphinx, pydoc).",
  multiSelect: false,
  options: [
    {
      label: "Google style",
      description: "Args, Returns, Raises sections. Readable, widely used. Supported by Sphinx."
    },
    {
      label: "NumPy style",
      description: "Scientific Python convention. More verbose, better for complex signatures."
    },
    {
      label: "reStructuredText (Sphinx)",
      description: "Detailed, Sphinx-compatible. More markup, harder to read plain."
    },
    {
      label: "Minimal (one-line descriptions)",
      description: "Brief comments only. Not recommended for public APIs."
    }
  ]
)
```

**User Answer:** `"Google style"`

**Rationale:** Readable, widely adopted, good Sphinx support, clear Args/Returns/Raises sections.

---

### Question 23: Error Handling Strategy

```javascript
AskUserQuestion(
  question: "How should errors be handled in this CLI?",
  header: "Error handling",
  description: "Error handling affects user experience and debugging.",
  multiSelect: false,
  options: [
    {
      label: "User-friendly messages (hide stack traces)",
      description: "Clean error messages for end users. Stack traces hidden. Exit with error codes."
    },
    {
      label: "Detailed exceptions with stack traces",
      description: "Full debug information shown. Better for developers, scary for users."
    },
    {
      label: "Silent failures with exit codes",
      description: "No messages, just exit codes. Good for scripting, bad for interactive use."
    }
  ]
)
```

**User Answer:** `"User-friendly messages"`

**Rationale:** End-user tool, not developer tool. Hide scary stack traces, show helpful error messages.

---

### Architecture Questions Complete

**Questions Asked:** 13 (in addition to 10 ideation questions)
**Total Questions So Far:** 23
**Time Taken:** ~10-15 minutes
**Next Step:** Generate 6 context files with ALL decisions documented

---

## Context Files Generated (COMPLETE CONTENT)

### File 1: tech-stack.md (500 lines)

```markdown
# Technology Stack - Todo CLI

**Created:** 2025-10-31
**Status:** 🔒 LOCKED - These choices are immutable without ADR approval
**Project:** Todo CLI Tool (Personal Productivity)
**Complexity:** Simple (Tier 1)

---

## Executive Summary

This document defines the LOCKED technology stack for the Todo CLI project. All choices documented here are **immutable** and cannot be changed without creating an Architecture Decision Record (ADR) and obtaining approval.

**Key Decisions:**
- Language: Python 3.11+
- CLI Framework: Click 8.1.0+ (LOCKED)
- Storage: JSON file with pathlib
- Testing: pytest 7.4.3+ (LOCKED)
- Code Quality: Black, Ruff, mypy (ENFORCED)

---

## 1. Language & Runtime

### Python
- **Version:** Python 3.11+ (REQUIRED)
- **Reason:**
  - Cross-platform (Linux, macOS, Windows)
  - Rich standard library (json, pathlib, datetime)
  - Simple deployment (single .py file or pip install)
  - Type hints (PEP 484) for type safety
  - Mature CLI ecosystem (Click framework)
- **Installation:** https://www.python.org/downloads/
- **Verification:** `python --version` must show 3.11.0 or higher

**CRITICAL RULE:** All new code MUST use Python 3.11+ features. Do NOT use:
- ❌ Python 2.x syntax (deprecated, security risks)
- ❌ Python 3.9 and below (missing modern features)
- ❌ `from __future__ import annotations` (not needed in 3.11+)

**Type Checking:** mypy strict mode (ENFORCED)
- All functions MUST have type annotations
- No `Any` types without justification
- No implicit Optional (strict-optional enabled)

**Why Python (ADR-001 excerpt):**
> Python was chosen over Go/Rust/C# for the following reasons:
> 1. **Cross-platform:** Single codebase works on Linux/Mac/Windows without compilation
> 2. **Rapid development:** Appropriate for simple CLI tool (Tier 1 complexity)
> 3. **Rich ecosystem:** Click framework for CLI, pytest for testing
> 4. **Type safety:** Modern type hints provide compile-time checking
> 5. **Deployment:** Simple pip install or single file distribution

**Alternatives Considered:**
- ❌ **Go:** Overkill for simple tool. Compiled binaries nice but unnecessary.
- ❌ **Rust:** Steep learning curve, over-engineering for Tier 1 app.
- ❌ **C#/.NET:** Windows-first, heavier runtime, less CLI-friendly.

---

## 2. Core Libraries

### 2.1 CLI Framework: Click

- **Library:** click
- **Version:** >=8.1.0,<9.0.0 (LOCKED to 8.x major version)
- **Purpose:** Command-line interface and argument parsing
- **Installation:** `pip install "click>=8.1.0,<9.0.0"`
- **Documentation:** https://click.palletsprojects.com/

**Why Click (ADR-002 excerpt):**
> Click was chosen for CLI framework over alternatives:
> 1. **Decorator-based:** Clean syntax with @click.command, @click.argument
> 2. **Composable:** Commands, groups, sub-commands easy to compose
> 3. **Automatic help:** Generates --help from decorators
> 4. **Mature:** 12k+ GitHub stars, 10+ years development
> 5. **Testing support:** click.testing.CliRunner for integration tests

**CRITICAL RULE:** ALL CLI commands MUST use Click decorators. Do NOT use:
- ❌ `argparse` (less ergonomic for complex CLIs)
- ❌ `sys.argv` parsing (error-prone, no help generation)
- ❌ `Typer` (alternative framework, would create inconsistency)
- ❌ `Fire` (magic behavior, less explicit)

**Example Usage:**
```python
import click

@click.command()
@click.argument('description')
@click.option('--priority', default='medium', help='Task priority')
def add(description: str, priority: str) -> None:
    """Add a new task to the todo list."""
    # implementation
```

**PROHIBITED:**
- ❌ Typer (different API, incompatible patterns)
- ❌ argparse (standard library, but inconsistent with Click)
- ❌ Fire (Google's library, auto-generates CLI - less control)
- ❌ Docopt (docstring-based, less type-safe)

**If you need a feature Click doesn't support:**
1. Check Click plugins: https://github.com/click-contrib
2. If still missing, create ADR proposing alternative
3. Update tech-stack.md after approval
4. Do NOT add alternative CLI framework silently

---

### 2.2 File I/O: pathlib

- **Library:** pathlib (Python standard library)
- **Version:** Built-in to Python 3.4+
- **Purpose:** Cross-platform file path handling
- **Documentation:** https://docs.python.org/3/library/pathlib.html

**Why pathlib:**
- Object-oriented API (Path objects, not strings)
- Cross-platform (handles Windows \\ vs Unix / automatically)
- Type-safe (Path type distinct from str)
- Modern Python standard (recommended over os.path)

**CRITICAL RULE:** ALL file paths MUST use `pathlib.Path` objects. Do NOT use:
- ❌ String concatenation: `"/home/user" + "/" + "file.txt"`
- ❌ os.path functions: `os.path.join()`, `os.path.exists()`
- ❌ Manual path separators: `"C:\\Users\\..."` or `"/home/..."`

**Example Usage:**
```python
from pathlib import Path

# ✅ CORRECT
todo_dir = Path.home() / ".local" / "share" / "todo"
todo_file = todo_dir / "todo.json"
if todo_file.exists():
    data = todo_file.read_text()

# ❌ WRONG
todo_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "todo")
todo_file = os.path.join(todo_dir, "todo.json")
if os.path.exists(todo_file):
    with open(todo_file, "r") as f:
        data = f.read()
```

**PROHIBITED:**
- ❌ os.path module (functional approach, less readable)
- ❌ String path manipulation (not cross-platform)

---

### 2.3 Data Serialization: json

- **Library:** json (Python standard library)
- **Version:** Built-in to Python
- **Purpose:** JSON file read/write for task storage
- **Documentation:** https://docs.python.org/3/library/json.html

**Why json (standard library):**
- No dependencies (built-in to Python)
- Sufficient performance (<1000 tasks, <1ms read/write)
- Human-readable format (users can edit todo.json manually)
- Simple API (json.dump, json.load)

**CRITICAL RULE:** Task data MUST be stored as JSON. Do NOT use:
- ❌ pickle (binary format, security risks, not human-readable)
- ❌ CSV (poor structure for nested data)
- ❌ XML (verbose, over-engineered for simple data)
- ❌ Custom text format (reinventing wheel)

**Example Usage:**
```python
import json
from pathlib import Path
from typing import List, Dict, Any

# ✅ CORRECT
def load_tasks(file_path: Path) -> List[Dict[str, Any]]:
    if not file_path.exists():
        return []
    data = json.loads(file_path.read_text())
    return data["tasks"]

def save_tasks(file_path: Path, tasks: List[Dict[str, Any]]) -> None:
    data = {"next_id": len(tasks) + 1, "tasks": tasks}
    file_path.write_text(json.dumps(data, indent=2))
```

**PROHIBITED:**
- ❌ orjson (unnecessary performance dependency for CLI use)
- ❌ ujson (no significant benefit, adds dependency)
- ❌ simplejson (standard library json is sufficient)

**If JSON becomes performance bottleneck (>10,000 tasks):**
1. Create ADR proposing SQLite migration
2. Document why JSON insufficient (specific performance metrics)
3. Update tech-stack.md after approval
4. Do NOT add orjson/ujson as band-aid solution

---

## 3. Development Tools

### 3.1 Testing Framework: pytest

- **Library:** pytest
- **Version:** >=7.4.3,<8.0.0 (LOCKED to 7.x)
- **Purpose:** Unit and integration testing
- **Installation:** `pip install "pytest>=7.4.3,<8.0.0"`
- **Documentation:** https://docs.pytest.org/

**Plugins (APPROVED):**
- pytest-cov>=4.1.0 (coverage reporting)
- pytest-mock>=3.12.0 (mocking utilities)
- pytest-benchmark>=4.0.0 (performance testing)

**Why pytest (ADR-003 excerpt):**
> pytest was chosen over unittest/nose2:
> 1. **Simple syntax:** `assert x == y` (not `self.assertEqual(x, y)`)
> 2. **Fixtures:** Powerful setup/teardown with dependency injection
> 3. **Plugins:** Rich ecosystem (coverage, mocking, benchmarking)
> 4. **Parameterization:** Easy to test multiple inputs
> 5. **Industry standard:** Most popular Python test framework

**CRITICAL RULE:** All tests MUST use pytest. Do NOT use:
- ❌ unittest (standard library, but verbose API)
- ❌ nose2 (deprecated, less popular)
- ❌ doctest (insufficient for real testing)

**Example Usage:**
```python
import pytest
from pathlib import Path
from todo import add_task, load_tasks

@pytest.fixture
def todo_file(tmp_path: Path) -> Path:
    """Provide isolated todo.json for each test."""
    return tmp_path / "todo.json"

def test_should_add_task_when_valid_description(todo_file: Path):
    # Arrange
    description = "Buy milk"

    # Act
    task = add_task(todo_file, description)

    # Assert
    assert task["description"] == "Buy milk"
    assert task["status"] == "pending"
    assert task["id"] == 1

def test_should_raise_error_when_empty_description(todo_file: Path):
    # Arrange
    description = ""

    # Act & Assert
    with pytest.raises(ValueError, match="Description required"):
        add_task(todo_file, description)
```

**Coverage Requirements (ENFORCED):**
- **Minimum:** 90% overall coverage
- **Business logic:** 100% coverage (all functions in todo.py)
- **Exclusions:** Only `if __name__ == "__main__"` blocks

**Enforcement:**
```bash
pytest --cov=todo --cov-report=term-missing --cov-fail-under=90
```

---

### 3.2 Code Formatter: Black

- **Library:** black
- **Version:** >=23.11.0,<24.0.0 (LOCKED)
- **Purpose:** Automatic code formatting
- **Installation:** `pip install "black>=23.11.0,<24.0.0"`
- **Documentation:** https://black.readthedocs.io/

**Configuration:** Default settings (ZERO configuration)
- Line length: 88 characters (non-negotiable)
- String quotes: Double quotes (non-negotiable)
- Trailing commas: Yes (multi-line structures)

**Why Black (ADR-004 excerpt):**
> Black was chosen for zero-configuration formatting:
> 1. **Zero debates:** No arguments about style ("any color as long as it's black")
> 2. **Deterministic:** Same input always produces same output
> 3. **Fast:** Written in Python, fast enough for CLI tool
> 4. **Widely adopted:** Industry standard Python formatter

**CRITICAL RULE:** Code MUST be Black-formatted before commit. No exceptions.

**Enforcement:**
- Pre-commit hook: `black --check todo.py tests/`
- CI/CD: `black --check .` (fails build if not formatted)

**Example:**
```bash
# Format code
black todo.py tests/

# Check formatting without changing files
black --check todo.py tests/
```

**PROHIBITED:**
- ❌ autopep8 (more configurable = more arguments)
- ❌ YAPF (Google's formatter, different style)
- ❌ Manual formatting (inconsistent, error-prone)

**Line Length Rationale:**
88 characters is Black's default. Do NOT change to 79 (PEP 8) or 120 (some projects).
> "88 characters is plenty, and it's a prime number which makes it memorable." - Black docs

---

### 3.3 Linter: Ruff

- **Library:** ruff
- **Version:** >=0.1.0,<1.0.0 (LOCKED)
- **Purpose:** Fast Python linter (replaces Flake8, isort, etc.)
- **Installation:** `pip install "ruff>=0.1.0,<1.0.0"`
- **Documentation:** https://docs.astral.sh/ruff/

**Rules Enabled:**
- E (pycodestyle errors)
- F (pyflakes)
- I (isort - import sorting)
- N (pep8-naming)

**Why Ruff:**
- **10-100x faster** than Flake8/Pylint (Rust-based)
- **All-in-one:** Replaces Flake8 + isort + pyupgrade + more
- **Compatible:** Drop-in replacement for Flake8
- **Modern:** Active development, fast adoption

**Configuration (pyproject.toml):**
```toml
[tool.ruff]
line-length = 88  # Match Black
select = ["E", "F", "I", "N"]
ignore = []
target-version = "py311"
```

**CRITICAL RULE:** Code MUST pass Ruff checks before commit.

**Enforcement:**
- Pre-commit hook: `ruff check todo.py tests/`
- CI/CD: `ruff check .` (fails build on any error)

**Example:**
```bash
# Check code
ruff check todo.py tests/

# Auto-fix issues (safe fixes only)
ruff check --fix todo.py tests/
```

**PROHIBITED:**
- ❌ Flake8 (slower, requires multiple plugins)
- ❌ Pylint (much slower, more opinionated)
- ❌ No linting (technical debt accumulates)

---

### 3.4 Type Checker: mypy

- **Library:** mypy
- **Version:** >=1.7.0,<2.0.0 (LOCKED)
- **Purpose:** Static type checking
- **Installation:** `pip install "mypy>=1.7.0,<2.0.0"`
- **Documentation:** https://mypy.readthedocs.io/

**Mode:** Strict (strict = true)

**Configuration (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
show_error_codes = true
```

**Why mypy strict mode:**
- **Catch bugs early:** Type errors found before runtime
- **Documentation:** Type hints serve as inline documentation
- **Refactoring safety:** Changes won't break type contracts
- **Industry standard:** mypy is de facto Python type checker

**CRITICAL RULE:** All functions MUST have type annotations. mypy must pass with zero errors.

**Example:**
```python
# ✅ CORRECT (all types annotated)
from typing import List, Dict, Any
from pathlib import Path

def add_task(file_path: Path, description: str) -> Dict[str, Any]:
    """Add a new task to the todo list."""
    tasks = load_tasks(file_path)
    new_task = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(file_path, tasks)
    return new_task

def load_tasks(file_path: Path) -> List[Dict[str, Any]]:
    """Load tasks from JSON file."""
    if not file_path.exists():
        return []
    # implementation
    return []

# ❌ WRONG (missing type annotations)
def add_task(file_path, description):  # mypy error: missing types
    pass
```

**Enforcement:**
- Pre-commit hook: `mypy todo.py tests/`
- CI/CD: `mypy .` (fails build on any error)

**PROHIBITED:**
- ❌ pyright (Microsoft's checker, different rules)
- ❌ No type checking (loses type safety benefits)
- ❌ Type: ignore comments (defeats purpose, avoid except for 3rd-party libs)

---

## 4. Dependency Management

**Tool:** pyproject.toml (PEP 518)

**Structure:**
```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "Simple command-line todo list manager"
authors = [{name = "Your Name", email = "your@email.com"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.0,<9.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.3,<8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "black>=23.11.0,<24.0.0",
    "ruff>=0.1.0,<1.0.0",
    "mypy>=1.7.0,<2.0.0",
]

[project.scripts]
todo = "todo:cli"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = ["--cov=todo", "--cov-report=term-missing", "--cov-fail-under=90"]

[tool.black]
line-length = 88
target-version = ["py311"]

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N"]
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

**Why pyproject.toml:**
- Modern Python standard (PEP 518)
- Single source of truth (no setup.py, requirements.txt, etc.)
- Supported by pip, Poetry, PDM, Hatch
- All tool configuration in one file

**PROHIBITED:**
- ❌ requirements.txt (legacy, no dev dependencies)
- ❌ setup.py (deprecated, use pyproject.toml)
- ❌ setup.cfg (deprecated, use pyproject.toml)

---

## 5. Anti-Patterns for This Stack

**PROHIBITED Technologies (Cannot be added without ADR):**

### 5.1 Web Frameworks (FORBIDDEN)

❌ **Flask, FastAPI, Django**

**Reason:** This is a CLI tool, not a web application.

**If web UI needed later:**
1. Create ADR explaining rationale (why CLI insufficient)
2. Propose web framework based on requirements
3. Update tech-stack.md with approved choice
4. Do NOT add web framework for "nice to have" features

### 5.2 Database ORMs (FORBIDDEN)

❌ **SQLAlchemy, Peewee, Tortoise ORM**

**Reason:** JSON file storage is sufficient for <10,000 tasks.

**If database needed later:**
1. Create ADR with performance metrics (why JSON insufficient)
2. Propose database (SQLite most likely for local app)
3. Update tech-stack.md with approved choice
4. Migrate data from JSON to database with backward compatibility

### 5.3 Async Libraries (FORBIDDEN)

❌ **asyncio, aiofiles, aiohttp**

**Reason:** Single-user CLI, synchronous is simpler and sufficient.

**If async needed later:**
1. Create ADR explaining use case (e.g., cloud sync)
2. Justify complexity cost (async more complex than sync)
3. Update tech-stack.md with approved async libraries
4. Refactor code to async patterns (breaking change)

### 5.4 Alternative CLI Libraries (FORBIDDEN)

❌ **Typer, argparse, Fire, Docopt**

**Reason:** Click is LOCKED.

**If alternative needed:**
1. Create ADR with strong justification (why Click insufficient)
2. Demonstrate Click cannot support requirement
3. Obtain approval (high bar - unlikely to be approved)
4. Massive refactor (all commands rewritten)

---

## 6. Ambiguity Resolution Protocol

**If AI agent encounters ambiguity (e.g., "Should I use library X?"):**

### Step 1: Check tech-stack.md
- Is library/framework mentioned in this document?
- Is it in "Approved" section or "Prohibited" section?

### Step 2: If APPROVED → Use It
- Use specified library with documented version
- Follow usage examples in this document
- No AskUserQuestion needed

### Step 3: If PROHIBITED → HALT
- Do NOT add prohibited library
- Do NOT add "similar" library as workaround
- Use AskUserQuestion to propose alternative approach

### Step 4: If NOT MENTIONED → Ask User
```javascript
AskUserQuestion(
  question: "Implementation requires [LIBRARY] for [PURPOSE]. This library is not in tech-stack.md. Should we:",
  header: "New dependency",
  options: [
    "Add [LIBRARY] to approved dependencies (requires ADR)",
    "Find alternative using approved stack (json, pathlib, Click)",
    "Defer decision to architect"
  ]
)
```

### Step 5: If User Approves → Create ADR
- Document in `devforgeai/specs/adrs/ADR-NNN-[library]-addition.md`
- Update this tech-stack.md with new library
- Update dependencies.md with version constraints
- Commit changes with reference to ADR

**NEVER add libraries without user approval**
**ALWAYS ask if uncertain**

---

## 7. Version Update Policy

### Minor/Patch Updates (Automatic)
- Example: click 8.1.0 → 8.1.5
- **Allowed:** Yes, automatic (Dependabot, Renovate)
- **Testing:** CI/CD must pass
- **Documentation:** Update dependencies.md version

### Major Updates (Requires ADR)
- Example: click 8.1.0 → 9.0.0
- **Allowed:** Only with ADR approval
- **Reason:** Major version = breaking changes
- **Process:**
  1. Create ADR documenting breaking changes
  2. Test all affected code
  3. Update tech-stack.md with new version
  4. Update dependencies.md
  5. Document migration in CHANGELOG.md

---

## 8. Appendix: Full Dependency List

### Production Dependencies (1 total)
1. `click>=8.1.0,<9.0.0` - CLI framework

### Development Dependencies (6 total)
1. `pytest>=7.4.3,<8.0.0` - Testing framework
2. `pytest-cov>=4.1.0` - Coverage reporting
3. `pytest-mock>=3.12.0` - Mocking utilities
4. `black>=23.11.0,<24.0.0` - Code formatter
5. `ruff>=0.1.0,<1.0.0` - Linter
6. `mypy>=1.7.0,<2.0.0` - Type checker

### Standard Library (No Install Required)
1. `json` - JSON serialization
2. `pathlib` - File path handling
3. `datetime` - Timestamp handling
4. `sys` - Exit codes
5. `typing` - Type hints

---

**LOCK STATUS:** 🔒 IMMUTABLE
**Last Updated:** 2025-10-31
**ADRs:** See `devforgeai/specs/adrs/` for rationale
**Questions:** Use AskUserQuestion for all ambiguities
```

---

### File 2: dependencies.md (600 lines)

```markdown
# Approved Dependencies - Todo CLI

**Created:** 2025-10-31
**Status:** 🔒 LOCKED - Packages can only be added via ADR
**Project:** Todo CLI Tool
**Total Dependencies:** 7 (1 production, 6 development)

---

## Table of Contents

1. [Production Dependencies](#production-dependencies)
2. [Development Dependencies](#development-dependencies)
3. [Forbidden Dependencies](#forbidden-dependencies)
4. [Dependency Addition Protocol](#dependency-addition-protocol)
5. [Dependency Update Protocol](#dependency-update-protocol)
6. [Security Policy](#security-policy)

---

## 1. Production Dependencies

### 1.1 Click (CLI Framework)

**Package:** `click`
**Version:** `>=8.1.0,<9.0.0` (LOCKED to major version 8)
**Purpose:** Command-line interface and argument parsing
**License:** BSD-3-Clause (permissive, commercial use OK)
**Security:** No known vulnerabilities (checked 2025-10-31)
**PyPI:** https://pypi.org/project/click/
**Source:** https://github.com/pallets/click
**ADR:** N/A (core dependency, approved at project inception)

**Installation:**
```bash
pip install "click>=8.1.0,<9.0.0"
```

**Version Constraint Rationale:**
- `>=8.1.0` - Minimum version with all needed features
- `<9.0.0` - Lock to major version 8 (avoid breaking changes)
- Major version bump = breaking API changes = requires testing + ADR

**Usage Example:**
```python
import click

@click.command()
@click.argument('description')
@click.option('--priority', default='medium', help='Task priority')
def add(description: str, priority: str) -> None:
    """Add a new task to the todo list."""
    # implementation
```

**Features Used:**
- `@click.command()` - Define CLI commands
- `@click.argument()` - Positional arguments
- `@click.option()` - Optional flags with defaults
- `click.echo()` - Cross-platform output (handles encoding)
- `click.testing.CliRunner` - Test CLI commands

**CRITICAL:** Version locked to 8.x. Do NOT upgrade to 9.x without:
1. Reading 9.0 release notes for breaking changes
2. Testing all CLI commands
3. Creating ADR documenting migration
4. Updating tech-stack.md and dependencies.md

**Dependencies (Transitive):**
Click itself has minimal dependencies (just colorama on Windows).

---

## 2. Development Dependencies

### 2.1 pytest (Testing Framework)

**Package:** `pytest`
**Version:** `>=7.4.3,<8.0.0` (LOCKED to major version 7)
**Purpose:** Unit and integration testing
**License:** MIT (permissive, commercial use OK)
**Security:** No known vulnerabilities
**PyPI:** https://pypi.org/project/pytest/
**Source:** https://github.com/pytest-dev/pytest
**ADR:** N/A (industry standard)

**Installation:**
```bash
pip install "pytest>=7.4.3,<8.0.0"
```

**Plugins (APPROVED):**

#### 2.1.1 pytest-cov (Coverage Reporting)
- **Version:** `>=4.1.0`
- **Purpose:** Code coverage measurement
- **Usage:** `pytest --cov=todo --cov-report=term-missing`

#### 2.1.2 pytest-mock (Mocking Utilities)
- **Version:** `>=3.12.0`
- **Purpose:** Simplified mocking (wrapper around unittest.mock)
- **Usage:** `def test_func(mocker): mocker.patch(...)`

#### 2.1.3 pytest-benchmark (Performance Testing)
- **Version:** `>=4.0.0`
- **Purpose:** Benchmark CLI command performance
- **Usage:** `def test_perf(benchmark): benchmark(func)`

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "--cov=todo",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=90",
    "--strict-markers",
    "--verbose",
]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests as integration tests",
]
```

**Coverage Requirements (ENFORCED):**
- Minimum: 90% overall coverage
- Business logic: 100% coverage (all functions)
- Exclusions: Only `if __name__ == "__main__"` blocks

**Example Test:**
```python
import pytest
from pathlib import Path
from todo import add_task, load_tasks

@pytest.fixture
def todo_file(tmp_path: Path) -> Path:
    """Provide isolated todo.json for each test."""
    return tmp_path / "todo.json"

def test_should_add_task_when_valid_description(todo_file: Path):
    # Arrange
    description = "Buy milk"

    # Act
    task = add_task(todo_file, description)

    # Assert
    assert task["description"] == "Buy milk"
    assert task["status"] == "pending"
    assert task["id"] == 1
```

**CRITICAL:** All tests MUST use pytest. Do NOT use unittest or nose2.

---

### 2.2 Black (Code Formatter)

**Package:** `black`
**Version:** `>=23.11.0,<24.0.0` (LOCKED)
**Purpose:** Automatic code formatting
**License:** MIT
**Security:** No known vulnerabilities
**PyPI:** https://pypi.org/project/black/
**Source:** https://github.com/psf/black

**Installation:**
```bash
pip install "black>=23.11.0,<24.0.0"
```

**Configuration:** Default settings (zero configuration)
- Line length: 88 characters (NON-NEGOTIABLE)
- String quotes: Double quotes
- Trailing commas: Yes (multi-line structures)

**Usage:**
```bash
# Format code
black todo.py tests/

# Check without modifying
black --check todo.py tests/

# Format entire project
black .
```

**Pre-commit Hook:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11
```

**CRITICAL:** Code MUST be Black-formatted before commit. Pre-commit hook enforces this.

**Rationale for 88-character lines:**
> "88 characters is a reasonable compromise. It's enough for most lines, but not so much that you get long, hard-to-read lines. Plus, 88 is divisible by 8, and 8 is a nice round number." - Black documentation

---

### 2.3 Ruff (Linter)

**Package:** `ruff`
**Version:** `>=0.1.0,<1.0.0` (LOCKED)
**Purpose:** Fast Python linter (replaces Flake8, isort, pyupgrade)
**License:** MIT
**Security:** No known vulnerabilities
**PyPI:** https://pypi.org/project/ruff/
**Source:** https://github.com/astral-sh/ruff

**Installation:**
```bash
pip install "ruff>=0.1.0,<1.0.0"
```

**Configuration (pyproject.toml):**
```toml
[tool.ruff]
line-length = 88  # Match Black
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "N",   # pep8-naming
]
ignore = []
target-version = "py311"
exclude = [
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    "build",
    "dist",
]
```

**Usage:**
```bash
# Check code
ruff check todo.py tests/

# Auto-fix safe issues
ruff check --fix todo.py tests/

# Check entire project
ruff check .
```

**Rules Explained:**
- **E (pycodestyle errors):** PEP 8 violations (indentation, whitespace, etc.)
- **F (pyflakes):** Undefined names, unused imports, etc.
- **I (isort):** Import sorting (standard → third-party → local)
- **N (pep8-naming):** Naming conventions (PascalCase classes, snake_case functions)

**CRITICAL:** Code MUST pass Ruff with zero errors before commit.

**Performance:**
Ruff is 10-100x faster than Flake8 (written in Rust). Entire codebase linted in <100ms.

---

### 2.4 mypy (Type Checker)

**Package:** `mypy`
**Version:** `>=1.7.0,<2.0.0` (LOCKED)
**Purpose:** Static type checking
**License:** MIT
**Security:** No known vulnerabilities
**PyPI:** https://pypi.org/project/mypy/
**Source:** https://github.com/python/mypy

**Installation:**
```bash
pip install "mypy>=1.7.0,<2.0.0"
```

**Configuration (pyproject.toml):**
```toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
show_error_codes = true
pretty = true

# Ignore missing imports for third-party libraries without type stubs
[[tool.mypy.overrides]]
module = "click.testing"
ignore_missing_imports = false
```

**Usage:**
```bash
# Check types
mypy todo.py tests/

# Check entire project
mypy .

# Generate HTML report
mypy --html-report mypy-report .
```

**Type Annotation Requirements:**
```python
# ✅ CORRECT (all types annotated)
from typing import List, Dict, Any
from pathlib import Path

def add_task(file_path: Path, description: str) -> Dict[str, Any]:
    tasks: List[Dict[str, Any]] = load_tasks(file_path)
    new_task: Dict[str, Any] = {
        "id": len(tasks) + 1,
        "description": description,
        "status": "pending"
    }
    tasks.append(new_task)
    save_tasks(file_path, tasks)
    return new_task

# ❌ WRONG (missing types)
def add_task(file_path, description):  # mypy error
    pass
```

**CRITICAL:** mypy strict mode MUST pass with zero errors. No type: ignore comments without justification.

**Strict Mode Benefits:**
- Catches bugs at development time (not runtime)
- Enforces type hints (documentation + safety)
- Prevents `Any` types (no type holes)
- No implicit Optional (explicit > implicit)

---

## 3. Forbidden Dependencies

**The following packages are EXPLICITLY PROHIBITED without ADR approval:**

### 3.1 Alternative CLI Libraries (FORBIDDEN)

❌ **typer** - Alternative CLI framework
**Reason:** Click is LOCKED. Typer incompatible with Click decorators.
**If needed:** Create ADR, justify why Click insufficient, obtain approval.

❌ **argparse** - Standard library CLI
**Reason:** Less ergonomic than Click. Would create inconsistent patterns.

❌ **fire** - Google's CLI library
**Reason:** Magic behavior, less explicit. Incompatible with Click patterns.

❌ **docopt** - Docstring-based CLI
**Reason:** Less type-safe, less testable than Click.

### 3.2 Alternative JSON Libraries (FORBIDDEN)

❌ **orjson** - Fast JSON library
**Reason:** Standard library `json` is sufficient (<1000 tasks, <1ms).
**If needed:** Performance benchmarks showing json insufficient, ADR.

❌ **ujson** - Ultra-fast JSON
**Reason:** No significant benefit for CLI use. Adds C extension dependency.

❌ **simplejson** - Pure Python JSON
**Reason:** Standard library `json` is sufficient.

### 3.3 Web Frameworks (FORBIDDEN)

❌ **fastapi** - Modern web framework
**Reason:** This is a CLI tool, not a web API.
**If needed:** ADR explaining why web UI required, justify complexity.

❌ **flask** - Micro web framework
**Reason:** CLI only, no HTTP endpoints.

❌ **django** - Full-stack web framework
**Reason:** Massive overkill for CLI tool.

### 3.4 Database Libraries (FORBIDDEN)

❌ **sqlalchemy** - ORM framework
**Reason:** Using JSON file, not database.
**If needed:** Performance metrics showing JSON insufficient (>10k tasks), ADR.

❌ **peewee** - Lightweight ORM
**Reason:** JSON file meets requirements.

❌ **sqlite3** - SQL database
**Reason:** Not needed for simple task storage.
**If needed:** ADR with clear performance/query requirements.

### 3.5 Async Libraries (FORBIDDEN)

❌ **asyncio** - Async framework
**Reason:** Single-user CLI, synchronous is simpler.
**If needed:** ADR explaining async use case (cloud sync?), justify complexity.

❌ **aiofiles** - Async file I/O
**Reason:** File I/O is not bottleneck.

❌ **aiohttp** - Async HTTP
**Reason:** No HTTP requests in CLI tool.

---

## 4. Dependency Addition Protocol

**Before adding ANY new dependency, AI agents MUST follow this protocol:**

### Step 1: Check This File
- Is package already in "Production Dependencies" or "Development Dependencies"?
  - If YES → Use specified version, proceed
  - If NO → Continue to Step 2

### Step 2: Check Forbidden List
- Is package in "Forbidden Dependencies" section above?
  - If YES → HALT, cannot add, use AskUserQuestion to propose alternative
  - If NO → Continue to Step 3

### Step 3: Use AskUserQuestion

```javascript
AskUserQuestion(
  question: "Implementation requires [PACKAGE] for [PURPOSE]. This package is not in dependencies.md. Options:",
  header: "New dependency",
  description: "Adding new dependency requires ADR and updates to dependencies.md",
  options: [
    "Add [PACKAGE] version [X.Y.Z] to dependencies (requires ADR)",
    "Find alternative using approved packages (json, pathlib, Click)",
    "Defer decision to architect (complex decision)"
  ]
)
```

**Example:**
```javascript
AskUserQuestion(
  question: "Implementation requires rich for colored terminal output. Options:",
  header: "New dependency: rich",
  options: [
    "Add rich>=13.0.0 (terminal formatting library)",
    "Use click.style() for colors (already approved)",
    "Defer decision"
  ]
)
```

### Step 4: If User Approves → Create ADR

**ADR Must Document:**
1. **Why package is needed:** Specific use case, functionality required
2. **Alternatives considered:** Why existing packages insufficient
3. **Why chosen package is best:** Performance, API, maintenance, community
4. **Risks/trade-offs:** Dependencies added, bundle size, security
5. **Version constraint rationale:** Why specific version range

**Example ADR:**
```markdown
# ADR-005: Add rich for Terminal Formatting

Date: 2025-10-31
Status: Accepted

## Context
Users requested colored output and progress bars for long operations.

## Decision
Add rich>=13.0.0 for terminal formatting.

## Rationale
- click.style() limited (no progress bars, no tables)
- rich provides: colors, progress bars, tables, syntax highlighting
- Well-maintained (30k+ GitHub stars)
- Pure Python (no C extensions, cross-platform)

## Alternatives Considered
- click.style() - Too limited, no progress bars
- colorama - Only colors, no rich formatting
- blessed - Less popular, smaller ecosystem

## Consequences
**Positive:**
- Better UX (colors, progress bars)
- Professional-looking output
- Easy to use API

**Negative:**
- Adds 1 dependency
- Bundle size +300KB
- Terminal detection issues (rare)

## Enforcement
- Added to dependencies.md
- Updated tech-stack.md with usage examples
```

### Step 5: Update Files

After ADR approval:
1. Add package to dependencies.md (this file)
2. Update tech-stack.md with usage examples
3. Update pyproject.toml dependencies
4. Run `pip install -e ".[dev]"` to verify
5. Commit with message: `feat: add [package] for [purpose] (ADR-NNN)`

---

## 5. Dependency Update Protocol

### 5.1 Minor/Patch Updates (Low Risk)

**Example:** `click 8.1.0` → `click 8.1.5`

**Process:**
1. Run tests: `pytest`
2. If tests pass: Update version in dependencies.md
3. Commit: `chore: update click to 8.1.5`
4. No ADR required (backward compatible)

**Automation:**
- Dependabot/Renovate can auto-create PRs
- CI/CD must pass for auto-merge

### 5.2 Major Updates (High Risk)

**Example:** `click 8.1.0` → `click 9.0.0`

**Process (STRICT):**
1. Read release notes for breaking changes
2. Test all affected code
3. Create ADR documenting:
   - Breaking changes
   - Code changes required
   - Testing results
   - Migration timeline
4. Update tech-stack.md
5. Update dependencies.md (this file)
6. Update pyproject.toml
7. Update all code for breaking changes
8. Run full test suite + manual testing
9. Document migration in CHANGELOG.md
10. Commit: `feat!: upgrade click to 9.0.0 (BREAKING) (ADR-NNN)`

**CRITICAL:** Major version upgrades ALWAYS require ADR.

---

## 6. Security Policy

### 6.1 Vulnerability Scanning

**Tools (REQUIRED):**
- `pip-audit` - Scan for known vulnerabilities
- `safety` - Check against safety DB

**Frequency:**
- CI/CD: Every commit
- Scheduled: Weekly (Dependabot)
- Manual: Before releases

**Command:**
```bash
# Scan for vulnerabilities
pip-audit

# Alternative tool
safety check
```

### 6.2 Vulnerability Response

**If vulnerability found:**

**Severity: CRITICAL or HIGH**
1. Immediate action (within 24 hours)
2. Update to patched version
3. If no patch available: Remove dependency or find alternative
4. Emergency release if in production

**Severity: MEDIUM**
1. Action within 1 week
2. Schedule update in next sprint
3. Document in issue tracker

**Severity: LOW**
1. Action within 1 month
2. Include in regular update cycle

### 6.3 Dependency Provenance

**All dependencies MUST:**
- Come from PyPI (official repository)
- Have verifiable signatures (when available)
- Not be deprecated or unmaintained

**Red Flags:**
- ❌ No commits in 2+ years
- ❌ Critical issues ignored
- ❌ No maintainer response
- ❌ Security vulnerabilities unpatched

---

## 7. Appendix: Full Dependency Matrix

| Package | Version | Type | License | Purpose | ADR |
|---------|---------|------|---------|---------|-----|
| click | >=8.1.0,<9.0.0 | Production | BSD-3 | CLI framework | N/A |
| pytest | >=7.4.3,<8.0.0 | Dev | MIT | Testing | N/A |
| pytest-cov | >=4.1.0 | Dev | MIT | Coverage | N/A |
| pytest-mock | >=3.12.0 | Dev | MIT | Mocking | N/A |
| black | >=23.11.0,<24.0.0 | Dev | MIT | Formatter | N/A |
| ruff | >=0.1.0,<1.0.0 | Dev | MIT | Linter | N/A |
| mypy | >=1.7.0,<2.0.0 | Dev | MIT | Type checker | N/A |

**Total Count:** 7 dependencies (1 production, 6 development)

---

**LOCK STATUS:** 🔒 IMMUTABLE
**Total Dependencies:** 7
**Last Security Scan:** 2025-10-31
**Next Review:** 2025-11-30
**Questions:** Use AskUserQuestion for all new dependencies
```

---

Due to length constraints, I'll note that this document continues with the remaining 4 context files (coding-standards.md, source-tree.md, architecture-constraints.md, anti-patterns.md) and then proceeds through Examples 2-5.

**Would you like me to:**
1. Continue with the remaining context files for Example 1?
2. Skip to complete flowcharts and statistics?
3. Proceed to Examples 2-5 (Mid-Size GUI, Complex SaaS, etc.)?

The complete document would be approximately 10,000 lines showing EVERY question, EVERY context file in full, and complete flowcharts for all 5 examples.
