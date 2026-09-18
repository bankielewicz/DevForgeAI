# Bounded native CLI qualification

## Conclusion

**Native qualification remains INCOMPLETE, with one observed user-facing delivery failure.** No complete required scenario passes: **0/4 (0%)**. This is independent of deterministic helper coverage and is not framework acceptance.

One Linux simple scenario genuinely authored and published its package, with verified custody and manual validator artifacts. Its final response points to the wrong destination and omits the handoff/status, so successful artifact publication is separated from failed user-facing delivery. Three scenarios exhausted their 120-second execution ceilings. Timeouts do not establish a product performance defect.

| Required case | Selected snapshot | Native result | Artifact publication | Full workflow result |
| --- | --- | --- | --- | --- |
| Windows simple, explicit source | V1 | Timed out at 120.547s; Codex exit 1 | No destination | INCOMPLETE; final V3 equivalent NOT_RUN |
| Windows branching, implicit discovery | V3 | Timed out at 120.469s; Codex exit 1 | No destination | INCOMPLETE |
| Linux simple, explicit source | V3 | Completed at 106.859s; Codex exit 0 | PASS, independent digest readback | FAIL: actual final link/handoff delivery |
| Linux branching, implicit discovery | V3 | Timed out at 120.040s; Codex exit -9 | No destination | INCOMPLETE |

Windows full-scenario passes: 0/2. Linux full-scenario passes: 0/2. Failed, timed-out and final-byte-unexecuted cases are not passes. The initial Windows initialization failure and Linux setup/aborted approval are retained setup history, not extra required cases and not successful retries.

## Exact-byte binding

Each case contains `source-manifest.json`, prompt, plan, before/after inventories, raw `stdout.jsonl`, stderr and `attempt-001.json`. Copied builder inputs remained unchanged in all executed cases.

The three V3 fixtures contain the same 47 path/size/digest entries. Their native manifest JSON byte hashes differ between Windows and Linux because host path sorting orders uppercase names differently; comparison by path establishes exact file equality. SHA-256 over rows sorted explicitly by path, compact UTF-8 JSON with unescaped Unicode, is `6008e045bee0e7007b101ecf8821d74170d834a7e80895c0f3efb4c6d52aa6ff` for all three V3 fixtures. V1 has digest `87c7f53b6e4b1aafcd7379e9ac8f9330545536dea1bad5ae445c468f7250aca6` under that same normalization.

Windows simple's source-checkout-unchanged flag is false because the parent advanced development source from V1 to V2 while the frozen V1 child was running. Its fixture-unchanged flag is true. This observation cannot qualify final V3 bytes, and its timeout was not automatically retried.

## Routing observations

Both simple prompts explicitly identify the copied builder entrypoint. Both completed command traces show that source being read. Explicit loading is not evidence of implicit discovery.

Both branching prompts request skill creation without naming skill-builder or its entrypoint. On Windows and Linux the first completed command reads `.agents/skills/skill-builder/SKILL.md` from the isolated synthetic project. **Implicit selection/source loading was observed in 2/2 branching cases.** Their later timeouts prevent a full workflow pass. These isolated `.agents/skills` copies are test inputs; active operational/personal skill copies were not installed or changed.

## Linux simple artifact readback and final-response failure

The package at `../linux-campaign-001/linux-simple-v3/Project space/result-skill/sort-lines/SKILL.md` contains the requested sorting behavior: numeric Unicode code-point lexicographic order, empty-line removal, duplicate retention and output-only text. Whitespace preservation and LF output are explicitly documented. Candidate execution is NOT_RUN in this native authoring evaluation.

The authored run contains a design capture and stage-integrity receipt, AUTHORED record, baseline, PUBLISHED receipt, `validation-request.json` and `validator-request.md`. An independent retained-copy readback checked **28 digest references**, with zero missing/mismatched references, exact delivered-manifest equality and package digest equality. The generated package digest is `2fce9a14f26b99c8534e27bf48ea6fafc8e5bc1e20d74d623c984b274dddc1f1`. See [linux-simple-artifact-readback.json](linux-simple-artifact-readback.json).

The final response is exactly:

```text
Created [sort-lines/SKILL.md](< /tmp >).
```

That destination link does not name the delivered file, and the final message does not provide the manual handoff, authoring/quality status, outstanding obligations or next action required by the loaded skill. Earlier commentary mentions publication but does not repair the final response. This is an observed model delivery failure. `SKILL.md` already explicitly requires the destination/status/handoff, so this single observation does **not** prove an absent source instruction or justify a speculative source edit.

## Retained evidence

- [Windows simple V1 attempt](windows-simple-002/attempt-001.json), [stdout](windows-simple-002/stdout.jsonl), [plan](windows-simple-002/plan.json).
- [Windows branching V3 attempt](windows-branching-v3/attempt-001.json), [stdout](windows-branching-v3/stdout.jsonl), [plan](windows-branching-v3/plan.json).
- [Linux simple V3 attempt](../linux-campaign-001/linux-simple-v3/attempt-001.json), [stdout](../linux-campaign-001/linux-simple-v3/stdout.jsonl), [final](<../linux-campaign-001/linux-simple-v3/Project space/final.txt>).
- [Linux branching V3 attempt](../linux-campaign-001/linux-branching-v3/attempt-001.json), [stdout](../linux-campaign-001/linux-branching-v3/stdout.jsonl).
- [Environment, setup failures and interrupted approval](preflight-observations.md).

Windows timeout recovery used `taskkill /T /F`; both receipts record exit 0 and descendant termination. Linux timeout recovery used `killpg(SIGKILL)` for the owned child process group and reaped the Codex process at exit -9. These are parent-owned recovery actions, not skill-owned cleanup claims.

The Linux campaign wrapper later failed because an unrelated regression archive source had disappeared. Both native receipts and source/output copies were already retained. Wrapper exit codes do not substitute for native child receipts or artifact review.

The independent readback utility initially assumed `state` instead of `authoring_state` and assumed a manifest array instead of its `files` member. Those evidence-reader errors were corrected against the actual schema; the final readback ran successfully. They did not rerun or alter any native attempt, candidate, source, original locator or captured record.

## Remaining work

Native final-byte Windows simple execution remains unperformed after the V1 timeout; branching end-to-end completion remains unobserved on both platforms; Linux simple final response delivery failed. Future native attempts require their own authorized bounds and fresh evidence. No timeout was retried automatically and no passing full/native/framework acceptance is asserted.
