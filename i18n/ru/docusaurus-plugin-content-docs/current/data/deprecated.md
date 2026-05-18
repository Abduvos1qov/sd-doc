---
sidebar_position: 8
title: Deprecated code inventory
audience: Backend engineers, ops, anyone refactoring the codebase
summary: Complete inventory of deprecated source files across sd-main, sd-cs and sd-billing. Files renamed to `.obsolete` are not loaded by PHP autoload and are safe candidates for removal. Vestigial-but-still-loaded code is flagged separately.
topics: [deprecated, cleanup, obsolete, refactoring, technical-debt]
---

# Deprecated code inventory

A complete inventory of source files that have been deprecated across the three projects. Use this as the source of truth when planning cleanup commits.

## Quick numbers

| Project | Deprecated files | Pattern | Status |
|---------|-----------------:|---------|--------|
| **sd-main** | 585 | `*.obsolete` suffix | Not loaded by PHP — safe to delete |
| **sd-cs** | 0 (no suffix convention) | — | Vestigial-but-loaded models exist; see below |
| **sd-billing** | 1 | `*.absolute` suffix (likely typo of `.obsolete`) | Single file; review needed |

:::info Why "deprecated"?
The repo convention is to rename a PHP file to `<name>.php.obsolete` when it's no longer needed but kept around for reference. PHP's autoloader and Yii's classmap only look for `*.php`, so renamed files are effectively dead. Their git history is preserved if anyone needs to recover them.
:::

---

## sd-main — 585 deprecated files

### Breakdown by category

| Category | Count | Action recommendation |
|----------|------:|-----------------------|
| Module views (`modules/*/views/*.obsolete`) | 307 | Delete — old screen layouts never rendered |
| Module controllers (`modules/*/controllers/*.obsolete`) | 151 | Delete — code paths replaced by newer controllers |
| JS bundles (`js/*.obsolete`) | 42 | Delete — old Vue.js bundles |
| Vendor directories (`vendors/*.obsolete`) | 27 | Delete — npm packages that were vendored and replaced |
| Top-level models (`models/*.obsolete`) | 14 | Delete — historical models with no active references |
| Layout templates (`views/layouts/*.obsolete`) | 10 | Delete — old page chrome |
| Top-level controllers (`controllers/*.obsolete`) | 6 | Delete — replaced by module-scoped equivalents |
| Module models (`modules/*/models/*.obsolete`) | 4 | Delete |
| Components (`components/*.obsolete`) | 1 | Delete — `Faktura.php.obsolete` (replaced by integration module) |
| **Total** | **585** | |

### Deprecated module controllers (151 files)

Grouped by module — these are the controllers that have been renamed `.php.obsolete` since their actions moved elsewhere.

#### `orders` module — 12 deprecated controllers, 123 deprecated files total

The biggest single module by deprecated-file count. Most of the 123 files are old view templates.

Deprecated controllers:
- `OrderDefectController`, `OrderController`, `Create2Controller`, `Create3Controller`, `CreateOrder2Controller`, `CreateOrder3Controller`, `Orders2Controller`, `StoreController`, `TaraDocumentController`, `TaraOrdersController`, `SupervayzerOrderController`, `DefaultController`

Active replacements: see [orders module](/docs/modules/orders).

#### `stock` module — 9 deprecated controllers, 51 deprecated files

Deprecated controllers:
- `StoreRemainderController`, `CreateStoreController`, `DefaultController`, `StatsController`, `TotalioController`, `ClientSecondSaleController`, `StoreDetailController`, `StoreHistoryController`, `ReserveController`

Active replacements: see [stock module](/docs/modules/stock).

#### `agents` module — 6 deprecated controllers, 50 deprecated files

Deprecated controllers:
- `AgentPlanController`, `DoPlanningController`, `PollController`, `ExpeditorController`, `PaketController`, `VisitingController`

Active replacements: see [agents module](/docs/modules/agents).

#### `settings` module — 6 deprecated controllers, 47 deprecated files

