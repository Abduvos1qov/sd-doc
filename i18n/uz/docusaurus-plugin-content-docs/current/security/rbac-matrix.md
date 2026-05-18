---
sidebar_position: 7
title: RBAC matrix
audience: [security engineers, devops, support]
summary: Cross-reference table of every numeric role in sd-main against every operation namespace, including filial scope, mobile/web surfaces, and a how-to-test grid.
topics: [rbac, roles, permissions, access-control, sd-main]
---

# RBAC matrix (sd-main)

This page is the canonical roles-times-operations cross-reference for the
sd-main (dealer CRM) codebase. The role list and the inheritance edges
come from `protected/config/auth.php`. The default grant per operation
comes from the seeded `authitem` / `authitemchild` / `authassignment`
rows that ship with the rbac fixture (`H::$bindRoles` short-circuits
specific role IDs to the canonical RBAC item names `role.operator`,
`role.kassir`, `role.svr`, `role.manager`).

If you need to look up a single operation string (e.g.
`operation.orders.update`), use the companion
[operations catalog](./operations-catalog.md). This page answers the
inverse question — "what can role X do?" — and surfaces the global
allow/deny short-circuits inside `H::access`.

## How the layer works

sd-main runs Yii 1.1 with a `DbAuthManager` (see
`protected/components/DbAuthManager.php`) backed by three tables:
`authitem`, `authitemchild`, `authassignment`. Cached per-tenant in
`redis_app` for 600 seconds.

There are three logical layers a request must pass:

1. **Role short-circuits** in `H::access` (`protected/components/H.php`):
   - `H::$allowRoles = [3, 1]` — Super Admin and Diler always pass any
     `H::access(...)` check without touching the database.
   - `H::$denyRoles = [11, 10, 4]` — Merchandiser, Expeditor, Agent are
     unconditionally rejected from any web operation (they live on
     mobile only).
2. **`authassignment` lookup** — for the remaining roles (2, 5, 6, 7,
   8, 9, 20), `Yii::app()->user->checkAccess($operation)` walks the
   `authitemchild` graph from the user's bound role-item upward and
   succeeds if any ancestor is the requested operation.
3. **Filial scope** — even when access is granted, the
   `BaseFilial` query scope restricts the rows returned to the user's
   `FILIAL_ID`. Role 1 (Super Admin) is the only role with implicit
   cross-filial visibility; every other role is effectively
   per-filial.

The `H::$bindRoles` array maps numeric role IDs to canonical
auth-item names so the legacy `User.ROLE` integer column drives the
RBAC seed:

| ROLE | bindRoles name |
|------|----------------|
| 5 | `role.operator` |
| 6 | `role.kassir` |
| 8 | `role.svr` |
| 9 | `role.manager` |

Roles 2 (Administrator Filial) and 7 (Partner) have no `bindRoles`
entry and are managed by hand-built `authassignment` rows.

## Role inventory

| ROLE | English label | Russian label | Inherits from | bindRoles | Filial scope | Web | Mobile (api3) |
|------|---------------|---------------|---------------|-----------|--------------|-----|---------------|
| 1 | Super Administrator | Супер-администратор | 2 | — (allowRoles) | global (all filials) | yes | no |
| 2 | Administrator Filial | Администратор филиала | 3 | — (custom assignment) | per-filial | yes | no |
| 3 | Diler | Дилер | 4 | — (allowRoles) | per-filial | yes | no |
| 4 | Agent | Агент | guest | — (denyRoles) | per-user (own visits/orders) | no | yes |
| 5 | Operator | Оператор | guest | `role.operator` | per-filial | yes | no |
| 6 | Kassir | Кассир | guest | `role.kassir` | per-filial cashbox | yes | no |
| 7 | Partner | Партнёр | guest | — (custom assignment) | per-partner scope | yes (limited) | no |
| 8 | Supervayzer | Супервайзер | guest | `role.svr` | per-team filial | yes | yes (supervisor app) |
| 9 | Manager | Менеджер | guest | `role.manager` | per-filial | yes | no |
| 10 | Expeditor | Экспедитор | guest | — (denyRoles) | per-trip | no | yes |
| 11 | Merchandiser | Мерчендайзер | guest | — (denyRoles) | per-route | no | yes |
| 20 | Stockman | Складчик | guest | — (custom assignment) | per-warehouse | yes (stock only) | yes |
| guest | Guest | Гость | — | — | none | login only | no |

