"""Makes src/tests/context a package, so pytest imports its test_structure.py as context.test_structure
and it doesn't clash with src/tests/prd/test_structure.py (SPEC-011 names both files)."""
