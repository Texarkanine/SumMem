# Task: windows-compat

* Task ID: windows-compat
* Complexity: Level 2
* Type: simple enhancement

Minimal internals port so native Windows can launch and run, following [`memory-bank/archive/enhancements/20260909-windows-compat-audit.md`](../archive/enhancements/20260909-windows-compat-audit.md). Branch on capability (directory flock, else runtime-dir file lock; `fcntl` if present else `msvcrt`). Do not advertise Windows. Stock `prompt_text()` / `AGENTS.md` stay Unix. Item 3 (this-repo git symlink) remains won’t-do.


## Test Plan (TDD)

### Behaviors to Verify

- CRLF note digest: `note_digest(b"hello\r\n")` and `note_digest(b"hello\r")` → same hex as `hashlib.sha256(b"hello\n")`; LF input is unchanged (`sha256` of those bytes)
- CRLF tree parse: `loads_tree` of canonical JSON with `\r\n` line endings → same `Tree` as LF bytes from `dumps_tree`
- CRLF caption: `_nap_caption` / `list_view` on a `.summ` or note file whose bytes are `hello\r\n` → caption `hello` (no CR)
- CRLF pair identity: `variant_tag` of CRLF tree/caption bytes → same 16-hex as the LF pair
- Directory flock when it works: `with_store_lock` runs `fn`; no store path whose name contains `lock` under `.summem/` (keep existing POSIX naps/ non-blocking probe)
- Directory flock unavailable, `fcntl` still importable: `os.open` of `naps/` raises `OSError` → `fn` still runs; lock file is under the runtime lock dir, not under `.summem/`; that file is flocked (not an in-store `.lock`)
- `msvcrt` backend: with `fcntl` import forced to fail and a fake `msvcrt` in `sys.modules`, `with_store_lock` opens the runtime file in append mode (`"a"`), ensures the file contains exactly one byte before lock, calls `msvcrt.locking(fd, LK_NBLCK, 1)`, runs `fn`, then `locking(..., LK_UNLCK, 1)`. A first `OSError` from `LK_NBLCK` is retried with bounded sleep (OptMem 30s cap); it does not raise a traceback to the CLI
- CLI lock miss: `main(["note", "x"])` must not print `Traceback` or `fcntl` on stderr when the directory-flock import/open fails and the fallback is used
- Host invoke: when `os.name == "nt"`, `how_to_text()` and `fold_request` `Run:` contain quoted `sys.executable` and the driver; `prompt_text()` still contains only `AGENT_BIN`
- POSIX invoke: `how_to_text()` and `fold_request` `Run:` still use `AGENT_BIN` (existing tests)
- Init warning: when `os.name == "nt"`, `init_text()` / `main(["init"])` prints a warning **above** `---` that the printed Windows invoke instructions only work on Windows, and includes `agent_invoke()`; text after `---` is still `prompt_text()`
- Init POSIX: `init_text()` has no Windows-only warning; recipe + `---` + `prompt_text()` unchanged in shape
- Shebang: driver first line remains `#!/usr/bin/env python3`; `S_IXUSR` asserted only when `os.name != "nt"`
- Wake still does not lock: overlapping HEAD `wake` does not call `with_store_lock` (replace the module-level `fcntl.flock` counter)

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini` (`testpaths = tests`); iterate with `tox -e py311`
- Test location: `tests/`
- Conventions: `test_*.py`; session `summem` fixture from `conftest.py`; helpers in `tests/gitutil.py`; no change-detectors on docs
- New test files: none

## Implementation Plan

### 1. Canonical LF on store reads — executable

- Files: `summem`; `tests/test_codec.py`

1. Stub tests: `tests/test_codec.py` — `test_note_digest_canonicalizes_crlf`, `test_loads_tree_canonicalizes_crlf`, `test_nap_caption_canonicalizes_crlf`, `test_variant_tag_canonicalizes_crlf` (empty bodies)
2. Stub interface: `store_bytes(data: bytes) -> bytes` in `summem` (empty body / identity)
3. Write tests and run red: LF bytes keep current `sha256`; CRLF and lone CR match the LF digest/`Tree`/caption/`variant_tag`. Run `tox -e py311 -- tests/test_codec.py::test_note_digest_canonicalizes_crlf tests/test_codec.py::test_loads_tree_canonicalizes_crlf tests/test_codec.py::test_nap_caption_canonicalizes_crlf tests/test_codec.py::test_variant_tag_canonicalizes_crlf`
4. Write code and run green: `store_bytes` replaces `\r\n` then lone `\r` with `\n`. Call it at the start of `note_digest`, `loads_tree`, `variant_tag`, `_nap_caption` (after `read_bytes` / before decode), and `list_view` note reads. `leaf_digests` must canonicalize `.tree` bytes the same way (via `loads_tree` or `store_bytes` before `json.loads`). Writes (`note_file_bytes`, `_replace_bytes`) stay LF. Do not rewrite the working tree.

### 2. Store lock by capability — executable

- Files: `summem`; `tests/test_zipper.py`; `tests/test_cli.py` (only if a CLI no-traceback case lives there)

1. Stub tests: in `tests/test_zipper.py` — `test_with_store_lock_fallback_lock_is_outside_store`, `test_with_store_lock_msvcrt_locks_one_byte_and_unlocks`, `test_with_store_lock_msvcrt_retries_then_acquires`. Keep `test_with_store_lock_blocks_and_writes_no_lock_file` but stop depending on a module-level `import fcntl` for the no-lock-file half. Add `test_cli_note_lock_fallback_has_no_traceback` (CLI `note` with directory flock forced to fail still exits 0, no `Traceback` / `fcntl` on stderr). Rewrite `test_cli_wake_on_overlapping_head_writes_nothing` to wrap `with_store_lock` instead of `fcntl.flock`.
2. Stub interface: `_runtime_lock_path(store) -> Path`; `with_store_lock` still has the same signature; fallback path empty
3. Write tests and run red: existing POSIX probe still expects blocking flock of `naps/` when directory flock works; skip that probe when `fcntl` cannot be imported or `os.open` on a directory fails. Fallback test monkeypatches directory `os.open` to fail (fcntl still present), points `_runtime_lock_path` at `tmp_path`, asserts `fn` ran and `.summem/` has no `lock` file. `msvcrt` tests: hide `fcntl` (`ImportError`), install a fake `msvcrt` (`LK_NBLCK`, `LK_UNLCK`, `locking(fd, mode, n)`), point `_runtime_lock_path` at `tmp_path`. Assert the lock file was opened `"a"` (not `"w"`), `stat().st_size == 1` before the first `LK_NBLCK`, `locking` is called with `n=1`, `fn` runs, then `LK_UNLCK`. Retry test: first `LK_NBLCK` raises `OSError`, second succeeds; `time.sleep` is called with a delay ≤ 0.25s; no 30s hang. Optional: if `C:\Python313\python.exe` exists, a native CMD probe may confirm contention; skip when missing — the fake `msvcrt` is the required oracle, not that probe. Run `tox -e py311 -- tests/test_zipper.py::test_with_store_lock_blocks_and_writes_no_lock_file tests/test_zipper.py::test_with_store_lock_fallback_lock_is_outside_store tests/test_zipper.py::test_with_store_lock_msvcrt_locks_one_byte_and_unlocks tests/test_zipper.py::test_with_store_lock_msvcrt_retries_then_acquires tests/test_zipper.py::test_cli_wake_on_overlapping_head_writes_nothing`
4. Write code and run green: `with_store_lock` tries `import fcntl` and `os.open(naps/, O_RDONLY)` + `LOCK_EX`. On `ImportError` or `OSError`, open `_runtime_lock_path` with `"a"` (not `"w"`). If that file’s size is 0, write and flush exactly one byte (`b"\0"`) so a one-byte `msvcrt` lock has a defined range; do not truncate. Then `fcntl.flock` on that file if `fcntl` imported, else OptMem `msvcrt.locking` (`LK_NBLCK`, 1 byte) with spin/backoff (sleep `min(0.01 + waited * 0.2, 0.25)`, raise after 30s) and `LK_UNLCK` in `finally`. Runtime dir: `LOCALAPPDATA` if set, else `XDG_RUNTIME_DIR`, else `tempfile.gettempdir()`, then `summem/locks/<sha256 of resolved store>`. Never create a lock file under `.summem/`. Lazy-import `fcntl` / `msvcrt` / `time` only on this path so `init` / `version` / `-h` still do not import them. Raise `ValueError` without store paths if both backends fail. `surgery.py` stays a caller of `with_store_lock`.

### 3. Host invoke strings and init warning — executable

- Files: `summem`; `tests/test_init.py`; `tests/test_fold.py` (only `Run:` assertions that must follow `agent_invoke()`)

1. Stub tests: `tests/test_init.py` — `test_agent_invoke_uses_interpreter_on_nt`, `test_how_to_text_uses_agent_invoke`, `test_init_text_windows_warning_above_fold`, `test_init_text_posix_has_no_windows_warning`. In `tests/test_fold.py` — `test_fold_request_run_uses_agent_invoke` (empty).
2. Stub interface: `agent_invoke() -> str` (returns `AGENT_BIN`); `init_text` / `how_to_text` / `fold_request` still use `AGENT_BIN` until step 4
3. Write tests and run red: monkeypatch `os.name` to `"nt"`: `agent_invoke()` is quoted `sys.executable` plus quoted `AGENT_BIN`; `how_to_text()` and `fold_request` `Run:` use that string, not a bare `.summem/summem` as the command; `prompt_text()` still has `` `{AGENT_BIN}` `` and no `sys.executable`. `init_text()` warning is above `---`, states the printed instructions only work on Windows, and includes `agent_invoke()`; after `---` is `prompt_text()`. On default POSIX `os.name`, `init_text()` matches today’s recipe shape (no Windows warning). `main(["init"])` still must not import `fcntl`. Run `tox -e py311 -- tests/test_init.py tests/test_fold.py::test_fold_request_run_uses_agent_invoke tests/test_cli.py` (import-isolation cases)
4. Write code and run green: `agent_invoke()` returns `AGENT_BIN` unless `os.name == "nt"`, then `"\"{sys.executable}\" \"{AGENT_BIN}\""`. `how_to_text` and `fold_request`’s `Run:` use `agent_invoke()`. `prompt_text()` stays `AGENT_BIN`. `init_text()` prepends the Windows warning and invoke lines above `---` only when `agent_invoke() != AGENT_BIN`. Do not put `python`, `sys.executable`, or `C:\` in `prompt_text()`. This is the one host check the brief allows; do not copy `os.name == "nt"` into the lock path.

### 4. Shebang execute-bit gate — executable

- Files: `tests/test_cli.py`

1. Stub tests: change `test_shebang_and_executable_bit` to a gated execute-bit (empty/partial until filled)
2. Stub interface: none (no driver change)
3. Write tests and run red: assert shebang always; `S_IXUSR` only if `os.name != "nt"`. On this Linux host the execute-bit assertion still runs (not red unless the bit is already missing). Confirm with `tox -e py311 -- tests/test_cli.py::test_shebang_and_executable_bit`
4. Write code and run green: no `summem` change unless the test requires a comment; this unit is the test gate the audit named.

### 5. Host stance in notes and atlas — prose/policy

- Files: `docs/notes.md`; `docs/architecture/index.md`
- No tests: prose/policy artifact

1. Rewrite the `Not this host` bullet: internals holes (directory flock, CRLF-as-identity, `fcntl` traceback) are closed; still not a supported advertised host; default `AGENTS.md` stays Unix; Usage/`Run:` / init wrapper may print this host’s interpreter.
2. Atlas sentence that “may lock this machine’s naps directory”: say the mutating invocation takes a same-machine lock (directory flock of `naps/` when that capability exists, else a runtime-dir file). Still not a committed object.

### 6. Persistent memory-bank lock wording — prose/policy

- Files: `memory-bank/productContext.md`; `memory-bank/systemPatterns.md`; `memory-bank/techContext.md` (only if the shipped lock sentence is factually wrong)
- No tests: prose/policy artifact

1. Surgical edit: same-machine lock is not a committed object; POSIX may still flock `naps/`; fallback is a runtime-dir file. `fcntl`/`msvcrt` stay lazy on the lock path. Do not add a Windows support claim.

## Technology Validation

No new technology - validation not required. `fcntl` / `msvcrt` / `tempfile` are stdlib. No `portalocker`. No `.gitattributes`. No `.cmd` wrapper.

## Dependencies

- Audit spec: `memory-bank/archive/enhancements/20260909-windows-compat-audit.md`
- OptMem `locked()` mechanism (append-mode file, `fcntl` else `msvcrt` spin) as evidence, not a transplant of OptMem’s in-store `.lock`
- Existing tests: `test_with_store_lock_blocks_and_writes_no_lock_file`, `test_agents_md_starts_with_prompt_text`, `test_cli.py` import isolation (`fcntl` still command-only)

## Challenges & Mitigations

- `note_digest` docstring today is SHA-256 of file bytes: canonicalize-on-read would make CRLF hash as LF. Mitigation: keep LF hashing identical; document that store identity is LF bytes; do not rewrite files.
- `init` / `version` / `-h` must not import `fcntl` or `msvcrt`. Mitigation: `agent_invoke()` uses `os.name` only; lock imports stay inside `with_store_lock`.
- Forcing the lock fallback on Linux without a Windows runner. Mitigation: monkeypatch directory `os.open` for the `fcntl`-on-file fallback; hide `fcntl` and install a fake `msvcrt` for the byte-range backend. Native `C:\Python313\python.exe` is optional skip, not the oracle.
- `msvcrt.locking(..., 1)` on a 0-byte file has no range. Mitigation: after open `"a"`, if size is 0 write one byte; test asserts size == 1 before `LK_NBLCK`.
- Scattered `if windows`. Mitigation: one `agent_invoke()` host check; lock is try-directory-flock then file lock (`fcntl` then `msvcrt`), not `if sys.platform`.
- Existing `how_to_text` / `fold_request` tests pin `AGENT_BIN`. Mitigation: POSIX `agent_invoke()` returns `AGENT_BIN`; NT behavior is extra tests with `os.name` patched.

## Pre-Mortem

- Plan treated Windows as a second advertised product and rewrote `AGENTS.md`: already forbidden; `prompt_text()` lockstep test is the backstop.
- Lock file landed in `.summem/` “just gitignored”: already covered by Challenge (no-lock-file assertion) and product constraint.
- `msvcrt` path ships untested because Linux has `fcntl`: unit 2 now hides `fcntl` and uses a fake `msvcrt` that records open mode, one-byte lock, retry, and unlock.
- CRLF canonicalize only in `note_digest` but not captions/JSON: list_view would still show `\r`. Plan step 1 lists every read surface; Preflight should fail the unit if a read path is missing.
- `how_to_text` always prints `sys.executable`, breaking Unix Usage: already covered by Challenge (POSIX returns `AGENT_BIN`).
- Native CMD never run in this WSL session, so a quoting bug ships: add a build-phase probe with `C:\Python313\python.exe` when that interpreter exists (audit machine); if missing, rely on tests plus the audit’s quoting rule. Not a new dependency.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [ ] Build
- [ ] QA
