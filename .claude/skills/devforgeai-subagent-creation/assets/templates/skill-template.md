# Skill Template v1.0

**Template Version:** 1.0
**Created:** 2026-02-11
**Purpose:** Canonical template for creating new DevForgeAI skills with standardized phase patterns and progressive disclosure.

---

## YAML Frontmatter Specification

### Required Fields

```yaml
---
name: skill-name-here              # Required: Unique identifier (kebab-case)
description: Brief purpose         # Required: One-line when-to-use description
model: inherit                     # Required: inherit | opus | sonnet | haiku
---
```

### Optional Fields

```yaml
---
allowed-tools:                     # Optional: Array format, one tool per line
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Skill
  - Task
version: 1.0                       # Optional: Semantic version
status: active                     # Optional: active | deprecated | experimental
---
```

**Field Constraints:**
- `name`: Required. Lowercase, hyphenated, no spaces (e.g., `implementing-stories`)
- `description`: Required. Brief description of WHEN to use this skill
- `model`: Required. Use `inherit` unless specific model needed for task
- `allowed-tools`: Optional. Array format with one tool per line (canonical)
- `version`: Optional. Use semantic versioning (MAJOR.MINOR)
- `status`: Optional. Defaults to `active` if omitted

**Deprecated Alias:** The `tools` string format (e.g., `tools: Read, Write`) continues to function but `allowed-tools` array is preferred for new skills.

---

## Execution Model Block

**COPY THIS BLOCK to your skill (lines ~40-60):**

```markdown
## Execution Model: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. Phase gates block progression if incomplete

**Do NOT:**
- Do NOT wait passively for skill to "return results"
- Do NOT assume skill is executing elsewhere
- Do NOT stop workflow after invocation
- Do NOT skip phases or reorder execution
- Do NOT omit required subagent invocations

**Proceed to Phase 01 and begin execution.**
```

---

## Phase Instruction Pattern

### Phase Numbering

Use zero-padded two-digit format for consistent sorting:

```markdown
## Phase 01: [Phase Name]
## Phase 02: [Phase Name]
...
## Phase 10: [Phase Name]
```

### Phase Structure Template

Each phase MUST include:

```markdown
## Phase NN: [Phase Name]

**Objective:** [One-sentence goal of this phase]

**Pre-Flight:** (if phase has prerequisites)
```bash
devforgeai-validate phase-check ${STORY_ID} --from=NN-1 --to=NN
```

**Steps:**

1. **Step description**
   ```
   Task(
     subagent_type="subagent-name",
     description="Brief task description",
     prompt="Detailed prompt..."
   )
   ```

2. **Step description**
   [Details...]

**Validation Checkpoint:**
- [ ] Required item verified
- [ ] Required subagent invoked

**Exit Gate:**
```bash
devforgeai-validate phase-complete ${STORY_ID} --phase=NN --checkpoint-passed
```
```

### Read() Hint Syntax

Reference loading uses absolute paths immediately after section headers:

```markdown
**Reference:** Load detailed workflow
Read(file_path=".claude/skills/{skill-name}/references/{file}.md")
```

**Loading Patterns:**
- Standard: `Read(file_path=".claude/skills/{skill-name}/references/{file}.md")`
- Conditional: `Load if [condition]: Read(file_path="...")`
- Multiple: List each Read() on separate line

---

## Progressive Disclosure Allocation

### Content Allocation Table

| Content Type | Location | Line Budget | When to Extract |
|--------------|----------|-------------|-----------------|
| Frontmatter, Purpose, Execution Model | SKILL.md | 50-80 lines | Never |
| Phase summaries with Read() hints | SKILL.md | 200-400 lines | Never |
| Success criteria, Error handling | SKILL.md | 50-100 lines | Never |
| **SKILL.md Total** | — | **300-600 lines** | — |
| Detailed phase guides | references/ | 100-500 lines each | Always for phases |
| Algorithms, validation procedures | references/ | 100-300 lines each | If section > 100 lines |
| Output file templates | assets/templates/ | Varies | Always |
| Per-phase guides (8+ phase skills) | phases/ | 50-200 lines each | If 8+ complex phases |

### Extraction Decision Matrix

