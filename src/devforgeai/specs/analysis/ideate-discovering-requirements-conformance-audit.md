# /ideate & discovering-requirements Anthropic Conformance Audit

**Date:** 2026-02-18
**Auditor:** Claude AI (3-agent parallel audit)
**Status:** Complete
**Categories Completed:** 10 / 10
**Prior Analysis:** `devforgeai/specs/analysis/ideation-anthropic-conformance-analysis.md` (9 categories, 29 findings against old `devforgeai-ideation` skill)

---

## Executive Summary

The `/ideate` command and `discovering-requirements` skill were audited across 10 Anthropic conformance categories using 23+ reference documents. **44 findings** were identified: **9 FAIL**, **23 PARTIAL**, **12 PASS**.

**Key improvements since prior analysis:** The skill rename from `devforgeai-ideation` to `discovering-requirements` resolved naming findings (gerund form, vendor prefix removal). SKILL.md is now 339 lines (well under 500-line recommendation).

**Persistent issues (not addressed since prior audit):** All structural prompt engineering issues persist — no XML tags, no role prompt, no multishot examples, YAML frontmatter format non-compliant, command contains excessive business logic.

**Top 5 highest-impact fixes:**
1. Add role prompt to SKILL.md (Finding 4.1 — FAIL, High)
2. Add multishot examples (Finding 5.1 — FAIL, High)
3. Introduce XML tags for structural separation (Finding 5.3 — FAIL, High)
4. Fix `allowed-tools` format to space-delimited (Finding 7.1 — FAIL, Medium)
5. Move command error handling to skill references (Finding 8.1 — PARTIAL, Medium)

---

## Summary Table

| # | Category | Status | Findings | PASS | PARTIAL | FAIL | vs Prior |
|---|----------|--------|----------|------|---------|------|----------|
| 1 | Prompt Structure (YAML) | FAIL | 7 | 1 | 3 | 3 | 4 PERSIST, 2 NEW |
| 2 | Clarity & Directness | PASS | 5 | 5 | 0 | 0 | 2 RESOLVED |
| 3 | Chain-of-Thought | PARTIAL | 3 | 0 | 3 | 0 | 2 PERSIST, 1 NEW |
| 4 | Role Definition | FAIL | 2 | 0 | 0 | 2 | 1 PERSIST, 1 NEW |
| 5 | Examples/Multishot | FAIL | 5 | 0 | 3 | 2 | 3 PERSIST, 1 NEW |
| 6 | Long Context Handling | PARTIAL | 4 | 2 | 2 | 0 | 4 NEW |
| 7 | Skill Spec Compliance | PARTIAL | 5 | 0 | 3 | 2 | 4 PERSIST, 1 NEW |
| 8 | Command-Skill Separation | PARTIAL | 3 | 0 | 3 | 0 | 3 PERSIST |
| 9 | Error Handling | PARTIAL | 5 | 2 | 3 | 0 | 5 NEW |
| 10 | User Interaction Patterns | PARTIAL | 5 | 2 | 3 | 0 | 1 PERSIST, 4 NEW |
| | **TOTAL** | | **44** | **12** | **23** | **9** | |

---

## Category 1: Prompt Structure (YAML Frontmatter)

**Overall Status:** FAIL (3 FAIL, 3 PARTIAL, 1 PASS)

#### Finding 1.1: `allowed-tools` Uses YAML Array Instead of Space-Delimited String
**Status:** FAIL | **Severity:** High
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 4-14 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > `allowed-tools: Read Grep Glob WebFetch WebSearch` (Source: agent-skills-spec.md, lines 45, 177-183)
**Current State:** Uses YAML array format with `- Read`, `- Write`, etc.
**Gap:** Spec defines `allowed-tools` as space-delimited string, not YAML array.
**Proposed Fix:** Change to: `allowed-tools: Read Write Edit Glob Grep AskUserQuestion WebFetch Bash Task`
**Impact:** Spec compliance; future validators would reject array format.

