# Phase A05: Audit Prioritization

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --from=A04 --to=A05 --workflow=doc-audit
# Exit 0: proceed | Exit 1: Phase A04 incomplete
```

## Contract

PURPOSE: Classify each finding by severity, assign sequential IDs, map fix modes from the fix catalog.
REQUIRED SUBAGENTS: (none)
REQUIRED ARTIFACTS: Prioritized findings array with IDs, severities, fix modes
STEP COUNT: 2 mandatory steps

---

## Reference Loading [MANDATORY]

```
Read(file_path="references/audit-fix-catalog.md")
```

IF Read fails: HALT -- "Phase A05 reference file not loaded. Cannot proceed."

---

## Mandatory Steps

### Step A05.1: Compile Findings from Analysis

EXECUTE: Convert all evidence items and issues into structured findings.
```
findings = []
finding_id = 1

# From Tone dimension
FOR each negative evidence in evidence_tone:
    findings.append({
        "id": "F-{finding_id:03d}",
        "severity": classify_severity(evidence),  # CRITICAL/HIGH/MEDIUM/LOW
        "type": "tone:{specific_type}",  # e.g., "tone:no_why", "tone:no_pronouns"
        "affected": [relevant_file],
        "summary": evidence,
        "evidence": detailed_description,
        "remediation": suggested_fix,
        "fix_mode": lookup_fix_mode(type, audit_fix_catalog),  # "automated" or "interactive"
        "fix_action": lookup_fix_action(type, audit_fix_catalog)
    })
    finding_id += 1

# From IA dimension
FOR each negative evidence in evidence_ia:
    findings.append({...similar structure...})
    finding_id += 1

# From Visual dimension
FOR each negative evidence in evidence_visual:
    findings.append({...similar structure...})
    finding_id += 1

# From Onboarding dimension
FOR each negative evidence in evidence_onboard:
    findings.append({...similar structure...})
    finding_id += 1

# From orphan detection
FOR each orphan in orphaned_files:
    findings.append({
        "id": "F-{finding_id:03d}",
        "severity": "LOW",
        "type": "architecture:orphan",
        "affected": [orphan],
        "summary": "Orphaned file with no inbound references",
        "evidence": "No other documentation file links to {orphan}",
        "remediation": "Add cross-reference from related docs or remove if obsolete",
        "fix_mode": "interactive",
        "fix_action": "add_cross_reference"
    })
    finding_id += 1

# From configuration discrepancies
FOR each discrepancy in discrepancies:
    findings.append({
        "id": "F-{finding_id:03d}",
        "severity": "MEDIUM",
        "type": "onboarding:config_mismatch",
        "affected": ["README.md", manifest_path],
        "summary": discrepancy,
        "evidence": discrepancy,
        "remediation": "Update documentation to match project manifest",
        "fix_mode": "automated",
        "fix_action": "sync_config"
    })
    finding_id += 1

Display: "Compiled {len(findings)} findings"
```
VERIFY: findings array populated. Each finding has id, severity, type, affected, summary, fix_mode.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A05 --step=A05.1 --workflow=doc-audit`

---

### Step A05.2: Sort and Classify

EXECUTE: Sort findings by severity and display summary counts.
```
# Severity ordering: CRITICAL > HIGH > MEDIUM > LOW
severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
findings.sort(key=lambda f: severity_order[f["severity"]])

# Count by severity
counts = {
    "CRITICAL": len([f for f in findings if f["severity"] == "CRITICAL"]),
    "HIGH": len([f for f in findings if f["severity"] == "HIGH"]),
    "MEDIUM": len([f for f in findings if f["severity"] == "MEDIUM"]),
    "LOW": len([f for f in findings if f["severity"] == "LOW"])
}

# Count by fix mode
automated_count = len([f for f in findings if f["fix_mode"] == "automated"])
interactive_count = len([f for f in findings if f["fix_mode"] == "interactive"])

Display: ""
Display: "Findings by severity:"
Display: "  CRITICAL: {counts['CRITICAL']}"
Display: "  HIGH:     {counts['HIGH']}"
Display: "  MEDIUM:   {counts['MEDIUM']}"
Display: "  LOW:      {counts['LOW']}"
Display: ""
Display: "Fix modes: {automated_count} automated, {interactive_count} interactive"
```
VERIFY: Findings sorted by severity. Counts match total findings length.
RECORD: `devforgeai-validate phase-record ${SESSION_ID} --phase=A05 --step=A05.2 --workflow=doc-audit`

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --phase=A05 --checkpoint-passed --workflow=doc-audit
```

## Phase Transition Display

```
Display: "Phase A05 complete: Audit Prioritization"
Display: "  Total findings: {len(findings)}"
Display: "  Proceeding to Phase A06: Audit Output"
```
