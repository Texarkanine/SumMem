# Task: version-tracking

* Task ID: version-tracking
* Complexity: Level 2
* Type: simple enhancement

Instrument [SumMem#20](https://github.com/Texarkanine/SumMem/issues/20): Release Please on `main` for semver tags, plus `summem version` that prints the in-script `__version__` Release Please extra-files will bump. One file. No Dependabot.

## Test Plan (TDD)

### Behaviors to Verify

- Version print: `main(["version"])` → exit 0, stdout is exactly `__version__` plus a newline
- Outside a repository: `main(["version"])` → exit 0, creates no store and no files
- Extra args: `main(["version", "x"])` → nonzero
- No `--path`: `main(["version", "--path", "."])` → nonzero; `main(["version", "-h"])` does not list `--path`
- Help routing: `main(["-h", "version"])` → exit 0, prints version help, not the top-level catalog
- Catalog: `usage_text()` names `summem version` and that line has no `--path`
- Marker: the `__version__` assignment line in repo-root `summem` contains `x-release-please-version`
- Lockstep: `summem.__version__` equals `.release-please-manifest.json` `"."`
- Extra-files: `release-please-config.json` `packages["."].extra-files` includes `{type: "generic", path: "summem"}`

### Edge Cases

- Invalid extra token and `--path` on `version` (same shape as `init`)
- Empty/null: bare `main([])` still prints the catalog (existing test); `version` is now one of the named commands
- Boundary: version works with cwd outside a git repository (like `init` and help)
- Existing `--path` matrix: `version` joins `start` and `init` as a rejector

### Test Infrastructure

- Framework: pytest via `tox` (`tests/`, `conftest.load_summem` / `SourceFileLoader`)
- Test location: `tests/`
- Conventions: one module per CLI surface (`test_init.py` is the analog); `main([...])` + `capsys`; no change-detectors on prose
- New test files: `tests/test_version.py`
- Existing tests to extend: `tests/test_cli.py` (`test_bare_invocation_prints_command_catalog`, `test_path_flag_is_known_on_all_non_start_commands`)

## Implementation Plan

### 1. Version CLI — executable

- Files: `summem`, `tests/test_version.py`, `tests/test_cli.py`

1. Stub tests: add `tests/test_version.py` empty cases for print, outside-repo, extra args, `--path` reject, `-h version`. Extend the two `test_cli.py` cases to include `version` in the catalog / `--path` reject set.
2. Stub interface: `__version__ = "0.1.0"  # x-release-please-version` next to `CLI_NAME`. `sub.add_parser("version")`. Add `"version"` to `_COMMANDS`. Handle `args.cmd == "version"` before `resolve_parent` (same as `init`).
3. Write tests and run red: stdout lockstep with `__version__`; rc 0 outside a repo; extra args and `--path` nonzero; catalog line exists without `--path`.
4. Write code and run green: `usage_text` line for `version` (no `--path`). `main` writes `__version__ + "\n"` and returns 0. Do not add `--version`. Do not split the script.

### 2. Release Please extra-files lockstep — executable

- Files: `release-please-config.json`, `.release-please-manifest.json`, `tests/test_version.py`

1. Stub tests: empty cases for marker, manifest lockstep, generic extra-files path `summem`.
2. Stub interface: commit the two JSON files with placeholder or empty packages if needed so paths exist; do not invent a second version file.
3. Write tests and run red: marker substring; `json.loads` manifest `"."` equals `m.__version__`; extra-files generic path is repo-root `summem` (not `.summem/summem`).
4. Write code and run green: `release-type: simple`, `bump-minor-pre-major: true`, `bump-patch-for-minor-pre-major: false`, `include-component-in-tag: false`, packages `"."` with generic extra-files on `summem` and the sibling pull-request-header (`:service_dog: I have created a release *bark* *woof*`). Manifest `"."` is `0.1.0`. Four-space JSON like stockroom.

### 3. Release Please workflow — prose/policy

Operator ruling 2026-08-20: this YAML only *invokes* a third-party action. That is not executable product behavior for TDD here. TDD would apply if SumMem were a GitHub Action.

- Files: `.github/workflows/release-please.yaml`
- No tests: prose/policy artifact

1. Copy stockroom’s workflow: `googleapis/release-please-action@v5`, `actions/create-github-app-token@v3`, `vars.HELPER_APP_ID`, `secrets.HELPER_APP_PRIVATE_KEY`, explicit `config-file` / `manifest-file`, permissions `contents` / `pull-requests` / `issues`, concurrency group on `github.workflow`+`github.ref` with `cancel-in-progress: false`.
2. No publish job. No `id-token`. Comment that the operator provisions the helper app after merge.
3. Do not add Dependabot. Do not pre-create `CHANGELOG.md` (Release Please writes it on the first release PR).

### 4. Living docs — prose/policy

- Files: `README.md`, `docs/architecture/index.md`, `memory-bank/systemPatterns.md`, `memory-bank/techContext.md`
- No tests: prose/policy artifact

1. README command table: add `summem version` (print the script version). Keep `init` / store commands unchanged.
2. Architecture scopes: “Outside a repository, store commands fail. `init`, `version`, and help still print.”
3. `systemPatterns.md`: include `version` in the agent-facing command list.
4. `techContext.md`: note Release Please (`simple` + extra-files on repo-root `summem`) as how tags happen; helper-bot names; no packaging step still.

## Technology Validation

No new technology - validation not required. Release Please and the helper-app token action are copied GitHub config, not a product dependency. No Python package, no `pyproject.toml`.

## Dependencies

- Sibling pattern: `../stockroom` (simple + generic extra-files + helper-bot workflow)
- Sibling header: `../inquirerjs-checkbox-search`, `../jekyll-mermaid-prebuild`, `../stockroom`
- Operator post-merge: repository variable `HELPER_APP_ID`, repository secret `HELPER_APP_PRIVATE_KEY`
- Existing: pytest / tox, repo-root `summem`

## Challenges & Mitigations

- Helper-bot auth is absent until the operator sets the variable and secret: document in the workflow comment; do not invent a `GITHUB_TOKEN` fallback (stockroom’s reason is that the app token makes the release PR trigger CI).
- `release-type: python` expects a package layout we do not have: use `simple` plus generic extra-files.
- Extra-files aimed at `.summem/summem` would edit a symlink: target repo-root `summem` only.
- Existing catalog / `--path` tests name a closed command set: extend those cases in Unit 1 so they do not fight the new command.
- Asserting Release Please JSON as a snapshot would be a change-detector: test only marker, lockstep, and the generic path.
- A later preflight may call the workflow “configuration or workflow the product runs”: it does not. The product is the script. See the operator ruling on unit 3. Do not add workflow tests.

## Pre-Mortem

- Operators type `summem --version` and get argparse failure: already covered — the CLI is a subcommand catalog; `init` is the analog. One surface: `version`.
- First release never bumps the script: already covered by Challenge on extra-files path and the lockstep/marker tests.
- Preflight rejects a JSON snapshot test: already covered by Challenge on change-detectors.
- Preflight blocks again on missing workflow tests: already covered by the operator ruling on unit 3. Keep unit 3 prose/policy.
- Starting at `0.1.0` surprises someone who wanted `1.0.0`: keep `0.1.0` (no prior tag; sibling `bump-minor-pre-major` applies). Do not add a second version source to “look official.”

## Status

- [x] Initialization complete
- [x] Test planning complete (TDD)
- [x] Implementation plan complete
- [x] Technology validation complete
- [x] Pre-Mortem complete
- [x] Preflight
- [x] Build
- [ ] QA