#### Finding 1.2: `Bash(git:*)` Is Not a Recognized Tool Name
**Status:** FAIL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, line 12 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > Available Tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch, Task, AskUserQuestion, TodoWrite, NotebookEdit (Source: agent-skills-spec.md, lines 186-197)
**Current State:** `Bash(git:*)` listed. Scoped tool syntax not in spec.
**Proposed Fix:** Replace with `Bash`. Document git-scoping in skill body.
**Impact:** Validation compliance.

#### Finding 1.3: `Skill` Tool Not in Agent Skills Spec
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, line 13 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > Spec lists `Task` for subagent spawning, not `Skill` (Source: agent-skills-spec.md, lines 194-197)
**Current State:** `Skill` listed but not in official spec. Claude Code extension.
**Proposed Fix:** Replace `Skill` with `Task` in allowed-tools.
**Impact:** Spec compliance and portability.

#### Finding 1.4: `model` Field Uses Non-Standard Value
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, line 15 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > `model: claude-opus-4-6` (Source: agent-skills-spec.md, line 49)
**Current State:** `model: claude-opus-4-6`. Command uses `model: opus`. Inconsistent.
**Proposed Fix:** Standardize to one format across files.
**Impact:** Consistency.

#### Finding 1.5: Command `allowed-tools` Uses Comma-Delimited Format
**Status:** FAIL | **Severity:** Medium
**File:** `src/claude/commands/ideate.md`, line 5 | **vs Prior:** NEW
**Anthropic Guidance:** > Space-delimited format required (Source: agent-skills-spec.md, line 45)
**Current State:** `allowed-tools: Read, Write, Edit, Glob, Skill, AskUserQuestion` (comma-delimited).
**Proposed Fix:** Change to space-delimited: `allowed-tools: Read Write Edit Glob Skill AskUserQuestion`
**Impact:** Spec compliance.

#### Finding 1.6: Command `model: opus` Abbreviated Format
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/commands/ideate.md`, line 4 | **vs Prior:** NEW
**Current State:** `model: opus` — ambiguous shorthand, inconsistent with SKILL.md's `claude-opus-4-6`.
**Proposed Fix:** Use consistent model identifier across files.
**Impact:** Consistency.

#### Finding 1.7: SKILL.md Line Count Within Budget
**Status:** PASS | **Severity:** N/A
**File:** `src/claude/skills/discovering-requirements/SKILL.md` (339 lines) | **vs Prior:** RESOLVED
**Anthropic Guidance:** > Keep SKILL.md under 500 lines (Source: best-practices.md, line 233)
**Current State:** 339 lines with 15 reference files loaded on-demand. Well within budget.

---

## Category 2: Clarity & Directness

**Overall Status:** PASS (5 PASS)

#### Finding 2.1: Skill Name Uses Gerund Form Correctly
**Status:** PASS | **vs Prior:** RESOLVED
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, line 2
**Current State:** `name: discovering-requirements` — gerund form per Anthropic best practices.

#### Finding 2.2: Vendor Prefix Removed
**Status:** PASS | **vs Prior:** RESOLVED
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, line 2
**Current State:** No `devforgeai-` prefix. Clean naming.

#### Finding 2.3: Description Includes Trigger Context
**Status:** PASS | **vs Prior:** NEW
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 3-4
**Current State:** Description includes "Use for requirements discovery, business analysis, PM role tasks" and trigger keywords.

#### Finding 2.4: Core Philosophy Section Appropriately Concise
**Status:** PASS | **vs Prior:** PERSISTS (was PASS)
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 49-65
**Current State:** 16 lines. General wisdom but serves as anchor directives for this workflow.

#### Finding 2.5: SKILL.md Under 500 Lines
**Status:** PASS | **vs Prior:** NEW
**Current State:** 339 lines.

---

## Category 3: Chain-of-Thought

**Overall Status:** PARTIAL (3 PARTIAL)

#### Finding 3.1: No XML-Structured CoT for Complexity Scoring
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 86-94 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "Use XML tags like `<thinking>` and `<answer>` to separate reasoning from the final answer." (Source: chain-of-thought.md, lines 50-51)
**Current State:** No `<thinking>` tag instructions for multi-factor decisions (complexity scoring, feasibility analysis).
**Gap:** Anthropic recommends CoT for "decisions with many factors." Complexity scoring across 4 dimensions is exactly this.
**Proposed Fix:** Add thinking guidance: "Before determining complexity tier, reason through factors in `<thinking>` tags, then present conclusion."
**Impact:** More transparent, debuggable reasoning for scoring decisions.

#### Finding 3.2: Phase Handoffs Use Implicit Context, Not Structured XML
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 93-228 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "Structure with XML for clear handoffs: Use XML tags to pass outputs between prompts." (Source: chain-complex-prompts.md, line 34)
**Current State:** Phase transitions use `session.problem_statement` and markdown context markers. No `<phase-1-output>` XML handoff tags.
**Proposed Fix:** Define XML-tagged handoff schemas between phases.
**Impact:** More reliable inter-phase data flow, easier debugging.

#### Finding 3.3: Discovery Workflow Lacks Guided CoT for Probing Questions
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/references/discovery-workflow.md`, lines 105-137 | **vs Prior:** NEW
**Anthropic Guidance:** > "Guided prompt: Outline specific steps for Claude to follow in its thinking process." (Source: chain-of-thought.md, lines 41-48)
**Current State:** Questions are template-driven, not adaptive. No reasoning step between question rounds.
**Proposed Fix:** Add: "Before asking the next question, think through what you've learned so far and identify the biggest remaining ambiguity."
**Impact:** More adaptive questioning.

