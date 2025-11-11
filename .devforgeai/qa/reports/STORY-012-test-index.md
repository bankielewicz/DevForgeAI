# STORY-012 Test Index - Quick Reference

**Test File:** `/mnt/c/Projects/DevForgeAI2/tests/test_template_customization.py`
**Total Tests:** 65 test methods in 13 test classes
**File Size:** 1,546 lines
**Status:** RED PHASE (All tests should FAIL)

---

## Test Classes and Methods

### 1. TestCustomFieldCreation (6 test methods)

Unit tests for creating custom template fields with different data types.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_create_custom_field_with_select_type` | Create select field with options | AC1 |
| `test_should_create_custom_field_with_text_type` | Create text field | AC4 |
| `test_should_create_custom_field_with_date_type` | Create date field | AC4 |
| `test_should_create_custom_field_with_number_type` | Create number field | AC4 |
| `test_should_create_custom_field_with_checkbox_type` | Create checkbox field | AC4 |
| `test_should_create_custom_field_with_textarea_type` | Create textarea field | AC4 |
| `test_should_set_field_as_required` | Mark field as required | AC1 |
| `test_should_set_field_as_optional` | Mark field as optional | AC1 |
| `test_should_create_personal_custom_field` | Personal scope field | AC1 |

### 2. TestCustomFieldUpdate (3 test methods)

Unit tests for updating custom template fields.

| Method | Purpose | Business Rule |
|--------|---------|---------------|
| `test_should_edit_custom_field_name` | Update field name and description | AC1 |
| `test_should_edit_custom_field_options` | Update select field options | AC1 |
| `test_should_not_allow_type_change_after_creation` | Type is immutable | BR2 |

### 3. TestCustomFieldDeletion (2 test methods)

Unit tests for deleting custom template fields.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_delete_custom_field_with_confirmation` | Delete with explicit confirmation | AC1 |
| `test_should_require_confirmation_for_field_deletion` | Confirmation is mandatory | AC1 |

### 4. TestTeamQuestionCreation (3 test methods)

Unit tests for creating team-specific questions.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_create_team_question` | Create new team question | AC2 |
| `test_should_create_optional_team_question` | Create optional question | AC2 |
| `test_should_store_team_question_in_configuration` | Verify storage in config | AC2 |

### 5. TestTeamQuestionOrdering (1 test method)

Unit tests for team question ordering in workflow.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_place_custom_questions_after_framework_questions` | Custom questions after defaults | AC2 |

### 6. TestCustomFieldValidation (8 test methods)

Unit tests for custom field value validation.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_validate_required_field` | Required fields block creation | AC4 |
| `test_should_validate_date_field_format` | Date format validation | AC4 |
| `test_should_validate_number_field_format` | Number format validation | AC4 |
| `test_should_validate_select_field_option` | Select option validation | AC4 |
| `test_should_validate_text_field_length_min` | Minimum length constraint | AC4 |
| `test_should_validate_text_field_length_max` | Maximum length constraint | AC4 |
| `test_should_validate_number_field_min_constraint` | Minimum value constraint | AC4 |
| `test_should_validate_number_field_max_constraint` | Maximum value constraint | AC4 |

### 7. TestDataValidationRules (11 test methods)

Unit tests for all 10 data validation rules from specification.

| Method | Purpose | Validation Rule |
|--------|---------|-----------------|
| `test_field_name_must_be_3_to_100_chars` | Field name length | VR1 |
| `test_field_name_must_be_unique_per_team` | Field name uniqueness | VR1 |
| `test_field_type_must_be_valid_enum` | Type enum validation | VR2 |
| `test_select_field_requires_min_2_options` | Select min options | VR3 |
| `test_select_field_requires_unique_option_values` | Option uniqueness | VR3 |
| `test_visibility_must_be_valid_enum` | Visibility enum | VR5 |
| `test_team_id_required_for_team_visibility` | Team ID requirement | VR6 |
| `test_question_text_must_be_10_to_500_chars` | Question length | VR7 |
| `test_template_name_must_be_5_to_100_chars` | Template name length | VR8 |
| `test_inherited_sections_min_1_and_must_exist` | Section existence | VR9 |
| `test_framework_version_must_be_valid_semver` | Version format | VR10 |

### 8. TestTemplateInheritance (6 test methods)

Unit tests for template inheritance behavior.

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_inherit_default_sections` | Inherit from defaults | AC3 |
| `test_should_add_custom_fields_as_new_sections` | Custom as new sections | AC3 |
| `test_should_render_default_sections_before_custom` | Default → custom ordering | AC3 |
| `test_should_auto_update_inherited_sections_on_framework_upgrade` | Auto-update on upgrade | AC3, BR5 |
| `test_should_revert_custom_template_to_defaults` | Revert to defaults action | AC3 |

