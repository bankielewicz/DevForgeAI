# Custody Chain Audit: STORY-544, STORY-546, STORY-547

**Audit Date:** 2026-03-03 (regenerated with --force)
**Scope:** selected — STORY-544, STORY-546, STORY-547
**Stories Validated:** 3
**Epic:** EPIC-076 (Legal & Compliance)

---

## 1. Document Inventory

| Layer | Document | Path |
|-------|----------|------|
| brainstorm | BRAINSTORM-011 | `devforgeai/specs/brainstorms/BRAINSTORM-011-business-skills-framework.brainstorm.md` |
| epic | EPIC-076 | `devforgeai/specs/Epics/EPIC-076-legal-compliance.epic.md` |
| sprint | Sprint-26 | `devforgeai/specs/Sprints/Sprint-26.md` |
| adr | ADR-017 | `devforgeai/specs/adrs/ADR-017-skill-gerund-naming-no-prefix.md` |
| story | STORY-544 | `devforgeai/specs/Stories/STORY-544-business-structure-decision-tree.story.md` |
| story | STORY-545 | `devforgeai/specs/Stories/STORY-545-ip-protection-checklist.story.md` |
| story | STORY-546 | `devforgeai/specs/Stories/STORY-546-legal-check-command-skill-assembly.story.md` |
| story | STORY-547 | `devforgeai/specs/Stories/STORY-547-when-to-hire-professional-framework.story.md` |

---

## 2. Context Validation Results

| Story ID | Status | CRITICAL | HIGH | MEDIUM | LOW |
|----------|--------|----------|------|--------|-----|
| STORY-544 | COMPLIANT | 0 | 0 | 1 | 0 |
| STORY-546 | COMPLIANT | 0 | 0 | 1 | 1 |
| STORY-547 | COMPLIANT | 0 | 0 | 1 | 0 |

**Compliance Rate:** 3/3 (100%)

### Validation Details

**Technology:** All 3 stories use Markdown only — compliant with tech-stack.md (zero external packages for core framework).

**Source tree:** File paths reference valid patterns:
- `src/claude/skills/advising-legal/` — follows `src/claude/skills/` pattern ✅
- `src/claude/commands/legal-check.md` — follows `src/claude/commands/` pattern ✅
- `tests/STORY-XXX/` — follows `tests/` pattern ✅
- `devforgeai/specs/business/legal/` — falls under `devforgeai/specs/business/` which is documented ✅

**Dependencies:** No external dependencies. Compliant.

**Architecture:** Three-layer architecture followed:
- Command → Skill → References (progressive disclosure) ✅
- Single responsibility per component ✅
- No circular dependencies ✅

**Anti-patterns:** No violations detected.

---

## 3. Provenance Map

```
BRAINSTORM-011 (Business Skills Framework)
  └── EPIC-076 (Legal & Compliance)
        ├── STORY-544 (Business Structure Decision Tree) — Feature 1
        ├── STORY-545 (IP Protection Checklist) — Feature 2 [NOT IN SCOPE]
        ├── STORY-546 (/legal-check Command) — Feature 3
        │     ├── depends_on: STORY-544 ✅
        │     └── depends_on: STORY-545 ✅
        └── STORY-547 (When to Hire Professional) — Feature 4 (independent)
```

### Provenance Verification

| Story | Epic Link | Brainstorm Link | Sprint Link | Provenance XML | Status |
|-------|-----------|-----------------|-------------|----------------|--------|
| STORY-544 | ✅ `epic: EPIC-076` | ✅ BRAINSTORM-011 lines 333 | ✅ Sprint-26 | ✅ Well-formed | VALID |
| STORY-546 | ✅ `epic: EPIC-076` | ✅ BRAINSTORM-011 lines 456 | ✅ Sprint-26 | ✅ Well-formed | VALID |
| STORY-547 | ✅ `epic: EPIC-076` | ✅ BRAINSTORM-011 lines 421 | ✅ Sprint-26 | ✅ Well-formed | VALID |

---

## 4. Findings

### F-001 (MEDIUM): `advising-legal` skill not explicitly registered in source-tree.md

- **Type:** context/source_tree_path_missing
- **Severity:** MEDIUM
- **Affected:** STORY-544, STORY-546, STORY-547
- **Summary:** The `src/claude/skills/advising-legal/` path is not explicitly listed in source-tree.md. While the generic `src/claude/skills/` directory pattern exists, new skills should be registered for discoverability. All 3 stories reference this skill path.
- **Remediation:** Add `advising-legal/` under the skills section in source-tree.md (requires ADR for immutable context file change, or bundle with next source-tree update).
- **Verification:** `Grep(pattern="advising-legal", path="devforgeai/specs/context/source-tree.md")` returns match.

---

### F-002 (MEDIUM): Professional referral trigger overlap between STORY-544 and STORY-547

