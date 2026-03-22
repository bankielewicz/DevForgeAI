# Phase 2 Analysis: /dev Command & devforgeai-development Skill
## Extended Analysis Against Anthropic Online Documentation

**Date:** 2026-02-15
**Extends:** Phase 1 Analysis (serene-plotting-sunrise.md, scored 8.1/10)
**Sources analyzed:** 5 Skills docs + 10 Prompt Engineering docs + Colab notebook (shell only) + PDF guide
**Scope:** Research & analysis only — NO file modifications

---

## 1. New Findings from Online Documentation

### 1A. Critical Findings NOT in the PDF Guide

| # | Finding | Source | Impact on devforgeai-development |
|---|---------|--------|----------------------------------|
| **N1** | **SKILL.md body MUST be under 500 lines** | best-practices.md line 233 | **CRITICAL VIOLATION**: Current SKILL.md is ~1,099 lines (2.2x over limit). Must split content into additional reference files. |
| **N2** | **Description must be third person** | best-practices.md line 188-193 | **VIOLATION**: Current description starts with imperative "Implement features..." Should be "Implements features..." |
| **N3** | **Gerund naming recommended** | best-practices.md line 156 | **STYLE GAP**: `devforgeai-development` doesn't follow gerund form. Preferred: `developing-features` or acceptable as noun-phrase. Low priority since "devforgeai-" prefix is a project convention. |
| **N4** | **References must be ONE level deep from SKILL.md** | best-practices.md lines 345-371 | **VIOLATION**: SKILL.md → `phases/*.md` → `references/*.md` is 2 levels deep. Risk: Claude may use `head -100` on deeply nested files, getting incomplete info. |
| **N5** | **File references >100 lines need table of contents** | best-practices.md lines 373-395 | **GAP**: Phase files (242-457 lines) and reference files (1,068-1,676 lines) lack TOCs. |
| **N6** | **Build evaluations BEFORE writing documentation** | best-practices.md lines 709-737 | **GAP**: No evaluation suite exists for this skill. No test scenarios with expected_behavior defined. |
| **N7** | **Test with Haiku, Sonnet, AND Opus** | best-practices.md lines 123-132 | **GAP**: Skill pins `model: claude-opus-4-6`. Never tested on Sonnet/Haiku. |
| **N8** | **"Degrees of freedom" matching** | best-practices.md lines 57-121 | **INSIGHT**: Skill correctly uses LOW freedom (fragile operations like DB migration = exact scripts) for TDD phases and MEDIUM freedom for implementation choices. Well-aligned. |
| **N9** | **Enterprise: Max 8 skills per API request** | using-agent-skills-with-the-api.md line 75 | N/A for Claude Code (filesystem), but important if skill migrates to API. |
| **N10** | **Enterprise: Separation of duties for review** | skills-for-enterprise.md line 85 | **GAP**: No formal review process for skill updates exists. |
| **N11** | **Enterprise: Evaluation-driven lifecycle** | skills-for-enterprise.md lines 47-77 | **GAP**: No triggering accuracy, isolation, coexistence, or instruction-following evaluations exist. |
| **N12** | **Enterprise: Risk tier assessment** | skills-for-enterprise.md lines 19-29 | The skill executes bash commands, references MCP-style subagents, and has broad file system access — ALL high risk indicators requiring audit. |
| **N13** | **Progressive disclosure architecture** | overview.md lines 40-107 | **STRENGTH**: The skill's 3-level architecture (SKILL.md → phases/*.md → references/*.md) aligns perfectly with Level 1/2/3 loading model. But see N4 re: depth. |

### 1B. Prompt Engineering Findings

| # | PE Principle | Source | Current State | Recommendation |
|---|-------------|--------|---------------|----------------|
| **PE1** | **Be clear and direct** | be-clear-and-direct.md | **EXCELLENT (9/10)**: Explicit DO NOT lists, self-check checklists, HALT triggers, numbered steps. One of the strongest aspects. | Maintain. |
| **PE2** | **XML tags for structure** | use-xml-tags.md | **WEAK (5/10)**: Uses Markdown headers/code blocks but NO XML tags. Docs say XML tags "help Claude parse prompts more accurately, leading to higher-quality outputs." | Add `<phase_requirements>`, `<deviation_protocol>`, `<success_criteria>` tags. |
| **PE3** | **Multishot prompting** | multishot-prompting.md | **ABSENT (2/10)**: Zero input/output examples in SKILL.md. Best practices say "Include 3-5 diverse, relevant examples." | Add 2-3 example scenarios showing good/bad phase execution. |
| **PE4** | **Chain of thought** | chain-of-thought.md | **IMPLICIT (7/10)**: Phase-by-phase execution IS CoT. But no explicit `<thinking>` tags or "think step by step" prompts for decision points. | Add structured CoT for deviation decisions and AC mapping. |
| **PE5** | **Role prompting** | give-claude-a-role.md | **ABSENT (3/10)**: No role assignment in SKILL.md. Docs show role prompting "can dramatically improve performance." | Add: "You are a senior TDD engineer following strict spec-driven development protocols." |
| **PE6** | **Prompt chaining** | chain-complex-prompts.md | **EXCELLENT (9/10)**: The 10-phase architecture IS prompt chaining. Each phase has clear handoff, XML-structured outputs, and single-task goals. | Maintain. Phase files are the "chains." |
| **PE7** | **Long context tips** | long-context-tips.md | **GOOD (7/10)**: Places methodology (constraints) at top before execution instructions. But at 1,099 lines, the "longform data at the top" advice means constraints should be even more front-loaded. | Move success criteria and subagent table higher. |
| **PE8** | **Extended thinking** | extended-thinking-tips.md | **MIXED (5/10)**: Docs say "Claude often performs better with high-level instructions rather than step-by-step prescriptive guidance." SKILL.md is hyper-prescriptive. For Opus, this may over-constrain. | For Opus: reduce prescription in SKILL.md, trust model more. Phase files can remain detailed. |
| **PE9** | **Templates/variables** | user-prompt-templates.md | **GOOD (8/10)**: Uses `${STORY_ID}`, `${STORY_FILE}`, `${MODE}` consistently. | Maintain. |
| **PE10** | **Self-correction chains** | chain-complex-prompts.md lines 47-69 | **PRESENT (8/10)**: TDD Red→Green→Refactor IS a self-correction chain. Phase 04.5 and 05.5 AC verification are review loops. | Consider adding explicit "review your work" prompts at phase transitions. |

---

## 2. Updated Scoring Matrix

### Original 15 Criteria (from PDF guide) — Reassessed

| # | Criterion | Phase 1 Score | Phase 2 Score | Change | Notes |
|---|-----------|:---:|:---:|:---:|-------|
| 1 | YAML Frontmatter | 9 | 9 | — | Name/description within limits. Description point-of-view issue (N2) is minor. |
| 2 | Progressive Disclosure | 9 | 8 | ↓1 | Excellent 3-level architecture, but 2-level nesting depth violates N4 best practice. |
| 3 | Instruction Clarity | 9 | 9 | — | Exceptional clarity with HALT triggers, self-checks. PE1 confirms. |
| 4 | File Organization | 8 | 7 | ↓1 | Good structure but SKILL.md at 1,099 lines violates 500-line limit (N1). |
| 5 | Workflow Design | 9 | 9 | — | 10-phase TDD with CLI gates is best-in-class. PE6 and PE10 confirm. |
| 6 | Error Handling | 8 | 8 | — | Comprehensive with exit code handling, backward compat, HALT triggers. |
| 7 | Subagent Integration | 9 | 9 | — | 12+ subagents with BLOCKING/CONDITIONAL classification. Enterprise-grade. |
| 8 | Security | 7 | 7 | — | HALT triggers for sensitive ops, but N12 notes high risk tier requiring audit. |
| 9 | Testing/Evaluation | 4 | 3 | ↓1 | N6 reveals no evaluation suite exists. N7 shows no multi-model testing. Critical gap. |
| 10 | Documentation | 7 | 7 | — | Good phase docs but README/INTEGRATION_GUIDE are stale (5-phase vs 10-phase). |
| 11 | Token Efficiency | 7 | 5 | ↓2 | N1 (500-line limit) is a hard violation. PE8 suggests less prescription for Opus. |
| 12 | Consistency | 8 | 8 | — | Consistent terminology, display templates, phase patterns throughout. |
| 13 | Conciseness | 6 | 5 | ↓1 | Best practices: "Claude is already very smart. Only add context Claude doesn't already have." Several sections explain TDD basics Claude already knows. |
| 14 | Examples | 5 | 3 | ↓2 | PE3 reveals zero multishot examples. Anthropic strongly recommends 3-5 examples. |
| 15 | Feedback Loops | 9 | 9 | — | TDD cycle, AC verification (4.5/5.5), deferral challenge, code review — excellent. |

### New Criteria (from Online Docs)

| # | Criterion | Score | Source | Notes |
|---|-----------|:---:|--------|-------|
| 16 | XML Tag Usage | 5/10 | use-xml-tags.md | Uses markdown not XML. PE2 shows XML improves accuracy. |
| 17 | Role Assignment | 3/10 | give-claude-a-role.md | No role prompt. PE5 shows dramatic performance improvement. |
| 18 | Extended Thinking Alignment | 5/10 | extended-thinking-tips.md | Over-prescriptive for Opus. PE8 suggests high-level first. |
| 19 | Enterprise Readiness | 5/10 | skills-for-enterprise.md | No eval suite, no separation of duties, no risk assessment. |
| 20 | Reference Depth Compliance | 6/10 | best-practices.md | 2-level nesting. Should be 1-level from SKILL.md. |
| 21 | TOC for Long Files | 4/10 | best-practices.md | Phase files (242-457 lines) and reference files lack TOCs. |

