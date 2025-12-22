# UI Spec Formatter Integration Guide

**Date:** 2025-11-05
**Component:** ui-spec-formatter subagent
**Location:** `.claude/agents/ui-spec-formatter.md`
**Reference:** `.claude/skills/devforgeai-ui-generator/references/ui-result-formatting-guide.md`

---

## Overview

The `ui-spec-formatter` subagent formats UI specification results for display after the devforgeai-ui-generator skill completes. This follows the lean orchestration pattern established by qa-result-interpreter.

**Problem Solved:**
- Commands become bloated with display logic (currently 614 lines for /create-ui)
- Formatting/validation logic duplicated between command and skill
- Result interpretation happens in wrong place (command vs. skill)
- Framework constraints not enforced on generated specs

**Pattern:**
- Skill generates UI specification
- Subagent formats and validates results
- Command displays subagent output (no additional processing)

---

## Integration Points

### Phase 6: Documentation (Existing in Skill)

**Current location in devforgeai-ui-generator skill:**
```
Phase 6: Documentation
├── Step 1: Update Story File
├── Step 2: Create UI Spec Summary
├── Step 3: Display Results ← REFACTOR HERE
├── Step 4: Return Summary (NEW)
└── Step 5: Success Message
```

**Refactoring needed:** Add Phase 6 Step 3.5 (new) between Step 3 and 4

---

## Implementation Steps

### Step 1: Add Subagent Invocation to Skill

**Location:** `.claude/skills/devforgeai-ui-generator/SKILL.md` Phase 6, Step 3.5

**Add this section:**

```markdown
### Step 3.5: Invoke UI Spec Formatter Subagent (NEW)

Format and validate UI specification results:

```
Task(
    subagent_type="ui-spec-formatter",
    description="Format UI specification results",
    prompt="Format UI specification for {STORY_OR_COMPONENT}.

            Specification generated at: devforgeai/specs/ui/{SPEC_ID}-ui-spec.md

            Story mode: {mode}
            Story ID: {story_id or 'standalone'}
            Framework: {framework}
            Styling: {styling_library}
            Component count: {component_count}

            Parse the specification file and generate structured display results.
            Validate against framework context files (tech-stack, source-tree, dependencies).
            Return structured JSON with display template and next steps."
)

Capture response as: formatter_result

Parse formatter_result.display.template
Extract formatter_result.next_steps
```

**What the subagent does:**
1. Reads generated UI spec file
2. Extracts component details
3. Validates against context files (tech-stack.md, source-tree.md, dependencies.md)
4. Generates display template (success/partial/failed)
5. Returns structured JSON for skill/command to display

---

### Step 2: Update Skill to Use Formatter Output

**Location:** `.claude/skills/devforgeai-ui-generator/SKILL.md` Phase 6, Step 4

**Current code (BEFORE):**
```markdown
### Step 4: Display Results

[... 50+ lines of display templates ...]
```

**New code (AFTER):**
```markdown
### Step 4: Return Formatter Results

The formatter subagent (Phase 6.3.5) has prepared results:

Display:
- formatter_result.display.template (user-facing output)
- formatter_result.next_steps (guidance for next actions)

If formatter_result.status == "FAILED":
    HALT and communicate error clearly
    Return error details and recovery steps
ELSE:
    Continue to Step 5 (Success Message)
```

**Benefit:**
- Skill delegates formatting to specialized subagent
- Skill focuses on generation logic (not display)
- Display templates in subagent = easier to maintain
- Command doesn't need to parse/format anything

---

### Step 3: Minimize Command Processing

**Location:** `.claude/commands/create-ui.md` (future refactoring)

**Current (before refactoring):**
```
Line count: 614
Character count: 18,908 (126% over 15K budget)
Issues:
  - 300+ lines of display templates
  - Validation logic duplicated
  - Result interpretation in command
```

**After refactoring:**
```
Line count: ~300 (50% reduction)
Character count: ~9,500 (63% of budget, within limit)

