# Changelog

## [0.10.0](https://github.com/Texarkanine/SumMem/compare/v0.9.0...v0.10.0) (2026-08-28)


### Features

* **cli:** print Saved. and idle line after successful nap ([#70](https://github.com/Texarkanine/SumMem/issues/70)) ([0e7eeb0](https://github.com/Texarkanine/SumMem/commit/0e7eeb0b4da96df2d33e25222249596639793f79))

## [0.9.0](https://github.com/Texarkanine/SumMem/compare/v0.8.0...v0.9.0) (2026-08-26)


### ⚠ BREAKING CHANGES

* stored nap leaf-set ids are 16 hex. Unmigrated four-part and five-part-64 pairs are invisible until migrate.py rewrites them (nested .tree ids included).

### Features

* store leaf-set ids as 16 hex [[#67](https://github.com/Texarkanine/SumMem/issues/67)] ([#68](https://github.com/Texarkanine/SumMem/issues/68)) ([eeb56bd](https://github.com/Texarkanine/SumMem/commit/eeb56bd2cfb8bb98afbf5e312c42c24473d5c84a))

## [0.8.0](https://github.com/Texarkanine/SumMem/compare/v0.7.0...v0.8.0) (2026-08-26)


### ⚠ BREAKING CHANGES

* Nap pair filenames are five-part (`{seq}-{leafset}-{grain}-{variant}`), not four-part. Unmigrated four-part files are invisible to wake, zoom, and recall. After copying the new script, rewrite existing complete pairs (including nested `.summem` stores). Do not `mv` by hand — the variant tag is a digest of the on-disk pair bytes. From a clone of this repository, with Python 3.11+, run `migrate.py` against the target git root as cwd (the script loads its sibling `summem`):

### Features

* **catalog:** enumerate stores with one git ls-files ([#54](https://github.com/Texarkanine/SumMem/issues/54)) ([ebb2583](https://github.com/Texarkanine/SumMem/commit/ebb25833c457be9e513ab05de334c2419fe995e6))
* drop dataclasses and lazy-import command-only modules ([#57](https://github.com/Texarkanine/SumMem/issues/57)) ([044d4cd](https://github.com/Texarkanine/SumMem/commit/044d4cd8d24cffb60203d665fc6d87d93aa7e047))
* five-part nap stems so same-block folds merge [[#61](https://github.com/Texarkanine/SumMem/issues/61)] ([#62](https://github.com/Texarkanine/SumMem/issues/62)) ([30b8293](https://github.com/Texarkanine/SumMem/commit/30b82938b6d72ae60d9b7b1400be44ee4ae647f2))
* **heal:** walk raw tree JSON for overlap checks ([#56](https://github.com/Texarkanine/SumMem/issues/56)) ([e2d50a4](https://github.com/Texarkanine/SumMem/commit/e2d50a4e4c6c1019dfa34bfeed802e9610df3b38))


### Bug Fixes

* **perf:** unique-prefix once and parse each view tree once ([#55](https://github.com/Texarkanine/SumMem/issues/55)) ([f5bd927](https://github.com/Texarkanine/SumMem/commit/f5bd92763adb3591a90b8e0fbf60397b5972326c))
* **wake:** never drop view nodes to fit WAKE_LINES ([#60](https://github.com/Texarkanine/SumMem/issues/60)) ([dcc27b8](https://github.com/Texarkanine/SumMem/commit/dcc27b88ed7b5abb1f432d8b1df783697f2c28a3))

## [0.7.0](https://github.com/Texarkanine/SumMem/compare/v0.6.0...v0.7.0) (2026-08-25)


### ⚠ BREAKING CHANGES

* Nap captions are `.summ`, not `.sum`. To migrate after copying the new script, rename existing captions (including nested `.summem` stores). You may try running the command below from the root of your repository if you don't want to do it by hand.

### Features

* rename nap captions from .sum to .summ ([#47](https://github.com/Texarkanine/SumMem/issues/47)) ([9325d74](https://github.com/Texarkanine/SumMem/commit/9325d740b00e36b3a76043e6428b0cb3178d7fef))


### Bug Fixes

* **prompt:** Tweak usage instructions a bit on inclusion of memories ([b944f0b](https://github.com/Texarkanine/SumMem/commit/b944f0be54a9a136687bce3037078e65438516da))

## [0.6.0](https://github.com/Texarkanine/SumMem/compare/v0.5.0...v0.6.0) (2026-08-25)


### Features

* print versioned how-to on root wake ([#44](https://github.com/Texarkanine/SumMem/issues/44)) ([15feb23](https://github.com/Texarkanine/SumMem/commit/15feb23887f5a0ccfa48264df21209f853ac302b))

## [0.5.0](https://github.com/Texarkanine/SumMem/compare/v0.4.0...v0.5.0) (2026-08-24)


### Features

* date wake leaves and unify recall/zoom listings ([#37](https://github.com/Texarkanine/SumMem/issues/37)) ([c003779](https://github.com/Texarkanine/SumMem/commit/c0037791f4540cbdacb1d6c4ad1f4d7fd8319006))


### Bug Fixes

* catch _TREE_PARSE_ERRORS in named_ids ([#41](https://github.com/Texarkanine/SumMem/issues/41)) ([6803ac5](https://github.com/Texarkanine/SumMem/commit/6803ac5ef9bf35a4486976b82265a2beeb9d6f69))
* drop unused equal_grain_pair from the driver [[#39](https://github.com/Texarkanine/SumMem/issues/39)] ([#43](https://github.com/Texarkanine/SumMem/issues/43)) ([eefd5e3](https://github.com/Texarkanine/SumMem/commit/eefd5e3b3dbec61e16855bf41baa289973bf7c12))
* include --path on nested-store fold_request Run: line ([#35](https://github.com/Texarkanine/SumMem/issues/35)) ([35f5cd0](https://github.com/Texarkanine/SumMem/commit/35f5cd021114c549439d9fcc185a390885c940f9))
* refuse Python 3.10 before import tomllib ([#42](https://github.com/Texarkanine/SumMem/issues/42)) ([475541f](https://github.com/Texarkanine/SumMem/commit/475541f82d9980e70fed5e08bbf9cafd21d2f506))

## [0.4.0](https://github.com/Texarkanine/SumMem/compare/v0.3.0...v0.4.0) (2026-08-23)


### Features

* **docs:** add AGPL section 7 invocation and 0BSD prompt terms ([#32](https://github.com/Texarkanine/SumMem/issues/32)) ([01f8266](https://github.com/Texarkanine/SumMem/commit/01f826646ba420f195fe97babe4927a618e5a927))

## [0.3.0](https://github.com/Texarkanine/SumMem/compare/v0.2.1...v0.3.0) (2026-08-21)


### Features

* add emergency zipper excision via repo-root surgery.py [[#28](https://github.com/Texarkanine/SumMem/issues/28)] ([#30](https://github.com/Texarkanine/SumMem/issues/30)) ([0c7de72](https://github.com/Texarkanine/SumMem/commit/0c7de727ea5cbfb2ba94f231818e25bcd9c59f84))


### Bug Fixes

* print Saved. after a successful note [[#27](https://github.com/Texarkanine/SumMem/issues/27)] ([#29](https://github.com/Texarkanine/SumMem/issues/29)) ([b350e59](https://github.com/Texarkanine/SumMem/commit/b350e594ee6fd976eda262d262048756c525cd04))

## [0.2.1](https://github.com/Texarkanine/SumMem/compare/v0.2.0...v0.2.1) (2026-08-20)


### Bug Fixes

* label root-wake memories when there is no catalog ([#25](https://github.com/Texarkanine/SumMem/issues/25)) ([42f9566](https://github.com/Texarkanine/SumMem/commit/42f9566d115b6457be15ef87753fb9476149534a))

## [0.2.0](https://github.com/Texarkanine/SumMem/compare/v0.1.0...v0.2.0) (2026-08-20)


### Features

* add summem version and Release Please tags [[#20](https://github.com/Texarkanine/SumMem/issues/20)] ([#22](https://github.com/Texarkanine/SumMem/issues/22)) ([2ab8cd9](https://github.com/Texarkanine/SumMem/commit/2ab8cd9e618532029c4cdc751b4159b400c193b4))
* archive the open-issue-wave L4 ([9b4c83b](https://github.com/Texarkanine/SumMem/commit/9b4c83bbb206f921e558a2260e118c79577aad5a))
* **docs:** sunset VISION and ROADMAP ([#11](https://github.com/Texarkanine/SumMem/issues/11)) ([185c686](https://github.com/Texarkanine/SumMem/commit/185c68689fce65ce3c0eb06313e9d2d008ef50fa))
* first file backend with proofs 1-8 ([#5](https://github.com/Texarkanine/SumMem/issues/5)) ([4b745bf](https://github.com/Texarkanine/SumMem/commit/4b745bffd901fbe68429d96e7d4330253e780193))
* run the test suite with tox on 3.11-3.14 ([#13](https://github.com/Texarkanine/SumMem/issues/13)) ([36d6d14](https://github.com/Texarkanine/SumMem/commit/36d6d14d42eba627974ddd86005acf443d67e181))
* search nested nap captions and warn on skipped packs ([#12](https://github.com/Texarkanine/SumMem/issues/12)) ([d39c1c5](https://github.com/Texarkanine/SumMem/commit/d39c1c507795682916262c623c33bd7e4c11daba))
* ship the root-wake prompt in AGENTS.md ([#10](https://github.com/Texarkanine/SumMem/issues/10)) ([91348b5](https://github.com/Texarkanine/SumMem/commit/91348b563e5fdbac71c1b43f8c9077444dd42ce9))
* split baked note membership onto clone-portability ([#18](https://github.com/Texarkanine/SumMem/issues/18)) ([f3fabfd](https://github.com/Texarkanine/SumMem/commit/f3fabfddcd6df28199006c28442b6a4f6e320e5d))
* tell agents to commit SumMem notes [[#14](https://github.com/Texarkanine/SumMem/issues/14)] ([#15](https://github.com/Texarkanine/SumMem/issues/15)) ([3a9d107](https://github.com/Texarkanine/SumMem/commit/3a9d1074f359a29144fd006d566ca2e7d2082476))
* upload Python coverage to Codecov ([#23](https://github.com/Texarkanine/SumMem/issues/23)) ([1e15d3e](https://github.com/Texarkanine/SumMem/commit/1e15d3e3a70b0c51ddae6a8c899f9a3a3fe1ee0f))


### Bug Fixes

* **ci:** secret/var names ([2759a5f](https://github.com/Texarkanine/SumMem/commit/2759a5f91b6aaeeaa1554cbee4d476f8aca125b8))
* **docs:** add AGPLv3 header to file ([6f81b66](https://github.com/Texarkanine/SumMem/commit/6f81b6695da55df6f461b62eeec32e85c0380a80))
* **docs:** onboarding instructions ([7469dec](https://github.com/Texarkanine/SumMem/commit/7469dec563b5742bb03dacc995b69d9a572a99cf))
* **docs:** tweak system prompt a bit ([9bb4932](https://github.com/Texarkanine/SumMem/commit/9bb49322c20af570e84a41206b2eec44a2ea8a9e))
* ratchet over-long note and nap errors [[#16](https://github.com/Texarkanine/SumMem/issues/16)] ([#17](https://github.com/Texarkanine/SumMem/issues/17)) ([70195c4](https://github.com/Texarkanine/SumMem/commit/70195c4456854c2b7004e7c0b0f7d2e848c907d0))
* ship the agent prompt as a copyable file [[#19](https://github.com/Texarkanine/SumMem/issues/19)] ([#21](https://github.com/Texarkanine/SumMem/issues/21)) ([78d91b7](https://github.com/Texarkanine/SumMem/commit/78d91b7a88140b08d4c91b20fb541b04c7863a19))
