---
title: Features catalog
sidebar_position: 11
---

# Features catalog

Index of every feature folder under `lib/presentation/features/`. One row per feature with its description, main route(s), primary BLoC(s), and main use case.

Routes are defined in `lib/core/router/app_router.dart`. BLoCs live under `lib/presentation/features/<feature>/.../bloc/`. Use cases live under `lib/domain/usecase/<feature>/`.

| Feature | Description | Main route(s) | Primary BLoC(s) | Use case(s) |
|---------|-------------|---------------|-----------------|-------------|
| **bill** | Bill receipt rendering (screen, PDF, thermal print) | `BillDetailRoute` | `BillDetailBloc`, `BillDetailSettingsBloc` | `BillDetailUseCase` |
| **check** | Initial server discovery / tenant-code entry on first launch | `CheckSeverRoute` *(initial)* | `CheckServerBloc` | — |
| **client** ★ | Client list, detail, info, map, manage, balance, pending, recommended, oddment | `ClientDetailRoute`, `ClientManageRoute`, `ClientListMapRoute`, `ClientMapRoute`, `ClientInfoRoute`, `ClientOddmentDashboardRoute`, `ClientOddmentManageRoute` | `ClientListBloc`, `ClientDetailBloc`, `ClientManageBloc`, `ClientInfoBloc`, plus oddment BLoCs | `ClientListUseCase`, `ClientDetailUseCase`, `ClientInfoUseCase`, `ClientOddmentUseCase` |
| **debt** | Debt order list and detail | `DebtOrderListRoute` | `DebtOrderListBloc` | `DebtOrderListUseCase` |
| **debtor** | Debtor list with filtering | `DebtorListRoute` | `DebtorListBloc`, `DebtorListFilterBloc` | (repository-driven; thin use case) |
| **defect** | Defect list, management, and summary report | `DefectListRoute`, `DefectManageRoute`, `DefectReportRoute` | `DefectListBloc`, `DefectManageBloc`, `DefectReportBloc` | `DefectListUseCase`, `DefectManageUseCase` |
| **direction** | Trade / sales direction creation | (embedded in location flows) | `CreateDirectionBloc` | (location-based) |
| **equipment** | Equipment list / manage / report (POS equipment at clients) | `EquipmentListRoute`, `EquipmentManageRoute`, `EquipmentReportManageRoute` | `EquipmentListBloc`, `EquipmentManageBloc`, `EquipmentReportManageBloc` | `EquipmentUseCase` |
| **kpi** | Monthly KPI dashboard with filtering | `KpiRoute` | `KpiBloc` | `KpiUseCase` |
| **location** | Manual location selection, fake location for testing, endpoint locations | `SelectedManualLocationsRoute`, `FakeLocationRoute` | `SelectedManualLocationsBloc`, `SelectedLocationBloc`, `FakeLocationBloc`, `EndPointLocationsBloc` | (core geolocation) |
| **log** | In-app viewer for the file-based network logs | `LogFilesRoute` | (state-based) | — |
| **login** | User authentication | `LoginRoute` | `LoginBloc` | `AuthUseCase` |
| **main** ★ | 4-tab shell + tab pages (home, daily-clients, oddments, more-menu) | `MainRoute` *(children: Home/DailyClients/Oddments/MoreMenu)* | `MainBloc`, `HomeBloc`, `DailyClientsBloc`, `OddmentsBloc`, `MoreMenuBloc` | `HomeUseCase`, `MainUseCase`, etc. |
| **oddments** | Agent's own container/stock dashboard (top-level, separate from client/oddment) | `OddmentsRoute` *(tab child of MainRoute)* | `OddmentsBloc`, `OddmentsFilterBloc` | `OddmentsUseCase` |
| **order** ★ | Order management — create, edit, draft, history, overview, photo, pre-order, bonuses, discounts, scanner | `OrderManageRoute`, `OrderOverviewRoute`, `OrderDetailRoute`, `PreOrderRoute`, `OrderHistoryListRoute`, `OrderHistoryDetailRoute`, `ProductPhotoManageRoute`, `ProductScannerRoute`, `DraftRoute` | `OrderManageBloc`, `OrderOverviewBloc`, `OrderDetailBloc`, `PreOrderBloc`, `OrderHistoryListBloc`, `OrderHistoryDetailBloc`, `ProductPhotoManageBloc`, `DraftBloc`, `OrderBonusBloc`, `OrderDiscountBloc`, `ProductScannerBloc` | `OrderManageUseCase`, `OrderOverviewUseCase`, `OrderDetailUseCase`, … |
| **payment** | Payment entry and management | `PaymentManageRoute` | `PaymentManageBloc` | `PaymentManageUseCase` |
| **pending** | Pending documents / approvals | `PendingDocsRoute` | `PendingDocsBloc` | `PendingDocsUseCase` |
| **qrcode** | QR-code scanner for product/order/client lookup | `QrCodeRoute` | `QrCodeBloc` | `QrCodeUseCase` |
| **refund** | Refund + refund-based-order management, overview, detail | `RefundManageRoute`, `RefundOverviewRoute`, `RefundDetailRoute`, `RefundBasedOrderListRoute`, `RefundBasedOrderDetailRoute`, `RefundBasedOrderOverviewRoute` | `RefundManageBloc`, `RefundOverviewBloc`, `RefundDetailBloc`, `RefundBasedOrderBloc`, `RefundBasedOrderDetailBloc`, `RefundBasedOrderOverviewBloc` | `RefundManageUseCase`, `RefundBasedOrderUseCase` |
| **replace** | Replacement/exchange management, overview, detail + reverted-products | `ReplaceManageRoute`, `ReplaceOverviewRoute`, `ReplaceDetailRoute`, `RevertedManageRoute` | `ReplaceManageBloc`, `ReplaceOverviewBloc`, `ReplaceDetailBloc`, `RevertedManageBloc` | `ReplaceManageUseCase` |
| **report** | Sales / replace / payment / defect reports | `ReportsRoute`, `SalesReportRoute`, `ReplaceReportRoute`, `PaymentReportRoute`, `DefectReportRoute` | `SalesReportBloc`, `ReplaceReportBloc`, `PaymentReportBloc`, `DefectReportBloc` | `SalesReportUseCase`, `ReplaceReportUseCase`, … |
| **revise** | Order revision report (start/finish-of-day reconciliation) | `ReviseReportRoute`, `ReviseOrderReportRoute` | `ReviseReportBloc`, `ReviseOrderReportBloc` | `ReviseReportUseCase` (the only `registerLazySingleton` use case) |
| **settings** | User and administration settings | `SettingsRoute` | `SettingsBloc`, `AdministrationSettingBloc` | `SettingsUseCase` |
| **support** | Contact / support page | `SupportRoute` | — | — |
| **synchronize** ★ | Full app data sync with progress UI | `SynchronizeRoute` | `SynchronizeBloc` (plus `HomeSynchronizeBloc`, `OrderSynchronizeBloc`, `PhotoSynchronizeBloc` for sub-flows) | `SynchronizeUseCase` |
| **tara** | Remaining-tara (container) management | `RemainingTaraRoute` | `RemainingTaraBloc` | `TaraUseCase` |
| **task** | Task dashboard + control + list | `TaskDashboardRoute` | `TaskDashboardBloc`, `TaskControlBloc` | `TaskListUseCase` |
| **user** | User picker for multi-account devices | `UserListRoute` | `UserListBloc` | `UserUseCase` |
| **vsorder** | Van-sell order pipeline (parallel to the regular order flow): list, manage, refund, pre-order, detail | `VanSellOrderListRoute`, `VanSellOrderDetailRoute`, `VanSellOrderManageRoute`, `VanSellPreOrderRoute`, `VanSellRefundManageRoute`, `VanSellPreRefundRoute` | `VanSellOrderListBloc`, `VanSellOrderDetailBloc`, `VanSellOrderManageBloc`, `VanSellPreOrderBloc`, `VanSellRefundManageBloc`, `VanSellPreRefundBloc` | `VanSellOrderUseCase`, `VanSellRefundUseCase` |
| **weblink** | Webview / external-link landing | — | — | — |

