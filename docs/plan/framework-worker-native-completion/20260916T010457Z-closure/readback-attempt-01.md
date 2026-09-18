# Root QA-seal readback setup error

Command: `C:\Program Files\Python310\python.exe -B -X utf8 docs/plan/framework-worker-native-completion/20260916T010457Z-closure/verify_qa.py 404cbff08f72b75402b4f5e11d01e032ea5b2311da006f2a114fd467f1391109`, cwd `C:\Projects\DevForgeAI`.

Native exit 1 after 2.3183974 seconds. The final QA manifest digest and root evidence entries passed before the external-fixture safety assertion stopped this read-only script. Original script retained as `verify_qa-attempt-01.py`.

Exact error:

```text
Traceback (most recent call last):
  File "C:\Projects\DevForgeAI\docs\plan\framework-worker-native-completion\20260916T010457Z-closure\verify_qa.py", line 31, in <module>
    assert path.resolve().is_relative_to(external_root) and path.parent.name.startswith('RT-source-type-')
AssertionError
```

Diagnosis: the declared external layout is `RT-source-type-<id>/fixture/task.json`; the original guard incorrectly required the immediate parent to be the trial ID rather than `fixture`. The corrected guard checks the resolved external root, exactly three relative components, the trial prefix, and the exact `fixture/task.json` suffix. Expected digests and all verification requirements are unchanged. This is a readback-helper setup error, not a product defect. No product tests were rerun and no sealed evidence was modified.
