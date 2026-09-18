# Phase 03: Technical Specification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=stories --from=02 --to=03 --project-root=.
```

| Exit Code | Action |
|-----------|--------|
| 0 | Prerequisites met. Proceed. |
| 1 | Phase 02 incomplete. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

- **PURPOSE:** Define API contracts, data models, business rules, and dependencies using v2.0 structured YAML format
- **REQUIRED SUBAGENTS:** api-designer (CONDITIONAL - only if API endpoints detected)
- **REQUIRED ARTIFACTS:** Technical specification in v2.0 YAML format with components, business_rules, non_functional_requirements
- **STEP COUNT:** 7
- **REFERENCE FILES:**
  - `references/technical-specification-creation.md`
  - `references/technical-specification-guide.md` (index — lists sub-files; loaded in Step 3.2.5 based on API type)
  - `.claude/skills/spec-driven-stories/assets/templates/story-template.md` (template, read fresh for SECTION_MANIFEST — TCR-004)

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-stories/references/technical-specification-creation.md")
Read(file_path=".claude/skills/spec-driven-stories/assets/templates/story-template.md")
```

Note: The monolithic guide is NOT loaded unconditionally here. Step 3.2.5 loads the relevant domain sub-file (REST, GraphQL, or gRPC variant) after Step 3.2 detects the API type. Non-API stories load no sub-file.

IF any Read fails: HALT -- "Phase 03 reference files not loaded."

---

## Mandatory Steps (6)

### Step 3.1: Evidence-Verification Pre-Flight (RCA-020)

**EXECUTE:**
```
# Identify target files that the technical specification will reference
target_files = extract file references from $REQUIREMENTS_OUTPUT

FOR each target_file in target_files:
  TRY:
    Read(file_path=target_file)
    Display: "Verified: {target_file} exists"
  CATCH:
    Display: "WARNING: Referenced file {target_file} does not exist"
    Remove from target_files list
```

**VERIFY:** All referenced target files have been verified (existing or removed from references).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.1 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.1")`

---

### Step 3.2: Detect API Needs

**EXECUTE:**
```
# Sprint 4.2 — PRIMARY path: CLI validator replaces inline keyword-scan loop.
# Contract: src/claude/scripts/devforgeai_cli/validators/indicators.py (Sprint 4.1).
# The CLI scans both API and UI indicators in one call; Phase 04 reuses the UI half.
# Exit codes: 0 = scan completed (always, regardless of detection), 2 = IO, 127 = CLI absent.
# Requirements output is written by Phase 02; we write it to a scratch file first so
# the CLI can read from disk.
scratch_path = "tmp/${SESSION_ID}/phase-outputs/phase-02-requirements.txt"
Write(file_path=scratch_path, content=$REQUIREMENTS_OUTPUT)

cli_result = Bash(f"devforgeai-validate detect-indicators --story-file={scratch_path} --format=json")

IF cli_result.exit_code == 0:
    parsed = json_parse(cli_result.stdout)
    detect_indicators_hint = parsed            # retain raw scanner output as an auditable HINT (never the routing authority)
    raw_api_detected = parsed.api_detected
    Display: f"API keyword hint (raw): {raw_api_detected} (indicators: {parsed.api_indicators_found}, Sprint 4.2)"
ELSE IF cli_result.exit_code == 127:
    # CLI absent — fall back to inline keyword loop (deprecated).
    api_indicators = ["endpoint", "API", "REST", "GraphQL", "gRPC", "HTTP", "POST", "GET", "PUT", "DELETE"]
    raw_api_detected = false

    FOR each indicator in api_indicators:
      IF indicator found in $REQUIREMENTS_OUTPUT (case-insensitive):
        raw_api_detected = true
        break

    detect_indicators_hint = {"api_detected": raw_api_detected, "source": "inline-fallback"}
    Display: f"API keyword hint (raw, inline fallback): {raw_api_detected} (CLI exit 127)"
ELSE:
    HALT: f"detect-indicators CLI unexpected exit {cli_result.exit_code}: {cli_result.stdout}"

# === CROSS-CHECK (Issue-719): the keyword hint ENABLES api-designer; the tech-spec component-type skeleton is the authoritative OVERRIDE that can only SUPPRESS it (never force it). ===
# The keyword scanner false-positives on prose — e.g. C# property getters ("GET"), "API host" infrastructure prose —
# for pure-backend stories (incident SEED-002 / COMP-001, a domain kernel with zero HTTP surface). The raw boolean is
# a HINT only. Two-pass fix: build a lightweight component-type SKELETON first (the minimum authority needed BEFORE the
# api-designer gate), then reconcile the routing boolean against it. The FULL tech-spec is generated later in Step 3.4.
#
# Pass 1 — Generate the tech-spec component skeleton (component TYPES ONLY; no endpoints / request-response schemas / OpenAPI yet).
TECH_SPEC_SKELETON = derive component list from ($FEATURE_DESCRIPTION + $REQUIREMENTS_OUTPUT):
    each component = {name, type, file_path}
    type ∈ {Service, Worker, Configuration, Logging, Repository, API, DataModel}   # the 7 valid tech-spec component types
Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-03-tech-spec-skeleton.yaml", content=TECH_SPEC_SKELETON)

# Pass 2 — Reconcile: api-designer routes ONLY when the skeleton declares at least one type:API component.
skeleton_types = [c.type for c in TECH_SPEC_SKELETON.components]
has_api_component = ("API" in skeleton_types)
api_detected = raw_api_detected AND has_api_component                              # api_detected is now the RECONCILED routing boolean

IF raw_api_detected AND NOT has_api_component:
    api_override_reason = "raw detect-indicators api_detected=true but the tech-spec skeleton has zero type:API components; keyword hit came from non-HTTP prose — api-designer suppressed"
    Display: f"CROSS-CHECK: {api_override_reason}"
    Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-03-cross-check.json", content={"detect_indicators_hint": detect_indicators_hint, "api_designer_override_reason": api_override_reason, "tech_spec_skeleton_types": skeleton_types})
ELSE:
    api_override_reason = null
    Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-03-cross-check.json", content={"detect_indicators_hint": detect_indicators_hint, "api_designer_override_reason": null, "tech_spec_skeleton_types": skeleton_types})
```

