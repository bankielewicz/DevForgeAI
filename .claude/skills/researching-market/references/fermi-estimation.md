# Fermi Estimation Guide for Market Sizing

Fermi estimation is a method for making approximate calculations with limited data by breaking complex questions into smaller, estimable components.

---

## When to Use Fermi Estimation

- **Primary use:** When internet-sleuth returns no data or fails (fallback path)
- **Secondary use:** Validating top-down or bottom-up estimates
- **Always use for:** SOM estimates where competitive capture rates are unknown

When Fermi estimation is the sole methodology for a tier, confidence should be marked as **Low** unless validated against independent data.

---

## The Fermi Process

### Step 1: Define the Question Precisely

State exactly what you are estimating. Avoid vague questions.

- Bad: "How big is the market?"
- Good: "What is the annual revenue of B2B SaaS project management tools in North America?"

### Step 2: Decompose into Estimable Components

Break the question into 3-5 sub-questions where each can be independently estimated:

```
Market Size = Component A x Component B x Component C

Example:
Annual revenue = (Number of target businesses)
               x (Adoption rate)
               x (Average annual spend per business)
```

### Step 3: Estimate Each Component

For each component, use one of these estimation strategies:

1. **Known anchor:** Start from a fact you know (e.g., US population = 330M)
2. **Order of magnitude:** Is it thousands, millions, or billions?
3. **Bounded range:** Estimate low and high bounds, then use geometric mean
4. **Proxy reasoning:** Use a related known quantity as a proxy

### Step 4: Combine and Validate

Multiply components together. Then validate:

- Does the result pass a sanity check?
- Is it within an order of magnitude of any known benchmarks?
- Would a different decomposition give a similar answer?

### Step 5: Document Assumptions

Every Fermi estimate must document:

- Each component and its estimated value
- The reasoning or source behind each estimate
- The confidence level of each component
- Any known limitations or biases

---

## Example: Estimating Market Size for Online Tutoring in the US

**Question:** What is the annual TAM for online K-12 tutoring in the US?

**Decomposition:**
```
TAM = (K-12 students in US)
    x (% who use tutoring)
    x (Average annual spend on tutoring)
```

**Component Estimates:**
1. K-12 students in US: ~56 million (known from NCES data)
2. % who use tutoring: ~20% (estimate based on education surveys)
3. Average annual spend: ~$2,000 (estimate based on tutoring platform pricing)

**Calculation:**
```
TAM = 56M x 0.20 x $2,000 = $22.4 billion
```

**Validation:** Published estimates for US tutoring market range $12-30B, so $22.4B is reasonable.

**Confidence:** Medium (one anchored data point, two estimates)

---

## Common Pitfalls

1. **Anchoring bias:** Do not let the first number you find dominate your thinking
2. **Precision illusion:** Fermi estimates are order-of-magnitude; do not report false precision (say "$20-25B" not "$22.4B")
3. **Missing components:** Ensure your decomposition covers the full scope
4. **Double counting:** When combining segments, verify no overlap
5. **Static assumptions:** Markets grow; note the year of your estimate

---

## Confidence Calibration

| Scenario | Confidence Level |
|----------|-----------------|
| All components have external data sources | Medium-High |
| Most components are reasonable estimates | Medium |
| Multiple components are rough guesses | Low |
| Pure speculation with no anchors | Very Low (flag for user review) |

Fermi estimates used as the sole methodology should generally be marked **Low confidence** unless corroborated by at least one independent data point.
