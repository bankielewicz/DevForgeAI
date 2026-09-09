# Publish DevForge and DevForgeAI to GitHub

Plan prepared 2026-09-09T12:32:56.335322+00:00. This packet contains a plan, two coordinator prompts and one separate prompt for each of the 22 existing secondary worktrees. It does not execute any push, PR, merge, installation or native evaluation. The user will send the relevant prompt to each owning session; that message grants its stated bounded publication authority.

## Outcome and current facts

Make committed source and selected pending work recoverable from the matching GitHub repositories, with draft PRs for real pending changes, preserved historical commit identities, and explicit accounting for important files that remain outside Git. No native qualification, operational installation, cleanup, release or new runtime feature is part of this task.

| Repository | Local main at planning | Target | Remote observation |
| --- | --- | --- | --- |
| DevForge | `4859a279784f902d5f9dabcb0664907b24b297a5` | https://github.com/bankielewicz/DevForge | Public; authenticated API size 0; Git advertises no refs |
| DevForgeAI | `d29430beace67a141d4d35c2beb066981060cda4` | https://github.com/bankielewicz/DevForgeAI | Public; authenticated API size 0; Git advertises no refs |

Both origin URLs are configured correctly. Authenticated repository IDs are 1357535417 and 1357534418 respectively. The prior cached web page showing a populated DevForgeAI repository is stale relative to these direct observations; do not use it as a base selection. Recheck remote identities, visibility and refs immediately before publication. No visibility change is authorized.

[inventory.json](inventory.json) records all 24 checkouts, selected HEADs, dirty/untracked paths and file hashes before this planning packet was created. The new planning folder itself is an additional uncommitted AI documentation change; the AI coordinator owns its publication. The inventory is a dated observation, not a lock that prevents an owner from completing its task.

## Sequence and ownership

1. **Send the two coordinator prompts first.** [DevForge coordinator](prompts/00-devforge-coordinator.md) and [DevForgeAI coordinator](prompts/01-devforgeai-coordinator.md) can proceed independently in their separate repositories. They alone seed their empty remote main with the selected committed baseline. They preserve existing local edits and prepare new follow-ups in fresh owned publication worktrees. They inspect the exact new public content/history before upload. No blanket git add, force push, mirror push or history replacement.
2. **Publish the shared changes once.** AI coordinator creates draft PR branch `publish/devforgeai-shared-foundation-20260909` for the pending contracts, guidance, coordination docs and this plan. It preserves the newer main revision and excludes provider candidate files and hooks. CLI coordinator creates `publish/devforge-cli-followups-20260909` for its five pending files, with logical commits and applicable checks. AI hooks use separate `publish/devforgeai-hooks-20260909` and remain unactivated.
3. **Send the four active provider prompts after the AI shared branch is published.** Their source scopes are disjoint. Base on remote main when the shared work is already merged; otherwise base the branches and DRAFT PRs on the published shared branch and link that dependency. Publication need not wait for shared-PR merge. No session is authorized to merge a PR.
4. **Send the detached-review disposition prompt.** Its old validation function and nine added test/setup definitions already match current main semantically. Preserve its pending patch/evidence, confirm the comparison, and create a minimal correction or evidence-only draft PR only if there is actually unique material. Do not overwrite newer main validation files.
5. **Preserve the eight historical branch tips; skip redundant implementation PRs.** The coordinators can handle clean historical refs and containment checks without restarting finished sessions. Send an individual historical prompt only when its owner is still active or you want that owner to supply the disposition. Their prompts use explicit `archive/20260909/<original-branch>` refs after inspecting public suitability. Ahead counts do not prove missing functionality; promoted packages selectively transcribe earlier policy, and automatic orchestration stays deferred. Nine other clean worktrees are already contained in main and ordinarily only need remote-containment verification.
6. **Verify publication and report remaining gaps.** Read back each pushed SHA and PR head/base. Verify important original commit pins remain available from retained remote refs. Clone the two published repositories into fresh disposable directories and confirm selected branches, source files and required durable evidence can be retrieved. Save concise results in the existing PR descriptions/report, not repeated self-referential commits. Do not claim that merely opening a PR proves all local files are backed up.

## Prompts to distribute first

