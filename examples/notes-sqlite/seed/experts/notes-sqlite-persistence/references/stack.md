# Selected API evidence

Target: Python 3.12 standard library. Retrieved 2026-09-04.

Source: https://docs.python.org/3.12/library/sqlite3.html

The official sqlite3 reference supports in-memory connections, parameter placeholders, executing queries, and retrieving rows. A connection context manages transactions but does not by itself close the connection; this example closes it explicitly.

Verification: the companion scripted POC exercises the supplied implementation and two behavioral cases. This reference does not claim that a terminal model has been behaviorally evaluated with this skill.