Deprecated controllers:
- `PriceController`, `AdminpriceController`, `AkbCategoryController`, `PlanController`, `SubProductCategoryController`, `InventoryController`

Active replacements: see [settings module](/docs/modules/settings).

#### `clients` module — 7 deprecated controllers, 41 deprecated files

Deprecated controllers:
- `ContractController`, `CorrectClientController`, `DebtCreditController`, `ClientsController`, `ClientTransactionController`, `DebtFinansController`, `ClientsupController`

Active replacements: see [clients module](/docs/modules/clients).

#### `report` module — 14 deprecated controllers, 30 deprecated files

Deprecated controllers:
- `AllProductsController`, `NeakbController`, `SaleController`, `StrikeController`, `BonusController`, `AgentExcelController`, `DiscountController`, `DefaultController`, `ExpeditorDefectController`, `AgentExcelNewController`, `DefectReportController`, `CreateImageReportController`, `ClosedOrdersController`, `StockExpController`

Active replacements: see [report module](/docs/modules/report).

#### `api` module (v1) — 29 deprecated controllers

Deprecated controllers:
- `RejectController`, `OnecController`, `EsaleController`, `PriceController`, `AlisherController`, `Intersok2Controller`, `TestController`, `CronVisit2Controller`, `SdocController`, `LogoutController`, `ProductoldController`, `ClientController`, `AbController`, `StoreController`, `Xml1CController`, `ProductController`, `PriceTypeController`, `HistoryController`, `KpiController`, `DoctorController`, `ProductCategoryController`, `OneController`, `PrefixController`, `IntersokNavoiController`, `VenkonController`, `OutletController`, `LoginController`, `IntersokController`, `TestDeyaController`

Active replacements: see [api v1 docs](/docs/api/api-v1) and the [api module reference](/docs/modules/orders) (action-level coverage in progress).

#### `api2` module — 26 deprecated controllers

Deprecated controllers:
- `RejectController`, `DbController`, `Product2Controller`, `PriceController`, `GpsController`, `StructureController`, `DiscountController`, `DefaultController`, `LogoutController`, `ProductoldController`, `ClientController`, `AddclientController`, `StoreController`, `LogController`, `Export1CController`, `ProductController`, `PriceTypeController`, `HistoryController`, `OrderController`, `KpiController`, `LoginTokenController`, `StockController`, `ProductCategoryController`, `PhotoController`, `LoginController` (plus 1 unnamed)

Active replacements: api/v3-mobile and api/v4-online; see [api v2 docs](/docs/api/api-v2) for the migration map.

#### `api3` module — 14 deprecated controllers

Deprecated controllers within the otherwise-active mobile API:
- `PriceController`, `Order2Controller`, `AuditController`, `DefaultController`, `SvController`, `SdClientController`, `ProductoldController`, `OrderUpdateController`, `AddclientController`, `LogController`, `Export1CController`, `LoginTokenController`, `StockExpController`, plus 1 named `unknown`

Active replacements: see [api v3 mobile](/docs/api/api-v3-mobile/auditor).

#### `api4` module — 2 deprecated controllers

- `CreateDefectController`, `CreateOrderController`

Active replacements: `EditController`, `GetController`, and `CreateOrderAction` in `api4`.

#### `sync` module — 6 deprecated controllers (the ENTIRE module is essentially dead)

- `DefaultController`, `SettingController`, `DilerController`, `PurchaseController`, `ProductController`, `ServerController`

All 13 files in `modules/sync/` are `.obsolete`. The sync surface migrated to `api3` and `api4`.

#### `dashboard` module — 6 deprecated controllers

- `CustomerController`, `AccessController`, `TestController`, `SupervisorController`, `HeyadminController`, `AdminController`

#### `adt` module — 6 deprecated controllers

- `SummaryController`, `PollReportController`, `UserController`, `MefStoreCheckController`, `StoreController`, `MefStoreCheck2Controller`

#### `manager` module — 2 deprecated controllers (entire module is deprecated)

