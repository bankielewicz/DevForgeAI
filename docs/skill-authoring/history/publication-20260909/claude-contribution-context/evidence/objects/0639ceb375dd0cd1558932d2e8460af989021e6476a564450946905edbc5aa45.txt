# STORY-001: Save and retrieve a note

Parent: EPIC-001. Governing architecture: ADR-001.

AC-001: save_and_list("hello") returns ["hello"].
AC-002: apostrophes and Unicode survive the round trip unchanged.

The return value is a list of strings. Tests run before implementation changes. The empty-list baseline is intentionally incomplete. This fixture uses isolated storage per call; durable storage between calls is outside this story.
