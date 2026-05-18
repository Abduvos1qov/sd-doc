---
sidebar_position: 1
title: sd-cs · schema reference
audience: Backend / data engineers, integrators, analysts
summary: Per-column reference for every `cs_*` table that lives on the HQ control-plane connection. Covers user/ACL, geography, plans, notifications, pivot config, telegram, and the audit log. The `d0_*` per-dealer schema is intentionally out of scope and is documented separately under sd-main.
topics: [sd-cs, schema, cs-prefix, hq-control-plane, multi-db, acl, plans]
---

# sd-cs · schema reference (`cs_*`, HQ control plane)

sd-cs runs against **two MySQL connections in parallel** — see [`sd-cs/multi-db`](../../sd-cs/multi-db.md) for the wiring. This page documents the **HQ-owned half only**.

## The two-connection model in one paragraph

`Yii::app()->db` is the HQ connection — a single database, `tablePrefix=cs_`, owned by sd-cs itself. Everything sd-cs writes (users, plans, audit log, pivot configs, region/territory hierarchy) lives here.

`Yii::app()->dealer` is the per-dealer connection — `tablePrefix=d0_`, pointed at one tenant's sd-main database at a time. sd-cs reads from it inside a per-filial loop (`Filial::find().setFilial(prefix)` swaps the dealer DSN) and **never writes** to it (read-only MySQL grants make that explicit at the database layer).

A model belongs to the `cs_` side if and only if it does **not** override `getDbConnection()`. The default `BaseModel::tableName()` returns `{{snake_case_class}}`, which the connection's `tablePrefix` expands. So `class Region extends BaseModel` resolves to `{{region}}` → `cs_region` on the default connection; `class Product extends BaseModel { getDbConnection() { return Yii::app()->dealer; } }` resolves to `{{product}}` → `d0_product` on the dealer connection.

**This page covers the `cs_*` side only.** For the `d0_*` schema (orders, agents, clients, stock, audits, GPS), see [sd-main · Schema reference](../schema-reference.md).

## Headline numbers

| Dimension | Count |
|---|---|
| `cs_*` tables on the HQ connection | 22 |
| Domains | 7 (users/ACL, geo, plans, notifications, telegram, pivot config, audit) |
| Tables with `create_by` / `update_by` / `create_time` / `update_time` audit columns | 14 |
| Foreign-key constraints declared in DDL | 1 (`cs_user_filial.user_id` → `cs_user.id` on delete cascade) |
| Tables logged to `cs_db_log` on every insert/update/delete | All `BaseModel` subclasses with `$writeLog = true` (default) |
| Tables seeded by `protected/migrations/empty.sql` | All 22 |

The cs_ schema is small because **HQ does not duplicate dealer data** — it only stores HQ's own state (who is logged in, which dealer they can see, what plans are set for which filial, what pivot views are saved). All operational data lives on the dealer side.

## Connection layout

```mermaid
flowchart LR
  CSApp[sd-cs PHP app]
  DBCS[(MySQL cs3_*<br/>tablePrefix=cs_)]
  DBDealer[(MySQL b_*<br/>tablePrefix=d0_<br/>read-only)]

  CSApp -- "Yii::app()->db<br/>read + write" --> DBCS
  CSApp -- "Yii::app()->dealer<br/>read only" --> DBDealer

  DBCS -. cs_user_filial.filial_id .-> DBDealer
```

`cs_user_filial.filial_id` is a logical reference to a row in `d0_filial` (in sd-main, the dealer registry) — there is no MySQL FK because the tables sit on different hosts. The reconciliation is purely an application-layer convention.

## Audit columns convention

Every "real" cs_ entity (not pure join tables) carries:

- `create_by INT` — `cs_user.id` of the creator. Stamped in `beforeSave()` when `isNewRecord == true`.
- `update_by INT NULL` — `cs_user.id` of the last editor. Stamped in `beforeSave()` when `isNewRecord == false`.
- `create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` — set by MySQL on insert.
- `update_time DATETIME NULL` — set by the application in `beforeSave()`, NOT by `ON UPDATE`.