### Composite Scores

| Category | Phase 1 | Phase 2 | Delta |
|----------|:---:|:---:|:---:|
| **Original 15 criteria** | 8.1/10 | 7.4/10 | -0.7 |
| **New 6 criteria** | N/A | 4.7/10 | N/A |
| **Combined 21 criteria** | N/A | **6.7/10** | N/A |

**Score decreased because:** The online documentation revealed hard requirements (500-line limit, 1-level reference depth, evaluation suites, multishot examples) that the PDF guide only hinted at. The skill's architectural strengths remain excellent, but compliance gaps are now measurable.

---

## 3. Prompt Engineering Assessment

### 3A. SKILL.md Prompt Quality

**Strengths (what Anthropic would praise):**
- **Sequential numbered steps** in every phase → Aligns with "be clear and direct" (provide instructions as sequential steps)
- **Explicit DO NOT lists** → Aligns with "be specific about what you want Claude to do"
- **Phase chaining** → Perfect alignment with "chain complex prompts"
- **Self-correction loops** → TDD Red→Green→Refactor, AC verification passes
- **Variable templates** → `${STORY_ID}`, `${STORY_FILE}` used consistently
- **Conditional workflows** → Clear decision trees for deviation protocol, resume logic

**Weaknesses (what Anthropic would flag):**

1. **No XML tags in SKILL.md body** — The entire 1,099-line file uses only Markdown. Per use-xml-tags.md: "XML tags help Claude parse your prompts more accurately, leading to higher-quality outputs." Key sections that should use XML:
   - `<execution_model>` for the inline execution instructions
   - `<deviation_protocol>` for the consent workflow
   - `<phase_requirements>` for the subagent table
   - `<success_criteria>` for completion checklist

2. **No multishot examples** — Per multishot-prompting.md: "Include 3-5 diverse, relevant examples to show Claude exactly what you want." The SKILL.md has zero examples of:
   - What a successful phase completion looks like
   - What a deviation request looks like
   - What a HALT scenario looks like

3. **No role prompt** — Per give-claude-a-role.md: "Using the system parameter to give it a role... can dramatically improve performance." The skill should start with a role like: "You are an expert TDD engineer executing a spec-driven development workflow."

4. **Over-prescription for Opus** — Per extended-thinking-tips.md: "Claude often performs better with high-level instructions rather than step-by-step prescriptive guidance. The model's creativity in approaching problems may exceed a human's ability to prescribe the optimal thinking process." The SKILL.md's hyper-detailed execution model (self-check boxes, "EXECUTE NOW" instructions) may actually degrade Opus performance.

### 3B. Subagent Prompt Templates in Phase Files

**Evaluated:** phase-01-preflight.md, phase-02-test-first.md

**Finding:** Subagent prompts are terse but functional:
```
Task(
  subagent_type="test-automator",
  description="Generate failing tests for ${STORY_ID}",
  prompt="Generate failing tests from acceptance criteria..."
)
```

**Against prompt engineering best practices:**
- ✅ Clear and direct — tells subagent exactly what to do
- ❌ No role assignment for subagents — should include "You are a TDD test generation specialist"
- ❌ No examples — subagent prompts should include an example of expected output format
- ❌ No XML-tagged context — story data should be wrapped in `<story>` tags
- ❌ No explicit output format — should specify "Output your tests in `<test_code>` tags"

**Recommended subagent prompt template:**
```
Task(
  subagent_type="test-automator",
  description="Generate failing tests for ${STORY_ID}",
  prompt="""
  You are a TDD test generation specialist.

  <story>${STORY_FILE_CONTENT}</story>
  <constraints>${CODING_STANDARDS}</constraints>

  Generate failing tests from the acceptance criteria above.

  Requirements:
  1. Each AC must have at least one test
  2. Tests MUST fail initially (Red phase)
  3. Follow naming: test_<function>_<scenario>_<expected>

  <example>
  Input AC: "User can log in with valid credentials"
  Output:
  def test_login_valid_credentials_returns_token():
      result = auth_service.login("user@test.com", "password123")
      assert result.token is not None
  </example>

  Output your tests in <test_code> tags.
  """
)
```

---

## 4. Updated Recommendations (Merged & Re-Prioritized)

### Priority 1 (CRITICAL — Hard Violations)

**R1: Split SKILL.md below 500-line limit**
- **Source:** best-practices.md line 233, N1
- **Current:** 1,099 lines
- **Action:** Extract Phase Completion Displays (~100 lines), Workflow Execution Checklist (~100 lines), TodoWrite-Gate Integration (~40 lines), Technical Debt Override (~30 lines) into `references/` files
- **Target:** SKILL.md ≤ 450 lines (with buffer)
- **Effort:** Medium (2-3 hours)
- **Files to modify:**
  - `.claude/skills/devforgeai-development/SKILL.md` — shrink from 1,099 → ~450 lines
  - `.claude/skills/devforgeai-development/references/phase-completion-displays.md` — new
  - `.claude/skills/devforgeai-development/references/todowrite-gate-pattern.md` — new
  - `.claude/skills/devforgeai-development/references/debt-override-banner.md` — new