- `DefaultController`, `OrdersController`

The module folder is otherwise empty — placeholder noted in [manager module](/docs/modules/manager).

#### `neakb` module — 2 deprecated controllers (entire module is deprecated)

- `BackendController`, `FrontendController`

The module folder is otherwise empty — placeholder noted in [neakb module](/docs/modules/neakb).

#### Smaller modules with 1–2 deprecated controllers

- `planning`: `ApiController`, `StoreController`
- `store`: `ReportController`
- `gps`: `ClientInMapController`
- `finans`: `ReportController`

### Deprecated top-level controllers (6 files)

Located in `protected/controllers/` (pre-module-namespace era):

- `AgentsController.php.obsolete`
- `ClientsController.php.obsolete`
- `MyController.php.obsolete`
- `PlanController.php.obsolete`
- `ProductController.php.obsolete`
- `RequestController.php.obsolete`

All have been replaced by module-scoped equivalents.

### Deprecated top-level models (14 files)

Located in `protected/models/`:

| Model | Likely replaced by |
|-------|--------------------|
| `AAudit.php.obsolete` | `AdtAuditResult` / `AdtAuditResultData` (audit v2) |
| `ACategory.php.obsolete` | `ClientCategory` |
| `AudProductGroup.php.obsolete` | `AdtProductGroup` |
| `ClientRemainder.php.obsolete` | `Stock` / `WarehouseDetail` |
| `ClientSecondSale.php.obsolete` | `OrderDetail` (no separate model) |
| `Contract.php.obsolete` | `Contragent` (per [`core-entities`](./core-entities) — old `d0_contract` table still queried) |
| `DoPlanning.php.obsolete` | `Plan` |
| `PartnerDetail.php.obsolete` | partner module's models |
| `ProductCatPartners.php.obsolete` | `Partner` + `ProductCategory` relations |
| `RejectCategory.php.obsolete` | inline enum on `OrderDetail` |
| `StoreRemainder.php.obsolete` | `WarehouseDetail` |
| `StoreReserve.php.obsolete` | `WarehouseDetail` reserve column |
| `StoreSecondSale.php.obsolete` | merged into order flow |
| `SubProductCategory.php.obsolete` | `ProductCategory` (parent_id pattern) |

### Deprecated components (1 file)

