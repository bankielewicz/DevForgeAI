# Windows QA declaration, candidate 02

Retain the denominator, exclusions, native boundary and commands from qa-declaration-01.md. No runtime lines are excluded. Candidate 01 remains 1061/1299 executed lines (81.67821401077752%), below the floor, with 20/20 required cases and 11 supplemental tests passing. This is a retained failed coverage result.

Candidate 02 is the exact source/test/config inventory in 038-clippy/candidate.json, SHA-256 f0730ae498c4c3815baad07cb43235e6e15ad8319287e6828dd6d0b1a96a3089. Clippy passed with warnings denied. Changes since candidate 01: normal CLI exit for profile flushing, expanded typed-event/error/pagination/CLI tests, retained synthetic profile snapshots and unavailable-review handling, explicit known credential-store source rejection, and frozen local fixture copies. No Codex account, configuration or credential store was inspected; source-rejection tests use synthetic files only.

Required cases remain 20, all subfixtures mandatory. Supplemental tests do not enter that denominator. Coverage-02.json will capture the full all-targets Windows run, including the production watchdog. Branch coverage remains NOT_RUN under the same stable collector. WN-01/WN-02 remain NOT_RUN; protected acceptance NOT_EVALUATED.
