---
id: STORY-040
title: DevForgeAI Documentation Skill and Command
epic: EPIC-008
sprint: SPRINT-001
status: Ready for Dev
points: 13
priority: High
created: 2025-11-16
updated: 2025-11-16
assignee: AI Agent
tags: [documentation, skill, command, automation, code-analysis]
---

# User Story

**As a** DevForgeAI user
**I want** automated documentation generation integrated into the SDLC workflow
**So that** my projects maintain comprehensive, up-to-date documentation without manual effort

---

## Acceptance Criteria

### AC1: Greenfield Project Documentation Generation
**Given** a greenfield project with completed stories (Dev Complete + QA Approved)
**When** I run `/document STORY-040` or `/document --type=readme`
**Then** the system should:
- Generate README.md with project overview, setup instructions, usage examples
- Create developer guide from technical specifications in story files
- Generate API documentation from implemented endpoints
- Create troubleshooting guide from edge cases and error handling
- All documentation follows coding-standards.md conventions
- Documentation placed according to source-tree.md structure

### AC2: Brownfield Project Documentation Analysis
**Given** an existing project with scattered or missing documentation
**When** I run `/document --mode=brownfield --analyze`
**Then** the system should:
- Perform deep codebase analysis (all source files)
- Discover and consolidate existing documentation fragments
- Identify documentation gaps (missing README, API docs, guides)
- Generate coverage report (what exists, what's missing, what's outdated)
- Provide actionable recommendations for documentation improvement

### AC3: Architecture Diagram Generation
**Given** implemented code with defined architecture patterns
**When** I run `/document --type=architecture`
**Then** the system should:
- Analyze code structure and layer dependencies
- Generate Mermaid flowcharts showing application flow
- Generate sequence diagrams for key user workflows
- Generate architecture diagrams showing component relationships
- Validate diagrams against architecture-constraints.md
- Embed diagrams in appropriate documentation files

### AC4: Incremental Documentation Updates
**Given** existing project documentation and a newly completed story
**When** I run `/document STORY-041` after QA approval
**Then** the system should:
- Detect existing documentation files
- Update affected sections (API endpoints, features, troubleshooting)
- Preserve user-authored content (marked sections)
- Add changelog entry for story implementation
- Update version numbers if applicable
- Maintain documentation consistency

### AC5: Documentation Quality Gate
**Given** a story in QA Approved status
**When** `/release STORY-040` is invoked
**Then** the system should:
- Verify documentation coverage ≥80% (via documentation-writer subagent)
- Check all public APIs have documentation
- Verify README.md exists and is current
- Validate diagrams render correctly
- Block release if documentation threshold not met (quality gate)

### AC6: Template Library and Customization
**Given** the devforgeai-documentation skill with template library
**When** I run `/document --list-templates`
**Then** the system should:
- Display available templates (README, Developer Guide, API Docs, Troubleshooting, Contributing, Changelog)
- Allow template selection via AskUserQuestion
- Support custom templates in .devforgeai/templates/documentation/
- Apply project-specific customizations from coding-standards.md

### AC7: Multi-Format Documentation Export
**Given** generated Markdown documentation
**When** I run `/document --export=html` or `/document --export=pdf`
**Then** the system should:
- Convert Markdown to HTML with styling
- Convert Markdown to PDF with formatting
- Preserve Mermaid diagrams in exported formats
- Include table of contents and navigation
- Apply branding if configured

### AC8: Roadmap Generation from Stories and Epics
**Given** project with defined epics, sprints, and stories
**When** I run `/document --type=roadmap`
**Then** the system should:
- Extract all epics and sprints from .ai_docs/
- Generate roadmap with timeline (completed, in-progress, planned)
- Include milestones and release targets
- Show story dependencies and feature relationships
- Update roadmap as epics/sprints progress

---

## Technical Specification

### Component Architecture

```
User → /document command → devforgeai-documentation skill → Subagents
                                       ↓
                    ┌──────────────────┴──────────────────┐
                    ↓                                     ↓
        documentation-writer subagent        code-analyzer subagent (NEW)
                    ↓                                     ↓
           Generate docs content              Extract code metadata
```

### devforgeai-documentation Skill Structure

**Location:** `.claude/skills/devforgeai-documentation/`

**Phases:**
1. **Phase 0: Mode Detection and Validation**
   - Detect greenfield vs brownfield mode
   - Validate context files exist
   - Determine documentation type (readme, api, architecture, roadmap, all)

