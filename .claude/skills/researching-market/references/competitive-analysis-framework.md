# Competitive Analysis Framework

Reference documentation for the competitive analysis phase of the researching-market skill.

---

## Purpose

This reference provides detailed methodology for the market-analyst subagent when synthesizing competitive landscape data into structured positioning analysis.

---

## Analysis Methodology

### Step 1: Competitor Identification

Gather competitor names from internet-sleuth research output:
1. Extract company/product names mentioned in market reports
2. Identify direct competitors (same market, same customer segment)
3. Identify indirect competitors (adjacent market or substitute products)
4. Deduplicate by name (case-insensitive matching)

### Step 2: Data Collection Per Competitor

For each identified competitor, collect:

| Dimension | Description | Requirement |
|-----------|-------------|-------------|
| **Name** | Company or product name | Required |
| **Category** | Market category or segment | Required |
| **Strengths** | Competitive advantages | Minimum of 1 |
| **Weaknesses** | Competitive disadvantages | Minimum of 1 |
| **Market Position Summary** | Brief market standing description | Required |
| **Differentiation** | Unique positioning factors | Minimum of 1 |

### Step 3: Count Enforcement

- If fewer than 3 competitors identified: Prompt user via AskUserQuestion for additional names
- If more than 10 competitors identified: Truncate to top 10 by market relevance, display warning

### Step 4: Deduplication

- Normalize competitor names (case-insensitive)
- Merge entries that reference the same entity (e.g., "Google Cloud" and "GCP")
- Note aliases in the merged entry

### Step 5: Data Completeness

- If a competitor has no strength or weakness data: Include entry with "Data insufficient" flag
- Never omit a competitor due to missing data
- Flag gaps explicitly for manual research follow-up

---

## Output Structure

The competitive analysis output follows this template:

```markdown
# Competitive Landscape Analysis: [Business/Market]

## Positioning Matrix

| Name | Category | Strengths | Weaknesses | Market Position Summary | Differentiation |
|------|----------|-----------|------------|------------------------|-----------------|
| [Competitor 1] | [Category] | [Strengths] | [Weaknesses] | [Summary] | [Differentiation] |

## Competitor Profiles

### [Competitor Name]
- **Category**: [segment]
- **Strengths**: [list]
- **Weaknesses**: [list]
- **Market Position**: [summary]
- **Differentiation**: [unique factors]

## Differentiation Opportunities

Based on competitive analysis, the following differentiation opportunities exist:
1. [Gap or opportunity identified from competitor weaknesses]
```

---

## Integration Points

- **Input**: Research data from internet-sleuth subagent (Step 5 of skill workflow)
- **Output**: Written to `devforgeai/specs/business/market-research/competitive-analysis.md`
- **Consumed by**: planning-business skill, coaching-entrepreneur skill

---

## Error Handling

| Scenario | Action |
|----------|--------|
| No research data provided | Return error: "No research data available for competitive analysis" |
| All competitors have insufficient data | Complete with "Data insufficient" flags on all entries |
| Duplicate competitor names detected | Merge and note aliases |
