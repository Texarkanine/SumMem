# Active Context

## Current Task: codecov-upload
**Phase:** QA - COMPLETE (PASS)

## What Was Done
- Opt-in `tox -e coverage` writes `coverage/lcov.info` via `pytest-cov --cov=summem`. Default `tox` stays coverage-free; `pytest-cov` is a default tox dep so the live nest can run.
- Live emit lives in `/home/mobaxterm/git/SumMem/tests/test_coverage_collection.py` (child `COVERAGE_FILE` under `tmp_path`, parent `COV_*` stripped). Ini locks live in `/home/mobaxterm/git/SumMem/tests/test_tox_runner.py`.
- Coverage env pins `base_python = py311` and `Path.mkdir`s the lcov parent.
- CI: `/home/mobaxterm/git/SumMem/.github/workflows/ci.yaml` (`permissions: contents: read`, concurrency, `codecov/codecov-action@v7`). `/home/mobaxterm/git/SumMem/codecov.yml` has project/patch status off.
- README badge + Developing note; techContext Testing Process updated.
- tox 236 passed on py311–py314.

## Next Step
- QA review.
