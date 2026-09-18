## Success Criteria

**Subagent output is successful when:**
- [ ] Returned markdown text (NOT files)
- [ ] All required sections present (User Story, AC, Edge Cases, NFRs)
- [ ] Minimum 3 acceptance criteria (Given/When/Then format)
- [ ] Minimum 2 edge cases
- [ ] All NFRs measurable (no vague terms like "fast", "secure")
- [ ] No file creation indicators in output
- [ ] Contract validation passes (checked by parent skill Step 2.2.5)
- [ ] Parent skill can assemble output into story-template.md without modification
- [ ] Content quality matches general-purpose requirements-analyst
- [ ] Token usage < 50K (isolated context)

---

## Testing

**Self-test before returning output:**

**Test 1: Content Return (Not Files)**
```python
# Check output type
assert isinstance(output, str), "Output should be string (markdown text)"
assert "## User Story" in output, "Missing User Story section"
assert "## Acceptance Criteria" in output, "Missing AC section"
assert ".md" not in output or "markdown" in output.lower(), "No file references"
assert "File created" not in output, "No file creation statements"
```

**Test 2: Required Sections**
```python
required = ["User Story", "Acceptance Criteria", "Edge Cases", "Non-Functional Requirements"]
for section in required:
    assert f"## {section}" in output, f"Missing section: {section}"
```

**Test 3: Measurable NFRs**
```python
nfr_section = extract_section(output, "Non-Functional Requirements")

vague_terms = ["fast", "secure", "scalable", "performant", "reliable"]
for term in vague_terms:
    if re.search(rf'\b{term}\b', nfr_section, re.IGNORECASE):
        WARNING: f"Vague NFR term: {term} - consider making measurable"
```

**Test 4: AC Format**
```python
ac_section = extract_section(output, "Acceptance Criteria")
ac_count = ac_section.count("### AC")

assert ac_count >= 3, f"Only {ac_count} AC (need minimum 3)"
assert "Given" in ac_section, "AC missing Given clauses"
assert "When" in ac_section, "AC missing When clauses"
assert "Then" in ac_section, "AC missing Then clauses"
```

---

## Success Declaration

**This subagent is successful when:**
- [ ] Invoked by spec-driven-stories Phase 2
- [ ] Returns markdown content (text string)
- [ ] All required sections present (User Story, AC, Edge Cases, NFRs)
- [ ] Minimum 3 AC (Given/When/Then format)
- [ ] Minimum 2 edge cases
- [ ] All NFRs measurable
- [ ] No file creation (guaranteed by tool restrictions)
- [ ] Contract validation passes (Step 2.2.5)
- [ ] File system diff passes (Step 2.2.7 - no files created)
- [ ] Content quality matches general-purpose requirements-analyst
- [ ] Parent skill assembles output into .story.md successfully
- [ ] Zero extra files in production (100% compliance)
