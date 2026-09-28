# Repository documentation update workflow

## Purpose

After repository work is complete, update or create `README.md`, `CHANGELOG.md`, and relevant documentation to reflect the resulting project state. Use Git diffs and inspected files as evidence. Produce professional, easy-to-navigate documents and concise explanations of meaningful outcomes for users, operators, and contributors.

This is a procedure for an AI coding assistant to follow directly. Run it at the end of an authorized work session or when explicitly asked to refresh documentation. It does not require a particular model, editor, or development framework.

## Inputs and defaults

| Input | Default or resolution rule |
| --- | --- |
| Repository | The local repository identified by the user or active work session. |
| Work scope | The completed task, feature, fix, or explicitly requested revision range. |
| Before state | A supplied comparison point, captured task-start state, or justified branch baseline. |
| Target state | Current working tree, including relevant local additions. Use a committed snapshot when explicitly requested. |
| Audience | Existing documentation's intended readers; otherwise infer the primary users, operators, and contributors from the project's purpose. |
| Template | Existing repository template first; otherwise select a document template and project profile from the catalog below. |
| Edit mode | Apply documentation edits when the current request or existing authorization covers them. Otherwise prepare proposed edits without modifying repository files. |
| Release context | Existing repository convention; otherwise treat the work as unreleased. |

Do not ask the user to repeat information or permission already established. Resolve routine choices from the repository and session context. Ask only when a remaining ambiguity prevents an accurate, properly scoped update.

## 1. Establish the scope

1. Confirm the repository root and read applicable repository instructions, contribution guidance, documentation conventions, and release configuration.
2. Inspect existing documentation and templates. Identify canonical files, missing documentation, generated outputs, project type, and intended readers. Account for README locations outside the repository root and release-note systems that use fragments.
3. Record the current Git status and retain the pre-edit content of documents being changed. Preserve existing content, unrelated work, and staging choices. A dirty working tree is not a reason to stop.
4. Resolve the before state using this priority:
   - User-specified revision or comparison range.
   - Captured task-start state, including pre-existing local edits when available.
   - The feature branch's common ancestor with its known integration branch, when the requested scope is that branch's work.
   - `HEAD` only when the intended scope is the current uncommitted changes.
5. State the selected scope and any material uncertainty briefly. Do not silently substitute the last commit, latest tag, or an assumed `main` branch for an unknown baseline.

If a task began with local changes, a starting commit alone cannot identify which edits belong to the task. Use any captured before snapshot and known task boundaries. Exclude unrelated edits; leave uncertain items unresolved rather than attributing them to the AI.

If the baseline cannot be recovered, inspect current files and complete unambiguous documentation corrections. Request the missing comparison point before inventing historical change claims. In a new repository without commits, document its initial state without manufacturing release history.

## 2. Build an evidence-based change inventory

Inspect the relevant committed changes, staged changes, unstaged changes, and untracked files. Read affected source, configuration, tests, specifications, and existing docs far enough to understand the outcome.

Use an AI's previous summary, a commit message, or a task description to locate evidence. Confirm each substantive claim against the repository. A diff establishes that content changed; it does not establish that tests passed, a feature was deployed, or a performance improvement was measured.

For each meaningful outcome, keep a temporary working note:

```text
Outcome: What changed in the resulting project state?
Audience: Who needs to know?
Evidence: Which diff and current file support the claim?
Action: Does anyone need to change usage, configuration, or deployment?
Destination: Which existing section or necessary new document should explain it?
```

Keep these notes out of public documentation unless the project requires an evidence record. Group related edits into one outcome. Account for reverted or superseded work so intermediate attempts do not become announced features.

Distinguish an authored specification, an implemented capability, a tested behavior, and a released feature. Describe only the status supported by evidence. If implementation conflicts with an accepted requirement, flag the discrepancy; do not rewrite the requirement to make the implementation appear compliant.

## 3. Select what deserves documentation

Include a change when it affects what a reader can do, how they must do it, or what they need to maintain or operate the project.

| Change | Documentation treatment |
| --- | --- |
| New capability or meaningful behavior change | Explain the capability and update the relevant usage guidance. |
| Defect with observable impact | Describe the corrected behavior and the affected condition. |
| Compatibility break, removal, or deprecation | Make the impact prominent and provide the required action or replacement. |
| Setup, defaults, configuration, API, CLI, or supported environment | Update exact instructions and reference material. |
| Operational behavior, recovery, or deployment | Update the applicable runbook or deployment guide. |
| Contributor workflow or maintained architecture | Update contributor or architecture documentation when it becomes inaccurate. |
| Formatting, internal renaming, routine cleanup, or extra tests | Usually omit from reader-facing summaries unless there is a material audience impact. |
| Dependency or lockfile updates | Report a consequential compatibility, security, behavior, or build requirement; omit routine churn. |
| Documentation-only corrections | Correct the affected content; add a changelog entry only when the correction is itself significant or repository policy requires one. |