Changes:
- Remove display templates (moved to subagent)
- Remove result interpretation (moved to subagent)
- Keep only: argument validation, story loading, skill invocation, result display
- Command outputs: subagent display template (no processing)
```

---

## Subagent Architecture

### Input (from Skill)

```json
{
  "spec_file": "devforgeai/specs/ui/STORY-XXX-ui-spec.md",
  "story_id": "STORY-XXX",
  "mode": "story|standalone",
  "framework": "React|Vue|Angular|Blazor|WPF|Tkinter",
  "styling": "Tailwind|CSS Modules|styled-components|etc",
  "component_count": 3
}
```

### Output (to Skill, then Command)

```json
{
  "status": "SUCCESS|PARTIAL|FAILED",
  "display": {
    "template": "✅ UI Component Specification Generated...",
    "content": "Full markdown output"
  },
  "component_details": [
    {
      "name": "LoginForm",
      "type": "Form",
      "framework": "React",
      "accessibility": "WCAG 2.1 AA",
      "responsive": true,
      "test_scenarios": 8
    }
  ],
  "validation": {
    "issues": [],
    "warnings": [],
    "status": "PASSED"
  },
  "next_steps": [
    "Review generated specification",
    "Begin implementation: `/dev STORY-XXX`"
  ]
}
```

---

## Reference File: ui-result-formatting-guide.md

**Location:** `.claude/skills/devforgeai-ui-generator/references/ui-result-formatting-guide.md`

**Purpose:** Provide framework constraints and validation rules to subagent

**Contains:**
1. **DevForgeAI Context** - Story workflow states, quality gates
2. **Framework Constraints** - Tech-stack, file structure, accessibility, testing
3. **Display Templates** - Success, partial, failed templates
4. **Framework Integration** - Context file references, related skills
5. **Validation Rules** - Severity levels, error scenarios
6. **Testing Checklist** - For validating subagent behavior

**Key sections:**
- Framework consistency (tech-stack.md validation)
- File structure compliance (source-tree.md validation)
- Accessibility requirements (WCAG mandatory)
- Component categorization (deterministic)
- Responsive design standards (mobile-first)

---

## Framework-Aware Design

The subagent is **NOT** a silo. It understands DevForgeAI constraints:

### Context File Awareness

**tech-stack.md:**
- Validates generated framework is approved
- Alerts if framework not in list
- Warns about dependencies not yet approved

**source-tree.md:**
- Validates file locations per project structure
- Alerts if components in wrong directories
- Recommends correct locations

**dependencies.md:**
- Validates external packages are approved
- Warns about missing dependencies
- Suggests additions if needed

**coding-standards.md:**
- Validates component naming conventions
- Checks component size limits
- References formatting standards

**architecture-constraints.md:**
- Validates component isolation in presentation layer
- Checks for layer boundary violations
- Ensures proper architectural boundaries

**anti-patterns.md:**
- Detects forbidden patterns in generated code
- Alerts to code smells
- Recommends refactoring

### Story Workflow Integration

The subagent understands story states:

```
Architecture → Ready for Dev (UI spec generated here)
    ↓
In Development (spec used for TDD)
    ↓
Dev Complete → QA In Progress (spec validates acceptance criteria)
    ↓
