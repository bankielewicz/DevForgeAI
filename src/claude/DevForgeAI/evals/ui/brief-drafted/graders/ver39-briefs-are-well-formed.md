---
type: llm
---

The workspace held BRN-001 (Shiftlog: record shifts) and no boards folder. Its promoted ideas IDEA-01 (Add a shift from the
terminal), IDEA-02 (List shifts in a table), IDEA-03 (A weekly report page) and IDEA-06 (A dark theme for the report page)
name screens, and IDEA-04 (Export shifts as CSV) names none. The session had no Artifact tool, and the request said to
proceed without questions.

Judge only the final reply.
PASS if all of these hold:
- It lists the screens the ideas name and proposes how they group into flows (one flow for the release, or two such as
  a terminal flow of IDEA-01 and IDEA-02 and a web flow of IDEA-03 and IDEA-06), with the key screen and the surface of
  each flow, and says the grouping is unconfirmed.
- It shows one brief for each proposed flow, whatever the grouping. Each brief has these parts, in order: a lead line that
  names the flow and the product (Shiftlog); a Context of two or three sentences; a Content that quotes at least one of
  the flow's ideas, lists the flow's screens in order and names at least one state (empty, error, loading or mid-flow);
  Must-haves of two to four items that state a monospace cell grid of columns by rows for a terminal flow, or a surface and
  a size for a web one; a Style that says to propose one and holds no hex value and no px size; and the exact closing line
  "Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each."
- A brief describes the problem and prescribes no layout: no positions, spacing, sizes of parts or component-by-component
  arrangement, and it invents no content the ideas do not support.
- It says that the session has no Artifact tool, that nothing was made or sent, and names docs/specs/design/DSN-001/boards/.
FAIL if any of these is missing, or if the reply draws a mockup of a screen.
