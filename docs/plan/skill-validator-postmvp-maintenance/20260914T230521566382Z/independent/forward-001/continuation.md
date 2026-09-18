# Native startup continuation

Both attempt-001 trials failed before model startup on Windows with `failed to initialize in-process app-server client: Access is denied. (os error 5)`. Each exit was 1 after approximately 2.4 seconds; no synthetic-project files changed and Windows Job cleanup was VERIFIED. The 600-second trial limits were not exhausted.

Each attempt-002 is a separately sealed continuation using the exact original plan and budget, preserving attempt-001. This was required by the host instruction to request escalation after a sandbox-related failure and explicitly authorized by the parent task to use host escalation when required. Host approval was obtained independently for the exact ledger-a and ledger-b commands; no blanket sandbox bypass flag, model override, authentication change, or automatic native retry was used.

The retained evaluator snapshot, fixture skill and specification are bound as immutable input references. Actor instructions authorize generated work only inside that actor's synthetic project. The snapshot was intentionally retained while root development continued; native results apply to those captured bytes, not automatically to later development changes. Host configuration and memory remain inherited; fresh CLI sessions are procedural separation, not complete informational or operating-system isolation.
