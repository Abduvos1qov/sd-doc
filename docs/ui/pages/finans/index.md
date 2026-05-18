---
title: "Finans — UI page reference"
audience: All sd-main developers, QA
summary: Landing page for the sd-main finans module UI pages
topics: [finans, page, ui, index]
---

# Finans — UI page reference

This section catalogues the live admin UI pages rendered by the `finans` module in `sd-main`. Each entry below maps a route to its controller action, view file and required RBAC permission. Pages were extracted by reading the view templates in `protected/modules/finans/views/` and the matching controller actions.

## Pages

| Page | Route | Controller :: action | Permission |
|---|---|---|---|
| [Расходы](./finans_index) | `/finans/consumption` | `ConsumptionController::index` | `operation.finans.consumption` |
| [Приходы](./finans_credit) | `/finans/consumption/credit` | `ConsumptionController::credit` | `operation.finans.credit` |
| [Статьи и фонды](./finans_category) | `/finans/consumption/category` | `ConsumptionController::category` | `operation.finans.consumptionCategory` |
| [Движения денежных средств](./finans_report) | `/finans/consumption/report` | `ConsumptionController::report` | `operation.finans.consumptionReport` |
| [Движения денежных средств — pivot](./finans_pivot) | `/finans/consumption/pivot` | `ConsumptionController::pivot` | `operation.finans.consumption` |
| [История расходов](./finans_history) | `/finans/consumption/history` | `ConsumptionController::history` | `operation.finans.consumption` |
| [Перемещение между кассами](./finans_cashboxDisplacement_index) | `/finans/cashboxDisplacement` | `CashboxDisplacementController::index` | `operation.finans.cashboxdisplacement` |
| [История перемещений](./finans_cashboxDisplacement_view) | `/finans/cashboxDisplacement/view` | `CashboxDisplacementController::index` (renders `view`) | `operation.finans.cashboxdisplacement` |
| [Перевод между филиалами](./finans_paymentTransfer_index) | `/finans/paymentTransfer` | `PaymentTransferController::index` | via `User::checkAccess` |
| [P&L](./finans_pnl_index) | `/finans/pnl` | `PnlController::index` | `operation.finans.pnl` |
| [P&L по агентам](./finans_agentPnl_index) | `/finans/agentPnl` | `AgentPnlController::index` | via `User::checkAccess` |
| [P&L по товарам](./finans_pivotPnl_byproduct) | `/finans/pivotPnl/byproduct` | `PivotPnlController::loadByProduct` | via `User::checkAccess` |

## See also

- Module reference: [/modules/finans](/docs/modules/finans)
- QA workflows: [/quality/finans/finans-qa](/docs/quality/finans/finans-qa)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
- Cross-module flow: [order → finans → payment → stock](/docs/concepts/order-to-cash)
