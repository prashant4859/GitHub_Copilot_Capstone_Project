---
applyTo: "docs/sdlc/**/*.md"
---

# SDLC Documentation Rules

All SDLC artifacts must be written in clear Markdown.

Requirements must be:

- atomic
- unambiguous
- testable
- traceable
- implementation-neutral unless a technology is explicitly mandated
- uniquely identified

Avoid vague words unless they are quantified or clarified, including:

- fast
- user-friendly
- scalable
- secure
- easy
- quickly
- efficient
- appropriate
- sufficient
- seamless

For example, do not write:

"The API should respond quickly."

Prefer:

"NFR-004: For 95% of requests under the defined normal load, the API response time must be less than 2 seconds."

Do not fabricate numerical targets. If the source does not provide the target, create a clarification question.

Never remove unresolved questions from an artifact.

Never mark unresolved blocking questions as assumptions simply to complete the document.

Every finalized functional requirement must have at least one verification method or acceptance criterion.

Every requirement must be traceable to one of:

- original user story
- source acceptance criterion
- explicit user clarification
- explicitly approved assumption