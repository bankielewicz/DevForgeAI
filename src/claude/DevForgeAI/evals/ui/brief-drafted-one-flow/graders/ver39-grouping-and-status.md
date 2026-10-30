---
type: llm
---

The agent ran in a session with no Artifact tool and was told to proceed without questions. The promoted ideas that name a screen
are IDEA-01, IDEA-02, IDEA-03 and IDEA-06; IDEA-04 names none. Judge the agent's output outside the briefs, and how many briefs it
shows. A pass needs all of these:
- It states the one flow for the whole release, with its key screen and its surface (or surfaces), and says the brief is unconfirmed.
  The request settled the grouping, so the reply may say so; it need not call the grouping unconfirmed.
- It shows one brief for each flow it proposes, each in a code block of its own: a reply that proposes two flows and shows one brief is
  not a pass.
- It says the session has no Artifact tool, and that no canvas was made and nothing was sent to claude.ai (wording such as "no
  screens designed" or "nothing goes to claude.ai without confirmation" counts).
- It names docs/specs/design/DSN-001/boards/, where a copy placed by hand is recorded.
- It contains no drawing of a screen made with characters. The words "box-drawing characters" inside a brief are a constraint on
  the canvas, not a drawing.
Anything else is not a pass.
