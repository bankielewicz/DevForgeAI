---
id: STORY-020
title: Feedback CLI Commands
epic: EPIC-005
sprint: Sprint-3
status: Backlog
points: 10
priority: High
created: 2025-11-07
---

# Story: Feedback CLI Commands

## User Story

**As a** DevForgeAI user,
**I want** to interact with the feedback system through CLI slash commands (/feedback, /feedback-config, /feedback-search, /export-feedback),
**so that** I can manually trigger feedback collection, manage configuration, explore feedback history, and export feedback data across projects.

## Acceptance Criteria

### 1. [ ] Manual Feedback Trigger via /feedback Command

**Given** the user is in an active CLI session,
**When** the user executes `/feedback` with optional context (current story, operation details),
**Then** the feedback system captures session metadata and triggers feedback collection,
**And** a confirmation message displays with feedback ID and next steps,
**And** the feedback is recorded in the feedback-register.md with timestamp and context.

---

### 2. [ ] View and Edit Configuration via /feedback-config Command

**Given** the user has the CLI framework initialized,
**When** the user executes `/feedback-config view`,
**Then** the current feedback configuration displays (collection triggers, retention policy, export options),
**And** the user can execute `/feedback-config edit [field] [value]` to modify settings,
**And** updated configuration persists to .devforgeai/feedback/config.yaml,
**And** validation prevents invalid configuration changes (e.g., negative retention days).

---

### 3. [ ] Search Feedback History via /feedback-search Command

**Given** feedback has been collected in previous sessions,
**When** the user executes `/feedback-search [query]` (story ID, operation type, date range, severity),
**Then** matching feedback entries display with metadata (timestamp, context, insights),
**And** results are sorted by relevance (date descending for time queries, relevance for text queries),
**And** pagination displays for results >10 entries (show first 10, offer "view next").

---

### 4. [ ] Export Feedback Package via /export-feedback Command

**Given** feedback data exists in local feedback system,
**When** the user executes `/export-feedback [options]` (date range, story IDs, format),
**Then** feedback package is created containing:
- Feedback entries matching selection criteria
- Metadata index (story IDs, operation types, temporal distribution)
- Configuration snapshot at export time
- Format options: JSON, CSV, markdown summary,
**And** package is saved to .devforgeai/feedback/exports/{timestamp}-feedback-export.{format},
**And** success message displays with file path and package contents summary.

---

### 5. [ ] Graceful Error Handling

**Given** user provides invalid arguments or operations fail,
**When** error condition occurs (invalid story ID, no feedback found, export fails),
**Then** clear error message displays explaining the issue,
**And** suggested resolution or help command displays,
**And** no partial/corrupted feedback or config files are created.

---

### 6. [ ] Command Help and Documentation

**Given** user is unfamiliar with feedback commands,
**When** user executes `/feedback --help`, `/feedback-config --help`, etc.,
**Then** concise help text displays with:
- Command purpose and common usage
- Available options and arguments
- Example usage patterns
- Link to detailed documentation.

---

## Technical Specification

### Command Definitions

#### /feedback Command

**Purpose:** Manually trigger feedback collection

**Syntax:** `/feedback [optional context]`

**Examples:**
```bash
/feedback
/feedback story-001 after-dev-completion
/feedback regression-testing phase-1
```

**Response (Success):**
```json
{
  "status": "captured",
  "feedback_id": "FB-2025-11-07-001",
  "timestamp": "2025-11-07T14:30:00Z",
  "context": "story-001 after-dev-completion",
  "next_steps": "Feedback captured. View recent feedback with: /feedback-search --limit=5",
  "message": "Feedback captured successfully"
}
```

#### /feedback-config Command

**Purpose:** View and edit feedback configuration

**Syntax:** `/feedback-config [view | edit | reset] [field] [value]`

**Examples:**
```bash
/feedback-config view
/feedback-config edit retention_days 30
/feedback-config reset
```

**Configuration Fields:**
- `retention_days`: Integer, 1-3650 (days to keep feedback)
- `auto_trigger_enabled`: Boolean (automatic feedback triggering)
- `export_format`: Enum (json, csv, markdown)
- `include_metadata`: Boolean (include metadata in exports)
- `search_enabled`: Boolean (enable search functionality)

