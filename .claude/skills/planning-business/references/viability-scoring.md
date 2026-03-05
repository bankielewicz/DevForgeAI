---
title: Viability Scoring
story_id: STORY-533
version: "1.0"
created: 2026-03-04
---

# Viability Scoring

Reference for the planning-business skill. Defines the scoring rubric, weighted dimensions, and pass/fail thresholds for business model viability assessment.

---

## Scoring Rubric

Each business model is scored across multiple dimensions. Per-dimension scores range from 0 to 100. The final viability score is a weighted average of all dimension scores.

**Scoring scale per dimension:**
- 90-100: Exceptional strength, clear competitive advantage
- 70-89: Solid foundation, minor risks manageable
- 50-69: Viable but significant gaps require attention
- 30-49: Weak, substantial investment needed to reach viability
- 0-29: Critical deficiency, likely not viable without pivot

---

## Dimensions

Score each of the following dimensions independently.

### 1. Market Opportunity (weight: 0.25)

Assess total addressable market size, growth trajectory, and competitive density.

| Score Range | Criteria |
|-------------|----------|
| 80-100 | Large TAM (>$1B), growing market, fragmented competition |
| 50-79 | Moderate TAM, stable or growing, some established competitors |
| 0-49 | Small TAM, shrinking market, or dominated by incumbents |

### 2. Revenue Model Clarity (weight: 0.20)

Assess how clearly defined and defensible the revenue streams are.

| Score Range | Criteria |
|-------------|----------|
| 80-100 | Proven pricing model, clear willingness-to-pay evidence |
| 50-79 | Defined pricing model, limited validation |
| 0-49 | Unclear monetization, no pricing validation |

### 3. Execution Feasibility (weight: 0.20)

Assess whether the team and resources can deliver the solution within constraints.

| Score Range | Criteria |
|-------------|----------|
| 80-100 | Team has domain expertise, tech is well-understood, timeline realistic |
| 50-79 | Partial expertise, some technical unknowns, tight timeline |
| 0-49 | Missing critical skills, unproven technology, unrealistic timeline |

### 4. Customer Validation (weight: 0.20)

Assess evidence of real customer demand beyond assumptions.

| Score Range | Criteria |
|-------------|----------|
| 80-100 | Paying customers or signed LOIs, strong interview/survey data |
| 50-79 | Positive user feedback, waitlist signups, pilot interest |
| 0-49 | No customer contact, assumptions only |

### 5. Defensibility (weight: 0.15)

Assess barriers to competition and long-term moat potential.

| Score Range | Criteria |
|-------------|----------|
| 80-100 | Strong network effects, proprietary data/tech, regulatory barriers |
| 50-79 | Some switching costs, brand recognition, first-mover advantage |
| 0-49 | Easily replicable, no moat, commodity risk |

---

## Weight Summary

| Dimension | Weight |
|-----------|--------|
| Market Opportunity | 0.25 |
| Revenue Model Clarity | 0.20 |
| Execution Feasibility | 0.20 |
| Customer Validation | 0.20 |
| Defensibility | 0.15 |
| **Total** | **1.00** |

---

## Thresholds

| Final Score | Result | Action |
|-------------|--------|--------|
| >= 70 | PASS | Proceed with business planning and story creation |
| >= 50 and < 70 | BORDERLINE | Flag risks, present to user for go/no-go decision |
| < 50 | FAIL | Recommend pivot, further validation, or scope reduction |

**BORDERLINE handling:** Present the dimension breakdown to the user via AskUserQuestion. Highlight dimensions scoring below 50 as critical gaps. Let the user decide whether to proceed, pivot, or investigate further.

---

## Calculation

```
final_score = sum(dimension_score * dimension_weight for each dimension)
```

Round the final score to the nearest integer.

---

## Disclaimer

This viability scoring system provides directional guidance only. It is designed to help structure early-stage thinking and surface potential risks.

This tool does not constitute financial advice. Do not use viability scores as the sole basis for financial decisions, fundraising, or resource allocation.

This tool does not constitute investment advice. Viability scores are not predictive of returns, market performance, or business success.

This tool does not constitute legal advice. Regulatory, compliance, and intellectual property considerations require qualified legal counsel.

All scores reflect subjective assessment of available information at a point in time. Actual outcomes depend on execution, market conditions, and factors outside the scope of this analysis. Users are responsible for conducting their own due diligence.
