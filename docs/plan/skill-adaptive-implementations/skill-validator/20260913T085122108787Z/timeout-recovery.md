# Timeout harness recovery

The first inspected synthetic sleep attempt reached its 120-second deadline. Its process-tree termination was denied, and the runner failed while waiting for termination. Partial stdout and stderr remain under `commands/timeout-attempt-001`; no successful terminal result is inferred.

The remaining child was identified as PID 64072 with the recorded matching start time. The separately logged `Stop-Process -Id 64072 -ErrorAction Stop` exited 0. This was cleanup of that specific synthetic child.

The corrected external harness retained the second attempt independently. Its fallback killed the parent process; its reported status is `timeout-parent-killed-tree-unverified`. The test script only sleeps and launches no children, but process-tree containment is not claimed from that fact. Resume-to-completion was not exercised.

The two actual full-validator Codex CLI attempts are separate trials: each reached 120 seconds, retained partial events, and reported successful process-tree termination. Neither produced a completed native assessment.
