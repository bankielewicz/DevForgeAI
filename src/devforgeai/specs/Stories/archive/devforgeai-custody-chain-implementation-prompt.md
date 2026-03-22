# DevForgeAI Framework Enhancement: Custody Chain Audit for /validate-stories

> **This is a self-contained implementation prompt.** It contains everything needed to implement the enhancement across multiple sessions. If your context window fills or a new session starts, re-read this document from the PROGRESS CHECKPOINT section to resume.

---

## PROGRESS CHECKPOINT

**Read this section FIRST on every session start or resume.**

Progress is tracked in a file you will create and maintain at:
```
devforgeai/specs/Stories/.validate-stories-implementation-progress.md
```

If that file exists, read it now to determine where to resume. If it does not exist, you are starting fresh — begin at Task 1.

**After completing each task**, update the progress file with:
```markdown
## Task N: [COMPLETE]
- Completed: {timestamp}
- Files modified: {list}
- Verification: {PASS/FAIL}
```

---

## MISSION

Enhance the `/validate-stories` slash command to add **custody chain auditing** — tracing provenance from brainstorms through requirements, epics, sprints, and into stories. This detects broken chains, missing ADRs, circular dependencies, ambiguous acceptance criteria, and stale labels that the current context-only validation misses.

**You are modifying 2 files in the framework's `src/` tree.** Do NOT modify operational files in `.claude/` directly.

---

## SCOPE: 2 Files to Modify

| # | File to Modify (src/ tree) | Operation | Est. Lines |
|---|---------------------------|-----------|------------|
| 1 | `src/claude/commands/validate-stories.md` | **REPLACE** entire file | ~670 lines |
| 2 | `src/claude/skills/implementing-stories/references/context-validation.md` | **APPEND** new section after existing content | ~200 lines added |

---

## EXISTING FILE CONTEXT

Before modifying, understand what exists:

### File 1: `validate-stories.md` (current state)
- 316 lines, 6-phase command
- Phase 1: Input Resolution (STORY-XXX, all, --since=)
- Phase 2: Story Discovery (Glob)
- Phase 3: Context File Loading (6 files)
- Phase 4: Story Validation (per-story against context files)
- Phase 5: Generate Report (display only, NOT persisted)
- Phase 6: Interactive Resolution (single-story fix-up)
- **Key gap:** No custody chain tracing, no persistent output, no resume, no epic/range modes

