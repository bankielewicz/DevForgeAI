---
description: Rebuild feedback index from all feedback sources (AI analysis, code reviews, reports, sessions)
argument-hint:
model: opus
allowed-tools: Bash, Read, Glob
---

# /feedback-reindex - Rebuild Unified Feedback Index

Rebuild `devforgeai/feedback/index.json` from ALL feedback sources:
- AI analysis folders (`ai-analysis/STORY-*/`, `EPIC-*/`, `RCA-*/`)
- Code review files (`code-review/`, `code-reviews/`)
- Root-level report files (code reviews, integration tests, coverage)
- Session files (`sessions/`) if present

**Use when:**
- Index file is corrupted or out of sync
- After manual feedback file modifications
- Periodic maintenance (monthly recommended)
- After `/dev` or `/qa` workflows to ensure all feedback is indexed

---

## Command Workflow

### Phase 0: Validation

**Check feedback directory exists:**

```
Glob(pattern="devforgeai/feedback/")
```

IF `devforgeai/feedback/` does not exist → HALT with error:
```
❌ ERROR: Feedback directory not found
Expected: devforgeai/feedback/
Initialize feedback system first by running /dev or /qa workflows.
```

---

### Phase 1: Execute Reindex via CLI

**Run the devforgeai-validate CLI:**

```bash
devforgeai-validate feedback-reindex --project-root=. --format=text
```

The CLI scans all feedback sources and outputs:
```
✅ Reindex completed successfully

Total files processed: 267
Successfully indexed: 265
Errors encountered: 2

Sources scanned:
  AI analysis files: 254
  Code review files:   5
  Root report files:   8
  Session files:       0

Index file: devforgeai/feedback/index.json
Index version: 2.0
```

**For JSON output:**
```bash
devforgeai-validate feedback-reindex --project-root=. --format=json
```

---

### Phase 2: Verify

**Read the generated index to confirm:**

```
Read(file_path="devforgeai/feedback/index.json")
```

Verify:
- `version` is `"2.0"`
- `feedback-sessions` array has entries
- `source_summary` shows counts per source type
- Entries have `source_type`, `story-id`, `file-path` fields

---

## Success Criteria

- [ ] Index file created/rebuilt at `devforgeai/feedback/index.json`
- [ ] All feedback files processed from all source types
- [ ] Index contains valid JSON with version, last-updated, feedback-sessions, source_summary
- [ ] All entries have required fields (id, timestamp, source_type, file-path)
- [ ] Documentation and config files are excluded from index
- [ ] Execution completes in <10 seconds for 1000+ files

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Feedback directory not found | `devforgeai/feedback/` doesn't exist | Run /dev or /qa to create feedback |
| CLI not available | devforgeai-validate not installed | `pip install -e .claude/scripts/` |
| Permission denied | No write access to feedback dir | Check file permissions |
| JSON parse errors | Malformed feedback files | Check error list in output, fix files |

---

## Integration

**Invoked by:** User running `/feedback-reindex`
**Invokes:** `devforgeai-validate feedback-reindex` CLI command
**Updates:** `devforgeai/feedback/index.json` (completely rebuilt)

---

**Token Budget:** ~800 tokens (lean command)
**Execution Time:** <10 seconds typical
**Status:** Production Ready
