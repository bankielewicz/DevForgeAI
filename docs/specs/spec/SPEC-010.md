---
id: SPEC-010
type: spec
title: "GitHub post skill"
status: approved       # draft | in-review | approved | superseded | deprecated
version: 1
created: 2026-09-29
updated: 2026-09-29
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "fdbef416-eebb-4053-95ce-624a311d72d5"
reviewed_by: []
approved_by: "Bryan"
approved_on: 2026-09-29
upstream:
  - {id: PRD-001, item: NFR-001, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-002, relation: constrains, version: 10, hash: null}
  - {id: PRD-001, item: NFR-003, relation: constrains, version: 10, hash: null}
  - {id: ADR-001, relation: constrains, version: 4, hash: null}
  - {id: SPEC-007, relation: informed_by, version: 1, hash: null, note: "the git skill: PR creation and the outward-action rule"}
supersedes: []
superseded_by: null
blocked_by: []
# --- spec-specific ---
components: ["src/claude/DevForgeAI/skills/github-post", "src/tests/github-post"]
---

# SPEC-010 — GitHub post skill

## 1. Overview

The `github-post` skill ships in the `devforgeai` plugin and is invoked as
`/devforgeai:github-post [PR|Incident|Enhancement] [subject]`, or when a user asks to file an
issue or write a pull request description. It writes one GitHub post of the chosen kind that a
reader with none of the author's context can act on, checks it, and posts it with `gh` when the
user has authorized that.

It codifies the workflow used to write issue #19 on 2026-09-29:
- pin every reference to one commit, a file and a line, and quote the exact text;
- rebuild run evidence (session IDs, versions, fixture, request, answers, a timeline) from its record;
- keep facts, proposals and the owner's decisions in separate sections, with the decision's status
  stated, and cite a decision already made rather than asking for it again;
- say what the next agent must do: investigate, obtain a decision, or implement a supported solution;
- give the implementer preconditions, exact old and new text where the evidence determines it,
  verification commands with their expected output, acceptance criteria and what is out of scope;
- make the post self-sufficient: a fresh agent with only the post and the repository can act on it;
- check that each quoted anchor occurs exactly once, and scan for local paths and personal data;
- post, write the new post's own number into its body, and view it back.

The skill is recorded as `SKL-009` in its `provenance.yaml`. SKL-008 is reserved by SPEC-009.

## 2. Constraints

- **PRD-001 NFR-001 to NFR-003**, as for the other skills: a short `SKILL.md` with detail in
  `references/`, spec-only frontmatter with provenance in the sidecar, and behaviour proven by the
  eval suite in §9.
- **ADR-001 v4:** built in a worktree from `src/`, deployed with rsync, evaluated from a plain terminal.
- **SPEC-007 (the git skill, draft):** git operations belong to the git skill. This skill never
  commits, pushes, merges, creates branches or runs documents-updater. It creates a pull request
  only from a branch already on the remote, as SPEC-007's pr phase also does; §12 records that
  overlap. Its outward-action rule (BEH-13) follows SPEC-007 BEH-04: an action is authorized when
  the request names it or the user confirms it in the run.
- **GitHub:** posting uses the `gh` CLI. Whatever is posted to a public repository is published,
  and may be cached or indexed even if deleted later.

## 3. Architecture and components

```
src/claude/DevForgeAI/
├── skills/github-post/
│   ├── SKILL.md                     # checklist, user decisions, output contract
│   ├── provenance.yaml              # SKL-009, implements SPEC-010
│   ├── assets/
│   │   ├── pr.md                    # moved from src/templates/github/ at build time
│   │   ├── incident.md
│   │   └── enhancement.md
│   ├── references/
│   │   ├── fidelity.md              # claims, sources, facts vs proposals vs decisions, cold-reader rules (BEH-03, BEH-05..07)
│   │   ├── evidence.md              # pinning revisions, quoting, run evidence and timelines (BEH-03, BEH-04)
│   │   └── posting.md               # PR mode, duplicates, labels, authorization, posting, reporting (BEH-08, BEH-11..14, BEH-16)
│   └── scripts/check_post.py        # read-only: references, anchors and the safety scan (BEH-09, BEH-10)
└── evals/github-post/<case>/        # one case per automated VER item (§9)
src/tests/github-post/               # unit tests for check_post.py (VER-08) and the eval generator; not deployed
```

