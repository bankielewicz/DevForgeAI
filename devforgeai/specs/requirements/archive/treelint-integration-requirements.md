# Treelint Integration - Requirements Specification

**Version:** 1.0
**Date:** 2026-01-30
**Status:** Approved
**Author:** DevForgeAI Ideation (from BRAINSTORM-009)
**Complexity Score:** 41/60 (Tier 3: Complex Platform)

---

## 1. Project Overview

### 1.1 Project Context

| Attribute | Value |
|-----------|-------|
| **Type** | Brownfield Enhancement |
| **Domain** | Developer Tools / AI Framework |
| **Timeline** | 8-12 weeks (Standard) |
| **Team** | Single developer + Claude Code |
| **Project Mode** | Existing (6/6 context files present) |

### 1.2 Problem Statement

> **DevForgeAI subagents and skills** experience **token waste of 40-80%** during code search operations because **text-based Grep/Glob tools lack semantic awareness**, resulting in **higher API costs, reduced context window capacity, and degraded code understanding quality**.

### 1.3 Solution Overview

Integrate Treelint (AST-aware code search CLI using tree-sitter) into DevForgeAI to provide semantic code navigation that returns functions and classes instead of raw line matches. Treelint is the author's own tool, currently at v0.12.0 with daemon, indexing, and file watching capabilities.

### 1.4 Success Criteria

| Metric | Target | Measurement |
|--------|--------|-------------|
| Token reduction | ≥40% vs Grep | Before/after comparison |
| Subagent adoption | 7/7 high-impact agents | Component audit |
| Workflow regressions | 0 failures | Integration test suite |
| False positive reduction | >50% | Manual review |

### 1.5 Key Value Proposition

- **40-80% token reduction** in code search operations
- **Semantic understanding** (functions, classes, methods vs. raw lines)
- **Feature-complete tool** at v0.12.0 (daemon, indexing, file watching)
- **Author controls both projects** (Treelint and DevForgeAI)

---

## 2. User Roles & Personas

### 2.1 Primary Users

| Persona | Role | Goals | Concerns |
|---------|------|-------|----------|
| Framework Architect | You | 40-80% token reduction, replace ast-grep gaps | Installation complexity, Rust dependency |
| Claude Code Terminal | AI Runtime | Token efficiency, fast search | NDJSON protocol integration, daemon lifecycle |

### 2.2 Secondary Users

| Persona | Role | Goals | Concerns |
|---------|------|-------|----------|
| Subagents (39) | Specialized AI Workers | Semantic results, faster TDD cycles | Learning new patterns, fallback behavior |
| Skills (17) | Workflow Orchestrators | Maintain progressive disclosure | Reference file updates |
| End Users | DevForgeAI Consumers | Lower API costs, transparent operation | Installation, disk space |

---

## 3. Functional Requirements

### 3.1 Core Requirements (MUST HAVE)

| Req ID | Requirement | Priority | Acceptance Criteria |
|--------|-------------|----------|---------------------|
| FR-001 | Basic treelint symbol search in subagents | MUST HAVE | Subagents can invoke `treelint search` via Bash and parse JSON results |
| FR-002 | Dependency graph and call chain analysis | MUST HAVE | `treelint deps --calls` returns caller/callee relationships |
| FR-003 | Hybrid fallback to Grep for unsupported languages | MUST HAVE | Automatic fallback with warning message when language not supported |
| FR-004 | Code quality metrics extraction | MUST HAVE | Extract function length, nesting depth from AST |
| FR-005 | Test-to-function coverage mapping | MUST HAVE | Semantic correlation between test files and source functions |
| FR-006 | JSON output format for AI consumption | MUST HAVE | All treelint commands support `--format json` |
| FR-007 | Full function/class body context in results | MUST HAVE | Results include complete code blocks, not just signatures |
| FR-008 | Warn-then-fallback error behavior | MUST HAVE | Display error message, then proceed with Grep |
| FR-009 | Daemon auto-start if stopped | SHOULD HAVE | Claude helps start daemon when status is stopped |

### 3.2 Feature Requirements by Epic

#### EPIC-055: Foundation & Distribution
- ADR-013 formalization with implementation details
- tech-stack.md update (add Treelint as approved tool)
- Binary distribution bundled in installer
- .treelint/ directory structure definition

#### EPIC-056: Context File Integration
- source-tree.md update (.treelint/ directory)
- dependencies.md update (binary distribution pattern)
- anti-patterns.md update (Treelint-specific guidance)
- .gitignore pattern for .treelint/

#### EPIC-057: Subagent Integration
- Skill reference files with treelint usage patterns
- 7 subagent updates:
  1. test-automator - Function-level test discovery
  2. backend-architect - Class/method semantic search
  3. code-reviewer - AST-aware pattern detection
  4. security-auditor - Semantic vulnerability detection
  5. refactoring-specialist - Structure-aware refactoring
  6. coverage-analyzer - Function-level coverage mapping
  7. anti-pattern-scanner - True AST-level detection