**Response (view):**
```json
{
  "status": "success",
  "config": {
    "retention_days": 90,
    "auto_trigger_enabled": true,
    "export_format": "json",
    "include_metadata": true,
    "search_enabled": true
  },
  "message": "Current feedback configuration loaded"
}
```

#### /feedback-search Command

**Purpose:** Search feedback history

**Syntax:** `/feedback-search [query] [options]`

**Query Formats:**
- Story ID: `STORY-001`
- Date range: `2025-11-01..2025-11-07`
- Operation type: `dev`, `qa`, `release`
- Keyword search: `regression testing`

**Options:**
- `--severity`: Filter by severity (low, medium, high, critical)
- `--status`: Filter by status (open, resolved, archived)
- `--limit`: Limit results (1-1000, default: 10)
- `--page`: Page number for pagination

**Examples:**
```bash
/feedback-search STORY-001
/feedback-search 2025-11-01..2025-11-07 --severity=high --limit=20
/feedback-search dev --status=open
```

**Response:**
```json
{
  "status": "success",
  "query": "STORY-001",
  "total_matches": 47,
  "page": 1,
  "page_size": 10,
  "results": [
    {
      "feedback_id": "FB-2025-11-07-042",
      "timestamp": "2025-11-07T14:30:00Z",
      "story_id": "STORY-001",
      "operation": "dev",
      "severity": "medium",
      "summary": "TDD cycle took longer than expected",
      "status": "open"
    }
  ],
  "next_page_info": "Use: /feedback-search STORY-001 --page=2 to see next 10 results"
}
```

#### /export-feedback Command

**Purpose:** Export feedback data to file

**Syntax:** `/export-feedback [options]`

**Options:**
- `--format`: Export format (json, csv, markdown)
- `--date-range`: Date range (YYYY-MM-DD..YYYY-MM-DD or relative like last-7-days)
- `--story-ids`: Comma-separated story IDs (STORY-001,STORY-002)
- `--severity`: Filter by severity
- `--status`: Filter by status

**Examples:**
```bash
/export-feedback --format=json
/export-feedback --date-range=2025-11-01..2025-11-07 --story-ids=STORY-001,STORY-002
/export-feedback --severity=high --status=open
```

**Response:**
```json
{
  "status": "success",
  "export_id": "EXP-2025-11-07-001",
  "timestamp": "2025-11-07T14:35:00Z",
  "file_path": ".devforgeai/feedback/exports/2025-11-07-feedback-export.json",
  "format": "json",
  "entries_count": 23,
  "metadata": {
    "selection_criteria": {
      "severity": "high",
      "status": "open"
    },
    "export_timestamp": "2025-11-07T14:35:00Z",
    "framework_version": "1.0.1"
  },
  "message": "Feedback exported successfully to .devforgeai/feedback/exports/"
}
```

### Data Models

#### FeedbackEntry

```typescript
interface FeedbackEntry {
  feedback_id: string;  // FB-YYYY-MM-DD-###
  timestamp: string;  // ISO8601
  story_id: string | null;  // STORY-### or null if manual
  operation_type: 'dev' | 'qa' | 'release' | 'manual';
  context: string;  // User-provided or auto-captured
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'open' | 'resolved' | 'archived';
  insights: string;  // Parsed feedback content
  metadata: {
    framework_version: string;
    command?: string;
    duration?: number;  // milliseconds
    user_approval?: boolean;
  };
}
```

#### FeedbackConfig

```typescript
interface FeedbackConfig {
  retention_days: number;  // 1-3650
  auto_trigger_enabled: boolean;
  export_format: 'json' | 'csv' | 'markdown';
  include_metadata: boolean;
  search_enabled: boolean;
  created_at: string;  // ISO8601
  last_modified: string;  // ISO8601
}
```

#### ExportPackage

```typescript
interface ExportPackage {
  export_id: string;
  timestamp: string;  // ISO8601
  file_path: string;
  format: 'json' | 'csv' | 'markdown';
  entries: FeedbackEntry[];
  selection_criteria: Record<string, any>;
  metadata: {
    framework_version: string;
    export_timestamp: string;
    config_snapshot: FeedbackConfig;
  };
}
```

### Business Rules

