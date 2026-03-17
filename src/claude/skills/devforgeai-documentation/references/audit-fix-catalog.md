# Documentation Audit Fix Action Catalog

This catalog defines every fix action available in Phase B (Documentation Fix). Each finding type maps to exactly one fix action with a classification of `automated` or `interactive`.

**Rule:** Automated fixes execute without user approval. Interactive fixes require AskUserQuestion confirmation before each change.

---

## Fix Actions by Category

### License

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `license:missing` | `create_dual_license` | interactive | Create LICENSE-MIT + LICENSE-APACHE at project root. Requires AskUserQuestion for license choice (MIT, Apache 2.0, dual MIT/Apache, other). |
| `license:cargo_toml` | `add_cargo_license` | automated | Add `license = "MIT OR Apache-2.0"` to `[package]` section of Cargo.toml. Adapts to chosen license from `license:missing` fix. |
| `license:readme_section` | `update_readme_license` | automated | Replace README.md License section with correct license text and links to LICENSE files. |

### Community Files

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `community:contributing` | `create_contributing` | automated | Generate CONTRIBUTING.md from `contributing-audit-template.md` with variable substitution ({{project_name}}, {{test_command}}, {{lint_command}}, {{format_command}}). |
| `community:security` | `create_security` | automated | Generate SECURITY.md from `security-template.md` with variable substitution ({{project_name}}, {{security_model}}, {{crypto_deps}}). |
| `community:code_of_conduct` | `create_code_of_conduct` | automated | Generate CODE_OF_CONDUCT.md from `code-of-conduct-template.md`. |
| `community:issue_templates` | `create_issue_templates` | automated | Create `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md` from templates. Creates directory if missing. |
| `community:pr_template` | `create_pr_template` | automated | Create `.github/PULL_REQUEST_TEMPLATE.md` from `pr-template.md` template. |

### Tone & Personality

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `tone:readme_opening` | `rewrite_readme_intro` | interactive | Generate new README opening with value proposition, tagline, and problem statement. Show before/after diff. Requires user approval of new text. |
| `tone:contributing_gatekeeping` | `warm_contributing` | interactive | Rewrite Contributing section/file with welcoming language. Show before/after. Requires approval. |
| `tone:no_human_voice` | `add_human_voice` | interactive | Add we/you pronouns and conversational phrasing to specified files. Show before/after per file. |
| `tone:clinical_troubleshooting` | `warm_troubleshooting` | interactive | Add empathetic language to troubleshooting entries ("This is the most common issue..."). Show changes per section. |
| `tone:faq_warmup` | `warm_faq` | interactive | Rewrite FAQ answers to explain rationale, not just state facts. Show before/after per answer. |

### Information Architecture

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `architecture:duplicate_files` | `add_scope_banners` | automated | Insert `> **Scope:** This document covers...` blockquote after H1 in each duplicate, linking to its counterpart. |
| `architecture:scope_confusion` | `add_scope_banners` | automated | Same action as duplicate_files — scope banners disambiguate. |
| `architecture:missing_nav` | `create_docs_index` | interactive | Generate docs/README.md navigation page with audience-based routing. Requires user review of navigation structure. |
| `architecture:no_crosslinks` | `add_crosslinks` | automated | Insert "See also:" links at bottom of related docs based on topic overlap detection. |
| `architecture:no_audience_routing` | `create_docs_index` | interactive | Same action as missing_nav — the index page provides audience routing. |
| `architecture:module_overdoc` | `consolidate_module_docs` | interactive | Merge N module files into single consolidated doc. Show merge plan. Requires user approval before file deletion. |
| `architecture:orphaned_file` | `delete_orphan` | interactive | Delete file with no inbound references. List each orphan with its superseding file (if any). Requires per-file confirmation. |