Notes:

- Role 1 inherits role 2 via `children: ['2']`. Role 2 inherits role 3,
  role 3 inherits role 4. So a Super Admin transitively holds every
  permission ever granted to roles 2, 3, 4.
- Even though role 4 (Agent) is a parent of role 3 in `auth.php`, the
  `denyRoles` list in `H::access` overrides the inheritance for any
  user logged in **as** role 4 — they cannot reach the web UI.
- Role 20 (Stockman) is **not** in `auth.php`. It is a `User::ROLE`
  constant defined in `protected/models/User.php` line 35 but operates
  purely through hand-rolled `accessRules()` in stock controllers and
  the `WebUser->ROLE == 20` checks in the warehouse module.

## Granted operations — per-role summary

The detailed cell-by-cell matrix follows below. This section gives the
top-level summary for each role: what they can broadly do.

### 1 — Super Administrator

- `H::$allowRoles` short-circuit: bypasses **every** `H::access(...)`
  check.
- Sees data across all filials (cross-filial queries unmasked).
- Can manage RBAC items and assignments
  (`operation.rbac.users`, `operation.rbac.roles`, etc.).
- Can edit ServerSettings, products, prices, currencies.
- Can close periods (`operation.settings.closeDay`).

### 2 — Administrator Filial

- Has assignments for almost every `operation.*` string except the
  RBAC-management operations (`operation.rbac.users`,
  `operation.rbac.roles`, `operation.rbac.tasks`,
  `operation.rbac.operations`).
- Filtered to one filial by `FilialComponent::getId()`.
- Cannot manage products/prices at the tenant level — only at the
  filial level.
- Can close day for their filial.

### 3 — Diler

- `H::$allowRoles` short-circuit: bypasses every `H::access(...)`
  check.
- Same visibility as Administrator Filial but on the dealer's data
  set.
- In practice the default tenant "admin" user is role 3.

### 4 — Agent

- `H::$denyRoles`: rejected from every web `H::access(...)` check.
- Only path in: api3 mobile endpoints (`LoginController` issues a
  bearer token; the agent app calls `/api3/order`, `/api3/visit`,
  `/api3/client`, etc.).
- Sees only their own visits, orders, route clients (scoped by
  `User.AGENT_ID`).

### 5 — Operator

- Bound to `role.operator`. Default grants:
  `operation.orders.*` (list/view/create/update/print/import),
  `operation.clients.*` (list/view/update/create/transactions/
  finansReport), `operation.stock.list`,
  `operation.reports.*` (most), `operation.task.list`.
- Cannot delete orders or stock entries (no `delete` grant).
- Cannot manage RBAC, products, prices, ServerSettings.

### 6 — Kassir

- Bound to `role.kassir`. Default grants:
  `operation.finans.cashbox`, `operation.finans.cashboxBalans`,
  `operation.finans.cashboxdisplacement`,
  `operation.finans.cashboxdisplacementAdd`,
  `operation.finans.cashboxdisplacementCancel`,
  `operation.finans.cashboxUpdate`,
  `operation.finans.paymentDisplacement`,
  `operation.clients.transactionsView`,
  `operation.clients.shipperFinans`,
  `operation.orders.list` (view-only of orders to apply payment).
- Filial-scoped to one cashbox via `BaseFilial`.
- Cannot create/edit orders or stock.

### 7 — Partner

- Custom `authassignment` rows per tenant. Typical grant: a thin slice
  of `operation.reports.*` and `operation.clients.list` only for
  clients owned by the partner.
- Hand-built `accessRules()` in `ClientController` line 127:
  `array('allow', 'actions' => ['index', 'jasonData', 'ExportXls',
  'SmartExportXls'], 'roles' => ['7'])`.

