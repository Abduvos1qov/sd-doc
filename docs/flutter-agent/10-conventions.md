---
title: Conventions
sidebar_position: 10
---

# Conventions

Coding rules, performance rules, and the current technical-debt snapshot. The authoritative source for orchestration rules is the repo's `CLAUDE.md`; this doc reproduces the human-facing parts so they're discoverable without grepping.

## Code style

- **English only** — all code, comments, file names, and identifiers. Russian and Uzbek live in `assets/translations/*.json`, not in source.
- **No `print()` statements** in production code. Use the file-based `LoggingInterceptor` for HTTP, or a `debugPrint` (which is stripped in release) for one-off diagnostics that should never appear in committed code.
- **No `ListView(children: [...])` with dynamic data** — always `ListView.builder` / `ListView.separated` / `ScrollablePositionedList.builder`. The `children:` constructor materializes every item eagerly and kills scroll performance.
- **Don't add docstrings or comments to code you didn't change.** New code: add a single-line comment **only when the WHY is non-obvious** — a hidden constraint, a workaround for a specific bug, a counter-intuitive invariant. If removing the comment wouldn't confuse a future reader, don't write it.
- **Don't explain WHAT the code does** in comments. Identifiers should already say it. Don't reference the current task, PR, or call site (`// added for the ZZZ flow`, `// see ticket #123`) — those belong in commit messages and PR bodies and they rot fast.
- **Don't add features, refactor, or improve code beyond what is asked.** Keep PRs small and focused. Three similar lines is better than a premature abstraction.

## Localization

- Strings live in `assets/translations/ru.json` and `assets/translations/uz.json`.
- Default locale and fallback: `ru`.
- Always use `.tr()` (from `easy_localization`) at the call site: `Text('clients'.tr())`.
- When you add a new `.tr()` key, add the value to **both** `ru.json` and `uz.json` in the same PR. The repo has a `/translate` skill that scans changed Dart files for new keys and fills the gaps.

## BLoC rules

The full rulebook is in `CLAUDE.md` and [04-presentation-layer](./04-presentation-layer.md). Short version:

- **State** is `@immutable`, has a `copyWith`, has a `Status` enum, every field has a default.
- **Events** are a `sealed class`; the file is `part of '<feature>_bloc.dart'`.
- **Internal events** (only added by the BLoC, never from outside) are `_`-prefixed.
- Every `StreamSubscription` is **stored as a nullable field** and **cancelled in `close()`**.
- **Cancel the previous subscription before re-subscribing** — `_sub?.cancel(); _sub = stream.listen(…);`.

## Page rules

- BLoC is `late final _bloc = MyBloc(...)` in the State.
- `_bloc.add(InitEvent())` in `initState`.
- `_bloc.close()` in `dispose`.
- `BlocProvider` (with `lazy: false`) in `build`; `BlocConsumer` for listener + builder.
- `switch (state.status)` to pick which UI subtree to render.

## Performance rules

Mirrored from `CLAUDE.md`:

| Rule | Why |
|------|-----|
| Always cancel every `StreamSubscription` | Prevents memory leaks |
| Cancel previous subscription before re-subscribing | Prevents duplicate listeners |
| Call `_bloc.close()` in `dispose()` | Cleans up BLoC and its subscriptions |
| Add `key: ValueKey(item.id)` to list item widgets | Prevents UI jank and state bugs on list updates |
| Use `ListView.builder` / `ListView.separated` | Performance on large lists |
| Use `const` constructors on widgets | Enables widget caching |
| Never mix `setState()` with BLoC | Double rebuilds; pick one pattern |
| No heavy computation (sort, filter, map) inside `build()` | Move to BLoC state or a getter on State |
| Use `BlocSelector` when only one field drives a subtree | Avoids unnecessary rebuilds |
| Prefix internal events with `_` | Enforces they are only added from within the BLoC |

## Known issues (pending fixes)

These are documented in `CLAUDE.md` as technical debt. **The patterns above are correct; these files just haven't been updated yet.** Verify against the current code before assuming the issue still exists — a fix may have shipped since `CLAUDE.md` was last updated.

### Critical — StreamSubscription leaks

