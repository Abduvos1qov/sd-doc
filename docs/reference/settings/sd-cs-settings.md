---
sidebar_position: 5
title: sd-cs settings
audience: Backend engineers, ops, support
summary: Every static config file, ACL row, saved-pivot, and role default that shapes the HQ control-plane behaviour in sd-cs.
topics: [settings, toggles, sd-cs, configuration, acl, filial-visibility, role-defaults, catalog]
---

# sd-cs — settings catalog

The HQ control-plane (`sd-cs`, "Country Sales") is the multi-dealer dashboard. A single sd-cs install can swap between several tenant databases at runtime via `Yii::app()->dealer`, present aggregate reports across all of them, and gate visibility per HQ user via a filial-scope ACL. Behaviour is shaped by five layers:

1. **Static config files** under `protected/config/` — modules, DB, redis, theme.
2. **The dealer-swap runtime knob** — `Yii::app()->dealer` is the per-tenant DB connection, swapped per request; not a setting per se but the master knob that decides which tenant's data you are looking at.
3. **Filial-visibility ACL** — `cs_user_filial` rows scope each HQ user to a set of filials.
4. **Saved pivot layouts** — the `cs_pivot_config` table stores named JSON layouts per pivot report, keyed by a controller-side `ReportConfigCode`.
5. **Role + per-action access rows** — `cs_access_role` (one row per role × operation) and `cs_access_user` (per-user overrides), with the canonical operation list hardcoded in `AccessManager::$accesses`.

## Static config — `protected/config/`

| File | Purpose | What changing it affects |
|------|---------|--------------------------|
| `main.php` | Web app bootstrap — modules, components, URL rules, asset manager, theme | Module registration list (`user`, `directory`, `report`, `dashboard`, `pivot`, `api`, `api3`). Adding or removing a module disables every controller under it. |
| `console.php` | CLI bootstrap — currently still on the Yii skeleton template (sqlite test DB). Production cron uses `db.php` overrides; this file is not actively used in deployed installs. | Almost nothing today — kept for `yiic` shell access. |
| `db.php` | The **two** database connections. `db` points to the HQ schema (default `cs3_demo`, prefix `cs_`). `dealer` points to one tenant's schema (default `b_demo`, prefix `d0_`). Both inherit `mysql:host=db`, user `jamshid`, password `secret` in the checked-in template — production overwrites this file via deploy. | Which HQ schema and which initial tenant the app reads. The `dealer` connection is reassigned per request — see below. |
| `db_sample.php` | Template for the above | Nothing — copy to `db.php` on first install. |
| `test.php` | PHPUnit harness config | Test runs only. |
| `params.php` | Optional override params, merged into the `params` array in `main.php`. The file is included only `if (file_exists(...))`. | Site-specific values (legacy — most installs do not ship one). |

### `params` in main.php

| Key | Default | Read where |
|-----|---------|-----------|
| `adminEmail` | `tillayev00@gmail.com` | Yii error / cron failure notifications. Merged with whatever `params.php` provides. |

### `components` in main.php

Notable components that act as switches at boot time:

| Component | Effect |
|-----------|--------|
| `accessManager` (class `user.components.AccessManager`) | Loads the canonical `$accesses` map. Every controller's `hasAccess(...)` call hits this singleton. |
| `themeManager` with `theme` = `classic` | Switches which `themes/<name>/` layout is rendered. Changing the theme key in `main.php` lets you ship a tenant-specific skin. |
| `redis_cache` (`hostname` 10.0.0.11, port 6379) | Cache backend. Hardcoded IP. Misroute it and every cache lookup throws. |
| `session` (class `CCacheHttpSession`, `cacheID` `redis_cache`, `timeout` 7200) | Session storage. Two-hour idle limit. |
| `assetManager.linkAssets` = `true`, `forceCopy` = `false` | Symlink assets in production for cache invalidation; copy them in dev. Flip to `forceCopy` on shared hosts that disallow symlinks. |

## The dealer-swap runtime knob

`Yii::app()->dealer` is a `CDbConnection` registered in `db.php` and reassigned at the start of every request based on which dealer the HQ user has selected. **It is not a setting** — there is no UI field that flips it permanently — but it is the master knob that decides which tenant's data you are reading.

It is referenced in dozens of places:

- `components/SideMenu.php` line 481 — builds the menu from the tenant DB.
- `components/BaseModel.php` line 165 — loads model lists from the tenant.
- `components/Report.php` lines 360 and 362 — every aggregated report runs against `dealer`.
- `commands/IsellmoreCommand.php` and `Isellmore4Command.php` — cron aggregators iterate over every active dealer, rebinding `dealer` on each pass.
- Every `pivot/*Controller.php` and most of `report/*Controller.php` and `directory/*Controller.php` issue `Yii::app()->dealer->createCommand(...)` directly.