### 8 — Supervayzer

- Bound to `role.svr`. Default grants:
  `operation.supervayzer.*` (create/list/update/delete subordinate
  agents), `operation.dashboard.supervayzer`,
  `operation.kpi.*` (read), `operation.adtAudit.*`,
  `operation.reports.agent`, `operation.reports.agentVisits`,
  `operation.adt.visit-report`.
- Sees only agents on their team
  (`User.SVR_ID = currentSupervisor.USER_ID`).
- Has a dedicated supervisor mobile app
  (api3 `Sv` controllers).

### 9 — Manager

- Bound to `role.manager`. Default grants:
  `operation.clients.list`, `operation.clients.view`,
  `operation.orders.list`, `operation.orders.view`,
  `operation.dashboard.sales`,
  `operation.reports.*` (most reads), `operation.kpi.list`,
  `operation.kpi.view`.
- Strictly read-only by default; no create/update/delete grants.
- Filial-scoped.

### 10 — Expeditor

- `H::$denyRoles`: blocked from any web operation.
- Mobile-only role. Uses `/api3/expeditor*` controllers to fetch
  assigned trips, mark deliveries, accept returns, record cash.
- Sees only trips where `Trip.EXPEDITOR_ID = self.USER_ID`.

### 11 — Merchandiser

- `H::$denyRoles`: blocked from web.
- Mobile-only. Uses `/api3/adt*` controllers for store-check, photo
  reports, planogram audits.
- Sees only routes assigned to them (`Route.AGENT_ID =
  self.USER_ID`).

### 20 — Stockman

- Not in `auth.php` and not in `H::$bindRoles`. Permissions are
  enforced by raw `User->ROLE == 20` checks plus `accessRules()` on
  `stock/*` controllers.
- Default grants (when an admin sets `User.ROLE = 20`):
  `operation.stock.list`, `operation.stock.view`,
  `operation.stock.update`, `operation.stock.purchase`,
  `operation.stock.purchaseRefund`, `operation.stock.movement`,
  `operation.inventory.*`.
- No orders, no finans, no clients.

## Master matrix

Columns are the eight roles that actually exercise the `authassignment`
table: 1 (admin bypass), 2 (filial admin), 3 (diler bypass), 5
(operator), 6 (kassir), 7 (partner), 8 (svr), 9 (manager). Roles 4, 10,
11 are always-deny and not shown.

Shorthand:

- **all** — full operation namespace (list + view + create + update +
  delete).
- **L** — list/index only.
- **V** — view single row only.
- **L+V** — list and view.
- **L+V+C** — list, view, create.
- **L+V+C+U** — list, view, create, update.
- **bypass** — short-circuit allowRoles.
- **deny** — short-circuit denyRoles.
- **—** — no default grant.

