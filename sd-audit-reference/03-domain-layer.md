# 03 — Domain layer

`lib/features/sd_audit/domain/` is the inner-most ring: plain Dart,
no Flutter, no Dio, no ObjectBox. Three sub-trees:

- `entities/` — value objects describing core concepts
- `repositories/` — abstract interfaces that the data layer implements
- `usecases/` — one class per action, each with a single `call(...)` method

Plus `enums/` and `models/` (response DTOs and display models).

Conventions: every repository method returns `Future<Either<Failure,
T>>`; every use case wraps a single repository method (see
[`01-architecture.md`](01-architecture.md)).

## Entities

`domain/entities/` — ~33 plain-Dart classes. Domain entities and
response models are deliberately separated: response DTOs that mirror
the API JSON shape live in `domain/models/response_models/` (and a
parallel set of display models in `domain/models/display_models/`).
The classes listed below are the user-facing domain objects.

| File | Class | Purpose |
|---|---|---|
| `agents_entity.dart` | `AgentEntity` | List of agents + success/status |
| `audit_entity.dart` | `AuditEntity` | Audit data with products and configuration flags |
| `avatar_entity.dart` | `AvatarEntity` | Client avatar (id, url, main flag) |
| `channel_entity.dart` | `ChannelEntity` | List of distribution channels |
| `client_balance_report_entity.dart` | `ClientBalanceReportModel` | Per-client balance with currency breakdown |
| `client_category_entity.dart` | `ClientCategoryEntity` | Client classification categories |
| `clients_entity.dart` | `ClientsEntity` | Aggregates avatars, inventories, client records |
| `comment_entity.dart` | `CommentsEntity` | Visit/audit comments from users |
| `config_entity.dart` | `ConfigEntity` | App config: audit, GPS, photo, order settings |
| `dashboard_data.dart` | `DashboardData` | Sales/visit metrics per agent with style |
| `home_entity.dart` | `HomeEntity` | Home screen aggregate (sales, visits) |
| `info_base.dart` | `InfoBase` | Knowledge base entries (HTML docs) |
| `login_request.dart` | `LoginData` | Login credentials (username, password) |
| `merchand_entity.dart` | `MerchandHomeEntity` | Merchandiser home (totals, clients) |
| `order_report_by_agent_entity.dart` | `OrderReportByAgentEntity` | Order report grouped by agent |
| `order_report_entity.dart` | `OrderReportEntity` | Order report summary and agent table |
| `order_report_request.dart` | `OrderReportRequest` | Request params for order reports |
| `photo_entity.dart` | `PhotoTypesEntity` | Hierarchical photo categories |
| `poll_entity.dart` | `PollEntity` | Polls with questions, variants, metadata |
| `report_client_balance.dart` | `ReportClientBalance` | Client balance report with currency details |
| `report_order.dart` | `ReportOrder` | Order report data structure |
| `report_order_by_agent.dart` | `ReportOrderByAgent` | Order report by agent (alt entity) |
| `report_visit.dart` | `ReportVisit` | Visit report with planned/unplanned + GPS |
| `report_visit_by_agent.dart` | `VisitReportByAgentEntity` | Visit report per agent |
| `server.dart` | `ServerData` | Server connection info (URL, status, name) |
| `server_request.dart` | `ServerRequest` | Request to check server connection |
| `task_entity.dart` | `TaskEntity` | List of tasks assigned to agents |
| `task_types_entity.dart` | `TaskTypesEntity` | Task type catalogue |
| `territory_entity.dart` | `TerritoryEntity` | Geographic territory definitions |
| `update_version.dart` | `UpdateVersion` | App version info with force / recommend flags |
| `user.dart` | `UserData` | Login result: profile + roles + tokens |
| `visit_entity.dart` | `TaskEntity` | Visit message/result wrapper (note: class is misnamed `TaskEntity`) |
| `visit_report_by_agent_entity.dart` | `VisitReportByAgentEntity` | Per-agent visit report with address/status |
| `visit_report_entity.dart` | `VisitReportEntity` | Visit report w/ plan/no-plan breakdown |

> **Naming oddity** — `visit_entity.dart` declares a class called
> `TaskEntity`, colliding with `task_entity.dart`. Both export. Code
> that imports `task_entity.dart` gets the task one; visit code uses
> the visit-file definition. This is a quiet trap during refactors.