- Hybrid fallback logic implementation

#### EPIC-058: Advanced Features
- Dependency graph integration (`treelint deps`)
- Code quality metrics extraction
- Test coverage mapping (semantic correlation)
- Repository map usage for context
- Daemon auto-start logic

#### EPIC-059: Validation & Rollout
- Token measurement framework (before/after)
- Integration test suite
- devforgeai-development skill update
- devforgeai-qa skill update
- User documentation and troubleshooting guide

---

## 4. Data Requirements

### 4.1 Data Model

| Entity | Location | Purpose | Git Strategy |
|--------|----------|---------|--------------|
| Treelint Index | `.treelint/index.db` | SQLite database of parsed symbols | Gitignored |
| Treelint Config | `.treelint/config.toml` | Project-specific settings | Optional commit |
| Pre-built Binaries | DevForgeAI installer | Treelint CLI executable | Committed to installer |
| Daemon Socket | `.treelint/daemon.sock` | IPC for daemon queries | Gitignored |

### 4.2 Data Flow

```
Subagent Request
       │
       ▼
┌─────────────────────────────────────────┐
│      Skill Reference (patterns)         │
├─────────────────────────────────────────┤
│  - Check language support               │
│  - Select treelint command              │
│  - Handle fallback to Grep              │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌──────────┐            ┌──────────┐
│ Treelint │            │  Grep    │
│ (AST)    │            │ (Text)   │
└────┬─────┘            └────┬─────┘
     │                       │
     ▼                       ▼
┌─────────────────────────────────────────┐
│         JSON Response to Subagent       │
└─────────────────────────────────────────┘
```

---

## 5. Integration Requirements

### 5.1 Integration Points

| Integration | Type | Protocol | Notes |
|-------------|------|----------|-------|
| Subagent → Treelint | CLI invocation | Bash + JSON | Direct execution, not wrapper subagent |
| Treelint → SQLite | Data storage | Local file | .treelint/index.db |
| Treelint → Tree-sitter | AST parsing | Library | Bundled in binary |
| Fallback → Grep | CLI invocation | Bash + text | Native Claude Code tool |

### 5.2 API Contracts

#### Treelint Search Command
```bash
treelint search <symbol> --type <function|class|method> --format json
```

**Response:**
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

#### Treelint Deps Command
```bash
treelint deps --calls --symbol <name> --format json
```

#### Treelint Map Command
```bash
treelint map --ranked --format json
```

### 5.3 Language Support

| Language | Status | Extensions |
|----------|--------|------------|
| Python | ✅ Complete | `.py` |
| TypeScript | ✅ Complete | `.ts`, `.tsx` |
| JavaScript | ✅ Complete | `.js`, `.jsx` |
| Rust | ✅ Complete | `.rs` |
| Markdown | ✅ Complete | `.md`, `.markdown` |

---

## 6. Non-Functional Requirements

### 6.1 Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Token reduction | ≥40% | Conservative minimum from 40-80% range |
| Query latency (CLI) | <100ms | Standard CLI invocation |
| Query latency (daemon) | <5ms | When daemon is running |
| Map generation | <10s | For 100K files |
| Index update | <1s | After file change |

### 6.2 Reliability

