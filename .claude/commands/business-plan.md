---
description: Generate a business plan with optional codebase context enrichment
argument-hint: [--standalone] flag to force standalone mode
model: sonnet
---

# /business-plan - Dual-Mode Business Plan Generation

Generate a structured business plan using the planning-business skill. Automatically detects whether you are in a DevForgeAI project (project-anchored mode) or working without context (standalone mode). Output format is consistent regardless of mode.

---

## Quick Reference

```bash
# Auto-detect mode (project-anchored if context exists, standalone otherwise)
/business-plan

# Force standalone mode even inside a DevForgeAI project
/business-plan --standalone
```

---

## Command Workflow

### Phase 0: Argument Parsing and Mode Detection

**Step 0.1: Parse $ARGUMENTS for --standalone flag**

```
STANDALONE_FLAG = false

FOR arg in $ARGUMENTS:
    IF arg == "--standalone":
        STANDALONE_FLAG = true

IF STANDALONE_FLAG == true:
    Display: "Mode override: --standalone flag detected — force standalone mode, skip detection"
    Display: "Flag overrides auto-detection of project context"
```

**Step 0.2: Mode Detection — Detect Project Context**

```
IF STANDALONE_FLAG == true:
    # Override: ignore context directory, force standalone mode
    SET MODE = "standalone"
    Display: "Mode: Standalone (override via --standalone flag)"
ELSE:
    # Auto-detect: check if devforgeai/specs/context/ directory exists
    context_check = Glob(pattern="devforgeai/specs/context/*.md")

    IF context_check is not empty:
        SET MODE = "project-anchored"
        Display: "Mode: Project-Anchored (devforgeai/specs/context/ detected)"
    ELSE:
        # No context directory found — without devforgeai context, use standalone mode
        SET MODE = "standalone"
        Display: "Mode: Standalone (no devforgeai/specs/context/ detected)"
```

---

### Phase 1: Context Collection

#### Project-Anchored Mode

When MODE == "project-anchored", read codebase context files to enrich the business plan with project-specific technical data. The project-anchored mode passes context to the planning-business skill.

**Step 1.1: Read Context Files with Graceful Degradation**

Each context file is checked individually. If a file does not exist or is empty, log a warning for the missing file and proceed with available context. The command does not halt on missing individual files — it uses graceful degradation to skip missing files and continue.

```
CONTEXT_DATA = {}
CONTEXT_FILES = [
    "devforgeai/specs/context/tech-stack.md",
    "devforgeai/specs/context/source-tree.md",
    "devforgeai/specs/context/architecture-constraints.md",
    "devforgeai/specs/context/dependencies.md",
    "devforgeai/specs/context/coding-standards.md",
    "devforgeai/specs/context/anti-patterns.md"
]

FOR each file_path in CONTEXT_FILES:
    result = Read(file_path=file_path)
    # Explicit reads for each context file:
    # Read(file_path="devforgeai/specs/context/tech-stack.md")
    # Read(file_path="devforgeai/specs/context/source-tree.md")
    # Read(file_path="devforgeai/specs/context/architecture-constraints.md")
    # Read(file_path="devforgeai/specs/context/dependencies.md")
    # Read(file_path="devforgeai/specs/context/coding-standards.md")
    # Read(file_path="devforgeai/specs/context/anti-patterns.md")

    IF file exists and is not empty:
        CONTEXT_DATA[file_path] = result
        Display: "  ✓ Loaded: {file_path}"
    ELSE:
        # Warning: missing file — proceed without it (fallback behavior)
        Display: "  ⚠️ Warning: {file_path} missing or empty — proceeding without it"
        # Graceful degradation: do not fail, continue with partial context

loaded_count = len(CONTEXT_DATA)
total_count = len(CONTEXT_FILES)

IF loaded_count == 0:
    Display: "⚠️ Warning: No context files available — falling back to standalone mode with default context"
    SET MODE = "standalone"
ELSE:
    Display: "Loaded {loaded_count}/{total_count} context files for project-anchored business plan"
```

#### Standalone Mode

When MODE == "standalone", there is no project context available. Prompt the user for a business idea description via AskUserQuestion.

**Step 1.2: Collect Business Idea from User**

```
# Standalone mode requires a business idea description input
AskUserQuestion(questions=[{
    question: "Describe your business idea for the business plan. What problem does it solve and who is the target market?",
    header: "Business Idea",
    options: [
        {label: "I'll type my business idea description", description: "Provide a detailed business idea for plan generation"},
        {label: "Generate from scratch", description: "Start with guided questions from the planning-business skill"}
    ],
    multiSelect: false
}])

SET BUSINESS_IDEA = user_response
Display: "Business idea collected — proceeding to plan generation"
```

---

### Phase 2: Invoke Planning-Business Skill

Both project-anchored and standalone modes invoke the same planning-business skill to ensure consistent output format and structure. The only difference is input richness — project-anchored mode includes codebase context, standalone mode includes the user's business idea description.

**Step 2.1: Skill Invocation**

```
IF MODE == "project-anchored":
    # Project-anchored: planning-business skill receives codebase context via conversation
    Display: "Invoking planning-business skill with project context (project-anchored mode)..."
    Display: "Context: ${loaded_count} context files loaded for enrichment"
    Skill(command="planning-business")

ELIF MODE == "standalone":
    # Standalone: planning-business skill receives business idea via conversation context
    Display: "Invoking planning-business skill with business idea (standalone mode)..."
    Display: "Business idea: ${BUSINESS_IDEA}"
    Skill(command="planning-business")
```

**Step 2.2: Output Format (Consistent Across Modes)**

The planning-business skill produces the same output sections regardless of mode. Output sections include business model analysis, revenue streams, market assessment, and viability scoring.

```
# Consistent output format regardless of mode:
# 1. Lean Canvas (9 blocks)
# 2. Business Model Analysis
# 3. Revenue Model
# 4. Market Viability Assessment
# 5. Milestone Plan
#
# The skill handles output format — this command does not modify output structure.
```

---

## Error Handling

**Missing context directory:** Falls back to standalone mode automatically.

**Missing individual context files:** Warning logged, proceeds with available context (graceful degradation).

**No business idea in standalone mode:** HALT — standalone mode requires business idea input. Cannot proceed without it.

**Planning-business skill unavailable:** Display error with suggestion to check skill installation.

---

## Notes

- Mode detection uses native Glob tool (not Bash) per tech-stack.md constraints
- Context file reading uses native Read tool per coding-standards.md
- The --standalone flag is useful for expert users who want to skip context injection even when inside a DevForgeAI project
