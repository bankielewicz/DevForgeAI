# ADR-005: Epic Coverage Validation - Native Tools Architecture

**Status:** Accepted
**Date:** 2025-11-25
**Context:** EPIC-015 (Epic Coverage Validation & Requirements Traceability)
**Decision Makers:** DevForgeAI Framework Maintainers
**Related:** RESEARCH-002 (Epic Coverage Traceability Feasibility Analysis)

---

## Context

EPIC-015 requires a system to validate epic coverage by matching epic features to stories and identifying gaps. Initial research (RESEARCH-002) recommended external Python libraries (RapidFuzz, PyYAML, mistune) for fuzzy matching and parsing. However, analysis of DevForgeAI's existing 13 epics and 63 stories revealed:

**Evidence-Based Findings:**
- **95% of stories** (60/63) have `epic:` field in YAML frontmatter
- **89% of stories** (56/63) have valid `epic: EPIC-XXX` values
- **38% of epics** (5/13) have `## Stories` tables with bidirectional mapping
- **Field name:** `epic:` (not `epic_id:` as initially assumed)

This evidence showed that **exact `epic:` field matching** would cover 95% of stories without needing fuzzy matching algorithms.

---

## Decision

**We will use Claude Code native tools (Grep, Read, Write, Bash) instead of external Python libraries for epic coverage validation.**

**Architecture:**
- **Language:** Bash scripting
- **Parsing:** Grep patterns for YAML frontmatter and markdown headers
- **Matching:** Exact `epic:` field matching via `grep "^epic: EPIC-XXX"`
- **Data Model:** JSON files or Bash associative arrays
- **Reporting:** Write tool for JSON/markdown generation
- **CLI:** Slash command in `.claude/commands/validate-epic-coverage.md`

**No external dependencies** - uses only tools available in Claude Code Terminal.

---

## Rationale

### Why Native Tools Over External Libraries

| Factor | Native Tools (Grep/Bash) | External Libraries (RapidFuzz/PyYAML) |
|--------|--------------------------|---------------------------------------|
| **Coverage** | 95% (exact `epic:` matching) | 100% (fuzzy + exact matching) |
| **Dependencies** | Zero | 3 libraries (RapidFuzz, PyYAML, mistune) |
| **Installation** | None (tools pre-installed) | `pip install` required |
| **Maintenance** | Claude Code guarantees | Library version management, breaking changes |
| **Evidence** | Verified via Grep on 63 stories | Projected performance (unmeasured) |
| **Complexity** | Simple Bash script (~200 lines) | Python module (~500 lines) |
| **Performance** | TBD (benchmarked during impl) | "3.2 seconds for 100 epics" (projection) |

### Key Evidence Supporting Native Tools

1. **`epic:` Field Prevalence (95%):**
   ```bash
   grep -c "^epic:" devforgeai/specs/Stories/STORY-*.story.md | grep ":1" | wc -l
   # Result: 60 out of 63 stories
   ```

2. **Valid Epic References (89%):**
   ```bash
   grep -h "^epic:" devforgeai/specs/Stories/STORY-*.story.md | sort | uniq -c
   # Result: 56 have EPIC-XXX, 4 have None/null/TBD
   ```

3. **Bidirectional Mapping (38%):**
   ```bash
   grep -c "## Stories" devforgeai/specs/Epics/EPIC-*.epic.md | grep ":1" | wc -l
   # Result: 5 out of 13 epics have Stories tables
   ```

### Trade-Offs Accepted

**What we gain:**
- ✅ Zero external dependencies (no library version conflicts)
- ✅ Evidence-based (95% coverage verified, not projected)
- ✅ Simple implementation (Bash script vs Python module)
- ✅ No installation required (works out of box)
- ✅ Maintainable (no breaking library changes)

