# Sources and maintenance

Retrieved/inspected 2026-09-07. Framework files and package derivations are bound in [derivation.json](derivation.json). These external references support design choices; they are not evidence that this package has passed evaluation.

| Source | Claims used here | Applicability / refresh |
| --- | --- | --- |
| [OpenAI skill documentation](https://learn.chatgpt.com/docs/build-skills) | Focused instructions, name/description discovery, supporting resources and provider behavior | Codex; recheck when installed client or discovery format changes |
| [OpenAI hook documentation](https://learn.chatgpt.com/docs/hooks) | Event support, command-hook decisions, trust and error/timeout limits | Conditional hook proposals only; inspect exact client and live docs before implementation |
| [OpenAI prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering#message-formatting-with-markdown-and-xml) | Clear structure and separation of instructions from input data | Prompt review criteria; no fixed model override or API call implied |
| [OpenAI evaluation practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices#llm-as-a-judge-and-model-graders) | Task-specific evaluations; model-grader bias and calibration limits | Record actual reviewer model/context; prefer bounded criterion judgments over uncalibrated scores |
| [Agent Skills specification](https://agentskills.io/specification) | Portable SKILL.md package shape and metadata constraints | Framework authoring-contract reference; provider-specific behavior still requires provider evidence |

Framework references describe a local Linux/WSL POC and draft contracts. The generic utility design does not complete the application-skill roadmap. The two local helpers inspect declared structure/evidence; they do not independently establish AI truth, native execution or external acceptance.

Refresh sequence: select source revision with the assignment owner; preserve old bytes/evidence; update affected package derivations; regenerate only authorized installed copies; hand changed identities to devforge-evaluate-expert for affected checks. A web document update alone does not replace an already selected contract.

## Worktree environment enhancement — 2026-09-07

[Official Git worktree documentation](https://git-scm.com/docs/git-worktree) supplies the local worktree add/list interface and detached/shared-metadata semantics used in [worktree environment setup](worktree-environment.md). The user's selected alternative-environment requirement and the existing packaged execution contract supply the setup scope, independent-attempt and evidence requirements. This addition does not refresh the previously selected shared contract revisions or assert active hook enforcement.

## Workspace allocation refinement — 2026-09-07

The current user authorizes a new usability enhancement: freeze a bounded workspace allocation before preparation, and require the complete experiment only before measured native execution. Model, authentication, repetitions and test budgets may remain pending during preparation. This supersedes the former plan-before-provisioning dependency, not the former evaluation's findings or evidence. Git interfaces and selected packaged contracts are unchanged. Provenance and the exact pre-enhancement bytes are retained outside the runtime package and referenced in derivation.json. Runtime integration remains separate under protected ownership.

## Bounded runtime alignment selection

The later user-authorized alignment explicitly selects the exact preserved revision-3 authoring/execution and shared-handoff inputs already used by builder, plus the separately reviewed DevForge utility mechanical interface. derivation.json records the active sources, former records as historical, transformations and refresh conditions. This selection supersedes earlier statements that shared-contract refresh was deferred; earlier observations and evaluations are unchanged. Native implementation, effective callbacks and model behavior require their own evidence.
