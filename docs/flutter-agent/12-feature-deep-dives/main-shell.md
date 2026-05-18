---
title: Main shell & home
sidebar_position: 4
---

# Main shell + home tab

This is the per-feature walkthrough of `MainPage` (the 4-tab shell) and `HomePage` (the default tab the user lands on). The shell mechanics — `AutoTabsRouter`, bottom-nav rendering, force-update hooks — are also covered at the architectural level in [08-navigation-and-shell](../08-navigation-and-shell.md).

| File | Lines |
|------|-------|
| `lib/presentation/features/main/main_page.dart` | 143 |
| `lib/presentation/features/main/features/home/home_page.dart` | 1,448 |
| `lib/presentation/features/main/features/home/bloc/home_bloc.dart` | 345 |
| `lib/presentation/features/main/features/home/bloc/home_state.dart` | 137 |
| `lib/presentation/features/main/features/home/bloc/home_event.dart` | 71 |
| `lib/presentation/features/main/features/daily/daily_clients_page.dart` | 413 |
| `lib/presentation/features/main/features/more/more_menu_page.dart` | 593 |

## `MainPage`

`@RoutePage()` shell hosting 4 tabs.

```dart
late final MainBloc _bloc = MainBloc(mainUseCase: appGetIt());

@override
void initState() {
  super.initState();
  _bloc.add(MainInitialEvent());
}

@override
void dispose() {
  _bloc.close();
  super.dispose();
}
```

The page registers `MainBloc` eagerly (`BlocProvider(lazy: false, …)`). The BLoC has minimal duties — first-launch setup of background services, that sort of thing.

### Tab definition

```dart
AutoTabsRouter(
  routes: const [
    HomeRoute(),
    DailyClientsRoute(),
    OddmentsRoute(),
    MoreMenuRoute(),
  ],
  builder: (context, child) {
    final tabsRouter = AutoTabsRouter.of(context);
    return Scaffold(/* child + custom bottom bar */);
  },
)
```

The default tab is `HomeRoute` (`initial: true` in `app_router.dart`).

### Custom bottom bar

Two-layer `Column`:

```dart
// Top: 4-segment selection indicator (underline)
Row(
  children: List.generate(4, (index) {
    return Expanded(
      child: Container(
        height: 2.0,
        color: tabsRouter.activeIndex == index
            ? context.textPrimary
            : context.border,
      ),
    );
  }),
),

// Bottom: standard BottomNavigationBar with 4 items
BottomNavigationBar(
  currentIndex: tabsRouter.activeIndex,
  onTap: tabsRouter.setActiveIndex,
  items: [
    _buildBottomNavigationBarItem(SvgIcons.icCompass,      'visits',   isSelected: tabsRouter.activeIndex == 0),
    _buildBottomNavigationBarItem(SvgIcons.icShopStore,    'clients',  isSelected: tabsRouter.activeIndex == 1),
    _buildBottomNavigationBarItem(SvgIcons.icBoxProduct,   'oddments', isSelected: tabsRouter.activeIndex == 2),
    _buildBottomNavigationBarItem(SvgIcons.icMenuHamburger,'more',     isSelected: tabsRouter.activeIndex == 3),
  ],
)
```

Icons themed via `ColorFilter.mode(...)`:

```dart
SvgPicture.asset(
  icon,
  colorFilter: ColorFilter.mode(
    isSelected ? context.textPrimary : context.neutral500,
    BlendMode.srcIn,
  ),
)
```

## `HomePage`

The largest page widget in the app (1,448 lines). It's the user's daily mission-control: visit count, sync banner, quick filters, "Visits" / "Results" tabs, sync dialog, route management.

### Local stream controllers

```dart
late final ClientVisitFilterStreamController _homeFilterController =
    ClientVisitFilterStreamController(isBroadcast: true);

late final TotalFilterStreamController _totalFilterController =
    TotalFilterStreamController(isBroadcast: true);

late final UpdateSyncRequiredStreamController updateSyncRequiredStreamController = appGetIt();
```

Two of them (`_homeFilterController`, `_totalFilterController`) are **constructed locally** — not pulled from DI. They carry the home tab's own filter state to child pages; they don't need to be shared globally. The third (`UpdateSyncRequiredStreamController`) is the DI singleton — the page listens for the global "sync required" signal so it can pop the sync dialog automatically.