QA Approved → Releasing → Released
```

**Next steps provided are context-aware:**
- Story mode: "Review spec, then `/dev STORY-XXX`"
- Standalone: "Copy to project, then integrate"
- With warnings: "Address warnings, then proceed"

---

## Token Efficiency

### Budget

- **Subagent token target:** <10K tokens per invocation
- **Skill passes:** ~2K tokens (structured input)
- **Subagent execution:** ~8K tokens (read, parse, validate, format)
- **Returned to command:** ~5K tokens (summary + display)

### Optimization

- Single file read (UI spec)
- Selective context file validation (only relevant sections)
- Focused pattern matching
- Deterministic output format
- No recursive file access

### Comparison

**Before (display logic in command):**
- Command: 8K+ tokens (display templates, validation)
- Skill: 85K tokens (generation, no formatting)
- Total main conversation: ~13K tokens

**After (display logic in subagent):**
- Command: 2-3K tokens (minimal orchestration)
- Skill: 85K tokens (generation only)
- Subagent: 8K tokens (isolated context)
- Total main conversation: ~5K tokens (61% reduction)

---

## Testing Strategy

### Unit Tests for Subagent

1. **Spec File Parsing:**
   - Parse story mode success spec
   - Parse standalone mode success spec
   - Handle missing spec file gracefully
   - Handle malformed spec gracefully

2. **Validation:**
   - Validate framework in tech-stack.md
   - Validate file structure per source-tree.md
   - Validate accessibility completeness
   - Detect framework mismatches
   - Detect file location violations

3. **Display Template Generation:**
   - Generate success template
   - Generate partial template (warnings)
   - Generate failed template (errors)
   - Use appropriate emoji and tone
   - Include all required sections

4. **Component Categorization:**
   - Categorize forms correctly
   - Categorize data displays correctly
   - Categorize navigation correctly
   - Identify dependencies
   - Estimate implementation time

5. **Next Steps:**
   - Recommend `/dev` for story mode
   - Recommend copy/integrate for standalone
   - Warn about validation issues
   - Provide recovery steps for failures

### Integration Tests

1. **Skill Integration:**
   - Skill generates spec
   - Formatter invoked automatically
   - Result returned to skill
   - Command displays result

2. **Full Workflow (Story Mode):**
   - Load story
   - Invoke /create-ui
   - Skill generates spec
   - Formatter validates and formats
   - Command displays results
   - User sees next steps
   - User runs `/dev STORY-XXX`

3. **Full Workflow (Standalone Mode):**
   - Invoke /create-ui with description
   - Skill generates spec
   - Formatter validates and formats
   - Command displays results
   - User copies component to project

---

## Rollout Plan

### Phase 1: Create Subagent
- [ ] Create ui-spec-formatter.md
- [ ] Create ui-result-formatting-guide.md
- [ ] Unit test subagent (30+ test cases)

### Phase 2: Integrate with Skill
- [ ] Add Phase 6.3.5 to skill
- [ ] Test skill → subagent → command flow
- [ ] Verify token budgets
- [ ] Validate framework constraints enforced

### Phase 3: Refactor /create-ui Command
- [ ] Remove display templates from command
- [ ] Remove validation logic from command
- [ ] Keep: argument parsing, story loading, skill invocation
- [ ] Reduce command from 614 to ~300 lines
- [ ] Reduce character count from 18.9K to ~9.5K
- [ ] Update .claude/memory/commands-reference.md
- [ ] Update .claude/memory/subagents-reference.md

### Phase 4: Testing and Validation
- [ ] Full integration testing
- [ ] Token budget verification
- [ ] Framework compliance verification
- [ ] User acceptance testing
- [ ] Monitor for 1 week

---

## Files Created/Modified

### New Files

1. **`.claude/agents/ui-spec-formatter.md`**
   - 507 lines
   - Complete subagent definition
   - Framework-aware design
   - Token target: <10K

2. **`.claude/skills/devforgeai-ui-generator/references/ui-result-formatting-guide.md`**
   - 394 lines
   - Framework guardrails
   - Validation rules
   - Display template guidelines
   - Testing checklist

3. **`devforgeai/specs/enhancements/UI-SPEC-FORMATTER-INTEGRATION.md`** (this file)
   - Integration guide
   - Architecture documentation
   - Rollout plan

### Files to Modify (Phase 3 - Future)

1. **`.claude/skills/devforgeai-ui-generator/SKILL.md`**
   - Add Phase 6.3.5: Invoke formatter subagent
   - Modify Phase 6.4: Return formatter results
   - Update references section

2. **`.claude/commands/create-ui.md`**
   - Remove display templates (~300 lines)
   - Remove validation logic
   - Keep minimal orchestration
   - Expected: 614 → 300 lines, 18.9K → 9.5K chars

3. **`.claude/memory/commands-reference.md`**
   - Update /create-ui section
   - Note refactoring and subagent
   - Show new architecture

4. **`.claude/memory/subagents-reference.md`**
   - Add ui-spec-formatter entry
   - Document invocation
   - Show token budget

---

## Success Criteria

### Subagent Quality
- [ ] Reads and parses UI spec files correctly
- [ ] Validates against all 6 context files
- [ ] Generates appropriate display templates
- [ ] Token usage <10K
- [ ] Framework-aware (not siloed)
- [ ] Reference file loaded for constraints

### Integration Success
- [ ] Skill invokes subagent automatically
- [ ] Subagent returns structured JSON
- [ ] Command displays result without processing
- [ ] Token efficiency improved (>50%)
- [ ] Character budget compliance achieved

### Framework Compliance
- [ ] Tech-stack constraints enforced
- [ ] Source-tree structure validated
- [ ] Accessibility requirements verified
- [ ] Anti-patterns detected and warned
- [ ] Architecture constraints checked

### Token Efficiency
- [ ] Command overhead: <3K tokens (down from ~8K)
- [ ] Main conversation: ~5K tokens total (down from ~13K)
- [ ] Savings: 61% reduction
- [ ] Subagent: <10K in isolated context

---

## Related Documentation

### Reference Files
- `devforgeai/protocols/lean-orchestration-pattern.md` - Pattern this follows
- `.ai_docs/prompt-engineering-best-practices.md` - Claude-specific optimizations

### Similar Implementations
- `.claude/agents/qa-result-interpreter.md` - Reference pattern
- `.claude/skills/devforgeai-qa/references/qa-result-formatting-guide.md` - Reference pattern

### Framework Documentation
- `CLAUDE.md` - Framework principles
- `.claude/memory/subagents-reference.md` - Subagent guidance
- `.claude/memory/commands-reference.md` - Command architecture

---

## Questions and Answers

### Q: Why create a subagent for formatting?
A: Formatting has specialized requirements (template selection, framework validation, constraint checking) that belong in isolated, reusable logic—not in commands. This pattern allows skill focus on generation, subagent focus on presentation, command focus on orchestration.

### Q: How does this differ from qa-result-interpreter?
A: Both follow the same pattern but for different domains. QA interprets validation results; UI formatter interprets generation results. Both validate against framework constraints and generate display templates.

### Q: What if framework validation fails?
A: Subagent marks result as PARTIAL (not blocker) and alerts user. User can confirm if it's intentional or regenerate. Framework constraints are guidelines, not blockers, but violations are always surfaced.

### Q: How much does this improve /create-ui performance?
A: Character budget: 18.9K → 9.5K (50% reduction). Token usage: ~8K → ~3K in main conversation (61% reduction). Speed: Similar (subagent runs in parallel isolated context).

### Q: Can this pattern be applied to other commands?
A: Yes. Any command with display logic (create-story, release, orchestrate) could use specialized formatter subagents following this pattern.

---

## Next Steps

1. **Verify files created:**
   ```bash
   ls -la .claude/agents/ui-spec-formatter.md
   ls -la .claude/skills/devforgeai-ui-generator/references/ui-result-formatting-guide.md
   ```

2. **Update memory references:**
   - Add ui-spec-formatter to `.claude/memory/subagents-reference.md`
   - Update /create-ui section in `.claude/memory/commands-reference.md`

3. **Test subagent:**
   - Unit tests: Parse specs, validate, generate templates
   - Integration tests: Skill → subagent → command
   - Framework compliance: Context file validation

4. **Integrate with skill:**
   - Add Phase 6.3.5 to devforgeai-ui-generator skill
   - Test end-to-end flow
   - Verify token budgets

5. **Refactor /create-ui command:** (Future phase)
   - Remove display logic
   - Reduce to ~300 lines
   - Stay within 10K character budget

---

**Document prepared:** 2025-11-05
**Implementation status:** Ready for integration
**Token budget:** ui-spec-formatter <10K, command refactoring future phase
