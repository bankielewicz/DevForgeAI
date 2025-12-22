# Phase 2 Implementation Plan - Structured Technical Specifications

**Version:** 1.0
**Date:** 2025-11-07
**Timeline:** Weeks 2-5 (4 weeks)
**Risk Level:** 🔴 Very High (Breaking Changes)
**Prerequisites:** Phase 1 successful (GO decision)

---

## 🎯 **Phase 2 Objectives**

### **Primary Goal**

Transform Technical Specifications from freeform text to machine-readable structured format, enabling deterministic parsing and validation.

### **Success Criteria**

- [ ] Machine-readable tech spec format defined
- [ ] Story creation generates structured specs automatically
- [ ] Parsing libraries can extract components programmatically
- [ ] All new stories use structured format
- [ ] Migration path exists for old stories (v1.0 → v2.0)
- [ ] Backward compatibility maintained (dual format support)
- [ ] Zero data loss during migration

### **Why Phase 2 Before Phase 3**

**CRITICAL CORRECTION:** Original RCA placed Phase 2 (Validation) before Phase 3 (Templates).

**Problem:** implementation-validator needs parseable tech specs to validate against.

**Solution:** Reverse order - Phase 2 (Templates) provides foundation for Phase 3 (Validation).

**Dependency:**
```
Phase 2: Structured Templates
    ↓ (Provides machine-readable specs)
Phase 3: Validation Enforcement
    ↓ (Uses structured specs for validation)
Production
```

---

## 📦 **Deliverables**

### **Modified Files (8 files)**

| File | Lines | Type | Purpose |
|------|-------|------|---------|
| `technical-specification-guide.md` | +400 | Enhancement | Add structured format spec |
| `story-template.md` | +300 | Replacement | New structured tech spec section |
| `devforgeai-story-creation/SKILL.md` | +50 | Enhancement | Note format version support |
| `requirements-analyst.md` | +100 | Enhancement | Generate structured format |
| `api-designer.md` | +100 | Enhancement | Generate structured API specs |
| `story-structure-guide.md` | +200 | Enhancement | Document structured format |
| `validation-checklists.md` | +150 | Enhancement | Validate structured format |
| `acceptance-criteria-patterns.md` | +100 | Enhancement | Tech spec integration |

**Total:** ~1,400 lines added

### **New Files (3 files)**

| File | Lines | Purpose |
|------|-------|---------|
| `validate_tech_spec.py` | 200 | Parser for structured tech specs |
| `migrate_story_v1_to_v2.py` | 300 | Migration script (v1.0 → v2.0) |
| `STRUCTURED-FORMAT-SPECIFICATION.md` | 500 | Format definition and examples |

**Total:** ~1,000 lines new

### **Documentation (3 files)**

| File | Lines | Purpose |
|------|-------|---------|
| `PHASE2-IMPLEMENTATION-GUIDE.md` | ~600 | User guide for structured format |
| `PHASE2-MIGRATION-GUIDE.md` | ~400 | Step-by-step migration procedures |
| `PHASE2-TESTING-CHECKLIST.md` | ~500 | Testing strategy and validation |

**Total:** ~1,500 lines documentation

---

## 📅 **Timeline: 4 Weeks**

### **Week 2: Design & Specification (5 days)**

**Day 1: Format Design**
- Define structured tech spec format
- Design component schema (YAML/CSV)
- Create format specification document
- Review examples from 10 existing stories
- **Time:** 6 hours

**Day 2: Validation Library**
- Create `validate_tech_spec.py` script
- Implement parser for structured format
- Add validation rules
- Unit tests for parser
- **Time:** 8 hours

**Day 3: Story Template Updates**
- Update `story-template.md` with structured format
- Update `technical-specification-guide.md`
- Update `story-structure-guide.md`
- **Time:** 6 hours

**Day 4: Subagent Enhancements**
- Update `requirements-analyst.md` (generate structured format)
- Update `api-designer.md` (structured API specs)
- Update `validation-checklists.md`
- **Time:** 6 hours

**Day 5: Review & Refinement**
- Review all changes
- Test format with 3 example stories
- Refine based on feedback
- **Time:** 4 hours

**Week 2 Total:** 30 hours

---

### **Week 3: Migration Tooling (5 days)**

**Day 1: Migration Script Design**
- Design migration algorithm (v1.0 → v2.0)
- Identify parsing patterns for freeform specs
- Create migration script outline
- **Time:** 6 hours