## Enums

`domain/enums/` — 10 enums. These drive UI state and DB status fields:

| File | Enum | Values |
|---|---|---|
| `audit_status.dart` | `AuditStatus` | `initial`, `ready`, `success` |
| `comment_status.dart` | `CommentStatus` | `initial`, `ready`, `success` |
| `language_code.dart` | `LanguageCode` | `en`, `uz`, `ru` |
| `note_status.dart` | `NoteStatus` | `initial`, `ready`, `success` |
| `photo_status.dart` | `PhotoStatus` | `initial`, `ready`, `success`, `failed` |
| `poll_status.dart` | `PollStatus` | `initial`, `ready`, `success` |
| `task_status_enum.dart` | `TaskStatusEnum` | `notSynced`, `newTask`, `completed`, `accepted`, `rejected`, `deleted` |
| `user_role.dart` | `UserRole` | `merchandiser`, `supervisor`, `manager` |
| `visit_list_page_enum.dart` | `VisitListPageEnum` | `firstTab`, `secondTab`, `search` |
| `visit_status.dart` | `VisitStatus` | `visiting`, `ready`, `success` |

The `*Status` enums all use roughly the same pattern: `initial` (no
local state yet), `ready` (filled in but not synced), `success` (synced
to server). `PhotoStatus` adds a `failed` value because uploads can
permanently fail (handled by the notification BLoC).

## Repository interfaces

`domain/repositories/` — 25 abstract classes. Grouped by domain area
below; full signatures live in the source. Some clusters are kept in
subfolders (`visit/`, `revise/`, `stock/`).

### Auth / server / user

- **`login_repository.dart`** → `LoginRepository`
  - `checkServer(ServerRequest)` → `ServerData`
  - `loginUser({loginData, serverInfo})` → `UserData`
  - `getSupportData()` → `SupportModel`
- **`common_repository.dart`** → `CommonRepository`
  - `checkUpdateVersion()` → `UpdateVersion`
- **`info_base_repository.dart`** → `InfoBaseRepository`
  - `getInfoBase()` → `InfoBase`

### Clients

- **`client_repository.dart`** → `ClientsRepository`
  - `getClientsData()`, `getVisitsData()`, `getConfigData()`,
    `getNewClientData()`, `getClientsList()`, `getSearchClient(text)`
- **`add_client_repository.dart`** → `AddClientRepository`
  - `getConfigData()`, `getAgents()`, `getChannel()`, `getTerritory()`,
    `getClientCategory()`, `setNewClient(ClientsModelBox)`
- **`client_edit_repositroy.dart`** *(typo in filename, see [`20`](20-known-issues-and-debt.md))* → `ClientEditRepository`
  - `getAgents()`, `getChannel()`, `getTerritory()`,
    `setEditedClient(EditedClientBox)`, `updateClient(ClientsModelBox)`
- **`client_info_repository.dart`** → `ClientInfoRepository`
  - `getAgentsName`, `getClientAvatarUrl`, `getEditedClient`,
    `getClient`, `getAddClient`, `getAgents`, `getAgents2`, `getAgents3`,
    `setAvatar`, `deleteAvatar`, `setMainAvatar`

### Visits

- **`visit_repository.dart`** → `VisitRepository`
  - `getVisitData()`, `getClientData()`, `getConfigData()`
- **`client_visit_repository.dart`** *(older API surface)* → `ClientsVisitRepository`
  - `getVisitData`, `getInitialVisitData`, `getPollData`,
    `getAuditData(clientId)`, `getAllVisitsData`, `getPhotoData(clientId)`,
    `getCommentData(clientId)`, `getClientById(clientId)`
- **`visit/clients_visit_repository.dart`** *(newer, display-model based)* → `ClientsVisitRepository`
  - GPS-validated start: `validateGpsAndStartVisit`, `startVisit`,
    `endVisit`, `deleteVisit`, `updateVisitCheckout`,
    `updatePhotosCheckout`, `updateClientVisitTimes`
  - Visit content: `getAudits`, `getPolls`, `getPhotos`,
    `getCommentStatus`, `getNote`, `saveNote`, `deleteNote`,
    `getPhotoStatus`, `deleteAuditResult`, `deletePollResult`,
    `deleteCommentResult`, `getActiveVisitClientName`,
    `updateAuditResultVisitFinished`, `updatePollResultVisitFinished`,
    `updateVisitTimesForAllResults`, `areRequiredAuditsFilled`,
    `areRequiredPollsFilled`, `getClientAvatarUrl`, `getCurrentPosition`