**VERIFY:** `api_detected` is boolean AND equals `raw_api_detected AND has_api_component` (the reconciled value Step 3.3 routes on). `tmp/${SESSION_ID}/phase-outputs/phase-03-cross-check.json` exists and contains `detect_indicators_hint` + `api_designer_override_reason` regardless of the override outcome (the gate decision is persisted and auditable).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.2 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2")`

---

### Step 3.2.5: Load Domain Guide Sub-Reference (Progressive Disclosure)

**EXECUTE:**
```
IF api_detected == true:
    # Determine API type from detect-indicators output
    api_type = parsed.api_type  # "rest" | "graphql" | "grpc" | "unknown"

    IF api_type == "graphql":
        Read(file_path=".claude/skills/spec-driven-stories/references/technical-specification-guide-graphql.md")
        Display: "Loaded: technical-specification-guide-graphql.md"
    ELSE IF api_type == "grpc":
        Read(file_path=".claude/skills/spec-driven-stories/references/technical-specification-guide-grpc.md")
        Display: "Loaded: technical-specification-guide-grpc.md"
    ELSE:  # REST or unknown API type — default to REST guide
        Read(file_path=".claude/skills/spec-driven-stories/references/technical-specification-guide-rest.md")
        Display: "Loaded: technical-specification-guide-rest.md"
ELSE:
    Display: "No API detected — skipping guide sub-reference (saves ~350 context lines)"
```

**VERIFY:** If `api_detected == true`, the appropriate sub-reference file was loaded.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.2.5 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.2.5")`

---

### Step 3.3: Invoke api-designer (CONDITIONAL)

**EXECUTE:**
```
# `api_detected` here is the RECONCILED routing boolean from Step 3.2's CROSS-CHECK (Issue-719) —
# never the raw keyword hint. A backend-only story whose keyword scan tripped on prose reaches this
# step with api_detected=false and correctly skips api-designer.
IF api_detected == true:
  # Pre-invocation snapshot
  pre_snapshot_count = count files in workspace

  # Read contract
  Read(file_path=".claude/skills/spec-driven-stories/contracts/api-designer-contract.yaml")

  # Invoke api-designer subagent
  Agent(subagent_type="api-designer") with prompt:
    - Feature: $FEATURE_DESCRIPTION
    - Requirements: $REQUIREMENTS_OUTPUT
    - Format: v2.0 structured YAML
    - Instructions: Generate API contracts, endpoints, request/response schemas

  $API_SPEC = captured output

  # Post-invocation verification
  post_snapshot_count = count files in workspace
  IF post_snapshot_count > pre_snapshot_count:
    Display: "WARNING: api-designer created unauthorized files"

ELSE:
  $API_SPEC = null
  Display: "No API endpoints detected. Skipping api-designer invocation."
```

**VERIFY:** If api_detected, `$API_SPEC` contains API contract YAML. If not api_detected, step explicitly skipped.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.3 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.3")`

---

### Step 3.4: Generate Technical Specification (v2.0 YAML)

