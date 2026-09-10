---
task_id: windows-compat-audit
complexity_level: 2
date: 2026-09-09
status: completed
---

# TASK ARCHIVE: windows-compat-audit

This archive is the decision record and spec for a later internals pass. No Windows port shipped in this task. Default prompt stays Unix. Do not advertise native Windows.

## SUMMARY

Level 2 audit of native Windows breakage, probed with `C:\Python313\python.exe` 3.13.3 and Git for Windows 2.53.0 (not WSL Python). Path resolution is fine. `note`/`nap`/surgery crash on `fcntl`. Shebang exec is WinError 193. Product stance: do not advertise Windows; a Windows-only shop may patch their `AGENTS.md` and forgo Unix. Runtime Usage/`Run:` may print `sys.executable` on `win32` (only those shops will see it). `docs/notes.md` has a “Not this host” bullet. QA PASS. No driver/test/README command-table changes.

## REQUIREMENTS

From the brief:

- List every native-Windows failure (driver, helpers, tests, invocation), not WSL-as-Linux.
- Pair each with a resolution and why that resolution beats the next-best option.
- Use OptMem’s Windows path as evidence, not a transplant (SumMem has no committed lock file).
- Probe Windows CMD on this machine.
- Do not implement the port.

Operator decisions after reflect (bind a later implementer):

- Do not advertise Windows. No language switch would have given one argv0 for `cmd.exe` and a Unix shell.
- Do not require consumer `.gitattributes` / `git config`. Canonicalize CRLF in the script.
- Punt this-repo git symlink (`.summem/summem` → `../summem`). Develop against repo-root `summem`.
- Print host-specific invoke at runtime. Stock `AGENTS.md` stays Unix.

## IMPLEMENTATION

Prose/policy only. Product code unchanged except store notes written during the audit. Pointer: `docs/notes.md` “Not this host”.

### Already fine (do not “fix”)

| Surface | Evidence |
| --- | --- |
| `python` + no-suffix driver | `python S:\…\.summem\summem version` → `0.11.0` |
| Forward vs backslash argv0 to Python | both exit 0 |
| Absolute Windows argv0 | `python S:\…\.summem\summem version` → `0.11.0` |
| `--path` | `pkg\nested`, `pkg/nested`, and absolute `S:\…` all resolve |
| Catalog / fold `--path` | Git for Windows `ls-files` uses `/`; `as_posix()` is fine; Python accepts `/` |
| `Path(parent) / ".summem"` | correct on `nt` |
| `os.replace` | OK |
| UTF-8 stdio reconfigure | OK |
| Note filenames | no `:`; `YYYYMMDDTHHMMSSZ-{hex}` |
| `version`, `init`, `wake`, `start`, `recall` | exit 0; no `with_store_lock` |
| `surgery.py --dry-run`, `migrate.py` | do not take the lock |

### Problems and resolutions

Each item is **problem → decided or recommended resolution → rejected alternatives**. Status `decided` binds a later port. `recommended` is still the intended fix unless a later task reopens it.

#### 1. `note` / `nap` / surgery crash on `fcntl` — recommended

**Problem:** `with_store_lock` does `import fcntl`, `os.open(naps/, O_RDONLY)`, `fcntl.flock`. Probe: `ModuleNotFoundError: No module named 'fcntl'` and a traceback. Even with `fcntl`, `os.open` on a directory is `PermissionError` on this Windows.

**Resolution:** One `with_store_lock`. POSIX: keep directory flock of `naps/`. Windows: lock a **file in an OS runtime directory** keyed by the resolved store path (e.g. `%LOCALAPPDATA%/summem/locks/<hex>`), opened `"a"` not `"w"`, `msvcrt.locking`, OptMem spin/backoff. Guard `import fcntl`.

**Why:** OptMem proved the mechanism. A `.summem/.lock` (even gitignored) violates `test_with_store_lock_blocks_and_writes_no_lock_file` and product context. Skipping the lock races heal. `portalocker` is a dependency the shebang does not have.

#### 2. Driver is not a Win32 executable — decided (split)

**Problem:** `cmd.exe` running `.summem/summem` is WinError 193. Python *argument* form works. There is no clone-portable command for both `cmd.exe` and a Unix shell. `.py` does not create one (`cmd` splits `.summem/summem.py` at `/`).

**Resolution:**

