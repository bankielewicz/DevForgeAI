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

### Archive-Fallback Helper (used by all referencer checks below)

When a frontmatter referencer field declares a literal path that does not exist on disk, the file may have been moved to an `archive/` or `archive/long-term/` subdirectory without the referencer being updated. Before emitting a `broken_*_ref` finding, run the archive-fallback Glob to determine whether the artifact actually exists at an archive location.

```
function find_file_with_archive_fallback(referenced_path, chain_doc_list) -> (resolved_path, status):
  IF file_exists(referenced_path):
    return (referenced_path, "present")

  # Literal path missing. Fall back: glob the basename under the parent spec directory
  # to detect archive relocation (e.g., requirements/ -> requirements/archive/).
  basename = Path(referenced_path).name
  spec_root = top_level_spec_directory_of(referenced_path)   # e.g., "devforgeai/specs/requirements"
  archive_matches = [f for f in Glob(pattern=f"{spec_root}/**/{basename}") if f != referenced_path]

  IF archive_matches:
    return (archive_matches[0], "archived")   # File exists, but referencer path is stale

  return (None, "missing")                     # File genuinely absent
```

This helper distinguishes three cases:

| Status | Severity | Finding type | Meaning |
|---|---|---|---|
| `present` | (no finding) | — | Referencer correct, file at declared path |
| `archived` | MEDIUM | `provenance/stale_referencer_path` | File exists, but at an archive path; referencer not updated |
| `missing` | HIGH | `provenance/broken_*_ref` | File genuinely absent anywhere |

Sub-phase 3a's individual checks (brainstorm_ref, requirements_ref, plan_file) all use this helper instead of bare `file_exists()`. Rationale: ADR-XXX-style stale-referencer-detection per `qa/audit/custody-chain-audit-STORY-573.md` Rev 3.

### Marker Allowlist (Template-Upgrade Compatibility)

Before emitting `provenance/broken_brainstorm_ref` or related missing-provenance findings, consult the per-story `flags.provenance_intentionally_deferred` flag (set by Rule 7 in `template-version-validation.md`).

```
IF story.flags.provenance_intentionally_deferred == true:
  # The story's Provenance section contains <!-- AUDIT-DEFERRED: template/section_content_pending --> marker.
  # This is an intentional scaffold inserted by /fix-story --upgrade, NOT a broken brainstorm reference.
  SKIP emission of provenance/broken_brainstorm_ref for this story.
```

Equivalent textual check (when the flag is not available — e.g., manual Phase 3 invocation): inspect the `## Provenance` section body for the regex `<!--\s*AUDIT-DEFERRED:\s*template/section_content_pending`. If present, treat as intentional deferral.

This allowlist prevents `/fix-story --upgrade`-inserted Provenance scaffolds from being re-flagged on subsequent `/validate-stories` runs.