### File 2: `context-validation.md` (current state)
- ~495 lines, 6 validation functions (#1-6)
- `validate_technologies()`, `validate_file_paths()`, `validate_dependencies()`
- `validate_coverage_thresholds()`, `validate_architecture()`, `validate_anti_patterns()`
- Plus: Greenfield Mode, Resolution Protocol, Report Format, Integration Points, Error Handling, Performance
- **Key gap:** No custody chain functions (provenance, dependency graph, ADR cross-ref, story quality)

---

## TASK 1: Create Progress Tracking File

**Do this first.** Create the progress file so future sessions can resume:

```
devforgeai/specs/Stories/.validate-stories-implementation-progress.md
```

Content:
```markdown
# /validate-stories Enhancement - Implementation Progress

## Status: IN PROGRESS
## Started: {current date}
## Last Updated: {current date}

## Tasks

| # | Task | Status | Files Modified |
|---|------|--------|----------------|
| 1 | Create progress file | COMPLETE | this file |
| 2 | Replace validate-stories.md | PENDING | src/claude/commands/validate-stories.md |
| 3 | Append to context-validation.md | PENDING | src/claude/skills/implementing-stories/references/context-validation.md |
| 4 | Verify backward compatibility | PENDING | n/a |
| 5 | Final review | PENDING | n/a |

## Notes
- All work in src/ tree ONLY
- Zero breaking changes to existing behavior
- Existing 3 argument modes (STORY-XXX, all, --since=) must work identically
```

---

## TASK 2: Replace `src/claude/commands/validate-stories.md`

**Operation:** Replace the entire file content.

**What's new vs existing:**
- Phase 0 (NEW): Enhanced argument parsing with range, epic, --chain, --force + resume detection
- Phase 1 (NEW): Scope discovery + document inventory for chain mode
- Phase 2 (was Phase 3+4): Context validation (PRESERVED, same logic)
- Phase 3 (NEW): Custody chain audit with 4 sub-phases (3a-3d)
- Phase 4 (NEW): Synthesis + report finalization
- Phase 5 (was Phase 5): Session handoff + display (ENHANCED with file output)
- Phase 6 (was Phase 6): Interactive resolution (PRESERVED, extended for chain findings)

**New argument modes added:**
- `STORY-013..STORY-033` — range (auto-enables chain mode)
- `EPIC-XXX` — all stories in epic (auto-enables chain mode)
- `--chain` — combinable flag with any existing mode
- `--force` — regenerate from scratch ignoring existing audit

**Resume mechanism:** The audit output file at `devforgeai/qa/audit/custody-chain-audit-{scope}.md` doubles as the checkpoint. Each phase appends numbered sections (## 1. through ## 8.). On re-invocation, scan for completed sections and offer to resume from the next one.

### COMPLETE REPLACEMENT CONTENT

Write this exact content to `src/claude/commands/validate-stories.md`:

---BEGIN FILE CONTENT---

```
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

   Reference: .claude/skills/implementing-stories/references/context-validation.md

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

   Reference: .claude/skills/implementing-stories/references/context-validation.md
   Section: "Custody Chain Validation Functions" (functions #7-10)

   findings = []
   finding_counter = 1

   # -- 3a: Provenance Tracing (function #7: validate_provenance_chain) --
   # Story -> Epic -> Requirements -> Brainstorm
   # Verify each link in the chain exists and is not broken

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

   # -- 3b: Dependency Graph (function #8: validate_dependency_graph) --
   # Check for circular deps, missing deps, stale status labels

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

   # -- 3c: ADR Cross-Reference (function #9: validate_adr_references) --

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

   # -- 3d: Stale Labels + Ambiguity (function #10: validate_story_quality) --

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
- `.claude/skills/implementing-stories/references/context-validation.md`
  Sections: "Validation Functions" (#1-6) + "Custody Chain Validation Functions" (#7-10)

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
```

---END FILE CONTENT---

**After writing this file, update the progress file: Task 2 = COMPLETE.**

---

## TASK 3: Append to `src/claude/skills/implementing-stories/references/context-validation.md`

**Operation:** APPEND the following content to the END of the existing file. Do NOT modify any existing content.

The existing file ends with a `## Performance Considerations` section. Append the new section AFTER that.

---BEGIN CONTENT TO APPEND---

```
---

## Custody Chain Validation Functions

**Purpose:** Validate inter-document traceability across the spec-driven development chain: brainstorm -> requirements -> epic -> sprint -> story. These functions complement the 6 context file validation functions above.

**Used by:**
- `/validate-stories` command (Phase 3: --chain mode)
- Future CI pipeline integration (custody chain gate)

---

### 7. validate_provenance_chain(story_meta, chain_docs)

**Purpose:** Verify each story traces back to its parent epic, requirements doc, and brainstorm

**Severity:** HIGH (broken chain) or MEDIUM (partial chain)

**Input:** story_meta dict (frontmatter from stories), chain_docs dict (Glob results for all spec layers)

**Process:**

1. Group stories by epic_id from frontmatter

2. FOR each epic_id in scope:
   a. Verify epic file exists on disk
      IF missing: CRITICAL finding ("Epic file not found")

   b. Read epic frontmatter
      Extract: brainstorm_ref, requirements_ref, research_ref

   c. Verify brainstorm back-reference:
      IF brainstorm_ref missing: HIGH finding ("no brainstorm back-reference")
      IF brainstorm_ref file not found: HIGH finding ("broken brainstorm reference")

   d. Verify requirements back-reference:
      IF requirements_ref path not found: MEDIUM finding ("broken requirements reference")

   e. Verify research ID consistency across chain:
      Extract research IDs from brainstorm, requirements, and epic
      IF mismatched IDs: HIGH finding ("research ID mismatch")
      IF path case mismatch (specs/research/ vs specs/Research/): MEDIUM finding

3. Return findings list

---

### 8. validate_dependency_graph(story_meta)

**Purpose:** Validate inter-story dependency DAGs for cycles, missing deps, stale labels, undeclared coupling

**Severity:** CRITICAL (cycles), HIGH (missing deps, undeclared coupling), MEDIUM (stale labels)

**Input:** story_meta dict with depends_on arrays

**Process:**

1. Build adjacency list: { story_id: [depends_on_ids] }

2. Cycle detection (BFS/DFS):
   FOR each story_id:
     Walk dependency chain tracking visited set
     IF revisit detected: CRITICAL finding ("circular dependency: A -> B -> C -> A")

3. Missing dependency detection:
   FOR each depends_on entry:
     IF target story_id has no file on disk: HIGH finding ("depends on non-existent story")

4. Stale status label detection:
   FOR each story's dependency table:
     Compare listed_status against target story's actual frontmatter status
     IF mismatch: MEDIUM finding ("lists DEP as 'Backlog' but actual is 'Ready for Dev'")

5. Undeclared mutual dependency detection:
   FOR each pair of stories (A, B) in scope:
     IF A's ACs/spec text references B's types/structs/interfaces
     AND A does NOT list B in depends_on:
       HIGH finding ("A references B but doesn't declare depends_on")

6. Return findings list

---

### 9. validate_adr_references(story_meta, chain_docs)

**Purpose:** Verify ADR references in stories are valid and accepted

**Severity:** CRITICAL (ADR TBD blocking implementation), HIGH (broken/unaccepted ADR)

**Input:** story_meta dict, chain_docs.adrs list

**Process:**

1. FOR each story in scope:

   a. Scan for "ADR TBD" or "ADR-TBD" text:
      IF found: CRITICAL finding ("unresolved ADR TBD - implementation blocked")

   b. Extract all ADR-NNN references via regex:
      FOR each unique ADR reference:
        Verify file exists in adrs/ directory
        IF missing: HIGH finding ("references ADR-NNN which has no file")

        IF file exists:
          Read ADR file, extract status field
          IF status == "proposed": HIGH finding ("ADR not yet accepted")
          IF status == "superseded":
            Extract superseded_by field
            MEDIUM finding ("references superseded ADR - update to successor")

2. Return findings list

---

### 10. validate_story_quality(story_meta)

**Purpose:** Detect ambiguity, broken file references, and internal inconsistency within story documents

**Severity:** HIGH (ambiguous ACs, internal contradiction), MEDIUM (broken refs, path issues)

**Input:** story_meta dict

**Process:**

1. FOR each story:

   a. Ambiguous AC detection:
      Grep for "(or {word})" patterns in AC text
      IF found: HIGH finding ("ambiguous AC text - pick one definitive answer")

   b. Internal inconsistency:
      Compare AC assertions against Design Decisions section
      IF contradiction found (e.g., AC says "Variable or Constant" but Design says "Variable"):
        HIGH finding ("AC contradicts design decision")

   c. Broken file path references:
      Extract all src/ file paths from tech spec
      FOR each concrete path (not wildcard):
        IF file does not exist AND story does not mark it as "new file to create":
          MEDIUM finding ("references non-existent file")

   d. Path case sensitivity:
      Grep for "specs/research/" (lowercase)
      IF found: MEDIUM finding ("wrong case - should be 'specs/Research/'")

   e. Unresolved TL items:
      Grep for "TL-\d{3}" items marked as "unresolved" or "pending"
      Count per story
      IF count > 2: MEDIUM finding ("N unresolved technical limitations - high implementation risk")

2. Return findings list

---

### Custody Chain Finding Format

Each finding uses this structure for consistency with the audit report:

  finding_id:   "F-NNN"              # Sequential, assigned during report generation
  severity:     "CRITICAL|HIGH|MEDIUM|LOW"
  type:         "category/specific"  # e.g., "provenance/broken_brainstorm_ref"
  affected:     ["STORY-XXX"]        # List of affected story/epic IDs
  summary:      "One-line description"
  evidence:     "Quoted text from source file (optional)"
  remediation:  "Numbered steps to fix"
  verification: "grep command to confirm fix (optional)"
  phase:        "3a|3b|3c|3d"        # Which sub-phase detected it

---

### Severity Decision Rules

| Severity | Trigger | Examples |
|----------|---------|---------|
| CRITICAL | Blocks TDD Red phase; no workaround | Missing ADR prerequisite, circular dependency, epic file missing |
| HIGH | Context loss causing likely rework (>30% story point risk) | Broken provenance chain, undeclared dependency, ambiguous AC, research ID mismatch |
| MEDIUM | Documentation gap or stale data; no implementation risk | Stale status label, path case mismatch, broken file reference |
| LOW | Known tradeoff, explicitly documented in ADR or design decision | ADR-006 field to Variable mapping, grammar maturity risk |
```

---END CONTENT TO APPEND---

**After writing this content, update the progress file: Task 3 = COMPLETE.**

---

## TASK 4: Verify Backward Compatibility

Run these checks (read-only) to verify existing behavior is preserved:

1. **Argument modes preserved:** Confirm Phase 0 still handles `STORY-XXX`, `all`, and `--since=STORY-XXX` identically to the original (they bypass chain mode entirely, go straight to Phase 2)

2. **Context validation unchanged:** Confirm Phase 2 uses the same 6 validation functions (#1-6) from context-validation.md with the same severity levels

3. **Interactive resolution preserved:** Confirm Phase 6 still offers the same AskUserQuestion flow for single-story mode

4. **No new dependencies:** Confirm no new external tools, skills, or subagents are required for the basic (non-chain) flow

**Update progress file: Task 4 = COMPLETE with verification results.**

---

## TASK 5: Final Review

1. Read both modified files end-to-end
2. Verify validate-stories.md has all 7 phases (0-6) with complete pseudocode
3. Verify context-validation.md has functions #1-10 (6 existing + 4 new)
4. Verify the finding format in context-validation.md matches the Phase 3 usage in validate-stories.md
5. Verify the resume mechanism: Phase 0 section scanning maps correctly to Phase-to-section table

**Update progress file: Task 5 = COMPLETE. Set overall Status: COMPLETE.**

---

## REFERENCE: Real-World Findings This Enhancement Would Detect

These 16 findings were discovered manually on Treelint project stories 013-033. The enhanced command would detect all of them automatically:

| ID | Severity | What It Catches | Phase |
|----|----------|----------------|-------|
| F-001 | CRITICAL | STORY-023 has "ADR TBD" — missing XML parser ADR | 3c |
| F-002 | CRITICAL | STORY-026/027/028 tree-sitter AST node names unknown | 3d (TL items) |
| F-003 | HIGH | STORY-031/032 undeclared mutual dependency | 3b |
| F-004 | HIGH | ADR-006 "add ALL variants first" vs incremental stories | 3c |
| F-005 | HIGH | BRAINSTORM-001 cites RESEARCH-005, downstream uses RESEARCH-001 | 3a |
| F-006 | HIGH | STORY-029 additive principle vs DELIMITER pre-processing | 3d |
| F-007 | HIGH | STORY-020 AC says "Variable (or Constant)" — ambiguous | 3d |
| F-008 | HIGH | STORY-016 three unresolved architectural gaps | 3d (TL items) |
| F-009 | MEDIUM | specs/research/ (lowercase) vs specs/Research/ (actual) | 3d |
| F-010 | MEDIUM | EPIC-002 sprint table shows "TBD" despite stories created | 3a |
| F-011 | MEDIUM | STORY-014/015 dep status says "Backlog" but STORY-013 is "Ready for Dev" | 3b |
| F-012 | MEDIUM | STORY-030 accepts depth 1-5 but only implements depth=1 | 3d |
| F-013 | MEDIUM | STORY-020 constructor name needs undocumented context tracking | 3d |
| F-014 | LOW | ADR-006 field-to-Variable mapping (known tradeoff) | n/a |
| F-015 | LOW | ADR-004 grammar maturity risk (known, has fallback) | n/a |
| F-016 | LOW | STORY-033 shared visited set semantics (documented) | n/a |

---

## RESUMPTION INSTRUCTIONS

If you are a new Claude session reading this for the first time:

1. Read `devforgeai/specs/Stories/.validate-stories-implementation-progress.md`
2. Find the first task with status `PENDING`
3. Execute that task following the instructions above
4. Update the progress file after completing each task
5. Continue until all 5 tasks are COMPLETE

If the progress file does not exist, start at Task 1.
