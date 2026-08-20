# Project Brief: version-tracking

Instrument [SumMem#20](https://github.com/Texarkanine/SumMem/issues/20): Release Please so `main` remains copyable and the repo also gets semantically versioned tags.

## Requirements

- Keep `summem` as one file. Do not split the driver.
- Release Please extra-files (stockroom generic-file pattern) bump a version variable *inside that script*.
- The script reports that version as `summem version` or `summem --version`, whichever fits the existing CLI.
- Match sibling Release Please config (`../inquirerjs-checkbox-search`, `../jekyll-mermaid-prebuild`, `../stockroom`): same PR header (`:service_dog: I have created a release *bark* *woof*`).
- Helper-bot token pattern: repository variable `HELPER_APP_ID` and repository secret `HELPER_APP_PRIVATE_KEY` (stockroom / jekyll-mermaid-prebuild). Operator provisions these after merge.
- Adhere to those repos' existing patterns unless they cannot work here.
- No Dependabot.

## Success

A Release Please workflow on `main` can open a release PR that tags a semver release and updates the in-script version. `summem` prints that version through the chosen CLI surface.
