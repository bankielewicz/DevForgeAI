# Phase G04: Content Generation

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G03 --to=G04 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G03 incomplete
```

## Contract

PURPOSE: For each documentation type, load the target framework document and invoke the documentation-writer subagent to generate section content. Generate Mermaid diagrams for architecture type.
REQUIRED SUBAGENTS: documentation-writer (BLOCKING)
REQUIRED ARTIFACTS: Generated section content per doc type, Mermaid diagrams (if architecture)
STEP COUNT: 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/documentation-standards.md")
Read(file_path="references/anti-aspirational-guidelines.md")
Read(file_path="references/diagram-generation-guide.md")
```

IF any Read fails: HALT -- "Phase G04 reference files not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G04.1: Derive Module Name

EXECUTE: Determine the module name for section markers using the post-generation workflow algorithm.
```
Read(file_path="references/post-generation-workflow.md")

# Module name derivation (Section 1 of post-generation-workflow.md):
# 1. From skill name if invoked by a skill
# 2. From story title (slugified)
# 3. From user input via AskUserQuestion

IF $STORY_ID provided:
    # Extract story title from story file
    module_name = slugify(story_title)  # e.g., "user-authentication"
ELSE:
    AskUserQuestion:
        Question: "What is the module/feature name for these docs?"
        Header: "Module Name"
        Options:
            - label: "Derive from project name"
              description: "Use the project directory name"
            - label: "Enter custom name"
              description: "Provide a specific module/feature name"
        multiSelect: false

Display: "Module name: {module_name}"
```
VERIFY: module_name is a non-empty string, lowercase with hyphens.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G04 --step=G04.1 --workflow=doc-gen`

---

### Step G04.2: Generate Section Content Per Doc Type

EXECUTE: For each documentation type, invoke documentation-writer subagent.
```
generated_sections = {}
skipped_types = []

FOR each doc_type in TYPES:
    target_file = OUTPUT_MAP[doc_type]

    # Read existing framework document (if it exists)
    existing_content = Read(file_path=target_file)
    # If file doesn't exist, existing_content = ""

    Task(
        subagent_type="documentation-writer",
        description="Generate {doc_type} section for {module_name}",
        prompt="Generate a SECTION (not a full document) for insertion into an existing
        framework document.

        Module: {module_name}
        Doc type: {doc_type}
        Story context:
        {documentation_context}

        Existing framework document (your section must match this voice and style):
        {existing_content}

        Section markers -- wrap your output in these exact markers:
        <!-- SECTION: {module_name} START -->
        ## {Module Display Name}
        (your content here)
        <!-- SECTION: {module_name} END -->

        Content rules (from anti-aspirational-guidelines.md):
        - No future tense for unimplemented features
        - No filler -- if nothing to say for this doc type, return SKIP
        - Problem-first headings for troubleshooting (symptom as heading, not module name)
        - Concrete examples with real values, no placeholders
        - Match the tone and depth of surrounding sections in the existing document
        - No duplicate introductions -- one sentence on what the module does, then specifics

        Return: Markdown section content wrapped in markers, OR the word SKIP"
    )

    IF subagent returned "SKIP":
        skipped_types.append(doc_type)
        Display: "  {doc_type}: SKIPPED (no content for this module)"
    ELSE:
        generated_sections[doc_type] = subagent_output
        Display: "  {doc_type}: Generated ({word_count} words)"

Display: ""
Display: "Content generation: {len(generated_sections)} sections, {len(skipped_types)} skipped"
```
VERIFY: generated_sections dict is non-empty (at least 1 section generated). If all types skipped, HALT via AskUserQuestion.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G04 --step=G04.2 --workflow=doc-gen`

---

### Step G04.3: Generate Mermaid Diagrams (Architecture Only)

EXECUTE: If architecture type is in TYPES, generate Mermaid diagrams.
```
IF "architecture" in TYPES AND "architecture" in generated_sections:
    # Extract architecture from context
    # Generate flowchart diagram
    flowchart = generate_mermaid_flowchart(documentation_context)

    # Generate sequence diagram (if API endpoints present)
    IF documentation_context.api_endpoints:
        sequence = generate_mermaid_sequence(documentation_context.api_endpoints)

    # Validate Mermaid syntax
    # Reference: references/diagram-generation-guide.md
    FOR each diagram in [flowchart, sequence]:
        errors = check_mermaid_syntax(diagram)
        IF errors:
            Display: "Diagram syntax warning: {errors}"
            Attempt auto-fix per diagram-generation-guide.md
            IF auto-fix fails:
                Display: "Manual review needed for diagram"

    # Embed diagrams into architecture section content
    generated_sections["architecture"] = embed_diagrams(
        generated_sections["architecture"],
        flowchart,
        sequence
    )
    Display: "Mermaid diagrams generated and embedded in architecture section"

ELSE:
    Display: "Architecture type not in scope -- skipping diagram generation"
```
VERIFY: If architecture in scope, diagrams embedded in section content. If not in scope, step acknowledged.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G04 --step=G04.3 --workflow=doc-gen`

---

### Step G04.4: Content Quality Pre-Check

EXECUTE: Run a preliminary quality check on all generated content before template application.
```
FOR each doc_type, content in generated_sections:
    # Check for section markers
    IF "<!-- SECTION:" not in content:
        Display: "Warning: {doc_type} missing section markers -- adding"
        content = wrap_with_markers(content, module_name)

    # Check for prohibited aspirational language
    aspirational_patterns = ["will be", "will support", "planned", "in the future",
                             "upcoming", "powerful", "robust", "seamless",
                             "easy to use", "simple", "intuitive"]
    violations = Grep(pattern=aspirational_pattern, content=content)
    IF violations:
        Display: "Warning: {doc_type} has {len(violations)} aspirational language violations"
        # Flag for Phase G08 detailed check

Display: "Content quality pre-check complete"
```
VERIFY: All sections have markers. Aspirational violations flagged (not blocking here, detailed check in G08).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G04 --step=G04.4 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G04 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G04 complete: Content Generation"
Display: "  Generated: {len(generated_sections)} sections"
Display: "  Skipped: {len(skipped_types)} types"
Display: "  Proceeding to Phase G05: Template Application"
```
