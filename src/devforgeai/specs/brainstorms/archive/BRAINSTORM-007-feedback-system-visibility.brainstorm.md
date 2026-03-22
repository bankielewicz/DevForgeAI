# BRAINSTORM-007: Framework Feedback System Visibility

**Session ID:** BRAINSTORM-007
**Date:** 2026-01-26
**Status:** Complete
**Confidence:** HIGH

---

## Key Files for Context

**Read these files to understand the problem space:**

| Component | File Path | Purpose |
|-----------|-----------|---------|
| **10-Phase Workflow** | `.claude/skills/devforgeai-development/SKILL.md` | Defines TDD phases 01-10 for /dev command |
| **Phase 09 (Feedback)** | `.claude/skills/devforgeai-development/phases/phase-09-feedback.md` | Current feedback hook implementation |
| **Observation Protocol** | `.claude/skills/devforgeai-development/references/observation-capture.md` | How observations SHOULD be captured |
| **Framework Analyst** | `.claude/agents/framework-analyst.md` | Subagent that synthesizes observations into recommendations |
| **Dev Result Interpreter** | `.claude/agents/dev-result-interpreter.md` | Phase 10 output formatter (where inline display would go) |
| **Hooks Configuration** | `devforgeai/config/hooks.yaml` | Hook triggers and settings (lines 170-224 for AI analysis) |
| **Phase State Files** | `devforgeai/workflows/{STORY_ID}-phase-state.json` | Per-story phase tracking including `observations[]` array |
| **Feedback Storage** | `devforgeai/feedback/ai-analysis/{STORY_ID}/` | Where AI analysis results are stored |
| **Feedback Skill** | `.claude/skills/devforgeai-feedback/SKILL.md` | The feedback collection skill |

---

## Glossary

| Term | Definition |
|------|------------|
| **Phase 01-10** | The 10-phase TDD workflow in `/dev` command: Preflight → Test-First → Implementation → Refactor → AC-Verify → Integration → AC-Verify → Deferral → DoD-Update → Git → Feedback → Result |
| **Exit Gate** | A validation checkpoint at the end of each phase (e.g., `devforgeai-validate phase-complete STORY-XXX --phase=09`) |
| **Subagent Contract** | The markdown file in `.claude/agents/` that defines a subagent's inputs, outputs, and behavior |
| **Two-Hat Problem** | Claude simultaneously executing tasks AND reflecting on the process - cognitive overload that deprioritizes reflection |
| **Inline Display** | Showing feedback during `/dev` workflow execution (specifically at Phase 10 result output), not requiring manual file searches |
| **Observation** | A structured note capturing friction, success, patterns, gaps, ideas, or bugs during workflow execution |
| **STORY-018** | The story that implemented the hook system architecture (hooks.yaml, check-hooks, invoke-hooks CLI commands) |

---

## Executive Summary

Framework owners are not seeing feedback from phases/subagents/workflows because subagents don't return observation data and the feedback system (STORY-018) was added after core components existed. This results in a framework that can't self-improve, repeated friction going unaddressed, and loss of institutional knowledge.

---

## Problem Statement

> **Framework owners** experience **inability to see feedback from phases/subagents/workflows** because **subagents don't return observation data and the feedback system was added after core components existed**, resulting in **framework that can't self-improve, repeated friction going unaddressed, manual effort to extract insights, and loss of institutional knowledge**.

---

## 5 Whys Root Cause Analysis

| Level | Question | Answer |
|-------|----------|--------|
| Why 1 | Why isn't feedback visible? | Feedback isn't being captured at all |
| Why 2 | Why isn't it captured? | Subagents don't return observation data |
| Why 3 | Why don't subagents return observation data? | Framework was designed before feedback system |
| Why 4 | Why wasn't feedback integrated when subagents were created? | Feedback was a later addition (STORY-018) |
| **Why 5** | Why hasn't feedback been retrofitted since? | **Low priority vs new features** |

**Root Cause:** Feedback system (STORY-018) came after subagents; retrofitting has been deprioritized vs new features.

---

## Stakeholder Analysis

### Primary Stakeholders

| Stakeholder | Goals | Concerns |
|-------------|-------|----------|
| **Framework Owner (User)** | See framework improvement insights during workflow; receive actionable recommendations | Feedback invisible during execution; must search files manually |
| **Framework Architect (Claude)** | Capture insights while context is fresh; avoid two-hat cognitive load | By Phase 09, reconstruction produces generic analysis |