### Audit / polls / photos / notes / comments

- **`audit_repository.dart`** → `AuditRepository`
  - `getAuditResultData({clientId, auditBox})`,
    `saveAuditData(AuditResultBox)`
- **`polls_repository.dart`** → `PollsRepository`
  - `getPollResult(clientId, pollId)`, `savePollResult(PollResultBox)`
- **`photo_report_repository.dart`** → `PhotoReportRepository`
  - `getPhotoTypes()`, `getVisit(clientId)`, `getPhotoReports(clientId)`,
    `getPhotoReportMap(clientId)`, `addNewPhoto(PhotoBox)`,
    `removePhoto(photoId)`

### Tasks

- **`tasks_repository.dart`** → `TasksRepository`
  - `getTasksData()`, `getAgentsData()`, `getTaskTypeData()`
- **`edit_task_repository.dart`** → `EditTaskRepository`
  - `getTaskType()`, `getAgentsId(clientId?)`, `setTask(TaskBox, clientId)`

### Reports

- **`report_repository.dart`** → `ReportRepository`
  - `getReportClientBalance(BaseParamWithSimpleDate)`
  - `getReportOrder(OrderReportRequest)`
  - `getReportOrderByAgent(OrderReportByAgentParam)`
  - `getReportVisit(BaseParamWithSimpleDate)`
  - `getReportVisitByAgent(VisitReportByAgentParam)`
- **`order_report_local_repository.dart`** → `OrderReportLocalRepository`
  - `getProductCategories()` *(synchronous local read for filter)*

### Dashboard / merch / notification

- **`dashboard_repository.dart`** → `DashboardRepository`
  - `getDashboardData(BaseParamWithDate)`, `getConfigData()`,
    `getUsersListData()`, `logOutUser()`, `sendLocation()`,
    `changeUser(UserModel)`
- **`merchandiser_repository.dart`** → `MerchandiserRepository`
  - `getMerchandiserFromServer()`, `getMerchandiserFromLocal()`,
    `getVisitsData()`
- **`notification_repository.dart`** → `NotificationRepository`
  - `getFailedPhotos()`, `deleteFailedPhoto(id)`,
    `resendFailedPhotos()`, `markAllAsFailed()`

### Sync / GPS / location

- **`synchronization_repository.dart`** → `SynchronizationRepository`
  - `checkToken()`, `getAllData({isNewDay})` *(returns an errorMap)*
- **`track_gps_repository.dart`** → `TrackGpsRepository`
  - `insertLocation({lat, lng, accuracy, gps, time})`,
    `insertTrackGpsWithoutLocation()`,
    `sendLocation(List<TrackGpsBox>)`
- **`get_location_repository.dart`** → `GetLocationRepository`
  - `getLocation(LocationAccuracy)` *(thin wrapper, see [`12`](12-services.md))*

### Stock / revise

- **`stock/stock_repository.dart`** → `StockRepository`
  - `getWarehouse`, `getAllProduct({selectedWarehouse, selectedPriceType})`,
    `getStock`, `getProduct`, `getPriceType`,
    `getProducts({selectedWarehouse, selectedPriceType})`
- **`revise/revise_repository.dart`** → `ReviseRepository`
  - `getReviseData({clientId, dateFrom, dateTo, tradeId?})`,
    `getTradeData()`

## Use cases

`domain/usecases/` — ~80 classes, one per action. Each:

```dart
class FooUsecase {
  final FooRepository _repo;
  FooUsecase(this._repo);

  Future<Either<Failure, T>> call(P param) => _repo.fooMethod(param);
}
```

Some use cases take no parameter; some take a record / model; a few
have explicit named parameters. **A use case is almost always a 1:1
forward to a repository method** — the indirection exists to (a) let
BLoCs depend on a clean unit instead of a multi-method repo, and (b)
allow per-action mocking in tests.

### Catalog (grouped by feature)

