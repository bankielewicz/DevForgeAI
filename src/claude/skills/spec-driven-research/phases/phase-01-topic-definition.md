# Phase 01: Topic Definition

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=00 --to=01 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 01 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - previous phase not complete |

## Contract

- **PURPOSE:** Define research topic, category, questions, and check for duplicates
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/parameter-extraction.md`
- **REQUIRED ARTIFACTS:** Checkpoint JSON must exist from Phase 00
- **STEP COUNT:** 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-research/references/parameter-extraction.md")
```

IF Read fails: HALT -- "parameter-extraction.md reference missing"

---

## Mandatory Steps (4)

### Step 1.1: Research Topic

**EXECUTE:**
```
AskUserQuestion:
  Question: "What is the research topic?"
  Header: "Topic"
  Options:
    - label: "New topic"
      description: "Start fresh research on a new subject"
    - label: "Expand existing research"
      description: "Add findings to an existing RESEARCH-NNN document"

IF "Expand existing":
  expand_id = AskUserQuestion:
    Question: "Which research ID to expand? (e.g., RESEARCH-001)"
    Header: "Expand"

  research_files = Glob(pattern=f"devforgeai/specs/research/{expand_id}-*.research.md")
  IF research_files:
    Read(file_path=research_files[0])
    Display: "Loaded {expand_id}. New findings will be appended."
    mode = "expand"
  ELSE:
    HALT -- "Research {expand_id} not found"

IF "New topic":
  IF $TOPIC already provided from command args:
    topic = $TOPIC
  ELSE:
    topic = AskUserQuestion:
      Question: "Enter the research topic:"
      Header: "Topic"
```

**VERIFY:**
`topic` variable is populated (non-empty string) OR mode is "expand" with valid expand_id.
IF neither: HALT -- "No topic defined"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=01 --step=1.1 --project-root=. 2>&1
```
Update checkpoint: `input.topic = topic`, `phases["01"].steps_completed.append("1.1")`

---

### Step 1.2: Category Selection

**EXECUTE:**
```
AskUserQuestion:
  Question: "What category does this research fall under?"
  Header: "Category"
  Options:
    - label: "Competitive Analysis"
      description: "Competitor features, pricing, positioning, strengths/weaknesses"
    - label: "Technology Evaluation"
      description: "Libraries, frameworks, tools - capabilities, performance, adoption"
    - label: "Market Research"
      description: "Industry trends, developer needs, statistics, pain points"
    - label: "Integration Planning"
      description: "External services, APIs, SDKs - integration requirements"
    - label: "Architecture Research"
      description: "Design patterns, best practices, architectural styles, case studies"

# Map display label to internal code (see parameter-extraction.md)
category_map = {
    "Competitive Analysis": "competitive",
    "Technology Evaluation": "technology",
    "Market Research": "market",
    "Integration Planning": "integration",
    "Architecture Research": "architecture"
}

category_code = category_map[selected_category]
```

**VERIFY:**
`category_code` is one of: competitive, technology, market, integration, architecture.
IF not: HALT -- "Invalid category selection"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=01 --step=1.2 --project-root=. 2>&1
```
Update checkpoint: `input.category = category_code`, `phases["01"].steps_completed.append("1.2")`

---

### Step 1.3: Research Questions

**EXECUTE:**
```
questions = []

approach = AskUserQuestion:
  Question: "How would you like to define research questions?"
  Header: "Questions"
  Options:
    - label: "Enter interactively (Recommended)"
      description: "Add questions one by one - helps focus the research"
    - label: "Provide later"
      description: "Define questions as research progresses"

IF "Enter interactively":
  LOOP:
    q = AskUserQuestion:
      Question: f"Enter research question #{len(questions) + 1} (or type 'done' when finished):"
      Header: f"Question {len(questions) + 1}"

    IF q.lower() == "done" OR q.lower() == "'done'":
      BREAK

    questions.append(q)

  Display: f"Captured {len(questions)} research questions"

ELSE:
  Display: "Questions will be defined during research execution"
```

**VERIFY:**
`questions` is a list (may be empty if user chose "Provide later").
Display count of captured questions.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=01 --step=1.3 --project-root=. 2>&1
```
Update checkpoint: `input.questions = questions`, `phases["01"].steps_completed.append("1.3")`

---

### Step 1.4: Duplicate Detection

**EXECUTE:**
```
# Extract keywords from topic
keywords = topic.split()  # Simple keyword extraction
significant_keywords = [k for k in keywords if len(k) > 3]  # Filter short words

# Search existing research
similar_research = []

FOR keyword in significant_keywords[:5]:  # Check top 5 keywords
  matches = Grep(
    pattern=keyword,
    path="devforgeai/specs/research/",
    glob="*.research.md",
    output_mode="files_with_matches",
    -i=true
  )
  similar_research.extend(matches)

# Deduplicate
similar_research = unique(similar_research)

IF len(similar_research) > 0:
  Display: "Similar research found:"
  FOR each research_file in similar_research:
    Read(file_path=research_file, limit=15)  # Read frontmatter
    Display: f"  - {id}: {title} ({category})"

  action = AskUserQuestion:
    Question: "How would you like to proceed?"
    Header: "Duplicate Check"
    Options:
      - label: "Continue with new research"
        description: "Topics are different enough to warrant separate research"
      - label: "Resume existing research"
        description: "Add findings to the existing document instead"
      - label: "Cancel"
        description: "Research not needed at this time"

  IF action == "Resume existing":
    selected_id = AskUserQuestion:
      Question: "Which research ID to resume?"
      Header: "Resume"
    # Restart with resume mode
    HALT -- "User chose to resume {selected_id}. Re-run with: /research --resume {selected_id}"

  ELIF action == "Cancel":
    Display: "Research cancelled by user"
    EXIT skill

ELSE:
  Display: "No similar research found - proceeding with new research"
```

**VERIFY:**
Duplicate check was executed (either similar_research found and user chose to continue, or no duplicates found).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=01 --step=1.4 --project-root=. 2>&1
```
Update checkpoint: `phases["01"].steps_completed.append("1.4")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=01 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["01"].status = "completed"`
- `progress.phases_completed.append("01")`
- `progress.current_phase = 2`
- `progress.total_steps_completed += 4`

Write updated checkpoint to disk. Verify via `Glob()`.
