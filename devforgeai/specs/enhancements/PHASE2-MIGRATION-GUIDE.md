# Phase 2 Migration Guide - v1.0 to v2.0 Story Format

**Version:** 1.0
**Date:** 2025-11-07
**Audience:** Framework Users and Maintainers
**Duration:** Weeks 3-5 (3 weeks for complete migration)

---

## Migration Overview

**What's Being Migrated:**
- Technical Specification sections in all story files
- Format: v1.0 (freeform markdown) → v2.0 (structured YAML)

**Why Migrate:**
- **Improved accuracy:** 85% → 95%+ component detection
- **Better test generation:** Direct mapping from requirements
- **Enables Phase 3:** Automated implementation validation
- **Zero ambiguity:** Machine-parseable schema

**Who Should Migrate:**
- ✅ Projects planning to use Phase 3 (automated validation)
- ✅ Projects with >10 stories (automation pays off)
- ✅ Teams wanting better coverage gap detection

**Who Can Skip:**
- ✅ Projects with <5 stories (manual migration easier)
- ✅ Projects satisfied with v1.0 accuracy (85%)
- ✅ Projects not planning Phase 3

---

## Migration Paths

### Path A: Automated Migration (Recommended)

**Best for:** Projects with 10+ stories

**Timeline:** Week 3-5 (3 weeks)

**Process:**
1. **Week 3:** Enhance migration script with AI-assisted parsing
2. **Week 4:** Pilot migration (10 stories), manual review
3. **Week 5:** Full migration (all stories), validation

**Accuracy:** 95%+ with AI-assisted parsing

**Effort:** ~30 min per story (mostly automated)

---

### Path B: Manual Migration

**Best for:** Projects with <5 stories, or specific high-value stories

**Timeline:** 1-2 hours per story

**Process:**
1. Read current tech spec (freeform)
2. Identify components manually
3. Write structured YAML
4. Validate
5. Test with /dev

**Accuracy:** 100% (human review)

**Effort:** 1-2 hours per story

---

### Path C: Gradual Migration

**Best for:** Large projects (50+ stories), risk-averse teams

**Timeline:** Ongoing over several sprints

**Process:**
1. New stories: v2.0 format (automatic)
2. Modified stories: Migrate when edited
3. Old stories: Keep v1.0 until touched

**Accuracy:** Mixed (v2.0 for new/modified, v1.0 for legacy)

**Effort:** Minimal (opportunistic)

---

## Week 3: Migration Tooling Enhancement

### Current State (Basic Migration)

**migrate_story_v1_to_v2.py capabilities:**
- ✅ Detects v2.0 stories (skips if already migrated)
- ✅ Creates backups automatically
- ✅ Extracts freeform tech spec section
- ✅ Basic pattern matching (workers, config, logging)
- ❌ Limited accuracy (~60-70% component detection)
- ❌ Misses complex patterns
- ❌ Generic test requirements

**Limitation:** Pattern matching cannot understand natural language like "The worker should coordinate with the service to..."

---

### Enhanced Migration (AI-Assisted)

**Enhancement needed (Week 3 Day 1-2):**

Add AI/LLM integration to `_convert_to_structured_format()` method:

```python
def _convert_to_structured_format_ai(self, freeform_text: str) -> Dict[str, Any]:
    """
    Use LLM to intelligently parse freeform tech spec.

    This replaces simple pattern matching with AI understanding.
    """
    prompt = f"""
    Convert this freeform technical specification to DevForgeAI v2.0 structured YAML format.

    Freeform tech spec:
    ```
    {freeform_text}
    ```

    Extract and structure:
    1. Components (identify type: Service, Worker, Configuration, Logging, Repository, API, DataModel)
    2. For each component: name, file_path, dependencies, requirements
    3. For each requirement: id, description, testable flag, test_requirement, priority
    4. Business rules with test requirements
    5. NFRs with measurable metrics and test requirements

    Return ONLY valid YAML matching the v2.0 schema.
    See schema: {STRUCTURED_FORMAT_SPECIFICATION_CONTENT}

    YAML output:
    """

    # Call Claude API or use Task subagent
    response = call_claude_api(prompt, model="haiku")

    # Parse and validate response
    structured = yaml.safe_load(response)

    return structured
```

