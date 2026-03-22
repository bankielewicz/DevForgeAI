# STORY-552: Funding Options Guide — Documentation

**Story:** STORY-552
**Epic:** EPIC-077 (Managing Finances)
**Status:** Released
**Implementation:** `src/claude/skills/managing-finances/references/funding-options-guide.md` (226 lines)
**Tests:** 58 tests (40 unit + 18 integration), all passing
**QA Result:** PASSED
**Generated:** 2026-03-21

---

## 1. Architecture

### Component Placement

The funding options guide is a **reference file** within the managing-finances skill. It follows the DevForgeAI skill reference pattern where the main `SKILL.md` orchestrates workflow phases and loads reference files on demand for detailed domain content.

```
src/claude/skills/managing-finances/
    SKILL.md                              # Financial planning orchestrator
    references/
        pricing-strategy-framework.md     # STORY-549
        break-even-analysis.md            # STORY-550
        funding-options-guide.md          # STORY-552 (this component)
```

### Decision Tree Design

The decision tree is a **content-driven** design (not executable code). It is implemented entirely in Markdown, with the decision logic encoded as structured prose and tables. The system relies on the LLM (Claude) to interpret the decision tree content, evaluate user inputs against the documented criteria, and produce the ranked output.

```
User Inputs (3 dimensions)
    │
    ├── Business Stage
    ├── Capital Need
    └── Equity Preference
    │
    ▼
Evaluate Against 5 Funding Types
    │
    ├── Bootstrapping (non-equity)
    ├── Grants (non-equity)
    ├── Angel Investment (equity → referral trigger)
    ├── Venture Capital (equity → referral trigger)
    └── Debt/Loans (non-equity)
    │
    ▼
Output: Ranked Shortlist OR Comparison Table
    │
    ▼
Written to: funding-strategy.md (dual disclaimer)
```

### Non-Functional Constraints

| NFR ID | Category | Constraint |
|--------|----------|------------|
| NFR-P001 | Performance | Decision tree traversal < 3 seconds |
| NFR-S001 | Security | Output file < 150KB |
| NFR-S002 | Security | No PII in output |
| NFR-S003 | Compliance | Dual disclaimer (first and last section) |

### Safety Boundary

Equity funding paths (Angel Investment, Venture Capital) include a **professional referral trigger** directing users to consult a financial advisor or attorney. Non-equity paths (Bootstrapping, Grants) remain within educational scope and omit the referral trigger (BR-002).

---

## 2. Developer Guide

### File Locations

| File | Purpose |
|------|---------|
| `src/claude/skills/managing-finances/SKILL.md` | Parent skill orchestrator |
| `src/claude/skills/managing-finances/references/funding-options-guide.md` | Funding decision tree reference (226 lines) |
| `devforgeai/specs/business/financial/funding-strategy.md` | Output artifact (generated at runtime) |
| `tests/STORY-552/` | Test suite (7 files, 58 tests) |

### How to Use the Funding Options Workflow

1. The managing-finances skill is invoked via the DevForgeAI CLI
2. When the user selects the funding options workflow, the skill loads `references/funding-options-guide.md`
3. The LLM prompts the user for three inputs:
   - **Business Stage**: idea, pre-revenue, revenue-generating, or scaling
   - **Capital Need**: amount range and timeframe
   - **Equity Preference**: willingness to give up ownership
4. The LLM evaluates the inputs against the decision tree criteria
5. A ranked shortlist is produced with rationale for each recommendation
6. The output is written to `devforgeai/specs/business/financial/funding-strategy.md`

### How to Extend with New Funding Types

**Technical Limitation TL-001** documents that the decision tree covers 5 funding types only. To add a new type:

1. Edit `src/claude/skills/managing-finances/references/funding-options-guide.md`
2. Add a new `## [Funding Type Name]` section following the existing pattern
3. For **equity-based** types: Include Dilution, Governance, Timeline, and Professional Referral subsections (per BR-001)
4. For **non-equity** types: Include Benefits/Drawbacks without Professional Referral (per BR-002)
5. Update the comparison table in "Boundary and Ambiguous Results" section
6. Add tests to verify the new type is present and follows the correct pattern

### Running Tests

```bash
# Run all STORY-552 tests (use -s flag on WSL)
pytest tests/STORY-552/ -v -s

# Run a specific AC's tests
pytest tests/STORY-552/test_ac1_decision_tree_ranked_shortlist.py -v -s

# Run integration tests only
pytest tests/STORY-552/test_integration_skill_guide_consistency.py -v -s
```

### Test File Inventory

