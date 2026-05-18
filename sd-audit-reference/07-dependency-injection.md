# 07 — Dependency injection

DI is done with **`get_it` 7.x**, a service-locator. The whole graph
is built in **`lib/injection_container.dart`** (1,101 lines), which
exposes a single `setUp()` function called from `main.dart` before
`runApp`.

```dart
// main.dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  ...
  await di.setUp();
  ...
  runApp(EasyLocalization(... child: MultiBlocProvider(...)));
}
```

`getIt` is the global instance; modules call `getIt<T>()` to resolve
dependencies, or use the convenience getter on the file scope.

## Registration kinds

Per `CLAUDE.md`:

| API | Behavior | Used for |
|---|---|---|
| `registerFactory<T>(() => ...)` | New instance on every `getIt<T>()` call | BLoCs, Repositories |
| `registerLazySingleton<T>(() => ...)` | Single instance, created on first access | Use cases, Data sources, Services, NetworkInfo |
| `registerSingleton<T>(...)` | Single instance, created eagerly | Dio, interceptors (eager because they're needed during DI init) |

**Why BLoCs are factories**: A page that re-opens needs a fresh BLoC
(no stale state from the previous mount). The `MultiBlocProvider` in
`main.dart` wires each BLoC type as `create: (_) => getIt<FooBloc>()`,
which invokes the factory.

**Why repositories are factories**: Same idea — a fresh repo per
consumer means no shared mutable state. (`SynchronizationRepositoryImpl`
in particular has an `errorMap` field that's reset per call.)

**Why use cases are lazy singletons**: Use cases are stateless wrappers
around a repository method; one instance shared everywhere is fine.

## Registration order

The `setUp()` function follows a strict bottom-up order:

```
core / network  →  data sources  →  repositories  →  use cases  →  blocs
```

In code:

```dart
Future<void> setUp() async {
  // 1. Core
  getIt.registerSingleton<LoggingInterceptor>(LoggingInterceptor());
  getIt.registerSingleton<ErrorLoggingInterceptor>(ErrorLoggingInterceptor());
  getIt.registerSingleton<NetworkCheckInterceptor>(NetworkCheckInterceptor());
  getIt.registerSingleton<Dio>(Dio()..interceptors.addAll([...]),
      instanceName: 'localDio');
  getIt.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(...));

  // 2. Hive
  getIt.registerLazySingleton<GeneralBox>(() => /* awaited init */ );

  // 3. HTTP client
  getIt.registerLazySingleton<HttpClient>(
      () => HttpClient(dio: getIt<Dio>(instanceName: 'localDio')));

  // 4. Data sources
  getIt.registerLazySingleton<RemoteDataSources>(
      () => RemoteDataSourceImpl(httpClient: getIt()));
  getIt.registerLazySingleton<UserDataSources>(() => UserDataSourceImpl());
  getIt.registerLazySingleton<TrackGpsDataSource>(() => TrackGpsDataSourceImpl());

  // 5. Repositories (factories)
  getIt.registerFactory<LoginRepository>(
      () => LoginRepositoryImpl(remoteData: getIt(), networkInfo: getIt()));
  // ... 22 more

  // 6. Use cases (lazy singletons)
  getIt.registerLazySingleton(() => LoginUsecase(getIt()));
  // ... 79 more

  // 7. Location services
  getIt.registerLazySingleton<LocationService>(...);
  getIt.registerLazySingleton<LocationSenderService>(...);
  getIt.registerLazySingleton<MainLocationService>(...);

  // 8. BLoCs (factories)
  getIt.registerFactory<LoginBloc>(() => LoginBloc(
        checkServerUsecase: getIt(),
        loginUsecase: getIt(),
        supportUsecase: getIt(),
      ));
  // ... 28 more
}
```

If you flip this order — register a BLoC before its use cases — the
first `getIt<UseCase>()` resolution will throw a "Not registered"
error at first BLoC construction. The order also matters for
`registerSingleton`s that depend on each other (`Dio` needs the three
interceptors registered first).

## The BLoC factory table

The 29 globally registered BLoCs (from `injection_container.dart` and
`main.dart`'s `MultiBlocProvider`):

| BLoC | Use cases / services injected |
|---|---|
| `LoginBloc` | `CheckServerUsecase`, `LoginUsecase`, `LoginSupportUsecase` |
| `InfoBaseBloc` | `InfoBaseUsecase` |
| `StockBloc` | `StockUsecase` |
| `ReviseBloc` | `ReviseUsecase` |
| `HelpBloc` | (none) |
| `NotificationBloc` | `NotificationUsecase` |
| `PhotoReportBloc` | `PhotoReportSortedPhotoUsecase`, `PhotoReportPhotosUsecase`, `PhotoReportPhotoTypesUsecase`, `PhotoReportVisitUsecase`, `PhotoReportRemovePhotoUsecase`, `PhotoReportAddNewPhotoUsecase` |
| `DashboardBloc` | `ChangeUserUsecase`, `DashboardUsecase`, `LogoutUsecase`, `DashboardConfigUsecase`, `SynchronizationUsecase`, `GetUsersListUsecase`, `CheckTokenUsecase`, `SendLocationUsecase`, `MainLocationService` |
| `SplashBloc` | `SplashUsecase` |
| `VisitReportBloc` | `VisitReportUsecase` |
| `ClientReportBloc` | `ClientBalanceReportUsecase` |
| `VisitReportByAgentBloc` | `VisitReportByAgentUsecase` |
| `OrderReportsBloc` | `OrderReportUsecase`, `DateRangeUsecase`, `OrderReportLocalRepository` (direct injection) |
| `DownloadBloc` | `SynchronizationUsecase`, `CheckTokenUsecase`, `LogoutUsecase` |
| `ClientsBloc` | `ClientsListUsecase`, `ClientsClientDataUsecase`, `ClientsVisitsUsecase`, `ClientsConfigUsecase`, `ClientsNewClientDataUsecase`, `ClientsSearchUsecase` |
| `ClientVisitBloc` | `GetClientByClientIdUsecase`, `CommentDataUsecase`, `VisitDataUsecase`, `PhotoDataUsecase`, `PollsDataUsecase`, `AuditDataUsecase`, `ClientVisitGetAllVisitsUsecase`, `ClientsConfigUsecase`, `VisitInitialDataUsecase` |
| `ClientsVisitBloc` | `ClientsVisitUsecase` |
| `ClientInfoBloc` | `ClientInfoAvatarUrlUsecase`, `ClientInfoClientUsecase`, `ClientInfoAgentsUsecase`, `SetAvatarUsecase`, `DeleteAvatarUsecase` |
| `ClientEditBloc` | `ClientEditGetAgentsUsecase`, `ClientEditGetTerritoriesUsecase`, `ClientEditGetChannelsUsecase`, `SetEditedClientUsecase`, `UpdateClientUsecase`, `ClientInfoClientUsecase`, `AddClientGetCategoryDataUsecase` |
| `AddNewClientBloc` | `AddClientConfigUsecase`, `AddClientGetAgentDataUsecase`, `AddClientGetTerritoryDataUsecase`, `AddClientGetChannelDataUsecase`, `AddClientGetCategoryDataUsecase`, `AddNewClientUsecase` |
| `VisitBloc` | `VisitGetConfigUsecase`, `VisitGetClientUsecase`, `VisitGetVisitUsecase` |
| `TasksBloc` | `TasksGetTasksUsecase`, `TasksGetAgentsUsecase`, `TasksGetTaskTypesUsecase` |
| `ManageTaskBloc` | (no use cases — uses static helpers) |
| `EditTaskBloc` | `EditTaskGetTaskTypesUsecase`, `EditTaskSetTaskUsecase`, `EditTaskGetAgentsIdUsecase` |
| `MerchandiserBloc` | mirror of `DashboardBloc` with merch-specific use cases |
| `PollsBloc` | `PollsGetPollResultUsecase`, `PollsSavePollResultUsecase` |
| `CommentBloc` | (no use cases — uses ObjectBox directly) |
| `OrderReportByAgentBloc` | `OrderReportByAgentUsecase` |
| `AuditBloc` | `AuditGetAuditResultUsecase`, `DashboardConfigUsecase`, `AuditSaveAuditUsecase` |

## `MultiBlocProvider` in `main.dart`

After `setUp()` resolves, every globally needed BLoC is provided once
to the widget tree:

```dart
runApp(
  EasyLocalization(...,
    child: MultiBlocProvider(
      providers: [
        BlocProvider<LoginBloc>(create: (_) => getIt()),
        BlocProvider<DashboardBloc>(create: (_) => getIt()),
        // ... 27 more
      ],
      child: Phoenix(child: const MyApp()),
    ),
  ),
);
```

Three BLoCs are deliberately **not** registered here:

- `ClientsVisitBloc`, `ReviseBloc`, `StockBloc`, `OrderReportsBloc`,
  `ClientBalanceBloc`, the date-range / map BLoCs — they're created
  locally with `BlocProvider(create: ...)` on the page that owns them.

The reason is lifecycle: a global provider keeps the BLoC alive for
the whole app session and you have to reset it manually; a local
provider disposes when the page pops, which is exactly right for
"one-shot" pages like a stock screen.

## The Phoenix wrapper

`MultiBlocProvider` is wrapped in `Phoenix(child: const MyApp())`.
`flutter_phoenix` lets the app restart itself (call
`Phoenix.rebirth(context)`), used after logout to clear all BLoC
state without manually closing every BLoC. The DI container itself
is **not** reset on rebirth — `getIt` is process-global. Only the
widget tree is rebuilt.

## Globals you can reach without `getIt`

A few singletons are exposed as plain Dart globals for convenience:

- `objectBox` — set in `main()` after `ObjectBox.create(name: 'obx-data')`.
- `generalBox` — declared in `lib/features/sd_audit/utils/objects.dart`
  as `final GeneralBox generalBox = getIt.call<GeneralBox>();`.
- `navigatorKey` — declared at top of `main.dart`, passed to
  `MaterialApp` so `didChangeAppLifecycleState` can push the
  `DownloadScreen` from outside a `BuildContext`.
- `selectedLocale` — `Locale?` updated by the settings screen so
  `EasyLocalization` can pick it up on restart.

These globals are a deliberate convenience but they're a **testing
liability**: any test that pulls in code referencing `objectBox` or
`generalBox` will need them initialised first. See [`19-testing.md`](19-testing.md).

## Adding a new dependency

Order matters. To add `FooBloc`:

1. Confirm its repository impl is registered (if new, add it before
   use cases).
2. Confirm its use cases are registered (after the repo, before the
   bloc).
3. Register `FooBloc` as a `registerFactory`.
4. Add `BlocProvider<FooBloc>(create: (_) => getIt())` to
   `MultiBlocProvider` in `main.dart` (or a local provider in the page).

Full step-by-step in
[`21-feature-development-guide.md`](21-feature-development-guide.md).
