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
  - Task
  - Bash(git:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(dotnet:*)
  - Bash(cargo:*)
  - Bash(mvn:*)
  - Bash(gradle:*)
  - Bash(python:*)
  - Skill
model: sonnet
---

# DevForgeAI Development Skill

Implement user stories using Test-Driven Development while enforcing architectural constraints to prevent technical debt.

---

## Parameter Extraction

This skill extracts the story ID from conversation context (loaded story file YAML frontmatter, context markers, or natural language).

**See `references/parameter-extraction.md` for complete extraction algorithm.**

---

## Purpose

Implement features following strict TDD workflow (Red → Green → Refactor) while enforcing all 6 context file constraints.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected → HALT and use AskUserQuestion**

**See `references/ambiguity-protocol.md` for resolution procedures.**

---

## When to Use This Skill

**Prerequisites:** Git repo (recommended), context files (6), story file

**Git modes:** Full workflow (with Git) OR file-based tracking (without Git) - auto-detects

**Invoked by:** `/dev [STORY-ID]` command, devforgeai-orchestration skill, manual skill call

---

## Pre-Flight Validation (Phase 0)

8-step validation before TDD begins:

1. Validate Git status (git-validator subagent)
2. Adapt workflow (Git vs file-based)
3. File-based tracking setup (if no Git)
4. Validate 6 context files exist
5. Load story specification
6. Validate spec vs context conflicts
7. Detect tech stack (tech-stack-detector subagent)
8. Detect QA failures (recovery mode)

**See `references/preflight-validation.md` for complete workflow.**

---

## TDD Workflow (5 Phases)

### Phase 1: Test-First Design (Red Phase)
Write failing tests from AC → test-automator subagent → Tests RED
**Reference:** `tdd-red-phase.md`

### Phase 2: Implementation (Green Phase)
Minimal code to pass tests → backend-architect/frontend-developer → Tests GREEN
**Reference:** `tdd-green-phase.md`

### Phase 3: Refactor (Refactor Phase)
Improve quality, keep tests green → refactoring-specialist, code-reviewer → Code improved
**Reference:** `tdd-refactor-phase.md`

### Phase 4: Integration & Validation
Cross-component testing, coverage validation → integration-tester → Thresholds met
**Reference:** `integration-testing.md`

### Phase 5: Git Workflow & DoD Validation
Commit changes, 3-layer DoD validation → deferral-validator → Story complete
**References:** `git-workflow-conventions.md`, `dod-validation-checkpoint.md`

**See `references/tdd-patterns.md` for comprehensive TDD guidance across all phases.**

---

## QA Deferral Recovery

Triggered when QA fails due to deferrals. Phase 0 Step 0.8 detects, then 3-step resolution workflow executes.

**See `references/qa-deferral-recovery.md` for complete procedure.**

---

## Integration Points

**From:** devforgeai-story-creation (story+AC), devforgeai-architecture (context files)
**To:** devforgeai-qa (validation), devforgeai-release (deployment)
**Auto-invokes:** devforgeai-architecture (if missing), devforgeai-qa (light mode), devforgeai-story-creation (deferrals)

---

## Subagent Coordination

**Phase 0:** git-validator, tech-stack-detector
**Phase 1:** test-automator
**Phase 2:** backend-architect/frontend-developer, context-validator
**Phase 3:** refactoring-specialist, code-reviewer
**Phase 4:** integration-tester
**Phase 5:** deferral-validator

**See phase-specific reference files for coordination details.**

---

## Reference Files

Load these on-demand during workflow execution:

### Core Workflow
- **parameter-extraction.md** (92 lines) - Story ID extraction from conversation
- **preflight-validation.md** (567 lines) - Phase 0: 8-step validation (git, context, tech stack)
- **tdd-red-phase.md** (125 lines) - Phase 1: Test-first design
- **tdd-green-phase.md** (167 lines) - Phase 2: Minimal implementation
- **tdd-refactor-phase.md** (202 lines) - Phase 3: Code improvement
- **integration-testing.md** (189 lines) - Phase 4: Cross-component tests

### Phase 5 (Git/DoD)
- **git-workflow-conventions.md** (885 lines) - Git operations and conventions
- **dod-validation-checkpoint.md** (519 lines) - 3-layer DoD validation

### Supporting Files
- **tdd-patterns.md** (1,013 lines) - Comprehensive TDD guidance (all phases)
- **refactoring-patterns.md** (797 lines) - Code smell detection and fixes
- **story-documentation-pattern.md** (532 lines) - Story update procedures
- **qa-deferral-recovery.md** (218 lines) - QA failure resolution
- **ambiguity-protocol.md** (234 lines) - When to ask user questions

**Total reference content:** ~5,540 lines (loaded progressively as needed)

---

## Success Criteria

This skill succeeds when:

- [ ] All tests pass (100% pass rate)
- [ ] Coverage meets thresholds (95%/85%/80%)
- [ ] Light QA validation passed
- [ ] No context file violations
- [ ] All AC implemented
- [ ] Code follows coding-standards.md
- [ ] No anti-patterns from anti-patterns.md
- [ ] DoD validation passed (3 layers)
- [ ] Changes committed (or file-tracked)
- [ ] Story status = "Dev Complete"
- [ ] Token usage <85K (isolated context)

**The goal: Zero technical debt from wrong assumptions, fully tested features that comply with architectural decisions.**
