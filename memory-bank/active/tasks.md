# Current Task: windows-compat-review

**Complexity:** Level 1

## Fix

**What broke:** `_with_runtime_lock`'s `msvcrt` retry compared `waited += 0.01` to `30.0` while sleeping up to 0.25s, so a held lock waited ~12 minutes. POSIX-named invoke tests assumed `_host_needs_interpreter()` was false.

**Why:** The 30.0 looked like seconds; it counted spins. Invoke tests used the real host.

**What changed:** Monotonic 30s deadline, sleep clamped to the remainder, backoff unchanged. Tests pin `_host_needs_interpreter`. New timeout regression test.

**Files:** `summem`, `tests/test_zipper.py`, `tests/test_init.py`, `tests/test_fold.py`, `tests/test_scopes.py`, `tests/test_surgery.py`

## QA Result

✅ PASS

- The fallback lock now measures the 30-second retry budget with a monotonic deadline, clamps each delay to the remaining budget, and retains the established backoff behavior.
- The regression test keeps `msvcrt.locking` busy and advances a fake monotonic clock through sleeps; it verifies the expected error and a total wait no greater than 30 seconds.
- All affected bare invoke assertions pin `_host_needs_interpreter` to `False`, while the interpreter-path assertions pin it to `True`; no test monkeypatches `os.name`.
- No unnecessary abstraction, duplicate implementation, debugging residue, or missing documentation was found.
- `uvx --with tox tox -e py311` passed: 388 tests.
