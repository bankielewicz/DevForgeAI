# Brainstorming with an admitted runtime

Read this reference when the protected runtime supplies context for an externally selected brainstorm task. The selected integration interface is implemented with synthetic runtime evidence; native admission, effective hook configuration, installed activation, native turn completion and rendered receipt delivery remain unverified. The default production launcher at this integration baseline refuses native admission. These instructions neither activate hooks nor establish enforcement in the current terminal.

## Use the selected task

The external owner selects a `devforge.brainstorm-session/v1` contract before admission. It binds the task and assignment, immutable input bytes, installed resources, original deadline, mutable-output baselines and archives, checkpoint destination and external receipt destination. Only the protected runtime owns accepted evidence snapshots, phase transitions and mechanical completion. A worker-written completion flag or PASS statement supplies no authority.

Read the actual installed SKILL.md, workflow and applicable templates. Resolve package resources from the loaded skill root and project artifacts from the selected project store. Use the selected artifact identities, revisions, required sections and destinations. Preserve the normal artifact/reference, ownership, attribution and adoption rules in [artifact-workflow.md](artifact-workflow.md). Runtime input hashes do not prove that the model read those inputs.

A ledger being revised is a mutable output with a selected baseline, not an immutable input. The runtime retains its preimage and selected archive before admission; use those actual preserved bytes when binding the previous revision. Do not replace an archive with a hash-only record or silently reuse changed bytes. Current managed outputs remain draft. Neither a runtime callback nor a correction means the user adopted an idea.

An ordinary brainstorm requires Recover → Explore → Record → Focus. Only an externally selected `handoff-only` contract uses Recover → Focus, with Explore and Record explicitly NOT_APPLICABLE. For ownership conflicts or routed tasks, preserve the conflict and required capability gap. Do not change the mode or destination yourself, manufacture a ledger, or continue another owner's writes. Discussion may continue within the existing scope while dependent completion is blocked.

## Write evidence for the current phase

Use the current task identity, phase, challenge, checkpoint destination and JSON shape supplied by the runtime. Never copy an illustrative task ID, path, challenge or fact. Write one strict UTF-8 JSON object, without a Markdown fence, at that exact checkpoint destination. Its complete bytes must be nonempty and no larger than 65,536 bytes, with exactly these six keys:

| Key | Required value |
| --- | --- |
| schema_version | `devforge.brainstorm-checkpoint/v1` |
| task_id | The runtime's current task identity |
| phase | The admitted phase: `Recover`, `Explore`, `Record` or `Focus` |
| challenge | The runtime-supplied challenge for this admission |
| state | `ready` or `awaiting_user` |
| content | Exactly the fields for that state and phase below |

Do the useful work before recording its evidence. After writing the current checkpoint, finish the response for that phase so the synchronous Stop callback can inspect it and supply the next context. Do not submit a later phase under the old admission or infer progress from a successful checkpoint write. The runtime accepts and snapshots evidence or reports a bounded correction; the worker does not invoke phase commands.

For `ready`, use the exact content fields below. Lists of strings may be empty unless otherwise specified; each is limited to 100 entries. Each string must be nonempty, at most 8,192 UTF-8 bytes, and free of unresolved template markers. These are evidence limits, not a request to fill unused entries.

| Phase | Exact content fields | Useful work and runtime boundary |
| --- | --- | --- |
| Recover | `known_ideas`, `known_decisions`, `missing_inputs`: lists of strings; at least one item across them | Recover the supplied steering and relevant selected ledger. Record actual known facts or missing inputs. Runtime binds the evidence to selected context before Explore. |
| Explore | `ideas`: 1–100 objects; `missing_inputs`: list of strings | Explore recognizable people, problem, outcome, alternatives and open questions. Runtime requires this evidence before Record. |
| Record | `ledger_path`: exactly the selected project-relative ledger destination | Save the selected ledger using the installed asset, preserving IDs, origins and attribution. Runtime reads its envelope, selected identity/revision, reference revision types and required populated headings before Focus. |
| Focus | `next_action`, `owner`, `completion_evidence`: strings; `non_goals`: list of strings; `handoff_path`: exactly the selected project-relative handoff destination | Save the shared handoff with a concrete continuation. Runtime checks all selected artifacts and the handoff's selected-ledger binding before accepting Focus as READY. |

