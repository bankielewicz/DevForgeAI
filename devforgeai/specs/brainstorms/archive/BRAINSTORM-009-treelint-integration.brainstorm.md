# BRAINSTORM-009: Treelint Integration into DevForgeAI Framework

---
brainstorm_id: "BRAINSTORM-009"
title: "Treelint AST-Aware Code Search Integration"
created: "2026-01-30"
status: "Complete"
confidence: "HIGH"
author: "DevForgeAI Brainstorming Session"
feeds_into: "/ideate"
---

## Key Files for Context

| File | Purpose |
|------|---------|
| `tmp/Treelint/readme.md` | Treelint documentation and feature reference |
| `tmp/Treelint/docs/architecture/ARCHITECTURE.md` | Treelint technical architecture |
| `tmp/Treelint/docs/api/cli-reference.md` | CLI command reference |
| `devforgeai/specs/adrs/ADR-013-treelint-integration.md` | Architecture Decision Record for this integration |
| `devforgeai/specs/context/tech-stack.md` | Approved technologies (requires ADR update) |
| `.claude/agents/*.md` | Subagent definitions requiring updates |
| `.claude/skills/devforgeai-development/SKILL.md` | Development workflow skill |

## Glossary

- **Subagent**: A specialized AI worker defined in `.claude/agents/` that handles specific tasks (e.g., test-automator, code-reviewer)
- **Skill**: A capability module defined in `.claude/skills/` that orchestrates workflows
- **Context file**: One of 6 architectural constraint files in `devforgeai/specs/context/` (tech-stack.md, source-tree.md, etc.)
- **TDD**: Test-Driven Development - Red → Green → Refactor cycle enforced by DevForgeAI
- **Phase**: A numbered step (01-10) in the DevForgeAI development workflow
- **ADR**: Architecture Decision Record - formal documentation for technology decisions
- **MCP**: Model Context Protocol - standardized protocol for AI assistant tool integration

---

## Executive Summary

**Problem:** DevForgeAI subagents waste 40-80% of token budget on irrelevant code search results because text-based Grep/Glob tools lack semantic awareness.