**Day 2: Migration Script Implementation**
- Implement `migrate_story_v1_to_v2.py`
- Add AI-assisted conversion (use LLM to parse freeform)
- Add validation after migration
- **Time:** 8 hours

**Day 3: Migration Testing**
- Test with 5 pilot stories
- Validate output quality
- Fix parsing edge cases
- **Time:** 6 hours

**Day 4: Dual Format Support**
- Update `devforgeai-development` skill to detect format version
- Support both v1.0 and v2.0 formats
- Add format version to story frontmatter
- **Time:** 6 hours

**Day 5: Documentation**
- Create migration guide
- Document dual format support
- Create FAQ for users
- **Time:** 4 hours

**Week 3 Total:** 30 hours

---

### **Week 4: Pilot Migration (5 days)**

**Day 1: Select Pilot Stories**
- Review all stories in `devforgeai/specs/Stories/`
- Select 10 representative stories (simple, medium, complex)
- Create backup of pilot stories
- **Time:** 2 hours

**Day 2-3: Execute Pilot Migration**
- Run migration script on 10 stories
- Manual review of each migrated story
- Fix migration issues
- Validate with `validate_tech_spec.py`
- **Time:** 12 hours (1.2h per story)

**Day 4: Pilot Testing**
- Run `/dev` on 3 migrated stories
- Verify Step 4 works with structured format
- Test parsing accuracy
- Collect metrics
- **Time:** 6 hours

**Day 5: Pilot Review**
- Analyze pilot results
- Document lessons learned
- Make GO/NO-GO decision for full migration
- **Time:** 4 hours

**Week 4 Total:** 24 hours

---

### **Week 5: Production Migration (5 days)**

**ONLY IF PILOT SUCCESSFUL**

**Day 1: Pre-Migration Preparation**
- Backup all stories (`devforgeai/specs/Stories/*.story.md`)
- Count total stories to migrate
- Estimate effort (stories × 1.2h)
- Schedule migration window
- **Time:** 3 hours

**Day 2-3: Full Migration**
- Run migration script on ALL remaining stories
- Batch process (10 stories at a time)
- Manual review of high-priority stories
- Automated validation with `validate_tech_spec.py`
- **Time:** 12-16 hours (depends on story count)

**Day 4: Post-Migration Validation**
- Run `/dev` on 5 random migrated stories
- Verify all stories have `format_version: 2.0`
- Check for parsing errors
- Fix any issues discovered
- **Time:** 6 hours

**Day 5: Documentation & Deployment**
- Update all framework documentation
- Create "What's New in v2.0" guide
- Announce to users (if team framework)
- Monitor production usage
- **Time:** 4 hours

**Week 5 Total:** 25-30 hours

---

## 🔧 **Detailed Implementation Steps**

### **STEP 1: Design Structured Format (Week 2, Day 1)**

#### **1.1 Define Component Schema**

