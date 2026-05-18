---
sidebar_position: 8
title: Operations catalog
audience: [security engineers, devops, support]
summary: Alphabetical reference of every operation.* string passed to H::access or Yii::app()->user->checkAccess in sd-main, with the controller/action it gates, the canonical call site, and the default roles granted.
topics: [rbac, operations, permissions, access-control, sd-main]
---

# Operations catalog (sd-main)

This page lists every `operation.*` permission string that sd-main
checks at runtime. The data was extracted by grepping
`H::access('operation.*')` and `Yii::app()->user->checkAccess(...)`
across `protected/modules/`, `protected/models/`, and
`protected/components/`.

Use it as a lookup when you encounter a 403 with a message like
"operation.orders.update (H::access)" and need to know:

- What controller/action threw the 403.
- Which method the check enforces (every `H::access(...)` call in
  sd-main is single-arg, so there is no SHOW/CREATE/UPDATE split —
  the **action name** itself encodes the method).
- Which default roles hold the permission (consult the
  [RBAC matrix](./rbac-matrix.md) for the authoritative role table).
- The canonical file:line to read for the gate.

## How the catalog is built

sd-main does not use the multi-arg `Access::check($operation,
Access::SHOW | Access::CREATE | Access::UPDATE | Access::DELETE)`
pattern that newer SalesDoctor services use. Instead, every operation
is its own atomic boolean: `operation.orders.create` is one row in
`authitem` distinct from `operation.orders.update`.

There is exactly one gate helper: `H::access($operation,
$isAjax = false)` in `protected/components/H.php`. Internally it
runs:

1. If guest → redirect to `/site/login`.
2. If `User.ROLE in H::$allowRoles = [3, 1]` → return true.
3. Call `Yii::app()->user->checkAccess($operation)`. If false, OR if
   `User.ROLE in H::$denyRoles = [11, 10, 4]` → throw 403 (or
   return false when `$isAjax = true`).
4. Otherwise return true.

So the "method" column in the table below is **derived from the
operation suffix**, not from a flag passed to the call. The
conventional suffixes are:

| Suffix | Method |
|--------|--------|
| `.list` / `.index` | SHOW (list) |
| `.view` / `.detail` / `.report` | SHOW (single) |
| `.create` / `.add*` | CREATE |
| `.update` / `.edit*` / `.bind` / `.setActive` | UPDATE |
| `.delete` / `.cancel` | DELETE |
| `.deny*` | NEGATIVE FLAG (granting blocks editing) |
| `.print` / `.export` | EXPORT |

Where a single operation gates multiple methods on the same screen
(e.g. `operation.finans.cashboxdisplacement` gates both the index
view and the cancel button), the table notes "SHOW + UPDATE".

## Catalog

### agents.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.agents.list` | `staff/agent/index` | SHOW | 1, 2, 3, 5, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.create` | `staff/agent/create` | CREATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.update` | `staff/agent/update` | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.delete` | `staff/agent/delete` | DELETE | 1, 2, 3 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.limit` | per-agent quantity limit edit | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.paket` | assign sales package to agent | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.reception` | reception screen access | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.reestablish` | restore a soft-deleted agent | UPDATE | 1, 2, 3 | `modules/staff/controllers/AgentController.php` |
| `operation.agents.visit.ordering` | reorder agent route stops | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/AgentController.php` |

### adt.\* / adtAudit.\* / adtPoll.\* / adtReports.\* / adtMixReport.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.adt.visit-report` | merchandising visit report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/VisitController.php` |
| `operation.adtAudit.list` | audit list view | SHOW | 1, 2, 3, 5, 8 | `modules/adt/controllers/AuditController.php` |
| `operation.adtAudit.create` | new audit | CREATE | 1, 2, 3, 8 | `modules/adt/controllers/AuditController.php` |
| `operation.adtAudit.update` | edit audit | UPDATE | 1, 2, 3, 8 | `modules/adt/controllers/AuditController.php` |
| `operation.adtAudit.changeVisitDetail` | post-hoc edit of visit fields | UPDATE | 1, 2, 3, 8 | `modules/adt/controllers/AuditController.php` |
| `operation.adtPoll.list` | poll list | SHOW | 1, 2, 3, 5, 8 | `modules/adt/controllers/PollController.php` |
| `operation.adtPoll.create` | new poll | CREATE | 1, 2, 3, 8 | `modules/adt/controllers/PollController.php` |
| `operation.adtPoll.update` | edit poll | UPDATE | 1, 2, 3, 8 | `modules/adt/controllers/PollController.php` |
| `operation.adtMixReport.index` | mix report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/MixReportController.php` |
| `operation.adtReports.available` | available-products report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.base` | base store-check report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.daily` | daily merchandising report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.monthly` | monthly merchandising report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.price` | price-shelf report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.retail` | retail-share report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |
| `operation.adtReports.storeCheck` | full store-check breakdown | SHOW | 1, 2, 3, 5, 8, 9 | `modules/adt/controllers/ReportsController.php` |

### audit.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.audit.all` | audit log viewer | SHOW | 1, 2, 3, 5, 8, 9 | `modules/audit/controllers/DefaultController.php` |

