# Pinned syntax interpretation

Source: https://spec.commonmark.org/0.31.2/#fenced-code-blocks
Version: CommonMark 0.31.2. Read-only browser-tool retrieval verified 2026-09-13, section 4.5, paragraphs corresponding to returned lines 1732-1740. This is a retained paraphrase, not a complete webpage capture or an independently executed Markdown renderer.

A fenced block ends at a fence with the same marker and sufficient marker length, optionally indented by up to three spaces. Its closing tail permits spaces and tabs only. Until that valid closure, content is literal and does not introduce resource links. A backtick opener's info string cannot contain backticks. EOF can terminate an unclosed code block; the selected project scanner may report an unresolved formatting candidate but must not invent a literal-code resource failure.
