# Discovery Mode Methodology - Internet-Sleuth

**Purpose:** High-level exploration and feasibility assessment for new ideas, technologies, or market opportunities.

**When to Use:** spec-driven-ideation Phase 5 (Feasibility & Constraints Analysis), early epic planning, technology evaluation pre-architecture

**Loaded:** Conditionally (when research_mode = "discovery")

**Location:** Absorbed from internet-sleuth-integration per ADR-045

---

## Discovery Mode Overview

**Scope:** Broad exploration (breadth over depth)
**Duration:** 3-5 minutes (p95)
**Output:** Feasibility score (0-10), high-level alternatives, go/no-go recommendation

**Research Questions Answered:**
- "Is this idea technically feasible?"
- "What are the main alternatives?"
- "What are high-level risks?"
- "Should we proceed to architecture phase?"

**Not Answered (Use investigation mode instead):**
- "How exactly should we implement this?"
- "What are all possible edge cases?"
- "What's the optimal database schema?"

---

## Discovery Workflow (6 Steps)

### Step 1: Define Research Scope

**Goal:** Clarify what to discover and boundaries.

**Inputs:**
- Epic description or business idea
- Workflow state (usually "Backlog" or early "Architecture")
- Current context files (if brownfield project)

**Actions:**
1. Extract research questions from epic/idea
2. Set exploration boundaries (technology, market, budget)
3. Document assumptions

**Outputs:**
- Research question list (3-5 primary questions)
- Scope boundaries (in-scope vs out-of-scope)
- Assumptions document

### Step 2: Broad Research

**Goal:** Gather high-level information from multiple sources.

**Query Structure:**
```
"What are the pros and cons of [TECHNOLOGY] for [USE CASE]?
Include: performance benchmarks, community support, learning curve, cost.
Cite official documentation and recent surveys (2023+)."
```

**Actions:**
1. Execute 3-5 queries (parallel if possible)
2. Collect responses with source URLs
3. Extract key facts, statistics, trade-offs
4. Note source quality scores

**Retry Logic:**
- Max 3 retries per query
- Exponential backoff: 1s, 2s, 4s
- Cache partial results on rate limit (429)

### Step 3: Alternatives Identification

**Goal:** Identify 3-5 viable alternatives for comparison.

**Criteria for Inclusion:**
- Active development (commits within last 6 months)
- Sufficient community (>=500 GitHub stars OR corporate backing)
- Compatible with constraints (tech-stack.md, architecture-constraints.md)
- Documented integration (official guides available)

**Actions:**
1. Filter alternatives by constraints
2. Score each alternative (0-10) on: Technical fit, Cost efficiency, Developer experience, Scalability
3. Calculate composite score
4. Rank alternatives by composite score

### Step 4: Feasibility Assessment

**Goal:** Determine technical feasibility score (0-10) and go/no-go recommendation.

**Feasibility Dimensions:**
1. **Technical Feasibility (0-10)** - Does technology exist and work?
2. **Team Capability (0-10)** - Does team have required skills?
3. **Risk Assessment (0-10, inverted)** - Vendor lock-in, breaking changes, sustainability
4. **Cost Feasibility (0-10)** - Within budget?

**Composite Feasibility Score:**
```
score = (technical * 0.4) + (capability * 0.2) + (risk * 0.2) + (cost * 0.2)
```

**Go/No-Go Thresholds:**
- **9-10:** GO (high confidence, low risk)
- **7-8.9:** GO with caution (identify mitigation strategies)
- **5-6.9:** CONDITIONAL (requires deeper investigation or risk acceptance)
- **0-4.9:** NO-GO (too risky, insufficient feasibility)

### Step 5: Framework Compliance Validation

**Goal:** Validate research findings against all 6 DevForgeAI context files.

**Validation Workflow:**
1. Load context files (tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md)
2. Check recommendations against constraints
3. Invoke context-validator subagent
4. Categorize violations by severity (CRITICAL/HIGH/MEDIUM/LOW)
5. HALT on CRITICAL violations -> AskUserQuestion

### Step 6: Report Generation

**Goal:** Create standardized research report with all findings.

**Report Sections (9 Required):**
1. Executive Summary
2. Research Scope
3. Methodology Used
4. Findings
5. Framework Compliance Check
6. Workflow State
7. Recommendations
8. Risk Assessment
9. ADR Readiness

---

## Integration with spec-driven-ideation

**Invocation Point:** Phase 5 (Feasibility & Constraints Analysis)

**Workflow:**
1. Determine if feasibility research needed
2. Invoke internet-sleuth (discovery mode) via Task()
3. Receive research report (feasibility score, recommendations, risks)
4. Incorporate into epic document
5. Update epic YAML frontmatter with research_references

---

## Success Criteria

Discovery mode research succeeds when:
- [ ] Research scope clearly defined (3-5 questions, boundaries, assumptions)
- [ ] Broad research completed (3-5 queries with quality sources)
- [ ] Alternatives identified (3-5 viable options with comparison matrix)
- [ ] Feasibility score calculated (0-10 with dimension breakdown)
- [ ] Framework compliance validated (6 context files checked, violations categorized)
- [ ] Report generated (9 required sections, YAML frontmatter correct)
- [ ] Duration <5 minutes (p95 threshold)
- [ ] Token usage <50K (within budget)

---

**Created:** 2025-11-17
**Absorbed into spec-driven-research:** 2026-03-20 (ADR-045)
**Version:** 1.1
**Purpose:** High-level exploration and feasibility assessment workflow
