# Command Refactoring Patterns

**Purpose:** Guidance for generating subagents that support slash command refactoring per lean orchestration protocol.

---

## When This Applies

**Trigger conditions:**
- User requests: "Create subagent for /[command] refactoring"
- User requests: "Generate [topic]-formatter subagent"
- User requests: "Create [topic]-interpreter subagent"
- Analysis shows command over budget (>15K characters)
- Command has display templates, parsing logic, or result interpretation

**Examples of command-related subagents:**
- qa-result-interpreter (QA report interpretation)
- story-formatter (story YAML/markdown generation)
- ui-spec-formatter (UI template generation)
- release-orchestrator (deployment sequence coordination)
- dev-result-interpreter (development workflow results)

---

## Mandatory Protocol Reference

**BEFORE generating command-related subagents:**

```
Read(file_path="devforgeai/protocols/lean-orchestration-pattern.md")
```

**Extract from protocol:**
- Subagent Responsibilities (lines 81-96)
- Subagent Creation Guidelines (lines 783-916)
- Subagent Template (lines 800-916)
- Reference File Template (lines 933-1040)
- Case Studies (lines 1216-1264)

---

## Subagent Design for Command Refactoring

### 1. Purpose: Specialized Task Extraction

Extract logic from over-budget command:
- Report parsing and interpretation
- Display template generation
- Result formatting and presentation
- Sequence coordination

**Purpose Template:**
```markdown
## Purpose

This subagent extracts [specific responsibility] from the /[command] slash command
to achieve lean orchestration.

**Original issue:**
- Command was [XXX] lines, [YYK] characters ([ZZ]% over 15K budget)
- [Specific logic] was embedded in command

**This subagent handles:**
1. [Primary responsibility]
2. [Secondary responsibility]
3. Returns structured result for command to display
```

### 2. Model Selection: Fast and Deterministic

| Task Type | Recommended Model |
|-----------|-------------------|
| Parsing/interpretation | haiku (<8K tokens) |
| Formatting/templates | haiku (<10K tokens) |
| Complex coordination | sonnet (8-50K tokens) |

### 3. Tool Access: Minimal (View-Only Preferred)

```yaml
# For parsing/analysis
tools: Read, Grep, Glob

# If generating files
tools: Read, Write

# Avoid unless necessary
tools: Edit, Bash
```

### 4. Framework-Aware: NOT Siloed

**CRITICAL:** Create companion reference file with framework guardrails

```
Reference file location:
.claude/skills/[related-skill]/references/[subagent-topic]-guide.md

Purpose:
- Provide DevForgeAI context (workflow states, quality gates)
- Define immutable constraints (thresholds, rules, patterns)
- Specify display guidelines (templates, tone, structure)
- Prevent autonomous decisions (explicit boundaries)
```

### 5. Structured Output: Reliable Parsing

```json
{
  "status": "SUCCESS|ERROR",
  "display": {
    "template": "[markdown for user]",
    "sections": [...]
  },
  "data": {...},
  "recommendations": [...]
}
```

---

## Required Sections in Command Refactoring Subagents

### Section 1: Purpose (with refactoring context)

```markdown
## Purpose

This subagent extracts [specific responsibility] from the /[command] slash command.

**Refactoring context:**
- Original command: [XXX] characters ([YY]% over 15K budget)
- Extracted logic: [what was moved to this subagent]
- Remaining in command: [what stays in the command]

**This subagent handles:**
1. [Primary task]
2. [Secondary task]
3. Structured result generation
```

### Section 2: Framework Integration

```markdown
## Framework Integration

**Invoked by:** devforgeai-[skill] skill, Phase [X] Step [Y]
**Timing:** After [what completes], before [what happens next]
**Context required:** [what information needed from caller]
**Returns:** Structured JSON with [fields]

**Framework constraints:**
Load reference file for complete guardrails:
```
Read(file_path=".claude/skills/[skill]/references/[topic]-guide.md")
```

**Key constraints from reference:**
- [Constraint 1] (immutable)
- [Constraint 2] (deterministic)
- [Constraint 3] (from context files)
```

### Section 3: Structured Output Contract

```markdown
## Output Format

Return JSON with this exact structure:

```json
{
  "status": "SUCCESS|ERROR",
  "result_type": "[specific_type]",
  "display": {
    "template": "[markdown template for user]",
    "title": "...",
    "sections": [...]
  },
  "data": {
    "[extracted_field_1]": "...",
    "[extracted_field_2]": "..."
  },
  "recommendations": {
    "next_steps": [...],
    "remediation": [...]
  }
}
```

**Command uses this output to:**
- Display: result.display.template
- Next steps: result.recommendations.next_steps
- Data: result.data (for further processing)
```

---

## Token Budget for Command Refactoring Subagents

**Subagent token targets:**
- Parsing/interpretation: <8K (haiku model)
- Formatting/template generation: <10K (haiku model)
- Coordination/orchestration: <20K (sonnet model)

**Reference file size:**
- Target: 200-400 lines
- Purpose: Framework guardrails, not comprehensive docs
- Content: Constraints, guidelines, templates, examples

---

## Validation Checklist

Before writing command refactoring subagent file:

- [ ] Protocol reference loaded (lean-orchestration-pattern.md)
- [ ] Subagent responsibilities clear (lines 81-96 of protocol)
- [ ] Character budget validated (command will be <15K after refactoring)
- [ ] Framework-aware design (NOT siloed)
- [ ] Reference file planned (framework guardrails)
- [ ] Structured output defined (JSON schema)
- [ ] Tool access minimal (principle of least privilege)
- [ ] Integration points documented (which skill invokes, when)

---

## Example: qa-result-interpreter

**Reference implementation:**
- File: `.claude/agents/qa-result-interpreter.md` (300 lines)
- Purpose: Interpret QA reports, generate user-facing displays
- Model: haiku (<8K tokens)
- Tools: Read, Grep, Glob (view-only)
- Framework guardrails: `.claude/skills/spec-driven-qa/references/qa-result-formatting-guide.md`
- Output: Structured JSON with display template
- Result: /qa command reduced from 692 to 295 lines (57% reduction)

**Key features:**
1. **Protocol-compliant:** Followed lean orchestration subagent template
2. **Framework-aware:** Reference file provides DevForgeAI context
3. **Structured output:** JSON enables reliable parsing by command
4. **Isolated context:** 8K tokens don't impact main conversation
5. **Explicit constraints:** Coverage thresholds, violation rules documented

---

## Commands Needing Refactoring (from audit)

| Command | Characters | Over Budget | Recommended Subagent |
|---------|------------|-------------|---------------------|
| create-story | 23K | 153% | story-formatter |
| create-ui | 19K | 126% | ui-spec-formatter |
| release | 18K | 121% | release-orchestrator |
| ideate | 15K | 102% | requirements-formatter |
| orchestrate | 15K | 100% | workflow-coordinator |

**Use qa-result-interpreter as reference when generating these subagents.**
