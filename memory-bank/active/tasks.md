# Current Task: fold-leaf-quotes

**Complexity:** Level 1

## What broke

`fold_request` quoted leaf pairs through `format_wake_line` (`x1 YYYY-MM-DD: text`). Pack pairs already quoted captions only after #72.

## Why

#72 left that leaf branch on purpose. Issue #80 is that leftover: fold quotes are the writing task, not a wake listing.

## What changed

Quote `node.caption` for every fold pair. Drop the kind/grain branch. `Run:` still has unique prefixes. Wake, recall, and zoom stay listing grammar.

## Files

- `summem` (`fold_request`)
- `tests/test_fold.py`
- `docs/architecture/index.md`
- `memory-bank/systemPatterns.md`
- `README.md` (example fold quotes)