| Feature | Use cases |
|---|---|
| Auth | `LoginUsecase`, `CheckServerUsecase`, `LoginSupportUsecase`, `LogoutUsecase`, `CheckTokenUsecase`, `SplashUsecase` |
| Version | `CheckUpdateVersionUsecase` |
| Clients (list) | `ClientsListUsecase`, `ClientsClientDataUsecase`, `ClientsVisitsUsecase`, `ClientsConfigUsecase`, `ClientsNewClientDataUsecase`, `ClientsSearchUsecase` |
| Clients (info / avatars) | `ClientInfoClientUsecase`, `ClientInfoAddClientUsecase`, `ClientInfoAvatarUrlUsecase`, `ClientInfoAgentsUsecase`, `ClientInfoAgentsUsecase2`, `ClientInfoAgentsNameUsecase`, `ClientInfoGetAgentsUsecase`, `ClientInfoGetAgentsUsecase2`, `ClientInfoGetEditedClientUsecase`, `SetAvatarUsecase`, `DeleteAvatarUsecase`, `GetClientByClientIdUsecase` |
| Add new client | `AddClientConfigUsecase`, `AddClientGetAgentDataUsecase`, `AddClientGetCategoryDataUsecase`, `AddClientGetChannelDataUsecase`, `AddClientGetTerritoryDataUsecase`, `AddNewClientUsecase` |
| Edit client | `ClientEditGetAgentsUsecase`, `ClientEditGetChannelsUsecase`, `ClientEditGetTerritoriesUsecase`, `SetEditedClientUsecase`, `UpdateClientUsecase` |
| Visits | `ClientsVisitUsecase` *(facade, returns `ClientVisitData`)*, `ClientVisitGetAllVisitsUsecase`, `VisitDataUsecase`, `VisitInitialDataUsecase`, `VisitGetClientUsecase`, `VisitGetConfigUsecase`, `VisitGetVisitUsecase`, `CommentDataUsecase` |
| Audits | `AuditDataUsecase`, `AuditGetAuditResultUsecase`, `AuditSaveAuditUsecase` |
| Polls | `PollsDataUsecase`, `PollsGetPollResultUsecase`, `PollsSavePollResultUsecase` |
| Photo report | `PhotoDataUsecase`, `PhotoReportPhotoTypesUsecase`, `PhotoReportPhotosUsecase`, `PhotoReportSortedPhotoUsecase`, `PhotoReportVisitUsecase`, `PhotoReportAddNewPhotoUsecase`, `PhotoReportRemovePhotoUsecase` |
| Tasks | `TasksGetTasksUsecase`, `TasksGetAgentsUsecase`, `TasksGetTaskTypesUsecase`, `EditTaskGetTaskTypesUsecase`, `EditTaskGetAgentsIdUsecase`, `EditTaskSetTaskUsecase` |
| Dashboard / merch | `DashboardUsecase`, `DashboardConfigUsecase`, `MerchGetLocalUsecase`, `MerchGetTotalUsecase`, `MerchGetVisitsUsecase`, `ChangeUserUsecase`, `GetUsersListUsecase`, `SendLocationUsecase` |
| Reports | `VisitReportUsecase`, `VisitReportByAgentUsecase`, `OrderReportUsecase`, `OrderReportByAgentUsecase`, `ClientBalanceReportUsecase`, `DateRangeUsecase` |
| Notifications | `NotificationUsecase` |
| Sync | `SynchronizationUsecase` |
| GPS | `InsertLocationUsecase`, `InsertTrackGpsWithoutLocationUsecase`, `SendTrackGpsUsecase` |
| Info base | `InfoBaseUsecase` |
| Stock / revise | `StockUsecase`, `ReviseUsecase` |

### When NOT to add a use case

`OrderReportLocalRepository.getProductCategories()` is invoked
directly by `OrderReportsBloc` without going through a use case
(verified in DI registration). The convention is "one use case per
repo method" but this one was skipped — synchronous, parameterless,
purely local — so don't be surprised by the inconsistency.

## Display models vs entities vs response models

Three coexisting kinds of plain-data objects:

| Kind | Lives in | Role |
|---|---|---|
| Domain entity | `domain/entities/` | Public-facing, used by BLoCs / pages |
| Response model | `domain/models/response_models/` and similar | Mirrors the JSON shape from the API |
| Display model | `domain/models/display_models/` | UI-friendly shape (e.g. `VisitDisplayModel` with computed booleans) |
| ObjectBox box | `lib/db/models/` | Storage shape with annotations + `ToOne`/`ToMany` |

Mappers in [`04-data-layer.md`](04-data-layer.md) translate between
these.
