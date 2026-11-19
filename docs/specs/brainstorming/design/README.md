# Brainstorm screens: mock-ups from Claude Design

**Status:** directions chosen by Bryan on 2026-11-18; the look is not settled and the further states are not drawn.
Written 2026-11-18 by claude-code on the model Fable 5.2 (session fa59a935-ed2e-4502-b6c4-93bb6d847546). The
boards were downloaded that day from the canvas "DevForgeAI Brainstorm pane",
<https://claude.ai/artifact/UnLaAUN58JATe7Ed4b9Pt4> (version 1795037172-1e31), which Bryan made in Claude Design
from prompts P1 to P5 of [../design-prompts.md](../design-prompts.md). No mod is specified or built.

## Workflow steps these screens show

| Step (SKILL.md's line) | Screens |
|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Intake A, B, C |
| 2 to 4, 6, 7 | Pane A, B, C; Band A, B, C |
| 5. Propose dispositions and ask the user to confirm | Confirm A, B, C |
| 8. Report and hand off | Hand-off A, B, C |

## Chosen directions

Bryan, 2026-11-18: "brainstorm pane = A / confirm decisions = A / Hand off = A / Brainstorm band - step 4 = B /
Intake-brownfield session = B".

| Screen | Chosen | Board | Next prompt |
|---|---|---|---|
| Brainstorm pane | A, step rail | `Main` | P6 |
| Confirm decisions | A, table over question | `Confirm-A-Table` | P7 |
| Hand-off | A, receipt | `Handoff-A-Receipt` | P8 |
| Band and status line | B, meters | `Band-B-Meters` | P9 |
| Intake | B, conclusion first | `Intake-B-ConclusionFirst` | P10 |

The other ten boards stay here as the record of what was not chosen.

## What is here

- `canvas/`: the canvas's own files as downloaded, unchanged: `canvas.json` (the index) and one `.dc.html` per
  board. A board loads `./support.js` from the Design canvas, so it renders only there; open the link above to see
  it drawn.
- `text/`: each board as plain text, one file per board, made from the board's rows (colour is lost). Read these
  in the repository.

## Checked against the prompts' must-haves

Checked by script on 2026-11-18: each board's rows counted and measured in monospace cells, and its text searched.

| Must-have | Result |
|---|---|
| Size: pane 58 by 40, confirm 100 by 36, hand-off 100 by 30, intake 100 by 32, band 120 wide | Met by all 15 boards (hand-off C is 99 wide) |
| Text, box-drawing and block characters only; monospace | Met by all 15; no image or drawing element |
| Band is two rows; status entry `brainstorm 4/8 · evaluate`; readable at 80 columns without a third row | Met by all 3, each drawn at 120 and at 80 columns |
| Pane: current, done and not-started steps told apart | Met. A names all eight steps; B and C abbreviate the list |
| "Proposed" never looks like "decided" | Met: dashed amber for open or proposed, solid blue for confirmed, with a legend |
| Confirm: proposals and reasons visible with the question; the recommended answer marked; "Leave them open" present | Met by all 3. They show "Question 1 of 3", the order of [../README.md](../README.md) §4, C-10 |
| Hand-off: the next step last and most prominent, one key, the command as `/devforgeai:prd BRN-001` | Met by all 3: `[ enter  Run /devforgeai:prd BRN-001 ]` is the last row; never a path |
| Intake: what was read and the conclusion both visible, the conclusion easy to correct; no ideas yet | Met by all 3 |
| Actions drawn as `[ label ]` | Met by all 15 |
| Style: the default design system; "must look like the same product" as DevForgeAI's progress pane and band | **Not met.** The canvas has no design system (`"designSystems": []`), so the colours and the font are Claude Design's own proposal and nothing ties them to the progress pane |

## Differences from the specs

- **States not drawn.** Each board is its key screen only. P6 to P10 ask for the rest in the chosen directions.
- **Why brownfield.** The intake boards give "because the project holds PRD-001" as the reason. In the specs the
  user's words decide the kind and a PRD in the project only suggests it ([../README.md](../README.md) §4, C-01).
  P10 corrects the wording.
- **Project kind's spelling.** Intake B draws `PROJECT KIND: BROWNFIELD`. That is display only; the line a BRN
  holds is `Project kind: brownfield`.
- **Pane buttons.** `[ Problems ] [ Ideas ] [ Assumptions ]` are tabs the prompt did not ask for. P6 asks Claude
  Design to drop or justify them.

## Left to Bryan

- The look: accept Claude Design's palette and font, or attach a design system to the canvas and regenerate the
  five chosen boards.
- Running P6 to P10 for the remaining states.
- Whether a brainstorm pane is built at all (`docs/backlog.md`, DEF-012). A build needs its own spec.
