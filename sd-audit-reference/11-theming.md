# 11 — Theming

Two themes (light + dark) selected via the `adaptive_theme` package.
Colors are accessed exclusively through `BuildContext` extensions on
`context.*`, **not** through static `AppColors` references. There's a
legacy `AppColors` class still imported by ~68 files; migrating those
is tracked separately (see [`20`](20-known-issues-and-debt.md) and the
project's `THEME_MIGRATION_GUIDE.md`).

## How a page picks a color

Only this:

```dart
import 'package:sdaudit/features/sd_audit/core/themes/extensions/theme_extensions.dart';

// In build():
Container(
  color: context.bgBase,
  child: Text('hello',
    style: TextStyle(color: context.textBase)),
)
```

No theme-mode branching at the call site — `context.bgBase` returns
the right value for the current mode. The extension reads
`Theme.of(context).brightness` internally.

## Token catalogue

From `lib/features/sd_audit/core/themes/extensions/theme_extensions.dart`:

### Brand

| Token | Meaning |
|---|---|
| `context.primary` | Brand color (call-to-action, focus rings) |
| `context.primarySubtle` | Tinted background of primary |
| `context.primarySoft` | A softer fill of primary |

### Background

| Token | Meaning |
|---|---|
| `context.bgBase` | Page background |
| `context.bgSecondary` | Card / panel background |
| `context.bgLower` | Recessed / divider regions |
| `context.buttonBg` | Default neutral button background |

### Text

| Token | Meaning |
|---|---|
| `context.textBase` | Primary content text |
| `context.textSecondary` | Captions / secondary labels |
| `context.textMuted` | Disabled / placeholder text |
| `context.textPrimary` | Text on primary-colored surfaces |
| `context.textWhite` | Always-white text (used over images) |
| `context.textSuccess` | Green status text |
| `context.textWarning` | Yellow status text |
| `context.textDanger` | Red status text |

### Borders

| Token | Meaning |
|---|---|
| `context.border` | Hairline divider / field border |
| `context.borderIntense` | Heavier border for focus / active |

### Status

| Token | Meaning |
|---|---|
| `context.success`, `context.successSoft`, `context.successSubtle` | Three intensities of green |
| `context.warning`, `context.warningSoft`, `context.warningSubtle` | Three intensities of amber |
| `context.danger`, `context.dangerSoft`, `context.dangerSubtle` | Three intensities of red |

### Neutrals (gray scale)

| Token | Meaning |
|---|---|
| `context.neutral0`, `neutral50`, `neutral100`, `neutral200`, `neutral300`, `neutral400`, `neutral500`, `neutral600`, `neutral700`, `neutral800`, `neutral900`, `neutral1000` | 12-step grayscale from black-to-white (or inverted in dark mode) |
| `context.white` | Pure white regardless of mode |

### Helpers

| Property / method | Behavior |
|---|---|
| `context.isDarkTheme` | `bool` getter, reads `Theme.of(context).brightness` |
| `context.dismissDialog()` | `Navigator.pop` for the currently shown dialog |
| `context.showUpdateVersionDialog(...)` | Dialog used by `AppVersionManager` (force / recommend update prompts) |

## Theme assembly

`lib/features/sd_audit/core/themes/theme_dart.dart` exports an
`AppThemeData` namespace with `lightTheme` and `darkTheme`:

```dart
class AppThemeData {
  static ThemeData lightTheme = ThemeData(
    brightness: Brightness.light,
    primaryColor: ...,
    // colorScheme, textTheme, etc.
  );
  static ThemeData darkTheme = ThemeData(
    brightness: Brightness.dark,
    ...
  );
}
```

Wiring in `main.dart`:

```dart
AdaptiveTheme(
  light: AppThemeData.lightTheme,
  dark: AppThemeData.darkTheme,
  initial: AdaptiveThemeMode.system,
  builder: (theme, darkTheme) => MaterialApp(
    theme: theme,
    darkTheme: darkTheme,
    ...
  ),
)
```

`AdaptiveTheme.of(context)` provides:

- `currentMode` — `light`, `dark`, or `system`
- `setLight()`, `setDark()`, `setSystem()`
- Persistence to `SharedPreferences` automatically

## Switching themes at runtime

`presentation/widgets/.../theme_switcher.dart` (in
`settings_screen.dart`) calls:

```dart
final adaptive = AdaptiveTheme.of(context);
if (newMode == AdaptiveThemeMode.dark)   adaptive.setDark();
if (newMode == AdaptiveThemeMode.light)  adaptive.setLight();
if (newMode == AdaptiveThemeMode.system) adaptive.setSystem();
```

The change propagates synchronously: the `MaterialApp` rebuilds with
the new theme, every `BuildContext.foo` getter resolves to the new
palette on the next frame.

## Migration status (`AppColors` → `context.*`)

`THEME_MIGRATION_GUIDE.md` in the project root lists the legacy
`AppColors` identifier → new `context.*` mapping. As of doc time:

- New code should never import `AppColors`.
- ~68 files still reference `AppColors`. Migration is opportunistic
  (touch a file, migrate its colors).
- A migration pass would be one PR per page or per widget folder.

## Pitfalls

1. **Hard-coded `Colors.white` / `Colors.black`** — defeats theming;
   use `context.white` or a neutral.
2. **`context.bgBase` in `initState`** — `BuildContext` isn't safe
   until `build()`. Compute colors in `build`, not `init`.
3. **Caching colors in fields** — colors capture the brightness at
   the time they were read. If you store `final c = context.primary`
   in a `late final` and the user toggles dark mode, `c` is now
   stale. Read tokens fresh each `build`.

## Dark mode coverage

Most pages render correctly in dark mode because they use the tokens.
Known weak spots (per `PROJECT_AUDIT.md`):

- A few legacy widgets in `widgets/client_form/` and
  `widgets/pie_chart/` still hard-code white or `AppColors.*`.
- Maps (`flutter_map`, Google maps) don't switch tile style — the
  light OSM tiles remain regardless of mode.

Verification path: open a screen, toggle dark mode in
`SettingsScreen`, look for any white panels that shouldn't be there
or black text on a black background.
