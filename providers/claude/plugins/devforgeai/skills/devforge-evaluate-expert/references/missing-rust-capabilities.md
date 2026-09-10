# Missing DevForge CLI capabilities, and how to evaluate without them

Two capabilities this workflow would otherwise depend on are not implemented in the compiled DevForge CLI. This file states them, explains why they are not supplied here in Python, gives the procedure for proceeding without them, and defines the labels that keep the gap visible in the report.

## The two statements

Record both in every evaluation report, whatever the observations turn out to be.

> **Skill-package structural inspection (S001–S013) and evidence reduction are not implemented in the DevForge CLI.**

> **Protected-manifest custody for the evaluation runner - binding the selected runner and grader files, the Python and dependency selection, the case inputs and the grading criteria outside evaluated-agent write access, and verifying those identities before acceptance criteria are applied - is not implemented in the DevForge CLI.**

Both are **evaluation prerequisites** owned by the DevForge integration owner. Neither is a defect in the candidate. Editing a candidate does not produce either of them, and a missing observation caused by either one never becomes a finding against the skill being evaluated.

## Why they are not supplied here

The Codex implementation of this skill carries two Python helpers that do this work: a package inspector implementing a thirteen-rule catalogue with a package-wide `overall` verdict and `PASS`/`FAIL`/`COULD_NOT_RUN` exit codes, and an evidence reducer that writes a decision receipt carrying `overall` and `coverage_complete` and exits to mean scoped-success, required-failure or unavailable.

Those are a validator gate and an acceptance decision. The framework's language policy assigns both to compiled Rust, and porting them into this package would move framework authority into Python under a new name. So they are not ported, and the gap is reported instead.

The narrowly scoped runner and graders that this package *does* ship are a different thing; [the runner interface](runner-interface.md) sets out the discriminator in detail.

## Verifying the gap yourself

Do not take this file's word for it. The CLI's own help is the evidence:

```text
devforge --help
devforge expert --help
devforge check --help
devforge delivery --help
```

`devforge check` is described as checking structural policy and provenance for a *project* against a policy, and explicitly does not certify semantic behaviour. It is not a skill-package inspector. If a future CLI revision adds either capability, that changes this file and the affected reports - inspect the actual help output for the binary you were given rather than assuming either state.

## Procedure in place of structural inspection

Gather the structural facts by reading. Every row is a manual observation and carries `method: INSPECTION_MANUAL` and `authority: none`.

| Observation | How to obtain it | Notes |
| --- | --- | --- |
| Package inventory and identities | Read the tree; record `{path, sha256}` per file | Record the bound you stopped at if you stopped |
| Frontmatter present | Read `SKILL.md` directly | Opening and closing `---` delimiters |
| `name` and `description` populated | Read the frontmatter block | Additional fields are permitted and their meaning is not judged here |
| `name` versus folder name | Record **both values** | Do not assert equality as a conformance rule; see below |
| Local links resolve | Follow each local Markdown destination | Record which resolved and which did not |
| `evals/` absent from an installed copy | Read the installed tree | Applies to installed mode only |
| JSON, TOML and Python files parse | Read and parse without executing | Never import or run candidate code |
| Semantic conformance | The independent review, criteria R01–R10 | `method: AI_REVIEW`, not a structural row |

**The name-and-folder rule needs care.** Claude sets the slash command from the *directory* name for a personal or project skill, and from the frontmatter `name` for a plugin skill, where the frontmatter `name` sets the command segment. A difference between them is therefore not a provider defect, and reporting one as a failure manufactures a finding. DevForgeAI packages keep the two equal by convention, so a case may legitimately assert equality - but it has to say so, and the report should state which of the two it was.

Where authored cases exist, run them with [the runner](runner-interface.md) and cite its rows as evidence alongside the manual observations. A complete set of matching rows is **not** a substitute for the missing rule catalogue: the dependency statement stays in the report, and the P5 disposition records that the deterministic evidence group was obtained by reading rather than from an implemented gate.

## Procedure in place of evidence reduction

Adjudicate by hand against [the results contract](results-contract.md):

- any applicable `FAIL` gives **revise**;
- otherwise a missing required observation gives **insufficient evidence**;
- every required observation passing supports only **suitable for the stated scope**, which is a recommendation and not an acceptance.

No file named `decision.json` is produced by this package. Record in the results that no implemented decision receipt exists and that the disposition was adjudicated against the contract directly.

## Legacy helpers, if an operator supplies them

The Codex package's `inspect_skill.py` and `assess_evidence.py` still exist. This package does not ship them, does not reference them by path and does not require them. Running an unchanged existing tool is permitted operational use, so if the **operator** supplies one - its absolute path, its own runtime, its own PyYAML - you may run it.

Record the result with all of:

- `source: legacy-codex-helper`, the helper's absolute path and its sha256;
- the exact command and the observed exit status;
- `authority: none - legacy Python, non-authoritative`.

Then keep the boundary. Do not promote a reducer's `overall` into your disposition, do not treat an inspector's exit code as the structural outcome, and do not let either close the missing-capability dependency. Adjudicate from the underlying evidence and cite the helper output as one more input to it.

## What to route where

| Situation | Owner | Recorded as |
| --- | --- | --- |
| Either capability is needed for a claim | DevForge integration owner | Evaluation prerequisite, with the blocked claim named |
| A demonstrated defect in the candidate | `devforge-project-expert-creator` | Finding with severity and a bounded change |
| A defect in a shared contract or a sibling gate | That contract's integration owner | Reported, not edited around |

Reporting is always possible. A blocked observation stops the claim that depends on it; it never stops the report.
