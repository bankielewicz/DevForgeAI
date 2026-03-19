# Parameter Extraction Reference

How to parse command arguments for the spec-driven-research skill.

---

## Command Syntax

```
/research [topic]                     # Start new research
/research --resume RESEARCH-NNN       # Resume existing research
/research --search "query"            # Search research documents
/research --list                      # List all research documents
/research --list --category type      # List filtered by category
```

---

## Argument Parsing

### Mode Detection Priority

Arguments are parsed in this priority order:

1. `--resume RESEARCH-NNN` -> mode = "resume", RESUME_ID = RESEARCH-NNN
2. `--search "query"` -> mode = "search", SEARCH_QUERY = query
3. `--list` -> mode = "list", CATEGORY_FILTER = args.get("--category", null)
4. `--category type` (without --list) -> mode = "list", CATEGORY_FILTER = type
5. Everything else -> mode = "new", TOPIC = remaining args joined

### Extraction Logic

```
args = command_arguments

IF "--resume" in args:
  idx = args.index("--resume")
  RESUME_ID = args[idx + 1]  # e.g., "RESEARCH-001"
  # Validate format: must match RESEARCH-\d{3}
  IF not regex_match(r"RESEARCH-\d{3}", RESUME_ID):
    HALT -- "Invalid research ID format. Expected: RESEARCH-NNN"
  mode = "resume"

ELIF "--search" in args:
  idx = args.index("--search")
  SEARCH_QUERY = args[idx + 1:]  # Everything after --search
  mode = "search"

ELIF "--list" in args:
  mode = "list"
  IF "--category" in args:
    idx = args.index("--category")
    CATEGORY_FILTER = args[idx + 1]
  ELSE:
    CATEGORY_FILTER = null

ELIF "--category" in args:
  mode = "list"
  idx = args.index("--category")
  CATEGORY_FILTER = args[idx + 1]

ELSE:
  mode = "new"
  TOPIC = " ".join(args)  # Join all args as topic string
  IF TOPIC == "":
    # Will be asked interactively in Phase 01
    TOPIC = null
```

---

## Category Code Mapping

Display labels map to internal category codes:

| Display Label | Internal Code | internet-sleuth Mode |
|---------------|---------------|---------------------|
| Competitive Analysis | `competitive` | `competitive-analysis` |
| Technology Evaluation | `technology` | `repository-archaeology` |
| Market Research | `market` | `market-intelligence` |
| Integration Planning | `integration` | `investigation` |
| Architecture Research | `architecture` | `discovery` |

### Mapping Function

```python
category_map = {
    "Competitive Analysis": "competitive",
    "Technology Evaluation": "technology",
    "Market Research": "market",
    "Integration Planning": "integration",
    "Architecture Research": "architecture"
}

# Also handle direct code input (from --category flag)
valid_codes = ["competitive", "technology", "market", "integration", "architecture"]

def normalize_category(input_value):
    if input_value in category_map:
        return category_map[input_value]
    elif input_value.lower() in valid_codes:
        return input_value.lower()
    else:
        HALT -- f"Invalid category: {input_value}. Valid: {valid_codes}"
```

---

## Research ID Format

- Pattern: `RESEARCH-NNN` (zero-padded 3-digit number)
- Examples: RESEARCH-001, RESEARCH-042, RESEARCH-100
- Storage: `devforgeai/specs/research/RESEARCH-NNN-{slug}.research.md`
- Checkpoint: `devforgeai/workflows/RESEARCH-NNN-phase-state.json`

### ID Generation (Gap-Aware)

```python
existing_files = Glob("devforgeai/specs/research/RESEARCH-*.research.md")

ids = []
for file in existing_files:
    match = re.match(r"RESEARCH-(\d{3})", basename(file))
    if match:
        ids.append(int(match.group(1)))

next_id = max(ids) + 1 if ids else 1
research_id = f"RESEARCH-{next_id:03d}"
```

This is gap-aware: if RESEARCH-001 and RESEARCH-003 exist (002 deleted), next ID is RESEARCH-004.
