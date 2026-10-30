---
type: llm
---

The agent ran in a session with no Artifact tool and was told to proceed without questions. The promoted ideas that name a screen
are IDEA-01, IDEA-02, IDEA-03 and IDEA-06; IDEA-04 names none. Judge the agent's output outside the briefs. A pass needs all of
these:
- It proposes how the screens group into flows (one flow for the release, or two such as a terminal flow of IDEA-01 and IDEA-02
  and a web flow of IDEA-03 and IDEA-06), with the key screen and the surface of each flow, and says the grouping is unconfirmed.
- It says the session has no Artifact tool, and that no canvas was made and nothing was sent to claude.ai (wording such as "no
  screens designed" or "nothing goes to claude.ai without confirmation" counts).
- It names docs/specs/design/DSN-001/boards/, where a copy placed by hand is recorded.
- It contains no drawing of a screen made with characters. The words "box-drawing characters" inside a brief are a constraint on
  the canvas, not a drawing.
Anything else is not a pass.
