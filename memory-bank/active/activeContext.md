# Active Context

## Current Task: windows-compat
**Phase:** BUILD - COMPLETE

## What Was Done
- Unit 1: `store_bytes` on digest, tree parse, caption, variant tag, list_view, leaf_digests.
- Unit 2: directory flock, else runtime-dir file (`fcntl` then `msvcrt`); fake-msvcrt tests; no in-store lock file; wake does not lock.
- Unit 3: `agent_invoke()` / `_host_needs_interpreter()`; Usage/`Run:` follow it; `prompt_text()` stays Unix; init warning above `---`.
- Unit 4: shebang execute-bit gated.
- Prose: notes.md, atlas lock sentence, surgical memory-bank wording.
- `tox -e py311`: 387 passed. Native `C:\Python313\python.exe` `version`, `init` warning, and `note` succeeded.

## Files modified
- `/home/mobaxterm/git/SumMem/summem`
- `/home/mobaxterm/git/SumMem/tests/test_codec.py`
- `/home/mobaxterm/git/SumMem/tests/test_zipper.py`
- `/home/mobaxterm/git/SumMem/tests/test_init.py`
- `/home/mobaxterm/git/SumMem/tests/test_fold.py`
- `/home/mobaxterm/git/SumMem/tests/test_cli.py`
- `/home/mobaxterm/git/SumMem/docs/notes.md`
- `/home/mobaxterm/git/SumMem/docs/architecture/index.md`
- `/home/mobaxterm/git/SumMem/memory-bank/productContext.md`
- `/home/mobaxterm/git/SumMem/memory-bank/systemPatterns.md`
- `/home/mobaxterm/git/SumMem/memory-bank/techContext.md`

## Key decisions
- Tests patch `_host_needs_interpreter`, not `os.name` (pathlib instantiates WindowsPath on Linux).
- Runtime lock file opened `"ab+"` (append, no truncate) so the one-byte range is binary.

## Deviations
- Plan said monkeypatch `os.name` to `"nt"`; that crashes pathlib. `_host_needs_interpreter()` is the single host check.
- Lock file mode is `"ab+"` rather than text `"a"` so `b"\0"` is one byte.

## Next Step
- QA review (subagent).
