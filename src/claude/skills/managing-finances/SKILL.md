---
name: managing-finances
description: Guides entrepreneurs through financial planning including pricing strategy selection and financial modeling
tools: Read, Write, Edit, Bash
model: inherit
---

# Managing Finances Skill

## Purpose

This skill helps entrepreneurs develop financial plans for their business, including pricing models, revenue projections, and cost analysis.

## When to Use

- When an entrepreneur needs to set pricing for their product or service
- When financial modeling or revenue planning is required
- When cost structure analysis is needed

## Workflow

### Phase 1: Financial Context Discovery

Gather business context: product/service type, target market, cost structure, and competitive landscape.

### Phase 2: Pricing Strategy

Guide the user through selecting and executing a pricing strategy.

This phase uses the pricing-strategy-framework reference to walk the user through three pricing approaches (cost-plus, value-based, competitive) and produce a documented pricing model.

For full details, see: [pricing-strategy-framework.md](references/pricing-strategy-framework.md) (Pricing Strategy Framework)

### Phase 3: Revenue Projection

Build revenue projections based on the selected pricing model and market assumptions.

### Phase 4: Financial Summary

Compile all financial artifacts into a cohesive financial plan.

### Phase 5: Break-Even Analysis

Calculate break-even point in units and revenue, generate an ASCII chart visualization, and append results to the financial projections file.

This phase guides the user through providing fixed costs, variable cost per unit, and selling price per unit, then computes break-even metrics with full formula transparency.

For full details, see: [break-even-analysis.md](references/break-even-analysis.md) (Break-Even Analysis)

## References

| Reference | Path | When to Load |
|-----------|------|--------------|
| Pricing Strategy Framework | `references/pricing-strategy-framework.md` | Phase 2: Pricing strategy selection and calculation |
| Break-Even Analysis | `references/break-even-analysis.md` | Phase 5: Break-even calculation, chart, and projections output |

## Success Criteria

- [ ] Pricing strategy selected and documented
- [ ] Pricing model output written to `devforgeai/specs/business/financial/pricing-model.md`
- [ ] All outputs include "not financial advice" disclaimer
