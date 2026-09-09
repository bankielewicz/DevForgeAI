# Collision observation for CONTRIB-95 (synthetic fixture)

Recorded by the operator on 2026-04-22, at the time TARGET-AUTHORIZATION-933 was issued. This is
an observation the operator made and wrote down, not a claim this fixture makes about itself.

Inspection performed:

- Worktree listing for the repository holding candidate/: one worktree, at
  /srv/devforgeai-fixture/worktrees/contrib-95, checked out on branch author/contrib-95.
- Branch listing: no other branch points at that worktree, and no other worktree references
  author/contrib-95.
- Assignment store scan for CONTRIB-95: no session or assignment record exists, and therefore no
  competing single-writer claim exists either.
- Working tree state at observation time: clean apart from the candidate/ files themselves.

Conclusion recorded by the operator: no competing writer was observable for candidate/ at that
time. The absence of a session record is a gap in the registry, not evidence of a second writer
and not evidence of exclusive ownership on its own.
