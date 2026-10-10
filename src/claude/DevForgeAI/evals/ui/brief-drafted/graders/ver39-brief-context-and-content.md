---
type: llm
---

The brainstorm behind the briefs holds these promoted ideas: IDEA-01 "Add a shift from the terminal", IDEA-02 "List shifts in a
table", IDEA-03 "A weekly report page" and IDEA-06 "A dark theme for the report page" (IDEA-04 "Export shifts as CSV" names no
screen). Its problem PRB-01 reads "Workers lose track of the hours they worked each week". Its assumption reads "We believe that
workers will record shifts every day." Its context says: Shift workers record when they start and stop work, and want to see the
hours they worked each week.

Judge the Context and the Content of each brief in the agent's output. A pass needs all of these:
- Each Context is two or three sentences about who uses the flow and the one job it does.
- Each Content quotes the wording of one or more of the ideas or the problem above, and lists the flow's screens in order.
- A state a Content names is acceptable when the ideas could support it: an empty state ("no shift recorded yet", "a week with no
  shifts"), a state with data, an error, a loading or a mid-flow state. The words empty, error and loading need not appear.
- Neither adds a feature, data or copy that the ideas, the problem and the assumption above do not support.
Anything else is not a pass.