A few late-arriving tables use `created_by` / `created_at` / `updated_by` / `updated_at` instead (Laravel-style). Both forms coexist; do not "normalise" without checking each call site.

## Domain 1 — User & ACL

### `cs_user`

The HQ user identity. The same login is mirrored into every dealer DB as `cs3_<login>` in `b_<prefix>.d0_user` so that sd-cs can authenticate against the dealer side too (see `User::beforeSave()` in `protected/modules/user/models/User.php` for the cross-DB sync logic).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `login` | `VARCHAR(100) NOT NULL` | Unique; mirrored as `cs3_<login>` in dealer-side `d0_user` |
| `hash` | `VARCHAR(255) NOT NULL` | Bcrypt via `CPasswordHelper::hashPassword` |
| `name` | `VARCHAR(255) NULL` | Display name |
| `role` | `INT NOT NULL` | `1=admin, 2=manager, 3=operator` (constants on `User` model) |
| `filial_role` | `INT NULL` | The role to assign on the dealer side (`5=operator, 6=kassir, 8=svr, 9=manager`). NULL → default operator |
| `dealer_password` | `VARCHAR(255) NULL` | Plaintext copy of the last set password. Used to re-bind to dealer-side `d0_user` when login changes. Yes, plaintext — see Gotchas |
| `phone` | `VARCHAR(20) NULL` | Used for Telegram bot linking |
| `active` | `TINYINT NOT NULL DEFAULT 1` | Soft-disable |
| `create_by` | `INT NULL` | `cs_user.id`; NULL for the seeded `admin` row |
| `update_by` | `INT NULL` | |
| `create_time` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | |
| `update_time` | `DATETIME NULL` | |
| `visit_time` | `DATETIME NULL` | Last login timestamp |

**Writes:** `user/DefaultController::actionForm` (CRUD), `User::beforeSave()` triggers downstream writes to `b_<prefix>.d0_user` and (for managers) `b_<prefix>.d0_structure_filial`.

**Reads:** every controller that needs the current operator (`Yii::app()->user->id`); `directory/*/controllers/*` for `createBy`/`updateBy` relations; the saved-report tables join on `create_by`.

**Gotcha 1** — `dealer_password` is plaintext. It is the only way to re-push the password to the dealer DB when the user changes their login. Restricting database access to the cs server is the only mitigation.

**Gotcha 2** — `role=1` (admin) is reserved. The `User::rules()` validator only allows non-admin assignments unless the editor is themselves admin.

### `cs_user_filial`

The visibility-ACL anchor. A row binds one HQ user to one dealer (filial). Without a row, that user cannot see that filial's data, period — `BaseModel::getOwnFilials()` filters every per-filial report loop by this table.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `filial_id` | `INT NOT NULL` | Logical FK to `d0_filial.id` (no MySQL FK — different host) |
| `user_id` | `INT NOT NULL` | FK to `cs_user.id`, `ON DELETE CASCADE` |
| `create_by` | `INT NOT NULL` | |
| `create_time` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | |

**Writes:** `directory/DealerController::actionForm` (when granting/revoking dealer access in the HQ UI).

**Reads:** every report. `BaseModel::getOwnModels()` and `BaseModel::getOwnFilials()` (in `protected/components/BaseModel.php`) loop this table on every cross-dealer query.

**Gotcha** — admins bypass this table entirely (`Yii::app()->user->isAdmin()` returns `getFilials()`, not `getOwnFilials()`). Quietly granting admin to a user gives them every dealer.

### `cs_access_user`

Per-user UI permission overrides. Each row is one access flag (named permission like `"report.sales.export"`) granted or denied to one user.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | Permission code |
| `access` | `TINYINT(1) NOT NULL` | `0=deny, 1=allow` |
| `user_id` | `INT NOT NULL` | FK (logical) to `cs_user.id` |
| `create_time` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | |
| `update_time` | `DATETIME NULL` | |

