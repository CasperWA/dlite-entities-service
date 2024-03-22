# Changelog

## [v0.2.0](https://github.com/SINTEF/entities-service/tree/v0.2.0) (2024-03-22)

[Full Changelog](https://github.com/SINTEF/entities-service/compare/v0.1.0...v0.2.0)

**Fixed bugs:**

- The pydantic model for `GitLabUserInfo` is too strict [\#83](https://github.com/SINTEF/entities-service/issues/83)
- The cache dir is not being created automatically [\#82](https://github.com/SINTEF/entities-service/issues/82)

**Closed issues:**

- Loosen name regex for retrieving entities [\#90](https://github.com/SINTEF/entities-service/issues/90)
- Minimize code repeats in SOFT models [\#64](https://github.com/SINTEF/entities-service/issues/64)
- Test with different "versions" of entity schemas [\#5](https://github.com/SINTEF/entities-service/issues/5)

**Merged pull requests:**

- Support specific namespaces [\#101](https://github.com/SINTEF/entities-service/pull/101) ([CasperWA](https://github.com/CasperWA))
- Unify entity version and name validation [\#91](https://github.com/SINTEF/entities-service/pull/91) ([CasperWA](https://github.com/CasperWA))
- Clean up authorization models [\#88](https://github.com/SINTEF/entities-service/pull/88) ([CasperWA](https://github.com/CasperWA))
- Try to create cache directory on each CLI call [\#87](https://github.com/SINTEF/entities-service/pull/87) ([CasperWA](https://github.com/CasperWA))
- Separate out entity models in SOFT and DLite [\#74](https://github.com/SINTEF/entities-service/pull/74) ([CasperWA](https://github.com/CasperWA))

## [v0.1.0](https://github.com/SINTEF/entities-service/tree/v0.1.0) (2024-01-31)

[Full Changelog](https://github.com/SINTEF/entities-service/compare/v0.0.1...v0.1.0)

This is the first "proper" release (after v0.0.1).

It introduces several steps up compared to a bare-bones REST API service that started as a way to return the entities from the URI/URL they have defined. Specifically on the onto-ns.com domain under the `/meta` path.

The main upgrade revolves around the CLI, implemented to facilitate uploading entities.
It does so by connecting to the REST API service, authenticating via SINTEF's GitLab OAuth2 flow.

A PyPI release is not planned yet. To install this package run (in a virtual environment):

```console
pip install "entities-service[cli] @ git+https://github.com/SINTEF/entities-service.git"
```

Then run:

```console
entities-service --help
```

To learn more about the CLI.

**Implemented enhancements:**

- Add a release workflow [\#68](https://github.com/SINTEF/entities-service/issues/68)
- Change target for the CLI upload [\#63](https://github.com/SINTEF/entities-service/issues/63)
- Integrate current docker tests into a local pytest runnable environment [\#53](https://github.com/SINTEF/entities-service/issues/53)
- Update to ruff [\#51](https://github.com/SINTEF/entities-service/issues/51)
- Add dependency CI workflows [\#13](https://github.com/SINTEF/entities-service/issues/13)
- Help script for uploading entities [\#12](https://github.com/SINTEF/entities-service/issues/12)

**Fixed bugs:**

- Onto-ns expects entity in the "wrong" format [\#38](https://github.com/SINTEF/entities-service/issues/38)
- Deployment to onto-ns failing due to mishandling URL to MongoDB [\#31](https://github.com/SINTEF/entities-service/issues/31)

**Closed issues:**

- Minimize repo name [\#62](https://github.com/SINTEF/entities-service/issues/62)
- Move repository to SINTEF organization [\#10](https://github.com/SINTEF/entities-service/issues/10)
- Implement CD workflow for deploying updates on onto-ns.com [\#6](https://github.com/SINTEF/entities-service/issues/6)
- Be reasonable regarding version and name regex [\#4](https://github.com/SINTEF/entities-service/issues/4)

**Merged pull requests:**

- Use the more concise 'Entities Service' name throughout [\#70](https://github.com/SINTEF/entities-service/pull/70) ([CasperWA](https://github.com/CasperWA))
- Add a release workflow [\#69](https://github.com/SINTEF/entities-service/pull/69) ([CasperWA](https://github.com/CasperWA))
- New `POST` create entity endpoint - also authentication [\#67](https://github.com/SINTEF/entities-service/pull/67) ([CasperWA](https://github.com/CasperWA))
- Minimal CLI for uploading functionality [\#55](https://github.com/SINTEF/entities-service/pull/55) ([CasperWA](https://github.com/CasperWA))
- Setup unit tests using `pytest` [\#54](https://github.com/SINTEF/entities-service/pull/54) ([CasperWA](https://github.com/CasperWA))
- Update dev tools [\#52](https://github.com/SINTEF/entities-service/pull/52) ([CasperWA](https://github.com/CasperWA))
- Split pydantic models to include SOFT5 as well [\#40](https://github.com/SINTEF/entities-service/pull/40) ([CasperWA](https://github.com/CasperWA))
- Use custom MongoDsn pydantic URL type [\#32](https://github.com/SINTEF/entities-service/pull/32) ([CasperWA](https://github.com/CasperWA))
- Add CI/CD workflows [\#14](https://github.com/SINTEF/entities-service/pull/14) ([CasperWA](https://github.com/CasperWA))
- Add deployment workflow [\#11](https://github.com/SINTEF/entities-service/pull/11) ([CasperWA](https://github.com/CasperWA))
- Enable custom port and user for mongodb + fixed typo in readme [\#9](https://github.com/SINTEF/entities-service/pull/9) ([jesper-friis](https://github.com/jesper-friis))
- Be more specific about the regex for version and name [\#8](https://github.com/SINTEF/entities-service/pull/8) ([CasperWA](https://github.com/CasperWA))
- Include a bit of logging [\#3](https://github.com/SINTEF/entities-service/pull/3) ([CasperWA](https://github.com/CasperWA))
- Add uvicorn worker [\#2](https://github.com/SINTEF/entities-service/pull/2) ([CasperWA](https://github.com/CasperWA))
- Fix new Docker CI test [\#1](https://github.com/SINTEF/entities-service/pull/1) ([CasperWA](https://github.com/CasperWA))

## [v0.0.1](https://github.com/SINTEF/entities-service/tree/v0.0.1) (2023-03-30)

[Full Changelog](https://github.com/SINTEF/entities-service/compare/aabe29f4aa4b20d4c2c3e1b46d0ad20467f6fbfb...v0.0.1)



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
