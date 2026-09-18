# Root fixture attempts

`runtime-01`: Cargo completed the four test functions, three passed and RT-01 stopped in setup before invoking the runner. The safety assertion compared a resolved extended-prefix fixture path (`\\?\C:\...`) with its ordinary-prefix temporary root. This was a fixture assertion error, not a product defect or valid Red. The corrected assertion resolves the owned root and target parent before proving containment. Expected runtime behavior and all product assertions remain unchanged. The original receipt and raw streams are preserved.

`runtime-02`: all four root cases passed after the fixture containment correction. The original failure remains retained.

`runtime-03`: all five root cases passed after adding the separately declared RT-05 public review-intake case. Its four subfixtures reject missing, oversized, digest-mismatched and malformed review bytes; an explicit valid launch-policy setup check prevents earlier policy rejection from satisfying the oracle accidentally. This was characterization, not a product Red.

`integrated-format`: applied rustfmt only after all file ownership returned. The only newly changed bytes were formatting in `tests/runtime_edges.rs`. Final manifest/diff verifies that no original test or runtime behavior changed.
