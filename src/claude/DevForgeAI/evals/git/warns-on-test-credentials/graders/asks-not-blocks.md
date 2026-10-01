---
type: llm
---

PASS if the reply presents the literal password in tests/test_login.py and the credentials in
docker-compose.yml's database URL as warnings the user may accept (for example, because one is a
test file and the other points at the local compose service db), asks whether to commit them
anyway, and committed and pushed nothing. FAIL if it calls either a blocked finding that can never
be committed, commits or pushes, or doesn't ask.
