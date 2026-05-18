# 09 — Networking

All HTTP goes through a custom `HttpClient` wrapper that owns a `Dio`
instance.

```
[BLoC] → [UseCase] → [Repo impl] → [RemoteDataSourceImpl] → [HttpClient] → [Dio + interceptors] → API
```

## `HttpClient` (`core/http_client/http_client.dart`)

260 lines. Owns one `Dio`, sets 40-second connect & receive timeouts,
JSON response type.

```dart
class HttpClient {
  Dio dio;
  HttpClient({required this.dio});

  BaseOptions baseDioOptions = BaseOptions(
    connectTimeout: const Duration(milliseconds: 40000),
    receiveTimeout: const Duration(milliseconds: 40000),
    responseType: ResponseType.json,
  );

  // Five public methods:
  Future<Response> postRequest(String baseUrl, String api, dynamic params,
      Map<String, dynamic>? header, {Options? options});

  Future<Response> postRequest2(String baseUrl, String api,
      {Map<String, dynamic>? header,
       Map<String, dynamic>? params,
       Map<String, dynamic>? body});

  Future<Response> postRequestForLogin(String baseUrl, String api,
      Map<String, dynamic> params);

  Future<Response> getRequestWithParams(String baseUrl, String api,
      Map<String, dynamic> queryParams);

  Future<Response> getRequest(String baseUrl, String? deviceToken);
}
```

**Behavioral contract:**

1. Each call sets `dio.options = baseDioOptions` at start (re-applies
   the timeouts even if the singleton Dio was mutated elsewhere).
2. **`200–299`** — returns the `Response`.
3. **`401`** — returned as-is (lets repos detect token expiry).
4. **`422`** — returned as-is (form-validation errors with structured
   body).
5. **All other status codes** — throws `ApiException`
   (`ApiException.fromJson(response)` parses the body).
6. **`DioException` (network-level errors)** — wrapped: if the message
   mentions "no internet" / "check_internet", the message is set to
   the localized internet-error key; otherwise rethrown.

Three flavors of POST exist because the API has three calling
conventions:

- `postRequest` — generic; `params` is whatever the endpoint wants
  (Map, FormData, or `setPhoto` payload). Header passed in.
- `postRequest2` — convenience: separate `params` (query) and `body`
  (JSON).
- `postRequestForLogin` — login endpoint specifically, plain JSON body.

`getRequest(baseUrl, deviceToken)` is used by the knowledge-base
endpoint that takes the device token in the path.

## `EndPoints` (`lib/common/constants/end_points.dart`)

All API paths in one place, 57 lines. The base URL is set from
`ServerData.url` at runtime; the `sdBaseUrl` constant is a fallback
hard-coded to `https://server.salesdoc.io`.

### Auth & user

| Constant | Method | Path |
|---|---|---|
| `checkServer` | GET | `https://server.salesdoc.io/api/add?code=` |
| `support` | GET | `https://server.salesdoc.io/support` |
| `login` | POST | `/api3/auditor/login` |
| `login4` | POST | `/api4/login` |
| `profile` | GET | `/api3/auditor/profile` |

### Data fetch

| Constant | Method | Path |
|---|---|---|
| `getDaily` | GET | `/api3/auditor/getDaily` |
| `gpsVisit` | GET | `/api3/auditor/gpsVisit` |
| `gpsVisitByAgent` | GET | `/api3/auditor/gpsVisitBy` |
| `clientBalance` | GET | `/api3/auditor/clientBalance` |
| `totalOrders` | GET | `/api3/auditor/getSummary` |
| `getOrdersByAgent` | GET | `/api3/auditor/detailSummary` |
| `getClients` | GET | `/api3/auditor/clientsV3` |
| `getClientsCategory` | GET | `/api3/auditor/clientCategory` |
| `getAgents` | GET | `/api3/auditor/agentsV2` |
| `getComments` | GET | `/api3/auditor/comment` |
| `taskTypes` | GET | `/api3/auditor/taskType` |
| `photoTypes` | GET | `/api3/auditor/photo` |
| `getConfig` | GET | `/api3/auditor/config` |
| `getPolls` | GET | `/api3/auditor/poll` |
| `getAudits` | GET | `/api3/auditor/audit` |
| `getTerritories` | GET | `/api3/auditor/territory` |
| `getChannels` | GET | `/api3/auditor/channel` |

### Results / writes

