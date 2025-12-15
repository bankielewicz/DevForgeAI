# STORY-035 Test Suite Summary

**Story:** Internet-Sleuth Framework Compliance (Phase 1 Migration)
**Test Generation Date:** 2025-11-17
**TDD Phase:** RED (Failing tests to drive implementation)

---

## Test Coverage Overview

### Acceptance Criteria Tests (6 AC)

| AC | Test File | Test Count | Status |
|----|-----------|------------|--------|
| AC1 | `test_internet_sleuth_ac1_frontmatter.py` | 14 tests | ❌ RED (will fail until migration) |
| AC2 | `test_internet_sleuth_ac2_path_migration.py` | 13 tests | ❌ RED (will fail until migration) |
| AC3 | `test_internet_sleuth_ac3_context_awareness.py` | 17 tests | ❌ RED (will fail until migration) |
| AC4 | `test_internet_sleuth_ac4_subagent_sections.py` | 19 tests | ❌ RED (will fail until migration) |
| AC5 | `test_internet_sleuth_ac5_command_framework_removal.py` | 17 tests | ❌ RED (will fail until migration) |
| AC6 | `test_internet_sleuth_ac6_output_standardization.py` | 16 tests | ❌ RED (will fail until migration) |

**Total AC Tests:** 96 tests

---

### Edge Case Tests (7 scenarios)

| Edge Case | Test File | Test Count | Status |
|-----------|-----------|------------|--------|
| 1. Greenfield projects | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |
| 2. Brownfield incomplete context | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |
| 3. Technology conflicts | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |
| 4. ADR-required scenarios | `test_internet_sleuth_edge_cases.py` | 1 test | ❌ RED |
| 5. Token budget exceeded | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |
| 6. Private repo auth | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |
| 7. Epic coordination | `test_internet_sleuth_edge_cases.py` | 2 tests | ❌ RED |

**Total Edge Case Tests:** 15 tests (13 specific + 2 comprehensive)

---

### Business Rule Tests (4 rules)

| Rule | Test File | Test Count | Status |
|------|-----------|------------|--------|
| BR-001: Context file validation | `test_internet_sleuth_business_rules.py` | 3 tests | ❌ RED |
| BR-002: REQUIRES ADR message | `test_internet_sleuth_business_rules.py` | 2 tests | ❌ RED |
| BR-003: Output directory | `test_internet_sleuth_business_rules.py` | 3 tests | ❌ RED |
| BR-004: GitHub URL validation | `test_internet_sleuth_business_rules.py` | 3 tests | ❌ RED |

**Total Business Rule Tests:** 14 tests (11 specific + 3 comprehensive)

---

### Non-Functional Requirement Tests

| NFR Category | Test File | Test Count | Status |
|--------------|-----------|------------|--------|
| Performance (NFR-001, NFR-002) | `test_internet_sleuth_nfrs.py` | 3 tests | ❌ RED |
| Security (NFR-003, NFR-004) | `test_internet_sleuth_nfrs.py` | 5 tests | ❌ RED |
| Reliability (NFR-005, NFR-006) | `test_internet_sleuth_nfrs.py` | 4 tests | ❌ RED |
| Observability | `test_internet_sleuth_nfrs.py` | 4 tests | ❌ RED |

**Total NFR Tests:** 20 tests (16 specific + 4 best practice)

---

## Test Organization

### Test Files

```
tests/unit/
├── conftest.py                                      # Shared fixtures
├── test_internet_sleuth_ac1_frontmatter.py          # AC1: Frontmatter compliance
├── test_internet_sleuth_ac2_path_migration.py       # AC2: Path references
├── test_internet_sleuth_ac3_context_awareness.py    # AC3: Context file awareness
├── test_internet_sleuth_ac4_subagent_sections.py    # AC4: Standard sections
├── test_internet_sleuth_ac5_command_framework_removal.py # AC5: Command removal
├── test_internet_sleuth_ac6_output_standardization.py    # AC6: Output location
├── test_internet_sleuth_edge_cases.py               # Edge case scenarios
├── test_internet_sleuth_business_rules.py           # Business rule enforcement
├── test_internet_sleuth_nfrs.py                     # Non-functional requirements
└── STORY-035-TEST-SUMMARY.md                        # This file
```

### Pytest Markers

