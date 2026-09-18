# Phase 09: Package Release

## Entry Gate

```bash
devforgeai-validate phase-check ${REL_ID} --workflow=release-package --from=03 --to=09 --project-root=${PROJECT_ROOT}
```

## Contract

PURPOSE: Encode the full npm package-release sequence as a deterministic, gate-backed workflow.
DELEGATES TO: none
REQUIRED ARTIFACTS: npm registry confirms target version published at correct dist-tag
STEP COUNT: 10 mandatory steps

Variables used in this phase:
- `${REL_ID}` — the release workflow id (e.g. `REL-001`), set via `/release --package ${VERSION}`
- `${VERSION}` — the target version string (e.g. `3.0.0-beta.8`)
- `${PROJECT_ROOT}` — project root passed to every gate

---

## Mandatory Steps

### Step 9.0: Release-branch preflight

EXECUTE: Detect the default branch and verify HEAD is not on it before any file modifications. This prevents the "head == base" PR failure that occurs when the release workflow runs from the protected default branch.
```bash
# Detect the default branch — mirrors stale-main-preflight.sh pattern (lines 66-68)
DEFAULT_BRANCH="$(git -C ${PROJECT_ROOT} symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|origin/||')"
[ -z "${DEFAULT_BRANCH}" ] && DEFAULT_BRANCH="main"

# Guard: HEAD must not be the default branch
CURRENT_BRANCH="$(git -C ${PROJECT_ROOT} rev-parse --abbrev-ref HEAD)"
if [ "${CURRENT_BRANCH}" = "${DEFAULT_BRANCH}" ]; then
    echo "phase-09 HALT: HEAD is '${DEFAULT_BRANCH}' (the default branch). Run from a release branch:"
    echo "  git -C \${PROJECT_ROOT} checkout -b chore/release-v\${VERSION}"
    exit 1
fi
```
If HEAD is the default branch: HALT with exit 1 and the corrective command. Create a release branch (e.g. `git -C ${PROJECT_ROOT} checkout -b chore/release-v${VERSION}`) then re-enter phase-09.
If HEAD is already on a non-default branch (e.g. `chore/release-v${VERSION}`): proceed.
VERIFY: `git -C ${PROJECT_ROOT} rev-parse --abbrev-ref HEAD` does not equal `${DEFAULT_BRANCH}`.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.0 --project-root=${PROJECT_ROOT}`

---

### Step 9.0.5: InfoSec release-gate preflight (ADR-150)

EXECUTE: Confirm a current, clean security review exists before any packaging. Run the gate against the project root (the whole project is the review target — this is a project-level prerequisite, not a per-story check):
```bash
devforgeai-validate validate-infosec-gate --project-root=${PROJECT_ROOT}
```
Act on the exit code:
- **0 (PASS)** — a valid, current review exists with no Open Critical/High finding. Proceed.
- **2 (BLOCK)** — no review exists, the envelope is invalid, or an Open Critical/High finding is present. **HALT.** Run `/infosec` and resolve (or accept) the Critical/High findings, then re-enter phase-09. Do not package over a BLOCK.
- **3 (STALE)** — the review is clean but its `git_baseline` is not an ancestor of HEAD (the code moved since the review). Use AskUserQuestion to let the user re-run `/infosec` or confirm the review still applies:
  ```
  AskUserQuestion:
    Question: "The InfoSec review predates the current HEAD (its git_baseline is not an ancestor). Re-run /infosec, or proceed with the existing review?"
    Header: "InfoSec gate"
    Options:
      - label: "Re-run /infosec (Recommended)"
        description: "Regenerate the review against current HEAD, then re-enter phase-09."
      - label: "Proceed with existing review"
        description: "Accept the stale review and continue packaging."
  ```
VERIFY: `validate-infosec-gate` exited 0, OR exited 3 and the user chose to proceed. A BLOCK (exit 2) is never packaged.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.0.5 --project-root=${PROJECT_ROOT}`

---

### Step 9.1: CHANGELOG promotion

EXECUTE: Promote the `[Unreleased]` section to `## [${VERSION}] - <date>`, preserving the forward-looking placeholder under `[Unreleased]`.