### billing.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.billing.index` | tenant billing dashboard | SHOW | 1, 3 only | `modules/billing/controllers/DefaultController.php` |
| `operation.billing.distr` | distribution report | SHOW | 1, 3 only | `modules/billing/controllers/DistrController.php` |
| `operation.billing.sms` | SMS-cost report | SHOW | 1, 3 only | `modules/billing/controllers/SmsController.php` |

Even role 2 (filial admin) cannot see billing — these are reserved
for `H::$allowRoles` (1 and 3) so that filial admins cannot see the
tenant's bill.

### clients.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.clients.list` | client list grid | SHOW | 1, 2, 3, 5, 6, 7, 8, 9 | `modules/clients/controllers/ClientController.php:156` |
| `operation.clients.view` | single-client view | SHOW | 1, 2, 3, 5, 6, 7, 8, 9 | `modules/clients/controllers/ClientController.php` |
| `operation.clients.create` | add new client | CREATE | 1, 2, 3, 5 | `modules/clients/controllers/AddClientController.php` |
| `operation.clients.update` | edit client | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/ViewController.php:9` |
| `operation.clients.duplicate` | clone client | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/ClientController.php` |
| `operation.clients.setActive` | toggle ACTIVE flag | UPDATE | 1, 2, 3, 5, 8 | `modules/clients/controllers/ClientController.php` |
| `operation.clients.banMakingClientActive` | block making client active | NEGATIVE | 1, 2, 3 | `modules/clients/controllers/ClientController.php` |
| `operation.clients.banMakingClientInactive` | block making client inactive | NEGATIVE | 1, 2, 3 | `modules/clients/controllers/ClientController.php` |
| `operation.clients.shipper` | shipper screen | SHOW | 1, 2, 3, 5 | `modules/clients/controllers/ShipperFinansController.php` |
| `operation.clients.shipperFinans` | shipper finans tab | SHOW | 1, 2, 3, 5, 6 | `modules/clients/controllers/ShipperFinansController.php:50` |
| `operation.clients.shipperFinans.initialBalans` | initial balance for shipper | CREATE | 1, 2, 3, 5 | `modules/clients/controllers/ShipperFinansController.php:573` |
| `operation.clients.shipperFinans.revise` | shipper reconciliation | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/ShipperFinansController.php:270` |
| `operation.clients.shipperFinans.report` | shipper report | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/ShipperFinansController.php:361` |
| `operation.clients.expeditorDolg` | expeditor debt | SHOW | 1, 2, 3, 5, 6 | `modules/clients/controllers/ComputationController.php` |
| `operation.clients.finans` | client finans card | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/FinansController.php` |
| `operation.clients.finansCreate` | create finans transaction | CREATE | 1, 2, 3, 5, 6 | `modules/clients/controllers/ComputationController.php:1440` |
| `operation.clients.finansDelete` | delete finans transaction | DELETE | 1, 2, 3 | `modules/clients/controllers/ComputationController.php` |
| `operation.clients.finansInitialBalans` | initial balance | CREATE | 1, 2, 3, 5 | `modules/clients/controllers/ComputationController.php` |
| `operation.clients.finansCreateInitialBalans` | create initial balance row | CREATE | 1, 2, 3, 5 | `modules/clients/controllers/ShipperFinansController.php:585` |
| `operation.clients.finansReport` | finans report | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/FinansController.php` |
| `operation.clients.finansRevise` | client reconciliation | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/ReviseController.php` |
| `operation.clients.transactions` | transactions list | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/TransactionsController.php` |
| `operation.clients.transactionsView` | view single transaction | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/ComputationController.php:48` |
| `operation.clients.transactionsUpdate` | edit transaction | UPDATE | 1, 2, 3, 6 | `modules/clients/controllers/ShipperFinansController.php:463` |
| `operation.clients.transactionWriteoff` | write off bad debt | UPDATE | 1, 2, 3 | `modules/clients/controllers/TransactionController.php` |
| `operation.clients.transactionsConversion` | currency conversion | UPDATE | 1, 2, 3 | `modules/clients/controllers/TransactionController.php` |
| `operation.clients.transactionPivot` | transactions pivot | SHOW | 1, 2, 3, 5, 6, 9 | `modules/clients/controllers/TransactionsController.php` |
| `operation.clients.paymentApproval` | approve pending payments | UPDATE | 1, 2, 3, 6 | `modules/clients/controllers/PaymentApprovalController.php` |
| `operation.clients.approval` | mass approval screen | UPDATE | 1, 2, 3, 5, 8 | `modules/clients/controllers/ApprovalController.php` |
| `operation.clients.approval.view` | approval log view | SHOW | 1, 2, 3, 5, 8 | `modules/clients/controllers/ApprovalController.php` |
| `operation.clients.approval.delete` | delete approval entry | DELETE | 1, 2, 3 | `modules/clients/controllers/ApprovalController.php` |
| `operation.clients.allowBind` | bind allow-list to client | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/BindController.php` |
| `operation.clients.priceTypeBind` | bind price type | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/BindController.php` |
| `operation.clients.rlpBind` | bind RLP package | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/BindController.php` |
| `operation.clients.bonusBind` | bind bonus program | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/BindController.php` |
| `operation.clients.configBind` | bind per-client config flags | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/BindController.php` |
| `operation.clients.map` | client map | SHOW | 1, 2, 3, 5, 8, 9 | `modules/clients/controllers/MapController.php` |
| `operation.clients.kassaIncome` | record cashbox income from client | CREATE | 1, 2, 3, 6 | `modules/clients/controllers/ComputationController.php` |
| `operation.clients.agentVisits` | visits tab on client card | SHOW | 1, 2, 3, 5, 8, 9 | `modules/clients/controllers/ViewController.php:15` |
| `operation.clients.generateQR` | generate client QR | SHOW | 1, 2, 3, 5 | `modules/clients/controllers/ClientController.php` |

