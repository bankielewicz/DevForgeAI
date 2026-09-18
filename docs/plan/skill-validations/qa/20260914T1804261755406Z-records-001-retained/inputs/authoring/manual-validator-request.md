# Manual QA skill validation request

Open `C:\Projects\DevForgeAI` in Codex on Windows. The current host catalog exposes `skill-validator`; this request does not invoke it. Paste the following into the Codex conversation for a separate task:

```text
$skill-validator

Validate and test the development skill C:\Projects\DevForgeAI\src\agents\skills\qa against C:\Projects\DevForgeAI\docs\specs\qa-skill-spec.md (SHA-256 6378025552bbbc4bfdaff8f1d3d14443cfacf44986f51f98845797b116b53e03).

Use C:\Projects\DevForgeAI\docs\plan\skill-authorings\qa\20260914T1748018341005Z\validation-request.json (SHA-256 86c446405103010123b2bf5a0278f6986aaf8e70dab82304d8cc577c18f34bc4). Expected package digest: 2ba0d049f58360a0360031789bce5c9045153540e200d363c8caa4f5c7be2db7. Read current project instructions, independently verify all packet/package/input and authoring-publication bindings, and reject stale identities before assessment.

Assess QA-001 through QA-026 and all QV-01 through QV-21 scenarios. In a fresh disjoint validator-owned evidence run, create and execute the mandatory Python JSONL runner, deterministic graders, bounded cases/fixtures, expected results, schema, runtime/dependency declaration and manifests binding the bundle and exact package bytes. Use independent behavioral oracles for interpretation, integrity findings, exact thresholds, literal output paths, report/fix fidelity and user-facing handoff routing. Report unavailable capabilities and unperformed required cases honestly. If the validator contract cannot produce a required resource, retain and report the precise gap; do not substitute builder execution.

Preserve the selected package, governing specification and all prior authoring/evaluation evidence. Do not repair, install, modify operational copies, create a plugin, run QA against the current application, invoke dev, deploy, or implement framework authority. Keep trial effects in authorized disposable locations and retain failed attempts. Obtain any separately required permission before effects beyond current authorization. Return exact bound results, confirmed findings and unresolved gaps, plus a manual revision handoff if needed. Python evidence is not compiled-Rust framework acceptance.
```

Current delivery status: authoring AUTHORED; publication PUBLISHED; Validation NOT_PERFORMED; Testing NOT_PERFORMED; framework acceptance NOT_EVALUATED. The mandatory evaluated-build bundle is pending the separate task.