**Benefits:**
- 95%+ accuracy (AI understands natural language)
- Contextual component identification
- Meaningful test requirements
- Handles edge cases

**Implementation effort:** 8 hours (Week 3 Day 2)

---

## Week 4: Pilot Migration (10 Stories)

### Story Selection

**Selection criteria:**

**Simple (3 stories):**
- 2-3 components
- Basic CRUD
- No complex business rules
- Example: User registration form

**Medium (4 stories):**
- 4-6 components
- Services + workers or API + repository
- Some business rules
- Example: Background task with API

**Complex (3 stories):**
- 8+ components
- Full stack (API, Service, Worker, Repository, Configuration, Logging, DataModel)
- Multiple business rules
- Example: Complete feature (like STORY-007, STORY-018)

**Actual selection (Week 4 Day 1):**
```bash
# List all stories
ls -lh devforgeai/specs/Stories/*.story.md

# Review each, categorize by complexity
# Select 10 representative stories
```

---

### Pilot Migration Procedure

**For each pilot story:**

**Pre-flight:**
```bash
# 1. Backup
cp devforgeai/specs/Stories/STORY-XXX.md devforgeai/backups/phase2-pilot/

# 2. Test baseline (v1.0)
/dev STORY-XXX
# Note: Time, component count, gaps detected
```

**Migration:**
```bash
# 3. Migrate with validation
python .claude/skills/devforgeai-story-creation/scripts/migrate_story_v1_to_v2.py \
  devforgeai/specs/Stories/STORY-XXX.md \
  --validate

# Expected output:
# ✅ STORY-XXX.md: Migrated to v2.0
# ✅ VALIDATION PASSED
```

**Post-migration:**
```bash
# 4. Manual review
cat devforgeai/specs/Stories/STORY-XXX.md
# Check: YAML quality, component accuracy, test requirements

# 5. Rate quality (1-5)
echo "Quality: 4/5" >> devforgeai/pilot-results.txt

# 6. Test with /dev
/dev STORY-XXX
# Note: Time, component count (should be ≥ v1.0), gaps detected

# 7. Compare v1.0 vs v2.0
# Components detected: v1.0 [X] vs v2.0 [Y] (Y should be ≥ X)
# Accuracy: Did v2.0 detect components v1.0 missed?
```

**Pilot metrics (per story):**
- Migration success: Yes/No
- Validation pass: Yes/No
- Component count: v1.0 [X] → v2.0 [Y]
- Quality score: 1-5
- /dev success: Yes/No
- Notes: Any issues

---

### Pilot Review (Week 4 Day 5)

**Calculate aggregate metrics:**

```bash
# Migration success rate
migrated=$(grep "✅ PASS" devforgeai/pilot-results.txt | wc -l)
total=10
success_rate=$((migrated * 100 / total))
echo "Migration success rate: $success_rate%"

# Average quality score
avg_quality=$(grep "Quality:" devforgeai/pilot-results.txt | awk '{sum+=$2; count++} END {print sum/count}')
echo "Average quality: $avg_quality/5"

# Component detection improvement
# (Manual calculation from notes)
```

**GO/NO-GO decision:**

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Migration success | 100% | ___% | ✅/⚠️/❌ |
| Validation pass | ≥90% | ___% | ✅/⚠️/❌ |
| /dev success | 100% | ___% | ✅/⚠️/❌ |
| Average quality | ≥4/5 | ___/5 | ✅/⚠️/❌ |
| Component accuracy | ≥95% | ___% | ✅/⚠️/❌ |

**Decision:**
- ✅ **GO:** All metrics met → Proceed to full migration (Week 5)
- ⚠️ **ITERATE:** Some metrics missed → Fix issues, re-pilot
- ❌ **NO-GO:** Critical failures → Rollback, reassess

---

## Week 5: Full Migration (If GO)

### Pre-Migration Preparation (Day 1)

**Step 1: Complete backup**
```bash
mkdir -p devforgeai/backups/phase2-full
cp devforgeai/specs/Stories/*.md devforgeai/backups/phase2-full/

# Verify backup
backup_count=$(ls devforgeai/backups/phase2-full/*.md | wc -l)
story_count=$(ls devforgeai/specs/Stories/*.md | wc -l)
echo "Backed up $backup_count of $story_count stories"
# Should match
```

