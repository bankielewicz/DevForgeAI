---
id: EPIC-056
title: Treelint Context File Integration
status: Planning
start_date: 2026-02-01
target_date: 2026-02-14
total_points: 8-13
created: 2026-01-30
updated: 2026-01-30
source_brainstorm: BRAINSTORM-009
source_requirements: treelint-integration-requirements.md
parent_initiative: Treelint AST-Aware Code Search Integration
related_epics: [EPIC-055, EPIC-057, EPIC-058, EPIC-059]
depends_on: [EPIC-055]
---

# Epic: Treelint Context File Integration

## Business Goal

Update DevForgeAI's constitutional context files to support Treelint infrastructure, ensuring the `.treelint/` directory structure is documented, gitignore patterns are established, and anti-pattern guidance includes Treelint-specific recommendations. This enables subsequent epics to reference standardized locations and patterns.

## Success Metrics

- **Metric 1:** source-tree.md includes `.treelint/` directory with correct structure
- **Metric 2:** .gitignore patterns for `.treelint/index.db` and `.treelint/daemon.sock` documented
- **Metric 3:** anti-patterns.md includes Treelint usage guidance (when to use Treelint vs Grep)
- **Metric 4:** Zero framework validation failures after context file updates
- **Metric 5:** All 6 context files remain syntactically valid (LOCKED markers intact)

## Scope

### Overview

This epic updates 2-3 context files to support Treelint infrastructure. It does NOT modify any subagents, skills, or application code. Focus is entirely on constitutional documentation updates that establish standards for subsequent implementation work.

### Features

1. **source-tree.md Update**
   - Description: Add `.treelint/` directory structure definition with index.db, config.toml, daemon.sock
   - User Value: AI agents know where Treelint artifacts belong in project structure
   - Estimated Points: 2-3 story points

2. **Gitignore Pattern Documentation**
   - Description: Document which `.treelint/` files should be gitignored vs committed
   - User Value: Prevents accidental commits of large index files and ephemeral sockets
   - Estimated Points: 1-2 story points

3. **anti-patterns.md Treelint Guidance**
   - Description: Add guidance for when to use Treelint vs Grep (supported languages, fallback behavior)
   - User Value: AI agents make correct tool choices without trial-and-error
   - Estimated Points: 2-3 story points

4. **Context File Validation**
   - Description: Validate all context file updates pass framework validation
   - User Value: Ensures constitutional documents remain consistent and valid
   - Estimated Points: 2-3 story points

### Out of Scope

- ❌ Subagent modifications (covered by EPIC-057)
- ❌ Skill modifications (covered by EPIC-059)
- ❌ tech-stack.md update (covered by EPIC-055)
- ❌ dependencies.md update (covered by EPIC-055)
- ❌ Binary distribution (covered by EPIC-055)
- ❌ Actual Treelint usage implementation

## Target Sprints

**Estimated Duration:** 1 sprint / 2 weeks (concurrent with EPIC-055)

**Sprint Breakdown:**
- **Sprint 1:** All 4 features - 8-13 story points

## Dependencies

### External Dependencies

- None - context file updates are documentation-only

### Internal Dependencies

- **EPIC-055 (Foundation):** ADR-013 must be approved before modifying context files
- **ADR-013 approved:** Treelint adoption decision must be formalized first

### Blocking Issues

- **Blocker 1:** If ADR-013 not approved, cannot add Treelint references to context files
  - Mitigation: EPIC-055 stories scheduled first; this epic starts after ADR approval

## Stakeholders

- **Product Owner:** Framework Architect (You)
- **Tech Lead:** Framework Architect (You)
- **Other Stakeholders:** AI agents that read context files, DevForgeAI users

## Requirements

### Functional Requirements

#### User Stories

**User Story 1: source-tree.md Update**
```
As an AI Agent,
I want the .treelint/ directory documented in source-tree.md,
So that I know where Treelint artifacts belong in project structure.
```

**Acceptance Criteria:**
- [ ] `.treelint/` directory added to directory structure section
- [ ] `index.db` documented as SQLite index (gitignored)
- [ ] `config.toml` documented as project config (optional commit)
- [ ] `daemon.sock` documented as IPC socket (gitignored)
- [ ] Directory placed at project root level in structure
- [ ] Comment explaining Treelint purpose included

**User Story 2: Gitignore Patterns**
```
As a Developer,
I want .treelint/ gitignore patterns documented,
So that I don't accidentally commit large index files or ephemeral sockets.
```

**Acceptance Criteria:**
- [ ] Gitignore patterns documented in source-tree.md or separate section
- [ ] `.treelint/index.db` marked as gitignored (can be large)
- [ ] `.treelint/daemon.sock` marked as gitignored (ephemeral)
- [ ] `.treelint/config.toml` marked as optional commit (project settings)
- [ ] Rationale provided for each pattern

