# Supplemental adaptive observations

Sibling of the schema-1 run `20260917T152344959349Z`, kept outside that run root because
`adaptive_observe.py` records belong to the adaptive record family, not to schema-1.

`adaptive-package.json` is the unmodified raw stdout of:

    python3 -B -X utf8 <validator>/scripts/adaptive_observe.py package \
      --source <run>/source

These are helper-local observations. They are wrapped by the separate run-bound checks in
`../20260917T152344959349Z/checks.jsonl` and were never rewritten into authored execution evidence.
The target declares no adaptive descriptor and requires no operational binding, so the AV catalog's
adaptive-only rules are recorded NOT_APPLICABLE in the schema-1 run with that justification.
