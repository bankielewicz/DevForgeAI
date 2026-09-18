# Authoring report

Record actual destination and identity, operation, source action (created, edited or unchanged), current authorization, prior origin and preserved legacy references. List actual changed and retained paths with before/candidate/delivered manifests and applied delta.

State AUTHORED, PARTIAL or BLOCKED with concrete unresolved authoring issues. Link authoring-record.json, successful publication readback and authoring-baseline.json when published. Validation: NOT_PERFORMED. Testing: NOT_PERFORMED. Reference separate external results only if they match these exact bytes, without rewriting earlier authoring records.

For design-enabled runs link the actual design source path/digest, design-capture.json and its origin binding, plus original requirement sources and open questions. Report outstanding helper/native evaluation obligations and distinguish authored design from observed behavior. Unchanged source, AUTHORED and handoff delivery do not imply evaluated-build completion.

Return validation-request.json and validator-request.md. Name the next owner (skill-validator for separately selected independent evaluation, or the decision owner for blocked work) and concrete next action. No automatic validation, installation or repair follows. Report publication/readback failures and partial operations honestly.