### Visual Design & Formatting

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `formatting:missing_admonitions` | `insert_admonitions` | automated | Scan for key patterns (WARNING-worthy: immutable, forbidden, required; TIP-worthy: shortcuts, commands; NOTE-worthy: common issues, expected behavior; IMPORTANT-worthy: security, compile-time enforcement) and wrap matching paragraphs in GFM admonition blocks. |
| `formatting:missing_badges` | `insert_badges` | automated | Insert badge row after H1 in README. Detect: CI badge from .github/workflows/*.yml, license badge from LICENSE files, MSRV from Cargo.toml rust-version, test count from README/CHANGELOG mentions, unsafe-forbidden from lib.rs. |
| `formatting:changelog_flat` | `restructure_changelog` | interactive | Reorganize [Unreleased] section into Keep a Changelog categories (Added, Changed, Fixed, Security, Documentation). Requires user review since classification is judgmental. |
| `formatting:wall_of_tables` | `group_tables` | automated | Insert `---` visual breaks and subheader rows in tables with >10 rows, grouping by detected category patterns. |
| `formatting:oversized_file` | `flag_oversized` | interactive | Report file size and recommend splitting strategy. No automatic action — structural decisions need user input. |
| `formatting:oversized_toc` | `expand_toc` | automated | Generate comprehensive Table of Contents with category groupings, replacing existing minimal ToC. |

### Onboarding Friction

| Finding Type | Fix Action Key | Mode | Description |
|---|---|---|---|
| `onboarding:missing_quickstart` | `create_quickstart` | interactive | Generate Quick Start section for README with install → init → verify flow. Requires user approval since it involves project-specific commands. |
| `onboarding:buried_install` | `move_install_up` | interactive | Restructure README to place install steps in top 50 lines. Requires approval since it reorders sections. |
| `onboarding:prerequisite_mismatch` | `fix_prerequisites` | automated | Update doc files to match values from project manifest (Cargo.toml, package.json). Deterministic: source of truth is the manifest. |
| `onboarding:msrv_mismatch` | `fix_msrv` | automated | Update all docs referencing old MSRV to match `rust-version` from Cargo.toml. Grep and replace. |
| `onboarding:readme_bloat` | `extract_readme_sections` | interactive | Move large sections (>100 lines) from README to docs/ files, replacing with a link. Requires user approval for which sections to extract. |

---

## Execution Rules

### Automated Fix Execution

1. Read the target file
2. Apply the transformation (insert, replace, create)
3. Write the result
4. Log: `"Applied {fix_action_key} to {file_path}"`

### Interactive Fix Execution

1. Generate the proposed change
2. Display before/after diff (or new file preview for creation)
3. AskUserQuestion with options:
   - **"Apply"** — execute the fix
   - **"Edit first"** — user provides modified text, then apply
   - **"Skip"** — mark finding as deferred, move to next
4. If applied, log: `"Applied {fix_action_key} to {file_path} (user approved)"`
5. If skipped, log: `"Skipped {fix_action_key} for {finding_id} (user deferred)"`

### Template Variable Resolution

When generating files from templates, resolve variables from these sources (priority order):

1. **Project manifest** (`Cargo.toml` / `package.json`): `{{project_name}}`, `{{version}}`, `{{license}}`
2. **Git config**: `{{author}}`, `{{repo_url}}`
3. **Detected values**: `{{test_command}}` (from scripts or Makefile), `{{msrv}}` (from rust-version)
4. **User input** (via AskUserQuestion): `{{contact_email}}`, any unresolvable variable
5. **Fallback defaults**: `{{project_name}}` = directory name, `{{license}}` = "MIT OR Apache-2.0"

---

## Fix Session Recording

After all fixes in a batch, append to `doc-audit.json`:

```json
{
  "fix_sessions": [
    {
      "timestamp": "2026-03-12T...",
      "type_filter": "all",
      "findings_processed": 18,
      "automated_applied": 12,
      "interactive_applied": 4,
      "skipped": 2,
      "details": [
        { "id": "F-001", "action": "create_dual_license", "status": "applied" },
        { "id": "F-005", "action": "warm_faq", "status": "skipped", "reason": "user deferred" }
      ]
    }
  ]
}
```

On subsequent runs, findings already `"applied"` in a previous session are skipped (resume capability).
