# Project Brief

## User Story

As a maintainer of SumMem's test suite, I want the obviously wrong and fixable smells in the 2026-08-25 SLOBAC audit applied so the suite is a tighter ratchet — not a perfect suite, and not a rewrite of the file-backend proofs.

## Use-Case(s)

### Use-Case 1

An assessor finding names a real hole (a test that can go green on a broken implementation, dead scaffold, or an oracle that is the SUT talking to itself). The suite is changed so that hole closes.

### Use-Case 2

An assessor finding names a product pattern (ValueError ratchets, subprocess proofs next to in-process units, `test_proof_*.py` as the acceptance surface). The finding is left alone.

## Requirements

1. Work from [`.slobac/2026-08-25T12-27-19/audit.md`](../../.slobac/2026-08-25T12-27-19/audit.md) as a ratchet, not as a mandatory punch list.
2. Apply remediations the build judge finds obviously wrong and fixable.
3. Leave findings 59–63: the proof files are the file-backend acceptance surface named in `productContext.md` / `techContext.md`. "First proof N" in module docstrings is leftover VISION numbering; that is cosmetic, not a reason to regroup or delete.
4. Do not invent a typed-exception hierarchy to satisfy loose-text-oracle on ratchet `ValueError` messages.
5. Do not replace existing process-boundary proofs with in-process units, or the reverse.

## Constraints

1. The audit is not expected to take the suite 100% of the way to perfection.
2. Executable behavior stays TDD-governed. This task is test-suite hygiene; product CLI behavior does not change unless a test fix proves a product bug.
3. Tests load repo-root `summem`; the suite command is `tox`.
4. Agents never write the store.

## Acceptance Criteria

1. Each accepted finding has a stronger oracle or less coupling, and the named test still fails if the behavior it claims is broken.
2. Rejected findings are listed with a one-line reason in the plan / progress, not silently skipped.
3. `tests/test_proof_*.py` remain in place with the same process-level claims.
4. `tox` (or `tox -e py311` if that is the local interpreter set) stays green.