### orders.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.orders.list` | bypass | all | bypass | L | L | — | L | L |
| `operation.orders.view` | bypass | all | bypass | V | V | — | V | V |
| `operation.orders.create` | bypass | all | bypass | C | — | — | — | — |
| `operation.orders.update` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.edit` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.print` | bypass | all | bypass | P | P | — | P | P |
| `operation.orders.import` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.importDefect` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.expeditor` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.tara` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.rejects` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.status` | bypass | all | bypass | U | — | — | — | — |
| `operation.orders.onMap` | bypass | all | bypass | V | — | — | V | V |
| `operation.orders.createRecovery` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.updateRecovery` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.createReplace` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.supplier.receipt` | bypass | all | bypass | — | — | — | — | — |
| `operation.orders.denyEditAgent` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditOnSent` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditOnDeliver` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditOnCancelOrReturn` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditPriceType` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditQuantity` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyEditWarehouse` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyFastEditing` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyFullyUpateRecovery` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.orders.denyPartialReturn` | bypass | all | bypass | yes | yes | yes | yes | yes |

The `operation.orders.denyEdit*` permissions are **negative** flags:
granting them blocks a category of order edits even for a role that
otherwise has `operation.orders.update`. Yes means the deny applies.

### finans.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.finans.cashbox` | bypass | all | bypass | V | V | — | — | V |
| `operation.finans.cashboxBalans` | bypass | all | bypass | — | V | — | — | — |
| `operation.finans.cashboxUpdate` | bypass | all | bypass | — | U | — | — | — |
| `operation.finans.cashboxdisplacement` | bypass | all | bypass | — | V | — | — | — |
| `operation.finans.cashboxdisplacementAdd` | bypass | all | bypass | — | C | — | — | — |
| `operation.finans.cashboxdisplacementCancel` | bypass | all | bypass | — | U | — | — | — |
| `operation.finans.consumption` | bypass | all | bypass | V | V | — | — | — |
| `operation.finans.addconsumption` | bypass | all | bypass | — | C | — | — | — |
| `operation.finans.editconsumption` | bypass | all | bypass | — | U | — | — | — |
| `operation.finans.deleteconsumption` | bypass | all | bypass | — | — | — | — | — |
| `operation.finans.consumptionCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.finans.consumptionReport` | bypass | all | bypass | V | V | — | — | V |
| `operation.finans.credit` | bypass | all | bypass | V | V | — | — | — |
| `operation.finans.editcredit` | bypass | all | bypass | — | U | — | — | — |
| `operation.finans.deletecredit` | bypass | all | bypass | — | — | — | — | — |
| `operation.finans.addDebt` | bypass | all | bypass | — | C | — | — | — |
| `operation.finans.paymentDisplacement` | bypass | all | bypass | — | C | — | — | — |
| `operation.finans.pnl` | bypass | all | bypass | — | — | — | — | V |

### clients.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.clients.list` | bypass | all | bypass | L | L | L | L | L |
| `operation.clients.view` | bypass | all | bypass | V | V | V | V | V |
| `operation.clients.create` | bypass | all | bypass | C | — | — | — | — |
| `operation.clients.update` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.duplicate` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.setActive` | bypass | all | bypass | U | — | — | U | — |
| `operation.clients.banMakingClientActive` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.banMakingClientInactive` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.shipper` | bypass | all | bypass | V | — | — | — | — |
| `operation.clients.shipperFinans` | bypass | all | bypass | V | V | — | — | — |
| `operation.clients.shipperFinans.initialBalans` | bypass | all | bypass | C | — | — | — | — |
| `operation.clients.shipperFinans.revise` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.shipperFinans.report` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.expeditorDolg` | bypass | all | bypass | V | V | — | — | — |
| `operation.clients.finans` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.finansCreate` | bypass | all | bypass | C | C | — | — | — |
| `operation.clients.finansDelete` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.finansInitialBalans` | bypass | all | bypass | C | — | — | — | — |
| `operation.clients.finansCreateInitialBalans` | bypass | all | bypass | C | — | — | — | — |
| `operation.clients.finansReport` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.finansRevise` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.transactions` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.transactionsView` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.transactionsUpdate` | bypass | all | bypass | — | U | — | — | — |
| `operation.clients.transactionWriteoff` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.transactionsConversion` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.transactionPivot` | bypass | all | bypass | V | V | — | — | V |
| `operation.clients.paymentApproval` | bypass | all | bypass | — | U | — | — | — |
| `operation.clients.approval` | bypass | all | bypass | U | — | — | U | — |
| `operation.clients.approval.view` | bypass | all | bypass | V | — | — | V | — |
| `operation.clients.approval.delete` | bypass | all | bypass | — | — | — | — | — |
| `operation.clients.allowBind` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.priceTypeBind` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.rlpBind` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.bonusBind` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.configBind` | bypass | all | bypass | U | — | — | — | — |
| `operation.clients.map` | bypass | all | bypass | V | — | — | V | V |
| `operation.clients.kassaIncome` | bypass | all | bypass | — | C | — | — | — |
| `operation.clients.agentVisits` | bypass | all | bypass | V | — | — | V | V |
| `operation.clients.generateQR` | bypass | all | bypass | V | — | — | — | — |

