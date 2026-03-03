---
name: validate-stories
description: Validate stories against context files and trace custody chain provenance
argument-hint: "[STORY-ID|EPIC-ID|STORY-A..STORY-B|all] [--chain] [--force]"
---

# /validate-stories Command

Validates story files against constitutional context files and optionally traces
the full custody chain from brainstorms through requirements, epics, and sprints.

## Purpose

Validates one or more stories against the 6 context files to identify compliance issues,
and optionally traces full document provenance to detect broken chains, missing ADRs,
circular dependencies, ambiguous acceptance criteria, and stale labels.

## Usage

/validate-stories STORY-042              # Context validation (single story)
/validate-stories all                    # Context validation (all stories)
/validate-stories --since=STORY-100      # Context validation (stories >= ID)
/validate-stories STORY-013..STORY-033   # Custody chain audit (range)
/validate-stories EPIC-003               # Custody chain audit (all stories in epic)
/validate-stories STORY-042 --chain      # Custody chain audit (single story + back-chain)
/validate-stories all --chain            # Custody chain audit (everything)
/validate-stories EPIC-003 --force       # Regenerate from scratch (ignore existing audit)

## Workflow

### Phase 0: Input Resolution + Resume Detection

0. Parse $ARGUMENTS:

   # Extract flags
   chain_mode = "--chain" in $ARGUMENTS
   force_mode = "--force" in $ARGUMENTS
   args_clean = $ARGUMENTS without "--chain" and "--force"

   # Determine scope mode
   IF args_clean matches "^STORY-\d+$":
     mode = "single"
     story_id = args_clean
   ELIF args_clean == "all" OR args_clean == "":
     mode = "all"
   ELIF args_clean starts with "--since=":
     since_id = extract_story_id(args_clean)
     mode = "since"
   ELIF args_clean matches "^STORY-\d+\.\.STORY-\d+$":
     [range_start, range_end] = args_clean.split("..")
     mode = "range"
     chain_mode = true   # Range always implies chain
   ELIF args_clean matches "^EPIC-\d+$":
     epic_id = args_clean
     mode = "epic"
     chain_mode = true   # Epic always implies chain
   ELSE:
     HALT: "Invalid argument. Use: STORY-XXX, all, --since=STORY-XXX, STORY-A..STORY-B, or EPIC-XXX"

   # Derive audit file path (for chain mode)
   IF chain_mode:
     SWITCH mode:
       "single": scope_str = story_id
       "all":    scope_str = "all-stories"
       "since":  scope_str = f"since-{since_id}"
       "range":  scope_str = f"stories-{extract_num(range_start)}-{extract_num(range_end)}"
       "epic":   scope_str = epic_id
     AUDIT_FILE = f"devforgeai/qa/audit/custody-chain-audit-{scope_str}.md"

     # Resume detection (skip if --force)
     IF NOT force_mode AND file_exists(AUDIT_FILE):
       existing = Read(file_path=AUDIT_FILE)
       completed_sections = count sections matching "^## [0-9]+\." in existing

       IF completed_sections >= 8:
         Display: "Audit is COMPLETE ({AUDIT_FILE}). Use --force to regenerate."
         RETURN

       ELIF completed_sections > 0:
         AskUserQuestion:
           Question: "Existing audit found with {completed_sections}/8 sections complete. Resume?"
           Header: "Resume audit"
           Options:
             - "Resume from where it stopped"
               Description: "Continue from section {completed_sections + 1}"
             - "Start fresh"
               Description: "Delete existing file and re-run from scratch"

         IF user_choice == "Resume":
           resume_from = completed_sections + 1
           GOTO Phase matching resume_from (see mapping below)
         ELSE:
           # Fresh start - proceed normally

   # Phase-to-section mapping for resume:
   # Phase 1 writes Section 1      -> resume_from=2 means skip Phase 1
   # Phase 2 writes Section 2      -> resume_from=3 means skip Phase 2
   # Phase 3 writes Sections 3,4   -> resume_from=5 means skip Phase 3
   # Phase 4 writes Sections 5,6,7 -> resume_from=8 means skip Phase 4
   # Phase 5 writes Section 8      -> complete

   IF NOT chain_mode:
     # Pure context validation mode - run existing validation only
     GOTO Phase 2 (skip Phase 1 inventory)


### Phase 1: Scope Discovery + Document Inventory

