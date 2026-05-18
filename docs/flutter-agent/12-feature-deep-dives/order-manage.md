---
title: order/manage
sidebar_position: 2
---

# `order/manage` — building an order

The product-picker screen the agent uses to assemble a new (or edit an existing) order. After this screen, the user moves to `OrderOverviewRoute` to confirm bonuses, discount, totals, and submit.

| File | Lines |
|------|-------|
| `lib/presentation/features/order/manage/order_manage_page.dart` | 644 |
| `lib/presentation/features/order/manage/bloc/order_manage_bloc.dart` | 506 |
| `lib/presentation/features/order/manage/bloc/order_manage_state.dart` | ~420 |
| `lib/presentation/features/order/manage/bloc/order_mange_event.dart` | ~104 |
| `lib/domain/usecase/order/order_manage_usecase.dart` | 37 |
| `lib/domain/usecase/order/order_manage_usecase_impl.dart` | (impl) |

## Page

`@RoutePage()` widget with `OrderManageType` and other inputs. The type is a sealed-style enum-of-classes that selects between "add new" and "edit existing":

```dart
class _OrderState extends State<OrderManagePage> {
  final OrderManageBloc _bloc = OrderManageBloc(
    orderUseCase: appGetIt(),
    updateOrderProductStreamController: appGetIt(),
  );

  final UpdateOrderProductStreamController updateOrderProductStreamController = appGetIt();

  bool isDisableCheckWarehouse = true;
  bool _isDetected = true;
  bool _isStreamSubscribed = false;

  @override
  void initState() {
    super.initState();
    if (widget.orderManageType is OrderManageTypeAddType) {
      isDisableCheckWarehouse =
          (widget.orderManageType as OrderManageTypeAddType).isDisableCheckWarehouse;
    } else if (widget.orderManageType is OrderManageTypeEditType) {
      isDisableCheckWarehouse =
          (widget.orderManageType as OrderManageTypeEditType).isCheckWarehouse;
    } else {
      isDisableCheckWarehouse = true;
    }
    _bloc.add(OrderInitialEvent(orderManageType: widget.orderManageType));
  }

  @override
  void dispose() {
    _bloc.close();
    super.dispose();
  }
}
```

The init event fan-out then loads visible categories, the client's order config, price-types, manual discount, the product wrapper list, and any data the order needs to display.

The page also subscribes (inside its `build`/state-tree) to `UpdateOrderProductStreamController` so barcode scans from the product-scanner sub-flow (`ProductScannerBloc`) and inline product-edit events both update the on-screen list without going back through the BLoC's main init path.

### Layout

`Scaffold` body wraps a `BlocProvider<OrderManageBloc>` → `BlocBuilder` → `KeyboardDismisser`. Inside:

- **AppBar**: conditional search bar (toggled by `OrderManageOpenSearchEvent`), back button, plus actions: search, QR-code scanner (`ProductScannerRoute`), and filter. Filter shows a badge when any of `selectedCategory`, `selectedBrand`, `query` are set.
- **Body** (`BlocConsumer`):
  - `state.status == loading` → spinner
  - `state.status == error` → error widget with retry
  - `state.status == searchNotFound` → empty result
  - default → `_updateUiBuilder(state)` (the real UI)
- **Main content** (`_updateUiBuilder`):
  - `CategoryWidget` row at top (selected category highlight)
  - `ScrollablePositionedList.builder` — the product list, with `state.selectCategoryProductIndex` driving auto-scroll to the active category
  - `_bottomBarUi` — `PriceTypeItemBuilder` + sticky action buttons

### Bottom bar

```dart
Widget _bottomBarUi(OrderManageState state) {
  return Column(
    children: [
      PriceTypeItemBuilder(priceType: state.priceType, onTap: …),
      Row(children: [
        // Payment-summary button → opens detail view of selected products
        // Next button → navigates to OrderOverviewRoute with the cart
      ]),
    ],
  );
}
```

Tapping "Next" pushes `OrderOverviewRoute` with the `OrderManageData` payload. The overview screen handles the final confirmation, applies discounts/bonuses, and POSTs the order.

