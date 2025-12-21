# Sanitization Guide

Understanding data privacy protection in feedback exports.

---

## Overview

Sanitization is mandatory for all feedback exports to protect your intellectual property and sensitive project data. This guide explains what gets sanitized, what's preserved, and why.

---

## What Is Sanitization?

**Sanitization** is the process of removing or replacing sensitive project-specific data with generic placeholders, making feedback safe to share publicly or with framework maintainers.

**Goal:** Enable feedback sharing without exposing:
- Your project's story IDs (business logic)
- Your file paths (directory structure)
- Your repository names (codebase location)
- Your custom field values (project-specific data)

---

## Sanitization Rules

### Rule 1: Story ID Replacement

**What:** Replace all story IDs with sequential placeholders

**Pattern:**
```
Original Story IDs (sorted): STORY-042, STORY-101, STORY-156
Sanitized Placeholders:      STORY-001, STORY-002, STORY-003
```

**Mapping:**
- Deterministic (same ID always maps to same placeholder)
- Sequential (placeholders numbered 001, 002, 003...)
- Alphabetically sorted (ensures consistency)
- Case-sensitive (STORY-042 ≠ story-042)

**Example Content Transformation:**
```markdown
# BEFORE SANITIZATION
Successfully completed /dev STORY-042
Tests for STORY-101 are passing
Related to STORY-156 implementation

# AFTER SANITIZATION
Successfully completed /dev STORY-001
Tests for STORY-002 are passing
Related to STORY-003 implementation
```

**Why:** Story IDs may reveal business logic, feature priorities, or project scope.

---

### Rule 2: File Path Masking

**What:** Remove all file paths, replace with `{REMOVED}`

**Pattern:**
```
/home/user/my-project/src/auth/login.py     → {REMOVED}
C:\Users\Name\project\components\form.tsx   → {REMOVED}
./src/utils/helpers.py                      → {REMOVED}
```

**Detection:**
- Absolute paths (starting with / or C:\)
- Relative paths (starting with ./ or ../)
- Mixed path formats (forward slash and backslash)

**Why:** Paths reveal directory structure, technology choices, and architecture.

---

### Rule 3: Repository URL Removal

**What:** Remove repository URLs and Git remotes

**Pattern:**
```
git@github.com:mycompany/private-repo.git  → {REMOVED}
https://github.com/user/project.git        → {REMOVED}
gitlab.com:team/codebase                   → {REMOVED}
```

