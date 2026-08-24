---
task_id: coderabbit-wave
complexity_level: 4
date: 2026-08-24
status: completed
---

# TASK ARCHIVE: coderabbit-wave

## SUMMARY

Parent-operated L4: three parallel niko-in-worktree agents disposed of the CodeRabbit issues on [Texarkanine/SumMem](https://github.com/Texarkanine/SumMem/issues). All three landed as non-draft fixes and are on `main` (`eefd5e3`). [#42](https://github.com/Texarkanine/SumMem/pull/42) prints the 3.11 floor before `import tomllib`. [#41](https://github.com/Texarkanine/SumMem/pull/41) makes `named_ids` catch `_TREE_PARSE_ERRORS`. [#43](https://github.com/Texarkanine/SumMem/pull/43) deletes `equal_grain_pair` from `summem` and keeps the selector in `tests/test_fold.py`. After #42 merged, #41 and #43 add/add-conflicted the same 8-pack caption; the parent kept main’s wording. That is the designed store conflict: same leaf set, two captions, one id.

## REQUIREMENTS

- One worker per issue, each on its own worktree from `main` `c003779`.
- Full standalone `/niko` through a non-draft PR so CI and reviews fire.
- Close-without-PR is a success when the issue is not real or not worth fixing; parent judges.
- Parent implements no product code. Parent L4 files stay off `main` until this capstone.
- Surgical edits. Python floor stays 3.11. Suite is `tox`.

## MILESTONE LIST

Original list; none added or reordered. #39 was re-scoped after a wrong close.

1. Guard Python 3.10 at import so `require_python` can print before `tomllib` dies (#38) — estimated L1, classified L1
2. Remove unused `equal_grain_pair` from `summem`; keep the selector in `tests/test_fold.py` only (#39) — first judged close, then rework to delete from production
3. Catch `_TREE_PARSE_ERRORS` in `named_ids` so zoom does not traceback on a corrupt tree (#40) — estimated L1, classified L1

All three ran in parallel. Parent L4 preflight of this list was skipped; each worker preflighted or QA’d its own run.

## SUB-RUN SUMMARIES

### require-python (L1, PR #42, merged first)

`summem` imported `tomllib` at module load. `require_python()` ran only from `main()`. On CPython 3.10 the process died with `No module named 'tomllib'` before the floor message. The fix is three lines after `import sys` and before `import tomllib`. `require_python()` stays for the existing version-tuple tests. Docs-toolchain pins untouched. Live check: `/usr/bin/python3.10 summem version` now prints `SumMem needs Python 3.11 or newer` and exits 1. `tox` 277 on py311–py314. QA PASS. `techContext` updated.

### named-ids-tree-errors (L1, PR #41)

`named_ids` used a narrower except tuple and omitted `AttributeError`. Payload `{"c":[1]}` made `_tree_from_dict` call `.get` on an int. Existing `{not json` tests only hit `ValueError`, so they hid the gap. `named_ids` now uses `except _TREE_PARSE_ERRORS:`. Three new zoom tests. `tox` 278 on py311–py314. QA PASS (advisory: no dedicated `recall_text` non-mapping test). Gemini QA spawn hit Other Models quota; used `cursor-grok-4.6-xhigh-fast`.

### drop-equal-grain-pair (L1, PR #43)

First report was CLOSE_CANDIDATE: production never calls `equal_grain_pair`, but `tests/test_fold.py` used it as the equal-grain selector (including cases `fold_request` never emits at default budget). Parent closed #39. Operator overruled: if `fold_request` still works without the method, it is a test oracle and must not ship. The script is copied into consumer repositories. Selector moved to `tests/test_fold.py` as `_equal_grain_pair`. `fold_request` still walks adjacent `ViewNode`s itself (duplicate ids stay two rows). Operator retitled the PR `chore` → `fix` so the deletion ships in a release. `tox` 275 on py311–py314. QA PASS.

## IMPLEMENTATION

Parent stayed on `niko/coderabbit-wave` in `~/.cursor/worktrees/summem-ops-coderabbit/SumMem` and did not implement product code. Workers: `feat/require-python`, `feat/named-ids-tree-errors`, `feat/drop-equal-grain-pair`. Standing consent through QA, cleanup of `memory-bank/active/`, and a non-draft PR. After #42 merged, the parent rebased #41 and #43 and kept main’s 8-pack `.sum` caption.

## TESTING

Each sub-run: TDD, full `tox` py311–py314, Niko QA. Parent did not re-run the suite. Capstone is documentary.

## SYSTEM STATE

On `main` `eefd5e3`: import-time 3.11 gate; `named_ids` shares `_TREE_PARSE_ERRORS` with the other tree readers; `equal_grain_pair` is gone from the driver. Release Please retargeted `release-please--branches--main` after the three `fix` merges.

## CROSS-RUN INSIGHTS

The store conflict mode happened in the wild. #42 folded two x4 packs into an 8-pack. #41 and #43 each wrote a different caption for the same leaf set (same `.tree`, different `.sum`). Rebase kept main’s caption. That is the honest conflict the file backend was built for.

Parent L4 files on `main` before the children start still make workers see `milestones.md` and try to run the parent L4. This wave kept them on the ops branch until capstone.

## LESSONS LEARNED

- Prefer not to ship code that does not run in production, even if it makes testing easier. Tests do not burden consumers and may do onerous work.
- Deleting shipped production code is `fix`, not `chore`. Especially a deletion: customers get less code, and Release Please must see it.
- A close-without-PR is only right when the issue is not real. “Tests need this helper” is not a reason to keep it in the copied script.
- Same-leafset naps conflict only on the caption and are resolvable by keeping one wording.

## PROCESS IMPROVEMENTS

Tell issue-wave workers that unused production symbols go to the test file, not into a judged close. Parent should rebase sibling PRs when the first merge caption-conflicts the store.

## TECHNICAL IMPROVEMENTS

`require_python()` and the import-time gate now say the same sentence. A later cleanup could call one function before `import tomllib` if that can be done without importing `tomllib` to define it.

## NEXT STEPS

None. Worker worktrees can be removed.
