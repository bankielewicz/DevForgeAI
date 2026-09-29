---
type: llm
---

Look at the final paragraph of the reply, the one that starts with "Next step".
PASS if it names the story step as next, with EPIC-001 as its input by ID: either telling the user to
run /devforgeai:story with EPIC-001, or saying stories are written by hand from the story template for
now and that the story skill (planned as /devforgeai:story) runs with EPIC-001 once it is built.
FAIL if it passes a file path instead of the ID, names a different next step, if anything follows
that paragraph, or if the reply says it wrote or started writing a story.
