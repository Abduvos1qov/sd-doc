# 20 — Known issues and technical debt

A consolidated list. Most are inherited from `PROJECT_AUDIT.md` (in
Uzbek); a few are spotted while assembling these docs.

## Security

### SSL bypass in release builds

**Where:** `lib/main.dart` (sets `HttpOverrides.global = MyHttpOverrides()`).

```dart
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
  }
}
```

Every certificate is accepted, no hostname check, no pinning. Active
in release builds. **Severity: high** — an attacker on the same
network can MITM all traffic, including login credentials and
location data.

**Fix path:**

1. Gate the override behind `kDebugMode`.
2. Add certificate pinning for `*.salesdoc.io` (`dio_certificate_pinning`
   or `pinned_http_client`).
3. Test on staging with a proxy to confirm pinning works.

### No transport-layer auth refresh

A 401 response is surfaced as a generic `ServerFailure`. Only three
BLoCs (`DashboardBloc`, `MerchandiserBloc`, `DownloadBloc`) react with
a token-expired state; the rest leave the user staring at an error.

**Fix path:** add a Dio interceptor that catches 401, sets
`generalBox.setUnauthenticatedError(true)`, and triggers a global
"go to login" via `navigatorKey`.

### Unencrypted local storage

ObjectBox, Hive, and SQLite stores are unencrypted on device. PII
(client names, phone numbers, addresses) and tokens sit in plain
files. On Android this is somewhat shielded by app sandboxing; on
iOS likewise. Still — for a rooted/jailbroken device or a forensic
extraction, everything is readable.

**Fix path:** ObjectBox supports a built-in encryption flag at store
creation; Hive can be encrypted via `HiveAesCipher`; sqflite has
SQLCipher bindings. Tokens at minimum should move to platform secure
storage (`flutter_secure_storage`).

### `chucker_flutter` in production

Debug-only by `if (kDebugMode)` guard in `MyApp.build`. Confirmed.
Still, double-check that release builds don't ship the package — if
they do (because `kDebugMode` is a runtime check, not a tree-shake
trigger), the package's payload remains in the binary.

## Architecture

### `SynchronizationRepositoryImpl` is too large (1,448 lines)

Does POSTing pending changes, GETing fresh state, mapping JSON to
boxes, persisting, and updating Hive flags. Every new sync step is a
file diff against a 1,500-line file.

**Fix path:** split into orchestrator + post queue + GET fetcher +
persisters. Outlined in [`10`](10-synchronization.md).

### `RemoteDataSourceImpl` is 801 lines

34 methods touching every API surface. A god object.

**Fix path:** split by domain — auth-and-user, reports, catalogs,
photos, etc. Or move to per-feature data sources whose `*Impl`
extends a thin base.

### `injection_container.dart` is 1,101 lines

Hard to scan, no per-feature segmentation.

**Fix path:** one `register*` function per feature, called in order
from `setUp()`. The current style is partial — there are section
comments but no functions.

### Three overlapping client/visit BLoCs

`ClientsBloc`, `ClientVisitBloc`, `ClientsVisitBloc` co-exist. The
last is the modern one. The other two still drive screens.

**Fix path:** migrate consumers off `ClientVisitBloc` first, then
delete it. `ClientsBloc` is fine to keep (different scope: list vs
single).

### Filename typo

`lib/features/sd_audit/domain/repositories/client_edit_repositroy.dart`
("repositroy" vs "repository"). It's also referenced by that name in
`injection_container.dart` and the impl path mirrors the typo.

**Fix path:** rename file + every import in one sweep. Low risk if
done with grep + IDE rename.

### Class-vs-file naming collision

`domain/entities/visit_entity.dart` declares a class named
`TaskEntity`. The actual task entity lives in `task_entity.dart`. A
search for `TaskEntity` returns both files.

**Fix path:** rename the class in `visit_entity.dart` to something
like `VisitMessageEntity` and update its few references.

### `ClientBalanceBloc` has empty event handlers

`pages/client_balance_report/bloc/` declares the bloc and is wired to
the screen, but its event handlers are TODO stubs. The screen
launches but the bloc emits nothing.

**Fix path:** complete the handler or remove the screen until ready.

## UI / state

### Theme migration not complete

