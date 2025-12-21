# STORY-116 Recovery Prompt

**Use this prompt if context window is full/crashes during implementation**

---

## Recovery Command

```
/resume-dev STORY-116 --from-phase 03
```

OR paste this prompt:

---

## Manual Recovery Prompt

I was implementing STORY-116 (Configuration Infrastructure - ast-grep Rule Storage) and my context window may have crashed. Please resume the TDD workflow.

### Current State

**Plan File:** `/home/bryan/.claude/plans/composed-yawning-marshmallow.md`

**Story File:** `devforgeai/specs/Stories/STORY-116-configuration-infrastructure.story.md`

**Completed Work:**

1. **Phase 01 Pre-Flight**: COMPLETE
   - Git validated (on branch `refactor/devforgeai-migration`)
   - All 6 context files validated
   - Tech stack detected (Python 3.8+, PyYAML, pytest)

2. **Phase 02 Test-First**: COMPLETE
   - Test files created with embedded implementations:
     - `tests/unit/test_rule_metadata_story116.py` (25 tests)
     - `tests/unit/test_config_init_story116.py` (17 tests)
     - `tests/unit/test_config_validator_story116.py` (16 tests)
     - `tests/integration/test_ast_grep_cli_story116.py`

3. **Phase 03 Implementation**: IN PROGRESS
   - Created `src/claude/scripts/devforgeai_cli/ast_grep/` package:
     - `__init__.py` - Package exports
     - `models.py` - RuleMetadata, RuleSeverity, RuleLanguage
     - `config_init.py` - ConfigurationInitializer class
     - `config_validator.py` - ConfigurationValidator class
   - **STILL NEEDED:**
     - Update test files to import from modules (not embedded classes)
     - Add CLI subcommands to `cli.py`
     - Run tests to verify

### Resume Instructions

1. **First, check current state:**
   ```
   Glob(pattern="**/ast_grep/*.py")
   ```

2. **Update test files** to import from modules instead of using embedded implementations

3. **Add CLI subcommands** to `cli.py`:
   - `devforgeai ast-grep init [--force]`
   - `devforgeai ast-grep validate-config [--config PATH]`

4. **Run all tests:**
   ```
   python3 -m pytest tests/unit/test_*story116*.py tests/integration/test_*story116*.py -v
   ```

5. **Continue to Phase 04** (Refactoring) after tests pass

### Key Files to Review

| File | Purpose |
|------|---------|
| `src/claude/scripts/devforgeai_cli/cli.py` | Add init/validate-config subcommands (lines 156-188) |
| `src/claude/scripts/devforgeai_cli/ast_grep/` | New package with implementation |
| `tests/unit/test_*story116.py` | Test files - need import updates |

### Acceptance Criteria Reminder

- AC#1: Create `devforgeai/ast-grep/` directory structure
- AC#2: Rules organized by language directory
- AC#3: `devforgeai ast-grep init` creates sgconfig.yml
- AC#4: `devforgeai ast-grep validate-config` validates configuration

---

**Last Updated:** During Phase 03 implementation
