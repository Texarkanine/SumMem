# Project Brief

## User Story

As an agent using SumMem, I want `start`, `help`, and a repeated `nap` to answer in one short line, so I can tell what happened and do the next right thing.

## Use-Case(s)

### Start an existing directory

The operator runs `start` on a directory that is already there. The command creates a store if needed, leaves an existing store alone, and prints one sentence that a store is there. The path looks like the root-wake catalog (`./packages/api`).

### Start a missing path

The operator runs `start` on a path that is not an existing directory, including a typo such as `start help`. The command creates nothing and exits with a short error.

### Ask for help

The operator or an agent runs `summem help`, or `summem help <command>`. They get the same text as `-h` or `<command> -h`, on stdout, exit 0. A bare `summem` stays a usage error.

### Nap a fold that already happened

An agent runs the same `nap` a fold request already completed. The command succeeds. The agent is finished with that pair. Any further fold is a new request.

### Nap an id that is not a fold

An agent passes an id that is not a row `nap` can fold. The refusal says what went wrong, in few words, and does not say to copy an id from `wake`.

## Requirements

1. `start` prints one sentence on success, the same sentence whether the store is new or already there.
2. `start` refuses a path that is not an existing directory. It does not create the path or missing parents.
3. CLI output still does not mention store files or git.
4. `summem help` prints the same catalog as `summem -h`, stdout, exit 0, from `usage_text()`.
5. `summem help <command>` may reuse the existing `-h` rewrite when that stays a few lines. It must not grow a new argument parser or a dependency.
6. Bare `summem` keeps printing the catalog to stderr and exiting 2.
7. A `nap` whose two ids are already the two children of a nap succeeds, writes nothing new, and uses the normal success output (`Saved.`, then the next real fold request or the idle line).
8. Any other id `nap` cannot fold gets one short refusal. Do not say "Copy an id from wake." Name the failure so the next attempt can be closer: an id that is not a current fold row, versus an id the store does not have.
9. `nap` still refuses ids it cannot fold, except the already-folded pair, which is success.
10. When this ships, update the user-guide sentences that say `start` prints nothing or creates a missing directory, and the architecture sentences that say a stale or expanded `nap` fails with `unknown id`.

## Constraints

1. The driver is pasted into every consumer repository. Fewest lines. No work beyond the outcome.
2. No new libraries. Help routing stays a small stdlib rewrite onto the existing `-h` / `--help` text.
3. Error text is short, in the style of a terse Unix tool. No extra sentence unless it changes what the agent does next.
4. One success string for `start` if one sentence can cover both outcomes.
5. `note help` still records the text `help`. `--` still passes a literal `--help`.

## Acceptance Criteria

1. `start ./existing` prints one line that a store is there, creates the store when missing, and leaves an existing config unchanged.
2. `start ./missing` exits non-zero, prints a short error, and creates no directory and no store.
3. `summem help` and `summem -h` print the same catalog to stdout and exit 0. `summem help note` prints the same text as `summem note -h` if the rewrite stays small.
4. Bare `summem` still writes the catalog to stderr and exits 2.
5. A second `nap` of a pair that is already folded exits 0, prints `Saved.`, does not add a nap, and does not tell the agent to retry that pair.
6. `nap` of an id that is not that pair exits non-zero, does not mention `wake`, and does not mention store files or git.
