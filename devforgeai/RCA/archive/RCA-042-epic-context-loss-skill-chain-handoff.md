# RCA-042: Epic Context Loss During Skill-Chain Handoff

**Date:** 2026-02-27
**Reported By:** User
**Affected Component:** designing-systems skill (Phase 6: Epic Creation) + ideation-to-epic handoff pipeline
**Severity:** HIGH

---

## Issue Description

EPIC-085 (QA Diff Regression Detection) was created by the designing-systems skill but was missing critical conversation context that would be needed by a fresh Claude session running `/create-story`. Specifically, the epic lacked:

1. **Design rationale** — WHY phase-boundary checksums were chosen over git diff for test integrity (the key architectural insight from the user)
2. **User observations** — That Claude "gaming" tests was directly observed behavior, not hypothetical
3. **Adversary model** — Explicitly scoped to Claude carelessness only (not multi-session drift, not human error)
4. **Non-aspirational constraint** — User explicitly required solutions that work within Claude Code Terminal (no aspirational proposals)
5. **Feature 3 mechanism** — Ambiguous whether heuristic patterns analyze git diff or Red-phase snapshot diff
6. **Implementation ordering** — Feature 2 must precede Feature 1 (QA can't verify snapshot that doesn't exist yet)
7. **Operational rule status** — FR-005 rules may already exist in CLAUDE.md (duplication risk)
8. **Stale cross-references** — Requirements doc still said "ADR-NNN" and "EPIC-NNN" instead of ADR-025 and EPIC-085

**Impact:** A fresh session running `/create-story` would have created ambiguous stories, potentially proposing aspirational solutions (subagent authorization logging), using wrong detection mechanism (git diff for tests), and duplicating existing rules.

**Expected Behavior:** Epic documents should be self-contained specifications that enable a fresh Claude session to create stories without needing the original conversation context.

**Actual Behavior:** Epic was a structural template populated from requirements YAML, missing the decision-making context that shaped those requirements.

---

## 5 Whys Analysis

**Issue:** EPIC-085 was incomplete and contained ambiguity when first created by the designing-systems skill.

1. **Why was the epic incomplete?**
   - The designing-systems skill populated the epic from the requirements document (F4 schema YAML) and the epic template. But conversation-specific context — user observations, design rationale, rejected alternatives, adversary model — exists only in conversation memory, not in the requirements doc.
   - **Evidence:** Requirements doc (`qa-diff-regression-detection-requirements.md`) has FR-001-005 with acceptance criteria but NO fields for design rationale, rejected alternatives, or threat model.

2. **Why wasn't conversation context captured in the requirements doc?**
   - The `/ideate` skill (discovering-requirements) outputs structured YAML per the F4 schema, which defines fields for `functional_requirements`, `non_functional_requirements`, `data_model`, `integrations`. There is NO field for `design_decisions`, `rejected_alternatives`, `conversation_insights`, or `threat_model`.
   - **Evidence:** F4 schema in artifact-generation.md lines 42-80 — no design context fields.

3. **Why doesn't the F4 schema include design decision context?**
   - The `/ideate` → requirements → epic pipeline was designed as a progressive narrowing funnel. Each stage discards context deemed "upstream" — the conversation is treated as disposable scaffolding, not a deliverable. RCA-031 Why #3 confirms: "Epic documents were designed for business-level planning, assuming technical details would be added during story creation in a SINGLE continuous session."
   - **Evidence:** RCA-031, RCA-035 document the same assumption. artifact-generation.md Cross-Session Context Requirements (lines 46-56) lists brainstorm, complexity, decomposition — but NOT "conversation design decisions."

4. **Why does the pipeline assume structured requirements are sufficient?**
   - There is no explicit "context preservation" gate between skills. The handoff is a data transfer (requirements YAML → epic template), not a context transfer. No validation asks: "Does the epic contain everything a fresh session needs?"
   - **Evidence:** Phase 6.6 (Validation & Self-Healing) validates structural sections (12 constitutional sections) but NOT conversation context completeness. No step checks for design rationale or rejected alternatives.