### stock.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.stock.list` | bypass | all | bypass | L | — | — | — | L |
| `operation.stock.detail` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.create` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.update` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.delete` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.movement` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.exchange` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.excretion` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.corrector` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.dailyRemainder` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.lotReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.materialReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.profit` | bypass | all | bypass | — | — | — | — | V |
| `operation.stock.purchase` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.purchaseUpdate` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.purchaseView` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.purchaseRefund` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.updatePurchaseRefund` | bypass | all | bypass | — | — | — | — | — |
| `operation.stock.purchaseReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.purchaseReportProfit` | bypass | all | bypass | — | — | — | — | V |
| `operation.stock.pivotDetail` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.recommend` | bypass | all | bypass | V | — | — | — | V |
| `operation.stock.vsExchange` | bypass | all | bypass | V | — | — | — | — |
| `operation.stock.vsExchangeAdd` | bypass | all | bypass | C | — | — | — | — |
| `operation.stock.vsExchangeEdit` | bypass | all | bypass | U | — | — | — | — |
| `operation.stock.vsReturn` | bypass | all | bypass | V | — | — | — | — |
| `operation.stock.vsReturnAdd` | bypass | all | bypass | C | — | — | — | — |
| `operation.stock.vsReturnEdit` | bypass | all | bypass | U | — | — | — | — |
| `operation.stock.vsReturnView` | bypass | all | bypass | V | — | — | — | — |

Role 20 (Stockman) — not in this table — receives the column-5
equivalents plus `purchase`/`update`/`movement`.

### settings.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.settings.user` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.product` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.productCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.productCaseType` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.price` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.priceType` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.changePrice` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.currency` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.closeDay` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.partners` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.diler` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.tradingTeam` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.city` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.channel` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.clientCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.akbCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.bonus` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.rlpBonus` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.loyalty` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.reject` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.rejectDefect` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.inventoryType` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.photoReportCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.tags` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.tara` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.taskType` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.knowledgeCategory` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.knowledgePost` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.unit` | bypass | all | bypass | — | — | — | — | — |
| `operation.settings.smartUp` | bypass | all | bypass | — | — | — | — | — |

`settings.*` is essentially a roles-1/2/3 zone. Operator may see a
few read-only fragments wired by hand (e.g. unit lists embedded in
order screens) but the canonical operations gate at admin level.

### reports.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.reports.agent` | bypass | all | bypass | V | — | — | V | V |
| `operation.reports.agentVisits` | bypass | all | bypass | V | — | — | V | V |
| `operation.reports.analyze` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.bonusReport` | bypass | all | bypass | V | — | — | V | V |
| `operation.reports.bonusReportDetail` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.bonusAccumulation` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.classification` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.classificationRFM` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.customer` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.customerDetail` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.discountDetail` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.expeditor` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.expeditorDebt` | bypass | all | bypass | V | V | — | — | V |
| `operation.reports.expeditorDefect` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.expeditorReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.export` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.inventorization` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.markupReport` | bypass | all | bypass | — | — | — | — | V |
| `operation.reports.minimum` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.photoReport` | bypass | all | bypass | V | — | — | V | V |
| `operation.reports.planExpeditor` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.price` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.report` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.reportBuilder` | bypass | all | bypass | — | — | — | — | V |
| `operation.reports.reportVisit` | bypass | all | bypass | V | — | — | V | V |
| `operation.reports.rlpReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.tara` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.telegram` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.tg.feedbackReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.volumeReport` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.volumeReportV2` | bypass | all | bypass | V | — | — | — | V |
| `operation.reports.workingTime` | bypass | all | bypass | V | — | — | V | V |

### rbac.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.rbac.users` | bypass | — | bypass | — | — | — | — | — |
| `operation.rbac.roles` | bypass | — | bypass | — | — | — | — | — |
| `operation.rbac.tasks` | bypass | — | bypass | — | — | — | — | — |
| `operation.rbac.operations` | bypass | — | bypass | — | — | — | — | — |

