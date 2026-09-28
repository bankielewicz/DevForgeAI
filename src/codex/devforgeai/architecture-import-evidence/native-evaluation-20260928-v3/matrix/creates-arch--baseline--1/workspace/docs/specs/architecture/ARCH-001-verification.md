# ARCH-001 verification record

Date: 2026-09-28. Scope: architecture documents for PRD-001, with no application code changes.

## Candidate identification

The workspace has an empty `.git` directory; `git status --short` returned exit 128, “not a git repository.” Verification therefore identifies the actual files by SHA-256, not a fabricated commit.

| File | SHA-256 |
|---|---|
| `docs/specs/prd/PRD-001.md` | `73a324099d4ea11fd4a99ab8f48f944ce36a2a0e955803de3f918bc9d5ac88ef` |
| `docs/specs/architecture/ARCH-001.md` | `f5f73f0bb7467d07116dcf76ea451aa1159bdd1cbab3d3c243c009289671df1d` |
| `docs/specs/adr/ADR-001.md` | `740c708167137222206a74069a43d581a973826cb5528a7ef5aa7224a963543b` |
| `docs/specs/adr/ADR-002.md` | `73786c4465946b61a8078242b9f82b4fee74157dcec9dc5fc17285e9e583fa91` |

## Checks and outcomes

| Check | Command / evidence | Outcome |
|---|---|---|
| Source preservation, complete requirement mapping, readiness states, runtime evidence labels, local links, requirement references and Markdown fences | `python3 /tmp/verify-prd001-architecture.py` — local document inspection script; checks all six PRD IDs occur exactly once in each architecture matrix and all design/ADR links resolve | PASS — exit 0; all three check groups passed and candidate fingerprints matched |
| Candidate fingerprints | `sha256sum docs/specs/architecture/ARCH-001.md docs/specs/adr/ADR-001.md docs/specs/adr/ADR-002.md` | PASS — matches the file identities above |
| Repository policy and required gate discovery | `rg --files --hidden --no-ignore -g '!.git/**' -g '!.agents/**' -g '!.codex/**'`, directory inspection, and ancestor instruction-file checks | PASS — initial workspace contained only PRD-001; no applicable AGENTS.md, code, test commands or validation configuration found |
| Initial document check invocation | `python -` | FAIL — `python` alias absent, exit 127; use available Python 3.12.3 via `python3` |
| Architecture coverage review | [ARCH-001 requirement matrix](ARCH-001.md) and both ADRs | PASS — all six requirements have components, decision links and verification obligations; shared constraints propagate to affected epics |
| Identity-provider resolution | [ADR-001](../adr/ADR-001.md) | BLOCKED — provider and lifecycle integration evidence absent; FR-001/NFR-001 explicitly blocked |
| Runtime acceptance, failing behavior tests, deployment and restore | No implementation or test harness in workspace | NOT_RUN — documentation-only change; planned tests are not runtime evidence |

The inspection script is a temporary verification aid, not a new repository gate. The matrices in ARCH-001 preserve requirement priorities and separate epic-definition readiness from implementation/release readiness. A-01 through A-04 and ASM-01 remain explicit refinement or rollout inputs. No unresolved decision is reported as tested software.
