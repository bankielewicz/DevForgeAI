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

## Mandatory Steps (Delegated Execution)

EXECUTE: Delegate the 4 read-only verification scans to documentation-writer (its tool surface — Read, Write, Edit, Grep, Glob — covers all 4 steps; this invocation is read-only verification mode, no writes).

```
mkdir -p tmp/${SESSION_ID}
: > tmp/${SESSION_ID}/doc-f07-documentation-writer-handoff-changed-files.txt

HANDOFF_OUTPUT_DOCUMENTATION_WRITER=$(devforgeai-validate build-subagent-handoff ${SESSION_ID} \
  --workflow=spec-driven-documentation \
  --phase=F07 \
  --subagent=documentation-writer \
  --changed-files-file=tmp/${SESSION_ID}/doc-f07-documentation-writer-handoff-changed-files.txt \
  --project-root=. 2>&1)
HANDOFF_PATH_DOCUMENTATION_WRITER=$(echo "$HANDOFF_OUTPUT_DOCUMENTATION_WRITER" | jq -r '.handoff_md_path')

VERIFY: HANDOFF_PATH_DOCUMENTATION_WRITER exists, is non-empty, and its manifest has context_pack.coverage_matrix == {} and unresolved == [].

verification = Task(subagent_type="documentation-writer", prompt="""Handoff: ${HANDOFF_PATH_DOCUMENTATION_WRITER}
Read the handoff first. Use its context_pack.coverage_matrix and role-domain rules as the context source. If a required domain or artifact is absent, return H-CONTEXT-MISS and stop.

Perform read-only post-fix verification for spec-driven-documentation Fix workflow.

Return JSON with these 4 keys:

1. new_orphans: list[str]
   - Re-inventory all docs (docs/**/*.md + *.md at root, exclusion filters per A03)
   - Build reference graph by parsing internal markdown links and resolving relative paths
   - Entry points: README.md, docs/README.md, docs/index.md, CHANGELOG.md
   - Orphan = file not in entry_points AND no incoming references in graph

2. broken_links: list[{source, link, resolved}]
   - For each doc, extract internal markdown links via Grep + parse
   - For each internal link, resolve relative path and check file_exists
   - Report unresolvable links

3. remaining_discrepancies: list[str]
   - IF manifest_path provided: Read manifest_data (version, license, engine)
   - Read README.md and check whether manifest values appear textually
   - Report each mismatch as a one-sentence string
   - IF no manifest_path: return empty list

4. updated_checklist: dict[str, bool]
   - Re-check community file presence via Glob:
     CONTRIBUTING.md, LICENSE, CODE_OF_CONDUCT.md, SECURITY.md, .github/ISSUE_TEMPLATE/
   - Map each filename to bool

Reference: .claude/skills/spec-driven-documentation/references/audit-workflow.md (canonical method spec).
This invocation is READ-ONLY — do not write, edit, or modify any files. Return only the JSON object.
Include a subagent-result-v1 coverage_attestation with context_pack_path='${HANDOFF_PATH_DOCUMENTATION_WRITER}', context_pack_consumed=true, and context_miss=[].

Manifest path (if available): ${MANIFEST_PATH}
Community checklist seed: ${COMMUNITY_CHECKLIST}
""")
state = parse_json(verification)
```

VERIFY (precondition for all 4 steps): state contains keys new_orphans, broken_links, remaining_discrepancies, updated_checklist. If any key is missing, HALT and re-invoke or escalate to F06 re-run.

---

### Step F07.1: Re-Run Orphan Detection

EXECUTE: Surface delegated orphan-detection results.
```
new_orphans = state["new_orphans"]
IF new_orphans:
    Display: "  Orphan check: {len(new_orphans)} orphaned files remain"
    FOR each orphan in new_orphans:
        Display: "    {orphan}"
ELSE:
    Display: "  Orphan check: No orphaned files"
```
VERIFY: state["new_orphans"] is a list (possibly empty).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.1 --workflow=doc-fix`

---

### Step F07.2: Check Link Integrity

EXECUTE: Surface delegated link-integrity results.
```
broken_links = state["broken_links"]
IF broken_links:
    Display: "  Link integrity: {len(broken_links)} broken links"
    FOR each bl in broken_links:
        Display: "    {bl['source']} -> {bl['link']} (not found)"
ELSE:
    Display: "  Link integrity: All links valid"
```
VERIFY: state["broken_links"] is a list (possibly empty).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.2 --workflow=doc-fix`

---

### Step F07.3: Check Fact Consistency

EXECUTE: Surface delegated fact-consistency results.
```
remaining_discrepancies = state["remaining_discrepancies"]
IF remaining_discrepancies:
    Display: "  Fact consistency: {len(remaining_discrepancies)} issues remain"
    FOR each d in remaining_discrepancies:
        Display: "    {d}"
ELIF not manifest_path:
    Display: "  Fact consistency: No manifest to check against"
ELSE:
    Display: "  Fact consistency: All facts consistent"
```
VERIFY: state["remaining_discrepancies"] is a list (possibly empty).
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=F07 --step=F07.3 --workflow=doc-fix`

---

### Step F07.4: Re-Inventory Community Files

EXECUTE: Surface delegated community-file inventory + emit verification summary.
```
updated_checklist = state["updated_checklist"]
new_present = sum(1 for v in updated_checklist.values() if v)
old_present = sum(1 for v in community_checklist.values() if v)
improvement = new_present - old_present

Display: "  Community files: {new_present}/{len(updated_checklist)} present"
IF improvement > 0:
    Display: "    +{improvement} new community files added"

missing = [f for f, v in updated_checklist.items() if not v]
IF missing:
    Display: "    Still missing: {', '.join(missing)}"

Display: ""
Display: "Verification summary:"
Display: "  Orphans: {'None' if not state['new_orphans'] else len(state['new_orphans'])}"
Display: "  Broken links: {'None' if not state['broken_links'] else len(state['broken_links'])}"
Display: "  Fact issues: {'None' if not state['remaining_discrepancies'] else len(state['remaining_discrepancies'])}"
Display: "  Community: {new_present}/{len(updated_checklist)}"
```
VERIFY: state["updated_checklist"] is a dict (possibly empty).
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