**Structured tech spec format using YAML:**

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "AlertingService"
      file_path: "src/OmniWatch.Service/Services/AlertingService.cs"
      interface: "IAlertingService"
      dependencies:
        - "IAlertDetectionService"
        - "IEmailService"
      requirements:
        - id: "SVC-001"
          description: "Must implement ServiceBase with OnStart/OnStop"
          testable: true
          test_requirement: "Verify OnStart transitions to Running state"
        - id: "SVC-002"
          description: "Must coordinate worker lifecycle"
          testable: true
          test_requirement: "Verify workers start when service starts"

    - type: "Worker"
      name: "AlertDetectionWorker"
      file_path: "src/OmniWatch.Service/Workers/AlertDetectionWorker.cs"
      interface: "BackgroundService"
      dependencies:
        - "IAlertDetectionService"
      requirements:
        - id: "WKR-001"
          description: "Must run continuous polling loop with cancellation"
          testable: true
          test_requirement: "Test: Worker polls at 30s intervals until cancellation"
        - id: "WKR-002"
          description: "Must handle exceptions without stopping"
          testable: true
          test_requirement: "Test: Exception in poll doesn't crash worker"

    - type: "Configuration"
      name: "appsettings.json"
      file_path: "src/OmniWatch.Service/appsettings.json"
      required_keys:
        - key: "ConnectionStrings.OmniWatchDb"
          type: "string"
          example: "Server=localhost;Database=OmniWatch;Trusted_Connection=true;"
          test_requirement: "Test: Configuration loads ConnectionStrings.OmniWatchDb"
        - key: "AlertingService.PollingIntervalSeconds"
          type: "int"
          default: 30
          test_requirement: "Test: PollingIntervalSeconds default is 30"

    - type: "Logging"
      name: "Serilog"
      file_path: "src/OmniWatch.Service/Program.cs"
      sinks:
        - name: "File"
          path: "logs/omniwatch-.txt"
          test_requirement: "Test: Log file created in logs/ directory"
        - name: "EventLog"
          source: "OmniWatch Service"
          test_requirement: "Test: Entry written to Windows Event Log"
        - name: "Database"
          table: "Logs"
          test_requirement: "Test: Log entry written to Logs table"

    - type: "Repository"
      name: "AlertRepository"
      file_path: "src/OmniWatch.Infrastructure/Repositories/AlertRepository.cs"
      interface: "IAlertRepository"
      data_access: "Dapper"
      requirements:
        - id: "REPO-001"
          description: "Must use parameterized queries (prevent SQL injection)"
          testable: true
          test_requirement: "Test: Query uses @parameters, not string concatenation"

  business_rules:
    - id: "BR-001"
      rule: "Alert severity must be Info, Warning, or Error"
      validation: "Enum validation in AlertSeverity"
      test_requirement: "Test: Invalid severity throws ArgumentException"

    - id: "BR-002"
      rule: "Alert message maximum 500 characters"
      validation: "String length check in Alert.SetMessage"
      test_requirement: "Test: 501-char message throws ValidationException"

  non_functional_requirements:
    - id: "NFR-001"
      requirement: "Service starts within 5 seconds"
      metric: "Startup time < 5s"
      test_requirement: "Test: Measure startup time, assert < 5 seconds"

    - id: "NFR-002"
      requirement: "Worker polling interval configurable"
      metric: "Default 30s, configurable 10-300s"
      test_requirement: "Test: Worker respects configured interval"
```

**Benefits:**
- ✅ Machine-readable (YAML parser)
- ✅ Every component has test requirements
- ✅ Validation rules explicit
- ✅ No ambiguity in parsing

---

#### **1.2 Create Format Specification Document**

**File:** `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md`

**Content:**
- Format version history (1.0 vs 2.0)
- Schema definition (YAML structure)
- Component types (7 types with schemas)
- Required fields per component type
- Test requirement format
- Validation rules
- 10 complete examples (CRUD, Auth, Worker, API, etc.)
- Migration guide from v1.0

**Length:** ~500 lines

---

### **STEP 2: Create Validation Library (Week 2, Day 2)**

#### **2.1 Implement Parser**

**File:** `.claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py`

```python
#!/usr/bin/env python3
"""
Technical Specification Validator for DevForgeAI v2.0

Validates structured technical specifications in story files.
"""

import yaml
import re
from typing import Dict, List, Any
from pathlib import Path

