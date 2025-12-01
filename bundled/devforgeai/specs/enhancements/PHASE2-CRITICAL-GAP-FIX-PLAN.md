# Phase 2 Critical Gap Fix Plan - Skill v2.0 Integration

**Date:** 2025-11-08
**Priority:** 🚨 CRITICAL
**Issue:** Skills won't auto-generate v2.0 format (only 15% of planned modifications done)
**Timeline:** 2-4 hours
**Risk Level:** 🟡 Medium (breaking changes possible if not careful)

---

## 🎯 **Problem Statement**

### **What's Broken**

**Phase 2 agent created v2.0 tooling but didn't update skills to USE it:**

**✅ What works:**
- story-template.md has v2.0 YAML format
- STRUCTURED-FORMAT-SPECIFICATION.md defines schema
- validate_tech_spec.py can parse v2.0
- technical-specification-creation.md (reference) has v2.0 guidance

**❌ What's missing:**
- devforgeai-story-creation/SKILL.md doesn't mention v2.0
- Requirements-analyst doesn't know to output structured format
- Story-structure-guide.md doesn't document v2.0
- Validation-checklists.md doesn't validate v2.0

**Impact:**
```
User: /create-story "New feature"
  ↓
Skill: No v2.0 instructions in SKILL.md
  ↓
Result: Might generate v1.0 freeform OR hybrid format
  ↓
Problem: Inconsistent story format
```

---

## 📋 **Fix Plan Overview**

### **3 Phases (Sequential)**

**Phase A: Verification (30 min)**
- Test if `/create-story` currently generates v2.0
- Determine if gap is theoretical or actual

**Phase B: Critical Fixes (1-2 hours)**
- Update SKILL.md files to reference v2.0
- Update subagent instructions
- Ensure progressive disclosure loads v2.0 guidance

**Phase C: Validation (30 min)**
- Test `/create-story` after fixes
- Verify v2.0 generated correctly
- Document results

**Total Time:** 2-3 hours

---

## 📅 **Detailed Implementation Plan**

### **PHASE A: VERIFICATION (30 minutes)**

#### **Step A.1: Test Current /create-story Behavior**

**Objective:** Determine if gap is real or theoretical

**Procedure:**
1. Create test story with `/create-story`
2. Check format_version in frontmatter
3. Check if Technical Specification uses YAML
4. Check if components have test_requirement fields

**Test command:**
```
/create-story "User login with email and password authentication"
```

**Check generated story:**
```bash
# Find the generated story
ls -lt .ai_docs/Stories/ | head -5

# Check frontmatter
head -15 .ai_docs/Stories/STORY-XXX-*.story.md | grep format_version

# Check tech spec format
grep -A 20 "## Technical Specification" .ai_docs/Stories/STORY-XXX-*.story.md
```

**Decision criteria:**

**If story has format_version: "2.0" AND YAML tech spec:**
- ✅ **Gap is theoretical** (reference file guidance is sufficient)
- ✅ Skills already work correctly
- ✅ No fixes needed
- **Action:** Document that v2.0 works, close gap

**If story has format_version: "1.0" OR freeform text:**
- 🚨 **Gap is real** (skills not generating v2.0)
- 🚨 Fixes required
- **Action:** Proceed to Phase B

**Time:** 20 minutes (10 min story creation + 10 min verification)

---

#### **Step A.2: Analyze Gap If Found**

**If gap confirmed, determine root cause:**

**Check which reference file skill loads:**
```bash
# See if SKILL.md mentions technical-specification-creation.md
grep "technical-specification" .claude/skills/devforgeai-story-creation/SKILL.md
```

**Hypothesis testing:**

**Hypothesis 1:** Skill doesn't load the reference file
- **Test:** Check if SKILL.md Phase 3 says "Load technical-specification-creation.md"
- **If missing:** Skill doesn't know v2.0 guidance exists
- **Fix:** Add reference file loading instruction

**Hypothesis 2:** Reference file loaded but subagents ignore it
- **Test:** Check if subagent prompts mention v2.0
- **If missing:** Subagents don't know to output structured format
- **Fix:** Update subagent instructions

**Hypothesis 3:** Template used but filled incorrectly
- **Test:** Check if story has YAML block but it's empty/placeholder
- **If true:** Skill loads template but doesn't populate YAML
- **Fix:** Update story file creation logic