### `initState`

```dart
@override
void initState() {
  super.initState();
  _bloc.add(InitialHomeEvent());

  _tabController = TabController(length: 2, vsync: this);
  _tabController.addListener(() => setState(() {}));

  _listenSyncRequired();
}

void _listenSyncRequired() {
  updateSyncRequiredStreamController.listen((data) {
    _openSynchronizePage(HomeSyncType.fullSync);
  });
}
```

When the sync-required signal arrives (from a notification tap or a per-client sync trigger), it opens the full sync flow inside the page rather than letting the user just see a banner.

### Sync dialog

`_handleState(HomeState state)` (page-level helper called from the BlocConsumer listener):

```dart
void _handleState(HomeState state) {
  if (state.showSyncDialog) {
    showCustomDialog(
      state.lastSyncTime,
      state.isSyncWithPhoto,
      state.isSyncOnlyOrder,
      state.isSyncOnlyPhoto,
    );
  }
  // … other status branches
}
```

`showCustomDialog` renders an `AlertDialog` with:

- A "last sync" timestamp: `"${'last_sync'.tr()}: ${DateFormatter.timeAgo(lastSyncTime)}"`.
- A radio-style toggle between **Photo** and **Order** partial-sync modes.
- A **Sync with Photo** checkbox (drives `state.isSyncWithPhoto`).
- Three actions: "Sync photos", "Sync orders", "Full sync".

