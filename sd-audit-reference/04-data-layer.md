# 04 — Data layer

`lib/features/sd_audit/data/` implements the domain repository
interfaces. It has three sub-trees:

- `repositories/` — `*Impl` classes that extend `BaseRepositoryImpl`
- `data_sources/` — remote (HTTP) and local (SQLite) data sources
- `mapper/` — static converters between Box ↔ Entity ↔ Display
- `model/` — request param classes consumed by repos

## `BaseRepositoryImpl` — the error-mapping contract

Every repository impl extends `BaseRepositoryImpl` and uses one of two
helpers. The whole class is small enough to reproduce verbatim:

```dart
abstract class BaseRepositoryImpl {
  final NetworkInfo? networkInfo;
  BaseRepositoryImpl([this.networkInfo]);

  Future<Either<Failure, T>> workWithServer<T>(Chooser<T> chooser) async {
    try {
      final response = await chooser();
      return Right(response);
    } on DioException catch (e) {
      if (e.type == DioExceptionType.connectionError) {
        if (e.message?.contains('No internet') == true ||
            e.message == 'check_internet') {
          return const Left(NetworkFailure('check_internet'));
        }
      }
      return Left(ServerFailure(
        e.message ?? 'Server xatosi',
        statusCode: e.response?.statusCode,
      ));
    } on ApiException catch (e) {
      if (e.message.toLowerCase().contains('internet') ||
          e.message.toLowerCase().contains('connection')) {
        return Left(NetworkFailure(e.message));
      }
      return Left(ServerFailure(e.message, statusCode: e.statusCode));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  Future<Either<Failure, T>> workWithLocal<T>(Chooser<T> chooser,
      {ErrorHandler? onError}) async {
    try {
      final response = await chooser();
      return Right(response);
    } catch (e) {
      if (kDebugMode) print("Local Exception: ${e.toString()}");
      if (onError != null) await onError.call(e.toString());
      return Left(LocaleFailure(e.toString()));
    }
  }

  Future<T> workWithError<T>(Chooser<T> chooser,
      {ErrorHandler? onError}) async {
    try {
      return await chooser();
    } catch (e) {
      if (kDebugMode) print("With Error: ${e.toString()}");
      await onError?.call(e.toString());
      rethrow;
    }
  }
}
```

**The contract:**

| Helper | Use for | Failure on error |
|---|---|---|
| `workWithServer` | calls that go to the network | `NetworkFailure` (no internet) or `ServerFailure` (HTTP / API) |
| `workWithLocal` | calls that only touch ObjectBox / Hive / SQLite | `LocaleFailure` (typo for "Local", carried through codebase) |
| `workWithError` | rare: rethrows after optional `onError` callback | n/a — returns raw `T`, not Either |

Implications:

1. **Repositories never `try/catch` manually.** Every method body is a
   one-liner: `workWithServer(() async { ... })`.
2. **`DioException` and `ApiException` are caught here and only here.**
   Anything else escapes as `ServerFailure(e.toString())`.
3. **The sentinel `'check_internet'`** flows from `HttpClient` →
   `DioException.message` → here → `NetworkFailure('check_internet')`
   → `.tr()` in the UI. Don't translate it inside the data layer.
4. **`LocaleFailure`** is the misspelling of "LocalFailure". The class
   name is wrong but baked in; don't rename without grepping for every
   `LocaleFailure` reference.

## Repository implementations

All under `lib/features/sd_audit/data/repositories/`. Each implements
its matching interface in `domain/repositories/`.

