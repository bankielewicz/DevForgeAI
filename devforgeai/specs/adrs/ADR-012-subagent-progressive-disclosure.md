# ADR-012: Subagent Progressive Disclosure Architecture

**Status:** Accepted
**Date:** 2026-01-29
**Accepted:** 2026-02-22
**Research:** RESEARCH-006
**Epic:** EPIC-053 (pending creation)

## Context

DevForgeAI subagents have grown significantly beyond constitutional limits:

**Constitutional Constraints (tech-stack.md, lines 344-347):**
```markdown
**Subagents**:
- Target: 100-300 lines (~4,000-12,000 characters)
- Maximum: 500 lines (~20,000 characters)
- Rationale: Separate context window per subagent
```

**Current State (RESEARCH-006 findings):**
- **26 of 32 subagents (81%)** exceed the 500-line maximum
- **Top violators:**
  - agent-generator.md: 2,370 lines (474% over max)
  - session-miner.md: 1,860 lines (372% over max)
  - test-automator.md: 1,761 lines (352% over max)
  - ac-compliance-verifier.md: 1,165 lines (233% over max)

**Constitutional Conflict:**

source-tree.md (line 582) explicitly prohibits subagent subdirectories:
```markdown
- ❌ NO subdirectories in `.claude/agents/`
```

But tech-stack.md (lines 355-358) prescribes progressive disclosure:
```markdown
**ENFORCEMENT**:
When components exceed targets:
1. Extract reference documentation to separate files
2. Use progressive disclosure (load references on demand)
3. Split into sub-components if necessary
```

These rules are in direct conflict. Progressive disclosure requires subdirectories, but subdirectories are prohibited for subagents.

## Decision

**We will allow `references/` subdirectories for subagents that exceed 500 lines, following the same progressive disclosure pattern established for skills.**

### Approved Pattern

```
src/claude/agents/
├── test-automator.md                    # Core subagent (≤300 lines)
└── test-automator/                      # Reference subdirectory
    └── references/
        ├── remediation-mode.md          # QA integration details
        ├── exception-path-coverage.md   # STORY-264 feature
        ├── technical-specification.md   # RCA-006 enhancement
        ├── framework-patterns.md        # Python/JS/C# patterns
        └── common-patterns.md           # Mocking, async, exceptions
```

### Core Subagent Structure (≤300 lines)

The main `{subagent}.md` file MUST contain:
- YAML frontmatter (name, description, tools, model)
- Purpose statement
- When Invoked triggers
- Core Workflow (condensed)
- Success Criteria
- Error Handling
- Reference pointers with `Read()` instructions
- Observation Capture (MANDATORY)

### Reference Loading Pattern

References are loaded on-demand when the subagent needs them:

```markdown
## Remediation Mode

For QA-Dev integration remediation workflow, load:
Read(file_path=".claude/agents/test-automator/references/remediation-mode.md")

Execute the remediation workflow as documented.
```

### Alternatives Considered

| Alternative | Why Rejected |
|-------------|--------------|
| **Raise the 500-line limit** | Doesn't solve token efficiency problem; just papers over the issue |
| **Split into multiple subagents** | Creates coordination complexity; single-responsibility principle already followed |
| **Convert to skills** | Skills have different invocation model; subagents need Task() invocation |
| **Keep status quo** | 81% violation rate is unsustainable; constitutional debt |

## Consequences

### Positive

- **Constitutional compliance:** Subagents can meet 300-line target
- **Token efficiency:** 60-80% reduction in context load per invocation
- **Maintainability:** Smaller files are easier to review and update
- **Consistency:** Same progressive disclosure pattern as skills
- **Scalability:** Subagents can grow without violating limits

### Negative

- **Migration effort:** 26 subagents need refactoring
- **Reference management:** More files to maintain
- **Discovery update:** source-tree.md rule change required
- **Testing:** Need to verify reference loading works correctly

### Neutral

- **No runtime behavior change:** Subagents function identically
- **Backward compatible:** Existing small subagents unchanged

## Implementation

### Phase 1: Constitutional Update

1. Update `devforgeai/specs/context/source-tree.md`:
   - Remove line 582 prohibition
   - Add new pattern for subagent references
   - Document when subdirectories are allowed (>500 lines)

2. Update `devforgeai/specs/context/tech-stack.md`:
   - Add subagent progressive disclosure section
   - Reference source-tree.md for directory structure

### Phase 2: Subagent Refactoring (EPIC-053)

Refactor subagents in priority order:

