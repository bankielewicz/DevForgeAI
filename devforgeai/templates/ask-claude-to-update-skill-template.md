/skill-creator Generate a new skill.  Explore the [skill-name] skill.  Generate a new skill with the same phases/steps as the [skill-name] skill.  This new skill MUST be compatible to work within claude code terminal.  The issue with the current [skill-name] skill is that it results in claude skipping phases/steps due to token optimization bias. The [skill-name] skill will be renamed to spec-driven-*? If not, what are other appropriate names?

Claude's typical response, when I ask it why it skips phases or steps is the following (not verbatim): I skipped steps/phases due to token optimization bias.

If you have Token optimization bias, you're going to get me into trouble.  Token optimization bias hurts me.  Token optimization bias is not helpful.

Token optimization bias is not helpful — it causes Claude to skip steps that exist for good reasons, creates double work for me and Claude, and undermines the framework's integrity.

Every step Claude skips is a step Claude & I have to catch and send Claude back to redo.  Claude will execute every Phase and step fully.

Be Honest. Be objective - never sycophantic.

Always create and present a TODO list to the end user.

these are the traits I'd like claude to exhibit as it's working through the skill.

3 - Generate a plan to create the new skill.  Tell me a few good names for this new skill that'll be used for the DevForgeAI Spec-Driven Development Framework.

When creating a plan, it MUST be self-contained with full documentation, reference links, and progress checkpoints that WILL survive context window clears or new sessions.

Backup related slashcommands into the .claude/commands/backup folder when modifying already existing slashcommands to use the new skill.  Ensure the slashcommand doesn't contain logic as it's an orchestrator for the skill.  Claude must invoke the skill when user enters the slashcommand.

4 - When creating a plan, it MUST be self-contained with full documentation, reference links, and progress checkpoints that WILL survive context window clears or new sessions.

Use AskUserQuestion if you need clarification on any requirement or detect any ambiguity.