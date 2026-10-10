---
type: llm
---

Everything the brainstorm behind the briefs (BRN-001, "Shiftlog: record shifts") says that a brief may quote:
- Context: Shift workers record when they start and stop work, and want to see the hours they worked each week.
- Problem PRB-01, raised by shift workers, evidence "Interview notes": "Workers lose track of the hours they worked each week".
- Target users: Shift workers.
- Promoted ideas: IDEA-01 "Add a shift from the terminal", IDEA-02 "List shifts in a table", IDEA-03 "A weekly report page" and
  IDEA-06 "A dark theme for the report page". (IDEA-04 "Export shifts as CSV" names no screen; IDEA-05 "Sync to a server" is
  parked.)
- Assumption ASM-01: "We believe that workers will record shifts every day."
- Candidate success signal: The hours worked each week are right (quoted as "The hours worked each week are right").


Judge the Context and the Content of each brief in the agent's output. A pass needs all of these:
- Each Context is two or three sentences about who uses the flow and the one job it does. It may paraphrase the context, the users
  and the problem above in other words.
- Each Content quotes the wording of one or more of the sources above (an idea, the problem, the assumption, the success signal),
  and lists the flow's screens in order.
- A state a Content names is acceptable when the ideas could support it: an empty state ("no shift recorded yet", "a week with no
  shifts"), a state with data, an error, a loading or a mid-flow state. The words empty, error and loading need not appear.
- Neither adds a feature, data or copy that nothing above supports. A quote of any source above is supported.
Anything else is not a pass.