**R2: Flatten reference depth to 1 level**
- **Source:** best-practices.md lines 345-371, N4
- **Current:** SKILL.md → phases/*.md → references/*.md (2 levels)
- **Action:** SKILL.md should directly reference all critical content. Phase files can still exist but SKILL.md must provide a direct "See [reference.md]" for each critical reference, not just "See phase file which then references..."
- **Effort:** Medium (1-2 hours)

### Priority 2 (HIGH — Significant Quality Improvement)

**R3: Add XML tags to SKILL.md**
- **Source:** use-xml-tags.md, PE2
- **Action:** Wrap key sections in XML tags:
  - `<execution_model>` for inline execution instructions
  - `<phase_brief>` for phase summary table
  - `<subagent_requirements>` for per-phase subagent table
  - `<success_criteria>` for completion checklist
- **Effort:** Low (1 hour)

**R4: Add role prompt to SKILL.md header**
- **Source:** give-claude-a-role.md, PE5
- **Action:** Add after frontmatter: "You are an expert TDD software engineer executing a spec-driven development workflow. You prioritize test quality, architectural compliance, and zero technical debt."
- **Effort:** Low (15 minutes)

**R5: Add 3 multishot examples**
- **Source:** multishot-prompting.md, PE3
- **Action:** Add to a new `references/execution-examples.md`:
  1. Example: Successful phase-02 execution (showing test generation from AC)
  2. Example: Deviation request (showing AskUserQuestion flow)
  3. Example: HALT scenario (showing what triggers HALT and recovery)
- SKILL.md links: "For execution examples, see [execution-examples.md]"
- **Effort:** Medium (2 hours)

**R6: Build evaluation suite**
- **Source:** best-practices.md lines 709-737, skills-for-enterprise.md, N6
- **Action:** Create 5 evaluation scenarios:
  1. Standard story implementation (happy path)
  2. Story with dependency conflicts (should HALT)
  3. Story with missing context files (should invoke architecture skill)
  4. Resume from interrupted session
  5. Remediation mode with gaps.json
- **Effort:** High (4-6 hours)

### Priority 3 (MEDIUM — Polish)

**R7: Fix description point-of-view**
- **Source:** best-practices.md lines 188-193, N2
- **Current:** "Implement features using TDD..."
- **Fix:** "Implements features using Test-Driven Development (TDD) while enforcing architectural constraints from context files. Use when implementing user stories, building features, or writing code that must comply with tech-stack.md, source-tree.md, and dependencies.md."
- **Effort:** Trivial (5 minutes)

**R8: Add TOCs to files >100 lines**
- **Source:** best-practices.md lines 373-395, N5
- **Action:** Add `## Contents` section to all phase files and reference files exceeding 100 lines
- **Effort:** Low (1-2 hours)

**R9: Reduce over-prescription for Opus**
- **Source:** extended-thinking-tips.md, PE8
- **Action:** The "Immediate Execution Checkpoint" section (lines 72-103) with self-check boxes telling Claude NOT to ask questions may actually cause Opus to second-guess itself. Consider replacing with a shorter, higher-level directive: "Execute phases sequentially. Do not pause for confirmation between phases."
- **Effort:** Low (30 minutes)

**R10: Update stale documentation**
- **Current:** README.md (350 lines) and INTEGRATION_GUIDE.md (567 lines) describe 5-phase workflow
- **Action:** Update to reflect current 10-phase architecture or mark as deprecated
- **Effort:** Medium (2-3 hours)

### Priority 4 (LOW — Future Improvement)

**R11: Enhance subagent prompt templates**
- **Source:** be-clear-and-direct.md, use-xml-tags.md, give-claude-a-role.md
- **Action:** Add role prompts, XML tags, and examples to all subagent Task() calls in phase files
- **Effort:** High (6-8 hours, 12 subagents × 10 phases)

**R12: Add enterprise review process**
- **Source:** skills-for-enterprise.md, N10, N11
- **Action:** Create review checklist, separation of duties for skill updates
- **Effort:** Medium (2-3 hours)

---

## 5. Enterprise Readiness Assessment

### Assessment Against skills-for-enterprise.md

| Dimension | Status | Score | Notes |
|-----------|--------|:---:|-------|
| **Security Review** | ⚠️ Partial | 6/10 | HALT triggers for sensitive ops, but no formal risk tier classification. Bash commands = High risk. |
| **Triggering Accuracy** | ✅ Good | 8/10 | Clear description with specific trigger words ("implementing user stories, building features"). |
| **Isolation Behavior** | ✅ Good | 8/10 | Skill works standalone. Dependencies (context files) are validated in Phase 01. |
| **Coexistence** | ✅ Good | 8/10 | Description is specific enough to avoid stealing triggers from other skills. |
| **Instruction Following** | ✅ Excellent | 9/10 | Hyper-detailed instructions with validation gates ensure high compliance. |
| **Output Quality** | ✅ Good | 8/10 | CLI gates and subagent checks enforce quality. |
| **Evaluation Suite** | ❌ Missing | 1/10 | No eval scenarios exist. Critical gap for enterprise deployment. |
| **Version Management** | ⚠️ Basic | 5/10 | Git-tracked but no formal versioning strategy (pinned versions, rollback plan). |
| **Skill Lifecycle** | ⚠️ Informal | 4/10 | No plan/review/test/deploy/monitor/iterate cycle documented. |
| **Risk Assessment** | ❌ Missing | 2/10 | No formal risk tier classification despite high-risk indicators (bash, file access). |

**Enterprise Readiness Score: 5.9/10**

**Blocking items for enterprise deployment:**
1. No evaluation suite
2. No formal risk assessment
3. No version pinning/rollback strategy
4. SKILL.md exceeds 500-line limit

---

## 6. Cross-Reference Summary

| Source URL/File | Key Insight | Impact | Recommendation |
|-----------------|-------------|--------|----------------|
| **skills/overview.md** | 3-level progressive disclosure architecture | Validates skill's phase-file approach | Ensure SKILL.md is the primary hub (1-level depth) |
| **skills/best-practices.md** | 500-line SKILL.md limit | CRITICAL violation (1,099 lines) | R1: Split to <450 lines |
| **skills/best-practices.md** | 1-level reference depth | Violation (2 levels deep) | R2: Flatten references |
| **skills/best-practices.md** | Gerund naming convention | Style gap (minor) | Low priority |
| **skills/best-practices.md** | Third-person description | Point-of-view violation | R7: Fix to "Implements..." |
| **skills/best-practices.md** | Evaluation-driven development | No eval suite exists | R6: Build 5 evaluation scenarios |
| **skills/best-practices.md** | Multi-model testing | Only tested on Opus | R6 also covers this |
| **skills/best-practices.md** | TOC for files >100 lines | Phase files lack TOCs | R8: Add TOCs |
| **skills/best-practices.md** | Degrees of freedom matching | Already well-aligned | No action |
| **skills/quick-start.md** | Basic skill structure | Confirmed compliance | No action |
| **skills/skills-for-enterprise.md** | Risk tier assessment | High risk (bash, file access) | R12: Add risk classification |
| **skills/skills-for-enterprise.md** | Separation of duties | No review process | R12: Add review process |
| **skills/skills-for-enterprise.md** | Evaluation lifecycle | No eval-driven lifecycle | R6, R12 |
| **skills/using-agent-skills-with-the-api.md** | Max 8 skills per request | N/A for Claude Code | Future API portability consideration |
| **prompt-engineering/be-clear-and-direct.md** | Explicit, numbered instructions | Already excellent | Maintain |
| **prompt-engineering/use-xml-tags.md** | XML tags improve accuracy | Not used in SKILL.md | R3: Add XML tags |
| **prompt-engineering/multishot-prompting.md** | 3-5 examples recommended | Zero examples | R5: Add 3 examples |
| **prompt-engineering/chain-of-thought.md** | Structured CoT with `<thinking>` tags | Implicit but not explicit | R3 partially addresses |
| **prompt-engineering/give-claude-a-role.md** | Role prompts boost performance | No role assigned | R4: Add role prompt |
| **prompt-engineering/chain-complex-prompts.md** | Multi-step prompt chaining | Already excellent (10 phases) | Maintain |
| **prompt-engineering/long-context-tips.md** | Data at top, query at bottom | Mostly aligned | R1 will improve by shrinking SKILL.md |
| **prompt-engineering/extended-thinking-tips.md** | High-level > prescriptive for Opus | Over-prescriptive currently | R9: Reduce prescription |
| **prompt-engineering/prompt-generator.md** | Meta-prompt techniques | Consider for subagent prompts | R11 (low priority) |
| **prompt-engineering/prompt-improver.md** | CoT refinement + XML organization | Pattern to follow for R3 | Apply during R3 implementation |
| **prompt-engineering/user-prompt-templates.md** | Template variables pattern | Already well-implemented | Maintain |

---

## 7. Key Questions Answered

### Does the online documentation introduce NEW skill design requirements not in the PDF?
**YES — 3 hard requirements:**
1. **500-line SKILL.md limit** — explicit numeric threshold not in PDF
2. **1-level reference depth** — explicit architectural constraint not in PDF
3. **Third-person description** — explicit grammar requirement not in PDF

### Do prompt engineering guides suggest changes to SKILL.md instructions?
**YES — 4 specific changes:**
1. Add XML tags (PE2)
2. Add role prompt (PE5)
3. Add multishot examples (PE3)
4. Reduce prescription for Opus (PE8)

### Do subagent prompt templates follow prompt engineering best practices?
**NO — 4 gaps:**
1. No role prompts in Task() calls
2. No XML-tagged context data
3. No output format specification
4. No examples of expected output

### Are there enterprise-specific requirements?
**YES — 4 blocking items:**
1. Evaluation suite (3-5 scenarios minimum)
2. Risk tier assessment
3. Version management strategy
4. Review separation of duties

### Does extended thinking tips apply?
**YES — key insight:** For Opus, high-level directives outperform hyper-prescriptive step-by-step instructions. The SKILL.md's "Immediate Execution Checkpoint" with self-check boxes may be counterproductive.

### Do long context tips apply given SKILL.md's ~8,800 word size?
**YES — key insight:** At 1,099 lines (~8,800 words), the skill is well into "long context" territory. The advice to "put longform data at the top, query at the bottom" validates the current architecture of placing methodology first, execution later. But the 500-line limit means most of this content should be in reference files.

---

## 8. Implementation Roadmap

| Phase | Recommendations | Effort | New Score (est.) |
|-------|----------------|--------|:---:|
| **Sprint 1** | R1 (500-line split), R7 (description fix) | 2-3 hours | 7.3/10 |
| **Sprint 2** | R3 (XML tags), R4 (role prompt), R9 (reduce prescription) | 2 hours | 7.8/10 |
| **Sprint 3** | R2 (flatten refs), R5 (examples), R8 (TOCs) | 4-5 hours | 8.3/10 |
| **Sprint 4** | R6 (evaluation suite), R10 (stale docs) | 6-8 hours | 8.8/10 |
| **Sprint 5** | R11 (subagent prompts), R12 (enterprise review) | 8-10 hours | 9.2/10 |

**Target: 9.2/10 after all sprints (up from 6.7/10 current combined score)**

---

## Appendix A: Files Analyzed

### Skills Documentation (read from local filesystem)
- `.claude/skills/claude-code-terminal-expert/references/skills/overview.md` (345 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` (1,140 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/quick-start.md` (527 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/skills-for-enterprise.md` (166 lines)
- `.claude/skills/claude-code-terminal-expert/references/skills/using-agent-skills-with-the-api.md` (1,572 lines)

### Prompt Engineering Documentation (read from local filesystem)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/overview.md` (72 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/be-clear-and-direct.md` (68 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/use=xml-tags.md` (66 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-of-though.md` (92 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/long-context-tips.md` (87 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/extended-thinking-tips.md` (399 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/chain-complex-prompts.md` (140 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/Use-examples-multishot prompting-to-guide-Claudes-behavior.md` (50 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/prompt-generator.md` (36 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/prompt-improver.md` (153 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/give-claude-a-role.md` (110 lines)
- `.claude/skills/claude-code-terminal-expert/references/prompt-engineering/user-prompt-templates.md` (57 lines)

### Skill Files Analyzed
- `.claude/commands/dev.md` (258 lines)
- `.claude/skills/devforgeai-development/SKILL.md` (~1,099 lines, read in 3 chunks)
- `.claude/skills/devforgeai-development/phases/phase-01-preflight.md` (80+ lines read)
- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md` (80+ lines read)

### Colab Notebook
- `https://colab.research.google.com/drive/1SoAajN8CBYTl79VyTwxtxncfCWlHlyy9` — WebFetch returned only Colab shell HTML, no notebook content. The prompt-generator.md already covers the metaprompt approach.

---

## Phase 3: Skill Rename & Command Backup Migration

**Date:** 2026-02-15
**Status:** PLAN ONLY — No files modified
**Prerequisite:** Phase 2 analysis complete (above)
**Source:** best-practices.md line 156 (gerund naming), N3 finding from Phase 2

---

### 3.1 Problem Statement

The current skill name `devforgeai-development` is generic and doesn't describe the activity/capability the skill provides. Per Anthropic's best practices (Source: best-practices.md, lines 156-181):

> "We recommend using **gerund form** (verb + -ing) for Skill names, as this clearly describes the activity or capability the Skill provides."

The name "development" is:
- **Vague** — could mean anything (documentation development, test development, architecture development)
- **Not gerund** — "development" is a noun, not a gerund (verb+-ing)
- **Poor signal for `/dev`** — Claude needs to intuitively connect the `/dev` command to this skill's TDD implementation workflow

### 3.1A Constitutional Conflict & ADR Requirement

**⚠️ HALT TRIGGER IDENTIFIED:** The proposed gerund rename conflicts with **two LOCKED context files**.

#### Conflicting Constitutional Definitions

**source-tree.md, line 834** (Status: LOCKED, Version 3.8):
> **Pattern**: `devforgeai-[phase]`
> **Examples**: `discovering-requirements`, `designing-systems`, `devforgeai-development`

**coding-standards.md, line 117** (Status: LOCKED, Version 1.2):
> **Skills**: `devforgeai-[phase]`

Both documents define the skill naming convention as `devforgeai-[phase]` where `[phase]` is a single-word lifecycle phase noun (ideation, architecture, development, qa, release). The proposed name `devforgeai-implementing-stories` is a gerund+noun phrase — not a `[phase]` name — and therefore **violates both LOCKED conventions**.

#### Additional Constitutional References Requiring Update

| Context File | Lines | Current Reference | Impact |
|-------------|-------|-------------------|--------|
| **source-tree.md** | 113, 559, 569, 582-591 | Directory listing `devforgeai-development/` with full subdirectory tree | Must update directory tree AND naming convention pattern |
| **source-tree.md** | 834-841 | Naming convention examples with `devforgeai-development` as ✅ CORRECT | Must update pattern definition and all examples |
| **source-tree.md** | 906-913 | Forbidden Patterns "Correct" example lists `devforgeai-development/` | Must update example |
| **coding-standards.md** | 117 | `Skills: devforgeai-[phase]` | Must update pattern definition |
| **architecture-constraints.md** | 31-33 | `devforgeai-development: TDD implementation only` | Must update skill name reference |
| **anti-patterns.md** | 42-47 | `devforgeai-development/` in correct examples for modular skills | Must update example |
| **tech-stack.md** | 365 | Path reference `devforgeai-development/phases/phase-01-preflight.md` | Must update path |

#### Resolution: ADR Required (Critical Rule #4, #9)

Per Critical Rule #4 (*"Context files are immutable. Changes require Architecture Decision Records."*) and Critical Rule #9 (*"Document all decisions in ADRs."*):

**An ADR MUST be created BEFORE the rename execution.** This ADR establishes the new naming convention for ALL `devforgeai-*` skills, not just this one.

**Proposed ADR:** `ADR-017-skill-gerund-naming-convention.md`

**ADR Scope:**
- **Decision:** Adopt Anthropic's recommended gerund naming convention for all `devforgeai-*` skills
- **Old Convention:** `devforgeai-[phase]` (single-word noun: development, architecture, ideation)
- **New Convention:** `devforgeai-[gerund-phrase]` (verb+-ing descriptor: implementing-stories, validating-quality, creating-stories)
- **Rationale:** Anthropic best practices (best-practices.md line 156); improved Claude skill discovery; clearer activity description
- **Migration Strategy:** MVP migration of `devforgeai-development` first; remaining skills migrated in subsequent stories
- **Context File Updates Required:** source-tree.md (naming convention pattern, directory tree, examples), coding-standards.md (naming convention), architecture-constraints.md (skill references), anti-patterns.md (examples), tech-stack.md (path references)

**ADR must be approved BEFORE Step 1 of the Migration Execution Order (Section 3.7).**

### 3.2 Name Candidates

| # | Candidate Name | Form | Pros | Cons |
|---|---------------|------|------|------|
| **A** | `devforgeai-implementing-stories` | Gerund | ✅ Exactly describes primary action; ✅ matches `/dev STORY-XXX` invocation pattern; ✅ gerund form per best practices; ✅ "implementing" + "stories" are the two key trigger words users say ("implement this story") | Slightly long (32 chars, well within 64-char limit) |
| **B** | `devforgeai-tdd-implementing` | Gerund | ✅ Highlights TDD methodology; ✅ gerund form; ✅ differentiates from non-TDD implementation | ❌ "tdd-implementing" is awkward grammar; ❌ doesn't mention stories (the primary input) |
| **C** | `devforgeai-developing-features` | Gerund | ✅ Clean gerund; ✅ aligns with "develop a feature" user intent; ✅ broader than stories alone | ❌ Still somewhat generic ("developing" is close to "development"); ❌ skill doesn't develop "features" — it implements *stories* |
| **D** | `devforgeai-story-implementing` | Noun-Gerund | ✅ Concise; ✅ clearly about stories; ✅ noun-phrase variant is "acceptable" per best practices | ❌ Not pure gerund form; ❌ reads slightly unnaturally |
| **E** | `devforgeai-implementing-tdd` | Gerund | ✅ Highlights TDD; ✅ gerund form | ❌ Sounds like "implementing TDD itself" rather than "using TDD to implement"; ❌ misleading semantics |

### 3.3 Recommended Name: `devforgeai-implementing-stories`

**Rationale:**

1. **Gerund form** ✅ — "implementing" is the gerund of "implement", matching best-practices.md line 156
2. **Descriptive** ✅ — tells Claude exactly what this skill does: it *implements stories*
3. **Trigger alignment** ✅ — when a user says "implement STORY-401" or `/dev STORY-401`, Claude sees "implementing-stories" in the skill list and immediately connects the dots
4. **Consistent with project convention** ✅ — keeps the `devforgeai-` prefix
5. **Within limits** ✅ — 32 characters (max 64)
6. **No reserved words** ✅ — no "anthropic" or "claude"
7. **Semantic precision** — differentiates from `devforgeai-story-creation` (which *creates* stories) vs this skill which *implements* them

**Constitutional Conflict Acknowledged (see Section 3.1A):**
This name departs from the current LOCKED `devforgeai-[phase]` convention. ADR-017 MUST be created and approved before execution. The ADR establishes `devforgeai-[gerund-phrase]` as the new naming standard for all skills.

**Updated YAML frontmatter would be:**
```yaml
---
name: devforgeai-implementing-stories
description: Implements user stories using Test-Driven Development (TDD) while enforcing architectural constraints from context files. Use when implementing user stories, building features, or writing code that must comply with tech-stack.md, source-tree.md, and dependencies.md. Automatically invokes designing-systems skill if context files are missing.
---
```

Note: Description also updated to third-person ("Implements" not "Implement") per N2/R7 finding.

---

### 3.4 Command Backup Plan

#### 3.4.1 Backup Before Rename

Before ANY rename operation:

```
1. Backup dev.md:
   cp .claude/commands/dev.md .claude/commands/dev.md.backup-pre-rename-2026-02-15

2. Backup SKILL.md:
   cp .claude/skills/devforgeai-development/SKILL.md .claude/skills/devforgeai-development/SKILL.md.backup-pre-rename-2026-02-15
```

#### 3.4.2 References Inside dev.md That Need Updating

| Line(s) | Current Reference | New Reference |
|---------|-------------------|---------------|
| 152 | `Skill(command="devforgeai-development")` | `Skill(command="devforgeai-implementing-stories")` |
| 161-167 | File paths `.claude/skills/devforgeai-development/...` | `.claude/skills/devforgeai-implementing-stories/...` |

#### 3.4.3 Other Files Referencing dev.md

The `/dev` command file (`dev.md`) is referenced from:
- `CLAUDE.md` (key entry points table)
- `.claude/memory/commands-reference.md`
- Various story files and plans

**The dev.md filename itself does NOT change** — only internal references to the skill name change.

---

### 3.5 Migration Checklist — Complete Reference Inventory

**Scope:** Every file that contains the string `devforgeai-development` needs updating. Files categorized by criticality.

#### Tier 0: PREREQUISITE — ADR + Constitutional Convention Updates (MUST complete first)

**These changes establish the legal basis for the rename. Without them, the rename violates LOCKED context files.**

| # | File | Change Type | Scope |
|---|------|------------|-------|
| 0a | `devforgeai/specs/adrs/ADR-017-skill-gerund-naming-convention.md` | **CREATE** new ADR | Decision record for `devforgeai-[phase]` → `devforgeai-[gerund-phrase]` convention change |
| 0b | `devforgeai/specs/context/source-tree.md` | **UPDATE** naming convention | Line 834: `devforgeai-[phase]` → `devforgeai-[gerund-phrase]`; Lines 838-841: update examples; Lines 113, 582-591: update directory tree; Lines 906-913: update Forbidden Patterns examples |
| 0c | `devforgeai/specs/context/coding-standards.md` | **UPDATE** naming convention | Line 117: `devforgeai-[phase]` → `devforgeai-[gerund-phrase]`; Update examples |
| 0d | `devforgeai/specs/context/architecture-constraints.md` | **UPDATE** skill reference | Lines 31-33: `devforgeai-development` → `devforgeai-implementing-stories` |
| 0e | `devforgeai/specs/context/anti-patterns.md` | **UPDATE** examples | Lines 42-47: update `devforgeai-development/` in correct modular example |
| 0f | `devforgeai/specs/context/tech-stack.md` | **UPDATE** path reference | Line 365: update path to new skill directory |
| 0g | `.claude/memory/Constitution/source-tree.md` | **UPDATE** mirror | Mirror changes from 0b |
| 0h | `.claude/memory/Constitution/coding-standards.md` | **UPDATE** mirror | Mirror changes from 0c |
| 0i | `.claude/memory/Constitution/architecture-constraints.md` | **UPDATE** mirror | Mirror changes from 0d |
| 0j | `.claude/memory/Constitution/anti-patterns.md` | **UPDATE** mirror | Mirror changes from 0e |
| 0k | `.claude/memory/Constitution/tech-stack.md` | **UPDATE** mirror | Mirror changes from 0f |

**Naming Convention Update Detail (source-tree.md line 834 + coding-standards.md line 117):**

Current (LOCKED):
```markdown
**Pattern**: `devforgeai-[phase]`
**Examples**:
- ✅ `discovering-requirements`
- ✅ `designing-systems`
- ✅ `devforgeai-development`
- ❌ `IdeationSkill` (no CamelCase)
- ❌ `dev-skill` (use full phase name)
```

New (after ADR-017):
```markdown
**Pattern**: `devforgeai-[gerund-phrase]` (per ADR-017, Anthropic best-practices.md line 156)
**Examples**:
- ✅ `devforgeai-implementing-stories` (gerund form — preferred)
- ✅ `discovering-requirements` (legacy noun form — accepted until migrated)
- ✅ `designing-systems` (legacy noun form — accepted until migrated)
- ❌ `IdeationSkill` (no CamelCase)
- ❌ `dev-skill` (use descriptive gerund phrase)

**Migration Status**: See Section 3.12 for full-fleet gerund migration roadmap.
Legacy noun-form names are accepted during the migration period.
New skills MUST use gerund form from ADR-017 forward.
```

**Version Bumps Required:**
- source-tree.md: 3.8 → 3.9
- coding-standards.md: 1.2 → 1.3
- architecture-constraints.md: 1.0 → 1.1
- anti-patterns.md: 1.1 → 1.2
- tech-stack.md: 1.4 → 1.5

#### Tier 1: CRITICAL — Must update for skill to function (breaks if skipped)

| # | File | Reference Type | Count | Notes |
|---|------|---------------|-------|-------|
| 1 | `.claude/skills/devforgeai-development/SKILL.md` | `name:` in frontmatter | 1 | **The rename itself** — directory must also move |
| 2 | `.claude/commands/dev.md` | `Skill(command="...")` + file paths | ~6 | Primary invocation point |
| 3 | `.claude/commands/resume-dev.md` | `Skill(command="...")` + file paths | ~3 | Resume command |
| 4 | `.claude/commands/orchestrate.md` | `Skill(command="...")` + file paths | ~3 | Orchestration invocation |

**Directory rename required:**
```
.claude/skills/devforgeai-development/ → .claude/skills/devforgeai-implementing-stories/
src/claude/skills/devforgeai-development/ → src/claude/skills/devforgeai-implementing-stories/
```

#### Tier 2: HIGH — Affects system-prompt skill list and subagent context

| # | File | Reference Type | Count |
|---|------|---------------|-------|
| 5 | `CLAUDE.md` | Skill references, key entry points, subagent registry | ~8 |
| 6 | `src/CLAUDE.md` | Mirror of CLAUDE.md | ~8 |
| 7 | `.claude/memory/skills-reference.md` | Skill catalog entry | ~5 |
| 8 | `.claude/memory/commands-reference.md` | Command → skill mapping | ~3 |

**Note:** Constitution files (source-tree.md, coding-standards.md, etc.) moved to Tier 0 above.

#### Tier 3: MEDIUM — Subagent files that reference this skill

| # | File | Count |
|---|------|-------|
| 15 | `.claude/agents/dev-result-interpreter.md` | ~3 |
| 16 | `.claude/agents/framework-analyst.md` | ~3 |
| 17 | `.claude/agents/observation-extractor.md` | ~2 |
| 18 | `.claude/agents/git-validator.md` | ~2 |
| 19 | `.claude/agents/git-worktree-manager.md` | ~2 |
| 20 | `.claude/agents/backend-architect.md` | ~2 |
| 21 | `.claude/agents/frontend-developer.md` | ~2 |
| 22 | `.claude/agents/code-reviewer.md` | ~2 |
| 23 | `.claude/agents/refactoring-specialist.md` | ~2 |
| 24 | `.claude/agents/integration-tester.md` | ~2 |
| 25 | `.claude/agents/test-automator.md` | ~2 |
| 26 | `.claude/agents/tech-stack-detector.md` | ~2 |
| 27 | `.claude/agents/sprint-planner.md` | ~2 |
| 28 | `.claude/agents/agent-generator.md` | ~2 |
| 29 | `.claude/agents/internet-sleuth.md` | ~2 |
| 30 | `.claude/agents/documentation-writer.md` | ~2 |
| 31 | `.claude/agents/ac-compliance-verifier.md` | ~2 |
| 32 | `.claude/agents/context-validator.md` | ~2 |
| 33 | `.claude/agents/deferral-validator.md` | ~2 |
| 34 | `.claude/agents/dependency-graph-analyzer.md` | ~2 |
| 35 | `.claude/agents/file-overlap-detector.md` | ~2 |
| 36 | `.claude/agents/requirements-analyst.md` | ~2 |
| 37 | `.claude/agents/requirements-analyst/references/story-format-template.md` | ~1 |
| 38 | `.claude/agents/agent-generator/references/canonical-agent-template.md` | ~1 |
| 39 | `.claude/agents/agent-generator/references/template-patterns.md` | ~1 |

**+ `src/claude/agents/` mirrors** — each of the above has a corresponding `src/` copy (~24 files)

#### Tier 4: LOW — Other skills, references, rules, memory files

| # | File | Count |
|---|------|-------|
| 40 | `.claude/skills/devforgeai-qa/SKILL.md` | ~3 |
| 41 | `.claude/skills/devforgeai-orchestration/references/*.md` | ~8 |
| 42 | `.claude/skills/devforgeai-story-creation/SKILL.md` | ~2 |
| 43 | `.claude/skills/devforgeai-story-creation/references/*.md` | ~4 |
| 44 | `.claude/skills/discovering-requirements/SKILL.md` | ~2 |
| 45 | `.claude/skills/devforgeai-rca/SKILL.md` | ~2 |
| 46 | `.claude/skills/devforgeai-rca/references/*.md` | ~5 |
| 47 | `.claude/skills/designing-systems/SKILL.md` | ~2 |
| 48 | `.claude/skills/devforgeai-documentation/SKILL.md` | ~2 |
| 49 | `.claude/skills/devforgeai-ui-generator/SKILL.md` | ~2 |
| 50 | `.claude/skills/devforgeai-subagent-creation/SKILL.md` | ~2 |
| 51 | `.claude/skills/devforgeai-shared/shared-phase-0-loader.md` | ~2 |
| 52 | `.claude/skills/devforgeai-feedback/references/*.md` | ~4 |
| 53 | `.claude/skills/claude-code-terminal-expert/references/*.md` | ~3 |
| 54 | `.claude/rules/workflow/commit-failure-recovery.md` | ~2 |
| 55 | `.claude/rules/core/citation-requirements.md` | ~1 |
| 56 | `.claude/memory/skill-execution-troubleshooting.md` | ~3 |
| 57 | `.claude/memory/context-files-guide.md` | ~2 |
| 58 | `.claude/memory/parallel-orchestration-guide.md` | ~2 |
| 59 | `.claude/memory/ui-generator-guide.md` | ~1 |
| 60 | `.claude/memory/git-operations-policy.md` | ~1 |
| 61 | `.claude/memory/command-pattern-compliance.md` | ~2 |
| 62 | `.claude/memory/subagents-reference.md` | ~2 |

**+ `src/` mirrors** for all of the above

#### Tier 5: HISTORICAL — Backups, archives, feedback, plans (update is optional)

| Category | Estimated Files | Recommendation |
|----------|----------------|----------------|
| `.claude/skills/*/SKILL.md.backup*` | ~12 | **Do NOT update** — historical snapshots |
| `.claude/skills/*/SKILL.md.original-*` | ~5 | **Do NOT update** — historical snapshots |
| `.claude/plans/*.md` | ~10 | **Do NOT update** — historical context |
| `devforgeai/specs/Stories/archive/*.story.md` | ~50+ | **Do NOT update** — completed stories |
| `devforgeai/feedback/ai-analysis/**/*.json` | ~20+ | **Do NOT update** — historical data |
| `devforgeai/workflows/completed/*.json` | ~30+ | **Do NOT update** — completed workflows |
| `devforgeai/specs/prompt-versions/**/*` | ~10+ | **Do NOT update** — version snapshots |
| `tests/results/**/*` | ~15+ | **Do NOT update** — test artifacts |

#### Tier 6: INTERNAL SKILL FILES — Self-references within the skill directory

Files inside `.claude/skills/devforgeai-development/` that reference the skill name:

| File | Count |
|------|-------|
| `SKILL.md` (frontmatter + body) | ~15 |
| `INTEGRATION_GUIDE.md` | ~10 |
| `README.md` | ~10 |
| `phases/*.md` (12 files) | ~1-3 each |
| `references/*.md` (~30+ files) | ~1-3 each |

**These move WITH the directory rename** — internal relative paths (e.g., `phases/phase-01-preflight.md`) do NOT need updating. Only absolute/skill-name references within the files need updating.

---

### 3.6 System-Reminder Skill List Impact

**Critical question:** Does renaming the skill directory also rename it in the system-reminder skill list that Claude sees?

**Answer: YES.** The system-reminder `<system-reminder>` block is auto-generated from the YAML frontmatter `name:` field in each SKILL.md. The process is:

1. Claude Code scans all `.claude/skills/*/SKILL.md` files at startup
2. Extracts `name:` and `description:` from frontmatter
3. Injects them into the system-reminder as the available skills list

**Therefore:**
- Renaming the `name:` field in SKILL.md frontmatter → **automatically updates** the system-reminder list
- Renaming the directory → **automatically discovered** by Claude Code's skill scanner
- The `/dev` command's `Skill(command="devforgeai-implementing-stories")` call → **must match** the new `name:` field exactly
- The old name `devforgeai-development` will **cease to exist** in the skill list after rename

**Risk:** If `dev.md` still references `Skill(command="devforgeai-development")` after rename, the skill invocation will **fail silently** or trigger a "skill not found" error.

---

### 3.7 Migration Execution Order

**CRITICAL: Tier 0 (ADR + constitution updates) MUST complete before any rename. The rename must be atomic — all Tier 0-1 changes in a single commit.**

```
Step 0: Create ADR-017 (PREREQUISITE — blocks all subsequent steps)
  └─ Create devforgeai/specs/adrs/ADR-017-skill-gerund-naming-convention.md
  └─ Decision: devforgeai-[phase] → devforgeai-[gerund-phrase]
  └─ Status: Accepted
  └─ Consequence: All new skills use gerund form; existing skills migrated progressively

