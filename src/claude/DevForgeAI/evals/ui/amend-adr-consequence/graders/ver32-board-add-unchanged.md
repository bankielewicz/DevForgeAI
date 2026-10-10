---
type: regex
target: {source: file, path: docs/specs/design/DSN-001/boards/Add.dc.html}
match: contains
---
^<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>shiftlog add</title>\n</head>\n<body>\n<pre>\n\$ shiftlog add\nStart time \(HH:MM\)\? 09:00\nStop time \(HH:MM\)\? 17:30\nSaved a shift of 8\.5 hours\.\n</pre>\n</body>\n</html>\n$
