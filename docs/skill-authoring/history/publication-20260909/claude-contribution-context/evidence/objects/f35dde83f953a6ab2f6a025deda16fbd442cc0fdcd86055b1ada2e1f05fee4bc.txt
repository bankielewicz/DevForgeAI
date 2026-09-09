# ADR-001: SQLite persistence

For this fixture select Python 3.12 and sqlite3. Use src/store.py for persistence and tests/test_store.py for behavioral checks. The external policy is selected by the authority terminal.

Use Python's standard sqlite3 module, parameter binding, and an in-memory database for this bounded round-trip experiment. Explicitly close the connection.

These fixture choices are not a universal DevForgeAI technology stack. A persistent multi-request application would require a different storage lifetime contract.