1. Discover stories in scope:

   story_dir = "devforgeai/specs/Stories/"
   all_story_files = Glob(pattern=f"{story_dir}STORY-*.story.md")

   SWITCH mode:
     "single":
       story_files = [f for f in all_story_files if story_id in f]
       IF empty: HALT "Story not found: {story_id}"

     "all":
       story_files = sort_by_numeric_id(all_story_files)

     "since":
       story_files = [f for f in all_story_files
                      if extract_numeric(f) >= extract_numeric(since_id)]

     "range":
       start_num = extract_numeric(range_start)
       end_num = extract_numeric(range_end)
       story_files = [f for f in all_story_files
                      if start_num <= extract_numeric(f) <= end_num]

     "epic":
       epic_file = Glob(pattern=f"devforgeai/specs/Epics/{epic_id}*.epic.md")[0]
       IF not found: HALT "Epic not found: {epic_id}"
       epic_content = Read(file_path=epic_file)
       story_ids = Grep(pattern="STORY-\\d+", content=epic_content, unique=true)
       story_files = [f for f in all_story_files if extract_story_id(f) in story_ids]

   story_files = sort_by_numeric_id(story_files)
   Display: f"Found {len(story_files)} stories to validate"

   # Read frontmatter from each story for metadata
   story_meta = {}
   FOR story_file in story_files:
     content = Read(file_path=story_file)
     frontmatter = parse_yaml_frontmatter(content)
     story_meta[extract_story_id(story_file)] = {
       "file": story_file,
       "content": content,
       "epic": frontmatter.get("epic"),
       "sprint": frontmatter.get("sprint"),
       "depends_on": frontmatter.get("depends_on", []),
       "status": frontmatter.get("status")
     }

   IF chain_mode:
     # Build document inventory for provenance tracing
     chain_docs = {
       "brainstorms": Glob(pattern="devforgeai/specs/brainstorms/*.brainstorm.md"),
       "research":    Glob(pattern="devforgeai/specs/Research/*.md"),
       "requirements": Glob(pattern="devforgeai/specs/requirements/*.md"),
       "epics":       Glob(pattern="devforgeai/specs/Epics/*.epic.md"),
       "sprints":     Glob(pattern="devforgeai/specs/Sprints/*.sprint.md"),
       "adrs":        Glob(pattern="devforgeai/specs/adrs/ADR-*.md")
     }

     # Write audit file header + Section 1 (Document Inventory)
     Write(file_path=AUDIT_FILE, content=f"""
     # Custody Chain Audit: {scope_str}

     **Audit Date:** {today}
     **Scope:** {mode} - {scope_str}
     **Stories Validated:** {len(story_files)}

     ---

     ## 1. Document Inventory

     | Layer | Document | Path |
     |-------|----------|------|
     {for doc_type, files in chain_docs.items():}
     {for f in files:}
     | {doc_type} | {extract_id(f)} | `{f}` |
     {/for}{/for}
     """)

     Display: f"Chain mode: {len(chain_docs.brainstorms)} brainstorms, {len(chain_docs.epics)} epics, {len(chain_docs.adrs)} ADRs"


### Phase 2: Context Validation