### dashboard.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.dashboard.finans` | finans dashboard | SHOW | 1, 2, 3, 5, 9 | `modules/dashboard/controllers/FinansController.php` |
| `operation.dashboard.sales` | sales dashboard | SHOW | 1, 2, 3, 5, 9 | `modules/dashboard/controllers/SalesController.php` |
| `operation.dashboard.supervayzer` | supervisor dashboard | SHOW | 1, 2, 3, 8 | `modules/dashboard/controllers/SupervayzerController.php:66` |

### doctor.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.doctor.akb` | AKB analytics | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/AkbController.php` |
| `operation.doctor.akbPlan` | edit AKB plan | UPDATE | 1, 2, 3, 8 | `modules/doctor/controllers/AkbController.php` |
| `operation.doctor.outlet` | outlet analytics | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/OutletController.php` |
| `operation.doctor.outletPlan` | edit outlet plan | UPDATE | 1, 2, 3, 8 | `modules/doctor/controllers/OutletController.php` |
| `operation.doctor.personal` | personal score | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/PersonalController.php` |
| `operation.doctor.sku` | SKU analytics | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/SkuController.php` |
| `operation.doctor.skuPlan` | edit SKU plan | UPDATE | 1, 2, 3, 8 | `modules/doctor/controllers/SkuController.php` |
| `operation.doctor.strikePlan` | strike plan | UPDATE | 1, 2, 3, 8 | `modules/doctor/controllers/StrikeController.php` |
| `operation.doctor.strikeRate` | strike rate analytics | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/StrikeController.php` |
| `operation.doctor.total` | total analytics | SHOW | 1, 2, 3, 5, 8, 9 | `modules/doctor/controllers/TotalController.php` |
| `operation.doctor.volumePlan` | volume plan editor | UPDATE | 1, 2, 3, 8 | `modules/doctor/controllers/VolumeController.php` |

### expeditor.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.expeditor.list` | expeditor list | SHOW | 1, 2, 3, 5, 8, 9 | `modules/staff/controllers/ExpeditorController.php` |
| `operation.expeditor.create` | add expeditor | CREATE | 1, 2, 3, 5 | `modules/staff/controllers/ExpeditorController.php` |
| `operation.expeditor.update` | edit expeditor | UPDATE | 1, 2, 3, 5 | `modules/staff/controllers/ExpeditorController.php` |

### filial.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.filial.movement.request.list` | filial-to-filial movement requests | SHOW | 1, 2, 3, 5, 9 | `modules/filial/controllers/MovementController.php` |
| `operation.filial.movement.request.create` | new request | CREATE | 1, 2, 3, 5 | `modules/filial/controllers/MovementController.php` |
| `operation.filial.movement.request.edit` | edit request | UPDATE | 1, 2, 3, 5 | `modules/filial/controllers/MovementController.php` |
| `operation.filial.movement.request.view` | view request detail | SHOW | 1, 2, 3, 5, 9 | `modules/filial/controllers/MovementController.php` |

