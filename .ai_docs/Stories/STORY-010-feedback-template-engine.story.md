---
id: STORY-010
title: Feedback Template Engine
epic: EPIC-003
sprint: Sprint-1
status: Backlog
points: 10
priority: High
assigned_to: TBD
created: 2025-11-07
---

# Story: Feedback Template Engine

## User Story

**As a** framework maintainer,
**I want** standardized feedback templates that adapt to operation context,
**so that** I can aggregate insights across users and provide consistent feedback structure regardless of operation type.

## Acceptance Criteria

### 1. [x] Template Definitions for Each Operation Type
**Given** feedback is collected for different operation types (command, skill, subagent)
**When** the template engine selects an appropriate template
**Then** operation-specific templates exist in `.claude/skills/devforgeai-feedback/templates/`
**And** templates include: `command-template.md`, `skill-template.md`, `subagent-template.md`
**And** each template defines required sections (What Went Well, What Went Poorly, Suggestions, Context)

---

### 2. [x] Success/Failure Template Variations
**Given** an operation completes with different statuses (passed, failed, partial)
**When** the template engine renders feedback
**Then** templates adapt sections based on status (success templates emphasize optimization, failure templates emphasize investigation)
**And** failure templates include additional sections: Root Cause Analysis, Blockers Encountered
**And** partial templates combine success + investigation sections

---