Role 2 (filial admin) does **not** receive RBAC management by default
to prevent privilege escalation by a filial-level admin assigning
themselves cross-filial operations.

### dashboard.\*, supervayzer.\*, kpi.\*

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.dashboard.finans` | bypass | all | bypass | V | — | — | — | V |
| `operation.dashboard.sales` | bypass | all | bypass | V | — | — | — | V |
| `operation.dashboard.supervayzer` | bypass | all | bypass | — | — | — | V | — |
| `operation.supervayzer.list` | bypass | all | bypass | — | — | — | L | — |
| `operation.supervayzer.create` | bypass | all | bypass | — | — | — | C | — |
| `operation.supervayzer.update` | bypass | all | bypass | — | — | — | U | — |
| `operation.supervayzer.delete` | bypass | all | bypass | — | — | — | — | — |
| `operation.kpi.list` | bypass | all | bypass | L | — | — | L | L |
| `operation.kpi.view` | bypass | all | bypass | V | — | — | V | V |
| `operation.kpi.create` | bypass | all | bypass | — | — | — | — | — |
| `operation.kpi.update` | bypass | all | bypass | — | — | — | — | — |
| `operation.kpi.result` | bypass | all | bypass | V | — | — | V | V |

### audit, adt, doctor, planning, task, inventory, expeditor, agents

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.audit.all` | bypass | all | bypass | V | — | — | V | V |
| `operation.adt.visit-report` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtAudit.list` | bypass | all | bypass | L | — | — | L | — |
| `operation.adtAudit.create` | bypass | all | bypass | — | — | — | C | — |
| `operation.adtAudit.update` | bypass | all | bypass | — | — | — | U | — |
| `operation.adtAudit.changeVisitDetail` | bypass | all | bypass | — | — | — | U | — |
| `operation.adtPoll.list` | bypass | all | bypass | L | — | — | L | — |
| `operation.adtPoll.create` | bypass | all | bypass | — | — | — | C | — |
| `operation.adtPoll.update` | bypass | all | bypass | — | — | — | U | — |
| `operation.adtMixReport.index` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.available` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.base` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.daily` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.monthly` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.price` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.retail` | bypass | all | bypass | V | — | — | V | V |
| `operation.adtReports.storeCheck` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.akb` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.akbPlan` | bypass | all | bypass | — | — | — | U | — |
| `operation.doctor.outlet` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.outletPlan` | bypass | all | bypass | — | — | — | U | — |
| `operation.doctor.personal` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.sku` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.skuPlan` | bypass | all | bypass | — | — | — | U | — |
| `operation.doctor.strikePlan` | bypass | all | bypass | — | — | — | U | — |
| `operation.doctor.strikeRate` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.total` | bypass | all | bypass | V | — | — | V | V |
| `operation.doctor.volumePlan` | bypass | all | bypass | — | — | — | U | — |
| `operation.planning.byproduct` | bypass | all | bypass | — | — | — | V | — |
| `operation.planning.byproductCreate` | bypass | all | bypass | — | — | — | C | — |
| `operation.planning.outlet` | bypass | all | bypass | — | — | — | V | — |
| `operation.planning.results` | bypass | all | bypass | V | — | — | V | V |
| `operation.planning.setup` | bypass | all | bypass | — | — | — | — | — |
| `operation.task.list` | bypass | all | bypass | L | — | — | L | L |
| `operation.task.create` | bypass | all | bypass | C | — | — | C | — |
| `operation.task.update` | bypass | all | bypass | U | — | — | U | — |
| `operation.task.photVote` | bypass | all | bypass | — | — | — | U | — |
| `operation.inventory.list` | bypass | all | bypass | L | — | — | — | L |
| `operation.inventory.create` | bypass | all | bypass | C | — | — | — | — |
| `operation.inventory.update` | bypass | all | bypass | U | — | — | — | — |
| `operation.inventory.history` | bypass | all | bypass | V | — | — | — | V |
| `operation.inventory.out` | bypass | all | bypass | — | — | — | — | — |
| `operation.expeditor.list` | bypass | all | bypass | L | — | — | L | L |
| `operation.expeditor.create` | bypass | all | bypass | C | — | — | — | — |
| `operation.expeditor.update` | bypass | all | bypass | U | — | — | — | — |
| `operation.agents.list` | bypass | all | bypass | L | — | — | L | — |
| `operation.agents.create` | bypass | all | bypass | — | — | — | C | — |
| `operation.agents.update` | bypass | all | bypass | — | — | — | U | — |
| `operation.agents.delete` | bypass | all | bypass | — | — | — | — | — |
| `operation.agents.limit` | bypass | all | bypass | — | — | — | U | — |
| `operation.agents.paket` | bypass | all | bypass | — | — | — | U | — |
| `operation.agents.reception` | bypass | all | bypass | — | — | — | U | — |
| `operation.agents.reestablish` | bypass | all | bypass | — | — | — | — | — |
| `operation.agents.visit.ordering` | bypass | all | bypass | — | — | — | U | — |

### sms, billing, marking, idokon, filial, vs, other

| Operation | 1 | 2 | 3 | 5 | 6 | 7 | 8 | 9 |
|-----------|---|---|---|---|---|---|---|---|
| `operation.sms.list` | bypass | all | bypass | V | — | — | — | V |
| `operation.sms.template` | bypass | all | bypass | — | — | — | — | — |
| `operation.sms.package.buying` | bypass | all | bypass | — | — | — | — | — |
| `operation.billing.index` | bypass | — | bypass | — | — | — | — | — |
| `operation.billing.distr` | bypass | — | bypass | — | — | — | — | — |
| `operation.billing.sms` | bypass | — | bypass | — | — | — | — | — |
| `operation.marking.incoming` | bypass | all | bypass | V | — | — | — | — |
| `operation.marking.outgoing` | bypass | all | bypass | V | — | — | — | — |
| `operation.idokon.incoming.request` | bypass | all | bypass | V | — | — | — | — |
| `operation.filial.movement.request.list` | bypass | all | bypass | L | — | — | — | L |
| `operation.filial.movement.request.create` | bypass | all | bypass | C | — | — | — | — |
| `operation.filial.movement.request.edit` | bypass | all | bypass | U | — | — | — | — |
| `operation.filial.movement.request.view` | bypass | all | bypass | V | — | — | — | V |
| `operation.vs.deny.status.to.lower` | bypass | all | bypass | yes | yes | yes | yes | yes |
| `operation.vs.downloads` | bypass | all | bypass | V | — | — | — | V |
| `operation.notification.list` | bypass | all | bypass | L | L | L | L | L |
| `operation.other.gps` | bypass | all | bypass | — | — | — | V | V |
| `operation.smartup5x.index` | bypass | all | bypass | V | — | — | — | — |

## Gotchas

### allowRoles bypasses the entire RBAC graph

Even if a tenant admin clears every `authassignment` row for role 3,
that user will still pass `H::access(...)` because the short-circuit in
`H.php` lines 63–65 runs before the database lookup. If you want to
actually deny a role-3 user, you must move them to a different role
(typically 2 with explicit assignments).

### denyRoles short-circuits before checkAccess

Conversely, roles 4, 10, 11 are unconditionally rejected from `H::access`,
even if you grant them every operation in the system. Their access
path is api3 only. If a web view contains `H::access('operation.X',
true)`, those users see a 403 even when the same screen would render
for a guest after they log in as another role.

### actionGetData does not re-check access

A common pattern in legacy controllers (e.g.
`orders/controllers/OrdersController.php`) is:

```php
public function actionIndex() {
    H::access('operation.orders.list');
    // render shell
}