**EXECUTE:**
```
# Build v2.0 structured YAML technical specification
# Reference: technical-specification-creation.md for v2.0 schema

$TECH_SPEC = construct YAML block with:
  technical_specification:
    components:
      - For each component identified in requirements:
        - name, type (Service/Worker/Configuration/API/Repository/DataModel/Logging)
        - description, file_path, dependencies
        - test_requirement (what to test for this component)
    business_rules:
      - For each business rule identified:
        - name, description, validation_logic
        - test_requirement
    non_functional_requirements:
      - For each NFR from Phase 02:
        - category, requirement, metric, threshold

IF $API_SPEC is not null:
  Merge API contracts into components section

Display: "Technical specification generated (v2.0 YAML format)"
Display: "  Components: {component_count}"
Display: "  Business rules: {rule_count}"
Display: "  NFRs: {nfr_count}"

# Self-containment mandate: embed technical details inline
IF any component has type "DataModel" or "Configuration":
    Embed complete JSON/YAML schema with field names, types, constraints, and 1 concrete example

IF any component has file_path containing "cli.py" or "commands/":
    Embed CLI command specification per command:
      - Synopsis (1 line)
      - Positional arguments with types
      - Flags with name, type, default, required/optional
      - Exit codes with meanings
      - 1 example invocation

IF $POINTS >= 5:
    Embed at least 1 concrete data example (valid JSON/YAML with real values, not placeholders)
```

**VALIDATE:**
```
# Sprint A (STORY-646): Validate generated YAML tech spec structure via CLI
# $STORY_FILE is the draft story file being assembled; CLI validates v2.0 YAML format.
cli_vts = Bash(f"devforgeai-validate validate-tech-spec --story-file={$SESSION_ID or $STORY_FILE} --format=json")
IF cli_vts.exit_code == 0:
  Display: "Technical specification: valid v2.0 structure (validate-tech-spec CLI, STORY-646)"
ELSE IF cli_vts.exit_code == 1:
  cli_parsed = json_parse(cli_vts.stdout)
  Display: f"WARNING: Tech spec {cli_parsed.error_count} error(s) — review before Phase 05"
ELSE IF cli_vts.exit_code == 127:
  Display: "WARNING: validate-tech-spec CLI not installed — skipping structured YAML validation (exit 127)"
```

**VERIFY:** `$TECH_SPEC` contains valid YAML with `components`, `business_rules`, and `non_functional_requirements` keys.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.4 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.4")`

---

### Step 3.5: Identify Dependencies

**EXECUTE:**
```
# Extract dependencies from technical specification
$DEPENDENCIES = {
  prerequisite_stories: [],  # STORY-NNN that must complete first
  external_dependencies: [], # External services, APIs
  technology_dependencies: [] # Libraries, frameworks from tech-stack.md
}

# Validate technology dependencies against tech-stack.md
Read(file_path="devforgeai/specs/context/tech-stack.md")
FOR each tech_dep in $DEPENDENCIES.technology_dependencies:
  IF tech_dep NOT found in tech-stack.md:
    HALT: "Technology {tech_dep} not in tech-stack.md. Cannot proceed without ADR."
```

**VERIFY:** Dependencies list populated. All technology dependencies in tech-stack.md.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.5 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.5")`

---

### Step 3.6: Generate Implementation Guide (CONDITIONAL)

