# 05 — Presentation layer

`lib/features/sd_audit/presentation/` contains everything the user
sees plus the BLoCs that drive it. Three sub-trees:

- `pages/` — full-screen widgets (27 root + nested page folders)
- `bloc/` — BLoCs grouped one folder per BLoC (35)
- `widgets/` — reusable widgets in 14 subfolders (~111 files)

Pattern (codified in `CLAUDE.md`): `StatefulWidget` page, `late final
_bloc = context.read<...>()` in `initState`, `build()` split into
private `_build*` helpers; events as `*_event.dart` (`part of`),
states as `*_state.dart` (`part of`).

## Pages

### Root-level pages (27)

| File | Class | Lines | Purpose |
|---|---|---:|---|
| `splash_screen.dart` | `SplashScreen` | 141 | Initial load; routes to login or role-based home |
| `login_screen_2.dart` | `LoginScreen` | 570 | Server URL + credentials + role-based redirect |
| `dashboard_screen.dart` | (page widget) | 1251 | Supervisor home, KPIs, agent list, charts |
| `merchandiser_dashboard_screen.dart` | `MerchandiserDashboardScreen` | 498 | Merchandiser home |
| `clients_list.dart` | `ClientsList` | 540 | Searchable client list with filters |
| `client_info_screen.dart` | `ClientInfoScreen` | 669 | Client detail (avatars, fields, history) |
| `clients_on_map_screen.dart` | `ClientsOnMapScreen` | 407 | Map view of clients with clustering |
| `audit_page.dart` | `AuditPage` | 1136 | Audit product checklist + result entry |
| `polls_page.dart` | `PollsPage` | 496 | Poll question display + answer entry |
| `photo_report_screen.dart` | `PhotoReportScreen` | 480 | Photo capture/manage during a visit |
| `comment_screen.dart` | `CommentScreen` | 185 | Visit comment entry |
| `tasks_screen.dart` | `TasksScreen` | 578 | Task list with filtering |
| `edit_task_screen.dart` | `EditOrAddNewTaskScreen` | 1205 | Create/edit a task |
| `manage_task_screen.dart` | `ManageTaskScreen2` | 1133 | Task assignment / status mgmt |
| `download_screen.dart` | `DownloadScreen` | 518 | Sync UI: progress, errors, retries |
| `notification_screen.dart` | `NotificationScreen` | 388 | Failed-photo queue + retry |
| `settings_screen.dart` | `SettingsScreen` | 236 | Profile, theme, language |
| `help_screen.dart` | `HelpScreen` | 219 | Help & contacts |
| `info_base_screen.dart` | `InfoBaseScreen` | 117 | Knowledge base (HTML viewer) |
| `log_file_page.dart` | `LogFilesPage` | 139 | Read on-device network logs |
| `gps_monitoring_page.dart` | `GpsMonitoringPage` | 56 | GPS sender / accuracy monitor |
| `report_screen.dart` | `ReportsScreen` | 94 | Index of report types |
| `visit_report_screen.dart` | `VisitReportScreen` | 200 | Visit report (by agent / date range) |
| `order_report/order_report_screen.dart` | `OrderReportScreen` | 304 | Order report |
| `client_balance_report/client_balance_report.dart` | (wrapper) | 55 | Balance report nav wrapper |
| `client/report/client_balance_report_screen.dart` | `ClientBalanceReportScreen` | 552 | Client balance report screen |
| `stock/stock_page.dart` | `StockPage` | 272 | Warehouse stock view |
| `custom_cards.dart` | (widget, not a screen) | 507 | Reused card components |

### Nested page folders

```
pages/
├── client/
│   ├── form/                        # client_form_page.dart (552), form_mode.dart
│   ├── report/                      # client_balance_report_screen.dart, *_filter.dart
│   ├── revise/                      # revise_screen.dart, balance_card, trade_selection, date_range, table
│   └── visit/                       # visit_list_page (327), clients_visit_page (937), client_header, navigation_row, visit_action_card, visit_button
├── client_balance_report/           # balance_report.dart (55)
├── order_report/                    # order_report_screen.dart (304), widget/ (date picker, filter, main_cards)
└── stock/                           # stock_page.dart (272)
```

`client/visit/clients_visit_page.dart` (937 lines) is the live-visit
screen: the user is checked in, sees the audit/photo/polls/notes
sub-actions, and checks out. It's the connective tissue between most
of the visit feature.

## BLoCs

### Top-level BLoCs (in `presentation/bloc/`)

Each folder contains `{name}_bloc.dart` + `{name}_event.dart` + `{name}_state.dart`.