### finans.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.finans.cashbox` | cashbox grid | SHOW | 1, 2, 3, 5, 6, 9 | `modules/finans/controllers/CashboxController.php` |
| `operation.finans.cashboxBalans` | cashbox balance report | SHOW | 1, 2, 3, 6 | `modules/finans/controllers/CashboxController.php` |
| `operation.finans.cashboxUpdate` | edit a cashbox row | UPDATE | 1, 2, 3, 6 | `modules/finans/controllers/CashboxController.php` |
| `operation.finans.cashboxdisplacement` | cashbox displacement list | SHOW | 1, 2, 3, 6 | `modules/finans/controllers/CashboxDisplacementController.php:22` |
| `operation.finans.cashboxdisplacementAdd` | new displacement | CREATE | 1, 2, 3, 6 | `modules/finans/controllers/CashboxDisplacementController.php:139` |
| `operation.finans.cashboxdisplacementCancel` | cancel displacement | DELETE | 1, 2, 3, 6 | `modules/finans/controllers/CashboxDisplacementController.php:109` |
| `operation.finans.consumption` | consumption list | SHOW | 1, 2, 3, 5, 6 | `modules/finans/controllers/ConsumptionController.php:39` |
| `operation.finans.addconsumption` | new consumption | CREATE | 1, 2, 3, 6 | `modules/finans/controllers/ConsumptionController.php:100` |
| `operation.finans.editconsumption` | edit consumption | UPDATE | 1, 2, 3, 6 | `modules/finans/controllers/ConsumptionController.php:82` |
| `operation.finans.deleteconsumption` | delete consumption | DELETE | 1, 2, 3 | `modules/finans/controllers/ConsumptionController.php:46` |
| `operation.finans.consumptionCategory` | manage consumption categories | SHOW + CRUD | 1, 2, 3 | `modules/finans/controllers/ConsumptionController.php:272` |
| `operation.finans.consumptionReport` | consumption report | SHOW | 1, 2, 3, 5, 6, 9 | `modules/finans/controllers/ConsumptionController.php:346` |
| `operation.finans.credit` | credit screen | SHOW | 1, 2, 3, 5, 6 | `modules/finans/controllers/ConsumptionController.php:175` |
| `operation.finans.editcredit` | edit credit row | UPDATE | 1, 2, 3, 6 | `modules/finans/views/consumption/credit.php:7` |
| `operation.finans.deletecredit` | delete credit row | DELETE | 1, 2, 3 | `modules/finans/controllers/ConsumptionController.php` |
| `operation.finans.addDebt` | record customer debt | CREATE | 1, 2, 3, 6 | `modules/finans/controllers/DebtController.php` |
| `operation.finans.paymentDisplacement` | move payment between cashboxes | CREATE | 1, 2, 3, 6 | `modules/finans/controllers/PaymentController.php` |
| `operation.finans.pnl` | profit-and-loss report | SHOW | 1, 2, 3, 9 | `modules/finans/controllers/PnlController.php:35` |

### idokon.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.idokon.incoming.request` | iDokon incoming-request inbox | SHOW | 1, 2, 3, 5 | `modules/idokon/controllers/IncomingController.php` |

### inventory.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.inventory.list` | inventarization list | SHOW | 1, 2, 3, 5, 9 | `modules/clients/controllers/InventorizationController.php` |
| `operation.inventory.create` | new inventarization | CREATE | 1, 2, 3, 5 | `modules/clients/controllers/InventorizationController.php` |
| `operation.inventory.update` | edit inventarization | UPDATE | 1, 2, 3, 5 | `modules/clients/controllers/InventorizationController.php` |
| `operation.inventory.history` | history view | SHOW | 1, 2, 3, 5, 9 | `modules/clients/controllers/InventorizationController.php` |
| `operation.inventory.out` | check-out inventory | UPDATE | 1, 2, 3 | `modules/clients/controllers/InventorizationController.php` |

### kpi.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.kpi.list` | KPI list | SHOW | 1, 2, 3, 5, 8, 9 | `modules/kpi/controllers/KpiController.php` |
| `operation.kpi.view` | KPI detail | SHOW | 1, 2, 3, 5, 8, 9 | `modules/kpi/controllers/KpiController.php` |
| `operation.kpi.create` | new KPI | CREATE | 1, 2, 3 | `modules/kpi/controllers/KpiController.php` |
| `operation.kpi.update` | edit KPI | UPDATE | 1, 2, 3 | `modules/kpi/controllers/KpiController.php` |
| `operation.kpi.result` | KPI result viewer | SHOW | 1, 2, 3, 5, 8, 9 | `modules/kpi/controllers/KpiController.php` |

### marking.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.marking.incoming` | mark-tracking incoming | SHOW | 1, 2, 3, 5 | `modules/marking/controllers/IncomingController.php` |
| `operation.marking.outgoing` | mark-tracking outgoing | SHOW | 1, 2, 3, 5 | `modules/marking/controllers/OutgoingController.php` |

### notification.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.notification.list` | notification inbox | SHOW | 1, 2, 3, 5, 6, 7, 8, 9 | `modules/notification/controllers/DefaultController.php` |