| Session | Prompt | Owned source |
| --- | --- | --- |
| claude-brainstorm | [Copy this prompt](prompts/20-claude-brainstorm.md) | `providers/claude/plugins/devforgeai/skills/devforge-brainstorm/**` |
| claude-contribution-context | [Copy this prompt](prompts/21-claude-contribution-context.md) | `project-experts/claude/devforgeai-contribution-context/**` |
| codex-brainstorm | [Copy this prompt](prompts/22-codex-brainstorm.md) | `providers/codex/plugins/devforgeai/skills/devforge-brainstorm/**` |
| codex-contribution-context | [Copy this prompt](prompts/23-codex-contribution-context.md) | `project-experts/codex/devforgeai-contribution-context/**` |
| Detached validator review | [Copy this prompt](prompts/15-validator-runtime-review-20260905T234329495677Z.md) | Compare/preserve scripts/validate_framework.py and tests/test_validation.py; likely no implementation PR |

Copy the full text of an individual prompt file into its owning session. The prompts include the exact worktree, observed branch/HEAD, destination, ownership and stopping condition. Do not send all prompts to every session or restart finished sessions merely to create an empty PR.

## Shared-file collision resolved in the plan

All four active provider worktrees hold identical older changes to `docs/mvp/skill-authoring-contract.md` and `docs/mvp/templates/shared/handoff.md`. Main's working contract includes their substantive additions and retains newer manual-mode/local-baseline sections; its handoff matches theirs. The five contributor coordination documents also match in main and both contribution worktrees.

The AI coordinator publishes these once. Provider PRs exclude the duplicate shared paths; originals remain in their old worktrees until their owners reconcile them later. Claude and Codex contribution candidates live under separate `project-experts/claude/` and `project-experts/codex/` subtrees. Both provider hook directories are owned by shared integration, not brainstorm sessions.

## Durable evidence and temporary files

`tmp/` should be disposable after the needed records have a durable home. Do not turn the whole directory into a permanent Git archive.

- Keep authored source/specifications/tests in their canonical source paths.
- Preserve only required public-safe historical records in existing repository documentation: CLI `docs/validation/publication-20260909/<session>/`; AI `docs/skill-authoring/history/publication-20260909/<session>/`, or an already established more appropriate location. Keep the referenced files needed to reconstruct the result, not just a hash list.
- Copy frozen bytes unchanged and add a small mapping of original path, durable path and SHA-256. Update current editable entry points, not historical claims. Check referenced snapshots remain resolvable; mark any unavailable item honestly. No automatic deletion of originals is in scope.
- Exclude credentials, cached authentication, raw client-state databases and unsanitized private transcripts from these PUBLIC repositories. Preserve those privately; if no private off-machine destination exists, explicitly report the remaining gap. Do not invent one or change repository visibility.
- Disposable build outputs/caches and reproducible staging can stay temporary. New native runs are not needed to manufacture a cleaner publication record.

Workspace-root instructions/research, private evidence, ignored worktree files, installed prototype copies, WSL `/home/bryan/.codex`, `/home/bryan/.claude`, `/home/bryan/.claude.json`, and Windows `C:\\Users\\bryan\\.codex` are not automatically protected by these pushes. A separate private backup remains necessary for them. This source-publication plan does not authorize copying credentials or stopping active clients.

## Verification, PRs and stopping conditions

Follow the current target AGENTS.md. Documentation-only deltas need content/link/format checks. Executable CLI deltas need the guide's build, Rust and Python checks; preserve actual RED/GREEN history and report gaps. Skill deltas use applicable existing structural checks and source review; no new native evaluation funding or installation is implied. Reuse existing valid evidence tied to identical bytes; do not repeatedly requalify untouched work. If a required check fails, retain that result and keep the PR draft; source preservation may still finish without claiming readiness. Do not weaken a test or gate to publish.

Each PR description states the problem/resulting change, exact scope, dependency PR/base, tests actually run, unrun/failed checks, durable evidence links and current acceptance limits. Use a body file or structured API argument for real newlines. Do not solicit extra people or send external messages beyond publishing the requested branches/PRs. No auto-merge or releases.

The publication pass is complete when both committed baselines are remotely verified, genuine pending changes have their scoped draft PRs or precise dispositions, required historical refs/evidence have durable locations, and every remaining local-only item is listed. This does not require every PR to be merged, every legacy branch to become a PR, all native cases to run, or the full backup gap to be silently declared solved.

## Full worktree dispatch index

