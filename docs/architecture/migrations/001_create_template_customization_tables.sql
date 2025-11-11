-- Migration: 001_create_template_customization_tables.sql
-- Story: STORY-012 - Template Customization
-- Implementation: src/template_customization.py (Data models lines 80-179)
-- Purpose: Create tables for custom template fields, team questions, and custom templates

-- =============================================================================
-- Table: custom_template_fields
-- Purpose: Custom fields that extend story templates (AC1, AC4)
-- Data Model: src/template_customization.py::CustomTemplateField (lines 80-113)
-- =============================================================================

CREATE TABLE IF NOT EXISTS custom_template_fields (
    -- Primary Key
    field_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Field Definition (VR1, VR2)
    field_name VARCHAR(100) NOT NULL CHECK (LENGTH(field_name) >= 3 AND LENGTH(field_name) <= 100),
    field_type VARCHAR(20) NOT NULL CHECK (field_type IN ('text', 'select', 'date', 'number', 'checkbox', 'textarea')),
    description VARCHAR(500),

    -- Field Configuration
    is_required BOOLEAN DEFAULT FALSE NOT NULL,
    field_order INTEGER,
    validation_rules JSONB DEFAULT '{}',  -- Constraints (min/max for numbers, min_length/max_length for text)
    options JSONB,  -- Array of {value, label} objects for select fields

    -- Visibility and Scoping (VR5, VR6)
    visibility VARCHAR(20) NOT NULL CHECK (visibility IN ('personal', 'team')) DEFAULT 'team',
    team_id UUID REFERENCES teams(team_id),

    -- Audit Fields
    created_by UUID NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Business Rule BR1: Field names unique within team/personal scope
    CONSTRAINT unique_field_name_per_team UNIQUE (field_name, COALESCE(team_id, created_by)),

    -- Validation Rule VR6: Team ID required if visibility='team'
    CONSTRAINT team_id_required_for_team_visibility
        CHECK (
            (visibility = 'team' AND team_id IS NOT NULL) OR
            (visibility = 'personal' AND team_id IS NULL)
        ),

    -- Validation Rule VR3: Select fields must have min 2 options with unique values
    CONSTRAINT select_field_options_valid
        CHECK (
            field_type != 'select' OR
            (options IS NOT NULL AND JSONB_ARRAY_LENGTH(options) >= 2)
        )
);

-- Indexes for performance
CREATE INDEX idx_custom_fields_team_id ON custom_template_fields(team_id) WHERE team_id IS NOT NULL;
CREATE INDEX idx_custom_fields_visibility ON custom_template_fields(visibility);
CREATE INDEX idx_custom_fields_created_by ON custom_template_fields(created_by);
CREATE INDEX idx_custom_fields_type ON custom_template_fields(field_type);

-- Business Rule BR2: Field type immutable after creation
CREATE OR REPLACE FUNCTION prevent_field_type_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.field_type != NEW.field_type THEN
        RAISE EXCEPTION 'Field type is immutable and cannot be changed';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER field_type_immutable
    BEFORE UPDATE ON custom_template_fields
    FOR EACH ROW
    EXECUTE FUNCTION prevent_field_type_change();

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER custom_fields_updated_at
    BEFORE UPDATE ON custom_template_fields
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE custom_template_fields IS 'Custom fields for extending story templates (STORY-012 AC1, AC4)';
COMMENT ON COLUMN custom_template_fields.field_name IS 'VR1: 3-100 chars, unique per team scope';
COMMENT ON COLUMN custom_template_fields.field_type IS 'VR2: text|select|date|number|checkbox|textarea (immutable per BR2)';
COMMENT ON COLUMN custom_template_fields.options IS 'VR3: Min 2 options for select type, unique values required';
COMMENT ON COLUMN custom_template_fields.team_id IS 'VR6: Required if visibility=team, null if visibility=personal';

-- =============================================================================
-- Table: team_questions
-- Purpose: Custom questions injected into story creation workflow (AC2)
-- Data Model: src/template_customization.py::TeamQuestion (lines 116-141)
-- =============================================================================

