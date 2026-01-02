---
id: STORY-188
title: Add Observation Capture Command to Phase CLI
type: feature
epic: EPIC-033
priority: LOW
points: 2
status: Backlog
created: 2025-12-31
source: STORY-155, STORY-147 framework enhancement analysis
---

# STORY-188: Add Observation Capture Command to Phase CLI

## User Story

**As a** DevForgeAI developer,
**I want** a phase-observe CLI command,
**So that** workflow observations are captured in phase state files.

## Background

Observations are documented in enhancement files but not captured in phase state, leaving AI analysis with no data.

## Acceptance Criteria

### AC-1: New Command Available
**Then** `devforgeai-validate phase-observe STORY-XXX --phase=04 --category=friction --note="..."`

### AC-2: Observations Array Added
**Then** observations array added to phase state file

### AC-3: Observation Structure Defined
**Then** structure: id, phase, category, note, severity, timestamp

### AC-4: Categories Defined
**Then** categories: friction, gap, success, pattern

### AC-5: Severities Defined
**Then** severities: low, medium, high

### AC-6: phase-init Creates Empty Array
**Then** phase-init includes empty observations array

## Technical Specification

### Files to Modify
- `.claude/scripts/devforgeai_cli/commands/phase_commands.py`
- `.claude/scripts/devforgeai_cli/cli.py`

### Implementation
```python
@cli.command('phase-observe')
@click.argument('story_id')
@click.option('--phase', required=True)
@click.option('--category', type=click.Choice(['friction', 'gap', 'success', 'pattern']))
@click.option('--note', required=True)
@click.option('--severity', default='medium', type=click.Choice(['low', 'medium', 'high']))
def phase_observe(story_id, phase, category, note, severity):
    # Add observation to state file
```

## Definition of Done

- [ ] phase-observe command implemented
- [ ] Observations array in phase state
- [ ] Categories: friction, gap, success, pattern
- [ ] Severities: low, medium, high
- [ ] phase-init creates empty observations array

## Effort Estimate
- **Points:** 2
- **Estimated Hours:** 1 hour

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | claude/opus | Story created from STORY-155/147 framework enhancement |
