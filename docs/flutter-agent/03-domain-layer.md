---
title: Domain layer
sidebar_position: 3
---

# Domain layer

`lib/domain/` holds the business contracts: models, repository interfaces, use cases, mappers, plus cross-feature stream controllers and notifiers. It has no Flutter dependency, no Dio, no Floor — anything that imports `package:flutter/` or `lib/data/` belongs elsewhere. **Exception**: mappers (`lib/domain/mapper/`) live here for proximity to the domain models they produce, even though they import data-layer entities.

```
lib/domain/
├── common/        # cross-feature StreamControllers, notifiers, exceptions
├── manager/       # stateful service contracts (LocationRepository)
├── mapper/        # entity/response → domain-model extensions
├── model/         # local/, request/, response/ models
├── repositories/  # 35 abstract repository interfaces (data layer implements)
└── usecase/       # 33 feature directories of use cases (interface + impl)
```

Inventory:

| Folder | Count |
|--------|-------|
| `model/local/*.dart` | 232 files, 61 directories |
| `model/request/*.dart` | 39 files |
| `model/response/*.dart` | 182 files |
| `repositories/*/` | 35 directories |
| `usecase/*/` | 33 directories |
| `mapper/*/` | 91 directories, 85 files |

## Models

Three flavors, separated by purpose:

- **`model/local/`** — domain entities used by use cases, BLoCs, and widgets. Immutable, with `copyWith`, factory `.empty()`, and computed getters.
- **`model/request/`** — payload shapes for outgoing HTTP requests. Have a `toJson()` method; usually mutable for incremental construction.
- **`model/response/`** — payload shapes for incoming HTTP responses. Have a `fromJson()` factory or named constructor; the same file often defines the request *or* response twin for an endpoint.

### Local model — `Client`

`lib/domain/model/local/client/client.dart` is the largest local model in the app (80+ fields). Shape:

```dart
class Client {
  String clientId;
  String clientName;
  String firmName;
  String address;
  List<WeekDays> visitDates;
  String visitType;
  // … many more fields

  Client({
    required this.clientId,
    required this.clientName,
    required this.firmName,
    required this.address,
    // …
    this.verifyStatus = AppConst.CLIENT_VERIFY_STATUS_VERIFIED,
    // sensible defaults for many fields
  });

  Client copyWith({
    double? balance,
    int? consignmentPeriod,
    String? maxDebtDay,
  }) {
    return Client(
      clientId: clientId,
      clientName: clientName,
      // … every field, with overrides
      balance: balance ?? this.balance,
      consignmentPeriod: consignmentPeriod ?? this.consignmentPeriod,
      maxDebtDay: maxDebtDay ?? this.maxDebtDay,
    );
  }

  Client.empty() : this(
    clientId: "",
    clientName: "",
    // … zero-valued instance
  );

  bool get isHaveLocation =>
      (double.tryParse(lat) ?? 0) != 0.0 && (double.tryParse(lon) ?? 0) != 0.0;
}
```

Conventions:
- Required-fields go first in the constructor; optional fields after, with defaults.
- `copyWith` lists only fields that callers commonly mutate — not every field. If you need to change a field that `copyWith` doesn't expose, add the parameter rather than working around it.
- `Client.empty()` is a factory-style named constructor used by mappers when a row is missing (`event != null ? event.toClient() : Client.empty()`). Never `null` flows through the system.
- Computed getters (`isHaveLocation`, `hasAnyVisitOperation`, `debtDaysRemaining`) live on the model so the same logic doesn't get reinvented in every widget.

### Request model — `OrderRequest`

`lib/domain/model/request/order/order_request.dart`:

```dart
class OrderRequest {
  final String requestId;
  final String mobileUuid;
  final String clientId;
  final String? dateLoad;
  final String storeId;
  final String tradeId;
  final String priceTypeId;
  final String bonusType; // 'auto' | 'manual' | 'none'
  final List<String> bonusIds;
  final String? manualDiscountId;
  final int? noteId;
  final String createdAt;
  final String? comment;
  final List<int> tagIds;
  final List<OrderProductRequest> products;
  final LocationActionRequest? locationActionRequest;
  final List<OrderBonusRequest>? bonusProductList;

  OrderRequest({
    required this.requestId,
    required this.mobileUuid,
    required this.createdAt,
    // …
    this.tagIds = const [],
    this.bonusIds = const [],
  });

  Map<String, dynamic> toJson() {
    return {
      'request_id': requestId,
      'mobile_uuid': mobileUuid,
      'comment': comment,
      'tag_ids': tagIds,
      'client_id': clientId,
      // …
      'products': products.map((e) => e.toJson()).toList(),
    };
  }
}
```