| File | Count |
|------|-------|
| `lib/presentation/features/client/list/client_list_page.dart` | 5 uncancelled subscriptions |
| `lib/presentation/features/defect/list/defect_list_page.dart` | 1 |
| `lib/presentation/features/client/detail/client_detail_page.dart` | 1 |
| `lib/presentation/features/client/oddment/detail/client_oddment_detail_page.dart` | 1 |

The repo has a `/fix-leaks` skill that scans and fixes these automatically.

### High — missing `key` on list items

13 files render list items without `key: ValueKey(item.id)`. Most impactful:
- `client_list_page`, `debtor_list_page`, `equipment_list_page`, `defect_list_page`, `oddments_page`

Adding the key is a one-line fix per builder; do it whenever you touch one of these files.

### Medium — mixed state management

- `lib/presentation/features/payment/payment_manage_page.dart` calls `setState()` **and** `_bloc.add(...)` together. Pick one pattern.
- `lib/presentation/features/settings/settings_page.dart` has an empty `setState(() {})` call. Remove it.

## Adding a new feature

The full orchestration is in `CLAUDE.md`'s "Full Parallel Pipeline". Short checklist for a feature with a new page:

1. **Explore** — read the closest existing feature and its DI/router wiring.
2. **Contracts** — pick model fields, use-case methods, state fields, status enum, events, entity fields.
3. **Domain** — `lib/domain/model/local/<feature>/<feature>.dart`, `lib/domain/repositories/<feature>/`, `lib/domain/usecase/<feature>/`.
4. **Data** — `lib/data/data_source/database/entity/<feature>/`, `lib/data/data_source/database/dao/<feature>/`, `lib/data/data_source/service/<feature>/`, `lib/data/repository_impls/<feature>/`.
5. **Mapper** — `lib/domain/mapper/<feature>/<feature>_mapper.dart`.
6. **BLoC + page** — `lib/presentation/features/<feature>/bloc/<feature>_bloc.dart`, `lib/presentation/features/<feature>/<feature>_page.dart`.
7. **DI** — register repo + use case (+ DAO if new entity) in `repository_module.dart`, `use_case_module.dart`, `database_module.dart`.
8. **Router** — `AutoRoute(page: MyFeatureRoute.page)` in `lib/core/router/app_router.dart`, then `flutter pub run build_runner build --delete-conflicting-outputs`.
9. **Migration** — if a new entity: bump `@Database(version: ...)` and add `_migrationN_to_Nplus1` to `migration_helper.dart` (use the `/db-migration` skill).
10. **Sync** — if the entity carries `is_sync`: add `getNotSyncedX()` DAO method, `sendXAndClear()` use case, a step in `SynchronizeBloc`, a `SyncType` enum value, and a `_retryData` case.
11. **Translations** — every new `.tr()` key goes into both `ru.json` and `uz.json` (use the `/translate` skill).
12. **Tests** — `test/bloc/<feature>/`, `test/unit/usecase/<feature>/`, `test/widget/<feature>/`. Use `mocktail`.
13. **Review** — `/review-flutter` on every Dart file created or changed.

## Useful skills

The repo ships with several `.claude/skills/` you can invoke from `claude code`:

- `/review-flutter` — runs the full Flutter/Dart review checklist on changed files.
- `/translate` — fills missing `.tr()` keys in `ru.json`/`uz.json`.
- `/db-migration` — adds a Floor migration when you create/modify an entity.
- `/fix-leaks` — finds and fixes StreamSubscription leaks.
- `/review-mr` — reviews a GitLab MR.

See `CLAUDE.md` for the routing rules that decide when each gets used.

## Cross-references

- BLoC and page patterns in depth → [04-presentation-layer](./04-presentation-layer.md)
- The 14 cross-feature stream controllers and how to use them safely → [06-streams-and-cross-feature](./06-streams-and-cross-feature.md)
- Boot order, DI modules, `FlavorConfig` → [01-architecture](./01-architecture.md)
- Sync architecture (foreground + background) → [07-synchronize](./07-synchronize.md)
- Database schema and migration rules → [05-database](./05-database.md)
- Error pipeline → [09-error-handling](./09-error-handling.md)
