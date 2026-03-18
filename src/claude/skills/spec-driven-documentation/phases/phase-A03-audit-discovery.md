# Phase A03: Audit Discovery

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=02 --to=A03 --workflow=doc-audit
# Exit 0: proceed | Exit 1: Phase 02 incomplete
```

## Contract

PURPOSE: Inventory all documentation files, read entry points (README), inventory community files (LICENSE, CONTRIBUTING, etc.), check configuration alignment (manifest vs docs).
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: File inventory, community file checklist, configuration discrepancies
STEP COUNT: 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-workflow.md")
```

IF Read fails: HALT -- "Phase A03 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step A03.1: Inventory Documentation Files

EXECUTE: Discover all documentation files in the project.
```
docs_files = Glob(pattern="docs/**/*.md")
root_md = Glob(pattern="*.md")

all_docs = docs_files + root_md
# Exclude non-documentation files (story files, ADRs, context files, skill files)
filtered_docs = filter out patterns:
    - devforgeai/specs/**
    - .claude/**
    - src/claude/**
    - node_modules/**

Display: "Documentation files found: {len(filtered_docs)}"
FOR each file in filtered_docs:
    Display: "  {file}"
```
VERIFY: filtered_docs is a list (may be empty for new projects).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A03 --step=A03.1 --workflow=doc-audit`

---

### Step A03.2: Read Entry Points

EXECUTE: Read primary documentation entry points.
```
entry_points = ["README.md", "docs/README.md", "docs/index.md"]
loaded_entries = {}

FOR each entry in entry_points:
    result = Read(file_path=entry)
    IF Read succeeds:
        loaded_entries[entry] = result
        Display: "  Entry point loaded: {entry} ({len(result)} chars)"
    ELSE:
        Display: "  Entry point missing: {entry}"

IF loaded_entries is empty:
    Display: "WARNING: No entry points found (README.md missing)"
```
VERIFY: At least README.md was attempted. loaded_entries dict populated with available files.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A03 --step=A03.2 --workflow=doc-audit`

---

### Step A03.3: Inventory Community Files

EXECUTE: Check existence of standard community/OSS files.
```
community_checklist = {
    "LICENSE": false,
    "LICENSE-MIT": false,
    "LICENSE-APACHE": false,
    "CONTRIBUTING.md": false,
    "CODE_OF_CONDUCT.md": false,
    "SECURITY.md": false,
    ".github/ISSUE_TEMPLATE/bug_report.md": false,
    ".github/ISSUE_TEMPLATE/feature_request.md": false,
    ".github/PULL_REQUEST_TEMPLATE.md": false
}

FOR each file, _ in community_checklist:
    result = Glob(pattern=file)
    IF found:
        community_checklist[file] = true

present_count = count(true values)
total_count = len(community_checklist)
Display: "Community files: {present_count}/{total_count} present"
FOR file, exists in community_checklist:
    status = "present" if exists else "MISSING"
    Display: "  [{status}] {file}"
```
VERIFY: community_checklist fully populated with boolean values.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A03 --step=A03.3 --workflow=doc-audit`

---

### Step A03.4: Check Configuration Alignment

EXECUTE: Compare project manifest with documentation claims.
```
# Detect project manifest
manifests = ["package.json", "Cargo.toml", "pyproject.toml", "pom.xml", "go.mod"]
manifest_path = null
manifest_data = {}

FOR each manifest in manifests:
    result = Read(file_path=manifest)
    IF Read succeeds:
        manifest_path = manifest
        # Extract: license, version, engine/MSRV, project name
        manifest_data = parse_manifest(result)
        Display: "  Manifest: {manifest_path}"
        Display: "    License: {manifest_data.license}"
        Display: "    Version: {manifest_data.version}"
        break

IF manifest_path is null:
    Display: "  No project manifest found -- skipping config alignment"
ELSE:
    # Compare against README/docs
    discrepancies = []

    IF "README.md" in loaded_entries:
        readme = loaded_entries["README.md"]

        # Check version consistency
        IF manifest_data.version and manifest_data.version not in readme:
            discrepancies.append("Version {manifest_data.version} in manifest but not in README")

        # Check license consistency
        IF manifest_data.license and manifest_data.license not in readme:
            discrepancies.append("License '{manifest_data.license}' in manifest but not in README")

        # Check prerequisites
        IF manifest_data.engine_version:
            IF manifest_data.engine_version not in readme:
                discrepancies.append("Engine version {manifest_data.engine_version} not in README prerequisites")

    IF discrepancies:
        Display: "  Configuration discrepancies found:"
        FOR each d in discrepancies:
            Display: "    - {d}"
    ELSE:
        Display: "  Configuration alignment: OK"
```
VERIFY: Configuration check completed. Discrepancies recorded for scoring.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A03 --step=A03.4 --workflow=doc-audit`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=A03 --checkpoint-passed --workflow=doc-audit
```

## Phase Transition Display

```
Display: "Phase A03 complete: Audit Discovery"
Display: "  Docs files: {len(filtered_docs)}"
Display: "  Community: {present_count}/{total_count}"
Display: "  Discrepancies: {len(discrepancies)}"
Display: "  Proceeding to Phase A04: Audit Analysis"
```