Do not infer improved speed, reliability, security, completeness, or production readiness from implementation changes alone. Use measured results or describe the concrete behavior without the unsupported benefit.

## 4. Choose documents and templates

Review `README.md` and `CHANGELOG.md` on every run. Update an existing document when its content needs to change; create a missing document under the creation rules below.

| Document | Update when | Content to include |
| --- | --- | --- |
| `README.md` | Project overview, capabilities, prerequisites, quick start, essential configuration, or documentation navigation changes. | Accurate current guidance and links to supporting detail. |
| `CHANGELOG.md` or release-note source | The work produces a notable change for the project's audience. | Brief entries grouped according to the repository's release convention. |
| Usage guides, tutorials, and examples | An affected task or example now works differently. | Correct steps, inputs, and expected results. |
| API, CLI, configuration, or schema reference | A public interface, default, constraint, or format changes. | Exact names, accepted values, defaults, compatibility, and examples. |
| Migration or upgrade guide | Existing users must take action. | Who is affected, what to change, and the required sequence. |
| Deployment, operations, and troubleshooting docs | Installation, monitoring, failure handling, or recovery changes. | The operational procedure readers need. |
| `CONTRIBUTING.md` or development setup | Build, test, local setup, or contribution practices change. | Updated contributor instructions. |
| Architecture docs and ADRs | Documented structure or an accepted architectural decision changes. | Current structure; preserve historical decisions and follow the project's supersession process. |
| Specifications and task records | Their recorded status or contract needs an authorized update. | Evidence-supported status; preserve acceptance requirements and unresolved gaps. |

Search for affected commands, options, configuration keys, paths, and concepts to locate relevant docs even when those documents are absent from the original diff. Include package READMEs in a monorepo when their audience is affected.

Preserve the repository's voice and structure. Edit the smallest useful sections. Keep detailed reference and migration material in their natural locations and link to it from summaries. Prefer relative links for files within the repository. [1]

If documentation or release notes are generated, edit their source or required change fragment and follow the existing generation process.

### Missing-document rules

| Condition | Required handling |
| --- | --- |
| A canonical document exists under another name or location | Update it and link to it; avoid creating a competing copy. |
| No README or equivalent exists | Create a concise project entry point from the relevant README profile. Inspect the current repository broadly enough to describe the project, prerequisites, and supported first-use path. |
| No changelog or release-note source exists | Create `CHANGELOG.md` when there are supported notable changes to record. Use verified task changes in an unreleased section; do not reconstruct old releases from assumptions. |
| A guide, reference, or runbook is missing | Create it when a concrete reader task requires detail that would overload the README. Use the corresponding document template and link it from the appropriate entry point. |
| There are no supported changelog entries | Leave the changelog absent unless the user or repository explicitly requires an initial scaffold. Report that no verified entries are available. |
| Information needed for accurate instructions is missing | Complete supported sections and identify the specific gap in the completion response. Ask only for information necessary to finish essential guidance. |

For a new document, inspect the current project as well as the task diff. A recent diff cannot establish the full installation process, project purpose, or supported interface. For an existing document, focus on the changed behavior and stale sections.

Use existing edit authorization when it covers creating documentation. In proposal mode, prepare the full proposed new file. Do not invent commands, URLs, credentials, owners, licenses, support guarantees, or release history. Remove irrelevant sections and empty placeholders before delivery. Clearly identify any essential known limitation.

### Template selection

Choose templates on two dimensions: **what the project is** and **what the document helps the reader do**. A hybrid repository can use several profiles. Keep tutorials, task instructions, reference material, and explanations distinct when their audiences or purposes differ. [6]

For an existing document, adapt its established structure. For a new one, prefer the repository's approved template; otherwise use the following outlines. These are recommended starting points, not requirements to create every listed document.

All README profiles begin with a short purpose statement, the intended audience, and any material maturity or availability constraint. Follow with the shortest supported path to a useful result, then relevant documentation links.