- `Faktura.php.obsolete` — replaced by the [integration module's Faktura.uz integration](/docs/integrations/faktura-uz).

### Deprecated layouts (10 files)

Pre-Vue.js page chrome under `protected/views/layouts/`:

- `auditSettings2.php.obsolete`, `column2.php.obsolete`, `column3.php.obsolete`, `columnAdmin.php.obsolete`, `iikoMenu.php.obsolete`, `main.php.obsolete`, `mainAdmin.php.obsolete`, `main_mobile.php.obsolete`, `main_webview.php.obsolete`, `menu.php.obsolete`

Replaced by the SPA single-page shell — no admin pages use the old layouts.

### Deprecated JS bundles (42 files)

Old Vue.js compiled bundles in `js/`. Examples: jQuery-knob, jPlist, gmaps, intro.js, ckeditor — all vendor-scoped one-off includes that were replaced by modern equivalents or removed entirely.

### Deprecated vendor directories (27 directories)

In `vendors/`:

- `jquery-knob.obsolete`, `sco.message.obsolete`, `flot-chart.obsolete`, `calendar.obsolete`, `jquery-tablesorter.obsolete`, `jquery-animateNumber.obsolete`, `pace.obsolete`, `skycons.obsolete`, `intro.js.obsolete`, `ckeditor.obsolete`, `bootstrap-wysihtml5.obsolete`, `jplist.obsolete`, `jquery-jvectormap.obsolete`, `jquery-bootstrap-wizard.obsolete`, `gps.obsolete`, `tableExport.obsolete`, `jquery-highcharts.obsolete`, `jquery-wow.obsolete`, `nouislider.obsolete`, `gmaps.obsolete` (+ 7 more)

These were vendored copies of jQuery plugins from the pre-Vue era.

---

## sd-cs — vestigial code

sd-cs does NOT use the `.obsolete` suffix convention. Deprecated code stays as `.php` and is simply no longer called.

### Audit results — call-graph analysis (2026-05-18)

A full programmatic audit walked every class in `protected/`, counted references in `.php` / `.js` / `.sql` / `.json` files (excluding the class's own file), and flagged any with zero external references. False positives from Yii's string-name dispatch (modules, controllers, commands) were filtered out by hand. Only models, components, and helpers were considered.

**Confirmed vestigial — zero references in any file:**

| Class | File | Action |
|-------|------|--------|
| `CreatedStores` | `protected/modules/directory/models/CreatedStores.php` | Safe to delete |
| `StoreReserve` | `protected/modules/directory/models/StoreReserve.php` | Safe to delete (sd-main has a matching `.obsolete` model of the same name) |
| `UserDiler` | `protected/modules/directory/models/UserDiler.php` | Safe to delete |

**Cleanup commit:** `chore/remove-vestigial-models` branch off `master` (worktree at `../sd-cs-cleanup`, commit `0dd7e154`, not pushed).

### NOT vestigial — flagged here for the record

A previous draft of this page (and the [sd-cs schema reference](./sd-cs/schema)) loosely described these as "vestigial." That description was inaccurate. They are **active**:

| Class | Why people thought it was vestigial | Actual status |
|-------|------------------------------------|---------------|
| `directory/models/Client.php` | No `getDbConnection` override — looks like it maps to a non-existent `cs_client` table | **Active.** Used by `Report` component, `api/V2Controller`, multiple pivot controllers, `Isellmore4Command`, `dashboard/DailyController`. Instantiated under the dealer connection — reads dealer `d0_client` data |
| `directory/models/WorkingDays.php` | Same reasoning as `Client` — uppercase column names suggest a dealer table | **Active.** Used by `directory/models/KpiTaskTemplate`, `dashboard/DailyController`, `api3/ManagerController`. Reads dealer `d0_working_days` |

Cross-tenant reader models that read from the swapped dealer connection are a real sd-cs pattern — they look like sd-cs models but operate on dealer data. See [sd-cs Multi-DB](/docs/sd-cs/multi-db) and the schema page's "Vestigial / external models" section for the canonical explanation.

---

## sd-billing — single deprecated file

| File | Note |
|------|------|
| `protected/modules/api/controllers/MaintenanceController.php.absolute` | Suffix `.absolute` looks like a typo of `.obsolete`. The file is unloaded by PHP either way. |

**Action:** rename `.absolute` → `.obsolete` for consistency with sd-main convention, OR delete outright.

Other sd-billing deprecated items (per the existing [sd-billing modules](/docs/sd-billing/modules) docs) are stale model docblocks rather than full deprecated files — those are documentation hygiene, not code cleanup.

---

## Recommended cleanup phases

### Phase 33.1 — Document (this page) ✅ done

You're reading it. The inventory is preserved here and in git history.

### Phase 33.2 — Delete sd-main `.obsolete` files (low risk)

Single commit on a branch:

```
chore: remove 585 .obsolete files (already non-loaded by PHP)
```

Verification: `find . -name "*.obsolete" -delete` from the sd-main repo root, then run the existing test suite + smoke-test the live app.

### Phase 33.3 — Fix sd-billing `.absolute` typo

Rename or delete `MaintenanceController.php.absolute`.

### Phase 33.4 — sd-cs vestigial audit (per-file review)

Call-graph audit using `composer dump-autoload` + grep across `use` statements + `new ClassName()` patterns. Manual review before removal.

---

## See also

- [Core entities](./core-entities) — current canonical models
- [Schema reference](./schema-reference) — live DB schema
- [sd-billing schema](./sd-billing/schema) — per-table sd-billing reference
- [sd-cs schema](./sd-cs/schema) — per-table sd-cs reference
- [Migrations](./migrations) — how schema changes flow through
