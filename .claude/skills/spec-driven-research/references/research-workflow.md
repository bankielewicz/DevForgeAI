# Research Workflow Reference

Core workflow patterns for the spec-driven-research skill.

---

## Research ID Generation

### Format
- Pattern: `RESEARCH-NNN` (zero-padded 3-digit number)
- Examples: RESEARCH-001, RESEARCH-042, RESEARCH-100

### Generation Logic (Gap-Aware)

```python
existing_files = Glob("devforgeai/specs/research/RESEARCH-*.research.md")

ids = []
for file in existing_files:
    match = re.match(r"RESEARCH-(\d{3})", basename(file))
    if match:
        ids.append(int(match.group(1)))

# Gap-aware: always use max + 1 (not fill gaps)
next_id = max(ids) + 1 if ids else 1
research_id = f"RESEARCH-{next_id:03d}"
```

---

## Slug Generation

### Rules
- Lowercase the topic string
- Replace non-alphanumeric characters with hyphens
- Strip leading/trailing hyphens
- Truncate to 50 characters maximum

### Implementation

```python
import re

def generate_slug(topic):
    slug = topic.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', slug)
    slug = slug.strip('-')
    return slug[:50]
```

### Examples

| Topic | Slug |
|-------|------|
| "AWS Kiro Competitive Analysis" | `aws-kiro-competitive-analysis` |
| "React vs Vue 2026 Comparison" | `react-vs-vue-2026-comparison` |
| "Developer Frustrations with AI Coding" | `developer-frustrations-with-ai-coding` |

---

## Research Document Frontmatter Schema

```yaml
---
id: RESEARCH-NNN           # Required. Format: RESEARCH-\d{3}
title: "Research Title"     # Required. Human-readable title
category: competitive       # Required. One of: competitive|technology|market|integration|architecture
status: complete            # Required. One of: draft|in-progress|complete
created: 2026-03-18         # Required. ISO 8601 date
updated: 2026-03-18         # Required. ISO 8601 date (same as created initially)
review_by: 2026-09-14       # Required. 6 months from created date
sources_count: 15           # Required. Integer count of cited sources
related_epics: []           # Optional. List of EPIC-NNN IDs
related_stories: []         # Optional. List of STORY-NNN IDs
tags: []                    # Optional. List of keyword tags
---
```

---

## Review Date Calculation

Research documents are flagged for review 6 months (180 days) after creation:

```python
import datetime

created_date = datetime.date.today()
review_date = created_date + datetime.timedelta(days=180)
```

---

## Research Index Format

The research index at `devforgeai/specs/research/research-index.md` uses a markdown table with an insertion marker:

```markdown
# Research Index

| ID | Title | Category | Status | Created | Review By |
|----|-------|----------|--------|---------|-----------|
| RESEARCH-003 | [Latest Research](RESEARCH-003-slug.research.md) | technology | complete | 2026-03-18 | 2026-09-14 |
| RESEARCH-002 | [Second Research](RESEARCH-002-slug.research.md) | competitive | complete | 2026-02-15 | 2026-08-14 |
| RESEARCH-001 | [First Research](RESEARCH-001-slug.research.md) | market | complete | 2026-01-18 | 2026-07-17 |
<!--- INSERT NEW RESEARCH HERE --->
```

### Index Update Procedure

```python
new_row = f"| {research_id} | [{title}]({filename}) | {category_code} | complete | {created_date} | {review_date} |"

Edit(
    file_path="devforgeai/specs/research/research-index.md",
    old_string="<!--- INSERT NEW RESEARCH HERE --->",
    new_string=f"{new_row}\n<!--- INSERT NEW RESEARCH HERE --->"
)
```

New entries are inserted at the TOP of the table (newest first) via the marker.

### Initial Index Creation

If the index doesn't exist, create it:

```markdown
# Research Index

| ID | Title | Category | Status | Created | Review By |
|----|-------|----------|--------|---------|-----------|
<!--- INSERT NEW RESEARCH HERE --->
```

---

## Research Output Paths

| Artifact | Path |
|----------|------|
| Research document | `devforgeai/specs/research/{RESEARCH-ID}-{slug}.research.md` |
| Assets folder | `devforgeai/specs/research/{RESEARCH-ID}/` |
| Research index | `devforgeai/specs/research/research-index.md` |
| Phase state | `devforgeai/workflows/${RESEARCH_ID}-phase-state.json` |

---

## Immutable Research Documents

Once a research document has `status: complete`:
- Finding content should NOT be modified (immutable record)
- Only metadata updates are allowed (tags, related_epics, related_stories)
- If new findings contradict or extend existing research, create a NEW research document with cross-reference to the original
- The Change Log section at the bottom tracks all modifications

---

**Last Updated:** 2026-03-18
**Version:** 2.0 (migrated from devforgeai-research to spec-driven-research)
