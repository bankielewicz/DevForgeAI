# Search and List Mode Reference

Handling for conditional branches in Phase 00 (Steps 0.2 and 0.3).

Both search and list modes exit the skill after Phase 00. No Phase 01-06 execution is needed.

---

## Search Mode (Step 0.2)

**Triggered by:** `/research --search "query"`

### Procedure

```
1. Grep research files for matching content:

   results = Grep(
     pattern=SEARCH_QUERY,
     path="devforgeai/specs/research/",
     glob="*.research.md",
     output_mode="files_with_matches",
     -i=true
   )

2. IF no results:
     Display: f'No research documents matching "{SEARCH_QUERY}"'
     Display: ""
     Display: "Tips:"
     Display: "  - Try broader search terms"
     Display: "  - Use /research --list to browse all research"
     Display: "  - Use /research --list --category competitive to filter"
     EXIT skill

3. FOR each result file:
     Read(file_path=result, limit=15)  # Read YAML frontmatter only
     Extract: id, title, category, status, created

4. Display results table:

   Search Results for "{SEARCH_QUERY}"

   | ID | Title | Category | Status | Created |
   |----|-------|----------|--------|---------|
   | RESEARCH-001 | Title Here | competitive | complete | 2026-01-18 |
   | RESEARCH-003 | Another Title | technology | complete | 2026-02-15 |

   Found {count} research documents matching "{SEARCH_QUERY}"

   Quick Actions:
     /research --resume RESEARCH-001    # Open specific research
     /research --search "other term"    # Search again

5. EXIT skill
```

### Frontmatter Parsing

Extract metadata from YAML frontmatter (lines between `---` markers):

```yaml
---
id: RESEARCH-001
title: "AWS Kiro Competitive Analysis"
category: competitive
status: complete
created: 2026-01-18
---
```

---

## List Mode (Step 0.3)

**Triggered by:** `/research --list` or `/research --list --category type`

### Procedure

```
1. Load all research files:

   all_research = Glob("devforgeai/specs/research/RESEARCH-*.research.md")

2. IF no research files found:
     Display: "No research documents found."
     Display: ""
     Display: "Start your first research:"
     Display: '  /research "Your Research Topic"'
     EXIT skill

3. FOR each research file:
     Read(file_path=file, limit=15)  # Read YAML frontmatter only
     Extract: id, title, category, status, created, review_by

4. IF CATEGORY_FILTER is not null:
     Filter results where category == CATEGORY_FILTER
     IF no results after filter:
       Display: f'No research documents in category "{CATEGORY_FILTER}"'
       Display: ""
       Display: "Available categories: competitive, technology, market, integration, architecture"
       Display: "Use /research --list to see all research"
       EXIT skill

5. Display results table:

   Research Documents {IF CATEGORY_FILTER: f"(Category: {CATEGORY_FILTER})"}

   | ID | Title | Category | Status | Created | Review By |
   |----|-------|----------|--------|---------|-----------|
   | RESEARCH-003 | Latest Research | technology | complete | 2026-03-18 | 2026-09-14 |
   | RESEARCH-002 | Second Research | competitive | complete | 2026-02-15 | 2026-08-14 |
   | RESEARCH-001 | First Research | market | complete | 2026-01-18 | 2026-07-17 |

   Total: {count} research documents

   Quick Actions:
     /research --resume RESEARCH-001           # Open specific research
     /research --search "keyword"              # Search by content
     /research --list --category competitive   # Filter by category
     /research "New Topic"                     # Start new research

6. EXIT skill
```

### Category Filter Values

| Valid Filter | Matches |
|-------------|---------|
| `competitive` | Competitive Analysis research |
| `technology` | Technology Evaluation research |
| `market` | Market Research |
| `integration` | Integration Planning research |
| `architecture` | Architecture Research |

---

## Exit Behavior

Both search and list modes exit the skill cleanly after displaying results:

1. Do NOT create a checkpoint JSON (no long-running workflow)
2. Do NOT run CLI gates (no phase transitions)
3. Do NOT proceed to Phase 01
4. Display results and return control to user

This is NOT phase skipping - it is conditional flow by design. Search and list are utility operations that don't need the full 7-phase research workflow.
