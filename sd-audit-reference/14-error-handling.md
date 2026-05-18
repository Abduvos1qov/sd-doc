# 14 — Error handling

Errors travel as **values** (`Either<Failure, T>`), not exceptions.
The translation from "exception" to "value" happens exactly once, in
`BaseRepositoryImpl`. Domain and presentation never `try/catch` for
business errors.

## The `Failure` hierarchy

`lib/features/sd_audit/core/error/failure.dart` (full file):

```dart
import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  const Failure(this.message);

  @override
  List<Object?> get props => [message];
}

class ServerFailure extends Failure {
  final int? statusCode;
  final String? errorCode;
  const ServerFailure(super.message, {this.statusCode, this.errorCode});

  @override
  List<Object?> get props => [message, statusCode, errorCode];
}

class LocaleFailure extends Failure {
  const LocaleFailure(super.message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(super.message);
}
```

| Class | Used when | Comparable | Carries |
|---|---|---|---|
| `ServerFailure` | HTTP non-2xx / API error envelope | yes | `message`, `statusCode`, optional `errorCode` |
| `NetworkFailure` | No-connectivity errors | yes | `message` (often the sentinel `'check_internet'`) |
| `LocaleFailure` | Local DB / mapping / cache error | yes | `message` |

`Failure` extends `Equatable`, so BLoC tests can compare error states
by value, not identity. Note the spelling: `LocaleFailure` is the
local-storage failure type; the name is a historical typo for
`LocalFailure` and is now baked in.

## `ApiException`

`lib/features/sd_audit/core/error/exceptions.dart` (full file):

```dart
import 'dart:convert';
import 'package:dio/dio.dart';

class ApiException implements Exception {
  final String message;
  final int? statusCode;
  final int? errorCode;

  ApiException({required this.message, this.statusCode, this.errorCode});

  factory ApiException.fromJson(Response response) {
    dynamic json = response.data;
    if (json is String) json = jsonDecode(json);

    var message = '';
    if (json['errors'] != null && json['errors']['login'] != null) {
      message = (json['errors']['login'] as List).first;
    } else if ((json as Map).containsKey('message')) {
      message = json['message'];
    } else if (json.containsKey('error')) {
      message = json['error'];
    }
    if (message.isEmpty) {
      if (json.containsKey('exception')) {
        message = json['exception'];
      } else {
        message = response.toString();
      }
    }

    return ApiException(
      message: message,
      statusCode: response.statusCode,
      errorCode: response.data['error_code'],
    );
  }

  @override
  String toString() => message;
}
```

`ApiException.fromJson(response)` parses several fields the server
may use, in this priority order:

1. `errors.login[0]` — login-form-style validation
2. `message`
3. `error`
4. `exception`
5. fallback: `response.toString()` (a string version of the Response)

This handles the SalesDoc API's varied error shapes without each call
site having to know which shape it's getting.

## End-to-end error flow

```mermaid
sequenceDiagram
    participant Bloc
    participant UC as UseCase
    participant Repo
    participant HC as HttpClient
    participant API

    Bloc->>UC: usecase.call(param)
    UC->>Repo: repo.method(param)
    Repo->>HC: dio call (via remote data source)
    HC->>API: HTTP
    alt 2xx
        API-->>HC: 200 + body
        HC-->>Repo: Response
        Repo-->>UC: Right(parsed)
        UC-->>Bloc: Right(value)
        Bloc->>Bloc: emit SuccessState
    else 4xx/5xx with body
        API-->>HC: 4xx + body
        HC->>HC: throw ApiException.fromJson(response)
        HC-->>Repo: ApiException
        Repo->>Repo: catch in workWithServer
        Repo-->>UC: Left(ServerFailure(msg, code))
        UC-->>Bloc: Left(...)
        Bloc->>Bloc: emit ErrorState(l.message.tr())
    else network error
        API--xHC: timeout / connection refused
        HC-->>Repo: DioException
        Repo->>Repo: catch in workWithServer; classify connection error
        Repo-->>UC: Left(NetworkFailure('check_internet'))
        UC-->>Bloc: Left(...)
        Bloc->>Bloc: emit ErrorState('check_internet'.tr())
    end
```

## The `Either.fold` pattern in BLoCs

```dart
final result = await usecase.call(param);
emit(result.fold(
  (l) => SomeErrorState(error: l.message.tr()),
  (r) => SomeSuccessState(data: r),
));
```

`fold((l) => ..., (r) => ...)` is exhaustive: every `Either` returns
exactly one of the two cases. The localization (`.message.tr()`)
happens **at emit**, not earlier. Reasons:

- Keeps `data/` and `domain/` Flutter-free (no `easy_localization`
  imports below the BLoC layer).
- Preserves the sentinel `'check_internet'` for log analysis until
  the very last moment.

## The `'check_internet'` sentinel

Three sites participate:

1. **`HttpClient`** — sets `'check_internet'` (or similar variants) as
   the `DioException.message` when the inner error indicates no
   connection.
2. **`BaseRepositoryImpl.workWithServer`** — recognizes
   `'No internet'` and `'check_internet'` in the message, returns
   `Left(NetworkFailure('check_internet'))`.
3. **BLoC** — `.tr()` resolves `check_internet` against the user's
   locale; the translation file shows a friendly message.

Stay consistent: don't rename the sentinel in one place without the
other two. There is no enum.

## 401 / token expiry

`HttpClient` does **not** auto-refresh tokens. A 401 response is
returned to the repo, the repo returns it as a `ServerFailure(401,
"unauthorized")`, and the consuming BLoC must:

1. Set `generalBox.setUnauthenticatedError(true)`.
2. Emit a `TokenExpiredState`.
3. The screen catches `TokenExpiredState` in `BlocListener` and
   navigates back to login (`Phoenix.rebirth(context)` is a common
   shortcut).

`DashboardBloc`, `MerchandiserBloc`, and `DownloadBloc` all emit a
`TokenExpiredState`. Other BLoCs treat 401 as just another
`ServerFailure`, which is a bug surface — if those error-stated
screens get stuck without redirecting, users see a vague error and
have to hard-restart.

## 422 (form validation)

`HttpClient` returns 422 responses without throwing. Repos must
parse the body and translate it into a domain error. Most don't —
they treat it as success and downstream code blows up. A targeted
review of every endpoint that can return 422 (login, set-client,
set-task) is on the cleanup list.

## What's logged

`ErrorLoggingInterceptor` writes every error response to
`network_logs_YYYY-MM-DD.txt` in the app documents directory. The
log includes the path, params (without secrets, by convention),
response body. The `LogFilesPage` lets a developer inspect them on
device. Logs older than 7 days are auto-deleted at startup.

`FlutterError.onError` is wired to `FlutterError.presentError` — i.e.
the default behavior of dumping to stderr. It does **not** record to
Crashlytics. To capture async errors, `PlatformDispatcher.instance.onError`
needs wiring (open item; see [`20`](20-known-issues-and-debt.md)).

## What an "error state" actually looks like to the user

A snackbar via `top_snackbar_flutter`:

```dart
showTopSnackBar(
  Overlay.of(context),
  CustomSnackBar.error(message: state.error),
);
```

Some pages also keep a red banner inline (e.g. `DownloadScreen` shows
the per-step `errorMap` from the sync repo as a list of error rows).
