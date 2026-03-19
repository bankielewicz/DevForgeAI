# Parameter Extraction for Remediation

Defines how the spec-driven-remediation skill extracts its input parameters from the conversation context set by the `/fix-story` command.

---

## Context Markers

The `/fix-story` command sets these context markers before invoking the skill:

| Marker | Format | Example |
|--------|--------|---------|
| `Fix Mode` | audit_file, story_id, or epic_id | `audit_file` |
| `Audit File` | Relative path to audit .md file | `devforgeai/qa/audit/custody-chain-audit-stories-413-424.md` |
| `Dry Run` | true or false | `false` |
| `Auto Only` | true or false | `false` |
| `Finding Filter` | F-NNN or "all" | `all` |

---

## Extraction Algorithm

```
1. Scan conversation context for the marker block:

   **Fix Mode:** {value}
   **Audit File:** {value}
   **Dry Run:** {value}
   **Auto Only:** {value}
   **Finding Filter:** {value}

2. Extract each value:
   FIX_MODE       = text after "**Fix Mode:**" (trim whitespace)
   AUDIT_FILE     = text after "**Audit File:**" (trim whitespace)
   DRY_RUN        = text after "**Dry Run:**" == "true"
   AUTO_ONLY      = text after "**Auto Only:**" == "true"
   FINDING_FILTER = text after "**Finding Filter:**" (trim whitespace)

3. Validate:
   IF FIX_MODE not in ["audit_file", "story_id", "epic_id"]:
       HALT: "Invalid fix mode: {FIX_MODE}"

   IF AUDIT_FILE is empty or null:
       HALT: "No audit file specified"

   result = Read(file_path=AUDIT_FILE)
   IF result fails:
       HALT: "Audit file not found: {AUDIT_FILE}"

   IF FINDING_FILTER != "all" AND not matches "F-\\d+":
       HALT: "Invalid finding filter: {FINDING_FILTER}. Expected F-NNN or 'all'"
```

---

## Session ID Derivation

The session ID uniquely identifies this remediation session. It is derived from the audit file name to allow multiple concurrent remediation sessions for different audit files.

```
SESSION_ID = "FIX-" + basename(AUDIT_FILE).replace(".md", "")

Examples:
  Audit file: devforgeai/qa/audit/custody-chain-audit-stories-413-424.md
  Session ID: FIX-custody-chain-audit-stories-413-424

  Audit file: devforgeai/qa/audit/custody-chain-audit-EPIC-066.md
  Session ID: FIX-custody-chain-audit-EPIC-066

  Audit file: devforgeai/qa/audit/custody-chain-audit-all.md
  Session ID: FIX-custody-chain-audit-all
```

---

## Story Path Resolution

When a finding references a story or epic by ID, resolve to file path:

```
resolve_story_path(story_id):
    files = Glob(pattern="devforgeai/specs/Stories/{story_id}-*.story.md")
    IF files is empty: HALT "Story file not found for {story_id}"
    RETURN files[0]

resolve_epic_path(epic_id):
    files = Glob(pattern="devforgeai/specs/Epics/{epic_id}-*.epic.md")
    IF files is empty: HALT "Epic file not found for {epic_id}"
    RETURN files[0]
```
