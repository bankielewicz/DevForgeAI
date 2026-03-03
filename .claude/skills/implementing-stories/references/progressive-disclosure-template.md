# Progressive Task Disclosure Template

This template defines the standard structure for all "Optional Captures" sections in phase files (phases 01-10). All 12 phase files must follow this exact order and structure for consistency.

## Standard Section Order

Every phase file should end with these sections in this exact order:

### 1. Validation Checkpoint
- List pre-exit requirements (checkboxes)
- Define HALT conditions
- Reference RCA-003 for AC checklist verification if applicable

### 2. Pre-Exit Checklist
- Detailed checklist of all mandatory/conditional items
- Include "N/A justification" escape clause
- HALT if unchecked items without N/A

### 3. Optional Captures
**Contains sub-sections in this order:**

#### 3a. Phase Completion Display
- Show progress (X/10, % complete)
- Display mandatory steps verification
- Show TDD iteration counter (if applicable)
- Include warning: "Approaching limit" at 4/5, "HALT" at 5/5

#### 3b. Observation Capture (EPIC-051)
- Standard three-step workflow:
  1. Collect Explicit Observations
  2. Invoke Observation Extractor
  3. Append to Phase State
- Non-blocking error handling (BR-001)
- Reference: `references/observation-capture.md`

#### 3c. Session Memory Update (STORY-341)
- Append observations to `.claude/memory/sessions/${STORY_ID}-session.md`
- Update last_updated timestamp
- Reference: EPIC-052 Session Memory Layer specification

#### 3d. Reflection (if subagents present in phase)
- Five reflection questions
- Optional observation capture if answers are YES
- JSON schema for observations
- Reference: `references/observation-capture.md`

### 4. Exit Gate
- CLI command for phase completion
- Exit code meanings (0=pass, 1=fail)
- Clear next phase indication

## Template Examples

### Phase Completion Display (Standard)
```markdown
### Phase Completion Display

**Before marking Phase {N} complete, display:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase {N}/10: {Phase Name} - Mandatory Steps Completed
  TDD Iteration: X/5 | Observations: N captured
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ {subagent1} invoked (lines XXX-YYY)
✓ {subagent2} invoked (lines XXX-YYY)
✓ {action1} completed
✓ {action2} verified

All Phase {N} mandatory steps completed. Proceeding to Phase {N+1}...
```

**Iteration counter display:**
- IF iteration_count >= 4: Display "TDD Iteration: X/5 ⚠️ Approaching limit"
- IF iteration_count >= max_iterations (5): HALT with "Maximum iterations reached"
```

### Observation Capture (Standard)
```markdown
### Observation Capture (EPIC-051)

Before exiting this phase, capture observations from subagent outputs:

1. **Collect Explicit Observations:**
   IF {SUBAGENT_NAME} returned `observations[]` in output:
   - Extract each observation object
   - Set source: "explicit"

2. **Invoke Observation Extractor:**
   ```
   Task(subagent_type="observation-extractor",
        description="Extract observations from Phase {N} subagent outputs",
        prompt="Extract implicit observations from {SUBAGENT_NAME} output including {CONTEXT_KEYWORDS}.")
   ```
   - Set source: "extracted" for returned observations

3. **Append to Phase State:**
   FOR each observation (explicit OR extracted):
   - Generate ID: "OBS-{N}-{timestamp}" (ISO8601 milliseconds)
   - Set fields: id, phase ("{N}"), category, note, severity, files[], source, timestamp
   - Append to phase-state.json observations[] array
   - Ensure no duplicate observations (skip if same finding in explicit and extracted)

**Error Handling:** If observation capture fails, log warning and continue phase completion (non-blocking per BR-001).
```

### Session Memory Update (Standard)
```markdown
### Session Memory Update (STORY-341)

Before exiting this phase, append observations to the session memory file:

