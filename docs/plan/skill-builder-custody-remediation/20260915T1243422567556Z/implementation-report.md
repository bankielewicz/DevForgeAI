# Skill-builder custody repair

## Implemented behavior

The selected development skill now binds its original stage mode and origin bytes before publication can choose the legacy path. A changed design flag, missing binding, removed capture, or inconsistent integrity receipt cannot silently turn a design-enabled run into a successful legacy publication.

`scripts/authoring.py` adds `recheck_stage` and a closed `stage-integrity.json` receipt containing schema version, run ID, target name, origin path/SHA-256 and original boolean design selection. `begin` writes and reads back this receipt before returning STAGED. Existing design checks invoke the stage check at each publication boundary, and each changed path is checked after the competing-writer callback and before destination creation or writing.

Preflight stage failures produce retained BLOCKED evidence and instruct the caller to start a fresh linked run. Failed attempts cannot be reused merely by restoring the receipt. Mid-publication drift retains actual applied paths as PARTIAL, with successful baseline publication prevented. Delaying destination creation until after the first per-path check prevents a BLOCKED first-path attempt from leaving an empty occupied skill destination.

## Compatibility and scope

Fresh no-design calls carry false-mode receipts and continue to support design-shaped JSON as ordinary input. Canonical historical stages without a mode marker or design evidence retain prior legacy handling. Pre-revision staged records with a mode marker but no receipt require a fresh linked run; no receipt is backfilled and no historical baseline is rewritten.

Updated development files:

- scripts/authoring.py
- references/authoring.md
- references/evidence-format.md
- references/regeneration.md
- package-manifest.json

SKILL.md, existing closed contract/validator packet schemas, legacy baseline readers, operational copies, validator source, installation, hooks, CI and Rust implementation are outside these edits. Python receipts remain editable consistency evidence; they do not provide protection against coherent rewriting of all artifacts or issue framework acceptance.

## Red, green and independent review

- `red-001`: original downgrade reproduced; new receipt and interruption requirements failed against the original source. The 29-case run had 20 assertion failures and two unhandled malformed/missing-origin errors. These errors were product failure-path observations; the reproduced downgrade assertion is the valid red for the original bug.
- `green-001`: initial receipt implementation passed 29 cases.
- `red-reuse-001.txt`: restoring a receipt allowed a rejected stage to be reused; `green-002` passed all 30 cases after recording failed attempts as non-reusable.
- `regression/qa-02`: independent regression exposed missing fresh-run guidance; the second source revision corrected that response.
- `regression/red-prewrite`: independent review demonstrated an empty destination after first-path drift. `green-prewrite-001.txt` passed after delaying directory creation.
- `repair-review.md`: independent comparison of the final source and selected repair contract found no additional substantiated production defect. Two legacy fault injectors were identified as relying on the previous eager directory creation; their fixture setup was corrected with assertions preserved and failed attempts retained.

The final structure keeps the new consistency rule in one function and reuses the existing design/publication boundaries. No additional refactoring was needed. Final source-bound regression, platform, native-workflow and generated-skill results are separate artifacts; earlier-source passes do not qualify the final bytes.

## Evidence boundaries

All attempts live in this new run. Earlier review, repair proposal, test source and operational files were preserved. Before/delivered snapshots, changed-file hashes, textual diff, final static checks, per-case JSONL, expected results, deterministic grading, runtime/dependency information and artifact manifests bind the work for review. These are maintenance and evaluation evidence, not protected framework acceptance.
