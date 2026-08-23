# Task: agpl-carve-outs

* Task ID: agpl-carve-outs
* Complexity: Level 3
* Type: enhancement

Two AGPL carve-outs (obligation-free prompt text; full permission for AI-agent invocation) with the script as the authoritative source.

## Component Analysis

### Affected Components
- `summem` header: AGPL short notice today → must carry the full grant (AGPL + both carve-outs)
- `prompt_text()` / `init` / `docs/agents-prompt.md`: baked paste-this prompt, lockstep → relicensed / dedicated so a paste carries no obligation
- `LICENSE`: full AGPL text; GitHub detection target → keep, replace with `COPYING`, or drop if REUSE
- `README.md` License section: points at `LICENSE` → must not outrank the script
- `surgery.py` header: same AGPL short notice; emergency tool, not the shipped CLI → whether it echoes the carve-outs is a placement question
- `summem version`: prints `__version__` only → Claude thread suggested printing the notice; not required by the brief

### Cross-Module Dependencies
- `init` prints `prompt_text()`; `docs/agents-prompt.md` must stay lockstep (`tests/test_init.py`)
- Consumers typically copy only `summem` into `.summem/summem`; repo-root files do not travel
- GitHub / SCA read `LICENSE` and SPDX on the script; a `LicenseRef-` exception would hide AGPL

### Boundary Changes
- Legal public interface of the program (what a recipient may do) changes; CLI behavior need not
- Possible `version` output change if Creative chooses to print the notice
- Possible rename `LICENSE` → `COPYING` if REUSE is adopted

## Open Questions

- [x] **Legal instruments** — How do we write the prompt dedication and the invocation permission so they are real grants, the program stays AGPL, and scanners still see AGPL?
  - Resolved: AGPL §7 additional permissions in the source (prompt = part-of-program, no-copyright + unrestricted copy; invocation = running only, including “even if”). No dual-license, no SPDX `WITH` exception. See `memory-bank/active/creative/creative-legal-instruments.md`.

- [x] **Authority and echoes** — Given the instruments, where does the text live so a script-only install is complete?
  - Resolved: script-complete, no REUSE. Full §7 text in the `summem` header; `LICENSE` stays verbatim AGPL; README premise + pointer; `surgery.py` echoes invocation only. No `COPYING` / `LICENSING.md` / REUSE. See `memory-bank/active/creative/creative-authority-echoes.md`.

## Status

- [x] Component analysis complete
- [ ] Open questions resolved
- [ ] Test planning complete (TDD)
- [ ] Implementation plan complete
- [ ] Technology validation complete
- [ ] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
