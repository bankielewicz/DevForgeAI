## Error Handling

### Error 1: Insufficient Information

**Detection:** Feature description too short (< 10 words)

**Response:**
```
ERROR: Insufficient Information

Feature description is too short (< 10 words).
Please provide more detail about:
- Who is the user/persona?
- What functionality is needed?
- Why is this valuable (business benefit)?

Minimum: 10 words describing who/what/why

Current description: {feature_description}
```

**Action:** Return error message to parent skill, parent skill will ask user for clarification

---

### Error 2: Ambiguous Requirements

**Detection:** Feature description unclear about user persona, specific actions, or acceptance criteria

**Response:**
```
CLARIFICATION NEEDED

Feature description is ambiguous:
- User persona unclear (who is this for?)
- Action ambiguous (what exactly should happen?)
- Success criteria undefined (how do we know it works?)

Please clarify:
1. Who is the primary user (DBA, developer, customer, admin)?
2. What specific functionality is needed?
3. What are the key acceptance criteria?

Current description: {feature_description}
```

**Action:** Return clarification request to parent skill

---

### Error 3: Contract Violation Risk

**Detection:** About to generate output that would violate contract

**Response:**
```python
# HALT before violating contract

if about_to_create_file:
    HALT: "Contract violation prevented (attempted file creation)"
    Log: "story-requirements-analyst attempted file creation - blocked by self-check"
    return "ERROR: Internal constraint violation prevented. Cannot create files (tool not available)."

if output_missing_required_sections:
    WARNING: "Output incomplete - missing required sections"
    # Attempt to fill gaps or return partial with warning
```

