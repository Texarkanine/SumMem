# Task: prompt-membership

* Task ID: prompt-membership
* Complexity: Level 2
* Type: simple enhancement

Split the baked SumMem Register Memories paragraph in `prompt_text()` so the mandatory-note workflow and the clone-portability membership test are separate sentences. Lockstep `AGENTS.md`. No store or CLI change. Design record: `memory-bank/active/creative/creative-note-membership.md`.

## Test Plan (TDD)

### Behaviors to Verify

- Clone-portability is taught: `prompt_text()` → contains `clone` (membership test is clone-portability, not only “git forever”)
- Membership is not a trailing clause of the dump imperative: the sentence that contains `Call it whenever` → does not contain `personal` or `machine-local`; the full prompt still contains both
- Existing activation contract: `prompt_text()` → still has `.summem/summem`, `wake`, `root`, `conversation`, `contributor`, `personal`; still omits `before any other tool call` and `./summem/summem`
- Lockstep: this repo’s `AGENTS.md` → starts with `prompt_text().strip()`
- `init` still prints `prompt_text()` (existing `test_init_prints_paste_recipe_and_prompt`)

### Test Infrastructure

- Framework: pytest as configured in `pytest.ini`; suite command is `tox`
- Test location: `tests/`
- Conventions: `test_*.py`, load repo-root `summem` via `SourceFileLoader` (`conftest.load_summem`); `test_init.py` already holds prompt invariants and AGENTS.md lockstep; substring contracts, not full-prompt snapshots
- New test files: none

## Implementation Plan

### 1. Baked prompt membership — executable

- Files: `tests/test_init.py`, `summem` (`prompt_text()`), `AGENTS.md`

1. Stub tests: in `test_prompt_text_invariants` (or a sibling in the same file), add empty assertions for `clone` in `prompt_text()` and for the `Call it whenever` sentence excluding `personal` / `machine-local`.
2. Stub interface: none. `prompt_text()` already exists; do not add functions.
3. Write tests and run red: fill those assertions. Run `uvx --with tox tox -- tests/test_init.py::test_prompt_text_invariants` (or the new sibling name). Expect fail: current paragraph has no `clone`, and `Call it whenever` shares a sentence with `Personal, machine-local`.
4. Write code and run green: rewrite the Register Memories body in `prompt_text()` per the creative: workflow sentence (when to note; nap if asked can stay with workflow or after membership, but membership must be its own sentence ending on clone-portability). Do not name OptMem. Do not quote the leaked uv/rc3 line. Copy the new `prompt_text()` prefix into `AGENTS.md`. Run the init tests, then full `tox`.

## Technology Validation

No new technology - validation not required

## Dependencies

- Existing `test_agents_md_starts_with_prompt_text` (edit `prompt_text()` and `AGENTS.md` in the same build step)
- Creative decision B in `memory-bank/active/creative/creative-note-membership.md`

## Challenges & Mitigations

- Change-detector tests: do not snapshot the full paragraph. Only add substring/structure checks in the same style as today’s `personal` / `contributor` invariants.
- Overlong prompt: keep the split to a few short sentences. Do not add examples, denylists, or OptMem.
- Branch `no-local-stuff-man` vs prompttweak (#14): this task does not land #14. Do not merge or rewrite the “tool manages them” / git-add lines unless they sit inside the Register Memories sentences we must split.

## Pre-Mortem

- Tests lock exact wording and QA fails them as change-detectors: already covered by the change-detector Challenge — substring/structure only.
- Prompt gets clearer but a future spawn still says “document this machine’s gap”: accepted creative tradeoff, not a plan defect; do not add spawn-template work here.
- `AGENTS.md` below the baked block is edited by mistake and the lockstep test still passes: the test only checks the prefix; do not touch the Agent context section.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight
- [ ] Build
- [ ] QA