**Time:** 10 minutes

---

### **PHASE B: CRITICAL FIXES (1-2 hours)**

**Only execute if Phase A confirms gap is real**

---

#### **Fix 1: Update devforgeai-story-creation/SKILL.md** (CRITICAL - 15 min)

**File:** `.claude/skills/devforgeai-story-creation/SKILL.md`

**Current Phase 3 section (likely says):**
```markdown
### Phase 3: Technical Specification
**Purpose:** Define API contracts, data models, business rules
**Reference:** `references/technical-specification-creation.md`
```

**Add after "Reference:" line:**

```markdown
**Format Version:** 2.0 (Structured YAML) - **Default for all stories created after 2025-11-07**

**Critical:** All new stories MUST use v2.0 structured YAML format in Technical Specification section. This enables:
- 95%+ parsing accuracy (vs 85% with v1.0 freeform text)
- Automated validation in Phase 3 (implementation-validator requires v2.0)
- Deterministic coverage gap detection in Phase 1 Step 4

**v2.0 Format Overview:**
Technical Specification section contains YAML code block with:
- `components`: Array of Service, Worker, Configuration, Logging, Repository, API, DataModel
- `business_rules`: Array of domain rules with test_requirement
- `non_functional_requirements`: Array of NFRs with measurable metrics

**Complete schema reference:**
`.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md`

**The reference file `technical-specification-creation.md` contains:**
- Complete v2.0 generation instructions
- Component type selection guide
- Test requirement format
- api-designer integration for API components

**Load and follow technical-specification-creation.md for Phase 3 execution.**
```

**Location to insert:** After Phase 3 header, before reference file load

**Validation:** Run `/create-story` after this change, verify v2.0 generated

**Time:** 15 minutes

---

#### **Fix 2: Update story-requirements-analyst.md** (HIGH - 20 min)

**File:** `.claude/agents/story-requirements-analyst.md`

**Find section:** "Output Format" or add new section after "Purpose"

**Add:**

```markdown
---

## Output Format (RCA-006 Phase 2: Structured Requirements)

**CRITICAL:** This subagent provides CONTENT ONLY (no file creation). Parent skill (devforgeai-story-creation) will assemble your output into v2.0 structured YAML format.

**Your role:** Extract component details from feature description

**Output structured component information:**

When you identify components (services, workers, configuration, logging, repositories, APIs, data models), output in this format:

**Component Type: [Service|Worker|Configuration|Logging|Repository|API|DataModel]**
**Name:** [ComponentName]
**File Path:** src/[layer]/[path]/[ComponentName].cs
**Dependencies:** [List dependencies]

**Requirements:**
1. [Requirement 1 description]
   - Test: [Specific test for this requirement]
   - Priority: [Critical|High|Medium|Low]

2. [Requirement 2 description]
   - Test: [Specific test for this requirement]
   - Priority: [Critical|High|Medium|Low]

**Example Output:**

```
Component Type: Worker
Name: AlertDetectionWorker
File Path: src/Workers/AlertDetectionWorker.cs
Dependencies: IAlertDetectionService, ILogger<AlertDetectionWorker>

Requirements:
1. Must run continuous polling loop with cancellation token support
   - Test: Worker polls at 30s intervals until CancellationToken signals stop
   - Priority: Critical

2. Must handle exceptions without stopping worker
   - Test: Exception in poll iteration doesn't crash worker, logs error, continues
   - Priority: High
```

**Parent skill will convert to YAML:**
```yaml
- type: "Worker"
  name: "AlertDetectionWorker"
  file_path: "src/Workers/AlertDetectionWorker.cs"
  dependencies:
    - "IAlertDetectionService"
    - "ILogger<AlertDetectionWorker>"
  requirements:
    - id: "WKR-001"
      description: "Must run continuous polling loop with cancellation token support"
      testable: true
      test_requirement: "Test: Worker polls at 30s intervals until CancellationToken signals stop"
      priority: "Critical"
    - id: "WKR-002"
      description: "Must handle exceptions without stopping worker"
      testable: true
      test_requirement: "Test: Exception in poll iteration doesn't crash worker, logs error, continues"
      priority: "High"
