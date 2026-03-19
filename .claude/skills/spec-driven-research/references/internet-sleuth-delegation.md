# internet-sleuth Delegation Contract

Subagent contract for Phase 02 (Research Execution).

---

## Overview

Phase 02 delegates research execution to the `internet-sleuth` subagent, which provides:
- **Repository archaeology** - Clone and analyze GitHub repos for code patterns
- **Context validation** - Validates recommendations against DevForgeAI context files
- **Progressive methodology** - Loads mode-specific research guides (65% token savings)
- **Multi-source synthesis** - Cross-references multiple sources for accuracy

---

## Category-to-Mode Mapping

| Research Category | internet-sleuth Mode | Research Focus |
|-------------------|---------------------|----------------|
| `competitive` | `competitive-analysis` | Competitor features, pricing, positioning, market share |
| `technology` | `repository-archaeology` | Code patterns, GitHub analysis, library evaluation |
| `market` | `market-intelligence` | Statistics, trends, developer needs, pain points |
| `integration` | `investigation` | APIs, SDKs, integration patterns, rate limits |
| `architecture` | `discovery` | Design patterns, best practices, case studies |

---

## Task() Invocation Template

```python
Task(
    subagent_type="internet-sleuth",
    description=f"{category_code} research: {topic}",
    prompt=f"""
Research Mode: {research_mode}
Topic: {topic}
Research ID: {RESEARCH_ID}

Research Questions:
{questions_formatted}

Execute comprehensive research following your methodology for {research_mode} mode.

Return structured findings with:
1. Executive summary (2-3 sentences max)
2. Key findings with evidence and citations
3. Recommendations ranked by priority (High/Medium/Low)
4. Sources with credibility assessment (title, URL, brief description)
5. Framework compliance check results (validate against DevForgeAI context files if applicable)

Format your output clearly with section headers so findings can be parsed:
- Use "## Key Findings" for findings
- Use "## Recommendations" for recommendations
- Use "## Sources" for sources

Note: Results will be formatted into {RESEARCH_ID} research document.
"""
)
```

---

## Expected Output Format

The internet-sleuth subagent should return output containing these sections:

### Required Sections

```markdown
## Executive Summary
2-3 sentence overview of research findings.

## Key Findings

### Finding 1: [Title]
[Description with evidence]
**Evidence:** [Source](URL) - "Quote"
**Confidence:** High|Medium|Low

### Finding 2: [Title]
...

## Recommendations

### Recommendation 1: [Action] [Priority: High|Medium|Low]
**Rationale:** Why this is recommended
**Effort:** Low|Medium|High
...

## Sources
- [Source Title](URL) - Brief description
- [Source Title](URL) - Brief description
...
```

### Optional Sections

```markdown
## Framework Compliance
- tech-stack.md: [Compatible|Conflict|Not Applicable]
- architecture-constraints.md: [Compatible|Conflict|Not Applicable]
- anti-patterns.md: [No violations|Violations detected]
```

---

## Parsing Sleuth Output

```python
def extract_section(section_name, output):
    """Extract content between ## section_name and the next ## heading."""
    pattern = f"## {section_name}\n(.*?)(?=\n## |$)"
    match = re.search(pattern, output, re.DOTALL)
    return match.group(1).strip() if match else ""

findings = extract_section("Key Findings", sleuth_output)
recommendations = extract_section("Recommendations", sleuth_output)
sources = extract_section("Sources", sleuth_output)
```

---

## Fallback Trigger Conditions

Switch to direct WebSearch/WebFetch (using `search-strategies.md`) when:

1. **Task() returns error** - internet-sleuth subagent unavailable or crashed
2. **Empty output** - Sleuth returned but produced no findings
3. **Timeout** - Research execution exceeded reasonable time
4. **Missing sections** - Output lacks all three required sections (findings, recommendations, sources)

### Fallback Procedure

```
Display: "internet-sleuth unavailable - falling back to direct web search"
Read(file_path="src/claude/skills/spec-driven-research/references/search-strategies.md")
# Execute the category-specific search strategy from that reference
```

---

## Subagent Reference

- **Agent definition:** `src/claude/agents/internet-sleuth.md`
- **Enforcement:** BLOCKING - Phase 02 cannot complete without either sleuth output or fallback search results
- **Deviation:** If neither sleuth nor fallback produces results, HALT and use AskUserQuestion to get user guidance
