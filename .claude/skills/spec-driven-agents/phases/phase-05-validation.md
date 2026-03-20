# Phase 05: Validation

## Contract

| Attribute | Value |
|-----------|-------|
| **PURPOSE** | Independently verify the generated agent passes 12-point framework compliance |
| **REFERENCE** | `src/claude/skills/spec-driven-agents/references/validation-checklist.md` |
| **STEP COUNT** | 3 mandatory steps |

## Phase Exit Criteria

Before this phase can complete, ALL of the following MUST be true:

- [ ] Generated agent file read and analyzed
- [ ] All 12 compliance checks executed (6 DevForgeAI + 6 Claude Code)
- [ ] Validation status determined (PASS, PASS WITH WARNINGS, FAIL)
- [ ] If FAIL: auto-fix attempted OR user decision captured
- [ ] Checkpoint updated with validation results

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-agents/references/validation-checklist.md")
```

IF Read fails: HALT -- "Phase 05 reference file not loaded. Cannot proceed without validation checklist."

---

## Why This Phase Exists Separately

The agent-generator subagent performs its own 12-point validation during generation (Phase 04). This phase re-validates independently because:

1. **Fresh context prevents bias** - The generator may have rationalized compliance during generation. Independent re-check catches what the generator missed.
2. **Visibility to enforcement** - Bundling validation inside the generator made it invisible to the skill's anti-skip enforcement. A separate phase ensures validation cannot be skipped.
3. **Auto-fix opportunity** - If the generator produced a near-miss, this phase can apply auto-fixes without re-invoking the full generation cycle.

---

## Mandatory Steps

### Step 5.1: Read and Analyze Generated Agent File

EXECUTE:
```
agent_path = checkpoint.generation.generated_files.subagent
Read(file_path=agent_path)