### 9. TestCompleteCustomFieldWorkflow (1 test method)

Integration test for complete custom field lifecycle.

| Method | Purpose | Scope |
|--------|---------|-------|
| `test_full_custom_field_lifecycle` | Create → use → update → delete workflow | Integration |

### 10. TestTeamQuestionWorkflow (1 test method)

Integration test for team question workflow in story creation.

| Method | Purpose | Scope |
|--------|---------|-------|
| `test_team_questions_appear_in_story_creation` | Question creation and appearance | Integration |

### 11. TestCustomTemplateSharing (6 test methods)

Integration tests for team sharing and permissions (AC5).

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_should_share_template_with_team` | Share template with team | AC5 |
| `test_shared_template_visible_to_team_members` | Team visibility | AC5 |
| `test_team_members_cannot_modify_shared_template` | Read-only enforcement | AC5 |
| `test_creator_can_modify_shared_template` | Creator permissions | AC5 |
| `test_team_member_can_copy_shared_template` | Copy capability | AC5 |
| `test_template_copy_is_independent` | Copy independence | AC5 |

### 12. TestEdgeCases (8 test methods)

Edge case tests for boundary conditions and error scenarios.

| Method | Purpose | Edge Case |
|--------|---------|-----------|
| `test_edge_case_1_field_name_conflict_with_inherited_section` | Name conflicts | EC1 |
| `test_edge_case_2_cannot_delete_field_in_use` | Delete field in use | EC2 |
| `test_edge_case_3_framework_upgrade_adds_required_section` | New required section | EC3 |
| `test_edge_case_4_version_mismatch_auto_updates` | Version mismatch | EC4 |
| `test_edge_case_5_non_creator_read_only_shared_template` | Read-only enforcement | EC5 |
| `test_edge_case_6_export_template_to_different_team` | Cross-team export | EC6 |
| `test_edge_case_7_select_field_empty_options_list` | Invalid field state | EC7 |
| `test_edge_case_8_circular_dependency_prevention` | Circular dependencies | EC8 |

### 13. TestDataPersistence (4 test methods)

Integration tests for data persistence across framework versions (AC6).

| Method | Purpose | Acceptance Criteria |
|--------|---------|-------------------|
| `test_custom_template_survives_framework_upgrade` | Version upgrade survival | AC6 |
| `test_inherited_sections_auto_reflect_v2_0_defaults` | Auto-reflection of defaults | AC6 |
| `test_custom_fields_preserved_unless_conflict` | Field preservation | AC6 |
| `test_conflict_notification_on_upgrade` | Conflict handling | AC6 |

### Metadata Tests (3 test methods)

Verification tests that coverage is complete.

| Method | Purpose |
|--------|---------|
| `test_all_acceptance_criteria_covered` | Verify AC1-AC6 coverage |
| `test_all_edge_cases_covered` | Verify EC1-EC8 coverage |
| `test_all_data_types_covered` | Verify 6 data types coverage |

---

## Test Fixtures

| Fixture | Purpose | Returns |
|---------|---------|---------|
| `user_uuid` | Valid user identifier | UUID string |
| `team_uuid` | Valid team identifier | UUID string |
| `another_team_uuid` | Different team identifier | UUID string |
| `valid_custom_field_payload` | Standard field creation data | Dict with select field payload |
| `valid_team_question_payload` | Standard question data | Dict with question payload |
| `valid_custom_template_payload` | Standard template data | Dict with template payload |

---

## Coverage Summary

### By Acceptance Criteria

- **AC1 (Custom Fields CRUD):** 10 tests ✅
- **AC2 (Team Questions):** 4 tests ✅
- **AC3 (Inheritance):** 6 tests ✅
- **AC4 (Validation):** 8 tests ✅
- **AC5 (Team Sharing):** 6 tests ✅
- **AC6 (Data Persistence):** 4 tests ✅

### By Test Category

- **Unit Tests:** 31 tests (49%)
- **Integration Tests:** 15 tests (24%)
- **Edge Case Tests:** 8 tests (13%)
- **Data Type Tests:** 6 tests (9%)
- **Meta Tests:** 3 tests (5%)

### By Data Type

- **text:** Tested ✅
- **select:** Tested ✅
- **date:** Tested ✅
- **number:** Tested ✅
- **checkbox:** Tested ✅
- **textarea:** Tested ✅

### By Validation Rule

- **VR1 (Field name):** 2 tests ✅
- **VR2 (Field type):** 1 test ✅
- **VR3 (Select options):** 2 tests ✅
- **VR5 (Visibility):** 1 test ✅
- **VR6 (Team ID):** 1 test ✅
- **VR7 (Question text):** 1 test ✅
- **VR8 (Template name):** 1 test ✅
- **VR9 (Inherited sections):** 1 test ✅
- **VR10 (Framework version):** 1 test ✅

### By Edge Case

- **EC1 (Name conflicts):** Tested ✅
- **EC2 (Delete in use):** Tested ✅
- **EC3 (Framework upgrade):** Tested ✅
- **EC4 (Version mismatch):** Tested ✅
- **EC5 (Read-only):** Tested ✅
- **EC6 (Cross-team):** Tested ✅
- **EC7 (Invalid state):** Tested ✅
- **EC8 (Circular deps):** Tested ✅

---

## Test Execution Guide

### Run All Tests

```bash
pytest tests/test_template_customization.py -v
```

### Expected Result (RED PHASE)

```
63 failed, 0 passed in 2.34s
```

All tests fail because implementation doesn't exist yet.

### Run Specific Test Class

```bash
pytest tests/test_template_customization.py::TestCustomFieldCreation -v
```

### Run Specific Test Method

```bash
pytest tests/test_template_customization.py::TestCustomFieldCreation::test_should_create_custom_field_with_select_type -v
```

### Run with Coverage

```bash
pytest tests/test_template_customization.py --cov=src --cov-report=html
```

### Run with Verbose Output

```bash
pytest tests/test_template_customization.py -vv --tb=short
```

---

## Quick Link to Requirements

| Item | Link |
|------|------|
| Full Test File | `/mnt/c/Projects/DevForgeAI2/tests/test_template_customization.py` |
| Test Summary | `/mnt/c/Projects/DevForgeAI2/.devforgeai/qa/reports/STORY-012-test-generation-summary.md` |
| Story Document | `/mnt/c/Projects/DevForgeAI2/.ai_docs/Stories/STORY-012-template-customization.story.md` |
| Tech Stack | `/mnt/c/Projects/DevForgeAI2/.devforgeai/context/tech-stack.md` |
| Source Tree | `/mnt/c/Projects/DevForgeAI2/.devforgeai/context/source-tree.md` |
| Coding Standards | `/mnt/c/Projects/DevForgeAI2/.devforgeai/context/coding-standards.md` |

---

## Implementation Roadmap

### Phase 1: RED (Test Definition) ✅ COMPLETE
- Tests written and failing
- Contract defined clearly
- All requirements specified via tests

### Phase 2: GREEN (Implementation) ⏳ PENDING
1. Implement POST /api/templates/custom-fields
2. Implement PUT /api/templates/custom-fields/{field_id}
3. Implement DELETE /api/templates/custom-fields/{field_id}
4. Implement POST /api/templates/team-questions
5. Implement POST /api/templates/custom
6. Implement validation logic (VR1-VR10)
7. Implement inheritance resolution
8. Implement team sharing permissions
9. Run tests - should pass incrementally

### Phase 3: REFACTOR (Optimization) ⏳ PENDING
- Improve performance
- Optimize database queries
- Refactor for maintainability
- Add caching if needed
- All tests continue to pass

---

**Status:** ✅ RED PHASE COMPLETE - Ready for implementation team
