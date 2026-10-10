---
type: llm
---

The agent was asked to design the UI for a brainstorm (BRN-001, Shiftlog: record shifts) in a session with no Artifact tool, so it
could only draft briefs for Claude Design. Each brief has a lead line, then Context, Content, Must-haves, Style and a closing line;
labels may be bold, plain or followed by a colon, and a brief may sit in a code block.
Judge ONLY the text after "Content:" in each brief, up to its "Must-haves:" label. The lead line, the Context, the Must-haves, the Style, the
closing line and the rest of the reply are judged by other graders. A pass needs all of these:
- Each Content quotes, between quotation marks, the wording of one or more of the sources in the facts below (an idea, the problem,
  the assumption or the success signal).
- Each Content lists the flow's screens in order, with the key screen marked.
- Each Content names at least one state to show. A state is acceptable when the ideas could support it: an empty state ("no shift
  recorded yet", "a week with no shifts"), a state with data, an error, a loading or a mid-flow state. The words empty, error and
  loading need not appear.
Anything else is not a pass.

Everything the brainstorm behind the briefs (BRN-001, "Shiftlog: record shifts") says that a brief may quote:
- The brainstorm's context section: Shift workers record when they start and stop work, and want to see the hours they worked
  each week.
- Problem PRB-01, raised by shift workers, evidence "Interview notes": "Workers lose track of the hours they worked each week".
- Target users: Shift workers.
- Promoted ideas: IDEA-01 "Add a shift from the terminal", IDEA-02 "List shifts in a table", IDEA-03 "A weekly report page" and
  IDEA-06 "A dark theme for the report page". (IDEA-04 "Export shifts as CSV" names no screen; IDEA-05 "Sync to a server" is
  parked.)
- Assumption ASM-01: "We believe that workers will record shifts every day."
- Candidate success signal: The hours worked each week are right (quoted as "The hours worked each week are right").

What the ideas support, in other words (not quotes):
- Surfaces: IDEA-01 and IDEA-02 are screens of a terminal tool; IDEA-03 and IDEA-06 are a web page. A terminal flow and a web flow, and
  a product called a terminal tool or a web app, are supported.
- Jobs: add a shift (IDEA-01); see the recorded shifts in a table (IDEA-02); read the hours worked in a week on a report page
  (IDEA-03), also in a dark theme (IDEA-06).
