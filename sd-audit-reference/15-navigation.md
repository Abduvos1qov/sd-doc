# 15 — Navigation

The app uses **plain `Navigator`** with `MaterialPageRoute`. There is
no `GoRouter`, no named routes, no declarative router. Every page
transition is an imperative push.

```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => const ClientInfoScreen()),
);
```

The `MaterialApp` has no `routes:` map and no `onGenerateRoute`. The
`home:` is `SplashScreen`. Everything else is pushed.

## Common patterns

### Push-and-replace (clear stack)

After login or sync completion:

```dart
Navigator.of(context).pushAndRemoveUntil(
  MaterialPageRoute(builder: (_) => const DashboardScreen()),
  (Route<dynamic> route) => false,
);
```

`(route) => false` removes everything; `(route) => route.isFirst`
removes everything but the root.

### Push-and-await result

For pages that return a value (e.g. picker, form):

```dart
final result = await Navigator.push<bool>(
  context,
  MaterialPageRoute(builder: (_) => const EditTaskScreen(taskId: id)),
);
if (result == true) {
  _bloc.add(TaskRefreshEvent());
}
```

### Pop with result

```dart
Navigator.pop(context, true);
```

### Bottom sheets and modals

Two helpers (see [`12-services.md`](12-services.md)):

- `BottomSheetRoute<T>` — a `PageRoute` styled as a draggable sheet.
- `MaterialWithModalsPageRoute` — page route that allows a modal
  sheet to slide over it without breaking the page transition.

```dart
showModalBottomSheet(
  context: context,
  isScrollControlled: true,
  builder: (_) => const AgentOrderReportBottomSheet(),
);
```

## The global `navigatorKey`

`lib/main.dart` declares:

```dart
final GlobalKey<NavigatorState> navigatorKey = GlobalKey<NavigatorState>();
```

Passed to `MaterialApp`:

```dart
MaterialApp(navigatorKey: navigatorKey, ...)
```

It's used to push routes from places that don't have a `BuildContext`
— specifically the lifecycle handler in `_MyAppState`:

```dart
void didChangeAppLifecycleState(AppLifecycleState state) {
  if (state == AppLifecycleState.resumed && differences >= 1) {
    navigatorKey.currentState?.pushAndRemoveUntil(
      MaterialPageRoute(builder: (_) => const DownloadScreen()),
      (route) => false,
    );
  }
}
```

That's the one source of "navigation triggered from outside the tree"
in this codebase. Resist adding more — the more pages can be reached
imperatively from anywhere, the harder back-button state becomes to
reason about.

## Back-button behavior

Default — `Navigator.maybePop` on the Android system back press. A
few pages override with `WillPopScope` / `PopScope` to:

- Confirm "discard changes?" on edit pages.
- Stop a visit cleanly before leaving `ClientsVisitPage`.
- Block back during a sync on `DownloadScreen` (a hard requirement —
  killing the activity mid-sync corrupts the errorMap state).

If you add a screen that has unsaved local state, wrap its root in
`PopScope` (Flutter 3.12+) and emit a confirm dialog from the
`onPopInvoked` callback.

## Why no router?

Flutter's plain Navigator works fine for an app that:

- Has no deep linking from external URLs.
- Has no web/desktop target needing URL-driven navigation.
- Has small screen-flow trees (login → home → page → page back).

The cost is felt in three places:

1. **No type-safe arguments.** Every screen takes constructor args
   freely; you can pass a `String clientId` to `AuditPage` without
   any framework help.
2. **No restoration.** Process-death restore-state in Android doesn't
   work; you have to handle it manually.
3. **No URL syncing for analytics.** Crashlytics has no per-route
   breadcrumb beyond `chucker_flutter`'s observer.

If a future requirement adds deep linking (e.g. "open task XYZ" from
a push notification), migrating to `GoRouter` would be the answer.
Until then, plain Navigator is consistent with the rest of the app.

## Screen-to-screen wiring (typical chain)

```
SplashScreen
   ↓ pushReplacement (user found)
LoginScreen / DashboardScreen
   ↓ pushAndRemoveUntil (DashboardScreen on login)
DashboardScreen
   ├─→ ClientsList → ClientInfoScreen → ClientsVisitPage
   │                                      ├─→ AuditPage
   │                                      ├─→ PhotoReportScreen
   │                                      ├─→ PollsPage
   │                                      └─→ CommentScreen
   ├─→ TasksScreen → EditTaskScreen
   ├─→ SettingsScreen
   ├─→ ReportsScreen → VisitReportScreen / OrderReportScreen / ClientBalanceReportScreen
   ├─→ NotificationScreen
   └─→ DownloadScreen (FAB or auto-trigger)
```

Merchandiser swaps `DashboardScreen` for `MerchandiserDashboardScreen`
but otherwise the same tree.
