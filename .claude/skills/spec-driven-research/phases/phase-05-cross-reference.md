# Phase 05: Cross-Reference

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${RESEARCH_ID} --workflow=research --from=04 --to=05 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Proceed to Phase 05 |
| 127 | CLI not installed - proceed without enforcement |
| Other | HALT - Phase 04 not complete |

## Contract

- **PURPOSE:** Link research to existing epics, stories, and ADRs for bidirectional traceability
- **REQUIRED SUBAGENTS:** none
- **REQUIRED REFERENCES:** none (self-contained logic)
- **REQUIRED ARTIFACTS:** Research document path from Phase 04 checkpoint
- **STEP COUNT:** 2 mandatory steps

---

## Mandatory Steps (2)

### Step 5.1: Epic/Story Linking

**EXECUTE:**
```
link_choice = AskUserQuestion:
  Question: "Should this research be linked to existing epics, stories, or ADRs?"
  Header: "Cross-Reference"
  Options:
    - label: "Link to epics/stories"
      description: "This research informs epic planning or story implementation"
    - label: "Link to ADRs"
      description: "This research supports architecture decisions"
    - label: "No linking needed"
      description: "Standalone research - no cross-references required"

IF "Link to epics/stories":
  epic_ids_raw = AskUserQuestion:
    Question: "Enter epic or story IDs to link (comma-separated, e.g., EPIC-001, STORY-045):"
    Header: "Link IDs"

  link_ids = parse_csv(epic_ids_raw)

  FOR each link_id in link_ids:
    # Determine if epic or story
    IF link_id.startswith("EPIC"):
      target_files = Glob(pattern=f"devforgeai/specs/Epics/{link_id}*.epic.md")
    ELIF link_id.startswith("STORY"):
      target_files = Glob(pattern=f"devforgeai/specs/Stories/{link_id}*.story.md")
    ELSE:
      Display: f"  Skipping {link_id} - unrecognized ID format"
      CONTINUE

    IF target_files:
      target_file = target_files[0]
      Read(file_path=target_file)

      # Add research reference to the target file's References section
      reference_line = f"- Research: [{RESEARCH_ID}: {topic}](../research/{filename})"

      # Try to add under ## References section
      IF file contains "## References":
        Edit(
          file_path=target_file,
          old_string="## References",
          new_string=f"## References\n\n{reference_line}"
        )
        Display: f"  Linked {RESEARCH_ID} -> {link_id}"
      ELSE:
        Display: f"  {link_id} has no ## References section - add link manually"

      # Update research doc with backlink
      IF link_id.startswith("EPIC"):
        # Update related_epics in research doc frontmatter
        Read(file_path=output.research_file_path)
        Edit(
          file_path=output.research_file_path,
          old_string="related_epics: []",
          new_string=f"related_epics: [{link_id}]"
        )
    ELSE:
      Display: f"  {link_id} not found - skipping"

ELIF "Link to ADRs":
  # Will be handled in Step 5.2
  Display: "ADR linking will be handled in Step 5.2"

ELSE:
  Display: "No cross-references needed - standalone research"
```

**VERIFY:**
Cross-reference decision was made (user responded to AskUserQuestion).
IF linking was chosen, verify at least one link was created successfully or documented as skipped.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=05 --step=5.1 --project-root=. 2>&1
```
Update checkpoint: `output.epics_linked = [linked_ids]`, `phases["05"].steps_completed.append("5.1")`

---

### Step 5.2: ADR Integration [CONDITIONAL]

**EXECUTE:**
```
IF category_code == "technology":
  # Technology research may recommend new technology adoption
  # Check if recommendations suggest technologies not in tech-stack.md

  new_tech_detected = false
  FOR rec in recommendations:
    IF rec suggests new library, framework, or tool adoption:
      new_tech_detected = true
      BREAK

  IF new_tech_detected:
    Display: """
Technology Research Alert

This research recommends adopting new technology.
Per DevForgeAI rules, new technologies require an Architecture Decision Record (ADR).

The ADR should document:
  - Decision to adopt (or not)
  - Alternatives considered
  - Rationale (citing this research)
  - Consequences
"""

    create_adr = AskUserQuestion:
      Question: "Create ADR for this technology decision?"
      Header: "ADR"
      Options:
        - label: "Yes, create ADR now"
          description: "Opens /create-context to create ADR referencing this research"
        - label: "Create ADR later"
          description: "I'll create it manually when ready"
        - label: "Not needed"
          description: "No technology adoption decision is being made"

    IF "Yes, create ADR now":
      Display: f"To create the ADR, run: /create-epic --adr (and reference {RESEARCH_ID})"
      # Note: We don't invoke the skill directly to avoid nested skill invocation
      checkpoint.output.adr_created = "pending"
    ELIF "Create ADR later":
      Display: f"Remember to reference {RESEARCH_ID} when creating the ADR"
      checkpoint.output.adr_created = "deferred"
    ELSE:
      checkpoint.output.adr_created = false

  ELSE:
    Display: "No new technology adoption detected - ADR not needed"
    checkpoint.output.adr_created = false

ELIF link_choice == "Link to ADRs":
  # Non-technology research linking to existing ADRs
  adr_ids = AskUserQuestion:
    Question: "Enter ADR IDs to link (comma-separated, e.g., ADR-001, ADR-015):"
    Header: "ADR Link"

  FOR adr_id in parse_csv(adr_ids):
    adr_files = Glob(pattern=f"devforgeai/specs/adrs/{adr_id}*.md")
    IF adr_files:
      Display: f"  Linked {RESEARCH_ID} -> {adr_id}"
    ELSE:
      Display: f"  {adr_id} not found - skipping"

ELSE:
  Display: "ADR integration: not applicable for this research"
  checkpoint.output.adr_created = false
```

**VERIFY:**
ADR integration step was executed (even if result was "not applicable").

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${RESEARCH_ID} --workflow=research --phase=05 --step=5.2 --project-root=. 2>&1
```
Update checkpoint: `phases["05"].steps_completed.append("5.2")`

---

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${RESEARCH_ID} --workflow=research --phase=05 --checkpoint-passed --project-root=. 2>&1
```

Update checkpoint:
- `phases["05"].status = "completed"`
- `progress.phases_completed.append("05")`
- `progress.current_phase = 6`
- `progress.total_steps_completed += 2`

Write updated checkpoint to disk. Verify via `Glob()`.
