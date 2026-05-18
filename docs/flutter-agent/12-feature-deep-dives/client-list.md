---
title: client/list
sidebar_position: 3
---

# `client/list` — the client list page

The list view of clients, used in two places:

1. As a child of each `DailyClientsPage` tab (one instance per day-of-week selection).
2. Standalone via `ClientListRoute` when navigating from search or filter.

The implementation is interesting for two reasons: it owns **five** `StreamSubscription` fields (cross-feature signal listeners), and its `ClientListBloc` owns **six more** internal stream subscriptions to Floor DAO observables. Both halves illustrate the cancel-before-resubscribe / cancel-in-dispose pattern at scale.

| File | Lines |
|------|-------|
| `lib/presentation/features/client/list/client_list_page.dart` | 557 |
| `lib/presentation/features/client/list/bloc/client_list_bloc.dart` | 266 |
| `lib/presentation/features/client/list/bloc/client_list_state.dart` | (small) |
| `lib/presentation/features/client/list/bloc/client_list_event.dart` | ~51 |
| `lib/domain/usecase/client/list/client_list_usecase.dart` | 50 |
| `lib/domain/usecase/client/list/client_list_usecase_impl.dart` | 157 |

## Page

### State class fields — 5 page-level subscriptions

```dart
StreamSubscription? _updateOrderSub;
StreamSubscription? _updateRejectionSub;
StreamSubscription? _updatePhotoReportSub;
StreamSubscription? _updateClientListSub;
StreamSubscription? _updateClientsSub;
```

Each subscribes to a different cross-feature stream controller (see [06-streams-and-cross-feature](../06-streams-and-cross-feature.md)) so the list refreshes when something elsewhere mutates clients, orders, rejections, or photo reports.

### `initState`

```dart
@override
void initState() {
  super.initState();
  _listenUpdateOrder();
  _listenUpdateRejection();
  _listenUpdatePhotoReport();
  _listenUpdateClientList();
  _listUpdateClients();

  _bloc.add(
    ClientListInitialEvent(
      clientDaySelection: widget.clientDaySelection,
      clientVisitFilter: widget.clientVisitFilter,
      isMadeRoute: widget.isMadeRoute,
    ),
  );
}
```

Each `_listenX()` method follows the same pattern. Example:

```dart
void _listenUpdateOrder() {
  _updateOrderSub?.cancel();
  _updateOrderSub = _updateOrderStreamController.listen((_) {
    _bloc.add(ClientListUpdateOrderEvent());
  });
}
```

`?.cancel()` before the new `.listen(...)` so repeated calls don't stack listeners.

### `dispose`

```dart
@override
void dispose() {
  _updateOrderSub?.cancel();
  _updateRejectionSub?.cancel();
  _updatePhotoReportSub?.cancel();
  _updateClientListSub?.cancel();
  _updateClientsSub?.cancel();
  _bloc.close();
  super.dispose();
}
```

> **Technical-debt note**: `CLAUDE.md` lists this page in its "Critical — StreamSubscription leaks" section. The current `dispose()` shown above does cancel all five subscriptions; the leak annotation may pre-date a fix. When auditing for memory leaks here, verify against the live code rather than assuming the CLAUDE.md note is current. **The pattern shown above is the correct pattern** — if the file deviates, fix it to match.

## BLoC

### Init event

The init event carries all three parameters the page received from its parent:

```dart
class ClientListInitialEvent extends ClientListEvent {
  final ClientDaySelection? clientDaySelection;
  final ClientVisitFilter? clientVisitFilter;
  final bool isMadeRoute;

  ClientListInitialEvent({
    required this.clientDaySelection,
    required this.clientVisitFilter,
    this.isMadeRoute = false,
  });
}
```