1. **Feedback Capture:** Manual `/feedback` command captures context and creates entry in feedback-register.md
2. **Config Persistence:** Changes via `/feedback-config edit` immediately persist to config.yaml
3. **Search Indexing:** Feedback indexed by story ID, operation type, severity, timestamp for fast querying
4. **Export Filtering:** Export respects selection criteria - entries not matching criteria excluded
5. **Data Retention:** Feedback older than config.retention_days automatically archived
6. **Concurrent Access:** Multiple concurrent `/feedback` commands handled safely (unique feedback_id)
7. **Validation on All Inputs:** Command arguments, config fields, search queries validated before processing
8. **Clear Error Messages:** Every error includes issue description, constraint, and suggested resolution

### Dependencies

**Internal Dependencies:**
- devforgeai-feedback skill (feedback capture, search, export logic)
- Feedback storage system (STORY-013)
- Configuration management (STORY-011)

**External Dependencies:**
- YAML parser for config.yaml
- JSON/CSV serializers for export

### File Structure

```
.devforgeai/feedback/
├── config.yaml              # Configuration settings
├── feedback-register.md     # Master feedback log
└── exports/
    ├── 2025-11-07-feedback-export.json
    ├── 2025-11-06-feedback-export.csv
    └── ...
```

---

## Edge Cases

### 1. Empty Feedback History

**Condition:** User executes `/feedback-search` when no feedback collected yet

**Expected Behavior:** Message displays: "No feedback collected. Run `/feedback` to start collecting or check configuration."

**Validation:** No error, user receives actionable guidance

---

### 2. Invalid Configuration Change

**Condition:** User executes `/feedback-config edit retention_days -5`

**Expected Behavior:** Validation error: "retention_days must be positive number (received: -5)"

**Validation:** Configuration NOT updated, user can retry with valid value

---

### 3. Large Feedback History (1000+ sessions)

**Condition:** User searches feedback with broad criteria returning 1,200+ results

**Expected Behavior:** First 10 results display, user can paginate through results (100 at a time)

**Validation:** Command responds quickly even with large dataset

---

### 4. Export with Selection Criteria Matching No Data

**Condition:** User executes `/export-feedback --story-ids STORY-999,STORY-998` (stories with no feedback)

**Expected Behavior:** Export created with empty entries list, metadata notes "0 entries matched selection criteria"

**Validation:** Export succeeds but user sees 0 entries (valid use case)

---

### 5. Concurrent Feedback Collection

**Condition:** `/feedback` triggered while feedback already being collected by active /dev operation

**Expected Behavior:** New feedback captured independently, no race condition or data loss

**Validation:** Both feedback entries preserved with distinct timestamps

---

### 6. Configuration File Corruption

**Condition:** .devforgeai/feedback/config.yaml is corrupted or unreadable

**Expected Behavior:** Error message: "Configuration file corrupted. Run `/feedback-config reset` to restore defaults."

**Validation:** Reset option provided to restore working state

---

### 7. Export Format Not Supported

**Condition:** User executes `/export-feedback --format=xml` (XML not implemented)

**Expected Behavior:** Error: "Format 'xml' not supported. Supported formats: json, csv, markdown"

**Validation:** Clear message with supported options

---

### 8. Missing Permissions for Export

**Condition:** Export directory .devforgeai/feedback/exports/ is read-only

**Expected Behavior:** Error: "Cannot write to exports directory. Check file permissions."

**Validation:** Clear permission error with remediation guidance

---

## Data Validation Rules

### /feedback Command Arguments

- **Context parameter (optional):**
  - Max 500 characters
  - Alphanumeric, hyphens, underscores only
  - Example: `story-001 dev-phase retrospective`

### /feedback-config Command Arguments

- **Subcommand:** Must be: `view`, `edit`, or `reset`
- **Field names (for edit):**
  - `retention_days`: Integer, 1-3650
  - `auto_trigger_enabled`: Boolean (true/false)
  - `export_format`: One of: json, csv, markdown
  - `include_metadata`: Boolean (true/false)
- **Value constraints:**
  - No SQL injection: Sanitize all inputs
  - No path traversal: Validate field names against whitelist

### /feedback-search Command Arguments

