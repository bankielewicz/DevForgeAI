# Go-to-Market Strategy Framework

**Purpose:** Guide users through creating a structured, actionable go-to-market (GTM) plan. This reference provides the channel selection matrix logic, budget allocation rules, and 30-day launch action plan template.

**Output File:** `devforgeai/specs/business/marketing/go-to-market.md`

---

## Executive Summary

The Executive Summary section provides a high-level overview of the GTM strategy, including:

- **Business Model:** The identified business model type (e.g., SaaS B2B, Marketplace, D2C)
- **Target Audience:** Primary customer segment description
- **Budget Range:** Monthly marketing budget allocation
- **Top Channels:** The 3 highest-ranked distribution channels
- **Timeline:** 30-day launch plan summary with key milestones

This section is auto-generated from the channel selection matrix output and should be written last, after all other sections are complete.

---

## Channel Strategy

The channel selection matrix scores and ranks distribution channels based on business model, budget, and target audience. The workflow produces a ranked list of recommended channels.

### Channel Ranking Process

1. Identify business model type from user input
2. Look up scoring weights in `channel-selection-matrix.md`
3. Apply budget modifier (paid channels scored lower for small budgets)
4. Apply audience modifier (B2B channels scored higher for developer audiences)
5. Rank channels by composite score, descending
6. Select top channels (minimum 3)

### Ranked Channel Output Format

Each ranked channel includes:

1. **Content Marketing** — High-value for most models; builds organic authority. Score: 9/10
2. **SEO / Organic Search** — Long-term compounding returns; low marginal cost. Score: 8/10
3. **Social Media (Organic)** — Community building and brand awareness. Score: 8/10
4. **Email Marketing** — Direct relationship with prospects; high ROI. Score: 7/10
5. **Paid Search (SEM)** — Immediate visibility for high-intent keywords. Score: 7/10
6. **Developer Communities** — Targeted reach for technical audiences. Score: 6/10

### Channel Rationale

Each channel recommendation must include:
- Why this channel fits the business model
- Expected cost range (monthly)
- Time to first results (days/weeks)
- Key metrics to track

---

## Budget Allocation

Budget allocation distributes the monthly marketing budget across selected channels. Percentages must sum to 100%.

### Default Allocation Template

| Channel | Allocation | Rationale |
|---------|-----------|-----------|
| Content Marketing | 30% | Highest long-term ROI for most models |
| SEO / Organic Search | 20% | Compounds over time, low ongoing cost |
| Social Media | 15% | Brand awareness and community building |
| Email Marketing | 15% | Direct prospect engagement |
| Paid Search (SEM) | 10% | Quick wins for high-intent traffic |
| Reserve / Testing | 10% | Experimentation with emerging channels |
| **Total** | **100%** | |

### Budget Allocation Rules

- Minimum 3 channels must receive budget allocation
- No single channel should exceed 40% allocation
- Reserve/testing budget recommended at 5-15%
- Percentages must sum to exactly 100%

### Zero-Budget Handling

When the user's budget is $0, not specified, or skipped:

- **Organic-only channels** are recommended (no paid channels)
- Recommended zero-budget channels: Content Marketing, SEO, Social Media (Organic), Community Engagement, Email (free tier)
- The Budget Allocation section is annotated with: "⚠️ Zero-budget plan: All channels are organic/free-tier only"
- Paid channels (SEM, paid social, display ads) are excluded from recommendations

---

## 30-Day Launch Plan

The 30-day post-launch action plan provides discrete, time-bound tasks organized into three phases. Each action item is tagged with the responsible role.

### Days 1-7: Foundation & Quick Wins

- Set up analytics tracking and conversion goals — **Role: engineer**
- Create landing page with clear value proposition — **Role: engineer**
- Write and publish 2 foundational blog posts — **Role: marketer**
- Set up email capture form and welcome sequence — **Role: marketer**
- Announce launch on social media profiles — **Role: founder**
- Submit product to relevant directories and listings — **Role: founder**

### Days 8-21: Momentum Building

