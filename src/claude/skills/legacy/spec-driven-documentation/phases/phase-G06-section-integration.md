# Phase G06: Section-Level Integration

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=G05 --to=G06 --workflow=doc-gen
# Exit 0: proceed | Exit 1: Phase G05 incomplete
```

## Contract

PURPOSE: Insert or update generated sections into fixed framework documentation files using HTML comment markers for idempotency. Track all updated files.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Framework files updated with module sections, updated_files tracking map
STEP COUNT: 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/post-generation-workflow.md")
```

IF Read fails: HALT -- "Phase G06 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step G06.1: Ensure Target Directories Exist

EXECUTE: Create target directories if they don't exist.
```
target_dirs = ["docs/api", "docs/architecture", "docs/guides"]

FOR each dir in target_dirs:
    Glob(pattern="{dir}/*")
    IF directory does not exist:
        Bash(command="mkdir -p {dir}")
        Display: "  Created: {dir}/"

Display: "Target directories verified"
```
VERIFY: All target directories exist (docs/api/, docs/architecture/, docs/guides/).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G06 --step=G06.1 --workflow=doc-gen`

---

### Step G06.2: Read Target Framework Files

EXECUTE: Read each target file that will receive section insertions.
```
# Section Insertion Map (from post-generation-workflow.md Section 2)
OUTPUT_MAP = {
    "api": "docs/api/API.md",
    "architecture": "docs/architecture/ARCHITECTURE.md",
    "developer-guide": "docs/guides/DEVELOPER-GUIDE.md",
    "troubleshooting": "docs/guides/TROUBLESHOOTING.md",
    "roadmap": "docs/guides/ROADMAP.md"
}

target_contents = {}

FOR each doc_type in generated_sections.keys():
    target_path = OUTPUT_MAP[doc_type]
    content = Read(file_path=target_path)

    IF Read fails (file doesn't exist):
        # Create empty framework file with header
        initial_content = "# {doc_type_title}\n\nProject documentation.\n\n---\n"
        Write(file_path=target_path, content=initial_content)
        target_contents[doc_type] = initial_content
        Display: "  {target_path}: Created (new file)"
    ELSE:
        target_contents[doc_type] = content
        Display: "  {target_path}: Loaded ({len(content)} chars)"

Display: "Target files loaded: {len(target_contents)}"
```
VERIFY: target_contents has same keys as generated_sections. All target files readable.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G06 --step=G06.2 --workflow=doc-gen`

---

### Step G06.3: Insert or Update Sections

EXECUTE: For each generated section, use HTML comment markers for idempotent insertion/update.
```
updated_files = {}

FOR each doc_type, section_content in generated_sections:
    target_path = OUTPUT_MAP[doc_type]
    existing = target_contents[doc_type]

    MARKER_START = "<!-- SECTION: {module_name} START -->"
    MARKER_END = "<!-- SECTION: {module_name} END -->"

    IF MARKER_START in existing:
        # UPDATE existing section (idempotent)
        # Extract old block from MARKER_START to MARKER_END (inclusive)
        old_block = extract_between(existing, MARKER_START, MARKER_END, inclusive=true)
        Edit(file_path=target_path, old_string=old_block, new_string=section_content)
        Display: "  Updated: {module_name} section in {target_path}"
    ELSE:
        # INSERT new section
        # Append before final --- separator or at end of file
        # Preserve user-authored content (<!-- USER CONTENT START/END -->)
        IF "---" at end of existing:
            insert_before = last "---" in existing
            Edit(file_path=target_path,
                 old_string=insert_before,
                 new_string=section_content + "\n\n---")
        ELSE:
            # Append to end
            new_content = existing + "\n\n" + section_content
            Write(file_path=target_path, content=new_content)
        Display: "  Added: {module_name} section to {target_path}"

    updated_files[doc_type] = target_path

Display: ""
Display: "Section integration: {len(updated_files)} files updated"
```
VERIFY: updated_files dict is non-empty. Each target file contains the MARKER_START pattern for module_name.
```
FOR each doc_type, path in updated_files:
    content = Read(file_path=path)
    IF "<!-- SECTION: {module_name} START -->" not in content:
        HALT: "Section marker not found in {path} after integration"
```
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G06 --step=G06.3 --workflow=doc-gen`

---

### Step G06.4: Calculate Word Counts

EXECUTE: Count words in each updated section for the completion summary.
```
word_counts = {}

FOR each doc_type, path in updated_files:
    content = Read(file_path=path)
    MARKER_START = "<!-- SECTION: {module_name} START -->"
    MARKER_END = "<!-- SECTION: {module_name} END -->"

    section = extract_between(content, MARKER_START, MARKER_END)
    word_count = len(section.split())
    word_counts[doc_type] = word_count
    Display: "  {doc_type}: {word_count} words"

Display: "Word counts calculated for all sections"
```
VERIFY: word_counts dict populated for all updated doc types.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=G06 --step=G06.4 --workflow=doc-gen`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=G06 --checkpoint-passed --workflow=doc-gen
```

## Phase Transition Display

```
Display: "Phase G06 complete: Section Integration"
Display: "  Files updated: {len(updated_files)}"
Display: "  Proceeding to Phase G07: Post-Generation Integration"
```