```mermaid
flowchart LR
    A[HQ user logs in] --> B[Picks dealer from header dropdown]
    B --> C[Session stores selected dealer ID]
    C --> D[Each request rebinds<br/>Yii::app()->dealer to that<br/>dealer's CDbConnection]
    D --> E[Every report / pivot /<br/>directory query reads from dealer]
    F[Cron Isellmore4] --> G[Iterates active dealers]
    G --> H[Rebinds dealer per iteration]
    H --> I[Aggregates into cs_ tables]
```

Cross-link: see [`/docs/sd-cs/multi-db`](/docs/sd-cs) for the full mechanics, including how the dealer DSN is built from `cs_diler` rows and how the cron walks the active list.

## Filial-visibility ACL — `cs_user_filial`

Every HQ user is scoped to a set of filials. The table is small:

```sql
CREATE TABLE cs_user_filial (
    id INT NOT NULL AUTO_INCREMENT,
    filial_id INT NOT NULL,
    user_id INT NOT NULL,
    create_by INT NOT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(id),
    CONSTRAINT user_key FOREIGN KEY (user_id) REFERENCES cs_user(id) ON DELETE CASCADE
);
```

| Column | Meaning |
|--------|---------|
| `user_id` | FK to `cs_user.id` — cascading delete |
| `filial_id` | FK to the tenant's `Filial` rows (lives in the dealer DB, not the HQ DB — no foreign-key constraint at the DB level) |
| `create_by` | HQ user who granted the scope |
| `create_time` | When the grant was made |

The model `UserFilial` (in `protected/modules/directory/models/UserFilial.php`) exposes two helpers:

| Helper | Purpose |
|--------|---------|
| `UserFilial::getFilials($prefix, $pre)` | Returns the list of filials the current HQ user can see. **Admins get every active filial** (`Filial::getList(... 'active = "Y"')`); non-admins get only filials with a row in `cs_user_filial`. |
| `UserFilial::getBonus($prefix, $modelFilial, $id)` | Returns the list of bonus / discount / royalty IDs visible to the user. Admins see all; non-admins see only those whose `FILIAL_ID` is in their scope. Called by `BonusController`, `SkidkaController`, `SkidkaManualController`, `RoyaltyController`. |

**ACL evaluation pattern:**

Every gated controller does roughly:

```php
$access = $this->accessManager->hasAccess('directory.bonus.update');
$user_filial_bonus = UserFilial::model()->getBonus();
if ($access || Yii::app()->user->isAdmin()
   || $bonus['create_by'] == Yii::app()->user->id
   || in_array($bonus['id'], $user_filial_bonus)) {
    // proceed
}
```

So a non-admin user can edit a bonus if **any** of these is true:

1. They have the operation row (`directory.bonus.update`) granted.
2. They created the bonus themselves.
3. The bonus is attached to a filial in their `cs_user_filial` scope.

### Other filial-scope tables

These extend the same pattern for specific reference data:

| Table | Notes |
|-------|-------|
| `cs_filial_detail` | Links filials to territories (and an `alt` label) |
| `cs_filial_group` | Many-to-many between filials and `cs_group` groupings |

## Saved-pivot semantics — `cs_pivot_config`

Every pivot-style report stores its named layouts (which columns, rows, filters, sorts) in `cs_pivot_config`:

```sql
CREATE TABLE cs_pivot_config (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(100) NOT NULL,
    config TEXT NOT NULL,
    create_by INT NOT NULL,
    update_by INT NULL,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME NULL,
    PRIMARY KEY(id)
);
```

Each controller declares its own `const ReportConfigCode` and uses it as the `code` filter when listing or saving. The full set:

| Controller | `ReportConfigCode` | What the row stores |
|------------|--------------------|---------------------|
| `pivot/UserAccessController` | `userAccess` | User-access pivot layouts |
| `pivot/PlanVisitController` | `planVisit` (also `planVisit_detail`) | Plan-visit summary and detail layouts |
| `pivot/NewDiscountController` | `sale` | Shared with `NewSaleController` — sale-side pivot layouts |
| `pivot/NewSaleController` | `sale` | Same code as above — both controllers share saved layouts |
| `pivot/ExpeditorController` | `expeditor` (plus detail variant) | Expeditor pivot layouts |
| `pivot/SkuController` | `consumption` | Shared with `ConsumptionController` |
| `pivot/ConsumptionController` | `consumption` | Same code as above |
| `pivot/PurchaseController` | `purchase` | Purchase pivot layouts |
| `pivot/AkbController` | `akb` | AKB pivot layouts |
| `pivot/LotReportController` | `lot_report` | Lot-tracking pivot layouts |
| `pivot/TransactionsController` | `transaction` | Transactions pivot layouts |
| `pivot/SaleDetailController` | `sale_detail` | Sale-detail pivot layouts |
| `report/PivotInventoryController` | `pivot_inventory` | Inventory pivot layouts |
| `report/MovementController` | `movement` | Inter-filial movement layouts |
| `report/PlanningController` | `planning` | Agent-planning pivot layouts |
| `report/InventoryController` | `inventoryScan` | Inventory-scan pivot |
| `report/SummaryBonusController` | `bonus` | Summary-bonus pivot |
| `report/BonusSaleController` | `bonus-sale` | Bonus-sale pivot |
| `directory/InventoryController` | `inv` | Directory-inventory pivot |

