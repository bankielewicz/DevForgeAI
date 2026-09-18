# Retrieved guidance extract: Claude Code skills `allowed-tools` / `disallowed-tools`

source_id: claude-code-skills
url: https://code.claude.com/docs/en/skills
retrieved_at_utc: 2026-09-17
retained_bytes: claude-code-skills-20260917.html
retained_bytes_sha256: 26eebfd9f5ee65177f0adbc5ce7a04cad668ffc10acdda98eecb0860e055041e
retrieval_method: HTTP GET (curl, read-only). Full response body retained verbatim and digested.
representation_honesty: >
  The passages below were located inside the retained bytes by literal substring search and are
  quoted from them. Byte offsets are zero-based and refer to claude-code-skills-20260917.html as
  retained in this run. The page is a server-rendered SPA payload, so the same sentence also
  appears once inside an embedded JSX hydration string; the offsets cited are the rendered prose
  occurrence. This establishes the content of the identified snapshot, not live-site permanence.

## Passage A - `allowed-tools` (section "Pre-approve tools for a skill")

Key phrase byte interval: start_byte 356035, end_byte 356078 (`does not restrict which tools are available`).

> The `allowed-tools` field grants permission for the listed tools during the turn that invokes the
> skill, so Claude can use them without prompting you for approval. The grant clears when you send
> your next message, even though the skill content stays in context; invoking the skill again
> re-applies it for that turn. It does not restrict which tools are available: every tool remains
> callable, and your permission settings still govern tools that are not listed. To pre-approve
> tools for the whole session rather than a single turn, add allow rules to those permission
> settings instead.

## Passage B - `disallowed-tools`

Passage byte offset: approximately 364405.

> To remove tools from Claude's available pool while a skill is active, list them in
> `disallowed-tools` in the skill's frontmatter. The restriction clears when you send your next
> message. Like deny rules, the field can't remove `EndConversation` while any other tool remains.
> To block tools across all skills and prompts, add deny rules in your permission settings.

## Bearing on this assessment

`allowed-tools` is a per-turn permission pre-approval. It does not remove tools from the callable
pool, so omitting a tool from `allowed-tools` does not make that tool unreachable.
`disallowed-tools` is the field that removes tools from the pool.