| Project profile | README emphasis | Supporting documents when needed |
| --- | --- | --- |
| CLI or automation tool | Install, prerequisites, first command, expected output. | Command reference, configuration, troubleshooting. |
| Library or SDK | Supported runtimes, installation, minimal working example. | API reference, examples, compatibility and migration guidance. |
| API or backend service | Local startup, configuration, first request, dependencies. | API contract, deployment, operations, architecture. |
| Web application | Purpose, local startup, primary user flow. | Configuration, contributor setup, deployment; screenshots when they explain usage. |
| Database or data tooling | Supported engines, permissions, setup, first operation. | Schema or data contracts, operational limits, migration, recovery. |
| Infrastructure project | Prerequisites, deployment scope, plan or preview, apply process. | Configuration, deployment, runbook, teardown where supported. |
| Agent or spec-driven framework | Execution environment, workflow entry point, implemented status, first task. | Workflow guide, skills or command catalog, artifact contracts, validation and governance. |
| Documentation or research project | Scope, reading path, how to use the material. | Methodology, references, contribution or reproduction instructions. |
| Monorepo | Workspace map and links to component entry points. | Component READMEs using their own profiles; shared setup and contribution guidance. |

The document templates supply the structure within those profiles:

| Document template | Suggested section order |
| --- | --- |
| README | Purpose → prerequisites → quick start → common use → documentation links. |
| Changelog | Unreleased entries → existing releases in descending order. |
| Tutorial | Learning goal → prerequisites → guided example → expected result → next task. |
| How-to guide | Task and applicability → prerequisites → steps → verify the result → troubleshooting. |
| API or CLI reference | Interface → parameters and defaults → returns or exit codes → errors → examples. |
| Configuration reference | Where configuration lives → precedence → settings and defaults → examples. |
| Migration guide | Affected users and versions → prerequisites → changes → migration steps → verify → recovery where supported. |
| Runbook | Trigger or symptom → prerequisites → diagnosis → procedure → verify → recovery and escalation. |
| Architecture explanation | Scope → components and responsibilities → interactions → constraints → decision links. |
| ADR | Decision status → context → decision → consequences → related decisions. |
| Contributor guide | Local setup → development workflow → checks → contribution process. |
| Specification or workflow | Purpose → inputs → required behavior or steps → outputs → acceptance evidence → known gaps. |

Omit sections that do not apply. Include information needed for the actual task even when it is absent from the outline. Keep a short guide inside an existing document when a separate file would add unnecessary navigation.

### README behavior

Describe the current supported state at the selected target. Keep the overview and getting-started path easy to scan. Preserve release or branch qualifiers so unreleased capabilities are not presented as available in the latest published version.

Do not append a work-session report, commit inventory, or implementation diary to the README.

### Changelog behavior

Use the existing format and release tooling. Where no convention exists, use an `Unreleased` section and the applicable Keep a Changelog categories: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, and `Security`. Include only categories with entries. [2]

Write one entry per meaningful outcome. Merge with existing unreleased entries when they describe the same change. Preserve published release history except for explicitly scoped factual corrections. Do not assign a version, fabricate a release date, or mark the work as released.

Make compatibility breaks prominent within the established format. Name the affected behavior and the required action, linking to migration details when necessary. Follow existing project disclosure rules for security entries.

## 5. Write for usability

Use a restrained, consistent Markdown layout that reads well both on GitHub and in a local editor. Apply the following standards to new and changed sections; avoid unrelated visual rewrites.

- Give each document one clear title and a logical heading hierarchy. Use descriptive, sentence-case headings without skipped levels. [8]
- Put purpose, applicability, and the reader's next action near the top.
- Use short paragraphs, ordered steps for procedures, and compact tables for comparisons or reference fields. [7]
- State prerequisites before commands. Identify the shell or language, working directory, required substitutions, and expected result when needed to make examples usable.
- Keep code examples complete enough for their purpose. Explain placeholders; never insert real secrets.
- Use meaningful link text, relevant relative links, and image descriptions. Add a contents list or documentation index only when it helps navigation. [1, 7]
- Use diagrams or screenshots when they explain a relationship or task more clearly. Keep an equivalent explanation in text.
- Avoid decorative badges, repeated banners, oversized tables, excessive emphasis, and unverified status indicators.
- Preserve a consistent vocabulary for concepts, commands, and project status. Keep operational facts in one maintained location and link to it where practical.

### Concise reporting rules

- Lead with the changed capability or behavior.
- Use one sentence per summary item where practical. Add a second only for a necessary condition, action, or limitation.
- Aim for roughly 15–35 words per changelog item as a default, not a hard limit.
- Group implementation steps that deliver the same result.
- Use exact technical names when the reader needs them to act.
- Keep explanations of individual files, functions, commits, and test cases out of summaries unless they matter to the audience.
- Replace vague claims such as "various improvements" with a concrete outcome.
- Keep required migration, compatibility, and operational details even when they make an entry longer.
- Link to deeper guidance instead of duplicating it.

Illustrative wording only; these are not claims about the target repository:

