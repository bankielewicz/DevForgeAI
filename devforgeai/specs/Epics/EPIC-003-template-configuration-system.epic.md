---
id: EPIC-003
title: Template & Configuration System
business-value: Provide structured, consistent feedback format through context-aware templates and comprehensive user configuration, enabling both framework maintainers (standardized feedback) and users (customization control)
status: Planning
priority: High
complexity-score: 44
architecture-tier: Tier 3 (Complex Platform)
created: 2025-11-07
estimated-points: 24-39
target-sprints: 3-4
dependencies:
  - EPIC-002 (Feature 1.2 - question bank structure)
---

# Template & Configuration System

## Business Goal

Transform raw feedback conversation responses into structured, portable templates that can be analyzed, aggregated, and fed into the DevForgeAI ideation pipeline. Provide users with comprehensive configuration control over feedback behavior (enable/disable, trigger rules, template customization).

**Success Metrics:**
- Template completeness: 95%+ of feedback sessions produce complete templates (all required fields populated)
- Configuration adoption: 70%+ of users customize default config within first month
- Cross-project portability: 100% of feedback templates successfully export/import without data loss
- Framework insight quality: 90%+ of exported templates contain structured, actionable data

## Features

### Feature 2.1: Feedback Template Engine
**Description:** Context-aware template system that structures feedback based on operation type (command, skill, subagent) and success status (passed, failed, partial), with automatic field mapping from conversation responses.

**User Stories (high-level):**
1. As a framework maintainer, I want standardized feedback templates, so that I can aggregate insights across users
2. As a user, I want feedback automatically structured, so that I don't have to manually organize my thoughts
3. As a maintainer, I want templates to adapt to context, so that command feedback differs from skill feedback

**Acceptance Criteria:**
- Template definitions for each operation type (command-template.md, skill-template.md, subagent-template.md)
- Success/failure template variations (different sections for pass vs fail)
- Automatic field mapping (map conversation responses to template fields)
- Template rendering with metadata (timestamp, operation type, status, story ID if applicable)
- YAML frontmatter + Markdown content format
- Templates stored in `.claude/skills/devforgeai-feedback/templates/`

**Template Sections (Example - Command Feedback):**
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
{User responses from question: "What aspects of the development workflow worked well?"}

## What Went Poorly
{User responses from question: "What aspects were confusing or frustrating?"}

## Suggestions for Improvement
{User responses from question: "How could DevForgeAI improve this workflow?"}

## Context
- **TodoWrite Status:** {final todo list status}
- **Errors Encountered:** {Y/N + error summary}
- **Performance Metrics:** {execution time, token usage}

## User Sentiment
{Derived from question: "How satisfied were you with this operation?" (1-5 scale)}

## Actionable Insights
{Auto-extracted from suggestions - keywords: "should", "could", "needs"}
```

**Estimated Effort:** Medium (8-13 story points)

### Feature 2.2: Configuration Management
**Description:** YAML-based configuration file (`devforgeai/config/feedback.yaml`) that controls feedback feature behavior, with validation and sensible defaults.

**User Stories (high-level):**
1. As a user, I want to enable/disable feedback with a single config change
2. As a user, I want to control when feedback triggers (always, failures-only, specific operations)
3. As a framework maintainer, I want consistent config structure across projects

**Acceptance Criteria:**
- Config file location: `devforgeai/config/feedback.yaml`
- Config structure:
  ```yaml
  enabled: true  # Master enable/disable

  trigger:
    mode: failures-only  # always, failures-only, specific-operations, never
    operations:  # If mode=specific-operations
      - /dev
      - /qa
      - devforgeai-development

  conversation:
    max-questions: 10  # Question limit (5-15)
    allow-skip: true   # Allow skipping individual questions

  skip-tracking:
    enabled: true
    threshold: 3  # Consecutive skips before suggesting disable

  templates:
    default: context-aware  # Use operation-specific templates
    custom-fields: []  # User-defined fields (advanced)
  ```
- Config validation on read (schema validation)
- Default config auto-generated if missing
- Config accessible via: `Read(file_path="devforgeai/config/feedback.yaml")`

**Estimated Effort:** Medium (8-13 story points)

### Feature 2.3: Template Customization
**Description:** Advanced customization allowing users to define custom template fields, inject custom questions into conversations, and extend default templates.

**User Stories (high-level):**
1. As a power user, I want to add custom fields to feedback templates (e.g., "Project phase", "Team size")
2. As a team lead, I want to inject team-specific questions (e.g., "Did you follow our coding conventions?")
3. As a framework maintainer, I want template inheritance, so custom templates extend (not replace) defaults

**Acceptance Criteria:**
- Custom field definitions in config:
  ```yaml
  templates:
    custom-fields:
      - name: project-phase
        prompt: "What project phase is this? (MVP, Beta, Production)"
        type: single-select
        options:
          - MVP
          - Beta
          - Production
      - name: team-context
        prompt: "Any team-specific context to share?"
        type: free-text
  ```
- Custom questions injected into conversation at configurable position (after core questions, before suggestions)
- Template inheritance: custom templates extend base templates (add fields, don't remove)
- Validation: Reject invalid custom field definitions (missing name, invalid type)

**Estimated Effort:** Medium (8-13 story points)

## Dependencies

**Prerequisites:**
- EPIC-002 Feature 1.2 (question bank structure) - defines question patterns for template mapping

**Dependent Epics:**
- EPIC-004 (Storage) depends on Feature 2.1 (template format)
- EPIC-005 (Framework Integration) depends on Feature 2.2 (config management)

## Technical Considerations

**Architecture:**
- Template engine in domain layer (template selection, field mapping, rendering logic)
- Configuration in infrastructure layer (YAML parsing, validation, defaults)
- Application layer orchestrates (template selection → field mapping → rendering)

**Technology Stack:**
- Templates: Markdown with YAML frontmatter
- Configuration: YAML (`devforgeai/config/feedback.yaml`)
- Validation: JSON Schema for config validation

**Framework Constraints:**
- Must be framework-agnostic (templates work for .NET, Node.js, Python, etc.)
- Cannot include language-specific examples in templates

## Risks

**Risk 1: Configuration Complexity**
- Likelihood: Medium
- Impact: Medium (users confused by too many options)
- Mitigation: Sensible defaults (failures-only, 10 questions max), progressive disclosure (basic config upfront, advanced in docs)

**Risk 2: Template Inflation**
- Likelihood: Low
- Impact: Low (too many templates to maintain)
- Mitigation: Start with 3 core templates (command, skill, subagent), defer specialized templates to future enhancement

## Acceptance Criteria (Epic Level)

- [ ] All 3 features implemented and tested
- [ ] Template engine renders context-aware templates for all operation types
- [ ] Configuration file provides comprehensive control (enable/disable, triggers, customization)
- [ ] Custom field and question injection working
- [ ] Config validation prevents invalid configurations
- [ ] Template format integrates with Epic 4 (storage) and Epic 5 (framework hooks)
- [ ] 95%+ template completeness achieved in testing

## Notes

This epic transforms raw feedback conversations into structured, portable data. It's the "translation layer" between human insights (Epic 2) and machine-readable artifacts (Epic 4).

**Key Design Decision:** YAML config + Markdown templates (vs JSON config + JSON templates)
- **Rationale:** YAML more human-readable, Markdown natural for Claude interpretation, aligns with DevForgeAI's Markdown-first design philosophy

**Target Complexity:** Tier 3 (Clean Architecture with domain-driven design)
**Timeline:** 3-4 sprints (6-8 weeks at 10 points/sprint)