All tests are marked with:
- `@pytest.mark.story_035` - Story identifier
- `@pytest.mark.acceptance_criteria` - AC tests
- `@pytest.mark.edge_case` - Edge case tests
- `@pytest.mark.business_rule` - Business rule tests
- `@pytest.mark.nfr` - Non-functional requirement tests
- `@pytest.mark.unit` - Unit test classification

---

## Test Execution

### Run All STORY-035 Tests

```bash
# Run all tests for this story
pytest tests/unit/ -m story_035 -v

# Expected output (initially):
# ============================= test session starts ==============================
# collected 145 items
#
# tests/unit/test_internet_sleuth_ac1_frontmatter.py::TestAC1FrontmatterCompliance::test_frontmatter_has_required_field_name FAILED
# tests/unit/test_internet_sleuth_ac1_frontmatter.py::TestAC1FrontmatterCompliance::test_frontmatter_name_uses_kebab_case FAILED
# ... (143 more failures)
#
# ========================= 145 failed in 2.34s ===============================
```

### Run Tests by Category

```bash
# Acceptance criteria tests only
pytest tests/unit/ -m "story_035 and acceptance_criteria" -v

# Edge case tests only
pytest tests/unit/ -m "story_035 and edge_case" -v

# Business rule tests only
pytest tests/unit/ -m "story_035 and business_rule" -v

# NFR tests only
pytest tests/unit/ -m "story_035 and nfr" -v
```

### Run Tests by AC

```bash
# AC1: Frontmatter compliance
pytest tests/unit/test_internet_sleuth_ac1_frontmatter.py -v

# AC2: Path migration
pytest tests/unit/test_internet_sleuth_ac2_path_migration.py -v

# ... etc for AC3-6
```

---

## Test Details by Acceptance Criteria

### AC1: Frontmatter Compliance (14 tests)

**Tests:**
1. `test_frontmatter_has_required_field_name` - Name field exists
2. `test_frontmatter_name_uses_kebab_case` - Name format validation
3. `test_frontmatter_has_required_field_description` - Description field exists
4. `test_frontmatter_description_includes_proactive_triggers` - Ideation/architecture keywords
5. `test_frontmatter_has_required_field_tools` - Tools field exists
6. `test_frontmatter_tools_comma_separated` - Tools format validation
7. `test_frontmatter_has_required_field_model` - Model field exists
8. `test_frontmatter_optional_field_color` - Color field validation (optional)
9. `test_frontmatter_forbids_deprecated_command_prefix` - No command_prefix
10. `test_frontmatter_forbids_deprecated_output_format` - No output_format
11. `test_frontmatter_yaml_valid_syntax` - Valid YAML
12. `test_frontmatter_completeness_all_required_fields` - All 4 required fields
13. `test_frontmatter_no_extra_unexpected_fields` - Edge case: unexpected fields

**Component Coverage:** COMP-001, COMP-002

---

### AC2: Path Migration (13 tests)

**Tests:**
1. `test_no_old_context_path_references` - No .claude/context/
2. `test_no_old_adrs_path_references` - No .claude/adrs/
3. `test_no_bmad_core_path_references` - No .bmad-core/
4. `test_no_old_research_path_references` - No devforgeai/specs/research/
5. `test_uses_new_devforgeai_context_path` - Uses devforgeai/context/
6. `test_uses_new_devforgeai_adrs_path` - Uses .devforgeai/adrs/
7. `test_uses_new_devforgeai_research_path` - Uses .devforgeai/research/
8. `test_uses_ai_docs_stories_path_correctly` - Uses devforgeai/specs/Stories/
9. `test_uses_ai_docs_epics_path_correctly` - Uses devforgeai/specs/Epics/
10. `test_no_mixed_path_conventions` - Edge case: no mixing old/new
11. `test_path_references_use_correct_format` - Edge case: format consistency
12. `test_no_absolute_paths_to_context_files` - No hardcoded absolute paths
13. `test_comp_003_all_path_references_migrated` - Comprehensive migration test

**Component Coverage:** COMP-003

---

### AC3: Context File Awareness (17 tests)

