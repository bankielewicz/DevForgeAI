# STORY-035 Integration Tests - Quick Reference

**Story:** Internet-Sleuth Framework Compliance (Phase 1 Migration)
**Test File:** `tests/integration/test_story_035_internet_sleuth_integration.py`
**Total Tests:** 32 integration tests

---

## Quick Test Execution

### Run All Tests

```bash
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py -v
```

### Run by Category

```bash
# Category 1: Agent Structure (8 tests)
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure -v

# Category 2: Framework Integration (7 tests)
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthFrameworkIntegration -v

# Category 3: Context File Awareness (6 tests)
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthContextFileAwareness -v

# Category 4: Output Compliance (5 tests)
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthOutputCompliance -v

# Category 5: Error Handling & Security (6 tests)
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthErrorHandlingAndSecurity -v
```

### Run Single Test

```bash
python3 -m pytest tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_file_exists -v
```

### Run with Markers

```bash
# All STORY-035 tests
python3 -m pytest -m story_035 -v

# All integration tests
python3 -m pytest -m integration -v
```

---

## Test Categories

### 1. Agent File Structure and Compliance (8 tests)

**What it tests:**
- Agent file exists at correct location
- YAML frontmatter validity
- Required sections present
- No command execution framework
- Proactive triggers documented
- Explicit invocation example
- Workflow phases defined
- Framework integration section complete

**Why it matters:**
- Ensures agent follows DevForgeAI subagent standards
- Validates agent can be invoked by skills
- Confirms framework-aware design

### 2. Framework Integration Points (7 tests)

**What it tests:**
- Context file paths use `devforgeai/` structure
- devforgeai-ideation skill compatibility
- devforgeai-architecture skill compatibility
- Output directory compliance
- ADR integration documented
- requirements-analyst coordination
- architect-reviewer coordination

**Why it matters:**
- Ensures agent integrates with existing framework
- Validates skill invocation compatibility
- Confirms proper output locations

### 3. Context File Awareness (6 tests)

**What it tests:**
- Phase 1 validates all 6 context files
- tech-stack.md validation documented
- dependencies.md validation documented
- anti-patterns.md validation documented
- architecture-constraints.md validation documented
- Context conflict handling documented

**Why it matters:**
- Ensures agent respects framework constraints
- Validates brownfield/greenfield mode detection
- Confirms conflict detection and resolution

### 4. Output Directory Compliance (5 tests)

**What it tests:**
- Research output directory documented
- Filename conventions documented
- Directory creation documented
- Repository cleanup documented
- Output examples provided

**Why it matters:**
- Ensures consistent output locations
- Validates cleanup procedures
- Confirms naming conventions

### 5. Error Handling and Security (6 tests)

**What it tests:**
- Error handling section exists
- Environment variable usage documented
- No hardcoded credentials
- Secret redaction documented
- Graceful degradation documented
- Structured error responses documented

**Why it matters:**
- Ensures robust error handling
- Validates security best practices
- Confirms no credential leaks

---

## Common Test Failures

### Missing YAML Frontmatter

**Error:** `AssertionError: No YAML frontmatter found`

**Cause:** Agent file doesn't start with `---`

**Fix:** Ensure file starts with:
```yaml
---
name: internet-sleuth
description: ...
tools: ...
model: haiku
---
```

### Command Framework Detected

**Error:** `AssertionError: Found prohibited command framework pattern`

**Cause:** Agent file contains command execution patterns

**Fix:** Remove patterns like:
- `argument-hint:`
- `$1`, `$2` (argument variables)
- `AskUserQuestion.*arguments`

### Missing Required Sections

**Error:** `AssertionError: Missing required section: ## Purpose`

**Cause:** Agent file missing one of the 10 required sections

**Fix:** Ensure all sections present:
1. `## Purpose`
2. `## When Invoked`
3. `## Workflow`
4. `## Framework Integration`
5. `## Success Criteria`
6. `## Error Handling`
7. `## Integration`
8. `## Token Efficiency`
9. `## Security Constraints`
10. `## References` (or similar)