### orders.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.orders.list` | order list grid | SHOW | 1, 2, 3, 5, 6, 8, 9 | `modules/orders/controllers/OrdersController.php` |
| `operation.orders.view` | view single order | SHOW | 1, 2, 3, 5, 6, 8, 9 | `modules/orders/controllers/ViewController.php:21` |
| `operation.orders.create` | new order | CREATE | 1, 2, 3, 5 | `modules/orders/controllers/CreateOrderController.php:327` |
| `operation.orders.update` | edit order | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/AddOrderController.php:52` |
| `operation.orders.edit` | order quick-edit | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/EditOrderController.php` |
| `operation.orders.print` | print PDFs/invoices | EXPORT | 1, 2, 3, 5, 6, 8, 9 | `modules/orders/controllers/OrdersController.php:240` |
| `operation.orders.import` | import orders from XLSX/1C | CREATE | 1, 2, 3 | `modules/orders/controllers/ImportOrderController.php:60` |
| `operation.orders.importDefect` | import defects | CREATE | 1, 2, 3 | `modules/orders/controllers/ImportOrderController.php:66` |
| `operation.orders.expeditor` | assign expeditor to order | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/OrdersController.php` |
| `operation.orders.tara` | tara (packaging) lines | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/TaraController.php` |
| `operation.orders.rejects` | mark order lines rejected | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/RejectController.php` |
| `operation.orders.status` | change order status | UPDATE | 1, 2, 3, 5 | `modules/orders/controllers/OrderStateController.php` |
| `operation.orders.onMap` | order on map view | SHOW | 1, 2, 3, 5, 8, 9 | `modules/orders/controllers/ViewController.php:28` |
| `operation.orders.createRecovery` | recovery (return) order — create | CREATE | 1, 2, 3 | `modules/orders/controllers/RecoveryController.php` |
| `operation.orders.updateRecovery` | edit recovery order | UPDATE | 1, 2, 3 | `modules/orders/controllers/RecoveryController.php` |
| `operation.orders.createReplace` | replacement order | CREATE | 1, 2, 3 | `modules/orders/controllers/ReplaceController.php` |
| `operation.orders.supplier.receipt` | supplier-receipt order | CREATE | 1, 2, 3 | `modules/orders/controllers/SupplierController.php` |
| `operation.orders.denyEditAgent` | block reassigning agent | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditOnSent` | block edit after status SENT | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditOnDeliver` | block edit after status DELIVERED | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditOnCancelOrReturn` | block edit after CANCEL/RETURN | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditPriceType` | block changing price type | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditQuantity` | block editing line quantity | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyEditWarehouse` | block changing warehouse | NEGATIVE | all granted by default | `modules/orders/controllers/AddOrderController.php` |
| `operation.orders.denyFastEditing` | block fast-edit modal | NEGATIVE | all granted by default | `modules/orders/controllers/OrdersController.php` |
| `operation.orders.denyFullyUpateRecovery` | block full recovery edit | NEGATIVE | all granted by default | `modules/orders/controllers/RecoveryController.php` |
| `operation.orders.denyPartialReturn` | block partial return | NEGATIVE | all granted by default | `modules/orders/controllers/ReturnController.php` |

### other.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.other.gps` | live GPS map for staff | SHOW | 1, 2, 3, 8, 9 | `modules/other/controllers/GpsController.php` |

### planning.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.planning.byproduct` | by-product planning view | SHOW | 1, 2, 3, 8 | `modules/stock/controllers/PlanProductController.php:43` |
| `operation.planning.byproductCreate` | create by-product plan | CREATE | 1, 2, 3, 8 | `modules/stock/controllers/PlanProductController.php` |
| `operation.planning.outlet` | outlet plan | SHOW | 1, 2, 3, 8 | `modules/stock/controllers/PlanOutletController.php` |
| `operation.planning.results` | plan results | SHOW | 1, 2, 3, 5, 8, 9 | `modules/stock/controllers/PlanController.php` |
| `operation.planning.setup` | plan setup | UPDATE | 1, 2, 3 | `modules/stock/controllers/PlanController.php` |

### rbac.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.rbac.users` | RBAC user assignments | SHOW + CRUD | 1, 3 only | `modules/access/controllers/BackendController.php` |
| `operation.rbac.roles` | RBAC role management | SHOW + CRUD | 1, 3 only | `modules/access/controllers/BackendController.php` |
| `operation.rbac.tasks` | RBAC tasks | SHOW + CRUD | 1, 3 only | `modules/access/controllers/BackendController.php` |
| `operation.rbac.operations` | RBAC operations management | SHOW + CRUD | 1, 3 only | `modules/access/controllers/BackendController.php` |