```

**Component Type Selection Guide:**

Use these component types based on feature description:
- **Service:** Main business logic classes, orchestrators, application services
- **Worker:** Background tasks, polling loops, scheduled jobs (keywords: "poll", "background", "scheduled", "monitor")
- **Configuration:** Settings files, config loading (keywords: "appsettings", "configuration", "settings")
- **Logging:** Log configuration, sinks (keywords: "log", "Serilog", "NLog", "audit")
- **Repository:** Data access layer (keywords: "database", "repository", "Dapper", "EF Core", "data access")
- **API:** HTTP endpoints (keywords: "API", "endpoint", "REST", "GraphQL", "HTTP")
- **DataModel:** Database entities, DTOs (keywords: "entity", "table", "model", "DTO")

**See `.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` for complete component schemas.**
```

**Location:** After "Purpose" section, before "Workflow"

**Time:** 20 minutes

---

#### **Fix 3: Update story-structure-guide.md** (MEDIUM - 20 min)

**File:** `.claude/skills/devforgeai-story-creation/references/story-structure-guide.md`

**Find section:** "Technical Specification" or "Story Sections"

**Add:**

```markdown
## Technical Specification Section (v2.0 Structured YAML)

**Format Version:** 2.0 (Current) - Structured YAML format

**Since:** 2025-11-07 (RCA-006 Phase 2)

**Purpose:** Machine-readable technical specifications enabling automated validation and test generation

**Structure:**

````markdown
## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service|Worker|Configuration|Logging|Repository|API|DataModel"
      name: "[ComponentName]"
      file_path: "src/[path]/[file]"
      requirements:
        - id: "[COMP-001]"
          description: "[What must be implemented]"
          testable: true
          test_requirement: "Test: [Specific test assertion]"
          priority: "Critical|High|Medium|Low"

  business_rules:
    - id: "BR-001"
      rule: "[Business rule description]"
      test_requirement: "Test: [Validation test]"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance|Security|Scalability|Reliability"
      requirement: "[NFR description]"
      metric: "[Measurable target with numbers]"
      test_requirement: "Test: [How to verify]"
```
````

**Complete schema:** `.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md`

**Legacy v1.0 Format (Deprecated):**

Stories created before 2025-11-07 may use freeform text format. These are still supported (backward compatibility) but should be migrated to v2.0 for Phase 3 automated validation.

**Frontmatter Requirement:**

All v2.0 stories MUST have `format_version: "2.0"` in YAML frontmatter:

```yaml
---
id: STORY-XXX
format_version: "2.0"  # <-- REQUIRED for v2.0
---
```

**Validation:**

Run `validate_tech_spec.py` to verify v2.0 format:
```bash
python3 .claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py STORY-XXX.story.md
```
```

**Time:** 20 minutes

---

#### **Fix 4: Update validation-checklists.md** (MEDIUM - 15 min)

**File:** `.claude/skills/devforgeai-story-creation/references/validation-checklists.md`

**Find section:** "Technical Specification Validation" or "Story Validation Checklist"

**Add:**

```markdown
## Technical Specification v2.0 Format Validation (RCA-006 Phase 2)

**For stories created after 2025-11-07, validate v2.0 structured format:**

### Format Version Check

**Validation:**
```python
# Check frontmatter
frontmatter = extract_yaml_frontmatter(story_content)
format_version = frontmatter.get("format_version", "1.0")

if format_version == "2.0":
    # v2.0 validation required
    validate_structured_yaml(story_content)
elif format_version == "1.0":
    # Legacy format (acceptable for backward compatibility)
    log_warning("Story uses legacy v1.0 format (consider migration)")
else:
    error("Unknown format version: {format_version}")
```

**Expected:** `format_version: "2.0"` for all new stories

---

### YAML Syntax Validation

**For v2.0 stories, validate YAML syntax:**

```python
# Extract YAML block
yaml_match = re.search(r"## Technical Specification\s+```yaml\s+(.*?)\s+```",
                        story_content, re.DOTALL)

if not yaml_match:
    error("v2.0 story missing YAML block in Technical Specification")

# Parse YAML
try:
    tech_spec = yaml.safe_load(yaml_match.group(1))
except yaml.YAMLError as e:
    error(f"Invalid YAML syntax: {e}")
```

**Expected:** Valid YAML, parseable without errors

---

### Structured Content Validation

