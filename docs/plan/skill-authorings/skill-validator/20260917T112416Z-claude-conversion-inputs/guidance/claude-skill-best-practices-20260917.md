# Retrieved: Skill authoring best practices (Anthropic)

- source_id: `claude-skill-best-practices`
- url: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
  (reached via a 302 from https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices)
- retrieved_at_utc: 2026-09-17
- representation: documentation extraction via the host `WebFetch` tool; NOT raw HTTP bytes.
- limitation: digests bind this retained extraction, not the original transport bytes.

## Section headings

Core principles (Concise is key; Set appropriate degrees of freedom; Test with all models you plan to use) · Skill structure (Naming conventions; Writing effective descriptions; Progressive disclosure patterns; Avoid deeply nested references; Structure longer reference files with table of contents) · Workflows and feedback loops (Use workflows for complex tasks; Implement feedback loops) · Content guidelines (Avoid time-sensitive information; Use consistent terminology) · Common patterns (Template pattern; Examples pattern; Conditional workflow pattern) · Evaluation and iteration (Build evaluations first; Develop Skills iteratively with Claude; Observe how Claude navigates Skills) · Anti-patterns to avoid (Avoid Windows-style paths; Avoid offering too many options) · Advanced: Skills with executable code (Solve, don't defer; Provide utility scripts; Use visual analysis; Create verifiable intermediate outputs; Package dependencies; Runtime environment; MCP tool references; Avoid assuming tools are installed) · Technical notes (YAML frontmatter requirements; Token budgets) · Checklist for effective Skills

## Frontmatter requirements stated here (verbatim)

`name`: "Maximum 64 characters"; "Must contain only lowercase letters, numbers, and hyphens"; "Cannot contain XML tags"; "Cannot contain reserved words: \"anthropic\", \"claude\"".

`description`: "Must be non-empty"; "Maximum 1,024 characters"; "Cannot contain XML tags"; "Should describe what the Skill does and when to use it".

**Conflict recorded:** the Claude Code skills reference page states no `name` length limit and no reserved-word rule, and gives a 1,536-character *listing truncation* for `description`. This page states a 64-character maximum, a reserved-word prohibition and a 1,024-character maximum. Both are retained; the reserved-word and XML-tag rules are carried as advisory, not as a required format rule, because the two official sources disagree.

## Descriptions

"Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems." "Be specific and include key terms". "Each Skill has exactly one description field."

## Progressive disclosure

"Keep SKILL.md body under 500 lines for optimal performance." "Keep references one level deep from SKILL.md." For reference files longer than 100 lines, "include a table of contents at the top".

## Workflows and feedback loops

"Break complex operations into clear, sequential steps." Feedback loop: "Run validator → fix errors → repeat". "Create verifiable intermediate outputs" — the plan-validate-execute pattern for batch, destructive or high-stakes operations.

## Scripts

"Solve, don't defer" — handle error conditions in scripts rather than deferring to the model. No "voodoo constants". Make execution intent explicit: "Run `analyze_form.py` to extract fields" (execute) versus "See `analyze_form.py` for the field extraction algorithm" (read as reference). "Avoid Windows-style paths" — always forward slashes. "Avoid assuming tools are installed."

## Evaluation

"Create evaluations BEFORE writing extensive documentation." Evaluation-driven development: identify gaps, create evaluations, establish baseline, write minimal instructions, iterate. "There is not currently a built-in way to run these evaluations." Checklist: "At least three evaluations created"; "Tested with Haiku, Sonnet, and Opus".

## MCP tool references

"always use fully qualified tool names" in the form `ServerName:tool_name`.
