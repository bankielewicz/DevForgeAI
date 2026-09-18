# Documentation review and retained observations

Recorded 2026-09-15. Scope: the 13 framework Markdown documents, retained enhancement notes, and structural configuration reference. This is a factual and cross-document review, not product QA, native runtime qualification, or protected acceptance.

## Independent review

An independent read-only reviewer examined the capability drafts and subsequently the completed index, roadmap, Pro constraints and notes. Two concrete findings were corrected:

1. Delivery readiness originally required prerequisites to be accounted for, which could include a documented failure. [Quality and delivery](../../../specs/framework/quality-and-delivery.md) now requires satisfaction of prerequisites with no unmet mandatory obligations.
2. The project-policy scenario initially made every source/business-rule disagreement require another resolution. [Project context](../../../specs/framework/project-context-and-policy.md) now distinguishes an authorized defect repair against an established requirement from genuinely conflicting governing requirements or authority.

The final independent review found no remaining concrete contradiction in the planning baseline. It did not claim complete runtime specifications or prove all possible inconsistencies absent.

## Connected walkthrough actually reviewed

The fictional OrderDesk scenario was traced through the documents, not executed as software:

| Step | Documents reviewed | Observation |
| --- | --- | --- |
| Select rule and policy | DFF-02/04 | Before/after-dispatch boundary is shared; genuinely unresolved race semantics block only the affected readiness claim |
| Select bounded work | DFF-03 | Cancellation is a coherent outcome; platform and TDD phases do not multiply story files; the race remains an acceptance obligation |
| Produce candidate and assess | DFF-02/08 | Candidate/evidence identity and independent requirement-derived QA are distinct from completion prose |
| Repair and retest | DFF-04/08 | An established requirement supports authorized repair; new evidence does not erase earlier failures or permit self-closure |
| Realign expertise | DFF-05/09 | Stale guidance produces scoped impact/revision and later validation; changed hashes alone do not prove a semantic defect |
| Resume and protect | DFF-07/10/12 | Selected obligations survive session end; advisory work remains possible while unqualified protection stays unavailable |

The primary author additionally aligned the eight-group authority illustration across notes and work items, made zero-denominator health observations explicit, and separated a proposed nonempty-name convention from documented native field requirements.

## Codex and individual Pro feasibility review

[Foundation](../../../specs/framework/foundation.md) owns the base constraint; runtime, installation, agent configuration, index and roadmap reference it. No base dependency assumes extra API billing, Enterprise controls, undocumented host functions, extracted credentials, unlimited usage, or a permanently running LLM worker. Optional other-host/GitHub integrations cannot become hidden core prerequisites.

Official [authentication](https://learn.chatgpt.com/docs/auth), [usage](https://learn.chatgpt.com/docs/pricing), [custom-agent](https://learn.chatgpt.com/docs/agent-configuration/subagents), and [configuration](https://learn.chatgpt.com/docs/config-file/config-reference) documentation informed the bounded claims. The actual account's complete entitlements were not inspected. CLI 0.154.0 was observed earlier in this conversation; no custom-agent or hook activation trial was run.

The live [configuration schema](https://learn.chatgpt.com/docs/config-schema.json) was downloaded read-only with explicit host approval after a sandboxed extraction did not yield usable JSON. An extraction correction retained property names such as description while removing prose annotations. The delivered reference records 98 root properties and 171 definitions. It is structural source evidence, not a schema pinned to the installed CLI or a demonstration that every key works in a subagent layer. The initial MCP schema URL retrieval returned 404 because that endpoint was treated as Markdown; it was not counted as successful schema retrieval. No credentials or model API calls were used for document retrieval.

## Verification limits

The [checker](verify_documents.py) reports link/anchor validity, required document inventory/metadata, native schema-field retention and hashes of 13 explicitly selected pre-existing inputs. It does not inspect the entire workspace or prove all unselected bytes unchanged. Authored mutations were limited to these new documentation/reference/evidence paths. Earlier product sources, operational skills and QA evidence were not edited by this task.

Automated documentation checks were rerun after actual document edits; successful earlier passes found 14 Markdown documents and 156 local links. The [latest report](verification.md) and [JSON observations](verification.json) include the final check with evidence-document links. [Document identities](document-manifest.json) bind the delivered Markdown/reference bytes; this evidence is not authority.

No Rust build, product test, runtime coverage, deployment, installation, startup/systemd change, remote synchronization, GitHub mutation or framework acceptance occurred. Required future ambiguities remain in [the register](../../../specs/framework/roadmap-and-decisions.md#ambiguity-register), with affected claims and resolution evidence named.