- Do **not** advertise Windows.
- Stock `prompt_text` / `AGENTS.md` stay Unix (`.summem/summem wake`). Do not put `python`, `sys.executable`, or `C:\…` in the committed prefix.
- Runtime `how_to_text` and `fold_request` `Run:` on `win32` print quoted `sys.executable` plus the driver file. POSIX keeps `{AGENT_BIN}`. Nobody on Windows sees those lines unless they patched the bootstrap; that is fine.
- Do not add `.py`, a store `.cmd`, or py2exe.
- README stays Unix. No Windows support paragraph.

**Why:** The advertising hole is process start plus a cloned relative path, not Python. OptMem can print `pretty(__file__)` on that machine; SumMem’s prompt is cloned. First wake is the shop’s patched `AGENTS.md`.

#### 3. Git symlink checkout — decided won’t-do

**Problem:** This repo’s `.summem/summem` is mode `120000`. Git for Windows `core.symlinks=false` checks it out as the text `../summem`.

**Resolution:** Punt. Develop on Windows against repo-root `summem`. Consumers already copy the driver. Do not spend the port on `core.symlinks` or a `.cmd` wrapper.

#### 4. CRLF vs content-addressed files — recommended

**Problem:** Notes, `.tree`, `.summ` are SHA-256 of LF bytes. Consumer `core.autocrlf=true` can check them out as CRLF. Digests and nap stems then disagree with the Unix writer.

**Resolution:** On every read of those files, canonicalize `\r\n` and lone `\r` to `\n` **before** digest, JSON parse, and caption. Writes stay LF. Do not rewrite the working tree just to strip CR. Do **not** require `.gitattributes` or `git config` in the consumer repo.

**Why:** We do not own consumer Git. Hashing raw checkout bytes is the bug. An earlier `.gitattributes` idea was rejected.

#### 5. `fcntl` ImportError is a traceback — recommended

**Problem:** Finding 1 is not `ValueError`; `main` only catches `ValueError` around `note`.

**Resolution:** Handle missing `fcntl` / directory-open inside `with_store_lock`. No traceback, no store paths. Do not say “install fcntl”.

#### Test-only — recommended (after lock helper)

| Problem | Resolution |
| --- | --- |
| `tests/test_zipper.py` module-level `import fcntl` | Tests call `with_store_lock` / a lock helper. Skip the POSIX directory-fd probe on `win32`. Keep the no-lock-file assertion. |
| `test_shebang_and_executable_bit` `S_IXUSR` | Keep the shebang assertion; gate the execute-bit on `os.name != "nt"`. |
| Mutating pytest via `note`/`nap` | Falls out of finding 1. Do not skip the suite. |
| CI `ubuntu-latest` only | Optional later `windows-latest`; not required to advertise support. |

### OptMem vs SumMem

[OptMem WINDOWS.md](https://github.com/VictorTaelin/OptMem/blob/main/WINDOWS.md): `fcntl` optional; `msvcrt` on `.lock` opened `"a"`; spin/backoff. Use that **mechanism**. Do not put the lock file in the store.

## TESTING

No new executable behavior; no pytest added (not a change-detector on this document). Native CMD probes as in IMPLEMENTATION. Preflight: PASS WITH ADVISORY (keep lock out of the store tree). `/niko-qa`: PASS. Product files `summem`, `surgery.py`, `migrate.py`, `tests/`, `README.md`, `AGENTS.md` were not edited for a port.

## LESSONS LEARNED

- Pathlib `--path` and `python C:\…\summem` were a false lead; lock and process-start are the holes.
- OptMem lock mechanism ≠ OptMem lock *target*.
- `os.open` on a directory fails on Windows even before `fcntl` is missing.
- From WSL, `cmd.exe` cannot use a UNC cwd; PATH may prefer Moba `python`. Pin `C:\Python313\python.exe`.
- Switching language would not have fixed advertising: the hole is `cmd` vs Unix exec of a cloned relative path.

## PROCESS IMPROVEMENTS

An audit that is the spec for later work should be archived at this depth, not collapsed to a few paragraphs. L2’s “brief archive” default is wrong when the brief is the deliverable.

## TECHNICAL IMPROVEMENTS

If Windows had been a host from day one: `AGENTS.md` would still not carry a pasteable Windows argv0 (clone-portable). Usage/`Run:` would print `sys.executable`. `with_store_lock` would lock a runtime-dir file on Windows (POSIX may keep directory flock). Reads would canonicalize CRLF. None of that is a support claim.

## NEXT STEPS

Later internals task, not advertised Windows support:

1. `with_store_lock` Windows branch (items 1 and 5).
2. Canonical CRLF on read (item 4).
3. Runtime invoke strings (item 2).
4. Tests follow the lock helper; shebang bit gated.
5. Item 3: won’t-do.
6. Do not change stock `AGENTS.md` into a Windows recipe.