Tapping one of the three closes the dialog and pushes `SynchronizeRoute` (or invokes `HomeSynchronizeBloc` for the partial flows). See [08-navigation-and-shell §`HomeSynchronizeBloc`](../08-navigation-and-shell.md#homesynchronizebloc--partial-sync-inside-the-home-tab) for the partial-sync sibling BLoC.

## `HomeBloc`

### State fields

`HomeState` carries the entire home dashboard's data. Grouped by concern:

| Group | Fields |
|-------|--------|
| Sync & dialog | `lastSyncTime: int`, `showSyncDialog: bool`, `showDefectDialog: bool`, `showFullLoadingDialog: bool`, `hideFullLoadingDialog: bool` |
| Display settings | `isShowClientBalance: bool`, `isShowVisitDays: bool`, `isShowClientLegalName: bool`, `isShowUnvisitedClients: bool` |
| Filter state | `clientVisitFilter: ClientVisitFilter`, `totalReportFilter: TotalReportFilter`, plus computed `isFilter` and `isTotalReportFilter` getters |
| Visit counts | `visitedCount: int`, `visitCount: int` |
| Status & lifecycle | `status: HomeStatus?` (`initial`, `loading`, `uploadUi`, `empty`, `error`, `routeFetched`), `isSuccess: bool`, `userName: String` |
| Route & location | `isMadeRoute: bool`, `isAutoRoute: bool`, `shareRoute: bool`, `latLonItems: List<LatitudeLongitude>`, `isSendCurrentLocation: bool`, `location: LocationAction?` |
| Sync modes | `isSyncWithPhoto: bool` *(default true)*, `isSyncOnlyOrder: bool`, `isSyncOnlyPhoto: bool` |

### Events (14)

```dart
InitialHomeEvent
HomeSyncEvent
HomeUpdateDataEvent
HomeFilterVisitEvent
HomeVisitCountEvent
HomeSettingsSaveEvent
HomeSyncWithPhotoEvent
HomeFilterTradeEvent
HomeSyncOnlyPhotoEvent
HomeSyncOnlyOrderEvent
HomeClearRouteEvent
HomeFetchRouteStatusEvent
HomeFetchAutoRouteStatusEvent
HomeClientRouteLocations
```

### Constructor

```dart
HomeBloc({
  required this.homeUseCase,
  required this.locationService,
  required this.geoLocatorService,
  required this.updateFilterController,
  required this.updateTotalFilterController,
  required this.updateClientDetailStreamController,
  required this.updateClientListStreamController,
}) : super(const HomeState()) {
  // event handlers
}
```

Seven constructor params:

| Dependency | Purpose |
|------------|---------|
| `homeUseCase` | Standard use case — sync, settings, defects, GPS, routes |
| `locationService: BackgroundLocationService` | GPS tracking via the `location` package |
| `geoLocatorService: BackgroundGeoLocatorService` | GPS tracking via the `geolocator` package |
| `updateFilterController: ClientVisitFilterStreamController` | Broadcast filter changes to child pages |
| `updateTotalFilterController: TotalFilterStreamController` | Broadcast trade filter changes to the results tab |
| `updateClientDetailStreamController` | Trigger client-detail refresh after sync |
| `updateClientListStreamController` | Trigger client-list refresh after sync |

### Dual GPS service

Both `BackgroundLocationService` (built on `location`) and `BackgroundGeoLocatorService` (built on `geolocator`) are injected. They're used together because the two packages have complementary platform behaviors — one is more reliable on certain Android versions, the other handles iOS background modes better. Both write to the same `LocationRepository`.

```dart
@override
Future<void> close() {
  geoLocatorService.stopTracking();
  return super.close();
}
```

The BLoC stops geolocator tracking on close so background updates don't continue against a disposed BLoC. `locationService` is managed separately (it usually keeps running).

## `DailyClientsPage`

The "clients" tab. `AutomaticKeepAliveClientMixin` keeps the day tabs alive across navigation:

```dart
class _DailyClientsState extends State<DailyClientsPage>
    with AutomaticKeepAliveClientMixin {
  late final DailyClientsBloc _bloc = DailyClientsBloc(
    updateFilterController: _dailyFilterController,
    clientListUseCase: appGetIt(),
  );

  StreamSubscription? _updateClientListSub;
  StreamSubscription? _updateOrderSub;
  StreamSubscription? _updateRejectionSub;
  StreamSubscription? _updatePhotoReportSub;

  @override
  bool get wantKeepAlive => true;
  // …
}
```

8 tabs: All + Mon, Tue, Wed, Thu, Fri, Sat, Sun. Each tab is a `ClientListPage` initialized with the appropriate `ClientDaySelection` value. Tab badges show `state.dayCounts[ClientDaySelection.xxx].visitCount`.

The 4 stream subscriptions follow the cancel-before-resubscribe / cancel-in-dispose pattern. Each triggers `DailyClientsInitialEvent` to refresh tab counts when the corresponding stream emits.

## `MoreMenuPage`

The "more" tab. Profile view + multi-account switcher + menu items (debtors, KPI, settings, tasks, support, reports, …).

```dart
final MoreMenuBloc _bloc = MoreMenuBloc(moreUseCase: appGetIt());
```

Notable state:

- `state.currentUser: User`
- `state.userList: List<User>` — for the account-switch picker
- `state.moreMenuList: List<MoreMenuItem>`
- `state.isShowUserList: bool` — toggle between profile and user-list views
- `state.accessDebtor: bool` — permission gate
- `state.startTime: int` — non-zero means there's an active check-in; **blocks account switching** to avoid losing the check-in session

Switching accounts (`MoreMenuChangeAccountEvent`) calls `MoreMenuUseCase.switchAccount(user)` which clears the user-bound preferences, then `Phoenix.rebirth(context)` restarts the app — see [08-navigation-and-shell §`Phoenix.rebirth(context)`](../08-navigation-and-shell.md#phoenixrebirthcontext--full-restart).

The page also listens to `UpdateRejectionStreamController` so the rejection badge in the menu stays current.

## When you change this code

- **Adding a new tab**: append `XxxRoute()` to `AutoTabsRouter.routes` AND add a `BottomNavigationBarItem`. Update the selection-indicator `Row(children: List.generate(N, …))` to match the new count. (Right now `N == 4` is hard-coded.)
- **Adding a new home event**: increment the count above and follow the same pattern as `HomeSyncEvent` — use `FutureHandler` for any async work.
- **Don't move `BackgroundGeoLocatorService.stopTracking()` out of `close()`** — leaving it running against a closed BLoC will throw.
- **Don't subscribe to a DI stream controller from a `StatelessWidget`** — there's nowhere to cancel. Use a `StatefulWidget` (or move the subscription into the BLoC).
