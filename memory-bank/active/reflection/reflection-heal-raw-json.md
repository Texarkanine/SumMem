---
task_id: heal-raw-json
date: 2026-08-25
complexity_level: 2
---

# Reflection: Heal raw-JSON overlap checks

## Summary

Heal overlap checks now hash leaves from `json.loads` dicts. `note` and `nap` reuse one view listing and the already-loaded knobs. QA PASS; tox 290 on py311–py314.

## Requirements vs Outcome

Delivered as specified. No skip-heal marker, no dataclass-class rewrite, no catalog or recall/zoom changes. `list_view` stayed closed. `os.scandir` stayed out. Rematerialize and pack writes still build `Tree`. Added one extra CLI test (`test_cli_nap_passes_heal_nodes_to_write_nap`) beyond the plan's stub list because the behavior list already required it.

## Plan Accuracy

The two-unit sequence held. The parse-equivalence challenge was real and was designed in: `_digests_of_dict` touches the same keys as `_tree_from_dict`. No surprise from `surgery.py`. Fold after `nap` still lists once, as planned.

## Build & QA Observations

TDD went red then green without iteration on the walker. One implementation slip: `fold_request` briefly defaulted omitted `wake_lines` from knobs instead of the script constant; corrected before the suite. QA PASS with a non-blocking advisory that the nap CLI test does not count post-write `list_view` calls.

## Insights

### Technical

- A digest-only walker that is looser than `loads_tree` will return a set for a pack `_as_child` cannot load, then rematerialize raises. Touch the same keys.

### Process

- Monkeypatch `loads_tree` is the right "no unused dataclasses" oracle. A wall-clock assertion would have been the flake.

### Million-Dollar Question

If heal had never used `Tree` for digests, this is what the write path would look like: optional `nodes` / `entry_chars` on the three functions, one list per heal pass, fold after nap lists because the view changed. A `StoreContext` type would have been extra.
