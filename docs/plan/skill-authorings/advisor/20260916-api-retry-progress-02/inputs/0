# Selected request
User supplied the proposed system/api_retry progress branch and asked for integer-only
retry counts and optional numeric status without server-controlled error text.
Assistant: "The patch is reasonable, with one adjustment: use type(value) is int so
booleans cannot appear as retry counts or status codes. Should I apply and test it in
src/agents/ only, or both development and operational copies?"
User: "src/ tree only"

Scope: implement and test the selected maintenance fix in the development advisor
package only. Preserve operational bytes and prior evidence. Update the matching
execution reference and artifact manifest. User authorization to apply and test,
plus repository mandatory TDD, takes precedence over the builder authoring-only
testing restriction for this maintenance task. Independent skill validation remains
separate and unperformed; do not invoke Claude or install the changed package.

Requirements:
R1: system/api_retry emits retry A/M when attempt and max_retries are actual integers.
R2: append status S only when error_status is an actual integer; bool is not an integer here.
R3: ignore malformed count fields; never emit error text, arbitrary fields, or terminal escapes.
R4: preserve raw evidence, result interpretation, limits, authentication, and existing progress.