**Detection:**
- Git SSH URLs (git@...)
- Git HTTPS URLs (https://.../...git)
- Repository shortcuts (github.com:user/repo)

**Why:** Repository names reveal organization, project name, and codebase location.

---

### Rule 4: Custom Field Value Removal

**What:** Remove custom field values while preserving field names

**Pattern:**
```yaml
# BEFORE SANITIZATION
---
project_name: "MySecretProject"
client_id: "ACME-Corp-2025"
internal_reference: "PROJECT-ALPHA"
custom_tag: "high-priority"
---

# AFTER SANITIZATION
---
project_name: ""
client_id: ""
internal_reference: ""
custom_tag: ""
---
```

**Framework Standard Fields (PRESERVED):**
- `operation_type`, `operation_name`, `status`
- `timestamp`, `framework_version`
- `session_id`, `duration_ms`

**Custom Fields (VALUES REMOVED):**
- Any field not in framework standard list
- User-defined fields in YAML frontmatter
- Project-specific metadata

**Why:** Custom fields often contain project identifiers, client names, or internal codes.

---

### Rule 5: Project Identifier Removal

**What:** Remove project-specific identifiers and hashes

**Pattern:**
```
Project ID: abc123-def456-789  → Project ID: {REMOVED}
Hash: sha256-abcdef123456       → Hash: {REMOVED}
```

**Why:** Identifiers can be traced back to specific projects or organizations.

---

## What Is Preserved?

### Framework Metadata (Always Kept)

**Operation Information:**
- Command names (`/dev`, `/qa`, `/release`, etc.)
- Skill names (`devforgeai-development`, etc.)
- Operation types (`command`, `skill`, `subagent`)
- Execution status (`success`, `partial`, `failed`)

**Temporal Data:**
- Timestamps (when feedback was created)
- Duration (how long operation took)
- Date ranges (for filtering)

**Framework Version:**
- Framework version (`1.0.1`, etc.)
- Compatibility information
- Export format version

**Feedback Content:**
- User observations and comments
- Issue descriptions
- Suggestions for improvements
- Error messages (generic ones)
- Framework-related context

---

## Sanitization Transparency

### Manifest Documentation

Every export includes complete sanitization details in `manifest.json`:

```json
{
  "sanitization": {
    "applied": true,
    "rules_applied": [
      "story_ids_replaced_with_placeholders",
      "custom_field_values_removed",
      "project_context_removed",
      "file_paths_masked",
      "repository_urls_removed"
    ],
    "replacement_mapping": {
      "story_id_mapping": {
        "STORY-042": "STORY-001",
        "STORY-101": "STORY-002",
        "STORY-156": "STORY-003"
      },
      "masked_fields": [
        "project_name",
        "client_id",
        "repository_url"
      ],
      "preserved_fields": [
        "operation_type",
        "status",
        "timestamp",
        "framework_version"
      ]
    }
  }
}
```

**Why Transparency Matters:**
- Users understand what was changed
- Recipients know limitations of data
- Audit trail for privacy compliance
- Trust through openness

---

## Irreversibility

### Can Sanitization Be Reversed?

**NO.** Sanitization is a one-way transformation:

- Story ID mappings are deterministic but not reversible (many-to-one)
- File paths are completely removed (no recovery possible)
- Custom field values are deleted (not masked)
- Repository URLs are removed (not encrypted)

**Original Data Location:**

Your original unsanitized feedback remains in:
```
devforgeai/feedback/sessions/  ← Original, never modified
```

Exported sanitized data is in:
```
devforgeai-feedback-export-*.zip  ← Sanitized copy
```

**Best Practice:** Keep original feedback locally, share only sanitized exports.

---

## Verification

### How to Verify Sanitization Worked

**Step 1: Open the export archive**
```bash
unzip devforgeai-feedback-export-*.zip -d /tmp/verify/
```

**Step 2: Check feedback session content**
```bash
cat /tmp/verify/feedback-sessions/*.md
```

**Step 3: Verify replacements**
- Search for your project name: Should be `{REMOVED}` or absent
- Search for file paths: Should be `{REMOVED}`
- Search for story IDs: Should be STORY-001, STORY-002, etc. (not your real IDs)
- Check custom fields: Values should be empty

**Step 4: Review manifest**
```bash
cat /tmp/verify/manifest.json | jq '.sanitization'
```

Should show:
- `"applied": true`
- Complete list of rules applied
- Replacement mappings documented

---

## When Sanitization Occurs

**Export Process:**
1. Read original feedback from `devforgeai/feedback/sessions/`
2. Apply all 5 sanitization rules
3. Write sanitized content to ZIP archive
4. Document replacements in manifest
5. Leave original feedback untouched

**Timeline:**
- Export command execution: Sanitization happens
- Original feedback: Never modified
- Archive creation: Contains only sanitized data

---

## Examples

### Example 1: Development Session Feedback

**Original (unsanitized):**
```markdown
# Development Session - STORY-042

## Context
Project: MyCompany Internal Portal
Repo: git@github.com:mycompany/portal-backend.git
File: /home/dev/portal/src/authentication/oauth_handler.py

## Feedback
Encountered issue with OAuth token refresh logic.
The implementation in STORY-042 needs refactoring.
```

**Sanitized:**
```markdown
# Development Session - STORY-001

## Context
Project: {REMOVED}
Repo: {REMOVED}
File: {REMOVED}

## Feedback
Encountered issue with OAuth token refresh logic.
The implementation in STORY-001 needs refactoring.
```

**Changes Applied:**
- STORY-042 → STORY-001
- Project name → {REMOVED}
- Repository URL → {REMOVED}
- File path → {REMOVED}
- Feedback content preserved

---

### Example 2: QA Validation Feedback

**Original:**
```yaml
---
session_id: 550e8400-e29b-41d4-a716-446655440000
operation_type: command
operation_name: /qa STORY-101
status: success
project_name: "FinTech Platform"
client_code: "BANK-XYZ-2025"
---

# QA Validation - STORY-101

Coverage: 94% for /home/dev/fintech/src/payments/
```

**Sanitized:**
```yaml
---
session_id: 550e8400-e29b-41d4-a716-446655440000
operation_type: command
operation_name: /qa STORY-002
status: success
project_name: ""
client_code: ""
---

# QA Validation - STORY-002

Coverage: 94% for {REMOVED}
```

**Changes Applied:**
- STORY-101 → STORY-002
- project_name value → "" (field name preserved)
- client_code value → "" (field name preserved)
- File path → {REMOVED}
- Framework fields preserved

---

## Security Considerations

### What Sanitization Prevents

**✅ Prevents:**
- Intellectual property leakage (story IDs, features)
- Directory structure disclosure (file paths)
- Codebase location exposure (repository URLs)
- Client identification (custom field values)
- Internal project codes (identifiers)

**✅ Allows:**
- Framework issue reporting (errors, bugs)
- Workflow feedback (UX, process improvements)
- Performance observations (speed, efficiency)
- Feature suggestions (enhancements)
- Error message sharing (framework-specific)

### What Sanitization Cannot Prevent

**⚠️ User Must Still Review:**
- Feedback text content (may contain project details in prose)
- Error messages (may include project-specific data)
- Code snippets (may reveal business logic)
- Screen content descriptions (may describe proprietary features)

**Best Practice:** Review exported content before sharing, even with sanitization.

---

## Compliance

### Data Privacy Standards

**GDPR Compliance:**
- No personally identifiable information (PII) in feedback
- No customer data in exports
- Sanitization removes project identifiers
- Users control what's shared

**Intellectual Property Protection:**
- Story IDs anonymized (business logic protected)
- File paths removed (architecture protected)
- Repository names removed (codebase location protected)
- Custom fields scrubbed (proprietary data protected)

### Audit Trail

All sanitization operations are logged:
```
2025-11-11T14:30:00Z - Export with Sanitization
  Date Range: last-30-days
  Sessions: 47
  Story IDs Replaced: 12 unique IDs
  File Paths Masked: 23 paths
  Repo URLs Removed: 5 URLs
  Custom Fields Scrubbed: 8 fields
  Output: devforgeai-feedback-export-2025-11-11T14-30-00-abc12345.zip
```

---

## FAQ

**Q: Can I disable sanitization?**
A: No. User exports always apply sanitization. Only framework maintainers with special flags can export unsanitized for internal debugging.

**Q: Why is sanitization mandatory?**
A: Secure by default. Prevents accidental sharing of sensitive data.

**Q: Can I recover original data from export?**
A: No. Sanitization is irreversible. Keep original feedback in `devforgeai/feedback/sessions/` if needed.

**Q: How accurate is sanitization?**
A: 100% for pattern-based rules (story IDs, paths, URLs). Review prose content manually for context-specific data.

**Q: Does sanitization affect local feedback?**
A: No. Original feedback in `devforgeai/feedback/sessions/` is never modified.

**Q: Can I see what was sanitized?**
A: Yes. Check `manifest.json` in the export for complete replacement mappings.

**Q: Is sanitized feedback useful for debugging?**
A: Yes. Framework errors, workflow issues, and UX feedback are fully preserved. Only project-specific identifiers are removed.

---

## Related Documentation

- **Export Guide:** `export-feedback-guide.md`
- **Archive Format:** `archive-format-spec.md`
- **API Documentation:** `api-documentation.md`

---

**Last Updated:** 2025-11-11
**Version:** 1.0
**Story:** STORY-017
