# Phase 03: Answer Synthesis

## Entry Gate

```bash
devforgeai-validate phase-check ${SESSION_ID} --workflow=cc-guide --from=02 --to=03 --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Transition allowed | Proceed to Phase 03 |
| 1 | Previous phase incomplete | HALT - complete Phase 02 first |
| 127 | CLI not installed | Continue without enforcement |

---

## Contract

- **PURPOSE:** Synthesize a comprehensive, accurate answer from the reference content loaded in Phase 02. The answer must cite specific sections from loaded reference files — not general knowledge.
- **REQUIRED SUBAGENTS:** None (inline synthesis — content is already in context from Phase 02)
- **REQUIRED ARTIFACTS:** Delivered answer with reference citations
- **STEP COUNT:** 3 mandatory steps
- **REFERENCE FILES:** None (uses content loaded in Phase 02)

---

## Mandatory Steps (3)

### Step 3.1: Synthesize Answer from Loaded Reference Content

**EXECUTE:**
Using the reference content loaded in Phase 02, construct a comprehensive answer to $QUESTION. The answer must meet these requirements:

1. **Source grounding:** Answer MUST reference specific content from the loaded reference files. Do not answer from general knowledge or SKILL.md summaries — the whole point of Phase 02 was to load the authoritative content.

2. **Code examples:** Include code snippets, configuration examples, or command syntax where applicable. Use actual examples from the reference files.

3. **Step-by-step guidance:** For "how to" questions, provide numbered steps the user can follow.

4. **Keyboard shortcuts:** If the question relates to a feature with keyboard shortcuts, include the relevant shortcut(s) from the Keyboard Shortcuts table.

5. **Cross-references:** If the answer touches on related features, mention them briefly with pointers to the relevant reference file section.

6. **Section citation:** Note which section of which reference file contains the detailed information (e.g., "See references/core-features.md, Section 1: Subagents for full configuration options").

**VERIFY:**
- Answer is non-empty
- Answer cites at least one specific section from a loaded reference file
- Answer directly addresses $QUESTION
- Code examples are syntactically correct

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=03 --step=3.1 --project-root=.
```

---

### Step 3.2: Add Quick Reference Addendum (if applicable)

**EXECUTE:**
If the question relates to common tasks or frequently used features, append a brief "Quick Reference" section with the most relevant commands, shortcuts, or configuration snippets.

```
IF $INTENT in ["how_to", "configuration", "creation"]:
    Include a brief summary of the most relevant commands/shortcuts
    Format as a compact table or bullet list

IF $INTENT == "comparison":
    Include relevant rows from the comparison matrix if loaded

IF $INTENT == "troubleshooting":
    Include relevant diagnostic commands (e.g., /doctor, /debug)

ELSE:
    Mark as "not-applicable" — addendum not needed for this question type
```

**VERIFY:**
Addendum present and relevant to the question, OR step explicitly marked as not-applicable with reason noted.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=03 --step=3.2 --project-root=.
```

---

### Step 3.3: Deliver Answer to User

**EXECUTE:**
Display the synthesized answer to the user. The answer should be well-formatted with:
- Clear headings for multi-part answers
- Code blocks with appropriate language tags
- Tables for comparative information
- Bold for emphasis on key points

**VERIFY:**
Answer displayed in conversation. User can see and read the response.

**RECORD:**
```bash
devforgeai-validate phase-record ${SESSION_ID} --workflow=cc-guide --phase=03 --step=3.3 --project-root=.
```

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${SESSION_ID} --workflow=cc-guide --phase=03 --checkpoint-passed --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Phase 03 complete | Proceed to Phase 04 |
| 1 | Steps incomplete | HALT - check step records |
| 127 | CLI not installed | Continue to Phase 04 |

**Phase 03 Summary:**
- Answer delivered: {yes/no}
- Reference sections cited: {list}
- Quick reference addendum: {included/not-applicable}