class TechSpecValidator:
    """Validates structured technical specifications."""

    REQUIRED_COMPONENT_FIELDS = {
        "Service": ["type", "name", "file_path", "requirements"],
        "Worker": ["type", "name", "file_path", "requirements"],
        "Configuration": ["type", "name", "file_path", "required_keys"],
        "Logging": ["type", "name", "file_path", "sinks"],
        "Repository": ["type", "name", "file_path", "interface", "data_access"],
        "API": ["type", "name", "endpoint", "method", "request", "response"],
        "DataModel": ["type", "name", "table", "fields"]
    }

    def __init__(self, story_file_path: str):
        self.story_file = Path(story_file_path)
        self.tech_spec = None
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        """
        Validate technical specification structure.

        Returns:
            True if valid, False otherwise
        """
        # Step 1: Extract tech spec from story file
        self.tech_spec = self._extract_tech_spec()
        if not self.tech_spec:
            self.errors.append("Technical Specification section not found")
            return False

        # Step 2: Validate format version
        if not self._validate_format_version():
            return False

        # Step 3: Validate components
        if not self._validate_components():
            return False

        # Step 4: Validate test requirements
        if not self._validate_test_requirements():
            return False

        # Step 5: Validate business rules
        self._validate_business_rules()

        # Step 6: Validate NFRs
        self._validate_nfrs()

        return len(self.errors) == 0

    def _extract_tech_spec(self) -> Dict[str, Any]:
        """Extract technical specification YAML from story file."""
        content = self.story_file.read_text()

        # Find tech spec section
        match = re.search(
            r"## Technical Specification\s+```yaml\s+(.*?)\s+```",
            content,
            re.DOTALL
        )

        if not match:
            return None

        # Parse YAML
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in tech spec: {e}")
            return None

    def _validate_format_version(self) -> bool:
        """Validate format version is 2.0."""
        version = self.tech_spec.get("technical_specification", {}).get("format_version")

        if not version:
            self.errors.append("Missing format_version field")
            return False

        if version != "2.0":
            self.warnings.append(f"Format version {version} (expected 2.0)")

        return True

    def _validate_components(self) -> bool:
        """Validate all components have required fields."""
        components = self.tech_spec.get("technical_specification", {}).get("components", [])

        if not components:
            self.errors.append("No components defined")
            return False

        for idx, component in enumerate(components):
            comp_type = component.get("type")

            if not comp_type:
                self.errors.append(f"Component {idx}: Missing 'type' field")
                continue

            if comp_type not in self.REQUIRED_COMPONENT_FIELDS:
                self.warnings.append(f"Component {idx}: Unknown type '{comp_type}'")
                continue

            # Validate required fields for this component type
            required_fields = self.REQUIRED_COMPONENT_FIELDS[comp_type]
            for field in required_fields:
                if field not in component:
                    self.errors.append(
                        f"Component {idx} ({comp_type}): Missing required field '{field}'"
                    )

        return len(self.errors) == 0

    def _validate_test_requirements(self) -> bool:
        """Validate all components have test requirements."""
        components = self.tech_spec.get("technical_specification", {}).get("components", [])

        for component in components:
            comp_name = component.get("name", "Unknown")

            # Check if component has test requirements
            if "requirements" in component:
                for req in component["requirements"]:
                    if "test_requirement" not in req:
                        self.warnings.append(
                            f"{comp_name}: Requirement missing 'test_requirement' field"
                        )

            elif "required_keys" in component:
                for key in component["required_keys"]:
                    if "test_requirement" not in key:
                        self.warnings.append(
                            f"{comp_name}: Key missing 'test_requirement' field"
                        )

            elif "sinks" in component:
                for sink in component["sinks"]:
                    if "test_requirement" not in sink:
                        self.warnings.append(
                            f"{comp_name}: Sink missing 'test_requirement' field"
                        )

        return True

    def _validate_business_rules(self) -> bool:
        """Validate business rules structure."""
        rules = self.tech_spec.get("technical_specification", {}).get("business_rules", [])

        for idx, rule in enumerate(rules):
            if "id" not in rule:
                self.warnings.append(f"Business rule {idx}: Missing 'id' field")
            if "test_requirement" not in rule:
                self.warnings.append(f"Business rule {idx}: Missing 'test_requirement'")

        return True

    def _validate_nfrs(self) -> bool:
        """Validate non-functional requirements."""
        nfrs = self.tech_spec.get("technical_specification", {}).get(
            "non_functional_requirements", []
        )

        for idx, nfr in enumerate(nfrs):
            if "metric" not in nfr:
                self.warnings.append(f"NFR {idx}: Missing 'metric' field")
            if "test_requirement" not in nfr:
                self.warnings.append(f"NFR {idx}: Missing 'test_requirement'")

        return True

    def get_report(self) -> str:
        """Generate validation report."""
        report = []

        if self.errors:
            report.append("❌ VALIDATION FAILED\n")
            report.append("Errors:")
            for error in self.errors:
                report.append(f"  - {error}")
        else:
            report.append("✅ VALIDATION PASSED\n")

        if self.warnings:
            report.append("\nWarnings:")
            for warning in self.warnings:
                report.append(f"  - {warning}")

        return "\n".join(report)


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: validate_tech_spec.py <story-file.md>")
        sys.exit(1)

    validator = TechSpecValidator(sys.argv[1])
    is_valid = validator.validate()

    print(validator.get_report())

    sys.exit(0 if is_valid else 1)


if __name__ == "__main__":
    main()
```

**Length:** ~200 lines

**Features:**
- YAML parsing
- Component validation
- Test requirement validation
- Error/warning reporting
- CLI interface

---

### **STEP 3: Update Story Template (Week 2, Day 3)**

#### **3.1 Replace Tech Spec Section in story-template.md**

**File:** `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Old format (v1.0 - Freeform):**
```markdown
## Technical Specification

### File Structure
src/
└── Workers/
    └── AlertDetectionWorker.cs

### Service Implementation Pattern
AlertDetectionWorker will poll the database every 30 seconds...

### Configuration
appsettings.json should contain ConnectionStrings.OmniWatchDb...
```

