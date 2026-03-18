# Phase A04: Audit Analysis

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=A03 --to=A04 --workflow=doc-audit
# Exit 0: proceed | Exit 1: Phase A03 incomplete
```

## Contract

PURPOSE: Score documentation across 4 dimensions (Tone & Personality, Information Architecture, Visual Design & Formatting, Onboarding Friction) with evidence. Run orphan detection algorithm.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: 4-dimension scorecard with evidence, orphan file list
STEP COUNT: 5 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-workflow.md")
```

IF Read fails: HALT -- "Phase A04 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step A04.1: Score Dimension 1 — Tone & Personality

EXECUTE: Analyze documentation tone and voice quality.
```
score_tone = 0  # out of 10
evidence_tone = []

IF "README.md" in loaded_entries:
    readme = loaded_entries["README.md"]

    # Check README opening for WHY vs WHAT
    first_50_lines = readme[:50 lines]
    IF contains value proposition or elevator pitch:
        score_tone += 3
        evidence_tone.append("README opens with value proposition")
    ELSE:
        evidence_tone.append("README opens with WHAT, not WHY")

    # Check for human voice (we/you pronouns)
    Grep(pattern="\\b(we|you|your|our)\\b", content=readme)
    IF matches found:
        score_tone += 2
        evidence_tone.append("Uses human pronouns (we/you)")
    ELSE:
        evidence_tone.append("No human pronouns -- reads as technical manual")

    # Check contributor language (welcoming vs gatekeeping)
    IF "CONTRIBUTING.md" exists:
        contrib = Read(file_path="CONTRIBUTING.md")
        IF contains welcoming language ("welcome", "happy to help", "first-time"):
            score_tone += 2
            evidence_tone.append("CONTRIBUTING.md uses welcoming language")
        ELSE:
            evidence_tone.append("CONTRIBUTING.md lacks welcoming tone")
    ELSE:
        evidence_tone.append("No CONTRIBUTING.md found")

    # Check troubleshooting for empathetic language
    troubleshooting_files = Grep(pattern="troubleshoot", path="docs/", output_mode="files_with_matches")
    IF troubleshooting_files:
        content = Read(file_path=troubleshooting_files[0])
        IF contains empathetic phrasing ("if you see", "this usually means"):
            score_tone += 2
        ELSE:
            evidence_tone.append("Troubleshooting lacks empathetic phrasing")

    # Minimum score for having a README at all
    score_tone += 1

ELSE:
    score_tone = 0
    evidence_tone.append("No README.md found -- cannot score tone")

key_blocker_tone = evidence_tone[0] if score_tone < 5 else "None"
Display: "  Tone & Personality: {score_tone}/10"
```
VERIFY: score_tone is 0-10. evidence_tone has at least 1 entry.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A04 --step=A04.1 --workflow=doc-audit`

---

### Step A04.2: Score Dimension 2 — Information Architecture

EXECUTE: Evaluate documentation organization and navigation.
```
score_ia = 0  # out of 10
evidence_ia = []

# Check for duplicate filenames across directories
filenames = [basename(f) for f in filtered_docs]
duplicates = find_duplicates(filenames)
IF duplicates:
    evidence_ia.append("Duplicate filenames: {duplicates}")
ELSE:
    score_ia += 2
    evidence_ia.append("No duplicate filenames")

# Check for navigation index (docs/README.md or docs/index.md)
IF "docs/README.md" in loaded_entries OR "docs/index.md" in loaded_entries:
    score_ia += 2
    evidence_ia.append("Navigation index exists")
ELSE:
    evidence_ia.append("No docs/README.md or docs/index.md navigation index")

# Check for cross-references between related docs
cross_ref_count = 0
FOR each doc in filtered_docs:
    content = Read(file_path=doc)
    links = extract_markdown_links(content)
    internal_links = filter(links, is_internal)
    cross_ref_count += len(internal_links)

