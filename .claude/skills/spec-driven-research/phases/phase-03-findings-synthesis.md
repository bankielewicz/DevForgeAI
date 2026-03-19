# Phase 03: Findings Synthesis

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=02 --to=03 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 03 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 02 not complete |

## Contract

- **PURPOSE:** Validate, structure, and enrich research findings for documentation
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** `references/citation-standards.md`
- **REQUIRED ARTIFACTS:** Findings, recommendations, and sources from Phase 02
- **STEP COUNT:** 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-research/references/citation-standards.md")
```

IF Read fails: HALT -- "citation-standards.md reference missing"

---

## Mandatory Steps (4)

### Step 3.1: Validate Output Structure

**EXECUTE:**
```
# Check that Phase 02 produced the required output sections
required_sections = ["findings", "recommendations", "sources"]
missing = []

IF findings is empty or None:
  missing.append("findings")
IF recommendations is empty or None:
  missing.append("recommendations")
IF sources is empty or None:
  missing.append("sources")

IF missing:
  Display: f"Output missing sections: {missing}"
  Display: "Attempting to extract from raw research output..."

  # Re-parse the research output more aggressively
  FOR section in missing:
    extracted = attempt_extraction(raw_output, section)
    IF extracted:
      assign(section, extracted)
      Display: f"  Recovered {section} from raw output"
    ELSE:
      Display: f"  Could not recover {section} - will be marked as gap"

ELSE:
  Display: "Research output validated - all required sections present"
```

**VERIFY:**
At minimum, `findings` is non-empty. Recommendations and sources may have gaps but findings is required.
IF findings still empty after recovery: HALT -- "No findings available for synthesis"

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=03 --step=3.1 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.1")`

---

### Step 3.2: Theme Extraction

**EXECUTE:**
```
# Group findings by theme/similarity
# When internet-sleuth was used, findings may already be grouped.
# When fallback search was used, manual grouping is needed.

themes = {}

FOR each finding in findings:
  # Identify the primary theme/concept
  theme = identify_theme(finding)

  IF theme in themes:
    themes[theme].append(finding)
  ELSE:
    themes[theme] = [finding]

Display: f"Organized {len(findings)} findings into {len(themes)} themes:"
FOR theme_name, theme_findings in themes.items():
  Display: f"  - {theme_name}: {len(theme_findings)} finding(s)"
```

**VERIFY:**
`themes` dictionary is populated with at least 1 theme.
Each theme has at least 1 finding.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=03 --step=3.2 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.2")`

---

### Step 3.3: Insight Extraction

**EXECUTE:**
```
insights = []

# 1. Cross-cutting patterns (connections between themes)
theme_names = list(themes.keys())
FOR i, theme_A in enumerate(theme_names):
  FOR theme_B in theme_names[i+1:]:
    connection = find_connection(themes[theme_A], themes[theme_B])
    IF connection:
      insights.append({
        "type": "cross-cutting",
        "themes": [theme_A, theme_B],
        "insight": connection
      })

# 2. Contradictions (conflicting findings)
FOR i, finding_A in enumerate(findings):
  FOR finding_B in findings[i+1:]:
    IF contradicts(finding_A, finding_B):
      insights.append({
        "type": "contradiction",
        "findings": [finding_A, finding_B],
        "insight": "Conflicting information - requires deeper investigation"
      })

# 3. Gaps (unanswered research questions)
FOR question in questions:
  answered = check_if_answered(question, findings)
  IF not answered:
    insights.append({
      "type": "gap",
      "question": question,
      "insight": "Research question not fully answered - may need additional investigation"
    })

Display: f"Extracted {len(insights)} insights:"
Display: f"  Cross-cutting patterns: {count_type(insights, 'cross-cutting')}"
Display: f"  Contradictions: {count_type(insights, 'contradiction')}"
Display: f"  Knowledge gaps: {count_type(insights, 'gap')}"
```

**VERIFY:**
Insight extraction was attempted. `insights` list exists (may be empty if no patterns found).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=03 --step=3.3 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.3")`

---

### Step 3.4: Format for Template

**EXECUTE:**
```
# Format findings for research template (see citation-standards.md for formats)

# Format each finding with evidence and confidence
formatted_findings = ""
FOR i, finding in enumerate(findings):
  formatted_findings += f"""
### Finding {i+1}: {finding.title}

{finding.description}

**Evidence:**
{format_evidence(finding.evidence)}

**Implications for DevForgeAI:**
{format_implications(finding.implications)}

**Confidence Level:** {finding.confidence}
{finding.confidence_justification}

"""

# Format recommendations with priority
formatted_recommendations = ""
FOR i, rec in enumerate(recommendations):
  formatted_recommendations += f"""
### Recommendation {i+1}: {rec.action} [{rec.priority}]

**Rationale:** {rec.rationale}
**Effort:** {rec.effort}
**Dependencies:** {rec.dependencies or "None"}

"""

# Format sources per citation-standards.md
formatted_sources = ""
FOR source in sources:
  formatted_sources += format_source_citation(source) + "\n"

Display: "Findings formatted for research template"
Display: f"  Formatted findings: {len(findings)}"
Display: f"  Formatted recommendations: {len(recommendations)}"
Display: f"  Formatted sources: {len(sources)}"
```

**VERIFY:**
`formatted_findings`, `formatted_recommendations`, and `formatted_sources` are all non-empty strings.
IF any empty: Display warning but do not HALT (partial research is still valuable).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=03 --step=3.4 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.4")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=03 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["03"].status = "completed"`
- `progress.phases_completed.append("03")`
- `progress.current_phase = 4`
- `progress.total_steps_completed += 4`

Write updated checkpoint to disk. Verify via `Glob()`.