**EXECUTE:**
```
IF $TYPE == "feature" AND $POINTS >= 5:
  # 1. Scan Phase 02 output for implementation elements
  implementation_elements = scan $REQUIREMENTS_OUTPUT for <implementation> blocks
  task_hints = extract task_hint sub-elements from each implementation element
  cross_cutting_concerns = extract cross-cutting patterns from approach elements

  # 2. Derive Implementation Guide subsections from SECTION_MANIFEST (TCR-004)
  # Sprint 4.2 — PRIMARY path: CLI validator replaces inline find()+parse_yaml().
  # Contract: src/claude/scripts/devforgeai_cli/validators/manifest.py (Sprint 4.1).
  # Exit codes: 0 = parsed OK, 1 = validation errors (HALT), 2 = IO, 127 = CLI absent.
  cli_result = Bash("devforgeai-validate parse-manifest --template-file=.claude/skills/spec-driven-stories/assets/templates/story-template.md --format=json")

  IF cli_result.exit_code == 0:
    $PARSED_MANIFEST = json_parse(cli_result.stdout).parsed_manifest
    Display: f"SECTION_MANIFEST parsed via CLI (Sprint 4.2)"
  ELSE IF cli_result.exit_code == 1:
    HALT: f"parse-manifest CLI reported errors: {cli_result.stdout}"
  ELSE IF cli_result.exit_code == 127:
    # CLI absent — inline fallback (deprecated).
    manifest_start = find("<!-- SECTION_MANIFEST", story_template_content)
    manifest_end = find("END_SECTION_MANIFEST -->", story_template_content)

    IF manifest_start is not found OR manifest_end is not found:
      HALT: "SECTION_MANIFEST markers not found in template — template may be pre-v3.0"

    manifest_raw = story_template_content[manifest_start..manifest_end]
    manifest_yaml = strip_comment_markers(manifest_raw)
    $PARSED_MANIFEST = parse_yaml(manifest_yaml)
  ELSE:
    HALT: f"parse-manifest CLI unexpected exit {cli_result.exit_code}: {cli_result.stdout}"

  # Sprint 3.2 — Persist parsed_manifest to phase-output cache for Phase 05.2 reuse.
  # Contract: src/claude/skills/spec-driven-stories/contracts/phase-output-schema.json (phase03Output).
  # Writing here (not at Exit Gate) because parsed_manifest is conditional on this IF branch;
  # when branch is skipped, phase-03.json.parsed_manifest remains null and Phase 05.2 falls back to re-parse.
  Bash("mkdir -p tmp/${SESSION_ID}/phase-outputs")
  Write(file_path="tmp/${SESSION_ID}/phase-outputs/phase-03.json",
        content=json_serialize({
          "schema_version": "1.0",
          "phase_id": "03",
          "technical_specification_yaml": $TECH_SPEC_YAML,
          "parsed_manifest": $PARSED_MANIFEST
        }))

  # Filter for Implementation Guide subsections: h3 entries within IG line range
  # Use the Implementation Guide h2 entry's line_range to scope the filter dynamically
  $IG_PARENT = find_entry($PARSED_MANIFEST.sections, name="Implementation Guide", header_level=2)
  $IG_SUBSECTIONS = filter($PARSED_MANIFEST.sections,
    header_level=3,
    line_range.start >= $IG_PARENT.line_range.start,
    line_range.start <= $IG_PARENT.line_range.end)
  $IG_SUBSECTIONS = sort_by($IG_SUBSECTIONS, line_range.start)

  # HALT guard: empty subsection list (AC#4)
  IF len($IG_SUBSECTIONS) == 0:
    HALT: "SECTION_MANIFEST contains zero Implementation Guide subsections — template may be malformed or pre-v3.0"

  Display: "Implementation Guide: {len($IG_SUBSECTIONS)} subsections from SECTION_MANIFEST"

  # 3. Build Implementation Guide by iterating over manifest-derived subsections
  # Content generation strategy dictionary maps subsection names to content sources
  content_strategy = {
    "Architecture Decisions": from tech spec component relationships,
    "Cross-Cutting Concerns": from approach elements,
    "Implementation Sequence": topological sort of ACs by dependency,
    "Task Prompt Templates": from task_hint elements,
    "Anti-Patterns": from rationale "Do NOT" patterns,
    "Patterns and References": from existing code patterns, similar stories, design pattern references
  }

  $IMPLEMENTATION_GUIDE = ""
  FOR each subsection in $IG_SUBSECTIONS:
    IF subsection.name in content_strategy:
      content = generate_content(content_strategy[subsection.name])
    ELSE:
      content = "<!-- TODO: Content generation for '{subsection.name}' — new subsection added to template -->"
    $IMPLEMENTATION_GUIDE += format_subsection(subsection.name, content)

  Display: "Implementation Guide generated (feature story >= 5 pts)"

ELSE:
  $IMPLEMENTATION_GUIDE = null
  IF zero implementation elements found:
    Display: "Implementation Guide: N/A (no implementation elements in requirements)"
  ELSE:
    Display: "Implementation Guide: N/A ($TYPE type, $POINTS pts — below threshold)"
```

**VERIFY:** $IMPLEMENTATION_GUIDE is set (full content or null). Variable is available for Phase 05. If non-null, subsections are manifest-derived (TCR-004 compliant).

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=stories --phase=03 --step=3.6 --project-root=.
```
Update checkpoint: `phases["03"].steps_completed.append("3.6")`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=stories --phase=03 --checkpoint-passed --project-root=.
```

## Exit Verification Checklist

- [ ] Technical specification in v2.0 YAML format
- [ ] At least 1 component defined
- [ ] Business rules section present (may be empty for simple stories)
- [ ] NFR section present with measurable metrics
- [ ] All technology dependencies validated against tech-stack.md
- [ ] If API detected: api-designer output integrated
- [ ] Implementation Guide populated (full content for feature >= 5pts, null otherwise)

IF any unchecked: HALT -- "Phase 03 exit criteria not met"

## Phase Transition Display

```
Display: "Phase 03 complete. Technical specification generated."
Display: "Proceeding to Phase 04: UI Specification..."
```

## Hook-backed OUT-Attestation

This phase has Phase-D dispatch entries in `subagent_out_attestation_registry.json`. When dispatching those named subagents, instruct them to return a `subagent-result-v1` result that includes `coverage_attestation` in the normal response. Phase completion is blocked by `subagent-out-attestation-gate.sh` when the hook-owned ledger line lacks `coverage_attestation_present:true`. This Phase-D path is OUT-attestation-only and does not require `tmp/<WORK_ID>/handoffs/`.