2. Load context files and validate each story:

   Reference: .claude/skills/devforgeai-story-creation/references/context-validation.md

   # Load all 6 context files in PARALLEL
   context_files = {
     "tech_stack":  Read("devforgeai/specs/context/tech-stack.md"),
     "source_tree": Read("devforgeai/specs/context/source-tree.md"),
     "dependencies": Read("devforgeai/specs/context/dependencies.md"),
     "coding_standards": Read("devforgeai/specs/context/coding-standards.md"),
     "architecture": Read("devforgeai/specs/context/architecture-constraints.md"),
     "anti_patterns": Read("devforgeai/specs/context/anti-patterns.md")
   }

   context_status = { k: v is not None for k, v in context_files.items() }

   IF all values are False:
     Display: """
     Greenfield Mode: No context files found.
     Run /create-context to generate context files.
     """
     RETURN early

   Display: f"Context files: {sum(context_status.values())}/6 loaded"

   # Validate each story against context files
   all_results = []
   FOR story_id, meta in story_meta.items():
     tech_spec = extract_section(meta.content, "Technical Specification")
     deps = extract_section(meta.content, "Dependencies")
     dod = extract_section(meta.content, "Definition of Done")
     file_paths = extract_file_paths(tech_spec)

     violations = []
     IF context_status.tech_stack:       violations.extend(validate_technologies(tech_spec))
     IF context_status.source_tree:      violations.extend(validate_file_paths(tech_spec))
     IF context_status.dependencies:     violations.extend(validate_dependencies(deps))
     IF context_status.coding_standards: violations.extend(validate_coverage_thresholds(dod, file_paths))
     IF context_status.architecture:     violations.extend(validate_architecture(tech_spec))
     IF context_status.anti_patterns:    violations.extend(validate_anti_patterns(tech_spec))
     IF context_status.source_tree:      violations.extend(validate_dual_path(tech_spec))

     result = {
       story_id, file: meta.file, violations,
       critical: count_severity(violations, "CRITICAL"),
       high: count_severity(violations, "HIGH"),
       medium: count_severity(violations, "MEDIUM"),
       low: count_severity(violations, "LOW"),
       status: "COMPLIANT" if no critical+high else "FAILED"
     }
     all_results.append(result)
     Display: f"  [{idx}/{total}] {story_id}: {result.status}"

   IF chain_mode:
     # Append Section 2 to audit file
     Append to AUDIT_FILE: f"""

     ## 2. Context Validation Results

     | Story ID | Status | CRITICAL | HIGH | MEDIUM | LOW |
     |----------|--------|----------|------|--------|-----|
     {for r in all_results:}
     | {r.story_id} | {r.status} | {r.critical} | {r.high} | {r.medium} | {r.low} |
     {/for}

     **Compliance Rate:** {compliant}/{total} ({pct}%)
     """


### Phase 3: Custody Chain Audit (chain mode only)

