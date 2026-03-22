---
id: EPIC-004
title: Storage & Indexing
business-value: Enable long-term feedback retention, searchability, and cross-project portability through file-based storage with metadata indexing and export/import capabilities
status: Planning
priority: High
complexity-score: 44
architecture-tier: Tier 3 (Complex Platform)
created: 2025-11-07
estimated-points: 21-34
target-sprints: 2-4
dependencies:
  - EPIC-002 Feature 1.1 (feedback data format)
  - EPIC-003 Feature 2.1 (template format)
---

# Storage & Indexing

## Business Goal

Persist feedback sessions to disk with searchable metadata, enabling users to review historical feedback, identify patterns over time, and export feedback for DevForgeAI maintainers (creating the feedback loop between project users and framework developers).

**Success Metrics:**
- Storage reliability: 99.9%+ of feedback sessions successfully persisted (no data loss)
- Search performance: <1s to search across 1000+ feedback sessions
- Export adoption: 40%+ of users export feedback to share with maintainers
- Cross-project portability: 100% of exported feedback successfully imports into DevForgeAI project

## Features

### Feature 3.1: Feedback File Persistence
**Description:** Save feedback sessions to `devforgeai/feedback/` directory with timestamp-based naming, atomic writes, and corruption prevention.

**User Stories (high-level):**
1. As a user, I want my feedback automatically saved, so that I can review it later
2. As a user, I want confidence that feedback won't be lost, even if system crashes during write
3. As a framework maintainer, I want consistent file naming, so that I can programmatically process feedback

**Acceptance Criteria:**
- Feedback directory: `devforgeai/feedback/sessions/`
- File naming: `{timestamp}-{operation-type}-{status}.md`
  - Example: `2025-11-07T10-30-00-command-dev-success.md`
- File format: Markdown with YAML frontmatter (template from Epic 3)
- Atomic writes (write to temp file, then rename to prevent corruption)
- Directory auto-creation if missing
- File permissions: User-readable/writable only (0600)

**Organization Options (Config-driven):**
```yaml
storage:
  organization: chronological  # chronological, by-operation, by-status
  subdirectories:
    by-operation: false  # If true: /commands/, /skills/, /subagents/
    by-status: false     # If true: /successes/, /failures/
```

**Estimated Effort:** Small (5-8 story points)

### Feature 3.2: Searchable Metadata Index
**Description:** Maintain searchable index (`devforgeai/feedback/index.json`) with metadata from all feedback sessions, enabling fast filtering by date, operation, status, tags, and keywords.

**User Stories (high-level):**
1. As a user, I want to search "all failed /qa runs in last month", so that I can identify patterns
2. As a maintainer, I want to find "all feedback mentioning 'confusing error messages'", so that I can prioritize UX improvements
3. As a user, I want search to be fast, even with hundreds of feedback sessions

**Acceptance Criteria:**
- Index file: `devforgeai/feedback/index.json`
- Index structure:
  ```json
  {
    "version": "1.0",
    "last-updated": "2025-11-07T10:30:00Z",
    "feedback-sessions": [
      {
        "id": "2025-11-07T10-30-00-command-dev-success",
        "timestamp": "2025-11-07T10:30:00Z",
        "operation": {
          "type": "command",
          "name": "/dev",
          "args": "STORY-042"
        },
        "status": "success",
        "tags": ["tdd", "backend"],
        "story-id": "STORY-042",
        "keywords": ["tests passed", "refactoring", "clean code"],
        "file-path": "sessions/2025-11-07T10-30-00-command-dev-success.md"
      }
    ]
  }
  ```
- Index update: Append new entry on feedback write (incremental update, not full rebuild)
- Index rebuild command: `/feedback-reindex` (in case of corruption)
- Search API (used by `/feedback-search` command):
  - Filter by date range
  - Filter by operation type/name
  - Filter by status (success/failure)
  - Keyword search across all fields
  - Tag-based filtering

**Estimated Effort:** Medium (8-13 story points)

### Feature 3.3: Cross-Project Export/Import
**Description:** Export feedback sessions into portable package for sharing with DevForgeAI maintainers, with sensitive data sanitization and import capability for framework project.

**User Stories (high-level):**
1. As a project user, I want to export my feedback and send it to DevForgeAI maintainers, so that they can fix issues I encountered
2. As a framework maintainer, I want to import user feedback into my DevForgeAI project, so that I can prioritize enhancements
3. As a user, I want sensitive data (project names, story IDs, custom fields) sanitized before export