### reports.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.reports.agent` | per-agent report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/AgentController.php` |
| `operation.reports.agentVisits` | agent-visits report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/AgentVisitsController.php` |
| `operation.reports.analyze` | analytics export | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/AnalyzeController.php` |
| `operation.reports.bonusReport` | bonus report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/BonusController.php` |
| `operation.reports.bonusReportDetail` | bonus report detail | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/BonusController.php` |
| `operation.reports.bonusAccumulation` | bonus accumulation | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/BonusController.php` |
| `operation.reports.classification` | client classification | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ClassificationController.php` |
| `operation.reports.classificationRFM` | RFM classification | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ClassificationController.php` |
| `operation.reports.customer` | customer report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/CustomerController.php` |
| `operation.reports.customerDetail` | customer report detail | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/CustomerController.php` |
| `operation.reports.discountDetail` | discount detail | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/DiscountController.php` |
| `operation.reports.expeditor` | expeditor report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ExpeditorController.php` |
| `operation.reports.expeditorDebt` | expeditor debt | SHOW | 1, 2, 3, 5, 6, 9 | `modules/reports/controllers/ExpeditorController.php` |
| `operation.reports.expeditorDefect` | expeditor defect | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ExpeditorController.php` |
| `operation.reports.expeditorReport` | full expeditor report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ExpeditorController.php` |
| `operation.reports.export` | export-everything button | EXPORT | 1, 2, 3, 5, 9 | `modules/reports/controllers/ExportController.php` |
| `operation.reports.inventorization` | inventarization report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/InventorizationController.php` |
| `operation.reports.markupReport` | markup report | SHOW | 1, 2, 3, 9 | `modules/reports/controllers/MarkupController.php` |
| `operation.reports.minimum` | minimum-stock report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/MinimumController.php` |
| `operation.reports.photoReport` | photo report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/PhotoController.php` |
| `operation.reports.planExpeditor` | expeditor plan | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/PlanController.php` |
| `operation.reports.price` | price report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/PriceController.php` |
| `operation.reports.report` | generic report runner | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/ReportController.php` |
| `operation.reports.reportBuilder` | report builder UI | SHOW | 1, 2, 3, 9 | `modules/reports/controllers/ReportBuilderController.php` |
| `operation.reports.reportVisit` | visit report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/VisitController.php` |
| `operation.reports.rlpReport` | RLP report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/RlpController.php` |
| `operation.reports.tara` | tara report | SHOW | 1, 2, 3, 5, 9 | `modules/clients/controllers/TaraController.php:49` |
| `operation.reports.telegram` | Telegram subscriber report | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/TelegramController.php` |
| `operation.reports.tg.feedbackReport` | TG feedback | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/TelegramController.php` |
| `operation.reports.volumeReport` | volume report v1 | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/VolumeController.php` |
| `operation.reports.volumeReportV2` | volume report v2 | SHOW | 1, 2, 3, 5, 9 | `modules/reports/controllers/VolumeController.php` |
| `operation.reports.workingTime` | working-time report | SHOW | 1, 2, 3, 5, 8, 9 | `modules/reports/controllers/WorkingTimeController.php` |

### settings.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.settings.user` | user admin | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/UserController.php:610` |
| `operation.settings.product` | product catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/ProductController.php` |
| `operation.settings.productCategory` | category tree | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/CategoryController.php` |
| `operation.settings.productCaseType` | product case types | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/CaseTypeController.php` |
| `operation.settings.price` | price book | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/PriceController.php` |
| `operation.settings.priceType` | price-type catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/PriceTypeController.php` |
| `operation.settings.changePrice` | bulk price change | UPDATE | 1, 2, 3 | `modules/settings/controllers/PriceController.php` |
| `operation.settings.currency` | currency rates | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/CurrencyController.php` |
| `operation.settings.closeDay` | close accounting period | UPDATE | 1, 2, 3 | `modules/settings/controllers/CloseDayController.php` |
| `operation.settings.partners` | partner catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/PartnersController.php` |
| `operation.settings.diler` | dealer catalog | SHOW + CRUD | 1, 3 only | `modules/settings/controllers/DilerController.php` |
| `operation.settings.tradingTeam` | trading team config | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/TradingTeamController.php` |
| `operation.settings.city` | city directory | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/CityController.php` |
| `operation.settings.channel` | sales channels | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/ChannelController.php` |
| `operation.settings.clientCategory` | client categories | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/ClientCategoryController.php` |
| `operation.settings.akbCategory` | AKB categories | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/AkbCategoryController.php` |
| `operation.settings.bonus` | bonus rules | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/BonusController.php` |
| `operation.settings.rlpBonus` | RLP bonus | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/RlpBonusController.php` |
| `operation.settings.loyalty` | loyalty programs | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/LoyaltyController.php` |
| `operation.settings.reject` | reject reasons | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/RejectController.php` |
| `operation.settings.rejectDefect` | defect catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/RejectDefectController.php` |
| `operation.settings.inventoryType` | inventarization types | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/InventoryTypeController.php` |
| `operation.settings.photoReportCategory` | photo-report categories | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/PhotoReportCategoryController.php` |
| `operation.settings.tags` | tag catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/TagsController.php` |
| `operation.settings.tara` | tara catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/TaraController.php` |
| `operation.settings.taskType` | task types | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/TaskTypeController.php` |
| `operation.settings.knowledgeCategory` | knowledge-base categories | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/KnowledgeCategoryController.php` |
| `operation.settings.knowledgePost` | knowledge-base posts | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/KnowledgePostController.php` |
| `operation.settings.unit` | unit-of-measure catalog | SHOW + CRUD | 1, 2, 3 | `modules/settings/controllers/UnitController.php` |
| `operation.settings.smartUp` | SmartUp integration settings | SHOW + CRUD | 1, 3 only | `modules/settings/controllers/SmartUpController.php` |

