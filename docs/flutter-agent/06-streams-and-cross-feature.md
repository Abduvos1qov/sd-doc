---
title: Streams & cross-feature communication
sidebar_position: 6
---

# Streams & cross-feature communication

When a user action in one feature must trigger a refresh in another — e.g. saving an order should make the home dashboard's "unsynced orders" badge tick down — the two features can't (and shouldn't) know about each other's BLoCs. The app uses **broadcast stream controllers as a global event bus**. 14 of them are registered as lazy singletons; each carries one kind of event.

## `BaseStreamController`

`lib/core/stream/controller/base_stream_controller.dart` — the shared base. All 14 controllers extend it.

```dart
import 'dart:async';

class BaseStreamController<T> {
  final StreamController<T> _controller;
  final bool cacheLastEvent;
  T? _cachedEvent;

  BaseStreamController({
    bool sync = false,
    bool isBroadcast = false,
    this.cacheLastEvent = false,
  }) : _controller = isBroadcast
            ? StreamController<T>.broadcast(sync: sync)
            : StreamController<T>(sync: sync);

  Stream<T> get stream => _controller.stream.map((event) => event);

  void add(T event) {
    if (cacheLastEvent) {
      _cachedEvent = event;
    }
    _controller.add(event);
  }

  StreamSubscription<T> listen(
    void Function(T event)? onData, {
    Function? onError,
    void Function()? onDone,
    bool? cancelOnError,
  }) {
    final subscription = _controller.stream.listen(
      onData,
      onError: onError,
      onDone: onDone,
      cancelOnError: cancelOnError,
    );

    if (cacheLastEvent && _cachedEvent != null) {
      onData?.call(_cachedEvent!);
    }

    return subscription;
  }

  Future<void> addAndClose(T event) async {
    add(event);
    await close();
  }

  void addError(Object error, [StackTrace? stackTrace]) {
    _controller.addError(error, stackTrace);
  }

  Future<void> close() => _controller.close();

  StreamSink<T> get sink => _controller.sink;
}
```

Three modes worth knowing:

| Constructor flag | Effect |
|------------------|--------|
| `isBroadcast: true` (default for all 14 controllers) | Multiple listeners can subscribe. Required for the global-bus use case. |
| `isBroadcast: false` | Single-subscription. Throws if you `.listen()` twice. Not used for any of the 14 controllers. |
| `cacheLastEvent: true` | The most recent `add(event)` is stored; new listeners receive it immediately on `.listen()`. Used by **only one** of the 14: `LocationServiceStreamController`. |
| `sync: true` | Listeners are notified synchronously within `add()`. Off by default — risky because exceptions in a listener would bubble up out of the `.add()` call site. |

Public API the subclasses inherit: `add(T)`, `listen(...)`, `addAndClose(T)`, `addError(...)`, `close()`, plus the `stream` and `sink` getters.

## Registration

`lib/presentation/application/di/presentation/stream_controller_module.dart`:

```dart
extension StreamControllerModule on GetIt {
  Future<void> streamControllerModule() async {
    registerLazySingleton(() => UpdateClientListActionStreamController());
    registerLazySingleton(() => UpdateClientDetailActionStreamController());
    registerLazySingleton(() => UpdateClientOddmentStreamController());
    registerLazySingleton(() => UpdatePaymentStreamController());
    registerLazySingleton(() => UpdateOrderStreamController());
    registerLazySingleton(() => UpdateRejectionStreamController());
    registerLazySingleton(() => UpdatePhotoReportStreamController());
    registerLazySingleton(() => LocationServiceStreamController());
    registerLazySingleton(() => ClientVisitFilterStreamController());
    registerLazySingleton(() => VanSellOrderHistoryStreamController());
    registerLazySingleton(() => SearchStreamController());
    registerLazySingleton(() => UpdateOrderProductStreamController());
    registerLazySingleton(() => TotalFilterStreamController());
    registerLazySingleton(() => UpdateSyncRequiredStreamController());
    await allReady();
  }
}
```

14 controllers, all lazy singletons. The module is async and ends with `await allReady()` to make sure DI is fully wired before anything tries to resolve a controller.

## Catalog

Each controller's contract: payload type, who emits, who listens. File paths are abbreviated to fit; all live under `lib/presentation/features/...` unless noted.

### `UpdateClientListActionStreamController`

`lib/domain/common/stream/client/update_client_list_stream_controller.dart`

```dart
class UpdateClientListActionStreamController extends BaseStreamController<void> {
  UpdateClientListActionStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| `add(null)` | `home_bloc.dart:86`, `home_bloc.dart:243` (home tab refresh after sync) |
| `add(null)` | `client_manage_bloc.dart:608` (after creating/editing a client) |
| `add(null)` | `pending_clients_page.dart:73` (after a pending client is verified) |
| listen | consumed indirectly via re-fetch events in client list BLoCs |

### `UpdateClientDetailActionStreamController`

`lib/domain/common/stream/client/detail/update_client_detail_stream_controller.dart` — carries a `DeleteAction` enum so listeners can react differently depending on what was just done on the client detail (order saved, rejection cleared, …).

```dart
class UpdateClientDetailActionStreamController extends BaseStreamController<DeleteAction> {
  final DeleteAction deleteAction;
  UpdateClientDetailActionStreamController({
    this.deleteAction = DeleteAction.none,
    super.isBroadcast = true,
  });
}
```

| Direction | Where |
|-----------|-------|
| `add(state.deleteAction)` | `order_overview_bloc.dart:212` (after order save) |
| `add(DeleteAction.none)` | `home_bloc.dart:85` |
| `add(DeleteAction.none)` | `client_oddment_list_bloc.dart:93`, `:121` |
| `add(DeleteAction.none)` | `client_oddment_manage_bloc.dart:275` |
| `add(DeleteAction.none)` | `client_detail_bloc.dart:1043` |
| listen | `client_detail_page.dart:1039` |
| listen | `total_page.dart:335` (home → total view) |

### `UpdateClientOddmentStreamController`

`lib/domain/common/stream/client/oddment/update_client_oddment_stream_controller.dart`

```dart
class UpdateClientOddmentStreamController extends BaseStreamController<void> {
  UpdateClientOddmentStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| listen | `client_oddment_detail_page.dart:63` |
| listen | `client_oddment_list_page.dart:71` |

(Emit sites are inside the oddment manage flow — search for the controller name to verify when wiring new emitters.)

### `UpdatePaymentStreamController`

```dart
class UpdatePaymentStreamController extends BaseStreamController<void> {
  UpdatePaymentStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| `add(null)` | `order_detail_bloc.dart:126` |
| `add(DeleteAction.none)` | `payment_manage_bloc.dart:138` |
| listen | `order_detail_page.dart:67` |
| listen | `task_control_bloc.dart:256` (re-emits to other consumers) |

### `UpdateOrderStreamController`

The busiest controller in the app — 13 emit sites, multiple listeners. Fires whenever an order is created, edited, deleted, defected, refunded, or pulled down by sync.

```dart
class UpdateOrderStreamController extends BaseStreamController<void> {
  UpdateOrderStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| emit | `order_overview_bloc.dart:213` |
| emit | `draft_bloc.dart:65`, `:68`, `:79` |
| emit | `order_detail_bloc.dart:127` |
| emit | `defect_manage_bloc.dart:222` |
| emit | `home_synchronize_bloc.dart:1171` |
| emit | `task_dashboard_bloc.dart:45` |
| emit | `synchronize_bloc.dart:1188`, `:1215` |
| emit | `client_detail_bloc.dart:704`, `:734` |
| emit | `refund_based_order_detail_bloc.dart:157` |
| listen | `draft_page.dart:52` |
| listen | `daily_clients_page.dart:389` (`_updateOrderSub`) |
| listen | `client_list_page.dart:404` (`_updateOrderSub`) |

### `UpdateRejectionStreamController`

```dart
class UpdateRejectionStreamController extends BaseStreamController<void> {
  UpdateRejectionStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| emit | `client_detail_bloc.dart:578, 631, 656, 680, 1065, 1080, 1105` (any rejection state change) |
| emit | `pending_docs_bloc.dart:140` |
| emit | `home_synchronize_bloc.dart:1172`, `synchronize_bloc.dart:1189, :1216` |
| listen | `daily_clients_page.dart:397` (`_updateRejectionSub`) |
| listen | `more_menu_page.dart:137` |
| listen | `client_list_page.dart:411` (`_updateRejectionSub`) |

### `UpdatePhotoReportStreamController`

```dart
class UpdatePhotoReportStreamController extends BaseStreamController<void> {
  UpdatePhotoReportStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| emit | `photo_synchronize_bloc.dart:109`, `home_synchronize_bloc.dart:1173`, `synchronize_bloc.dart:1190, :1217` |
| emit | `client_detail_bloc.dart:550, :942` |
| listen | `daily_clients_page.dart:405` (`_updatePhotoReportSub`) |
| listen | `client_list_page.dart:418` (`_updatePhotoReportSub`) |

### `LocationServiceStreamController`

The only controller that caches its last event:

```dart
class LocationServiceStreamController extends BaseStreamController<LocationAction> {
  LocationServiceStreamController({
    super.isBroadcast = true,
    super.cacheLastEvent = true,
  });
}
```

Caching matters here: any new screen that opens (order, refund, replace, …) needs the most recent GPS reading immediately — it can't wait for the next location ping. With `cacheLastEvent: true`, the screen subscribes and synchronously receives the cached location in the same microtask as `.listen()`.

| Direction | Where |
|-----------|-------|
| `add(data)` | `order_history_detail_bloc.dart:210` |
| `add(data)` | `client_detail_bloc.dart:1004` |
| listen | `order_overview_page.dart:994` |
| listen | `replace_overview_page.dart:671` |
| listen | `refund_based_order_list.dart:306` (`_locationSubscription`) |
| listen | `refund_based_order_detail_page.dart:349` |
| listen | `refund_overview_page.dart:444` |

### `ClientVisitFilterStreamController`

Carries the current `ClientVisitFilter` selection between the home page and the client list/map.

```dart
class ClientVisitFilterStreamController extends BaseStreamController<ClientVisitFilter> {
  ClientVisitFilterStreamController({super.isBroadcast = true});
}
```

Used as a DI-resolved dependency in pages where the filter must persist across navigation. Emitters and listeners are inside those pages' BLoCs — search for the controller name when wiring a new feature into the filter flow.

### `VanSellOrderHistoryStreamController`

```dart
class VanSellOrderHistoryStreamController extends BaseStreamController<void> {
  VanSellOrderHistoryStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| `add(null)` | `van_sell_order_manage_bloc.dart:227` |
| `add(null)` | `van_sell_refund_manage_bloc.dart:271` |
| listen | `van_sell_order_list_page.dart:228` |

### `SearchStreamController`

```dart
class SearchStreamController extends BaseStreamController<void> {
  SearchStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| `add(null)` | `client_manage_bloc.dart:607` (after client edit / create — search results need to refresh) |
| listen | `lib/presentation/common/search/search/search_page.dart:193` |

### `UpdateOrderProductStreamController`

Carries a `productId` so listeners know which order line to refresh.

```dart
class UpdateOrderProductStreamController extends BaseStreamController<String> {
  final String productId;
  UpdateOrderProductStreamController({
    this.productId = "",
    super.isBroadcast = true,
  });
}
```

| Direction | Where |
|-----------|-------|
| `add(event.productId)` | `product_scanner_bloc.dart:56` (after barcode scan) |
| `add(event.productId)` | `order_manage_bloc.dart:504` |
| listen | `order_manage_page.dart:289` |

### `TotalFilterStreamController`

```dart
class TotalFilterStreamController extends BaseStreamController<TotalReportFilter> {
  TotalFilterStreamController({super.isBroadcast = true});
}
```

Similar to `ClientVisitFilterStreamController`: a filter-state carrier used by the home → total report flow. Emit/listen sites live inside the total-page BLoC.

### `UpdateSyncRequiredStreamController`

Drives the "you need to sync now" UX (see [07-synchronize](./07-synchronize.md)).

```dart
class UpdateSyncRequiredStreamController extends BaseStreamController<bool> {
  UpdateSyncRequiredStreamController({super.isBroadcast = true});
}
```

| Direction | Where |
|-----------|-------|
| `add(true)` | `app.dart:81` (notification tap with `openSyncScreen` payload) |
| `add(true)` | `client_detail_page.dart:160` |
| `add(true)` | `client_detail_bloc.dart:1123` |
| listen | `home_page.dart:450` (shows the sync banner / triggers navigation to SynchronizeRoute) |
| listen | `client_detail_page.dart:154` (re-emits to home after replaceAll) |

## Safe usage pattern

The lifecycle rules in [04-presentation-layer](./04-presentation-layer.md) apply to every page/BLoC that listens to one of these controllers:

```dart
class _ClientDetailState extends State<ClientDetailPage> {
  final UpdateClientDetailActionStreamController updateClientDetailActionStreamController = appGetIt();

  StreamSubscription? _updateClientDetailSubscription;
  StreamSubscription? _syncRequiredSubscription;

  @override
  void initState() {
    super.initState();
    _listenClientDetailUpdateOrder();
    _listenSyncRequired();
    _bloc.add(ClientDetailInitialEvent(clientId: widget.clientId));
  }

  void _listenClientDetailUpdateOrder() {
    _updateClientDetailSubscription?.cancel();    // cancel before re-subscribe
    _updateClientDetailSubscription = updateClientDetailActionStreamController.listen((data) {
      if (data == DeleteAction.deleteOneRejectionAfterOrderSaved) {
        _bloc.add(ClientDetailDeleteAllRejectionsEvent());
      }
      _bloc.add(ClientDetailUpdateOrderEvent());
      _bloc.add(ClientDetailUpdateBalanceEvent());
    });
  }

  void _listenSyncRequired() {
    _syncRequiredSubscription?.cancel();
    _syncRequiredSubscription = _bloc.updateSyncRequiredStreamController.listen((data) {
      if (data) {
        context.router.replaceAll([const MainRoute()]);
        Future.delayed(const Duration(milliseconds: 300), () {
          _bloc.updateSyncRequiredStreamController.add(true);
        });
      }
    });
  }

  @override
  void dispose() {
    _updateClientDetailSubscription?.cancel();
    _syncRequiredSubscription?.cancel();
    _bloc.close();
    super.dispose();
  }
}
```

Both halves matter:

- **`?.cancel()` before re-subscribing** — otherwise re-running an `initState`-style helper later (e.g. after a tab switch) leaves multiple listeners attached and the BLoC processes every event N times. Memory grows; behavior gets weird.
- **`?.cancel()` in `dispose()`** — otherwise the subscription survives the widget. Next time the controller emits, the dead listener tries to `add(event)` to a closed BLoC and throws.

The same applies inside BLoCs — see the `ClientInfoBloc.close()` example in [04-presentation-layer §StreamSubscription lifecycle](./04-presentation-layer.md#streamsubscription-lifecycle).

## Adding a new cross-feature event

1. Define the controller class under `lib/domain/common/stream/<topic>/<name>_stream_controller.dart`:
   ```dart
   class UpdateNewThingStreamController extends BaseStreamController<void> {
     UpdateNewThingStreamController({super.isBroadcast = true});
   }
   ```
2. Register it in `lib/presentation/application/di/presentation/stream_controller_module.dart`:
   ```dart
   registerLazySingleton(() => UpdateNewThingStreamController());
   ```
3. Inject it into emitting BLoCs:
   ```dart
   class FeatureABloc extends Bloc<…, …> {
     final UpdateNewThingStreamController updateNewThingStreamController;
     FeatureABloc({required this.updateNewThingStreamController, …}) : …;

     void _onSomething(…) {
       updateNewThingStreamController.add(null);
     }
   }
   ```
4. Listen in receiving pages (or BLoCs) and **cancel-before-resubscribe + cancel-in-dispose**.

Use `cacheLastEvent: true` only when **late subscribers absolutely need the previous value** — i.e. the consumer's behavior on first-frame depends on the most recent emission (like `LocationServiceStreamController`). For pure "something happened, go refresh yourself" events, leave it off.

## Architecture notes

- **`void` events dominate** (10 of 14 are `BaseStreamController<void>`). They mean "go refresh yourself" — the listener doesn't need the *what*, only the *when*. The actual data is fetched fresh from the DB on the next event.
- **Data-bearing events** (`DeleteAction`, `LocationAction`, `ClientVisitFilter`, `TotalReportFilter`, `String productId`, `bool`) carry just enough to skip a query or pick a code path on the receiver.
- **Lazy singletons**, not factories — every consumer must see the same instance. `appGetIt<UpdateOrderStreamController>()` always returns the same controller.
- **Notification deep-link** is the one external trigger (the OS, not another feature, raises the event in `app.dart:81`).