---

## Category 4: Role Definition

**Overall Status:** FAIL (2 FAIL)

#### Finding 4.1: No Role Prompt in SKILL.md
**Status:** FAIL | **Severity:** High
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, all | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "You can dramatically improve its performance by using the `system` parameter to give it a role. This technique, known as role prompting, is the most powerful way to use system prompts with Claude." (Source: give-claude-a-role.md, lines 9, 17)
**Current State:** No role assignment. Mentions "PM Role Focus" as a philosophy bullet point but never assigns Claude a persona.
**Gap:** Without a role, Claude defaults to general assistant, producing shallower analysis per Anthropic's own demonstrated examples.
**Proposed Fix:** Add after execution model section:
```markdown
## Your Role
You are an expert Product Manager and Requirements Analyst specializing in transforming vague business ideas into structured, implementable requirements. You excel at stakeholder discovery, requirements elicitation, complexity assessment, and epic decomposition. You ask precise questions, validate assumptions explicitly, and never infer requirements from incomplete information.
```
**Impact:** Significantly improved requirements quality, domain-appropriate questioning.

#### Finding 4.2: No Role Context in ideate.md Command
**Status:** FAIL | **Severity:** Medium
**File:** `src/claude/commands/ideate.md`, all | **vs Prior:** NEW
**Anthropic Guidance:** > "The right role can turn Claude from a general assistant into your virtual domain expert!" (Source: give-claude-a-role.md, line 11)
**Current State:** Command describes phases and logic but never establishes a role for the orchestrating agent.
**Proposed Fix:** Add: "You are acting as a requirements orchestrator, guiding the user from raw business idea through structured requirements."
**Impact:** More focused command execution.

---

## Category 5: Examples/Multishot

**Overall Status:** FAIL (2 FAIL, 3 PARTIAL)

#### Finding 5.1: No Multishot Examples in SKILL.md
**Status:** FAIL | **Severity:** High
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, all | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "Examples are your secret weapon shortcut for getting Claude to generate exactly what you need... Include 3-5 diverse, relevant examples." (Source: Use-examples-multishot prompting-to-guide-Claudes-behavior.md, lines 9, 12)
**Current State:** Zero input/output examples. No sample discovery sessions, requirement outputs, or epic decompositions.
**Proposed Fix:** Create `references/examples.md` with 2-3 multishot examples for discovery, elicitation, and decomposition phases. Reference from SKILL.md.
**Impact:** Dramatically improved consistency and quality.

