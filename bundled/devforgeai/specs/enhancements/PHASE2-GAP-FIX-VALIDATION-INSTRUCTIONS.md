# Phase 2 Critical Gap Fix - Validation Instructions

**Date:** 2025-11-08
**Status:** ✅ All fixes implemented, ready for validation
**Next:** User testing required

---

## ✅ **What Was Fixed**

### **5 Files Updated (+326 lines)**

| File | Lines Added | Purpose |
|------|-------------|---------|
| devforgeai-story-creation/SKILL.md | +24 | Declares v2.0 as default format |
| story-requirements-analyst.md | +75 | Structured component output guide |
| story-structure-guide.md | +75 | Documents v2.0 YAML structure |
| validation-checklists.md | +114 | v2.0 validation procedures |
| acceptance-criteria-patterns.md | +38 | AC to v2.0 component mapping |

**Backup location:** `devforgeai/backups/phase2-gap-fix/`

---

## 🧪 **Validation Procedure (YOU MUST RUN)**

### **Step 1: Restart Claude Code Terminal**

**Why:** Skills are cached on terminal startup. Modifications won't take effect until restart.

**Action:**
```
Close current terminal session
Reopen Claude Code Terminal
```

**Expected:** Terminal loads updated SKILL.md and reference files

---

### **Step 2: Create Test Story**

**Run this command in terminal:**
```
/create-story "User login with email and password authentication"
```

**Expected behavior:**
- devforgeai-story-creation skill activates
- Skill loads updated SKILL.md (Phase 3 mentions v2.0)
- Skill loads technical-specification-creation.md (has v2.0 instructions)
- story-requirements-analyst generates structured component info
- Skill assembles into v2.0 YAML format
- Story file created in devforgeai/specs/Stories/

**Duration:** 5-10 minutes

---

### **Step 3: Check Generated Story Format**

**Find the generated story:**
```bash
ls -lt devforgeai/specs/Stories/ | head -5
```

**Expected:** Newest file is STORY-XXX-user-login-with-email-and-password-authentication.story.md

**Check frontmatter:**
```bash
head -15 devforgeai/specs/Stories/STORY-XXX-*.story.md
```

**Critical check:**
```yaml
---
id: STORY-XXX
format_version: "2.0"  # <-- MUST BE PRESENT
---
```

**✅ PASS if:** format_version: "2.0" exists
**❌ FAIL if:** format_version missing or "1.0"

---

### **Step 4: Check Technical Specification Format**

**Extract tech spec section:**
```bash
grep -A 50 "## Technical Specification" devforgeai/specs/Stories/STORY-XXX-*.story.md
```

**Expected structure:**
```markdown
## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "API"
      name: "UserLogin"
      endpoint: "/api/auth/login"
      method: "POST"
      requirements:
        - id: "API-001"
          description: "Must validate email and password"
          testable: true
          test_requirement: "Test: POST with valid credentials returns 200 OK with JWT token"
          priority: "Critical"

    - type: "Service"
      name: "AuthenticationService"
      file_path: "src/Application/Services/AuthenticationService.cs"
      requirements:
        - id: "SVC-001"
          description: "Must verify password hash matches stored hash"
          testable: true
          test_requirement: "Test: Correct password returns success, incorrect returns error"
          priority: "Critical"
```
```

**Critical checks:**
- ✅ Has ```yaml code block (not freeform text)
- ✅ Has format_version: "2.0" inside YAML
- ✅ Has components array
- ✅ Components have type, name, file_path
- ✅ Requirements have test_requirement fields

**✅ PASS if:** All checks pass
**❌ FAIL if:** Freeform text OR missing fields

---

### **Step 5: Run Automated Validation**

**Validate with script:**
```bash
python3 .claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py \
  devforgeai/specs/Stories/STORY-XXX-user-login-with-email-and-password-authentication.story.md
```

**Expected output:**
```
✅ VALIDATION PASSED

Summary:
  Components: 2-4
  Business Rules: 1-3
  NFRs: 4-8
  Errors: 0
  Warnings: 0-2 (warnings acceptable)
```

**Exit code check:**
```bash
echo $?
# Expected: 0 (success)
```

**✅ PASS if:** Exit code 0, no critical errors
**❌ FAIL if:** Exit code 1, has errors

---

## 📊 **Validation Results Matrix**

### **Fill out after testing:**

| Check | Expected | Actual | Status |
|-------|----------|--------|--------|
| **Terminal restarted** | Yes | ___ | ___ |
| **Story created** | Yes | ___ | ___ |
| **format_version in frontmatter** | "2.0" | ___ | ___ |
| **Tech spec format** | YAML | ___ | ___ |
| **Components present** | 2+ | ___ | ___ |
| **test_requirement fields** | All | ___ | ___ |
| **validate_tech_spec.py** | Exit 0 | ___ | ___ |
| **No errors** | 0 errors | ___ | ___ |

**Overall result:** ✅ PASS / ❌ FAIL

---

## ✅ **If All Checks PASS**

**Success! Gap is fixed.**

**What this means:**
- ✅ Skills now generate v2.0 format automatically
- ✅ All new stories will use structured YAML
- ✅ Phase 1 Step 4 will have 95%+ accuracy (not 85%)
- ✅ Phase 3 ready (if you decide to proceed)
- ✅ Consistent framework

**Next actions:**
- Document success
- Update CLAUDE.md if needed
- Use `/create-story` normally going forward

---

