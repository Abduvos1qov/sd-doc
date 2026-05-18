---
title: Presentation layer
sidebar_position: 4
---

# Presentation layer

The presentation layer (`lib/presentation/`) is BLoC-driven and routed by `AutoRoute`. State is immutable, events are sealed, every async call goes through `FutureHandler`, every `StreamSubscription` is owned and cancelled by the same widget that opened it. This doc covers the BLoC pattern, the page pattern, `FutureHandler`, `AutoRoute`, and the shared `widgets/` + `support/` + `common/` toolboxes.

```
lib/presentation/
├── app.dart                  # root widget (see 08-navigation-and-shell)
├── application/              # DI (see 01-architecture)
├── base/                     # base themes/styles
├── common/                   # shared BLoC-driven flows (search, selection, photoview, …)
├── features/                 # 30 feature modules
└── support/                  # extensions, alert helpers, percentage calculator
```

The 30 features under `lib/presentation/features/`:

`bill, check, client, debt, debtor, defect, direction, equipment, kpi, location, log, login, main, oddments, order, payment, pending, qrcode, refund, replace, report, revise, settings, support, synchronize, tara, task, user, vsorder, weblink`

For an index with routes, BLoCs, and use cases per feature, see [11-features-catalog](./11-features-catalog.md).

## BLoC pattern

Every feature has at least one `Bloc` under `lib/presentation/features/<feature>/bloc/`. The pattern is rigid: **state is immutable with `copyWith` and a status enum, events are a sealed class, internal events are `_`-prefixed, every StreamSubscription field is cancelled in `close()`**.

### State

`lib/presentation/features/order/orderoverview/bloc/order_overview_state.dart`:

```dart
@immutable
class OrderOverviewState {
  final List<Product> productList;
  final double totalOrderSumma;
  final double totalDiscountSumma;
  final double totalPaymentSumma;
  final String errorMessage;
  final String comment;
  final List<int> tagIds;
  final List<SelectionItem> selectedTagList;
  final Trade trade;
  final BonusType bonusType;
  final List<String> bonusIds;
  final List<OrderDiscountBonusDetail> bonusList;
  final List<OrderBonusProduct> bonusProductList;
  final PriceType priceType;
  final Warehouse warehouse;
  final OrderOverviewStatus status;
  // … ~30 fields total

  OrderOverviewState({
    this.productList = const [],
    this.clientId = "",
    this.orderId = "-1",
    this.totalOrderSumma = 0.0,
    // … every field has a default
    this.status = OrderOverviewStatus.updateUi,
    Trade? trade,
    PriceType? priceType,
    Warehouse? warehouse,
  })  : priceType = priceType ?? PriceType.empty(),
        trade = trade ?? Trade.empty(),
        warehouse = warehouse ?? Warehouse.empty();

  OrderOverviewState copyWith({
    List<Product>? productList,
    double? totalOrderSumma,
    // …
    OrderOverviewStatus? status,
    bool resetDateLoad = false,
    bool resetConsignDate = false,
  }) {
    return OrderOverviewState(
      productList: productList ?? this.productList,
      // …
      consignDate: resetConsignDate ? null : consignDate ?? this.consignDate,
      dateLoad: resetDateLoad ? null : dateLoad ?? this.dateLoad,
    );
  }
}

enum OrderOverviewStatus {
  initial,
  updateUi,
  save,
  showFullLoadingDialog,
  hideFullLoadingDialog,
  error,
  timeError,
}
```

Rules to follow:

- `@immutable` annotation on the state class.
- Every field has a default in the constructor — `BlocBuilder` should never crash on a fresh instance.
- A `status` enum drives UI rendering. The page's `BlocBuilder` switches on `state.status` to pick which subtree to show. Statuses are domain-specific; common values are `loading, success, error, empty`, plus feature-specific ones like `showFullLoadingDialog`, `hideFullLoadingDialog`, `timeError`, `save`.
- `copyWith` covers all fields that callers commonly mutate. For nullable fields that need to be **explicitly cleared**, add a `resetX: bool` flag (see `resetDateLoad`, `resetConsignDate` above) — `null ?? this.x` would otherwise just keep the old value.

### Event

`lib/presentation/features/order/orderoverview/bloc/order_overview_event.dart`:

