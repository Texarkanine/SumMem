# Active Context

## Current Task: windows-compat-review
**Phase:** BUILD - COMPLETE

## What Was Done
- `agent_invoke()` on nt is `python .summem/summem`; POSIX stays bare `AGENT_BIN`.
- `prompt_text()` wake is `python .summem/summem wake`; `init_text()` has no host wrapper.
- `AGENTS.md` prefix lockstep. Briefing: `systemPatterns.md`, `docs/notes.md`, `techContext.md`.
- `tox -e py311`: 389 passed.

## Next Step
- QA subagent, then push `windows-support`.
