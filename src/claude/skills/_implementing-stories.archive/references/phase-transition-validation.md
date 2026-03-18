# Phase Transition Validation Calls

**Source:** STORY-153
**Purpose:** CLI validation calls required at every phase transition.

See `devforgeai/config/validation-call-locations.yaml` for complete mapping.

---

## Phase-Check Calls (11 total)

| From | To | Command |
|------|-----|---------|
| 01 | 02 | `devforgeai-validate phase-check STORY-XXX --from=01 --to=02` |
| 02 | 03 | `devforgeai-validate phase-check STORY-XXX --from=02 --to=03` |
| 03 | 04 | `devforgeai-validate phase-check STORY-XXX --from=03 --to=04` |
| 04 | 4.5 | `devforgeai-validate phase-check STORY-XXX --from=04 --to=4.5` |
| 4.5 | 05 | `devforgeai-validate phase-check STORY-XXX --from=4.5 --to=05` |
| 05 | 5.5 | `devforgeai-validate phase-check STORY-XXX --from=05 --to=5.5` |
| 5.5 | 06 | `devforgeai-validate phase-check STORY-XXX --from=5.5 --to=06` |
| 06 | 07 | `devforgeai-validate phase-check STORY-XXX --from=06 --to=07` |
| 07 | 08 | `devforgeai-validate phase-check STORY-XXX --from=07 --to=08` |
| 08 | 09 | `devforgeai-validate phase-check STORY-XXX --from=08 --to=09` |
| 09 | 10 | `devforgeai-validate phase-check STORY-XXX --from=09 --to=10` |

## Phase-Complete Calls (12 total)

| Phase | Command |
|-------|---------|
| 01-10 | `devforgeai-validate phase-complete STORY-XXX --phase=NN --checkpoint-passed` |
| 4.5, 5.5 | `devforgeai-validate phase-complete STORY-XXX --phase=4.5 --checkpoint-passed` |

## Record-Subagent Calls

After each Task() invocation:
```bash
devforgeai-validate phase-record STORY-XXX --phase=NN --subagent=SUBAGENT_NAME
```