**Save / delete mechanics** (typical implementation, e.g. `PivotInventoryController::actionSaveReport()` lines 507-543):

1. POST body is decoded by `getData()`.
2. If the body carries an `id`, that `PivotConfig` row is loaded and updated; otherwise a new row is inserted.
3. `name` ← user-supplied title, `config` ← JSON-encoded layout, `code` ← the controller's `ReportConfigCode`.
4. `actionDeleteReport()` hard-deletes by primary key — no soft-delete, no ownership check beyond what the controller's `allowedActions` whitelist enforces.

**Special-case rows** — a few controllers use `name` + `code` together as a singleton config slot rather than a list:

| Row | Used by | Purpose |
|-----|---------|---------|
| `name = 'okb_config', code = 'okb_config'` | `report/OkbController` | The single OKB configuration (type + items) — there is only one such row, edited in place |
| `name = 'nmedov_categories', code = 'nmedov_categories'` | `report/NmedovController` | NMEDOV category whitelist |
| `name = 'nmedov_filials', code = 'nmedov_filials'` | `report/NmedovController` | NMEDOV filial whitelist |

## Role defaults — `AccessManager::$accesses`

The canonical operation list is **hardcoded** in `protected/modules/user/components/AccessManager.php` as a static array. Every entry is `'<module>.<controller>.<action>' => '<Russian label>'`. Granting an operation means inserting a row in `cs_access_role` (per role) or `cs_access_user` (per user) with `name` matching the operation key and `access` = `1`.

| User role (`User::ROLE_*`) | Value | Default access |
|----------------------------|-------|----------------|
| `ROLE_ADMIN` | `1` | **Bypasses every check** — `AccessManager::hasAccess()` short-circuits on `isAdmin()` and returns true. No `cs_access_role` rows are consulted. |
| `ROLE_MANAGER` | `2` | Only the operations explicitly listed in `cs_access_role` where `role = 2` |
| `ROLE_OPERATOR` | `3` | Same pattern, `role = 3` |

The full operation namespace (≈ 250 entries) is grouped by module:

| Module | Sample operations | Notes |
|--------|-------------------|-------|
| `report.*` | `report.sell.index`, `report.store.index`, `report.okb.index`, `report.akb.index`, `report.debt.index`, `report.inventory.index`, `report.movement.index`, `report.purchase.index`, `report.kpi.index`, `report.nmedov.index`, ... | Each top-level report has at least an `.index` operation. Subsections add `.scan`, `.dashboard`, `.daily`. |
| `user.default.*` | `user.default.index`, `.create`, `.update`, `.delete` | HQ user CRUD |
| `dashboard.daily.index` | One row | The single daily dashboard |
| `directory.<entity>.*` | `directory.region.{index,create,update,delete}`, `directory.territory.*`, `directory.adtAudit.*`, `directory.adtBrand.*`, ..., `directory.bonus.{index,create,update,onlyUsers}`, `directory.skidka.*`, `directory.skidkaManual.*`, `directory.royalty.*`, `directory.rlpBonus.*`, ... | The largest group. Most entities have `.index`, `.create`, `.update`; `.delete` is commented out for many (intentional — soft-delete only). `bonus`, `skidka`, `royalty`, `skidkaManual` each add `.onlyUsers` (show only items attached to current user). |
| `pivot.<report>.index` | `pivot.sale.index`, `pivot.discount.index`, `pivot.rfm.index`, `pivot.saleDetail.index`, `pivot.defect.index`, `pivot.transactions.index`, `pivot.consumption.index`, `pivot.planVisit.index`, `pivot.expeditor.index`, `pivot.userAccess.index`, `pivot.lotReport.index`, `pivot.purchase.index`, `pivot.akb.index` | Each pivot report needs its own grant |

### Hierarchy

`AccessManager::hasAccess($operation)`:

1. If user is admin (`User::ROLE_ADMIN = 1`) → return true.
2. Lazy-load `cs_access_role` rows for the user's role into `$this->_access`.
3. Then load `cs_access_user` rows for the user — these override role grants.
4. Return `!empty($this->_access[$operation])`.