### smartup5x.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.smartup5x.index` | SmartUp 5.x sync console | SHOW | 1, 2, 3, 5 | `modules/smartup5x/controllers/DefaultController.php` |

### sms.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.sms.list` | outbound SMS list | SHOW | 1, 2, 3, 5, 9 | `modules/sms/controllers/DefaultController.php` |
| `operation.sms.template` | SMS templates | SHOW + CRUD | 1, 2, 3 | `modules/sms/controllers/TemplateController.php` |
| `operation.sms.package.buying` | buy SMS package | UPDATE | 1, 3 only | `modules/sms/controllers/PackageController.php` |

### stock.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.stock.list` | stock grid | SHOW | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/StockController.php` |
| `operation.stock.detail` | warehouse line detail | SHOW | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/StockController.php` |
| `operation.stock.create` | new stock row | CREATE | 1, 2, 3, 20 | `modules/stock/controllers/StockController.php` |
| `operation.stock.update` | edit stock row | UPDATE | 1, 2, 3, 20 | `modules/stock/controllers/StockController.php` |
| `operation.stock.delete` | delete stock row | DELETE | 1, 2, 3 | `modules/stock/controllers/StockController.php` |
| `operation.stock.movement` | warehouse-to-warehouse movement | SHOW + CRUD | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/MovementController.php` |
| `operation.stock.exchange` | exchange between cars | CREATE | 1, 2, 3 | `modules/stock/controllers/ExchangeController.php` |
| `operation.stock.excretion` | car write-off | CREATE | 1, 2, 3 | `modules/stock/controllers/ExcretionController.php` |
| `operation.stock.corrector` | manual stock correction | UPDATE | 1, 2, 3 | `modules/stock/controllers/CorrectorController.php` |
| `operation.stock.dailyRemainder` | daily-remainder report | SHOW | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/DailyController.php` |
| `operation.stock.lotReport` | per-lot report | SHOW | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/LotController.php` |
| `operation.stock.materialReport` | material report | SHOW | 1, 2, 3, 5, 9 | `modules/stock/controllers/MaterialController.php` |
| `operation.stock.profit` | profit by product | SHOW | 1, 2, 3, 9 | `modules/stock/controllers/ProfitController.php` |
| `operation.stock.purchase` | new purchase doc | CREATE | 1, 2, 3, 20 | `modules/stock/controllers/PurchaseController.php` |
| `operation.stock.purchaseUpdate` | edit purchase | UPDATE | 1, 2, 3, 20 | `modules/stock/controllers/PurchaseController.php` |
| `operation.stock.purchaseView` | view purchase | SHOW | 1, 2, 3, 5, 9, 20 | `modules/stock/controllers/PurchaseController.php` |
| `operation.stock.purchaseRefund` | purchase refund | CREATE | 1, 2, 3, 20 | `modules/stock/controllers/PurchaseRefundController.php` |
| `operation.stock.updatePurchaseRefund` | edit purchase refund | UPDATE | 1, 2, 3, 20 | `models/PurchaseRefund.php:111` |
| `operation.stock.purchaseReport` | purchase report | SHOW | 1, 2, 3, 5, 9 | `modules/stock/controllers/PurchaseReportController.php` |
| `operation.stock.purchaseReportProfit` | purchase profit report | SHOW | 1, 2, 3, 9 | `modules/stock/controllers/PurchaseReportController.php` |
| `operation.stock.pivotDetail` | stock pivot detail | SHOW | 1, 2, 3, 5, 9 | `modules/stock/controllers/PivotController.php` |
| `operation.stock.recommend` | recommended order | SHOW | 1, 2, 3, 5, 9 | `modules/stock/controllers/RecommendController.php` |
| `operation.stock.vsExchange` | VS exchange list | SHOW | 1, 2, 3, 5 | `modules/vs/controllers/EditOrderController.php` |
| `operation.stock.vsExchangeAdd` | new VS exchange | CREATE | 1, 2, 3, 5 | `modules/vs/controllers/CreateOrderController.php` |
| `operation.stock.vsExchangeEdit` | edit VS exchange | UPDATE | 1, 2, 3, 5 | `modules/vs/controllers/EditOrderController.php` |
| `operation.stock.vsReturn` | VS return list | SHOW | 1, 2, 3, 5 | `modules/vs/controllers/OrderController.php` |
| `operation.stock.vsReturnAdd` | new VS return | CREATE | 1, 2, 3, 5 | `modules/vs/controllers/CreateOrderController.php` |
| `operation.stock.vsReturnEdit` | edit VS return | UPDATE | 1, 2, 3, 5 | `modules/vs/controllers/EditOrderController.php` |
| `operation.stock.vsReturnView` | view VS return | SHOW | 1, 2, 3, 5 | `modules/vs/controllers/ViewController.php` |

