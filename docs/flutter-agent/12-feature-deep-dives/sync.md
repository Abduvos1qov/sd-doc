---
title: Sync — page and BLoC
sidebar_position: 1
---

# Sync — page and BLoC

This is the per-route walkthrough of the sync UI. For the cross-cutting sync architecture (background notifications, the `is_sync` contract, `SyncConfigCache`, full sync chain) see [07-synchronize](../07-synchronize.md).

## Files

| File | Lines |
|------|-------|
| `lib/presentation/features/synchronize/synchronize_page.dart` | 428 |
| `lib/presentation/features/synchronize/bloc/synchronize_bloc.dart` | 1,430 |
| `lib/presentation/features/synchronize/bloc/synchronize_state.dart` | 77 |
| `lib/presentation/features/synchronize/bloc/synchronize_event.dart` | small (2 events) |
| `lib/domain/usecase/synchronize/synchronize_usecase.dart` | 145 |
| `lib/domain/usecase/synchronize/synchronize_usecase_impl.dart` | 420 |
| `lib/presentation/support/percentage/percentage_calculator.dart` | 42 |

## Page

`lib/presentation/features/synchronize/synchronize_page.dart`:

```dart
late final SynchronizeBloc _bloc = SynchronizeBloc(
  synchronizeUseCase: appGetIt(),
  updateOrderStreamController: appGetIt(),
  updateRejectionStreamController: appGetIt(),
  updatePhotoReportStreamController: appGetIt(),
  isNeedSyncConfig: widget.isNeedSyncConfig,
);

late AnimationController _animationController;
double lastPercentage = 0.0;
```

The BLoC injects three of the cross-feature stream controllers — every sync emits to them so other features ([06-streams-and-cross-feature](../06-streams-and-cross-feature.md)) refresh their data after the pipeline finishes.

### BlocConsumer

```dart
listener: (context, state) {
  if (state.status == SynchronizeStatus.hasForcedSyncInToday) {
    _openMainPage(context);
  }
  if (state.status == SynchronizeStatus.timeZoneError) {
    _showErrorAlertDialog(state.errorMessage, state.type);
  }
  if (state.status == SynchronizeStatus.error) {
    showErrorAlert(state.errorMessage, state.type);
  }
  if (state.status == SynchronizeStatus.completed) {
    _handleUpdateDialog(context, state);
  }
},
```

| Status | UI behavior |
|--------|-------------|
| `loading` | Animated `CircularPercentIndicator` + `LinearProgressIndicator` + current step name |
| `hasForcedSyncInToday` | Skip the sync screen entirely — server says sync was already forced today; navigate straight to MainRoute |
| `timeZoneError` | Custom error dialog with a button to open the device's date/time settings (device clock is too far from the server's) |
| `error` | Error alert with a Retry button that fires `RetryEvent(syncType: state.type)` |
| `completed` | `_handleUpdateDialog(...)` checks `forceUpdate`/`recommendUpdate` and pops the update dialog if needed; then navigates to MainRoute |

### Loading UI

```dart
CircularPercentIndicator(
  radius: MediaQuery.of(context).size.width * 0.4,
  percent: _circlePercentage(state),
  lineWidth: 4,
  animation: true,
  animationDuration: 1000,
  animateFromLastPercent: true,
  backgroundColor: context.border,
  progressColor: context.textPrimary,
),
```

A 4-pixel-wide animated ring around the percentage. `animateFromLastPercent: true` means the indicator interpolates smoothly between emissions instead of snapping.

Below the ring, the current step name and percentage text:

```dart
Widget _resultPercentageText(String synchronizeName, double percentage) {
  return Column(
    children: [
      Text('${'synchronized'.tr()}: ${percentage.toInt()}%', …),
      const SizedBox(height: 10),
      Text(synchronizeName, …),
    ],
  );
}
```

`synchronizeName` is the localized name of the current step (e.g. `'clients'.tr()`, `'photo_reports'.tr()`) — set on every state emission by the BLoC's `_emitPercentageAndNameState(value)`.

A linear progress bar sits below:

```dart
LinearProgressIndicator(
  value: progressValue,
  minHeight: 6,
  backgroundColor: context.border,
  valueColor: AlwaysStoppedAnimation<Color>(context.textSuccess),
)
```

### End-of-sync update dialog