**New format (v2.0 - Structured):**
```markdown
## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Worker"
      name: "AlertDetectionWorker"
      file_path: "src/OmniWatch.Service/Workers/AlertDetectionWorker.cs"
      interface: "BackgroundService"
      dependencies:
        - "IAlertDetectionService"
      requirements:
        - id: "WKR-001"
          description: "Must run continuous polling loop with cancellation"
          testable: true
          test_requirement: "Test: Worker polls at 30s intervals until cancellation"
          priority: "Critical"
        - id: "WKR-002"
          description: "Must handle exceptions without stopping"
          testable: true
          test_requirement: "Test: Exception in poll doesn't crash worker"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Alert severity must be Info, Warning, or Error"
      validation: "Enum validation in AlertSeverity"
      test_requirement: "Test: Invalid severity throws ArgumentException"

  non_functional_requirements:
    - id: "NFR-001"
      requirement: "Worker polling interval configurable"
      metric: "Default 30s, range 10-300s"
      test_requirement: "Test: Worker respects configured interval"
```
```

**Changes:**
- YAML code block replaces freeform text
- Every component has explicit test requirements
- IDs for traceability
- Structured schema (parseable)

---

### **STEP 4: Create Migration Script (Week 3, Day 1-2)**

#### **4.1 Migration Algorithm**

**File:** `.claude/skills/devforgeai-story-creation/scripts/migrate_story_v1_to_v2.py`

**High-level algorithm:**

```python
def migrate_story(story_file: str) -> bool:
    """
    Migrate story from v1.0 (freeform) to v2.0 (structured) format.

    Process:
    1. Read story file
    2. Extract freeform tech spec
    3. Use LLM to parse and structure
    4. Generate YAML format
    5. Replace tech spec section
    6. Update format_version in frontmatter
    7. Validate with validate_tech_spec.py
    8. Write updated story
    """

    # Step 1: Read story
    story_content = read_file(story_file)

    # Step 2: Extract freeform tech spec
    tech_spec_text = extract_tech_spec_section(story_content)

    if not tech_spec_text:
        print(f"⚠️ {story_file}: No tech spec section found")
        return False

    # Step 3: Parse with LLM (AI-assisted conversion)
    structured_spec = convert_to_structured_format(tech_spec_text)

    # Step 4: Generate YAML
    yaml_spec = generate_yaml(structured_spec)

    # Step 5: Replace section
    updated_content = replace_tech_spec_section(story_content, yaml_spec)

    # Step 6: Update frontmatter
    updated_content = update_format_version(updated_content, "2.0")

    # Step 7: Validate
    write_temp_file(updated_content)
    if not validate_with_script(temp_file):
        print(f"❌ {story_file}: Validation failed after migration")
        return False

    # Step 8: Write updated story
    write_file(story_file, updated_content)

    print(f"✅ {story_file}: Migrated to v2.0")
    return True


def convert_to_structured_format(freeform_text: str) -> Dict:
    """
    Use LLM to convert freeform tech spec to structured format.

    This is AI-assisted conversion using Claude to parse natural language.
    """
    prompt = f"""
    Convert this freeform technical specification to structured YAML format.

    Freeform text:
    {freeform_text}

    Extract:
    - Components (type, name, file_path, requirements)
    - Business rules (id, rule, validation, test_requirement)
    - NFRs (id, requirement, metric, test_requirement)

    Return YAML matching the v2.0 schema.
    """

    # Call Claude API or use Task tool
    structured_data = call_llm(prompt)

    return yaml.safe_load(structured_data)
```

**Length:** ~300 lines

**Features:**
- AI-assisted parsing (uses LLM to understand freeform text)
- YAML generation
- Automatic validation
- Backup before migration
- Rollback on validation failure

---

### **STEP 5: Dual Format Support (Week 3, Day 4)**

#### **5.1 Update devforgeai-development Skill**

**File:** `.claude/skills/devforgeai-development/SKILL.md` or phase workflow

**Add format detection in Phase 1 Step 4:**

```python
# Step 4.1: Extract Technical Specification Components

# Detect format version
story_frontmatter = extract_yaml_frontmatter(story_content)
format_version = story_frontmatter.get("format_version", "1.0")

