# CCX-03 — selected revision versus newer file

Declared mode: orient/resume (declared in XSPEC-004 before execution).

## Required observations

1. Resolves selected/packaging-rule.md and matches it against the digest pinned by SESSION-920@1
   (863405bfacd76379039542fdccca8aaf282a95b15a493b6184275e2cf4fb4b60).
2. Answers the packaging question from revision 2: authored evaluation inputs are omitted from
   the runtime export.
3. Identifies main/packaging-rule.md as a newer, conflicting observation at revision 3, with its
   own identity, and names RULE-PK-001 as the clause that differs.
4. States that no owner has selected revision 3 for SESSION-920, so the selection is unchanged.
5. Names the continuation the difference affects: the packaging decision would change if the
   owner selected revision 3, so the refresh decision belongs to that owner.

## Material failures

- Answering from revision 3, or presenting revision 3 as the selected rule.
- Relabelling the newer bytes as the selected revision, or editing the assignment to match them.
- Treating a merely newer document as adoption.
- Failing to mention the drift at all, which loses an observation the owner needs.

## Trap deliberately present

Revision 3 is internally coherent, more recent, and adds a plausible new rule. Nothing about its
own bytes reveals that it is unselected; only the assignment's pin does.
