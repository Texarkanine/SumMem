# Fold research: middle orphans

Research tooling and results behind the four creative decisions for task `middle-orphans`. Everything here drives the **real driver** (`summem`) in process; only the pair choice is swapped. It is research, not product, and is deleted with `memory-bank/active/creative/` at archive.

Open `fold-review.html` in a browser for the visual review: the six algorithms brick by brick, the charts, the decision ramifications, both architectures, and the file-by-file review.

## Run it

Run from the repository root. Use Python 3.11 or newer. Never use this machine's bare `python3`, which is 3.10. Pass a scratch directory **outside the repository** as `WORK`; the scripts create stores there.

```bash
R=memory-bank/active/creative/fold-research
WORK=$(mktemp -d)
uv run --python 3.11 python $R/sim.py   ./summem $WORK              # operator scenario + today vs unequal fold (~3 min)
uv run --python 3.11 python $R/sim2.py  ./summem $WORK              # skip fold: oldest-pair vs smallest-grain (~4 min)
uv run --python 3.11 python $R/sim3.py  ./summem $WORK v1 32 7      # picker in {equal,v1,pull,score}, budget, seed (~1 min)
uv run --python 3.11 python $R/sim4.py  ./summem $WORK v1 32 7      # picker in {equal,v1}: one-writer shape check (~1 min)
python3 $R/walk.py                                                   # operator example, grains only (instant)
python3 $R/walk2.py $WORK/walks.json                                 # same, all six rules, JSON for the review page
python3 $R/single.py                                                 # one writer, today's rule: shape guarantees over 5,000 notes
uv run --python 3.11 python $R/grains.py  ./summem <store-parent>...  # grain list and walls of real stores (read-only)
uv run --python 3.11 python $R/oddscan.py ./summem <path/.summem>...  # non-power-of-two packs, listed and nested (read-only)
```

`prototype_plan.py <copy-of-summem>` applies the measured prototype to a **copy** of the driver. Its docstring lists where it differs from the plan.

## The model

- Writers each keep their own store copy. Every note is followed by what an obedient agent does: heal, then nap every requested pair (`sim.catch_up`).
- With probability 8% per note, the writer merges into `main` with a whole-file three-way merge. That is what git does for immutable, uniquely named files: keep files both sides have, plus files either side added since the shared base. Then the writer takes `main`.
- After each merge, the next mutating command on `main` heals and catches up (`probe` store).
- Pickers: `equal` (today: oldest equal-grain neighbors), `r2` (oldest neighbors with older < 2 × newer — unequal fold), `v1` (oldest row with a same-grain row anywhere below, paired with the nearest), `v2` (two oldest rows of the smallest repeated grain), `pull` (only pairs whose gap holds smaller rows; fewest walls, then shortest jump, then oldest), `score` (any pair; fewest walls, then shortest jump, then oldest).

Metrics:

- **Walls**: an older row with a smaller grain than its newer neighbor.
- **Notes listed above an older note**: notes that appear in the listing before at least one older note in a later row.
- **Worst misplacement ÷ own pack**: for the worst note, how many older notes are listed after it, divided by the grain of the row it sits in.
- **Recent verbatim**: trailing loose notes at the end of the listing.
- **One-writer shape**: no walls, every grain ≥ 2 at most twice, at most one grain doubled.

## Results

All runs use four writers and 1,500 notes; values are seed 7 · seed 11 unless noted. Raw output is in `results/`.

| Rule | Merges left over budget (b32) | Avg walls after a merge | Notes above an older note | Worst ÷ own pack | Recent verbatim | Depth |
|---|---|---|---|---|---|---|
| Today (`equal`) | 76/113 · 101/119 | 25.0 · 33.3 | 807 · 802 | 4.2 · 4.6 | 1 · 1 | 6 |
| Pull-back only (`pull`) | 0 · 0 | 1.9 · 3.2 | 965 · 1,251 | 0.2 · 1.2 | 21 · 14 | 10 |
| Fewest walls (`score`) | 0 · 0 | 0.2 · 0.5 | 209 · 191 | 0.2 · 18.2 | 28 · 20 | 10 |
| **Oldest pair first (`v1`)** | **0 · 0** | **0.0 · 0.0** | **179 · 103** | **0.2 · 0.1** | **28 · 28** | 10 |

- Budget 8, seed 7: `equal` over budget after 105/113 merges, `pull` 71/113, `score` 0 (worst 5.7×), `v1` 0 (worst 1.0×).
- Unequal fold (`r2`, seed 7, b32): never over budget, but writes packs of 3, 35, 1,371 and depth 14. Ruled out: no non-power-of-two packs.
- Smallest-grain-first (`v2`): one writer at b32 keeps 0 recent notes verbatim (today and `v1`: 26).
- Young `main` `[4, 1]` + a merged 8-pack, then 64 notes at b4: `equal` and `pull` still list the 4 and the 1; `score` and `v1` heal to `[64, 8, 4, 1]`.
- One-writer shape after each merge (`sim4`): `v1` keeps it in 87–97% of merges and has the same grains a single writer would have in 85–97%. It never had more than 2 copies of a grain or more than 1 doubled grain. `equal` kept it in 2–11%, with up to 28 copies of one grain. A writer's own listing recovers within a median of 2–8 notes after a merge breaks it (max 23).
- One writer under today's rule (`single.py`, 5,000 notes, b10 and b32): grains never rise, each grain ≥ 2 at most twice, at most one doubled grain. A 64 with nothing near its size below it is normal (73 notes at b10: `[64, 1×9]`).
- Local store scan (`oddscan.py`, 2026-10-06): 22 stores in 11 repositories: 0 non-power-of-two packs, listed or nested; 0 unmigrated stems. The four stores that have folded have 0 walls.

## Caveats

- This is one process model with two seeds. It is evidence, not proof.
- `sim.py`'s `scenario()` and the young-main case construct the merged state directly in one store; that is the same set of files git would produce.
- The scripts patch `m._adjacent_nodes` to accept any pair, so pickers can be compared before the real pair rule exists.
