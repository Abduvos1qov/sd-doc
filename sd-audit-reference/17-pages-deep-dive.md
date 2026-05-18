# 17 — Pages deep dive

One-line-per-page is in [`05-presentation-layer.md`](05-presentation-layer.md).
This doc zooms in on the ten pages that carry the most logic and the
most user time, plus a quick reference for everything else.

## Heavyweights

### `splash_screen.dart` (141 lines)

**Class:** `SplashScreen`  •  **BLoC:** `SplashBloc` via `SplashUsecase`

Sequence:

1. `CheckUserEvent` on mount.
2. `SplashUsecase.call()` returns `true` if a stored user exists with
   a non-expired token.
3. On success, the BLoC emits `SplashSuccess` → push role-based home.
4. On failure / no user, emit `SplashError` → push `LoginScreen`.
5. A configurable delay before the navigation lets the splash logo
   show for a minimum time.

Also responsible for triggering the day-rollover sync if the last
sync date is yesterday or earlier.

### `login_screen_2.dart` (570 lines)

**Class:** `LoginScreen`  •  **BLoC:** `LoginBloc`

Has two distinct "modes":

- **Server selection** — user enters a 4–8 character code; BLoC posts
  to `https://server.salesdoc.io/api/add?code=...` and returns a
  resolved server URL. The user can also pick from a "previously
  logged in users" list (read from SQLite via `UserDataSourceImpl`).
- **Credential entry** — username + password against the resolved
  server.

Visible BLoC states: `Initial`, `Loading`, `CheckServerSuccess`,
`LoginSuccess`, `LoginSupportData`, `UpdateUI`, `Error`. UI listens
for `LoginSuccess` and runs an initial sync before pushing the
dashboard.

`LoginSupportDataState` populates a contact / help section after
fetching `/support`.

### `dashboard_screen.dart` (1,251 lines)

**Primary BLoC:** `DashboardBloc`  •  **Also reads:** `DownloadBloc`,
the global `objectBox`.

The supervisor home screen. Big — five distinct sub-sections:

1. Header with user info + change-user dropdown.
2. KPI cards (sales today, visits today, etc.).
3. Pie chart breakdown by status (uses `widgets/pie_chart/`).
4. Agent list with per-agent visit counts.
5. FAB → trigger manual sync (delegates to `DownloadBloc`).

States to know:

- `DashboardLoadingState` — initial load
- `DashboardLoadedState` — data ready
- `DashboardSyncLoadingState` — sync running (shows spinner overlay
  but does not redraw the dashboard body)
- `DashboardLocationLoadingState` — sending location only
- `TokenExpiredState` — listener should `Phoenix.rebirth(context)`
- `DashboardErrorNoInternetState` — distinguishes "no net" from
  generic error for a more helpful message
- `UserChangedState` — after `ChangeUserEvent`, triggers a reload

Refactor candidates: the body's five sub-sections should each be a
separate `StatelessWidget`; today they're inlined in `_build*`
methods that share state via local variables in `_DashboardScreenState`.

### `clients_list.dart` (540 lines)

**BLoC:** `ClientsBloc`

Searchable list of clients (`ClientsModelBox`) with:

- Search bar (debounced, dispatches `ClientsSearchEvent`).
- Filters: agent, territory, category, visit-day, status. Filter
  state lives in `SearchModelBox` (ObjectBox) so it survives restarts.
- Tappable rows → `ClientInfoScreen`.
- An "Active visit?" banner at the top if `getActiveVisitClientName`
  returns non-null.

`ClientsBloc` differs from `VisitBloc` and `ClientVisitBloc` —
`ClientsBloc` owns the **list**, not any single visit.

### `client_info_screen.dart` (669 lines)

**BLoC:** `ClientInfoBloc`

Client details + actions. Sections:

- Avatars carousel (`PhotoView`); pick image / delete / set main.
- Identity fields (firm, tel, address).
- Agents who visit (`ToMany`).
- "Start visit" button → `ClientsVisitPage`.
- "Edit client" button → goes to the edit form.

Events: `ClientInfoInitialEvent`, `ClientInfoDeleteAvatarEvent`,
`ClientInfoSetMainAvatarEvent`, `ClientInfoPickImageEvent`.

### `audit_page.dart` (1,136 lines)

**BLoC:** `AuditBloc`

Per-product checklist with custom answer widgets (yes/no, integer,
photo, etc.). The page builds dynamically from the audit's product
list. Heavy on conditional rendering — a candidate to split into
multiple files. See [`16-key-flows.md`](16-key-flows.md) flow 4 for
the data lifecycle.

