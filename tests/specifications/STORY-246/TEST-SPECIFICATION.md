# Test Specification: STORY-246 Release Skill Registry Integration

**Story Type:** Documentation (Markdown files only)
**Output Type:** Test Specification Document (non-executable)
**Created:** 2026-01-08

---

## AC#1: Phase 0.5 Addition to Release Skill

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC1-001 | Phase 0.5 section exists | `grep -qE "^### Phase 0\.5"` | Section header present |
| AC1-002 | Phase 0.5 after Phase 0 | Line number comparison | Phase 0.5 line > Phase 0 line |
| AC1-003 | Phase 0.5 before Phase 1 | Line number comparison | Phase 0.5 line < Phase 1 line |
| AC1-004 | Phase 0.5 section size | Line count between headers | 5-15 lines |
| AC1-005 | Reference link present | `grep -q "registry-publishing.md"` | Reference documented |
| AC1-006 | SKILL.md line limit | `wc -l` | < 1000 lines |

### Validation Commands

```bash
# AC1-001: Phase 0.5 exists
grep -nE "^### Phase 0\.5" .claude/skills/devforgeai-release/SKILL.md

# AC1-002/003: Phase ordering
PHASE_0=$(grep -n "^### Phase 0:" SKILL.md | head -1 | cut -d: -f1)
PHASE_05=$(grep -n "^### Phase 0\.5" SKILL.md | head -1 | cut -d: -f1)
PHASE_1=$(grep -n "^### Phase 1:" SKILL.md | head -1 | cut -d: -f1)
# Validate: PHASE_0 < PHASE_05 < PHASE_1

# AC1-006: Line limit
wc -l .claude/skills/devforgeai-release/SKILL.md
```

---

## AC#2: Registry Publishing Reference Documentation

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC2-001 | File exists | File presence check | File created |
| AC2-002 | npm registry documented | `grep -q "npm"` | Section present |
| AC2-003 | PyPI registry documented | `grep -q "PyPI\|pypi"` | Section present |
| AC2-004 | NuGet registry documented | `grep -q "NuGet\|nuget"` | Section present |
| AC2-005 | Docker registry documented | `grep -q "Docker\|docker"` | Section present |
| AC2-006 | GitHub registry documented | `grep -q "GitHub\|github"` | Section present |
| AC2-007 | crates.io documented | `grep -q "crates"` | Section present |
| AC2-008 | Credentials section | `grep -qE "^## Credential"` | Section present |
| AC2-009 | Error handling section | `grep -qE "^## Error"` | Section present |
| AC2-010 | Retry logic section | `grep -qE "^## Retry"` | Section present |
| AC2-011 | File size limit | `wc -l` | < 500 lines |

### Validation Commands

```bash
# AC2-001: File exists
test -f .claude/skills/devforgeai-release/references/registry-publishing.md

# AC2-002 through AC2-007: Registry coverage
for registry in npm PyPI NuGet Docker GitHub crates; do
  grep -qi "$registry" registry-publishing.md || echo "FAIL: $registry"
done

# AC2-011: Line limit
wc -l registry-publishing.md
```

---

## AC#3: Phase 0.5 Workflow Execution

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC3-001 | Config loading documented | `grep -q "registry-config.yaml"` | Config path referenced |
| AC3-002 | Sequential execution | `grep -qi "sequence\|sequential"` | Execution order documented |
| AC3-003 | Results aggregation | `grep -qi "aggregate\|results"` | Aggregation documented |

---

## AC#4: Skip Registry Publishing Option

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC4-001 | Skip flag documented | `grep -q "\-\-skip-registry"` | Flag documented |
| AC4-002 | Skip behavior described | `grep -qi "skip.*registry"` | Behavior explained |

---

## AC#5: Dry-Run Mode Integration

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC5-001 | Dry-run flag integration | `grep -q "\-\-dry-run"` | Flag documented |
| AC5-002 | Dry-run behavior | `grep -qi "dry.run\|would.*publish"` | Behavior explained |

---

## AC#6: Phase 0.5 Failure Handling

### Structural Tests

| Test ID | Test Description | Validation Pattern | Expected Result |
|---------|------------------|-------------------|-----------------|
| AC6-001 | User prompt documented | `grep -qi "prompt\|AskUserQuestion"` | Prompt referenced |
| AC6-002 | Continue option | `grep -qi "continue"` | Option documented |
| AC6-003 | Abort option | `grep -qi "abort\|halt"` | Option documented |

---

## Validation Checklist

### Pre-Implementation (All should FAIL)
- [ ] AC1-001 through AC1-006 - Phase 0.5 not yet added
- [ ] AC2-001 through AC2-011 - Reference file not yet created

### Post-Implementation (All should PASS)
- [ ] All structural tests pass
- [ ] Line limits respected
- [ ] All 6 registries documented

---

**Template Version:** 1.0
**Test Type:** Structural Validation (non-executable)