The PHP class is `AccessUser` but its docblock claims `{{access_control}}` — the migration created `cs_access_user`. Model-vs-DDL drift; both names refer to the same table in deployed databases (the migration is authoritative).

### `cs_access_role`

Same shape as `cs_access_user`, keyed by `role` (the integer role code on `cs_user.role`) instead of a specific user.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | Permission code |
| `access` | `TINYINT(1) NOT NULL` | `0=deny, 1=allow` |
| `role` | `INT NOT NULL` | Role code (1, 2, 3) |
| `create_time` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | |
| `update_time` | `DATETIME NULL` | |

Resolution order at runtime: deny first, then allow. `cs_access_user` overrides `cs_access_role`. Admins (`role=1`) skip the check entirely.

### `cs_user_product`

Product-level restriction list per HQ user. If a user has rows here, they only see those products in reports; an empty set means "all products".

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `user_id` | `INT NOT NULL` | FK (logical) to `cs_user.id` |
| `product` | `TEXT NOT NULL` | A single `PRODUCT_ID` value — yes, one row per product, despite the column name |

**Reads:** `UserProduct::findByUser()` and `UserProduct::getUserRestrictions()` are called from the pivot/report controllers to extend the SQL `WHERE` with `PRODUCT_ID IN (...)`. The lookups join across to dealer-side `d0_product`, `d0_product_category`, `d0_product_group`, `d0_adt_brand` to enrich the UI but the filter itself is stored cs-side.

**Gotcha** — the column is named `product` (singular) and the model description still says it stores "product" but the code (`getUserRestrictions`) clearly iterates rows, not items in a list. Treat as one product per row; if you find serialised JSON in there, it is legacy.

## Domain 2 — Geography & filial grouping

### `cs_country`

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | |
| `sort` | `INT NOT NULL DEFAULT 1` | UI ordering |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

Seeded with `Узбекистан` at id `1`. The whole geographic hierarchy is country → region → territory → filial-detail → filial (the last one lives in `d0_filial` on the dealer side).

**Writes:** `directory/CountryController`.

**Reads:** any cross-dealer report that filters by country (via `BaseModel::setCountry($id)`, which then filters `getOwnModels()` by `region.country_id`).

### `cs_region`

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | |
| `sort` | `INT NOT NULL DEFAULT 1` | |
| `country_id` | `INT NOT NULL DEFAULT 1` | FK (logical) to `cs_country.id`. Added by a follow-up `ALTER` in `empty.sql` line 145 |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** `directory/RegionController`.

**Reads:** filter cascade in every cross-dealer pivot.

### `cs_territory`

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | |
| `sort` | `INT NOT NULL DEFAULT 1` | |
| `region_id` | `INT NOT NULL` | FK (logical) to `cs_region.id` |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** `directory/TerritoryController`. Cannot delete if `cs_filial_detail` rows depend on it (`Territory::dependences = ['filialDetails']`).

### `cs_filial_detail`

Extra HQ-side attributes for a dealer/filial that do NOT belong on the dealer side (because they describe HQ's view of the filial, not the filial's view of itself).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `alt` | `VARCHAR(255) NULL` | Alternative/short name for HQ reports |
| `filial_id` | `INT NOT NULL` | Logical FK to `d0_filial.id`. Unique — one detail row per filial |
| `territory_id` | `INT NULL` | FK (logical) to `cs_territory.id` |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** `directory/DealerController::actionForm` (the same UI that grants user/filial access).

**Reads:** geography rollups; `BaseModel::getOwnModels()` joins this in when filtering by `country_id`.

### `cs_group`

