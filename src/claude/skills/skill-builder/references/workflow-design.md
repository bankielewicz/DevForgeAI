# Design observable workflows before staging

Use this reference for create, edit, import and specification builds, including each explicitly selected authored adaptive member. Custody-only adoption, proposals and update reviews need no design unless they also perform selected authoring. Do not expand a set to fill gaps.

Fill [authoring-design-template.json](../assets/authoring-design-template.json) in the selected disjoint authoring input area. Its empty strings are fields to fill, not a valid staged design. Keep the completed design external to the generated runtime package. Bind it in the existing contract's `inputs`, alongside original requirement sources, before running `authoring.py begin --contract <file> --run-root <new-run> --design <file>`. Relative CLI arguments resolve from the command working directory; use absolute source references and quote native-shell arguments as data.

## Behaviors and decisions

For every selected behavior record the trigger, required inputs, source requirement IDs or source-qualified locators, observable completion, outputs and destination-selection rules, prerequisites, authorized effects, failure and recovery, and responsible package resources. A goal such as “perform QA” is not an observable completion. Derive expectations from original requirements or identify an explicit design decision; do not copy current implementation output as the oracle.

Missing decisions that change required behavior block dependent authoring. Record the exact question, affected behavior IDs and decision owner in `open_questions`; continue only independent authorized work. An open question preserves a gap, not permission to invent a product fact or present the dependent design as complete.

Preserve the selected task's execution semantics: planning, execution and handoff are distinct only when meaningful to that task. Complete authorized workflows through required outputs without inventing an approval boundary. Preserve actual execution limits, permissions and ownership. Do not impose QA modes, phase names, thresholds or stop classifications on other skills.

## Resource consumers and helpers

Each resource needs a purpose and `load_when` consumer condition. Keep shared constraints and routing in SKILL.md; put substantial branch-specific detail in the resource for that branch. Require all resources on every invocation only when all are necessary. Explain a requirement in one authoritative location. A simple skill can have one behavior, one instruction resource and empty optional arrays.

Consider a helper for repeated deterministic transformations or file operations. Declare inputs, outputs, runtime/dependencies, permitted effects and write scope, error/exit behavior, caller/loading condition and concrete reuse benefit. Helpers that merely announce success, write a decorative status or wrap a trivial one-off operation have no such benefit. Author selected helpers without executing them; testing belongs in the manual validator obligations.

## Delivery, interruption and adverse conditions

For file-producing behavior define literal destination resolution, when each output becomes available, required content and readback, write-failure reporting and what remains incomplete. An announced path, template or intention is not delivery. Preserve meaningful intermediate outputs at their natural completion boundaries when permitted. Do not manufacture checkpoints for a simple task or silently change a destination to evade host write restrictions.

For interruption or retry, identify resumable state, process/resource ownership, uncertain effects and the conditions that permit retry. A killed process may not have cleaned up; distinguish parent-owned recovery from skill-owned cleanup. Classify supplied timeouts in `execution_limits` as `specified_requirement` or `execution_ceiling`, with provenance. Ceiling exhaustion means incomplete evidence; do not invent timing measurements or turn a validator's default ceiling into a universal product requirement.

Record relevant adverse conditions and requirement-derived expected observations. Consider missing/contradictory inputs, unavailable dependencies/platforms, stale evidence, partial work, announced-but-unwritten outputs, incomplete failure reports, uncertain side effects on retry and helper success mistaken for workflow completion. Include only conditions applicable to selected requirements. These are non-executable design descriptions; do not generate fixtures, graders or executable campaigns, score the candidate or claim testing. The validator must independently construct its fixtures and oracles.

## Input integrity and custody

The [design schema](../schemas/authoring-design.schema.json) defines `authoring-design-v1`. All object fields are closed. Required strings and string-array members are nonempty. Behaviors have unique IDs and at least one requirement locator; resource paths are unique valid package-relative paths. Adverse-condition IDs and open-question IDs are unique within their respective arrays. References to behavior IDs and resource paths resolve within the design. Only helpers have a nonnull helper contract.

`source_refs` uses existing `{path, sha256}` raw-byte references to selected contract inputs other than this design. The `--design` file must resolve to exactly one contract input, with the same digest. Duplicate keys, nonfinite numbers, unknown fields, invalid paths, links/junctions and disallowed input/target/run overlaps are rejected. The input capture remains bounded to 2,000 files and 32 MiB, including the contract for design-enabled runs. Shape and reference checks establish input integrity, not the quality of a generated workflow or correctness of an oracle.

The normal `inputs/<index>` snapshot is the only captured design copy. `design-capture.json` binds its original source and snapshot references, run ID and target name with version `authoring-design-capture-v1`. Internal `origin.json` binds that capture record through `design_capture_ref`. Capture/readback completes before STAGED. Existing authoring contract and validator packet field sets do not change.

Publication rechecks original design, snapshot, capture record and origin/contract bindings. Missing or changed evidence blocks dependent publication; a design input cannot silently become a legacy stage by removing its capture binding. Preserve capture failures and actual applied deltas. A substantive design revision needs a fresh linked run; never edit captured inputs to fit later output. Existing no-design CLI stages remain supported for legacy input contracts. These custody checks do not execute or assess the authored skill.

Return the design path/digest, original requirement references, open questions and unperformed helper/native obligations using [validation-handoff.md](validation-handoff.md). An absent validator does not block authoring. No handoff grants evaluation, installation, external-effect or repair authorization.
