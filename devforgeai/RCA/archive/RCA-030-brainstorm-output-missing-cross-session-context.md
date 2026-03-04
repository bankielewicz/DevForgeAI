# RCA-030: Brainstorm Output Missing Cross-Session Context

**Date:** 2026-01-26
**Reporter:** User
**Component:** devforgeai-brainstorming skill
**Severity:** MEDIUM
**Status:** Open

---

## Issue Description

Brainstorm document BRAINSTORM-007 was created without sufficient context for another Claude session running `/ideate` to understand. The document contained:

- Framework-specific terminology without definitions (e.g., "Phase 09", "exit gates", "subagent contracts", "two-hat problem")
- Incomplete file paths (e.g., `hooks.yaml` instead of `devforgeai/config/hooks.yaml`)
- References to DevForgeAI components without explanation

**Impact:** Required user intervention to add a "Key Files for Context" section and "Glossary" section with 7 term definitions before the document was usable by another Claude session.

**Expected Behavior:** Brainstorm outputs should be self-contained and consumable by a fresh Claude session without prior context.

**Actual Behavior:** Document assumed reader had session context and knowledge of DevForgeAI framework terminology.

---

## 5 Whys Analysis

| Level | Question | Answer |
|-------|----------|--------|
| **Why 1** | Why was the brainstorm document missing cross-session context? | The document contained project-specific terminology and incomplete file paths without definitions |
| **Why 2** | Why didn't the skill generate these sections automatically? | The brainstorm document template has NO "Key Files for Context" section or "Glossary" section defined |
| **Why 3** | Why doesn't the template include cross-session context sections? | The template was designed for business domain brainstorms, not technical framework brainstorms where DevForgeAI-specific terms need definition |
| **Why 4** | Why wasn't the technical brainstorm case considered when designing the template? | The skill was designed assuming brainstorms would feed into `/ideate` which runs in the same session with shared context |
| **Why 5** | **ROOT CAUSE:** Why does the skill assume same-session continuation? | **The skill design lacks a "cross-session portability" requirement.** There is no explicit instruction to make outputs self-contained for consumption by a fresh Claude session. |

---

## Evidence Collected

### Files Examined

#### 1. `.claude/skills/devforgeai-brainstorming/SKILL.md`

**Lines:** All (770 lines)
**Finding:** No cross-session portability validation in Phase 7 (Handoff Synthesis)

**Excerpt (lines 559-596):**
```markdown
3. **Create brainstorm document:**
   ```
   Write(
     file_path="devforgeai/specs/brainstorms/${brainstorm_id}-${short_name}.brainstorm.md",
     content=BRAINSTORM_TEMPLATE with all values
   )
   ```
```

**Significance:** CRITICAL - No validation that output is self-contained for cross-session use

---

#### 2. `.claude/skills/devforgeai-brainstorming/references/output-templates.md`

**Lines:** All (670 lines)
**Finding:** Template structure lacks glossary and context file reference sections

**Excerpt (lines 24-69):** YAML frontmatter template shows fields for problem_statement, stakeholders, constraints - but NO field for "key_files_for_context" or "glossary"

**Significance:** HIGH - Template defines what outputs contain; missing sections mean missing context

---

#### 3. `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md`

**Lines:** All (589 lines)
**Finding:** Step 7.9 "Validate with User" only checks accuracy, not cross-session readability

**Excerpt (lines 419-444):**
```markdown
AskUserQuestion:
  questions:
    - question: "Does this summary accurately capture what we discussed?"
      header: "Validation"
      options:
        - label: "Yes, looks accurate"
        - label: "Needs minor corrections"
        - label: "Missing something important"
```

**Significance:** HIGH - Validation doesn't check "Would another Claude understand this?"

---

### Context Files Status