2. **Phase 1: Discovery and Analysis**
   - **Greenfield:** Read story files, extract implemented features
   - **Brownfield:** Scan codebase, discover existing docs, identify gaps

3. **Phase 2: Content Generation**
   - Invoke documentation-writer subagent for prose content
   - Invoke code-analyzer subagent (NEW) for code metadata extraction
   - Generate Mermaid diagrams from architecture patterns

4. **Phase 3: Template Application**
   - Load templates from assets/ or custom .devforgeai/templates/
   - Apply project-specific customizations
   - Populate template sections with generated content

5. **Phase 4: Integration and Updates**
   - Detect existing documentation files
   - Merge new content with existing (preserve user sections)
   - Update table of contents, version numbers, changelogs

6. **Phase 5: Validation and Quality Check**
   - Verify documentation coverage ≥80%
   - Validate all public APIs documented
   - Check Mermaid diagrams render
   - Verify framework constraint compliance

7. **Phase 6: Export and Finalization**
   - Write Markdown files to appropriate locations
   - Generate HTML/PDF if requested
   - Update story file with documentation status
   - Return completion summary

### New Subagent: code-analyzer

**Purpose:** Deep codebase analysis to extract documentation metadata

**Location:** `.claude/agents/code-analyzer.md`

**Tools:** Read, Glob, Grep, Bash (for syntax parsing)

**Capabilities:**
- Extract public API signatures (classes, functions, methods)
- Identify architecture patterns (MVC, Clean Architecture, DDD)
- Discover dependencies and layer relationships
- Extract comments and docstrings
- Identify entry points and main workflows
- Generate call graphs for key operations

**Returns:** Structured JSON with code metadata for documentation generation

### /document Slash Command Structure

**Location:** `.claude/commands/document.md`

**Syntax:**
```bash
/document [STORY-ID]                    # Document specific story
/document --type=readme                 # Generate README.md
/document --type=api                    # Generate API documentation
/document --type=architecture           # Generate architecture diagrams
/document --type=roadmap                # Generate project roadmap
/document --type=all                    # Generate all documentation
/document --mode=brownfield --analyze   # Analyze brownfield project
/document --export=html                 # Export to HTML
/document --export=pdf                  # Export to PDF
/document --list-templates              # Show available templates
```

**Workflow (Lean Orchestration):**
- Phase 0: Argument validation and parsing
- Phase 1: Set context markers, invoke devforgeai-documentation skill
- Phase 2: Display results (documentation files created, coverage metrics)

### Template Library Structure

**Location:** `.claude/skills/devforgeai-documentation/assets/templates/`

**Templates:**
- `readme-template.md` - Project overview, setup, usage
- `developer-guide-template.md` - Development workflow, architecture, conventions
- `api-docs-template.md` - API reference, endpoints, schemas
- `troubleshooting-template.md` - Common issues, solutions, debugging
- `contributing-template.md` - Contribution guidelines, PR process
- `changelog-template.md` - Version history, release notes
- `architecture-template.md` - System design, diagrams, decisions

**Template Variables:**
```handlebars
{{project_name}}
{{project_description}}
{{tech_stack}}
{{installation_steps}}
{{usage_examples}}
{{api_endpoints}}
{{architecture_diagram}}
{{troubleshooting_entries}}
```

### Reference Files

**Location:** `.claude/skills/devforgeai-documentation/references/`

**Files:**
1. `documentation-standards.md` (450 lines)
   - Documentation style guide (tone, structure, formatting)
   - Markdown conventions and best practices
   - Mermaid diagram guidelines
   - Code example formatting

2. `greenfield-workflow.md` (380 lines)
   - Story file analysis procedures
   - Content extraction from AC and tech specs
   - Incremental update strategies
   - Version control integration

3. `brownfield-analysis.md` (520 lines)
   - Codebase scanning strategies
   - Pattern recognition for architecture discovery
   - Existing documentation consolidation
   - Gap analysis procedures

4. `diagram-generation-guide.md` (410 lines)
   - Mermaid syntax reference
   - Flowchart generation from code
   - Sequence diagram patterns
   - Architecture diagram conventions

5. `template-customization.md` (290 lines)
   - Custom template creation
   - Variable substitution rules
   - Conditional sections
   - Project-specific overrides

### Data Models

