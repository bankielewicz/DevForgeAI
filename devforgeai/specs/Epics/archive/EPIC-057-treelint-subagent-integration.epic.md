---
id: EPIC-057
title: Treelint Subagent Integration
status: Planning
start_date: 2026-02-15
target_date: 2026-03-07
total_points: 34-55
created: 2026-01-30
updated: 2026-01-30
source_brainstorm: BRAINSTORM-009
source_requirements: treelint-integration-requirements.md
parent_initiative: Treelint AST-Aware Code Search Integration
related_epics: [EPIC-055, EPIC-056, EPIC-058, EPIC-059]
depends_on: [EPIC-055, EPIC-056]
---

# Epic: Treelint Subagent Integration

## Business Goal

Enable 7 high-impact DevForgeAI subagents to use Treelint for semantic code search, achieving 40-80% token reduction in code search operations. This is the core value delivery epic that transforms how subagents discover and understand code, replacing text-based Grep patterns with AST-aware symbol search.

## Success Metrics

- **Metric 1:** All 7 target subagents updated with Treelint search patterns
- **Metric 2:** Token reduction ≥40% measured in controlled workflow tests
- **Metric 3:** Hybrid fallback to Grep works seamlessly for unsupported languages
- **Metric 4:** Zero workflow regressions (existing functionality preserved)
- **Metric 5:** False positive reduction >50% vs Grep-only search

## Scope

### Overview

This epic updates 7 subagents that perform frequent code search operations. Each subagent receives Treelint integration via skill reference files that document search patterns. The epic also implements hybrid fallback logic ensuring Grep is used for unsupported file types.

### Features

1. **Skill Reference Files for Treelint Patterns**
   - Description: Create reference documentation with Treelint usage patterns for subagents
   - User Value: Consistent, documented patterns for all subagents to follow
   - Estimated Points: 5-8 story points

2. **test-automator Subagent Update**
   - Description: Enable function-level test discovery using `treelint search --type function`
   - User Value: Find test functions and source functions semantically
   - Estimated Points: 5-8 story points

3. **backend-architect Subagent Update**
   - Description: Enable class/method semantic search for implementation work
   - User Value: Find implementation targets by symbol name, not text patterns
   - Estimated Points: 5-8 story points

4. **code-reviewer Subagent Update**
   - Description: Enable AST-aware pattern detection for code review
   - User Value: More accurate violation detection with fewer false positives
   - Estimated Points: 3-5 story points

5. **security-auditor Subagent Update**
   - Description: Enable semantic vulnerability detection using symbol search
   - User Value: Find security-sensitive functions by semantic meaning
   - Estimated Points: 3-5 story points

6. **refactoring-specialist Subagent Update**
   - Description: Enable structure-aware refactoring with dependency awareness
   - User Value: Understand code structure before proposing refactors
   - Estimated Points: 3-5 story points

7. **coverage-analyzer Subagent Update**
   - Description: Enable function-level coverage mapping
   - User Value: Map coverage to specific functions, not just files
   - Estimated Points: 3-5 story points

8. **anti-pattern-scanner Subagent Update**
   - Description: Enable true AST-level anti-pattern detection
   - User Value: Detect code smells using structural analysis
   - Estimated Points: 3-5 story points

9. **Hybrid Fallback Logic Implementation**
   - Description: Implement automatic fallback to Grep for unsupported languages
   - User Value: Seamless experience regardless of file type
   - Estimated Points: 3-5 story points

### Out of Scope

- ❌ Skill modifications (covered by EPIC-059)
- ❌ Advanced features like dependency graphs (covered by EPIC-058)
- ❌ MCP server integration (explicitly out of scope per requirements)
- ❌ Subagents not in the high-impact list (e.g., documentation-writer, sprint-planner)

## Target Sprints

**Estimated Duration:** 2-3 sprints / 3 weeks

**Sprint Breakdown:**
- **Sprint 2:** Reference files + test-automator + backend-architect (15-24 pts)
- **Sprint 3:** code-reviewer + security-auditor + refactoring-specialist + fallback (12-20 pts)
- **Sprint 4:** coverage-analyzer + anti-pattern-scanner + validation (7-11 pts)

## Dependencies

### External Dependencies

- **Treelint v0.12.0 binary:** Must be deployed to target projects (via EPIC-055)
- **JSON output format:** Treelint must return machine-parseable results

### Internal Dependencies

- **EPIC-055 (Foundation):** ADR-013 approved, tech-stack.md updated, binary distributed
- **EPIC-056 (Context Files):** source-tree.md and anti-patterns.md updated
- **Treelint reference patterns:** Must be documented before subagent updates

### Blocking Issues

- **Blocker 1:** If EPIC-055 not complete, subagents cannot reference Treelint in tech-stack.md
  - Mitigation: Strict dependency sequencing
- **Blocker 2:** If Treelint binary not available, subagents cannot execute searches
  - Mitigation: EPIC-055 includes binary distribution validation

## Stakeholders