### `photo_report_screen.dart` (480 lines)

**BLoC:** `PhotoReportBloc`

Grid of photos grouped by category. Adding a photo:

1. `image_picker` (camera or gallery).
2. `flutter_image_compress` to shrink.
3. Save file path + metadata into `PhotoBox` (status `ready`).
4. The next sync POSTs multipart to `setphoto`.

Failed photos surface in `NotificationScreen`.

### `tasks_screen.dart` (578 lines)

**BLoC:** `TasksBloc`

Task list with status filtering (`TaskStatusEnum`). Supervisor can
"manage" (assign / reassign) via `ManageTaskScreen2`; anyone can
create or edit via `EditOrAddNewTaskScreen`. Status transitions are
local-first — the new status writes to ObjectBox immediately and
syncs later.

### `download_screen.dart` (518 lines)

**BLoC:** `DownloadBloc`

The sync UI. Triggers `SynchronizationUsecase.call(isNewDay:)`.
States: `DownloadLoadingState`, `SuccessfullyLoadedState`,
`DownloadErrorState`, `TokenExpiredState`. Renders the `errorMap`
returned by the sync repo as a per-step list with error rows
highlighted.

Has a hard back-button block during loading — confirmed via
`PopScope` — because aborting mid-sync corrupts state.

Also handles the `LogOutEvent` from `DashboardBloc` (consolidated
logout flow lives here).

### `gps_monitoring_page.dart` (56 lines)

Tiny — debug screen showing current `MainLocationService` state +
last-sent positions count. Useful for QA but not exposed in
production menus.

## Notable lighter pages

| Page | Lines | Note |
|---|---|---|
| `merchandiser_dashboard_screen.dart` | 498 | Mirror of `DashboardScreen` for the merchandiser role; emits same state-shape events |
| `comment_screen.dart` | 185 | Form for a single visit comment; writes `CommentResultBox` |
| `polls_page.dart` | 496 | Renders different question widgets from `widgets/polls/` based on `PollVariantBox` type |
| `notification_screen.dart` | 388 | Failed-photo retry queue; entry point: `NotificationBloc` |
| `info_base_screen.dart` | 117 | Renders HTML knowledge-base entries via `flutter_widget_from_html` |
| `log_file_page.dart` | 139 | Lists `network_logs_*.txt` and lets you open one; helpful for support |
| `settings_screen.dart` | 236 | Theme switcher, language switcher, logout |
| `help_screen.dart` | 219 | Contact info from `SupportModel` |
| `client_info_screen.dart` | 669 | (above) |
| `clients_on_map_screen.dart` | 407 | Map view; uses `flutter_map` + clustering |
| `client/visit/clients_visit_page.dart` | 937 | Active-visit screen — the orchestrator for audits, photos, polls, notes, comments |
| `client/form/client_form_page.dart` | 552 | Unified add/edit form, mode chosen by `ClientFormMode` |
| `client/report/client_balance_report_screen.dart` | 552 | Aggregate balance report with date-range filter |
| `client/revise/revise_screen.dart` | 266 | Daily revise per-client view |
| `edit_task_screen.dart` | 1,205 | Add/edit task form; many conditional fields |
| `manage_task_screen.dart` | 1,133 | Status transitions and assignee changes; named `ManageTaskScreen2` because it replaced an earlier version |
| `stock/stock_page.dart` | 272 | Warehouse / product / price-type filter, stock listing |
| `order_report/order_report_screen.dart` | 304 | Order report, drilldown by date/category |
| `report_screen.dart` | 94 | Just an index/navigator to the report screens |

## Gotchas to know

1. **`ClientBalanceBloc` has empty handlers.** `pages/client_balance_report/bloc/`
   declares the bloc but the event handlers are TODOs. The screen is
   navigated to but the bloc never emits anything useful — see
   [`20`](20-known-issues-and-debt.md).
2. **Tabbed pages lose state on swipe.** None of the tab children
   use `AutomaticKeepAliveClientMixin`. Switching tabs and back
   rebuilds the BLoC body, sometimes refetching. Add the mixin if
   you find a tabbed view that's slow.
3. **`visit_entity.dart`'s class is `TaskEntity`.** If you `grep`
   for `TaskEntity` expecting only task code, you'll also catch
   visit code. See [`03`](03-domain-layer.md).
4. **Manage task is the `*Screen2` not `*Screen`.** Old screen still
   exists but is unrouted.
5. **`custom_cards.dart`** at the pages root is _not_ a screen.
   It's a widget file accidentally placed under `pages/`.