#### Finding 5.2: Output Templates Lack Completed Examples
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/references/output-templates.md` | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "Examples are wrapped in `<example>` tags for structure." (Source: Use-examples-multishot prompting-to-guide-Claudes-behavior.md, line 25)
**Current State:** Templates have placeholder variables but no filled-in examples showing expected quality.
**Proposed Fix:** Add at least one completed example for the Completion Summary Template.
**Impact:** Quality anchoring for output.

#### Finding 5.3: No XML Tags for Structural Separation
**Status:** FAIL | **Severity:** High
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, all | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "Use tags like `<instructions>`, `<example>`, and `<formatting>` to clearly separate different parts of your prompt." (Source: use-xml-tags.md, lines 9-11)
**Current State:** Uses only markdown headers and bold markers. No XML tags anywhere.
**Proposed Fix:** Wrap key sections: `<instructions>` for phases, `<context>` for background, `<example>` for any examples, `<output_format>` for expected structure.
**Impact:** Reduced misinterpretation of instructions vs. context.

#### Finding 5.4: Box-Drawing Characters for Display
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 107-109 | **vs Prior:** PERSISTS
**Current State:** Uses `━━━━━━━━` for visual section headers. Acceptable for CLI display.
**Proposed Fix:** None required for display content. Use XML for structural separation instead.

#### Finding 5.5: Domain-Specific Patterns Lack Usage Examples
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/references/domain-specific-patterns.md` | **vs Prior:** NEW
**Anthropic Guidance:** > "Your examples mirror your actual use case" and "cover edge cases" (Source: Use-examples-multishot prompting-to-guide-Claudes-behavior.md, lines 23-24)
**Current State:** Comprehensive domain pattern catalog but no examples of how to USE patterns during elicitation.
**Proposed Fix:** Add "Usage Example" section showing how patterns influence questioning.
**Impact:** Better domain-specific questioning.

---

## Category 6: Long Context Handling

**Overall Status:** PARTIAL (2 PASS, 2 PARTIAL)

#### Finding 6.1: Progressive Disclosure Well-Implemented
**Status:** PASS | **vs Prior:** NEW
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 296-326
**Current State:** 339-line SKILL.md with 15 reference files loaded on-demand. Explicit `Read(file_path=...)` directives. Conformant.

#### Finding 6.2: Some Reference Files Lack Table of Contents
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/references/brainstorm-data-mapping.md` (1027 lines) | **vs Prior:** NEW
**Anthropic Guidance:** > "For reference files longer than 100 lines, include a table of contents at the top." (Source: best-practices.md, lines 374-395)
**Current State:** `brainstorm-data-mapping.md` (1027 lines) has no TOC. Several other large files also missing TOC.
**Proposed Fix:** Add linked TOC to files exceeding 100 lines.
**Impact:** Better navigation during partial reads.

#### Finding 6.3: No XML Wrapping for Multi-Source Inputs
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 96-194 | **vs Prior:** NEW
**Anthropic Guidance:** > "When using multiple documents, wrap each document in `<document>` tags" (Source: long-context-tips.md, lines 17-39)
**Current State:** Brainstorm context, user input, and project mode passed as flat markdown markers without XML structuring.
**Proposed Fix:** Wrap in XML: `<brainstorm_context source="BRAINSTORM-001">`, `<user_input>`, `<project_context>`.
**Impact:** Reduced confusion with multiple data sources in context.

#### Finding 6.4: Queries Placed After Data
**Status:** PASS | **vs Prior:** NEW
**Anthropic Guidance:** > "Queries at the end can improve response quality by up to 30%." (Source: long-context-tips.md, lines 13-15)
**Current State:** Context loaded in Phase 0-1, skill invoked in Phase 2. Conformant.

---

## Category 7: Skill Spec Compliance

**Overall Status:** PARTIAL (2 FAIL, 3 PARTIAL)

#### Finding 7.1: `allowed-tools` Array Format
**Status:** FAIL | **Severity:** Medium | **vs Prior:** PERSISTS
Same as Finding 1.1. Spec requires space-delimited string.

#### Finding 7.2: `Bash(git:*)` Invalid Tool Name
**Status:** FAIL | **Severity:** Medium | **vs Prior:** PERSISTS
Same as Finding 1.2. Spec recognizes only `Bash`.

#### Finding 7.3: `Skill` Not in Spec Tool List
**Status:** PARTIAL | **Severity:** Low | **vs Prior:** PERSISTS
Same as Finding 1.3. Claude Code extension, acceptable but noted.

#### Finding 7.4: `model` Field Format Discrepancy
**Status:** PARTIAL | **Severity:** Low | **vs Prior:** PERSISTS
Same as Finding 1.4.

#### Finding 7.5: Missing `metadata` Section
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 1-16 | **vs Prior:** NEW
**Anthropic Guidance:** > "CRITICAL: Properties like `version`, `author`, `category` MUST be nested under `metadata`" (Source: agent-skills-spec.md, line 142)
**Current State:** No `metadata` section with version, author, or category.
**Proposed Fix:** Add:
```yaml
metadata:
  author: DevForgeAI
  version: "3.0.0"
  category: requirements-discovery
