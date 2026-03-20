# Phase 04: Self-Update Check

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=cc-guide --from=03 --to=04 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 04 |
| 1 | Previous phase incomplete | HALT - complete Phase 03 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Check if the reference content used to answer the question may be outdated. If staleness is detected, offer to fetch the latest documentation from official sources.
- **REQUIRED SUBAGENTS:** None
- **REQUIRED ARTIFACTS:** Staleness assessment, optional update
- **STEP COUNT:** 3 mandatory steps
- **REFERENCE FILES:** documentation-urls.md

---

## Reference Loading [MANDATORY]

```
Read(file_path=".claude/skills/spec-driven-cc-guide/references/documentation-urls.md")
```

IF Read fails: Log warning, skip update check (non-blocking — the answer has already been delivered in Phase 03).

---

## Mandatory Steps (3)

### Step 4.1: Load Documentation URLs

**EXECUTE:**
```
Read(file_path=".claude/skills/spec-driven-cc-guide/references/documentation-urls.md")
```

**VERIFY:**
URLs loaded into context. At least one documentation URL is visible.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=04 --step=4.1 --project-root=.
```

---

### Step 4.2: Evaluate Staleness Signals

**EXECUTE:**
Check the conversation context for any of these staleness indicators:

1. **User contradiction:** User says "that's not how it works anymore", "this doesn't work", "that's outdated", "they changed this", or similar corrections
2. **Missing feature:** User asks about a feature that had zero matches in the reference content loaded in Phase 02
3. **Version mismatch:** User mentions a Claude Code version newer than the skill's compatibility field (currently v2.1.x)
4. **Zero routing matches:** $QUESTION had zero keyword matches in the domain routing table (from Phase 01 fallback)
5. **User request:** User explicitly asks to check for updates or latest documentation

```
$STALENESS_DETECTED = false

IF any staleness signal found:
    $STALENESS_DETECTED = true
    $STALENESS_REASON = description of which signal triggered
```

**VERIFY:**
$STALENESS_DETECTED is a boolean value. If true, $STALENESS_REASON is a non-empty string.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=04 --step=4.2 --project-root=.
```

---

### Step 4.3: Offer Update (if stale)

**EXECUTE:**

```
IF $STALENESS_DETECTED == true:
    1. Identify the most relevant official documentation URL from documentation-urls.md
       based on $QUESTION and $DOMAINS

    2. Inform the user:
       "The reference content for this topic may be outdated ({$STALENESS_REASON}).
        I can check the latest documentation at {URL}. Would you like me to update?"

    3. IF user approves:
       - WebFetch(url={official_documentation_url})
       - Compare fetched content with current reference file
       - If differences found, update the reference file with new content
       - Display: "Updated {reference_file} with latest content from {URL}"

    4. IF user declines:
       - Display: "Keeping current reference content. You can request an update anytime."

IF $STALENESS_DETECTED == false:
    Display nothing — the content appears current. This is the ONLY step in the entire
    skill where a skip is explicitly allowed, and only when staleness is genuinely
    not detected.
```

**VERIFY:**
- If stale: Update was offered (user accepted or declined)
- If not stale: Step completed with no-staleness confirmation

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=04 --step=4.3 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=cc-guide --phase=04 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 04 complete | Workflow complete |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Workflow complete |

**Phase 04 Summary:**
- Staleness detected: {$STALENESS_DETECTED}
- Staleness reason: {$STALENESS_REASON or "N/A"}
- Update performed: {yes/no/not-applicable}

---

## Workflow Complete

All 4 phases executed. Knowledge retrieval workflow is complete.
