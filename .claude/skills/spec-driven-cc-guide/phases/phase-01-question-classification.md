# Phase 01: Question Classification

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=cc-guide --from=00 --to=01 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 01 |
| 1 | Previous phase incomplete | HALT - complete Phase 00 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Parse the user's question about Claude Code and classify it into knowledge domain(s) to determine which reference files must be loaded in Phase 02.
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** $QUESTION, $DOMAINS[], $REFERENCE_FILES[]
- **STEP COUNT:** 3 mandatory steps
- **REFERENCE FILES:** domain-routing-table.md

---

## Reference Loading [MANDATORY]

Load the domain routing table fresh. Do NOT rely on the summary in SKILL.md.

```
Read(file_path=".claude/skills/spec-driven-cc-guide/references/domain-routing-table.md")
```

IF Read fails: HALT — "Domain routing table not found. Cannot classify question without routing rules."

---

## Mandatory Steps (3)

### Step 1.1: Load Domain Routing Table

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-cc-guide/references/domain-routing-table.md")
```

**VERIFY:**
File content is loaded into context. Domain definitions and keyword patterns are visible. Content is non-empty.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=01 --step=1.1 --project-root=.
```

---

### Step 1.2: Extract Question from Conversation Context

**EXECUTE:**
Scan the conversation context to identify the user's question about Claude Code Terminal. Extract the core question, intent, and any specific feature/topic mentioned.

```
$QUESTION = The user's question or request about Claude Code
$INTENT = One of: "feature_discovery", "how_to", "troubleshooting", "configuration", "creation", "comparison", "prompt_engineering", "skills_spec"
```

**VERIFY:**
$QUESTION is a non-empty string that represents a question about Claude Code Terminal (not a coding task).

IF $QUESTION is empty or not about Claude Code: Display the answer using general knowledge. Do NOT proceed through remaining phases — this skill only adds value for Claude Code-specific questions.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=01 --step=1.2 --project-root=.
```

---

### Step 1.3: Classify Question into Domain(s)

**EXECUTE:**
Match $QUESTION keywords and intent against the domain routing table patterns loaded in Step 1.1. Build two arrays:

```
$DOMAINS = []      # Knowledge domains that match (1-3 domains)
$REFERENCE_FILES = [] # Reference file paths to load in Phase 02

FOR each domain in routing_table:
    IF $QUESTION contains any keyword from domain.keywords:
        $DOMAINS.append(domain.name)
        $REFERENCE_FILES.append(domain.primary_reference)

IF $DOMAINS is empty:
    # Fallback: default to "components" domain
    $DOMAINS = ["components"]
    $REFERENCE_FILES = ["references/core-features.md"]
```

**VERIFY:**
- $DOMAINS.length >= 1 (at least one domain matched or fallback applied)
- $REFERENCE_FILES.length >= 1 (at least one reference file identified)
- No duplicate entries in $REFERENCE_FILES

Display classification result:
```
Question: {$QUESTION}
Classified domains: {$DOMAINS}
Reference files to load: {$REFERENCE_FILES}
```

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=01 --step=1.3 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=cc-guide --phase=01 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 01 complete | Proceed to Phase 02 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 02 |

**Phase 01 Summary:**
- $QUESTION: {value}
- $INTENT: {value}
- $DOMAINS: {value}
- $REFERENCE_FILES: {value}
