# Project Brief

## User Story

As an operator on a native Windows machine, I want SumMem to launch and run so that a Windows-only shop can use it after patching their bootstrap, without the driver crashing or hashing CRLF checkout bytes.

## Use-Case(s)

### Use-Case 1

An agent on Windows runs `note` / `nap` / surgery. The store lock is taken, the write completes, and the process does not traceback on a missing `fcntl` or a directory `os.open`.

### Use-Case 2

Notes, `.tree`, and `.summ` that Git checked out with CRLF still digest, parse, and caption as LF content. Writes stay LF. No consumer `.gitattributes` is required.

### Use-Case 3

On Windows, root-wake Usage and `fold_request` `Run:` print this host’s interpreter plus the driver file. Stock `AGENTS.md` / `prompt_text()` stay Unix. `summem init` prints a warning above the `---` fold that the printed Windows instructions only work on Windows.

## Requirements

1. Ship the internals port in [`memory-bank/archive/enhancements/20260909-windows-compat-audit.md`](../archive/enhancements/20260909-windows-compat-audit.md): lock (items 1 and 5), CRLF canonicalize on read (item 4), runtime invoke strings (item 2), tests that follow the lock helper and gate the shebang execute-bit.
2. Item 3 (this-repo git symlink) remains won’t-do. Develop against repo-root `summem`.
3. Branch on capability, not OS, following OptMem (`fcntl` if present, else `msvcrt` / runtime-dir lock file opened `"a"`, spin/backoff). Avoid `if (windows) else if (posix)` except where a host-specific warning truly needs the host.
4. On Windows, `summem init` prints a warning above the `---` fold that the printed instructions are for Windows and only work on Windows.
5. Do not advertise native Windows. No Windows support paragraph in the README. No `.py` suffix, store `.cmd`, or py2exe.
6. Keep the lock file out of the store tree. POSIX may keep directory flock of `naps/`.

## Constraints

1. Minimal bloat: platforms we do not expect to actually use still must not grow a second codepath for every call.
2. Stock committed prefix stays Unix (`.summem/summem`). Do not put `python`, `sys.executable`, or `C:\…` in `prompt_text()`.
3. Do not require consumer `.gitattributes` or `git config`.
4. `main` around `note` must not leak a traceback for missing `fcntl` / failed directory-open. No store paths on stderr. Do not say “install fcntl”.
5. Keep `test_with_store_lock_blocks_and_writes_no_lock_file`’s no-lock-file-in-store assertion. Do not skip the mutating suite on Windows.

## Acceptance Criteria

1. `note` / `nap` / surgery take a store lock on Windows and POSIX without crashing; no lock file appears under `.summem/`.
2. Content-addressed reads canonicalize `\r\n` and lone `\r` to `\n` before digest, JSON parse, and caption; writes remain LF.
3. On Windows, Usage and `Run:` print quoted `sys.executable` plus the driver; POSIX keeps `{AGENT_BIN}`.
4. On Windows, `summem init` warning appears above `---` and states that the printed Windows instructions only work on Windows. `prompt_text()` / stock `AGENTS.md` remain Unix.
5. Tests call the lock helper rather than importing `fcntl` at module level; shebang execute-bit is gated where the host has no execute bit. Full `tox -e py311` (then `tox run-parallel` at end-of-work) passes.
