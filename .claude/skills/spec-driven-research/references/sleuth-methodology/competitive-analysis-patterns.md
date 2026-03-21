# Competitive Analysis Patterns - Internet-Sleuth

**Purpose:** Analyze market landscape, competitive positioning, and SWOT analysis for technology/product decisions.

**When to Use:** spec-driven-ideation Phase 5 (market viability assessment), strategic planning, vendor selection, differentiation analysis

**Loaded:** Conditionally (when research_mode = "competitive-analysis")

**Location:** Absorbed from internet-sleuth-integration per ADR-045

---

## Competitive Analysis Overview

**Scope:** Market landscape and strategic positioning (competitive intelligence)
**Duration:** 6-8 minutes (p95)
**Output:** Competitive matrix, SWOT analysis, market positioning recommendations

**Research Questions Answered:**
- "Who are our competitors in [market]?"
- "What are their strengths and weaknesses?"
- "How do we differentiate from competitors?"
- "What are market opportunities and threats?"

---

## Competitive Analysis Workflow (7 Steps)

### Step 1: Define Competitive Scope
- Market segment (industry, target audience, geography, price tier)
- Competitive set (direct, indirect, substitutes, adjacent)
- Comparison dimensions (features, pricing, tech stack, UX, market share, differentiation)

### Step 2: Competitor Research
- Official sources (websites, docs, marketing materials) - Quality: 10/10
- Third-party reviews (G2, Capterra, industry reports) - Quality: 7-8/10
- Community discussions (Reddit, HackerNews, Product Hunt) - Quality: 5-6/10
- Technical analysis (GitHub repos, Stack Overflow, API docs) - Quality: 8/10

### Step 3: Feature Comparison Matrix
- 10-15 key features compared across competitors
- Score features: Full support / Limited / Not supported
- Identify feature gaps and parity assessment

### Step 4: Pricing Analysis
- Base plans, usage-based costs, add-ons, hidden costs
- Cost scenarios at different scales (1K, 10K, 100K users)
- 3-year Total Cost of Ownership (TCO) analysis

### Step 5: SWOT Analysis
- Strengths (internal advantages with evidence)
- Weaknesses (internal disadvantages with impact)
- Opportunities (external advantages with market evidence)
- Threats (external disadvantages with competitive evidence)
- Strategic positioning (SO, WO, ST, WT strategies)

### Step 6: Market Positioning Map
- 2-axis positioning visualization
- Competitive clustering identification
- Whitespace opportunity detection
- Positioning statement generation

### Step 7: Report Generation
- 9 required sections with YAML frontmatter
- Competitive matrix, SWOT, pricing tables embedded
- Save to devforgeai/specs/research/

---

## Success Criteria

Competitive analysis succeeds when:
- [ ] Competitive scope defined (market segment, 4-8 competitors, comparison dimensions)
- [ ] Competitor research complete (detailed profiles with sources)
- [ ] Feature comparison matrix created (10-15 features, all competitors)
- [ ] Pricing analysis complete (3 scenarios, TCO calculated)
- [ ] SWOT analysis synthesized (4 quadrants, 4-5 items each)
- [ ] Market positioning map created (2-axis visual, whitespace identified)
- [ ] Report generated (9 sections, positioning recommendation)
- [ ] Duration <8 minutes (p95 threshold)
- [ ] Token usage <50K (within budget)

---

**Created:** 2025-11-17
**Absorbed into spec-driven-research:** 2026-03-20 (ADR-045)
**Version:** 1.1
**Purpose:** Market landscape analysis and competitive positioning