Each Explore idea object has exactly `idea_id`, `people`, `problem`, `outcome`, `alternatives` and `open_questions`. Idea IDs are unique within the checkpoint and preserve the ledger's stable identities where applicable. Alternatives and open_questions are lists of strings. Unknown people, problem or outcome may be null, but require a real open question; known values are strings. Do not invent a user, problem, adoption or research result to fill the shape. Retain split/merge origins and AI attribution in the ledger even though the checkpoint is a bounded summary.

Checkpoint path fields use the runtime-selected spelling. Keep runtime absolute locators and project-relative checkpoint content separate from artifact references, which retain the selected `store` and root-relative `path`. Never rewrite a supplied reference or discover another authority root to get through a phase.

## Blocking questions, correction and resume

When a real user answer is required for the current dependent work, ask the question and write `state: awaiting_user`. In this state, `content` has exactly two nonempty string fields: `question` and `blocking_dependency`. Describe the question actually asked and the work it blocks. This shape replaces the ready-phase content; do not add ready fields or claim the phase finished.

The runtime preserves WAITING_USER at the current phase and issues no receipt. UserPromptSubmit resumes that phase with the runtime's current admission context. Read what the user actually answered: a submitted prompt alone neither resolves the dependency nor adopts a proposal. If the dependency remains, record it honestly. Nonblocking unknowns stay in ordinary phase evidence and need not stop useful exploration.

Each phase permits one bounded correction of reported checkpoint/artifact issues. Correct only within the current task and returned admission; a rejected checkpoint does not advance the phase. Exhausted correction, stale/replayed or out-of-order evidence, expired original deadline, changed selected authority or unavailable runtime stops dependent completion. Do not launch retries, reset the deadline, edit protected runtime state, invoke operator advance/resume/complete/check/verify commands, or substitute package receipt/check helpers.

After interruption, preserve the task's current evidence and use the runtime's resumed phase, assignment and input/resource identities. Waiting, correction and resume retain the original allocation. If selected identities differ, report the affected stale evidence and required owner action. An already committed historical receipt remains evidence of its original scope; later drift requires a separate current-applicability result, not rewriting that receipt.

## Handoff and delivery

Finish and read back any ledger before binding its complete-byte digest in the handoff. Calculating truthful artifact metadata is allowed. Keep the installed handoff's input/output, observed-verification and continuation tables. Inspect every repeated reference and claim, including raw evidence versus artifact identity, source section versus row locators, adoption scope and output paths.

The saved handoff records only checks already observed. Its own later readback, hash check, receipt publication and delivery remain NOT_RUN at creation; the receipt destination is planned. Exclude the handoff itself from its input/output table and never insert its own digest. A useful continuation or content-ready statement is separate from completed delivery. Leave this historical snapshot unchanged after later checks.

For an admitted managed session, the qualifying Stop callback after Focus reaches READY performs completion while the owned client may remain alive. The protected runtime:

1. Reads and mechanically checks the final selected artifact bytes against the accepted evidence and contract.
2. Exclusively publishes a separate external receipt without a self-digest.
3. Reads the complete receipt back and verifies its current target bindings.
4. Returns the actual receipt path and full SHA-256 in the synchronous `systemMessage`.

Report only the result actually supplied. A successful socket write (`SOCKET_WRITE_COMPLETED`) is transport evidence; it does not establish rendered delivery, which may remain NOT_OBSERVED. A failed later client process does not erase an already committed task receipt. Native turn completion, process cleanup, receipt rendering, current applicability, semantic quality and human acceptance need their own observations. Mechanical checks do not certify hidden reasoning, user adoption or usefulness, nor every reference/table/prose claim.

If no active runtime was admitted, continue useful discussion and authorized draft artifacts with delivery explicitly unverified. If an admitted runtime fails or is unavailable, preserve its state and cause and stop dependent completion. In either case, do not manufacture a receipt or add a manual helper chain. When only terminal output is authorized, use the shared handoff tables and disclose pending persistence. The external owner handles runtime repair and any new allocation.