### Secondary Stakeholders

| Stakeholder | Role | Gap |
|-------------|------|-----|
| **Subagent System** | Execute specialized tasks | Rich output exists but not captured as observations |
| **Hook System** | Trigger feedback collection | Hooks fire but no inline display |
| **Phase State System** | Persist observations | observations[] array often empty |

### Key Conflict

**Visibility vs Context Pressure:** User wants inline display; Claude experiences context pressure that deprioritizes reflection during execution.

**Resolution:** Move observation capture FROM exit gates TO subagent return contracts. Extract observations automatically from structured outputs.

---

## Current State

**Status:** Automated but broken

**Evidence (with file paths):**
- `devforgeai/config/hooks.yaml` lines 170-196 shows `post-dev-ai-analysis: enabled=true`
- `devforgeai/feedback/ai-analysis/STORY-293/`, `STORY-200/`, `STORY-286/` contain ai-analysis.json files
- `devforgeai/workflows/STORY-306-phase-state.json` completed all 10 phases with `"observations": []`
- `.claude/agents/dev-result-interpreter.md` has no "Framework Insights" display section

**What Works:**
- Phase state tracking in `devforgeai/workflows/{STORY_ID}-phase-state.json` (phases complete)
- Subagent invocation recording in phase-state.json `subagents_invoked[]` arrays
- Hook configuration in `devforgeai/config/hooks.yaml`
- Storage layer in `devforgeai/feedback/ai-analysis/`