| Repository | Existing worktree | Initial disposition | Individual prompt |
| --- | --- | --- | --- |
| DevForge | `expert-foundation-gate-20260908` | Already integrated; verify remote coverage | [Prompt](prompts/10-expert-foundation-gate-20260908.md) |
| DevForge | `framework-validation-20260908` | Already integrated; verify remote coverage | [Prompt](prompts/11-framework-validation-20260908.md) |
| DevForge | `ni11-interactive-20260908` | Already integrated; verify remote coverage | [Prompt](prompts/12-ni11-interactive-20260908.md) |
| DevForge | `skill-utilities-runtime-20260907` | Already integrated; verify remote coverage | [Prompt](prompts/13-skill-utilities-runtime-20260907.md) |
| DevForge | `skill-utilities-runtime-continuation-20260907T220803638693Z` | Already integrated; verify remote coverage | [Prompt](prompts/14-skill-utilities-runtime-continuation-20260907T220803638693Z.md) |
| DevForge | `validator-runtime-review-20260905T234329495677Z` | Compare/preserve; likely no implementation PR | [Prompt](prompts/15-validator-runtime-review-20260905T234329495677Z.md) |
| DevForge | `vpi01-20260908T144631697661Z-repair-cli` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/16-vpi01-20260908T144631697661Z-repair-cli.md) |
| DevForge | `vpi01-20260908T144631697661Z-runtime-core` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/17-vpi01-20260908T144631697661Z-runtime-core.md) |
| DevForge | `vpi01-20260908T144631697661Z-runtime-schedule` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/18-vpi01-20260908T144631697661Z-runtime-schedule.md) |
| DevForgeAI | `agent-scope-lessons-20260908T151556Z` | Already integrated; verify remote coverage | [Prompt](prompts/19-agent-scope-lessons-20260908T151556Z.md) |
| DevForgeAI | `claude-brainstorm` | Active provider draft PR | [Prompt](prompts/20-claude-brainstorm.md) |
| DevForgeAI | `claude-contribution-context` | Active provider draft PR | [Prompt](prompts/21-claude-contribution-context.md) |
| DevForgeAI | `codex-brainstorm` | Active provider draft PR | [Prompt](prompts/22-codex-brainstorm.md) |
| DevForgeAI | `codex-contribution-context` | Active provider draft PR | [Prompt](prompts/23-codex-contribution-context.md) |
| DevForgeAI | `concise-handoffs-20260909T032242Z` | Already integrated; verify remote coverage | [Prompt](prompts/24-concise-handoffs-20260909T032242Z.md) |
| DevForgeAI | `expert-foundation-20260908` | Already integrated; verify remote coverage | [Prompt](prompts/25-expert-foundation-20260908.md) |
| DevForgeAI | `skill-builder-runtime-alignment-20260907` | Already integrated; verify remote coverage | [Prompt](prompts/26-skill-builder-runtime-alignment-20260907.md) |
| DevForgeAI | `skill-validation-policy-20260908T114822309238Z` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/27-skill-validation-policy-20260908T114822309238Z.md) |
| DevForgeAI | `vpi01-20260908T144631697661Z-builder` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/28-vpi01-20260908T144631697661Z-builder.md) |
| DevForgeAI | `vpi01-20260908T144631697661Z-contracts` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/29-vpi01-20260908T144631697661Z-contracts.md) |
| DevForgeAI | `vpi01-20260908T144631697661Z-repair-ai` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/30-vpi01-20260908T144631697661Z-repair-ai.md) |
| DevForgeAI | `vpi01-20260908T144631697661Z-validator` | Historical branch preservation; no automatic implementation PR | [Prompt](prompts/31-vpi01-20260908T144631697661Z-validator.md) |

## Source notes

- Current filesystem/Git inspection and authenticated GitHub repository metadata, captured in inventory.json. No stash/tag refs currently exist; the single detached worktree HEAD is already reachable from named branches. Deleted branches/reflog-only objects were not audited.
- [GitHub: creating a PR](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request): PRs compare different branches and may use a selected base, including draft PRs.
- [Git bundle](https://git-scm.com/docs/git-bundle): an optional private Git-history archive can preserve refs, but does not include uncommitted working files. It is not a substitute for a workspace/session backup.

Preparation checks: all 24 prompts have unique addressed assignments; all 30 local document links resolved; JSON, Markdown fences and whitespace checks passed. A bounded independent review found no blockers. Its evidence-routing advisory was incorporated into the archive prompts. Git HEADs and all recorded pre-existing working-file hashes remained unchanged. No source tests, commits, pushes, PRs or native runs were performed while preparing this packet.