| Requirement | Specification |
|-------------|---------------|
| Error handling | Display error message, then fallback to Grep |
| Parse errors | Tree-sitter error recovery built-in |
| Daemon lifecycle | User-initiated with auto-start fallback |
| Caching | None (rely on treelint's SQLite index) |

### 6.3 Distribution

| Requirement | Specification |
|-------------|---------------|
| Binary bundling | Pre-built binaries in DevForgeAI installer |
| Binary size | 7.7 MB |
| Platform support | Linux, macOS, Windows (via installer) |
| Offline mode | Full functionality without network |

### 6.4 Compatibility

| Requirement | Specification |
|-------------|---------------|
| Claude Code Terminal | Bash tool invocation |
| Existing Grep/Glob | Hybrid fallback preserved |
| DevForgeAI subagents | 7 high-impact agents updated |
| DevForgeAI skills | 4 skills updated |

---

## 7. Complexity Assessment

### 7.1 Score Breakdown

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Functional** | 20/20 | 7 subagents, 4 skills, 3 context files affected |
| **Technical** | 13/20 | CLI integration, JSON parsing, fallback logic |
| **Team/Org** | 5/10 | Single developer + Claude |
| **NFR** | 3/10 | No hard performance requirements |
| **TOTAL** | **41/60** | |

### 7.2 Architecture Tier

**Tier 3: Complex Platform (31-45 points)**

- Multiple component updates required
- Cross-cutting concerns (subagents, skills, context files)
- Integration testing complexity
- Progressive rollout needed

### 7.3 Recommended Approach

- Skill reference files + direct Bash calls (not wrapper subagent)
- JSON output for AI consumption
- Hybrid fallback with warnings
- TDD with integration tests

---

## 8. Feasibility Analysis

### 8.1 Technical Feasibility: FEASIBLE (9/10)

| Factor | Assessment | Notes |
|--------|------------|-------|
| Technology maturity | HIGH | Treelint v0.12.0 proven |
| Integration complexity | MEDIUM | 7 subagents + 4 skills + 3 context files |
| Team expertise | HIGH | Author controls both projects |
| Performance | HIGH | <5ms daemon queries documented |
| Offline capability | HIGH | Local SQLite index |

### 8.2 Business Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Timeline | 8-12 weeks fits 89-144 story points |
| Budget | Personal time with Claude Code Opus |
| Resources | Single developer + Claude sufficient |

### 8.3 Resource Feasibility: FEASIBLE

| Factor | Assessment |
|--------|------------|
| Development capacity | 1 FTE + AI assistance |
| Skill gaps | None (author of both tools) |
| Infrastructure | Local development only |

### 8.4 Overall Assessment

| Dimension | Status |
|-----------|--------|
| Technical | ✅ FEASIBLE |
| Business | ✅ FEASIBLE |
| Resource | ✅ FEASIBLE |
| Risk Profile | ✅ LOW (no CRITICAL risks) |
| **Recommendation** | **PROCEED** |

---

## 9. Risk Register

| Risk | Category | Prob | Impact | Severity | Mitigation |
|------|----------|------|--------|----------|------------|
| Binary distribution bloat | Technical | LOW | MEDIUM | LOW | Optimize binary size, document size |
| Language coverage gaps | Technical | LOW | MEDIUM | LOW | Grep fallback for unsupported |
| Parser errors on malformed code | Technical | MEDIUM | LOW | LOW | Tree-sitter error recovery |
| Daemon process complexity | Technical | MEDIUM | MEDIUM | MEDIUM | On-demand mode as default |
| Subagent update scope creep | Team | MEDIUM | MEDIUM | MEDIUM | Clear feature boundaries per story |
| Token measurement accuracy | Technical | LOW | LOW | LOW | Manual spot checks |

---

## 10. Constraints & Assumptions

### 10.1 Technical Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Must work with Claude Code Terminal (Bash tool) | Integration via Bash commands | JSON output parsing |
| Must support offline mode | No cloud dependencies | Local SQLite index |
| Must not break existing Grep/Glob workflows | Backward compatibility | Hybrid fallback |
| Must support all DevForgeAI target languages | Python, TS, Rust, Markdown | Already supported |
| Subagents cannot delegate to other subagents | No wrapper subagent | Skill reference pattern |

### 10.2 Organizational Constraints

| Constraint | Requirement |
|------------|-------------|
| ADR required | Document rationale in ADR-013 |
| Documentation complete | Reference files, skill updates |
| TDD enforcement | Test coverage for integration code |

### 10.3 Assumptions (Validated)

| Assumption | Status | Evidence |
|------------|--------|----------|
| Treelint v0.12.0 is stable | ✅ Validated | Author confirmation |
| JSON output works for AI consumption | ✅ Validated | Treelint design goal |
| Hybrid fallback is reliable | ✅ Validated | Pattern exists in DevForgeAI |
| 40% token reduction achievable | ⚠️ To validate | Before/after measurement needed |

---

## 11. Affected Components

### 11.1 Subagents (7 total)

| Subagent | Current Search | Treelint Benefit | Priority |
|----------|---------------|------------------|----------|
| test-automator | Grep for test patterns | Function-level test discovery | P0 |
| backend-architect | Grep for implementation | Class/method semantic search | P0 |
| code-reviewer | Grep for violations | AST-aware anti-pattern detection | P0 |
| security-auditor | Grep for OWASP patterns | Semantic vulnerability detection | P0 |
| refactoring-specialist | Grep for smells | Structure-aware refactoring | P0 |
| coverage-analyzer | File-based analysis | Function-level coverage mapping | P0 |
| anti-pattern-scanner | Pattern matching | True AST-level detection | P0 |

### 11.2 Skills (4 total)

| Skill | Update Needed |
|-------|---------------|
| devforgeai-development | Search integration in TDD phases |
| devforgeai-qa | Anti-pattern scanning, coverage |
| devforgeai-rca | Evidence collection |
| designing-systems | Brownfield code analysis |

### 11.3 Context Files (3 total)

| File | Update Needed |
|------|---------------|
| tech-stack.md | Add Treelint as approved tool |
| dependencies.md | Document Treelint binary |
| source-tree.md | Add .treelint/ directory |

---

## 12. Epic Breakdown

### 12.1 Epic Roadmap

```
Week 1-2:   EPIC-055 (Foundation) + EPIC-056 (Context Files)
            ├── ADR finalization
            ├── tech-stack.md update
            ├── Binary distribution
            └── Context file updates

Week 3-5:   EPIC-057 (Subagent Integration)
            ├── Skill reference files
            ├── 7 subagent updates
            └── Hybrid fallback logic

Week 6-7:   EPIC-058 (Advanced Features)
            ├── Dependency graph
            ├── Code quality metrics
            ├── Test coverage mapping
            └── Daemon auto-start

Week 8+:    EPIC-059 (Validation & Rollout)
            ├── Token measurement
            ├── Integration tests
            ├── Skill updates
            └── Documentation
```

### 12.2 Epic Summaries

| Epic ID | Name | Business Goal | Features | Est. Points |
|---------|------|---------------|----------|-------------|
| EPIC-055 | Foundation & Distribution | Establish Treelint as approved tool | 5 | 13-21 |
| EPIC-056 | Context File Integration | Update constitutional documents | 4 | 8-13 |
| EPIC-057 | Subagent Integration | Enable 7 agents to use semantic search | 9 | 34-55 |
| EPIC-058 | Advanced Features | Leverage full Treelint capabilities | 5 | 21-34 |
| EPIC-059 | Validation & Rollout | Validate and document integration | 5 | 13-21 |
| **TOTAL** | | | **28** | **89-144** |

### 12.3 Epic Dependencies

```
EPIC-055 (Foundation) ──┬──► EPIC-057 (Subagent Integration)
                        │
EPIC-056 (Context Files)┘
                              │
                              ▼
                        EPIC-058 (Advanced Features)
                              │
                              ▼
                        EPIC-059 (Validation & Rollout)
```

---

## 13. Out of Scope

The following items are explicitly **NOT included** in this integration:

- ❌ **MCP server integration** - Removed from scope (focus on Bash CLI)
- ❌ **Wrapper subagent** - Architecture constraint (subagents can't delegate)
- ❌ **Additional language support** - Use existing Treelint languages
- ❌ **Cloud-based indexing** - Offline-first design
- ❌ **Real-time streaming** - JSON batch responses sufficient

---

## 14. Next Steps

### 14.1 Immediate Actions

1. **Create 5 epics** via `/create-epic` command:
   - `/create-epic EPIC-055 Treelint Foundation & Distribution`
   - `/create-epic EPIC-056 Treelint Context File Integration`
   - `/create-epic EPIC-057 Treelint Subagent Integration`
   - `/create-epic EPIC-058 Treelint Advanced Features`
   - `/create-epic EPIC-059 Treelint Validation & Rollout`

2. **Create Sprint 1** via `/create-sprint`:
   - Include EPIC-055 and EPIC-056 stories

3. **Finalize ADR-013** with implementation details

### 14.2 Project Context (Existing)

All 6 context files exist. No `/create-context` needed.

Recommended workflow:
1. Create epics (5 documents)
2. Create Sprint 1 with EPIC-055 + EPIC-056 stories
3. Begin TDD implementation via `/dev`

---

## Appendices

### A. Glossary

| Term | Definition |
|------|------------|
| AST | Abstract Syntax Tree - structured representation of source code |
| Treelint | AST-aware code search CLI using tree-sitter |
| tree-sitter | Incremental parsing library used by GitHub, Neovim, etc. |
| Daemon | Background process for fast query responses (<5ms) |
| Subagent | Specialized AI worker in `.claude/agents/` |
| Skill | Capability module in `.claude/skills/` |
| Context file | Constitutional constraint file in `devforgeai/specs/context/` |

### B. References

| Reference | Location |
|-----------|----------|
| BRAINSTORM-009 | `devforgeai/specs/brainstorms/BRAINSTORM-009-treelint-integration.brainstorm.md` |
| ADR-013 | `devforgeai/specs/adrs/ADR-013-treelint-integration.md` |
| Treelint README | `tmp/Treelint/readme.md` |
| Treelint Architecture | `tmp/Treelint/docs/architecture/ARCHITECTURE.md` |
| Treelint CLI Reference | `tmp/Treelint/docs/api/cli-reference.md` |

### C. Open Questions

| Question | Status | Resolution |
|----------|--------|------------|
| Exact binary size impact? | Open | Measure during EPIC-055 |
| Token reduction validation method? | Resolved | Before/after comparison |
| Daemon auto-start trigger? | Resolved | Claude helps start when status=stopped |

---

**Document Version:** 1.0
**Created:** 2026-01-30
**Source:** BRAINSTORM-009 + DevForgeAI Ideation Workflow
**Status:** Ready for Epic Creation
