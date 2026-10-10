---
type: llm
---

Judge the Must-haves and the Style of each brief in the agent's output. A pass needs all of these:
- Each Must-haves is two to four short constraints. Several constraints written on one line and separated by commas or semicolons
  count as several.
- A terminal flow's Must-haves state a monospace cell grid of columns by rows; a web flow's state the surface and a size. A
  rendering note such as "drawn only with text, box-drawing and block characters", "keyboard-driven" or "readable in a dark theme"
  is a constraint.
- No brief prescribes a solution: no positions, spacing, sizes of parts or component-by-component layout. A surface, a screen size
  or a cell grid is a constraint, not a layout.
- Each Style refers to a design system or says to propose one, and states no colour value, no token and no font size.
Anything else is not a pass.