```mermaid
flowchart LR
    K[Kind and subject BEH-01] --> R[Repository and access BEH-02]
    R --> E[Evidence, pinned BEH-03 BEH-04]
    E --> D[Draft from the template BEH-05..08]
    D --> C[Check references and anchors BEH-09]
    C --> S[Safety scan BEH-10]
    S --> U[Duplicates BEH-11]
    U --> A{Authorized? BEH-13}
    A -->|no or no user| Q[Show the draft and ask, or draft only]
    A -->|yes| P[Labels, post, own number, view back BEH-12 BEH-14]
    P --> O[Report BEH-16]
    Q --> O
```

## 4. Data model

**Kinds** (the first word of `$ARGUMENTS`, matched case-insensitively):

| Kind | Template | Required sections |
|---|---|---|
| `pr` | `assets/pr.md` | Summary; Changes; Implements and references; Checks run (each at the head SHA); Not verified and limitations; Revision (base and head SHAs); the attribution line |
| `incident` | `assets/incident.md` | Summary with the next action; Where the gap is; Evidence; Why it matters; Decision required (when a choice belongs to the owner); Implementation, or Investigation for next action investigate; Verification; Acceptance criteria; Out of scope; References |
| `enhancement` | `assets/enhancement.md` | Summary with the next action; Current behaviour; Motivation; Proposed behaviour; Decision required (when a choice belongs to the owner); Implementation, or Investigation for next action investigate; Verification; Acceptance criteria; Out of scope; References |

**Claims and sources.** Every factual sentence in a post has a source the reader can check:
- a file and line at a named commit;
- a document's version and SHA-256 at that commit;
- a command with its output;
- a run or session ID, with where its record is;
- a URL, or who said it, when and where.