**Tests:**
1. `test_framework_integration_section_exists` - Section exists
2. `test_references_tech_stack_context_file` - tech-stack.md referenced
3. `test_references_source_tree_context_file` - source-tree.md referenced
4. `test_references_dependencies_context_file` - dependencies.md referenced
5. `test_references_coding_standards_context_file` - coding-standards.md referenced
6. `test_references_architecture_constraints_context_file` - architecture-constraints.md referenced
7. `test_references_anti_patterns_context_file` - anti-patterns.md referenced
8. `test_comp_004_all_six_context_files_listed` - All 6 files present
9. `test_context_files_have_purpose_documented` - Purpose documented
10. `test_context_files_have_when_to_check_guidance` - "When to check" guidance
11. `test_adr_awareness_workflow_present` - ADR check workflow
12. `test_adr_workflow_includes_askuserquestion_for_conflicts` - Edge case: AskUserQuestion
13. `test_br_001_agent_halts_if_context_files_missing` - BR-001: HALT behavior
14. `test_br_002_requires_adr_message_for_tech_not_in_stack` - BR-002: REQUIRES ADR
15. `test_framework_aware_not_autonomous` - Framework-aware behavior

**Component Coverage:** COMP-004, COMP-005, BR-001, BR-002

---

### AC4: Subagent Sections (19 tests)

**Tests:**
1. `test_when_invoked_section_exists` - When Invoked section
2. `test_when_invoked_has_proactive_triggers` - Proactive triggers documented
3. `test_when_invoked_mentions_devforgeai_ideation` - Ideation skill mentioned
4. `test_when_invoked_mentions_devforgeai_architecture` - Architecture skill mentioned
5. `test_when_invoked_has_explicit_invocation_pattern` - Task invocation example
6. `test_framework_integration_section_exists` - Framework Integration section
7. `test_framework_integration_documents_invoking_skills` - Invoking skills documented
8. `test_framework_integration_documents_required_context` - Context requirements
9. `test_success_criteria_section_exists` - Success Criteria section
10. `test_success_criteria_is_measurable_checklist` - Checkbox format
11. `test_success_criteria_includes_token_budget` - Token budget (<40K)
12. `test_integration_section_exists` - Integration section
13. `test_integration_lists_devforgeai_ideation` - Ideation in Integration
14. `test_integration_lists_devforgeai_architecture` - Architecture in Integration
15. `test_comp_006_007_008_all_sections_present` - All 3 new sections
16. `test_sections_follow_devforgeai_formatting_conventions` - Edge case: formatting
17. `test_success_criteria_has_multiple_measurable_items` - Edge case: ≥3 items
18. `test_integration_section_documents_coordination` - Coordination documented

**Component Coverage:** COMP-006, COMP-007, COMP-008

---

### AC5: Command Framework Removal (17 tests)

**Tests:**
1. `test_no_command_execution_framework_heading` - No "Command Execution Framework"
2. `test_no_step_1_load_decision_history` - No legacy Step 1
3. `test_no_step_2_load_dependencies` - No legacy Step 2
4. `test_no_available_commands_section` - No "Available Commands"
5. `test_no_research_command_syntax` - No *research syntax
6. `test_no_competitive_analysis_command_syntax` - No *competitive-analysis
7. `test_no_technology_monitoring_command_syntax` - No *technology-monitoring
8. `test_no_repository_archaeology_command_syntax` - No *repository-archaeology
9. `test_no_market_intelligence_command_syntax` - No *market-intelligence
10. `test_no_validate_research_command_syntax` - No *validate-research
11. `test_comp_009_010_all_command_patterns_removed` - Comprehensive removal
12. `test_has_research_capabilities_or_workflow_section` - Narrative section exists
13. `test_narrative_section_uses_prose_not_commands` - Prose workflow
14. `test_no_command_parsing_logic_in_agent` - Edge case: no parsing logic
15. `test_no_dependencies_field_in_command_documentation` - Edge case: old dependencies
16. `test_simplified_capabilities_focus_on_research_tasks` - Research focus
17. `test_no_command_prefix_execution_framework_in_any_section` - Comprehensive check

**Component Coverage:** COMP-009, COMP-010, COMP-011

---

### AC6: Output Standardization (16 tests)

