# Project Brief

## User Story

As an agent napping two notes, I want the fold prompt to quote only the two sentences so I write a caption from the facts, not from wake listing grammar.

## Use-Case(s)

### Use-Case 1

Two equal-grain notes over budget request a nap. The quoted lines are the note texts. `Run:` still has unique prefixes.

### Use-Case 2

A pack pair already quotes captions only after #72. That stays. Empty captions stay blank quotes.

## Requirements

As described in [issue #80](https://github.com/Texarkanine/SumMem/issues/80):

1. Quoted fold source lines are always the caption / note text: no `xN`, no date, no prefix.
2. Empty caption stays a blank quote, not a reconstructed listing line.
3. `Run:` still has unique prefixes (and `--path` when needed).
4. Wake, recall, and zoom stay `x1 YYYY-MM-DD:` / `xN <prefix>:`.
5. `tests/test_fold.py::test_fold_request_mentions_remaining` moves off dated leaf-pair quotes.
6. Atlas / `systemPatterns.md` say fold quotes, not only pack captions.

## Constraints

1. Do not change OptMem.
2. Do not put ACK or idle inside `fold_request`.
3. Do not strip grain, date, or hash from wake, recall, or zoom listings.

## Acceptance Criteria

1. A leaf-pair `fold_request` quotes `  {text}` for each note.
2. A pack-pair `fold_request` still quotes captions only.
3. Empty caption is a blank quote.
4. `Run:` still names both ids by unique prefix.
5. Wake / recall / zoom listings are unchanged.
