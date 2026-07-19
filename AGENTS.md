<!-- Shared guidance from fezzlk/agent-kit @ 1089cb3036e50c7d354c63dbc3c7236321feb6f7. Project-specific guidance follows. -->

# Shared AI development guidance

- Keep changes small, preserve existing user work, and run appropriate verification.
- Do not expose secrets or commit environment values.
- Before cloud or paid API changes, state the likely cost and impact.
- pico is the long-term memory: read its project context and decisions when needed; record completed facts and decisions only when asked.
- Linear is the only source of task status, priority, owner, due date, and next actions. Do not duplicate them here or in pico.
- For AI features, add versioned evaluation cases, expected behavior, and failure handling before expanding scope.

## Project-specific guidance

Add repository-specific commands, architecture constraints, and verification steps here.
