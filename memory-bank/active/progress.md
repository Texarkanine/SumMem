# Progress

Implement ingest: Python 3 CLI, git-root store auto-create, `note` and wait-free `wake` of loose notes, first proof 1, freeze store layout and leaf-set hashing.

**Complexity:** Level 3

## 2026-08-18 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified L4 `file-backend` milestone 1 (ingest) as Level 3
    - Scoped `projectbrief.md` to ingest; left `milestones.md` and later proofs to later sub-runs
    - Cleared the L4 `.preflight-status` so it cannot gate this sub-run's build
* Decisions made
    - Level 3, not Level 4: multiple components (package, CLI, store I/O, worktree proof, identity codec) under an architecture already settled in `VISION.md`
    - Format freezes (`.tree` bytes, hash join, wake print, package layout) belong in this plan, not a creative rediscovery of whether notes are files
* Insights
    - L4 preflight advisory still applies: failing compatibility-vector tests before the codec
    - Default `python3` on this machine is 3.10; the floor is 3.11 (`python3.11` via pyenv) because `tomllib` is stdlib there

## 2026-08-18 - PLAN - COMPLETE

* Work completed
    - Wrote the L3 ingest plan in `tasks.md` with TDD-ordered units: codec, store, wake, CLI, proof 1
    - Validated hatchling + pytest under `uv run --python 3.11` in a throwaway package
* Decisions made
    - No creative phase: `VISION.md` already settled architecture; remaining format choices are pinned in the plan
    - Leaf-set join is concatenation of sorted lowercase hex with no delimiter
    - `.tree` is canonical JSON (`sort_keys`, no extra spaces, `ensure_ascii=False`, trailing newline) with note and nested nap children
    - Wake prints the full 64-hex content id
    - Tests run through `uv run --python 3.11`; do not use the bare `python3.11` pyenv shim
* Insights
    - Nested nap vectors belong in ingest even though this milestone does not write naps, or Phase 2 will invent a second identity

## 2026-08-18 - PREFLIGHT - COMPLETE

* Work completed
    - Validated implementation plan against codebase reality
    - Confirmed TDD encoding for all executable units
    - Verified convention compliance and completeness
    - Wrote `.preflight-status` to PASS
* Decisions made
    - No radical innovation required; the plan is extremely thorough and aligns with `VISION.md`
* Insights
    - The plan correctly uses `tmp_path` and `monkeypatch.chdir` for tests to avoid adding test-only flags to the CLI

## 2026-08-18 - REPLAN - INITIATED

* Work completed
    - Operator rejected the hatchling package plan and invoked `/niko-plan`
    - Cleared `.preflight-status` so the old PASS cannot gate build
    - Rewrote `projectbrief.md` around a shebang driver at `.summem/summem`
* Decisions made
    - Product is one shebang script, not a package
    - `.summem/` is the brand; the driver lives at `.summem/summem`
    - Clock is `datetime.now(timezone.utc)`; `Z` without UTC is a defect
    - Tests stay outside the script
* Insights
    - OptMem already keeps `memo` inside `.optmem/`, not at `$HOME/memo`. The earlier "put it at repo root" recommendation was a misread of that layout

## 2026-08-18 - PLAN - COMPLETE

* Work completed
    - Rewrote the L3 ingest plan around `.summem/summem` as the only product file
    - Validated shebang + pytest load via `SourceFileLoader` in a throwaway tree
* Decisions made
    - No creative phase: operator already chose the brand path
    - `spec_from_file_location` is unusable on a no-suffix file; tests use `SourceFileLoader` + `exec_module`
    - Auto-create copies the running file into `.summem/summem` only when missing
    - Process tests invoke `sys.executable` so this machine's `python3` 3.10 is not the runner
    - `VISION.md` / `ROADMAP.md` invocation lines update to `.summem/summem` as prose/policy
* Insights
    - `.summem/summem` is the tool path, like `~/.optmem/memo`. `notes/` and `naps/` remain the store files agents must not be told to edit
