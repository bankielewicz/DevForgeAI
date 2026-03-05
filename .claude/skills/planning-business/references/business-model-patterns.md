---
title: Business Model Pattern Matching
story_id: STORY-533
version: "1.0"
created: 2026-03-04
---

# Business Model Pattern Matching

Reference for the planning-business skill. Provides detection signal patterns, confidence scoring, and per-model guidance for classifying business models from lean canvas and ideation artifacts.

---

## Detection Signals

Identify the business model type by analyzing detection signal keywords and structures found in the lean canvas, brainstorm documents, and requirements artifacts.

**Signal sources:**
- Lean canvas sections (problem, solution, revenue streams, channels)
- User-provided descriptions and brainstorm notes
- Revenue model keywords and pricing language
- Customer segment definitions

**Detection process:**
1. Extract keywords from each canvas section
2. Match keywords against model-specific signal lists below
3. Score each candidate model by signal density
4. Rank candidates by confidence score

---

## Confidence Levels

| Level | Threshold | Meaning |
|-------|-----------|---------|
| high | >= 0.8 | Strong signal match. Proceed with this model classification. |
| medium | >= 0.5 | Moderate signal match. Viable candidate but verify with user. |
| low | < 0.5 | Weak signal match. Insufficient evidence for classification. |

A confidence score is calculated as: `matched_signals / total_signals_for_model`, expressed as a decimal from 0.0 to 1.0 (where 1.0 = 100% match).

---

## SaaS

**Detection signal keywords:** subscription, recurring revenue, monthly/annual pricing, churn, MRR, ARR, freemium, trial, seats, per-user, cloud-hosted, multi-tenant, onboarding, retention.

**Framework guidance:** Use subscription economics framework. Evaluate unit economics (CAC, LTV, LTV:CAC ratio). Map the customer journey from trial to paid conversion.

**Key metric targets:**
- Monthly Recurring Revenue (MRR) growth rate
- Churn rate (target < 5% monthly)
- Customer Acquisition Cost (CAC) payback period
- Net Revenue Retention (NRR)
- Trial-to-paid conversion rate

**Lean canvas emphasis:** Revenue Streams (subscription tiers), Key Metrics (MRR, churn), Unfair Advantage (switching costs, data lock-in).

---

## Marketplace

**Detection signal keywords:** buyers, sellers, two-sided, platform, commission, take rate, transaction fee, listing, matching, network effects, liquidity, GMV, supply, demand.

**Framework guidance:** Use platform economics framework. Evaluate chicken-and-egg dynamics, liquidity thresholds, and network effect strength. Map supply-side and demand-side acquisition separately.

**Key metric targets:**
- Gross Merchandise Volume (GMV)
- Take rate percentage
- Supply-side and demand-side acquisition costs
- Match rate / transaction success rate
- Repeat transaction rate

**Lean canvas emphasis:** Channels (separate for supply/demand), Revenue Streams (commission model), Key Metrics (GMV, liquidity).

---

## Service

**Detection signal keywords:** consulting, hourly rate, project-based, retainer, billable hours, deliverables, SOW, engagement, expertise, custom, bespoke, professional services, agency.

**Framework guidance:** Use service delivery framework. Evaluate utilization rates, margin per engagement, and scalability constraints. Map the sales pipeline from lead to signed contract.

**Key metric targets:**
- Revenue per employee
- Utilization rate (target > 70%)
- Average contract value
- Client retention rate
- Gross margin per engagement

**Lean canvas emphasis:** Cost Structure (labor-heavy), Revenue Streams (project/retainer), Key Metrics (utilization, margin).

---

## Product

**Detection signal keywords:** one-time purchase, unit price, inventory, SKU, manufacturing, shipping, retail, wholesale, COGS, physical, digital download, license, perpetual.

**Framework guidance:** Use product economics framework. Evaluate unit margins, inventory turns, and distribution channel costs. Map the product lifecycle from development to end-of-life.

**Key metric targets:**
- Gross margin per unit
- Customer Acquisition Cost (CAC)
- Average Order Value (AOV)
- Repeat purchase rate
- Inventory turnover (physical products)

**Lean canvas emphasis:** Cost Structure (COGS, manufacturing), Channels (distribution), Revenue Streams (unit sales).

---

## Ambiguity Handling

When detection signals produce ambiguous results, apply these rules:

**Ambiguity threshold:** If the confidence gap between the top two candidate models is less than 0.1, the result is ambiguous and requires user intervention.

**Resolution process:**
1. Rank all candidate models by confidence score (descending)
2. If the gap between rank 1 and rank 2 candidates is < 0.1, flag as ambiguous
3. Present the top candidates to the user with signal evidence for each
4. Invoke AskUserQuestion to let the user select the correct model

**AskUserQuestion format for ambiguous results:**
- Present the top 2-3 candidate models with their confidence scores
- Show which detection signals matched for each candidate
- Ask the user to select which model best describes their business
- Include an "Other / Hybrid" option for edge cases

**Hybrid models:** If the user confirms elements of multiple models (e.g., SaaS + Marketplace), create a composite profile noting the primary and secondary model types. Weight framework and metric guidance 70/30 toward the primary model.