Nested request types (`OrderProductRequest`, `OrderBonusRequest`, `LocationActionRequest`) live in the same `request/order/` directory and serialize the same way. Repositories build these with `Order.toRequest()` mappers and hand them to services as `request.toJson()`.

### Response models

Simpler — usually mutable with nullable fields and a `fromJson()` factory:

```dart
// lib/domain/model/response/login/login_request.dart
class LoginRequest {
  String? login;
  String? password;
  String? app;
  String? deviceModel;
  String? deviceId;

  LoginRequest({this.login, this.password, this.app, this.deviceModel, this.deviceId});

  Map<String, dynamic> toJson() => {
    'login': login,
    'password': password,
    'app': app,
    'deviceModel': deviceModel,
    'deviceId': deviceId,
  };
}
```

(Note the file is under `response/login/` even though the class is a request — the directory groups everything related to the `login` endpoint. Don't try to be clever about request/response split when an existing endpoint has the file in the "wrong" place; keep matching the existing layout.)

### Representative `model/local/` subdirectories

The 61 subdirectories of `model/local/` follow a feature shape:

| Folder | What's inside |
|--------|--------------|
| `order/` | `order.dart`, `order_manage_data.dart`, `pre_order_data.dart`, plus `bonus/`, `product/`, `discount/`, `state/`, `status/` — every facet of an order |
| `client/` | `client.dart` plus 23 sub-directories: `category/`, `city/`, `channel/`, `type/`, `class/`, `visit/filter/`, `day/selection/`, `config/{order,trade,payment}/`, `sale/`, `oddment/`, `photo/`, `report/`, `search/`, … |
| `product/` | `product.dart`, `product_wrapper.dart`, plus `category/`, `brand/`, `price/`, `pinned/`, `validation/` |
| `config/` | `config_client.dart`, `config_order.dart`, `config_visiting.dart`, `config_vansell.dart`, `config_photo.dart`, … — server-driven feature flags. Used everywhere via `commonRepository.getConfigX()` |
| `sync/` | `sync_type.dart` (enum of every resumable sync step — see [07-synchronize](./07-synchronize.md)), `home_sync_type.dart`, `stock.dart` |
| `task/` | `task.dart`, `task_type.dart`, `task_status.dart`, plus `category/`, `summary/` |
| `error/` | `global_error_type.dart` enum used by `DisplayErrorRepository` (see [09-error-handling](./09-error-handling.md)) |

If you create a new local model, drop it under `model/local/<feature>/` matching the feature's BLoC location in `presentation/features/<feature>/`.

## Repository interfaces

35 directories under `lib/domain/repositories/`. Each holds one or more `abstract class XxxRepository` declarations. The data layer implements them under `lib/data/repository_impls/`.

`ClientRepository` is by far the heaviest — 66 public methods spread across three logical groups:

```dart
// lib/domain/repositories/client/client_repository.dart
abstract class ClientRepository {

  // 1. Server sync — POST local changes / GET server data
  Future<bool> hasNotSyncClients();
  Future<void> sendClient({bool isClearData = false, String? clientId});
  Future<void> getClientInfo();
  Future<void> updateClientInfo();
  Future<void> getClientDirectoryList();
  Future<void> getDayTransactions();
  Future<ClientOrderConfig> getClientOrderConfig(String clientId);
  Future<List<ClientTradeConfig>> getClientTradeConfig(String clientId);
  Future<Client> getClientIdByQrCode(String qrCode);

  // 2. Reactive streams — UI subscribes; emits on every DB change
  Stream<Client> observeGetClient(String clientId);
  Stream<List<Client>> observeGetClientList(ClientVisitFilter filter);
  Stream<List<Client>> observeGetTodayClientList(ClientVisitFilter? filter, bool isMadeRoute);
  Stream<List<Client>> observeGetClientListByDay(ClientDaySelection day, ClientVisitFilter filter);
  Stream<int> observeNotVisitClientsCount({String tradeId = ""});
  Stream<int> observeVisitedClientsCount({String tradeId = ""});
  Stream<List<ClientPhoto>> observeClientPhotosByClientId(String clientId);
  // … ~20 more observe* methods

  // 3. One-shot futures — for actions and lookups
  Future<Client> getClientById(String clientId);
  Future<Client> getClientInfoById(String clientId);
  Future<List<ClientCategory>> getActiveClientCategoryList();
  Future<void> updateClient(String clientId, String name, /* … 11 more params */);
  Future<void> addNewClient(String clientId, String name, /* … 13 more params */);
  Future<bool> checkClientInnDuplicate(String inn, {String? clientId, CancelToken? cancelToken});
  Future<bool> checkClientPinflDuplicate(String pinfl, {String? clientId, CancelToken? cancelToken});
  Future<bool> checkClientFirmNameDuplicate(String firmName, {String? clientId, CancelToken? cancelToken});
  Future<bool> isCanDeleteClientActions(String clientId);
  Future<int> getClientLocationCount();
}
```

Conventions:
- `send*` and `get*` for sync POST/GET (matches `SynchronizeUseCase` naming).
- `observe*` returns `Stream<T>` — backed by Floor DAO streams. UI subscribes; Floor re-emits on table change.
- `get*ById`, `update*`, `addNew*`, `check*` for one-shot futures.
- `CancelToken` is exposed on duplicate-check methods because they're called from text-field validators that fire repeatedly while the user types.

## Use cases

33 feature directories under `lib/domain/usecase/`. Each typically has a `*_usecase.dart` (interface) + `*_usecase_impl.dart` (implementation) pair. Use cases are the layer that BLoCs talk to — they hide the fact that a single user-facing operation usually needs multiple repositories.

```dart
// lib/domain/usecase/client/list/client_list_usecase.dart
abstract class ClientListUseCase {
  void setClientDaySelection(ClientDaySelection? value, ClientVisitFilter? filter);
  void setIsMadeRoute(bool value);

  Stream<ConfigClient> getClientConfig();
  Future<int> getLastSyncTime();
  Stream<List<Client>> getClientList();
  Future<int?> getClientVisitCount(String day);
  Future<int?> getClientVisitCountWithFilter(String day, ClientVisitFilter filter);
  Future<CheckInOut> hasActiveCheckInOut();
  Future<bool> getShowClientBalance();
  Future<bool> getShowClientLegalName();
  Future<bool> getShowUnvisitedClients();
  Future<bool> getShowVisitDays();
  Stream<int> getTotalOrderCountNotSync();
  Stream<int> getTotalRejectionCountNotSync();
  Stream<int> getTotalPhotoReportCountNotSync();
  Future<ConfigVisiting> getConfigVisiting();
  Future<bool> getRouteStatus();
  Future<int> getPendingClientCount();
  Stream<int> observePendingClientCount();
}
```

The implementation composes eight repositories:

```dart
// lib/domain/usecase/client/list/client_list_usecase_impl.dart
class ClientListUseCaseImpl implements ClientListUseCase {
  final ClientRepository clientRepository;
  final CommonRepository commonRepository;
  final ClientCheckInOutRepository clientCheckInOutRepository;
  final UserRepository userRepository;
  final OrderRepository orderRepository;
  final PhotoRepository photoRepository;
  final LocationRepository locationRepository;
  final PendingClientRepository pendingClientRepository;

  ClientListUseCaseImpl({
    required this.clientRepository,
    required this.commonRepository,
    // …
  });

  ClientDaySelection? _clientDaySelection;
  ClientVisitFilter? _clientVisitFilter;
  bool isMadeRoute = false;

  @override
  Stream<List<Client>> getClientList() {
    switch (_clientDaySelection) {
      case null:
      case ClientDaySelection.all:
        return clientRepository.observeGetClientList(_clientVisitFilter!);
      case ClientDaySelection.today:
        return clientRepository.observeGetTodayClientList(_clientVisitFilter, isMadeRoute);
      default:
        return clientRepository.observeGetClientListByDay(
          _clientDaySelection!,
          _clientVisitFilter!,
        );
    }
  }

  @override
  Stream<int> getTotalOrderCountNotSync() =>
      orderRepository.observeTotalOrderCountNotSync();

  @override
  Stream<int> getTotalRejectionCountNotSync() =>
      commonRepository.observeTotalRejectionCountNotSync();

  @override
  Stream<int> getTotalPhotoReportCountNotSync() =>
      photoRepository.observeTotalPhotoReportCountNotSync();

  // …
}
```

Patterns:
- Use cases **own stateful filter/selection state** (the `_clientDaySelection` and `_clientVisitFilter` private fields above). The BLoC doesn't have to wire those through to multiple repositories on every event.
- Most methods are thin delegators that forward to a repository. The value the use case adds is being the one place where multi-repository coordination happens, and being the layer that tests can mock without touching `Dio`/`Floor`.
- One use case = one feature area, usually one page or one BLoC. There is no "GodUseCase".

Registered as `registerFactory` (each `appGetIt<MyUseCase>()` call returns a fresh instance — no shared mutable filter state between unrelated BLoCs). The one exception is `ReviseReportUseCase`, registered as `registerLazySingleton`.

## Mappers

`lib/domain/mapper/<feature>/` — Dart extension methods on entity, relation, and response classes producing domain models. Already covered in [02-data-layer §Mappers](./02-data-layer.md#mappers); the key fact is they live under `domain/` because they **produce** domain models, even though they **consume** data-layer types.

## `common/` — cross-feature plumbing

### `common/exception/`

Domain-level exceptions thrown by use cases or downstream. Example: `search/search_exception.dart`. These extend `AppException` and are caught by `FutureHandler.onError` like any other (see [09-error-handling](./09-error-handling.md)).

### `common/notifier/`

`dependencies_reset_notifier.dart` — a global broadcast bus used when DI must be re-initialized mid-session (e.g. after user switch):

```dart
class DependenciesResetNotifier {
  static final DependenciesResetNotifier instance = DependenciesResetNotifier._();
  final StreamController<void> _controller = StreamController<void>.broadcast();
  Stream<void> get stream => _controller.stream;
  void notify() => _controller.add(null);
}
```

Subscribed by `App` so it can re-fetch any DI-resolved singletons it cached.

### `common/stream/`

The 14 cross-feature stream controllers — see [06-streams-and-cross-feature](./06-streams-and-cross-feature.md) for the full catalog with emitter/listener pairings. Each lives under `common/stream/<topic>/<name>_stream_controller.dart`, e.g.:

```dart
// lib/domain/common/stream/client/update_client_list_stream_controller.dart
class UpdateClientListActionStreamController extends BaseStreamController<void> {
  UpdateClientListActionStreamController({super.isBroadcast = true});
}
```

`BaseStreamController` is in `lib/core/` (it has no domain dependency). The thin subclasses here exist purely so DI can register a uniquely-typed singleton per concern.

## `manager/` — when a "repository" is really a service

`lib/domain/manager/location/location_repository.dart`:

```dart
abstract class LocationRepository {
  Future<Position?> getCurrentLocation();
  Future<LocationAction> getLocationActionByClientId(String clientId);
  Future<LocationAction> getLiveLatitudeAndLongitude();
  Future<bool> checkLocationPermission();
  Future<bool> checkGpsStatus();
  Future<LocationAction> getCurrentLocationAction();
  Future<void> sendCurrentLocationAction();
  Future<bool> getRouteStatus();
  Future<bool> getAutoRouteStatus();
  Future<List<LatitudeLongitude>> getClientRouteLocations();
  Future<void> clearRoute();
  Future<void> makeRoute(
    List<Client> manualClientList,
    double startLatitudePoint, double startLongitudePoint,
    double endLatitudePoint, double endLongitudePoint,
  );
  Future<List<SelectedLocation>> getSelectedLocations();
  Future<void> saveSelectedLocation(String placeName, double lat, double lon);
}
```

Why is this under `manager/` and not `repositories/`? Because it's a **stateful service** that coordinates platform APIs (geolocator, permission_handler, RouteXL via `routeDio`, the Floor `location` table) rather than being a thin data-access layer. The folder name signals the difference to readers: anything in `manager/` carries state and orchestrates multiple concerns; anything in `repositories/` is closer to "talk to the server / talk to the DB".

The data-layer implementation is still under `lib/data/repository_impls/location/` (because that's where Floor + Dio integration belongs), but the contract sits here.

## Adding to the domain layer

When adding a new feature:

1. **Model**: `lib/domain/model/local/<feature>/<feature>.dart` — immutable, with `copyWith` and `.empty()`.
2. **Repository interface**: `lib/domain/repositories/<feature>/<feature>_repository.dart` — `abstract class`, group methods by send / observe / one-shot.
3. **Use case interface**: `lib/domain/usecase/<feature>/<feature>_usecase.dart` — narrowly scoped to one feature.
4. **Use case impl**: `lib/domain/usecase/<feature>/<feature>_usecase_impl.dart` — constructor-inject repositories.
5. **Mapper**: `lib/domain/mapper/<feature>/<feature>_mapper.dart` — `extension XxxMapper on XxxEntityRelation { Xxx toX() => … }`.
6. **Register**: add to `repository_module.dart` and `use_case_module.dart` (see [01-architecture](./01-architecture.md)).

For an end-to-end walkthrough including BLoC, page, DI, and tests, see the orchestrator's "Full Parallel Pipeline" at the top of `CLAUDE.md`.

Next:

- [04-presentation-layer](./04-presentation-layer.md) — how BLoCs consume use cases
- [05-database](./05-database.md) — Floor entities that mappers read from
- [09-error-handling](./09-error-handling.md) — how exceptions thrown by use cases reach the UI
