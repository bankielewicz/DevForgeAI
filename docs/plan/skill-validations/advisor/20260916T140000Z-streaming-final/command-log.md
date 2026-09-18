# Command log

All commands ran from `C:\Projects\DevForgeAI` unless a working directory is stated. Python used `-B`, and coverage/native subprocess commands set `PYTHONDONTWRITEBYTECODE=1`. No command invoked Claude.

| Purpose | Command summary | Exit | Duration / evidence |
|---|---|---:|---|
| Authoring intake | `authoring_intake.py --request …/validation-request.json --request-sha256 e0258f…` | 0 | `authoring-intake.json` |
| Final source snapshot | `observe.py snapshot --source src/agents/skills/advisor --output …/20260916T140000Z-streaming-final` | 0 | 0.40s; `source-manifest.json` |
| Independent cases 001 | `independent_cases.py … --trial-root trials/independent-001` | 1 | 9.57s; validator CRLF oracle mismatch, retained |
| Independent cases 002 | same frozen inputs, corrected raw-byte oracle, `trials/independent-002` | 0 | 10.68s; 30/30 |
| Unit regression with coverage | `coverage run --parallel-mode -m unittest discover -s source/tests -v` | 0 | 14.12s; 81/81 |
| Deterministic evaluation with coverage | `coverage run --parallel-mode source/evals/run_evaluation.py --output evaluation` | 0 | 0.57s; 38/38 |
| Coverage execution of independent cases | `coverage run --parallel-mode independent_cases.py … trials/independent-003-coverage` | 0 | 18.04s; 30/30, denominator unchanged |
| Coverage combine/report | `coverage combine`, `coverage json`, `coverage report` from `…/coverage` | 0/0/0 | 0.77s; 604/635 lines |
| PowerShell 5.1 Pester | exact command in `coverage-independent/command-receipts.json` | 0 | 4/4 tests; 13/13 lines |
| PowerShell 7 Pester | exact command in `coverage-independent/command-receipts.json` | 0 | 4/4 tests; 13/13 lines |
| Default-policy wrapper controls | native `powershell.exe -NoProfile -File policy-control.ps1` and `pwsh.exe -NoProfile -File policy-control.ps1`; no `-ExecutionPolicy` argument | 0/0 | `policy-ps5.*`, `policy-ps7.*` |
| Structure observer | `observe.py structure --source …/source` | 0 | 14/14 emitted checks |
| Installed Skill Creator checker | `quick_validate.py …/source` | 0 | `Skill is valid!` |
| Final source readback | `observe.py readback --source src/agents/skills/advisor --manifest …/source-manifest.json` | 0 | `MATCH`, 19 files |

Historical failed or superseded validator attempts remain under the pre-change run and `coverage/`; none was deleted or counted as a final pass.
