# Active Context

## Current Task: prompt-commit-notes
**Phase:** BUILD - COMPLETE (rework)

## What Was Done
- Tightened `test_prompt_text_teaches_git_publish` to assert `commit them` and `own commit` instead of a bare `commit` substring.
- `"committed AGENTS.md"` is not in `prompt_text()`; the generic `commit` assert was still too loose.
- 208 pytest passed.

## Next Step
- Rerun QA