5. **Why is there no context preservation gate?**
   - **ROOT CAUSE:** The DevForgeAI skill-chain handoff protocol treats conversation context as ephemeral and only transfers structured artifacts. **There is no "Decision Context" preservation mechanism** that captures WHY decisions were made, WHAT alternatives were rejected, and WHAT user observations drove the design. The epic template has structural sections but no section for decision context.
   - **Evidence:** This is the **4th occurrence** of this root cause class: RCA-030 (brainstorm cross-session context), RCA-031 (epic missing constitutional sections), RCA-035 (epic technical specification gaps), now RCA-042.

---

## Evidence Collected

### Files Examined

#### 1. `devforgeai/specs/requirements/qa-diff-regression-detection-requirements.md`
- **Finding:** F4 schema has no fields for design rationale, rejected alternatives, adversary model, or implementation constraints
- **Significance:** CRITICAL — Requirements doc is the primary handoff artifact but lacks decision context

#### 2. `.claude/skills/designing-systems/references/artifact-generation.md`
- **Lines:** 26-56 (Section Compliance Checklist, Cross-Session Context Requirements)
- **Finding:** Checklist validates 12 structural sections. Cross-session requirements list brainstorm/complexity/decomposition but NOT "conversation design decisions"
- **Significance:** HIGH — Validation gate exists but doesn't check for decision context

#### 3. `.claude/skills/designing-systems/references/epic-management.md`
- **Lines:** 1-100 (Epic Creation Process)
- **Finding:** Step 1 extracts from requirements doc: business goals, personas, features, metrics, complexity. No step for extracting design decisions or rejected alternatives.
- **Significance:** HIGH — Epic creation workflow has no decision-context extraction step

