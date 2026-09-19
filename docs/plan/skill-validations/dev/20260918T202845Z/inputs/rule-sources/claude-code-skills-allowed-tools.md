# Retrieved passage: allowed-tools / disallowed-tools

source_id: claude-code-skills
url: https://code.claude.com/docs/en/skills
retrieved_at_utc: 2026-09-18T20:33Z
retrieval_method: WebFetch (read-only)
representation: model-extracted quotation of the live page; not a full-page byte capture

## allowed-tools (quoted)

"The `allowed-tools` field grants permission for the listed tools during the turn that
invokes the skill, so Claude can use them without prompting you for approval. The grant
clears when you send your next message, even though the skill content stays in context;
invoking the skill again re-applies it for that turn. It does not restrict which tools are
available: every tool remains callable, and your permission settings still govern tools
that are not listed."

## disallowed-tools (quoted)

"To remove tools from Claude's available pool while a skill is active, list them in
`disallowed-tools` in the skill's frontmatter. The restriction clears when you send your
next message. Like deny rules, the field can't remove EndConversation while any other tool
remains."

## Limitation

Extraction was performed by the fetch tool's summarizing model against the live page.
The quoted sentences are the basis for rule FMT-003/FMT-004 applicability and for the
unenforced_control_claim finding; a byte-exact page capture was not retained.
