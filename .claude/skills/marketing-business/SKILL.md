---
name: marketing-business
description: Go-to-market strategy builder with channel selection matrix, budget allocation, and 30-day launch action plan. Use when users need to create marketing strategies or go-to-market plans.
---

# Marketing Business

Marketing and customer acquisition skill that guides users through creating structured go-to-market strategies. Produces actionable GTM plans with channel prioritization, budget allocation, and launch timelines.

## When to Use

- User wants to create a go-to-market strategy
- User needs channel recommendations for their business model
- User wants a 30-day launch action plan
- User needs marketing budget allocation guidance

## Workflows

### Go-to-Market Strategy Builder

Guides user through creating a complete GTM plan based on business model, budget, and target audience.

**Reference Files:**
- `references/go-to-market-framework.md` - Complete GTM workflow with channel scoring, budget allocation rules, and action plan templates
- `references/channel-selection-matrix.md` - Channel scoring data for 8+ business model types

**Output File:** `devforgeai/specs/business/marketing/go-to-market.md`

**Workflow Steps:**

1. **Gather Inputs** via AskUserQuestion:
   - Business model type (SaaS B2B, SaaS B2C, Marketplace, D2C, E-commerce, Subscription, Freemium, Agency)
   - Monthly marketing budget range
   - Target audience description

2. **Channel Selection:**
   - Load `references/channel-selection-matrix.md`
   - Score channels based on business model, budget, and audience
   - Rank minimum 3 channels with rationale
   - Allocate budget percentages (must sum to 100%)

3. **30-Day Launch Plan:**
   - Generate minimum 10 action items
   - Assign to 3 time windows: Days 1-7, Days 8-21, Days 22-30
   - Tag each item with responsible role (founder, marketer, engineer)

4. **Output Generation:**
   - Write complete GTM plan to output file
   - Include 4 required sections: Executive Summary, Channel Strategy, Budget Allocation, 30-Day Launch Plan
   - Validate Markdown structure (ATX headings)

**Edge Cases:**
- Zero budget: Recommend organic-only channels
- Unknown business model: Ask up to 3 clarifying questions
- Existing output file: Prompt before overwrite
- Conflicting model/audience: Detect mismatch and advise

## Business Rules

- Budget allocation percentages must sum to 100%
- Minimum 3 channels ranked per recommendation
- Minimum 10 action items in 30-day plan
- All action items must have role tags
- Zero-budget input produces organic-only recommendations

## References

- EPIC-075: Marketing & Customer Acquisition
- STORY-539: Go-to-Market Strategy Builder