if format_version == "2.0":
    # Use structured parser
    tech_spec = parse_structured_tech_spec_yaml(story_content)
    components = tech_spec["technical_specification"]["components"]

elif format_version == "1.0":
    # Use legacy parser (freeform text extraction)
    tech_spec = parse_freeform_tech_spec(story_content)
    components = extract_components_from_freeform(tech_spec)

else:
    raise ValidationError(f"Unknown format version: {format_version}")

# Continue with Step 4.2 (coverage analysis)
```

**Benefits:**
- Supports both formats
- No breaking changes
- Gradual migration possible

---

### **STEP 6: Pilot Migration (Week 4)**

#### **6.1 Select 10 Pilot Stories**

**Criteria:**
- 3 simple stories (CRUD, 2-3 components)
- 4 medium stories (Services, 4-6 components)
- 3 complex stories (Workers, APIs, 8+ components)

**Backup:**
```bash
mkdir -p devforgeai/backups/phase2-pilot/
cp devforgeai/specs/Stories/STORY-*.story.md devforgeai/backups/phase2-pilot/
```

---

#### **6.2 Execute Migration**

**For each pilot story:**

```bash
# Migrate
python .claude/skills/devforgeai-story-creation/scripts/migrate_story_v1_to_v2.py \
  devforgeai/specs/Stories/STORY-001.story.md

# Validate
python .claude/skills/devforgeai-story-creation/scripts/validate_tech_spec.py \
  devforgeai/specs/Stories/STORY-001.story.md

# Manual review
# Open story file, verify quality

# Test with /dev
/dev STORY-001
# Verify Step 4 works with structured format
```

**Success criteria per story:**
- [ ] Migration completes without errors
- [ ] Validation passes
- [ ] Manual review confirms quality
- [ ] `/dev` works with migrated story
- [ ] Step 4 parses structured format correctly

---

#### **6.3 Pilot Review & GO/NO-GO**

**After 10 pilot stories migrated:**

**Calculate metrics:**
- Migration success rate: __ / 10 (target: 100%)
- Validation pass rate: __ / 10 (target: 100%)
- Manual review quality: __ / 5 average (target: ≥4)
- /dev success rate: __ / 10 (target: 100%)
- Parsing accuracy: __ % (target: ≥95%)

**GO Decision Criteria:**
- ✅ Migration success rate 100%
- ✅ Validation pass rate ≥90%
- ✅ Manual review quality ≥4/5
- ✅ /dev success rate 100%
- ✅ Parsing accuracy ≥95%
- ✅ No critical bugs

**If GO:** Proceed to Week 5 (full migration)

**If NO-GO:** Fix issues, re-test pilot, or rollback

---

### **STEP 7: Full Migration (Week 5)**

#### **7.1 Count & Estimate**

```bash
# Count stories to migrate
STORY_COUNT=$(find .ai_docs/Stories -name "*.story.md" | wc -l)
echo "Stories to migrate: $STORY_COUNT"

# Estimate effort (1.2 hours per story)
HOURS=$(echo "$STORY_COUNT * 1.2" | bc)
echo "Estimated effort: $HOURS hours"
```

---

#### **7.2 Batch Migration**

**Process in batches of 10:**

```bash
# Batch 1 (stories 1-10)
for story in STORY-001 STORY-002 ... STORY-010; do
  python migrate_story_v1_to_v2.py devforgeai/specs/Stories/$story.story.md
  python validate_tech_spec.py devforgeai/specs/Stories/$story.story.md
done

# Review batch
# Manual spot-check 2-3 stories

