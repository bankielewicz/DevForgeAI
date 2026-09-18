# Research Report Template

**Purpose:** Standard structure for all internet-sleuth research reports ensuring consistency, completeness, and framework compliance.

**Usage:** All research reports must follow this template structure (9 required sections + YAML frontmatter).

**Location:** Absorbed from internet-sleuth-integration per ADR-045

---

## YAML Frontmatter Schema

**All fields required unless marked optional:**

```yaml
---
# Identifiers
research_id: RESEARCH-NNN         # Gap-aware ID (RESEARCH-001, RESEARCH-002, ...)
epic_id: EPIC-NNN | null          # Epic this research supports (null if not epic-specific)
story_id: STORY-NNN | null        # Story this research supports (null if not story-specific)

# Workflow Context
workflow_state: Backlog | Architecture | Ready for Dev | In Development | Dev Complete | QA In Progress | QA Approved | QA Failed | Releasing | Released
research_mode: discovery | investigation | competitive-analysis | repository-archaeology | market-intelligence

# Metadata
timestamp: YYYY-MM-DDTHH:MM:SSZ   # ISO 8601 format
quality_gate_status: PASS | WARN | FAIL | BLOCKED
version: "2.0"                    # Template version

# Optional Fields
author: string | null              # Researcher name (null if agent-generated)
tags: [string] | null              # Keywords (e.g., ["authentication", "oauth2", "aws"])
---
```

**Validation Rules:**
- `research_id` must match pattern `RESEARCH-[0-9]{3}`
- `epic_id` must exist in `devforgeai/specs/Epics/` if not null
- `story_id` must exist in `devforgeai/specs/Stories/` if not null
- `workflow_state` must be one of 11 valid DevForgeAI states
- `research_mode` must be one of 5 valid modes
- `timestamp` must be valid ISO 8601 datetime
- `quality_gate_status` must be PASS | WARN | FAIL | BLOCKED

---

## Report Sections (9 Required)

### 1. Executive Summary
- 2-3 sentences: what was researched, key recommendation, critical insight/risk
- Must include feasibility or quality score if applicable

### 2. Research Scope
- 3-5 primary research questions
- In-scope vs out-of-scope boundaries
- Technology constraints (from context files)
- Assumptions (budget, scale, timeline)

### 3. Methodology Used
- Research mode specified
- Duration (minutes:seconds)
- Data sources with quality scores
- Methodology steps enumerated

### 4. Findings
- Format varies by research mode (comparison matrix, code examples, SWOT)
- Evidence-based with sources
- Quality scores included

### 5. Framework Compliance Check
- Validation timestamp
- 6/6 context files checked
- Status per file (PASS/WARN/FAIL/BLOCKED)
- Violation details with severity
- Quality gate status

### 6. Workflow State
- Current workflow state
- Research focus alignment
- Staleness check (CURRENT or STALE)

### 7. Recommendations
- Top 3 ranked with scores
- Benefits and drawbacks for each
- Applicability criteria
- Implementation details (effort, complexity, prerequisites)

### 8. Risk Assessment
- 5-10 risks with severity, probability, impact
- Mitigation strategy for each
- Risk matrix visualization (optional)

### 9. ADR Readiness
- ADR required? (Yes/No/Conditional)
- ADR title if required
- Evidence collection status
- Next steps

---

## Template Footer

```markdown
---

**Report Generated:** YYYY-MM-DD HH:MM:SS
**Report Location:** devforgeai/specs/research/[feasibility|examples|shared]/[filename].md
**Research ID:** RESEARCH-NNN
**Version:** 2.0 (template version)
```

---

## Validation Checklist

- [ ] YAML frontmatter complete (all required fields)
- [ ] research_id follows pattern `RESEARCH-[0-9]{3}`
- [ ] All 9 sections present
- [ ] Executive Summary <=3 sentences
- [ ] Research Scope has 3-5 questions
- [ ] Framework Compliance validates all 6 context files
- [ ] Recommendations ranked (top 3 with scores)
- [ ] Risk Assessment has 5-10 risks with mitigation
- [ ] ADR Readiness status clear
- [ ] Report footer included

---

**Created:** 2025-11-17
**Absorbed into spec-driven-research:** 2026-03-20 (ADR-045)
**Template Version:** 2.0
**Purpose:** Standard structure for all internet-sleuth research reports