1. **Read** `${PROJECT_ROOT}/CHANGELOG.md`.
2. **Find the `[Unreleased]` section boundary** — the content between `## [Unreleased]` and the next `## [` heading.
3. **Separate the section content** into two parts:
   - **Placeholder** — any forward-looking summary line (e.g., `` Post-`<prev>` changes accumulate here… ``). This is NOT a release change entry — it must stay under `[Unreleased]` with the version reference updated to `${VERSION}`.
   - **Change entries** — lines under `### Added`, `### Fixed`, `### Changed`, etc. These move under the new `## [${VERSION}]` heading.
4. **Replace the `[Unreleased]` section** using `Edit()`:
   - Construct the `old_string` to match `## [Unreleased]` through (but not including) the next version heading — including the placeholder line.
   - Construct the `new_string` as:
     ```
     ## [Unreleased]

     Post-`${VERSION}` changes accumulate here.

     ## [${VERSION}] - <ISO date today>

     <change entries from step 3, or empty if the section had only the placeholder>

     ```
   - The existing `## [<previous version>]` heading stays in place immediately after.
5. **Add link anchor** at the bottom of the file if the CHANGELOG uses reference links:
   `[${VERSION}]: https://github.com/<org>/<repo>/releases/tag/v${VERSION}`

VERIFY: (a) `CHANGELOG.md` contains `## [${VERSION}]` heading; (b) the placeholder text does NOT appear directly under `## [${VERSION}]`; (c) `## [Unreleased]` is immediately followed by the updated placeholder, not by the new version heading.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.1 --project-root=${PROJECT_ROOT}`

---

### Step 9.2: Version bumps + docs:cli-ref regen

EXECUTE: Bump `package.json`, `package-lock.json`, and regenerate `docs/installer/cli-reference.md`.
```bash
# Bump version in package.json (no git tag — tagging happens in Step 9.5)
cd ${PROJECT_ROOT} && npm version ${VERSION} --no-git-tag-version

# package-lock.json is updated automatically by npm version; verify
# Regenerate the cli-reference version banner
npm run docs:cli-ref
```
VERIFY: `package.json` `.version` field equals `${VERSION}`.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.2 --project-root=${PROJECT_ROOT}`

---

### Step 9.2.5: README.md version-marker sync

EXECUTE: Update README.md current-version markers to the target version. README.md ships in the npm tarball (`package.json` `files[]`) and carries hardcoded version markers (the install-command comment, the blurb, the "shipped" banner, the roadmap line, the v2-vs-v3 FAQ answer, the "Try the beta" section); without this step the published tarball's README carries the previous version (ISSUE-583).
```bash
# Derive the previous version from the last commit's package.json. Step 9.2 already
# bumped the working-tree package.json, so HEAD still carries the pre-bump version.
OLD_VERSION=$(git -C ${PROJECT_ROOT} show HEAD:package.json | python3 -c "import json,sys; print(json.load(sys.stdin)['version'])")

# Replace every occurrence of the previous version string with the target version.
sed -i "s/${OLD_VERSION}/${VERSION}/g" ${PROJECT_ROOT}/README.md
```
VERIFY: `grep -q "${VERSION}" ${PROJECT_ROOT}/README.md` exits 0 AND `grep -c "${OLD_VERSION}" ${PROJECT_ROOT}/README.md` returns 0 (no stale current-version markers remain). If a marker legitimately references an older version for historical context, scope the `sed` to the current-version lines rather than a blanket replace.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.2.5 --project-root=${PROJECT_ROOT}`

---

### Step 9.2.6: Regenerate the installer OUTPUT-screen golden

EXECUTE: Regenerate the interactive OUTPUT-screen golden after the version bump. The golden masks the version text to `<VERSION>` but keeps the original padding, so its Manifest box border sits at `68 - len(version) + 9` — a version string whose character count changed (e.g. `3.0.0-beta.9` → `3.0.0-beta.10`) shifts that border one column per character and the committed golden stops matching (ISSUE-907; observed red in PR #868 and PR #906).
```bash
UPDATE_SCREENS=1 npx jest tests/npm-package/integration/v3/interactive-output-screens.test.js
```
VERIFY: re-run WITHOUT the flag — `npx jest tests/npm-package/integration/v3/interactive-output-screens.test.js` exits 0. If `git status --porcelain tests/npm-package/snapshots/screens/` shows no change, the version width was unchanged and the regen was a no-op — that is a valid outcome, not a failure.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.2.6 --project-root=${PROJECT_ROOT}`