### Detection Logic

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
    # Use archive-fallback helper to distinguish missing from stale-archived path
    brainstorm_file, brainstorm_status = find_file_with_archive_fallback(brainstorm_ref, chain_docs.brainstorms)
    IF brainstorm_status == "missing":
      findings.append(F(finding_counter, "HIGH", [epic_id],
        summary=f"{epic_id} references {brainstorm_ref} which does not exist on disk",
        type="provenance/broken_brainstorm_ref",
        remediation="Create brainstorm or fix reference"))
    ELIF brainstorm_status == "archived":
      findings.append(F(finding_counter, "MEDIUM", [epic_id],
        summary=f"{epic_id} brainstorm_ref points at literal path that doesn't exist, but file is at {brainstorm_file}",
        type="provenance/stale_referencer_path",
        evidence=f"Declared: {brainstorm_ref}; actual: {brainstorm_file}",
        remediation=f"Update {epic_id} brainstorm frontmatter to {brainstorm_file}, OR move file back to {brainstorm_ref}"))

  # Check: epic -> requirements reference
  req_ref = extract_field(epic_content, "requirements_ref")
  IF req_ref is not null:
    req_file, req_status = find_file_with_archive_fallback(req_ref, chain_docs.requirements)
    IF req_status == "missing":
      findings.append(F(finding_counter, "HIGH", [epic_id],
        summary=f"{epic_id} requirements_ref path not found anywhere: {req_ref}",
        type="provenance/broken_requirements_ref",
        remediation="Create the requirements doc, fix the path, or remove the field"))
    ELIF req_status == "archived":
      findings.append(F(finding_counter, "MEDIUM", [epic_id],
        summary=f"{epic_id} requirements_ref points at literal path that doesn't exist, but file is at {req_file}",
        type="provenance/stale_referencer_path",
        evidence=f"Declared: {req_ref}; actual: {req_file}",
        remediation=f"Update {epic_id} requirements_ref to {req_file}, OR move file back to {req_ref}"))

  # Check: epic -> plan_file reference (plan files live under .claude/plans/, not /devforgeai/specs/,
  # so archive-fallback only applies to spec-tree referencers above).
  #
  # Three-step classifier (per STORY-573 Rev 8 audit F-007 Option A, 2026-05-11):
  #   1. Null/empty value -> epic explicitly declares no plan; no finding.
  #   2. "deleted (was: <name>)" breadcrumb pattern -> intentional historical marker
  #      for plans deleted BEFORE .claude/rules/workflow/plan-file-archive.md existed;
  #      no finding (the breadcrumb preserves the original plan name; future deletions
  #      are blocked by the rule's HALT trigger so no new instances of this pattern
  #      should appear).
  #   3. Any other non-null value -> treat as path; emit broken_plan_ref if missing.
  plan_ref = extract_field(epic_content, "plan_file")

  IF plan_ref is null OR plan_ref is empty:
    # Step 1: no plan declared; nothing to check.
    PASS

  ELIF plan_ref matches regex /^"?deleted \(was:.*\)"?$/:
    # Step 2: intentional breadcrumb pattern. The plan was deleted before archive
    # policy existed (or as an explicit user decision to preserve only the name).
    # The pattern is documented in .claude/rules/workflow/plan-file-archive.md.
    # Going forward, plan deletions are blocked by the rule's HALT trigger and
    # archival to .claude/plans/archive/ is required, so this branch is for
    # historical plan losses only — no finding emitted.
    PASS

  ELIF NOT file_exists(plan_ref):
    # Step 3: real path value but file is missing.
    findings.append(F(finding_counter, "MEDIUM", [epic_id],
      summary=f"{epic_id} plan_file path not found: {plan_ref}",
      type="provenance/broken_plan_ref",
      remediation=(
        f"Choose one: (a) restore the plan file at the declared path, "
        f"(b) update plan_file to the current authoritative plan's path, "
        f"(c) archive the plan to .claude/plans/archive/ and update plan_file to the archive path "
        f"(per .claude/rules/workflow/plan-file-archive.md), "
        f"(d) replace with the 'deleted (was: <name>)' breadcrumb pattern if the file was "
        f"deleted before archive policy existed, "
        f"OR (e) remove the field entirely if no plan governs this epic."
      )))

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

**Purpose:** Check for circular deps, missing deps, stale status labels, undeclared coupling, and active-story dependencies on archived prerequisites.

