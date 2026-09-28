---
type: llm
---

PASS if the final reply names the PRD workflow (the DevForgeAI Codex PRD skill) as the next step,
says that workflow is not built yet, and gives the brainstorm at
docs/specs/brainstorm/BRN-001.md as its input.
FAIL if it claims the PRD skill is available to run now, passes a file path as the
command's argument, or starts drafting PRD content (requirements, success metrics).

The last paragraph must start with "Next step", be outside a code block, name the
BRN ID as the future workflow input, and have nothing after it. The initial report block
comes before any discussion. Do not suggest a Claude slash command.