## ❌ **If Checks FAIL**

**Failure scenarios and fixes:**

### **Scenario 1: format_version Missing**

**Symptom:** Frontmatter doesn't have format_version field

**Root cause:** SKILL.md not loaded or template not used correctly

**Fix:**
- Verify terminal restarted
- Check SKILL.md Phase 3 section has v2.0 text
- Check story-template.md has format_version: "2.0" in frontmatter example

**Action:** Add format_version manually to template, retry

---

### **Scenario 2: Tech Spec is Freeform Text**

**Symptom:** Technical Specification section has markdown text, not YAML

**Root cause:** Skill not loading technical-specification-creation.md reference

**Fix:**
- Check SKILL.md Phase 3 says "Load technical-specification-creation.md"
- Verify technical-specification-creation.md exists and has v2.0 instructions
- Check story-requirements-analyst outputs component info

**Action:** Update story-file-creation.md to assemble YAML (Phase 5 logic)

---

### **Scenario 3: YAML Exists But Invalid**

**Symptom:** YAML code block present but validate_tech_spec.py fails

**Root cause:** YAML syntax errors or missing fields

**Fix:**
- Check YAML syntax (indentation, colons, quotes)
- Verify components have required fields
- Run validator to see specific errors

**Action:** Fix YAML syntax issues manually

---

### **Scenario 4: Hybrid Format (Some YAML, Some Freeform)**

**Symptom:** YAML block present but incomplete, plus freeform text

**Root cause:** Template has both formats, skill not removing v1.0 section

**Fix:**
- Update story-template.md to ONLY have v2.0 section
- Remove v1.0 freeform text examples from template
- Regenerate story

**Action:** Clean up template

---

## 🔄 **Rollback Procedure (If Fixes Break Things)**

**If /create-story fails or generates broken stories:**

```bash
# Restore original files (10 minutes)
cp devforgeai/backups/phase2-gap-fix/SKILL.md.backup \
   .claude/skills/devforgeai-story-creation/SKILL.md

cp devforgeai/backups/phase2-gap-fix/story-requirements-analyst.md.backup \
   .claude/agents/story-requirements-analyst.md

cp devforgeai/backups/phase2-gap-fix/story-structure-guide.md.backup \
   .claude/skills/devforgeai-story-creation/references/story-structure-guide.md

cp devforgeai/backups/phase2-gap-fix/validation-checklists.md.backup \
   .claude/skills/devforgeai-story-creation/references/validation-checklists.md

cp devforgeai/backups/phase2-gap-fix/acceptance-criteria-patterns.md.backup \
   .claude/skills/devforgeai-story-creation/references/acceptance-criteria-patterns.md

# Restart terminal
# Test /create-story (should work with old behavior)

# Document rollback reason
echo "Rollback reason: [ISSUE]" > devforgeai/backups/phase2-gap-fix/ROLLBACK-REASON.txt
```

---

## 📋 **Reporting Template**

**After validation, fill this out and provide to me:**

```markdown
# Validation Results

**Date:** [Date]
**Terminal restarted:** [Yes/No]

## Test Story Created

**Story ID:** STORY-XXX
**Filename:** [full filename]

## Format Checks

**Frontmatter:**
- format_version present: [Yes/No]
- format_version value: ["2.0" / "1.0" / missing]
- Status: [✅ PASS / ❌ FAIL]

**Technical Specification:**
- Format: [YAML code block / Freeform text / Hybrid]
- YAML parseable: [Yes/No / N/A]
- Components found: [count]
- test_requirement fields: [All present / Some missing / None]
- Status: [✅ PASS / ❌ FAIL]

## Validation Script

**Command:**
```
python3 validate_tech_spec.py STORY-XXX.story.md
```

**Output:**
[Paste output here]

**Exit code:** [0 / 1 / 2]
**Status:** [✅ PASS / ❌ FAIL]

## Overall Assessment

**Gap fixed:** [YES / NO]

**If NO:**
- Issue: [Describe problem]
- Scenario: [Which failure scenario from above]

**If YES:**
- ✅ Skills generate v2.0 correctly
- ✅ Critical gap resolved
```

---

## 🎯 **What Happens After Validation**

### **If Validation PASSES:**

**I will:**
1. Document success in PHASE2-GAP-FIX-COMPLETE.md
2. Update CLAUDE.md to note v2.0 format (if needed)
3. Create summary report
4. Mark Phase 2 gap as RESOLVED

**You can:**
- Use `/create-story` normally (generates v2.0 automatically)
- Trust that all new stories will be v2.0
- Proceed with Phase 3 if desired (v2.0 available)

---

### **If Validation FAILS:**

**I will:**
1. Analyze failure scenario
2. Implement additional fixes
3. Provide updated validation instructions
4. Iterate until working

**We can:**
- Debug root cause together
- Apply targeted fixes
- Re-test until successful
- Rollback if necessary

---

## 🚀 **Ready for Your Testing**

**What you need to do NOW:**

1. ✅ **Restart terminal** (critical - loads updated skills)
2. ✅ **Run:** `/create-story "User login with email and password authentication"`
3. ✅ **Check:** frontmatter for format_version
4. ✅ **Check:** Tech spec for YAML format
5. ✅ **Run:** validate_tech_spec.py on generated story
6. ✅ **Report:** Results using template above

**I'm waiting for your validation results to proceed with Phase C documentation!**

---

**All fixes implemented. Ball is in your court for testing.**