| Folder | BLoC | Key events | Key states |
|---|---|---|---|
| `add_new_client/` | `AddNewClientBloc` | `Initial`, `ButtonPressed` | `Initial`, `Loading`, `SuccessfullyLoad`, `SuccessfullySave`, `Error` |
| `audit/` | `AuditBloc` | `Initial`, `ButtonPressed` | `Initial`, `Loading`, `SuccessfullySave`, `Load`, `Error` |
| `client_edit/` | `ClientEditBloc` | `Initial`, `ButtonPressed` | `Loading`, `SuccessfullyLoad`, `SuccessfullySave`, `Error` |
| `client_info/` | `ClientInfoBloc` | `Initial`, `DeleteAvatar`, `SetMainAvatar`, `PickImage` | `Loading`, `Loaded`, `AvatarLoaded`, `AvatarDeleted`, `Error` |
| `client_report/` | `ClientReportBloc` | `LoadClientBalanceReport`, `SearchClientBalanceReport`, `FilterClientBalanceReport` | `ClientReportState` (single sealed-style state) |
| `clients/` | `ClientsBloc` | `Initial`, `Search` | `Initial`, `Loading`, `Loaded`, `Error`, `Search` |
| `comment/` | `CommentBloc` | `Initial`, `ButtonPressed` | `Initial`, `Loading`, `SuccessfullySave`, `Load`, `Error` |
| `dashboard/` | `DashboardBloc` | `Initial`, `Refresh`, `LogOut`, `SendLocation`, `ChangeUser`, `ButtonPressed` | `Initial`, `Loading`, `SyncLoading`, `LocationLoading`, `UserChanged`, `FabFinish`, `LoggedOut`, `SendSuccess`, `LocationNotSend`, `Loaded`, `Error`, `ErrorNoInternet`, `TokenExpired` |
| `edit_task/` | `EditTaskBloc` | `Initial`, `ButtonPressed` | `Initial`, `Loading`, `Load`, `Save`, `Error` |
| `floating_action_button/` | `DownloadBloc` | `FabPressed`, `UpdateUI`, `Synchronization`, `LogOut` | `Initial`, `DownloadLoading`, `DownloadError`, `TokenExpired`, `UpdateUI`, `Logout`, `SuccessfullyLoaded` |
| `help/` | `HelpBloc` | `Initial` | `Loading`, `Success`, `Error` |
| `info_base/` | `InfoBaseBloc` | `Initial` | `Loading`, `Success`, `Error` |
| `login/` | `LoginBloc` | `CheckServer`, `LoginUser`, `Initial`, `DownloadSupportData` | `Initial`, `Loading`, `UpdateUI`, `Error`, `CheckServerSuccess`, `LoginSuccess`, `LoginSupportData` |
| `manage_task/` | `ManageTaskBloc` | `UpdateTask`, `Update` | `Initial`, `Loading`, `Load`, `Error` |
| `merchandiser/` | `MerchandiserBloc` | `Initial`, `Refresh`, `Search`, `ChangeUser`, `ButtonPressed`, `Logout`, `SendLocation` | many — mirrors `DashboardBloc` with merch tweaks |
| `notification/` | `NotificationBloc` | `Load`, `DeletePhoto`, `ResendPhotos`, `MarkAllFailed` | `Initial`, `Loaded`, `Resending`, `ResendSuccess`, `Error` |
| `order_report/` | `OrderReportsBloc` | `Initialize`, `LoadReport`, `UpdateDateRange`, `UpdateStatusFilter`, `UpdateCategoryFilter`, `ApplyFilter`, `Dispose` | single `OrderReportState` (sealed-style) |
| `photo_report/` | `PhotoReportBloc` | `Initial`, `RemovePhoto`, `AddPhoto` | `Loaded`, `Error` |
| `polls/` | `PollsBloc` | `Initial`, `ButtonPressed` | `Initial`, `Loading`, `Load`, `SuccessfullySave`, `Error` |
| `splash/` | `SplashBloc` | `CheckUser` | `Initial`, `Success`, `Error` |
| `tasks/` | `TasksBloc` | `Load` | `Initial`, `Loading`, `Loaded`, `Error` |
| `visit/` | `VisitBloc` | `Initial`, `Search` | `Loading`, `Load`, `Error` |
| `visit_report/` | `VisitReportBloc` | `Initial`, `Load` | `Initial`, `Loading`, `Loaded`, `Error` |

### Page-scoped and widget-scoped BLoCs

Not registered globally; created at the page or widget level via
local `BlocProvider`.

