# DevForgeAI Roadmap

> Spec-driven development with zero technical debt.

## Vision

DevForgeAI is an AI-powered software development framework that enforces engineering discipline through constitutional constraints, TDD workflows, and specialized subagent orchestration. The goal is to make it impossible to ship low-quality software by embedding quality gates directly into the development process.

The long-term vision is a framework that any team can adopt to get consistent, auditable, high-quality software output from AI-assisted development — across languages, platforms, and project types.

---

## Recent Releases

### Sprint 22 — Claude Hooks for Step-Level Phase Enforcement (EPIC-086)

**Status:** Complete | **Released:** 2026-03

Introduced Claude Hooks integration for granular phase enforcement, moving from trust-based phase tracking to automated, hook-driven validation.

| Story | Description | Status |
|-------|-------------|--------|
| STORY-525 | Phase Steps Registry + Step-Level Tracking (72 steps, 12 phases) | QA Approved |
| STORY-526 | SubagentStop Hook — Auto-Track Invocations | QA Approved |
| STORY-527 | TaskCompleted Hook — Step Validation Gate | QA Approved |

**Impact:** Subagent invocations and step completions are now automatically tracked and validated via hooks, eliminating the possibility of skipped phases going undetected.

---

## Current Framework Capabilities

| Category | Count | Details |
|----------|-------|---------|
| Skills | 17 | Full SDLC coverage from discovery through release |
| Subagents | 26+ | Specialized agents for architecture, testing, QA, documentation, and more |
| Constitutional Files | 6 | Immutable constraint files governing tech stack, architecture, anti-patterns, coding standards, source tree, and dependencies |
| CLI | Python | `devforgeai-validate` for phase management, DoD validation, and quality gates |
| Installer | NPM | Package-based installation for new projects |

---

## Upcoming Features

### Near-Term (Next 1-2 Sprints)

- **Enhanced Parallel Story Development** — Improve matrix-based parallel execution with better conflict detection and automatic merge resolution when multiple stories modify overlapping files.

- **Hook Coverage Expansion** — Extend the Claude Hooks system beyond step tracking to cover additional enforcement points such as context file mutation attempts and unauthorized test modifications.

---

## Contributing to the Roadmap

Roadmap items originate from three sources:

1. **RCA Findings** — Root Cause Analyses from QA failures often reveal framework gaps that become roadmap items. See `devforgeai/RCA/` for historical analyses.

2. **ADR Proposals** — Architecture Decision Records in `devforgeai/specs/adrs/` can propose new capabilities or changes to existing constraints.

3. **Direct Feedback** — Open an issue or discussion describing the problem, the proposed solution, and which framework layer it affects (skills, subagents, rules, CLI, or constitutional files).

### Prioritization Criteria

| Factor | Weight |
|--------|--------|
| Quality gate impact (prevents defect escape) | High |
| Developer experience improvement | Medium |
| Framework adoption barrier removal | Medium |
| Token efficiency gains | Medium |
| Feature request frequency | Low |

### Process

1. Propose via ADR or issue
2. Review against constitutional constraints (does it conflict with existing context files?)
3. If approved, create Epic with story decomposition
4. Implement through standard DevForgeAI workflow (`/dev` skill, TDD, QA gates)

---

*Last updated: 2026-03-03*
