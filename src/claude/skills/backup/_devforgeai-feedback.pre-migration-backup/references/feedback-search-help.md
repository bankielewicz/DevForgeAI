# feedback-search Reference: Query Formats, Filters, Pagination, Examples, Troubleshooting

Extended documentation for the /feedback-search command. Load on-demand when users need
query syntax details, pagination guidance, examples, or troubleshooting help.

---

## Query Formats

### Story ID Query
```bash
/feedback-search STORY-001
/feedback-search STORY-042
```
**Pattern:** STORY-### (case-insensitive)
**Matches:** All feedback entries for that story

### Date Range Query
```bash
/feedback-search 2025-11-01..2025-11-07
/feedback-search 2025-11-07..2025-11-07  # Single day
```
**Pattern:** YYYY-MM-DD..YYYY-MM-DD
**Matches:** Feedback within date range (inclusive)

### Operation Type Query
```bash
/feedback-search dev
/feedback-search qa
/feedback-search release
/feedback-search manual
```
**Pattern:** dev | qa | release | manual
**Matches:** Feedback from that operation type

### Keyword Query
```bash
/feedback-search "performance issue"
/feedback-search regression
/feedback-search "TDD cycle"
```
**Pattern:** Free text (max 200 chars)
**Matches:** Feedback containing keywords (case-insensitive)

---

## Filter Options

### --severity
```bash
--severity=low       # Low severity only
--severity=medium    # Medium severity only
--severity=high      # High severity only
--severity=critical  # Critical severity only
```

### --status
```bash
--status=open        # Open feedback only
--status=resolved    # Resolved feedback only
--status=archived    # Archived feedback only
```

### --limit
```bash
--limit=5            # Show 5 results per page
--limit=20           # Show 20 results per page
--limit=100          # Show 100 results per page (max: 1000)
```

### --page
```bash
--page=1             # First page (default)
--page=2             # Second page
--page=5             # Fifth page
```

---

## Pagination

**Default:** 10 results per page

**Pagination Logic:**
- Page 1: Results 1-10
- Page 2: Results 11-20
- Page N: Results (N-1)*limit+1 to N*limit

**Last Page Detection:**
- If total_matches <= page * limit → Last page (no next_page_info)
- Otherwise → next_page_info shows command for next page

**Example:**
```bash
# Search returns 47 results with limit=10
/feedback-search STORY-001

# Response shows page 1/5 (results 1-10)
# next_page_info: "Use: /feedback-search STORY-001 --page=2 to see next 10 results"

# Navigate to page 2
/feedback-search STORY-001 --page=2

# Response shows page 2/5 (results 11-20)
```

---

## Result Sorting

**Date Range Queries:** Sort by date descending (newest first)
```bash
/feedback-search 2025-11-01..2025-11-07
# Returns newest feedback first
```

**Text/Keyword Queries:** Sort by relevance
```bash
/feedback-search "performance"
# Returns most relevant matches first
```

**Story ID Queries:** Sort by date descending
```bash
/feedback-search STORY-001
# Returns newest feedback for STORY-001 first
```

---

## Performance

**Target Response Time:** <500ms for typical queries (1000 entries)

**Performance by Dataset Size:**
- Small (<100 entries): <100ms
- Medium (100-1000 entries): <500ms
- Large (1000-10000 entries): <2s

**Optimization:** Uses indexed search via feedback_index.py

---

## Examples

### Example 1: Find All Feedback for a Story
```bash
/feedback-search STORY-042
```

**Result:** All feedback entries for STORY-042, sorted by date (newest first)

### Example 2: Find High-Severity Issues
```bash
/feedback-search --severity=high --limit=20
```

**Result:** 20 most recent high-severity feedback entries

### Example 3: Find Open Issues in Date Range
```bash
/feedback-search 2025-11-01..2025-11-07 --status=open
```

**Result:** Open feedback from November 1-7, sorted by date

### Example 4: Search with Keyword
```bash
/feedback-search "test failure"
```

**Result:** Feedback containing "test failure", sorted by relevance

### Example 5: Paginate Through Large Result Set
```bash
# Get first 10 results
/feedback-search dev --limit=10 --page=1

# Get next 10 results
/feedback-search dev --limit=10 --page=2

# Get results 41-50
/feedback-search dev --limit=10 --page=5
```

---

## Troubleshooting

### Issue: No results found but feedback exists

**Symptoms:** Query returns 0 results but feedback was collected

**Cause:** Query doesn't match feedback entries

**Resolution:**
```bash
# Check what feedback exists
/feedback-search --limit=100

# Verify query format
# Story ID: STORY-001 (not Story-001, story-001)
# Date: YYYY-MM-DD (not MM/DD/YYYY, DD-MM-YYYY)
```

### Issue: Search performance slow (>2s)

**Symptoms:** Search takes >2 seconds to return results

**Cause:** Large feedback dataset (>10,000 entries)

**Resolution:**
```bash
# Narrow query with filters
/feedback-search STORY-001 --limit=10  # Instead of broad query

# Use date ranges
/feedback-search 2025-11-01..2025-11-07  # Instead of all-time search

# Archive old feedback (via config)
/feedback-config edit retention_days 30  # Auto-archive old entries
```

### Issue: Pagination shows wrong page count

**Symptoms:** "Page 3/2" displayed when should be "Page 2/2"

**Cause:** Beyond last page

**Resolution:** System handles gracefully, shows empty results for pages beyond last page