```dart
@immutable
sealed class OrderOverviewEvent {}

class OrderOverviewInitialEvent extends OrderOverviewEvent {
  final OrderManageType orderManageType;
  final List<Product> productList;
  OrderOverviewInitialEvent({required this.orderManageType, required this.productList});
}

class OrderOverviewCommentEvent extends OrderOverviewEvent {
  final String comment;
  OrderOverviewCommentEvent({required this.comment});
}

class AddNewOrderOverviewEvent extends OrderOverviewEvent {
  final OrderType orderType;
  final LocationAction? locationAction;
  final String? preOrderId;
  AddNewOrderOverviewEvent({required this.orderType, this.locationAction, this.preOrderId});
}

// … more event subclasses
```

Rules:
- File is `part of '<feature>_bloc.dart'` (you'll see `part 'order_overview_event.dart';` in the BLoC file).
- `sealed class` so the compiler enforces exhaustive switches.
- Internal events — events the BLoC adds to itself, never from outside — are prefixed with `_`. The convention is enforced by review; underscores in Dart make the class file-private, so leaking one to a page won't compile.

### BLoC

```dart
// lib/presentation/features/order/orderoverview/bloc/order_overview_bloc.dart
class OrderOverviewBloc extends Bloc<OrderOverviewEvent, OrderOverviewState> {
  final OrderOverviewUseCase orderOverviewUseCase;
  final UpdateClientDetailActionStreamController updateClientDetailStreamController;
  final UpdateOrderStreamController updateOrderStreamController;

  OrderOverviewBloc({
    required this.orderOverviewUseCase,
    required this.updateOrderStreamController,
    required this.updateClientDetailStreamController,
  }) : super(OrderOverviewState()) {
    on<OrderOverviewInitialEvent>(_onInitialEvent);
    on<OrderOverviewCommentEvent>(_updateComment);
    on<AddNewOrderOverviewEvent>(_saveOrder);
    on<OrderOverviewConsignDateEvent>(_updateConsignDate);
    // … one handler per event
  }
}
```

Async handler — note the FutureHandler chain:

```dart
Future<void> _saveOrder(
  AddNewOrderOverviewEvent event,
  Emitter<OrderOverviewState> emit,
) async {
  orderOverviewUseCase.setOrderType(event.orderType);
  orderOverviewUseCase.setNewLocationAction(event.locationAction);
  await orderOverviewUseCase
      .saveOrder(preOrderId: event.preOrderId ?? "")
      .initFuture()
      .onStart(() {
        emit(state.copyWith(status: OrderOverviewStatus.showFullLoadingDialog));
      })
      .onSuccess((data) {
        updateClientDetailStreamController.add(state.deleteAction);
        updateOrderStreamController.add(null);
        emit(state.copyWith(status: OrderOverviewStatus.save));
      })
      .onError((error) {
        if (error is IncorrectTimeException) {
          emit(state.copyWith(status: OrderOverviewStatus.timeError));
        }
        emit(state.copyWith(
          status: OrderOverviewStatus.error,
          lastOrderType: event.orderType,
        ));
      })
      .onFinished(() {})
      .executeFuture();
}
```

### StreamSubscription lifecycle

BLoCs that subscribe to use-case streams or cross-feature controllers store the subscription, cancel before re-subscribing, and cancel in `close()`. Example (from `ClientInfoBloc`):

```dart
class ClientInfoBloc extends Bloc<ClientInfoEvent, ClientInfoState> {
  final ClientInfoUseCase clientInfoUseCase;

  StreamSubscription? _clientInfoStreamSubscription;
  StreamSubscription? _clientPhotoStreamSubscription;

  ClientInfoBloc({required this.clientInfoUseCase}) : super(ClientInfoState.initial()) {
    on<ClientInfoInitialEvent>((event, emit) async {
      clientInfoUseCase.setClientId(event.clientId);
      _getClient();
      _getClientPhotos();
      await _getConfigClient(emit);
    });
  }

  void _getClient() {
    _clientInfoStreamSubscription?.cancel();
    _clientInfoStreamSubscription = clientInfoUseCase.getClient().listen(
      (event) => add(ClientInfoGetEvent(client: event)),
      onError: (error) {},
    );
  }

  @override
  Future<void> close() {
    _clientInfoStreamSubscription?.cancel();
    _clientPhotoStreamSubscription?.cancel();
    return super.close();
  }
}
```

**Cancel before re-subscribing.** Every `_xxxSub = stream.listen(...)` is preceded by `_xxxSub?.cancel()`. Otherwise re-running `_getClient()` (e.g. on `clientId` change) leaves the old listener attached and the BLoC starts processing two events for every emission.

**Cancel in `close()`.** Every BLoC overrides `close()` and cancels every subscription field before calling `super.close()`. Otherwise the subscription survives the BLoC and tries to emit into a closed BLoC, throwing.

## Page pattern

Pages live next to their BLoC under `lib/presentation/features/<feature>/<feature>_page.dart`. Every page is a `StatefulWidget` with the same lifecycle.

```dart
// lib/presentation/features/order/orderoverview/order_overview_page.dart
@RoutePage()
class OrderOverviewPage extends StatefulWidget {
  final OrderManageType orderManageType;
  final List<Product> productList;

  const OrderOverviewPage({
    super.key,
    required this.orderManageType,
    required this.productList,
  });

  @override
  State<OrderOverviewPage> createState() => _OrderOverviewState();
}

class _OrderOverviewState extends State<OrderOverviewPage> {
  late final OrderOverviewBloc _bloc = OrderOverviewBloc(
    orderOverviewUseCase: appGetIt(),
    updateOrderStreamController: appGetIt(),
    updateClientDetailStreamController: appGetIt(),
  );

  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final TextEditingController commentController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _callResultLocationStream();
    _bloc.add(OrderOverviewInitialEvent(
      orderManageType: widget.orderManageType,
      productList: widget.productList,
    ));
  }

  @override
  void dispose() {
    commentController.dispose();
    _bloc.close();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      lazy: false,
      create: (context) => _bloc,
      child: initialUi(),
    );
  }

  Widget initialUi() {
    return Scaffold(
      resizeToAvoidBottomInset: false,
      appBar: AppBar(/* … */),
      body: BlocConsumer<OrderOverviewBloc, OrderOverviewState>(
        listener: (context, state) => _listenerBuilder(state),
        builder: (context, state) => _initialBuilder(state),
      ),
    );
  }
}
```

Conventions:
- `@RoutePage()` on the widget class — AutoRoute codegen picks it up to generate `OrderOverviewRoute`.
- `late final _bloc = MyBloc(...)` field, BLoCs resolved via `appGetIt()` constructor injection.
- `initState` adds the init event.
- `dispose` calls `_bloc.close()` **always**, and any `TextEditingController`/`AnimationController`/`StreamSubscription` fields are disposed/cancelled here too.
- `build` returns `BlocProvider` (with `lazy: false` so `initState`-emitted state is available on first frame); body is `BlocConsumer` (listener for side effects, builder for rendering).
- The builder typically switches on `state.status` to pick a subtree.

### Pages with StreamSubscriptions

Pages that listen to cross-feature stream controllers (see [06-streams-and-cross-feature](./06-streams-and-cross-feature.md)) own the subscriptions themselves:

```dart
// lib/presentation/features/client/detail/client_detail_page.dart
class _ClientDetailState extends State<ClientDetailPage>
    with SingleTickerProviderStateMixin {
  final UpdateClientDetailActionStreamController updateClientDetailActionStreamController = appGetIt();

  StreamSubscription? _updateClientDetailSubscription;
  StreamSubscription? _syncRequiredSubscription;

  late final AnimationController _menuAnimationController;
  late final Animation<Offset> _slideAnimation;

  final ClientDetailBloc _bloc = ClientDetailBloc(/* … */);

  @override
  void initState() {
    super.initState();
    _menuAnimationController = AnimationController(vsync: this, duration: const Duration(milliseconds: 300));
    _slideAnimation = Tween<Offset>(begin: const Offset(0, 1), end: Offset.zero)
        .animate(CurvedAnimation(parent: _menuAnimationController, curve: Curves.easeOutCubic));
    _listenClientDetailUpdateOrder();
    _listenSyncRequired();
    _bloc.add(ClientDetailInitialEvent(clientId: widget.clientId));
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
    _menuAnimationController.dispose();
    _updateClientDetailSubscription?.cancel();
    _syncRequiredSubscription?.cancel();
    _bloc.close();
    super.dispose();
  }
}
```

The same cancel-before-resubscribe / cancel-in-dispose rule that applies to BLoC subscriptions applies to page subscriptions.

> The `client_detail_page.dart` and `client_list_page.dart` files currently have known StreamSubscription leaks flagged in CLAUDE.md (see [10-conventions §Known issues](./10-conventions.md)). The pattern shown above is the **correct** pattern — those files just don't follow it yet.

## `FutureHandler`

`lib/core/handler/future_handler.dart` — the standard error-funnel for use-case calls. Every BLoC handler that awaits a `Future<T>` from a use case wraps it in this chain.

```dart
class FutureHandler<T> {
  final Future<T> future;
  Function? _onStart;
  Function(T data)? _onSuccess;
  Function(AppException error)? _onError;
  Function? _onFinished;

  FutureHandler(this.future);

  FutureHandler<T> onStart(Function callback) { _onStart = callback; return this; }
  FutureHandler<T> onSuccess(Function(T data) callback) { _onSuccess = callback; return this; }
  FutureHandler<T> onError(Function(AppException error) callback) { _onError = callback; return this; }
  FutureHandler<T> onFinished(Function callback) { _onFinished = callback; return this; }

  Future<void> executeFuture() async {
    try {
      _onStart?.call();
      final result = await future;
      _onSuccess?.call(result);
    } catch (e, stackTrace) {
      _onError?.call(e.toAppException(stackTrace));
    } finally {
      _onFinished?.call();
    }
  }
}
```

Exposed as a Future extension:

```dart
// lib/core/handler/future_handler_exts.dart
extension FutureExtensions<T> on Future<T> {
  FutureHandler<T> initFuture() => FutureHandler(this);
}
```

Standard usage:

```dart
await useCase
    .getConfigOrder()
    .initFuture()
    .onStart(() { /* maybe emit loading */ })
    .onSuccess((data) {
      emit(state.copyWith(
        isRequertDateLoad: data.dateLoad,
        paymentRequired: data.paymentRequired,
      ));
    })
    .onError((error) {
      // error is AppException
    })
    .onFinished(() { /* maybe hide loading */ })
    .executeFuture();
```

What `FutureHandler` buys you:

- **Type guarantee on errors.** `executeFuture` catches `dynamic`, converts via `.toAppException(stackTrace)` (which knows about Dio, the four `AppNetworkException` subtypes, and falls back to `AppNetworkDioException` for unknown errors), so `.onError` always gets an `AppException`. Pages and BLoCs never see raw `DioException` or `SqliteException`.
- **No try/catch boilerplate** in every BLoC handler.
- **Consistent ordering** — start always runs first, success or error runs in the middle, finished always runs even on exception. Cleanup (e.g. hide dialog) belongs in `onFinished` exclusively.

See [09-error-handling](./09-error-handling.md) for the full exception pipeline.

## AutoRoute

`lib/core/router/app_router.dart` — every navigation target is declared here as an `AutoRoute(page: XxxRoute.page)` entry. The codegen tool `build_runner` generates `app_router.gr.dart` with the `XxxRoute` classes that match each `@RoutePage()` widget. Re-run generation any time you add/remove a route:

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

```dart
@AutoRouterConfig()
class AppRouter extends $AppRouter {
  @override
  List<AutoRoute> get routes => [
    AutoRoute(page: CheckSeverRoute.page, initial: true),
    AutoRoute(page: LoginRoute.page),
    AutoRoute(page: UserListRoute.page),
    AutoRoute(page: MainRoute.page, children: [
      AutoRoute(page: HomeRoute.page, initial: true),
      AutoRoute(page: DailyClientsRoute.page),
      AutoRoute(page: OddmentsRoute.page),
      AutoRoute(page: MoreMenuRoute.page),
    ]),
    AutoRoute(page: ClientDetailRoute.page),
    AutoRoute(page: TaskDashboardRoute.page),
    AutoRoute(page: SearchRoute.page),
    AutoRoute(page: SynchronizeRoute.page),
    AutoRoute(page: QrCodeRoute.page),
    AutoRoute(page: ClientListMapRoute.page),
    AutoRoute(page: ClientManageRoute.page),
    AutoRoute(page: PreOrderRoute.page),
    AutoRoute(page: OrderManageRoute.page),
    AutoRoute(page: ProductPhotoManageRoute.page),
    AutoRoute(page: OrderOverviewRoute.page),
    AutoRoute(page: ClientMapRoute.page),
    AutoRoute(page: ClientInfoRoute.page),
    AutoRoute(page: DebtorListRoute.page),
    AutoRoute(page: ReviseReportRoute.page),
    AutoRoute(page: SettingsRoute.page),
    AutoRoute(page: OrderHistoryListRoute.page),
    AutoRoute(page: OrderHistoryDetailRoute.page),
    // … 77 routes total
  ];
}
```

Key observations:

- `CheckSeverRoute` is the initial route at the router level. The actual first screen the user sees is decided by `App._initialRoute()` (see [08-navigation-and-shell](./08-navigation-and-shell.md)) which uses `FlavorConfig.isLogin / isNewDay / hasUsers` to override.
- **`MainRoute` is a 4-tab shell.** Its children are `HomeRoute` (default), `DailyClientsRoute`, `OddmentsRoute`, `MoreMenuRoute`. The page widget is `MainPage` and it uses `AutoTabsRouter` with a custom bottom-navigation bar. See [12-feature-deep-dives/main-shell](./12-feature-deep-dives/main-shell.md).
- Navigation in code uses the generated route classes:
  ```dart
  context.router.push(const SynchronizeRoute());
  context.router.replaceAll([const MainRoute()]);
  context.router.navigateBack();
  ```

## `lib/widgets/` — shared widget library

A large reusable widget library: **133 Dart files across 135 directories**. Highlights:

| Folder | What it offers |
|--------|----------------|
| `builder/` | List/grid item builders per domain — `builder/client/`, `builder/order/`, `builder/product/`, `builder/payment/`, `builder/refund/`, `builder/report/`, `builder/selection/`, `builder/state/` (loading/empty/error scaffolding), `builder/total/`, … |
| `form_field/` | `custom_text_form_field.dart`, `custom_labeled_drop_down_flied.dart`, `password_form_field.dart`, `login_form_field.dart`, plus `validator/` for shared validation rules |
| `button/` | Elevated, text, icon, menu variants |
| `dialog/` | Loading, add, monthly, price |
| `alerts/` | Toast/snackbar/alert dialogs |
| `bottomsheet/` | Bottom-sheet shells |
| `image/` | Image builders, photo loaders |
| `card/`, `divider/`, `menu/`, `text/`, `radiobutton/`, `switch/`, `time/`, `keyboard/`, `map/`, `snack_bar/` | Smaller composites |

When you need a list item for a feature, look in `widgets/builder/<feature>/` first — there's almost always an existing one.

## `lib/presentation/support/`

| Folder | Purpose |
|--------|---------|
| `alert/` | Alert dialog helpers and extensions |
| `bottomsheet/` | `bottom_sheet_extension.dart` — `context.showBottomSheet(...)` style helpers |
| `button_general_padding/` | Padding constants for button layouts |
| `error/` | `error_message_exts.dart` — `.toAppException()`, `.localizedMessage` extensions |
| `extensions/` | `call/`, `date/`, `double/`, `exception/`, `image/`, `int/`, `location/`, `string/`, `xfile/` — utility extensions used everywhere |
| `percentage/` | `percentage_calculator.dart` (used by `SynchronizeBloc` — see [07-synchronize](./07-synchronize.md)) |
| `yandex/` | Yandex Maps integration helpers |

## `lib/presentation/common/`

Shared BLoC-driven flows used by multiple features. Each is a full feature shell (page + BLoC + state + event), invoked by name:

| Folder | Purpose |
|--------|---------|
| `bluetooth/` | Discovery + pairing a Bluetooth thermal printer |
| `comment/` | Comment input + display reused across orders and clients |
| `filter/` | Generic filter selection UI |
| `location/` | Location picker / map overlay |
| `menu/` | Shared menu / popup actions |
| `photoview/` | Image viewer with zoom/pan |
| `product/` | Product picker / selector |
| `search/` | Global search page (`SearchRoute`) |
| `selection/` | `selection/single/`, `selection/multiple/` — selection dialogs |
| `time/` | Time picker / duration input |

These are real routes (e.g. `SearchRoute` is in `app_router.dart`). Feature BLoCs push them and listen for results via the page's pop value or via a stream controller.

## Performance rules (recap)

Mirrored from `CLAUDE.md` because they're presentation-layer rules:

| Rule | Why |
|------|-----|
| Always cancel every `StreamSubscription` | Prevents memory leaks |
| Cancel previous subscription before re-subscribing | Prevents duplicate listeners |
| Call `_bloc.close()` in `dispose()` | Cleans up BLoC + its subscriptions |
| `key: ValueKey(item.id)` on list item widgets | Prevents UI jank and state bugs on list updates |
| Use `ListView.builder` / `ListView.separated` | Performance on large lists |
| Use `const` constructors on widgets | Enables widget caching |
| Never mix `setState()` with BLoC | Double rebuilds |
| No heavy computation (sort, filter, map) inside `build()` | Move to state or a getter on State |
| Use `BlocSelector` when only one field drives a subtree | Avoids unnecessary rebuilds |
| Prefix internal events with `_` | Enforces they are only added from within the BLoC |

See [10-conventions](./10-conventions.md) for the full code-style list and known pending issues.

Next:

- [06-streams-and-cross-feature](./06-streams-and-cross-feature.md) — the 14 cross-feature stream controllers
- [08-navigation-and-shell](./08-navigation-and-shell.md) — `App`, `_initialRoute`, MainPage tabs, force-update
- [12-feature-deep-dives/](./12-feature-deep-dives/main-shell.md) — concrete examples
