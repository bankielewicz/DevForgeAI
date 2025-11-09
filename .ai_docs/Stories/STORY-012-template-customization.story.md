---
id: STORY-012
title: Template Customization
epic: EPIC-003
sprint: Sprint-1
status: Backlog
points: 10
priority: High
assigned_to: TBD
created: 2025-11-07
---

# Story: Template Customization

## User Story

**As a** power user or team lead,
**I want to** define custom template fields, inject team-specific questions, and extend default templates with custom values,
**so that** I can tailor the template system to my team's specific needs without losing access to the framework's default templates.

## Acceptance Criteria

### 1. [x] Power Users Can Define and Manage Custom Template Fields
**Given** a power user is authenticated and has access to the template customization interface
**When** the user creates a new custom field with name "Project phase", type "select", and options ["Planning", "Development", "Testing", "Release"]
**Then** the custom field is persisted to the custom template configuration
**And** the field is immediately available for use in new story templates
**And** the custom field can be edited to modify options or constraints
**And** the custom field can be deleted with confirmation (no in-use stories affected)

---

### 2. [x] Team Leads Can Inject Team-Specific Questions
**Given** a team lead has team configuration access
**When** the team lead adds a custom question "Did you follow our coding conventions?" with expected answer "Yes (link to standards)"
**Then** the question is stored in the team configuration
**And** the question appears in the story creation workflow for all team members
**And** the question appears AFTER default framework questions (custom questions supplement, not replace)
**And** the question can be marked optional or required
**And** team members' answers are captured in the story workflow history

---

### 3. [x] Custom Templates Extend Default Templates via Inheritance
**Given** a custom template "Our Standard Story" is created
**When** the custom template includes inherited sections from the default template (User Story, Acceptance Criteria, Technical Spec)
**Then** the custom template inherits all required sections from the default
**And** custom fields are added as NEW sections (not replacing defaults)
**And** the custom template renders with default sections first, custom sections after
**And** when default template is updated (new framework version), inherited sections update automatically in custom templates
**And** custom template can be reverted to defaults with one action (restores inheritance to current defaults)

---

### 4. [x] Custom Fields Validated with Multiple Data Types Support
**Given** a power user defines a custom field with type "date", name "Review Date", and constraint "required"
**When** a user attempts to create a story using the custom template
**Then** the custom field validation rules are enforced
**And** invalid values (e.g., invalid date format) produce clear error messages
**And** the system supports field types: text (string), select (dropdown), date, number, checkbox, textarea
**And** custom fields can have min/max constraints (for numbers), length constraints (for strings)
**And** custom fields can be marked required or optional

---