**What we sacrifice:**
- ❌ 5% stories without `epic:` field (manual addition required)
- ❌ No fuzzy matching (typos in epic: field won't match)
- ❌ Simple YAML parsing only (complex nested YAML requires manual handling)

**Mitigation for sacrifices:**
- 5% gap: Validation reports missing `epic:` fields for manual addition
- Typos: Git history tracks `epic:` field changes, validation detects mismatches
- Complex YAML: DevForgeAI uses simple YAML (key:value pairs only)

---

## Alternatives Considered

### Alternative 1: Full Library Stack (RESEARCH-002 Recommendation)

**Description:** Python module with RapidFuzz (fuzzy matching), PyYAML (YAML parsing), mistune (markdown parsing)

**Pros:**
- 100% coverage (handles stories without `epic:` field via title matching)
- Robust YAML parsing (handles complex nested structures)
- Typo tolerance (75% similarity threshold catches variations)

**Cons:**
- 3 external dependencies (installation, versioning, breaking changes)
- Performance claims unmeasured ("3.2 seconds for 100 epics" - projection)
- Complexity (500+ lines vs 200 lines for native tools)
- Aspirational (fuzzy matching not needed for 95% exact matches)

**Rejected because:** Evidence showed 95% coverage achievable with native tools, making libraries unnecessary.

---

### Alternative 2: Hybrid Approach (Exact + Fuzzy)

**Description:** Use Grep for `epic:` matching (95%), add RapidFuzz only for the 5% without `epic:` field

**Pros:**
- Best of both worlds (95% simple, 5% fuzzy)
- Single dependency (RapidFuzz only)

**Cons:**
- Still requires external dependency for 5% edge case
- Complexity of two code paths (exact vs fuzzy)
- Fuzzy matching for 5% stories may have false positives

**Rejected because:** 5% edge case doesn't justify dependency overhead; manual addition is acceptable.

---

### Alternative 3: Manual Mapping File

**Description:** User creates `.devforgeai/epic-story-mappings.yaml` manually mapping epics to stories

**Pros:**
- 100% accurate (user explicitly defines mappings)
- Zero libraries, zero algorithms

**Cons:**
- Manual maintenance overhead (defeats automation goal)
- Prone to human error (typos, forgotten updates)
- Duplicate effort (already have `epic:` field in 95% of stories)

**Rejected because:** Goal is automation; manual mapping defeats purpose.

---

## Implementation Details

### Parsing Strategy

**Extract `epic:` field from stories:**
```bash
grep "^epic:" devforgeai/specs/Stories/STORY-*.story.md
# Output: devforgeai/specs/Stories/STORY-066-npm-package-creation-structure.story.md:epic: EPIC-012
```

**Extract `## Stories` table from epics:**
```bash
# Read epic file, grep for table rows after ## Stories header
grep -A 20 "## Stories" devforgeai/specs/Epics/EPIC-012-npm-package-distribution.epic.md
```

**Match epic features to stories:**
```bash
# For each epic feature, find stories with matching epic: field
epic_id="EPIC-012"
grep -l "^epic: $epic_id" devforgeai/specs/Stories/*.story.md
```

### Data Model

**JSON file structure:**
```json
{
  "EPIC-012": {
    "title": "NPM Package Distribution",
    "features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4"],
    "stories": ["STORY-066", "STORY-067", "STORY-068", "STORY-069"],
    "coverage_percent": 100,
    "missing_features": []
  }
}
```

### Reporting

**Terminal output:**
```
Epic Coverage Validation Report
================================

EPIC-012: NPM Package Distribution [100%] ✓
  ✓ Feature 1: NPM Package Creation → STORY-066
  ✓ Feature 2: Registry Publishing → STORY-067
  ✓ Feature 3: Global CLI → STORY-068
  ✓ Feature 4: Offline Install → STORY-069

EPIC-015: Epic Coverage Validation [0%] ✗
  ✗ Feature 0: Traceability Matrix → NO STORIES
  ✗ Feature 1: Metadata Parser → NO STORIES
  ...

Summary: 1/2 epics complete (50%), 4/11 features have stories (36%)
```

---

## Consequences

### Positive

1. **Zero Dependencies:** No `pip install`, no version conflicts, no breaking changes
2. **Evidence-Based:** 95% coverage verified via Grep, not projected
3. **Simple Implementation:** ~200 lines Bash vs ~500 lines Python
4. **Immediate Availability:** Works out of box in Claude Code Terminal
5. **Maintainable:** Grep/Bash patterns stable, no library updates

### Negative

1. **5% Manual Gap:** 3 stories without `epic:` field require manual addition
2. **No Fuzzy Matching:** Typos in `epic:` field won't match (rely on git history)
3. **Simple YAML Only:** Complex nested YAML structures require manual parsing

### Neutral

1. **Performance TBD:** Benchmarking required during implementation (no projections)
2. **Scalability:** Works for current 13 epics, future 100 epics TBD (will measure)

---

## Validation Criteria

**This decision will be considered successful if:**

1. ✅ Gap detection achieves ≥95% accuracy (matches evidence-based coverage)
2. ✅ Zero external dependencies remain (no libraries installed)
3. ✅ Implementation completes in ≤200 lines of Bash
4. ✅ Performance acceptable for 13 epics (<5 seconds) - benchmarked during impl
5. ✅ Reports correctly identify missing stories (validated against manual audit)

**This decision will be reconsidered if:**

1. ❌ Coverage drops below 90% (indicating `epic:` field usage declining)
2. ❌ Performance exceeds 10 seconds for current scale (unacceptable UX)
3. ❌ Complex YAML parsing becomes required (nested structures appear)
4. ❌ Fuzzy matching proves necessary (typos common, manual fixes exceed cost)

---

## Notes

- **Decision Date:** 2025-11-25
- **Decision Maker:** DevForgeAI Framework Maintainers
- **Revisit Date:** After EPIC-015 implementation (Sprint 2 completion)
- **Related Documents:**
  - EPIC-015: `devforgeai/specs/Epics/EPIC-015-epic-coverage-validation-traceability.epic.md`
  - RESEARCH-002: `.devforgeai/research/shared/RESEARCH-002-epic-coverage-traceability.md`
  - Evidence: `grep "^epic:" devforgeai/specs/Stories/STORY-*.story.md` (60/63 = 95%)

---

**Status:** ✅ **ACCEPTED**
**Next Steps:** Update `tech-stack.md` and `source-tree.md`, begin Feature 0 implementation
