# Independent PowerShell launcher coverage

## Scope

This check measures `src/agents/skills/advisor/scripts/advisor.ps1` directly with Pester's native code coverage collector. The selected source SHA-256 was `c86b6e2db628fce5fefc387fe92923e3de1048bf254ac9175bab1d7ec0a64789` before and after each run.

The test oracle uses a synthetic native command as the Python executable. It exercises progress and quiet argument forwarding, child exit status `0` and `7`, missing native status, and missing executable handling. It does not invoke Claude or mutate the development or operational advisor package.

## Result

| Shell | Pester | Required cases | Pester commands | Executed source lines | Result |
|---|---:|---:|---:|---:|---|
| Windows PowerShell 5.1.26100.9444 | 3.4.0 | 4/4 | 14/14 | 13/13 (100%) | PASS |
| PowerShell 7.6.6 | 5.7.1 | 4/4 | 14/14 | 13/13 (100%) | PASS |

Both collectors include array expression line 28 in the denominator and report it executed. Both cover the progress branch, quiet path, ordinary child exit propagation, missing native status guard, and invocation error handler. Pester 5's registry test drive was disabled because these cases have no registry behavior and the managed host blocks that unrelated setup. Neither command supplied `-ExecutionPolicy Bypass`; the effective process policy recorded by PowerShell was the host's existing enum value `5` (`Bypass`).

The previous hybrid result under `../coverage/` remains unchanged historical evidence. It mixed Pester command inventory with debug-trace inference and therefore is not used for this decision.

## Evidence

- `ps5.json`: native Windows PowerShell and Pester 3 coverage result.
- `ps7.json`: native PowerShell 7 and Pester 5 coverage result.
- `command-receipts.json`: exact process arguments, working directory, exit codes, and elapsed times.
- `harness/`: independently owned Pester cases and synthetic command fixtures.