**Step 2: Count and categorize**
```bash
# Count total stories
total_stories=$(find .ai_docs/Stories -name "*.story.md" | wc -l)
echo "Total stories to migrate: $total_stories"

# Subtract pilot stories (already done)
pilot_count=10
remaining=$((total_stories - pilot_count))
echo "Remaining to migrate: $remaining"

# Estimate effort
hours=$(echo "$remaining * 0.5" | bc)  # 30 min per story
echo "Estimated: $hours hours (~$((hours / 8)) days)"
```

**Step 3: Schedule migration window**
- Best time: Low-activity period (weekend, off-hours)
- Duration: Based on estimate + 20% buffer
- Rollback plan: Ready to restore from backup

---

### Batch Migration (Day 2-3)

**Process in batches of 10:**

```bash
# Batch 1: Stories 11-20 (pilot was 1-10)
for i in {11..20}; do
  story_num=$(printf "%03d" $i)
  python migrate_story_v1_to_v2.py devforgeai/specs/Stories/STORY-$story_num*.md --validate

  if [ $? -eq 0 ]; then
    echo "✅ STORY-$story_num migrated"
  else
    echo "❌ STORY-$story_num FAILED" >> migration-failures.txt
  fi
done

# Manual spot-check (20% of batch)
# Review STORY-011, STORY-015

# If batch successful, continue to next batch
# If failures, HALT and investigate
```

**Safety protocols:**
- HALT on first failure (investigate before continuing)
- Manual review every 5th story (20% sampling)
- Validation required for every story
- Rollback ready at each batch boundary

**Progress tracking:**
```
Batch 1 (stories 11-20): 10/10 migrated ✅
Batch 2 (stories 21-30): 9/10 migrated ⚠️ (1 failure - investigate)
Batch 3 (stories 31-40): PENDING
...
```

---

### Post-Migration Validation (Day 4)

**Comprehensive validation:**

```bash
# 1. Validate ALL stories
for story in devforgeai/specs/Stories/*.story.md; do
  python validate_tech_spec.py "$story" || echo "FAILED: $story" >> validation-failures.txt
done

# Count failures
failures=$(wc -l < validation-failures.txt)
echo "Validation failures: $failures"

# Target: 0 failures (100% pass rate)
```

**If validation failures:**
```bash
# Review each failure
cat validation-failures.txt

# For each failed story:
# 1. Read validation error
# 2. Fix YAML manually
# 3. Re-validate
# 4. Re-test with /dev
```

**Format version check:**
```bash
# Verify all stories migrated
grep -L 'format_version: "2.0"' devforgeai/specs/Stories/*.md

# Expected: Empty (all should have v2.0)
# If any missing: Those weren't migrated, investigate why
```

**Test with /dev (spot check 5 random stories):**
```bash
# Random selection
shuf -n 5 -e STORY-*.md | while read story; do
  story_id=$(basename "$story" .md | cut -d'-' -f1-2)
  /dev $story_id
  # Verify: Phase 1 Step 4 works, detects v2.0 format, completes successfully
done
```

---

## Rollback Procedures

### Rollback Single Story

**Scenario:** One story migration failed, need to restore

```bash
# Find backup
story_id="STORY-042"
backup=$(ls devforgeai/backups/phase2-*/STORY-042*.md | tail -1)

# Restore
cp "$backup" devforgeai/specs/Stories/

# Verify
diff "$backup" devforgeai/specs/Stories/STORY-042*.md
# Expected: No differences

# Test
/dev STORY-042
# Expected: Works with v1.0 format
```

---

### Rollback Batch

**Scenario:** Entire batch failed, restore 10 stories

```bash
# Restore batch 3 (stories 31-40)
for i in {31..40}; do
  story_num=$(printf "%03d" $i)
  backup=$(ls devforgeai/backups/phase2-full/STORY-$story_num*.md)
  cp "$backup" devforgeai/specs/Stories/
done

# Verify count
restored=$(ls devforgeai/specs/Stories/STORY-03*.md | wc -l)
echo "Restored: $restored stories"
# Expected: 10
```

---

### Rollback Full Migration

**Scenario:** Phase 2 fails, restore all stories to v1.0