```
**Impact:** Better discoverability and lifecycle management.

---

## Category 8: Command-Skill Separation

**Overall Status:** PARTIAL (3 PARTIAL)

#### Finding 8.1: Command Has 175 Lines of Error Handling Business Logic
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/commands/ideate.md`, lines 365-539 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "SKILL.md serves as an overview that points Claude to detailed materials as needed" (Source: best-practices.md, lines 229-230)
**Current State:** Command contains TRY/CATCH pseudocode, error categorization taxonomy (FILE_MISSING, YAML_PARSE_ERROR, etc.), handler display templates, and recovery action tables. Violates "commands orchestrate, skills implement" stated at command line 568.
**Proposed Fix:** Reduce to: (1) check skill exists, (2) invoke skill, (3) on failure display generic error with pointer to skill's error handling. Move detail to skill references.
**Impact:** Cleaner separation, reduced command size (~175 lines saved).

#### Finding 8.2: Phase 0 Brainstorm Parsing Is Deep Command Logic
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/commands/ideate.md`, lines 19-112 | **vs Prior:** PERSISTS
**Current State:** Command parses YAML frontmatter, extracts 8 fields, builds typed context object. This is implementation logic the skill already handles in Step 0.1-0.2.
**Proposed Fix:** Command should: (1) detect brainstorms exist, (2) ask user which one, (3) pass file path. Skill handles parsing.
**Impact:** Reduced duplication.

#### Finding 8.3: Context Markers Are Fragile String Protocol
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/commands/ideate.md`, lines 211-252 | **vs Prior:** PERSISTS
**Current State:** `**Business Idea:**` markdown bold markers detected via string matching. Fragile if format drifts.
**Proposed Fix:** Use structured YAML block or XML tags for context markers. Document as contract.
**Impact:** Reduces silent failure risk.

---

## Category 9: Error Handling

**Overall Status:** PARTIAL (2 PASS, 3 PARTIAL)

#### Finding 9.1: Monolithic error-handling.md Duplicates Decomposed Files
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/references/error-handling.md` (1063 lines) | **vs Prior:** NEW
**Anthropic Guidance:** > Progressive disclosure — split content (Source: best-practices.md, lines 233-235)
**Current State:** `error-handling.md` (1063 lines) duplicates ~95% of content in `error-type-1` through `error-type-6` files. SKILL.md references decomposed files, not the monolithic one.
**Proposed Fix:** Delete `error-handling.md` or convert to thin redirect index (like `error-handling-index.md` already does).
**Impact:** Eliminates ~1000 lines of duplicated content.

#### Finding 9.2: SKILL.md Omits Error Types 3 and 5
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 260-271 | **vs Prior:** NEW
**Current State:** Error handling section lists only types 1, 2, 4, 6. Types 3 (Complexity Errors) and 5 (Constraint Conflicts) exist on disk but are undiscoverable from SKILL.md.
**Proposed Fix:** Add all 6 types to SKILL.md error list, or note that full list is in `error-handling-index.md`.
**Impact:** All error handlers discoverable.

#### Finding 9.3: Error Types Use Feedback Loops Correctly
**Status:** PASS | **vs Prior:** NEW
**Current State:** All error types implement validate-fix-retry with max retry limits and escalation paths. Conformant.

#### Finding 9.4: Error Reporting Format Is Clear and Tiered
**Status:** PASS | **vs Prior:** NEW
**Current State:** Three templates (auto-corrected, user-resolvable, blocking) with severity tiers. Good UX.

#### Finding 9.5: Self-Validation References Stale Phase Numbers
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/references/self-validation-workflow.md`, line 251 | **vs Prior:** NEW
**Current State:** File header says "Phase 3.3" but line 251 references "Step 6.4" (old numbering).
**Proposed Fix:** Change "References Used in Step 6.4" to "References Used in Phase 3.3".
**Impact:** Terminology consistency.

