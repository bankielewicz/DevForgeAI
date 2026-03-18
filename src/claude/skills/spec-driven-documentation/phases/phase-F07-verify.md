# Phase F07: Verify Fixes

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=F06 --to=F07 --workflow=doc-fix
# Exit 0: proceed | Exit 1: Phase F06 incomplete
```

## Contract

PURPOSE: After all fixes applied, re-run orphan detection, check link integrity, verify fact consistency, and re-inventory community files.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Verification results (orphans, links, facts, community status)
STEP COUNT: 4 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-workflow.md")
```

IF Read fails: HALT -- "Phase F07 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step F07.1: Re-Run Orphan Detection

EXECUTE: Check that no new orphans were created by the fixes.
```
# Re-inventory all docs files
docs_files = Glob(pattern="docs/**/*.md")
root_md = Glob(pattern="*.md")
all_docs = docs_files + root_md
# Apply same exclusion filters as A03

# Re-build reference graph
reference_graph = {}
FOR each doc in all_docs:
    content = Read(file_path=doc)
    links = extract_markdown_links(content)
    internal_links = filter(links, is_relative_path)

    FOR each link in internal_links:
        resolved = resolve_relative_path(doc, link)
        IF resolved in all_docs:
            reference_graph.setdefault(resolved, []).append(doc)

# Find orphans
entry_points = ["README.md", "docs/README.md", "docs/index.md", "CHANGELOG.md"]
new_orphans = []
FOR each doc in all_docs:
    IF doc not in entry_points:
        IF doc not in reference_graph OR len(reference_graph[doc]) == 0:
            new_orphans.append(doc)

IF new_orphans:
    Display: "  Orphan check: {len(new_orphans)} orphaned files remain"
    FOR each orphan in new_orphans:
        Display: "    {orphan}"
ELSE:
    Display: "  Orphan check: No orphaned files"
```
VERIFY: Orphan detection completed. new_orphans list populated.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.1 --workflow=doc-fix`

---

### Step F07.2: Check Link Integrity

EXECUTE: Verify all internal links in documentation resolve to existing files.
```
broken_links = []

FOR each doc in all_docs:
    content = Read(file_path=doc)
    links = extract_markdown_links(content)
    internal_links = filter(links, is_relative_path)

    FOR each link in internal_links:
        resolved = resolve_relative_path(doc, link)
        IF not file_exists(resolved):
            broken_links.append({
                "source": doc,
                "link": link,
                "resolved": resolved
            })

IF broken_links:
    Display: "  Link integrity: {len(broken_links)} broken links"
    FOR each bl in broken_links:
        Display: "    {bl['source']} -> {bl['link']} (not found)"
ELSE:
    Display: "  Link integrity: All links valid"
```
VERIFY: Link check completed. broken_links list populated.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.2 --workflow=doc-fix`

---

### Step F07.3: Check Fact Consistency

EXECUTE: Re-verify that manifest data matches documentation claims.
```
IF manifest_path:
    manifest_content = Read(file_path=manifest_path)
    manifest_data = parse_manifest(manifest_content)

    remaining_discrepancies = []

    IF "README.md" in [basename(d) for d in all_docs]:
        readme = Read(file_path="README.md")

        # Re-check version, license, engine version
        IF manifest_data.get("version") and manifest_data["version"] not in readme:
            remaining_discrepancies.append("Version mismatch persists")

        IF manifest_data.get("license") and manifest_data["license"] not in readme:
            remaining_discrepancies.append("License mismatch persists")

    IF remaining_discrepancies:
        Display: "  Fact consistency: {len(remaining_discrepancies)} issues remain"
        FOR each d in remaining_discrepancies:
            Display: "    {d}"
    ELSE:
        Display: "  Fact consistency: All facts consistent"

ELSE:
    Display: "  Fact consistency: No manifest to check against"
```
VERIFY: Fact check completed. remaining_discrepancies list populated.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.3 --workflow=doc-fix`

---

### Step F07.4: Re-Inventory Community Files

EXECUTE: Re-check community file presence after fixes.
```
updated_checklist = {}
FOR each file in community_checklist.keys():
    result = Glob(pattern=file)
    updated_checklist[file] = bool(result)

new_present = sum(1 for v in updated_checklist.values() if v)
old_present = sum(1 for v in community_checklist.values() if v)
improvement = new_present - old_present

Display: "  Community files: {new_present}/{len(updated_checklist)} present"
IF improvement > 0:
    Display: "    +{improvement} new community files added"

# Display remaining gaps
missing = [f for f, v in updated_checklist.items() if not v]
IF missing:
    Display: "    Still missing: {', '.join(missing)}"

Display: ""
Display: "Verification summary:"
Display: "  Orphans: {'None' if not new_orphans else len(new_orphans)}"
Display: "  Broken links: {'None' if not broken_links else len(broken_links)}"
Display: "  Fact issues: {'None' if not remaining_discrepancies else len(remaining_discrepancies)}"
Display: "  Community: {new_present}/{len(updated_checklist)}"
```
VERIFY: Community re-inventory completed. Improvement tracked.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.4 --workflow=doc-fix`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=F07 --checkpoint-passed --workflow=doc-fix
```

## Phase Transition Display

```
Display: "Phase F07 complete: Verify Fixes"
Display: "  Proceeding to Phase F08: Fix Report"
```