~68 files still import `AppColors` (per `PROJECT_AUDIT.md`). Mapping
to the new `context.*` tokens is in
`THEME_MIGRATION_GUIDE.md` at the project root. See
[`11-theming.md`](11-theming.md).

### Tab children don't preserve state

No `AutomaticKeepAliveClientMixin` on `_TabContentState` widgets.
Switching tabs causes rebuilds and sometimes refetches.

**Fix path:** add the mixin where rebuild is expensive (visit list,
client list with filters, etc.).

### Two image-cache libraries

`fast_cached_network_image` (initialized in `main()`) and the older
`cached_network_image` are both depended on. Different code paths
use different libs.

**Fix path:** pick one (most likely `fast_cached_network_image`,
since it's the one initialized at boot), migrate call sites, remove
the other from `pubspec.yaml`.

### No `GoRouter` / named routes

Imperative `Navigator.push` everywhere. No deep linking, no
restoration. See [`15-navigation.md`](15-navigation.md).

**Fix path:** introduce `GoRouter` when there's a concrete need
(push-notification deep links, restoration). Today's pattern is
acceptable.

## Data quality

### Date fields stored as `String`

Many DTOs store dates as `String` (often `"yyyy-MM-dd"` or
`"dd.MM.yyyy"`). Conversion happens at use sites with `DateFormat`.
Risk: format drift, locale issues.

**Fix path:** define a wrapping `Date` type or migrate fields to
`DateTime`. Persistence (ObjectBox) supports int millis directly.

### `LocaleFailure` (sic) — typo for `LocalFailure`

Baked-in name. Renaming touches every file that switches on Failure
type.

**Fix path:** low priority; rename in a single sweep if you do a
data-layer refactor.

### `errorMap` keys are stringly-typed

`SynchronizationRepositoryImpl` populates a `Map<String, String>`
with hard-coded step names (`"clients"`, `"audits"`). Spelling drift
across steps is invisible until you read the screen.

**Fix path:** define a `SyncStep` enum and key the map by it.

## Observability

### Crashlytics doesn't get async errors

`FlutterError.onError` is set to `presentError` (default). No wiring
of `PlatformDispatcher.instance.onError` to
`FirebaseCrashlytics.recordError`. Uncaught async errors don't show
in the console.

**Fix path:** add:

```dart
PlatformDispatcher.instance.onError = (error, stack) {
  FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
  return true;
};
FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError;
```

inside `main()`.

### No analytics events

`firebase_analytics` is imported but unused. No screen-tracking, no
custom events.

**Fix path:** at minimum, log screen views via a `NavigatorObserver`.

## Testing

See [`19-testing.md`](19-testing.md). Coverage is minimal:

- ~5 of 80 use cases have tests.
- 1 of 35 BLoCs has tests.
- 0 of 27 pages have widget tests.
- The repo translations (`workWithServer`) — the single most
  important contract in the codebase — are untested.

## Build hygiene

### Manual `objectbox.g.dart` edit after every codegen

Documented in `README.md`. A CI re-run of `build_runner` will undo
the fix.

**Fix path:**

- Add a Makefile target or `tool/postgen.dart` that re-applies the
  edit programmatically.
- Or change the entity / relation definitions so the generator emits
  the right type.

### Empty / placeholder folders

`lib/features/sd_audit/data/data_sources/db/` and
`lib/features/sd_audit/data/data_sources/database/main_objectbox/entities/client/`
are empty. Remnants of an abandoned refactor.

**Fix path:** delete after confirming with the team.

## Misc

- Several `*Screen2` / `*_v2` files exist alongside their predecessors.
  Sanity-check which is wired before editing — old versions still
  compile.
- The `getDataFromServer({param, api})` family in
  `RemoteDataSourceImpl` collapses many different endpoints behind
  one generic method. Convenient, but means the request shape isn't
  type-checked per endpoint.

## How to triage

If a single quarter of dev time were available, ranked priority:

1. **SSL bypass + certificate pinning** — security hole, ship-stopper.
2. **Crashlytics async error wiring** — small change, big visibility
   gain.
3. **Split `SynchronizationRepositoryImpl`** — unlocks tests for a
   contract that today is untestable.
4. **Theme migration sweep** — paying off existing tokens; low risk.
5. **Filename typo + class collision** — quick, satisfying cleanups.
6. **`ClientBalanceBloc`** — either finish or remove.
