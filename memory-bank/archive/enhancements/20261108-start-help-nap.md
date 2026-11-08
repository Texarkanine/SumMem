---
task_id: start-help-nap
complexity_level: 2
date: 2026-11-08
status: completed
---

# TASK ARCHIVE: start, help, and a finished nap

## SUMMARY

`start` reports a store in one sentence and refuses a missing directory. `help` reuses the existing help text and stays off the printed catalog. A `nap` of an already-folded pair prints `Saved.` and writes nothing, including when that nap sits inside a larger one. Any other bad id gets a short refusal that does not point at `wake`. Shipped on main as [PR #101](https://github.com/Texarkanine/SumMem/pull/101). QA passed. py311–py314 passed (443).

## REQUIREMENTS

From the project brief, then the PR 101 rework the operator chose over the first archive:

- `start` prints `There is a store in ./path.` whether the store is new or already there. A path that is not an existing directory is `not a directory: ./path`, and `start` creates nothing.
- `summem help` and `summem help <command>` print the same text as `-h` and `<command> -h`, on stdout, exit 0. Bare `summem` stays a usage error (stderr, exit 2). `note help` still records the text `help`.
- The catalog names one way to do each thing. `help` keeps working and is not listed. The user-guide table matches that printout.
- A `nap` whose two ids are already some nap's two direct children succeeds, prints `Saved.`, writes nothing, and then the next real fold or the idle line. That includes a nap buried inside a larger one.
- Any other id is `not a fold row` or `unknown id`, with no wake hint.
- Fewest lines. No new library. No sentence whose only job is to mention the nested case. The four sentences that already described that success stay.

## IMPLEMENTATION

In [`summem`](../../../summem):

- `start` calls `ensure_store` only when the path is already a directory, then prints the one sentence. A missing path returns 1.
- `main` rewrites a leading `help` onto `-h` before argparse. `usage_text` has no `help` row. The options line stays `{CLI_NAME} <command> -h`.
- `_nap_miss` walks each view nap with `_as_child` and `_index_tree`. A pair match on `index["root_kids"]` or any list in `index["kids"]` returns `None`, which skips `write_nap`. `root_kids` is only the view nap's own pair. Nested pairs live in `kids`. Both stay. Known ids that are not that pair are `not a fold row`. A token that names nothing is `unknown id`.

[`docs/user-guide/commands.md`](../../../docs/user-guide/commands.md) dropped the `help` row so the table is what `-h` prints. [`memory-bank/systemPatterns.md`](../../systemPatterns.md) records the one-way catalog and that `start` does not create the directory. `docs/user-guide/troubleshooting.md`, `docs/architecture/wake.md`, and `docs/architecture/merges-and-healing.md` already said the buried pair succeeds. They were left as written.

Preflight advised a `pairs` field on `_index_tree`. The loop over `kids` and `root_kids` was enough, and that is what shipped.

## TESTING

TDD in `tests/test_cli.py` and `tests/test_scopes.py`. New cases: the catalog has no `summem help` line and still has `<command> -h`; a four-note fold buried inside one outer nap, then `nap` of the inner pair, exits 0 with `Saved.` and the idle line, empty stderr, and unchanged nap filenames. Existing help, start, and nap-refusal tests stayed.

The buried-pair test went red as `not a fold row` for the same ids the review named, then green.

Preflight of the first plan: FAIL (fixable), then PASS WITH ADVISORY after the id check used `leafset_id` of the digest and known ids covered view rows plus nested tree ids. Preflight of the rework: PASS WITH ADVISORY. QA of both the first build and the rework: PASS. `tox -e py311` then `tox run-parallel`: 443 passed on py311–py314.

## LESSONS LEARNED

- A note id on wake is `leafset_id` of the digest. The raw digest matches nothing in the view.
- `root_kids` is the view nap's own pair. Each nap inside that tree is a separate list in `kids`. A check that reads only `root_kids` accepts one depth and refuses the next.
- `kids` is already every nested nap's children. A second pairs field would copy that.

## PROCESS IMPROVEMENTS

Nothing to change. The rework sequence held: catalog test, table, buried-pair test, then the loop.

## TECHNICAL IMPROVEMENTS

None. The preflight pairs-field advisory was declined.

## NEXT STEPS

None. [PR #101](https://github.com/Texarkanine/SumMem/pull/101) is on main.
