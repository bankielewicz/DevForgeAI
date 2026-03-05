---
title: Positioning Strategy Reference
skill: marketing-business
version: 1.0
---

# Positioning Strategy Workflow

This reference documents the complete positioning and messaging framework for the marketing-business skill. It covers positioning statement generation, key message creation, output file management, and overwrite behavior.

## Positioning Statement

The positioning statement framework is built on three core elements:

1. **Category** - The market category the product competes in
2. **Differentiation** - What makes the product unique versus alternatives
3. **Audience** - The target audience segment the product serves

### Template

Use the following positioning statement template:

> For [target audience] who [need/problem], [product name] is a [category] that [key benefit]. Unlike [alternative], our product [primary differentiator].

Each placeholder must be filled with validated, non-empty content before the statement is considered complete.

## Key Messages

Key messages translate the positioning statement into audience-specific talking points. The workflow generates 3 to 5 messages per segment, each with a 50-word limit.

### Rules

- Minimum 3 messages per segment
- Maximum 5 messages per segment
- Each message must be <= 50 words
- Messages must align with the positioning statement

### Audience Segment Mapping

Messages are organized under named audience segments using the format `### Segment: [Name]`. Each segment subsection contains its tailored messages. The skill processes each segment independently.

### Input Validation (BR-003)

If the audience input is empty, the workflow produces a validation error and blocks entirely. No partial output is written when audience validation fails.

### Segment Truncation (BR-004)

When more than 5 audience segments are provided, the skill truncates to the first 5 alphabetically. The user is notified that remaining segments were omitted via a truncation warning.

### Segment Deduplication (BR-005)

Duplicate segment names are removed via case-insensitive deduplication. The first occurrence is retained; subsequent duplicates are discarded.

## Output Creation

### Output File Path

The generated positioning document is written to:

```
devforgeai/specs/business/marketing/positioning.md
```

### Directory Auto-Creation

The skill will automatically create the directory path if it does not exist. This uses mkdir to create any missing intermediate directories along the output path.

### YAML Frontmatter

The output file includes YAML frontmatter with the following required fields:

- `story_id` - The story identifier that triggered generation (frontmatter field)
- `generated_date` - ISO 8601 timestamp of generation (frontmatter field)
- `skill` - The skill name that produced the output (frontmatter field)

Example output file structure:

```markdown
---
story_id: STORY-540
generated_date: 2026-03-05T10:00:00Z
skill: marketing-business
---

## Positioning Statement

[Generated positioning statement content]

## Key Messages

[Generated key messages organized by segment]
```

### Required Output Sections

The output file must contain these sections:

- **## Positioning Statement** - The completed positioning statement
- **## Key Messages** - All generated messages organized by segment

## Overwrite Behavior

When the output file already exists, the skill will overwrite the existing file rather than append to it. The full content is replaced with new content on each run.

### Timestamp Tracking

On overwrite, the skill records:

- **Previous version timestamp** - The generated_date from the old file before replacement
- **New version timestamp** - The updated generated_date written to the replacement file

### User Notification

The user is notified via a confirmation message indicating the existing positioning document was updated. This message includes both the previous and new timestamps.
