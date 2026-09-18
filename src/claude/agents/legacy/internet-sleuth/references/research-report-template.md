# Research Report Template for Internet Sleuth

**Version**: 1.0 | **Status**: Reference | **Agent**: internet-sleuth

---

## YAML Frontmatter Schema

```yaml
---
research_id: {research_id}           # Gap-aware ID (RESEARCH-001, RESEARCH-002, ...)
epic_id: {epic_id} | null            # From conversation context or null
story_id: {story_id} | null          # From conversation context or null
workflow_state: {detected_state}     # From Step 1.4
research_mode: {mode}                # From Phase 0 Step 0.1
timestamp: {iso8601_timestamp}       # YYYY-MM-DDTHH:MM:SSZ
quality_gate_status: {status}        # From Step 3.1.2
version: "2.0"                       # Template version
---
```

## 9 Required Sections

1. **Executive Summary:** 2-3 sentences (what researched, key finding, critical insight/risk)
2. **Research Scope:** Questions, boundaries, assumptions
3. **Methodology Used:** Research mode, duration, data sources, methodology steps
4. **Findings:** Mode-specific (comparison matrix, code patterns, SWOT, etc.)
5. **Framework Compliance Check:** Validation table (from Step 3.1.5)
6. **Workflow State:** Current state, research focus, staleness check
7. **Recommendations:** Top 3 ranked with scores, benefits, drawbacks, applicability
8. **Risk Assessment:** 5-10 risks with severity, probability, impact, mitigation
9. **ADR Readiness:** Required (Yes/No), ADR title, evidence summary, next steps

## Complete Report Template

```markdown
---
research_id: RESEARCH-{NNN}           # Gap-aware ID (RESEARCH-001, RESEARCH-002, ...)
epic_id: {EPIC-ID} | null             # From context or null
story_id: {STORY-ID} | null           # From context or null
workflow_state: {state}               # Detected state (Backlog through Released)
research_mode: {mode}                 # discovery|investigation|competitive-analysis|repository-archaeology|market-intelligence
timestamp: {ISO8601}                  # YYYY-MM-DDTHH:MM:SSZ
quality_gate_status: {status}         # PASS|WARN|FAIL|BLOCKED
version: "2.0"                        # Template version
---

# Research Report Title

## 1. Executive Summary
[2-3 sentences: what researched, key finding, critical insight/risk]

## 2. Research Scope
[Questions, boundaries, assumptions]

## 3. Methodology Used
[Mode, duration, data sources, methodology steps]

## 4. Findings
[Mode-specific findings: comparison matrix, code patterns, SWOT, etc.]

## 5. Framework Compliance Check
[Validation table showing 6 context files status + violations]

## 6. Workflow State
[Current state, research focus, staleness check]

## 7. Recommendations
[Top 3 ranked with scores, benefits, drawbacks, applicability]

## 8. Risk Assessment
[5-10 risks with severity, probability, impact, mitigation]

## 9. ADR Readiness
[Required Yes/No, ADR title, evidence summary, next steps]

**Report Generated:** {timestamp} | **Location:** {filepath} | **Version:** 2.0
```

## Output Locations

- **Feasibility research (epic/story-specific):** `devforgeai/specs/research/feasibility/{EPIC-ID or STORY-ID}-{timestamp}-research.md`
- **General research (multi-epic):** `devforgeai/specs/research/shared/RESEARCH-{NNN}-{topic}.md`
- **Example reports:** `devforgeai/specs/research/examples/{example-name}.md`

## Naming Conventions

- Research ID: `RESEARCH-{NNN}` (gap-aware, 3-digit zero-padded, fills gaps before incrementing)
- Timestamp slug: `YYYY-MM-DD-HHMMSS` format
- Topic slug: `kebab-case` (e.g., oauth2-evaluation, react-patterns)

## Report Structure

- YAML frontmatter: research_id, epic_id, story_id, workflow_state, research_mode, timestamp, quality_gate_status, version
- 9 required sections: Executive Summary through ADR Readiness (per this template)
- Footer: Report generated timestamp, location, research ID, version