- Publish 4 additional content pieces targeting key topics — **Role: marketer**
- Engage in 5 relevant online communities (forums, Reddit, Discord) — **Role: founder**
- Set up and optimize paid search campaign (if budget allows) — **Role: marketer**
- Conduct outreach to 10 potential partners or influencers — **Role: founder**
- Implement A/B test on landing page headline — **Role: engineer**
- Send first email newsletter to subscriber list — **Role: marketer**

### Days 22-30: Optimization & Scaling

- Analyze first 3 weeks of analytics data and identify top channels — **Role: marketer**
- Double down on top 2 performing channels — **Role: founder**
- Create case study or testimonial from early users — **Role: marketer**
- Optimize conversion funnel based on data — **Role: engineer**
- Plan Month 2 strategy based on Month 1 learnings — **Role: founder**

### Action Plan Rules

- Minimum 10 discrete action items across all windows
- Each item must be tagged with exactly one role: **founder**, **marketer**, or **engineer**
- Items should be specific and actionable (not vague aspirations)
- If template produces fewer than 10 items, pad with generic items and flag for review

---

## Ambiguity and Clarification Handling

When the user's business model type is not explicitly covered by the channel selection matrix (unknown or hybrid models), the workflow must resolve ambiguity before proceeding. The workflow asks a maximum of 3 clarifying questions:

1. What is your primary revenue model? (e.g., subscription, one-time purchase, marketplace fees, advertising)
2. Who is your primary customer? (e.g., businesses, consumers, developers, enterprises)
3. What is your primary distribution method? (e.g., self-serve, sales-led, partner-led, marketplace)

The workflow must **proceed** and not halt even for unknown business models. If clarifying questions are answered, the answers are **incorporated into the channel scoring** to adjust and refine rankings. If the user skips questions, the workflow uses a **default/generalist** channel recommendation set. The output file must still contain all 4 required sections with valid content. A note is appended: "Channel recommendations based on generalist defaults — consider refining after market validation."

After receiving clarification answers, the workflow maps answers to the closest matching business model type in the matrix, **adjusts scoring weights** based on the specific answers provided, and **updates the channel ranking** with refined scores before proceeding to generate the full GTM output.

---

## Overwrite Protection

When the output file `devforgeai/specs/business/marketing/go-to-market.md` already exists:

- The workflow must **prompt the user before overwriting** the existing file
- Display the file's last modified date
- Offer three options: **Overwrite**, **Append**, or **Abort**
- No silent overwrites are permitted (BR-004)

---

## Output File Template

The generated output file must contain exactly these 4 top-level sections in ATX heading style:

```markdown
# Go-to-Market Strategy: [Business Name]

## Executive Summary
[Auto-generated summary of GTM strategy]

## Channel Strategy
[Ranked channel list with rationale and scores]

## Budget Allocation
[Table with percentage allocation per channel, summing to 100%]

## 30-Day Launch Plan
[Time-windowed action items with role tags]
```

### Output Validation Rules

- All 4 sections (Executive Summary, Channel Strategy, Budget Allocation, 30-Day Launch Plan) must be present
- Each section must be non-empty (contain at least one paragraph or list item)
- All headings must use ATX style (# prefix, not underline)
- File must be valid Markdown

---

## Workflow Sequence

1. **Gather Inputs:** Business model type, budget range, target audience
2. **Resolve Ambiguity:** If model unknown, ask maximum of 3 clarifying questions
3. **Score Channels:** Run channel selection matrix with inputs
4. **Rank & Select:** Pick top channels (minimum 3)
5. **Allocate Budget:** Distribute budget across channels (sum to 100%)
6. **Generate Action Plan:** Create 30-day plan with role-tagged items
7. **Check Existing File:** If output exists, prompt before overwrite
8. **Write Output:** Generate `devforgeai/specs/business/marketing/go-to-market.md`
9. **Confirm:** Display success message with file path

---

**Reference:** STORY-539, EPIC-075 (Marketing & Customer Acquisition)