## BLoC

### State

```dart
@immutable
class OrderManageState {
  final List<ProductWrapper> originalProductWrapperList;
  final ProductFilter productFilter;
  final DiscountManual discountManual;
  final String errorMessage;
  final double orderMinAmount;
  final String clientId;
  final String tradeId;
  final String orderId;
  final PriceType priceType;
  final OrderManageStatus status;
  final int selectCategoryProductIndex;
  final int selectCategoryIndex;
  final bool isVisibleSearchBar;
  final double minClientOrderSumma;
  final double maxClientOrderSumma;
  final bool isProductsByAlphabet;
  final String query;
  final ProductCategory selectedCategory;
  final ProductBrand selectedBrand;
  final String selectedSubCategoryId;
  final String selectedBrandId;
  final bool isFollowVisitRules;
  final List<String> allowedCategoryIds;

  OrderManageState({ /* every field has a default */ });

  OrderManageState copyWith({ … });
}

enum OrderManageStatus {
  initial, loading, success, empty, error, searchNotFound,
}
```

Note `searchNotFound` as a status separate from `empty` — search yields a different UI treatment from "no products configured at all".

### Events

```dart
class OrderInitialEvent extends OrderManageEvent {
  final OrderManageType orderManageType;
  OrderInitialEvent({required this.orderManageType});
}

class LoadingOrderEvent extends OrderManageEvent {}
class ProductRequested extends OrderManageEvent {}
class UpdateProductItemEvent extends OrderManageEvent { … }
class OrderManageUpdatePriceTypeDetailEvent extends OrderManageEvent { … }
class OrderManageOpenSearchEvent extends OrderManageEvent {}
class OrderManageSearchQueryEvent extends OrderManageEvent { … }
class OrderManageProductFilterEvent extends OrderManageEvent { … }
class OrderManageProductEvent extends OrderManageEvent { … }
class OrderManageUpdateProductListEvent extends OrderManageEvent { … }
class OrderManageProductBrandEvent extends OrderManageEvent { … }
class OrderManageSuccessResultEvent extends OrderManageEvent {}
```

12 events covering: init, in-flight loading, fetch products, edit a single line, change price type / category / brand, open search, search query, filter, save-success.

### Constructor

```dart
OrderManageBloc({
  required this.orderUseCase,
  required this.updateOrderProductStreamController,
}) : super(OrderManageState()) {
  on<OrderInitialEvent>(_onInitialEvent);
  on<UpdateProductItemEvent>(_updateProductItem);
  on<OrderManageUpdatePriceTypeDetailEvent>(_updatePriceType);
  on<OrderManageOpenSearchEvent>(_openSearch);
  on<OrderManageSearchQueryEvent>(_search);
  on<OrderManageProductFilterEvent>(_filter);
  on<OrderManageProductEvent>(_filterByCategory);
  on<OrderManageUpdateProductListEvent>(_updateProductList);
  on<OrderManageProductBrandEvent>(_filterByBrand);
  on<OrderManageSuccessResultEvent>(_clearSelection);
}
```

### Representative handler

```dart
Future<void> _getProductList(emit) async {
  await orderUseCase
      .getProductWrapperList()
      .initFuture()
      .onStart(() {
        emit(state.copyWith(status: OrderManageStatus.loading));
      })
      .onSuccess((data) {
        List<ProductWrapper> sortedList = sortList(data);
        emit(state.copyWith(
          originalProductWrapperList: sortedList,
          status: OrderManageStatus.success,
          selectCategoryProductIndex: 0,
        ));
      })
      .onError((error) {
        emit(state.copyWith(
          status: OrderManageStatus.error,
          errorMessage: error.toString(),
        ));
      })
      .onFinished(() {})
      .executeFuture();
}
```