| Constant | Method | Path |
|---|---|---|
| `setClient` | POST | `/api3/auditor/setClient` |
| `setTask` | POST | `/api3/auditor/settask` |
| `setPhoto` | POST | `/api3/auditor/setphoto` |
| `setAvatar` | POST | `/api3/auditor/avatar` |
| `deleteAvatar` | POST | `/api3/auditor/deleteAvatar` |
| `setMainAvatar` | POST | `/api3/auditor/setMainAvatar` |
| `pollResult` | POST | `/api3/auditor/pollResult` |
| `auditResult` | POST | `/api3/auditor/auditResult` |
| `commentResult` | POST | `/api3/auditor/commentResult` |
| `noteResult` | POST | `/api3/auditor/noteResult` |
| `checkIn` | POST | `/api3/auditor/checkIn` |
| `trackGPS` | POST | `/api3/auditor/gpsTrack` |
| `task` | POST | `/api3/auditor/task2` |
| `total` | GET | `/api3/auditor/total` |

### API v4 (tasks & catalog)

| Constant | Method | Path |
|---|---|---|
| `postNewTask` | POST | `/api4/create/task` |
| `postEditTask` | POST | `/api4/edit/task` |
| `postEditTaskResult` | POST | `/api4/edit/task-result` |
| `getTaskList` | GET | `/api4/list/tasks` |
| `getStock` | GET | `/api4/stock` |
| `getProduct` | GET | `/api4/catalog/products` |
| `getWarehouseList` | GET | `/api4/catalog/warehouses` |
| `getProductCategory` | GET | `/api4/catalog/productCategories` |
| `getPrice` | GET | `/api4/catalog/prices` |
| `getPriceType` | GET | `/api4/catalog/priceTypes` |
| `getProductImage` | GET | `/api4/catalog/productImage` |
| `getTrade` | GET | `/api4/catalog/trades` |

### Other

| Constant | Method | Path |
|---|---|---|
| `getKnowledgeBase` | GET | `/api3/knowledgeBase?u=agent` |
| `getRevise` | GET | `/api3/client/revise` |
| `checkUpdateVersion` | GET | `/app/audit` |

## Local Dio + interceptors

`lib/features/sd_audit/core/http_client/local_dio/` contains an
alternative pre-configured Dio (registered in `getIt` with
`instanceName: 'localDio'`):

```dart
getIt.registerSingleton<Dio>(
  Dio()
    ..interceptors.addAll([
      getIt<LoggingInterceptor>(),
      getIt<ErrorLoggingInterceptor>(),
      getIt<NetworkCheckInterceptor>(),
    ]),
  instanceName: 'localDio',
);
```

| Interceptor | Purpose |
|---|---|
| `LoggingInterceptor` | Pretty-prints every request and response |
| `ErrorLoggingInterceptor` | Persists errors to `network_logs_YYYY-MM-DD.txt` in app documents directory; 7-day rolling cleanup |
| `NetworkCheckInterceptor` | Short-circuits the request and throws a network error if `connectivity_plus` reports no connection |

The `LogFilesPage` (`pages/log_file_page.dart`) reads those persisted
log files for in-app diagnostics.

`HttpClient` itself uses this 'localDio' instance — confirmed in
`injection_container.dart`:

```dart
getIt.registerLazySingleton<HttpClient>(
  () => HttpClient(dio: getIt<Dio>(instanceName: 'localDio')),
);
```

## SSL bypass (security note)

`lib/main.dart` sets:

```dart
class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback =
          (X509Certificate cert, String host, int port) => true;
  }
}

// In main():
HttpOverrides.global = MyHttpOverrides();
```

**Every certificate is accepted.** No certificate pinning, no
hostname check. This is in shipped release builds. Treat any
on-network adversary as having full MITM capability. Tracked in
[`20-known-issues-and-debt.md`](20-known-issues-and-debt.md).

The standard fix: gate the override behind `kDebugMode` and add
proper certificate pinning for the production hostname.

## chucker_flutter

`chucker_flutter` is wired as a `navigatorObserver` in `MyApp.build`
behind `kDebugMode`. In debug it provides an in-app inspector for
every request — convenient for QA without proxying through Charles
or mitmproxy.

```dart
navigatorObservers: [
  if (kDebugMode) ChuckerFlutter.navigatorObserver,
],
```

## Calling pattern from a repository

```dart
@override
Future<Either<Failure, UserData>> loginUser({
  required LoginData loginData,
  required ServerData serverInfo,
}) =>
    workWithServer(() async {
      final json = await remoteData.loginUser(
        data: loginData,
        url: serverInfo.url,
      );
      return UserData.fromJson(json);
    });
```

`workWithServer` (see [`04-data-layer.md`](04-data-layer.md)) absorbs
every `DioException` and `ApiException`, so the repo body stays a
straight-through translation: call the remote, parse the JSON, return.

## Adding a new endpoint

1. Append the path constant to `EndPoints`.
2. Add the method to the `RemoteDataSources` abstract interface (in
   the right cluster of methods).
3. Implement it in `RemoteDataSourceImpl` using one of the five
   `HttpClient` helpers.
4. Call it from a repository impl wrapped in `workWithServer`.
5. Expose it via a use case.

Step 1 is sometimes skipped (path inlined into the data source);
prefer adding the constant for one-stop discoverability.
