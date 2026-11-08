# Progress

`start` reports a store in one sentence and refuses a missing directory. `help` reuses the existing help text. A `nap` of an already-folded pair succeeds, and any other bad id gets a short refusal that does not point at `wake`.

**Complexity:** Level 2

## 2026-11-07 - COMPLEXITY-ANALYSIS - COMPLETE

* Work completed
    - Classified the three open issues as one Level 2 enhancement of the CLI
* Decisions made
    - Level 2: one script, contained behavior changes, wording still to try during build
* Insights
    - Bare `summem` is an intentional usage error (stderr, exit 2) from the first CLI. `-h` is already stdout and exit 0. The blog post's stdout rule covers help probes, which this path already is.

## 2026-11-07 - PLAN - COMPLETE

* Work completed
    - Wrote the Level 2 plan for start, help, and nap replies
* Decisions made
    - One start sentence: `There is a store in ./path.`
    - Missing path: `not a directory: ./path`, and no `mkdir`
    - `help` rewrites to the existing `-h` path, including `help <command>`
    - An already-folded pair succeeds with `Saved.` and the real next fold or the idle line
    - Other nap misses are `not a fold row` or `unknown id`, with no wake hint
* Insights
    - Napping the two children `wake` expanded is the nap that already exists, so it is the success path, not a second error