**Tests:**
1. `test_documents_devforgeai_research_output_path` - .devforgeai/research/ documented
2. `test_repository_management_uses_devforgeai_research` - Repository Management section
3. `test_no_old_research_output_paths` - No deprecated paths
4. `test_documents_tech_eval_filename_convention` - tech-eval-{topic}-{date}.md
5. `test_documents_pattern_analysis_filename_convention` - pattern-analysis-{repo}-{date}.md
6. `test_documents_competitive_filename_convention` - competitive-{topic}-{date}.md
7. `test_filename_conventions_use_iso_date_format` - ISO dates (YYYY-MM-DD)
8. `test_comp_012_013_output_structure_comprehensive` - Comprehensive structure
9. `test_documents_directory_creation_if_not_exists` - Edge case: directory creation
10. `test_no_hardcoded_output_paths_in_examples` - Edge case: no absolute paths
11. `test_br_003_research_directory_documented` - BR-003: output directory
12. `test_br_003_directory_permissions_documented` - BR-003: 755 permissions
13. `test_output_format_consistency_across_research_types` - Consistent format
14. `test_no_references_to_tmp_repos_research_pattern` - No old tmp/repos pattern

**Component Coverage:** COMP-012, COMP-013, BR-003

---

## Edge Cases Coverage

| Scenario | Test Count | Key Assertions |
|----------|------------|----------------|
| 1. Greenfield (no context files) | 2 | Greenfield mode documented, tech-stack recommendations |
| 2. Brownfield (4 of 6 files) | 2 | HALT behavior, recommend /create-context |
| 3. Technology conflicts | 2 | REQUIRES ADR message, AskUserQuestion with 2 options |
| 4. ADR-required | 1 | ADR check workflow, proper naming format |
| 5. Token budget exceeded | 2 | Progressive disclosure, partial analysis |
| 6. Private repo auth | 2 | Auth error handling, gh CLI link, no retries |
| 7. Epic coordination | 2 | Read epic file, align recommendations |

---

## Business Rules Coverage

| Rule | Test Count | Key Assertions |
|------|------------|----------------|
| BR-001: Context file validation | 3 | Check all 6 files, HALT if missing, list missing files |
| BR-002: REQUIRES ADR | 2 | Return REQUIRES ADR message, AskUserQuestion with 2 options |
| BR-003: Output directory | 3 | Write to .devforgeai/research/, create if not exists, 755 permissions |
| BR-004: GitHub URL validation | 3 | Validate GitHub pattern, reject malformed, specify format in error |

---

## Test Execution Estimates

**Total Test Count:** 145 tests
- **AC Tests:** 96 tests (~60 seconds to run)
- **Edge Case Tests:** 15 tests (~10 seconds to run)
- **Business Rule Tests:** 14 tests (~10 seconds to run)
- **NFR Tests:** 20 tests (~15 seconds to run)

**Estimated Total Execution Time:** ~95 seconds (1.5 minutes)

---

## Success Criteria

### Phase: RED (Current)

All tests are expected to FAIL initially:
- ✅ Tests generated for all 6 acceptance criteria
- ✅ Edge cases covered (7 scenarios)
- ✅ Business rules tested (4 rules)
- ✅ NFRs validated
- ✅ Tests follow AAA pattern
- ✅ Tests use pytest markers
- ✅ Tests ready to run: `pytest tests/unit/ -m story_035`

### Phase: GREEN (After Implementation)

After migration implementation, tests should PASS:
- All 96 AC tests passing
- All 15 edge case tests passing
- All 14 business rule tests passing
- All 20 NFR tests passing
- **Total: 145/145 tests passing (100% pass rate)**

### Phase: REFACTOR (Optional)

After GREEN phase:
- Test code refactoring for DRY principles
- Additional integration tests (optional)
- Performance tests for repository analysis (optional)

---

## Test Maintenance

**Update triggers:**
- Story changes: Update affected test files
- AC modifications: Regenerate AC tests
- New edge cases: Add to `test_internet_sleuth_edge_cases.py`
- New business rules: Add to `test_internet_sleuth_business_rules.py`

**Test review:**
- After migration complete: Review all tests for relevance
- After QA feedback: Update assertions if needed
- After production: Add regression tests for any bugs found

---

## References

- **Story:** `devforgeai/specs/Stories/STORY-035-internet-sleuth-framework-compliance.story.md`
- **Agent File:** `.claude/agents/internet-sleuth.md`
- **Test Files:** `tests/unit/test_internet_sleuth_*.py`
- **Pytest Config:** `pytest.ini`
- **Shared Fixtures:** `tests/unit/conftest.py`

---

**Generated:** 2025-11-17
**Story:** STORY-035
**Test Generation Tool:** test-automator skill (TDD Red phase)
**Framework:** DevForgeAI Test-Driven Development
