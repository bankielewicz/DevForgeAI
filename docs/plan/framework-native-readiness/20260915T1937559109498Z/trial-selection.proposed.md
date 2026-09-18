# Two native trial requests — prepared, blocked, not selected for launch

The user's instruction selected readiness preparation. The exact model/effort and profile effect changes below are proposed for concrete review after their implementation/qualification. This record is not an operator approval or a command to launch the drafts.

| Field | WN-01 | WN-02 |
| --- | --- | --- |
| Scenario | complete | cancel immediately after receiving turn ID |
| Model / effort | gpt-6-astra / high | gpt-6-astra / high |
| Prompt / fixture / expected | Exact base-contract synthetic OrderDesk files, copied beside draft request | Same exact files |
| Request | trials/WN-01/request.draft.json | trials/WN-02/request.draft.json |
| Review | trials/WN-01/profile-review.unqualified.json | trials/WN-02/profile-review.unqualified.json |
| Execution | NOT_RUN | NOT_RUN |

One server/thread/turn per trial, zero automatic retries.120-second total dispatch;10-second RPC cap;5-second grace and5-second tree termination; external145-second safety cap including local finalization. Run WN-01 before WN-02; assess each result before any further launch. A safety-bound failure preserves the attempt and stops for diagnosis. WN-02 completion-before-interrupt is inconclusive; no automatic retry. User cancellation always stops owned work and preserves unfinished obligations.

WN-01 pass requires exact final JSON, no tool/delegation use, unchanged fixture and stopped process tree. WN-02 pass requires actual interrupted-turn evidence and stopped tree; exit5 alone does not suffice. Raw commands, binary/source/profile hashes, stdout/stderr, events, usage when supplied and held process-handle observations must be retained in fresh trial roots named in native-trial-inventory.json. Any unknown effects remain unresolved.

Launch blockers: identity code amendment unimplemented; versioned restrictive launch policy unimplemented/unqualified; current profile unqualified; account/model availability not observed; explicit final selection of exact qualified requests pending. Approval of these drafts alone cannot waive those prerequisites. The next user-facing execution decision must name final request/review/policy digests after they exist, not ask for blanket future permissions.

No shell command is supplied because these drafts intentionally fail native admission and a future schema2 request is required for the proposed restrictive policy. Rebuild in a new attempt after independent QA. Keep these original drafts and all prior worker evidence.