- **Query parameter:**
  - Max 200 characters
  - Supports: story ID (STORY-###), date range (2025-11-01..2025-11-07), operation type (dev, qa, release)
  - Case-insensitive matching
- **Filters (optional):**
  - `--severity`: One of: low, medium, high, critical
  - `--status`: One of: open, resolved, archived
  - `--limit`: Integer 1-1000 (default: 10)

### /export-feedback Command Arguments

- **Date range validation:**
  - Format: YYYY-MM-DD or relative (last-7-days, last-month)
  - Start date ≤ end date
- **Story ID selection:**
  - Format: STORY-001, STORY-002 (comma-separated)
  - Validate IDs exist in feedback history
- **Format selection:**
  - One of: json, csv, markdown
  - Default: json

---

## Non-Functional Requirements

### Performance

- `/feedback` command response: <200ms
- `/feedback-config view`: <100ms
- `/feedback-config edit`: <150ms
- `/feedback-search`: <500ms for typical queries (1000 entries)
- `/export-feedback`: <2s for small exports (<100 entries), <5s for large exports (<10K entries)
- Feedback register: Scales to 10,000+ entries without performance degradation

### Usability

- Help text available for all commands: `/command --help`
- Error messages explain issue + constraint + suggested resolution
- Search syntax intuitive: `STORY-001`, `2025-11-01..2025-11-07`, `dev`
- Success messages confirm action and provide next steps

### Reliability

- No feedback data loss on concurrent `/feedback` calls
- Config validation prevents corruption (invalid values rejected)
- Export validation prevents partial/incomplete exports
- Graceful degradation if feedback directory missing (auto-create with defaults)

### Scalability

- Search performance maintained up to 10,000+ feedback entries
- Export packages handle 10,000+ entries without timeout
- Pagination prevents UI overload with large result sets

### Security

- Input validation prevents SQL injection in feedback queries
- Path validation prevents directory traversal in export paths
- Config file permissions restrict access to .devforgeai/feedback/
- User context sanitized (max 500 chars, alphanumeric only)

---

## Definition of Done

### Implementation

- [ ] /feedback command implemented (manual feedback trigger)
- [ ] /feedback-config command implemented (view, edit, reset)
- [ ] /feedback-search command implemented (query, filters, pagination)
- [ ] /export-feedback command implemented (formats, selection criteria)
- [ ] Each command ≤300 lines (lean orchestration pattern)
- [ ] Business logic delegated to devforgeai-feedback skill
- [ ] Help text available for all commands

### Quality Assurance

- [ ] Unit tests for command argument validation (30+ test cases)
- [ ] Unit tests for config persistence
- [ ] Unit tests for search logic
- [ ] Integration tests for full workflows
- [ ] Edge case tests (empty history, large datasets, invalid inputs)
- [ ] Performance tests (response time targets met)

### Testing

- [ ] All acceptance criteria verified
- [ ] Edge cases handled with clear error messages
- [ ] Data validation implemented for all inputs
- [ ] Performance targets met (<200ms-5s depending on command)
- [ ] Security tests (injection prevention, path validation)

### Documentation

- [ ] Command syntax documented
- [ ] Examples provided for each command
- [ ] Help text implemented
- [ ] Troubleshooting guide created

### Code Review

- [ ] Code follows coding standards
- [ ] No violations of anti-patterns
- [ ] Architecture constraints respected
- [ ] Lean orchestration pattern followed

### Deployment

- [ ] Deployed to staging environment
- [ ] QA validation passed
- [ ] Ready for production release

---

## Notes

**Command Architecture:**

All commands follow the lean orchestration pattern:
- Commands ≤300 lines
- Argument parsing and validation only
- Skill invocation for business logic
- Result display and next steps guidance

**Integration Points:**

- devforgeai-orchestration: Can trigger `/feedback` after story completion
- devforgeai-development: Auto-capture context during dev operations
- devforgeai-qa: Auto-capture QA phase and severity context
- devforgeai-release: Auto-capture deployment context

**User Experience:**

All commands provide:
- Clear help text (`--help`)
- Intuitive syntax
- Actionable error messages
- Next steps guidance

**Related Stories:**

- STORY-018: Event-Driven Hook System (prerequisite)
- STORY-019: Operation Lifecycle Integration (provides context)
- STORY-013: Feedback File Persistence (storage backend)
- STORY-011: Configuration Management (config system)
