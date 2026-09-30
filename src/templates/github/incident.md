<!-- guide: Incident: a defect or gap in an existing contract or behaviour, written so a session with
     none of the author's context can act on it. Every factual sentence cites its source: a file and
     line at a named commit, a command and its output, a run or session ID, or a URL. Facts, proposals
     and the owner's decisions stay in separate sections. Proposals are labelled "Proposed". Nothing
     aspirational: no future benefit, effort or certainty without a cited basis. Write
     "Unknown: <what is missing>" rather than guess. Delete every guide comment before posting.
     Title: "<component or document>: <what is wrong>", in plain words. -->

## Summary

<!-- guide: Two to four sentences of fact: what is wrong or missing, where, and how it showed up.
     No proposal here. End with what the issue asks for: a decision (section 4), a fix, or both. -->

{{What is wrong or missing, where, and how it showed up.}}

This issue asks {{the owner}} for a decision (section 4), then gives exact steps for implementing
it (sections 5 to 8). **Don't start implementing until {{the owner}} has recorded the decision as a
comment on this issue.**

## 1. Where the gap is

<!-- guide: Pin the revision first: every reference below is to one commit. For a versioned document,
     give its version, status and SHA-256 at that commit. Quote the relevant text exactly, as a block
     quote, with path:line. Name the rules that bear on the choice, also quoted with path:line. -->

Every reference below is to `{{branch}}` at `{{short SHA}}` ({{what that commit is}}, {{date}}).
There, `{{path of the governing document}}` is **version {{N}}, `status: {{status}}`**, with
SHA-256 `{{sha256}}`.

- `{{path}}` line {{N}}: {{what it says, quoted exactly}}
- `{{path}}` line {{N}}, quoted in full:

  > {{exact text}}

**The rules that bear on the choice:**
- `{{path}}` line {{N}}: "{{exact text}}"

## 2. Evidence

<!-- guide: How it was found, and the run that shows it: the session or run ID, tool and model versions,
     the plugin or build revision, the fixture or input, the exact request and answers. Mark evidence
     that exists only on one machine as local, with a ~ path, and say what was overwritten. Rebuild a
     timeline from the transcript or logs, in UTC. -->

**Found by:** {{session or person}}, while {{activity}} on {{date}}. It is recorded in {{where}}.

**The run:**
- {{Session or run ID}}, {{tool and version}}, {{model}}.
- Build: {{revision and how it was loaded}}.
- Input: `{{fixture path}}` ({{what it seeds}}).
- Request: `{{exact request}}`.
- Answers: {{the answers given, and how}}.
- Transcript: `{{~ path}}`, on {{whose}} machine only ({{retention}}).

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

<!-- guide: One row per option, each with its consequence. Label one option "(proposed)" only when the
     evidence supports it, and say why in its row. The status is "pending" until the owner decides;
     "decided" cites who, when and where. Implementation below covers the proposed option only. -->

**Status: pending.** Record the choice as a comment on this issue, such as "Decision: Option A".

| Option | {{What the option decides}} | Consequence |
|---|---|---|
| **A (proposed)** | {{option}} | {{consequence, with the evidence that supports it}} |
| B | {{option}} | {{consequence}} |

If {{the owner}} picks another option, **stop and ask for revised steps**: sections 5 to 8
implement Option A only.

## 5. Implementation (Option A)

<!-- guide: Written for a session that has none of the author's context. Name the repository's rules to
     read first. List preconditions that must hold, and what to do when one doesn't. For every edit,
     give the file, the exact text to replace (checked to occur exactly once; say so when it is
     wrapped across lines) and the exact new text. Say which files are not changed. -->

Read {{the repository's instruction files}} first. They hold {{the rules that matter here}}.

**Preconditions:**
1. {{The owner}} has commented "Decision: Option A" on this issue.
2. {{Revision or text that must still hold}}. If it differs from the quotes above, stop and report
   the difference.
3. {{Where to work, with the exact command}}

**5.1 `{{path}}`:**
- replace
  `{{exact old text}}`
  with
  `{{exact new text}}`

**Not changed:** {{files that must stay unchanged, and how to confirm it}}.

## 6. Verification

<!-- guide: Every command, from where to run it, and the output expected from each. Manual checks name the
     runbook section and what to record. Anything that costs money or time is the owner's decision:
     state the cost and ask. -->

Run these from {{where}}. Each must pass, with the output shown:

```
{{command}}
```

- Expected output: {{exact expected output}}.
- **Manual:** {{steps or runbook section}}; record {{what}}.
- **{{Paid or long step}}: {{owner}} decides.** {{Why it may not be needed, the cost, and where the
  commands are}}.

## 7. Acceptance criteria

- [ ] {{The owner}}'s decision is recorded on this issue.
- [ ] {{Each change, checkable}}
- [ ] Every command in section 6 passes, with its output shown.
- [ ] No push, PR or merge happens unless {{the owner}} asks.

## 8. Out of scope

- {{Related work not done here, and why, with where it will be handled}}

## References

- {{path, section or line, and what it is}}
- This issue was written by {{tool and session ID}} on {{date}}, at {{whose}} request.
