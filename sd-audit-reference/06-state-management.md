# 06 — State management

`flutter_bloc` 9.x throughout. No `Cubit`, no `ChangeNotifier`, no
`Riverpod`, no `setState` for shared state.

## The `part of` pattern

Each BLoC is one folder containing three files. The bloc file declares
`part` directives; the event and state files declare `part of`. This
collapses the public surface to a single import.

```
presentation/bloc/login/
├── login_bloc.dart        // part 'login_event.dart'; part 'login_state.dart';
├── login_event.dart       // part of 'login_bloc.dart';
└── login_state.dart       // part of 'login_bloc.dart';
```

Other files only ever import `login_bloc.dart` — and through that
single import they see `LoginBloc`, every event, and every state.

## Worked example: `LoginBloc`

The login flow is small enough to be the canonical example.

```dart
// login_event.dart
part of 'login_bloc.dart';

abstract class LoginEvent { const LoginEvent(); }
class LoginInitialEvent          extends LoginEvent {}
class CheckServerEvent           extends LoginEvent {
  final ServerRequest serverRequest;
  const CheckServerEvent({required this.serverRequest});
}
class LoginUserEvent             extends LoginEvent {
  final LoginData loginData;
  final ServerData serverInfo;
  const LoginUserEvent({required this.loginData, required this.serverInfo});
}
class DownloadSupportDataEvent   extends LoginEvent {}
```

```dart
// login_state.dart
part of 'login_bloc.dart';

abstract class LoginState { const LoginState(); }
class InitialState              extends LoginState {}
class LoginLoadingState         extends LoginState {}
class UpdateUIState             extends LoginState {}
class CheckServerSuccessState   extends LoginState {
  final ServerData serverInfo;
  const CheckServerSuccessState({required this.serverInfo});
}
class LoginSuccessState         extends LoginState {
  final UserData user;
  const LoginSuccessState({required this.user});
}
class LoginSupportDataState     extends LoginState {
  final SupportModel support;
  const LoginSupportDataState({required this.support});
}
class LoginErrorState           extends LoginState {
  final String error;
  const LoginErrorState({required this.error});
}
```

```dart
// login_bloc.dart
part 'login_event.dart';
part 'login_state.dart';

class LoginBloc extends Bloc<LoginEvent, LoginState> {
  final CheckServerUsecase _checkServerUsecase;
  final LoginUsecase _loginUsecase;
  final LoginSupportUsecase _supportUsecase;

  LoginBloc({
    required CheckServerUsecase checkServerUsecase,
    required LoginUsecase loginUsecase,
    required LoginSupportUsecase supportUsecase,
  })  : _checkServerUsecase = checkServerUsecase,
        _loginUsecase = loginUsecase,
        _supportUsecase = supportUsecase,
        super(InitialState()) {

    on<CheckServerEvent>((event, emit) async {
      emit(LoginLoadingState());
      final result = await _checkServerUsecase.call(event.serverRequest);
      emit(result.fold(
        (l) => LoginErrorState(error: l.message.tr()),
        (r) => CheckServerSuccessState(serverInfo: r),
      ));
    });

    on<LoginUserEvent>((event, emit) async {
      emit(LoginLoadingState());
      final result = await _loginUsecase.call(
        LoginParam(loginData: event.loginData, serverInfo: event.serverInfo),
      );
      emit(result.fold(
        (l) => LoginErrorState(error: l.message.tr()),
        (r) => LoginSuccessState(user: r),
      ));
    });

    on<DownloadSupportDataEvent>((event, emit) async {
      final result = await _supportUsecase.call();
      emit(result.fold(
        (l) => LoginErrorState(error: l.message.tr()),
        (r) => LoginSupportDataState(support: r),
      ));
    });
  }
}
```

The pattern repeats in every BLoC:

1. `on<Event>(...)` for each event class.
2. Emit a `Loading` state immediately.
3. Call a use case (or several).
4. `result.fold((l) => ErrorState(l.message.tr()), (r) => SuccessState(r))`.
5. Localize the error message **right at the emit site** with `.tr()`
   (the sentinel `'check_internet'` becomes a translated string).

## When to use which Bloc widget

| Situation | Widget |
|---|---|
| Rebuild UI as state changes | `BlocBuilder` |
| Side effects only (snackbar, navigation, dialog) | `BlocListener` |
| Both — rebuild AND side effect | `BlocConsumer` |
| Read BLoC without listening (e.g. add event in `initState`) | `context.read<Bloc>()` |
| Reactively read in `build()` | `context.watch<Bloc>()` — **avoid**; use `BlocBuilder` |

`BlocSelector` is rare in the codebase; most "rebuild a small piece"
needs are solved with `BlocBuilder` + `buildWhen`.

## `buildWhen` for rebuild scoping

The standard "ignore irrelevant states" idiom:

```dart
BlocBuilder<DashboardBloc, DashboardState>(
  buildWhen: (prev, curr) => curr is DashboardLoadedState
                          || curr is DashboardLoadingState
                          || curr is DashboardErrorState,
  builder: (context, state) {
    if (state is DashboardLoadingState) return const LoadingWidget();
    if (state is DashboardLoadedState) return _buildContent(state.data);
    if (state is DashboardErrorState) return _buildError(state.error);
    return const SizedBox.shrink();
  },
)
```

If a `DashboardSyncLoadingState` is emitted mid-render, `buildWhen`
returns `false`, so the existing UI doesn't blink. That's important
because dashboards emit many ancillary states (location-loading,
user-changed, etc.) that should not redraw the dashboard body.

## `listener` for navigation / snackbars

Side effects belong in `BlocListener`, not `BlocBuilder`:

```dart
BlocListener<LoginBloc, LoginState>(
  listener: (context, state) {
    if (state is LoginErrorState) {
      showTopSnackBar(Overlay.of(context),
        CustomSnackBar.error(message: state.error));
    } else if (state is LoginSuccessState) {
      Navigator.pushReplacement(context,
        MaterialPageRoute(builder: (_) => SplashScreen()));
    }
  },
  child: ...
)
```

Emitting a snackbar inside a `builder:` is a known footgun — the
builder may run twice in the same frame and stack two snackbars.

## State design: single sealed vs many subclasses

Two styles co-exist:

- **Many subclasses** (most BLoCs): each meaningful state is its own
  class, often `is`-checked with `if (state is FooLoadedState)`. No
  fields on the abstract base.
- **Single sealed-style state** (`ClientReportBloc`, `OrderReportsBloc`,
  `ClientsVisitBloc`): one state class with a `status` field plus
  payload fields. Updates use `state.copyWith(...)`.

The single-state style is newer and cleaner for screens with many
filter knobs (date range, status, category) where the user toggles
several without re-loading. Don't mix the two within a single BLoC.

## Emission rules

1. **Don't `emit` after `close()`.** A BLoC closed during navigation
   that's still running an `await` will throw. The common fix is to
   check `if (isClosed) return;` before each emit, but most BLoCs in
   this codebase rely on awaits being short.
2. **Don't `emit` from outside an event handler.** All emissions
   happen inside an `on<Event>` callback.
3. **States must be immutable.** Use `final` fields; don't mutate
   collections in place.

## Tests

The recommended test stack is `bloc_test` + `mocktail`. Patterns and
the (sparse) current coverage are in
[`19-testing.md`](19-testing.md).