---

### Step 9.3: Version coherence gate

EXECUTE: Run the `verify-release-versions` gate — all 5 release files must be coherent before a PR is opened.
```bash
devforgeai-validate verify-release-versions --version=${VERSION} --project-root=${PROJECT_ROOT}
# Exit 0: all files coherent → proceed
# Exit 1: drift detected (file path(s) printed to stdout) → HALT, fix drift, rerun
# Exit 2: error (missing/malformed file) → HALT, investigate
```
VERIFY: `verify-release-versions` exits 0.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.3 --project-root=${PROJECT_ROOT}`

---

### Step 9.4: Release PR → merge

EXECUTE: Open the release PR and merge when the required check is green.
```bash
# Stage the changed files (README.md included — Step 9.2.5 synced its version markers;
# output-install.screens.txt included — Step 9.2.6 regenerated the installer OUTPUT-screen golden)
git -C ${PROJECT_ROOT} add package.json package-lock.json docs/installer/cli-reference.md CHANGELOG.md README.md tests/npm-package/snapshots/screens/output-install.screens.txt

# Commit with a conventional message
git -C ${PROJECT_ROOT} commit -m "chore(release): bump version to ${VERSION}"

# Push the release branch
git -C ${PROJECT_ROOT} push origin HEAD

# Open the PR
gh pr create --title "chore(release): ${VERSION}" \
    --body "Version bump and CHANGELOG promotion for ${VERSION}." \
    --base main

# Wait for the required check (Run Python CLI Tests) to pass, then merge
# NEVER use --auto (the repo disallows auto-merge; gh pr merge --auto fails)
gh pr merge --squash
```
VERIFY: `gh pr view --json state | jq -r '.state'` equals `MERGED`.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.4 --project-root=${PROJECT_ROOT}`

---

### Step 9.5: Tag vX.Y.Z at the merge commit

EXECUTE: Tag the merge commit and push the tag (this triggers `npm-publish.yml`).
```bash
# Fast-forward local main to origin/main after merge
git -C ${PROJECT_ROOT} fetch origin main:main

# Tag at the merge commit
git -C ${PROJECT_ROOT} tag v${VERSION} main

# Push the tag (triggers the npm-publish.yml workflow)
git -C ${PROJECT_ROOT} push origin v${VERSION}
```
VERIFY: `git -C ${PROJECT_ROOT} tag --list "v${VERSION}"` returns `v${VERSION}`.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.5 --project-root=${PROJECT_ROOT}`

---

### Step 9.6: Create GitHub Release

EXECUTE: Create the GitHub Releases page entry for `v${VERSION}`.
```bash
# Determine if this is a pre-release version (beta, rc, or alpha suffix)
# Match pattern: X.Y.Z-beta.N  |  X.Y.Z-rc.N  |  X.Y.Z-alpha.N
# Use --prerelease flag for pre-release versions; omit for stable GA.

if echo "${VERSION}" | grep -qE '^[0-9]+\.[0-9]+\.[0-9]+-(beta|rc|alpha)\.[0-9]+$'; then
    gh release create v${VERSION} \
        --title "v${VERSION}" \
        --notes "See CHANGELOG.md for details." \
        --prerelease
else
    gh release create v${VERSION} \
        --title "v${VERSION}" \
        --notes "See CHANGELOG.md for details."
fi
```
VERIFY: `gh release view v${VERSION} --json tagName | jq -r '.tagName'` equals `v${VERSION}`.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.6 --project-root=${PROJECT_ROOT}`

---

### Step 9.7: Watch the npm-publish.yml run