| File | Tests | Coverage |
|------|-------|----------|
| `conftest.py` | 0 (fixtures) | Shared: `guide_content`, `guide_sections` |
| `test_ac1_decision_tree_ranked_shortlist.py` | 8 | Input dimensions, ranked shortlist, dual disclaimer |
| `test_ac2_equity_funding_path.py` | 8 | Dilution, control, timeline, referral for VC and Angel |
| `test_ac3_bootstrapping_grants_path.py` | 7 | Pros/cons, grant eligibility, no referral trigger |
| `test_ac4_output_artifact.py` | 9 | File path, Markdown validity, 5 types, disclaimer, source ref |
| `test_ac5_boundary_ambiguous_results.py` | 8 | Conflicting inputs, comparison table, suitability ratings |
| `test_integration_skill_guide_consistency.py` | 18 | Cross-file consistency, reachability, path consistency |
| **Total** | **58** | |

---

## 3. CLI Reference

### Decision Tree Inputs

| Parameter | Type | Required | Valid Values |
|-----------|------|----------|--------------|
| `business_stage` | Enum | Yes | `idea`, `pre-revenue`, `revenue-generating`, `scaling` |
| `capital_need` | Enum | Yes | `low` ($0-100K), `medium` ($25K-500K), `high` ($1M+) |
| `equity_preference` | Enum | Yes | `retain-full`, `willing-some`, `open-significant` |

### Output Format

**File Path:** `devforgeai/specs/business/financial/funding-strategy.md`

| Section | Content | Required |
|---------|---------|----------|
| Disclaimer (top) | Educational-only disclaimer | Always |
| Ranked Shortlist | 1-5 funding types ranked with rationale | Always |
| Comparison Table | All types with suitability ratings | Boundary cases only |
| Explanation | Plain-language ambiguity explanation | Boundary cases only |
| Disclaimer (bottom) | Same disclaimer text | Always |
| Source Reference | Cites funding-options-guide.md | Always |

### Equity vs Non-Equity Path Content

**Equity Paths (Angel, VC):** Dilution explanation, board/control implications, funding timeline, professional referral trigger

**Non-Equity Paths (Bootstrapping, Grants, Debt/Loans):** Benefits, drawbacks, eligibility criteria. No professional referral trigger.

---

## 4. Troubleshooting

### Common Issues

| Issue | Cause | Resolution |
|-------|-------|------------|
| Comparison table instead of ranked shortlist | Contradictory inputs | Adjust one input dimension to break tie |
| Referral trigger in non-equity output | BR-002 violation (regression) | Verify reference file content |
| Missing disclaimer | NFR-S003 regression | Check first and last `## Disclaimer` sections in reference file |
| FileNotFoundError in tests | Guide file moved/deleted | Verify file at expected path, run from project root |
| Missing funding type | Reference file section missing | Verify all 5 `##` funding type sections exist |

### Boundary Cases

| Scenario | Input Combination | Expected Output |
|----------|-------------------|-----------------|
| High capital + no equity | high capital, retain-full | Comparison table |
| Pre-idea stage | pre-idea business stage | Comparison table |
| Unknown grant eligibility | Unclear sector/geography | Grants branch notes uncertainty |
| No credit or collateral | Debt path, no qualifying signals | Debt branch notes limitations |

### FAQ

**Q: Can I add a 6th funding type?**
A: Yes, by editing `funding-options-guide.md`. See Developer Guide "How to Extend" section. TL-001 documents the current 5-type limitation.

**Q: Why do equity paths include referral triggers?**
A: Equity transactions involve dilution, governance, and legal complexity exceeding educational scope (BR-001). Non-equity paths remain within educational guidance (BR-002).

**Q: Is PII stored in output?**
A: No. NFR-S002 prohibits PII. Inputs are categorical buckets, not personal data.

---

## 5. Roadmap

### Known Limitation: TL-001

Only 5 funding types supported. Types not modelled: crowdfunding, revenue-based financing (standalone), convertible notes, SAFE agreements, corporate VC.

### Potential Future Work

| Item | Description |
|------|-------------|
| Crowdfunding branch | Add reward-based and equity-based crowdfunding |
| SAFE/Convertible Notes | Add pre-seed instruments as distinct category |
| Revenue-Based Financing | Separate from Debt/Loans umbrella |
| Government programs | Region-specific loan/grant programs |
| Input dimension expansion | Add 4th dimension (e.g., industry sector) |

All extensions must comply with BR-001 (equity referral), BR-002 (non-equity no referral), BR-003 (comparison table), NFR-S003 (dual disclaimer), NFR-S002 (no PII), NFR-S001 (< 150KB).

---

## Documentation Coverage

| Type | Status | Key Sections |
|------|--------|-------------|
| Architecture | Complete | Component placement, decision tree design, NFRs, safety boundary |
| Developer Guide | Complete | File locations, workflow, extension guide, test inventory |
| CLI Reference | Complete | Inputs, output format, equity vs non-equity paths |
| Troubleshooting | Complete | 5 issues, 4 boundary cases, 3 FAQ entries |
| Roadmap | Complete | TL-001, 5 future items, extension constraints |
