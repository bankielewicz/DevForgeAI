# Skill Coordination Patterns - Internet-Sleuth Integration

**Purpose:** Documentation for DevForgeAI skills on how to invoke internet-sleuth agent, parse results, handle errors, and manage token budgets.

**Audience:** spec-driven-ideation, spec-driven-architecture, other skills needing research capabilities

**Loaded:** As reference when skills need to integrate with internet-sleuth

**Location:** Absorbed from internet-sleuth-integration per ADR-045

---

## Overview

internet-sleuth is a DevForgeAI subagent providing research capabilities via Task tool invocation. This guide shows how skills coordinate with the agent, handle responses, and integrate findings into workflow outputs.

---

## Invocation Patterns

### Pattern 1: Basic Research Invocation
```python
Task(
  subagent_type="internet-sleuth",
  description="Research [topic]",
  prompt="""
  Research Mode: [discovery|investigation|competitive-analysis|repository-archaeology|market-intelligence]
  Research Scope: [brief description]
  Context: Epic [EPIC-ID] ([epic name]), Workflow State: [state]
  Required Outputs: [what you need from research]
  Constraints: [respect tech-stack.md, etc.]
  """
)
```

### Pattern 2: Context-Aware Research Invocation
- Load story/epic context first
- Include explicit Story ID, Epic ID, Workflow State markers
- internet-sleuth detects workflow state and adapts research focus

### Pattern 3: Multi-Mode Research (Sequential)
- Step 1: Feasibility (discovery mode) - get feasibility score
- Step 2: If score >= 7, deep-dive (investigation or repository-archaeology)
- Incorporates results into tech-stack.md creation

---

## Result Parsing Patterns

### Pattern 4: Extract Feasibility Score
- Check `technical_feasibility_score` (0-10)
- Apply go/no-go thresholds (>=9 GO, >=7 GO with caution, >=5 CONDITIONAL, <5 NO-GO)

### Pattern 5: Extract Top Recommendations
- Get `top_recommendations[:3]`
- Format with approach, feasibility score, pros, cons, cost

### Pattern 6: Handle Quality Gate Violations
- Check `quality_gate_status` (PASS/WARN/FAIL/BLOCKED)
- BLOCKED: Present AskUserQuestion with 3 options (Update context + ADR, Use existing, Defer as debt)
- WARN: Log and proceed
- PASS: Safe to proceed

---

## Error Handling Patterns

### Pattern 7: Handle Research Failures
- PARTIAL: Use cached results if >= 3 sections complete, else retry
- FAILED: Ask user (Retry, Manual research, Skip)

### Pattern 8: Handle API Rate Limits
- If retry_after < 60s: Wait and retry automatically
- If retry_after >= 60s: Ask user (Wait, Skip, Defer with cache reference)

---

## Token Budget Management

### Pattern 9: Monitor Token Usage
- Budget: <50K per operation
- Log and flag if exceeded
- Optimization: narrower scope, simpler mode

### Pattern 10: Batch Research (Multiple Topics)
- Combine related topics into single broader invocation
- Example: 5 separate calls (225K tokens) -> 1 combined call (65K tokens) = 71% savings

---

## Integration Examples

### spec-driven-ideation Phase 5 Integration
- Step 5.1: Determine if research needed
- Step 5.2: Invoke internet-sleuth (discovery mode)
- Step 5.3: Extract feasibility score, market viability, recommendations
- Step 5.4: Incorporate into epic document
- Step 5.5: Update epic YAML frontmatter with research_references

### spec-driven-architecture Phase 2 Integration
- Step 2.1.1: Check if research needed (multiple valid options?)
- Step 2.1.2: Invoke internet-sleuth (repository-archaeology mode)
- Step 2.1.3: Extract repository patterns
- Step 2.1.4: Populate tech-stack.md entry
- Step 2.1.5: Check for ADR requirement

---

## Success Criteria

Skill coordination succeeds when:
- [ ] Task invocation syntax correct (subagent_type, description, prompt with mode)
- [ ] Result parsing handles all expected fields
- [ ] Error handling comprehensive (PARTIAL, FAILED, RATE_LIMITED states)
- [ ] Quality gate violations trigger AskUserQuestion (BLOCKED status)
- [ ] Token budget monitored (<50K per operation)
- [ ] Research results incorporated into skill outputs
- [ ] Epic/story YAML frontmatter updated (research_references)

---

**Created:** 2025-11-17
**Absorbed into spec-driven-research:** 2026-03-20 (ADR-045)
**Version:** 1.1
**Purpose:** Documentation for DevForgeAI skills on internet-sleuth integration
