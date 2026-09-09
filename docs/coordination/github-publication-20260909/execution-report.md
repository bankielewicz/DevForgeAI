# GitHub publication execution

Both committed baselines, eight selected historical branch tips, the pending shared changes and four released author candidates are now recoverable from GitHub. Seven draft PRs were opened. No PR was merged and original worktrees remain unchanged.

| Repository / scope | Draft PR | Published source/evidence head |
| --- | --- | --- |
| DevForge / CLI follow-ups | https://github.com/bankielewicz/DevForge/pull/1 | `20a89ac08d3aa8178cc98326ce99e4e3ab8febf1` |
| DevForgeAI / shared foundation | https://github.com/bankielewicz/DevForgeAI/pull/1 | `1c912649e5686701e8204a22173a02c6894df707` |
| DevForgeAI / devforgeai-hooks | https://github.com/bankielewicz/DevForgeAI/pull/2 | `0ae0855d12c411751ec4ff4651be32d26d3160c8` |
| DevForgeAI / codex-brainstorm | https://github.com/bankielewicz/DevForgeAI/pull/3 | `0af2a253cd4601ebf8c5c982c5a4f6a9876225c4` |
| DevForgeAI / claude-brainstorm | https://github.com/bankielewicz/DevForgeAI/pull/4 | `ddc8298f5e81e9cfdc5b01c94d8c711fdf21f5b8` |
| DevForgeAI / codex-contribution-context | https://github.com/bankielewicz/DevForgeAI/pull/5 | `e8332a2468bf80b8f3bc27597750be248e652db7` |
| DevForgeAI / claude-contribution-context | https://github.com/bankielewicz/DevForgeAI/pull/6 | `25641dcf6a894af838cc344ec6209dacc3adfef9` |

The shared-foundation row identifies the source/evidence commit verified before this closeout-only documentation commit. PR bodies and GitHub branch refs identify the current head; this record does not include its own digest.

All five AI dependents use `publish/devforgeai-shared-foundation-20260909` as their base. Merge/reconciliation is a later owner decision. Historical archive branches preserve exact tips and do not adopt deferred runtime orchestration.

## Verification and recovery

- Fresh GitHub clones reproduced all 24 CLI changed files and 1,309 distinct AI revision/path selections, including all 312 exact released source files, complete package file sets and Git executable modes.
- Every original main/author file hash checked remained unchanged; all 24 original worktree heads are covered by published main or explicit archive refs.
- CLI formatting, Clippy, locked build, Rust tests and 621 Python tests passed. Framework and MVP checks passed for shared and candidate worktrees; hooks passed structural checks with runtime host NOT_VERIFIED.
- CLI GitHub CI failed during bubblewrap setup: `bwrap: setting up uid map: Permission denied`. Hosted Rust/Python steps were skipped. The scripted demo failed at the promoted-package manual-adoption evidence requirement. Neither failure was hidden or repaired by weakening requirements.
- Frozen evidence remains byte-identical, including whitespace and documented historical false/self-digest claims. Newly authored source/publication checks are reported separately. No native model evaluation or qualification occurred.

## Retained evidence and remaining gap

Original paths and hashes map to retained evidence under `docs/skill-authoring/history/publication-20260909/<role>/` in each AI draft branch and `docs/validation/publication-20260909/` in the CLI draft. Historical snapshot objects use inert `.txt` names; read their role evidence map to find the original named file. This avoids installing or structurally interpreting historical skill snapshots as active source.

Shared records map 92 original paths to 78 objects. Author records map 1,684 original paths to 820 retained destinations. These are explicitly selected records and named receipt dependencies, not a blanket backup of every prior campaign. Original temporary records were not deleted.

Still local-only: workspace-root guidance/research outside the repositories, installed/generated packages, unselected ignored `.poc`/`tmp` contents, WSL/Windows client conversations and settings, credentials and client databases. No private off-machine backup destination was supplied. No credential copying or session shutdown occurred. Reflog-only/deleted history was not audited.

The original shared checkouts still show their pre-existing uncommitted changes; these selected bytes are now preserved in draft PRs. Publication worktrees contain the new commits. No reset, cleanup, original-branch switch, rebase or merge was performed.

Machine-readable references and check results: [execution-results.json](execution-results.json).
