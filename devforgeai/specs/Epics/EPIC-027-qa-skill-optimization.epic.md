---
id: EPIC-027
title: QA Skill Optimization
business-value: Reduce token consumption and improve QA validation efficiency through story type awareness and streamlined checkpoints
status: Planning
priority: High
complexity-score: 8
architecture-tier: Tier 2 (Standard Application)
created: 2025-12-20
estimated-points: 14
target-sprints: 2
research-reference: STORY-114 architectural analysis
related-epics: [EPIC-025]
stories: [STORY-130, STORY-131, STORY-132]
---

# QA Skill Optimization

## Business Goal

Optimize the DevForgeAI QA skill based on architectural analysis from STORY-114 validation experience. The current QA skill has verbose checkpoint patterns and lacks story type awareness, resulting in unnecessary token consumption and suboptimal validation paths for non-feature stories.

**Success Metrics:**
- Token reduction: 25-45% depending on story type
- Documentation stories: Skip coverage/quality phases (35-45% reduction in light mode)
- Checkpoint verbosity: Reduce from 25 lines to 6 lines per phase
- Report consistency: Template-based generation for all reports

## What Works Well (Preserve)

1. **Progressive Disclosure Model** - Load references when phase executes, not upfront
2. **AC-to-DoD Traceability Validation** - 5-step algorithm with 50% keyword threshold
3. **Story File Structure** - v2.2 template with YAML frontmatter + checkbox syntax
4. **Subagent Delegation** - Isolated context for anti-pattern-scanner, deferral-validator
5. **Test Organization** - Per-story directories (`devforgeai/tests/STORY-XXX/`)

## Areas Needing Improvement

1. **QA Phase Complexity** - 8 phases with 5-7 mandatory checkpoints each
2. **Story Type Classification Missing** - Documentation stories run coverage metrics
3. **Anti-Pattern Severity Calibration** - LOW violations clutter console output
4. **Parallel Validation Conditional** - Full parallel validation overkill for simple stories
5. **Manual QA Report Generation** - No template-based approach
6. **Feedback Hook Skip Conditions** - Implicit rather than explicit

## Features

### Feature 1: Story Type Classification with QA Routing (STORY-130)

**Description:** Add `type` field to story frontmatter and implement conditional QA phase execution based on story type.

**User Stories (high-level):**
1. As a developer, I want stories to have a type field (feature/documentation/bugfix/refactor)
2. As a developer, I want documentation stories to skip coverage and code quality phases
3. As a developer, I want backward compatibility when type field is missing

**Estimated Effort:** 5 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | Add `type` field |
| MODIFY | `.claude/skills/devforgeai-qa/SKILL.md` | Add type extraction + phase routing |
| MODIFY | `.claude/skills/devforgeai-development/SKILL.md` | Add phase skipping for /dev |

**Phase Skip Matrix:**
| Type | Skipped QA Phases | Rationale |
|------|-------------------|-----------|
| feature | None | Full validation |
| documentation | Phase 1 (coverage), Phase 4 (quality) | No runtime code |
| bugfix | Phase 2.5 (parallel validators) in light | Fast feedback |
| refactor | None | Full regression check |

**Acceptance Criteria Themes:**
- AC#1: Story frontmatter supports `type` field with 4 valid values
- AC#2: Missing `type` defaults to "feature" (backward compatible)
- AC#3: QA skill extracts type and routes phases accordingly
- AC#4: Log message displayed when phase skipped
- AC#5: /dev command respects story type for TDD phase skipping

### Feature 2: Simplified QA Checkpoint Pattern (STORY-131)

**Description:** Replace verbose checkpoint checklists with decision gate pattern and document explicit hook skip conditions.

**User Stories (high-level):**
1. As a developer, I want concise phase checkpoints (6 lines vs 25 lines)
2. As a developer, I want clear decision gates (Execute→Validate→Display→Gate)
3. As a developer, I want explicit hook skip conditions documented

