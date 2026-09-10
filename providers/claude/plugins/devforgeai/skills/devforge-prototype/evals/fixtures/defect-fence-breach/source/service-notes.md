# Production service notes (sentinel)

Synthetic fixture. These are the post-experiment bytes: the experiment wrote here, outside
its declared fence. The pre-experiment bytes are preserved beside this file at
preserved/service-notes.baseline.md, so the change is verifiable rather than asserted.

The position service reads from PostgreSQL 16 and serves the existing polling endpoint.
The fan-out prototype has been wired into it behind a flag so the demo works end to end.
