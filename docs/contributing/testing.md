# Testing

The tests run under [tox](https://tox.wiki/), on Python 3.11 through 3.14. If tox is not installed, [uv](https://docs.astral.sh/uv/)'s `uvx --with tox` supplies it for one command.

## The full run

From the repository root:

```bash
uvx --with tox tox run-parallel
```

This is the full local run. It tests each installed Python from 3.11 through 3.14 at the same time. Each Python uses at most four test workers (`-n auto --maxprocesses=4`). Run it before you open a pull request.

Do not run two tox commands for the same Python version in one checkout. Both commands write the same directory under `.tox/`.

## While you edit

Test on Python 3.11 only:

```bash
uvx --with tox tox -e py311
```

Run one file or one test. Put the pytest path after `--`:

```bash
uvx --with tox tox -e py311 -- tests/test_foo.py::test_bar
```

Run those tests one at a time. Add `-n0` after `--`:

```bash
uvx --with tox tox -e py311 -- -n0 tests/test_foo.py::test_bar
```

When `tox` is already on your `PATH`, leave out `uvx --with tox`.

`tox` with no extra arguments runs the same Python versions one after another.

## Notes

The tests load the `summem` file at the repository root. That file has no `.py` suffix.

Pull requests run [`.github/workflows/pr.yaml`](https://github.com/Texarkanine/SumMem/blob/main/.github/workflows/pr.yaml). That workflow runs `tox -e py311` through `py314`.

A push to `main` runs [`.github/workflows/ci.yaml`](https://github.com/Texarkanine/SumMem/blob/main/.github/workflows/ci.yaml). That workflow runs the same tests, then `tox -e coverage`, and uploads the report to Codecov.

`tox -e coverage` writes `coverage/lcov.info`. It runs the tests one at a time. Run it as its own command.