**Implication:** per-user rows in `cs_access_user` override per-role rows in `cs_access_role`. To revoke a single operation from a single manager without affecting other managers, insert a `cs_access_user` row with `access = 0`.

## Geographic hierarchy reference

Four tables form the geographic tree HQ uses to group filials:

| Table | Columns | FK | Notes |
|-------|---------|-----|-------|
| `cs_country` | `id`, `name`, `sort`, `create_by`, `update_by`, `create_time`, `update_time` | — | Top of the hierarchy. Seeded with `('Узбекистан', 1, 1)` on install. |
| `cs_region` | + `country_id` (default `1`) | `country_id` → `cs_country.id` | Region within a country. |
| `cs_territory` | + `region_id` | `region_id` → `cs_region.id` | Territory within a region. |
| `cs_group` | `id`, `name`, `sort` | — | Free-form grouping. Many-to-many with filials via `cs_filial_group`. |
| `cs_filial_group` | `filial_id`, `group_id` | both | Pivot table. |
| `cs_filial_detail` | `filial_id`, `territory_id`, `alt` | `territory_id` → `cs_territory.id` | Attaches one territory and a display alias to each filial. |

These are pure reference tables — they don't gate anything by themselves, but reports filter by them, and the filial-visibility ACL above scopes through `cs_filial_detail` to derive region / territory aggregates.

## Gotchas

- **The `dealer` connection is not a setting you save — it is a runtime knob.** Confusing the two leads to "I changed the setting and it didn't stick" bug reports. Cross-link: [`/docs/sd-cs/multi-db`](/docs/sd-cs).
- **`cs_user_filial` has no FK to `cs_filial`** — the `filial` table lives in the dealer DB, not the HQ DB. Deleting a filial in the dealer DB leaves dangling `filial_id` values in HQ. The model silently ignores them in `getFilials()`.
- **Two controllers share the `sale` code.** `NewSaleController` and `NewDiscountController` both use `ReportConfigCode = 'sale'` for their saved layouts. They share the same `cs_pivot_config` row pool. A layout saved on one shows up in the other. This is intentional but undocumented — verify before "fixing."
- **Same for `consumption`** — `SkuController` and `ConsumptionController` share the same code.
- **The `okb_config`, `nmedov_categories`, `nmedov_filials` rows are singletons by convention only.** Nothing at the schema level prevents creating a second row with the same `name`/`code` pair; the controllers always `findByAttributes(['name' => ..., 'code' => ...])` which returns the first match. Cleanup migration recommended if duplicates appear.
- **Admin bypass is total.** `AccessManager::hasAccess()` returns true for any operation when `Yii::app()->user->isAdmin()`. There is no way to scope an admin to specific filials — admins always see every active filial via `Filial::getList(... 'active = "Y"')`. To restrict, demote the user to manager and grant individual operations.
- **`role = 1` cannot be assigned through the standard role dropdown.** `User.php` line 36 restricts the `in` range — only existing admins can keep themselves as admins; new admin grants must be done via direct DB edit or by another admin.
- **`session` timeout is 7200 seconds (2 hours).** Long-running cron-style HQ users (e.g. a dashboard left open) will lose session and need to re-pick the dealer. Their saved pivot layouts persist, but the active dealer selection is lost.
- **The `redis_cache` hostname `10.0.0.11` is hardcoded.** On a fresh install the redis container is reachable only at that IP. Editing the IP requires `main.php` redeploy — there is no env-var fallback.
- **`themeManager` defaults to `classic`.** Custom themes ship by adding `themes/<name>/` and changing the top-level `'theme'` key. The change is global — there is no per-tenant theme.
- **`cs_access_user.access` is a TINYINT(1) but treated as a bitmask in some sd-billing-style code paths.** In sd-cs, `AccessManager` reads it strictly as `(int)$model->access` and uses `!empty(...)` — so any non-zero value grants. Avoid setting it to `2` or `4` thinking it means SHOW vs UPDATE; that only works in sd-billing.
- **`PivotConfig.deleteByPk` has no soft-delete.** `actionDeleteReport` hard-deletes the row. Lost saved layouts cannot be restored without DB backups.

## See also

- [`sd-cs` overview](/docs/sd-cs) — the HQ control-plane in detail, including multi-DB mechanics
- [`sd-cs` modules](/docs/sd-cs) — per-module deep dives (`directory`, `pivot`, `report`, `user`, `api`, `api3`)
- [`sd-main` server settings](./sd-main-server-settings.md) — tenant-side settings the HQ aggregator reads from
- [`sd-billing` settings](./sd-billing-settings.md) — vendor-side settings
- [Security / RBAC](/docs/security/rbac) — how `AccessManager` and `cs_access_role` / `cs_access_user` interact across modules
- [Settings catalog index](./index.md)