| Path | BLoC | Notes |
|---|---|---|
| `pages/client/revise/bloc/` | `ReviseBloc` | client revise screen |
| `pages/client/revise/widgets/revise_date_range/bloc/` | `ReviseDateRangeBloc` | date-range submodule |
| `pages/client/visit/list/bloc/` | `VisitListBloc` | visit list page |
| `pages/client/visit/manage/bloc/` | `ClientsVisitBloc` | the active visit page (start/end visit, save note, delete results) |
| `pages/client_balance_report/bloc/` | `ClientBalanceBloc` | **empty event handler — see [`20`](20-known-issues-and-debt.md)** |
| `pages/order_report/widget/date_picker/bloc/` | `DateRangeBloc` | order report date range |
| `pages/stock/bloc/` | `StockBloc` | stock page |
| `widgets/visit_report_by_agent_bottom_sheet/bloc/` | `VisitReportByAgentBloc` | bottom sheet bloc |
| `widgets/agent_order_report_bottom_sheet/bloc/` | `OrderReportByAgentBloc` | bottom sheet bloc |
| `widgets/map_page/visited_on_map_page/bloc/` | `AllClientsMapBloc` | all-clients map (flutter_map) |
| `widgets/map_page/google_map_pages/clients_on_map_google/bloc/` | `AllClientsMapBloc` | all-clients map (google_maps) |

> Two BLoCs both named `AllClientsMapBloc` — one for the OSM map and
> one for the Google map. They're in different folders, so no name
> conflict, but a refactor that pulls them into the same library would
> collide.

### The three client/visit BLoCs

Worth calling out because they overlap:

| BLoC | Lives in | What it actually owns |
|---|---|---|
| `ClientsBloc` | `bloc/clients/` | Top-level **list of clients** (search, load) |
| `ClientVisitBloc` | `bloc/client_visit/` *(if present)* | Older single-visit data loader (audit + polls + photos + comments + visit-state) |
| `ClientsVisitBloc` | `pages/client/visit/manage/bloc/` | Newer visit lifecycle (start/end, save note, delete results, GPS validation) |

Migration direction: `ClientsVisitBloc` (page-scoped, uses
`ClientsVisitUsecase`) is the modern one. Pages that still use
`ClientVisitBloc` are pre-refactor.

## Widgets

`lib/features/sd_audit/presentation/widgets/` — 14 subfolders, ~111
files.

| Folder | Files | Purpose |
|---|---:|---|
| `agent_order_report_bottom_sheet/` | 4 | Order-report-by-agent bottom sheet (+ its bloc) |
| `bottom_sheet/` | 9 | Generic bottom-sheet building blocks |
| `buttons/` | 2 | Reusable action buttons |
| `client_form/` | 16 | Fields, sections, sheets used by add/edit-client forms |
| `expansion_tile/` | 1 | Custom expandable tile |
| `image_display_screen/` | 3 | Image viewer for avatars/photos |
| `map/` | 3 | Markers, clustering, controls (shared by flutter_map and google_maps) |
| `map_page/` | 8 | Full-page map implementations (OSM + Google) |
| `pie_chart/` | 8 | Chart widget + utilities |
| `polls/` | 8 | Per-question-type widgets (e.g., yes/no, multi-select) |
| `single_selection/` | 1 | Single-choice picker |
| `task_widgets/` | 1 | Task-specific UI pieces |
| `time_zone/` | 1 | Time-zone picker |
| `visit_report_by_agent_bottom_sheet/` | 4 | Visit-report-by-agent bottom sheet (+ its bloc) |

### Localization helpers

`presentation/localization/` holds two files
(`home_localization.dart`, `visit_report_localization.dart`) that
group `.tr()` keys for those subsystems. They're optional sugar — most
files call `.tr()` directly.

## Page-authoring template

```dart
class FooScreen extends StatefulWidget {
  const FooScreen({super.key});
  @override
  State<FooScreen> createState() => _FooScreenState();
}

class _FooScreenState extends State<FooScreen> {
  late final FooBloc _bloc;

  @override
  void initState() {
    super.initState();
    _bloc = context.read<FooBloc>();
    _bloc.add(FooInitialEvent());
  }

  @override
  Widget build(BuildContext context) => Scaffold(
        appBar: _buildAppBar(),
        body: _buildBody(),
      );

  PreferredSizeWidget _buildAppBar() => ...;
  Widget _buildBody() => BlocConsumer<FooBloc, FooState>(
        buildWhen: (prev, curr) => curr is! FooSideEffectState,
        listener: (context, state) {
          if (state is FooErrorState) {
            showTopSnackBar(...);
          }
        },
        builder: (context, state) {
          if (state is FooLoadingState) return const LoadingIndicator();
          if (state is FooLoadedState) return _buildContent(state.data);
          return const SizedBox.shrink();
        },
      );
}
```

See [`06-state-management.md`](06-state-management.md) for the
`Builder` vs `Listener` vs `Consumer` decision matrix and `buildWhen`
guidance.
