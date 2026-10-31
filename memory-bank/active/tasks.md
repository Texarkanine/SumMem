# Current Task: fold-scan-rows

**Complexity:** Level 1

## Fix

A note unlinked after listing aborted every other row because `_fold_grains` opened it through `_as_child`, and `FileNotFoundError` is not `ValueError`. The scan now keeps a note at `node.leaves` and does not open the note file. `OSError` stays on `_as_child` of the row being napped.

A children file that parses, whose note text is not a string, raised `AttributeError` from `note_file_bytes` outside the scan's `ValueError` catch. `_digests_of_tree` now raises `ValueError("unreadable pack")` for that text. The existing catch makes the pack grain 0. Other exceptions are not caught.

Files: `summem`, `tests/test_fold.py`.
