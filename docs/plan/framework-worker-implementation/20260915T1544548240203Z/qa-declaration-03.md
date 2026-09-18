# Final Windows campaign declaration

Candidate: `046-clippy/candidate.json`, SHA256 `fa277503c85bbfd7ed2c2f1b71d99899666baa887eccd9ae57487895c261db8c`. All first-party executable lines under the package's `src/` form the executed-line denominator, including main, Windows, native adapter and failure paths. No src exclusions. Tests, deterministic peer/drivers, generated dependencies and third-party code are outside that denominator.

Run every target, every WF-01 through WF-20 test and their subfixtures, plus supplemental tests. Required-case denominator is 20, each counted once; every mandatory case must pass. Report supplemental test count separately from the actual output. Retain earlier failures without inflating the denominator with retries. Line coverage must be >=95% without rounding. Branch measurement is NOT_RUN (stable toolchain; no installation or unstable collector requested).

Campaign 042 was diagnostic and omitted the four process suite cases; it cannot qualify the package. Campaign 031 had 20 mandatory and 10 supplemental tests, correcting the earlier 31/11 prose count. Campaigns 031 and 039 passed their tests but failed line-coverage floors; their evidence is retained.

Native WN-01/WN-02 remain NOT_RUN. This is developer QA and does not close independent findings or establish framework acceptance.
