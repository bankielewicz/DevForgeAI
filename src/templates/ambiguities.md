---
id: AMB-000
type: ambiguities
title: ""              # the work item this log belongs to, e.g. "STORY-012: request a magic link"
status: open           # open | reviewed (every entry accepted or rejected)
version: 1             # appending an entry doesn't bump it; a decision on an entry does
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: ""              # the human who reviews the entries
authors: []
generated_by:
  tool: ""
  model: ""
  session: ""
reviewed_by: []
approved_by: ""        # not used: each entry records its own decision
approved_on: null
upstream: []           # e.g. {id: STORY-012, relation: informed_by, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- ambiguities-specific ---
work_item: ""          # the story ID, or the branch name when there is no story
---

# AMB-000 — Ambiguities log: <work item>

<!-- The pressure relief valve (ADR-004 D8). A skill or session that meets a small choice
     does not stop for it: it records the choice here and continues, and a human reviews
     the entries later. One log per work item (one story, or one branch), so parallel
     worktrees never append to the same file. Named by ID only, like every document:
     docs/specs/ambiguities/AMB-NNN.md, the next free number. The log is reused across
     sessions: a later session appends to the work item's existing log, and only a work
     item without a log gets a new one.

     RECORD AND CONTINUE (then review later):
       - a small, reversible choice outside every spec and AC obligation, for example a
         library patch or minor version within the range tech-stack.md allows, a naming or
         wording choice, a test-fixture detail, or a folder a context document doesn't name;
       - an unknown that doesn't affect the current work.
     Routine choices the spec already leaves to the implementer need no entry.

     ASK THE USER; NEVER LOG INSTEAD:
       - anything that changes required behaviour, scope, an interface, permissions or security;
       - a spec or AC obligation;
       - a policy value or an approval;
       - a new dependency, or a major version.

     HARD BOUNDARY: logging never authorizes contradicting a spec, inventing a requirement
     or bypassing an approval. Writing an assumption down doesn't approve it.

     REVIEW: entries are reviewed at the pull request, and QA lists the open ones in its
     verdict. The owner accepts an entry (the change stays, and the context skill folds it
     into the right context document when one applies) or rejects it (the change is
     reverted, following its "reverse" field). Delete these comments when you fill it in. -->

## Entries

<!-- One item per choice. Qualified reference: AMB-000#ENT-01. Never delete an entry;
     a rejected one stays, with its resolution. -->

```yaml items
entries:
  - id: ENT-01
    status: active
    date: YYYY-MM-DD
    recorded_by: ""        # e.g. "claude-code (session <ID>)"
    question: ""           # what happened, and the question the owner must answer
    checked: []            # sources read before deciding, e.g. ["docs/specs/context/tech-stack.md (CTX-003 v2)"]
    action: ""             # the change made, e.g. "bumped serde 1.0.210 → 1.0.214 (in range ^1.0)", or "none"
    reverse: ""            # how to undo it, e.g. "revert commit <sha>" or "set serde back to 1.0.210"
    impact: ""             # what depends on it, and what can proceed meanwhile
    resolve_before: ""     # the step that needs the answer, e.g. "PR review" or "the spec step"
    relates_to: []         # qualified references, e.g. ["CTX-003", "STORY-012#AC-02"]
    state: open            # open | accepted | rejected
    decided_by: ""         # the human who accepted or rejected it
    decided_on: null
    resolution: ""         # what happened on the decision, e.g. "folded into CTX-003 v3" or "reverted in <sha>"
```
