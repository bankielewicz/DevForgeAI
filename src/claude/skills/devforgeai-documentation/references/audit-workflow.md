# Documentation Audit Workflow Reference

This reference defines the 8-phase methodology for the `/document --audit` mode. The skill executes these phases sequentially when `AUDIT_MODE` is set.

---

## Phase A.0: Discovery

**Goal:** Build a complete inventory of what exists before forming opinions.

### Step 1: Inventory documentation files

```
docs_files = Glob("docs/**/*.md")
root_md_files = Glob("*.md")  # README.md, CHANGELOG.md, CONTRIBUTING.md, etc.
```

Record each file: path, approximate size (line count via Grep for `\n`).

### Step 2: Read entry points

Read these files in full (they define navigation):
- `README.md`
- `docs/README.md` (if exists)
- `docs/index.md` (if exists)
- Any file named `*INDEX*` or `*index*` in docs/

### Step 3: Inventory community-standard files

Check existence of each. Record `true`/`false`:

| File | Check |
|------|-------|
| `LICENSE` or `LICENSE-MIT` + `LICENSE-APACHE` | Glob at root |
| `CONTRIBUTING.md` | Read at root |
| `CODE_OF_CONDUCT.md` | Read at root |
| `SECURITY.md` | Read at root |
| `.github/ISSUE_TEMPLATE/bug_report.md` | Glob in .github/ |
| `.github/ISSUE_TEMPLATE/feature_request.md` | Glob in .github/ |
| `.github/PULL_REQUEST_TEMPLATE.md` | Read in .github/ |
| `.github/FUNDING.yml` | Read in .github/ |

### Step 4: Check configuration alignment

Read the project manifest (`Cargo.toml`, `package.json`, or `pyproject.toml`):
- Extract `license` field → compare to LICENSE file and README License section
- Extract MSRV / `rust-version` / `engines.node` → compare to README Prerequisites
- Extract `version` → compare to README status line and CHANGELOG

Record all discrepancies as findings.

**Output:** `inventory` object for doc-audit.json.

---

## Phase A.1: Analysis

**Goal:** Score documentation quality across 4 dimensions with specific evidence.

### Dimension 1: Tone & Personality (score 1-10)

Evaluate by reading README.md first 30 lines and CONTRIBUTING.md (if exists):

| Check | Evidence Method | Finding if fails |
|-------|----------------|-----------------|
| Opening line explains WHY not just WHAT | Read README line 1-5 | `tone:readme_opening` |
| Value proposition present | Search for "why", problem statement, or elevator pitch | `tone:readme_opening` |
| Contributing language is welcoming | Read CONTRIBUTING.md or Contributing section | `tone:contributing_gatekeeping` |
| Human voice present (we/you pronouns) | Grep for "\\bwe\\b\|\\byou\\b\|\\byour\\b" in README | `tone:no_human_voice` |
| Troubleshooting has empathetic language | Grep for "common\|don't worry\|most frequent" in troubleshooting files | `tone:clinical_troubleshooting` |
| FAQ answers explain rationale, not just facts | Read FAQ sections for "because\|rationale\|reason" | `tone:faq_warmup` |

### Dimension 2: Information Architecture (score 1-10)

| Check | Evidence Method | Finding if fails |
|-------|----------------|-----------------|
| No duplicate filenames across directories | Compare basenames of all docs files | `architecture:duplicate_files` |
| Scope is clear (no version/product confusion) | Check for mixed version refs in same file | `architecture:scope_confusion` |
| Navigation index exists (docs/README.md) | Check if docs/README.md or docs/index.md exists | `architecture:missing_nav` |
| Cross-references present between related docs | Grep for relative links in each doc | `architecture:no_crosslinks` |
| Audience routing exists (user/contributor/maintainer) | Search index for audience-based paths | `architecture:no_audience_routing` |
| No over-documented modules (>3 files for one module) | Count files per docs subdirectory | `architecture:module_overdoc` |
| README is under 250 lines | Count README lines | `onboarding:readme_bloat` |

### Dimension 3: Visual Design & Formatting (score 1-10)

| Check | Evidence Method | Finding if fails |
|-------|----------------|-----------------|
| GFM admonitions used | Grep for `> \[!NOTE\]\|> \[!WARNING\]\|> \[!TIP\]\|> \[!IMPORTANT\]` | `formatting:missing_admonitions` |
| README badges present | Grep for `\[!\[` (badge markdown) in README | `formatting:missing_badges` |
| CHANGELOG follows Keep a Changelog categories | Grep for `### Added\|### Changed\|### Fixed\|### Security` | `formatting:changelog_flat` |
| Tables have visual grouping (subheaders between groups) | Manual: check tables >10 rows for `---` breaks | `formatting:wall_of_tables` |
| Oversized files identified (>50KB) | Check file sizes from inventory | `formatting:oversized_file` |

### Dimension 4: Onboarding Friction (score 1-10)

| Check | Evidence Method | Finding if fails |
|-------|----------------|-----------------|
| Install steps in first 50 lines of README | Grep for "install\|cargo build\|npm install\|pip install" in README lines 1-50 | `onboarding:buried_install` |
| Quick Start / first command narrative exists | Grep for "quick start\|getting started\|your first" (case-insensitive) | `onboarding:missing_quickstart` |
| Prerequisites consistent across docs | Compare prerequisites in README vs developer guide | `onboarding:prerequisite_mismatch` |
| LICENSE present and stated | Check community file inventory | `license:missing` |
| MSRV/version matches config | Check discrepancy list from A.0 | `onboarding:msrv_mismatch` |

