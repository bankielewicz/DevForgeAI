---
type: llm
---

The workspace held BRN-001 (Shiftlog: record shifts) and no boards folder. Its promoted ideas IDEA-01 (Add a shift from the
terminal), IDEA-02 (List shifts in a table), IDEA-03 (A weekly report page) and IDEA-06 (A dark theme for the report page)
name screens, and IDEA-04 (Export shifts as CSV) names none. The session had no Artifact tool, and the request said to
proceed without questions. The reply may begin with a checklist.

Judge only the final reply. The regular-expression graders already check the exact closing line, the cell grid or size and the
words "propose one"; you judge the shape and the substance.
PASS if all of these hold:
- It proposes how the screens the ideas name group into flows (one flow for the release, or two such as a terminal flow of
  IDEA-01 and IDEA-02 and a web flow of IDEA-03 and IDEA-06), with the key screen and the surface of each, and says the
  grouping is unconfirmed.
- It shows one brief for each proposed flow, whatever the grouping. Each brief starts with a lead line that names the flow and
  the product (Shiftlog), then has a Context, a Content, Must-haves and a Style, in that order, and ends with the closing line
  that asks for 3 distinctly different directions of the key screen first.
- Each Context is two or three sentences about who uses the flow and the one job it does.
- Each Content quotes the wording of the brainstorm's ideas or problems and lists the flow's screens in order. The states it
  names must be ones the ideas could support: an empty state such as "no shift recorded yet", a list or week with data, an
  error, a loading or a mid-flow state. The words empty, error and loading need not appear. It invents no feature the ideas do
  not name.
- Each Must-haves is two to four short constraints (written on one line and separated by commas or semicolons counts as
  several items): the surface and its size, and for a terminal flow a monospace cell grid of columns by rows.
- Each brief describes the problem and prescribes no layout: no positions, spacing, sizes of parts or component-by-component
  arrangement. A surface, a screen size or a cell grid is a constraint, not a layout.
- It says that the session has no Artifact tool, that nothing was made or sent, and names docs/specs/design/DSN-001/boards/.
FAIL if any of these is missing, or if the reply draws a mockup of a screen with characters (the words "box-drawing characters"
inside a brief's Must-haves are a constraint on the canvas, not a drawing).