| Priority | Subagent | Lines | Effort |
|----------|----------|-------|--------|
| P0 | agent-generator | 2,370 | 3h |
| P0 | session-miner | 1,860 | 3h |
| P0 | test-automator | 1,761 | 3h |
| P0 | ac-compliance-verifier | 1,165 | 2h |
| P1 | story-requirements-analyst | 961 | 2h |
| P1 | internet-sleuth | 937 | 2h |
| P1 | git-validator | 905 | 2h |
| P2 | Remaining 19 subagents | 500-900 | 1h each |

### Phase 3: Enforcement

1. Add pre-commit hook to warn on subagent files >500 lines
2. Add CI check to fail on subagent files >600 lines (hard limit)
3. Update subagent creation templates to include reference pattern

## Implementation Evidence

**Adoption Status:** 19 of 32 subagents (59%) now use progressive disclosure with `references/` subdirectories, containing 69 reference files total.

**Date of Evidence Collection:** 2026-02-22

### Agents Using Progressive Disclosure Pattern

The following agents have been refactored to use the `references/` subdirectory pattern prescribed by this ADR:

| # | Agent | Main File | References Directory |
|---|-------|-----------|---------------------|
| 1 | ac-compliance-verifier | `.claude/agents/ac-compliance-verifier.md` | `.claude/agents/ac-compliance-verifier/references/` |
| 2 | agent-generator | `.claude/agents/agent-generator.md` | `.claude/agents/agent-generator/references/` |
| 3 | alignment-auditor | `.claude/agents/alignment-auditor.md` | `.claude/agents/alignment-auditor/references/` |
| 4 | anti-pattern-scanner | `.claude/agents/anti-pattern-scanner.md` | `.claude/agents/anti-pattern-scanner/references/` |
| 5 | api-designer | `.claude/agents/api-designer.md` | `.claude/agents/api-designer/references/` |
| 6 | backend-architect | `.claude/agents/backend-architect.md` | `.claude/agents/backend-architect/references/` |
| 7 | code-analyzer | `.claude/agents/code-analyzer.md` | `.claude/agents/code-analyzer/references/` |
| 8 | code-quality-auditor | `.claude/agents/code-quality-auditor.md` | `.claude/agents/code-quality-auditor/references/` |
| 9 | code-reviewer | `.claude/agents/code-reviewer.md` | `.claude/agents/code-reviewer/references/` |
| 10 | coverage-analyzer | `.claude/agents/coverage-analyzer.md` | `.claude/agents/coverage-analyzer/references/` |
| 11 | dead-code-detector | `.claude/agents/dead-code-detector.md` | `.claude/agents/dead-code-detector/references/` |
| 12 | deployment-engineer | `.claude/agents/deployment-engineer.md` | `.claude/agents/deployment-engineer/references/` |
| 13 | frontend-developer | `.claude/agents/frontend-developer.md` | `.claude/agents/frontend-developer/references/` |
| 14 | integration-tester | `.claude/agents/integration-tester.md` | `.claude/agents/integration-tester/references/` |
| 15 | refactoring-specialist | `.claude/agents/refactoring-specialist.md` | `.claude/agents/refactoring-specialist/references/` |
| 16 | requirements-analyst | `.claude/agents/requirements-analyst.md` | `.claude/agents/requirements-analyst/references/` |
| 17 | security-auditor | `.claude/agents/security-auditor.md` | `.claude/agents/security-auditor/references/` |
| 18 | session-miner | `.claude/agents/session-miner.md` | `.claude/agents/session-miner/references/` |
| 19 | test-automator | `.claude/agents/test-automator.md` | `.claude/agents/test-automator/references/` |
| 20 | story-requirements-analyst | `.claude/agents/story-requirements-analyst.md` | N/A (uses cross-agent `Read()` references) |

### Key Metrics

- **19 agents** with dedicated `references/` subdirectories
- **1 additional agent** (story-requirements-analyst) using cross-agent progressive disclosure via `Read()` calls
- **69 total reference files** across all agent subdirectories
- **Pattern consistency:** All agents follow the same `{agent}/references/*.md` structure
- **Token efficiency:** 60-80% reduction in initial context load per invocation

### Progressive Disclosure Loading Pattern

All listed agents use the standard on-demand reference loading pattern:

```markdown
For detailed workflow, load:
Read(file_path=".claude/agents/{agent-name}/references/{reference-file}.md")
```

This ensures core agent files remain under the 300-line target while full documentation is available on demand.

## References

- RESEARCH-006: Subagent Progressive Disclosure Analysis
- tech-stack.md: Token Budget Constraints section (lines 330-359)
- source-tree.md: `.claude/agents/` rules (lines 572-621)
- EPIC-053: Subagent Progressive Disclosure Refactoring (pending)