- **Type:** coherence/scope_overlap
- **Severity:** MEDIUM
- **Affected:** STORY-544, STORY-547
- **Summary:** STORY-544 AC#3 defines 5 professional referral triggers for business structure (multi-state, international, 2+ partners, S-Corp election, C-Corp equity). STORY-547 AC#1 defines 6 complexity indicators for general legal (multi-party contracts, regulatory filings, litigation risk, IP protection, equity structures, employment disputes). "Equity" appears in both lists. While the contexts differ (business structure vs general legal), implementation should clarify which reference file is authoritative per context.
- **Remediation:** Add cross-reference note in each story's technical spec. During implementation, ensure business-structure-guide.md handles entity-selection equity triggers and when-to-hire-professional.md handles general equity complexity triggers without duplication.
- **Verification:** Both reference files address equity without contradicting each other.

---

### F-003 (MEDIUM): `devforgeai/specs/business/legal/` not explicitly in source-tree.md

- **Type:** context/source_tree_subdirectory_missing
- **Severity:** MEDIUM
- **Affected:** STORY-544 (AC#4)
- **Summary:** STORY-544 writes output to `devforgeai/specs/business/legal/business-structure.md`. Source-tree.md documents `devforgeai/specs/business/` generically (line 876 reference) but does not explicitly list the `legal/` subdirectory. The parent path exists, so this is a documentation gap rather than a violation.
- **Remediation:** Add `legal/` subdirectory under `devforgeai/specs/business/` in source-tree.md during next update.
- **Verification:** `Grep(pattern="business/legal", path="devforgeai/specs/context/source-tree.md")` returns match.

---

### F-004 (LOW): STORY-546 dependency status labels stale

- **Type:** chain/stale_dependency_status
- **Severity:** LOW
- **Affected:** STORY-546
- **Summary:** STORY-546 Dependencies section (line 314) shows STORY-544 status as "Ready for Dev" and STORY-545 as "Backlog". STORY-545 is listed as "Ready for Dev" in Sprint-26. Minor label staleness.
- **Remediation:** Update STORY-546 dependency status for STORY-545 from "Backlog" to "Ready for Dev".
- **Verification:** Dependency status labels match actual story frontmatter.

---

### F-005 (LOW): Epic placeholder story IDs in Target Sprints section

- **Type:** documentation/stale_labels
- **Severity:** LOW
- **Affected:** EPIC-076
- **Summary:** EPIC-076 Target Sprints section (lines 82-86) uses placeholder IDs "STORY-A, STORY-B, STORY-C, STORY-D, STORY-E" instead of actual IDs (STORY-544 through STORY-547). These were not updated after story creation.
- **Remediation:** Replace placeholder IDs with actual story IDs.
- **Verification:** `Grep(pattern="STORY-A", path="devforgeai/specs/Epics/EPIC-076-legal-compliance.epic.md")` returns no matches.

---

### F-006 (LOW): STORY-547 dependency mismatch with epic chain

- **Type:** chain/dependency_mismatch
- **Severity:** LOW
- **Affected:** STORY-547
- **Summary:** EPIC-076 Feature Dependency Chain shows Feature 4 as "Independent" which matches STORY-547's `depends_on: []`. However, STORY-547's reference file (`when-to-hire-professional.md`) will be loaded by the `advising-legal` skill (STORY-546). This is an integration relationship, not a build dependency, so `depends_on: []` is technically correct.
- **Remediation:** No action needed. The epic correctly marks Feature 4 as independent. The integration point is handled by STORY-546's assembly.
- **Verification:** N/A — informational only.

---

## 5. Cross-Cutting Issues

1. **Source-tree registration gap:** Both `advising-legal/` skill path and `business/legal/` output path lack explicit source-tree.md entries. A single source-tree.md update (via ADR) can address F-001 and F-003 together.
2. **Previous audit fixes partially applied:** The prior audit (Section 9) claimed all 7 findings resolved. Re-validation shows F-001 (advising-legal) and F-003 (business/legal/) were NOT actually applied to source-tree.md. The duplicate STORY-545 issue (prior F-003) WAS resolved — only one STORY-545 file exists now.

---

## 6. Summary Statistics

| Metric | Count |
|--------|-------|
| Stories validated | 3 |
| Stories compliant | 3 |
| Stories failed | 0 |
| Total findings | 6 |
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 3 |
| LOW | 3 |

---

## 7. Remediation Priority Order

1. **F-001** (MEDIUM) - Register `advising-legal` skill in source-tree.md
2. **F-003** (MEDIUM) - Register `business/legal/` subdirectory in source-tree.md
3. **F-002** (MEDIUM) - Clarify equity trigger scope overlap between STORY-544 and STORY-547
4. **F-004** (LOW) - Update STORY-546 dependency status for STORY-545
5. **F-005** (LOW) - Replace epic placeholder story IDs
6. **F-006** (LOW) - Informational — no action needed

---

## 8. Session Handoff Instructions

**For future Claude sessions reading this document:**

1. This document is self-contained. You do not need the original conversation.
2. Check current state before remediating — prior sessions may have fixed some items.
3. Use the verification step in each finding to confirm fixes were applied.
4. File paths are relative to project root.
5. For CRITICAL findings: these block story implementation. Prioritize them.
6. For quick fixes (path corrections, label updates): batch these in one session.
7. For architectural decisions: use AskUserQuestion to confirm approach before changing.
8. F-001 and F-003 require source-tree.md update — this is an IMMUTABLE context file requiring ADR approval.
