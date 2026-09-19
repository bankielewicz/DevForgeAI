# Retrieved passage: allowed-tools / disallowed-tools

source_id: claude-code-skills
url: https://code.claude.com/docs/en/skills
retrieved_at_utc: 2026-09-19T02:16Z
retrieval_method: WebFetch (read-only)
representation: model-extracted quotation of the live page; not a full-page byte capture
refresh_of: prior run 20260918T202845Z retained extract sha256
  07ab488c43a12359f780f22864a129240e9f89d46c17b1f71fd4a77ae11dd67f

## allowed-tools (quoted)

"Tools Claude can use without asking permission during the turn that invokes this skill.
The grant clears when you send your next message. Accepts a space- or comma-separated
string, or a YAML list."

"It does not restrict which tools are available: every tool remains callable, and your
permission settings still govern tools that are not listed."

## disallowed-tools (quoted)

"Tools removed from Claude's available pool while this skill is active. Use for autonomous
skills that should never call certain tools, such as `AskUserQuestion` for a background
loop. Accepts a space- or comma-separated string, or a YAML list. The restriction clears
when you send your next message. Like deny rules, the field can't remove EndConversation
while any other tool remains."

## Bearing on this run

1. The corrected passage at SKILL.md line 33 states that `allowed-tools` "pre-approves the
   listed tools for the invoking turn and does not remove the unlisted ones". The live page
   says the grant applies "during the turn that invokes this skill" and "does not restrict
   which tools are available: every tool remains callable". The corrected text is an
   accurate representation of this source. Prior finding F-c3d23eda is resolved.
2. The live page states `allowed-tools` "Accepts a space- or comma-separated string, or a
   YAML list", so the package's YAML-list form is valid on this host. The Agent Skills
   specification defines only the space-separated string, so FMT-003 remains a recorded
   source divergence and an advisory row, never a defect.

## Limitation

Extraction was performed by the fetch tool's summarizing model against the live page. A
byte-exact page capture was not retained. The digest covers this retained extract only.