CREATE TABLE IF NOT EXISTS team_questions (
    -- Primary Key
    question_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Question Content (VR7)
    question_text VARCHAR(500) NOT NULL CHECK (LENGTH(question_text) >= 10 AND LENGTH(question_text) <= 500),
    expected_answer VARCHAR(1000),

    -- Question Configuration
    is_required BOOLEAN DEFAULT FALSE NOT NULL,
    question_order INTEGER DEFAULT 0 NOT NULL,

    -- Team Scoping
    team_id UUID NOT NULL REFERENCES teams(team_id),

    -- Audit Fields
    created_by UUID NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Indexes
CREATE INDEX idx_team_questions_team_id ON team_questions(team_id);
CREATE INDEX idx_team_questions_order ON team_questions(team_id, question_order);
CREATE INDEX idx_team_questions_required ON team_questions(is_required) WHERE is_required = TRUE;

-- Updated_at trigger
CREATE TRIGGER team_questions_updated_at
    BEFORE UPDATE ON team_questions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE team_questions IS 'Custom questions for story creation workflow (STORY-012 AC2, BR8)';
COMMENT ON COLUMN team_questions.question_text IS 'VR7: 10-500 chars';
COMMENT ON COLUMN team_questions.question_order IS 'BR8: Custom questions ordered AFTER framework questions';

-- =============================================================================
-- Table: custom_templates
-- Purpose: Custom story templates with inheritance from framework defaults (AC3, AC5, AC6)
-- Data Model: src/template_customization.py::CustomTemplate (lines 144-179)
-- =============================================================================

CREATE TABLE IF NOT EXISTS custom_templates (
    -- Primary Key
    template_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    -- Template Definition (VR8)
    template_name VARCHAR(100) NOT NULL CHECK (LENGTH(template_name) >= 5 AND LENGTH(template_name) <= 100),
    description VARCHAR(500),

    -- Inheritance Configuration (VR9, VR10, BR4, BR5)
    inherited_sections JSONB NOT NULL,  -- Array of section names from framework defaults
    custom_field_ids JSONB DEFAULT '[]',  -- Array of custom field UUIDs
    custom_question_ids JSONB DEFAULT '[]',  -- Array of team question UUIDs
    framework_version VARCHAR(20) NOT NULL CHECK (framework_version ~ '^\d+\.\d+\.\d+$'),  -- VR10: Semantic versioning
    inheritance_status VARCHAR(20) DEFAULT 'active' CHECK (inheritance_status IN ('active', 'pending_update', 'conflict')),
    inheritance_updated_at TIMESTAMP WITH TIME ZONE,

    -- Team Scoping and Visibility (AC5, BR6, BR7)
    team_id UUID REFERENCES teams(team_id),
    visibility VARCHAR(20) NOT NULL CHECK (visibility IN ('personal', 'team', 'read-only')) DEFAULT 'team',

    -- Audit Fields
    created_by UUID NOT NULL REFERENCES users(user_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Business Rule: Template names unique per team
    CONSTRAINT unique_template_name_per_team UNIQUE (template_name, COALESCE(team_id, created_by)),

    -- Validation Rule VR9: At least 1 inherited section required
    CONSTRAINT min_one_inherited_section
        CHECK (JSONB_ARRAY_LENGTH(inherited_sections) >= 1)
);

-- Indexes
CREATE INDEX idx_custom_templates_team_id ON custom_templates(team_id) WHERE team_id IS NOT NULL;
CREATE INDEX idx_custom_templates_created_by ON custom_templates(created_by);
CREATE INDEX idx_custom_templates_visibility ON custom_templates(visibility);
CREATE INDEX idx_custom_templates_framework_version ON custom_templates(framework_version);
CREATE INDEX idx_custom_templates_inheritance_status ON custom_templates(inheritance_status);

-- Updated_at trigger
CREATE TRIGGER custom_templates_updated_at
    BEFORE UPDATE ON custom_templates
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

COMMENT ON TABLE custom_templates IS 'Custom story templates with inheritance (STORY-012 AC3, AC5, AC6)';
COMMENT ON COLUMN custom_templates.template_name IS 'VR8: 5-100 chars, unique per team';
COMMENT ON COLUMN custom_templates.inherited_sections IS 'VR9: Min 1 section, must exist in framework defaults (BR4)';
COMMENT ON COLUMN custom_templates.framework_version IS 'VR10: Semantic versioning x.y.z, auto-updated per BR5';
COMMENT ON COLUMN custom_templates.inheritance_status IS 'AC6: active|pending_update|conflict based on framework version changes';
COMMENT ON COLUMN custom_templates.visibility IS 'BR6, BR7: personal=user-only, team=visible to all, read-only=non-creator cannot modify';

-- =============================================================================
-- Helper Tables (Optional - for production use)
-- =============================================================================

-- Track field usage across stories to enforce EC2 (cannot delete field in use)
CREATE TABLE IF NOT EXISTS custom_field_usage (
    field_id UUID NOT NULL REFERENCES custom_template_fields(field_id) ON DELETE CASCADE,
    story_id VARCHAR(50) NOT NULL,
    used_in_section VARCHAR(100),
    used_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY (field_id, story_id)
);

CREATE INDEX idx_field_usage_field ON custom_field_usage(field_id);
CREATE INDEX idx_field_usage_story ON custom_field_usage(story_id);

COMMENT ON TABLE custom_field_usage IS 'Tracks which stories use which custom fields (EC2: prevent deletion of fields in use)';

-- Audit trail for security logging (addresses LOW-002 from security scan)
CREATE TABLE IF NOT EXISTS template_audit_log (
    audit_id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50) NOT NULL CHECK (event_type IN ('CREATE', 'UPDATE', 'DELETE', 'SHARE', 'COPY', 'EXPORT', 'ACCESS_DENIED')),
    entity_type VARCHAR(50) NOT NULL CHECK (entity_type IN ('FIELD', 'QUESTION', 'TEMPLATE')),
    entity_id UUID NOT NULL,
    user_id UUID NOT NULL REFERENCES users(user_id),
    team_id UUID REFERENCES teams(team_id),
    event_data JSONB,  -- Additional event context (old/new values)
    ip_address INET,
    user_agent TEXT,
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE INDEX idx_audit_log_entity ON template_audit_log(entity_type, entity_id);
CREATE INDEX idx_audit_log_user ON template_audit_log(user_id);
CREATE INDEX idx_audit_log_timestamp ON template_audit_log(event_timestamp DESC);
CREATE INDEX idx_audit_log_event_type ON template_audit_log(event_type);

COMMENT ON TABLE template_audit_log IS 'Audit trail for all template customization operations (addresses security finding LOW-002)';

-- =============================================================================
-- Validation Functions
-- =============================================================================

-- EC7: Validate select field has valid options before usage
CREATE OR REPLACE FUNCTION validate_select_field_options()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.field_type = 'select' THEN
        -- VR3: Min 2 options required
        IF NEW.options IS NULL OR JSONB_ARRAY_LENGTH(NEW.options) < 2 THEN
            RAISE EXCEPTION 'Select fields must have at least 2 options';
        END IF;

        -- VR3: Option values must be unique
        IF (
            SELECT COUNT(DISTINCT value)
            FROM JSONB_ARRAY_ELEMENTS(NEW.options) opt,
            JSONB_EACH_TEXT(opt) AS kv
            WHERE kv.key = 'value'
        ) < JSONB_ARRAY_LENGTH(NEW.options) THEN
            RAISE EXCEPTION 'Select field options must have unique values';
        END IF;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_select_options
    BEFORE INSERT OR UPDATE ON custom_template_fields
    FOR EACH ROW
    EXECUTE FUNCTION validate_select_field_options();

-- EC1: Prevent field name conflicts with framework sections
CREATE OR REPLACE FUNCTION prevent_field_name_conflict()
RETURNS TRIGGER AS $$
DECLARE
    reserved_names TEXT[] := ARRAY['User Story', 'Acceptance Criteria', 'Technical Spec', 'Non-Functional Requirements', 'Definition of Done'];
BEGIN
    IF NEW.field_name = ANY(reserved_names) THEN
        RAISE EXCEPTION 'Field name conflicts with framework section: %', NEW.field_name;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER prevent_reserved_field_names
    BEFORE INSERT OR UPDATE ON custom_template_fields
    FOR EACH ROW
    EXECUTE FUNCTION prevent_field_name_conflict();

-- =============================================================================
-- Views
-- =============================================================================

-- View: Field usage statistics for deletion validation (EC2)
CREATE OR REPLACE VIEW custom_field_usage_stats AS
SELECT
    f.field_id,
    f.field_name,
    f.field_type,
    f.visibility,
    f.created_by,
    COUNT(u.story_id) AS usage_count,
    ARRAY_AGG(DISTINCT u.story_id ORDER BY u.story_id) FILTER (WHERE u.story_id IS NOT NULL) AS used_in_stories
FROM custom_template_fields f
LEFT JOIN custom_field_usage u ON f.field_id = u.field_id
GROUP BY f.field_id, f.field_name, f.field_type, f.visibility, f.created_by;

COMMENT ON VIEW custom_field_usage_stats IS 'Shows field usage counts for deletion validation (EC2)';

-- View: Template with inherited section resolution (for rendering)
CREATE OR REPLACE VIEW template_with_sections AS
SELECT
    t.template_id,
    t.template_name,
    t.inherited_sections,
    t.custom_field_ids,
    t.custom_question_ids,
    t.framework_version,
    t.visibility,
    t.team_id,
    t.created_by,
    -- Count custom fields
    JSONB_ARRAY_LENGTH(t.custom_field_ids) AS custom_field_count,
    -- Count team questions
    JSONB_ARRAY_LENGTH(t.custom_question_ids) AS custom_question_count,
    -- Count inherited sections (BR4: min 1)
    JSONB_ARRAY_LENGTH(t.inherited_sections) AS inherited_section_count
FROM custom_templates t;

COMMENT ON VIEW template_with_sections IS 'Template metadata with section counts for validation';

-- =============================================================================
-- Sample Data (For Testing)
-- =============================================================================

-- Insert sample users (assuming users table exists)
-- INSERT INTO users (user_id, username) VALUES
--     ('550e8400-e29b-41d4-a716-446655440000', 'user_a'),
--     ('660e8400-e29b-41d4-a716-446655440001', 'user_b');

-- Insert sample teams (assuming teams table exists)
-- INSERT INTO teams (team_id, team_name) VALUES
--     ('770e8400-e29b-41d4-a716-446655440002', 'Backend Team'),
--     ('880e8400-e29b-41d4-a716-446655440003', 'Frontend Team');

-- Example: Insert custom field
-- INSERT INTO custom_template_fields (field_name, field_type, visibility, team_id, created_by, options)
-- VALUES (
--     'Project Phase',
--     'select',
--     'team',
--     '770e8400-e29b-41d4-a716-446655440002',
--     '550e8400-e29b-41d4-a716-446655440000',
--     '[
--         {"value": "planning", "label": "Planning"},
--         {"value": "development", "label": "Development"},
--         {"value": "testing", "label": "Testing"},
--         {"value": "release", "label": "Release"}
--     ]'::jsonb
-- );

-- Example: Insert team question
-- INSERT INTO team_questions (question_text, expected_answer, is_required, team_id, created_by)
-- VALUES (
--     'Did you follow our coding conventions?',
--     'Yes (link to standards)',
--     TRUE,
--     '770e8400-e29b-41d4-a716-446655440002',
--     '550e8400-e29b-41d4-a716-446655440000'
-- );

-- Example: Insert custom template
-- INSERT INTO custom_templates (template_name, inherited_sections, custom_field_ids, framework_version, team_id, created_by)
-- VALUES (
--     'Our Standard Story',
--     '["User Story", "Acceptance Criteria", "Technical Spec"]'::jsonb,
--     '["field-uuid-1"]'::jsonb,
--     '1.0.1',
--     '770e8400-e29b-41d4-a716-446655440002',
--     '550e8400-e29b-41d4-a716-446655440000'
-- );

-- =============================================================================
-- Migration Validation
-- =============================================================================

-- Verify all constraints are in place
DO $$
BEGIN
    -- Check table exists
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'custom_template_fields') THEN
        RAISE EXCEPTION 'Migration failed: custom_template_fields table not created';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'team_questions') THEN
        RAISE EXCEPTION 'Migration failed: team_questions table not created';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'custom_templates') THEN
        RAISE EXCEPTION 'Migration failed: custom_templates table not created';
    END IF;

    RAISE NOTICE 'Migration 001 completed successfully';
    RAISE NOTICE 'Tables created: custom_template_fields, team_questions, custom_templates';
    RAISE NOTICE 'Triggers created: field_type_immutable, validate_select_options, updated_at';
    RAISE NOTICE 'Views created: custom_field_usage_stats, template_with_sections';
END $$;