Step 0.1: Update constitutional context files (Tier 0)
  └─ devforgeai/specs/context/source-tree.md — naming convention + directory tree + examples (bump 3.8 → 3.9)
  └─ devforgeai/specs/context/coding-standards.md — naming convention (bump 1.2 → 1.3)
  └─ devforgeai/specs/context/architecture-constraints.md — skill reference (bump 1.0 → 1.1)
  └─ devforgeai/specs/context/anti-patterns.md — modular examples (bump 1.1 → 1.2)
  └─ devforgeai/specs/context/tech-stack.md — path reference (bump 1.4 → 1.5)

Step 0.2: Update Constitution mirrors (.claude/memory/Constitution/)
  └─ Mirror all 5 context file changes to .claude/memory/Constitution/

Step 1: Create backups
  └─ dev.md.backup-pre-rename-2026-02-15
  └─ SKILL.md.backup-pre-rename-2026-02-15

Step 2: Rename directories (BOTH operational and src/)
  └─ mv .claude/skills/devforgeai-development/ .claude/skills/devforgeai-implementing-stories/
  └─ mv src/claude/skills/devforgeai-development/ src/claude/skills/devforgeai-implementing-stories/

Step 3: Update SKILL.md frontmatter
  └─ name: devforgeai-development → name: devforgeai-implementing-stories
  └─ description: "Implement..." → "Implements..." (R7 fix)