**Scoring formula:** Start at 10. Subtract points per finding:
- CRITICAL finding: -3
- HIGH finding: -2
- MEDIUM finding: -1
- LOW finding: -0.5

Floor at 1 (never score 0).

**Output:** `scorecard` object for doc-audit.json.

---

## Phase A.2: Prioritization

**Goal:** Classify each finding by severity and assign fix metadata.

### Severity classification rules

| Severity | Criteria |
|----------|----------|
| CRITICAL | Legally blocks usage (missing LICENSE) or makes project appear abandoned/hostile |
| HIGH | Causes repeated user confusion or friction (duplicates, missing CONTRIBUTING, no Quick Start) |
| MEDIUM | Reduces polish or discoverability (missing admonitions, badges, scope banners) |
| LOW | Nice-to-have improvement (tone warmup, FAQ personality, table grouping) |

### Fix mode classification

| fix_mode | Criteria |
|----------|----------|
| `automated` | Deterministic, single-file creation or text insertion. No judgment needed. Safe to apply without user review. |
| `interactive` | Requires user approval: content rewrites, file deletions, structural reorganization, legal choices. |

Reference `audit-fix-catalog.md` for the complete mapping of finding type → fix action → fix mode.

### Finding ID assignment

Assign sequential IDs: F-001, F-002, ... ordered by severity (CRITICAL first, then HIGH, MEDIUM, LOW).

**Output:** `findings` array for doc-audit.json.

---

## Phase A.3: Output

**Goal:** Write the structured audit file.

Write to: `devforgeai/qa/audit/doc-audit.json`

Schema:
```json
{
  "version": "1.0",
  "generated": "<ISO-8601 timestamp>",
  "project_root": "<absolute path>",
  "scorecard": {
    "<dimension>": { "score": <int>, "max": 10, "key_blocker": "<string>" }
  },
  "findings": [
    {
      "id": "F-NNN",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "type": "<category>:<specific>",
      "affected": ["<file paths>"],
      "summary": "<one-line description>",
      "evidence": "<file:line or quoted text>",
      "remediation": "<what fix does>",
      "fix_mode": "automated|interactive",
      "fix_action": "<action key from fix catalog>"
    }
  ],
  "inventory": {
    "docs_files": ["<paths>"],
    "community_files": { "<name>": true|false },
    "orphaned_files": ["<paths>"],
    "duplicate_groups": [{ "scope": "<name>", "files": ["<paths>"] }]
  },
  "fix_sessions": []
}
```

Ensure the `devforgeai/qa/audit/` directory exists before writing.

---

## Phase A.4: Display

**Goal:** Present audit results to the user.

### Display format:

```
## Documentation Audit Results

### Scorecard
| Dimension | Score | Key Blocker |
|-----------|-------|-------------|
| Tone & Personality | 3/10 | README opens with spec, not pitch |
| Information Architecture | 4/10 | Duplicate docs, no navigation |
| Visual Design | 6/10 | No admonitions or badges |
| Onboarding Friction | 5/10 | No Quick Start, LICENSE missing |

### Findings Summary
| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| HIGH | 5 |
| MEDIUM | 8 |
| LOW | 3 |

### Top Findings
| ID | Severity | Type | Summary |
|----|----------|------|---------|
| F-001 | CRITICAL | license:missing | No LICENSE file |
| F-002 | CRITICAL | tone:readme_opening | README has no value proposition |
| ... | ... | ... | ... |

### Next Steps
- Run `/document --audit-fix --type=all` to apply all fixes
- Run `/document --audit-fix --type=license` to fix license only
- Run `/document --audit-fix --finding=F-001` to fix a single finding

Audit file saved to: devforgeai/qa/audit/doc-audit.json
```

---

## Orphan Detection Algorithm (used in Phase A.1 and Phase B.4)

```
entry_points = [README.md, docs/README.md, docs/MODULE-INDEX.md, ...]  # all index files
all_docs = Glob("docs/**/*.md")
referenced = Set()

FOR each entry_point:
    content = Read(entry_point)
    FOR each file in all_docs:
        basename = file.name
        IF basename appears in content OR relative_path appears in content:
            referenced.add(file)

# Transitive pass: check if referenced files link to unreferenced files
FOR each file in referenced:
    content = Read(file)
    FOR each unreferenced_file in (all_docs - referenced):
        IF unreferenced_file.name appears in content:
            referenced.add(unreferenced_file)

orphaned = all_docs - referenced
```

Report orphaned files as `architecture:orphaned_file` findings.

---

## Verification Checklist (Phase B.4)

After fixes are applied, verify:

1. **Link integrity:** Every file in docs/ is reachable from at least one entry point (re-run orphan detection)
2. **Fact consistency:** MSRV, prerequisites, version numbers match across all docs (re-run config alignment check)
3. **Community files complete:** All files in community checklist exist
4. **README length:** Under 250 lines
5. **No new orphans:** Consolidation/restructuring didn't create new unreferenced files
