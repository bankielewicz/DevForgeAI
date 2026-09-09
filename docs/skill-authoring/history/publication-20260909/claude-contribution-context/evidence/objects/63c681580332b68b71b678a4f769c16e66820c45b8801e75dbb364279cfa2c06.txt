---
name: devforge-review
description: Review a DevForge candidate or generated project expert skill against its upstream intent and evidence, distinguishing structural checks from semantic acceptance.
---

Obtain the candidate, accepted upstream decisions, expert specification when applicable, and evidence paths. Inspect the raw artifacts rather than relying on the author's summary. If the requested review requires fresh context, establish a new independent session before reading the candidate; this skill does not automatically create one.

Run the appropriate read-only `devforge check`, `expert status`, or `verify` command with the owner's external policy and state. These checks establish structural facts. Independently assess whether requirements were interpreted correctly, tests discriminate expected behavior, source responsibilities fit the architecture, and the skill's instructions are useful and appropriately scoped.

Report each finding with concrete file/evidence references and impact. Route candidate defects to the candidate; route policy contradictions to their owner. Do not repair or reinterpret the governing gate as part of a candidate review.

State which checks ran, which could not run, which claims remain unverified, and whether the evidence supports the requested acceptance. An author's provenance hash or a CURRENT skill binding alone is insufficient behavioral evidence.
