# Tasks: pr99-review-fixes

## Fix Record

Docs on branch `docsite` stated five things the driver does not do. Each claim was checked against `summem` (and, for items 1, 2, 4, 5, by running it in scratch repos).

| Item | What was wrong | Why | What changed | File |
|---|---|---|---|---|
| Zipper example | Heal was shown opening `ABCDEFGH`. | Of two same-size overlapping naps, `_first_overlap` opens the earlier filename; with these labels that is `ABCD1234`. | Diagrams and sentences now open `ABCD1234` and end with `ABCDEFGH` beside `1234`; the same-size rule is stated. | `docs/how-it-works/no-conflicts.md` |
| Same-size rule | Overlap said only "the smaller one", and "the larger nap". | Same-size case was unstated. | Added the name-order rule; "larger" became "other". | `docs/architecture/merges-and-healing.md` |
| Nap pair rule | "`nap` refuses any other pair." | `write_nap` accepts any same-grain pair with no same-grain row between them. | States what `nap` also accepts; Troubleshooting lists refusals. | `docs/user-guide/commands.md` |
| Test-first rule | Link to a missing `.claude/` rule file. | Operator: tech docs do not link to agent rule files. | Link sentence removed; the bullet already states the rule. | `docs/contributing/index.md` |
| Unreadable children files | Said every unreadable file prints `skipped a pack` once. | Zoom of the broken nap raises `unreadable pack`; the warning prints once per unreadable file passed while searching. | Rewritten in two sentences. | `docs/architecture/zoom-and-recall.md` |
| Surgery check | Root-store `recall` with raw text. | `recall` is per store and takes a regex. | Same `--path`, escape list, what a remaining hit means. | `docs/advanced/surgery.md` |

## Verification

- `uv run --no-config properdocs build --strict`: OK.
- `tox -e py311`: 426 passed (docs-only change; no product behavior touched).

## QA

PASS. All five claims checked against `summem` (`_first_overlap`, `heal_view`, `write_nap`, `zoom_text`, `recall_text`, `surgery.py` arguments). QA re-ran the strict docs build: OK. Four advisories, none blocking; see `.qa-validation-status`:

- Zipper: the `ABCD1234`-first result holds when labels are read as names; real names sort by hashed content id after a shared prefix.
- Zoom: a missing `.tree` gives `unknown id`, not `skipped a pack`; Troubleshooting already covers it.
- Surgery: no hint for telling a note hit (`x1`) from a summary hit (`xN`).
- Surgery: the code block always shows `--path PATH`, though the prose says "if any".