| File | Class | Interface | Constructor deps |
|---|---|---|---|
| `add_client_repository_impl.dart` | `AddClientRepositoryImpl` | `AddClientRepository` | uses global `objectBox` |
| `audit_repository_impl.dart` | `AuditRepositoryImpl` | `AuditRepository` | uses global `objectBox` |
| `base_repository_impl.dart` | (abstract base) | n/a | optional `NetworkInfo` |
| `client_edit_repository_impl.dart` | `ClientEditRepositoryImpl` | `ClientEditRepository` | none |
| `client_info_repository_impl.dart` | `ClientInfoRepositoryImpl` | `ClientInfoRepository` | `RemoteDataSources`, `NetworkInfo` |
| `client_repository_impl.dart` | `ClientsRepositoryImpl` | `ClientsRepository` | none |
| `common_repository_impl.dart` | `CommonRepositoryImpl` | `CommonRepository` | `RemoteDataSources` |
| `dashboard_repository_impl.dart` | `DashboardRepositoryImpl` | `DashboardRepository` | `RemoteDataSources`, `UserDataSources`, `TrackGpsDataSource`, `NetworkInfo` |
| `edit_task_repository_impl.dart` | `EditTaskRepositoryImpl` | `EditTaskRepository` | none |
| `get_location_repository_impl.dart` | `GetLocationRepositoryImpl` | `GetLocationRepository` | (geolocator package) |
| `info_base_repository_impl.dart` | `InfoBaseRepositoryImpl` | `InfoBaseRepository` | `RemoteDataSources`, `NetworkInfo` |
| `login_repository_impl.dart` | `LoginRepositoryImpl` | `LoginRepository` | `RemoteDataSources`, `NetworkInfo` |
| `merchandiser_repository_impl.dart` | `MerchandiserRepositoryImpl` | `MerchandiserRepository` | `RemoteDataSources`, `NetworkInfo` |
| `notification_repository_impl.dart` | `NotificationRepositoryImpl` | `NotificationRepository` | `RemoteDataSources`, `NetworkInfo` |
| `order_report_local_repository_impl.dart` | `OrderReportLocalRepositoryImpl` | `OrderReportLocalRepository` | none |
| `photo_report_repository_impl.dart` | `PhotoReportRepositoryImpl` | `PhotoReportRepository` | none |
| `polls_repository_impl.dart` | `PollsRepositoryImpl` | `PollsRepository` | none |
| `report_repository_impl.dart` | `ReportRepositoryImpl` | `ReportRepository` | `RemoteDataSources`, `NetworkInfo` |
| `revise/revise_repository_impl.dart` | `ReviseRepositoryImpl` | `ReviseRepository` | `RemoteDataSources`, `NetworkInfo` |
| `stock/stock_repository_impl.dart` | `StockRepositoryImpl` | `StockRepository` | none |
| `synchronization_repository_impl.dart` | `SynchronizationRepositoryImpl` | `SynchronizationRepository` | `RemoteDataSources`, `NetworkInfo` (1,448 lines — see [`10`](10-synchronization.md)) |
| `tasks_repository_impl.dart` | `TasksRepositoryImpl` | `TasksRepository` | none |
| `track_gps_repository_impl.dart` | `TrackGpsRepositoryImpl` | `TrackGpsRepository` | `RemoteDataSources` |
| `visit/clients_visit_repository_impl.dart` | `ClientsVisitRepositoryImpl` | `ClientsVisitRepository` (visit/) | uses global `objectBox` |
| `visit_repository_impl.dart` | `VisitRepositoryImpl` | `VisitRepository` | none |

**Patterns:**

- Repos that talk to the API take `RemoteDataSources` + `NetworkInfo`.
- Repos that only read/write local DBs take **no** constructor deps
  and use the global `objectBox` instance from `lib/main.dart` /
  `lib/features/sd_audit/utils/objects.dart`.
- That global access is convenient but couples local repos to a
  process-wide singleton; testing them requires either an isolated
  ObjectBox or stubbing the global.

## Data sources

### Remote: `RemoteDataSources` (interface + `Impl`)

File: `lib/features/sd_audit/data/data_sources/remote_data_source/remote_data_sources.dart`,
**801 lines.** Lines 29–125 are the abstract interface; 127–801 are
the impl.

The interface has **34 methods** that fall into clusters:

| Cluster | Methods |
|---|---|
| Auth / user | `getSupportData()`, `checkServer({data})`, `loginUser({data, url})`, `profile({data})`, `getAvatar(url)` |
| Reports (server-rendered) | `getVisitReport({param})`, `getOrderReport({param})`, `getClientBalanceReport({param})`, `getVisitReportByAgent({param})`, `getOrderReportByAgent({param})`, `getDashboardData({param})`, `getMerchandiserDashboardData()` |
| Generic GETs | `getDataFromServer({param, api})`, `getConfigDataFromServer({param, api})`, `getMerchandDataFromServer({param, api})`, `getConfigData({param})` |
| Tasks | `getTaskList({header, param, api})`, `sendTaskDataToServer({api, params, extra})` |
| Generic POSTs | `sendDataToServer({api, params})`, `sendLocation({param})` |
| Photos | `sendPhotoToServer({setPhotoRequest})` |
| Avatars | `sendClientAvatar({param})`, `deleteClientAvatar({param})`, `setMainClientAvatar({param})` |
| Knowledge / version | `getKnowledge({deviceToken})`, `checkUpdateVersion({device, version})` |
| Stock / catalog | `getStockFromServer()`, `getPriceFromServer()`, `getPriceTypeFromServer()`, `getProductCategoryFromServer()`, `getWarehouseFromServer()`, `getProductFromServer()` |
| Trade / revise | `getTradeFromServer()`, `getReviseFromServer({clientId, dateFrom, dateTo, tradeId?})` |

The impl uses `HttpClient` (see [`09-networking.md`](09-networking.md))
and exposes getters `serverUrl`, `positionId`, `token`, `userId` that
read from `UserDataSourceImpl` / `Config`.

