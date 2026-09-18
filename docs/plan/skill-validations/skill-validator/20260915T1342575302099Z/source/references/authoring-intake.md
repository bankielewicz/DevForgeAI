# Authoring request intake and test ownership

Accept a user-selected validation-request-v1 packet without requiring another builder specification. Inspect scripts/authoring_intake.py and run:

```text
python -B -X utf8 <validator>/scripts/authoring_intake.py --request <packet> --request-sha256 <selected-digest>
```

The helper independently reads current target bytes and verifies target manifest, package digest, authoring record, identity, changed paths and applicable input references. It emits observations only, never invokes builder or mutates the target. A stale target, altered reference, uncompleted authoring or mismatched identity rejects the packet. Retain exact stdout/stderr and the raw packet plus implementation before assessment. A packet does not authorize side effects; use current user permission and disposable test roots.

Use the captured authoring contract as an existing source of requirements, with any supplied specification refs. Distinguish observed, adopted, legacy generated and authored history. An observed first edit is not adoption. An authoring baseline is custody, not a previous tested build. Preserve legacy COMPLETE meaning. Standalone validation remains available without a packet.

Select applicable format, instructions, workflow and behavior rules independently. Create cases and expected outputs from the actual user contract before running them. Execute structural checks, relevant helper tests, positive/negative behaviors and proportionate cold trials when authorized. Retain failures/retries and exact snapshots. Use the legacy evaluation interfaces only for legacy schema-1/schema-2 evidence; do not demand old COMPLETE outputs from authoring-v1. Results belong to a separate exact-package assessment record and never rewrite an authoring record.

Report structural results, deterministic tests, routing classification, native activation, independent workflow execution and self-review separately. Explicit source loading is not native implicit activation. A development validator's self-review is not independent evidence. Revalidation is a new user-selected invocation; no automatic builder call or repair loop.