```
# Append Phase {N} observations to session memory
session_path = ".claude/memory/sessions/${STORY_ID}-session.md"

Edit(
  file_path=session_path,
  old_string="## Observations",
  new_string="## Observations\n\n### Phase {N} ({Phase Name})\n${OBSERVATIONS_LIST}"
)

# Update last_updated timestamp
Edit(
  file_path=session_path,
  old_string="last_updated: ${OLD_TIMESTAMP}",
  new_string="last_updated: ${CURRENT_TIMESTAMP}"
)
```

**Reference:** EPIC-052 Session Memory Layer specification
```

### Reflection (Standard)
```markdown
### Reflection

**Before exiting this phase, reflect:**
1. Did I encounter any friction? (unclear docs, missing tools, workarounds)
2. Did anything work particularly well? (constraints that helped, patterns that fit)
3. Did I notice any repeated patterns?
4. Are there gaps in tooling/docs?
5. Did I discover any bugs?

**If YES to any:** Append to phase-state.json `observations` array:
```json
{
  "id": "obs-{N}-{seq}",
  "phase": "{N}",
  "category": "{friction|success|pattern|gap|idea|bug}",
  "note": "{1-2 sentence description}",
  "files": ["{relevant files}"],
  "severity": "{low|medium|high}"
}
```

**Reference:** `references/observation-capture.md`
    Read(file_path="references/observation-capture.md")
```

## Phase-Specific Variations

### Phases 04.5, 05.5 (AC Verification)
- **Skip Phase Completion Display** (short phases, already minimal)
- **Keep Observation Capture** (but minimal, 4-5 reflection questions only)
- **ADD Session Memory Update** (was missing)
- **Skip Reflection subsection** (already reflection questions in Observation Capture)

### Phases 08 (Git Workflow)
- **Add Phase Completion Display** (was missing)
- **Keep Observation Capture** (standard)
- **Keep Session Memory Update** (standard)
- **ADD Reflection subsection** (was missing)

### Phase 09 (Feedback Hook)
- **Keep Phase Completion Display** (standard)
- **Skip Observation Capture** (Phase 09 IS the observation phase)
- **Skip Session Memory Update** (not applicable)
- **Skip Reflection** (inherently non-blocking, documented as such)
- **Add explicit note:** "Phase 09 feedback hooks and AI analysis are inherently non-blocking. No additional optional captures beyond what is documented in Mandatory Steps."

### Phase 10 (Result Interpretation)
- **Keep Phase Completion Display** (standard)
- **Skip Observation Capture** (final phase, no subagents to extract from)
- **Skip Session Memory Update** (handled as Archive Session Memory in mandatory steps)
- **Skip Reflection** (final phase, review happens in Phase 09)

## Consistency Checklist

For each phase file, verify:

- [ ] Section order matches template (Validation Checkpoint → Pre-Exit Checklist → Optional Captures → Exit Gate)
- [ ] Validation Checkpoint has bullet list with HALT conditions
- [ ] Pre-Exit Checklist has checkbox items with "N/A justification" escape clause
- [ ] Optional Captures has sub-sections in correct order (where applicable)
- [ ] Phase Completion Display (if included) shows phase X/10 and iteration counter
- [ ] Observation Capture (if included) has 3-step workflow with error handling
- [ ] Session Memory Update (if included) uses correct phase number
- [ ] Reflection (if included) has 5 questions + JSON schema
- [ ] Exit Gate shows CLI command with exit codes
- [ ] All file references use correct phase ID format ({N} or decimal notation)
- [ ] No duplicated content from other phases
- [ ] File ends with Exit Gate (final section)

## Reference Updates

- All phases should cite: `references/observation-capture.md` in Reflection section
- All phases should cite: `EPIC-052 Session Memory Layer specification` in Session Memory section
- Phase Completion Display is NEW - all phases that add it are implementing existing pattern from Phase-03/04

## Benefits

1. **Consistency** - All 12 files follow identical structure
2. **DRY** - Reduced observation capture boilerplate from 2,700 lines to ~200 lines (+ template)
3. **Readability** - Clear progression from mandatory → validation → optional captures → exit
4. **Maintainability** - Changes to observation capture workflow update in one template
5. **User Experience** - Consistent display progression across all phases