### supervayzer.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.supervayzer.list` | supervisor list | SHOW | 1, 2, 3, 8 | `modules/staff/controllers/SupervayzerController.php` |
| `operation.supervayzer.create` | add supervisor | CREATE | 1, 2, 3, 8 | `modules/staff/controllers/SupervayzerController.php` |
| `operation.supervayzer.update` | edit supervisor | UPDATE | 1, 2, 3, 8 | `modules/staff/controllers/SupervayzerController.php` |
| `operation.supervayzer.delete` | delete supervisor | DELETE | 1, 2, 3 | `modules/staff/controllers/SupervayzerController.php` |

### task.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.task.list` | task list | SHOW | 1, 2, 3, 5, 8, 9 | `modules/task/controllers/TaskController.php` |
| `operation.task.create` | new task | CREATE | 1, 2, 3, 5, 8 | `modules/task/controllers/TaskController.php` |
| `operation.task.update` | edit task | UPDATE | 1, 2, 3, 5, 8 | `modules/task/controllers/TaskController.php` |
| `operation.task.photVote` | photo-vote review | UPDATE | 1, 2, 3, 8 | `modules/task/controllers/PhotoVoteController.php` |

### vs.\*

| Operation | Gates | Method | Default roles | Canonical |
|-----------|-------|--------|---------------|-----------|
| `operation.vs.deny.status.to.lower` | block lowering VS status | NEGATIVE | all granted by default | `modules/vs/controllers/OrderController.php` |
| `operation.vs.downloads` | VS document downloads | EXPORT | 1, 2, 3, 5, 9 | `modules/vs/controllers/ViewController.php` |

## Gotchas

### Operation strings can be partial in error messages

`H::access` truncates the operation string to 16 chars when it
appears in error logs:

```text
H::access('operation.dashb...')
H::access('operation.setti...')
```

When you see a 403 stack trace like that, grep the responsible
controller (the third line of the stack trace) for `H::access(`
and read the operation string directly from the source.

### NEGATIVE flags are inverted

Operations under `operation.orders.denyEdit*` and
`operation.vs.deny.status.to.lower` are **inverted**: granting them
to a role blocks an action. The "default roles" column above lists
who has the deny — meaning who is **restricted**, not who is
permitted.

### Single check call may stand in for multiple methods

Many controllers gate the entire CRUD surface behind a single
operation string. For example,
`operation.finans.consumptionCategory` covers list, add, edit, and
delete — there is no separate `.deleteConsumptionCategory`. The
"Method" column shows "SHOW + CRUD" when this is the case.

### ServerSettings can bypass an operation

A few code paths short-circuit `H::access` based on a
`ServerSettings::*()` flag. Example
(`modules/finans/views/consumption/index.php:159`):

```php
if (ServerSettings::enableDeleteConsumptionOfShipperPayment() ||
    H::access('operation.finans.deleteconsumption', true) ...)
```

When the server setting is on for the tenant, the deletion button
appears for **anyone**, regardless of role. Audit the
`ServerSettings` table when investigating "why can this role do X?"

### Some operations have no canonical check

A handful of legacy operations exist in the `authitem` table but are
never referenced by any `H::access` call in current code. Examples:
`operation.rbac.` (with trailing dot, used as a prefix scan in the
RBAC admin UI). Removing such rows is safe.

### file:line references can drift

The "Canonical" column points at the file and (where available) line
where the operation is checked. The line numbers were extracted from
the sd-main commit at the time of writing; subsequent refactors will
move them. If a line doesn't match, search the file for the operation
string — there will typically be only one occurrence.

### View-layer gates differ from controller-layer gates

The same operation is often checked twice:

1. At the top of the controller action (the primary gate).
2. Inside the view, around a button or menu item, to hide or show it
   in the UI.

Granting the operation makes the button appear AND lets the
controller serve the request. Revoking it hides the button but
**does not block** the controller — unless the controller also
gates it. When debugging "I revoked X but they can still POST to
it", check whether the controller has `H::access(...)` at the top
of the action.

## See also

- [RBAC matrix](./rbac-matrix.md) — roles-times-operations grid.
- [RBAC primer](./rbac.md) — `authitem` table layout and cache
  wiring.
- [Auth and roles](./auth-and-roles.md) — canonical role list.
- [sd-main landmines](./sd-main-landmines.md) — RBAC-adjacent
  footguns.