**This is the central "god object" of the data layer.** Any new
network call is added here, in both the interface and the impl. The
file's size (801 lines) is a warning — splitting it by cluster is a
plausible refactor (see [`20`](20-known-issues-and-debt.md)).

### Local data sources

`lib/features/sd_audit/data/data_sources/local_data_sources/`

| File | Class | Backed by | Surface |
|---|---|---|---|
| `user_data_sources.dart` | `UserDataSourceImpl` | SQLite | `insertUserData`, `getUser`, `getAllUsers`, `setUsersNotSelected`, `removeUser`, `clearDB`, `close`, `deleteUserData` |
| `track_gps_data_sources.dart` | `TrackGpsDataSourceImpl` | SQLite | `insertOrUpdateTrackGpsData`, `getMaxId`, `trackGpsDataList`, `updateAndReturnFirst20Records`, `deleteTrackGpsData20`, `deleteAllTrackGpsData`, `removeUser`, `close` |

Why SQLite for these two and ObjectBox for everything else? They
predate the ObjectBox migration; they're isolated, small, and
relational enough that nobody felt the need to port them. There's no
strong reason to leave them this way long-term.

## Mappers

`lib/features/sd_audit/data/mapper/` — static-method classes.

| File | Class / extension | Method pattern |
|---|---|---|
| `client_visit_mapper.dart` | `ClientVisitMapper` (abstract, static) | `visitBoxToDisplayModel`, `displayModelToVisitBox`, `clientBoxToDisplayModel`, `auditBoxToDisplayModel`, `pollBoxToDisplayModel`, `noteBoxToDisplayModel`, `displayModelToNoteBox`, `commentBoxToDisplayModel`, `photoBoxToDisplayModel`, plus `*ListToDisplayModelList` variants |
| `client_form_mapper.dart` | `ClientFormMapper` (abstract final) | `agentToDisplayModel`, `agentsToDisplayModels`, `channelToDisplayModel`, `channelsToDisplayModels`, `territoryToDisplayModel`, `territoriesToDisplayModels`, `categoryToDisplayModel`, `categoriesToDisplayModels`, `configToDisplayModel`, `clientBoxToDisplayModel`, `saveDataToNewClientBox`, `saveDataToEditClientBox` |
| `revise/revise_mapper.dart` | (extensions) | `ReviseResponse.toBox`, `ReviseBox.toDisplay` |
| `revise/trade_mapper.dart` | `TradeMapper`, `TradeMapper2` (extensions) | `TradeResponse.toBox()`, `TradeBox.toDisplay()` |
| `stock/stock_mapper.dart` | `StockMapper`, `StockMapper2` (extensions) | `StockResponse.toBox()`, `StockBox.toDisplay()` |
| `stock/price_mapper.dart` | `PriceMapper`, `PriceMapper2`, `PriceMapper3`, `PriceMapper4` (extensions) | Layered: response→box→display for both `PriceBox` and `PriceTypeBox` |
| `stock/product_mapper.dart` | `ProductMapper` (extension) | `ProductResponse.toBox()` etc. |
| `stock/product_category_mapper.dart` | `ProductCategoryMapper` (extension) | `ProductCategoryResponse.toBox()` etc. |
| `stock/warehouse_mapper.dart` | `WarehouseMapper`, `WarehouseMapper2`, `WarehouseMapper3` (extensions) | response↔box↔display |

**Pattern: `{source}To{target}`.** The newer stock/revise mappers use
Dart extensions (`.toBox()`, `.toDisplay()`) instead of static methods
on a named class. Both styles co-exist.

The trailing digit on extension names (`PriceMapper2`,
`WarehouseMapper3`) is the standard workaround for the Dart limitation
that two extensions can't have the same name and target different
types in the same library — one extension per source type, numbered
to disambiguate.

## Request / param models

`lib/features/sd_audit/data/model/`

- `user_model.dart` — `UserModel` (carries token + role; persisted via
  SQLite)
- `support_model.dart` — login support info (e.g. server URL display)
- `update_version_response.dart` — DTO for `checkUpdateVersion`
- `base_params/` — 20+ request param classes (`BaseParam`,
  `BaseParamWithDate`, `BaseParamWithSimpleDate`, `ConfigBaseParam`,
  `OrderReportRequest`, `OrderReportByAgentParam`,
  `VisitReportByAgentParam`, `SetAvatarParam`, `DeleteAvatarParam`,
  `SetMainAvatarParam`, `SetPhotoRequest`, `PostAuditResultParam`, …)

The `BaseParam*` family encapsulates "common request fields like
token, version, language" so individual call sites don't have to
repeat them.

## Empty / placeholder folders

Per the survey:

- `data_sources/db/` — empty (legacy)
- `data_sources/database/main_objectbox/entities/client/` — empty
  scaffolding from an aborted refactor

Safe to delete, but they're harmless. Confirm before removing.
