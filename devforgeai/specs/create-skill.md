Create the next OmniWatchAI Claude Skill following the proper Claude Skills format specified in docs/claude-skills.md.

## Behavior

**With no parameters:**
- Read SKILLS-PROGRESS-AND-ROADMAP.md to find next uncompleted skill
- Create skill file in proper format (YAML frontmatter + markdown body)
- Update SKILLS-PROGRESS-AND-ROADMAP.md progress tracking
- Show completion status

**Parameters:**
- `--auto`: Automatically create next skill from queue without interaction
- `--skill NAME`: Create specific named skill
- `--batch N`: Create next N skills from queue
- `--menu`: Show interactive menu (default if no params)

## Task

1. **Read Progress File**
   - Read .claude/skills/SKILLS-PROGRESS-AND-ROADMAP.md
   - Parse skill list (54 total)
   - Identify next skill with status ⏸️ (not started) or 🔄 (in progress)

2. **Gather Context**
   - Identify skill category (backend, frontend, database, domain, etc.)
   - Find relevant OmniWatchAI architecture docs for context
   - Review existing skills in same category for pattern

3. **Generate Skill File**
   - Create file in `.claude/skills/{category}/{skill-name}.md`
   - **YAML Frontmatter (REQUIRED):**
     ```yaml
     ---
     name: {Skill Name} (max 64 chars)
     description: {What skill does and when to use it} (max 1024 chars)
     ---
     ```
   - **Markdown Body:**
     - # {Skill Title}
     - ## Context (OmniWatchAI platform background)
     - ## Inputs (required parameters)
     - ## Output (what gets generated)
     - ## Example Usage (detailed OmniWatchAI-specific example)
     - ## Expected Output (code sample)
     - ## Best Practices
     - ## Tags

4. **Update Progress**
   - Mark skill as ✅ COMPLETED in SKILLS-PROGRESS-AND-ROADMAP.md
   - Add completion timestamp
   - Increment counter (X/54 complete)

5. **Report**
   - Show: "Created {skill-name}.md ({X}/54 complete)"
   - Show next skill: "Next: {next-skill-name}"
   - If all 54 complete: "All skills complete! Generate final index?"

## Skill Format Requirements (per docs/claude-skills.md)

**YAML Frontmatter (Lines 1-4):**
```yaml
---
name: Skill Name Here
description: Brief description of what this skill does and when Claude should use it
---
```

**Markdown Body:**
- Clear, step-by-step instructions
- OmniWatchAI-specific context
- Concrete examples with proper parameters
- Expected output (code samples)
- Best practices for OmniWatchAI

**File Location:**
`.claude/skills/{category}/{skill-name}.md`

## Example Skill Structure

```markdown
---
name: Generate API Controller
description: Generate ASP.NET Core Web API controller for OmniWatchAI with authentication, RBAC, logging, and Swagger documentation. Use when creating new API endpoints for servers, compliance, configuration, or monitoring.
---

# Generate ASP.NET Core API Controller for OmniWatchAI

[Instructions, context, examples, best practices...]
```

## Important

- **Unique Skills:** Each skill must be unique and specific to its purpose
- **OmniWatchAI Context:** All skills include OmniWatchAI platform context (150 servers, 9 personas, RBAC, etc.)
- **Proper Format:** Strictly follow Claude Skills specification (YAML frontmatter required)
- **Progress Tracking:** Always update SKILLS-PROGRESS-AND-ROADMAP.md after creating skill
- **Quality:** Match quality and detail of existing 8 skills

## Context Files

**Skill Queue:** .claude/skills/SKILLS-PROGRESS-AND-ROADMAP.md
**Skill Format Spec:** docs/claude-skills.md
**OmniWatchAI Specs:** docs/enhancements/*.md (41 architecture documents)
**Existing Skills:** .claude/skills/*/*.md (8 examples as templates)