- **Product Owner:** Framework Architect (You)
- **Tech Lead:** Framework Architect (You)
- **Other Stakeholders:**
  - 7 target subagents (consumers of Treelint patterns)
  - Skills that invoke these subagents (devforgeai-development, devforgeai-qa)
  - End users (benefit from reduced API costs)

## Requirements

### Functional Requirements

#### User Stories

**User Story 1: Skill Reference Files**
```
As a Subagent Developer,
I want Treelint usage patterns documented in reference files,
So that all subagents follow consistent search patterns.
```

**Acceptance Criteria:**
- [ ] Reference file created with Treelint command patterns
- [ ] JSON output parsing examples provided
- [ ] Fallback logic documented (when to use Grep)
- [ ] Language support matrix included
- [ ] Error handling patterns documented

**User Story 2: test-automator Update**
```
As a test-automator Subagent,
I want to use Treelint for function-level test discovery,
So that I can find test functions and source functions semantically.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use `treelint search --type function` for function discovery
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages
- [ ] Test file → source file mapping using semantic search
- [ ] Performance validated (<100ms for typical searches)

**User Story 3: backend-architect Update**
```
As a backend-architect Subagent,
I want to use Treelint for class/method semantic search,
So that I can find implementation targets by symbol name.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use `treelint search --type class` for class discovery
- [ ] Method search using `treelint search --type function`
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages
- [ ] Implementation pattern discovery validated

**User Story 4: code-reviewer Update**
```
As a code-reviewer Subagent,
I want to use Treelint for AST-aware pattern detection,
So that I can detect violations with fewer false positives.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use Treelint for code pattern detection
- [ ] Anti-pattern detection using structural search
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages
- [ ] False positive rate reduced vs Grep-only approach

**User Story 5: security-auditor Update**
```
As a security-auditor Subagent,
I want to use Treelint for semantic vulnerability detection,
So that I can find security-sensitive functions accurately.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use Treelint for security function search
- [ ] Sensitive function patterns (auth, crypto, input validation) documented
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages

**User Story 6: refactoring-specialist Update**
```
As a refactoring-specialist Subagent,
I want to use Treelint for structure-aware refactoring,
So that I understand code structure before proposing changes.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use Treelint for code structure analysis
- [ ] Symbol relationship discovery enabled
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages

**User Story 7: coverage-analyzer Update**
```
As a coverage-analyzer Subagent,
I want to use Treelint for function-level coverage mapping,
So that I can map coverage to specific functions.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use Treelint for function enumeration
- [ ] Coverage data correlated with function symbols
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages

**User Story 8: anti-pattern-scanner Update**
```
As an anti-pattern-scanner Subagent,
I want to use Treelint for true AST-level anti-pattern detection,
So that I can detect code smells using structural analysis.
```

**Acceptance Criteria:**
- [ ] Subagent updated to use Treelint for structural anti-pattern detection
- [ ] God class detection (class with >20 methods)
- [ ] Long function detection (function with >50 lines)
- [ ] JSON parsing implemented for search results
- [ ] Fallback to Grep for unsupported languages

**User Story 9: Hybrid Fallback Logic**
```
As an AI Agent,
I want automatic fallback to Grep for unsupported languages,
So that I have a seamless experience regardless of file type.
```

**Acceptance Criteria:**
- [ ] Language support detection implemented
- [ ] Automatic Grep fallback when Treelint doesn't support file type
- [ ] Warning message displayed when falling back
- [ ] No workflow failures when Treelint unavailable
- [ ] Graceful degradation documented

### Non-Functional Requirements (NFRs)

#### Performance
- **Search Latency:** <100ms for CLI mode, <5ms for daemon mode
- **Token Reduction:** ≥40% reduction vs Grep-only searches
- **Memory Usage:** No significant increase in subagent context window usage

#### Reliability
- **Error Handling:** All Treelint errors caught and handled with Grep fallback
- **Graceful Degradation:** Workflow continues with Grep if Treelint fails
- **Parse Errors:** Tree-sitter error recovery handles malformed code

#### Compatibility
- **Language Support:** Python, TypeScript, JavaScript, Rust, Markdown
- **Backward Compatibility:** All existing Grep-based workflows still function
- **Subagent Isolation:** Updates don't affect non-search subagent functionality

### Data Requirements

#### Data Flow

```
Subagent Request
       │
       ▼
┌─────────────────────────────────────────┐
│      Language Support Check             │
│  - Check file extension                 │
│  - Supported: .py, .ts, .tsx, .js, .jsx │
│  - Supported: .rs, .md                  │
└────────────────┬────────────────────────┘
                 │
    ┌────────────┴────────────┐
    │ Supported?              │
    │                         │
    ▼ YES                     ▼ NO
┌──────────┐            ┌──────────┐
│ Treelint │            │  Grep    │
│ (AST)    │            │ (Text)   │
└────┬─────┘            └────┬─────┘
     │                       │
     ▼                       ▼
┌─────────────────────────────────────────┐
│         JSON/Text Response              │
│         to Subagent                     │
└─────────────────────────────────────────┘
```

