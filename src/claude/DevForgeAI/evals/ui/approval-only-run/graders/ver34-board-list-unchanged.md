---
type: regex
target: {source: file, path: docs/specs/design/DSN-001/boards/List.dc.html}
match: contains
---
^<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>shiftlog list</title>\n</head>\n<body>\n<pre>\n\$ shiftlog list\n  DATE        START  STOP   HOURS\n  2026-10-05  09:00  17:30  8\.5\n  2026-10-06  09:00  17:00  8\.0\n</pre>\n</body>\n</html>\n$
