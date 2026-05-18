---
title: client/oddment
sidebar_position: 5
---

# `client/oddment` — a newer end-to-end feature

This is the per-client "oddment" tracking flow — recording how many product units the client has in stock at the time of the visit. It exists alongside the agent's own `oddments` tab on `MainPage` (which tracks the agent's container/stock inventory).

Worth using as a reference example because it's a **complete end-to-end vertical slice** added in DB schema **v13** (mid-2024-ish). Everything is there: entity, DAO, relation view, service, repository, mapper, use cases, BLoC, page, dashboard, history, detail, manage. If you want to see how the full pattern looks for a feature that wasn't grafted on top of legacy code, this is the cleanest one.

## File map

```
lib/presentation/features/client/oddment/
├── dashboard/              # ClientOddmentDashboardPage + bloc
├── detail/                 # ClientOddmentDetailPage + bloc
├── history/                # history list + detail
├── list/                   # ClientOddmentListPage + bloc
└── manage/                 # ClientOddmentManagePage + bloc (create/edit)

lib/data/data_source/database/
├── entity/client/oddment/
│   ├── client_oddment_entity.dart           # the parent record
│   └── client_oddment_product_entity.dart   # line items
├── relation/client/oddment/
│   └── product/                             # joined view models
└── dao/client/oddment/
    ├── client_oddment_dao.dart
    └── client_oddment_product_dao.dart

lib/data/data_source/service/oddment/
└── client_oddment_service.dart              # thin Dio wrapper

lib/data/repository_impls/client/oddment/
└── client_oddment_repository_impl.dart

lib/domain/usecase/oddments/                 # interfaces + impls
└── … (dashboard, manage, detail, list, history use cases)

lib/domain/mapper/oddment/                   # entity → domain extensions

lib/domain/common/stream/client/oddment/
└── update_client_oddment_stream_controller.dart  # cross-feature notification
```

## Database

Two tables added in `migration_helper.dart` v12→v13:

```sql
CREATE TABLE IF NOT EXISTS client_oddment (
  client_oddment_id TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  created_at TEXT NOT NULL,
  total_count_products REAL NOT NULL,
  comment TEXT NOT NULL,
  state TEXT NOT NULL,
  type TEXT NOT NULL,
  consignation INTEGER NOT NULL,
  finished INTEGER NOT NULL,
  location_id TEXT NOT NULL,
  is_sync INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS client_oddment_product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id TEXT NOT NULL,
  client_oddment_id TEXT NOT NULL,
  category_id TEXT NOT NULL,
  total_blocks REAL NOT NULL,
  total_pcs REAL NOT NULL,
  total_items REAL NOT NULL,
  pack_quantity REAL NOT NULL
);
```

The entity:

```dart
// lib/data/data_source/database/entity/client/oddment/client_oddment_entity.dart
@Entity(tableName: 'client_oddment')
class ClientOddmentEntity {
  @PrimaryKey()
  @ColumnInfo(name: "client_oddment_id")
  final String clientOddmentId;

  @ColumnInfo(name: "client_id")
  final String clientId;

  @ColumnInfo(name: "created_at")
  final String createdAt;

  // … total_count_products, comment, state, type, consignation, finished,
  //    location_id, is_sync
}
```

