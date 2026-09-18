# Record assembly corrections

The first legacy record check rejected the nested raw readback manifest's source-relative file rows as if they were run-relative evidence references. The raw readback was moved unchanged from the record capsule top level to `inputs/evidence/final-source-readback.stdout.json`; the supported `source-after-manifest.json` stays at the top level. No source data or native receipt changed.

The first adaptive record check accepted `adaptive-observations.json` but rejected the custom authored-custody supplement as an unknown new record family. That custom JSON was moved unchanged into supplemental `inputs/` for separate manual field/reference review. It is not claimed to have adaptive-helper schema coverage.

Both first-attempt stdout, stderr and command receipts remain retained. The second integrity run uses the same installed helper bytes. These packaging errors are evaluator record assembly limitations, not confirmed story-create defects. The earlier supplemental assembly error and its script remain separately retained.