A statement without one is a proposal (labelled "Proposed") or an unknown ("Unknown: <what is
missing>").

**The next action** (incident and enhancement) is exactly one of these, stated in the Summary:

| Next action | When | Section 5 |
|---|---|---|
| `investigate` | The evidence doesn't establish the cause, or no solution is supported yet | **Investigation**: the questions to answer, where to look (paths and commands), how to reproduce, what to record, when to stop, and what to report back on the issue. No patch |
| `decide` | A supported solution has options that belong to the owner, and no decision is recorded | **Implementation** of the proposed option, gated on the owner's decision (the decision block is pending) |
| `implement` | The solution is decided (a cited decision) or needs no owner decision, and the evidence supports it | **Implementation**: exact old and new text, or a new file's exact content, for each change the evidence fully determines. A change that can't be fixed exactly without running code is a bounded step with the check that confirms it, never a guessed patch |

**The decision block** (incident and enhancement, when a choice belongs to the owner):
- a status: `pending`, or `decided` with who decided, when and where, quoting the decision (a
  conversation line with its date, an issue comment's URL, or a record such as a Change Log row);
- one row per option, each with its consequence, and at most one labelled "(proposed)" or "(decided)";
- when pending: the gate (don't implement until the owner records the decision on the issue), and
  the implementation of the proposed option only, with the instruction to stop and ask for new steps
  if another option is chosen;
- when decided: no gate; the post cites the decision, and the implementation follows it.

**Citations** use a form `check_post.py` can read (BEH-09):
- the pinned revision: `Every reference below is to <ref> at <SHA>`, with a SHA of at least 7 hex
  digits that resolves in the repository;
- a quoted source: `` `<path>` line N `` or `` `<path>` lines N–M ``, optionally followed by
  `at <SHA>` when it differs from the pinned revision, then either `: "<quote>"` on the same line or
  a `>` block quote on the next lines. An omission inside a quote is written `…`;
- a replacement: the step names the file as `` `<path>` ``, then `replace`, the old text in a code
  span or block, `with`, and the new text.

**Accessible evidence.** Everything the next action depends on is readable by someone who has only
the post and the repository: committed at the cited revision, quoted in the post, or at a URL they
can open. Evidence that exists on one machine only, such as a session transcript, may be cited as
supporting evidence and marked local, but the post quotes the parts the next action needs.

**The post's own number.** Until the post exists it has no number, so the draft writes a
reference to itself as `#{{self}}`. BEH-14 replaces it after the post is created.

**The draft** lives in the system temp folder, as the file passed to `--body-file`. It is never
written into the repository.

## 5. Interfaces and contracts

```yaml
# Proposed SKILL.md frontmatter (validated by src/schemas/skill-frontmatter.schema.json)
name: github-post
description: Writes and posts a GitHub pull request description, incident or enhancement that a reader with no context can act on. Every claim is pinned to a commit, file and line or to a recorded run, quotes are checked, facts are kept apart from proposals and the owner's decisions, and incidents and enhancements give the implementer exact steps, verification and acceptance criteria. Use when the user asks to file, open, post or write up a GitHub issue, bug, incident, enhancement or feature request, or to write, post or update a pull request's description, even when they don't name the skill. Not for committing, pushing or merging (use /devforgeai:git), or for GitHub questions that post nothing.
argument-hint: "[PR|Incident|Enhancement] [subject]"
metadata:
  devforgeai-id: "SKL-009"
  devforgeai-version: "1"   # at the first build; always equal to provenance.yaml's version
```

- **The name must be exactly `github-post`.** The skill is model-invocable.
- **The version isn't fixed here.** `metadata.devforgeai-version` must equal `provenance.yaml`'s
  `version`.
- **Arguments:** the kind (`PR`, `Incident` or `Enhancement`, in any case), then an optional subject
  in free text.
- **Tools:**
  - Read, Glob and Grep;
  - Bash for read-only `git` (`rev-parse`, `show`, `log`, `ls-remote`, `status --porcelain`,
    `diff --cached`), for `gh` (`repo view`, `auth status`, `issue list`, `issue create`,
    `issue edit`, `issue view`, `pr list`, `pr create`, `pr edit`, `pr view`, `label list`,
    `label create`), and for `python3` with `scripts/check_post.py`;
  - AskUserQuestion for the user's decisions, or plain text ending the turn when it isn't available.
- **Output:** the posted URL, or the full draft with the exact `gh` command that would post it.

## 6. Behavior

```yaml items
behaviors:
  - id: BEH-01
    status: active
    rule: "Take the kind from the first word of $ARGUMENTS: pr, incident or enhancement, in any case; the rest is the subject. When the kind is missing, ask which of the three, and write nothing until the answer arrives. When the request states the kind in words (file a bug, write up an enhancement, write the PR description), that is the kind."
  - id: BEH-02
    status: active
    rule: "Resolve the target repository from the origin remote with gh repo view --json nameWithOwner,visibility,defaultBranchRef, and check gh auth status. Record the visibility, because BEH-10 blocks more on a public repository. When there is no GitHub remote, gh is signed out or the network can't be reached, continue in draft-only mode (ERR-02)."
  - id: BEH-03
    status: active
    rule: "Pin every reference to one commit: record its full SHA (git rev-parse), cite files as path and line at that commit, and cite a versioned document by its version, status and SHA-256 at that commit. Never present uncommitted content as fact about the repository; when the draft relies on the working tree, say so and name the files."
  - id: BEH-04
    status: active
    rule: "Gather evidence read-only: Read, Grep, git show, git log, gh issue view and gh pr view. Quote the text a claim rests on exactly. For a run, cite its session or run ID, tool and model versions, the build or plugin revision and how it was loaded, the fixture, the exact request and answers, and a timeline in UTC rebuilt from the transcript or log. Evidence that exists only on one machine is marked local, cited with a ~ path rather than an absolute home path, and anything since overwritten is named."
  - id: BEH-05
    status: active
    rule: "Write every factual sentence with a source from §4, and keep facts, proposals and decisions in separate sections. Label each proposal Proposed. Write nothing aspirational: no future benefit, saving, effort or certainty without a cited basis. State an unknown as Unknown: <what is missing> instead of guessing."
  - id: BEH-06
    status: active
    rule: "In an incident or enhancement, record every choice that belongs to the owner in the decision block (§4). When the owner already decided, in this conversation or in a cited record, the status is decided: cite who, when and where, quote the decision, give no gate, and make the implementation follow the decided option. Otherwise the status is pending: give each option its consequence, label at most one (proposed) and only when the evidence supports it, include the gate, and make the implementation cover the proposed option only, with the instruction to stop and ask when another option is chosen."
  - id: BEH-07
    status: active
    rule: "Write an incident or enhancement for a reader with none of the author's context. State the next action (§4) in the Summary, chosen from the evidence: investigate when the cause or a supported solution isn't established, decide when a supported solution needs the owner's choice, implement when it is decided or needs no decision. For investigate, section 5 is the investigation plan (§4). For decide and implement, section 5 names the repository's instruction files to read first, the preconditions and what to do when one doesn't hold, and each change: exact old and new text, or a new file's exact content, where the evidence fully determines it, otherwise a bounded step with the check that confirms it. Say which files are not changed; give each verification command with where to run it and its expected output; leave anything that costs money or time to the owner's decision, with its cost; end with an acceptance checklist, what is out of scope and the references, including which tool and session wrote the post."
  - id: BEH-08
    status: active
    rule: "For a pr, bind the post to the remote head. Read the remote branch's SHA (git ls-remote --heads origin <branch>). Stop with ERR-03 when the branch isn't there, when its SHA differs from git rev-parse HEAD (commits not pushed or not pulled), or when git status --porcelain shows tracked changes. Take the base as the remote default branch's SHA (git ls-remote), and its merge base with HEAD when that commit is present locally. The Revision section states the base and head SHAs. Each check listed under Checks run cites the SHA it ran at, with its result, and comes from this session or a cited record; a check run at another SHA, or with tracked changes present, is listed under Not verified with that SHA. Look for an open PR from the branch (gh pr list --head <branch> --state open --json number,headRefOid). With none, create it with gh pr create --base <default branch> --head <branch> --title <title in the repository's commit convention> --body-file <draft>, as a draft PR when a required check failed or wasn't run at the head. With one, stop with ERR-03 when its headRefOid differs from the head SHA the body describes; otherwise update its title and body with gh pr edit. Run no document-ID collision check: when this skill creates the PR, its limitations say 'Document-ID collision not checked; /devforgeai:git pr runs that check.' Never commit, push, merge, change a PR's draft state after creation, or run documents-updater."
  - id: BEH-09
    status: active
    rule: "Before posting, run python3 ${CLAUDE_SKILL_DIR}/scripts/check_post.py on the draft. Reading each cited commit with git show <sha>:<path>, it checks the citations written in the §4 form: every cited path and line range exists; every quotation attributed to a path and lines matches the text at those lines, comparing with whitespace normalized and matching the parts around each … in order; and each text the implementation says to replace occurs exactly once in its file at the pinned revision, with an anchor wrapped across lines reported so the draft can say so. Fix the draft or remove the claim until the check passes; never post while it fails (ERR-04). When a cited commit can't be read, the check for those citations is unavailable (ERR-09): it is never replaced by reading the working tree, and the report lists the citations not checked."
  - id: BEH-10
    status: active
    rule: "Scan the draft before posting, with the same script: absolute home paths (/home/<user>, /Users/<user>, C:\\Users\\<user>), email addresses, token and secret patterns, and transcript excerpts longer than a short quote. Rewrite home paths as ~ or repository-relative paths. On a public repository any remaining hit blocks posting until it is removed (ERR-05); on a private one, ask. Report each hit by its line in the draft, never by repeating the text."
  - id: BEH-11
    status: active
    rule: "Before creating an issue or PR, search the open ones for the same subject (gh issue list --search and gh pr list --search, with the subject's key terms). When a candidate exists, list it and ask whether to create a new post, comment on the existing one, or stop. With no user, create nothing."
  - id: BEH-12
    status: active
    rule: "Label an incident bug and an enhancement enhancement; a PR gets no label. When the label doesn't exist (gh label list), create it with gh label create, using GitHub's default colour and description for that name, as part of the authorized post (BEH-13), and report that it was created. Never create any other label."
  - id: BEH-13
    status: active
    rule: "Posting is outward-facing. Creating or editing an issue or PR, and creating a label for it, is authorized when the request names the action (post an incident about X, open the PR, update the PR description) or when the user confirms it in this run after seeing the draft; the authorization covers this run only. Otherwise show the full draft in the reply (kind, title, labels, target repository, body) and ask whether to post it. When no answer can arrive, post nothing and give the exact gh command that would post it."
  - id: BEH-14
    status: active
    rule: "Post with --body-file, never with the body inline. After creation, replace each #{{self}} in the body with the new number through gh issue edit or gh pr edit, then view the post back (gh issue view or gh pr view --json title,state,labels,body) and confirm the title, the labels and that no #{{self}} or {{ placeholder remains."
  - id: BEH-15
    status: active
    rule: "Write nothing into the repository: no file edits, commits, pushes or branches. The draft lives in the system temp folder."
  - id: BEH-16
    status: active
    rule: "Report, in order: the URL, or 'not posted' with the reason and the exact gh command; the kind, the title and the next action; the labels, naming any created; each check with its result (citations and anchors: passed, failed or unavailable; the safety scan; the duplicate search; for a pr, the base and head SHAs); the decision status; and anything pending, such as a failed edit (ERR-07). When nothing was posted, the reply also contains the full draft."
  - id: BEH-17
    status: active
    rule: "Make the post self-sufficient (§4, accessible evidence): everything the next action depends on is readable with only the post and the repository, as content committed at the cited revision, a quotation in the post, or a URL the reader can open. Evidence that exists on one machine only is cited as supporting evidence and marked local, and the post quotes the parts the next action needs."
```

## 7. Errors and edge cases

```yaml items
errors:
  - id: ERR-01
    status: active
    condition: "The kind is not pr, incident or enhancement"
    handling: "Say so, list the three kinds, ask which one, and write nothing"
    user_result: "The three kinds and a question"
  - id: ERR-02
    status: active
    condition: "There is no GitHub remote, gh is signed out, or the network can't be reached"
    handling: "Continue in draft-only mode: every check still runs, nothing is posted, and the reply gives the draft and the exact gh command, plus gh auth login when gh is signed out"
    user_result: "The full draft, the reason it wasn't posted and the command to post it"
  - id: ERR-03
    status: active
    condition: "For a pr, the branch isn't on the remote, its remote SHA differs from the local HEAD, tracked changes are uncommitted, or the open PR's head differs from the head the body describes"
    handling: "Post nothing. Name the mismatch with both SHAs, say what to do first (commit and push with /devforgeai:git, or pull the remote commits), and offer the draft body"
    user_result: "The mismatch, the next step and the draft"
  - id: ERR-04
    status: active
    condition: "The reference or anchor check still fails after the draft is fixed, for example when the cited text has changed at the cited commit"
    handling: "Post nothing. List each failing reference or anchor with the reason, and keep the draft"
    user_result: "The failures and the draft"
  - id: ERR-05
    status: active
    condition: "The safety scan still finds a home path, email address, secret or long transcript excerpt on a public repository"
    handling: "Post nothing. List each hit by its line in the draft without repeating it, and keep the draft"
    user_result: "The lines to fix and the draft"
  - id: ERR-06
    status: active
    condition: "The user declines to post, or no answer can arrive"
    handling: "Post nothing and keep the draft"
    user_result: "The draft and the command that would post it"
  - id: ERR-07
    status: active
    condition: "The post was created but a later step failed: filling in its own number, a label, or the view-back"
    handling: "Never delete the post. Report its URL and the exact command for each step still pending"
    user_result: "The URL and the pending commands"
  - id: ERR-08
    status: active
    condition: "The evidence doesn't support a required section, or the core claim has no evidence at all"
    handling: "Write the section as Unknown: <what is missing>, and make the next action investigate rather than guess a solution. When the core claim has no evidence, ask before posting; with no user, post nothing"
    user_result: "A draft with its unknowns stated and an investigation plan, and a question when the core claim is unsupported"
  - id: ERR-09
    status: active
    condition: "A cited commit can't be read, for example in a shallow clone or a sandbox that blocks git, so the citation check is unavailable for some citations"
    handling: "Never check against the working tree instead. Report the check as unavailable and list the citations not checked. Ask before posting; with no user, post nothing"
    user_result: "The citations not checked, and a question"
```

## 8. Non-functional design

```yaml items
quality_responses:
  - id: QR-01
    status: active
    response: "SKILL.md holds only the checklist, the user's decisions and the output contract; the fidelity, evidence and posting rules live in references/, and the templates in assets/"
    measured_by: "SKILL.md line count (at most 500) and description length (at most 1024 characters)"
    upstream:
      - {id: PRD-001, item: NFR-001, relation: satisfies, version: 10, hash: null}
  - id: QR-02
    status: active
    response: "Frontmatter limited to the fields in §5; provenance in provenance.yaml; metadata values quoted, with devforgeai-version equal to the provenance version"
    measured_by: "Reading against skill-frontmatter.schema.json and skill.schema.json, and comparing the two version values"
    upstream:
      - {id: PRD-001, item: NFR-002, relation: satisfies, version: 10, hash: null}
  - id: QR-03
    status: active
    response: "One eval case per automated VER item, tagged github-post and ver-NN, run against the no-plugin baseline; VER-12, which needs two sessions in sequence, runs as a harness script instead"
    measured_by: "claude plugin eval --threshold 0.8 over 3 runs"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 10, hash: null}
```

## 9. Verification

| Kind | Status |
|---|---|
| Version 1 | Approved by Bryan on 2026-09-29, after the revision that followed his review of `aa3563f`; not built. The templates are staged in `src/templates/github/` |
| Structural: this spec against `spec.schema.json` | Passes (checked 2026-09-29) |
| Scope of the automated suite | Eval runs have no network, so every automated case runs in draft-only mode (ERR-02). The automated suite verifies drafting, the checks and refusals. **Posting (BEH-11 to BEH-14, ERR-07) is verified only by hand** (VER-09, VER-10), the same gap SPEC-007 has for pushes and merges. Whether a fresh agent can act on a post is verified by the VER-12 harness, run from a plain terminal |
| Risk to settle at build time | `check_post.py` reads `git show <sha>:<path>`, so VER-01's and VER-11's fixtures are git repositories with commits. The eval sandbox masks `.git/config.lock` in repositories a scaffold builds, where `git config`, `remote add` and `push -u` fail (CLAUDE.md, "Evaluating a skill"); whether read-only `git show` works there is unverified. The check never falls back to the working tree: if `git show` fails, the run reports the check unavailable (ERR-09), and the cases grade the draft's quotations against the fixture text at the SHAs that `make_evals.py` records after verifying them itself when it generates the cases |

```yaml items
verifications:
  - id: VER-01
    status: active
    obligation: "Incident, decided: a fixture git repository with commits, holding a spec whose rule leaves a case unhandled and a committed run log showing it. The request names the kind and the gap and states the owner's decision with its date; there is no network. The reply holds the full draft with every incident section from §4; the Summary states next action implement; the decision block is decided, cites the request's decision and has no gate; each cited path and line exists at the pinned SHA and each quotation matches the fixture text at those lines; the implementation gives exact old and new text for the fix; no absolute home path appears; and the reply says nothing was posted, with the gh command. Eval case incident-decided: regex and llm on last_message."
    level: e2e
    covers:
      - BEH-01
      - BEH-03
      - BEH-04
      - BEH-05
      - BEH-06
      - BEH-07
      - BEH-09
      - BEH-15
      - BEH-16
      - BEH-17
      - ERR-02
  - id: VER-02
    status: active
    obligation: "Enhancement, pending: a fixture repository and a request for a new capability, attributed to a named requester, with two ways to provide it and no decision. The draft has every enhancement section; the Summary states next action decide; each proposal is labelled Proposed; the motivation cites who asked; no benefit, saving or effort estimate appears without a cited basis; and the decision block is pending, with the gate. Eval case enhancement-pending: llm and regex on last_message."
    level: e2e
    covers:
      - BEH-01
      - BEH-05
      - BEH-06
      - BEH-07
  - id: VER-03
    status: active
    obligation: "PR not bound to the remote: a fixture repository with a local bare origin, as the git skill's evals use. In one case the branch isn't on the remote; in the other the remote branch is one commit behind the local HEAD. Each posts nothing, names the mismatch with both SHAs where both exist, says to push first with /devforgeai:git, and runs no git push. Eval cases pr-branch-not-pushed and pr-head-not-pushed: regex on last_message; the bare remote is unchanged afterwards."
    level: e2e
    covers:
      - BEH-08
      - ERR-03
  - id: VER-04
    status: active
    obligation: "Unknown kind: '/devforgeai:github-post Question about the roadmap' lists the three kinds, asks which one, and writes no draft. Eval case unknown-kind: regex and llm on last_message."
    level: e2e
    covers:
      - BEH-01
      - ERR-01
  - id: VER-05
    status: active
    obligation: "Not authorized: a request that asks for an enhancement write-up without asking to post it. With no user, the reply holds the full draft, asks whether to post it or says nothing was posted, and gives the gh command. Eval case not-authorized: llm on last_message."
    level: e2e
    covers:
      - BEH-13
      - BEH-16
      - ERR-06
  - id: VER-06
    status: active
    obligation: "Safety: the fixture's run log contains an absolute home path (/home/alex/...) and an email address. The draft cites the log with a ~ or repository-relative path, contains neither the home path nor the email address, and the reply doesn't repeat them. Eval case safety-scan: regex not_contains on last_message."
    level: e2e
    covers:
      - BEH-10
      - ERR-05
  - id: VER-07
    status: active
    obligation: "A request such as 'explain how GitHub issue templates work' does not invoke the skill. Eval case ignores-unrelated-request: tool_used Skill min 0 max 0 arm both."
    level: e2e
    covers:
      - QR-02
      - QR-03
  - id: VER-08
    status: active
    obligation: "check_post.py unit tests: a path and line that exists at the commit passes and one that doesn't fails; a quotation that matches its cited lines passes, one that differs fails, and one with … matching its parts in order passes; an anchor found once passes, twice or never fails, and one wrapped across lines passes with the wrap reported; a citation at a commit that can't be read is reported unavailable and the working tree is never read; a home path, an email address and a token pattern are each reported by line without the text; a clean draft passes. Tests in src/tests/github-post/."
    level: unit
    covers:
      - BEH-09
      - BEH-10
      - ERR-04
      - ERR-09
  - id: VER-09
    status: active
    obligation: "Manual, on a GitHub test repository: post an incident with a missing bug label (the label is created and reported); #{{self}} is replaced with the new number and the view-back shows no placeholder; create a PR from a pushed branch whose body states the base and head SHAs and lists each check at the head SHA, then update its body; an update is refused when someone has pushed to the PR after the body was drafted; a second incident on the same subject finds the first and asks; a simulated failure after creation (for example a revoked label permission) reports the URL and the pending command and deletes nothing; the repository's visibility is read and reported."
    level: manual
    covers:
      - BEH-02
      - BEH-08
      - BEH-11
      - BEH-12
      - BEH-14
      - ERR-07
  - id: VER-10
    status: active
    obligation: "Manual: a request that names the posting action posts after the checks pass; a request that doesn't shows the draft and asks, and posts only on a yes; an incident whose core claim has no evidence asks before posting and writes Unknown in the unsupported sections; SKILL.md is within the NFR-001 limits."
    level: manual
    covers:
      - BEH-13
      - ERR-08
      - QR-01
  - id: VER-11
    status: active
    obligation: "Incident, investigate: a fixture repository whose committed log shows a failure but whose sources don't establish its cause. The draft's Summary states next action investigate; section 5 is an investigation plan with the questions to answer, where to look, how to reproduce, what to record, a stop condition and what to report back; it gives no replacement text; and it writes Unknown where the cause would go. Eval case incident-investigate: regex and llm on last_message."
    level: e2e
    covers:
      - BEH-07
      - ERR-08
  - id: VER-12
    status: active
    obligation: "Cold-session acceptance, run by src/tests/github-post/cold_session.py from a plain terminal. Stage A runs the skill with claude -p in a copy of a fixture repository and drafts two incidents: one implement (the request states the decision) and one investigate. Stage B gives only a draft's body to a fresh claude -p session, without the plugin and without the author's conversation, in a clean copy of the fixture repository at the pinned SHA that holds none of the author's local files. For the implement draft, stage B's changes meet every acceptance criterion and each verification command prints its expected output; for the investigate draft, stage B's report answers every listed question with cited evidence. A draft that depends on anything outside the post and the repository fails. It is a harness, not a claude plugin eval case."
    level: e2e
    covers:
      - BEH-07
      - BEH-17
```

## 10. Rollout, migration and rollback

The skill is new; removing its directory rolls it back. It changes no document type or schema.
Building it bumps `plugin.json` and extends the plugin description, at Bryan's choice at build time.

## 11. Implementation plan

After Bryan approves this spec:

1. Create an ADR-001 worktree for the build.
2. Copy `src/templates/skill/` to `skills/github-post/`; write `SKILL.md` from §5–§7 and
   `provenance.yaml` as SKL-009 implementing SPEC-010.
3. `git mv src/templates/github/{pr,incident,enhancement}.md skills/github-post/assets/`, and update
   the templates README row.
4. Write `references/fidelity.md`, `references/evidence.md` and `references/posting.md`.
5. Write `scripts/check_post.py` (BEH-09, BEH-10) and its unit tests in `src/tests/github-post/`
   (VER-08). Settle the §9 risk first: check `git show` in a scaffold-built repository under
   `claude plugin eval`.
6. Write `src/tests/github-post/make_evals.py`, which generates the cases for VER-01 to VER-07 and
   VER-11, verifies their fixture commits and records the SHAs, and check the regex graders offline
   with good and bad replies. Write `src/tests/github-post/cold_session.py` for VER-12.
7. Bump `plugin.json` and extend its description (Bryan's choice); add the CLAUDE.md and AGENTS.md
   rows.
8. Evaluate cheapest first (a pilot, one run, then three runs with the baseline), deploy, and run
   VER-09 and VER-10 by hand.

## 12. Alternatives considered

| Option | Why not chosen |
|---|---|
| Extend the git skill with incident and enhancement posting | Measured on 2026-09-29, the git skill is the plugin's largest: SKILL.md 274 lines, 20 behaviours, 5 references, 3 scripts and 16 eval cases, built from a draft SPEC-007 of 776 lines. Its description is 842 of 1,024 characters. Issue posting is a different concern (evidence, quote checks, decision blocks); adding it would push the description near the limit, blur when the skill triggers, and require re-evaluating all 16 cases. Bryan's rule was to choose this separate skill if extending the git skill would make it unstable (2026-09-29) |
| Call the git skill's `repo_state.py` for the document-ID collision check before creating a PR | Couples this skill to a script of a draft spec that could change. The PR's limitations say the check didn't run and point to `/devforgeai:git pr` instead (BEH-08) |
| GitHub issue forms only (`.github/ISSUE_TEMPLATE/`) | A web form can't pin evidence to a commit, check quotes or scan for local paths. Bryan chose the templates in `src/templates/` and this spec for now (2026-09-29) |
| One template for every kind | The kinds need different sections: a PR reports checks run and not verified; an incident needs evidence and a timeline; an enhancement needs the requester and the proposal |
| Always require an owner comment before implementation | Blocks work the owner has already authorized. A decided status cites the decision instead, and the gate applies only while a decision is pending (BEH-06; Bryan's review, 2026-09-29) |
| Always give exact patches | Not every incident has an established cause or a supported solution; a guessed patch misleads the next agent. The next action says whether to investigate, decide or implement (BEH-07, ERR-08) |
| Check citations against the working tree when the cited commit can't be read | The working tree doesn't show what existed at the cited commit. The check is reported unavailable instead (ERR-09) |

## 13. Open questions

- Not decided, and outside this spec: whether SPEC-007's pr phase adopts `assets/pr.md` for its PR bodies (a SPEC-007 change), and a Codex port of this skill.
- Resolved by Bryan on 2026-09-29:
  - PR mode creates from a pushed branch or updates the open PR, and never pushes (BEH-08);
  - posting follows BEH-13;
  - missing labels are created (BEH-12);
  - this change delivers the spec and the templates, and the skill is built after approval (§11).
- Resolved by Bryan on 2026-09-29, after approval: the label mapping stays as BEH-12 has it, incident → bug ("bug is fine").

## Change Log

| Version | Date | Author | Change | Items affected |
|---|---|---|---|---|
| 1 | 2026-09-29 | claude-code (session fdbef416-eebb-4053-95ce-624a311d72d5) | Initial draft from Bryan's decisions of 2026-09-29: the workflow used for issue #19 as a skill, with PR mode that creates or updates but never pushes, posting when the request names it, labels created when missing, and the templates staged in src/templates/github/. The label mapping (§13) awaits confirmation. Awaiting Bryan's approval | all |
| 1 | 2026-09-29 | claude-code (session fdbef416-eebb-4053-95ce-624a311d72d5) | Revised after Bryan's review of commit aa3563f, still version 1 and still a draft: (1) a decision already made is cited and doesn't gate the work (§4, BEH-06); (2) the next action is investigate, decide or implement, with exact patches only where the evidence determines them (§4, BEH-07, ERR-08, VER-11); (3) citations are never checked against the working tree, an unreadable commit makes the check unavailable, and every quotation is matched to its cited lines (§4 citations, BEH-09, ERR-09, §9); (4) a PR is bound to its remote head, with base and head SHAs and each check at the head (BEH-08, ERR-03, VER-03); (5) posts are self-sufficient, and a cold session acting on a post is tested (BEH-17, VER-12). The frontmatter example's version is 1. Awaiting Bryan's approval | §1, §4, §5, BEH-06..09, BEH-16, BEH-17, ERR-03, ERR-08, ERR-09, QR-03, §9, VER-01..03, VER-08..12, §11, §12 |
| 1 | 2026-09-29 | Bryan | Approved | status |
| 1 | 2026-09-29 | claude-code (session fdbef416-eebb-4053-95ce-624a311d72d5) | Record-only update, with no version bump: §13 records Bryan's confirmation of the label mapping (incident → bug, "bug is fine") and drops its open question. BEH-12 is unchanged | §13 |