**Documentation Metadata (YAML):**
```yaml
documentation:
  coverage: 85%              # Overall documentation coverage
  last_updated: 2025-11-16
  stories_documented:
    - STORY-001
    - STORY-002
  files:
    - path: README.md
      type: readme
      coverage: 100%
      last_updated: 2025-11-16
    - path: docs/API.md
      type: api
      coverage: 90%
      endpoints_documented: 15
      endpoints_total: 17
    - path: docs/DEVELOPER.md
      type: developer-guide
      coverage: 80%
  diagrams:
    - path: docs/architecture.mmd
      type: architecture
      components: 12
    - path: docs/user-flow.mmd
      type: sequence
      actors: 4
```

**Code Analysis Output (JSON):**
```json
{
  "project_name": "TaskManager",
  "tech_stack": ["Node.js", "Express", "React", "PostgreSQL"],
  "architecture_pattern": "Clean Architecture",
  "layers": {
    "presentation": ["src/controllers/", "src/views/"],
    "application": ["src/use-cases/"],
    "domain": ["src/entities/", "src/repositories/"],
    "infrastructure": ["src/database/", "src/external/"]
  },
  "public_apis": [
    {
      "endpoint": "POST /api/tasks",
      "signature": "createTask(title: string, description: string)",
      "documented": false
    }
  ],
  "entry_points": ["src/index.ts", "src/app.tsx"],
  "dependencies": {
    "external": ["express", "react", "pg"],
    "internal": ["@domain/Task", "@use-cases/CreateTask"]
  }
}
```

### Integration with SDLC Workflow

**Updated Complete Development Lifecycle:**

```
1. IDEATION (/ideate)
   ↓
2. ARCHITECTURE (/create-context)
   ↓
3. EPIC PLANNING (/create-epic)
   ↓
4. SPRINT PLANNING (/create-sprint)
   ↓
5. STORY CREATION (/create-story)
   ↓
6. UI GENERATION (/create-ui) [OPTIONAL]
   ↓
7. DEVELOPMENT (/dev)
   ↓
8. QA VALIDATION (/qa)
   ↓
9. DOCUMENTATION (/document) ← NEW PHASE
   ↓ Quality Gate: Documentation coverage ≥80%
   ↓
10. RELEASE (/release)
```

**Story Status Transitions:**

```
QA Approved → Documentation In Progress → Documentation Complete → Releasing
```

**Quality Gate Enhancement:**

Before `/release`, verify:
- ✅ Tests pass (existing gate)
- ✅ Coverage ≥95%/85%/80% (existing gate)
- ✅ **Documentation coverage ≥80% (NEW GATE)**
- ✅ **README.md exists and current (NEW GATE)**
- ✅ **Public APIs documented (NEW GATE)**

---

## Non-Functional Requirements

### Performance
- **Greenfield documentation generation:** <2 minutes for average story
- **Brownfield analysis:** <10 minutes for codebase with 500 files
- **Diagram generation:** <30 seconds per Mermaid diagram
- **Incremental update:** <1 minute for single file update

### Scalability
- Support projects with up to 5,000 source files (brownfield)
- Handle documentation sets up to 100 files
- Generate diagrams with up to 50 components

### Documentation Quality
- 80% minimum coverage for public APIs
- 100% of stories have associated documentation
- Zero broken links in generated documentation
- All Mermaid diagrams must render without errors

### Usability
- Single command invocation for most common use cases
- Interactive mode for template customization (AskUserQuestion)
- Clear error messages if documentation generation fails
- Preview mode before committing documentation changes

---

## Edge Cases and Error Handling

### Edge Case 1: No Implemented Code Found
**Scenario:** `/document STORY-040` but story has no code implementation
**Handling:**
- Detect empty implementation via code-analyzer
- Warning: "Story STORY-040 has no code implementation. Documentation cannot be generated."
- Offer to generate placeholder documentation from story AC
- Ask user: "Generate placeholder docs from acceptance criteria?"

### Edge Case 2: Conflicting Existing Documentation
**Scenario:** User-authored README.md conflicts with generated content
**Handling:**
- Detect user-authored sections (via special markers or git blame)
- Preserve user sections, update only auto-generated sections
- Create backup: `README.md.backup-{timestamp}`
- Ask user: "Existing README.md found. Merge or replace?"

