---
task_id: drop-dataclasses
date: 2026-08-25
complexity_level: 2
---

# Reflection: drop-dataclasses

## Summary

Slots replaced the five frozen dataclasses and command-only stdlib modules now import only on the paths that need them. `version` / `init` / `-h` skip those imports, including argparse. tox 287 passed on py311–py314; Python 3.10 still prints the 3.11 floor.

## Requirements vs Outcome

Delivered as specified. Unit 4 ran because argparse was the leftover. Added `__eq__` after codec tests compared `Tree` objects. Isolation tests track the driver's `__import__`, not `sys.modules`, because 3.14 pathlib imports fcntl.

## Plan Accuracy

Sequence and file list were right. The surprise was 3.14, not argparse or the zipper `m.fcntl` patch.

## Build & QA Observations

Build was linear after the 3.14 oracle fix. QA PASS; advisory that the probe omits `random` (acceptance does not name it).

## Insights

### Technical
- 3.14 pathlib imports fcntl. A "module absent from sys.modules" test is not portable across CPython minors.

### Process
- Nothing notable

### Million-Dollar Question

If this had been assumed from the start: plain slot types, no dataclasses, and argparse never at module import. Command `-h` can stay argparse as long as exact `version` / `init` / bare help return first. That is what we built.
