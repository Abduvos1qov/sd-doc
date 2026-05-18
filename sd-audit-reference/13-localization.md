# 13 — Localization

`easy_localization` 3.x. Three locales, JSON-keyed strings, default
`uz` (Uzbek).

## Setup

In `main.dart`:

```dart
await EasyLocalization.ensureInitialized();
runApp(
  EasyLocalization(
    supportedLocales: const [
      Locale('ru', ''),
      Locale('uz', ''),
      Locale('en', ''),
    ],
    path: 'assets/translations',
    fallbackLocale: const Locale('uz', ''),
    startLocale: selectedLocale,  // null on first run
    child: MultiBlocProvider(...),
  ),
);
```

And on `MaterialApp`:

```dart
MaterialApp(
  localizationsDelegates: context.localizationDelegates,
  supportedLocales: context.supportedLocales,
  locale: context.locale,
  ...
)
```

## Files

`assets/translations/`:

```
en.json
ru.json
uz.json
```

Each is a flat JSON object: `{ "login": "Login", "error_no_internet": "..." }`.

Plurals and gendered forms use `easy_localization`'s `.plural(n)` API
where needed; most keys are flat strings.

## Usage

The `.tr()` extension on `String`:

```dart
Text('login'.tr());
Text('error_internet'.tr());
```

Some pages group their keys into a static class for autocomplete:

```dart
// presentation/localization/visit_report_localization.dart
abstract class VisitReportL10n {
  static String get title => 'visit_report_title'.tr();
  static String get plan  => 'visit_report_plan'.tr();
  static String get noPlan => 'visit_report_no_plan'.tr();
}
```

These helper classes are optional — they reduce typos but most files
call `.tr()` directly on a string literal.

## Default and startup locale

- **`fallbackLocale`** is `'uz'`. If a key is missing in the current
  locale, Uzbek is consulted.
- **`startLocale`** is the global `Locale? selectedLocale` set by
  `SettingsScreen`. Updating it is a two-step:
  ```dart
  selectedLocale = Locale('en', '');
  await context.setLocale(Locale('en', ''));
  ```
  `easy_localization` persists the choice in `SharedPreferences`.

## Critical keys (used by infrastructure)

| Key | Where it's emitted |
|---|---|
| `check_internet` | `BaseRepositoryImpl.workWithServer`, `HttpClient` — sentinel for the "no connection" error |
| `update_forced`, `update_recommended`, `update`, `later`, `message_forced_update_version` | `AppVersionManager` → version dialog |
| `gps_permission_required`, `gps_permission_required_text` | location-service permission denied state |
| `unauthorized` | 401 response handling |

**Don't translate these inside the data layer.** The convention is
"data layer emits the key as a `Failure.message`, the BLoC translates
it at emission time".

```dart
// In a BLoC handler:
emit(result.fold(
  (l) => LoginErrorState(error: l.message.tr()),  // ← translate here
  (r) => LoginSuccessState(user: r),
));
```

## Day-name abbreviations

Calendar / agent-visit-days widgets reference per-day keys: `mo`, `tu`,
`we`, `th`, `fr`, `sa`, `su` plus combined `mo-su`. They live in each
locale file and are case-sensitive.

## Adding a new key

1. Add the English text to `assets/translations/en.json`.
2. Provide translations in `uz.json` and `ru.json`.
3. Use `'my_new_key'.tr()` at the call site.

You don't need to re-run codegen — `easy_localization` reads files at
runtime. The keys are **not** type-checked; a typo silently renders
the key itself. Test on each locale.

## What is `LanguageCode`?

`lib/features/sd_audit/domain/enums/language_code.dart` declares an
enum (`en`, `uz`, `ru`). It's used in **API requests** — some
endpoints accept a language parameter so server-rendered strings come
back in the user's locale. It's separate from the UI locale.

The two get out of sync if the user changes language: the UI updates
immediately, but the API param refreshes only on the next request
(typically the next sync). Brief inconsistency, harmless.