IF cross_ref_count >= len(filtered_docs):
    score_ia += 2
    evidence_ia.append("{cross_ref_count} cross-references found")
ELIF cross_ref_count > 0:
    score_ia += 1
    evidence_ia.append("Some cross-references ({cross_ref_count}) but could be improved")
ELSE:
    evidence_ia.append("No cross-references between docs")

# Check for audience-based routing
IF "README.md" in loaded_entries:
    readme = loaded_entries["README.md"]
    IF contains audience routing ("For users", "For developers", "For contributors"):
        score_ia += 2
        evidence_ia.append("Audience-based routing present")
    ELSE:
        evidence_ia.append("No audience-based routing in README")

# Check for over-documented modules (>3 files for one module)
module_file_counts = count_files_per_module(filtered_docs)
over_documented = [m for m, c in module_file_counts if c > 3]
IF over_documented:
    evidence_ia.append("Over-documented modules: {over_documented}")
ELSE:
    score_ia += 2
    evidence_ia.append("No over-documented modules")

key_blocker_ia = evidence_ia[0] if score_ia < 5 else "None"
Display: "  Information Architecture: {score_ia}/10"
```
VERIFY: score_ia is 0-10. evidence_ia has at least 1 entry.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A04 --step=A04.2 --workflow=doc-audit`

---

### Step A04.3: Score Dimension 3 — Visual Design & Formatting

EXECUTE: Evaluate markdown formatting quality and visual elements.
```
score_visual = 0  # out of 10
evidence_visual = []

# Check for GFM admonitions
admonition_count = 0
FOR each doc in filtered_docs:
    matches = Grep(pattern="> \\[!(NOTE|WARNING|TIP|IMPORTANT|CAUTION)\\]", path=doc, output_mode="count")
    admonition_count += matches

IF admonition_count >= 3:
    score_visual += 2
    evidence_visual.append("{admonition_count} GFM admonitions used")
ELIF admonition_count > 0:
    score_visual += 1
    evidence_visual.append("Some admonitions ({admonition_count}) but could use more")
ELSE:
    evidence_visual.append("No GFM admonitions (> [!NOTE], > [!WARNING], etc.)")

# Check for README badges
IF "README.md" in loaded_entries:
    readme = loaded_entries["README.md"]
    badge_count = count_occurrences("![", readme[:20 lines])
    IF badge_count >= 2:
        score_visual += 2
        evidence_visual.append("{badge_count} badges in README")
    ELSE:
        evidence_visual.append("Few or no badges in README ({badge_count})")

# Check CHANGELOG for Keep a Changelog categories
changelog = Read(file_path="CHANGELOG.md")
IF changelog:
    categories = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security"]
    found_cats = [c for c in categories if "### " + c in changelog]
    IF len(found_cats) >= 3:
        score_visual += 2
        evidence_visual.append("CHANGELOG uses Keep a Changelog categories: {found_cats}")
    ELIF len(found_cats) > 0:
        score_visual += 1
    ELSE:
        evidence_visual.append("CHANGELOG doesn't use Keep a Changelog categories")
ELSE:
    evidence_visual.append("No CHANGELOG.md found")

# Check for oversized files (>50KB)
oversized = []
FOR each doc in filtered_docs:
    # Estimate size from line count
    content = Read(file_path=doc)
    IF len(content) > 50000:
        oversized.append(doc)

IF oversized:
    evidence_visual.append("Oversized files (>50KB): {oversized}")
ELSE:
    score_visual += 2
    evidence_visual.append("No oversized files")

# Check tables with >10 rows without grouping
score_visual += 2  # Default if no table issues

key_blocker_visual = evidence_visual[0] if score_visual < 5 else "None"
Display: "  Visual Design & Formatting: {score_visual}/10"
```
VERIFY: score_visual is 0-10. evidence_visual has at least 1 entry.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A04 --step=A04.3 --workflow=doc-audit`

---

### Step A04.4: Score Dimension 4 — Onboarding Friction

EXECUTE: Evaluate how easy it is for a new user to get started.
```
score_onboard = 0  # out of 10
evidence_onboard = []