# Batch 2 (stories 11-20)
# Repeat...
```

**Safety:**
- Backup before each batch
- Validate after each migration
- Manual review 20% of batch
- HALT on validation failures

---

#### **7.3 Post-Migration Validation**

**After all stories migrated:**

```bash
# Validate ALL stories
for story in devforgeai/specs/Stories/*.story.md; do
  python validate_tech_spec.py "$story" || echo "FAILED: $story"
done

# Check format versions
grep -r "format_version:" devforgeai/specs/Stories/
# Expected: All should be "2.0"

# Test with /dev
/dev STORY-001  # Simple
/dev STORY-042  # Complex
/dev STORY-100  # Recent

# Verify Step 4 works on all
```

**Success criteria:**
- [ ] 100% stories migrated
- [ ] 100% validation passing
- [ ] All format_version = "2.0"
- [ ] /dev works on migrated stories
- [ ] Step 4 parses all stories correctly

---

## 🚨 **Breaking Changes & Migration**

### **Breaking Change 1: Story Format**

**What breaks:**
- v1.0 stories incompatible with Phase 3 validation
- Freeform tech spec cannot be parsed deterministically
- Custom scripts parsing tech spec may fail

**Mitigation:**
- Dual format support (v1.0 + v2.0)
- Migration script provided
- Gradual migration path

---

### **Breaking Change 2: Story Creation**

**What changes:**
- `/create-story` now generates YAML tech specs
- `requirements-analyst` outputs structured format
- `api-designer` outputs structured API specs

**Mitigation:**
- User doesn't write YAML manually (auto-generated)
- Examples provided in all documentation
- FAQ for common questions

---

### **Breaking Change 3: devforgeai-development Skill**

**What changes:**
- Step 4 now parses YAML (not freeform text)
- Parser expects structured components
- Coverage analysis uses schema fields

**Mitigation:**
- Dual format support (detects version, uses appropriate parser)
- Backward compatible with v1.0 stories
- Gradual migration (new stories v2.0, old stories v1.0)

---

## 🔄 **Rollback Strategy**

### **Rollback Scope Options**

**Option A: Rollback Entire Phase 2**
- Restore all files from Week 2 Day 1 backups
- Delete migration scripts
- Revert story template changes
- **Time:** 30 minutes
- **Data loss:** All migrations lost

**Option B: Rollback Pilot Only**
- Restore 10 pilot stories from backup
- Keep format and scripts (for future retry)
- **Time:** 15 minutes
- **Data loss:** Pilot migrations only

**Option C: Rollback Full Migration**
- Restore all stories from Week 5 Day 1 backup
- Keep format and scripts
- **Time:** 30-60 minutes
- **Data loss:** All migrations (30+ stories)

**Recommendation:** Test rollback procedures BEFORE full migration

---

## 📊 **Success Metrics**

### **Phase 2 Success Criteria**

**Technical:**
- [ ] Structured format specification complete (v2.0 schema)
- [ ] Validation library functional (validate_tech_spec.py)
- [ ] Migration script reliable (≥95% success rate)
- [ ] Dual format support works (v1.0 + v2.0)
- [ ] Story creation generates structured format
- [ ] 100% stories migrated (or dual format active)

**Quality:**
- [ ] Parsing accuracy ≥95%
- [ ] Validation detects all format errors
- [ ] No data loss during migration
- [ ] Manual review quality ≥4/5

**User Experience:**
- [ ] Story creation time <10 min (not slower)
- [ ] Migration per story <1.5 hours
- [ ] User satisfaction ≥80%
- [ ] Documentation clear (FAQ, examples)

---

## 🎯 **Decision Point: End of Week 5**

### **GO Criteria (Proceed to Phase 3)**

**GREEN LIGHT if ALL met:**
- ✅ All technical criteria met
- ✅ 100% stories migrated successfully
- ✅ Validation accuracy ≥95%
- ✅ User satisfaction ≥80%
- ✅ No critical bugs
- ✅ Performance acceptable

**Action:** Create Phase 3 implementation plan

---

### **ITERATE Criteria**

**YELLOW LIGHT if SOME missed:**
- ⚠️ Validation accuracy 85-95%
- ⚠️ User satisfaction 60-80%
- ⚠️ Minor migration issues
- ⚠️ Performance slower than expected

**Action:** Spend Week 6 optimizing, re-test

---

### **NO-GO Criteria**

**RED LIGHT if ANY critical:**
- 🛑 Validation accuracy <85%
- 🛑 Migration success rate <90%
- 🛑 Data loss occurred
- 🛑 User rejection
- 🛑 Critical bugs

**Action:** Rollback, document issues, reassess

---

## 📚 **References**

**Format specification:**
- `devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` (NEW - Week 2)

**Migration:**
- `devforgeai/specs/enhancements/PHASE2-MIGRATION-GUIDE.md` (NEW - Week 3)

**Testing:**
- `devforgeai/specs/enhancements/PHASE2-TESTING-CHECKLIST.md` (NEW - Week 4)

**Backups:**
- `devforgeai/backups/phase2-pilot/` (10 pilot stories)
- `devforgeai/backups/phase2-full/` (All stories before full migration)

---

**Phase 2 provides machine-readable foundation for Phase 3 validation enforcement.**