**User Story 3: anti-patterns.md Treelint Guidance**
```
As an AI Agent,
I want Treelint usage guidance in anti-patterns.md,
So that I know when to use Treelint vs Grep without trial-and-error.
```

**Acceptance Criteria:**
- [ ] New section or subsection for "Code Search Tool Selection"
- [ ] Treelint recommended for: Python, TypeScript, JavaScript, Rust, Markdown
- [ ] Grep recommended for: unsupported languages, simple text patterns
- [ ] Anti-pattern: Using Treelint for unsupported file types
- [ ] Anti-pattern: Using Grep when Treelint available for supported language
- [ ] Severity levels assigned to each anti-pattern

**User Story 4: Context File Validation**
```
As a Framework Maintainer,
I want all context file updates validated,
So that constitutional documents remain consistent after changes.
```

**Acceptance Criteria:**
- [ ] All 6 context files pass syntax validation
- [ ] LOCKED markers remain intact in all files
- [ ] Version numbers updated in modified files
- [ ] Last Updated dates updated in modified files
- [ ] No circular references or contradictions introduced

### Non-Functional Requirements (NFRs)

#### Documentation Quality
- **Consistency:** All additions follow existing format patterns in each file
- **Clarity:** New sections include examples and rationale
- **Completeness:** All Treelint artifacts documented (nothing left undefined)

#### Backward Compatibility
- **Existing Content:** No removal or modification of existing valid content
- **Format Preservation:** Markdown structure and YAML frontmatter preserved

### Data Requirements

#### Entities

**Entity 1: .treelint/ Directory Structure**
- **Attributes:**
  - index.db (SQLite, generated, gitignored)
  - config.toml (TOML, optional, committable)
  - daemon.sock (Unix socket, ephemeral, gitignored)
- **Relationships:**
  - Located at project root
  - Used by Treelint CLI and daemon

### Integration Requirements

None - documentation updates only

## Architecture Considerations

### Complexity Tier
**Tier 1: Simple Enhancement (1-15 points)**
- **Score:** 8-13 points
- **Rationale:** Documentation-only changes, no code modifications

### Recommended Architecture Pattern

**Pattern:** Documentation-as-Code

**Justification:** Context files are constitutional documents that AI agents reference. Updates must be precise, validated, and consistent with existing patterns.

### Technology Constraints

- **Constraint 1:** Must follow existing context file format (Markdown with LOCKED markers)
- **Constraint 2:** Version numbers must be incremented for modified files
- **Constraint 3:** Changes must not break existing AI agent workflows

## Risks & Constraints

### Technical Risks

**Risk 1: Format Inconsistency**
- **Description:** New sections might not match existing documentation style
- **Probability:** Low
- **Impact:** Medium (AI agents may misinterpret)
- **Mitigation:** Use existing patterns as templates, validate formatting

**Risk 2: Incomplete Coverage**
- **Description:** Missing some Treelint artifacts or patterns
- **Probability:** Low
- **Impact:** Low (can add in later stories)
- **Mitigation:** Reference Treelint documentation for complete artifact list

### Constraints

**Constraint 1: ADR Dependency**
- **Description:** Cannot add Treelint references until ADR-013 approved
- **Impact:** Story sequencing must wait for EPIC-055 ADR story
- **Mitigation:** Plan this epic to start after ADR approval

## Assumptions

1. ADR-013 will be approved in EPIC-055
2. Current context file format will remain stable
3. `.treelint/` directory structure is final (no major changes expected)
4. Gitignore patterns are standardized across projects

## Next Steps

### Immediate Actions
1. **Wait for EPIC-055 ADR approval:** ADR-013 must be approved first
2. **Create Stories:** Use `/create-story` to create 4 stories for this epic
3. **Sprint Planning:** Add stories to Sprint 1 (after EPIC-055 ADR story)

### Pre-Development Checklist
- [ ] EPIC-055 ADR-013 story completed (APPROVED status)
- [ ] Stories created for this epic
- [ ] Current context file formats reviewed

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Stories

| Story ID | Title | Points | Status | Depends On |
|----------|-------|--------|--------|------------|
| STORY-357 | Update source-tree.md with .treelint/ Directory Structure | 2 | Backlog | STORY-349 |
| STORY-358 | Document .treelint/ Gitignore Patterns | 2 | Backlog | STORY-357 |
| STORY-359 | Add Treelint Usage Guidance to anti-patterns.md | 3 | Backlog | STORY-349 |
| STORY-360 | Validate Context File Updates After Treelint Integration | 2 | Backlog | STORY-357, STORY-358, STORY-359 |

## Notes

- This is the **second of 5 epics** in the Treelint integration initiative
- Can run **concurrently** with EPIC-055 after ADR-013 is approved
- EPIC-057 (Subagent Integration) depends on both EPIC-055 and EPIC-056
- Changes are low-risk documentation updates (no code modifications)

---

**Epic Status:**
- ⚪ **Planning** - Requirements being defined

**Last Updated:** 2026-01-30 by DevForgeAI
