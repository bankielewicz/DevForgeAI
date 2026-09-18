# Retained assembly failure

Command: `python -B -X utf8 docs/plan/skill-validations/dev/20260914T0704028557004Z/inputs/prepare_bundle.py`

Observed exit 1. AssertionError at the capsule's source-manifest.json: a carried DV-16 reference names the older manifest while the new run has a fresh manifest timestamp/root binding. Both describe the same package but are different raw bytes. No overwrite occurred. Partial capsule `20260914T0704028557004Z-evaluation` remains untouched.

The second assembly uses a fresh `20260914T0704028557004Z-evaluation-v2` capsule and retains historical evidence under `inputs/carried/`. Native command/plan records retain their original trial IDs and actual historical project paths. The runner and grader implementation remain byte-identical. This is evidence orchestration, not a dev-source defect or a native-case retry.