| Condition | Action |
|-----------|--------|
| Section exceeds 100 lines | Extract to references/ |
| Skill has 8+ complex phases | Use phases/ subdirectory |
| Content is output template | Place in assets/templates/ |
| Content duplicates SKILL.md | REMOVE (no duplication allowed) |
| Skill exceeds 800 lines | MUST extract until under 800 |
| Skill exceeds 1000 lines | BLOCKED - cannot deploy |

---

## Reference File Requirements

### Standalone Readability

Each reference file MUST be independently understandable:

```markdown
# [Reference Title]

**Purpose:** [What this reference provides]
**Parent Skill:** [skill-name]
**When to Load:** [Condition or phase]

---

## [Section 1]
[Content...]

## [Section 2]
[Content...]
```

### Reference Loading Rules

1. **No Duplication:** Reference files MUST NOT duplicate SKILL.md content
2. **Single Source of Truth:** Content exists in ONE location only
3. **Load on Demand:** References loaded only when phase/condition triggers
4. **Absolute Paths:** Use `.claude/skills/{skill-name}/references/{file}.md`
5. **H1 Title Required:** Every reference file starts with `# Title`

---

## Line Budget Guidance

### Section Budget Table

| Section | Target Lines | Maximum Lines |
|---------|--------------|---------------|
| YAML Frontmatter | 5-10 | 15 |
| Purpose/Overview | 5-15 | 25 |
| Execution Model | 15-25 | 35 |
| Phase Summaries (all) | 150-300 | 400 |
| Success Criteria | 10-20 | 30 |
| Error Handling | 15-30 | 50 |
| References Section | 10-20 | 30 |
| **Template Total** | **~220** | **300** |
| **Skill-Specific Content** | **280-500** | **700** |
| **SKILL.md Total** | **500-720** | **1000** |

### Size Reduction Checklist

When approaching 800 lines, extract in priority order:

1. [ ] Long examples (> 20 lines) → `references/examples/`
2. [ ] Detailed algorithms → `references/{algorithm-name}.md`
3. [ ] Validation matrices → `references/validation-*.md`
4. [ ] Multi-step procedures → `phases/phase-NN-*.md`
5. [ ] Error handling details → `references/error-handling.md`

---

## Migration Notes

### Backward Compatibility

This template is **additive** - existing skills continue to function without modification:

- **Existing skills:** Not required to immediately adopt this template
- **tools string format:** Continues to work alongside `allowed-tools` array
- **Unpadded phase numbers:** Continue to function alongside zero-padded
- **Template scope:** Applies only to NEW skills and skills being actively UPDATED

### Adoption Timeline

| Phase | Scope | Action |
|-------|-------|--------|
| Immediate | New skills | Use this template |
| On Update | Existing skills | Migrate to template when updating |
| Never | Stable skills | No forced migration required |

### Migration Checklist (When Updating Existing Skills)

- [ ] Convert `tools:` string to `allowed-tools:` array
- [ ] Add zero-padding to phase numbers (1 → 01)
- [ ] Add Objective statement to each phase
- [ ] Add Pre-Flight verification where prerequisites exist
- [ ] Extract sections > 100 lines to references/
- [ ] Verify total lines < 1000 (target < 800)
- [ ] Add Execution Model block if missing

---

## Self-Validation Checklist

Before deploying a skill created from this template, verify:

1. [ ] YAML frontmatter has `name`, `description`, `model` (3 required fields)
2. [ ] `allowed-tools` uses array format (if present)
3. [ ] Execution Model block present with 4-point list and 3+ Do NOT items
4. [ ] All phases use zero-padded numbering (01, 02, ... 10)
5. [ ] Each phase has Objective statement
6. [ ] Phases with prerequisites have Pre-Flight verification
7. [ ] Reference loading uses Read() hint syntax with absolute paths
8. [ ] No content duplicated between SKILL.md and references/
9. [ ] Total SKILL.md under 1000 lines (target 500-800)
10. [ ] Sections exceeding 100 lines extracted to references/

---

## Example Structures

**Simple Skill (3-5 phases):** `SKILL.md` (400-600 lines) + `references/` for deep docs

**Complex Skill (8+ phases):** `SKILL.md` (600-800 lines) + `phases/` for per-phase guides + `references/` + `assets/templates/`

---

**References:** source-tree.md, tech-stack.md, prompt-engineering-patterns.md (PE-052, PE-036)

**Template Version:** 1.0 | **Updated:** 2026-02-11 | **Source:** EPIC-061, STORY-387
