---
id: STORY-126
title: Story Type Detection & Phase Skipping
type: feature
status: Backlog
priority: MEDIUM
story-points: 5
epic: EPIC-025
sprint: null
created: 2025-12-20
assignee: null
depends-on: [STORY-125]
---

# STORY-126: Story Type Detection & Phase Skipping

## User Story

**As a** DevForgeAI developer
**I want** story type detection with automatic phase skipping
**So that** documentation stories don't run unnecessary integration tests and bugfix stories skip refactoring

## Background

The current TDD workflow treats all stories uniformly, requiring all phases regardless of story type. This creates unnecessary work:
- Documentation stories run integration tests for code that doesn't exist
- Bugfix stories go through refactoring when minimal changes are preferred
- Refactor stories write new tests when tests already exist

**Observation from STORY-114:** As a documentation-only story, it executed performance tests that validated documented claims rather than runtime behavior.

## Acceptance Criteria

### AC#1: Story Frontmatter Supports Type Field
**Given** a story file frontmatter
**When** the `type` field is set
**Then** it accepts one of: `feature`, `documentation`, `bugfix`, `refactor`
**And** invalid types cause validation error

### AC#2: /create-story Prompts for Story Type
**Given** a developer runs `/create-story`
**When** the interactive prompts are displayed
**Then** one prompt asks for story type
**And** the 4 types are presented with descriptions:
- `feature` - Full TDD workflow (default)
- `documentation` - Skip integration testing
- `bugfix` - Skip refactoring phase
- `refactor` - Skip writing new tests

### AC#3: /dev Skips Appropriate Phases
**Given** a story with `type: documentation`
**When** `/dev STORY-XXX` runs
**Then** Phase 05 Integration is skipped
**And** a log message explains: "Skipping Phase 05: Story type 'documentation' does not require integration tests"

### AC#4: All Story Types Skip Correctly
**Given** stories of each type
**When** `/dev` runs for each
**Then** phase skipping follows this matrix:

| Type | Skipped Phases | Rationale |
|------|----------------|-----------|
| `feature` | None | Full TDD workflow |
| `documentation` | Phase 05 Integration | No runtime code |
| `bugfix` | Phase 04 Refactor | Minimal changes |
| `refactor` | Phase 02 Red | Tests exist |

### AC#5: Default Type is Feature (Backward Compatible)
**Given** a story file without `type` field
**When** `/dev` runs
**Then** it defaults to `type: feature`
**And** no phases are skipped
**And** no warnings are displayed about missing type

## Technical Specification

### Files to Modify
| File | Changes |
|------|---------|
| `.claude/skills/devforgeai-story-creation/SKILL.md` | Add type field to story template, add prompt for type selection |
| `.claude/skills/devforgeai-development/SKILL.md` | Add phase-skipping logic based on type |
| `devforgeai/specs/context/coding-standards.md` | Document story types |

### Story Type Enum
```yaml
# Valid story types
type: feature        # Default - all phases required
type: documentation  # Skip Phase 05 Integration
type: bugfix         # Skip Phase 04 Refactor
type: refactor       # Skip Phase 02 Red
```

### Phase Skipping Logic (Claude Code Terminal)
```markdown
## Phase Skip Decision Matrix

| Story Type | Skip Phases |
|------------|-------------|
| feature | (none) |
| documentation | Phase 05 Integration |
| bugfix | Phase 04 Refactor |
| refactor | Phase 02 Red |

## Implementation in SKILL.md

1. Read story frontmatter:
   Read(file_path="devforgeai/specs/Stories/STORY-XXX.story.md")
   Extract: type field from YAML frontmatter

2. Check if current phase should be skipped:
   IF story_type == "documentation" AND phase == "Phase 05 Integration":
     Log: "Skipping Phase 05: Story type 'documentation' does not require integration tests"
     SKIP phase

3. Default behavior:
   IF type field missing OR type == "feature":
     Execute ALL phases (no skipping)
```

### Story Template Update
```yaml
---
id: STORY-XXX
title: {title}
type: feature  # Options: feature, documentation, bugfix, refactor
status: Backlog
# ... rest of frontmatter
---
```

## Test Strategy

### Test Files Location
`devforgeai/tests/STORY-126/`

### Test Cases
| Test ID | Description | Type |
|---------|-------------|------|
| test-ac1-type-validation.sh | Verify frontmatter accepts valid types, rejects invalid | Bash |
| test-ac2-create-story-prompt.sh | Verify /create-story prompts for type | Manual |
| test-ac3-phase-skip-docs.sh | Verify documentation type skips Phase 05 | Bash |
| test-ac4-phase-skip-matrix.sh | Verify all 4 types skip correct phases | Bash |
| test-ac5-backward-compat.sh | Verify stories without type default to feature | Bash |

## Definition of Done

### Implementation
- [ ] Story frontmatter schema updated to include `type` field
- [ ] Type enum validation added (feature, documentation, bugfix, refactor)
- [ ] /create-story skill prompts for story type
- [ ] /dev skill includes phase-skipping logic
- [ ] Phase skip logging implemented with clear messages
- [ ] coding-standards.md updated with story types documentation

### Quality
- [ ] All 5 test cases pass
- [ ] Existing stories without type field work correctly
- [ ] Phase skip messages are clear and actionable

### Documentation
- [ ] Story types documented in coding-standards.md
- [ ] Phase skip rationale documented for each type

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Story type enum may need expansion | Start with 4 types, add via ADR if needed |
| Phase skipping causes test gaps | Document when to override default type |
| Developers forget to set type | Default to `feature` (all phases) for safety |

## Out of Scope

- Adding new story types beyond the 4 defined
- Automatic story type inference (aspirational - requires ML)
- Changing existing story files to add type field
