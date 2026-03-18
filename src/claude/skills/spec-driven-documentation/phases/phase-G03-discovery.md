# Phase G03: Discovery & Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=02 --to=G03 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Load story files (greenfield) or invoke code-analyzer subagent (brownfield), extract technical specifications, load context files for reference, identify documentation gaps.
REQUIRED SUBAGENTS: code-analyzer (CONDITIONAL, brownfield only)
REQUIRED ARTIFACTS: Documentation context loaded with technical specs, API endpoints, features
STEP COUNT: 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
IF $MODE == "greenfield":
    Read(file_path="references/greenfield-workflow.md")
ELIF $MODE == "brownfield":
    Read(file_path="references/brownfield-analysis.md")
```

IF Read fails: HALT -- "Phase G03 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G03.1: Load Story Files (Greenfield) OR Invoke Code Analyzer (Brownfield)

EXECUTE:
```
IF $MODE == "greenfield":
    IF $STORY_ID provided:
        stories = [Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")]
    ELSE:
        all_stories = Glob(pattern="devforgeai/specs/Stories/*.story.md")
        stories = filter by status IN ["Dev Complete", "QA Approved", "Released"]

    IF stories is empty:
        HALT: "No completed stories found. Nothing to document."

    Display: "Loaded {len(stories)} story file(s) for documentation"

ELIF $MODE == "brownfield":
    Task(
        subagent_type="code-analyzer",
        description="Analyze codebase for documentation",
        prompt="Analyze the codebase to extract:
        - Architecture pattern (MVC, Clean, DDD, Layered)
        - Layer structure (presentation, application, domain, infrastructure)
        - Public APIs (classes, functions, endpoints)
        - Entry points (main files, startup)
        - Dependencies (external, internal)
        - Key workflows (user flows, data flows)

        Return structured JSON with code metadata."
    )

    Display: "Codebase analysis complete (code-analyzer subagent)"
```
VERIFY: For greenfield: stories array is non-empty. For brownfield: code-analyzer returned structured JSON.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G03 --step=G03.1 --workflow=doc-gen`

---

### Step G03.2: Extract Technical Specifications

EXECUTE: Extract documentation-relevant content from stories or codebase analysis.
```
documentation_context = {
    features: [],
    api_endpoints: [],
    configuration: [],
    architecture_decisions: [],
    troubleshooting_items: []
}

IF $MODE == "greenfield":
    FOR each story in stories:
        Read(file_path=story)
        Extract from story:
            - User story text -> features
            - Acceptance criteria -> features
            - Technical specification -> api_endpoints, configuration
            - API endpoints section -> api_endpoints
            - Non-functional requirements -> configuration

ELIF $MODE == "brownfield":
    # Use code-analyzer output
    Extract from analysis JSON:
        - public_apis -> api_endpoints
        - architecture_pattern -> architecture_decisions
        - entry_points -> features
        - dependencies -> configuration

Display: "Extracted: {len(features)} features, {len(api_endpoints)} API endpoints"
```
VERIFY: documentation_context has at least one non-empty array (features, api_endpoints, or configuration).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G03 --step=G03.2 --workflow=doc-gen`

---

### Step G03.3: Load Context Files for Reference

EXECUTE: Read the 3 context files most relevant to documentation generation.
```
Read(file_path="devforgeai/specs/context/tech-stack.md")
Read(file_path="devforgeai/specs/context/source-tree.md")
Read(file_path="devforgeai/specs/context/coding-standards.md")

Display: "Context files loaded: tech-stack, source-tree, coding-standards"
```
VERIFY: All 3 Read operations succeed.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G03 --step=G03.3 --workflow=doc-gen`

---

### Step G03.4: Discover Existing Documentation (Brownfield)

EXECUTE: If brownfield mode, discover and categorize existing documentation.
```
IF $MODE == "brownfield":
    existing_docs = Glob(pattern="**/*.md")
    # Filter to documentation files (README, CONTRIBUTING, API, etc.)
    # Exclude: story files, ADRs, context files, skill files

    categorized = {
        readme: [],
        api_docs: [],
        developer_guide: [],
        troubleshooting: [],
        other: []
    }

    FOR each doc in existing_docs:
        Read(file_path=doc)
        Categorize by content/filename patterns
        Add to appropriate category

    Display: "Existing docs: {counts per category}"

    # Identify gaps
    gap_report = compare(categorized, expected_doc_types)
    Display: "Documentation gaps: {gap_report}"

ELIF $MODE == "greenfield":
    Display: "Greenfield mode: Skipping existing doc discovery"
```
VERIFY: If brownfield, categorized map populated. If greenfield, step acknowledged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G03 --step=G03.4 --workflow=doc-gen`

---

### Step G03.5: Compile Documentation Context Summary

EXECUTE: Compile a summary of all discovered content for subsequent phases.
```
context_summary = {
    mode: $MODE,
    story_count: len(stories) if greenfield else 0,
    feature_count: len(documentation_context.features),
    api_count: len(documentation_context.api_endpoints),
    types_to_generate: TYPES,
    existing_docs: categorized if brownfield else {},
    gaps: gap_report if brownfield else {}
}

Display: ""
Display: "Discovery Summary:"
Display: "  Mode: {$MODE}"
Display: "  Features: {feature_count}"
Display: "  API endpoints: {api_count}"
Display: "  Types to generate: {TYPES}"
Display: ""
```
VERIFY: context_summary object is populated with all required fields.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G03 --step=G03.5 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G03 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G03 complete: Discovery & Analysis"
Display: "  Proceeding to Phase G04: Content Generation"
```