Standard FutureHandler chain (see [04-presentation-layer §FutureHandler](../04-presentation-layer.md#futurehandler)). The interesting bit is `sortList(data)` — the list is sorted once in the BLoC and stored on state, never in `build()` (the no-heavy-compute-in-build rule from CLAUDE.md).

### Stream emission

Inside `_updateProductItem`:

```dart
updateOrderProductStreamController.add(event.productId);   // ~line 504
```

This is how the BLoC tells anyone subscribed to that controller (notably the page itself, via the `ProductScannerBloc` listening for scan results, and the inline cart-edit widget) that a specific product line just changed.

## UseCase

```dart
abstract class OrderManageUseCase {
  void setOrderMangeType(OrderManageType value);
  Future<ConfigOrder> getConfigOrder();
  Future<ClientOrderConfig> getClientOrderConfig();
  Future<PriceType> getPriceTypeById();
  Future<DiscountManual> getManualDiscount();
  Future<List<ProductWrapper>> getProductWrapperList();
  Future<List<ProductPrice>> getProductPriceList(String priceTypeId);
  void setIsProductsByAlphabet(bool value);
  bool getIsProductsByAlphabet();
  String getClientId();
  String getTradeId();
  bool isFollowVisitRules();
  Future<List<Category>> getVisibleProductCategoryList();
}
```

13 methods. Some return futures (the data fetches), some are setters/getters for state the use case carries between BLoC events (so the BLoC doesn't have to pass them through every method). `OrderManageType` is set once in `_onInitialEvent`, then `getProductWrapperList()` and friends use it internally.

## Order feature siblings

The order module is the largest in the app — 10+ sub-features sit under `lib/presentation/features/order/`. Brief tour:

| Folder | Purpose |
|--------|---------|
| `bonus/` | Bonus picker (auto / manual selection of promotional items attached to the order) |
| `detail/` | Read-only order detail view (after the order is created/synced) |
| `discount/` | Discount picker (manual discount selection per the merchant's discount catalog) |
| `draft/` | Draft list — orders the agent started but didn't submit; they're stored locally and resumable |
| `history/` | Historical order list (server-side orders + locally-synced) with detail view |
| `manage/` | **This page** — product selection / quantity edits |
| `orderoverview/` | Final confirmation screen — totals, comment, tags, price type, bonus, discount, location, save |
| `photo/` | Photo-report attachment flow for an order |
| `preorder/` | Pre-order flow for orders scheduled for a future shipment date |
| `manage/scanner/` | QR/barcode scanner sub-flow (`ProductScannerBloc`) that emits to `UpdateOrderProductStreamController` |

### Hand-off to overview

`OrderManagePage`'s "Next" button calls:

```dart
context.router.push(OrderOverviewRoute(
  orderManageType: widget.orderManageType,
  productList: _bloc.state.originalProductWrapperList.where(/* selected */).toList(),
));
```

`OrderOverviewPage` then:

1. Loads config (`paymentRequired`, `allowToChooseNoBonus`, `isRequertDateLoad`, …)
2. Lets the user add comment, tags, consign date, date-load, price-type
3. Lets the user pick bonus type (auto/manual/none) and select discount
4. On save, calls `orderOverviewUseCase.saveOrder(...)` which builds an `OrderRequest`, persists it, and emits to `UpdateOrderStreamController` + `UpdateClientDetailActionStreamController` to refresh the home dashboard and the client detail page.

For the cross-feature streams it touches, see [06-streams-and-cross-feature §UpdateOrderStreamController](../06-streams-and-cross-feature.md#updateorderstreamcontroller) (13 emit sites; `OrderOverviewBloc` at `:213` is one).

## When you change this code

- **Adding a new product filter dimension** (e.g. by tag): add a state field, an event, a handler. Don't try to add it to the search query — different dimension.
- **Changing the BLoC's stream emission**: keep `UpdateOrderProductStreamController.add(productId)` synchronous with the state update. Listeners assume the controller fires after the state already reflects the change.
- **Sub-flow integration**: anything that mutates products (scanner, photo, bonus) must emit to `UpdateOrderProductStreamController` so the manage page picks it up — don't push events directly to `OrderManageBloc` from another feature.
- **Performance**: this page renders a long list of `ProductWrapper` items. Use `ScrollablePositionedList.builder` (already used), keep `ValueKey(product.id)` on each item, and never sort or filter inside `build()`.
