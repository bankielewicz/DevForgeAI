# Final expanded negative-case campaign

Selected source/test manifest: `063-clippy/candidate.json`, SHA256 `177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604`. Production src bytes are unchanged from campaign 059. Only the external peer and supplemental requirement tests changed: exact/conflicting duplicate completion observations and valid output followed by worker exit 9. Focused attempt 061 passed without runtime changes; these are added regression checks, not fabricated Red results.

Campaign 059 passed every test but covered 1305/1374 src lines (94.97816593886463%), a FAIL against the >=95% floor. Campaign 060 passed its normal suite on those same bytes. Both are retained and superseded for qualification by this candidate's full campaigns.

Run full all-target normal tests and coverage-05.json on this candidate. The declared denominator is unchanged: all first-party executable src, no runtime exclusions; tests/support, fixtures and generated/vendor dependencies excluded. Required cases are WF-01..20, once each with every subfixture mandatory. Supplemental tests are reported separately. Branch measurement NOT_RUN on this stable collector. WN-01/WN-02 NOT_RUN and protected acceptance NOT_EVALUATED.

Normal and instrumented suites may overlap in wall time using separate debug and llvm-cov-target build outputs and disjoint retained attempt fixtures. No source changes during either campaign. Final output readback must match this candidate.