EXECUTE: Monitor the tag-triggered `npm-publish.yml` workflow run. It determines the dist-tag from the version string (stable → `latest`, `*-beta.*` → `beta`, `*-rc.*` → `rc`, others → `next`) and publishes to the npm registry.
```bash
# Fetch the run id for the tag-triggered workflow
gh run list --workflow=npm-publish.yml --branch=v${VERSION} --limit=1 --json databaseId,status

# Watch until completion (or timeout)
gh run watch <run-id>
```
VERIFY: `gh run view <run-id> --json conclusion | jq -r '.conclusion'` equals `success`.

IF the run **fails**: classify the failed step before routing.
```bash
# Identify the step that failed
gh run view <run-id> --json jobs --jq '.jobs[].steps[] | select(.conclusion=="failure") | .name'
```
- If the failed step is **"Run tests (authoritative subset — matches installer-testing.yml; gh#268/gh#154)"**:
  **HALT** — do NOT proceed to Step 9.8. The test suite is red; publishing over failing tests is forbidden.
  Fix the failing tests, re-create the tag (`git tag -d v${VERSION} && git push origin :refs/tags/v${VERSION}` then retag after the fix), and return to Step 9.7.
- If the failed step is **"Publish to NPM"** (authentication or registry failure):
  Proceed to Step 9.8 (manual fallback). Do NOT re-run `npm-publish.yml` directly — it may have authentication issues or other CI-environment constraints.
- If the failed step is anything else (setup, checkout, dependency install, version validation):
  **HALT** — investigate the infrastructure failure before proceeding. Do NOT route to Step 9.8.

IF the run **succeeds**: SKIP Step 9.8 and proceed directly to Step 9.9.

RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.7 --project-root=${PROJECT_ROOT}`

---

### Step 9.8: Manual-publish fallback (on CI run failure)

EXECUTE ONLY IF the `npm-publish.yml` run failed **at the "Publish to NPM" step** in Step 9.7 (authentication or registry failure). Do NOT execute if the run failed at the test step — that path is a HALT per Step 9.7.

Determine the dist-tag from the version string:
- `X.Y.Z` (stable GA) → `latest`
- `X.Y.Z-beta.N` → `beta`
- `X.Y.Z-rc.N` → `rc`
- any other pre-release → `next`

```bash
# Checkout the release tag in an isolated worktree so package.json version is confirmed
git -C ${PROJECT_ROOT} worktree add ${PROJECT_ROOT}/worktrees/publish-v${VERSION} v${VERSION}

# Publish from the tag checkout — no --provenance (CI-only flag; manual publish omits it)
# NEVER bare `npm publish` (would publish @latest even for pre-release versions)
cd ${PROJECT_ROOT}/worktrees/publish-v${VERSION}
npm publish --tag <dist-tag>

# Clean up the publish worktree
git -C ${PROJECT_ROOT} worktree remove ${PROJECT_ROOT}/worktrees/publish-v${VERSION}
```
VERIFY: Step 9.9's `npm view` gate will confirm the published version.
RECORD: `devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=9.8 --project-root=${PROJECT_ROOT}`

---

### Step 9.9: Terminal registry gate (09.REGISTRY)

EXECUTE: Confirm the target version is live in the npm registry at the correct dist-tag.
```bash
# Determine dist-tag from version pattern (same logic as Step 9.8)
DIST_TAG=<computed dist-tag>

# Query the registry
PUBLISHED=$(npm view devforgeai@${DIST_TAG} version)

# Assert equality (string comparison — no LLM judgment)
if [ "${PUBLISHED}" = "${VERSION}" ]; then
    echo "Registry confirmed: devforgeai@${DIST_TAG} = ${VERSION}"
else
    echo "REGISTRY MISMATCH: expected ${VERSION}, got ${PUBLISHED}"
    # HALT — do not call phase-record until the version is confirmed live
    exit 1