IF "README.md" in loaded_entries:
    readme = loaded_entries["README.md"]

    # Check install steps in first 50 lines
    first_50 = first_n_lines(readme, 50)
    IF contains install/setup commands (npm install, pip install, cargo build, etc.):
        score_onboard += 3
        evidence_onboard.append("Install steps within first 50 lines")
    ELSE:
        evidence_onboard.append("No install steps in first 50 lines of README")

    # Check for Quick Start narrative
    IF "quick start" in readme.lower() OR "getting started" in readme.lower():
        score_onboard += 2
        evidence_onboard.append("Quick Start / Getting Started section present")
    ELSE:
        evidence_onboard.append("No Quick Start section")

    # Check prerequisites consistency
    prereqs_in_readme = extract_prerequisites(readme)
    IF prereqs_in_readme:
        score_onboard += 1
        evidence_onboard.append("Prerequisites listed in README")
    ELSE:
        evidence_onboard.append("No prerequisites section")

ELSE:
    evidence_onboard.append("No README.md -- onboarding impossible")

# Check LICENSE presence
IF community_checklist.get("LICENSE") or community_checklist.get("LICENSE-MIT"):
    score_onboard += 2
    evidence_onboard.append("LICENSE file present")
ELSE:
    evidence_onboard.append("No LICENSE file -- legal friction for contributors")

# Check MSRV/version consistency with manifest
IF manifest_data and manifest_data.get("engine_version"):
    IF discrepancies and any("version" in d for d in discrepancies):
        evidence_onboard.append("Version inconsistency between manifest and docs")
    ELSE:
        score_onboard += 2
        evidence_onboard.append("Version consistent between manifest and docs")
ELSE:
    score_onboard += 2  # No version to check

key_blocker_onboard = evidence_onboard[0] if score_onboard < 5 else "None"
Display: "  Onboarding Friction: {score_onboard}/10"
```
VERIFY: score_onboard is 0-10. evidence_onboard has at least 1 entry.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A04 --step=A04.4 --workflow=doc-audit`

---

### Step A04.5: Run Orphan Detection

EXECUTE: Identify documentation files with zero inbound references.
```
# Build reference graph
reference_graph = {}  # file -> [files that link to it]

FOR each doc in filtered_docs:
    content = Read(file_path=doc)
    links = extract_markdown_links(content)
    internal_links = filter(links, is_relative_path)

    FOR each link in internal_links:
        resolved = resolve_relative_path(doc, link)
        IF resolved in filtered_docs:
            reference_graph.setdefault(resolved, []).append(doc)

# Find orphans (files with no inbound references, excluding entry points)
entry_point_names = ["README.md", "docs/README.md", "docs/index.md", "CHANGELOG.md"]
orphaned_files = []

FOR each doc in filtered_docs:
    IF doc not in entry_point_names:
        IF doc not in reference_graph OR len(reference_graph[doc]) == 0:
            orphaned_files.append(doc)

Display: "Orphan detection: {len(orphaned_files)} orphaned files"
FOR each orphan in orphaned_files:
    Display: "  {orphan} (no inbound links)"
```
VERIFY: Orphan detection completed. orphaned_files list populated (may be empty).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A04 --step=A04.5 --workflow=doc-audit`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=A04 --checkpoint-passed --workflow=doc-audit
```

## Phase Transition Display

```
Display: "Phase A04 complete: Audit Analysis"
Display: "  Scores: Tone={score_tone}, IA={score_ia}, Visual={score_visual}, Onboard={score_onboard}"
Display: "  Orphans: {len(orphaned_files)}"
Display: "  Proceeding to Phase A05: Audit Prioritization"
```
