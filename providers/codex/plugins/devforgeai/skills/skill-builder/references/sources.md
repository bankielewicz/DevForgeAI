# Sources and maintenance

Retrieved/inspected 2026-09-07. Framework files and package derivations are bound in [derivation.json](derivation.json). These external references support design choices; they are not evidence that this package has passed evaluation.

The G5 canonical refresh selects the accepted VPR-2 policy and requirement diff at DevForgeAI `8ede26450ae737a5e928c5f70a945aa995969b30`, and G1 shared contracts/template at `75bcba915fd1d5f88477318d4b27db6e6961ca81`. The package-local authoring/execution references retain portable historical guidance and mechanically transcribe G1's VPR-2 sections, replacing source-only links with retained provenance locators. The shared handoff is adapted to builder authoring and its creation-time evidence boundary. Exact source/destination SHA-256 values and previous selections are in derivation.json. The artifact-contract bytes are unchanged. This is a local frozen-source refresh; no external documentation was re-retrieved or runtime capability observed.

| Source | Claims used here | Applicability / refresh |
| --- | --- | --- |
| [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) | Focused instructions, name/description discovery, supporting resources and provider behavior | Codex; recheck when installed client or discovery format changes |
| [OpenAI hook documentation](https://learn.chatgpt.com/docs/hooks) | Event support, command-hook decisions, trust and error/timeout limits | Conditional hook proposals only; inspect exact client and live docs before implementation |
| [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering#message-formatting-with-markdown-and-xml) | Clear structure and separation of instructions from input data | Prompt review criteria; no fixed model override or API call implied |
| [OpenAI evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices#llm-as-a-judge-and-model-graders) | Task-specific evaluations; model-grader bias and calibration limits | Record actual reviewer model/context; prefer bounded criterion judgments over uncalibrated scores |
| [Agent Skills specification](https://agentskills.io/specification) | Portable SKILL.md package shape and metadata constraints | Framework authoring-contract reference; provider-specific behavior still requires provider evidence |

Framework references describe a local Linux/WSL POC, historical draft contracts and the explicitly accepted VPR-2 amendment. The generic utility design does not complete the application-skill roadmap. The paired validator's helpers inspect declared structure/evidence under their selected contract; they do not independently establish AI truth, native execution or external acceptance, and this builder does not execute them.

Refresh sequence: select source revision with the assignment owner; preserve old bytes/evidence; update affected package derivations; regenerate only authorized installed copies; hand changed identities to skill-validator for affected checks. A web document update alone does not replace an already selected contract.
