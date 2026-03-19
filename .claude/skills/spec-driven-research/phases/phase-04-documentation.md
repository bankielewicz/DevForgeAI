# Phase 04: Documentation

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=03 --to=04 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 04 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 03 not complete |

## Contract

- **PURPOSE:** Write structured research document, create assets folder, update research index
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/research-workflow.md`
- **REQUIRED ARTIFACTS:** Formatted findings, recommendations, sources from Phase 03
- **STEP COUNT:** 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-research/references/research-workflow.md")
```

IF Read fails: HALT -- "research-workflow.md reference missing"

---

## Mandatory Steps (5)

### Step 4.1: Load Template

**EXECUTE:**
```
template = Read(file_path="src/claude/skills/spec-driven-research/assets/templates/research-template.md")
```

**VERIFY:**
Template content was loaded successfully. Contains expected sections: Executive Summary, Research Questions, Key Findings, Recommendations, Sources, Related Work, Change Log.
IF Read fails: HALT -- "Research template not found at assets/templates/research-template.md"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=04 --step=4.1 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.1")`

---

### Step 4.2: Populate Template

**EXECUTE:**
```
# Calculate dates
import datetime
created_date = datetime.date.today().isoformat()
review_date = (datetime.date.today() + datetime.timedelta(days=180)).isoformat()

# Generate executive summary (2-3 sentences synthesizing key findings)
executive_summary = generate_summary(findings, max_sentences=3)

# Format research questions as numbered list
questions_md = ""
FOR i, q in enumerate(questions):
  questions_md += f"{i+1}. {q}\n"
IF questions_md == "":
  questions_md = "Research was conducted broadly without specific pre-defined questions."

# Extract tags from topic and findings
tags = extract_tags(topic, category_code, findings)

# Fill template
document = template
document = replace(document, "{research_id}", RESEARCH_ID)
document = replace(document, "{title}", topic)
document = replace(document, "{category}", category_code)
document = replace(document, "{status}", "complete")
document = replace(document, "{created_date}", created_date)
document = replace(document, "{updated_date}", created_date)
document = replace(document, "{review_date}", review_date)
document = replace(document, "{sources_count}", str(len(sources)))
document = replace(document, "{executive_summary}", executive_summary)
document = replace(document, "{research_questions}", questions_md)
document = replace(document, "{findings}", formatted_findings)
document = replace(document, "{recommendations}", formatted_recommendations)
document = replace(document, "{sources}", formatted_sources)
document = replace(document, "{related_work}", "No related work linked yet.")

# Update tags in frontmatter
document = replace(document, "tags: []", f"tags: [{', '.join(tags)}]")
```

**VERIFY:**
`document` string is populated with no remaining `{placeholder}` tokens.
IF placeholders remain: Display warning and fill with "[TO BE COMPLETED]"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=04 --step=4.2 --project-root=. 2>&1
```
Update checkpoint: `phases["04"].steps_completed.append("4.2")`

---

### Step 4.3: Write Research Document

**EXECUTE:**
```
# Generate slug from topic (see research-workflow.md for slug rules)
slug = topic.lower()
slug = re.sub(r'[^a-z0-9]+', '-', slug)
slug = slug.strip('-')[:50]  # Max 50 chars

# Full filename
filename = f"{RESEARCH_ID}-{slug}.research.md"
filepath = f"devforgeai/specs/research/{filename}"

# Ensure research directory exists
Bash(command="mkdir -p devforgeai/specs/research/")

# Write file
Write(file_path=filepath, content=document)

Display: f"Research document created: {filepath}"
```

**VERIFY:**
```
verification = Glob(pattern=f"devforgeai/specs/research/{RESEARCH_ID}-*.research.md")
IF not verification:
  HALT -- "Research document was NOT written to disk"
ELSE:
  Display: f"Verified: {filepath} exists on disk"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=04 --step=4.3 --project-root=. 2>&1
```
Update checkpoint: `output.research_file_path = filepath`, `phases["04"].steps_completed.append("4.3")`

---

### Step 4.4: Create Assets Folder

**EXECUTE:**
```
assets_dir = f"devforgeai/specs/research/{RESEARCH_ID}/"

Bash(command=f"mkdir -p {assets_dir}")

Display: f"""
Assets folder created: {assets_dir}

You can add:
  - Screenshots: {RESEARCH_ID}/screenshot-*.png
  - Diagrams: {RESEARCH_ID}/diagram-*.svg
  - PDFs: {RESEARCH_ID}/document-*.pdf

Reference in research doc:
  ![Screenshot]({RESEARCH_ID}/screenshot-name.png)
  [PDF]({RESEARCH_ID}/document-name.pdf)
"""
```

**VERIFY:**
Assets directory exists (it was just created via mkdir -p, which is idempotent).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=04 --step=4.4 --project-root=. 2>&1
```
Update checkpoint: `output.assets_folder = assets_dir`, `phases["04"].steps_completed.append("4.4")`

---

### Step 4.5: Update Research Index

**EXECUTE:**
```
index_path = "devforgeai/specs/research/research-index.md"

# Check if index exists
index_exists = Glob(pattern=index_path)

IF not index_exists:
  # Create initial index
  initial_index = """# Research Index

| ID | Title | Category | Status | Created | Review By |
|----|-------|----------|--------|---------|-----------|
<!--- INSERT NEW RESEARCH HERE --->
"""
  Write(file_path=index_path, content=initial_index)
  Display: "Created new research index"

# Read current index
Read(file_path=index_path)

# Create new row
new_row = f"| {RESEARCH_ID} | [{topic}]({filename}) | {category_code} | complete | {created_date} | {review_date} |"

# Insert before marker
Edit(
  file_path=index_path,
  old_string="<!--- INSERT NEW RESEARCH HERE --->",
  new_string=f"{new_row}\n<!--- INSERT NEW RESEARCH HERE --->"
)

Display: "Research index updated"
```

**VERIFY:**
```
# Verify the index contains our new entry
index_check = Grep(
  pattern=RESEARCH_ID,
  path=index_path,
  output_mode="content"
)
IF not index_check:
  HALT -- "Research index was NOT updated with {RESEARCH_ID}"
ELSE:
  Display: f"Verified: {RESEARCH_ID} appears in research index"
```

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=04 --step=4.5 --project-root=. 2>&1
```
Update checkpoint: `output.index_updated = true`, `phases["04"].steps_completed.append("4.5")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=04 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["04"].status = "completed"`
- `progress.phases_completed.append("04")`
- `progress.current_phase = 5`
- `progress.total_steps_completed += 5`

Write updated checkpoint to disk. Verify via `Glob()`.
