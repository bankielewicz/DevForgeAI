<!-- guide: Enhancement: a new capability or a change to a working one, written so a session with none of
     the author's context can act on it with only this post and the repository. Every factual sentence
     cites its source: a file and line at a named commit, a command and its output, or who asked for it
     and where. Facts, proposals and the owner's decisions stay in separate sections. Proposals are
     labelled "Proposed". Nothing aspirational: no benefit, saving or effort estimate without a cited
     basis. Write "Unknown: <what is missing>" rather than guess. Citations use the form the check
     reads: `path` line N (or lines N–M), optionally "at <SHA>", then `: "quote"` or a > block quote;
     write an omission inside a quote as … Delete every guide comment before posting.
     Title: "<component or document>: <what it should do>", in plain words. -->

## Summary

<!-- guide: Two to four sentences: what exists today, what is asked for, and who asked. Then the next
     action, exactly one of:
       investigate: what is needed or how to provide it isn't established yet;
       decide: a supported proposal needs the owner's choice, and none is recorded;
       implement: the proposal is decided (cite it) or needs no decision.
     Then ONE of the two closing sentences below, and delete the other. -->

{{What exists today, what is asked for, and who asked.}}

**Next action: {{investigate | decide | implement}}.**

This issue asks {{the owner}} for a decision (section 4), then gives exact steps for implementing
it (sections 5 to 8). **Don't start implementing until {{the owner}} has recorded the decision as a
comment on this issue.**

Decided by {{who}} on {{date}} ({{where: a conversation, a comment URL or a record}}): "{{the
decision, quoted}}". Sections 5 to 8 implement it.

## 1. Current behaviour

<!-- guide: What the product or contract does now, pinned to one commit, with the governing text quoted
     exactly in the citation form. Say what is missing, not what would be nicer. -->

Every reference below is to `{{branch}}` at `{{SHA}}` ({{what that commit is}}, {{date}}).

- `{{path}}` line {{N}}: "{{exact text}}"

## 2. Motivation

<!-- guide: Who asked, when and where (a quote, an issue, a decision record). The concrete situation that
     can't be handled today, with evidence the reader can open: committed, quoted here, or at a URL.
     Local-only evidence is supporting evidence, marked local, with the needed parts quoted. Any benefit
     claimed needs a cited basis, such as a measurement or a recorded incident; otherwise leave it out. -->

- **Requested by:** {{who}}, {{when}}, {{where}}: "{{their words}}".
- **The situation today:** {{what happens now, with evidence}}.

## 3. Proposed behaviour

<!-- guide: Labelled Proposed throughout. Name each specification item added or changed (for example a new
     BEH or VER item, or the exact sentence changed), and each file or component affected. Keep the
     proposal to what the motivation needs. For next action investigate, say what must be established
     before a proposal can be made. -->

**Proposed:**
- {{behaviour, with the spec items it adds or changes}}

## 4. Decision required ({{owner}})

<!-- guide: Only when a choice belongs to the owner; otherwise delete this section. One row per option,
     each with its consequence. Pending: label at most one option "(proposed)" and keep the "If …
     picks another option" sentence. Decided: use the decided status line, label the chosen option
     "(decided)", and delete that sentence. -->

**Status: pending.** Record the choice as a comment on this issue, such as "Decision: Option A".

**Status: decided** by {{who}} on {{date}} ({{where}}): "{{the decision, quoted}}".

| Option | {{What the option decides}} | Consequence |
|---|---|---|
| **A (proposed)** | {{option}} | {{consequence}} |
| B | {{option}} | {{consequence}} |

If {{the owner}} picks another option, **stop and ask for revised steps**: sections 5 to 8
implement Option A only.

## 5. Implementation (Option A)

<!-- guide: For next action decide or implement; for investigate, replace it with "5. Investigation"
     below. Name the repository's rules to read first and the preconditions. Give exact old and new text,
     or a new file's exact content, only where the evidence fully determines it (old text checked to
     occur exactly once); otherwise a bounded step with the check that confirms it. Say which files are
     not changed. -->

Read {{the repository's instruction files}} first.

**Preconditions:**
1. {{Pending only: The owner has commented "Decision: Option A" on this issue.}}
2. {{Revision or text that must still hold}}. If it differs, stop and report the difference.
3. {{Where to work, with the exact command}}

**5.1 `{{path}}`:**
- replace
  `{{exact old text}}`
  with
  `{{exact new text}}`

**Not changed:** {{files that must stay unchanged}}.

## 5. Investigation

<!-- guide: For next action investigate; delete the Implementation section above. -->

- **Questions to answer:** {{each question}}
- **Where to look:** `{{path}}`, `{{command}}`
- **What to record:** {{outputs, SHAs, versions}}
- **Stop when:** {{the condition that ends the investigation}}
- **Report back:** a comment on this issue with {{the findings, each with its evidence}}, and a
  proposal.

## 6. Verification

<!-- guide: Every command, from where to run it, and the output expected from each. Manual checks name the
     runbook section and what to record. Anything that costs money or time is the owner's decision. -->

```
{{command}}
```

- Expected output: {{exact expected output}}.
- **Manual:** {{steps}}; record {{what}}.

## 7. Acceptance criteria

- [ ] {{Pending only: The owner's decision is recorded on this issue.}}
- [ ] {{Each change or finding, checkable}}
- [ ] Every command in section 6 passes, with its output shown.
- [ ] No push, PR or merge happens unless {{the owner}} asks.

## 8. Out of scope

- {{Related work not done here, and why}}

## References

- {{path, section or line, and what it is}}
- This issue was written by {{tool and session ID}} on {{date}}, at {{whose}} request.
