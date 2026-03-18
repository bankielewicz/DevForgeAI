# Brownfield Map Integration

**Purpose:** Integrate Treelint repository map generation into the designing-systems skill for brownfield analysis of existing codebases.

**Version:** 1.0
**Story:** STORY-373

---

## Overview

When the designing-systems skill operates in brownfield mode on an existing codebase, it queries the Treelint repository map to identify the most important symbols. This enables context-efficient discovery of the codebase structure without reading every file.

---

## Integration with Project-Context-Discovery Phase

During the project-context-discovery phase of the architecture skill, the following steps integrate the repository map:

### Step 1: Detect Brownfield Mode

When the architecture skill is invoked on an existing codebase (brownfield analysis), it detects that source files already exist. This triggers the repository map query to understand the codebase structure.

### Step 2: Query Repository Map

Execute the TreelintRepositoryMapService to generate a ranked symbol map:

```bash
treelint map --ranked --format json
```

For complete command documentation, parsing guidance, error handling, and fallback chain details, see the primary reference: `treelint-repository-map.md` in `implementing-stories/references/`.

### Step 3: Extract Top 50 Symbols

From the full map result, extract the top 50 symbols by rank (K=50 default). These represent the most-referenced functions, classes, and modules in the codebase.

### Step 4: Generate Key Symbols Section

Include the extracted symbols in the architecture analysis output as a **Key Symbols** section.

---

## Key Symbols Output Format

The architecture analysis output includes a Key Symbols section listing the top symbols with their types and reference counts:

### Key Symbols

| Name | Type | References |
|------|------|------------|
| validateInput | function | 142 |
| UserService | class | 98 |
| handleRequest | method | 76 |
| DatabaseConnection | class | 64 |
| formatResponse | function | 52 |
| ... | ... | ... |

**Columns:**
- **Name** - Symbol identifier (function name, class name, etc.)
- **Type** - Symbol type (function, class, method, variable)
- **References** - Number of references across the codebase

---

## Using Key Symbols for Architecture Analysis

The ranked symbol data informs architecture decisions:

1. **Technology Detection** - If top symbols include React component classes, the architecture analysis identifies React as a frontend framework
2. **Architectural Pattern Recognition** - Concentration of symbols in specific modules reveals layered architecture, MVC, or microservice patterns
3. **Dependency Hotspots** - Symbols with high reference counts indicate core dependencies that constrain architecture decisions
4. **Module Importance** - Files containing highly-ranked symbols are the most critical to understand first

---

## Error Handling

If the repository map query fails (Treelint unavailable, empty codebase, or stale index), the architecture skill continues with standard file-based discovery. The map integration is an enhancement, not a hard requirement.

For the complete error handling specification including the 3-tier fallback chain (daemon -> CLI -> Grep), see `treelint-repository-map.md`.

---

## References

- **Primary Reference:** `implementing-stories/references/treelint-repository-map.md` (TreelintRepositoryMapService documentation)
- **Architecture Skill:** `designing-systems/SKILL.md` (Phase 1: Project Context Discovery)
- **Brownfield Integration:** `designing-systems/references/brownfield-integration.md` (General brownfield workflow)
- **STORY-373:** Integrate Repository Map Generation via Treelint map
