# 19 — Testing

## Current state

`test/` contains a handful of files — coverage is light. From the
project survey:

| Path | What it tests |
|---|---|
| `test/features/sd_audit/domain/usecases/check_update_version_usecase_test.dart` | The version-check use case happy path |
| `test/features/sd_audit/presentation/bloc/floating_action_button/download_bloc_update_version_test.dart` | A specific download-bloc edge involving version update |
| `test/features/sd_audit/data/mapper/client_form_mapper_test.dart` *(or similar)* | A few mapper conversions |
| `test/features/sd_audit/domain/.../client_model_box_builder_test.dart` | Box builder fixtures |
| `test/widget_test.dart` | Default scaffolding |

**~5 of 80** use cases have a dedicated test. **1 of 35** BLoCs has
focused coverage. **0 of 27** pages have widget tests.

## Stack: `mocktail` + `bloc_test`

From `CLAUDE.md` (authoritative):

```yaml
dev_dependencies:
  bloc_test: ^9.1.0
  mocktail: ^1.0.0
  flutter_test:
    sdk: flutter
```

Why not `mockito`? Mocktail needs no codegen — mocks are inline
classes (`class MockX extends Mock implements X {}`), so adding a
test for a new use case is a single file, not a file plus a re-run
of `build_runner`.

## Use case test pattern

```dart
import 'package:dartz/dartz.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockLoginRepository extends Mock implements LoginRepository {}

void main() {
  late LoginUsecase usecase;
  late MockLoginRepository repo;

  setUp(() {
    repo = MockLoginRepository();
    usecase = LoginUsecase(repo);
  });

  test('returns UserData on success', () async {
    final user = UserData(id: '1', name: 'Test');
    when(() => repo.loginUser(
      loginData: any(named: 'loginData'),
      serverInfo: any(named: 'serverInfo'),
    )).thenAnswer((_) async => Right(user));

    final result = await usecase.call(
      LoginParam(loginData: dummyData, serverInfo: dummyServer),
    );

    expect(result, Right(user));
  });

  test('returns ServerFailure on error', () async {
    when(() => repo.loginUser(
      loginData: any(named: 'loginData'),
      serverInfo: any(named: 'serverInfo'),
    )).thenAnswer((_) async => const Left(ServerFailure('boom')));

    final result = await usecase.call(LoginParam(loginData: dummyData,
        serverInfo: dummyServer));

    expect(result, const Left(ServerFailure('boom')));
  });
}
```

The use cases in this codebase are almost always 1:1 forwards to a
repo method, so the bulk of the meaningful logic is in the repo
impl. Don't waste effort writing a thousand "the use case forwards
to the repo" tests; instead test the repo's translation of
exceptions (a `DioException` should produce a specific `Failure`).

## BLoC test pattern

`bloc_test` removes the boilerplate of subscribing to streams:

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';

class MockLoginUsecase extends Mock implements LoginUsecase {}
class MockCheckServerUsecase extends Mock implements CheckServerUsecase {}
class MockSupportUsecase extends Mock implements LoginSupportUsecase {}

void main() {
  late LoginBloc bloc;
  late MockLoginUsecase loginUsecase;
  late MockCheckServerUsecase checkServerUsecase;
  late MockSupportUsecase supportUsecase;

  setUp(() {
    loginUsecase = MockLoginUsecase();
    checkServerUsecase = MockCheckServerUsecase();
    supportUsecase = MockSupportUsecase();
    bloc = LoginBloc(
      loginUsecase: loginUsecase,
      checkServerUsecase: checkServerUsecase,
      supportUsecase: supportUsecase,
    );
  });

  tearDown(() => bloc.close());

  blocTest<LoginBloc, LoginState>(
    'emits [Loading, Success] on login success',
    build: () {
      when(() => loginUsecase.call(any()))
          .thenAnswer((_) async => Right(UserData(id: '1', name: 'a')));
      return bloc;
    },
    act: (b) => b.add(LoginUserEvent(
        loginData: dummyLogin, serverInfo: dummyServer)),
    expect: () => [
      isA<LoginLoadingState>(),
      isA<LoginSuccessState>(),
    ],
  );

  blocTest<LoginBloc, LoginState>(
    'emits [Loading, Error] on login failure',
    build: () {
      when(() => loginUsecase.call(any()))
          .thenAnswer((_) async => const Left(ServerFailure('boom')));
      return bloc;
    },
    act: (b) => b.add(LoginUserEvent(
        loginData: dummyLogin, serverInfo: dummyServer)),
    expect: () => [
      isA<LoginLoadingState>(),
      isA<LoginErrorState>(),
    ],
  );
}
```

`isA<>()` matchers are used because most state classes don't extend
`Equatable` — comparing by type is the cheapest reliable check.
Where you do want equality, give the state class `Equatable` and
test with literal instances.

## Widget test pattern

Wrap with `EasyLocalization` and `BlocProvider`:

```dart
Widget buildTestWidget(Widget child) {
  return EasyLocalization(
    supportedLocales: const [Locale('uz')],
    path: 'assets/translations',
    fallbackLocale: const Locale('uz'),
    child: BlocProvider<LoginBloc>(
      create: (_) => mockBloc,
      child: MaterialApp(home: child),
    ),
  );
}