| File | Status | Relevance |
|------|--------|-----------|
| tech-stack.md | N/A | Not directly relevant |
| source-tree.md | N/A | Not directly relevant |
| dependencies.md | N/A | Not directly relevant |
| coding-standards.md | N/A | Not directly relevant |
| architecture-constraints.md | N/A | Not directly relevant |
| anti-patterns.md | N/A | Not directly relevant |

---

## Recommendations

### HIGH Priority

#### REC-1: Add Cross-Session Portability Validation to Phase 7

**Implemented in:** STORY-320

**Problem Addressed:** Brainstorm outputs may contain undefined terms and missing context

**Proposed Solution:** Add validation step to Phase 7 that checks for cross-session readability

**File:** `.claude/skills/devforgeai-brainstorming/SKILL.md`
**Section:** Phase 7: Handoff Synthesis, after Step 3 "Create brainstorm document"

**Implementation (insert after line 596):**

```markdown
4. **Validate cross-session portability:**
   ```
   # Check for undefined framework terms
   FRAMEWORK_TERMS = ["Phase", "exit gate", "subagent", "context file",
                      "quality gate", "workflow state", "TDD", "DoD"]

   FOR each term in FRAMEWORK_TERMS:
     IF term appears in document AND term not in glossary_section:
       Add to missing_definitions[]

   # Check for incomplete file paths
   IF document references files without full paths:
     Add to missing_paths[]

   # If issues found, add context sections
   IF missing_definitions.length > 0 OR missing_paths.length > 0:
     Generate "Key Files for Context" section
     Generate "Glossary" section with term definitions
     Prepend to document body (after frontmatter)
   ```
```

**Rationale:** This ensures every brainstorm document is consumable by a fresh Claude session running /ideate.

**Testing:**
1. Create a technical brainstorm about DevForgeAI internals
2. Open a new Claude session (fresh context)
3. Run `/ideate` on the brainstorm
4. Verify: No questions about undefined terms or missing file paths

**Effort:** Medium (1-2 hours)

---

#### REC-2: Add Glossary Section to Output Template

**Implemented in:** STORY-321

**Problem Addressed:** Template has no placeholder for term definitions

**File:** `.claude/skills/devforgeai-brainstorming/references/output-templates.md`
**Section:** After YAML frontmatter, before Executive Summary (line 71)

**Implementation:**

```markdown
## Key Files for Context (Optional)

{If brainstorm references framework-specific files:}

| Component | File Path | Purpose |
|-----------|-----------|---------|
| {Component 1} | `{path}` | {What it does} |
| {Component 2} | `{path}` | {What it does} |

---

## Glossary (Optional)

{If brainstorm uses framework-specific terminology:}

| Term | Definition |
|------|------------|
| {Term 1} | {Definition} |
| {Term 2} | {Definition} |

---
```

**Rationale:** Makes the template structure explicit so Claude knows these sections should be generated when needed.

**Testing:**
1. Run `/brainstorm` on a technical DevForgeAI topic
2. Check output document has glossary section populated
3. Verify definitions are accurate

**Effort:** Low (30 minutes)

---

### MEDIUM Priority

#### REC-3: Add "Cross-Session Readability" to Validation Questions

**Implemented in:** STORY-322

**Problem Addressed:** User validation doesn't check portability

**File:** `.claude/skills/devforgeai-brainstorming/references/handoff-synthesis-workflow.md`
**Section:** Step 7.9 "Validate with User" (line 433)

**Implementation (add to options array):**

```markdown
        - label: "Needs context for other sessions"
          description: "Another Claude session wouldn't understand all terms"
```

**Rationale:** Gives user explicit opportunity to flag portability issues before finalizing.

**Effort:** Low (15 minutes)

---

### LOW Priority

#### REC-4: Document Cross-Session Portability Principle

**Implemented in:** STORY-323

**Problem Addressed:** No explicit documentation of portability requirement

**File:** `.claude/skills/devforgeai-brainstorming/SKILL.md`
**Section:** After "Prerequisites" section (line 29)

**Implementation:**