★ = has a dedicated deep-dive doc in [12-feature-deep-dives/](./12-feature-deep-dives/main-shell.md).

## Deep-dives

For five representative features, see the deep-dives folder:

- [synchronize](./12-feature-deep-dives/sync.md) — the SynchronizeBloc/Page pair, the 44-step chain, status enum, retry, end-of-sync update dialog.
- [order/manage](./12-feature-deep-dives/order-manage.md) — `OrderManagePage` + `OrderManageBloc` event surface, FutureHandler usage, sub-flow links (bonus, discount, photo).
- [client/list](./12-feature-deep-dives/client-list.md) — 5 page-level StreamSubscriptions, 6 BLoC-level subscriptions, the technical-debt annotation from CLAUDE.md, `ClientListInitialEvent` constructor shape.
- [main shell + home](./12-feature-deep-dives/main-shell.md) — `MainPage` 4-tab navigation, `HomeBloc`'s 14 events, sync dialog UX, dual GPS service.
- [client/oddment](./12-feature-deep-dives/client-oddment.md) — newer end-to-end feature added in DB v13, full stack walk-through.

## Where to look for the rest

For any feature without a deep-dive:

1. Open `lib/presentation/features/<feature>/` and read the page and BLoC together.
2. Find the use case under `lib/domain/usecase/<feature>/`.
3. Find the routes by `grep <Feature>Route lib/core/router/app_router.dart`.
4. Find related entities by looking at the use case's imports and following them into `lib/data/repository_impls/<feature>/`.

The patterns are uniform across features — once you've read one BLoC + page + use case set per CLAUDE.md, the rest read the same way.