# Parse the agent file structure
Extract:
- YAML frontmatter (name, description, tools, model)
- Section headings (## headers)
- Tool references in workflow steps
- Context file references
- Framework integration section
- Token efficiency section
```

VERIFY: Agent file was successfully read and parsed. Frontmatter extracted.
IF Read fails or frontmatter is empty: HALT -- "Step 5.1: Cannot read generated agent file."

RECORD: Update checkpoint:
```
checkpoint.phases["05"].steps_completed.push("5.1")
```

---

### Step 5.2: Execute 12-Point Compliance Check

Run each check from the validation checklist reference. For each check, apply the EXECUTE-VERIFY-RECORD pattern.

EXECUTE:
```
validation_results = {
  "devforgeai": {
    "tool_usage": null,          # Check 1: Native tools only (no Bash file ops)
    "context_awareness": null,    # Check 2: References appropriate context files for domain
    "framework_integration": null,# Check 3: ## Framework Integration section present
    "tool_protocol": null,        # Check 4: ## Tool Usage Protocol with native tools mandate
    "token_efficiency": null,     # Check 5: ## Token Efficiency with strategies
    "lean_orchestration": null    # Check 6: Reference file generation for command-related agents
  },
  "claude_code": {
    "yaml_frontmatter": null,     # Check 7: Valid YAML with required fields
    "description_quality": null,  # Check 8: Includes proactive triggers
    "tool_selection": null,       # Check 9: Appropriate for task (least privilege)
    "model_selection": null,      # Check 10: Appropriate for token usage
    "system_prompt_structure": null, # Check 11: All 10 required sections present
    "workflow_quality": null       # Check 12: 3-15 steps (not too simple/complex)
  }
}

# Execute each check against the parsed agent file:

# CHECK 1: Tool Usage Validation
Grep(pattern="Bash.*cat |Bash.*echo |Bash.*sed |Bash.*awk ", path=agent_path)
IF matches found: validation_results.devforgeai.tool_usage = "FAIL"
ELSE: validation_results.devforgeai.tool_usage = "PASS"

# CHECK 2: Context File Awareness
expected_files = checkpoint.framework_context.context_files_required
Grep(pattern="context/", path=agent_path)
IF references match expected domain context files: validation_results.devforgeai.context_awareness = "PASS"
ELSE: validation_results.devforgeai.context_awareness = "WARN"

# CHECK 3: Framework Integration Section
Grep(pattern="## Framework Integration", path=agent_path)
IF found: validation_results.devforgeai.framework_integration = "PASS"
ELSE: validation_results.devforgeai.framework_integration = "FAIL"

# CHECK 4: Tool Usage Protocol Section
Grep(pattern="## Tool Usage Protocol", path=agent_path)
IF found: validation_results.devforgeai.tool_protocol = "PASS"
ELSE: validation_results.devforgeai.tool_protocol = "FAIL"

# CHECK 5: Token Efficiency Section
Grep(pattern="## Token Efficiency", path=agent_path)
IF found: validation_results.devforgeai.token_efficiency = "PASS"
ELSE: validation_results.devforgeai.token_efficiency = "WARN"

# CHECK 6: Lean Orchestration Compliance
IF domain requires reference file AND checkpoint.generation.reference_file_needed:
  Glob(pattern=checkpoint.generation.generated_files.reference)
  IF found: validation_results.devforgeai.lean_orchestration = "PASS"
  ELSE: validation_results.devforgeai.lean_orchestration = "WARN"
ELSE:
  validation_results.devforgeai.lean_orchestration = "PASS" (N/A)

# CHECK 7: YAML Frontmatter
IF frontmatter has name, description, tools, model: validation_results.claude_code.yaml_frontmatter = "PASS"
ELSE: validation_results.claude_code.yaml_frontmatter = "FAIL"

# CHECK 8: Description Quality
IF description includes proactive trigger language: validation_results.claude_code.description_quality = "PASS"
ELSE: validation_results.claude_code.description_quality = "WARN"

# CHECK 9: Tool Selection
IF tools match domain expectations: validation_results.claude_code.tool_selection = "PASS"
ELSE: validation_results.claude_code.tool_selection = "WARN"

# CHECK 10: Model Selection
IF model appropriate for estimated complexity: validation_results.claude_code.model_selection = "PASS"
ELSE: validation_results.claude_code.model_selection = "WARN"

# CHECK 11: System Prompt Structure (10 sections)
required_sections = ["Purpose", "When Invoked", "Workflow", "Framework Integration",
                     "Tool Usage Protocol", "Success Criteria", "Principles",
                     "Token Efficiency", "References"]
missing_sections = []
FOR section in required_sections:
  Grep(pattern="## ${section}", path=agent_path)
  IF not found: missing_sections.push(section)
IF missing_sections.length == 0: validation_results.claude_code.system_prompt_structure = "PASS"
ELIF missing_sections.length <= 2: validation_results.claude_code.system_prompt_structure = "WARN"
ELSE: validation_results.claude_code.system_prompt_structure = "FAIL"

# CHECK 12: Workflow Quality
step_count = count lines matching /^\d+\./ or /### Step/
IF step_count >= 3 AND step_count <= 15: validation_results.claude_code.workflow_quality = "PASS"
ELSE: validation_results.claude_code.workflow_quality = "WARN"

# Determine overall status
fail_count = count("FAIL" in validation_results)
warn_count = count("WARN" in validation_results)
IF fail_count > 0: overall_status = "FAIL"
ELIF warn_count > 0: overall_status = "PASS WITH WARNINGS"
ELSE: overall_status = "PASS"
```

VERIFY: All 12 checks have a result (none are null).
IF any check is null: HALT -- "Step 5.2: Not all validation checks completed."

RECORD: Update checkpoint:
```
checkpoint.generation.validation_results = {
  "checks": validation_results,
  "overall_status": overall_status,
  "fail_count": fail_count,
  "warn_count": warn_count,
  "pass_count": 12 - fail_count - warn_count
}
checkpoint.phases["05"].steps_completed.push("5.2")
```

---

### Step 5.3: Handle Validation Outcome

EXECUTE:
```
IF overall_status == "PASS":
  Display: "Validation PASSED: 12/12 checks passed."

ELIF overall_status == "PASS WITH WARNINGS":
  Display: "Validation PASSED WITH WARNINGS: ${warn_count} warnings."
  Display warnings to user.
  # Warnings are non-blocking - proceed automatically

ELIF overall_status == "FAIL":
  Display: "Validation FAILED: ${fail_count} checks failed."
  Display failures to user.

  # Attempt auto-fix for auto-fixable checks
  auto_fixable = ["framework_integration", "tool_protocol", "token_efficiency",
                   "yaml_frontmatter", "description_quality"]

  FOR each failed check:
    IF check in auto_fixable:
      Apply auto-fix (add missing section, fix frontmatter, etc.)
      Edit(file_path=agent_path, old_string=..., new_string=...)
      Re-run that specific check
    ELSE:
      Manual fix required

  # Re-assess after auto-fixes
  remaining_failures = count remaining FAIL results
  IF remaining_failures == 0:
    overall_status = "PASS" or "PASS WITH WARNINGS"
    Display: "Auto-fixes applied. Validation now: ${overall_status}"
  ELSE:
    AskUserQuestion:
      Question: "${remaining_failures} validation checks still failing after auto-fix. What would you like to do?"
      Header: "Validation"
      Options:
        - label: "Proceed with warnings"
          description: "Accept the agent as-is with known issues"
        - label: "Regenerate"
          description: "Go back to Phase 04 and regenerate"
        - label: "Cancel"
          description: "Abort agent creation"
    IF "Proceed": overall_status = "PASS WITH WARNINGS (USER ACCEPTED)"
    IF "Regenerate": GOTO Phase 04
    IF "Cancel": EXIT skill
```

VERIFY: Validation outcome handled. Status is PASS or PASS WITH WARNINGS (including user-accepted).
IF status is still FAIL without user decision: HALT -- "Step 5.3: Validation failure not resolved."

RECORD: Update checkpoint:
```
checkpoint.generation.validation_results.overall_status = final_status
checkpoint.phases["05"].steps_completed.push("5.3")
checkpoint.phases["05"].status = "completed"
checkpoint.progress.current_phase = 6
checkpoint.progress.phases_completed.push("05")
checkpoint.progress.completion_percentage = 83
```
Write updated checkpoint to disk.

---

## Phase Exit Verification

```
VERIFY ALL:
  checkpoint.generation.validation_results.overall_status in ["PASS", "PASS WITH WARNINGS", "PASS WITH WARNINGS (USER ACCEPTED)"]
  checkpoint.generation.validation_results.checks has 12 entries (none null)
  checkpoint.phases["05"].status == "completed"

IF ANY fails: HALT -- "Phase 05 exit criteria not met."
```

---

## Phase Transition Display

```
Display:
"Phase 05 Complete: Validation
  Status: ${checkpoint.generation.validation_results.overall_status}
  DevForgeAI: ${devforgeai_pass_count}/6 passed
  Claude Code: ${claude_code_pass_count}/6 passed
  ${IF warnings: 'Warnings: ' + warn_count}
  → Proceeding to Phase 06: Result Processing & Handoff"
```
