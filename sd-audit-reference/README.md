# sd_audit_flutter — Reference Documentation

A documentation-grade deep dive into the **sdaudit** Flutter app
(`/Users/abdulbosit/SD-Projects/sd_audit_flutter`, clean architecture,
v3.1.2+25). These docs are additive — no project source files were
changed to produce them.

## How to read these docs

| If you are… | Read in this order |
|---|---|
| New to the project | `00` → `01` → `02` → `16` (key flows) → pick by feature |
| Adding a new feature | `21` (recipe) first, then `03`–`07` for layer rules |
| Debugging a sync / network issue | `09` → `10` → `14` |
| Working on UI / theming | `05` → `11` → `17` |
| Reviewing for security or tech debt | `20`, plus `01` + `09` |

Every file is standalone and cross-links to siblings. Each claim is
backed by a file path (and where useful a line number).

## Table of contents

| # | Doc | What it covers |
|---|---|---|
| — | [README](README.md) | This index |
| 00 | [Overview](00-overview.md) | What the app does, roles, high-level component map |
| 01 | [Architecture](01-architecture.md) | Clean architecture, three layers, dependency rules |
| 02 | [Project structure](02-project-structure.md) | Folder map, naming conventions |
| 03 | [Domain layer](03-domain-layer.md) | Entities, repository interfaces, use cases, enums |
| 04 | [Data layer](04-data-layer.md) | BaseRepositoryImpl, repo impls, data sources, mappers |
| 05 | [Presentation layer](05-presentation-layer.md) | Pages, BLoCs, widgets |
| 06 | [State management](06-state-management.md) | BLoC pattern, `part of`, build/listener/consumer |
| 07 | [Dependency injection](07-dependency-injection.md) | GetIt graph, factory vs singleton |
| 08 | [Databases](08-databases.md) | ObjectBox, Hive, SQLite |
| 09 | [Networking](09-networking.md) | HttpClient, Dio, endpoints, interceptors |
| 10 | [Synchronization](10-synchronization.md) | Sync pipeline, POST→GET ordering, error map |
| 11 | [Theming](11-theming.md) | Token system, dark/light, AdaptiveTheme |
| 12 | [Services](12-services.md) | Location stack, background, Firebase |
| 13 | [Localization](13-localization.md) | easy_localization, uz/ru/en |
| 14 | [Error handling](14-error-handling.md) | Failure hierarchy, Either flow, ApiException |
| 15 | [Navigation](15-navigation.md) | Navigator, navigatorKey, custom routes |
| 16 | [Key flows](16-key-flows.md) | Login, sync, visit, audit, task, photo |
| 17 | [Pages deep dive](17-pages-deep-dive.md) | Per-page purpose, BLoCs, gotchas |
| 18 | [Build and deploy](18-build-and-deploy.md) | flutter commands, codegen, iOS pod |
| 19 | [Testing](19-testing.md) | mocktail/bloc_test, current coverage |
| 20 | [Known issues and debt](20-known-issues-and-debt.md) | SSL bypass, TODOs, typos, dupes |
| 21 | [Feature development guide](21-feature-development-guide.md) | Step-by-step recipe |

## How these docs were generated

Built by reading the project's source verbatim — `main.dart`,
`injection_container.dart`, the ObjectBox class, the synchronization
repository, every BLoC trio, every entity and use case file — and the
existing `CLAUDE.md`, `PROJECT_AUDIT.md`, `THEME_MIGRATION_GUIDE.md`,
and `README.md`. Counts cited in these docs (605 dart files, 27 pages,
35 BLoCs, etc.) come from direct file enumeration at time of writing
(May 2026) and will drift over time.

## Scope and non-goals

- Additive only — no project files were modified.
- No code generation, no dependency upgrades, no analyzer runs.
- The user-facing app strings, Figma designs, and runtime screenshots
  are out of scope.

## A note on existing docs in the project

The project already ships with:

- **`CLAUDE.md`** — concise instructions for Claude Code. Authoritative
  on conventions; these docs expand on them rather than restating them.
- **`PROJECT_AUDIT.md`** — Uzbek high-level inventory and tech-debt
  list. These docs reorganize and translate the actionable parts (see
  [`20-known-issues-and-debt.md`](20-known-issues-and-debt.md)).
- **`THEME_MIGRATION_GUIDE.md`** — mapping of legacy `AppColors`
  identifiers to the new `context.*` tokens. Referenced from
  [`11-theming.md`](11-theming.md).
- **`README.md`** — quick start + codegen edit gotcha. Referenced from
  [`18-build-and-deploy.md`](18-build-and-deploy.md).