```bash
# 1. Restore ALL stories from full backup
rm devforgeai/specs/Stories/*.md
cp devforgeai/backups/phase2-full/*.md devforgeai/specs/Stories/

# 2. Verify restoration
original_count=$(ls devforgeai/backups/phase2-full/*.md | wc -l)
restored_count=$(ls devforgeai/specs/Stories/*.md | wc -l)
echo "Original: $original_count, Restored: $restored_count"
# Should match

# 3. Verify format versions
grep -c 'format_version: "1.0"' devforgeai/specs/Stories/*.md
# Expected: All stories (or no format_version field)

# 4. Test sample
/dev STORY-001  # Should work with v1.0 format
/dev STORY-050  # Should work with v1.0 format

# 5. Document rollback
echo "Phase 2 rolled back on $(date)" > devforgeai/specs/enhancements/PHASE2-ROLLBACK.md
echo "Reason: [DESCRIBE REASON]" >> devforgeai/specs/enhancements/PHASE2-ROLLBACK.md

# 6. Revert code changes
git checkout HEAD~N .claude/skills/devforgeai-story-creation/assets/templates/story-template.md
git checkout HEAD~N .claude/skills/devforgeai-development/references/tdd-red-phase.md
# (N = number of Phase 2 commits)
```

**Time to rollback:** 30-45 minutes

---

## Migration Quality Checklist

### Per-Story Quality Review

**For manual review of migrated stories:**

**YAML Structure (1-5):**
- 5: Perfect indentation, proper quotes, valid YAML
- 4: Minor formatting issues (extra spaces)
- 3: Some syntax issues but parseable
- 2: Multiple syntax issues
- 1: Invalid YAML, doesn't parse

**Component Accuracy (1-5):**
- 5: All components identified, correct types
- 4: Most components (≥90%), correct types
- 3: Most components (≥80%), some type errors
- 2: Half components (≥50%)
- 1: Few components (<50% detected)

**Test Requirements (1-5):**
- 5: All specific, actionable, start with "Test: "
- 4: Most specific (≥90%)
- 3: Some generic (≥70% specific)
- 2: Many generic (≥50%)
- 1: Mostly generic or missing

**Overall Quality:**
- Average the 3 scores above
- Target: ≥4.0 average
- Acceptable: ≥3.5 average
- Re-migrate if <3.0

---

## Troubleshooting

### Issue: Migration script produces empty components array

**Symptom:**
```yaml
components: []
```

**Cause:** Pattern matching failed to detect components in freeform text

**Solutions:**
1. **Use AI-assisted migration** (Week 3 enhancement)
2. **Manual migration** (write YAML by hand)
3. **Improve patterns** (add more keywords to detect components)

---

### Issue: "Invalid YAML in tech spec"

**Symptom:** Validator error during `--validate`

**Cause:** Migration generated malformed YAML (quotes, indentation)

**Solutions:**
1. Check YAML syntax: `python -c "import yaml; yaml.safe_load(open('story.md').read())"`
2. Fix common issues:
   - Strings with `:` need quotes: `description: "Alert: Warning"`
   - Consistent indentation (2 spaces per level)
   - Arrays use `- ` prefix

---

### Issue: Components detected with wrong type

**Symptom:** Worker classified as Service

**Cause:** Pattern matching ambiguity

**Solution:** Manually fix component type in migrated YAML:
```yaml
# Change this:
- type: "Service"
  name: "AlertDetectionWorker"

# To this:
- type: "Worker"
  name: "AlertDetectionWorker"
```

---

### Issue: Test requirements too generic

**Symptom:** `test_requirement: "Test: Verify it works"`

**Cause:** Migration script couldn't infer specific test from freeform text

**Solution:** Manually refine test requirements:
```yaml
# Generic (before)
test_requirement: "Test: Verify it works"

# Specific (after)
test_requirement: "Test: Worker polls at 30s intervals until cancellation"
```

---

### Issue: /dev fails after migration

**Symptom:** `/dev STORY-XXX` fails with YAML parsing error

**Cause:** Malformed YAML in migrated story

**Solutions:**
1. Run validator: `python validate_tech_spec.py STORY-XXX.md`
2. Fix reported errors
3. Re-test /dev

**If unfixable:**
```bash
# Rollback this story
cp devforgeai/backups/phase2-pilot/STORY-XXX*.md devforgeai/specs/Stories/
```

---

