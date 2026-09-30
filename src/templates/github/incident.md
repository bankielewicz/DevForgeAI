<!-- guide: Incident: a defect or gap in an existing contract or behaviour, written so a session with
     none of the author's context can act on it with only this post and the repository. Every
     factual sentence cites its source: a file and line at a named commit, a command and its output,
     a run or session ID, or a URL. Facts, proposals and the owner's decisions stay in separate
     sections. Proposals are labelled "Proposed". Nothing aspirational: no future benefit, effort or
     certainty without a cited basis. Write "Unknown: <what is missing>" rather than guess.
     Citations use the form the check reads: `path` line N (or lines N–M), optionally "at <SHA>",
     then `: "quote"` or a > block quote; write an omission inside a quote as …
     Delete every guide comment before posting.
     Title: "<component or document>: <what is wrong>", in plain words. -->

## Summary

<!-- guide: Two to four sentences of fact: what is wrong or missing, where, and how it showed up.
     No proposal here. Then the next action, exactly one of:
       investigate: the evidence doesn't establish the cause, or no solution is supported yet;
       decide: a supported solution needs the owner's choice, and none is recorded;
       implement: the solution is decided (cite it) or needs no decision, and the evidence supports it.
     Then ONE of the two closing sentences below, and delete the other:
       pending decision: keep the "Don't start implementing…" sentence;
       decided, or no decision needed: keep the "Decided by…" sentence (or delete both). -->

{{What is wrong or missing, where, and how it showed up.}}

**Next action: {{investigate | decide | implement}}.**

This issue asks {{the owner}} for a decision (section 4), then gives exact steps for implementing
it (sections 5 to 8). **Don't start implementing until {{the owner}} has recorded the decision as a
comment on this issue.**

Decided by {{who}} on {{date}} ({{where: a conversation, a comment URL or a record}}): "{{the
decision, quoted}}". Sections 5 to 8 implement it.

## 1. Where the gap is

<!-- guide: Pin the revision first: every reference below is to one commit. For a versioned document,
     give its version, status and SHA-256 at that commit. Quote the relevant text exactly, with its
     path and line in the citation form. Name the rules that bear on the choice, quoted the same way. -->

Every reference below is to `{{branch}}` at `{{SHA}}` ({{what that commit is}}, {{date}}).
There, `{{path of the governing document}}` is **version {{N}}, `status: {{status}}`**, with
SHA-256 `{{sha256}}`.

- `{{path}}` line {{N}}: "{{exact text}}"
- `{{path}}` lines {{N}}–{{M}}, quoted in full:

  > {{exact text}}

**The rules that bear on the choice:**
- `{{path}}` line {{N}}: "{{exact text}}"

## 2. Evidence

<!-- guide: How it was found, and the run that shows it: the session or run ID, tool and model versions,
     the build revision and how it was loaded, the fixture or input, the exact request and answers, and
     a timeline in UTC. Everything the next action depends on must be readable with only this post and
     the repository: committed, quoted here, or at a URL. Evidence that exists on one machine only (such
     as a transcript) is supporting evidence: mark it local, cite it with a ~ path, say what was
     overwritten, and quote here the parts the next action needs. -->

**Found by:** {{session or person}}, while {{activity}} on {{date}}. It is recorded in {{where}}.

**The run:**
- {{Session or run ID}}, {{tool and version}}, {{model}}.
- Build: {{revision and how it was loaded}}.
- Input: `{{fixture path}}` ({{what it seeds}}).
- Request: `{{exact request}}`.
- Answers: {{the answers given, and how}}.
- Transcript (supporting, local): `{{~ path}}`, on {{whose}} machine only ({{retention}}). The parts
  this issue depends on are quoted below.

**Timeline (UTC, {{date}}):**

| Time | What happened |
|---|---|
| {{hh:mm:ss}} | {{event, quoting the output where it matters}} |

**The final state:** {{what was verified at the end, and by whom}}.

## 3. Why it matters