### Integration Requirements

#### API Contracts

**Treelint Search Command:**
```bash
treelint search <symbol> --type <function|class|method> --format json
```

**Expected Response:**
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

**Fallback Grep Pattern:**
```bash
Grep(pattern="validateUser", glob="**/*.py", output_mode="content")
```

## Architecture Considerations

### Complexity Tier
**Tier 3: Complex Platform (31-45 points)**
- **Score:** 34-55 points
- **Rationale:** 7 subagent updates, hybrid logic, integration testing required

### Recommended Architecture Pattern

**Pattern:** Reference File + Direct CLI Integration

**Justification:** Subagents cannot delegate to other subagents (architecture constraint). Instead, each subagent uses Treelint directly via Bash tool, following patterns documented in shared reference files.

### Technology Constraints

- **Constraint 1:** Subagents cannot delegate to wrapper subagent (architecture rule)
- **Constraint 2:** Must use Bash tool to invoke Treelint CLI
- **Constraint 3:** Must handle JSON parsing in subagent context
- **Constraint 4:** Fallback to native Grep tool (not Bash grep)

## Risks & Constraints

### Technical Risks

**Risk 1: Subagent Context Window Limits**
- **Description:** Adding Treelint patterns may exceed subagent size limits (500 lines)
- **Probability:** Medium
- **Impact:** Medium
- **Mitigation:** Use progressive disclosure pattern (reference files)

**Risk 2: JSON Parsing Complexity**
- **Description:** Subagents must parse Treelint JSON output correctly
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Document parsing patterns clearly, provide examples

**Risk 3: Fallback Logic Errors**
- **Description:** Incorrect language detection may cause wrong tool selection
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Use file extension checking, explicit language mapping

**Risk 4: Scope Creep**
- **Description:** Temptation to update more than 7 target subagents
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Explicit out-of-scope list, defer additional subagents to future epic

### Constraints

**Constraint 1: Architecture Rule**
- **Description:** Subagents cannot delegate to other subagents
- **Impact:** Cannot create wrapper subagent for Treelint
- **Mitigation:** Each subagent uses Treelint directly via reference patterns

**Constraint 2: Progressive Disclosure**
- **Description:** Subagents must stay under 500 lines
- **Impact:** Complex patterns must go in reference files
- **Mitigation:** Use ADR-012 progressive disclosure pattern

## Assumptions

1. EPIC-055 and EPIC-056 will be complete before this epic starts
2. Treelint JSON output format is stable (v0.12.0)
3. 7 subagent updates can be done in 3 weeks
4. Reference file pattern will be effective for sharing patterns

## Next Steps

### Immediate Actions
1. **Wait for dependencies:** EPIC-055 and EPIC-056 must complete first
2. **Create Stories:** Use `/create-story` to create 9 stories for this epic
3. **Sprint Planning:** Distribute stories across Sprints 2-4

### Pre-Development Checklist
- [ ] EPIC-055 complete (ADR approved, tech-stack updated, binary distributed)
- [ ] EPIC-056 complete (source-tree.md, anti-patterns.md updated)
- [ ] Stories created for this epic
- [ ] Reference file structure designed

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Stories

| Story ID | Title | Points | Status | Sprint |
|----------|-------|--------|--------|--------|
| STORY-361 | Create Treelint Skill Reference Files for Subagent Integration | 5 | Backlog | Backlog |
| STORY-363 | Update test-automator with Treelint AST-Aware Function Discovery | 5 | Backlog | Backlog |
| STORY-365 | Update backend-architect with Treelint AST-Aware Class/Method Semantic Search | 5 | Backlog | Backlog |
| STORY-364 | Update code-reviewer with Treelint AST-Aware Pattern Detection | 3 | Backlog | Backlog |
| STORY-366 | Update security-auditor with Treelint AST-Aware Semantic Vulnerability Detection | 5 | Backlog | Backlog |
| STORY-367 | Update refactoring-specialist with Treelint AST-Aware Structure Analysis | 5 | Backlog | Backlog |
| STORY-362 | Implement Hybrid Fallback Logic (Treelint to Grep) | 3 | Backlog | Backlog |
| STORY-368 | Update coverage-analyzer with Treelint AST-Aware Function-Level Coverage Mapping | 5 | Backlog | Backlog |
| STORY-369 | Update anti-pattern-scanner with Treelint AST-Aware Anti-Pattern Detection | 5 | Backlog | Backlog |

## Notes

- This is the **third of 5 epics** and the **largest** in the Treelint integration initiative
- Represents the **core value delivery** - this is where token reduction actually happens
- Depends on both EPIC-055 (Foundation) and EPIC-056 (Context Files)
- EPIC-058 (Advanced Features) depends on this epic completing
- Consider splitting into 2 smaller epics if velocity is slower than expected

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-01-30 by DevForgeAI
