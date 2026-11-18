# Brainstorm screens: mock-ups from Claude Design

**Status:** directions chosen by Bryan on 2026-11-18 (table below); the style must-have is not met, so the look
is not settled (see the check table). Downloaded 2026-11-18 by claude-code (session
fa59a935-ed2e-4502-b6c4-93bb6d847546) from the canvas "DevForgeAI Brainstorm pane",
<https://claude.ai/artifact/UnLaAUN58JATe7Ed4b9Pt4> (version 1795037172-1e31), which Bryan made from the five
prompts of [../design-prompts.md](../design-prompts.md). Each prompt gave three directions of its key screen.
No mod is specified or built: these files record the options and the directions Bryan chose.

The prompts were the first version of that file; the review of 2026-11-18 later corrected some of their sample
data to the specs' exact shapes (P2, P3 and P5), so a board's sample text can differ from today's prompt.

## Workflow steps these screens show

| Step (SKILL.md's line) | Screens |
|---|---|
| 1. Intake: topic, existing BRNs, clarifying questions | Intake A, B, C |
| 2 to 4, 6, 7 | Pane A, B, C; Band A, B, C |
| 5. Propose dispositions and ask the user to confirm | Confirm A, B, C |
| 8. Report and hand off | Hand-off A, B, C |

## What is here

- `canvas/`: the canvas's own files as downloaded, unchanged: `canvas.json` (the index) and one `.dc.html` per
  board. A board loads `./support.js` from the Design canvas, so it renders only there; open the link above to see
  it drawn.
- `text/`: each board as plain text, one file per board, made from the board's rows (colour is lost). Read these
  in the repository.

| Prompt | Screen | Direction A | Direction B | Direction C |
|---|---|---|---|---|
| P1 | Brainstorm pane, step 4 | `Main` (step rail) | `B-ScoreBoard` | `C-DecisionLedger` |
| P2 | Confirm decisions, question 1 | `Confirm-A-Table` | `Confirm-B-Split` | `Confirm-C-Lanes` |
| P3 | Hand-off, converged and validated | `Handoff-A-Receipt` | `Handoff-B-Ledgers` | `Handoff-C-NextFirst` |
| P4 | Band and status line, step 4 | `Band-A-Strip` | `Band-B-Meters` | `Band-C-Turn` |
| P5 | Intake, brownfield session | `Intake-A-ReadThenConcluded` | `Intake-B-ConclusionFirst` | `Intake-C-EvidenceTrail` |

## Chosen directions

Bryan, 2026-11-18: "brainstorm pane = A / confirm decisions = A / Hand off = A / Brainstorm band - step 4 = B /
Intake-brownfield session = B".

| Screen | Chosen | Board |
|---|---|---|
| Brainstorm pane | A, step rail | `Main` |
| Confirm decisions | A, table over question | `Confirm-A-Table` |
| Hand-off | A, receipt | `Handoff-A-Receipt` |
| Band and status line | B, meters | `Band-B-Meters` |
| Intake | B, conclusion first | `Intake-B-ConclusionFirst` |

The other ten boards stay here as the record of what was not chosen.

## Checked against the prompts' must-haves

Checked by script on 2026-11-18 (each board's rows counted and measured in monospace cells):

| Must-have | Result |
|---|---|
| Size: pane 58 by 40, confirm 100 by 36, hand-off 100 by 30, intake 100 by 32, band 120 wide | All 15 boards fit exactly (hand-off C is 99 wide) |
| Text, box-drawing and block characters only; monospace | Yes, all 15; no image or drawing element |
| Band is two rows; status entry `brainstorm 4/8 · evaluate`; readable at 80 columns without a third row | Yes, all 3, each drawn at 120 and at 80 columns |
| Pane: current, done and not-started steps told apart | Yes. A names all eight steps; B names the current, done and next ones and shows 6 to 8 as numbers; C names only the current step |
| "Proposed" never looks like "decided" | Yes: dashed amber for open or proposed, solid blue for confirmed, with a legend, in the pane, confirm and intake boards |
| Confirm: proposals and reasons visible with the question; recommended answer marked; "Leave them open" present | Yes, all 3. They show "Question 1 of 3", the order of README §4, C-10 |
| Hand-off: the next step last and most prominent, one key, the command as `/devforgeai:prd BRN-001` | Yes, all 3: `[ enter  Run /devforgeai:prd BRN-001 ]` is the last row; never a path |
| Intake: what was read and the conclusion both visible, the conclusion easy to correct; no ideas yet | Yes, all 3: `[ k Change to greenfield ]`, the parked idea offered, the rejected one not re-proposed |
| Actions drawn as `[ label ]` | Yes, all 15 |
| Style: the default design system, and "must look like the same product" as DevForgeAI's progress pane and band | **Not met.** The canvas has no design system (`"designSystems": []`), so the colours and the font are Claude Design's own proposal and nothing ties them to the progress pane |

## Differences from the specs to settle before a build

- **States not drawn.** Each board is the key screen only. The prompts' other states (nothing captured yet; the
  validator failing; nothing confirmed; the brownfield variants of the pane, confirm and hand-off; the kind that
  can't be decided; a skipped document) are the next thing to ask Claude Design for, in the chosen directions.
- **Why brownfield.** The intake boards say "because the project holds PRD-001" as the reason. In
  [../intake-and-evidence.md](../intake-and-evidence.md) a PRD in the project is the recommended answer and the
  default assumption, and the user's words decide. The wording should follow that document.
- **Project kind's spelling.** Intake B draws `PROJECT KIND: BROWNFIELD`. That is display only; the line a BRN
  holds is `Project kind: brownfield` (README §4, C-01).
- **No design system.** The canvas has none installed; the colours and the font are Claude Design's proposal.
- **Pane buttons.** `[ Problems ] [ Ideas ] [ Assumptions ]` are tabs the prompt did not ask for; whether a pane
  has them is part of the decision to build one.

## Left to Bryan

- The look: accept Claude Design's palette and font, or attach a design system to the canvas and regenerate the
  five chosen boards.
- Whether a brainstorm pane is built at all (`docs/backlog.md`, DEF-012). A build needs its own spec.