### 5. [x] Custom Templates Can Be Shared Within Teams
**Given** a custom template "Backend Story Template" is created by a power user
**When** the user clicks "Share with Team" and selects visibility "Team: Development"
**Then** all team members see the custom template in their template library
**And** team members can use the template without ability to modify (read-only)
**And** the original creator can modify/delete the shared template (all instances updated)
**And** team members can create their own variants by "Copying" the shared template
**And** the custom template copy is independent (changes to original don't affect copies)

---

### 6. [x] Custom Template Data Persists Across Framework Versions
**Given** a custom template was created in framework v1.0 with custom fields and inherited sections
**When** the framework is upgraded to v2.0 with updated default templates
**Then** the custom template still exists with all custom data intact
**And** the inherited sections automatically reflect v2.0 defaults (if compatible)
**And** custom fields are preserved unless they conflict with new framework changes
**And** if conflicts occur, the user is notified with migration options (keep old or adopt new)

## Technical Specification

### API Contracts

#### POST /api/templates/custom-fields
**Request:**
```json
{
  "name": "Project phase",
  "type": "select",
  "description": "Current phase of the project",
  "required": true,
  "field_order": 5,
  "options": [
    { "value": "planning", "label": "Planning" },
    { "value": "development", "label": "Development" },
    { "value": "testing", "label": "Testing" },
    { "value": "release", "label": "Release" }
  ],
  "visibility": "team|personal"
}
```

**Response (201 Created):**
```json
{
  "field_id": "uuid-v4",
  "name": "Project phase",
  "type": "select",
  "created_at": "2025-11-07T10:30:00Z",
  "created_by": "user-uuid",
  "team_id": "team-uuid"
}
```

#### POST /api/templates/team-questions
**Request:**
```json
{
  "question": "Did you follow our coding conventions?",
  "expected_answer": "Yes (link to standards)",
  "required": true,
  "order": 1,
  "team_id": "team-uuid"
}
```

**Response (201 Created):**
```json
{
  "question_id": "uuid-v4",
  "question": "Did you follow our coding conventions?",
  "required": true,
  "created_at": "2025-11-07T10:30:00Z",
  "created_by": "user-uuid"
}
```

#### POST /api/templates/custom
**Request:**
```json
{
  "name": "Our Standard Story",
  "description": "Custom story template with team fields",
  "inherit_sections": ["User Story", "Acceptance Criteria", "Technical Spec"],
  "custom_field_ids": ["field-uuid-1", "field-uuid-2"],
  "custom_question_ids": ["question-uuid-1"],
  "team_id": "team-uuid|null"
}
```

**Response (201 Created):**
```json
{
  "template_id": "uuid-v4",
  "name": "Our Standard Story",
  "version": 1,
  "framework_version": "1.0.1",
  "created_at": "2025-11-07T10:30:00Z",
  "inheritance_status": "active"
}
```

### Data Models

#### CustomTemplateField
- field_id (UUID, primary key)
- field_name (String, 3-100 chars, unique per team)
- field_type (Enum: text|select|date|number|checkbox|textarea)
- field_description (String, max 500 chars, optional)
- is_required (Boolean, default false)
- field_order (Integer, default last)
- validation_rules (JSON, optional)
- options (JSON Array, required for select type)
- visibility (Enum: personal|team)
- team_id (UUID, conditional)
- created_by (UUID)
- created_at (DateTime)
- updated_at (DateTime)

#### TeamQuestion
- question_id (UUID, primary key)
- question_text (String, 10-500 chars)
- expected_answer (String, max 1000 chars, optional)
- is_required (Boolean, default false)
- question_order (Integer, optional)
- team_id (UUID)
- created_by (UUID)
- created_at (DateTime)
- updated_at (DateTime)

#### CustomTemplate
- template_id (UUID, primary key)
- template_name (String, 5-100 chars, unique per team)
- description (String, max 500 chars, optional)
- inherited_sections (JSON Array)
- custom_field_ids (JSON Array, optional)
- custom_question_ids (JSON Array, optional)
- framework_version (String)
- inheritance_status (Enum: active|deprecated|migrated)
- inheritance_updated_at (DateTime, optional)
- team_id (UUID, optional)
- visibility (Enum: personal|team|read-only)
- created_by (UUID)
- created_at (DateTime)
- updated_at (DateTime)

### Business Rules

1. **Field Name Uniqueness:** Custom field names unique within team/personal scope
2. **Field Type Immutability:** Type cannot change after creation (delete + recreate required)
3. **Required Field Enforcement:** Required custom fields block "Ready for Dev" status
4. **Inheritance Preservation:** Core framework sections always inherited (cannot remove)
5. **Inheritance Auto-Update:** Framework upgrades auto-update inherited sections
6. **Team Scope:** Team visibility = accessible to all members, modifiable by creator/admins only
7. **Template Sharing:** Shared templates read-only for team, copyable to personal
8. **Question Ordering:** Custom questions appear AFTER framework questions
9. **Data Persistence:** Custom values stored in story YAML frontmatter
10. **Backward Compatibility:** Stories valid even if template deleted later

### Dependencies

- Database: PostgreSQL or equivalent (relational DB for entities)
- YAML Parser: PyYAML for story file updates
- JSON Schema: For custom field validation
- Authentication: User/team identity system

## Edge Cases

### 1. Custom Field Name Conflicts with Inherited Section
**Scenario:** User tries to create custom field "User Story" (conflicts with framework default)
**Expected:** System prevents creation, error: "Field name conflicts with inherited section. Choose different name."
**Handling:** Validate field name against inherited section names

### 2. User Deletes Custom Field In Use by 15 Stories
**Scenario:** Custom field used in active stories
**Expected:** System prevents deletion, shows warning with affected stories list
**Handling:** Check field usage before deletion, require migration or confirmation

### 3. Framework Upgrade Adds New Required Section
**Scenario:** Framework v2.0 adds "Security Considerations" required section
**Expected:** Custom templates auto-update, user notified, side-by-side comparison shown
**Handling:** Auto-update with notification + approval

### 4. Custom Template Accessed with Framework Version Mismatch
**Scenario:** Template created in v1.0, accessed in v1.5
**Expected:** Auto-update inherited sections, update timestamp
**Handling:** Version detection + auto-update

### 5. Team Member Attempts to Modify Shared Template
**Scenario:** Non-creator accesses team template
**Expected:** Read-only UI, modification disabled, tooltip explains
**Handling:** Permission check on template access

### 6. Export Custom Template to Different Team
**Scenario:** User exports template to another team
**Expected:** Copy with new team_id, regenerated UUIDs, original unaffected
**Handling:** Deep copy with ID regeneration

### 7. Custom Select Field Has Empty Options List
**Scenario:** Database corruption clears options array
**Expected:** System detects invalid state, prevents usage, alerts owner
**Handling:** Validation on retrieval

### 8. Circular Dependency in Custom Field Values
**Scenario:** Field A references Field B, Field B references Field A
**Expected:** System prevents assignment, error message
**Handling:** Dependency graph validation

## Data Validation Rules

1. **Field Name:** 3-100 chars, unique per team, no reserved words
2. **Field Type:** Must be: text|select|date|number|checkbox|textarea
3. **Options (select type):** Required, min 2 options, unique values
4. **Validation Rules:** Valid JSON, supported constraints only
5. **Visibility:** Must be: personal|team
6. **Team ID:** Required if visibility=team
7. **Question Text:** 10-500 chars
8. **Template Name:** 5-100 chars, unique per team
9. **Inherited Sections:** Min 1 section, all must exist in framework defaults
10. **Framework Version:** Valid semver format (x.y.z)

## Non-Functional Requirements

### Performance
- Custom field validation: <100ms
- Template retrieval (with inheritance): <200ms
- Auto-update on framework upgrade: <5 seconds per template

### Security
- Team-scoped fields: Team members only
- Personal fields: Creator only
- Modify permissions: Creator or team admins
- Input sanitization: Prevent injection attacks
- Audit trail: All custom data modifications logged

### Scalability
- Support 100 custom fields per template
- Support 50 team questions per team
- Support 1,000 custom templates per organization
- Handle 10,000+ concurrent story creations

### Reliability
- Database replication for custom data
- Auto-update idempotent (safe to run multiple times)
- Rollback available for inheritance updates

### Usability
- Clear validation error messages
- Help text visible for custom fields
- Visual indication of custom vs default sections
- Preview template before using

## Definition of Done

### Implementation
- [ ] Custom field CRUD endpoints
- [ ] Team question CRUD endpoints
- [ ] Custom template CRUD endpoints
- [ ] Template inheritance resolution
- [ ] Custom field validation (6 data types)
- [ ] Custom data persistence in story files
- [ ] Team scoping and visibility
- [ ] Inheritance auto-update on upgrades

### Quality
- [ ] All 6 acceptance criteria have passing tests
- [ ] Edge cases covered (8 scenarios)
- [ ] Data validation enforced (10 rules)
- [ ] NFRs met (validation <100ms, retrieval <200ms, coverage ≥95%)
- [ ] Code coverage >95%

### Testing
- [ ] Unit tests: 30+ cases (validation, inheritance, auto-update)
- [ ] Integration tests: 15+ cases (full workflow, team sharing, permissions)
- [ ] Edge case tests: 8+ cases (all edge cases validated)
- [ ] Performance tests: Validation, retrieval, auto-update latency

### Documentation
- [ ] API documentation (OpenAPI/Swagger)
- [ ] Custom template creation guide
- [ ] Team question injection guide
- [ ] Data model documentation (ER diagram)
- [ ] Inheritance behavior examples
- [ ] Troubleshooting guide

### Release Readiness
- [ ] Security scan passed (OWASP Top 10)
- [ ] Team/personal scoping validated
- [ ] Audit trail logging verified
- [ ] Database migrations tested
- [ ] Deployed to staging for smoke testing

## Workflow History

- **2025-11-07:** Story created from EPIC-003 Feature 2.3 (batch mode)