---

## Category 10: User Interaction Patterns

**Overall Status:** PARTIAL (2 PASS, 3 PARTIAL)

#### Finding 10.1: AskUserQuestion Patterns Well-Structured
**Status:** PASS | **vs Prior:** NEW
**File:** `src/claude/skills/discovering-requirements/references/user-interaction-patterns.md`
**Current State:** 8 documented question patterns with templates covering quantification, scope negotiation, technology discovery, compliance, priority trade-offs, integration probing, brownfield constraints, and risk assessment. Conformant.

#### Finding 10.2: Success Criteria Missing "Copy and Track" Instruction
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/SKILL.md`, lines 282-292 | **vs Prior:** PERSISTS
**Anthropic Guidance:** > "For particularly complex workflows, provide a checklist that Claude can copy into its response and check off as it progresses." (Source: best-practices.md, lines 402-403)
**Current State:** Checklist exists but no instruction for Claude to copy and track it during execution.
**Proposed Fix:** Add: "Copy this checklist into your response at phase start. Update checkboxes as you complete each item:"
**Impact:** Better progress tracking across long sessions.

#### Finding 10.3: No Feedback Loop for Requirements Validation
**Status:** PARTIAL | **Severity:** Medium
**File:** `src/claude/skills/discovering-requirements/references/completion-handoff.md` | **vs Prior:** NEW
**Anthropic Guidance:** > "Common pattern: Run validator -> fix errors -> repeat." (Source: best-practices.md, lines 493-496)
**Current State:** Phase 3.3 validation halts on issues rather than iterating. Validate-halt instead of validate-fix-repeat.
**Proposed Fix:** Add feedback loop: fix automatically where possible, re-validate. Only halt on unfixable critical failures.
**Impact:** Fewer halts from fixable issues.

#### Finding 10.4: Question Fatigue Management Is Strong
**Status:** PASS | **vs Prior:** NEW
**Current State:** Explicit fatigue management: batch questions, defaults for low-priority, skip optional on urgency, "Help me decide" option. Conformant.

#### Finding 10.5: Error Recovery Patterns Lack Multishot Examples
**Status:** PARTIAL | **Severity:** Low
**File:** `src/claude/skills/discovering-requirements/references/user-interaction-patterns.md`, lines 349-384 | **vs Prior:** NEW
**Anthropic Guidance:** > "Examples reduce misinterpretation of instructions" (Source: Use-examples-multishot prompting-to-guide-Claudes-behavior.md, lines 16-18)
**Current State:** Recovery patterns provide templates but no concrete conversation examples showing recovery end-to-end.
**Proposed Fix:** Add 1-2 conversation examples per recovery pattern.
**Impact:** More consistent error recovery.

---

## Prioritized Recommendations

### High Priority (FAIL findings — should fix)

| # | Finding | Severity | Effort | File |
|---|---------|----------|--------|------|
| 1 | 4.1: Add role prompt | High | 15 min | SKILL.md |
| 2 | 5.1: Add multishot examples | High | 1-2 hrs | New references/examples.md |
| 3 | 5.3: Add XML tags for structure | High | 1 hr | SKILL.md, ideate.md |
| 4 | 1.1/7.1: Fix allowed-tools format | High/Med | 5 min | SKILL.md |
| 5 | 1.2/7.2: Replace Bash(git:*) | Medium | 5 min | SKILL.md |
| 6 | 1.5: Fix command allowed-tools | Medium | 5 min | ideate.md |
| 7 | 4.2: Add role to command | Medium | 10 min | ideate.md |
| 8 | 1.3/7.3: Replace Skill with Task | Medium | 5 min | SKILL.md |

### Medium Priority (PARTIAL findings — nice to have)

| # | Finding | Severity | Effort | File |
|---|---------|----------|--------|------|
| 9 | 8.1: Move error handling to skill | Medium | 45 min | ideate.md → references/ |
| 10 | 8.2: Simplify Phase 0 parsing | Medium | 30 min | ideate.md |
| 11 | 9.1: Remove duplicate error-handling.md | Medium | 15 min | references/ |
| 12 | 3.1: Add CoT for complexity scoring | Medium | 30 min | references/ |
| 13 | 3.2: Add XML phase handoffs | Medium | 1 hr | references/ |
| 14 | 6.3: XML wrap multi-source inputs | Medium | 30 min | SKILL.md |
| 15 | 10.2: Add copy-and-track instruction | Medium | 5 min | SKILL.md |
| 16 | 10.3: Add validation feedback loop | Medium | 30 min | references/ |
| 17 | 5.2: Add completed output example | Medium | 30 min | references/ |
| 18 | 5.5: Add domain pattern usage examples | Medium | 30 min | references/ |

### Low Priority (informational / cosmetic)

| # | Finding | File |
|---|---------|------|
| 19 | 1.4/7.4: Standardize model field | SKILL.md, ideate.md |
| 20 | 1.6: Consistent model format | ideate.md |
| 21 | 7.5: Add metadata section | SKILL.md |
| 22 | 8.3: Formalize context marker contract | ideate.md, SKILL.md |
| 23 | 9.2: List all 6 error types in SKILL.md | SKILL.md |
| 24 | 9.5: Fix stale phase reference | self-validation-workflow.md |
| 25 | 6.2: Add TOC to large reference files | Multiple references/ |
| 26 | 3.3: Add guided CoT for probing | discovery-workflow.md |
| 27 | 10.5: Add error recovery examples | user-interaction-patterns.md |
| 28 | 5.4: Box-drawing chars (acceptable) | N/A |

---

## Effort Estimate

| Priority | Count | Estimated Hours |
|----------|-------|-----------------|
| High (FAIL) | 8 | 2.5 |
| Medium (PARTIAL) | 10 | 5.0 |
| Low | 10 | 3.0 |
| **Total** | **28 actionable** | **10.5** |

---

## Prior Analysis Delta Summary

| Status | Count | Details |
|--------|-------|---------|
| RESOLVED | 3 | Gerund naming (2.1), vendor prefix (2.2), SKILL.md line count |
| PERSISTS | 14 | All YAML frontmatter issues, no role prompt, no examples, no XML tags, command bloat |
| NEW | 17 | Long context, user interaction, error handling, multishot gaps |
| PASS (confirmed) | 12 | Progressive disclosure, query placement, question patterns, error loops, fatigue mgmt |

---

## Appendix: Anthropic Reference Documents Read

### Prompt Engineering (16 files)
- `use-xml-tags.md` — XML tag best practices
- `use=xml-tags.md` — Duplicate/variant of above
- `be-clear-and-direct.md` — Clarity guidelines
- `give-claude-a-role.md` — Role prompting guidance
- `overview.md` — Prompt engineering overview
- `pompt-engineering-overview.md` — Variant overview
- `chain-of-thought.md` — CoT patterns
- `chain-of-though.md` — Typo variant of above
- `chain-complex-prompts.md` — Prompt chaining
- `extended-thinking-tips.md` — Extended thinking
- `long-context-tips.md` — Long context handling
- `Use-examples-multishot prompting-to-guide-Claudes-behavior.md` — Multishot examples
- `user-prompt-templates.md` — User prompt templates
- `prompt-generator.md` — Prompt generation
- `prompt-improver.md` — Prompt improvement
- `The-Complete-Guide-to-Building-Skill-for-Claude.pdf` — Comprehensive skill guide (pages 1-40)

### Skills Documentation (7 files)
- `agent-skills-spec.md` — Agent Skills specification
- `overview.md` — Skills overview
- `best-practices.md` — Skills best practices
- `be-clear-and-direct.md` — Skills clarity guide
- `quick-start.md` — Skills quick start
- `skills-for-enterprise.md` — Enterprise skills
- `using-agent-skills-with-the-api.md` — API integration