**Validate technical_specification contains required sections:**

```python
required_sections = ["format_version", "components"]
tech_spec = tech_spec.get("technical_specification", {})

for section in required_sections:
    if section not in tech_spec:
        error(f"Missing required section: {section}")
```

**Expected:**
- `format_version: "2.0"` within YAML
- `components: [...]` array with at least 1 component

---

### Component Validation

**For each component, validate required fields:**

```python
for idx, component in enumerate(tech_spec["components"]):
    # Validate type
    if "type" not in component:
        error(f"Component {idx}: Missing 'type' field")

    comp_type = component["type"]
    if comp_type not in ["Service", "Worker", "Configuration", "Logging", "Repository", "API", "DataModel"]:
        error(f"Component {idx}: Invalid type '{comp_type}'")

    # Validate required fields by type
    required_fields = get_required_fields(comp_type)
    for field in required_fields:
        if field not in component:
            error(f"Component {idx} ({comp_type}): Missing '{field}'")
```

**Expected:** All components have type, name, file_path, and type-specific required fields

---

### Test Requirement Validation

**Validate every requirement has test_requirement:**

```python
for component in tech_spec["components"]:
    if "requirements" in component:
        for req_idx, req in enumerate(component["requirements"]):
            if "test_requirement" not in req:
                warning(f"{component['name']}: Requirement {req_idx} missing test_requirement")
            elif not req["test_requirement"].startswith("Test:"):
                warning(f"{component['name']}: test_requirement should start with 'Test:'")
```

**Expected:** All requirements have `test_requirement: "Test: [assertion]"`

---

### Automated Validation with validate_tech_spec.py

**Run validation script:**

```bash
python3 .claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py {story_file}
```

**Expected exit codes:**
- 0: PASS (v2.0 format valid)
- 1: FAIL (errors found)
- 2: Invalid arguments

**Integration:** Phase 7 self-validation should run this script automatically for v2.0 stories.
```

**Time:** 15 minutes

---

#### **Fix 5: Update acceptance-criteria-patterns.md** (LOW - 10 min)

**File:** `.claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md`

**Find section:** End of file or "Integration with Tech Spec"

**Add:**

```markdown
---

## Integration with Technical Specification (v2.0)

**For stories using v2.0 structured YAML format:**

**Acceptance criteria drive tech spec components:**

**Example mapping:**

**AC:** "Given user submits registration form, When validation passes, Then account created"

**Generates components:**
```yaml
components:
  - type: "API"
    name: "UserRegistration"
    endpoint: "/api/users/register"
    method: "POST"
    requirements:
      - id: "API-001"
        description: "Must validate email format before account creation"
        test_requirement: "Test: POST with invalid email returns 400 Bad Request"
        priority: "Critical"

  - type: "Service"
    name: "UserRegistrationService"
    file_path: "src/Application/Services/UserRegistrationService.cs"
    requirements:
      - id: "SVC-001"
        description: "Must create user account when validation passes"
        test_requirement: "Test: Valid request creates user in database"
        priority: "Critical"
```

**Each Given/When/Then should map to:**
- Component requirement (what must be built)
- Test requirement (how to verify it)

**See:** `technical-specification-creation.md` for complete v2.0 generation guide
```

**Time:** 10 minutes

---

### **PHASE C: VALIDATION (30 minutes)**

#### **Step C.1: Test /create-story After Fixes**

**Procedure:**
1. Restart Claude Code Terminal (reload modified skill files)
2. Create new test story with `/create-story`
3. Verify format_version: "2.0" in frontmatter
4. Verify Technical Specification uses YAML
5. Verify components have proper structure
6. Run validate_tech_spec.py on generated story

**Test command:**
```
/create-story "Product catalog with search and filtering"
```

**Success criteria:**
- [ ] format_version: "2.0" in frontmatter
- [ ] Technical Specification has ```yaml code block
- [ ] Components array has 2+ components
- [ ] All components have test_requirement fields
- [ ] validate_tech_spec.py exits with code 0 (PASS)
- [ ] No errors or critical warnings

**Time:** 15 minutes

---

#### **Step C.2: Document Fix Results**

**Create validation report:**