Default `is_sync = 0` — newly-created oddment records are unsynced from the start; they enter the sync flow at the next `_sendClientOddments` step ([07-synchronize §The chain](../07-synchronize.md#the-chain-in-order), step 7).

## Relation view

`lib/data/data_source/database/relation/client/oddment/product/client_oddment_product_entity_relation.dart` joins `client_oddment_product` against `product` and `product_category` so the UI gets product name + category name without a separate query per row. Listed in `AppDatabase.@Database(views: [...])`.

## DAO

`ClientOddmentDao` and `ClientOddmentProductDao` follow the standard DAO shape (`@Insert`, `@Query`, `@Delete`, `Stream` returns). Notably:

- `getNotSyncedClientOddments()` — for the sync pipeline.
- `observeOddmentsByClientId(clientId)` — Stream the list for the client-detail page to react in real time.

## Service

`lib/data/data_source/service/oddment/client_oddment_service.dart` — thin Dio wrapper around the `/oddments` endpoint family. POST to sync, GET to refresh server-side state. Returns raw `Response`.

Registered in `service_module.dart:98-99` against `localDio`:

```dart
registerLazySingleton<ClientOddmentService>(
  () => ClientOddmentService(dio: get<Dio>(instanceName: localDio)),
);
```

## Repository

`lib/data/repository_impls/client/oddment/client_oddment_repository_impl.dart` composes the service + the two DAOs + relevant preferences + mapper extensions. Registered as a `registerLazySingleton` in `repository_module.dart:522-530`.

Implements `ClientOddmentRepository` from `lib/domain/repositories/client/oddment/`.

## Mapper

`lib/domain/mapper/oddment/client_oddment_mapper.dart` (extension on `ClientOddmentEntityRelation`, similar to `ClientMapper`):

```dart
extension ClientOddmentRelationMapper on ClientOddmentEntityRelation {
  ClientOddment toClientOddment() { … }
}
```

Plus the inverse (`ClientOddment.toEntity()`) and request mappers for the POST payload.

## Use cases

Under `lib/domain/usecase/oddments/` — one use case per page:

- `ClientOddmentDashboardUseCase` — list aggregation for the dashboard view
- `ClientOddmentListUseCase` — per-client list, with filtering and search
- `ClientOddmentManageUseCase` — create/edit form support (load existing, save, validate)
- `ClientOddmentDetailUseCase` — single-record detail
- `ClientOddmentHistoryUseCase` — history list

Registered as `registerFactory` in `use_case_module.dart`.

## Pages and BLoCs

```
ClientOddmentDashboardPage  →  ClientOddmentDashboardBloc
ClientOddmentListPage       →  ClientOddmentListBloc
ClientOddmentManagePage     →  ClientOddmentManageBloc  (create + edit modes)
ClientOddmentDetailPage     →  ClientOddmentDetailBloc
ClientOddmentHistoryPage    →  ClientOddmentHistoryBloc
```

Each follows the [04-presentation-layer](../04-presentation-layer.md) page pattern: `@RoutePage()` annotation, `late final _bloc`, `initState` dispatching an init event, `dispose` closing the BLoC, `BlocProvider` + `BlocConsumer` in `build`.

Routes registered in `app_router.dart`:

```dart
AutoRoute(page: ClientOddmentDashboardRoute.page),
AutoRoute(page: ClientOddmentManageRoute.page),
// detail, history, list also present
```

## Cross-feature notification

`UpdateClientOddmentStreamController` exists for cross-feature signaling — see [06-streams-and-cross-feature §UpdateClientOddmentStreamController](../06-streams-and-cross-feature.md#updateclientoddmentstreamcontroller). It's listened by:

- `client_oddment_detail_page.dart:63`
- `client_oddment_list_page.dart:71`

Emitters are inside the oddment management flow (manage page's save handler). When the user saves a new oddment, those two pages refresh themselves.

The manage page also emits to `UpdateClientDetailActionStreamController` so the per-client detail view's "oddments" tab badge updates:

```dart
// client_oddment_manage_bloc.dart:275 (approx)
updateClientDetailStreamController.add(DeleteAction.none);
```

And `ClientOddmentListBloc` does the same on certain operations:

```dart
// client_oddment_list_bloc.dart:93, :121
updateClientDetailStreamController.add(DeleteAction.none);
```

## Sync integration

In the sync pipeline, oddments are sent at step 7:

```
… → _sendClientOddments() → synchronizeUseCase.sendClientOddmentsAndClear() → …
```

`sendXAndClear` semantics (see [07-synchronize §Naming convention](../07-synchronize.md#naming-convention-on-synchronizeusecase)): POST unsynced rows, delete them locally on success. Oddments are a once-and-done write — once the server has them, the device doesn't need them anymore (they show up in subsequent client info pulls if needed for display).

## Why this is a good template

If you're adding a new feature with the same shape (per-client write-side data, syncs to server, has dashboard + list + detail + manage screens), copy this feature's structure exactly:

1. **DB**: entity + product/line entity + relation view + DAO + DAO migration. Add to `AppDatabase.@Database(entities: [...], views: [...])` and `_setupDaoLocator`.
2. **Service**: one Dio wrapper class.
3. **Repository**: implements `lib/domain/repositories/<feature>/` interface; composes service + DAOs + preferences + mapper.
4. **Use cases**: one per page; group under `lib/domain/usecase/<feature>/`. Registered as `registerFactory`.
5. **Pages and BLoCs**: dashboard / list / manage / detail / history. Each follows the [04-presentation-layer](../04-presentation-layer.md) page pattern.
6. **Routes**: `AutoRoute(page: XxxRoute.page)` in `app_router.dart`. Run build_runner.
7. **Cross-feature signal**: a `BaseStreamController<void>` subclass. Register in `stream_controller_module.dart`. Emit from save handlers; listen from any page that needs to refresh.
8. **Sync integration**: add a `getNotSyncedX` DAO method, a `sendXAndClear` use-case method, and a step in `SynchronizeBloc`'s chain + matching `SyncType` enum value + `_retryData` case ([07-synchronize](../07-synchronize.md)).
9. **Migration**: bump `@Database(version: ...)` and append a `Migration(N, N+1, ...)` to `migration_helper.dart` + `resultMigration`.
10. **Tests**: BLoC test, use case test, mapper test, widget test.

The orchestrator's "Full Parallel Pipeline" at the top of `CLAUDE.md` codifies this exact flow for AI agents.
