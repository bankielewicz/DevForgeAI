# Custody Chain Audit Workflow

**Purpose:** Detailed orchestration for `/validate-stories` Phase 3 (chain mode only).
**Loaded by:** `/validate-stories` command when `--chain` flag is active.
**Companion reference:** `context-validation.md` (functions #7-10 define the validation logic).

---

## Prerequisites

Before executing this workflow, the following must be available from prior phases:

- `story_meta` — dict of story metadata keyed by story_id (from Phase 1)
- `chain_docs` — dict of Glob results for brainstorms, research, requirements, epics, sprints, adrs (from Phase 1)
- `all_results` — context validation results (from Phase 2)
- `AUDIT_FILE` — path to audit output file (from Phase 0)

---

## Sub-Phase 3a: Provenance Tracing (function #7: validate_provenance_chain)

**Purpose:** Story → Epic → Requirements → Brainstorm — verify each link exists and is not broken.

```
findings = []
finding_counter = 1

epics_in_scope = set(meta.epic for meta in story_meta.values() if meta.epic)

FOR epic_id in epics_in_scope:
  epic_file = find_file(chain_docs.epics, epic_id)

  IF epic_file is None:
    findings.append(F(finding_counter, "CRITICAL", [epic_id],
      summary=f"Epic file not found for {epic_id}",
      phase="3a", type="missing_epic"))
    CONTINUE

  epic_content = Read(file_path=epic_file)

  # Check: epic -> brainstorm reference
  brainstorm_ref = extract_field(epic_content, "brainstorm")
  IF brainstorm_ref is null:
    findings.append(F(finding_counter, "HIGH", [epic_id],
      summary=f"{epic_id} has no brainstorm back-reference",
      remediation="Add brainstorm_ref to epic frontmatter"))
  ELSE:
    brainstorm_file = find_file(chain_docs.brainstorms, brainstorm_ref)
    IF brainstorm_file is None:
      findings.append(F(finding_counter, "HIGH", [epic_id],
        summary=f"{epic_id} references {brainstorm_ref} which does not exist on disk",
        remediation="Create brainstorm or fix reference"))

  # Check: epic -> requirements reference
  req_ref = extract_field(epic_content, "requirements_ref")
  IF req_ref is not null AND NOT file_exists(req_ref):
    findings.append(F(finding_counter, "MEDIUM", [epic_id],
      summary=f"{epic_id} requirements_ref path not found: {req_ref}",
      remediation="Fix path or remove reference"))

  # Check: research ID consistency across the full chain
  brainstorm_research = extract_research_refs(brainstorm_content)
  epic_research = extract_research_refs(epic_content)
  IF brainstorm_research != epic_research AND both non-empty:
    findings.append(F(finding_counter, "HIGH", [epic_id],
      summary=f"Research ID mismatch: brainstorm cites {brainstorm_research}, downstream cites {epic_research}",
      remediation="Align research IDs across all documents in the chain"))

Display: f"  Provenance: {len(epics_in_scope)} epics traced"
```

---

## Sub-Phase 3b: Dependency Graph (function #8: validate_dependency_graph)

**Purpose:** Check for circular deps, missing deps, stale status labels, undeclared coupling.

```
FOR story_id, meta in story_meta.items():
  FOR dep_id in meta.depends_on:
    IF dep_id not in story_meta AND NOT story_file_exists(dep_id):
      findings.append(F(finding_counter, "HIGH", [story_id],
        summary=f"{story_id} depends on {dep_id} which has no story file",
        type="missing_dependency",
        remediation="Create the dependency story or remove the depends_on reference"))

    IF dep_id in story_meta:
      actual_status = story_meta[dep_id].status
      listed_status = extract_dep_listed_status(meta.content, dep_id)
      IF listed_status is not null AND listed_status != actual_status:
        findings.append(F(finding_counter, "MEDIUM", [story_id],
          summary=f"{story_id} lists {dep_id} as '{listed_status}' but actual is '{actual_status}'",
          type="stale_dependency_status",
          remediation=f"Update dependency table: {dep_id} status -> {actual_status}"))

# Cycle detection
graph = { sid: meta.depends_on for sid, meta in story_meta.items() }
FOR cycle in detect_cycles(graph):
  findings.append(F(finding_counter, "CRITICAL", cycle,
    summary=f"Circular dependency: {' -> '.join(cycle)}",
    type="circular_dependency",
    remediation="Break the cycle by removing one depends_on reference"))

# Undeclared mutual dependency detection
FOR (story_a, story_b) in pairs(story_meta.keys()):
  a_refs_b = story_b in extract_story_refs(story_meta[story_a].content)
  a_declares_b = story_b in story_meta[story_a].depends_on
  IF a_refs_b AND NOT a_declares_b:
    findings.append(F(finding_counter, "HIGH", [story_a, story_b],
      summary=f"{story_a} references {story_b} in ACs/spec but doesn't declare depends_on",
      type="undeclared_dependency",
      remediation=f"Add {story_b} to {story_a} depends_on list"))

Display: f"  Dependencies: {len(graph)} stories graphed"
```

---

## Sub-Phase 3c: ADR Cross-Reference (function #9: validate_adr_references)

**Purpose:** Verify ADR references in stories are valid and accepted.

```
FOR story_id, meta in story_meta.items():
  IF "ADR TBD" in meta.content OR "ADR-TBD" in meta.content:
    findings.append(F(finding_counter, "CRITICAL", [story_id],
      summary=f"{story_id} has an unresolved 'ADR TBD' - implementation blocked",
      type="missing_required_adr",
      evidence=extract_line_containing(meta.content, "ADR TBD"),
      remediation="Create the required ADR before starting TDD"))

  adr_refs = Grep(pattern="ADR-\\d{3}", content=meta.content)
  FOR adr_ref in unique(adr_refs):
    adr_file = find_file(chain_docs.adrs, adr_ref)
    IF adr_file is None:
      findings.append(F(finding_counter, "HIGH", [story_id],
        summary=f"{story_id} references {adr_ref} which has no file in adrs/",
        type="broken_adr_reference",
        remediation="Create the ADR or fix the reference"))
    ELSE:
      adr_content = Read(file_path=adr_file)
      adr_status = extract_field(adr_content, "status")
      IF adr_status == "proposed":
        findings.append(F(finding_counter, "HIGH", [story_id],
          summary=f"{story_id} references {adr_ref} which is still 'proposed'",
          type="adr_not_accepted",
          remediation="Get ADR accepted before implementation begins"))

Display: f"  ADRs: {len(chain_docs.adrs)} validated"
```

---

## Sub-Phase 3d: Stale Labels + Ambiguity (function #10: validate_story_quality)

**Purpose:** Detect ambiguous ACs, broken file references, path case issues.

```
FOR story_id, meta in story_meta.items():
  # Ambiguous AC text
  ambiguous = Grep(pattern="\\(or \\w+\\)", content=meta.content)
  IF ambiguous:
    FOR match in ambiguous:
      findings.append(F(finding_counter, "HIGH", [story_id],
        summary=f"{story_id} has ambiguous AC text: '{match}'",
        type="ambiguous_acceptance_criteria",
        remediation="Remove the '(or X)' alternative - pick one definitive answer"))

  # Broken file references
  file_refs = extract_src_file_paths(meta.content)
  FOR ref_path in file_refs:
    IF is_concrete_path(ref_path) AND NOT file_or_glob_exists(ref_path):
      findings.append(F(finding_counter, "MEDIUM", [story_id],
        summary=f"{story_id} references '{ref_path}' which does not exist",
        type="broken_file_reference",
        remediation="Verify path or acknowledge as new file to create"))

  # Path case sensitivity
  IF "specs/research/" in meta.content:
    findings.append(F(finding_counter, "MEDIUM", [story_id],
      summary=f"{story_id} uses 'specs/research/' - actual is 'specs/Research/'",
      type="path_case_mismatch",
      remediation="Replace 'specs/research/' with 'specs/Research/'"))

Display: f"  Labels & refs: checked"
```

---

## Post-Phase 3: Write Audit Sections

After all 4 sub-phases complete:

```
# Write Section 3: Provenance Chain Map
Append to AUDIT_FILE: build_provenance_map(epics_in_scope, chain_docs, story_meta)

# Write Section 4: Findings Detail
Append to AUDIT_FILE: build_findings_section(findings, all_results)
```

The `findings` list carries forward to Sub-Phase 3e (if applicable) and then Phase 4 (Synthesis) for merging with context violations.

---

## Sub-Phase 3e: Plan-Story Coherence Validation (functions #11-17)

**Purpose:** Detect specification drift, schema mismatches, and contradictions across stories in the same epic. Catches issues that arise when a plan is translated into stories by a different session.

**Trigger:** Chain mode only. Requires 2+ stories from same epic in scope.

**Prerequisites:**
- `story_meta` — dict of story metadata keyed by story_id (from Phase 1)
- `chain_docs` — dict of Glob results for brainstorms, epics, plans (from Phase 1)
- `dependency_graph` — from Sub-Phase 3b (for dependency assumption checks)

**Reference:** Functions #11-17 are defined in `context-validation.md` (Plan-Story Coherence Validation Functions section).

### Plan File Discovery

```
associated_plans = {}  # {epic_id: plan_file_path}

FOR each epic_id in epics_in_scope:
  # Search .claude/plans/ for files referencing this epic or its stories
  plan_files = Glob(pattern=".claude/plans/*.md")

  FOR plan_file in plan_files:
    content_preview = Read(plan_file, limit=50)  # Check header area
    IF epic_id in content_preview:
      associated_plans[epic_id] = plan_file
      BREAK

    # Check if any story in this epic is referenced
    epic_story_ids = [s for s in story_meta if story_meta[s].epic == epic_id]
    FOR story_id in epic_story_ids:
      IF story_id in content_preview:
        associated_plans[epic_id] = plan_file
        BREAK

  IF epic_id NOT in associated_plans:
    # Fallback: check brainstorm for plan reference
    brainstorm = find_brainstorm_for_epic(epic_id, chain_docs)
    IF brainstorm:
      brainstorm_content = Read(brainstorm)
      plan_ref = extract_field(brainstorm_content, "Feeds Into")
      # plan_ref might be a path like ".claude/plans/smooth-tumbling-beacon.md"
      IF plan_ref and Glob(pattern=plan_ref):
        associated_plans[epic_id] = plan_ref

  # None found is acceptable — functions #13 and #16 skip plan comparison
```

### Execution

```
coherence_findings = []

FOR each epic_id in epics_in_scope:
  epic_stories = [s for s in story_meta.values() if s.epic == epic_id]

  IF len(epic_stories) < 2:
    CONTINUE  # Need 2+ stories for cross-story validation

  plan_file = associated_plans.get(epic_id, None)

  # Run 7 coherence validation functions (defined in context-validation.md #11-17)
  coherence_findings += validate_cross_story_schema(epic_stories)         # #11
  FOR story in epic_stories:
    coherence_findings += validate_api_contracts(story)                    # #12
  coherence_findings += validate_plan_story_drift(epic_stories, plan_file) # #13 (per story)
  coherence_findings += validate_naming_consistency(epic_stories)          # #14
  coherence_findings += validate_format_consistency(epic_stories)          # #15
  coherence_findings += validate_instruction_consistency(epic_stories, plan_file)  # #16
  coherence_findings += validate_dependency_assumptions(epic_stories)      # #17

# Merge into main findings list
findings.extend(coherence_findings)
```

### Finding Type Prefix

All findings from this sub-phase use the `coherence/` prefix:
- `coherence/schema_mismatch`
- `coherence/api_contract_error`
- `coherence/plan_story_drift`
- `coherence/naming_inconsistency`
- `coherence/format_inconsistency`
- `coherence/instruction_contradiction`
- `coherence/dependency_assumption_mismatch`

This prefix enables `/fix-story` to route these findings to the correct fix procedures in `fix-actions-catalog.md`.

### Output

The `coherence_findings` list merges into `findings` and carries forward to Phase 4 (Synthesis) for cross-cutting analysis and Section 4 (Findings Detail) in the audit report.
