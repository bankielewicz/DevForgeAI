---
id: STORY-209
title: Glob Patterns Test Story
epic: EPIC-TEST
sprint: SPRINT-TEST
status: In Development
points: 3
priority: Medium
depends_on: []
created: 2025-12-16
format_version: "2.0"
---

# Story: Glob Patterns Test Story

## Description

Test story with glob patterns in file_path values.
Tests edge case handling of glob patterns.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "multi-service"
      file_path: "src/services/*.py"
      interface: "Python Modules"
      requirements:
        - id: "SVC-001"
          description: "Multiple service files"
          testable: true

    - type: "Configuration"
      name: "all-configs"
      file_path: "src/config/**/*.yaml"
      requirements:
        - id: "CFG-001"
          description: "All YAML configs in config directory"
          testable: true
```

## Definition of Done

### Implementation
- [ ] Multiple services implemented
- [ ] Config files created