**Opportunity:** Integrate Treelint (the author's own AST-aware code search CLI using tree-sitter) to provide semantic code navigation that returns functions and classes instead of raw line matches.

**Key Value:**
- 40-80% token reduction in code search operations
- Semantic understanding (functions, classes, methods vs. raw lines)
- Already feature-complete at v0.12.0 with daemon, indexing, file watching

**Confidence Level:** HIGH (Treelint is proven, framework is stable, author controls both projects)

---

## 1. Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| Framework Architect (You) | 40-80% token reduction, replace ast-grep | Installation complexity, Rust dependency |
| Claude Code Terminal | Token efficiency, fast search | NDJSON protocol integration, daemon lifecycle |

### Secondary Stakeholders

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| Subagents (39) | Semantic results, faster TDD cycles | Learning new patterns, fallback behavior |
| Skills (17) | Maintain progressive disclosure | Reference file updates |
| End Users | Lower API costs, transparent operation | Installation, disk space |

### Key Conflicts & Resolutions

| Conflict | Resolution |
|----------|------------|
| Rust dependency vs. zero-dependency philosophy | Bundle pre-built binaries; optional enhancement with Grep fallback |
| Daemon process vs. stateless tool model | On-demand indexing with optional daemon for large projects |
| 15K character budget vs. new features | Progressive disclosure - docs in reference files only |

---

## 2. Problem Statement

> **DevForgeAI subagents and skills** experience **token waste of 40-80%** during code search operations because **text-based Grep/Glob tools lack semantic awareness**, resulting in **higher API costs, reduced context window capacity, and degraded code understanding quality**.

### 5 Whys Root Cause Analysis

```
Problem: Token waste in DevForgeAI code search operations
│
├─► Why #1: Text-based matching has no semantic awareness
│   └─► No filter for symbol types, context lines add noise, redundant matches
│
├─► Why #2: AI needs complete functions + can't distinguish code from comments
│   └─► Search-modify-verify cycles multiply the waste
│
├─► Why #3: Context window is finite, API costs scale, subagent isolation needs lean context
│   └─► Quality degrades when AI can't see enough code
│
├─► Why #4: Building AST tooling wasn't the priority (framework dev came first)
│
└─► Why #5: NOW is the right time
    ├─► Treelint v0.12.0 feature-complete (daemon, indexing, file watching)
    ├─► DevForgeAI framework stable
    └─► Personal investment - built Treelint specifically for this use case
```

### Current Pain Points

1. **Token waste** - Grep returns comments, strings, variable names matching pattern
2. **False positives** - Pattern matching isn't semantically aware
3. **Missing context** - Line matches don't show full function/class
4. **Speed** - Large codebases take too long to search

---

## 3. Treelint Capabilities (Current v0.12.0)

### Core Features (Already Implemented)

| Feature | Status | DevForgeAI Benefit |
|---------|--------|-------------------|
| Symbol-based search | ✅ Complete | Find functions/classes by name |
| JSON/text output | ✅ Complete | Machine-parseable for subagents |
| Symbol type filtering | ✅ Complete | `--type function`, `--type class` |
| AST parsing (tree-sitter) | ✅ Complete | Semantic code understanding |
| SQLite index storage | ✅ Complete | Fast queries on large codebases |
| Background daemon | ✅ Complete | Sub-5ms query latency |
| File watcher | ✅ Complete | Auto-update index on changes |
| Repository map | ✅ Complete | Full codebase symbol listing |
| Dependency graph | ✅ Complete | Call and import relationships |
| Context modes | ✅ Complete | Full, lines, signatures-only |

### Language Support

| Language | Status | Extensions |
|----------|--------|------------|
| Python | ✅ Complete | `.py` |
| TypeScript | ✅ Complete | `.ts`, `.tsx` |
| JavaScript | ✅ Complete | `.js`, `.jsx` |
| Rust | ✅ Complete | `.rs` |
| Markdown | ✅ Complete | `.md`, `.markdown` |

### Performance Metrics

- Query latency: <5ms via daemon (p95)
- Map generation: <10 seconds for 100K files
- File change → index update: <1 second
- Binary size: 7.7 MB

---

## 4. Competitive Analysis Summary

| Competitor | Approach | Token Efficiency | DevForgeAI Fit |
|------------|----------|------------------|----------------|
| **Aider** | Tree-sitter + PageRank | 4.3-6.5% utilization | HIGH - offline, graph-based |
| Cursor | Embeddings + Turbopuffer | 12.5% accuracy gain | LOW - requires cloud |
| Sourcegraph Cody | SCIP + embeddings | Enterprise-grade | MEDIUM - heavyweight |
| Continue.dev | MCP + model-agnostic | Open source | MEDIUM - MCP alignment |

**Recommendation:** Adopt Aider's approach (tree-sitter + graph ranking) which aligns with DevForgeAI's offline-first, Claude Code Terminal constraints. Treelint already implements this pattern.

---

## 5. Opportunity Mapping

### Ideal State (User Vision)

1. **Transparent replacement** - Subagents use treelint instead of grep automatically
2. **Hybrid mode** - Treelint for supported languages, grep fallback for others
3. **Full AST intelligence** - Dependency graphs, call chains, impact analysis

### Related Problems to Solve

| Problem | Treelint Capability | Priority |
|---------|---------------------|----------|
| Code quality metrics | Can count function lengths, nesting | MUST HAVE |
| Dependency analysis | `treelint deps --calls` already exists | MUST HAVE |
| Documentation generation | Signature extraction possible | SHOULD HAVE |
| Test coverage mapping | Semantic test-to-code correlation | MUST HAVE |

---

## 6. Constraints

### Technical Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Must work with Claude Code Terminal (Bash tool) | Integration via Bash commands | JSON output parsing |
| Must support offline mode | No cloud dependencies | Local SQLite index |
| Must not break existing Grep/Glob workflows | Backward compatibility | Hybrid fallback |
| Must support all DevForgeAI target languages | Python, TS, Rust, Markdown | Already supported |

### Organizational Constraints

| Constraint | Requirement |
|------------|-------------|
| ADR required | Document rationale for adding Treelint to tech-stack.md |
| Documentation complete | Reference files, skill updates |
| TDD enforcement | Test coverage for integration code |

### Resource Constraints

- **Budget:** Personal time with Claude Code Opus
- **Timeline:** Progressive rollout (dogfooding approach)

---

## 7. Hypotheses to Validate

| # | Hypothesis | Success Criteria | Risk if Wrong |
|---|------------|------------------|---------------|
| H1 | Treelint reduces tokens by 40-80% vs Grep | Measure in /dev workflow | Core value gone |
| H2 | Subagents can use treelint via Bash tool | Commands execute, JSON parses | Architecture change |
| H3 | Hybrid mode works seamlessly | No workflow failures | User disruption |
| H4 | Daemon lifecycle is manageable | Start/stop works, no orphans | Complexity overhead |

---

## 8. Prioritization

### MoSCoW Classification

| Feature | Priority | Effort |
|---------|----------|--------|
| Basic Treelint search in subagents | **MUST HAVE** | Medium |
| Full dependency graph/call chain analysis | **MUST HAVE** | Low (exists) |
| Hybrid fallback to Grep | **MUST HAVE** | Medium |
| Code quality metrics | **MUST HAVE** | Medium |
| Test-to-function coverage mapping | **MUST HAVE** | High |
| MCP server integration | COULD HAVE | High |

### Implementation Phases

```
Phase 1: Foundation (Quick Wins) - Week 1-2
├── ADR-013: Treelint Integration Decision
├── tech-stack.md update
├── Basic treelint search wrapper subagent
└── Validation: Token reduction measurement

Phase 2: Subagent Integration (Major Project) - Week 3-4
├── test-automator subagent update
├── code-reviewer subagent update
├── backend-architect subagent update
├── Grep fallback mechanism
└── Validation: Integration tests

Phase 3: Advanced Features (Major Project) - Week 5-6
├── Dependency graph integration
├── Code quality metrics
├── Test coverage mapping
└── Validation: Full workflow tests

Phase 4: Polish (Fill-ins) - Week 7+
├── MCP server (if time)
├── Performance optimization
└── Enhanced error handling
```

---

## 9. Integration Architecture

### Proposed Design

```
DevForgeAI Subagent
       │
       ▼
┌─────────────────────────────────────────┐
│         treelint-search wrapper         │
│  (new reference file or subagent)       │
├─────────────────────────────────────────┤
│  - Route search requests                 │
│  - Check language support                │
│  - Handle fallback to Grep               │
│  - Parse JSON responses                  │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌──────────┐            ┌──────────┐
│ Treelint │            │  Grep    │
│ (AST)    │            │ (Text)   │
└──────────┘            └──────────┘
```

### Usage Pattern

```bash
# Basic symbol search
treelint search validateUser --type function --format json

# Repository map for context
treelint map --ranked --format json

# Dependency analysis
treelint deps --calls --symbol handleRequest --format json

# With daemon (for repeated queries)
treelint daemon start
treelint search ... # <5ms response
treelint daemon stop
```

### JSON Output Integration

```json
{
  "query": {"symbol": "validateUser", "type": "function"},
  "results": [
    {
      "type": "function",
      "name": "validateUser",
      "file": "src/auth/validator.py",
      "lines": [10, 45],
      "signature": "def validateUser(email: str, password: str) -> bool",
      "body": "def validateUser(...):\n    ..."
    }
  ],
  "stats": {"files_searched": 150, "elapsed_ms": 36}
}
```

---

## 10. Affected DevForgeAI Components

### Subagents (High Priority)

| Subagent | Current Search | Treelint Benefit |
|----------|---------------|------------------|
| test-automator | Grep for test patterns | Function-level test discovery |
| backend-architect | Grep for implementation | Class/method semantic search |
| code-reviewer | Grep for violations | AST-aware anti-pattern detection |
| security-auditor | Grep for OWASP patterns | Semantic vulnerability detection |
| refactoring-specialist | Grep for smells | Structure-aware refactoring |
| coverage-analyzer | File-based analysis | Function-level coverage mapping |
| anti-pattern-scanner | Pattern matching | True AST-level detection |

### Skills

| Skill | Update Needed |
|-------|---------------|
| devforgeai-development | Search integration in TDD phases |
| devforgeai-qa | Anti-pattern scanning, coverage |
| devforgeai-rca | Evidence collection |
| designing-systems | Brownfield code analysis |

### Context Files

| File | Update Needed |
|------|---------------|
| tech-stack.md | Add Treelint as approved tool |
| dependencies.md | Document Treelint binary |
| source-tree.md | Add .treelint/ directory |

---

## 11. Success Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Token reduction | 40-80% | Compare Grep vs Treelint in same workflow |
| Query latency | <50ms (CLI), <5ms (daemon) | Timing measurements |
| False positive reduction | >50% | Manual review of search results |
| Subagent adoption | 100% of search-heavy agents | Component audit |
| Zero workflow regressions | 0 failures | Integration test suite |

---

## 12. Risks & Mitigations

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| Language coverage gaps | MEDIUM | LOW | Text fallback for unsupported |
| Parser errors on malformed code | LOW | MEDIUM | Tree-sitter error recovery |
| Daemon process complexity | MEDIUM | MEDIUM | On-demand mode as default |
| Installation friction | MEDIUM | LOW | Bundle in DevForgeAI installer |
| Performance on huge repos | HIGH | LOW | Scope limits, caching |

---

## 13. Next Steps

### Immediate Actions

1. ~~**Create ADR-013:** Treelint Integration Decision (documents rationale)~~ ✅ **DONE** - See `devforgeai/specs/adrs/ADR-013-treelint-integration.md`
2. **Run /ideate:** Transform this brainstorm into formal requirements
3. **Create EPIC:** Scope the full integration work

### Recommended Command

```bash
/ideate
```

The ideation phase will:
- Detect this brainstorm document automatically
- Generate formal requirements
- Assess complexity (likely Tier 3: Enhancement Platform)
- Create epic specification

---

## Appendix A: Treelint Installation

```bash
# From source (current method)
git clone https://github.com/bankielewicz/treelint
cd treelint
cargo build --release

# Binary location
target/release/treelint

# Verify installation
treelint --version  # treelint 0.12.0
```

---

## Appendix B: Research Sources

- [Aider Repository Map](https://aider.chat/docs/repomap.html)
- [Cursor Semantic Search](https://cursor.com/blog/semsearch)
- [Tree-sitter Documentation](https://tree-sitter.github.io/tree-sitter/)
- [DevForgeAI tech-stack.md](devforgeai/specs/context/tech-stack.md)

---

## Appendix C: Generated Artifacts

| Artifact | Path | Status |
|----------|------|--------|
| ADR-013 | `devforgeai/specs/adrs/ADR-013-treelint-integration.md` | ✅ Created 2026-01-30 |

---

**Session ID:** BRAINSTORM-009
**Duration:** ~30 minutes
**Questions Asked:** 14
**Confidence:** HIGH
**Status:** Ready for /ideate