#### 4. `devforgeai/RCA/RCA-030-brainstorm-output-missing-cross-session-context.md`
- **Finding:** ROOT CAUSE (Why #5): "The skill design lacks a 'cross-session portability' requirement"
- **Significance:** CRITICAL — Same root cause class, 4th occurrence

#### 5. `devforgeai/RCA/RCA-031-ideation-epic-missing-constitutional-sections.md`
- **Finding:** ROOT CAUSE: Simplified inline template used instead of constitutional template; validation only checks YAML frontmatter, not section completeness
- **Significance:** HIGH — Partially fixed (template loading added) but decision context still not addressed

#### 6. `devforgeai/RCA/RCA-035-epic-technical-specification-gaps.md`
- **Finding:** ROOT CAUSE: Epic template intentionally abstract; assumes single continuous session
- **Significance:** HIGH — Same root cause class, confirms systemic pattern

### Context Files Status

All 6 context files exist and are valid. No context file violations in this RCA — the issue is in the skill-chain handoff, not context file enforcement.

---

## Recommendations (Evidence-Based)

### CRITICAL Priority (Implement Immediately)

**REC-1: Add "Decision Context" Section to Epic Template**
**Priority:** CRITICAL

**Problem:** Epic template has 12 structural sections but none for design rationale, rejected alternatives, or user observations. This is the root cause of 4 RCAs.

**Solution:** Add a mandatory 13th section "## Decision Context" to the constitutional epic template.

**File:** `.claude/skills/designing-systems/assets/templates/epic-template.md` (constitutional template)
**Section:** After "Technical Considerations" and before "Dependencies"
**Change:** Add new section:

```markdown
## Decision Context

### Design Rationale
[WHY were the key technical decisions made? What user observations or constraints drove the design?]

### Rejected Alternatives
[WHAT approaches were considered and explicitly rejected? WHY were they rejected?]

### Adversary/Threat Model
[WHO or WHAT is the system defending against? What is NOT in scope for the threat model?]

### Implementation Constraints
[WHAT constraints limit the solution space? (e.g., "must work within Claude Code Terminal", "no external dependencies")]

### Key Insights from Discovery
[WHAT non-obvious insights emerged during brainstorming/ideation that would be lost if not documented?]
```

**Rationale:** This section captures the "why behind the what" — the conversation context that currently exists only in ephemeral session memory. Without it, a fresh session must re-derive design decisions from first principles, often reaching different conclusions.

**Testing:**
1. Create a test epic using the updated template
2. Have a fresh Claude session attempt `/create-story` from the epic
3. Verify the session doesn't ask questions already answered in Decision Context
4. Success: Zero ambiguity questions about design rationale

**Effort:** Low (30 min template edit + validation update)
**Implemented in:** STORY-507

---

**REC-2: Add Decision Context Validation to Epic Section Compliance Checklist**
**Priority:** CRITICAL

**Problem:** artifact-generation.md Section Compliance Checklist validates 12 sections but not Decision Context.

**Solution:** Add 13th row to the checklist table.

**File:** `.claude/skills/designing-systems/references/artifact-generation.md`
**Section:** Section Compliance Checklist table (lines 29-43)
**Change:** Add row:

```markdown
| Decision Context | ✓ | Design rationale, rejected alternatives, constraints, key insights |
```

Also update the count references from "12 constitutional sections" to "13 constitutional sections" throughout.

**Rationale:** Validation gate already exists — just needs the new section added to the checklist. Without this, the template change (REC-1) won't be enforced.

**Testing:**
1. Generate an epic without Decision Context section
2. Verify validation flags it as non-compliant
3. Generate epic WITH Decision Context section
4. Verify validation passes

**Effort:** Low (15 min edit)
**Implemented in:** STORY-508

---

### HIGH Priority (Implement This Sprint)

**REC-3: Add `design_decisions` Field to F4 Requirements Schema**
**Priority:** HIGH

**Problem:** The F4 schema output by `/ideate` has no field for design decisions, rejected alternatives, or conversation insights. This means the requirements doc — the primary handoff artifact — cannot carry decision context.

**Solution:** Add new top-level section to F4 schema:

**File:** `.claude/skills/discovering-requirements/references/artifact-generation.md` (F4 schema definition)
**Change:** Add after `integrations:` section:

```yaml
design_decisions:
  - id: "DD-001"
    decision: "{what was decided}"
    rationale: "{why this approach}"
    alternatives_rejected:
      - name: "{alternative name}"
        reason: "{why rejected}"
    user_observations: "{direct user quotes or observations that drove this decision}"
    constraints: "{implementation constraints that limit solution space}"

threat_model:
  adversary: "{who/what the system defends against}"
  in_scope: ["{threat 1}", "{threat 2}"]
  out_of_scope: ["{explicitly excluded threat}"]
```

**Rationale:** Captures design decisions at the point they're made (/ideate session), not retroactively during epic creation. This is the most natural place since the user is present and answering questions.

**Testing:**
1. Run `/ideate` for a test feature
2. Verify requirements doc contains `design_decisions` section
3. Verify `/create-epic` can extract and populate Decision Context from it

**Effort:** Medium (1-2 hours — schema change + skill update + downstream parsing)
**Implemented in:** STORY-509

---

**REC-4: Add Cross-Reference Auto-Update Step to Epic Creation**
**Priority:** HIGH

**Problem:** Requirements doc contained stale references ("ADR-NNN", "EPIC-NNN") because the epic creation workflow doesn't update the requirements doc with actual IDs after creation.

**Solution:** Add Step 6.7.5 (post-write) to designing-systems Phase 6:

**File:** `.claude/skills/designing-systems/references/artifact-generation.md` (epic artifact generation workflow)
**Section:** After Step 6.1 "Generate Epic Document(s)" verification gate (around line 100), add new step
**Change:** After epic file is written, update the requirements doc:

```markdown
### Step 6.7.5: Update Cross-References

After epic and ADR creation, update the requirements document with actual IDs:

Read(file_path="devforgeai/specs/requirements/{project}-requirements.md")

Replace all placeholder references:
- "EPIC-NNN" → "EPIC-{actual_number}"
- "ADR-NNN" → "ADR-{actual_number}"
- "STORY-NNN" → (leave as-is, stories not yet created)

Write updated file.
```

**Rationale:** Stale cross-references are a symptom of one-way data flow. The epic creation should update its input artifact with the actual IDs it generated.

**Testing:**
1. Create an epic from a requirements doc with "EPIC-NNN" placeholders
2. Verify requirements doc is updated with actual EPIC-XXX number
3. Verify no "NNN" placeholders remain

**Effort:** Low (30 min)
**Implemented in:** STORY-510

---

### MEDIUM Priority (Next Sprint)

**REC-5: Create Context Preservation Validator Subagent Enhancement**
**Priority:** MEDIUM

**Problem:** No automated validation that epic documents are "cross-session complete." The `context-preservation-validator` subagent exists but focuses on brainstorm→epic→story provenance chains, not on decision context completeness.

**Solution:** Extend context-preservation-validator to check for Decision Context section completeness:

**File:** `.claude/agents/context-preservation-validator.md`
**Change:** Add validation rule:

```markdown
### Decision Context Completeness Check

FOR each epic document:
  IF "## Decision Context" section exists:
    Check: "### Design Rationale" is non-empty (not placeholder)
    Check: "### Rejected Alternatives" has at least 1 entry
    Check: "### Implementation Constraints" is non-empty
    IF any empty: WARN "Decision Context section incomplete"
  ELSE:
    WARN "Missing Decision Context section"
```

**Rationale:** Automated enforcement prevents regression. The validator already runs during workflow transitions.

**Testing:**
1. Create epic with empty Decision Context section
2. Run validator — should warn
3. Create epic with populated Decision Context
4. Run validator — should pass

**Effort:** Medium (1 hour)
**Implemented in:** STORY-511

---

### LOW Priority (Backlog)

**REC-6: Create "Epic Completeness Scorecard" for User Review**
**Priority:** LOW

**Problem:** User had to manually audit the epic to discover it was incomplete. No quick way to assess if an epic is "ready for story creation."

**Solution:** After epic creation, display a completeness scorecard:

```
Epic Completeness Scorecard:
✅ Business Goal (present, non-empty)
✅ Success Metrics (4 metrics with targets)
✅ Features (6 features with points)
✅ Dependencies (documented)
⚠️ Decision Context (MISSING — add design rationale)
⚠️ Rejected Alternatives (MISSING — add what was considered)
✅ Data Flow (documented)
Score: 8/10 sections complete
```

**Rationale:** Quick visual feedback helps the user catch gaps before leaving the session.

**Effort:** Low (30 min)
**Implemented in:** STORY-512

---

## Implementation Checklist

- [x] REC-1: Add "Decision Context" section to epic template — See **STORY-507** (Implemented 2026-02-28, QA Approved)
- [ ] REC-2: Update Section Compliance Checklist (12 → 13 sections) — See **STORY-508**
- [ ] REC-3: Add `design_decisions` field to F4 requirements schema — See **STORY-509**
- [x] REC-4: Add cross-reference auto-update step to epic creation — See **STORY-510** (Implemented 2026-02-28)
- [ ] REC-5: Extend context-preservation-validator for decision context — See **STORY-511**
- [x] REC-6: Create epic completeness scorecard display — See **STORY-512** (Dev Complete 2026-02-28)
- [ ] Update EPIC-085 epic (DONE — already rewritten with Decision Context during this session)
- [ ] Update requirements doc cross-references (DONE — ADR-NNN → ADR-025, EPIC-NNN → EPIC-085)
- [x] Create stories from CRITICAL/HIGH recommendations (DONE — STORY-507 through STORY-512)
- [ ] Mark RCA as RESOLVED after implementation

---

## Prevention Strategy

### Short-Term (REC-1, REC-2, REC-4)

- Add Decision Context section to epic template (prevents new epics from missing context)
- Add to validation checklist (enforces the new section)
- Auto-update cross-references (prevents stale IDs)

### Long-Term (REC-3, REC-5)

- Capture design decisions at the source (/ideate F4 schema) so they flow through the pipeline
- Automated validation catches gaps that human review misses

### Monitoring

- After next 3 epics created: Verify Decision Context section is populated
- Track: Number of "ambiguity questions" a fresh session asks when running /create-story from epic
- Target: Zero ambiguity questions about design rationale
- Escalation: If another RCA with this root cause class appears, elevate to CRITICAL and mandate systemic fix

---

## Related RCAs

- **RCA-030:** Brainstorm Output Missing Cross-Session Context (same root cause class — brainstorm level)
- **RCA-031:** Ideation Epic Missing Constitutional Sections (same root cause class — epic structural level)
- **RCA-035:** Epic Technical Specification Gaps (same root cause class — epic technical detail level)
- **RCA-032:** Story Creation Missing Cross-Session Context Validation (downstream consequence of same root cause)

**Pattern:** This is the **4th occurrence** of the "cross-session context loss" root cause class. The pattern is: each skill in the chain (brainstorm → ideate → epic → story) loses context because handoff artifacts carry structure but not decisions.

---

## Resolution Status

**Status:** Open
**Immediate Fix Applied:** EPIC-085 manually rewritten with full Decision Context (this session)
**Systemic Fix:** Pending implementation of REC-1 through REC-6