`clientDaySelection`: nullable. `null` and `ClientDaySelection.all` both mean "show every client", but the use case branches differently on each (one observes `observeGetClientList(filter)`, the other observes `observeGetClientList(filter)` with `Today` semantics). See `ClientListUseCaseImpl.getClientList()` in [03-domain-layer §Use cases](../03-domain-layer.md#use-cases).

### Other events

```dart
class ClientRefreshEvent extends ClientListEvent {}
class ClientListCallSuccessEvent extends ClientListEvent { … }
class ClientListCallLoadingEvent extends ClientListEvent {}
class ClientListCallErrorEvent extends ClientListEvent { … }
class ClientListUpdateOrderEvent extends ClientListEvent {}
class ClientListUpdateRejectionEvent extends ClientListEvent {}
class ClientListUpdatePhotoReportEvent extends ClientListEvent {}
class ClientListPendingCountEvent extends ClientListEvent { … }
class ClientListConfigClientEvent extends ClientListEvent { … }
```

10 events total. The three `Update*Event` events fire from the page when one of the cross-feature controllers emits — the BLoC then refreshes the relevant badge / sub-count.

### BLoC-level subscriptions — 6 of them

```dart
StreamSubscription? _clientListStreamSubscription;
StreamSubscription? _clientConfigStreamSubscription;
StreamSubscription? _clientOrderCountNotSyncStreamSubscription;
StreamSubscription? _clientRejectionCountNotSyncStreamSubscription;
StreamSubscription? _clientPhotoReportCountNotSyncStreamSubscription;
StreamSubscription? _pendingClientCountSubscription;
```

These are subscriptions to the use case's reactive streams (which themselves are Floor DAO streams under the hood). Each emits an event whenever the underlying DB rows change:

```dart
_clientOrderCountNotSyncStreamSubscription =
    clientListUseCase.getTotalOrderCountNotSync().listen((count) {
      add(ClientListCallSuccessEvent(totalOrderCountNotSync: count));
    });
```

All six are cancelled in `_disposeStreamSubscription()`, called from `close()`:

```dart
@override
Future<void> close() {
  _disposeStreamSubscription();
  return super.close();
}

void _disposeStreamSubscription() {
  _clientListStreamSubscription?.cancel();
  _clientConfigStreamSubscription?.cancel();
  _clientOrderCountNotSyncStreamSubscription?.cancel();
  _clientRejectionCountNotSyncStreamSubscription?.cancel();
  _clientPhotoReportCountNotSyncStreamSubscription?.cancel();
  _pendingClientCountSubscription?.cancel();
}
```

## UseCase

```dart
abstract class ClientListUseCase {
  void setClientDaySelection(ClientDaySelection? value, ClientVisitFilter? filer);
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

The `setClientDaySelection(...)` and `setIsMadeRoute(...)` are deliberate state-holders on the use case so the BLoC doesn't need to pass them through every method call. The `getClientList()` reads them privately and picks one of three repository methods:

```dart
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
```

Eight repositories are injected. The use case is the one place where the "show clients" semantics across orders / rejections / photo reports / location / pending all converge.

## Cross-feature dependencies

The page subscribes to (via cross-feature stream controllers; see [06-streams-and-cross-feature](../06-streams-and-cross-feature.md)):

- `UpdateOrderStreamController` (`add` happens from 13 sites including `OrderOverviewBloc`, `DraftBloc`, `OrderDetailBloc`, `SynchronizeBloc`, `ClientDetailBloc`)
- `UpdateRejectionStreamController` (`add` from 11 sites)
- `UpdatePhotoReportStreamController` (`add` from 6 sites)
- `UpdateClientListActionStreamController` (`add` from 4 sites)
- (one more — likely `UpdateClientDetailActionStreamController` or a similar list-mutation controller)

Each emission triggers the corresponding `ClientListUpdateXEvent`. The BLoC handler typically re-fetches the relevant badge count from its already-subscribed stream — the page doesn't have to do anything beyond passing the event through.

## When you change this code

- **Don't add a sixth page-level subscription without auditing dispose** — the file is dense and an unpaired `?.cancel()` is easy to miss.
- **Don't `listen` to use-case streams directly from the page** — go through the BLoC. The BLoC owns the lifetime.
- **If you add a new badge** (e.g. "unsynced replacements" count), the pattern is: new `Stream<int>` on the use case → new BLoC-internal `StreamSubscription` field → new `*CallSuccessEvent` carrying the count → cancel in `_disposeStreamSubscription`.
- **Performance**: this page renders a list with `ValueKey(client.id)` on each row. The CLAUDE.md known-issues list flagged it as missing keys at one point — verify keys are present before adding new list rendering.
