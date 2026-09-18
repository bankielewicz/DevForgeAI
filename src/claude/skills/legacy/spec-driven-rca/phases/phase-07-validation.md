# Phase 07: Validation & Self-Check (Strategic Mode Only)

**Purpose:** Verify RCA document completeness, quality, and self-containedness.
**Applies to:** Strategic mode only.

---

## Reference Loading [MANDATORY]

```
# No required references for this phase. Phase 07 validates the RCA document
# just written in Phase 06 — its Reads target the workflow's own output
# (devforgeai/RCA/RCA-NNN-*.md, a write-then-read-back verification) plus
# dynamic recommendation file paths. The pre-rca-document-write.sh and
# pre-rca-recommendation-write.sh hooks (ADR-074) enforce structural
# validation at Write time; this phase performs post-write self-checks only.
```

---

## Step 07.1: Read the RCA Document [MANDATORY]

### EXECUTE

```
Read(file_path="devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md")
```

Load the entire document for validation.

### VERIFY

- Document loaded successfully
- Content is non-empty

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.1
```

---

## Step 07.2: Validate Structure [MANDATORY]

### EXECUTE

Check all 8 required sections exist:

```
- [ ] Header (with all metadata: number, title, date, reporter, component, severity)
- [ ] Issue Description
- [ ] 5 Whys Analysis
- [ ] Evidence Collected
- [ ] Codebase Context Snapshot (if recommendations touch code)
- [ ] Recommendations (by priority)
- [ ] Implementation Checklist
- [ ] Prevention Strategy
- [ ] Related RCAs

IF any section missing:
    CRITICAL ERROR: "Section '{name}' missing from RCA document"
    Self-heal: Add missing section with content from phase data
```

### VERIFY

- All required sections present
- No sections are empty placeholders

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.2
```

---

## Step 07.3: Validate 5 Whys [MANDATORY]

### EXECUTE

```
Check:
- [ ] All 5 Whys answered (not empty)
- [ ] Each "why" has evidence reference (file:line)
- [ ] Why #5 marked as ROOT CAUSE
- [ ] Root cause is specific (not vague like "process wasn't followed")
- [ ] Each why builds logically on the previous answer

IF any check fails:
    WARNING: "5 Whys validation issue: {issue}"
    Self-heal: Add missing evidence references or clarify root cause
```

### VERIFY

- All 5 validation items pass
- Root cause is specific and actionable

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.3
```

---

## Step 07.4: Validate Evidence [MANDATORY]

### EXECUTE

```
Check:
- [ ] At least 3 files examined
- [ ] Each file has excerpts with line numbers
- [ ] Significance explained for each file
- [ ] "Supports Why #" linkage present for CRITICAL/HIGH files
- [ ] Context files validated (if relevant to issue)

IF < 3 files:
    WARNING: "Evidence insufficient: Only {count} files examined"
    Self-heal: Identify additional relevant files to examine
```

### VERIFY

- At least 3 files in evidence section
- Each has excerpts with line numbers

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.4
```

---

## Step 07.5: Validate Recommendations [MANDATORY]

### EXECUTE

**Hook-enforced (ADR-074).** Per-REC field validation is performed at the tool layer by two cooperating hooks:

| Hook | Coverage |
|---|---|
| `pre-rca-recommendation-write.sh` | Required/Rendered tier fields per REC-N block (see Step 05.9 table) — fires on every Write/Edit |
| `pre-rca-document-write.sh` | Whole-document structure: 8 mandatory sections, 5 numbered Why entries, ≥1 REC-N block present, Recommendations + Validation sections — fires on Write to `devforgeai/RCA/RCA-NNN-*.md` |

The composer does not need to perform per-REC validation manually here — the document Write in Step 06.10 is blocked (exit 2) if either hook detects a violation, and the block message enumerates the missing fields. If the document needs self-healing (e.g., a REC was written incrementally and missed a field), the composer re-renders the REC-N block from Phase 05 data and retries.

### VERIFY