```dart
void _handleUpdateDialog(BuildContext context, SynchronizeState state) {
  if (!state.forceUpdate && !state.recommendUpdate) return;
  final currentVersion = AppVersionManager().getVersion();

  if (state.forceUpdate) {
    context.showUpdateVersionDialog(
      () => Platform.isAndroid
          ? _launchInAppUpdate(immediate: true)
          : _openStore(),
      forceUpdate: true,
    );
  } else if (state.recommendUpdate &&
             _isNewerVersion(state.appVersion, currentVersion)) {
    final versionPref = appGetIt<VersionDataPreference>();
    if (versionPref.getDismissedRecommendVersion() == state.appVersion) return;
    context.showUpdateVersionDialog(
      () => Platform.isAndroid
          ? _launchInAppUpdate(immediate: false)
          : _openStore(),
      onDismiss: () => versionPref.saveDismissedRecommendVersion(state.appVersion),
    );
  }
}
```

This is the same dialog `App._checkForceUpdate` shows (see [08-navigation-and-shell §Force / recommend update](../08-navigation-and-shell.md#force--recommend-update-flow)). For a new-day sync, `App._checkForceUpdate` skips the dialog and lets the sync page show it instead — so the user sees it once, after sync, rather than mid-pipeline.

## State

`lib/presentation/features/synchronize/bloc/synchronize_state.dart`:

```dart
@immutable
class SynchronizeState {
  final int percentage;
  final String synchronizeName;
  final String currentRequestName;
  final int current;
  final int total;
  final SyncType type;
  final String lastSyncName;
  final bool forceUpdate;
  final bool recommendUpdate;
  final String appVersion;
  final SynchronizeStatus status;
  final String errorMessage;
  final bool checkingUpdateVersion;

  SynchronizeState({
    this.percentage = 0,
    this.synchronizeName = "",
    this.currentRequestName = "",
    this.current = 0,
    this.total = 0,
    this.lastSyncName = '',
    this.type = SyncType.config,
    this.forceUpdate = false,
    this.status = SynchronizeStatus.loading,
    this.recommendUpdate = false,
    this.appVersion = "",
    this.errorMessage = "",
    this.checkingUpdateVersion = false,
  });

  SynchronizeState copyWith({ … });
}

enum SynchronizeStatus {
  completed,
  error,
  hasForcedSyncInToday,
  timeZoneError,
  loading,
}
```

Fields worth knowing about:
- `current`/`total` — populated by the photo-report streaming step so the UI can show "uploading 3 of 17".
- `type: SyncType` — every error-state emission carries the step it failed on, so the Retry button knows what to re-fire.
- `lastSyncName` — the most-recently-completed step's localized name. Shown on error states so the user sees "Last successful: clients" before the failing step.

## Events

```dart
sealed class SynchronizeEvent {}

class InitialEvent extends SynchronizeEvent {}
class RetryEvent extends SynchronizeEvent {
  final SyncType syncType;
  RetryEvent({required this.syncType});
}
```

Two events. `InitialEvent` kicks off the whole pipeline from `_getConfig`; `RetryEvent` re-enters at a specific step.

## BLoC essentials

```dart
on<InitialEvent>((event, emit) {
  _getConfig(isNeedSyncConfig);
});
on<RetryEvent>((event, emit) {
  _retryData(event.syncType);
});

PercentageCalculator calculator = PercentageCalculator(29);
```

The pipeline is implemented as 44+ private methods chained via `FutureHandler.onSuccess(...) → _nextHandler()`. Each handler:

1. Calls `_emitPercentageAndNameState(localizedStepName)` on start.
2. Awaits the matching `synchronizeUseCase.xxx()` future via `.initFuture().onSuccess(...).onError(...).executeFuture()`.
3. On success, calls the next handler.
4. On error, calls `_emitErrorState(syncType, lastSynName, message)`.

See the [§The chain, in order](../07-synchronize.md#the-chain-in-order) table in 07-synchronize for the full ordered list of 44 steps with line numbers.

### `PercentageCalculator(29)`

`lib/presentation/support/percentage/percentage_calculator.dart`:

```dart
class PercentageCalculator {
  final int count;        // 29
  int currentIndex = -1;
  List<int> percentages = [];
  int cumulativeSum = 0;

  PercentageCalculator(this.count) { _calculateInitialPercentages(); }

  void _calculateInitialPercentages() {
    const int totalPercentage = 100;
    int basePercentage = totalPercentage ~/ count;
    int remainingPercentage = totalPercentage - (basePercentage * count);
    percentages = List<int>.filled(count, basePercentage);
    for (int i = 0; i < remainingPercentage; i++) percentages[i]++;
    percentages.shuffle();
  }

  int calculatePercentages() {
    if (currentIndex == -1) { currentIndex = 0; return 0; }
    if (currentIndex < count) {
      cumulativeSum += percentages[currentIndex];
      currentIndex++;
    }
    return cumulativeSum;
  }
}
```

`29` is hard-coded at `synchronize_bloc.dart:48`. It's the historical step count — the pipeline has since grown to ~44 distinct handlers. In practice not every handler ticks the percentage, so the bar reaches 100% close to (not exactly at) sync completion. **If you add a new step that calls `_emitPercentageAndNameState`, increment `29`** (or refactor `PercentageCalculator` to track the live step count).

The `shuffle()` is intentional — it distributes the rounding remainder pseudo-randomly so the bar doesn't accelerate noticeably in the first few or last few steps.

### Error path

```dart
void _emitErrorState(SyncType type, String lastSynName, String message) {
  emit(SynchronizeState(
    errorMessage: message,
    lastSyncName: lastSynName,
    type: type,
    status: SynchronizeStatus.error,
  ));
}
```

Notice this constructs a **new** `SynchronizeState`, not `state.copyWith(...)`. All transient fields (percentage, syncName, current/total) reset to defaults; only the error info is set. The Retry button reads `state.type` and dispatches `RetryEvent(syncType: state.type)` to resume from that exact step.

### Retry dispatch

`_retryData(SyncType)` (line 1285) is one giant switch that maps every `SyncType` enum value to its private handler. When adding a new step:

1. Add a `SyncType` value in `lib/domain/model/local/sync/sync_type.dart`.
2. Add a `case SyncType.newThing: _newThingHandler(); break;` in `_retryData`.
3. Add the handler itself.
4. Wire the handler into the chain at the right position (`.onSuccess(...) → _newThingHandler();` in the prior handler).

Skipping step 2 silently breaks Retry — the switch falls through and nothing happens.

## Sub-flows worth knowing

### Photo report streaming (`_sendPhotoReport`)

```dart
// synchronize_bloc.dart:298 (abridged)
final stream = synchronizeUseCase.sendAndClearPhotoReports();
await for (final progress in stream) {
  emit(state.copyWith(
    current: progress.current,
    total: progress.total,
    synchronizeName: 'photo_reports'.tr(),
    status: SynchronizeStatus.loading,
  ));
}
```

Unlike every other step (one HTTP call per resource), photo reports are sent one at a time and the stream yields progress events so the UI can show "uploading 3 of 17". After it finishes, the BLoC calls `_sendPhotoReportTgNotify(ids)` (line 327) with the list of successfully-uploaded photo report IDs so the server can fan out a Telegram notification to the supervisor.

### Conditional `_getPendingClients`

```dart
// synchronize_bloc.dart:470 (abridged)
.onSuccess((_) async {
  final verifyEnabled = await synchronizeUseCase.isVerifyEnabled();
  if (verifyEnabled) {
    _getPendingClients();
  } else {
    _getProductList();
  }
})
```

The "pending clients" feature exists for tenants who require supervisor verification of new agent-created clients. If the tenant has it disabled, the step is skipped entirely.

## Cross-feature emissions at the end

After `_saveLastSyncTime` and `_checkUpdateVersion`, the BLoC fires:

```dart
updateOrderStreamController.add(null);          // synchronize_bloc.dart:1188 / 1215
updateRejectionStreamController.add(null);      // :1189 / :1216
updatePhotoReportStreamController.add(null);    // :1190 / :1217
```

Three of the cross-feature stream controllers. Pages subscribed to those (daily clients, client list, more-menu) automatically refresh their badge counts. See [06-streams-and-cross-feature](../06-streams-and-cross-feature.md) for the full emitter/listener map.

## When you change this code

- **Adding a new step** — see "Retry dispatch" above. Plus: update `PercentageCalculator(29)` and add the right `add(...)` calls to relevant stream controllers at the end of the chain.
- **Changing step order** — sends must always run before gets. The send→get boundary is around line 466 (`_getClientInfo`); never reorder a get to run before the matching send.
- **Adding a new failure mode** — if the new error needs a special UI (like `timeZoneError`), add a `SynchronizeStatus` value and a case in the page's `BlocConsumer.listener`. Don't reuse `error` — the Retry button assumes generic errors.
- **Changing the photo-report streaming protocol** — keep `current`/`total` in the state so the UI's "3 of 17" still works.
