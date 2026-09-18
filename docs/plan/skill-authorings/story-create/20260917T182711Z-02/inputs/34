# Acceptance Criteria — Refactor Story Patterns

**Conditional reference:** Load ONLY when story `type: refactor` in YAML frontmatter.

**See also:**
- `acceptance-criteria-core.md` — Core principles + universal patterns (always loaded)
- `acceptance-criteria-domains.md` — Domain-specific patterns (always loaded)

---

## Purpose

Auto-generate content-preservation acceptance criteria for refactor stories to prevent logic loss during implementation. Without these patterns, refactor stories generate only size-reduction ACs (proxy metrics) without content-completeness ACs (substance).

**Reference:** EPIC-071 STORY-457 revert — ACs measured structure/size but not content. Seven stories required manual amendments (~2 hours each).

**Trigger:** These templates are used ONLY when `type: refactor` in story YAML frontmatter.

---

## Template 1: Content Preservation AC

```xml
<acceptance_criteria id="AC_CONTENT_PRESERVE">
  <given>The original {artifact_name} contains {display_count} Display statements, {error_count} error handling blocks, and {governance_count} governance sections ({section_names})</given>
  <when>The artifact is refactored to lean orchestration pattern</when>
  <then>ALL {display_count} Display statement patterns preserved in target artifacts (command, skill, or reference files), ALL {error_count} error handling blocks preserved with exact emoji+message+action format, ALL governance sections ({section_names}) preserved verbatim in skill reference files or command</then>
</acceptance_criteria>
```

## Template 2: Backward-Compatible Output AC

```xml
<acceptance_criteria id="AC_BACKWARD_COMPAT">
  <given>Pre-refactoring golden output samples captured for: {list_all_invocation_modes}</given>
  <when>Refactored command runs with identical arguments</when>
  <then>Help text contains ALL original sections ({section_count} sections: {section_names}), error messages use identical formatting, visual indicators match originals, display format matches golden reference</then>
</acceptance_criteria>
```

## Template 3: AskUserQuestion Placement AC

```xml
<acceptance_criteria id="AC_ASKUSER_PLACEMENT">
  <given>The lean orchestration pattern (lean-orchestration-pattern.md line 104) states "User interaction (AskUserQuestion belongs in commands for UX decisions)". Original {artifact_name} has {askuser_count} AskUserQuestion calls</given>
  <when>Refactored command and skill are inspected</when>
  <then>Skill/reference files contain ZERO AskUserQuestion calls, ALL {askuser_count} prompts remain in command file with original text and options, skills receive user decisions via context markers</then>
</acceptance_criteria>
```

## Template 4: Skill Content Completeness AC

```xml
<acceptance_criteria id="AC_SKILL_COMPLETE">
  <given>The following business logic items are extracted from {artifact_name}: {enumerated_list_of_items}</given>
  <when>Skill or reference file is inspected</when>
  <then>ALL {item_count} items present in skill body or references/ directory, each item verifiable by grep for its key identifier</then>
</acceptance_criteria>
```

## Template 5: Interactive Prompt Completeness AC

```xml
<acceptance_criteria id="AC_PROMPT_COMPLETE">
  <given>Original {artifact_name} has {askuser_count} AskUserQuestion calls: {list_each_prompt_purpose}</given>
  <when>Refactored command executes with user interaction</when>
  <then>ALL {askuser_count} prompts produce identical question text and option lists as originals, including: {enumerate_each_prompt_with_options}</then>
</acceptance_criteria>
```

## Template 6: Golden Output Capture DoD Item

```markdown
### DoD Item Template (Refactor Stories)
- [ ] Golden output samples captured BEFORE refactoring for all {mode_count} invocation modes
- [ ] Post-refactoring output diffed against golden samples
- [ ] Help text section count matches original ({section_count} sections)
- [ ] Error message count matches original ({error_count} error types)
```

---

## Template Placeholder Reference

| Placeholder | Source | How to Populate |
|---|---|---|
| `{artifact_name}` | Filename being refactored | e.g., "validate-epic-coverage.md" |
| `{display_count}` | `Grep(pattern="Display:", path=file)` count | Count of Display statement patterns |
| `{askuser_count}` | `Grep(pattern="AskUserQuestion", path=file)` count | Count of AskUserQuestion calls |
| `{error_count}` | `Grep(pattern="^### Error", path=file)` count | Count of error handling blocks |
| `{governance_count}` | Count of Architecture, Hook Integration, etc. sections | From governance section grep |
| `{section_names}` | `Grep(pattern="^## \\|^### ", path=file)` | Extracted section headers |
| `{section_count}` | Count of `## ` and `### ` headers | Total section count |
| `{mode_count}` | Count of invocation modes from Quick Reference | e.g., 3 modes: single, all, epic |

**Usage:** Step 2.1.7 in requirements-analysis.md auto-populates these placeholders by reading target files during story creation.