**Estimated Effort:** 3 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-qa/SKILL.md` | Simplify all 8 phase checkpoints |

**Before (verbose):**
```markdown
**Phase 1 Completion Checklist:**
Before proceeding to Phase 2, verify you executed ALL 7 steps:
- [ ] Loaded coverage-analysis-workflow.md (Step 1.0)
- [ ] Step 1: Loaded coverage thresholds...
[...25 lines...]
```

**After (decision gate):**
```markdown
**Phase 1 Gate:**
- **Execute:** Load `references/coverage-analysis-workflow.md`, execute all steps
- **Validate:** Coverage metrics for BL (95%), App (85%), Infra (80%)
- **Display:** `✓ Phase 1: Coverage - BL: X%/95% | App: X%/85% | Infra: X%/80%`
- **Gate:** coverage_calculated → Phase 2 | ELSE → HALT
```

**Acceptance Criteria Themes:**
- AC#1: All 8 phases use Execute→Validate→Display→Gate pattern
- AC#2: Token reduction ≥1500 measured
- AC#3: Phase 6 has explicit hook skip conditions
- AC#4: All existing QA scenarios still pass

### Feature 3: QA Report Templates with Severity Filtering (STORY-132)

**Description:** Implement template-based report generation and severity-based display filtering.

**User Stories (high-level):**
1. As a developer, I want light mode to use a concise report template
2. As a developer, I want MEDIUM violations shown as count only in console
3. As a developer, I want LOW violations in report file only

**Estimated Effort:** 6 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| CREATE | `.claude/skills/devforgeai-qa/assets/templates/qa-report-light.md` | Light mode template |
| MODIFY | `.claude/skills/devforgeai-qa/references/report-generation.md` | Template loading + severity filtering |
| MODIFY | `.claude/skills/devforgeai-qa/assets/templates/qa-report-template.md` | Update MEDIUM/LOW sections |

**Severity Display Rules:**
| Severity | Console Output | Report File |
|----------|----------------|-------------|
| CRITICAL | Full details + file:line + remediation | Full details |
| HIGH | Full details + remediation | Full details |
| MEDIUM | Count only: "4 MEDIUM - see report" | Full details |
| LOW | Never displayed | Full details with "Advisory:" prefix |

**Acceptance Criteria Themes:**
- AC#1: Light mode uses qa-report-light.md template
- AC#2: Deep mode uses qa-report-template.md
- AC#3: MEDIUM violations show count + report reference
- AC#4: LOW violations never in console output

## Token Impact Summary

| Improvement | Tokens Saved | When Applied |
|-------------|--------------|--------------|
| Simplified checkpoints | -1600 | Every QA run |
| Severity filtering | -200 to -500 | Reports with MEDIUM/LOW |
| Conditional execution | -2000 to -4000 | Documentation stories |
| Template reuse | -500 | Light mode |

**Net by Story Type:**
| Type | Light Mode | Deep Mode |
|------|------------|-----------|
| feature | -15 to -20% | -3 to -4% |
| documentation | -35 to -45% | -25 to -35% |
| bugfix | -18 to -23% | -3 to -4% |

## Architecture Principles (Document)

Create `devforgeai/specs/context/architecture-principles.md` documenting:

1. **Progressive Disclosure Over Upfront Loading**
2. **Subagent Delegation for Complex Validation**
3. **Story Type Awareness**
4. **Decision Gates Over Checklists**
5. **Template-Based Output Generation**
6. **Severity-Based Display Filtering**

## Dependencies

- STORY-130 must complete before STORY-131 and STORY-132 can use story type routing
- STORY-131 and STORY-132 can be implemented in parallel after STORY-130

## Relationship to EPIC-025

STORY-126 (in EPIC-025) covers story type detection for `/dev` command.
STORY-130 (this epic) covers story type detection for `/qa` command.

Recommendation: Keep separate - QA routing has additional complexity (phase skip matrix, hooks) that warrants its own story. Both can share the story type field in frontmatter.

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Backward compatibility break | Default `type` to "feature" if missing |
| Checkpoint simplification gaps | Test all 8 phases with both modes |
| Template variable mismatch | Validate all {{VAR}} patterns exist |
| Phase skip causes validation gaps | Document override mechanism for edge cases |
