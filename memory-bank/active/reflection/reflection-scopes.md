---
task_id: scopes
date: 2026-08-19
complexity_level: 2
---

# Reflection: scopes

## Summary

Last slice of L4 `file-backend`: `start`, `--path` walk-up, per-store `config.toml`, and a root-wake catalog. Proofs 7-8 pass. 156 pytest. QA passed on the first try.

## Requirements vs Outcome

Every scopes requirement landed. Nested stores are started directories, not inferred packages. Walk-up never creates a store. Git-root auto-create stays. Catalog is a computed walk that honors git ignore, including `.git/info/exclude`. `wake_text` is still the decaying document. Identity, nap, zipper, and zoom-from-`HEAD` unchanged. Nothing descoped. Nothing added outside the brief.

## Plan Accuracy

The five-unit order (resolve, `start`, `--path`, knobs, catalog) was the right sequence. File list was right: one script plus `tests/test_scopes.py` and `tests/test_proof_scopes.py`. Preflight's three amendments were real: `--path` on `nap`/`zoom`/`recall`, `ENTRY_CHARS` through `write_note`/`write_nap`, and `store_stats` grain instead of loose-file count.

The surprise was not in the product. Duplicate empty stub names in the test module overwrote the filled catalog tests, so the first red run was a lie. Deleting the leftovers made the tests fail for the right reason.

## Build & QA Observations

Build was linear once the shadowed tests were gone. QA ([scopes L2 QA](9365a782-6d45-4190-a4a3-11c3ce1a967b), gemini-3.1-pro) passed with no blocking findings. No rework.

## Insights

### Technical

- Two functions with the same name in a pytest module mean only the last is collected. Leftover `pass` stubs after filling tests will silently eat the real cases.

### Process

- Preflight rewriting the plan to close coverage holes (`nap`/`zoom`/`recall --path`, `ENTRY_CHARS` through writers, folded catalog grain) was cheaper than finding those in QA.

### Million-Dollar Question

If addressing had existed in ingest, `find_store_parent` would never have meant "the git root is the store." Git-root auto-create and first-`.summem/` resolve are two walks. That split is what we built; it is the shape that belongs.