```markdown
## Output Portability Principle

**All brainstorm outputs must be self-contained for cross-session consumption.**

This means:
- Framework-specific terms must be defined in a Glossary section
- File references must include full paths from project root
- Another Claude session running `/ideate` should not need prior context to understand the document

This is especially important for:
- Technical brainstorms about DevForgeAI internals
- Brainstorms referencing specific framework components
- Documents intended for review in separate sessions
```

**Rationale:** Makes the implicit requirement explicit for future skill maintenance.

**Effort:** Low (15 minutes)

---

## Implementation Checklist

- [ ] **REC-1:** Add cross-session portability validation to SKILL.md Phase 7 → **STORY-320**
- [ ] **REC-2:** Add Glossary section to output-templates.md → **STORY-321**
- [ ] **REC-3:** Add validation option to handoff-synthesis-workflow.md → **STORY-322**
- [ ] **REC-4:** Document portability principle in SKILL.md → **STORY-323**
- [ ] Test with technical DevForgeAI brainstorm
- [ ] Verify output is consumable by fresh Claude session
- [ ] Update this RCA status to RESOLVED
- [ ] Commit changes

---

## Prevention Strategy

### Short-term

1. Implement REC-1 (portability validation) to catch missing context automatically
2. Implement REC-2 (template sections) to provide structure for context

### Long-term

1. Apply same portability principle to other skills that produce documents (devforgeai-ideation, devforgeai-story-creation)
2. Consider framework-wide "document portability validator" subagent
3. Add portability check to QA validation for documentation artifacts

### Monitoring

- **Watch for:** User complaints about documents missing context
- **Audit frequency:** Each new brainstorm on technical topics
- **Escalation:** If portability issues recur, escalate to architectural review

---

## Related RCAs

- **RCA-029:** Brainstorm Skill Bypass Plan Mode - Related to brainstorm skill behavior
- None directly related to output portability

---

## Appendix: BRAINSTORM-007 Sections Added

The following sections were manually added to BRAINSTORM-007 to fix the portability issue:

### Key Files for Context (9 entries)

| Component | File Path | Purpose |
|-----------|-----------|---------|
| 10-Phase Workflow | `.claude/skills/devforgeai-development/SKILL.md` | Defines TDD phases 01-10 |
| Phase 09 (Feedback) | `.claude/skills/devforgeai-development/phases/phase-09-feedback.md` | Current feedback hook implementation |
| Observation Protocol | `.claude/skills/devforgeai-development/references/observation-capture.md` | How observations SHOULD be captured |
| Framework Analyst | `.claude/agents/framework-analyst.md` | Subagent that synthesizes observations |
| Dev Result Interpreter | `.claude/agents/dev-result-interpreter.md` | Phase 10 output formatter |
| Hooks Configuration | `devforgeai/config/hooks.yaml` | Hook triggers and settings |
| Phase State Files | `devforgeai/workflows/{STORY_ID}-phase-state.json` | Per-story phase tracking |
| Feedback Storage | `devforgeai/feedback/ai-analysis/{STORY_ID}/` | Where AI analysis results are stored |
| Feedback Skill | `.claude/skills/devforgeai-feedback/SKILL.md` | The feedback collection skill |

### Glossary (7 entries)

| Term | Definition |
|------|------------|
| Phase 01-10 | The 10-phase TDD workflow in `/dev` command |
| Exit Gate | A validation checkpoint at the end of each phase |
| Subagent Contract | The markdown file in `.claude/agents/` that defines a subagent |
| Two-Hat Problem | Claude simultaneously executing tasks AND reflecting on the process |
| Inline Display | Showing feedback during `/dev` workflow execution |
| Observation | A structured note capturing friction, success, patterns, gaps, ideas, or bugs |
| STORY-018 | The story that implemented the hook system architecture |

---

**RCA Created:** 2026-01-26
**Last Updated:** 2026-01-26