**What Doesn't Work:**
- Observation capture during phases 01-08 (the "Observation Capture (Before Exit)" prompts in each phase file are skipped)
- Inline display during workflow (dev-result-interpreter doesn't read Phase 09 ai-analysis output)
- Automatic extraction from subagent outputs (subagents don't return `observations[]` field)

---

## Market Research: AI Agent Feedback Patterns

### Top 5 Approaches

| Pattern | Source | Applicability |
|---------|--------|---------------|
| **Callback-Based Tracing** | LangSmith, Langfuse | HIGH - Wrap phases with decorators |
| **Reflexion (Verbal RL)** | NeurIPS 2023 | HIGH - "What went wrong, how to improve" |
| **Multi-Layer Memory** | CrewAI | MEDIUM-HIGH - Short/long-term memory |
| **TAO Cycle** | ReAct Pattern | HIGH - Thought-Action-Observation loop |
| **Self-Evolving Agents** | EvoAgentX | MEDIUM - Framework-level improvements |

### Key Insights

1. **Automatic capture beats manual logging** - Use decorator/callback patterns
2. **Verbal reflections are actionable** - Concrete improvement directions
3. **Multi-layer memory enables learning** - Short-term + long-term
4. **89% of production agents have observability** - Industry standard
5. **32% cite quality as top barrier** - Inline observation helps earlier

### Recommended Hybrid

Combine **Reflexion** + **TAO Cycle** for DevForgeAI's 10-phase TDD workflow:

```
Phase Execution → Capture Observation → Generate Reflection → Store in Memory → Display Inline
```

**How Reflexion Applies to DevForgeAI:**
- **Current state:** When Phase 03 (Implementation) fails, Claude retries without structured reflection
- **With Reflexion:** Store verbal reflection ("Tests failed because X, next time do Y") in phase-state.json
- **Benefit:** Next TDD iteration starts with context about WHY previous attempt failed
- **Implementation:** Add `reflection` field to phase-state.json for failed phases

**How TAO Cycle Applies to DevForgeAI:**
- **Thought:** Claude reasons about current phase (e.g., "Executing Phase 02 test-first for STORY-XXX")
- **Action:** Invoke subagent (e.g., test-automator) and execute phase steps
- **Observation:** Capture what happened (coverage gaps, warnings, patterns) into `observations[]`
- **Implementation:** Each subagent returns optional `observations[]` array in its output

---

## Constraints

| Type | Constraint |
|------|------------|
| **Budget** | Large - can redesign the system |
| **Timeline** | This month |
| **Technical** | Must work with existing subagent architecture |
| **Technical** | Must use Claude Code tools only |
| **Technical** | Must preserve backward compatibility |
| **Technical** | CAN modify subagent contracts |

---

## Hypotheses to Validate

| ID | Hypothesis | Success Criteria |
|----|------------|------------------|
| **H1** | Adding observation schema to subagents will capture data | phase-state.json `observations[]` populated automatically |
| **H2** | Inline display will increase feedback visibility | Users report seeing feedback during /dev workflow |
| **H3** | Automatic capture is better than manual reflection | Observation richness increases (more fields, more context) |
| **H4** | Verbal reflections improve retry success | TDD iteration counts decrease |

---

## Prioritization

### MoSCoW Classification

| Feature | Priority | Rationale |
|---------|----------|-----------|
| Subagent observation schema | **Must Have** | Enables all other features |
| Inline observation display | **Must Have** | Primary user-facing requirement |
| Reflexion pattern for TDD | **Must Have** | Improves retry success |
| Multi-layer memory | **Must Have** | Enables cross-session learning |

### Recommended Sequence

1. **Quick Win (Week 1):** Inline observation display in dev-result-interpreter
2. **Foundation (Week 2):** Subagent observation schema (test-automator first)
3. **Enhancement (Week 3):** Reflexion pattern for TDD retry improvement
4. **Platform (Week 4):** Multi-layer memory (short-term + long-term)

---

## Solution Architecture (Proposed)

### 1. Subagent Observation Schema

Add optional `observations[]` field to high-frequency subagents:

```typescript
interface SubagentOutput {
  // Existing fields...
  result: any;

  // NEW: Optional observations
  observations?: Array<{
    category: 'friction' | 'success' | 'pattern' | 'gap' | 'idea' | 'bug';
    note: string;
    severity: 'low' | 'medium' | 'high';
    files?: string[];
  }>;
}
```

**Priority subagents:**
1. test-automator (coverage_gaps → observation)
2. backend-architect (pattern_selections → observation)
3. code-reviewer (issues_by_severity → observation)
4. ac-compliance-verifier (ac_pass_rates → observation)

### 2. Observation Extractor

**Location:** New subagent at `.claude/agents/observation-extractor.md`

**Purpose:** Mines existing subagent outputs for observations without requiring subagent schema changes.

**Integration Point:** Called at end of each phase (01-08) in the phase files, before exit gate.

**Implementation:**

```python
# Pseudocode for observation extraction logic
def extract_observations(subagent_type: str, subagent_output: dict) -> list:
    observations = []

    # test-automator specific extraction
    if subagent_type == 'test-automator':
        if 'coverage_gaps' in subagent_output:
            observations.append({
                'category': 'gap',
                'note': f"Coverage gap: {subagent_output['coverage_gaps']}",
                'severity': 'high',
                'files': subagent_output.get('affected_files', [])
            })

    # code-reviewer specific extraction
    if subagent_type == 'code-reviewer':
        if 'issues_by_severity' in subagent_output:
            for issue in subagent_output['issues_by_severity'].get('high', []):
                observations.append({
                    'category': 'friction',
                    'note': issue,
                    'severity': 'high'
                })

    # backend-architect specific extraction
    if subagent_type == 'backend-architect':
        if 'pattern_deviations' in subagent_output:
            observations.append({
                'category': 'pattern',
                'note': f"Pattern deviation: {subagent_output['pattern_deviations']}",
                'severity': 'medium'
            })

    return observations
```

**Alternative Approach:** Instead of a separate subagent, add extraction logic to each phase file's "Observation Capture (Before Exit)" section.

### 3. Inline Display (dev-result-interpreter)

**File to Modify:** `.claude/agents/dev-result-interpreter.md`

**Current State:** Outputs TDD phase summary, test results, DoD status, next steps - but NO framework insights.

**Change Required:** Add step to read Phase 09 ai-analysis output and display summary.

**New Step in dev-result-interpreter:**
```markdown
### Step N: Read Framework Insights

1. Check if Phase 09 generated ai-analysis:
   Read(file_path="devforgeai/feedback/ai-analysis/${STORY_ID}/")

2. If ai-analysis.json exists, extract:
   - Top 3 `what_worked_well` items
   - Top 3 `areas_for_improvement` items
   - Top 3 `recommendations` (sorted by priority)

3. Display in output template (see below)
```

**New Output Section:**
```markdown
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Framework Insights (Phase 09 Analysis)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

What Worked Well:
  ✓ Phase state validation prevented skipping Phase 03
  ✓ anti-patterns.md caught God Object before commit

Areas for Improvement:
  ⚠ Test naming convention unclear for shell scripts
  ⚠ DoD update required manual intervention

Top Recommendations:
  1. Document shell script test naming convention (15 min)
  2. Automate DoD checkbox updates from phase-state.json (30 min)

Full analysis: devforgeai/feedback/ai-analysis/${STORY_ID}/
```

**Fallback:** If no ai-analysis exists, display: "No framework insights captured. Run with observation capture enabled."

### 4. Reflexion Pattern Integration

Store verbal reflections for failed phases:

```json
{
  "phase": "03",
  "failed": true,
  "reflection": {
    "what_happened": "Tests passed but implementation violated Single Responsibility Principle",
    "why_it_failed": "Class grew beyond 500 lines without refactoring",
    "how_to_improve": "Check line count after each implementation step"
  }
}
```

### 5. Multi-Layer Memory

```
.claude/memory/
  sessions/
    {STORY_ID}-{workflow}-session.md  # Short-term (current story)
  learning/
    tdd-patterns.md                   # Long-term (cross-story patterns)
    friction-catalog.md               # Common friction points
    success-patterns.md               # What works well
```

---

## Next Steps

1. **Review this brainstorm** for accuracy
2. **Run `/ideate`** to transform into formal requirements
3. **Create EPIC** for feedback system redesign
4. **Generate stories** for each priority feature

**Recommended command:**
```
/ideate
```

---

## Appendix: Evidence

| Finding | Source File | Specific Location |
|---------|-------------|-------------------|
| Feedback system IS working | `devforgeai/feedback/index.json` | Shows FB-2026-01-20-001 entry |
| Hooks are enabled | `devforgeai/config/hooks.yaml` | Lines 170-196 (post-dev-ai-analysis hook) |
| Observations often empty | `devforgeai/workflows/STORY-306-phase-state.json` | `"observations": []` despite 10 phases complete |
| No inline display | `.claude/agents/dev-result-interpreter.md` | Missing "Framework Insights" section |
| Phase 09 has framework-analyst | `.claude/skills/devforgeai-development/phases/phase-09-feedback.md` | Step 2.2 invokes framework-analyst |
| Observation capture protocol exists | `.claude/skills/devforgeai-development/references/observation-capture.md` | Defines schema but not enforced |
| framework-analyst handles empty input | `.claude/agents/framework-analyst.md` | Error handling section shows fallback for empty observations |

### How to Verify Current State

```bash
# Check if hooks are enabled
grep -A5 "post-dev-ai-analysis" devforgeai/config/hooks.yaml

# Check a recent phase-state file for observations
cat devforgeai/workflows/STORY-306-phase-state.json | jq '.observations'

# Check if any ai-analysis files exist
ls -la devforgeai/feedback/ai-analysis/

# Check dev-result-interpreter for Framework Insights section
grep -i "framework\|insight" .claude/agents/dev-result-interpreter.md
```

---

## Appendix: Current Observation Capture Prompt

**Location:** Each phase file (e.g., `.claude/skills/devforgeai-development/phases/phase-03-implementation.md`)

**Current Prompt (not being followed):**
```markdown
### Observation Capture (Before Exit)

**Before marking this phase complete, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds needed)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns across phases?
4. Are there gaps in tooling/docs that would help future stories?
5. Did I discover any bugs or unexpected behavior?

**If YES to any:** Append observation to phase-state.json `observations` array:
{
  "id": "obs-{phase}-{seq}",
  "phase": "{current_phase}",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files if any}"],
  "severity": "{low|medium|high}"
}

**If NO observations:** Continue to exit gate (no action needed).
```

**Why It's Not Working:**
1. The prompt is at the END of each phase - by then, Claude is focused on completing the phase exit gate
2. It's generic (same 5 questions for all phases) - doesn't prompt for phase-specific observations
3. It's optional ("If NO observations: Continue") - easy to skip under context pressure
4. Subagent outputs aren't analyzed for observations - rich data is lost

---

## References

- [LangSmith Observability](https://www.langchain.com/langsmith/observability)
- [Reflexion GitHub (NeurIPS 2023)](https://github.com/noahshinn/reflexion)
- [CrewAI Memory Documentation](https://docs.crewai.com/en/concepts/memory)
- [LangChain State of Agent Engineering 2026](https://www.langchain.com/state-of-agent-engineering)