### Path Structure Issues

**Error:** `AssertionError: Found deprecated path pattern`

**Cause:** Agent uses old path structure

**Fix:** Replace:
- `.claude/context/` → `devforgeai/context/`
- `devforgeai/specs/research/` → `devforgeai/research/`

### Missing Context File Documentation

**Error:** `AssertionError: Missing tech-stack.md in Framework Integration`

**Cause:** Framework Integration section doesn't mention all 6 context files

**Fix:** Document all 6 context files:
1. tech-stack.md
2. source-tree.md
3. dependencies.md
4. coding-standards.md
5. architecture-constraints.md
6. anti-patterns.md

---

## Expected Test Output

```
platform linux -- Python 3.12.3, pytest-7.4.4, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /mnt/c/Projects/DevForgeAI2/tests/integration
configfile: pytest.ini
plugins: mock-3.15.0, cov-4.1.0, asyncio-0.21.2, anyio-4.10.0

collected 32 items

tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_file_exists PASSED [  3%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_has_valid_yaml_frontmatter PASSED [  6%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_has_required_sections PASSED [  9%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_no_command_execution_framework PASSED [ 12%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_mentions_proactive_triggers PASSED [ 15%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_agent_has_explicit_invocation_example PASSED [ 18%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_workflow_phases_defined PASSED [ 21%]
tests/integration/test_story_035_internet_sleuth_integration.py::TestInternetSleuthAgentStructure::test_framework_integration_section_complete PASSED [ 25%]
[... 24 more tests ...]
============================== 32 passed in 0.35s ===============================
```

---

## Test Maintenance

### When to Re-run Tests

- After modifying internet-sleuth.md
- Before committing changes
- After merging updates from other branches
- When adding new framework integration points

### When to Update Tests

- When adding new required sections to subagent standard
- When changing context file locations
- When adding new error handling scenarios
- When modifying framework integration patterns

### Adding New Tests

1. Choose appropriate test class (by category)
2. Follow naming convention: `test_<description>`
3. Add `@pytest.mark.story_035` marker
4. Add `@pytest.mark.integration` marker
5. Use helper method `_extract_section(heading)` for section parsing
6. Include clear assertion messages

**Example:**
```python
@pytest.mark.story_035
@pytest.mark.integration
def test_new_feature(self):
    """INT-033: Description of new test"""
    section = self._extract_section('## New Section')
    assert 'expected content' in section, \
        "Clear error message"
```

---

## Troubleshooting

### Tests Won't Collect

**Error:** `'story_035' not found in markers configuration option`

**Solution:** Add to `tests/integration/pytest.ini`:
```ini
markers =
    story_035: STORY-035 - Internet-Sleuth Framework Compliance
```

### Tests Timeout

**Error:** `timeout exceeded`

**Solution:** Increase timeout in pytest.ini or run with `--timeout=60`

### Tests Skip

**Error:** `1 skipped`

**Solution:** Check if test has `@pytest.mark.skip` decorator. Remove or fix underlying issue.

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'yaml'`

**Solution:** Install dependencies:
```bash
pip install pyyaml pytest
```

---

## Integration Test Checklist

Before committing changes to internet-sleuth.md:

- [ ] All 32 integration tests pass
- [ ] No new test failures introduced
- [ ] Test execution time < 1 second
- [ ] No deprecation warnings
- [ ] pytest.ini includes story_035 marker
- [ ] Test documentation updated (if needed)

---

## Related Files

- **Agent File:** `.claude/agents/internet-sleuth.md`
- **Test File:** `tests/integration/test_story_035_internet_sleuth_integration.py`
- **pytest Config:** `tests/integration/pytest.ini`
- **Test Summary:** `tests/STORY-035-INTEGRATION-TEST-SUMMARY.md`
- **Story File:** `devforgeai/specs/Stories/STORY-035.story.md`

---

**Last Updated:** 2025-11-17
**Test Suite Maintainer:** integration-tester subagent
**Story:** STORY-035