public function actionGetData() {
    // returns JSON for the grid, NO H::access call
}
```

If the action returning JSON is ever exposed as a direct route
(`/orders/orders/getData`), it bypasses the gate. Always re-check
inside the data endpoint, or rely on the framework's `accessRules` /
`filters` chain.

### accessRules in controller can grant broader access than H::access

Some controllers (`clients/controllers/ClientController.php` line
115–148) ship a hand-rolled `accessRules()` array that admits role 7
to `index`, `jasonData`, etc. — without ever consulting `authitem`.
That list is the actual access gate; the `H::access` call inside the
action is the secondary gate. When you grep for "who can hit
/clients/client/index?", you need to read **both**.

### Role 20 (Stockman) is not in auth.php

The stock module uses `User::ROLE_STOCKMAN = 20` and switches on
`Yii::app()->user->ROLE == 20` directly. There are no `authitem`
rows for role 20. When a tenant migrates from raw role-int checks to
RBAC, role 20 users typically lose access until the admin manually
binds `role.stockman` (the suggested item name) to the relevant
`operation.stock.*` entries.

### The cache TTL is 600 seconds

`DbAuthManager` caches the resolved permission set per (tenant, user)
in `redis_app` for 600 s. After granting a new permission to a user
that's currently logged in, expect up to 10 minutes before the change
takes effect — or call `bumpUserVersion($userId)` from `Access.php`
explicitly.

### bindRoles only covers four roles

`H::$bindRoles` only maps {5,6,8,9} to canonical RBAC item names. When
a tenant admin changes a user's role to 2 (Administrator Filial) or 7
(Partner), the `setUserRole` helper hits the `not_found` branch and
returns an error. Those two roles must be configured via direct
`authassignment` inserts in the RBAC admin UI.

### denyEdit\* are positive flags meaning "block"

The `operation.orders.denyEdit*` family is **inverted**: granting them
to a role blocks specific edit categories. So if you remove
`operation.orders.denyEditAgent` from role 5, the operator gains the
ability to reassign orders to different agents. This is the source of
frequent footgun confusion when documenting per-role permissions.

## How to test access

For each role, here is one URL that should pass and one that should
fail. Replace `example.salesdoc.io` with your tenant host. Log in as
the role (use the seed `operator@example`, `kassir@example`, etc.) and
hit each URL.

| ROLE | should pass | should 403 |
|------|-------------|-----------|
| 1 | `/settings/user/index` | n/a — bypasses everything |
| 2 | `/orders/orders/index` | `/access/backend/users` |
| 3 | `/finans/cashbox/index` | n/a — bypasses everything |
| 4 | `/api3/login` (POST) | `/orders/orders/index` (web) |
| 5 | `/orders/orders/index` | `/finans/cashbox/index` |
| 6 | `/finans/cashbox/index` | `/orders/createOrder/index` |
| 7 | `/clients/client/index` | `/orders/orders/index` |
| 8 | `/dashboard/supervayzer/index` | `/settings/product/index` |
| 9 | `/dashboard/sales/index` | `/orders/createOrder/index` |
| 10 | `/api3/expeditor/trips` (GET) | `/orders/orders/index` (web) |
| 11 | `/api3/adt/storeCheck` (GET) | `/clients/client/index` (web) |
| 20 | `/stock/stock/index` | `/orders/orders/index` |

### Manual audit query

To list every operation actually granted to a user in a given filial:

```sql
SELECT a.itemname AS operation
FROM authassignment a
WHERE a.userid = :user_id
  AND a.filial_id = :filial_id
ORDER BY a.itemname;
```

To list the full transitive closure (including inherited children):

```sql
WITH RECURSIVE walk(parent, child) AS (
  SELECT parent, child FROM authitemchild
  WHERE parent IN (
    SELECT itemname FROM authassignment WHERE userid = :user_id
  )
  UNION
  SELECT c.parent, c.child FROM authitemchild c
  JOIN walk w ON c.parent = w.child
)
SELECT DISTINCT child FROM walk WHERE child LIKE 'operation.%'
ORDER BY child;
```

## See also

- [Auth and roles](./auth-and-roles.md) — canonical role list and
  authentication paths.
- [RBAC primer](./rbac.md) — table layout, cache wiring, how to add a
  new permission.
- [Operations catalog](./operations-catalog.md) — every
  `operation.*` string with file:line references.
- [sd-main landmines](./sd-main-landmines.md) — broader list of
  RBAC-adjacent footguns.