```markdown
# Phase 2 Critical Gap Fix - Validation Report

**Date:** [Date]
**Status:** [PASS / FAIL]

## Test Results

**Test Story:** STORY-XXX ([title])

**Frontmatter:**
- format_version: [value]
- Status: [✅ v2.0 / ❌ v1.0 or missing]

**Technical Specification:**
- Format: [YAML / Freeform text]
- Components detected: [count]
- Business rules: [count]
- NFRs: [count]

**Validation Script:**
```
$ python3 validate_tech_spec.py STORY-XXX.story.md
[Output]
```

**Exit code:** [0 = PASS / 1 = FAIL]

## Assessment

**Gap fixed:** [YES / NO]

**If NO, additional fixes needed:**
- [List issues found]
- [Recommended actions]

**If YES, confirmation:**
- ✅ Skills generate v2.0 format correctly
- ✅ All new stories will be v2.0
- ✅ Critical gap resolved
```

**Time:** 15 minutes

---

## 📋 **Rollback Plan**

### **If Fixes Break /create-story**

**Symptoms:**
- /create-story command fails
- Story generation errors
- YAML syntax errors in generated stories
- Skill can't load reference files

**Rollback procedure (10 minutes):**

```bash
# 1. Backup modified files BEFORE fixes
cp .claude/skills/devforgeai-story-creation/SKILL.md \
   .devforgeai/backups/phase2-gap-fix/SKILL.md.backup

cp .claude/agents/story-requirements-analyst.md \
   .devforgeai/backups/phase2-gap-fix/story-requirements-analyst.md.backup

# (Repeat for other modified files)

# 2. If rollback needed, restore originals
cp .devforgeai/backups/phase2-gap-fix/SKILL.md.backup \
   .claude/skills/devforgeai-story-creation/SKILL.md

# 3. Restart terminal
# 4. Test /create-story (should work with old behavior)
```

---

## 🎯 **Success Criteria**

### **Phase B Fixes Successful If:**

- [ ] All 5 files modified without errors
- [ ] Modifications follow specification
- [ ] No YAML syntax errors introduced
- [ ] Reference file paths correct
- [ ] Instructions clear and actionable

---

### **Phase C Validation Successful If:**

- [ ] /create-story generates story with format_version: "2.0"
- [ ] Technical Specification section uses YAML code block
- [ ] Components have all required fields
- [ ] All requirements have test_requirement fields
- [ ] validate_tech_spec.py returns exit code 0 (PASS)
- [ ] No critical errors or warnings

---

## 📊 **Effort Summary**

| Phase | Tasks | Time | Risk |
|-------|-------|------|------|
| **Phase A: Verification** | Test current behavior | 30 min | Low |
| **Phase B: Fixes** | Update 5 files | 1-2 hours | Medium |
| **Phase C: Validation** | Test and document | 30 min | Low |
| **TOTAL** | 8 tasks | **2-3 hours** | Medium |

---

## 🎯 **Alternative: Minimal Fix (If Phase A Shows Partial Working)**

**If Phase A reveals:**
- Story has format_version: "2.0" ✅
- BUT tech spec is hybrid (some YAML, some freeform) ⚠️

**Then minimal fix:**
- Only update SKILL.md (Fix 1) - 15 minutes
- Skip other files
- Test again

**This might be sufficient** if reference file guidance is mostly working

---

## 📋 **File Modification Checklist**

### **Files to Modify (5 files)**

**Priority 1 (Critical - Must Do):**
- [ ] `.claude/skills/devforgeai-story-creation/SKILL.md` (+60 lines)
- [ ] `.claude/agents/story-requirements-analyst.md` (+150 lines)

**Priority 2 (High - Should Do):**
- [ ] `.claude/skills/devforgeai-story-creation/references/story-structure-guide.md` (+200 lines)
- [ ] `.claude/skills/devforgeai-story-creation/references/validation-checklists.md` (+150 lines)

**Priority 3 (Medium - Nice to Have):**
- [ ] `.claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md` (+100 lines)

**Total lines to add:** ~660 lines

---

## 🎯 **Decision Points**

### **Decision Point A: After Verification (Step A.1)**

**If /create-story generates v2.0 correctly:**
- ✅ **STOP** - Gap is theoretical, reference file is sufficient
- ✅ Document that v2.0 works
- ✅ No fixes needed

