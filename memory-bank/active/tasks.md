# Current Task: pr-90-review-fixes

**Complexity:** Level 1

## Fix

What broke: `df6a144` deleted `test_main_prints_fold_request_when_over_budget`, so a root excision over budget no longer had to name the two oldest surviving short ids or omit the excised id. README and `docs/surgery.md` still quoted `Compress these two`. The serial Developing command dropped `tests/test_foo.py::test_bar`.

Why: the verb pin was removed on purpose, and the id checks left with it. The docs still showed the old printed verb and a copy-paste command that runs the whole suite serially.

What changed: restored the root-excision id checks without asserting the fold-prompt verb. Pointed both quotes at `Summarize these two`. Put the test path back on the `-n0` command.

Files: `tests/test_surgery.py`, `README.md`, `docs/surgery.md`.
