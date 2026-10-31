# Task: read-once

* Task ID: read-once
* Complexity: Level 2
* Type: performance enhancement (rework of PR #95)

`note` and `nap` read and digest each nap children file (`.tree`) at most once per command. Heal, the fold scan, and `nap` share one parse: `_as_child`'s, the same parse whose refusals decide what `nap` can fold (#88). While `with_store_lock` holds the lock, `_as_child` remembers each children-file path it has parsed. Outside the lock nothing is remembered. Heal's `leaf_digests` reads through `_as_child`, so the raw-JSON walk `_digests_of_dict` goes away.

## Measurements

Scratch store `/tmp/summem-bench` (script `bench.py`, outside the repo): 11 naps of grain 2048 down to 2 (4094 leaves, 901 KiB of `.tree`), then 23 loose notes = 34 rows, over `WAKE_LINES` 32. `nap` names the pair `fold_request` asks for, so its own follow-up request also scans. `.tree` reads and `note_digest` calls are counted in-process. Time is the median of 15 runs on a fresh copy each run. "in-process" is `main()` work only. "subprocess" includes interpreter startup (`version` is about 66 ms) and is interleaved across drivers to cancel drift.

| Driver | `note` .tree reads | `note` digests | `note` in-process | `note` subprocess | `nap` .tree reads | `nap` digests | `nap` in-process | `nap` subprocess |
|---|---|---|---|---|---|---|---|---|
| origin/main 060f078 | 22 | 4142 | 61.5 ms | 144 ms | 34 | 4163 | 79.3 ms | 171 ms |
| dd16eac (PR #95 head) | 22 | 8236 | 63.1 ms | 165 ms | 34 | 12353 | 97.3 ms | 185 ms |
| prototype (path cache) | 11 | 4142 | 42.1 ms | 159 ms | 12 | 4165 | 41.9 ms | 161 ms |

The prototype was a process-wide path cache. It halves reads and JSON decodes, and the profiler shows 22 to 11 `raw_decode` calls with `note` work dropping from 175 to 124 ms under profile. Its fresh-subprocess `note` gain is smaller and noisy at this scale. The prototype broke 10 tests: nine read a `.tree` or `.summ`, edit it in place, and read again through direct calls, so a cache that outlives one command is stale. The tenth pinned heal's raw-JSON walk. The plan therefore scopes the cache to the store lock. Re-measure after build.

## Test Plan (TDD)

### Behaviors to Verify

- Contract: one mutating command reads each children file at most once. The driver runs inside agent turns, so a second parse of the same `.tree` is pure waste.
  - `note` on a store over the wake budget, with naps, one broken `.tree`, and a loose note that heal must drop (a relist) → every `.tree` path is read at most once. A fold request is still printed.
  - `nap` that leaves the store over budget → every `.tree` path, including the one it writes, is read at most once. Its follow-up fold request is still printed.
- Edge: outside a command, direct calls still see in-place edits. Existing tests already cover this, for example `test_leaf_digests_none_when_tree_missing_or_malformed`, `test_heal_malformed_overlapping_nap_skipped`, and `test_fold_request_skips_a_pack_whose_*`. These went red under the process-wide prototype and must stay green.
- Edge: a broken or unreadable children file is still grain 0, heal still skips it, and `_as_child` still raises `ValueError("unreadable pack")` or `ValueError("unknown id")` as before. Existing tests in `test_fold.py`, `test_nap.py`, and `test_zipper.py` cover this.
- Regression: `leaf_digests` of a note, a nap, a missing or malformed tree, and identical notes are unchanged. The existing `test_leaf_digests_*` tests cover these.

### Test Infrastructure

- Framework: pytest under tox (`tox -e py311`), with xdist.
- Test location: `tests/`. Zipper and heal tests live in `tests/test_zipper.py`, next to the existing "does no extra work" CLI contracts (`test_cli_note_lists_once_when_disjoint`, `test_write_nap_reuses_nodes`).
- Conventions: `summem` fixture, `init_repo`, `_write_notes`, `monkeypatch` spies on `Path.read_bytes` (precedent in `test_fold.py`), `WAKE_LINES` set through `.summem/config.toml`.
- New test files: none.

## Implementation Plan

### 1. Read each children file once per locked command — executable

- Files: `summem`, `tests/test_zipper.py`

1. Stub tests: in `tests/test_zipper.py` add `test_cli_note_reads_each_children_file_once` and `test_cli_nap_reads_each_children_file_once`, with empty bodies and docstrings that name the contract. Delete `test_leaf_digests_nap_does_not_build_tree`, because heal now shares nap's parse on purpose.
2. Stub interface: none. No new public function, and no signature changes. The new private module state is `_CHILDREN` (`None` outside the lock).
3. Write tests and run red. Spy `Path.read_bytes` and count `.tree` paths in a `Counter`.
   - The note test builds a grain-4 nap (A–D), a grain-2 nap (E, F), and a grain-2 nap whose `.tree` is overwritten with `{not json`. It writes a loose note whose text is already inside a nap, so heal drops it and relists. It adds loose notes, sets `WAKE_LINES = 2`, runs `main(["note", ...])`, and asserts rc 0, a `Run:` line in the output, and `max(counts.values()) == 1`.
   - The nap test uses the same kind of store over budget and naps the requested pair. It asserts rc 0, a follow-up `Run:` line, and that no `.tree` path is read twice.
   - Run `tox -e py311 -- tests/test_zipper.py` and expect both tests red at dd16eac.
4. Write code and run green in `summem`.
   - Add `_CHILDREN: dict | None = None` right after `_TREE_PARSE_ERRORS`.
   - `with_store_lock`: `global _CHILDREN`, then `_CHILDREN = {}`, then `try:` around the existing body and `finally: _CHILDREN = None`. Add one docstring line saying that under the lock a nap path names fixed bytes, so `_as_child` parses each children file once.
   - `_as_child`: nap branch. Use `cache = {} if _CHILDREN is None else _CHILDREN`, keyed on `tree_path`. On a miss, parse and digest inside the existing `try`, storing `(inner Tree, digests)`, or storing `None` on `_TREE_PARSE_ERRORS`, which already includes `_digests_of_tree`'s `ValueError`. Raise `ValueError("unreadable pack")` on `None`. Otherwise build `NapChild(id=node.id, sum=node.caption, tree=inner)` from the current node on every call, so captions are never cached (preflight finding 1). The `is_file()` "unknown id" check stays ahead of the cache, so an unlinked nap is never served from it.
   - `_replace_bytes` (the only store writer): drop `dest` from the cache, as one line `(_CHILDREN or {}).pop(dest, None)`. A file this process writes is never served stale: a heal-repaired `.tree` or a write over a lying stem is parsed fresh (preflight finding 2 and its advisory).
   - `leaf_digests`: `try: return set(_as_child(node)[1])` with `except (OSError, ValueError): return None`.
   - Delete `_digests_of_dict`; it has no other callers.
   - Run the file, then the full `tox -e py311`.

### 2. Architecture note — prose/policy

- Files: `docs/architecture/index.md`
- No tests: prose/policy artifact

1. In the lock paragraph (near "That invocation takes a same-machine lock"), add one sentence: under that lock each nap's children file is parsed once, and heal, fold, and `nap` share the result.

### 3. SumMem note — prose/policy

- Files: `.summem/notes/*` (written by the driver)
- No tests: prose/policy artifact

1. `python .summem/summem note "…"`: the driver is pasted into every consumer repo and runs in agent turns, so use fewest lines and do no more work than the outcome needs. If it asks for a nap, do the nap. Commit the written files with the work.

### 4. Re-measure

1. Run `/tmp/summem-bench/bench.py` with `main`, `dd16eac`, and the built driver. Record the numbers in `progress.md`, along with the net `summem` line delta (`git diff --numstat dd16eac -- summem`).

## Technology Validation

No new technology - validation not required. `global` and a module dict are stdlib Python; no import is added.

## Dependencies

- `tox` via `uvx --with tox`; Python 3.11 for the py311 env.

## Challenges & Mitigations

- Stale reads across commands in one process (tests run many commands in one pytest worker): the cache exists only inside `with_store_lock`, and `finally` resets it. Direct calls outside the lock parse fresh, as before.
- Captions: heal can write a missing `.summ` under the lock (`rematerialize_child` writes the pair unless both exist). The cache therefore holds only what the `.tree` yields, and `NapChild` takes `node.caption` from the current listing on every call.
- Driver writes under the lock (heal rematerialize, `write_nap`, `write_note`) all go through `_replace_bytes`, which drops the path from the cache. A repaired broken `.tree` and a write over a lying stem are both parsed fresh. `is_file()` runs before the cache, so an unlinked nap is not served.
- `surgery.py` runs `excise_note` under `with_store_lock`, so it gets the cache too. Its `fold_request` runs after the lock and parses fresh. `tests/test_surgery.py` covers it in the full py311 run.
- `_CHILDREN` and `global` are the driver's first mutable module state. The `with_store_lock` docstring states why the state exists and where it is live. Callers must not mutate returned digests; today they only `set()`, `len()`, or concatenate them.
- Refusal drift (#88): there is one parse, `_as_child`. Heal's refusal set was already equal to it (`_digests_of_dict` and `loads_tree` plus `_digests_of_tree` reject the same inputs), so heal's skip behavior does not change.

## Pre-Mortem

- The subprocess wall-time gain is small enough that the operator calls it not worth it. Response: report in-process and subprocess numbers both, and give the line delta (expected net negative, about −11). If lines go positive, reconsider.
- The read-count test is a change-detector. Response: it asserts an outcome contract (at most one read per children file per command), not a call sequence. It goes red only when a command does redundant I/O, which is the regression the operator named.
- A hidden caller of `_digests_of_dict` or a `leaf_digests` behavior difference. Response: grep found no other callers. The prototype ran the full suite, and only the cache-scope tests and the raw-JSON pin failed.

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [ ] Preflight (run 1 FAIL fixable: cached caption; plan amended)
- [ ] Build
- [ ] QA
