# Docs Site

This site is built with [ProperDocs](https://github.com/ProperDocs/properdocs), a continuation of MkDocs 1.x, and the [Material](https://squidfunk.github.io/mkdocs-material/) theme.

| What | Where |
|---|---|
| Configuration | [`properdocs.yaml`](https://github.com/Texarkanine/SumMem/blob/main/properdocs.yaml) |
| Pages | [`docs/`](https://github.com/Texarkanine/SumMem/tree/main/docs) |
| Page order | The `.pages` file in each folder of `docs/` |
| Build tools | The `docs` group in [`pyproject.toml`](https://github.com/Texarkanine/SumMem/blob/main/pyproject.toml), locked in `uv.lock` |
| Publishing | [`.github/workflows/docs.yaml`](https://github.com/Texarkanine/SumMem/blob/main/.github/workflows/docs.yaml) |

`pyproject.toml` exists only for the docs tools. It does not package `summem`, and the tests do not use it.

## Preview and build

You need [uv](https://docs.astral.sh/uv/). From the repository root:

```bash
uv sync --group docs --frozen --no-config
uv run --no-config properdocs serve
```

`serve` rebuilds the site as you edit and serves it locally.

Before you push, build it the way CI does:

```bash
uv run --no-config properdocs build --strict
```

`--strict` turns warnings into errors, including broken links and anchors. During a large restructure you can preview with `properdocs serve --no-strict`, but CI is always strict.

`--no-config` keeps your user-level uv settings, such as an extra package index, out of the docs environment.

`docs` is the default dependency group, so a bare `uv sync` installs the same tools. Keep `--frozen --no-config` anyway: without them, a stale lock is silently rewritten using your own uv settings.

## Links

- Link to another page by its path in `docs/`, such as `../user-guide/quickstart.md`. The build checks these links.
- Link to files outside `docs/`, such as the script or a workflow, with a full `https://github.com/Texarkanine/SumMem/blob/main/...` URL. The build cannot check relative links that leave `docs/`.
- Give each fact one home, and link to it from everywhere else.

## Change the build tools

After you change the `docs` group in `pyproject.toml`, lock again:

```bash
uv lock --no-config
uv sync --group docs --frozen --no-config
```

CI checks that `uv.lock` matches `pyproject.toml`, and that it was written by the uv version pinned in `docs.yaml`. Lock with that uv version.

## Publishing

The Docs workflow builds the site, strictly, on every pull request and every push to `main`. It publishes to GitHub Pages when a release is published, or when someone runs the workflow by hand. See [Pull requests and releases](index.md#pull-requests-and-releases).
