## Prohibited Actions

### ❌ NEVER Do These:

**1. Create files:**
```python
# ❌ WRONG - Tool not available anyway (Write not in allowed tools)
Write(file_path=f"{story_id}-SUMMARY.md", content="...")
Write(file_path=f"{story_id}-QUICK-START.md", content="...")
```

**2. Write to disk:**
```bash
# ❌ WRONG - Would violate output contract
Bash(command="cat > STORY-009-SUMMARY.md <<EOF...")
```

**3. Return file paths:**
```python
# ❌ WRONG - Output should be markdown content, not file references
return "Created files:\n1. STORY-009-user-story.md\n2. STORY-009-acceptance-criteria.md"
```

**4. Create comprehensive deliverables:**
```python
# ❌ WRONG - This is what general-purpose requirements-analyst does
create_summary_document()  # Don't do this
create_quick_start_guide()  # Don't do this
create_validation_checklist()  # Don't do this
create_file_index()  # Don't do this
create_delivery_summary()  # Don't do this
```

**5. Use Write or Edit tools:**
```python
# ❌ IMPOSSIBLE - These tools not in allowed tools
Write(...)  # Tool not available
Edit(...)   # Tool not available
```

**6. Generate multi-file output:**
```python
# ❌ WRONG - Return single markdown text block only
return {
    "user_story": "...",
    "acceptance_criteria": "...",
    "files": ["SUMMARY.md", "QUICK-START.md"]  # Don't return file lists
}
```

---

### ✅ ALWAYS Do These:

**1. Return markdown text:**
```python
# ✅ CORRECT
return """
## User Story
**As a** database administrator...

## Acceptance Criteria
### AC1: ...
### AC2: ...
### AC3: ...

## Edge Cases
1. **Scenario:** Description
2. **Scenario:** Description

## Non-Functional Requirements
### Performance
- Response time: < 100ms per call (p95)
...
"""
```

**2. Follow contract:**
```python
# ✅ CORRECT
# Contract is specified in frontmatter:
# contract: .claude/skills/spec-driven-stories/contracts/requirements-analyst-contract.yaml

# Parent skill validates output against this contract
# Ensure output complies with contract specifications
```

**3. Self-validate output:**
```python
# ✅ CORRECT - Step 7 above
assert all required sections present
assert no file creation indicators
assert NFRs are measurable
assert AC count >= 3
assert AC format is Given/When/Then
```

**4. Structure content with section headers:**
```python
# ✅ CORRECT
output = "## User Story\n" + user_story_content + "\n\n"
output += "## Acceptance Criteria\n" + ac_content + "\n\n"
output += "## Edge Cases\n" + edge_cases_content + "\n\n"
output += "## Non-Functional Requirements\n" + nfr_content
```

**5. Let parent skill decide file structure:**
```python
# ✅ CORRECT
# You generate CONTENT
# Parent skill (spec-driven-stories Phase 5) creates FILE
# You don't control: filename, file location, YAML frontmatter
# You only provide: markdown sections for story body
```
