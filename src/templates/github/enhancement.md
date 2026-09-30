<!-- guide: Enhancement: a new capability or a change to a working one, written so a session with none of
     the author's context can act on it. Every factual sentence cites its source: a file and line at a
     named commit, a command and its output, or who asked for it and where. Facts, proposals and the
     owner's decisions stay in separate sections. Proposals are labelled "Proposed". Nothing
     aspirational: no benefit, saving or effort estimate without a cited basis. Write
     "Unknown: <what is missing>" rather than guess. Delete every guide comment before posting.
     Title: "<component or document>: <what it should do>", in plain words. -->

## Summary

<!-- guide: Two to four sentences: what exists today, what is asked for, and who asked. End with what the
     issue asks for: a decision (section 4), then the implementation. -->

{{What exists today, what is asked for, and who asked.}}

This issue asks {{the owner}} for a decision (section 4), then gives exact steps for implementing
it (sections 5 to 8). **Don't start implementing until {{the owner}} has recorded the decision as a
comment on this issue.**

## 1. Current behaviour

<!-- guide: What the product or contract does now, pinned to one commit, with the governing text quoted
     exactly with path:line. Say what is missing, not what would be nicer. -->

Every reference below is to `{{branch}}` at `{{short SHA}}` ({{what that commit is}}, {{date}}).

- `{{path}}` line {{N}}: "{{exact text}}"

## 2. Motivation

<!-- guide: Who asked, when and where (a quote, an issue, a decision record). The concrete situation that
     can't be handled today, with evidence. Any benefit claimed needs a cited basis, such as a
     measurement or a recorded incident; otherwise leave it out. -->

- **Requested by:** {{who}}, {{when}}, {{where}}: "{{their words}}".
- **The situation today:** {{what happens now, with evidence}}.

## 3. Proposed behaviour

<!-- guide: Labelled Proposed throughout. Name each specification item added or changed (for example a new
     BEH or VER item, or the exact sentence changed), and each file or component affected. Keep the
     proposal to what the motivation needs. -->

**Proposed:**
- {{behaviour, with the spec items it adds or changes}}

## 4. Decision required ({{owner}})

<!-- guide: One row per option, each with its consequence. Label one option "(proposed)" only when the
     evidence supports it. The status is "pending" until the owner decides; "decided" cites who, when
     and where. Implementation below covers the proposed option only. -->

**Status: pending.** Record the choice as a comment on this issue, such as "Decision: Option A".

| Option | {{What the option decides}} | Consequence |
|---|---|---|
| **A (proposed)** | {{option}} | {{consequence}} |
| B | {{option}} | {{consequence}} |

If {{the owner}} picks another option, **stop and ask for revised steps**: sections 5 to 8
implement Option A only.

## 5. Implementation (Option A)

<!-- guide: Written for a session that has none of the author's context. Name the repository's rules to
     read first, the preconditions, and for every edit the file, the exact text to replace (checked to
     occur exactly once) and the exact new text, or the exact content of a new file. Say which files are
     not changed. -->

Read {{the repository's instruction files}} first.

**Preconditions:**
1. {{The owner}} has commented "Decision: Option A" on this issue.
2. {{Revision or text that must still hold}}. If it differs, stop and report the difference.
3. {{Where to work, with the exact command}}

**5.1 `{{path}}`:**
- {{exact change}}

**Not changed:** {{files that must stay unchanged}}.

## 6. Verification

<!-- guide: Every command, from where to run it, and the output expected from each. Manual checks name the
     runbook section and what to record. Anything that costs money or time is the owner's decision. -->

```
{{command}}
```

- Expected output: {{exact expected output}}.
- **Manual:** {{steps}}; record {{what}}.

## 7. Acceptance criteria

- [ ] {{The owner}}'s decision is recorded on this issue.
- [ ] {{Each change, checkable}}
- [ ] Every command in section 6 passes, with its output shown.
- [ ] No push, PR or merge happens unless {{the owner}} asks.

## 8. Out of scope

- {{Related work not done here, and why}}

## References

- {{path, section or line, and what it is}}
- This issue was written by {{tool and session ID}} on {{date}}, at {{whose}} request.