testWidgets('shows loading on LoadingState', (tester) async {
  whenListen(
    mockBloc,
    Stream.fromIterable([LoginLoadingState()]),
    initialState: InitialState(),
  );
  await tester.pumpWidget(buildTestWidget(const LoginScreen()));
  await tester.pump();
  expect(find.byType(CircularProgressIndicator), findsOneWidget);
});
```

Use `MockBloc<E, S>` from `bloc_test`:

```dart
class MockLoginBloc extends MockBloc<LoginEvent, LoginState> implements LoginBloc {}
```

then `whenListen(...)` to stream states deterministically.

## Testing repo impls

The interesting part. Two approaches:

### Approach A: mock the data source

```dart
class MockRemoteDataSources extends Mock implements RemoteDataSources {}
class MockNetworkInfo extends Mock implements NetworkInfo {}

test('login impl translates DioException to NetworkFailure for no internet', () async {
  final remote = MockRemoteDataSources();
  final repo = LoginRepositoryImpl(
      remoteData: remote, networkInfo: MockNetworkInfo());

  when(() => remote.loginUser(data: any(named: 'data'), url: any(named: 'url')))
      .thenThrow(DioException(
        requestOptions: RequestOptions(path: ''),
        type: DioExceptionType.connectionError,
        message: 'check_internet',
      ));

  final result = await repo.loginUser(
      loginData: dummyLogin, serverInfo: dummyServer);

  expect(result, const Left(NetworkFailure('check_internet')));
});
```

This is the highest-value test in the codebase — it pins the
`BaseRepositoryImpl` contract.

### Approach B: actual ObjectBox in `setUp`

Local repos (e.g. `ClientsRepositoryImpl`, which uses the global
`objectBox`) can be tested by creating an in-memory or temp-dir
ObjectBox in `setUp` and assigning it to the global. This requires
either:

- Refactoring those repos to take an `ObjectBox` in the constructor
  (clean fix), or
- Reassigning `objectBox` at test setup — works but is ugly.

Prefer the constructor refactor when you start adding tests to a
local repo.

## File layout

Mirror the source path:

```
lib/features/sd_audit/presentation/bloc/login/login_bloc.dart
→ test/features/sd_audit/presentation/bloc/login/login_bloc_test.dart
```

## What to write first

Triage if you have one afternoon:

1. **`BaseRepositoryImpl` translation tests** — three tests: 
   `DioException(connectionError, "check_internet")` → `NetworkFailure`,
   `DioException` other → `ServerFailure`,
   `ApiException(500, "boom")` → `ServerFailure`.
2. **`SynchronizationRepositoryImpl.getAllData` happy path** — wire a
   mock `RemoteDataSources` that returns dummy maps; assert the
   `errorMap` is empty and `lastAutoSynchronizationDate` is updated.
3. **One BLoC per "shape"** — `LoginBloc` covers the
   single-event-then-fold pattern; `DashboardBloc` covers
   multi-state-with-sub-events; that's enough to inform the rest.

`mockito` was deliberately excluded — don't introduce it. Stick with
`mocktail` so tests stay codegen-free.