A free-form filial grouping label. Think "TOP10 dealers", "Beverage division", "Pilot dealers".

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(100) NOT NULL` | |
| `sort` | `TINYINT NOT NULL DEFAULT 1` | |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

Cannot delete a group while `cs_filial_group` references it (`Group::dependences = ['dealers']`).

### `cs_filial_group`

Many-to-many join between `cs_group` and `d0_filial` (logical).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `filial_id` | `INT NOT NULL` | Logical FK to `d0_filial.id` |
| `group_id` | `INT NOT NULL` | FK to `cs_group.id` |

No audit columns — pure link table. The model docblock incorrectly references `{{group}}`; the table is `cs_filial_group`.

## Domain 3 — Plans & targets

### `cs_plan`

A monthly summary plan for one filial: total target in summa/volume/count units, optionally split into categories via `cs_plan_category`.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `date` | `DATE NOT NULL` | First day of the planned month |
| `summary` | `FLOAT NOT NULL` | The headline number |
| `filial_id` | `INT NOT NULL` | Logical FK to `d0_filial.id` |
| `unit` | `TINYINT NOT NULL` | `1=summa (money), 2=volume, 3=count`. Constants on `Plan::UNIT_*` |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** `directory/PlanController`.

**Reads:** every plan-vs-actual report in `pivot/*`. The actual is pulled from `d0_order` / `d0_order_detail` per filial; cs joins them in PHP.

### `cs_plan_category`

A category-level breakdown of one `cs_plan`.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `plan_id` | `INT NOT NULL` | FK to `cs_plan.id` |
| `product_category_id` | `VARCHAR(60) NOT NULL` | Logical FK to `d0_product_category.PRODUCT_CAT_ID` |
| `value` | `FLOAT NOT NULL` | Target value in the plan's `unit` |

No audit columns. Cascading delete is application-level (`Plan` relation `categories`).

### `cs_plan_product`

A product-level breakdown — flatter than `cs_plan_category`, used by the product-plan UI.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `date` | `DATE NOT NULL` | First day of planned period |
| `product_id` | `VARCHAR(11) NOT NULL` | Logical FK to `d0_product.PRODUCT_ID` |
| `product_cat_id` | `VARCHAR(11) NOT NULL` | Logical FK to `d0_product_category.PRODUCT_CAT_ID` |
| `filial_id` | `INT NOT NULL` | Logical FK to `d0_filial.id` |
| `region_id` | `VARCHAR(60) NOT NULL` | Logical FK to `cs_region.id` (stored as string for legacy reasons) |
| `brand_id` | `VARCHAR(60) NOT NULL` | Logical FK to `d0_adt_brand.ID` |
| `unit` | `TINYINT(11) NOT NULL` | Same encoding as `cs_plan.unit` |
| `value` | `FLOAT NOT NULL` | |
| `created_at` | `DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP` | Laravel-style audit |
| `created_by` | `VARCHAR(60) DEFAULT '0'` | |
| `updated_at` | `DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP` | |
| `updated_by` | `VARCHAR(60) NOT NULL DEFAULT '0'` | |

**Writes:** `directory/PlanProductController`.

**Gotcha** — note the audit columns are `created_*` / `updated_*` here, not `create_*` / `update_*` like everywhere else. The model's `beforeSave` writes to `created_by` / `updated_at` / `updated_by` — easy to miss if you copy from another model.

## Domain 4 — Notifications

### `cs_notification`

Push-style notifications HQ broadcasts to selected dealers and selected dealer-side roles. The dealer-side `sd-main` polls `/api/notifications` to pull these in.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT(11) AI PK` | |
| `title` | `VARCHAR(200) NOT NULL` | |
| `type` | `TINYINT(2) NOT NULL` | `1=Новости, 2=Уведомление, 3=Предупреждение` |
| `preview` | `VARCHAR(255) NOT NULL` | Short body shown in the list |
| `detail` | `TEXT NULL` | Full HTML body |
| `status` | `TINYINT(2) NOT NULL DEFAULT 1` | `1=new, 2=in process, 3=sent` |
| `dealer_ids` | `TEXT NULL` | Semicolon-separated `d0_filial.id` list. Empty means all dealers |
| `roles` | `VARCHAR(200) NULL` | Semicolon-separated dealer-side role codes |
| `auto` | `TINYINT(2) NOT NULL DEFAULT 0` | `1` = auto-generated by a job, not a human |
| `is_deleted` | `TINYINT(2) NOT NULL DEFAULT 0` | Soft-delete |
| `created_by` | `INT(11) NOT NULL` | FK to `cs_user.id` |
| `updated_by` | `INT(11) NULL` | |
| `created_at` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` | |
| `updated_at` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | |

**Writes:** `directory/NotificationController`.

**Reads:** the dealer-poll endpoint in `api/*` and the moderation UI.

**Gotcha** — `created_at` has `ON UPDATE CURRENT_TIMESTAMP`. That means every update bumps `created_at` too. Audit reports that assume `created_at` is immutable will be wrong.

## Domain 5 — Telegram integration

Three small tables drive a Telegram reporting bot that posts daily/weekly summary reports to a group chat per HQ user.

### `cs_telegram_bot`

The bot itself — token, type, username.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | Internal label |
| `token` | `VARCHAR(255) NOT NULL` | Telegram bot token. Secret |
| `type` | `TINYINT NOT NULL DEFAULT 1 UNIQUE` | Currently only `1=report` |
| `username` | `VARCHAR(255) NOT NULL` | The bot's `@handle` |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** `directory/TelegramBotController`. `TelegramBot::beforeSave` calls `setWebhook` on Telegram's API on every save (via `bilolpro.uz/webhook.php` proxy, see `TelegramBot::beforeSave`).

**Gotcha** — `type` is unique. There is one bot per type, ever. The `TYPE_REPORT=1` constant is the only one defined; expanding requires extending the enum and the unique index.

### `cs_telegram_bot_user`

Binds an HQ user to a Telegram chat.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `telegram_bot_id` | `INT NOT NULL` | FK to `cs_telegram_bot.id` |
| `user_id` | `INT NOT NULL` | FK to `cs_user.id` |
| `chat_id` | `INT NOT NULL` | Telegram chat id |

**Writes:** the Telegram webhook handler (`api/TelegramReportController`), invoked on first `/start` from the user. Also cleaned up by `User::beforeSave` when the user's `phone` changes.

### `cs_telegram_bot_config`

Per-user per-report configuration. Key/value pairs used by the bot to remember settings ("which dealer to include", "which language", etc.).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `user_id` | `INT NOT NULL` | FK to `cs_user.id` |
| `report_id` | `TINYINT NOT NULL` | The report-type code |
| `name` | `VARCHAR(50)` | Setting name |
| `value` | `VARCHAR(50)` | Setting value |

Accessed via `TelegramBotConfig::getConfig($user_id, $report_id)` which returns a `ConfigHelper` proxy with magic `__get`/`__set` — every set writes a row immediately. **Gotcha** — there is no compound unique index, so setting the same `(user_id, report_id, name)` twice writes a second row; reads pick whichever the helper saw last.

### `cs_telegram_group`

A Telegram group/channel target (for system log streams, not report subscriptions).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(255) NOT NULL` | |
| `chat_id` | `INT NOT NULL` | The group's chat id |
| `type` | `TINYINT NOT NULL` | `1=log` (only defined value) |
| `create_by`, `update_by`, `create_at`, `update_at` | audit columns (note `_at`, not `_time`) | |

Used by `TelegramBot::sendProductRestrictionUpdateLog` to publish admin actions to a shared moderation channel.

## Domain 6 — Pivot configuration

### `cs_pivot_config`

A saved set of filters/columns/rollups for one of the cs-side pivot reports. The `code` field selects which report (e.g. `sale`, `defect`, `purchase`, `transactions`, `rfm`).

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `name` | `VARCHAR(100) NOT NULL` | User-facing label |
| `code` | `VARCHAR(100) NOT NULL` | Report code — matches the pivot controller's id |
| `config` | `TEXT NOT NULL` | JSON-serialised pivot definition (rows, cols, filters, measures). Originally `VARCHAR(1000)`, widened to `TEXT` in a follow-up `ALTER` |
| `create_by`, `update_by`, `create_time`, `update_time` | audit columns | |

**Writes:** every pivot controller's "save view" action under `pivot/*`.

**Reads:** `PivotConfig::getReports($code)` returns the list of saved views, decoding `config` as JSON. The pivot controller then re-runs the underlying SQL with the saved filters.

**Gotcha** — `config` is HTML-purified on save (`CHtmlPurifier`), which can strip JSON that includes `<` characters in string values. If a saved view loses filters mysteriously, that's why.

## Domain 7 — Audit log

### `cs_db_log`

Every insert/update/delete on any `cs_*` table (via a `BaseModel` subclass) appends one row **per changed attribute** here. Per-column granularity is intentional — the log doubles as a diff history.

| Column | Type | Notes |
|---|---|---|
| `id` | `INT AI PK` | |
| `model` | `VARCHAR(100) NOT NULL` | PHP class name (e.g. `Plan`, `UserFilial`) |
| `action` | `VARCHAR(50) NOT NULL` | `insert`, `update`, or `delete` |
| `attribute` | `VARCHAR(100) NOT NULL` | Column that changed |
| `old_value` | `VARCHAR(500) NULL` | Previous value (NULL for `insert`) |
| `new_value` | `VARCHAR(500) NULL` | New value (NULL for `delete`) |
| `pk` | `VARCHAR(100) NULL` | Primary key of the affected row (composite keys joined with `,`) |
| `user_id` | `INT NULL` | `cs_user.id`, NULL for guests |
| `ip` | `VARCHAR(20) NULL` | `$_SERVER['REMOTE_ADDR']` |
| `user_agent` | `VARCHAR(500) NULL` | |
| `date` | `TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP` | When the change was recorded |
| `request_url` | `VARCHAR(500) NULL` | Host + URI of the request that triggered it |

Indexes (added later): `model`, `action`, `date`. Search by `model + date` is the canonical query.

**Writes:** `DbLog::log($model, $action, $oldValues)` from `BaseModel::afterSave` / `afterDelete`. Skipped for models with `$writeLog = false` (only `DbLog` itself has this set).

**Reads:** `report/LogController` powers the audit-trail report. The "what changed and by whom" UI under `/report/log`.

**Gotcha 1** — values are truncated to 500 characters. Long `config` JSONs in `cs_pivot_config` lose the tail in the log.

**Gotcha 2** — the model uses `{{log}}` in its docblock but the migration created `cs_db_log`. Yii resolves `{{log}}` against the cs prefix and falls back to whatever exists at runtime — in deployed databases the table is `cs_db_log` and that's what gets logged to. Model-vs-DDL drift again; the migration is authoritative.

## Domain 8 — Vestigial / external models

The cs source tree contains a handful of `BaseModel` subclasses that look like cs models but in fact reference dealer-side tables or are not in active use:

| Class | Maps to | Actual home | Why it's here |
|---|---|---|---|
| `Client` | `{{client}}` | `d0_client` (dealer) | No `getDbConnection` override — but in practice the model is only instantiated under the dealer connection by the surrounding controller. Treat as a typo, not as a `cs_client` table. There is no `cs_client` in the cs schema |
| `WorkingDays` | `{{working_days}}` | `d0_working_days` (dealer) | Same — uppercase column names give it away. No corresponding `cs_working_days` |
| `LoginForm` | (no table) | — | A `CFormModel` wrapper. Not an `ActiveRecord` |
| `UserProduct` | `{{user_product}}` | `cs_user_product` | Real cs table, covered above |

If you grep for "all sd-cs models without `getDbConnection` override and assume they map to cs_*", you'll get these three false positives. Cross-check against `protected/migrations/empty.sql` — that is the authoritative cs_* table list.

## Access patterns at a glance

This table summarises who writes and who reads each cs_ table. "report loop" means the per-filial loop in `pivot/*` and `report/*` controllers that swaps `Yii::app()->dealer`'s DSN per dealer and merges results in PHP.

| Table | Written by | Read by |
|---|---|---|
| `cs_user` | `user/DefaultController` | Every controller (`Yii::app()->user`); audit join targets |
| `cs_user_filial` | `directory/DealerController` | `BaseModel::getOwnFilials` (every report loop) |
| `cs_access_user` | `user/AccessController` | Auth filter on every controller action |
| `cs_access_role` | `user/AccessController` | Same |
| `cs_user_product` | `user/DefaultController` (product-restriction UI) | All pivot/report SQL builders |
| `cs_country` | `directory/CountryController` | Geo rollups, `BaseModel::setCountry` filter |
| `cs_region` | `directory/RegionController` | Geo rollups; FK target of `cs_territory` and `cs_plan_product` |
| `cs_territory` | `directory/TerritoryController` | Geo rollups; FK target of `cs_filial_detail` |
| `cs_filial_detail` | `directory/DealerController` | Geo rollups; territory-by-filial joins |
| `cs_group` | `directory/GroupController` | Group-by-dealer rollups in pivots |
| `cs_filial_group` | `directory/GroupController` | Same |
| `cs_plan` | `directory/PlanController` | Plan-vs-actual reports |
| `cs_plan_category` | `directory/PlanController` (cascading insert via `Plan` relation) | Plan-vs-actual at category level |
| `cs_plan_product` | `directory/PlanProductController` | Plan-vs-actual at product level |
| `cs_notification` | `directory/NotificationController` | Dealer-poll endpoint in `api/*` |
| `cs_telegram_bot` | `directory/TelegramBotController` | `TelegramBot::sendProductRestrictionUpdateLog`, report-bot worker |
| `cs_telegram_bot_user` | `api/TelegramReportController` (webhook on `/start`) | Report-bot worker (whom to send to) |
| `cs_telegram_bot_config` | Magic-setter on `ConfigHelper` in `TelegramBotConfig` | Report-bot worker (config lookup) |
| `cs_telegram_group` | `directory/TelegramGroupController` | `TelegramBot::sendProductRestrictionUpdateLog` |
| `cs_pivot_config` | every controller under `pivot/*` (save-view) | Same controllers (load-view) |
| `cs_db_log` | `BaseModel::afterSave` and `afterDelete` for every cs_ model | `report/LogController` (audit UI) |

## Cross-project touchpoints

`cs_user_filial` is the load-bearing piece that makes "who-can-see-which-dealer" work. It carries one half of the relation (the HQ user). The other half is in **sd-main's `d0_filial`** (the dealer registry that lives in a separate "billing" DB called `b_*`). The application joins them in PHP, never in SQL.

`cs_filial_detail.filial_id` similarly mirrors `d0_filial.id`. Adding a new dealer means inserting into `d0_filial` (via sd-main / sd-billing) AND into `cs_filial_detail` (via sd-cs Dealers UI). Forgetting the second insert leaves the dealer invisible from HQ.

`cs_plan.filial_id`, `cs_plan_product.filial_id`, `cs_notification.dealer_ids` all carry logical references into `d0_filial.id`. The lack of database-level FK means deleting a dealer from `d0_filial` orphans these rows silently. The cleanup is manual.

`cs_user.login` is mirrored as `cs3_<login>` into every dealer's `d0_user`. `User::beforeSave` performs the cross-DB sync. If the cs row's login changes, every dealer-side mirror gets renamed too — and `cs_user.dealer_password` is the only way to reconstruct the bcrypt hash on the dealer side, hence the plaintext storage.

`User::setFilialRole` writes into the dealer-side `b_<prefix>.authassignment` table (not `d0_authassignment` — there is no `d0_` prefix on the Yii RBAC tables because they pre-date the prefix convention). That coupling is the reason an HQ-side role change has to also be re-applied to every dealer.

## Schema-drift gotchas

A list of things that look wrong but are intentional, or are wrong but irreparable:

1. **`AccessUser` / `AccessRole` reference `{{access_control}}` in their docblocks**, but the migration creates `cs_access_user` and `cs_access_role`. The docblocks are stale. The DDL is authoritative.

2. **`DbLog` references `{{log}}`** in its docblock, but the migration creates `cs_db_log`. Same story — the DDL wins.

3. **`FilialGroup` references `{{group}}`** in its docblock (copy-paste from `Group`). The actual table is `cs_filial_group`. Same story.

4. **`cs_notification` uses `created_at` / `updated_at` / `created_by` / `updated_by`** instead of the cs convention's `create_time` / `update_time` / `create_by` / `update_by`. Both naming styles coexist; do not normalise.

5. **`cs_plan_product` uses `created_at` / `created_by` / `updated_at` / `updated_by`** for the same reason. Its `beforeSave` writes `created_by` and `updated_*` only — `created_at` is set by MySQL.

6. **`cs_notification.created_at` has `ON UPDATE CURRENT_TIMESTAMP`** — meaning it mutates on update. Treat it as "last-touched", not "created".

7. **`cs_user.dealer_password` stores plaintext**. The only mitigation is DB-host isolation. Restrict the cs DB user to the cs host only and you are roughly as safe as you'd be with hashed passwords plus a side channel.

8. **`cs_telegram_bot_config` lacks a unique key** on `(user_id, report_id, name)`. The `ConfigHelper` magic setter writes a new row every time the same setting is set; reads pick the last one indexed.

9. **`cs_pivot_config.config` is HTML-purified on save**. Pivot definitions containing the literal characters `<` or `<script>` substrings (rare but possible in product names) are silently corrupted.

10. **There is exactly one foreign-key constraint in the cs DDL** (`cs_user_filial.user_id → cs_user.id`). Every other relationship is application-managed, including the cross-DB ones — there is no MySQL guarantee that `cs_plan.filial_id` resolves to a live dealer.

11. **`cs_db_log.old_value` and `new_value` are `VARCHAR(500)`**. JSON columns, long config strings, and big text fields get truncated in the audit log. The truncation is silent.

12. **The seeded `admin` user (`cs_user.id=1`) has `role=1`** which is the only role the validator refuses to assign through the UI. The only way to get a second admin is via direct SQL or by an existing admin editing themselves.

## Sizing & growth profile

- `cs_db_log` is the only table that grows continuously. In a busy installation it can dwarf the rest of the schema combined. There is no built-in pruning — operationally this is rotated by an external `DELETE FROM cs_db_log WHERE date < ...` job.
- `cs_pivot_config` rows are small (one row per saved report view) but `config` blobs can be tens of KB.
- Every other table is bounded — at most a few hundred rows of HQ-managed state.
- The cs schema is **deliberately small**: HQ's "system of record" stance is to own only the HQ-side state and to read everything else from the dealer DBs. Adding new tables to cs is rare and is usually a sign that the same data should have lived on the dealer side.

## See also

- [`sd-cs/multi-db`](../../sd-cs/multi-db.md) — how the two connections are wired
- [`sd-cs/data-schemes`](../../sd-cs/data-schemes.md) — the high-level overview that this page replaces for column-level detail
- [`sd-cs/sd-main-integration`](../../sd-cs/sd-main-integration.md) — how cs reads from the dealer connection
- [sd-main · Schema reference](../schema-reference.md) — the `d0_*` columns (everything not on this page)
- [sd-main · Core ERD](../erd.md) — the dealer-side relationships
- [`sd-cs/architecture`](../../sd-cs/architecture.md) — controllers, modules, the per-filial loop
- [RBAC matrix](../../security/rbac-matrix.md) — how `cs_access_user` / `cs_access_role` resolve at runtime