- The RCA document Write in Step 06.10 succeeded (no hook block events in the session log)
- `Read(file_path="devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md")` returns content; each REC-N block matches the recommendation-contract Required/Rendered tier shape

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.5
```

---

## Step 07.6: Validate Placeholders [MANDATORY]

### EXECUTE

```
Grep(pattern="\\{[A-Z_]+\\}", path="devforgeai/RCA/RCA-{RCA_NUMBER}-{slug}.md", output_mode="content")

IF placeholders found:
    CRITICAL ERROR: "Placeholders not replaced: {list}"
    Self-heal: Replace with actual values from phase data
    Write updated document
```

### VERIFY

- Zero placeholder patterns remain in document
- All `{PLACEHOLDER}` strings replaced

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.6
```

---

## Step 07.7: Validate File Paths [MANDATORY]

### EXECUTE

```
FOR each file path referenced in recommendations:
    Extract path from document text

    Read(file_path="{path}")

    IF Read succeeds:
        VALID
    ELSE:
        WARNING: "File path may be incorrect: {path}"
        Note in document: "Verify path before implementing"
```

### VERIFY

- File path validation attempted for all referenced paths
- Invalid paths noted with warnings

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.7
```

---

## Step 07.8: Self-Containedness Check [MANDATORY]

### EXECUTE

This is the critical quality gate. The RCA document must be usable by a fresh Claude session without reading source files.

**Document-level checks:**
```
- [ ] Codebase Context Snapshot present and non-empty (if recs touch code files)
- [ ] At least one type definition or function signature quoted (if recs touch .rs files)
- [ ] Applicable Architecture Constraints section present (if recs touch .rs files)
- [ ] 5 Whys each have inline **Evidence:** citation with file:line
```

**Per-recommendation checks:**
```
FOR each REC-N:
    - [ ] Has "**Addresses:** Why #{N}" on first content line
    - [ ] Has "#### Current Code Context" with 5-30 line excerpt (or N/A)
    - [ ] Has "#### Test Specification" with markdown table
    - [ ] Has "**Time:** {N} hours" (parseable by /create-stories-from-rca)
    - [ ] Has "#### Success Criteria" with checkboxes
```

**Fresh Session Test (mental model):**

Imagine a fresh Claude session opens ONLY this RCA document. Can it:
1. Understand the root cause without Read()ing any source files?
2. Implement every REC-N without Read()ing any source files?
3. Create accurate stories via `/create-stories-from-rca`?
4. Know exact file paths, function signatures, and constraints?

IF any answer is NO:
```
HALT: "Self-containedness check failed: {which question}"
Identify: What's missing that would make the answer YES
Self-heal: Add the missing context from phase data
Re-validate after self-heal
```

### VERIFY

- All document-level checks pass
- All per-recommendation checks pass
- Fresh session test passes (all 4 questions YES)

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.8
```

---

## Step 07.9: Quality Standards Check [MANDATORY]

### EXECUTE

```
From rca-writing-guide.md "Document Quality Checklist":

Verify:
- [ ] Title 3-6 words
- [ ] No aspirational content ("we should strive to...")
- [ ] No vague recommendations ("improve the process")
- [ ] All evidence-based (no speculation presented as fact)
- [ ] Copy-paste ready code in all code-change recommendations

IF violations found:
    Self-heal: Fix violations (shorten title, make specific, etc.)
    Write updated document
```

### VERIFY

- All quality standards met
- Document is professional and actionable

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.9
```

---

## Step 07.10: Phase 07 Summary [MANDATORY]

### EXECUTE

```
PHASE 07 COMPLETE (VALIDATION)
================================
Structure: PASS ({N}/8 sections)
5 Whys: PASS (all answered with evidence)
Evidence: PASS ({count} files, {count} excerpts)
Recommendations: PASS ({count} complete)
Placeholders: PASS (all replaced)
File Paths: {valid_count}/{total_count} valid
Self-Containedness: PASS
Quality: PASS

{If warnings}: Warnings: {count}
  - {Warning 1}
  - {Warning 2}

Proceeding to Phase 08: Completion & Pipeline...
```

### VERIFY

- Summary displayed with all validation results

### RECORD

```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=${WORKFLOW} --phase=07 --step=07.10
```