Step 4: Update Tier 1 files (commands)
  └─ dev.md, resume-dev.md, orchestrate.md

Step 5: Update Tier 2 files (system context)
  └─ CLAUDE.md, src/CLAUDE.md, memory files

Step 6: Update Tier 3 files (subagents)
  └─ All .claude/agents/*.md files + src/ mirrors

Step 7: Update Tier 4 files (other skills, rules, references)
  └─ All cross-skill references

Step 8: Verify
  └─ Grep for any remaining "devforgeai-development" in Tiers 0-4
  └─ Test: /dev STORY-001 (dry run or with a test story)

Step 9: Commit
  └─ Single atomic commit: "refactor(ADR-017): rename devforgeai-development → devforgeai-implementing-stories"
```

**Estimated file count for Tiers 0-4 (operational + src/):**
- Tier 0: ~12 files (1 ADR + 5 context files + 5 mirrors + 1 src/ mirror)
- Tier 1: ~8 files
- Tier 2: ~12 files (reduced — constitution files moved to Tier 0)
- Tier 3: ~48 files (24 agents × 2 trees)
- Tier 4: ~44 files
- Tier 6 (internal): ~45 files
- **Total: ~169 files** (excluding Tier 5 historical files)

---

### 3.8 Rollback Plan

**If rename causes issues after commit:**

```
# Option A: Git revert (preferred)
git revert HEAD  # Reverts the rename commit

# Option B: Manual rollback from backups
mv .claude/skills/devforgeai-implementing-stories/ .claude/skills/devforgeai-development/
mv src/claude/skills/devforgeai-implementing-stories/ src/claude/skills/devforgeai-development/
cp .claude/commands/dev.md.backup-pre-rename-2026-02-15 .claude/commands/dev.md
cp .claude/skills/devforgeai-development/SKILL.md.backup-pre-rename-2026-02-15 .claude/skills/devforgeai-development/SKILL.md
# Then grep-replace "devforgeai-implementing-stories" → "devforgeai-development" in all Tier 1-4 files
```

**Rollback verification:**
```bash
# Verify no references to new name remain
grep -r "devforgeai-implementing-stories" .claude/ src/ CLAUDE.md --include="*.md" --include="*.py" --include="*.yaml" --include="*.json" | grep -v ".backup" | grep -v "archive"
```

---

### 3.9 Risk Assessment

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Constitutional violation** — rename without ADR breaks LOCKED files | **CRITICAL** | ADR-017 MUST be created in Step 0 BEFORE any rename; Tier 0 gates all subsequent steps |
| **Convention drift** — old-name skills coexist with new-name skills | MEDIUM | source-tree.md explicitly marks legacy names as "accepted until migrated"; new convention enforced for NEW skills only |
| **Missed reference** — a file still says "devforgeai-development" | HIGH | Post-rename grep scan; test with actual `/dev` invocation |
| **Backup files break** — old SKILL.md.backup references don't work | LOW | Backups are historical; they should NOT be updated |
| **Pre-commit hook failure** — DoD validator paths hardcoded | MEDIUM | Check `.claude/scripts/devforgeai_cli/validators/` for hardcoded paths |
| **Phase state files** — existing `STORY-XXX-phase-state.json` reference old skill | LOW | Phase state tracks story phases, not skill name |
| **Active development interrupted** — stories in "In Development" status | MEDIUM | Complete or pause active `/dev` workflows before rename |
| **src/ tree drift** — src/ and .claude/ get out of sync | MEDIUM | Update both trees in same commit; verify with diff |
| **Full-fleet migration scope creep** — attempting to rename all skills at once | HIGH | Section 3.12 defines phased rollout; MVP is devforgeai-development ONLY; other skills migrated in separate stories |

---

### 3.10 Pre-Rename Validation Script

Before executing the rename, run this validation:

```bash
# 1. Count all references (expect ~1,425 across all files including historical)
grep -r "devforgeai-development" . --include="*.md" --include="*.py" --include="*.yaml" --include="*.json" --include="*.sh" | wc -l

# 2. Count Tier 1-4 references only (exclude archives, backups, feedback, plans, tests)
grep -r "devforgeai-development" .claude/ src/ CLAUDE.md devforgeai/specs/context/ \
  --include="*.md" --include="*.py" --include="*.yaml" --include="*.json" \
  | grep -v ".backup" | grep -v ".original" | grep -v "archive/" | grep -v "plans/" \
  | grep -v "feedback/" | grep -v "tests/" | grep -v "workflows/completed" \
  | wc -l

# 3. Verify no active dev workflows
ls devforgeai/workflows/STORY-*-phase-state.json 2>/dev/null | head -5
```

---

### 3.11 Implementation Notes

- **This is a PLAN ONLY** — no files have been modified
- **Recommended approach:** Create a dedicated story (e.g., STORY-413) for this rename using `/create-story`
- **ADR-017 is a prerequisite** — must be created and accepted before any file rename
- **Combine with R7 (description fix)** — since we're editing SKILL.md frontmatter anyway, fix the description point-of-view simultaneously
- **Do NOT combine with R1 (500-line split)** — the rename is a mechanical find-replace operation; the content split is a structural refactoring. Mixing them increases risk
- **Do NOT rename other skills in this story** — MVP scope is `devforgeai-development` only; other skills follow in Section 3.12 roadmap
- **The rename can be executed with a script** — a simple `sed -i` or editor find-replace across all Tier 0-4 files, followed by directory renames

---

### 3.12 Full-Fleet Gerund Migration Roadmap

**Purpose:** Establish the complete migration plan for ALL `devforgeai-*` skills from the legacy `devforgeai-[phase]` noun convention to the new `devforgeai-[gerund-phrase]` convention per ADR-017.

**Strategy:** Progressive migration — one skill per story. MVP (this plan) handles `devforgeai-development` first. Remaining skills migrated in priority order based on invocation frequency and user-facing impact.

#### Migration Status Table

| # | Current Name | Proposed Gerund Name | Priority | Story | Status |
|---|-------------|---------------------|----------|-------|--------|
| **1** | `devforgeai-development` | `devforgeai-implementing-stories` | **MVP** | STORY-413 (TBD) | 📋 Planned (this document) |
| 2 | `devforgeai-qa` | `devforgeai-validating-quality` | HIGH | TBD | ⬜ Not started |
| 3 | `devforgeai-story-creation` | `devforgeai-creating-stories` | HIGH | TBD | ⬜ Not started |
| 4 | `designing-systems` | `devforgeai-designing-architecture` | MEDIUM | TBD | ⬜ Not started |
| 5 | `discovering-requirements` | `devforgeai-discovering-requirements` | MEDIUM | TBD | ⬜ Not started |
| 6 | `devforgeai-orchestration` | `devforgeai-orchestrating-workflows` | MEDIUM | TBD | ⬜ Not started |
| 7 | `devforgeai-documentation` | `devforgeai-generating-documentation` | LOW | TBD | ⬜ Not started |
| 8 | `devforgeai-feedback` | `devforgeai-collecting-feedback` | LOW | TBD | ⬜ Not started |
| 9 | `devforgeai-rca` | `devforgeai-analyzing-root-causes` | LOW | TBD | ⬜ Not started |
| 10 | `devforgeai-release` | `devforgeai-releasing-stories` | LOW | TBD | ⬜ Not started |
| 11 | `devforgeai-ui-generator` | `devforgeai-generating-ui-specs` | LOW | TBD | ⬜ Not started |
| 12 | `devforgeai-subagent-creation` | `devforgeai-creating-subagents` | LOW | TBD | ⬜ Not started |
| 13 | `devforgeai-brainstorming` | ✅ Already gerund | — | — | ✅ Compliant |
| 14 | `devforgeai-mcp-cli-converter` | `devforgeai-converting-mcp-cli` | LOW | TBD | ⬜ Not started |
| 15 | `devforgeai-github-actions` | `devforgeai-configuring-github-actions` | LOW | TBD | ⬜ Not started |
| 16 | `devforgeai-shared` | N/A (utility, not a skill) | — | — | ⚠️ Exempt |
| 17 | `claude-code-terminal-expert` | N/A (no `devforgeai-` prefix) | — | — | ⚠️ Exempt |
| 18 | `skill-creator` | N/A (no `devforgeai-` prefix) | — | — | ⚠️ Exempt |

#### Migration Rules

1. **One skill per story** — each rename is a separate story for clean git history and isolated rollback
2. **ADR-017 covers all** — no additional ADRs needed for subsequent renames (convention already established)
3. **Legacy names accepted** — during migration period, old noun-form names are valid in context files; they're updated when their skill is migrated
4. **New skills MUST use gerund form** — from ADR-017 approval forward, all new `devforgeai-*` skills must follow gerund convention
5. **Non-devforgeai skills exempt** — `claude-code-terminal-expert`, `skill-creator`, and similar non-prefixed skills are not affected
6. **`devforgeai-brainstorming` already compliant** — no migration needed (already gerund form)
7. **`devforgeai-shared` exempt** — utility module, not a user-facing skill; naming convention doesn't apply

#### Estimated Effort Per Skill

Based on the MVP analysis (devforgeai-development → ~169 files):

| Skill | Estimated Reference Count | Effort |
|-------|--------------------------|--------|
| `devforgeai-development` (MVP) | ~1,425 total (~169 active) | HIGH (most referenced skill) |
| `devforgeai-qa` | ~400-600 | MEDIUM |
| `devforgeai-story-creation` | ~300-500 | MEDIUM |
| `devforgeai-orchestration` | ~200-400 | MEDIUM |
| `designing-systems` | ~200-400 | MEDIUM |
| All others | ~50-200 each | LOW |

**Total estimated migration effort:** 6-10 stories across 3-4 sprints after MVP validation.

#### Success Criteria for Full Migration

- [ ] All `devforgeai-*` skills use gerund naming (except exemptions)
- [ ] All 6 context files reflect new convention with no legacy pattern references
- [ ] All subagent files reference skills by new names
- [ ] All slash commands invoke skills by new names
- [ ] Zero grep hits for old skill names in Tiers 0-4 files (Tier 5 historical exempt)
- [ ] `/dev`, `/qa`, `/orchestrate`, and all other commands function correctly with new names

---

### Story Verification Checklist

Before creating stories from this plan:

- [x] All target files verified to exist (Read each file — dev.md, SKILL.md, best-practices.md, all 6 context files read during analysis)
- [x] All test paths match source-tree.md patterns (N/A — no test files created)
- [x] No references to deleted files (checked git status — no relevant deletions)
- [x] All dependencies verified to exist (Grep confirmed all referenced files exist)
- [x] Exact edits specified (frontmatter changes, directory renames, string replacements)
- [x] Constitutional conflicts identified and ADR requirement documented (Section 3.1A)
- [x] All 6 context files read and cross-referenced for naming convention conflicts
- [x] Full-fleet migration roadmap established (Section 3.12)

**Status:** ✅ Verified

---

## Phase 4: Session Handoff & Workflow Execution Guide

**Date:** 2026-02-15
**Purpose:** Self-contained instructions for any future Claude session to execute this plan without the original conversation context.

---

### 4.1 Workflow Decision: Skip Brainstorm & Ideate, Proceed to Epic → Story → Dev

| Workflow Stage | Decision | Rationale |
|---------------|----------|-----------|
| `/brainstorm` | **SKIP** | Brainstorming already completed in this plan document (Sections 3.1-3.3: problem analysis, 5 candidates evaluated, recommendation made) |
| `/ideate` | **SKIP** | Ideation transforms business problems into requirements. This is an internal framework refactoring with fully specified scope (Sections 3.1A, 3.5, 3.7, 3.12). No discovery needed. |
| `/create-epic` | **EXECUTE** | Section 3.12 defines 14 skill renames across 6-10 stories. This constitutes an epic-level body of work requiring tracking. |
| `/create-story` | **EXECUTE** | MVP story for `devforgeai-development` → `devforgeai-implementing-stories` rename. Story must include ADR creation as part of scope. |
| `/dev` | **EXECUTE** | Standard TDD workflow for the rename implementation |
| `/qa` | **EXECUTE** | Validation that all references updated, no broken invocations |
| `/release` | **EXECUTE** | Commit and release the rename |

---

### 4.2 How to Proceed: Step-by-Step Commands

**A future Claude session should execute these steps IN ORDER. Each step includes the exact command and all context needed.**

#### Step 1: Read This Plan

```
Read(file_path=".claude/plans/dev-analysis-phase2-online-docs.md")
```

Focus on Phase 3 (Sections 3.1-3.12) and Phase 4 (this section). All decisions, rationale, constitutional conflicts, and migration checklists are documented here. **Do NOT re-derive decisions.**

#### Step 2: Create the Epic

```
/create-epic EPIC-065 Skill Gerund Naming Convention Migration
```

**Epic context to provide when prompted:**

- **Business Problem:** DevForgeAI skill names use generic noun-form (`devforgeai-development`) that violates Anthropic's recommended gerund naming convention (best-practices.md line 156). This reduces Claude's skill discovery accuracy and creates vague naming that doesn't describe what skills do.
- **Scope:** Rename all 14 `devforgeai-*` skills from noun-form to gerund-form per new convention (ADR-017). One skill per story. MVP: `devforgeai-development` → `devforgeai-implementing-stories`.
- **Features:** (1) ADR-017 creation establishing gerund convention, (2) Constitutional context file updates (5 files), (3) MVP skill rename with ~169 file updates, (4) Subsequent skill renames (13 remaining), (5) Full-fleet verification
- **Source Plan:** `.claude/plans/dev-analysis-phase2-online-docs.md` (Phase 3, Section 3.12 has the complete migration table)
- **Acceptance Criteria for Epic:** All `devforgeai-*` skills use gerund naming; all context files updated; all commands function correctly; zero grep hits for old names in active files

#### Step 3: Create the MVP Story

```
/create-story
```

**Story context to provide when prompted:**

- **Epic:** EPIC-065
- **Title:** Rename devforgeai-development to devforgeai-implementing-stories
- **Type:** refactor
- **Priority:** HIGH
- **Points:** 5 (high file count but mechanical changes)
- **Description:** Rename the `devforgeai-development` skill to `devforgeai-implementing-stories` following Anthropic's gerund naming best practice. This is the MVP of the full-fleet gerund naming migration (EPIC-065). Includes ADR-017 creation, constitutional context file updates, directory rename, and ~169 file reference updates across Tiers 0-4.

**Acceptance Criteria to include:**

```
AC1: ADR-017 Created and Accepted
- Given: The naming convention `devforgeai-[phase]` is LOCKED in source-tree.md and coding-standards.md
- When: ADR-017-skill-gerund-naming-convention.md is created in devforgeai/specs/adrs/
- Then: ADR establishes `devforgeai-[gerund-phrase]` as the new convention, documents the decision rationale (Anthropic best-practices.md line 156), and specifies progressive migration strategy

AC2: Constitutional Context Files Updated (5 files)
- Given: ADR-017 is accepted
- When: All 5 context files are updated with new naming convention
- Then: source-tree.md (pattern, directory tree, examples), coding-standards.md (pattern), architecture-constraints.md (skill reference), anti-patterns.md (examples), tech-stack.md (path reference) all reflect new convention. Version numbers bumped. Legacy names documented as "accepted until migrated."

AC3: Skill Directory Renamed
- Given: Context files updated
- When: Skill directory is renamed in both operational and src/ trees
- Then: `.claude/skills/devforgeai-implementing-stories/` exists with all original content; `.claude/skills/devforgeai-development/` no longer exists; `src/` mirror updated identically

AC4: SKILL.md Frontmatter Updated
- Given: Directory renamed
- When: SKILL.md frontmatter is updated
- Then: `name: devforgeai-implementing-stories`; description uses third-person ("Implements..." not "Implement...")

AC5: All Command Files Updated
- Given: SKILL.md updated
- When: dev.md, resume-dev.md, orchestrate.md are updated
- Then: All `Skill(command="...")` calls reference `devforgeai-implementing-stories`; all file paths reference new directory

AC6: All Cross-References Updated (Tiers 2-4)
- Given: Commands updated
- When: All files in Tiers 2-4 are updated
- Then: CLAUDE.md, memory files, subagent files, other skill files, rule files all reference new skill name and directory path

AC7: Zero Residual References
- Given: All tiers updated
- When: Grep scan runs across .claude/, src/, CLAUDE.md, devforgeai/specs/context/
- Then: Zero hits for "devforgeai-development" in active files (Tier 5 historical files exempt)

AC8: Functional Verification
- Given: All references updated
- When: `/dev STORY-XXX` is invoked (dry run or test story)
- Then: Skill invocation succeeds; phase state initializes correctly; no "skill not found" errors
```

**Technical Specification to include:**

```
Files to modify: ~169 (see Section 3.5 of plan for complete inventory by tier)
Files to create: 1 (ADR-017)
Directories to rename: 2 (.claude/skills/ and src/claude/skills/)

Execution order: Section 3.7 of plan (Steps 0 → 0.1 → 0.2 → 1 → ... → 9)
Rollback plan: Section 3.8 of plan (git revert or manual)
Risk assessment: Section 3.9 of plan

Source plan: .claude/plans/dev-analysis-phase2-online-docs.md (Phase 3)
```

#### Step 4: Execute Development

```
/dev STORY-NNN
```

Where `STORY-NNN` is the story ID created in Step 3. The `/dev` workflow will follow TDD phases. For this refactoring story:
- **Phase 02 (Red):** Tests verify grep counts match expected reference counts before/after rename
- **Phase 03 (Green):** Execute the rename per Section 3.7 execution order
- **Phase 04 (Refactor):** Clean up any formatting inconsistencies introduced during bulk replacement
- **Phase 05 (Integration):** Verify `/dev` command invocation works end-to-end with new skill name

#### Step 5: QA Validation

```
/qa STORY-NNN Deep
```

QA validates:
- All ACs met (especially AC7: zero residual references and AC8: functional verification)
- No broken file paths
- Context file version bumps are consistent
- ADR-017 follows ADR template format

#### Step 6: Release

```
/release STORY-NNN
```

---

### 4.3 ADR-017 Draft Content

**Purpose:** Future Claude should use this draft as the starting point for ADR creation, NOT re-derive the decision.

```markdown
# ADR-017: Skill Gerund Naming Convention

**Status:** Accepted
**Date:** 2026-02-XX (date of implementation)
**Decision Makers:** DevForgeAI Framework Team
**Supersedes:** Naming convention in source-tree.md v3.8 (line 834) and coding-standards.md v1.2 (line 117)

## Context

DevForgeAI skills follow a `devforgeai-[phase]` naming convention established in source-tree.md
and coding-standards.md. This uses single-word noun-form lifecycle phase names:
`discovering-requirements`, `designing-systems`, `devforgeai-development`, `devforgeai-qa`,
`devforgeai-release`.

Anthropic's official skill authoring best practices (best-practices.md, lines 156-181) recommend
gerund form (verb+-ing) for skill names:

> "We recommend using gerund form (verb + -ing) for Skill names, as this clearly describes the
> activity or capability the Skill provides."

The current noun-form names are:
- **Vague** — "development" could mean documentation, test, or architecture development
- **Not gerund** — "development" is a noun, not a gerund
- **Poor for skill discovery** — Claude matches skills by name+description; gerund names
  like "implementing-stories" provide stronger signal than "development"

## Decision

Adopt gerund naming convention for all `devforgeai-*` skills:

**Old Convention:** `devforgeai-[phase]` (noun-form: development, architecture, ideation)
**New Convention:** `devforgeai-[gerund-phrase]` (verb+-ing phrase: implementing-stories,
designing-architecture, discovering-requirements)

## Consequences

### Positive
- Aligns with Anthropic's recommended best practice
- Improves Claude's skill discovery accuracy (gerund names describe activities)
- Differentiates similar skills (implementing-stories vs creating-stories)
- Future-proofs naming as Anthropic's tooling may optimize for gerund discovery

### Negative
- ~169 file updates for MVP rename (devforgeai-development → devforgeai-implementing-stories)
- 6-10 additional stories for full-fleet migration
- Temporary coexistence of old and new naming during migration period

### Migration Strategy
- **Progressive:** One skill per story, prioritized by invocation frequency
- **MVP:** devforgeai-development → devforgeai-implementing-stories (STORY-NNN)
- **Legacy acceptance:** Old noun-form names valid during migration period
- **New skill rule:** All new devforgeai-* skills MUST use gerund form from this ADR forward
- **Exempt:** devforgeai-shared (utility), claude-code-terminal-expert (non-prefix),
  skill-creator (non-prefix), devforgeai-brainstorming (already gerund)

### Context Files Updated
- source-tree.md: 3.8 → 3.9 (naming pattern, directory tree, examples)
- coding-standards.md: 1.2 → 1.3 (naming pattern)
- architecture-constraints.md: 1.0 → 1.1 (skill references)
- anti-patterns.md: 1.1 → 1.2 (modular skill examples)
- tech-stack.md: 1.4 → 1.5 (path references)

## References
- Anthropic best-practices.md, lines 156-181 (gerund naming recommendation)
- Plan: .claude/plans/dev-analysis-phase2-online-docs.md (Phase 3)
- Full migration table: Phase 3, Section 3.12
```

---

### 4.4 Source Files Referenced in This Plan

**Future Claude sessions should read these files to understand context. Listed in priority order.**

| Priority | File | Why Read It |
|----------|------|-------------|
| **1 (MUST)** | `.claude/plans/dev-analysis-phase2-online-docs.md` | **THIS FILE** — the complete plan with all decisions, checklists, and ADR draft |
| **2 (MUST)** | `devforgeai/specs/context/source-tree.md` | Contains LOCKED naming convention (line 834) that the ADR supersedes; directory tree structure that must be updated |
| **3 (MUST)** | `devforgeai/specs/context/coding-standards.md` | Contains LOCKED naming convention (line 117) that the ADR supersedes |
| **4 (SHOULD)** | `.claude/skills/devforgeai-development/SKILL.md` | The skill being renamed — verify current frontmatter before editing |
| **5 (SHOULD)** | `.claude/commands/dev.md` | The primary command that invokes the skill — verify current Skill() call |
| **6 (SHOULD)** | `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` | Anthropic's naming guidance at line 156 (the authority for this change) |
| **7 (REFERENCE)** | `devforgeai/specs/context/architecture-constraints.md` | Skill reference at lines 31-33 |
| **8 (REFERENCE)** | `devforgeai/specs/context/anti-patterns.md` | Modular skill examples at lines 42-47 |
| **9 (REFERENCE)** | `devforgeai/specs/context/tech-stack.md` | Path reference at line 365 |
| **10 (REFERENCE)** | `devforgeai/specs/context/dependencies.md` | No direct conflicts, but read for completeness |

---

### 4.5 Decisions Already Made (Do NOT Re-Derive)

**These decisions were made with full context in the original analysis session. Future sessions MUST NOT revisit them unless the user explicitly requests it.**

| Decision | Made In | Rationale Summary |
|----------|---------|-------------------|
| **Skip /brainstorm and /ideate** | Section 4.1 | Plan already contains complete analysis; ideation adds overhead for internal refactoring |
| **Name: `devforgeai-implementing-stories`** | Section 3.2-3.3 | 5 candidates evaluated; this one best matches gerund form + skill's actual function (implements stories via TDD) + trigger alignment with `/dev STORY-XXX` |
| **ADR required (ADR-017)** | Section 3.1A | Two LOCKED context files define `devforgeai-[phase]`; Critical Rule #4 requires ADR for convention changes |
| **ADR number: ADR-017** | Section 4.3 | ADR-016 is taken (`ADR-016-dead-code-detector-read-only.md`, accepted 2026-02-14) |
| **Epic number: EPIC-065** | Section 4.2 | Latest epic is EPIC-064 (`ai-generated-code-smell-detection-gap-closure`) |
| **Full-fleet migration is phased** | Section 3.12 | One skill per story; MVP first; legacy names accepted during transition |
| **Tier 5 (historical) files NOT updated** | Section 3.5 | Backups, archives, feedback, completed workflows are historical snapshots |
| **Description fix combined with rename** | Section 3.11 | "Implement..." → "Implements..." (third-person per N2/R7) done in same story since both edit frontmatter |
| **500-line split NOT combined** | Section 3.11 | Separate structural refactoring; mixing with rename increases risk |
| **devforgeai-brainstorming already compliant** | Section 3.12 | Already uses gerund form; no migration needed |
| **devforgeai-shared exempt** | Section 3.12 | Utility module, not user-facing skill |

---

### 4.6 Known Constraints for Future Sessions

1. **Next available story ID:** STORY-413+ (latest is STORY-412 as of 2026-02-15)
2. **Next available epic ID:** EPIC-065 (latest is EPIC-064 as of 2026-02-15)
3. **Next available ADR ID:** ADR-017 (ADR-016 is taken by dead-code-detector)
4. **Active stories in development:** Check `devforgeai/workflows/STORY-*-phase-state.json` — complete or pause any active `/dev` workflows before executing the rename
5. **Git status:** Main branch has uncommitted changes (see git status at top of plan). Ensure clean working tree before rename commit.
6. **WSL environment:** Tests must run against `src/` tree per CLAUDE.md. Use `/mnt/c/` paths.

---

### 4.7 Context Preservation Verification

**This plan is self-contained if a future Claude session can answer ALL of these questions by reading ONLY this file:**

- [x] What skill is being renamed and to what? → Section 3.3
- [x] Why is it being renamed? → Section 3.1 (Anthropic best practice) + Section 3.1A (constitutional conflict)
- [x] What ADR is needed and what should it contain? → Section 4.3 (full draft)
- [x] What files need updating and in what order? → Section 3.5 (tiers) + Section 3.7 (execution order)
- [x] What constitutional files conflict and how? → Section 3.1A (exact lines and quotes)
- [x] How to rollback if something goes wrong? → Section 3.8
- [x] What workflow commands to run? → Section 4.2 (step-by-step with exact commands)
- [x] What story ACs should look like? → Section 4.2 Step 3 (8 ACs pre-written)
- [x] What other skills need renaming later? → Section 3.12 (full table with proposed names)
- [x] What decisions should NOT be re-derived? → Section 4.5 (10 locked decisions)
- [x] What are the ID numbers to use? → Section 4.6 (ADR-017, EPIC-065, STORY-413+)

**Status:** ✅ Self-contained — no conversation context required
