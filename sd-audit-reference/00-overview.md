# 00 — Overview

## What sdaudit is

`sdaudit` is a Flutter mobile app for **field audit and merchandising**
at retail outlets. Field users (auditors, merchandisers, supervisors)
travel between client locations, check in via GPS, run product audits,
take photos, fill in polls, capture notes, and submit reports. The
server side is the SalesDoc backend (`server.salesdoc.io`).

Project facts (`pubspec.yaml`):

| | |
|---|---|
| Package name | `sdaudit` |
| Version | `3.1.2+25` |
| Dart SDK | `>=3.0.5 <4.0.0` |
| Primary deps | flutter_bloc 9, dio 5, objectbox 5, hive 2, get_it 7 |
| Platforms | Android, iOS, web/desktop scaffolding only |

## Roles

Three values in `domain/enums/user_role.dart`:

- **`supervisor`** — sees the supervisor `DashboardScreen`, manages
  agents, reviews aggregate reports.
- **`manager`** — distinct from supervisor in API but currently lands
  on the same dashboard.
- **`merchandiser`** — sees `MerchandiserDashboardScreen`, focused on
  trade/stock workflows.
- (Plain auditor / agent — not in the enum; routed to `ClientsList`
  directly.)

Role-based routing happens at the end of login (see
[`16-key-flows.md`](16-key-flows.md)).

## What users do — five core flows

1. **Login** — server URL → credentials → role → first data download.
2. **Sync** — POST any pending local changes then GET fresh server
   state. Triggered on day rollover, on cold start, manually, and on
   app resume.
3. **Visit** — pick a client → check in (GPS validated) → audit /
   photos / polls / note / comment → check out → photos and results
   get a check-out timestamp.
4. **Task** — supervisor creates tasks for agents; agents see and
   complete them.
5. **Report** — client balance, order, visit reports queried on demand
   by date range.

Each is broken down with sequence diagrams in
[`16-key-flows.md`](16-key-flows.md).

## High-level component map

```mermaid
flowchart TB
    UI[Flutter UI<br/>Pages + Widgets]
    BLOC[BLoCs<br/>35 of them]
    UC[Use cases<br/>~80]
    REPO[Repository interfaces<br/>~25]
    IMPL[Repository impls<br/>~25]
    DS_R[RemoteDataSourceImpl<br/>34 methods]
    DS_OB[ObjectBox<br/>36 boxes]
    DS_H[Hive<br/>GeneralBox]
    DS_SQL[SQLite<br/>users + GPS]
    API[(server.salesdoc.io)]

    UI -->|events| BLOC
    BLOC -->|call()| UC
    UC --> REPO
    REPO -.implements.-> IMPL
    IMPL --> DS_R
    IMPL --> DS_OB
    IMPL --> DS_H
    IMPL --> DS_SQL
    DS_R --> API
```

Dependency rule: every arrow points downward and outward (presentation
→ domain → data); domain never depends on data or presentation. See
[`01-architecture.md`](01-architecture.md) for the rule in detail.

## Where things live

A four-line answer for newcomers:

- **Feature module** — `lib/features/sd_audit/` (everything user-facing).
- **DB schemas** — `lib/db/` (ObjectBox + Hive + SQLite).
- **Shared utilities** — `lib/common/` (endpoints, background service).
- **App entrypoint** — `lib/main.dart` + `lib/injection_container.dart`.

Full folder map in [`02-project-structure.md`](02-project-structure.md).

## What sdaudit relies on

| Concern | Library | Notes |
|---|---|---|
| State | `flutter_bloc` 9.x | Events/states declared via `part of` |
| DI | `get_it` 7.x | Set up in `lib/injection_container.dart` |
| FP | `dartz` | All repos return `Either<Failure, T>` |
| HTTP | `dio` 5.x | Custom `HttpClient` wrapper, 40s timeouts |
| Storage | `objectbox` 5.x, `hive` 2.x, `sqflite` | Three persistence systems, see [`08`](08-databases.md) |
| L10n | `easy_localization` | `assets/translations/*.json` |
| Theme | `adaptive_theme` | System / light / dark |
| Maps | `flutter_map` + `geolocator` | OSM tiles, GPS via geolocator |
| Push / crash | `firebase_messaging`, `firebase_crashlytics` | Wired in `main.dart` |
| Image cache | `fast_cached_network_image` (+legacy `cached_network_image`) | Two libs co-exist, see [`20`](20-known-issues-and-debt.md) |
