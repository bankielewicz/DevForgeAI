# Break-Even Analysis Reference

## Calculation Methodology

### Overview

Break-even analysis determines the minimum sales volume needed to cover all costs. All calculations use Python standard library only (`math.ceil`) -- no third-party imports or external dependencies permitted (BR-003).

### Formulas

Four metrics are computed, each showing the formula alongside its computed value (BR-002):

**1. Break-Even Units**

```
Break-even units = ceil(fixed_costs / (price - variable_cost))
```

**Worked Example** (Fixed costs = $50,000, Price = $100, Variable cost = $60):

```
Break-even units = ceil(50000 / (100 - 60)) = ceil(1250.0) = 1250
```

**2. Break-Even Revenue**

```
Break-even revenue = units * price
```

**Worked Example:**

```
Break-even revenue = 1250 * $100 = $125,000
```

**3. Contribution Margin Per Unit**

The contribution margin = price - variable cost per unit (the amount each unit contributes toward covering fixed costs).

**Worked Example:**

```
Contribution margin = $100 - $60 = $40
```

**4. Contribution Margin Ratio**

The margin ratio = (price - variable cost) / price * 100% (what percentage of each sale contributes to fixed costs).

**Worked Example:**

```
Contribution margin ratio = ($100 - $60) / $100 * 100% = 40.0%
```

---

## Chart Rendering Specification

### ASCII Chart Visual Specification

The chart displays two lines and their intersection within an 80-character width constraint:

- **Revenue line:** rendered with `/` character
- **Cost line:** rendered with `*` character (represents total cost = fixed + variable)
- **Break-even intersection:** marked with a distinct symbol `X` -- this is a different character from either line symbol to make it visually prominent
- **X-axis:** labeled "Units"
- **Y-axis:** labeled "Amount ($)"

All chart output lines must fit within 80 characters width.

### Chart Example

```
Amount ($)
  |
  |                                    /
  |                               /
  |                          / *
  |                     X *
  |                * /
  |           *  /
  |      *  /
  | *  /
  +------------------------------------------
  0         500       1000      1500     Units
```

### Auto-Scaling Behavior

When break-even units exceed the default chart scale range, the chart must auto-scale the axis to accommodate the larger values. A note is added that the scale was adjusted to fit the break-even point. Dynamic scale adjustment ensures the break-even intersection always appears within the visible chart area.

---

## Edge Case Handling

### Edge Case 1: Zero Fixed Costs

When fixed costs are 0 (zero fixed costs), the break-even calculation produces:
- Break-even units = 0 units
- Break-even revenue = $0
- The chart shows lines originating from the origin

### Edge Case 2: Non-Integer Break-Even Units (BR-005)

When the division produces a fractional result, ceiling rounding is applied using `math.ceil`:
- Exact value: 10.3 units (fractional result from division)
- Ceiling rounded: 11 units (always round up to next whole unit)
- Both the exact fractional value and the ceiling function result are displayed in output

### Edge Case 3: Zero Variable Cost

When variable cost is 0 (zero variable cost), the contribution margin equals the full selling price:
- Contribution margin = selling price
- Break-even units = fixed_costs / selling_price

### Edge Case 4: High Break-Even Exceeding Chart Scale

Chart auto-scales axes to accommodate large break-even values (see Auto-Scaling Behavior above).

### Edge Case 5: projections.md Does Not Exist

When `devforgeai/specs/business/financial/projections.md` does not exist, the file is created with the break-even section as the first content. No error is raised for a missing file.

### Edge Case 6: Multiple Analyses in Same Session

Each break-even analysis is appended as a new dated section. Prior sections are preserved and not overwritten. The existing content in projections.md remains intact.

---

## Error Handling

### Input Validation Rules

All validation occurs before any calculation or file output. If validation fails, no output is written to projections.md (halt before write).

**Error: Price Equals Variable Cost (Zero Contribution Margin)**

When price equals variable cost, a zero contribution margin makes break-even impossible. A clear error message is raised:

"Selling price must exceed variable cost per unit. The contribution margin must be positive for break-even analysis to be meaningful."

**Error: Price Less Than Variable Cost (Negative Margin)**

When price is less than variable cost, the negative contribution margin means every unit sold increases losses. A descriptive error message explains:

"Selling price ($X) is below variable cost ($Y), resulting in a negative margin. Price must exceed variable cost."

**Error: Negative Selling Price**

When a negative selling price is provided, input validation rejects it with a user-friendly error message before any calculation proceeds.

**Error: Negative Fixed Costs**

When negative fixed costs are provided, input validation rejects them. Fixed costs must be zero or positive.

### Error Message Standards

All error messages must be clear and descriptive, explaining:
1. What went wrong (the specific invalid input)
2. Why it is invalid (the business rule violated)
3. What the user should do (provide valid inputs)

Example error message: "Error: Selling price ($50) does not exceed variable cost ($60). The contribution margin must be positive. Please provide a selling price greater than the variable cost per unit."

---

## Output Format for projections.md

### Output Path

All break-even results are written to: `devforgeai/specs/business/financial/projections.md`

If projections.md does not exist, it is created automatically.

### Output Structure

Each analysis is appended (not overwritten) to the file. Previous and existing sections are preserved.

```markdown
## Break-Even Analysis

**Timestamp:** 2026-03-05T14:30:00Z (ISO 8601 format)

### Results Section

| Metric | Formula | Value |
|--------|---------|-------|
| Break-Even Units | ceil(fixed_costs / (price - var_cost)) | 1,250 units |
| Break-Even Revenue | units * price | $125,000 |
| Contribution Margin | price - variable_cost | $40/unit |
| Margin Ratio | (price - var_cost) / price * 100% | 40.0% |

### Chart

(ASCII chart visualization included in projections output)

### Assumptions Section

The assumptions list includes all input values: fixed costs, variable cost per unit, and selling price per unit. The following input values were used:
- Fixed Costs: $50,000
- Variable Cost per Unit: $60
- Selling Price per Unit: $100

### Disclaimer

These results are estimates based on the input values provided and are not professional financial advice. Actual break-even may vary due to market conditions, demand elasticity, and other factors not captured in this simplified model. Consult a qualified financial professional for business-critical decisions.
```

### Append Behavior

When multiple analyses are performed, each new analysis is appended as a new section with its own timestamp. The file is not overwritten -- all prior content is preserved.

---

## Implementation Notes

- **stdlib only:** All calculation uses Python `math.ceil` from the standard library. No third-party library imports are permitted (BR-003).
- **Formula transparency (BR-002):** Every calculation step shows both the formula and the computed value side by side.
- **Ceiling rounding (BR-005):** Non-integer break-even units are always rounded up using the ceiling function.
