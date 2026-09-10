# Task: windows-compat-review

* Task ID: windows-compat-review
* Complexity: Level 2
* Type: simple enhancement

`init` / `prompt_text` always teach `python .summem/summem wake`. Root-wake Usage and `fold_request` `Run:` stay host-specific: bare `.summem/summem` on *nix, `python .summem/summem` on Windows. Drop quoted `sys.executable` and the Windows-only init warning.

## Test Plan (TDD)

### Behaviors to Verify

- Bootstrap wake: `prompt_text()` → contains `` `python .summem/summem wake` `` and does not contain `sys.executable` or `only work on Windows`, on either host pin.
- Init is host-agnostic: `_host_needs_interpreter` True or False → `init_text()` is the same string; recipe above `---` has no Windows warning; body after `---` is `prompt_text()`.
- POSIX Usage: `_host_needs_interpreter` False → `agent_invoke()` is `AGENT_BIN`; `how_to_text()` recipes start with `` `.summem/summem note` ``.
- Windows Usage: `_host_needs_interpreter` True → `agent_invoke()` is `python .summem/summem`; `how_to_text()` recipes use that prefix; `sys.executable` is absent.
- Windows fold: `_host_needs_interpreter` True → `fold_request` `Run:` uses `python .summem/summem nap`, not a quoted interpreter and not a leading bare `.summem/summem nap `.
- Lockstep: this repo's `AGENTS.md` prefix starts with `prompt_text()`.
- Init print: `main(['init'])` stdout equals `init_text()`.

### Test Infrastructure

- Framework: pytest via `tox -e py311`
- Test location: `tests/`
- Conventions: behavior docstrings; pin `_host_needs_interpreter`, never `os.name`
- New test files: none

## Implementation Plan

### 1. Invoke recipes — executable

- Files: `tests/test_init.py`, `tests/test_fold.py`, `summem`, `AGENTS.md`

1. Stub tests: retarget `test_agent_invoke_uses_interpreter_on_nt`, `test_how_to_text_uses_agent_invoke`, `test_init_text_windows_warning_above_fold` (host-agnostic init), keep POSIX pins; add `test_prompt_text_bootstrap_wake_is_python` if the wake line is not already asserted.
2. Stub interface: none (reuse `agent_invoke` / `prompt_text` / `init_text`).
3. Write tests and run red: Windows invoke is `python {AGENT_BIN}`; init equal under both host pins; prompt wake is `python {AGENT_BIN} wake`; fold `Run:` matches `agent_invoke()`.
4. Write code and run green: `agent_invoke()` returns `f"python {AGENT_BIN}"` when `_host_needs_interpreter()`; `prompt_text()` wake line is that portable command; `init_text()` drops the Windows wrapper. Copy `prompt_text()` onto `AGENTS.md` prefix (lockstep).

### 2. Briefing and notes — prose/policy

- Files: `memory-bank/systemPatterns.md`, `docs/notes.md`, `memory-bank/techContext.md` (only if the invoke sentence is now wrong)
- No tests: prose/policy artifact

1. systemPatterns: `prompt_text` wake is `python .summem/summem wake`; `agent_invoke()` is bare `AGENT_BIN` or `python {AGENT_BIN}`, never `sys.executable`.
2. docs/notes.md: replace the `sys.executable` / Unix-only AGENTS.md sentence; still do not advertise native Windows as a supported host.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `tests/test_init.py` lockstep and host pins
- `AGENTS.md` prefix must be copied from `prompt_text()` in the same commit

## Challenges & Mitigations

- `python .summem/summem note` contains the substring `.summem/summem note`: Windows tests that forbid a bare recipe must not use `AGENT_BIN + " note" not in text`. Assert prefix (`python {AGENT_BIN}`) or that recipes do not start with a backtick-bare bin.
- Committed `AGENTS.md` after the fold (`---` + Niko suffix) must still `startswith(prompt_text().strip())`.

## Pre-Mortem

- Bootstrap still says bare `.summem/summem wake` so Windows first-wake fails: pin the exact `` `python .summem/summem wake` `` string in `prompt_text` tests and lockstep.
- Wake on *nix starts requiring `python` and breaks shebang users: POSIX `agent_invoke()` stays `AGENT_BIN`; tests pin False.
- Plan puts `python` in Usage on POSIX: already covered by Challenge on host pin.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