**If /create-story generates v1.0 or hybrid:**
- 🚨 **PROCEED** to Phase B fixes
- 🚨 Update skills as planned

---

### **Decision Point B: After Minimal Fix (Fix 1 only)**

**After updating just SKILL.md:**
- Test `/create-story` again
- **If v2.0 generated:** STOP (minimal fix sufficient)
- **If still v1.0:** Continue with Fixes 2-5

---

### **Decision Point C: After All Fixes**

**After all 5 files updated:**
- Test `/create-story`
- **If v2.0 and valid:** SUCCESS - Gap fixed
- **If errors:** Debug and iterate
- **If v1.0 still:** Root cause analysis needed

---

## 🎯 **Recommended Execution Strategy**

### **Conservative Approach (Test Before Fixing)**

**Step 1: Verify Gap is Real** (30 min)
```
Run: /create-story "Test feature"
Check: format_version and YAML format
```

**Step 2a: If v2.0 works**
- Document success
- No fixes needed
- Close gap as "theoretical"

**Step 2b: If v1.0 generated**
- Proceed to fixes

**Step 3: Minimal Fix First** (15 min)
- Update SKILL.md only
- Test again

**Step 4: Full Fix If Needed** (1 hour)
- Update remaining 4 files
- Test comprehensively

**Total:** 30 min to 2.5 hours (depending on verification results)

---

## 📋 **Post-Fix Validation Checklist**

### **After fixes applied, validate:**

**Functionality:**
- [ ] /create-story generates v2.0 stories
- [ ] format_version: "2.0" in all new stories
- [ ] Technical Specification uses YAML
- [ ] Components have test_requirement fields
- [ ] validate_tech_spec.py passes on new stories

**Quality:**
- [ ] No YAML syntax errors
- [ ] Components match feature description
- [ ] Test requirements are specific
- [ ] No placeholder text (TODO, TBD)

**Integration:**
- [ ] Phase 1 Step 4 parses v2.0 correctly (95%+ accuracy)
- [ ] Coverage gap detection improved
- [ ] No regressions in story creation

**Documentation:**
- [ ] Fixes documented
- [ ] Validation results recorded
- [ ] Updated framework docs (CLAUDE.md if needed)

---

## 🚨 **Critical Success Factor**

### **The Fix MUST Ensure:**

**Every new story created via `/create-story` has:**

```yaml
---
format_version: "2.0"  # <-- In frontmatter
---

## Technical Specification

```yaml  # <-- YAML code block
technical_specification:
  format_version: "2.0"
  components:
    - type: "Service"  # <-- Structured components
      name: "..."
      requirements:
        - test_requirement: "Test: ..."  # <-- Explicit test requirements
```
```

**Verification method:**
```bash
python3 validate_tech_spec.py STORY-XXX.story.md
# Exit code 0 = SUCCESS
```

---

## 📖 **Supporting Documentation**

**Created this session:**
- `PHASE2-DEVIATION-AUDIT.md` - Complete deviation analysis
- `PHASE2-AUDIT-REPORT.md` - Detailed compliance scorecard
- `PHASE2-CRITICAL-GAP-FIX-PLAN.md` - This document

**From Phase 2 agent:**
- `STRUCTURED-FORMAT-SPECIFICATION.md` - v2.0 schema reference
- `.claude/skills/devforgeai-story-creation/references/technical-specification-creation.md` - v2.0 generation guide

---

## 🎯 **Next Steps**

### **Immediate (Your Decision):**

**Option 1: Execute Fix Plan Now** (2-3 hours)
- I implement all 5 file modifications
- Test /create-story after each fix
- Validate v2.0 generation works
- **Result:** Skills generate v2.0 automatically

**Option 2: Verify First, Then Fix** (30 min to 2.5 hours)
- Test /create-story first
- IF already works: No fixes needed
- IF broken: Then implement fixes
- **Result:** Minimal work if gap is theoretical

**Option 3: Defer Until Needed** (0 hours now)
- Fix when creating first new story
- Test then, fix if needed
- **Result:** Just-in-time fixing

**My Recommendation:** **Option 2** (Verify first - might already work!)

**Want me to:**
1. ✅ Test `/create-story` right now to verify gap?
2. ✅ Implement fixes if gap confirmed?
3. ⏸️ Create the plan and let you decide when to execute?

**What's your preference?**