## Migration Metrics Tracking

### Per-Story Metrics Template

```markdown
| Story ID | Complexity | Components v1.0 | Components v2.0 | Migration Time | Quality | /dev Success | Notes |
|----------|------------|-----------------|-----------------|----------------|---------|--------------|-------|
| STORY-001 | Simple | 2 | 3 | 25 min | 4/5 | ✅ | Config key added |
| STORY-002 | Medium | 5 | 5 | 35 min | 5/5 | ✅ | Perfect |
| STORY-003 | Complex | 7 | 8 | 45 min | 4/5 | ✅ | Added NFR |
| ... | ... | ... | ... | ... | ... | ... | ... |
```

**Aggregate metrics:**
- Migration success rate: (Migrated / Total) × 100
- Average quality: Sum(Quality) / Count
- Component accuracy: (v2.0 detected / v1.0 detected) × 100
- Average time: Sum(Time) / Count

**Targets:**
- Success rate: 100%
- Average quality: ≥4.0
- Component accuracy: ≥100% (v2.0 should detect same or more)
- Average time: <30 min

---

## Data Loss Prevention

### Validation Checkpoints

**Before migration:**
- [ ] All stories backed up
- [ ] Backup verified (count matches)
- [ ] Test restore (1 sample)

**During migration:**
- [ ] Backup before each batch
- [ ] Validate after each story
- [ ] HALT on first failure
- [ ] Manual review 20% of stories

**After migration:**
- [ ] All stories have format_version: "2.0"
- [ ] Validation passes for all (100%)
- [ ] Component count ≥ original
- [ ] /dev works for all (spot check 10%)

**If data loss detected:**
1. HALT migration immediately
2. Rollback affected stories
3. Document what was lost
4. Fix migration script
5. Re-migrate with fix

---

## Success Criteria

### Pilot Migration Success (Week 4)

**Required (all must pass):**
- [ ] 10/10 stories migrated successfully (100%)
- [ ] ≥9/10 validations passing (≥90%)
- [ ] 10/10 /dev workflows successful (100%)
- [ ] Average quality ≥4.0
- [ ] Zero data loss

**Optional (nice to have):**
- [ ] Migration time <25 min average
- [ ] Component accuracy 100% (v2.0 ≥ v1.0 for all)
- [ ] Zero manual fixes needed

---

### Full Migration Success (Week 5)

**Required (all must pass):**
- [ ] 100% stories migrated
- [ ] ≥90% validation passing
- [ ] All format_version fields = "2.0"
- [ ] /dev works (spot check 10 random stories)
- [ ] Zero data loss

**Optional:**
- [ ] 100% validation passing (vs ≥90%)
- [ ] Parsing accuracy 95%+ (measured)

---

## Phase 2 Complete Checklist

**Code artifacts:**
- [x] STRUCTURED-FORMAT-SPECIFICATION.md created
- [x] validate_tech_spec.py created and tested
- [x] migrate_story_v1_to_v2.py created
- [ ] Migration script enhanced with AI (Week 3)
- [x] story-template.md updated to v2.0
- [x] tdd-red-phase.md Step 4.1 updated (format detection)
- [x] api-designer.md updated for v2.0 output

**Documentation:**
- [x] PHASE2-IMPLEMENTATION-GUIDE.md created
- [x] PHASE2-TESTING-CHECKLIST.md created (this document)
- [x] PHASE2-MIGRATION-GUIDE.md created
- [ ] Phase 2 completion summary

**Testing:**
- [ ] Validator unit tests (12 cases) - all pass
- [ ] Migration unit tests (10 cases) - all pass
- [ ] Integration tests (8 cases) - all pass
- [ ] Pilot migration (10 stories) - 100% success
- [ ] Full migration (all stories) - ≥90% success
- [ ] Regression tests (6 cases) - all pass

**Migration:**
- [ ] 10 pilot stories migrated and validated
- [ ] All stories migrated to v2.0
- [ ] All validation passing
- [ ] /dev works with v2.0 stories

**Decision:**
- [ ] Pilot review complete (GO/NO-GO)
- [ ] Full migration complete (if GO)
- [ ] Decision Point 2 evaluated
- [ ] Phase 3 decision made

---

**Use this checklist to track Phase 2 testing progress. All items must complete for Phase 2 success.**
