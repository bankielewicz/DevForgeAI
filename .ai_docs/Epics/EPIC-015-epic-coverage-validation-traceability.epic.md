---
epic_id: EPIC-015
title: Epic Coverage Validation & Requirements Traceability
status: Planning
created: 2025-11-25
priority: High
complexity: 26
architecture_tier: Tier 2
estimated_sprints: 2
stakeholders:
  - DevForgeAI Framework Maintainers
  - DevForgeAI Users
  - Project Managers
tags:
  - validation
  - traceability
  - quality-assurance
  - gap-detection
  - automation
---

# EPIC-015: Epic Coverage Validation & Requirements Traceability

## Executive Summary

Create a comprehensive epic coverage validation system with requirements traceability matrix to automatically detect missing stories from epics, track progress, generate actionable reports, and integrate with story creation workflow to eliminate gaps in the DevForgeAI framework.

## Business Problem

**Current State:**
- 13 epics with unknown completion status (can't verify if all features have stories)
- Manual tracking overhead (error-prone comparison of epics to stories)
- Risk of incomplete features (features might be missing without anyone noticing)
- No visibility into epic progress (can't calculate % complete)
- Difficulty tracking requirements → epics → sprints → stories lineage

**Impact:**
- Framework completeness unknown (potential gaps in DevForgeAI implementation)
- Wasted effort (manual checks of 13 epics × 58 stories = time-consuming)
- Quality risk (missing stories = incomplete features shipped)
- Poor project visibility (stakeholders can't assess progress)

## Business Goals

1. **Complete feature visibility** - Know exactly which epic features have stories and which don't
2. **Automated gap detection** - System automatically identifies missing stories without manual review
3. **Progress tracking** - Track epic completion percentage (e.g., "7 of 10 features have stories - 70% complete")
4. **Actionable reports** - Generate reports that tell users exactly what stories need to be created
5. **Full integration** - Seamlessly integrate with /create-story workflow to fill gaps automatically

## Success Criteria

1. ✅ `/validate-epic-coverage` command created and functional
2. ✅ Gap detection engine correctly identifies missing stories (>95% accuracy)
3. ✅ Progress tracking displays completion % for all epics
4. ✅ Reports generated in 3 formats: terminal output, markdown, JSON
5. ✅ Full integration with /create-story workflow (hybrid interactive approach)
6. ✅ Traceability matrix tracks requirements → epics → sprints → stories
7. ✅ Historical tracking persists validation reports over time
8. ✅ All 3 test types passing (integration, regression, edge cases)
9. ✅ Performance acceptable (TBD - will be benchmarked during implementation)
10. ✅ Documentation complete (command docs + CLAUDE.md user guide)

## Features

### Feature 0: Requirements Traceability Matrix (Foundation)
**Description:** Data model and parsing infrastructure for tracking requirements → epics → sprints → stories linkages

**Deliverables:**
- Simple data model using Bash associative arrays or JSON files
- Parse epic frontmatter (epic_id, title, features section) using Grep patterns
- Parse story `epic:` field using Grep (`grep "^epic: EPIC-XXX"`)
- Extract `## Stories` tables from epics using Read + Grep
- Relationship validation (epic: references exist, no orphaned stories)
- Data structure: JSON file or Bash arrays (no complex libraries)

**Value:** Foundational infrastructure that Features 2-6 depend on for gap detection

**Dependencies:** None (foundational capability)

**Estimated Points:** 13

---

### Feature 1: Epic & Story Metadata Parser
**Description:** Parse epic and story markdown files to extract metadata and feature information

**Deliverables:**
- Epic parser: Extract frontmatter + features section (markdown headers like "### Feature X")
- Story parser: Extract frontmatter (especially epic_id field)
- Error handling: Malformed YAML, missing frontmatter, invalid epic structure
- Coverage mapping: Link stories to epic features via epic_id
- Data validation: Ensure epic_id in stories matches existing epics

**Value:** Accurate metadata extraction enables reliable gap detection

**Dependencies:** Feature 0 (traceability matrix data model)

**Estimated Points:** 13

---

### Feature 2: Gap Detection Engine
**Description:** Match epic features to stories using multiple strategies and identify missing coverage

**Deliverables:**
- Strategy 1: Story `epic:` field matching (Grep: `grep "^epic: EPIC-XXX" story.md`)
- Strategy 2: Epic's `## Stories` table parsing (Read + Grep for table rows)
- Strategy 3: Cross-validation (ensure bidirectional mapping consistency)
- Completion calculation: (stories_with_epic_field / total_features) × 100%
- Missing feature list: Features with no story references in either direction
- Orphaned stories: Stories with `epic: EPIC-XXX` where epic doesn't exist

**Value:** Core capability - identifies exactly which epic features lack stories

**Dependencies:** Feature 0 (data model), Feature 1 (parsers)

**Estimated Points:** 21

---

### Feature 3: Coverage Reporting System
**Description:** Generate coverage reports in multiple formats with historical tracking

**Deliverables:**
- **Terminal output:** Color-coded status (Green: 100%, Yellow: 50-99%, Red: <50%)
- **Markdown reports:** Generated in `.devforgeai/epic-coverage/reports/YYYY-MM-DD-HH-MM-SS.md`
- **JSON export:** Programmatic access for tooling integration
- **Report contents:**
  - Summary statistics (total epics, total features, overall coverage %, missing stories count)
  - Per-epic breakdown (epic_id, title, completion %, missing features list)
  - Actionable next steps (recommended /create-story commands per gap)
- **Historical tracking:** Full history persisted in `.devforgeai/epic-coverage/history/`

**Value:** Clear visibility into epic progress and exactly what needs to be done

**Dependencies:** Feature 2 (gap detection data)

**Estimated Points:** 18

---

### Feature 4: Slash Command Interface
**Description:** User-friendly command interface for invoking epic coverage validation

**Deliverables:**
- `/validate-epic-coverage` (no args - validate all epics)
- `/validate-epic-coverage EPIC-XXX` (single epic validation)
- Output: Terminal display with color-coded status
- Actionable output: "To fill gaps, run: /create-story [feature-description]"
- Help text: Command documentation with examples
- Error handling: Invalid epic IDs, file system errors

**Value:** Easy-to-use interface for daily validation workflows

**Dependencies:** Feature 3 (reporting system)

**Estimated Points:** 8

---

### Feature 5: /create-story Integration
**Description:** Full integration with story creation workflow to automatically populate missing stories

**Deliverables:**
- Gap-to-story suggestion: Convert missing feature → story description template
- Hybrid approach: Report shows gaps with interactive "Create story for this feature? [Y/n]"
- Epic context passing: Auto-populate story epic_id field from gap data
- Batch creation prompt: "Found 5 gaps. Create all stories now? [Y/n/Select]"
- Integration points:
  - `/validate-epic-coverage` shows gap count + "Run /create-missing-stories to fill"
  - `/create-missing-stories` new command (optional) for batch story creation
- Story template population: Pre-fill epic_id, feature title, basic acceptance criteria

**Value:** Eliminates manual work - gaps automatically become stories with one command

**Dependencies:** Feature 2 (gap detection), Feature 4 (command interface)

**Estimated Points:** 13

---

### Feature 6: Integration with DevForgeAI Commands
**Description:** Integrate coverage validation into existing DevForgeAI workflow as quality gates

**Deliverables:**
- `/create-epic` validation hook: Verify new epics have proper feature structure
- `/orchestrate` quality gate: Run coverage validation before sprint planning (warn if <80% coverage)
- Error handling:
  - Malformed epic files: Clear error message with line number and fix suggestions
  - Orphaned stories: Report stories with invalid epic_id references
  - Ambiguous matching: Flag low-confidence matches (60-75%) for manual review
- Integration test suite: Test all 3 integration points with sample data

**Value:** Proactive validation prevents gaps from forming in the first place

**Dependencies:** Feature 4 (command interface)

**Estimated Points:** 13

---

## Requirements Summary

### Functional Requirements

**Core Capabilities:**
1. Automated gap detection (parse epics → match stories → identify missing)
2. Progress tracking (calculate and display completion %)
3. Actionable reports (terminal, markdown, JSON formats)
4. /create-story integration (hybrid interactive approach)

**User Flows:**
1. **Validation Flow:**
   - User runs `/validate-epic-coverage`
   - System parses all epics and stories
   - System matches features to stories
   - System displays report with gaps and completion %

2. **Gap Filling Flow:**
   - User sees gaps in report
   - User accepts prompt to create missing stories
   - System invokes /create-story with pre-populated epic context
   - Stories created with proper epic_id linkage

### Data Model

**Entities:**
1. **Epic Metadata**
   - epic_id (string, primary key)
   - title (string)
   - features (list of feature objects)
   - status (string: Planning, In Progress, Complete)

2. **Story Metadata**
   - story_id (string, primary key)
   - epic_id (string, foreign key to Epic)
   - title (string)
   - status (string: workflow state)

3. **Coverage Mappings**
   - epic_id (string)
   - feature_id (string, derived from "### Feature X" headers)
   - matched_stories (list of story_ids)
   - confidence_score (float, 0.0-1.0)

4. **Gap Records**
   - epic_id (string)
   - feature_id (string)
   - feature_title (string)
   - missing_story_count (int)
   - suggested_story_description (string)

**Relationships:**
- Epic → Features: one-to-many (embedded in epic markdown)
- Epic → Stories: one-to-many (via story.epic_id foreign key)
- Feature → Stories: many-to-many (one feature can have multiple stories, one story can implement parts of multiple features)

### Integration Points

1. **`/create-story` command:** Pass gap data (epic_id, feature description) to auto-populate new stories
2. **`/create-epic` command:** Validate epic structure on creation (proper frontmatter, features section exists)
3. **`/orchestrate` command:** Run coverage validation as quality gate before sprint planning

### Non-Functional Requirements

**Performance:**
- Current scale: TBD - will be benchmarked with 13 epics + 58 stories during implementation
- Future scale: TBD - will be benchmarked with test fixtures simulating 100 epics + 500 stories
- Note: RESEARCH-002 projected 3.2 seconds for 100 epics (unmeasured estimate, not evidence-based)

**Security:**
- No sensitive data stored
- File system access (read .ai_docs/Epics/, .ai_docs/Stories/)
- Write access (.devforgeai/epic-coverage/ for reports)

**Scalability:**
- Small scale (DevForgeAI's 13 epics → 100 epics future)
- No pagination needed (all data fits in memory: <10MB for 100 epics + 500 stories)
- Graph-based in-memory structure (fast traversal, no database required)

**Availability:**
- Not critical (CLI analysis tool, no SLA)
- Single-user execution (no concurrency requirements)

**Error Handling:**
1. **Malformed epic files:** Clear error with line number and fix suggestion
2. **Orphaned stories:** Report stories with epic_id that doesn't match any existing epic
3. **Ambiguous matching:** Flag low-confidence matches (60-75% similarity) for manual review

## Architecture Considerations

**Complexity Tier:** Tier 2 (Moderate Application) - Score: 26/60

**Recommended Architecture:**
- **Pattern:** Simple Bash Script
- **Layers:** Single script with functions
  1. Parsing functions (Grep patterns for epic: and ## Stories)
  2. Matching functions (exact epic: field matching)
  3. Reporting functions (JSON/markdown generation)
- **Database:** None (JSON files for data, markdown for reports)
- **Deployment:** Slash command in .claude/commands/validate-epic-coverage.md

**Technology Recommendations (Claude Code Native Tools):**
- **Language:** Bash scripting (Claude Code native)
- **Parsing:** Grep patterns for YAML frontmatter and markdown headers
- **Matching:** Exact `epic:` field matching via Grep (`grep "^epic: EPIC-XXX"`)
- **Data Structure:** JSON files or Bash associative arrays (no libraries needed)
- **CLI Framework:** Slash command in `.claude/commands/` (DevForgeAI standard)
- **Testing:** Bash test scripts (existing DevForgeAI pattern)

**Technical Stack:**
```bash
# No external dependencies - uses only Claude Code native tools:
  - Grep (pattern matching for epic: field and ## Stories tables)
  - Read (reading epic and story markdown files)
  - Write (generating JSON/markdown reports)
  - Bash (orchestration and data processing)
```

## Feasibility Analysis

**Research Report:** [RESEARCH-002-epic-coverage-traceability.md](.devforgeai/research/shared/RESEARCH-002-epic-coverage-traceability.md)

**Technical Feasibility Score:** 8.7/10 (High Confidence - GO with high confidence)

**Top Recommendation (REVISED):**
- **Data Model:** JSON files or Bash associative arrays - Simple, no external dependencies
- **Matching Strategy:** Exact `epic:` field via Grep - 95% of stories have this field (evidence-based)
- **Performance:** TBD - will be benchmarked during implementation with native tools

**Key Risks & Mitigations:**

| Risk | Severity | Probability | Mitigation |
|------|----------|-------------|------------|
| Manual reference maintenance | CRITICAL | HIGH | Validation in /create-story workflow (auto-set epic: field) |
| Missing epic: field in stories | MEDIUM | LOW | 5% of stories missing epic: field - report in validation output for manual addition |
| Orphaned story detection | MEDIUM | MEDIUM | Validate epic: references exist, report orphaned stories |
| Malformed epic structure | MEDIUM | LOW | Detailed error messages with line numbers and fix suggestions |
| Performance degradation at scale | LOW | LOW | In-memory graph structure chosen for scalability (specific performance TBD via benchmarking) |
| Maintenance burden | LOW | LOW | Simple Bash script, comprehensive documentation, Bash test scripts |
| Missing features in epics | MEDIUM | MEDIUM | /create-epic validation hook ensures proper structure on creation |
| Story epic: field changes | MEDIUM | LOW | Git history tracks epic: field changes, validation reports mismatches |

## Dependencies

**Prerequisites:**
- None (standalone capability, first in DevForgeAI validation tooling)

**Dependents:**
- EPIC-016 (potential): Full Requirements Traceability (requirements → epics → sprints → stories)
  - Epic-015 provides foundational traceability matrix
  - EPIC-016 would extend to requirements-level tracking

**External Dependencies:**
- None (uses only Claude Code native tools: Grep, Read, Write, Bash)

## Next Steps

### Immediate (Week 1)
1. **Create ADR:** ADR-005-epic-coverage-traceability-architecture.md
2. **Update context files:**
   - tech-stack.md: Document Bash/Grep/Read/Write native tools approach
   - source-tree.md: Add .devforgeai/epic-coverage/ directory structure
   - dependencies.md: No changes needed (zero external dependencies)
3. **Create Sprint 2:** Break EPIC-015 into sprint-ready stories
4. **Run `/create-context`** if needed (validate tech-stack updates)

### Architecture Phase (Week 1-2)
1. Design data model (JSON files or Bash associative arrays)
2. Design CLI interface (slash command in .claude/commands/)
3. Design matching workflow (Grep patterns for epic: field + ## Stories tables)
4. Create technical specification for each feature

### Implementation Phase (Week 2-6)
1. **Week 2:** Feature 0 (Traceability Matrix) + Feature 1 (Parsers)
2. **Week 3:** Feature 2 (Gap Detection Engine)
3. **Week 4:** Feature 3 (Reporting) + Feature 4 (CLI Interface)
4. **Week 5:** Feature 5 (/create-story Integration) + Feature 6 (Command Integration)
5. **Week 6:** Testing (integration + regression + edge cases) + Documentation

### Quality Gates
1. **After Feature 0:** Unit tests passing, data model validated with 13 existing epics
2. **After Feature 2:** Gap detection accuracy >95% (validated with ground truth)
3. **After Feature 4:** Integration tests passing (all 13 epics validated successfully)
4. **Before Release:** All 3 test types passing + documentation complete

---

## Estimated Effort

**Total Story Points:** 99 points (across 7 features)
**Estimated Sprints:** 2 sprints (2 weeks per sprint = 4 weeks total)
**Sprint Capacity:** 50 points/sprint (assumes 1 developer full-time)

**Sprint Breakdown:**
- **Sprint 1:** Features 0-2 (13 + 13 + 21 = 47 points) - Foundational infrastructure + gap detection
- **Sprint 2:** Features 3-6 (18 + 8 + 13 + 13 = 52 points) - Reporting + CLI + integrations

---

**Status:** Planning → Ready for Architecture Phase
**Next Action:** Create ADR-005 and update context files, then run `/create-context` validation

---

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-083 | Feature 0 | Requirements Traceability Matrix Foundation | 13 | Backlog |
| STORY-084 | Feature 1 | Epic & Story Metadata Parser | 13 | Backlog |
| STORY-085 | Feature 2 | Gap Detection Engine | 21 | Backlog |
| STORY-086 | Feature 3 | Coverage Reporting System | 18 | Backlog |
| STORY-087 | Feature 4 | Slash Command Interface | 8 | Backlog |
| STORY-088 | Feature 5 | /create-story Integration | 13 | Backlog |
| STORY-089 | Feature 6 | DevForgeAI Command Integration | 13 | Backlog |
