# Task: windows-compat-audit

* Task ID: windows-compat-audit
* Complexity: Level 2
* Type: audit / recommendations (prose/policy)

Native-Windows incompatibility audit of SumMem. List every surface that will not work on Windows, with a recommended resolution and why that resolution is optimal. OptMem is evidence, not a drop-in transplant. This task does not implement the port.


## Test Plan (TDD)

### Behaviors to Verify

No new executable behavior.

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` / `tox.ini` (unused this task)
- Test location: `tests/`
- Conventions: n/a
- New test files: none

## Implementation Plan

### 1. Inventory POSIX surfaces — prose/policy — done

- Files: `summem`, `surgery.py`, `migrate.py`, `tests/`, `README.md`, `AGENTS.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

- Files: `summem`, `surgery.py`, `migrate.py`, `tests/`, `README.md`, `AGENTS.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. Scan the driver and helpers for POSIX-only APIs and invocation: `fcntl` / `with_store_lock`, `os.open` on `naps/`, shebang, `AGENT_BIN`, `git` subprocess, `Path.as_posix` vs git output, `.git` detection, `os.replace`, symlink driver, executable bit.
2. Classify each hit as product-command failure, test-only failure, or docs/invocation-only.
3. Record candidates in `memory-bank/active/windows-compat-findings.md` as an inventory draft (severity only; resolutions come in unit 4).

### 2. Probe native Windows CMD — prose/policy — done

- Files: none in-repo (read-only probes from WSL)
- No tests: prose/policy artifact

1. From WSL, invoke this machine’s Windows `cmd.exe` / `python` (operator reported 3.13). Confirm version and that it is not the WSL interpreter.
2. Probe, without needing the checkout: `import fcntl`, `os.open` on a directory, `msvcrt`, `os.replace`, UTF-8 stdio reconfigure.
3. If the Windows interpreter can see this checkout (for example `\\wsl$\…`), run `python summem version` and one mutating command against a throwaway git repo; if it cannot, record that limit and do not treat WSL success as Windows success.
4. Append probe evidence to the findings draft. Distinguish proven-on-this-machine from code-certain.

### 3. Compare OptMem fallbacks — prose/policy — done

- Files: OptMem `WINDOWS.md` and `locked()` (already fetched); SumMem `with_store_lock` and `test_with_store_lock_blocks_and_writes_no_lock_file`
- No tests: prose/policy artifact

1. Map OptMem’s Windows path (`fcntl` optional, `msvcrt` on a `.lock` file opened `"a"`, spin/backoff) onto SumMem’s contract: same-machine flock of `naps/` is not a committed object; tests assert no lock file appears.
2. Note where a naive copy would violate that contract (committed or leftover `.lock`) and where the mechanism (advisory lock + spin) is still the right idea.

### 4. Write findings with resolutions — prose/policy — done

- Files: `memory-bank/active/windows-compat-findings.md`, `docs/notes.md`
- No tests: prose/policy artifact

1. For each finding: what breaks, recommended resolution, why that resolution is optimal (name the rejected alternative).
2. Keep product-command failures separate from test-only and docs-only rows.
3. Add a short “Not this host” bullet to `docs/notes.md` stating native Windows is not yet a supported host, pointing at the archive/findings rather than restating every row. Do not change README command tables or `AGENT_BIN` in this task.

## Technology Validation

No new technology - validation not required

## Dependencies

- This machine’s native Windows Python 3.13 via `cmd.exe` from WSL
- OptMem Windows notes: https://github.com/VictorTaelin/OptMem/blob/main/WINDOWS.md
- Product constraint: no committed lock file; flock of `naps/` is same-machine only

## Challenges & Mitigations

- Windows Python may not see the WSL checkout: probe stdlib first; only attempt `summem` if a path is reachable; never infer from WSL Linux Python.
- Copying OptMem’s `.lock` file would contradict `test_with_store_lock_blocks_and_writes_no_lock_file` and product context: recommend locking a gitignored, uncommitted file or an existing directory handle, not a store object.
- `fcntl` is both a product crash (`with_store_lock` on `note`/`nap`) and a test import (`tests/test_zipper.py`): classify those rows separately so a later port does not “fix tests” by weakening the product lock.

## Pre-Mortem

- The report treats WSL as Windows and ships a false “it runs” claim: unit 2 forbids that inference.
- The report recommends OptMem’s `.lock` as a store file: unit 3 and Challenge 2 already block that; each lock finding must name a non-committed lock target.
- The report lists only `flock` and misses invocation (`AGENT_BIN` / shebang) so Windows agents still cannot start the script after a lock port: unit 1 explicitly inventories invocation and docs.
- The report invents an executable Windows port: constraint and unit 4 forbid product-code changes beyond a `docs/notes.md` gap pointer.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