### 3. [x] Automatic Field Mapping
**Given** user provides responses during retrospective conversation
**When** responses are mapped to template fields
**Then** conversation responses automatically populate template sections without manual intervention
**And** mapping rules defined in template metadata (e.g., "What went well?" → ## What Went Well section)
**And** unmapped responses stored in ## Additional Feedback section

---

### 4. [x] Template Rendering with Metadata
**Given** feedback data is ready for template rendering
**When** the template engine generates the final document
**Then** YAML frontmatter includes: operation, type, status, timestamp, story-id (if applicable)
**And** markdown content follows template structure
**And** rendered template saved to `.devforgeai/feedback/{operation-type}/{timestamp}-retrospective.md`

---

### 5. [x] YAML Frontmatter + Markdown Content Format
**Given** a template is rendered
**When** viewing the output file
**Then** file starts with YAML frontmatter delimited by `---`
**And** frontmatter contains structured metadata (operation, type, status, timestamp, story-id)
**And** markdown content follows frontmatter with sections defined by `##` headers
**And** format is consistent with DevForgeAI story/epic format standards

---

### 6. [x] Context-Aware Template Selection
**Given** multiple template variations exist
**When** determining which template to use
**Then** selection logic considers: operation type (command/skill/subagent), success status (passed/failed/partial), user preferences (from config)
**And** default to context-aware mode (operation-specific templates)
**And** fallback to generic template if operation-specific template missing

## Technical Specification

### Data Models

#### Template Definition Schema
```yaml
---
template-id: command-success
operation-type: command
success-status: passed
version: "1.0"
---

# Template: Command Success Retrospective

## Metadata Extraction
- operation: {operation_name}  # e.g., "/dev STORY-042"
- type: command
- status: success
- timestamp: {ISO 8601}
- story-id: {STORY-XXX or null}

## Field Mappings
what-went-well:
  question-id: "cmd_success_01"
  section: "## What Went Well"

what-went-poorly:
  question-id: "cmd_success_02"
  section: "## What Went Poorly"

suggestions:
  question-id: "cmd_success_03"
  section: "## Suggestions for Improvement"

## Required Sections
- What Went Well
- What Went Poorly
- Suggestions for Improvement
- Context (auto-populated)
- User Sentiment (auto-calculated)
- Actionable Insights (auto-extracted)
```

#### Rendered Template Output
```markdown
---
operation: /dev STORY-042
type: command
status: success
timestamp: 2025-11-07T10:30:00Z
story-id: STORY-042
---

# Retrospective: /dev STORY-042

## What Went Well
- TDD workflow was clear and well-structured
- Test-automator subagent generated comprehensive tests
- Coverage threshold (95%) achieved without issues

## What Went Poorly
- Initial git setup was confusing (missing context about repository initialization)
- Deferral challenge checkpoint asked questions multiple times

## Suggestions for Improvement
- Provide clearer git initialization guidance at start of /dev
- Deduplicate deferral questions if user already answered in previous session

## Context
- **TodoWrite Status:** 4 of 4 tasks completed
- **Errors Encountered:** No
- **Performance Metrics:** Execution time: 12m 34s, Token usage: 87,500

## User Sentiment
Satisfied (4/5)

## Actionable Insights
1. **Git guidance:** Provide clearer context about repository initialization [Priority: Medium]
2. **Deduplication:** Avoid repeating deferral questions in same session [Priority: High]
```

### Template Engine Algorithm

```python
def select_template(operation_type, success_status, user_config):
    """Select appropriate template based on context."""

    # Priority 1: User custom template (if defined)
    if user_config.templates.custom and operation_type in user_config.templates.custom:
        return load_custom_template(operation_type, success_status)

    # Priority 2: Operation-specific + status-specific template
    template_name = f"{operation_type}-{success_status}"  # e.g., "command-passed"
    template_path = f".claude/skills/devforgeai-feedback/templates/{template_name}.md"

    if file_exists(template_path):
        return load_template(template_path)

    # Priority 3: Operation-specific template (any status)
    generic_template_name = f"{operation_type}-generic"
    generic_path = f".claude/skills/devforgeai-feedback/templates/{generic_template_name}.md"

    if file_exists(generic_path):
        return load_template(generic_path)

    # Priority 4: Fallback to universal generic template
    return load_template(".claude/skills/devforgeai-feedback/templates/generic-template.md")


def render_template(template, conversation_responses, metadata):
    """Render template with user responses and metadata."""

    # Extract field mappings from template
    field_mappings = template.field_mappings

    # Build content sections
    sections = {}
    for field_name, mapping in field_mappings.items():
        question_id = mapping['question_id']
        section_header = mapping['section']

        # Find response for this question
        response = conversation_responses.get(question_id, "No response provided")

        sections[section_header] = response

    # Auto-populate Context section
    sections["## Context"] = generate_context_section(metadata)

    # Auto-calculate User Sentiment
    sections["## User Sentiment"] = calculate_sentiment(conversation_responses)

    # Auto-extract Actionable Insights
    sections["## Actionable Insights"] = extract_insights(sections["## Suggestions for Improvement"])

    # Assemble final document
    frontmatter = generate_frontmatter(metadata)
    markdown_content = assemble_sections(sections)

    return f"{frontmatter}\n\n{markdown_content}"
```

### API Endpoints

None - Internal template rendering engine

### Business Rules

1. **Template Selection Priority:**
   - Custom templates (user-defined) override default templates
   - Operation-specific templates preferred over generic
   - Status-specific templates (passed/failed/partial) used when available
   - Fallback to generic template if no match found

2. **Field Mapping Rules:**
   - Each template defines question_id → section_header mappings
   - Unmapped responses collected in "Additional Feedback" section
   - Missing responses show "No response provided" (not blank)

3. **Auto-Population Rules:**
   - Context section: Auto-generated from TodoWrite status, errors, performance metrics
   - User Sentiment: Calculated from satisfaction rating question (1-5 scale)
   - Actionable Insights: Extracted from suggestions using keyword patterns ("should", "could", "needs")

4. **Template Versioning:**
   - Templates include version field (e.g., "1.0")
   - Rendered feedback includes template version used
   - Version mismatches logged (template updated since config created)

### Dependencies

- **Question Bank:** EPIC-002 Feature 1.2 (question IDs referenced in field mappings)
- **Configuration:** EPIC-003 Feature 2.2 (user preferences for template selection)
- **File System:** `.claude/skills/devforgeai-feedback/templates/` directory

## Edge Cases

### 1. Template File Missing
**Scenario:** Operation-specific template doesn't exist (e.g., new operation type added)
**Expected:** Fall back to generic template, log warning
**Handling:** Check file existence before loading, use fallback chain

### 2. Malformed Template YAML
**Scenario:** Template file has invalid YAML frontmatter
**Expected:** Log error, skip malformed template, use next in fallback chain
**Handling:** YAML parsing with exception handling

### 3. Question ID Not in Conversation Responses
**Scenario:** Template expects question_id "cmd_success_05" but user skipped that question
**Expected:** Show "No response provided" in that section
**Handling:** Default value for missing responses

### 4. User Provides Response Not Mapped to Any Section
**Scenario:** User answers optional question not defined in template field mappings
**Expected:** Collect in "Additional Feedback" section
**Handling:** Track unmapped responses separately

### 5. Multiple Operations Same Timestamp
**Scenario:** Two operations complete within same second (same timestamp)
**Expected:** Append unique identifier to filename (timestamp + UUID)
**Handling:** Filename format: `{timestamp}-{uuid}-retrospective.md`

## Data Validation Rules

1. **Template ID Validation:**
   - Format: `{operation-type}-{status}` (e.g., "command-passed")
   - Operation type: command|skill|subagent|workflow
   - Status: passed|failed|partial|generic

2. **Field Mapping Validation:**
   - question_id must exist in question bank
   - section header must start with "##"
   - Each mapping must have question_id + section

3. **Rendered Output Validation:**
   - YAML frontmatter must be valid YAML
   - Required frontmatter fields: operation, type, status, timestamp
   - Markdown sections must use ## headers (level 2)

4. **File Path Validation:**
   - Templates stored in `.claude/skills/devforgeai-feedback/templates/`
   - Rendered feedback stored in `.devforgeai/feedback/{operation-type}/`
   - Filenames: `{timestamp}-retrospective.md` (ISO 8601 timestamp)

## Non-Functional Requirements

### Performance
- Template selection: <100ms
- Template rendering: <500ms
- File write (rendered template): <200ms
- Total latency: <1000ms (P95)

### Scalability
- Support 50+ template definitions without performance degradation
- Support 10,000+ rendered feedback files per project
- Template size: <50KB each (keep templates concise)

### Maintainability
- Template format documented with examples
- Field mapping rules clearly defined
- Template versioning enables updates without breaking existing feedback

### Portability
- Rendered feedback files portable across projects (standard Markdown + YAML)
- No project-specific paths or identifiers in templates
- Templates framework-agnostic (no language-specific examples)

## Definition of Done

### Implementation
- [ ] Template definitions for command, skill, subagent operation types
- [ ] Success/failure template variations (passed, failed, partial)
- [ ] Field mapping logic (question_id → section_header)
- [ ] Template selection algorithm (priority chain)
- [ ] Template rendering engine (YAML frontmatter + Markdown content)
- [ ] Auto-population logic (Context, User Sentiment, Actionable Insights)
- [ ] Fallback to generic template if specific template missing
- [ ] Rendered templates saved to `.devforgeai/feedback/{operation-type}/`

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (missing template, malformed YAML, missing question ID, unmapped responses, timestamp collision)
- [ ] Data validation enforced (4 validation categories)
- [ ] NFRs met (latency <1000ms P95, scalability 50+ templates, portability verified)
- [ ] Code coverage >95% for template engine

### Testing
- [ ] Unit tests: Template selection (20+ cases)
- [ ] Unit tests: Field mapping (15+ cases)
- [ ] Unit tests: Template rendering (25+ cases)
- [ ] Integration tests: End-to-end (conversation → template → file)
- [ ] E2E test: Command success (standard template)
- [ ] E2E test: Skill failure (failure-specific sections)
- [ ] E2E test: Missing template (fallback to generic)
- [ ] E2E test: Unmapped response (additional feedback section)

### Documentation
- [ ] Template format specification
- [ ] Field mapping guide for creating new templates
- [ ] Template examples for all operation types
- [ ] User guide: How to customize templates (link to Feature 2.3)

### Release Readiness
- [ ] Default templates for command, skill, subagent
- [ ] Generic fallback template
- [ ] Template directory structure created
- [ ] File write permissions validated
- [ ] Rendered feedback readable by all DevForgeAI tools

## Workflow History

- **2025-11-07:** Story created from EPIC-003 Feature 2.1 (batch mode)