```
# Constant: statuses that indicate an archived/completed story (per template-version-validation.md Filter A).
# Kept as cross-reference documentation; semantically aligned with LONG_TERM_REQUIRED_STATUSES below.
GRANDFATHERED_STATUSES = {"QA Approved", "Released"}

# Constant: statuses required for residency in archive/long-term/ per ADR-064 (Accepted 2026-05-11).
# Invariant: stories in archive/long-term/ MUST have status in this set; stories in archive/
# (non-long-term) may have any status.
LONG_TERM_REQUIRED_STATUSES = {"QA Approved", "Released"}

# Helper: classify a story file's archive tier (per ADR-064 § Decision step 2).
# Replaces the pre-ADR-064 boolean is_archived_path() with a tri-state classifier so
# the active-→-archive check below can distinguish deprecated (archive/) from
# operationally-consumed (archive/long-term/) cross-state dependencies.
function archive_tier(file_path) -> Enum["active", "archive", "archive_long_term"]:
  IF "/archive/long-term/" in file_path:
    return "archive_long_term"
  ELIF "/archive/" in file_path:
    return "archive"
  ELSE:
    return "active"

FOR story_id, meta in story_meta.items():
  current_tier = archive_tier(meta.file)

  FOR dep_id in meta.depends_on:
    # Locate dep file (chain_docs.stories is now recursive — includes archived files)
    dep_meta = story_meta.get(dep_id)
    dep_file = dep_meta.file if dep_meta else find_file(chain_docs.stories, dep_id)

    IF dep_file is None:
      findings.append(F(finding_counter, "HIGH", [story_id],
        summary=f"{story_id} depends on {dep_id} which has no story file",
        type="dependency/missing_story",
        remediation="Create the dependency story or remove the depends_on reference"))
      CONTINUE

    IF dep_meta is None:
      # File exists in chain_docs but not loaded into story_meta (out-of-scope story).
      # Parse its frontmatter just enough to extract status for the next check.
      dep_content = Read(file_path=dep_file)
      dep_meta_lite = parse_yaml_frontmatter(dep_content)
      actual_status = dep_meta_lite.get("status")
    ELSE:
      actual_status = dep_meta.status

    # Existing check: stale status label
    listed_status = extract_dep_listed_status(meta.content, dep_id)
    IF listed_status is not null AND listed_status != actual_status:
      findings.append(F(finding_counter, "MEDIUM", [story_id],
        summary=f"{story_id} lists {dep_id} as '{listed_status}' but actual is '{actual_status}'",
        type="dependency/stale_dependency_status",
        remediation=f"Update dependency table: {dep_id} status -> {actual_status}"))

    # Archive-policy check (refined per ADR-064 Accepted 2026-05-11).
    # Original detection was a single boolean (archived vs not); now tri-state so we
    # distinguish deprecated archive/ (always a defect) from archive/long-term/
    # (expected cross-state pattern; only flag invariant violations).
    # Pre-ADR-064 history: surfaced by qa/audit/custody-chain-audit-STORY-573.md Rev 3 (F-007).
    dep_tier = archive_tier(dep_file)

    IF dep_tier == "archive" AND current_tier == "active":
      # Case 1: active story depends on DEPRECATED archive entry.
      # archive/ holds stories that were withdrawn or superseded — they should NOT
      # be operationally consumed. Active stories declaring depends_on against them
      # indicate the dependent is referencing replaced work and needs to be updated.
      findings.append(F(finding_counter, "MEDIUM", [story_id, dep_id],
        summary=f"{story_id} (active) depends on {dep_id} which is in deprecated archive/ ({actual_status}) at {dep_file}",
        type="dependency/archived_dependency_for_active_story",
        evidence=f"{story_id} status: {meta.status}; {dep_id} archived at: {dep_file} (deprecated tier, not long-term)",
        remediation=(
          f"{dep_id} lives in archive/ (deprecated). Options: "
          f"(a) replace the depends_on with the canonical successor story, "
          f"(b) if {dep_id} is still operationally consumed, move it to archive/long-term/ instead "
          f"(matches the ADR-064 invariant for shipped + still-consumed work), "
          f"OR (c) remove the dep from depends_on if it's purely historical context."
        )))

    ELIF dep_tier == "archive_long_term" AND current_tier == "active":
      # Case 2: active story depends on archive/long-term/ entry.
      # Per ADR-064, this is the EXPECTED pattern — long-term archive holds shipped
      # (QA Approved / Released) stories whose outputs are still operationally consumed.
      # Suppress the finding UNLESS the long-term residency invariant is violated.
      IF actual_status NOT IN LONG_TERM_REQUIRED_STATUSES:
        # Invariant violation: a story in archive/long-term/ must be QA Approved or Released.
        # If it isn't, the tier semantics are broken — flag it for correction.
        findings.append(F(finding_counter, "MEDIUM", [story_id, dep_id],
          summary=f"{story_id} depends on {dep_id} which is in archive/long-term/ but has status='{actual_status}' (violates ADR-064 invariant)",
          type="dependency/archive_long_term_invariant_violation",
          evidence=f"{dep_id} at {dep_file}; status='{actual_status}' NOT IN {LONG_TERM_REQUIRED_STATUSES} (ADR-064 § Decision 'Invariant')",
          remediation=(
            f"archive/long-term/ MUST contain only QA Approved or Released stories. "
            f"Options: (a) promote {dep_id}'s status to QA Approved or Released if shipping is complete, "
            f"(b) move {dep_id} OUT of archive/long-term/ back to the active Stories/ directory if it's not yet shipped, "
            f"OR (c) re-classify by moving {dep_id} to archive/ (non-long-term) if it's deprecated rather than long-term."
          )))
      # ELSE: expected cross-state pattern — NO FINDING emitted.
      #       This is the case STORY-573 → STORY-535/536/537: active story consuming
      #       shipped framework primitives from archive/long-term/. Pre-ADR-064 this
      #       fired F-004/F-005/F-006 (false positives). Post-ADR-064: suppressed.

# Cycle detection
graph = { sid: meta.depends_on for sid, meta in story_meta.items() }
FOR cycle in detect_cycles(graph):
  findings.append(F(finding_counter, "CRITICAL", cycle,
    summary=f"Circular dependency: {' -> '.join(cycle)}",
    type="circular_dependency",
    remediation="Break the cycle by removing one depends_on reference"))

# Undeclared mutual dependency detection — Pass 1 (in-scope pairs, existing behavior)
# Fires when BOTH stories are in story_meta (multi-story scope: --chain over an epic,
# range, or "all" mode). For single-story scope, only the in-scope story is in
# story_meta and this pass cannot fire; Pass 2 below covers that case.
FOR (story_a, story_b) in pairs(story_meta.keys()):
  a_refs_b = story_b in extract_story_refs(story_meta[story_a].content)
  a_declares_b = story_b in story_meta[story_a].depends_on
  IF a_refs_b AND NOT a_declares_b:
    findings.append(F(finding_counter, "HIGH", [story_a, story_b],
      summary=f"{story_a} references {story_b} in ACs/spec but doesn't declare depends_on",
      type="undeclared_dependency",
      remediation=f"Add {story_b} to {story_a} depends_on list"))

# Undeclared dependency to out-of-scope (archived) stories — Pass 2 coverage extension.
# Catches the single-story chain-mode case where story_meta contains only the
# in-scope story but that story references additional stories that live under
# chain_docs.stories (recursive Glob exposes archive/long-term/ per Approach A
# archive-blindness fix landed 2026-05-11). STORY-573 F-006 pattern.
FOR story_a in story_meta.keys():
  referenced_ids = extract_story_refs(story_meta[story_a].content)
  # Filter to IDs that are NOT story_a itself, NOT already declared in depends_on,
  # AND NOT already covered by Pass 1 (i.e., not in story_meta.keys() either).
  candidates = [sid for sid in referenced_ids
                if sid != story_a
                AND sid NOT IN story_meta[story_a].depends_on
                AND sid NOT IN story_meta.keys()]
  FOR sid in candidates:
    # Look up sid in chain_docs.stories (recursive Glob already includes archive/
    # and archive/long-term/ per Phase 1 inventory). Returns matching file path
    # OR empty list if the referenced ID does not resolve to any story file
    # (which would itself be a different finding type — broken_story_reference —
    # handled by Function #10 sub-step 1c). Pass 2 only emits when archive_match
    # is non-empty, i.e., the ref resolves to a real archived story.
    archive_match = [f for f in chain_docs.stories if extract_id(f) == sid]
    IF archive_match:
      # Read the archived story's frontmatter to determine its status for the
      # remediation hint. Skip non-blocking read errors (would degrade to generic
      # remediation text).
      try:
        archived_status = parse_yaml_frontmatter(Read(archive_match[0])).get("status", "unknown")
      except: archived_status = "unknown"

      findings.append(F(finding_counter, "HIGH", [story_a, sid],
        summary=f"{story_a} references {sid} in ACs/spec but doesn't declare depends_on (resolved at archived path {archive_match[0]})",
        type="undeclared_dependency",
        evidence=f"{story_a} content references '{sid}' but depends_on={story_meta[story_a].depends_on}; {sid} lives at {archive_match[0]} with status={archived_status}",
        remediation=f"Add {sid} to {story_a} depends_on list. Use /fix-story (interactive — no --upgrade) to be prompted via AskUserQuestion for the resolution choice. Procedure P10 in template-upgrade-procedures.md.",
        phase="3b"
      ))

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

  # Non-deterministic AC via deferred Open Question (sub-step 1f, F-009 pattern).
  # See context-validation.md Function #10 sub-step 1f for full pseudocode + heuristic.
  # Summary: for each AC, check whether its <then> clause references content whose
  # format/schema is in an unresolved Open Question (semantic-overlap threshold >=2
  # content words OR explicit "format of X" pattern). Emits HIGH `non_deterministic_AC`
  # finding because ac-compliance-verifier in /dev Phase 4.5/5.5 cannot make a DIRECT
  # match against an undefined contract. Resolved interactively via P9 in
  # template-upgrade-procedures.md (user supplies format via AskUserQuestion).

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

---

## Sub-Phase 3f: Cross-Story Template Coherence

**Trigger:** Chain mode only (2+ stories from the same epic in scope).
**Severity:** LOW (advisory)
**Purpose:** Detect template-version mismatches across sibling stories in the same epic. Stories in the same epic SHOULD share the same `format_version`; divergence indicates an incomplete migration that warrants coordinated `/fix-story --upgrade` runs.

```
FOR each epic_id in epics_in_scope:
  epic_stories = [s for s in story_meta.values() if s.epic == epic_id]

  IF len(epic_stories) < 2:
    CONTINUE   # Need at least 2 stories to detect cross-story drift

  versions = {}
  FOR story in epic_stories:
    versions[story.story_id] = story.frontmatter.format_version  # may be None for v1.0-era stories

  unique_versions = set(versions.values())
  IF len(unique_versions) > 1:
    findings.append({
      finding_id:  "TPL-XS-001",                  # cross-story sentinel
      type:        "template/cross_story_drift",
      severity:    "LOW",
      affected:    list(versions.keys()),
      summary:     f"Epic {epic_id} contains {len(unique_versions)} different format_version values: {sorted(filter(None, unique_versions))}",
      evidence:    f"Per-story versions in {epic_id}: {versions}",
      remediation: "Run /fix-story --upgrade on each story to align to canonical template version. Coordinate via /validate-stories EPIC-NNN --chain to verify epic-wide consistency after upgrades.",
      verification: "After upgrades, /validate-stories EPIC-NNN --chain should produce zero template/cross_story_drift findings.",
      phase:       "3f"
    })
```

### Finding Type Prefix

This sub-phase emits findings with the `template/` prefix (not `coherence/`) because it is a template-version concern. `/fix-story` routes `template/cross_story_drift` as **advisory** — no automated fix; resolution is per-story upgrades coordinated by the user.