### Edge Case 3: Incomplete Architecture Discovery
**Scenario:** Brownfield project has non-standard architecture
**Handling:**
- code-analyzer returns "unknown" architecture pattern
- Generate basic documentation without architecture assumptions
- Ask user: "Architecture pattern unclear. Select pattern (MVC/Clean/DDD/Custom)?"
- Use selected pattern for diagram generation

### Edge Case 4: Missing Context Files
**Scenario:** Documentation requested before `/create-context` run
**Handling:**
- Detect missing .devforgeai/context/ files
- HALT with error: "Context files required. Run /create-context first."
- Prevent documentation generation without framework constraints

### Edge Case 5: Export Format Failure
**Scenario:** `/document --export=pdf` but PDF generation fails
**Handling:**
- Attempt Markdown to HTML conversion first
- If HTML succeeds, try HTML to PDF (fallback)
- If all fail, return Markdown and error message
- Suggest: "Install wkhtmltopdf for PDF export support"

### Edge Case 6: Diagram Rendering Error
**Scenario:** Generated Mermaid diagram has syntax errors
**Handling:**
- Validate Mermaid syntax before writing file
- If invalid, attempt auto-fix (common issues: missing semicolons, quotes)
- If auto-fix fails, log error and skip diagram
- Continue with text-only documentation
- Report: "Diagram generation failed. Manual review needed."

### Edge Case 7: Documentation Drift (Outdated Docs)
**Scenario:** Code changed but documentation not updated
**Handling:**
- Compare code implementation dates with doc last_updated dates
- Flag outdated documentation (>30 days drift)
- Regenerate outdated sections automatically
- Add changelog entry: "Updated documentation to match current implementation"

---

## Definition of Done

### Implementation
- [x] `devforgeai-documentation` skill created in `.claude/skills/devforgeai-documentation/SKILL.md`
- [x] `/document` slash command created in `.claude/commands/document.md`
- [x] `code-analyzer` subagent created in `.claude/agents/code-analyzer.md`
- [x] 7 documentation templates created in `assets/templates/`
- [x] 5 reference files created (documentation-standards, greenfield-workflow, brownfield-analysis, diagram-generation-guide, template-customization)

### Testing
- [ ] Unit tests: Template loading, variable substitution, diagram validation
- [ ] Integration tests: Full greenfield workflow (story → documentation)
- [ ] Integration tests: Full brownfield workflow (codebase analysis → docs)
- [ ] Integration tests: Incremental update workflow
- [ ] Regression tests: Existing documentation preserved during updates
- [ ] Performance tests: <2 min greenfield, <10 min brownfield

### Documentation
- [ ] `.claude/memory/documentation-guide.md` created (user-facing guide)
- [ ] CLAUDE.md updated with documentation phase in SDLC
- [ ] `.claude/memory/commands-reference.md` updated with `/document` entry
- [ ] `.claude/memory/subagents-reference.md` updated with `code-analyzer` entry

### Framework Integration
- [ ] Quality gate added to `/release` command (documentation coverage ≥80%)
- [ ] Story status workflow updated (Documentation In Progress → Documentation Complete)
- [ ] Orchestration skill updated to invoke documentation after QA
- [ ] Template library accessible via skill

### Validation
- [ ] Greenfield project: Generate README.md from 3 test stories
- [ ] Brownfield project: Analyze sample codebase (Node.js project with 100 files)
- [ ] Architecture diagrams: Generate Mermaid flowchart and sequence diagram
- [ ] Export: Convert Markdown to HTML successfully
- [ ] Quality gate: Release blocked when documentation coverage <80%
- [ ] All 8 acceptance criteria validated with real scenarios

---

## Story Workflow History

### 2025-11-16 16:30:00 - Status: Ready for Dev
- Added to SPRINT-001: Documentation Skill - Sprint 1
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 13 points (optimal for focused implementation)
- Priority in sprint: [1 of 1]
- Epic updated: EPIC-007 → EPIC-008 (DevForgeAI Documentation System)

### 2025-11-16 - Story Created
- Status: Backlog
- Epic: EPIC-007 (Lean Orchestration Compliance)
- Points: 13 (Large - new skill, command, subagent, templates)
- Priority: High (critical SDLC gap)
- Assignee: AI Agent

---

## Dependencies

### Prerequisite Stories
- None (can be implemented independently)

### Context File Dependencies
- `coding-standards.md` - Documentation style conventions
- `source-tree.md` - Documentation file placement rules
- `tech-stack.md` - Technology references in documentation

