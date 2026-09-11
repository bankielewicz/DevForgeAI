# Defect note (synthetic)

Reported by: a surveyor, via the field support inbox
Date: 2026-09-08

> The heading on the survey export screen says "Recieved" instead of "Received".

Affected: `client/screens/export.py` line 44, a UI string.

No acceptance criterion, architecture rule, contract or expert mentions this string. It is
not referenced by STORY-031 or STORY-033.