fi
```
VERIFY: `npm view devforgeai@<dist-tag> version` equals `${VERSION}` (string equality).

**ONLY after this gate exits 0**, record the terminal step:
```bash
devforgeai-validate phase-record ${REL_ID} --workflow=release-package --phase=09 --step=09.REGISTRY --project-root=${PROJECT_ROOT}
```

This `phase-record --step=09.REGISTRY` call is the terminal gate: `phase-complete --workflow=release-package --phase=09` exits non-zero until this record exists.

---

### Final Step (conditional): End-of-run framework-friction review (#620)

EXECUTE (toggle-gated, default-OFF): read the friction-reporting toggle —
`devforgeai-validate friction-config --get enabled --project-root=${PROJECT_ROOT}`. If it is not
`true`, SKIP this step (friction reporting is opt-in). When `true`, run the verbatim friction
prompt below (`${ID}` is this workflow's id — here `${REL_ID}`). Honest determinism boundary:
the `pre-friction-report-gate.sh` gate forces exactly ONE verdict artifact to exist; it does NOT
make the friction judgment deterministic — that judgment is **NOT-DETERMINISTIC** (the gate can be
satisfied with `{"friction":"none"}`). The deterministic teeth are the toggle, the gate's
force-one-emission, the enforcement-hook auto-append, and the mandatory remote dedup.

```
Role. You are the workflow orchestrator performing the end-of-run framework-friction review for DevForgeAI. Decide whether this run surfaced any framework defect or missing enforcement worth filing, and if so file it correctly and non-redundantly.
Scope. Only friction caused by the framework itself: a skill/phase/subagent that failed to guide a required action without a user reminder (e.g. not being prompted to create a worktree), a gate that fired wrongly or not at all, a phase file that contradicts a hook, prose an LLM predictably skipped, or a CLI/hook defect. Exclude: your own mistakes, the bug this run was fixing, and environment/network issues.
Inputs. (1) devforgeai/feedback/ai-analysis/${ID}/consolidated-analysis.json (captured observations). (2) Your session memory of where the workflow under- or mis-guided you.
Grounding contract. Every candidate must cite verifiable evidence: an exact file:line, the exact command/tool-call + path, and/or an exit code. No claim from memory. Drop any candidate that is not grounded. Use no aspirational language; describe only what IS broken and what WILL change.
Duplicate check (remote, mandatory). For each grounded candidate search open AND closed issues before filing: gh issue list --repo bankielewicz/DevForgeAI --state all --search "<3-5 keywords>" and gh search issues "<phrase>" --repo bankielewicz/DevForgeAI. If any result is the same defect/enhancement, do not file; record its number as the duplicate.
Decision gate. File via /create-incident ONLY when ALL hold: grounded, non-duplicate, scoped to one concrete change, non-aspirational. Otherwise do not file.
Filing. For each qualifying item: /create-incident "<one-sentence observation>" --type=<bug|enhancement> --work="<originating ID> -> <plan path> -> PR #<n>" --related="<chain>". Keep the provenance chain intact end-to-end.
Output (mandatory artifact). Write devforgeai/feedback/ai-analysis/${ID}/friction-summary.json: either {"friction":"filed","issues":[...],"duplicates_skipped":[...]} or {"friction":"none","rationale":"<one sentence>"}. The friction gate requires this artifact; the run cannot complete without it.
Few-shot (file it). "spec-sprint Phase 03 created the worktree but the phase file never told me to set CLAUDE_PROJECT_DIR, so the first gate ran against main (evidence: phase-03-worktree-materialize.md:35; gate exit 2)." -> grounded, scoped: file as bug.
Few-shot (do NOT file). "The board did not auto-update" when that IS the bug this run fixed -> exclude (own-scope). "Tests felt slow" with no file/command/exit evidence -> exclude (ungrounded).
```

VERIFY: `devforgeai/feedback/ai-analysis/${ID}/friction-summary.json` exists with one of the two
shapes — `{"friction":"filed","issues":[...],"duplicates_skipped":[...]}` or
`{"friction":"none","rationale":"..."}`. `duplicates_skipped` records any remote duplicate found by
the mandatory remote dedup probe. The `pre-friction-report-gate.sh` gate reads this artifact at the
final-phase `phase-complete`.

---

## Exit Gate

```bash
devforgeai-validate phase-complete ${REL_ID} --workflow=release-package --phase=09 --checkpoint-passed --project-root=${PROJECT_ROOT}
# Exit 0: package release complete | Exit != 0: HALT (09.REGISTRY step not yet recorded)
```