3. Custody chain analysis (ONLY if chain_mode is true):

   IF NOT chain_mode: SKIP to Phase 4

   Reference: Load .claude/skills/devforgeai-story-creation/references/custody-chain-workflow.md
   Reference: .claude/skills/devforgeai-story-creation/references/context-validation.md
   Section: "Custody Chain Validation Functions" (functions #7-10)

   findings = []
   finding_counter = 1

   Execute the 5 sub-phases documented in custody-chain-workflow.md:
   - 3a: Provenance Tracing (validate_provenance_chain) -> findings
   - 3b: Dependency Graph (validate_dependency_graph) -> findings
   - 3c: ADR Cross-Reference (validate_adr_references) -> findings
   - 3d: Story Quality + Stale Labels (validate_story_quality) -> findings
   - 3e: Plan-Story Coherence (functions #11-17 in context-validation.md) -> findings

   # Sub-Phase 3e: Plan-Story Coherence Validation
   # Trigger: chain_mode AND 2+ stories from same epic in scope
   # Detects: schema mismatches, API contract errors, plan-story drift,
   #          naming inconsistencies, format inconsistencies,
   #          instruction contradictions, dependency assumption mismatches
   # Reference: custody-chain-workflow.md Sub-Phase 3e + context-validation.md #11-17

   IF len(epics_in_scope) > 0:
     Read("src/claude/skills/devforgeai-story-creation/references/context-validation.md")
     # Functions #11-17 define the coherence validation logic

     FOR epic_id in epics_in_scope:
       epic_stories = [s for s in story_files if story_meta[s].epic == epic_id]
       IF len(epic_stories) >= 2:
         plan_file = discover_plan_file(epic_id)  # See custody-chain-workflow.md 3e
         coherence_findings = run_coherence_validation(epic_stories, plan_file)
         findings.extend(coherence_findings)

   # Write Sections 3 and 4 to audit file
   Append to AUDIT_FILE: build_provenance_map(epics_in_scope, chain_docs, story_meta)
   Append to AUDIT_FILE: build_findings_section(findings, all_results)


### Phase 4: Synthesis + Report Finalization

4. Synthesize findings and generate summary:

   # Merge context violations into findings list
   all_findings = []
   FOR result in all_results:
     FOR v in result.violations:
       all_findings.append(F(finding_counter, v.severity, [result.story_id],
         summary=v.description, type=f"context/{v.type}",
         remediation=v.remediation))

   IF chain_mode:
     all_findings.extend(findings)

   all_findings = sort_by_severity(all_findings)

   stats = {
     stories_validated: len(story_files),
     compliant: count(all_results, status="COMPLIANT"),
     failed: count(all_results, status="FAILED"),
     total_findings: len(all_findings),
     critical: count(all_findings, severity="CRITICAL"),
     high: count(all_findings, severity="HIGH"),
     medium: count(all_findings, severity="MEDIUM"),
     low: count(all_findings, severity="LOW")
   }

   IF chain_mode:
     priority_list = prioritize(all_findings)

     Append to AUDIT_FILE: f"""

     ## 5. Cross-Cutting Issues
     {identify systemic patterns: same issue in 3+ stories, missing sprint assignments, assignee inconsistencies}

     ## 6. Summary Statistics

     | Metric | Count |
     |--------|-------|
     | Stories validated | {stats.stories_validated} |
     | Stories compliant | {stats.compliant} |
     | Stories failed | {stats.failed} |
     | Total findings | {stats.total_findings} |
     | CRITICAL | {stats.critical} |
     | HIGH | {stats.high} |
     | MEDIUM | {stats.medium} |
     | LOW | {stats.low} |

     ## 7. Remediation Priority Order

     {for idx, f in enumerate(priority_list):}
     {idx+1}. **{f.finding_id}** ({f.severity}) - {f.summary}
     {/for}
     """


### Phase 5: Session Handoff + Display

5. Write handoff section and display results:

   IF chain_mode:
     Append to AUDIT_FILE: f"""

     ## 8. Session Handoff Instructions

     **For future Claude sessions reading this document:**

     1. This document is self-contained. You do not need the original conversation.
     2. Check current state before remediating - prior sessions may have fixed some items.
     3. Use the verification step in each finding to confirm fixes were applied.
     4. File paths are relative to project root.
     5. For CRITICAL findings: these block story implementation. Prioritize them.
     6. For quick fixes (path corrections, label updates): batch these in one session.
     7. For architectural decisions: use AskUserQuestion to confirm approach before changing.
     """
     Display: f"Audit written to {AUDIT_FILE}"

   Display: f"""
   ## {'Custody Chain Audit' if chain_mode else 'Context Validation'} Complete

   **Stories Validated:** {stats.stories_validated}
   **Compliant:** {stats.compliant}/{stats.stories_validated} ({pct}%)
   **Findings:** {stats.critical} CRITICAL, {stats.high} HIGH, {stats.medium} MEDIUM, {stats.low} LOW
   {if chain_mode: f"**Report:** {AUDIT_FILE}"}
   """


### Phase 6: Interactive Resolution (Optional)

6. Interactive fix-up (single story mode with violations only):

   IF mode == "single" AND stats.failed > 0:
     critical_high = [f for f in all_findings if f.severity in ["CRITICAL", "HIGH"]]

     IF critical_high:
       AskUserQuestion:
         Question: f"{len(critical_high)} blocking issues found. Fix now?"
         Header: "Fix issues"
         Options:
           - "Fix all" / Description: "Walk through each violation and resolve"
           - "Show details only" / Description: "Display details, don't fix"
           - "Skip" / Description: "Exit without changes"

       IF choice == "Fix all":
         FOR finding in critical_high:
           AskUserQuestion:
             Question: f"[{finding.severity}] {finding.type}: {finding.summary}\n\nHow to resolve?"
             Header: "Resolution"
             Options:
               - "Fix in story" / Description: "I'll provide the correct value"
               - "Create required ADR" / Description: "Needed for tech decisions"
               - "Update context file" / Description: "Requires ADR first"
               - "Defer to manual review" / Description: "Flag for later"

           SWITCH choice:
             "Fix in story":    AskUserQuestion for value -> Edit story
             "Create ADR":      Display: "Run /create-story for ADR, then re-validate"
             "Update context":  Display: "Create ADR first, update context, re-validate"
             "Defer":           Edit story to add: "<!-- AUDIT-DEFERRED: {finding.type} -->"

         Display: "Re-validating after fixes..."
         GOTO Phase 2 (single story)


### Phase 7: Refactor Story Quality Validation

7. Refactor-specific content-preservation checks (CONDITIONAL):

   IF NOT any story in story_meta has type == "refactor": SKIP to Output

   Reference: STORY-457 revert — refactor stories with size-only ACs led to logic loss during implementation.

   FOR story_id, meta in story_meta.items():
     frontmatter = parse_yaml_frontmatter(meta.content)
     IF frontmatter.get("type") != "refactor": CONTINUE

     refactor_findings = []

     #### Check 7.8.1: Content-Preservation AC Present

     ```
     ac_text = concatenate all AC <then> clauses from meta.content

     has_content_ac = any of these patterns found in ac_text:
         - "preserved" (content preservation)
         - "backward.compat" (output verification)
         - "golden" (golden output diffing)
         - "identical.*format" (display format matching)

     IF NOT has_content_ac:
         refactor_findings.append(finding(
             severity="HIGH",
             type="quality/refactor_missing_preservation_ac",
             affected=story_id,
             summary="Refactor story has size/structure ACs but no content-preservation ACs",
             remediation="Add AC verifying all Display/error/governance content preserved. Use /fix-story to auto-generate."))
     ```

     #### Check 7.8.2: NFR-002 Enforcement AC Present

     ```
     nfr_section = extract_section(meta.content, "Non-Functional Requirements")

     IF nfr_section AND "backward compatibility" in nfr_section.lower():
         has_enforcement_ac = any AC <then> clause contains:
             - "help text" AND "sections"
             - "error messages" AND "format"
             - "golden" OR "output.*diff"

         IF NOT has_enforcement_ac:
             refactor_findings.append(finding(
                 severity="HIGH",
                 type="quality/refactor_nfr_without_ac",
                 affected=story_id,
                 summary="NFR-002 backward compatibility declared but no AC enforces output verification",
                 remediation="Add AC with golden output diffing for all invocation modes."))
     ```

     #### Check 7.8.3: AskUserQuestion Placement AC Present

     ```
     # Check if story references files that contain AskUserQuestion
     tech_spec = extract_section(meta.content, "Technical Specification")
     target_files = extract_file_paths(tech_spec)

     has_askuser_in_targets = false
     FOR file in target_files:
         IF file_exists(file):
             content = Read(file_path=file)
             IF "AskUserQuestion" in content:
                 has_askuser_in_targets = true
                 BREAK

     IF has_askuser_in_targets:
         has_placement_ac = any AC <then> clause contains:
             - "AskUserQuestion" AND ("ZERO" OR "zero" OR "0") AND "skill"

         IF NOT has_placement_ac:
             refactor_findings.append(finding(
                 severity="MEDIUM",
                 type="quality/refactor_askuser_placement_missing",
                 affected=story_id,
                 summary="Source files have AskUserQuestion but no AC enforces lean orchestration placement",
                 remediation="Add AC requiring zero AskUserQuestion in skill, all in command per lean-orchestration-pattern.md line 104."))
     ```

     #### Check 7.8.4: Golden Output DoD Present

     ```
     dod_text = extract_section(meta.content, "Definition of Done")

     has_golden_dod = dod_text AND any of:
         - "golden output" in dod_text.lower()
         - "pre-refactoring" in dod_text.lower()
         - regex "output.*captured" matches dod_text

     IF NOT has_golden_dod:
         refactor_findings.append(finding(
             severity="MEDIUM",
             type="quality/refactor_missing_golden_capture",
             affected=story_id,
             summary="Refactor story DoD missing golden output capture items",
             remediation="Add DoD items for pre-refactoring output capture and post-refactoring diff."))
     ```

     all_findings.extend(refactor_findings)
     Display: f"  [{story_id}] Refactor checks: {len(refactor_findings)} findings"


## Output

**Success (all compliant, context only):**
  Context Validation Complete
  Stories Validated: 15
  Compliant: 15/15 (100%)

**Chain audit with findings:**
  Custody Chain Audit Complete
  Stories Validated: 21
  Compliant: 19/21 (90.5%)
  Findings: 2 CRITICAL, 6 HIGH, 5 MEDIUM, 3 LOW
  Report: devforgeai/qa/audit/custody-chain-audit-stories-013-033.md

**Resume:**
  Existing audit found with 4/8 sections complete. Resume?
  > Resume from where it stopped
  Resuming from Phase 4 (Synthesis)...

## Integration

**Invokes validation logic from:**
- `.claude/skills/devforgeai-story-creation/references/context-validation.md`
  Sections: "Validation Functions" (#1-6) + "Custody Chain Validation Functions" (#7-10)
- `.claude/skills/devforgeai-story-creation/references/custody-chain-workflow.md`
  Section: Phase 3 sub-phases (3a-3d) detailed orchestration

**Can be called:**
- Standalone via `/validate-stories`
- Before sprint planning (ensure stories are ready)
- After bulk story creation (batch validation)
- By future Claude sessions to pick up remediation work (resume mode)

**Related commands:**
- `/create-context` - Generate context files (required for validation)
- `/create-story` - Create new story (includes context validation)
- `/qa` - Quality validation (includes context compliance)
- `/validate-epic-coverage` - Validate epic feature coverage
