# Pricing Strategy Framework

This framework guides entrepreneurs through selecting and applying a pricing strategy. All outputs include a disclaimer that this is **not financial advice** — consult a qualified professional before making financial decisions.

---

## Step 1: Strategy Selection

The user must **select one strategy** from the three options below before proceeding. Present all three strategies and ask the user to choose a strategy that best fits their business context.

### Available Strategies

| # | Strategy | Description |
|---|----------|-------------|
| 1 | **Cost-Plus Pricing** | Calculate price by adding a target margin percentage on top of your total unit cost (variable costs plus allocated fixed costs). Best for businesses with well-understood cost structures. |
| 2 | **Value-Based Pricing** | Set price based on the perceived value your product delivers to customers, anchored by willingness-to-pay (WTP) research and comparable alternatives. Best for differentiated products. |
| 3 | **Competitive Pricing** | Position your price relative to competitor pricing data from market research. Best when entering an established market with known competitor price points. |

After the user selects their strategy, proceed to the corresponding section below.

---

## Strategy 1: Cost-Plus Pricing

### Input Collection

Collect the following inputs from the user:

1. **Variable cost** per unit — direct costs that scale with production (materials, labor per unit)
2. **Fixed cost** total — overhead costs that do not change with volume (rent, salaries, equipment)
3. **Unit volume** (expected units) — the number of units expected to be sold in the period
4. **Target margin %** — the desired profit margin percentage

### Formula

```
Price = (VarCost + FixedCost / Units) x (1 + Margin%)
```

Where:
- VarCost = Variable cost per unit
- FixedCost = Total fixed costs for the period
- Units = Expected unit volume
- Margin% = Target margin as a decimal (e.g., 20% = 0.20)

### Worked Example

| Input | Value |
|-------|-------|
| Variable cost per unit | $12.00 |
| Fixed cost (monthly) | $5,000 |
| Expected units (monthly) | 500 |
| Target margin % | 25% |

Calculation:
- Cost per unit = $12.00 + ($5,000 / 500) = $12.00 + $10.00 = $22.00
- Price = $22.00 x (1 + 0.25) = $22.00 x 1.25 = **$27.50**

### Output Table

Render the result as an ASCII table:

```
+-------------------------+-----------+
| Field                   | Value     |
+-------------------------+-----------+
| Variable Cost / Unit    | $12.00    |
| Fixed Cost (period)     | $5,000    |
| Expected Units          | 500       |
| Cost Per Unit           | $22.00    |
| Target Margin           | 25%       |
| Calculated Price        | $27.50    |
+-------------------------+-----------+
```

### Edge Cases

- **Zero cost warning**: If variable cost is zero (0), display a caution note asking the user to confirm that the product truly has no variable cost component.
- **Negative price prevention**: If the calculated price result is negative, block the file write and display an error asking the user to review inputs — negative prices indicate a data entry issue.
- **Implausible margin confirmation**: If the target margin exceeds 500%, prompt the user to confirm the margin is intentional before proceeding.

---

## Strategy 2: Value-Based Pricing

### Perceived Value Indicators

Collect the following perceived value inputs:

1. **Key benefits** — list the top 3-5 benefits your product provides to the customer
2. **Differentiation factors** — what makes your product unique compared to alternatives

These inputs establish the perceived value your product delivers.

### Willingness-to-Pay (WTP) Anchors

Collect the following WTP anchoring inputs:

1. **Comparable alternatives** — list similar products or substitutes and their prices
2. **Budget range** — the customer segment's typical budget range for this category

These anchors help frame the willingness-to-pay ceiling and floor.

### Floor Price

Collect the **floor price** — the minimum price below which the business cannot sustain operations (typically cost-based).

### Price Range Generation

Using the collected inputs, generate a recommended **price range** with:

- **Floor**: The floor price (cost-based minimum)
- **Ceiling**: Derived from WTP anchors and perceived value strength
- **Recommended**: A specific point within the range

Include a **rationale** explaining why the range was selected based on the differentiation strength, comparable alternative pricing, and budget range alignment.

---

## Strategy 3: Competitive Pricing

### Data Source: EPIC-074 Market Research

This strategy integrates with EPIC-074 market research data. Attempt to read competitor data from:

```
devforgeai/specs/business/market-research/competitive-landscape.md
```

Extract the following from the file:
- **Competitor names** — each competitor listed in the landscape analysis
- **Competitor pricing** — the price point data for each competitor

### Competitor Comparison Table

Render a **comparison table** showing all competitors and their prices, with **your price** positioned relative to competitors. Sort by price to show whether your proposed pricing is above, below, or between competitor offerings.

Example:

```
| Competitor       | Price   | Position         |
|------------------|---------|------------------|
| Budget Co        | $15.00  |                  |
| Your Price       | $22.00  | <-- Your Price   |
| Premium Inc      | $35.00  |                  |
```

### Graceful Degradation

If the `competitive-landscape.md` file is missing or unavailable, display a message:

> "Market research data unavailable or not found. Falling back to manual entry mode."

If the file exists but is **unparseable or malformed**, the workflow will fallback to manual entry and continue without error:

> "Market research file could not be parsed (malformed content). Falling back to manual entry."

**Manual entry fallback**: When data is unavailable, prompt the user to:
- **Enter competitor names** directly via AskUserQuestion
- **Enter price point** data for each competitor manually

The workflow must **proceed to complete without error** even when the market research file is absent or corrupt. This graceful degradation ensures the pricing workflow always finishes.

---

## Output File

### Output Path

Write the final pricing model to:

```
devforgeai/specs/business/financial/pricing-model.md
```

### Required Output Sections

The output file must contain the following sections:

1. **Strategy name header** — which strategy type was selected (e.g., "# Cost-Plus Pricing Model")
2. **Date** — timestamp of when the model was generated
3. **Inputs summary** — summary of all inputs collected during the workflow
4. **Calculated price** (or recommended price range for value-based) — the final price result
5. **Rationale** — explanation of why this price was chosen
6. **Disclaimer** — Include the BR-001 disclaimer (see Disclaimer section below)

### Atomic Write Behavior

Use an **atomic write** pattern to prevent partial file writes on failure:

1. Build the complete output content in memory
2. Write the entire file in a single Write() operation
3. If an existing file is present, the Write() operation will overwrite the existing file completely
4. No partial or incomplete writes should be left on disk — atomic write ensures all-or-nothing

---

## Disclaimer (BR-001)

All pricing strategy outputs — whether cost-plus, value-based, or competitive — must include the following disclaimer:

> **This is not financial advice.** The pricing models generated by this tool are for informational and planning purposes only. Consult a qualified financial professional before making pricing or financial decisions.
