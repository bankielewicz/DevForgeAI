# ADR-001: JSON file persistence

For this fixture select Python 3.12 and json-file. Use src/store.py for persistence and tests/test_store.py for behavioral checks. The external policy is selected by the authority terminal.

Use the standard json module and an isolated temporary UTF-8 file for this bounded round-trip experiment. Do not import another project's SQLite or ORM rules.

These fixture choices are not a universal DevForgeAI technology stack. A persistent multi-request application would require a different storage lifetime contract.
