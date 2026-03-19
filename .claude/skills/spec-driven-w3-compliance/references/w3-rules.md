# W3 Rules Reference

This file contains the W3 violation definitions, severity categories, remediation guidance, and authoritative references. Load this file fresh at the start of phases that need W3 context. Do NOT rely on memory of previous reads.

---

## W3 Definition

**W3 (Workflow-level Warning for auto-invocation Without user consent):**

Skills or commands that auto-invoke other skills without user approval, causing:
- **Token overflow** — Cascading skill invocations consume entire context window
- **Loss of user control** — User cannot review or cancel chained invocations
- **Lean orchestration violation** — Commands should be thin orchestrators, not recursive skill launchers

**Origin:** BRAINSTORM-001 (line 85) identified auto-skill chaining as a systemic risk. STORY-135 implemented the W3 compliance framework to detect and prevent it.

---

## Violation Severity Categories

### CRITICAL: Subagent Skill Invocation

**Rule:** Subagents CANNOT invoke skills. This is an absolute prohibition defined in architecture-constraints.md.

**Why it matters:** Subagents run in fresh-context isolation. If a subagent invokes a skill, that skill expands inline within the subagent's limited context, potentially consuming its entire budget. The subagent was not designed to orchestrate skills — that responsibility belongs to the orchestrator (opus) or dedicated orchestration skills.

**Detection:** Any `.claude/agents/*.md` file containing `Skill(command=...)` is a CRITICAL violation.

**Remediation:** Remove the Skill() call from the subagent. If the subagent needs functionality provided by a skill, it should either:
1. Implement the logic directly (preferred for simple operations)
2. Return a recommendation to the orchestrator to invoke the skill (display-only pattern)

### HIGH: Non-Orchestration Skill Auto-Chaining

**Rule:** Only `devforgeai-orchestration` may coordinate skills freely. All other skills must either use display-only recommendations or include an AskUserQuestion gate before any Skill() call.

**Why it matters:** When Skill A auto-invokes Skill B, the token cost compounds unpredictably. The user loses visibility into what is being executed and cannot cancel mid-chain. This violates the lean orchestration principle where commands are thin wrappers and skills are single-responsibility units.

**Detection:** Any `.claude/skills/*.md` file (excluding orchestration) containing `Skill(command=...)` without a preceding AskUserQuestion or display-only marker.

**Remediation:**
- **Option A (Preferred):** Replace Skill() call with a display-only recommendation telling the user which command to run next.
- **Option B:** Add AskUserQuestion before the Skill() call to get user consent.

### MEDIUM: Missing W3 Compliance Documentation

**Rule:** Files that contain Skill() calls should document their W3 compliance status. This provides auditability and makes the intent explicit.

**Why it matters:** Without W3 documentation, it is unclear whether a Skill() call is intentional (with proper gates) or an oversight. Documentation makes compliance reviewable.

**Detection:** Any `.claude/skills/*.md` file (excluding orchestration) that contains `Skill(command=...)` but does NOT contain the string "W3" or "display-only".

**Remediation:** Add a W3 compliance note to the file explaining why the Skill() call exists and what gate protects it. Example:
```markdown
## W3 Compliance
This skill invokes Skill(command="...") with an AskUserQuestion gate at line N.
The user must explicitly approve before the skill is invoked.
```

### INFO: Auto-Invoke Language Patterns

**Rule:** Language that suggests auto-invocation intent should be reviewed, even if no Skill() call is present. These patterns may indicate future W3 violations being planned.

**Why it matters:** Language like "automatically invoke" or "then invoke the skill" may indicate that a developer intends to add auto-invocation later. Catching these early prevents violations from being introduced.

**Detection:** Any `.claude/*.md` file containing case-insensitive patterns: `auto.*invoke`, `then invoke`, `invoking.*skill`, `automatically`.

**Remediation:** Review the context of each pattern. If it describes intended behavior, ensure a W3-compliant implementation is used. If it is purely documentation, no action needed.

---

## Authoritative References

| Reference | Description |
|-----------|-------------|
| BRAINSTORM-001 (line 85) | Original identification of auto-skill chaining as systemic risk |
| STORY-135 | Implementation of W3 compliance framework |
| EPIC-071 | Hybrid Command Lean Orchestration Refactoring |
| ADR-020 | Structural Changes Authorization (audit-w3 refactoring) |
| architecture-constraints.md | Defines subagent Skill() invocation as forbidden |
| STORY-462 | Special cases cleanup (original auditing-w3-compliance skill creation) |

---

## Legitimate Exceptions

The following are NOT W3 violations:

1. **devforgeai-orchestration skill** — Explicitly authorized to coordinate skills as the framework's central orchestrator.
2. **Backup files** (*.backup, *.backup-*, *.original-*) — Not active code.
3. **Skill() calls with AskUserQuestion gates** — User consent obtained before invocation.
4. **Display-only recommendations** — Skill() shown as example/recommendation, not executed.
5. **Code examples in documentation** — Skill() shown in fenced code blocks as reference patterns.
