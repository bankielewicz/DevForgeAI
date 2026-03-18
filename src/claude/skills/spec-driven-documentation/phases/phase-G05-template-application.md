# Phase G05: Template Application & Customization

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G04 --to=G05 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G04 incomplete
```

## Contract

PURPOSE: Load base templates (custom or default), apply project-specific customizations from coding-standards.md, populate template variables with generated content.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Fully populated template content ready for integration
STEP COUNT: 3 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/template-customization.md")
```

IF Read fails: HALT -- "Phase G05 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G05.1: Load Templates

EXECUTE: For each doc type with generated content, load the appropriate template.
```
templates = {}

FOR each doc_type in generated_sections.keys():
    # Check for custom template first
    custom_path = "devforgeai/templates/documentation/{doc_type}-template.md"
    default_path = "assets/templates/{doc_type}-template.md"

    custom_exists = Glob(pattern=custom_path)
    IF custom_exists:
        templates[doc_type] = Read(file_path=custom_path)
        Display: "  {doc_type}: Custom template loaded"
    ELSE:
        # Map doc_type to template filename
        template_map = {
            "api": "api-docs-template.md",
            "architecture": "architecture-template.md",
            "developer-guide": "developer-guide-template.md",
            "troubleshooting": "troubleshooting-template.md",
            "roadmap": "roadmap-template.md",
            "readme": "readme-template.md",
            "contributing": "contributing-template.md",
            "changelog": "changelog-template.md"
        }
        template_file = template_map.get(doc_type, "{doc_type}-template.md")
        templates[doc_type] = Read(file_path="assets/templates/{template_file}")
        Display: "  {doc_type}: Default template loaded"

Display: "Templates loaded: {len(templates)}"
```
VERIFY: templates dict has same keys as generated_sections (every generated type has a template).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G05 --step=G05.1 --workflow=doc-gen`

---

### Step G05.2: Apply Coding Standards Customizations

EXECUTE: Read coding-standards.md and apply style preferences to templates.
```
Read(file_path="devforgeai/specs/context/coding-standards.md")

# Extract documentation-related preferences:
# - Heading styles (ATX vs Setext)
# - Code block formatting (language tags, line limits)
# - Example structure (inline vs collapsible)
# - Tone and voice (formal/informal)
# - Naming conventions

FOR each doc_type, template in templates:
    # Apply heading style
    # Apply code block conventions
    # Apply tone adjustments

Display: "Coding standards applied to all templates"
```
VERIFY: Templates modified according to coding-standards.md preferences. No context file violation.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G05 --step=G05.2 --workflow=doc-gen`

---

### Step G05.3: Populate Template Variables

EXECUTE: Substitute template variables with actual values from documentation context.
```
# Common variables across all templates
variables = {
    "{{project_name}}": extract from context or package.json/Cargo.toml/pyproject.toml,
    "{{project_description}}": extract from story or README,
    "{{tech_stack}}": from tech-stack.md,
    "{{installation_steps}}": generate from dependencies.md,
    "{{usage_examples}}": from acceptance criteria,
    "{{api_endpoints}}": from documentation_context.api_endpoints,
    "{{architecture_diagram}}": from generated Mermaid diagrams,
    "{{version}}": from git tags or package manifest
}

FOR each doc_type, template in templates:
    FOR each variable, value in variables:
        template = template.replace(variable, value)

    # Handle conditional sections
    FOR each conditional section in template:
        IF condition met (e.g., API endpoints exist):
            Include section
        ELSE:
            Remove section placeholder

    templates[doc_type] = template

Display: "Template variables populated for {len(templates)} types"
```
VERIFY: No unresolved `{{variable}}` patterns remain in any template. All placeholders replaced or removed.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G05 --step=G05.3 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G05 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G05 complete: Template Application & Customization"
Display: "  Templates populated: {len(templates)}"
Display: "  Proceeding to Phase G06: Section Integration"
```