**Acceptance Criteria:**
- Export command: `/export-feedback [--date-range=last-30-days] [--sanitize=true]`
- Export package format: `devforgeai-feedback-export-{timestamp}.zip`
- Package contents:
  - `feedback-sessions/` (all session files, sanitized if requested)
  - `index.json` (filtered index matching exported sessions)
  - `manifest.json` (export metadata: date range, sanitization applied, session count)
- Sanitization rules (if `--sanitize=true`):
  - Replace story IDs with placeholders (STORY-XXX → STORY-001)
  - Remove custom field values (keep field names for analysis)
  - Remove project-specific context (file paths, repo names)
- Import command: `/import-feedback [file.zip]`
  - Extract to `devforgeai/feedback/imported/{timestamp}/`
  - Merge index entries with conflict resolution (duplicate IDs get -imported-N suffix)
  - Validation: Reject corrupted or incompatible exports

**Estimated Effort:** Medium (8-13 story points)

## Dependencies

**Prerequisites:**
- EPIC-002 Feature 1.1 (feedback data format) - defines what to store
- EPIC-003 Feature 2.1 (template format) - defines file structure

**Dependent Epics:**
- EPIC-005 (Framework Integration) uses storage for persisting feedback from hooks

## Stories

| Story ID | Feature | Title | Points | Status |
|----------|---------|-------|--------|--------|
| STORY-013 | Feature 3.1 | Feedback File Persistence with Atomic Writes | 8 | QA Approved |
| STORY-016 | Feature 3.2 | Searchable Metadata Index for Feedback Sessions | 13 | QA Approved |
| STORY-017 | Feature 3.3 | Cross-Project Export/Import for Feedback Sessions | 13 | QA Approved |

## Technical Considerations

**Architecture:**
- File I/O in infrastructure layer (atomic writes, directory management)
- Indexing in domain layer (metadata extraction, search logic)
- Export/import in application layer (orchestration, sanitization)

**Technology Stack:**
- Storage: File system (`devforgeai/feedback/`)
- Index: JSON (`devforgeai/feedback/index.json`)
- Export: ZIP archive with JSON manifest
- Sanitization: Regex-based replacements + manual review prompts

**Performance:**
- Index size: ~500 bytes per feedback session → 1000 sessions = ~500KB (negligible)
- Search: JSON parsing in-memory → sub-second for 10K sessions
- Export: ZIP compression → 1MB per 100 sessions typical

**Framework Constraints:**
- File-based storage (no database required - aligns with DevForgeAI simplicity)
- Cross-platform paths (Windows, Linux, macOS compatible)

## Risks

**Risk 1: Index Corruption**
- Likelihood: Low
- Impact: Medium (search broken until rebuilt)
- Mitigation: Atomic index updates (write to temp, rename), `/feedback-reindex` command

**Risk 2: Export File Size**
- Likelihood: Medium (users export years of feedback)
- Impact: Low (large files slow to share)
- Mitigation: Date range filtering, compression, prompt user if export >10MB

**Risk 3: Sanitization Gaps**
- Likelihood: Medium
- Impact: High (sensitive data leaked to maintainers)
- Mitigation: Conservative sanitization by default, user review before export, clear warnings

## Acceptance Criteria (Epic Level)

- [ ] All 3 features implemented and tested
- [ ] Feedback sessions reliably persisted to disk (99.9%+ success rate)
- [ ] Searchable index enables filtering by date, operation, status, keywords
- [ ] Export/import workflow functional with sanitization
- [ ] 1000+ feedback sessions handled without performance degradation
- [ ] Cross-project portability validated (export from Project A → import to DevForgeAI project)
- [ ] No data loss in crash scenarios (atomic writes tested)

## Notes

This epic makes feedback **durable** and **actionable**. Without storage, feedback is ephemeral (lost after conversation). Without indexing, feedback is unactionable (can't find patterns). Without export/import, the feedback loop to framework maintainers is broken.

**Key Design Decision:** File-based storage (vs database)
- **Rationale:** Aligns with DevForgeAI simplicity philosophy, no additional dependencies, Git-compatible (can version control feedback)

**Target Complexity:** Tier 3 (Clean Architecture with robust error handling)
**Timeline:** 2-4 sprints (4-8 weeks at 10 points/sprint)