### External Tool Dependencies
- **Mermaid CLI** (optional) - For diagram rendering validation
- **wkhtmltopdf** (optional) - For PDF export
- **Pandoc** (optional) - For advanced export formats

---

## Related Stories

### Follow-Up Stories (Potential)
- STORY-041: Documentation versioning and changelog automation
- STORY-042: Multi-language documentation support (i18n)
- STORY-043: Interactive documentation with live code examples
- STORY-044: Documentation search and indexing
- STORY-045: Documentation analytics (coverage trends, usage)

### Related Existing Features
- `/qa` command - Documentation coverage validation integrated here
- `/release` command - Documentation quality gate integrated here
- `documentation-writer` subagent - Reused for prose generation
- `devforgeai-orchestration` skill - Updated to include documentation phase

---

## Notes

### Design Decisions

**Why separate `/document` command instead of auto-generating in `/qa`?**
- User control: Documentation may need manual review before generation
- Flexibility: Different documentation types for different needs
- Performance: Brownfield analysis is expensive, shouldn't block QA
- Separation of concerns: QA validates code, documentation validates communication

**Why new `code-analyzer` subagent instead of using existing subagents?**
- Specialized task: Deep codebase analysis is distinct from code review
- Reusability: code-analyzer useful for other features (refactoring, metrics)
- Token efficiency: Isolated context for heavy analysis work

**Why quality gate at 80% instead of 100%?**
- Pragmatic: Some code (internal utilities) may not need public documentation
- Flexibility: Allows exceptions for generated code, third-party integrations
- Consistency: Matches existing coverage thresholds (95%/85%/80%)

### Implementation Approach

**Phase 1: Greenfield MVP (Stories 1-3)**
1. Create skill, command, templates (basic README only)
2. Implement story-based documentation generation
3. Test with 3 sample stories

**Phase 2: Brownfield Analysis (Stories 4-5)**
4. Create code-analyzer subagent
5. Implement codebase scanning and gap analysis
6. Test with sample Node.js project

**Phase 3: Advanced Features (Stories 6-8)**
7. Add diagram generation (Mermaid)
8. Add export formats (HTML, PDF)
9. Integrate quality gates into `/release`

**Estimated Total Effort:** 13 story points (~26-39 hours implementation + testing)

---

## Acceptance Criteria Validation Checklist

Before marking this story as "Dev Complete":

**AC1: Greenfield Documentation**
- [ ] README.md generated from story with all sections
- [ ] Developer guide created from technical specifications
- [ ] API documentation generated from implemented endpoints
- [ ] Troubleshooting guide created from edge cases
- [ ] All files follow coding-standards.md
- [ ] Files placed per source-tree.md

**AC2: Brownfield Analysis**
- [ ] Codebase analysis completes for 100-file project
- [ ] Existing documentation discovered and consolidated
- [ ] Documentation gaps identified (missing, outdated)
- [ ] Coverage report generated with recommendations

**AC3: Architecture Diagrams**
- [ ] Mermaid flowcharts generated from code
- [ ] Sequence diagrams created for key workflows
- [ ] Architecture diagrams show component relationships
- [ ] Diagrams validated against architecture-constraints.md

**AC4: Incremental Updates**
- [ ] Existing documentation detected and preserved
- [ ] Only affected sections updated
- [ ] User-authored content not overwritten
- [ ] Changelog entry added for new story

**AC5: Documentation Quality Gate**
- [ ] Coverage calculation accurate (≥80% threshold)
- [ ] Public APIs verified as documented
- [ ] README.md existence checked
- [ ] Release blocked if threshold not met

**AC6: Template Library**
- [ ] All 7 templates available and functional
- [ ] Template selection via AskUserQuestion works
- [ ] Custom templates in .devforgeai/templates/ supported
- [ ] Project-specific customizations applied

**AC7: Multi-Format Export**
- [ ] Markdown to HTML conversion works
- [ ] Markdown to PDF conversion works (if dependencies installed)
- [ ] Mermaid diagrams render in HTML/PDF
- [ ] Table of contents generated correctly

**AC8: Roadmap Generation**
- [ ] Epics and sprints extracted from .ai_docs/
- [ ] Timeline shows completed, in-progress, planned items
- [ ] Milestones and dependencies visualized
- [ ] Roadmap updates as project progresses

---

**End of Story**