| Raw implementation detail | Reader-facing entry |
| --- | --- |
| Added a parser, renderer, and tests for an output format. | Added CSV export for filtered monitoring results. |
| Changed timer handling and added a regression test. | Fixed dashboard refreshes stopping after a temporary connection failure. |
| Renamed a required configuration key and updated validation. | **Breaking:** Replaced `poll_interval` with `poll_interval_seconds`; update existing configuration files before upgrading. |

## 6. Validate and finish

Before reporting completion:

- Compare every substantive claim with the selected target and its evidence.
- Confirm affected commands, options, defaults, paths, examples, and links agree across the edited documents.
- Check changed Markdown, relative links, heading anchors, and available documentation build or lint rules. Run only relevant checks and required repository gates.
- Preview the rendered documents when a preview is available. Check table readability, code fences, navigation, and heading structure; distinguish a source review from a rendered preview in validation results.
- For newly created documents, confirm a first-time reader can identify the purpose, prerequisites, next action, and expected result without relying on this conversation.
- Verify example behavior with existing evidence or safe, appropriate checks. Do not report an unexecuted example or test as passing.
- Review the final documentation edits against the pre-edit state, including new files. Confirm unrelated content and staging choices were preserved.
- Remove duplicate entries, speculative claims, and unnecessary detail.
- Ensure running the workflow again with the same evidence would add no duplicate entries or cosmetic churn.

Apply edits directly when authorized. If concurrent edits affect a target section, reread it and preserve the newer content. In proposal mode, provide exact replacement text or a reviewable patch rather than general suggestions.

This workflow does not itself authorize code changes, staging, commits, pushes, tags, releases, or deployments. Perform those only when already included in the user's authorized task.

An unchanged document is a valid result. If all documentation remains accurate and there are no notable undocumented changes, finish without edits.

## Completion response

Return a short result in this format. Omit empty fields and keep the highlights to one to three bullets unless more are needed for a required user action.

```text
Result: updated | proposed | no_change | partial | blocked
Scope: <comparison point and target; mention uncertainty only if material>
Documents: <paths created, updated, or proposed>
Highlights:
- <meaningful outcome>
Validation: <checks performed and relevant limitations>
Action required: <migration, unresolved discrepancy, or essential clarification>
```

Use `updated` for completed updates or creations, `proposed` for fully prepared edits in proposal mode, and `no_change` when no edits are warranted. Use `partial` when supported updates are complete but an unresolved issue remains; use `blocked` when no accurate update can proceed.

Report the documentation outcome. Do not repeat every implementation change or paste the evidence inventory into the completion response.

## Git inspection reference

These are command templates, not a script. Run them from the repository root; replace `<BASE>` with the resolved commit. [3–5]

| Purpose | Command |
| --- | --- |
| Inspect local state | `git status --short --untracked-files=all` |
| Inspect unstaged changes | `git diff --` |
| Inspect staged changes | `git diff --cached --` |
| List untracked, non-ignored files | `git ls-files --others --exclude-standard` |
| Inspect committed changes since baseline | `git diff <BASE> HEAD --` |
| Inspect net tracked working-tree changes since baseline | `git diff <BASE> --` |
| Inspect changed paths and renames | `git diff --name-status --find-renames <BASE> --` |
| Check tracked documentation whitespace | `git diff --check -- <DOC_PATHS>` and `git diff --cached --check -- <DOC_PATHS>` |

The staged and unstaged views can overlap or cancel each other. Use the selected target's net state for reporting; inspect untracked files separately. A clean working tree does not exclude relevant committed work. Review newly created docs directly because normal tracked-file diffs omit untracked content. When scripting file inventories, use NUL-delimited output and parsing to handle unusual filenames.

## Invocation example

```text
Run the repository documentation update workflow after completing this task.
Use the established task scope and before state, inspect the actual diffs,
and update README.md, CHANGELOG.md, and any affected documentation.
Create missing documents when warranted, using the appropriate project
profile and document template. Keep the results professional and usable.
Apply the edits under the existing repository-edit authorization.
Summarize meaningful outcomes concisely, preserve required user actions,
validate the documentation, and return the compact completion response.
```

## References

The workflow's scope, authorization, evidence, editorial, and completion rules are recommended operating rules. The sources below support the underlying README, changelog, and Git conventions.

1. [GitHub: About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
2. [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/)
3. [Git: git-diff](https://git-scm.com/docs/git-diff)
4. [Git: git-status](https://git-scm.com/docs/git-status)
5. [Git: git-ls-files](https://git-scm.com/docs/git-ls-files)
6. [Diátaxis: documentation purposes and structure](https://diataxis.fr/)
7. [Google developer documentation style guide: highlights](https://developers.google.com/style/highlights)
8. [Google developer documentation style guide: headings and titles](https://developers.google.com/style/headings)