<!-- guide: Observed consequences only, each tied to the evidence above. A consequence that hasn't been
     observed is labelled as a possibility and says why it is possible. Say what the current checks
     can and can't catch. -->

- {{observed consequence, citing the evidence}}

## 4. Decision required ({{owner}})

<!-- guide: Only when a choice belongs to the owner; otherwise delete this section. One row per option,
     each with its consequence. Pending: label at most one option "(proposed)", only when the evidence
     supports it, and keep the "If … picks another option" sentence. Decided: replace the status line
     with the decided form, label the chosen option "(decided)", and delete the "picks another option"
     sentence. -->

**Status: pending.** Record the choice as a comment on this issue, such as "Decision: Option A".

**Status: decided** by {{who}} on {{date}} ({{where}}): "{{the decision, quoted}}".

| Option | {{What the option decides}} | Consequence |
|---|---|---|
| **A (proposed)** | {{option}} | {{consequence, with the evidence that supports it}} |
| B | {{option}} | {{consequence}} |

If {{the owner}} picks another option, **stop and ask for revised steps**: sections 5 to 8
implement Option A only.

## 5. Implementation (Option A)

<!-- guide: For next action decide or implement; for investigate, replace this section with
     "5. Investigation" below. Written for a session that has none of the author's context. Name the
     repository's rules to read first, and the preconditions with what to do when one doesn't hold.
     Give exact old and new text (or a new file's exact content) only where the evidence fully
     determines the change: the old text is checked to occur exactly once, and wrapping across lines
     is noted. A change that can't be fixed exactly without running code is a bounded step with the
     check that confirms it, never a guessed patch. Say which files are not changed. -->

Read {{the repository's instruction files}} first. They hold {{the rules that matter here}}.

**Preconditions:**
1. {{Pending only: The owner has commented "Decision: Option A" on this issue.}}
2. {{Revision or text that must still hold}}. If it differs from the quotes above, stop and report
   the difference.
3. {{Where to work, with the exact command}}

**5.1 `{{path}}`:**
- replace
  `{{exact old text}}`
  with
  `{{exact new text}}`

**5.2 {{A change that can't be written exactly}}:** {{the bounded step}}. Confirm it with
`{{command}}`, which prints {{expected output}}.

**Not changed:** {{files that must stay unchanged, and how to confirm it}}.

## 5. Investigation

<!-- guide: For next action investigate; delete the Implementation section above. Say exactly what to
     find out and how, when to stop, and what to report, so the next session doesn't guess a fix. -->

- **Questions to answer:** {{each question}}
- **Where to look:** `{{path}}`, `{{command}}`
- **How to reproduce:** {{exact steps, from where, with the expected symptom}}
- **What to record:** {{outputs, SHAs, versions}}
- **Stop when:** {{the condition that ends the investigation}}
- **Report back:** a comment on this issue with {{the findings, each with its evidence}}, and a
  proposed next action.

## 6. Verification

<!-- guide: Every command, from where to run it, and the output expected from each. Manual checks name the
     runbook section and what to record. Anything that costs money or time is the owner's decision:
     state the cost and ask. For an investigation, say how the findings are checked. -->

Run these from {{where}}. Each must pass, with the output shown:

```
{{command}}
```

- Expected output: {{exact expected output}}.
- **Manual:** {{steps or runbook section}}; record {{what}}.
- **{{Paid or long step}}: {{owner}} decides.** {{Why it may not be needed, the cost, and where the
  commands are}}.

## 7. Acceptance criteria

- [ ] {{Pending only: The owner's decision is recorded on this issue.}}
- [ ] {{Each change or finding, checkable}}
- [ ] Every command in section 6 passes, with its output shown.
- [ ] No push, PR or merge happens unless {{the owner}} asks.

## 8. Out of scope

- {{Related work not done here, and why, with where it will be handled}}

## References

- {{path, section or line, and what it is}}
- This issue was written by {{tool and session ID}} on {{date}}, at {{whose}} request.
