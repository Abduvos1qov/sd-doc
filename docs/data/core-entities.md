---
sidebar_position: 3
title: Core entities
audience: Backend engineers, QA, Data engineers, Integrators, BI / reporting team
summary: Per-table deep reference for the 30 most-important sd-main tables. Each section covers the model file, table name, primary key, key foreign-key relations, columns with type and purpose, indexes, and which controllers / cron jobs write and read the row. Use this together with `schema-reference.md` (DB-wide stats + 306-model index) as the single source of truth for the data layer.
topics: [schema, models, tables, columns, foreign-keys, indexes, sd-main, base-filial, multi-tenant]
---

# Core entities

This page is the **per-table deep dive** for the 30 most-loaded tables in
sd-main. Open `docs/data/schema-reference.md` first if you need the
DB-wide picture (counts, engine / charset distribution, full
306-model index). This page goes deeper for the 30 tables that show up
in every report, every sync request, and every period close.

## How to read this page

Each H2 section follows the same shape:

- **Source line** — model file path, the `tableName()` / `filialTable()`
  value, primary key.
- **Columns** — every column documented in the `@property` docblock,
  cross-checked against the live MySQL schema. Type column shows the
  PHP type; the live DB type is added in parentheses where it adds
  information (e.g. `int (TINYINT)`, `string (varchar 32)`).
- **Indexes** — non-trivial indexes from the live schema, when the
  table has any. Single-column PK indexes are omitted.
- **Relationships** — what the model's `relations()` declares plus
  any back-references from other models that matter at read time.
- **Read / write surface** — which controllers, actions, cron jobs,
  and APIs write to the row, and which reports / endpoints read it.
- **Gotchas** — subtle behaviour, deprecated columns, soft-delete vs
  hard-delete, double-bookkeeping pairs, etc. Read these before
  touching the table.

## `BaseFilial` and the per-filial table prefix

The base class `BaseFilial` (in `protected/models/BaseFilial.php`) is
the per-tenant subdivision mechanic. A model that extends `BaseFilial`
declares its logical table name through `filialTable()` (e.g.
`return '{{order}}'`). At runtime `tableName()` rewrites the placeholder
into `d0_fN_order` where `fN` is the active filial prefix returned by
`FilialComponent::getFilialPrefix()`. The `f0_` prefix represents the
shared / root filial — most master-data tables live there.

A model that extends `CActiveRecord` directly (e.g. `Product`,
`PriceType`, `Filial`, `Bonus`, `Skidka`) is **filial-shared** — there
is exactly one row across the whole tenant.

The `BaseFilial::isCommon` flag lets a per-filial model bypass the
rewrite for queries that should hit only the root filial. Read
`BaseFilial::allTables()` if you need to enumerate every per-filial
copy of a table (used by the period-close engine and by cross-filial
reports).

`{{tableName}}` syntax (the Yii table placeholder) is processed by
the Yii DB layer to inject the configured table prefix (`d0_`). For
a `BaseFilial` model the placeholder also gets the filial prefix
injected by `BaseFilial::getFilialTable()`.

---

## `Order`

Source: `protected/models/Order.php`. Extends `BaseFilial`. `filialTable()`
returns `{{order}}`, resolves to `d0_fN_order`. Primary key `ORDER_ID`
(varchar UUID-like). Live DB: 59 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ORDER_ID` | string | PK. UUID-like, also used as cross-filial sync ID. |
| `DILER_ID` | string | Tenant subdivision (legacy "dealer"); see `Diler` model. |
| `CLIENT_ID` | string | FK to `Client.CLIENT_ID`. |
| `AGENT_ID` | string | FK to `Agent.AGENT_ID`. NULL for web / B2B-portal orders. |
| `CLIENT_CAT` | string | Denormalised client category at submit time. |
| `CITY_ID` | string | FK to `City`. |
| `PRICE_TYPE` | string | FK to `PriceType.PRICE_TYPE_ID`. Locks the price list at submit time. |
| `OLD_PRICE_TYPE` | string | Pre-migration price-list ID; legacy. |
| `COUNT` | float | Sum of `OrderDetail.COUNT` (units delivered). |
| `SUMMA` | float | Total after discount, in `CURRENCY`. |
| `DISCOUNT` | float | Sum of `OrderDetail.DISCOUNT` for the order. |
| `DATE` | datetime | Submitted-at. Set on first save, never overwritten. |
| `STATUS` | int (TINYINT) | Macro state: 1 New, 2 Loaded, 3 Delivered, 4 Returned, 5 Cancelled, 6 Editing, 7 New (second-sale variant). |
| `SUB_STATUS` | int | Fine-grained UI step inside `STATUS`. |
| `DOB_STATUS` | string | Warehouse picking sub-status: NULL not started, `picking`, `picked`. Independent of `STATUS`. |
| `DATE_LOAD` | datetime | When the order was loaded onto a trip. |
| `DATE_DELIVERED` | datetime | When the expeditor confirmed delivery. |
| `DATE_CANCEL` | datetime | When `STATUS=5`. |
| `DATE_STATUS` | datetime | Last status transition; used for SLA tracking. |
| `DEBT` | float | Outstanding receivable; mirrored from `ClientTransaction` net. |
| `REPLACE_ID` | string | If non-empty, this order replaces another order. |
| `DEFECT_ID` | string | If non-empty, defect-return parent of this order. |
| `BONUS_ORDER_ID` | string | FK to `BonusOrder` (auto-generated promo line). |
| `BONUS_TYPE` | string | `-1` auto bonus, `-2` skip bonus, `d0_*` manual bonus ID. |
| `TIMESTAMP_X` | datetime | Last DB-side write; trigger-managed. |
| `COMMENT` | string | Agent free-text. |
| `ID` | int | Surrogate auto-increment for sync ordering only. NOT a PK. |
| `TRADE_ID` | int | FK to `TradeDirection`. |
| `ACTIVE` | char(1) | `Y` active, `N` soft-deleted. Hard delete is rare. |
| `SYNC` | string | Sync ledger flag for mobile clients. |
| `TIME` | int | Mobile-client clock at submit (epoch). |
| `VOLUME` | float | Cubic m3 (for trip planning). |
| `SKIDKA` | int | Snapshot of discount mode at submit time. |
| `CURRENCY` | string | FK to `Currency.CURRENCY_ID`. |
| `CURRENCY_SYMBOL` | string | Denormalised display symbol. |
| `UNIT` | string | FK to `Unit.UNIT_ID` (base UOM). |
| `UNIT_SYMBOL` | string | Denormalised UOM symbol. |
| `EXPEDITOR` | string | Assigned `Expeditor.EXPEDITOR_ID`. NULL until trip assignment. |
| `TYPE` | string | 1 Order, 2 Shelf-return, 3 Exchange. |
| `CONTRACT_ID` | string | FK to `ContractClient.ID` if a contract is active. |
| `COMMENT_2` | string | Internal manager comment. |
| `CONSIGNMENT` | string | Consignment ref (legacy 1C integration). |
| `CONSIG_DATE` | datetime | Consignment date. |
| `XML_ID` | string | External 1C / ERP ID. |
| `REAL_ID` | string | Mobile-client local ID before server reconciliation. |
| `STORE_ID` | string | Source warehouse `Store.STORE_ID`. |
| `DEFECT` | string | Defect-flag column (legacy). |
| `CREATE_BY` / `CREATE_AT` | string / datetime | Audit. |
| `UPDATE_BY` / `UPDATE_AT` | string / datetime | Audit. |
| `SOURCE` | string | mobile / web / online / import. |
| `STOCKMAN_ID` | string | Picker `User.USER_ID`. |
| `CISES_STATUS` | int | Markirovka (Honest Sign) state for the order's CIS codes. |

### Indexes

`d0_order` is the busiest read table in sd-main. The live schema
declares non-unique indexes on `CLIENT_ID`, `AGENT_ID`, `DATE`,
`STATUS`, `STORE_ID`, `EXPEDITOR`, `XML_ID`, plus the PK on `ORDER_ID`.

### Relationships

| Name | Type | Target |
|------|------|--------|
| `Diler` | BELONGS_TO | `Diler` on `DILER_ID` |
| `Client` | BELONGS_TO | `Client` on `CLIENT_ID` |
| `Agent` | HAS_ONE | `Agent` on `AGENT_ID` |
| `City` | HAS_ONE | `City` on `CITY_ID` |
| `Unit` | HAS_ONE | `Unit` on `UNIT` to `UNIT_ID` |
| `Currency` | HAS_ONE | `Currency` on `CURRENCY` to `CURRENCY_ID` |
| `PriceType` | HAS_ONE | `PriceType` on `PRICE_TYPE` to `PRICE_TYPE_ID` |
| `Visit` | HAS_ONE | `Visiting` on `DILER_ID` |
| `Debt` | HAS_ONE | `DebtFinans` on `ORDER_ID` |
| `OrderDetail` | HAS_MANY | `OrderDetail` on `ORDER_ID` |
| `Contragent` | BELONGS_TO | conditional, only when `ServerSettings::isContragent()` |

### Read / write surface

Writes: `OrderController::actionSave`, mobile API v1 / v2 / v3 (agent
submit, expeditor confirm), warehouse picking module, defect-return
flow (`OrderDefectController`), bonus engine
(`BonusComponent::generate` produces auto-bonus child orders), 1C
import job. Reads: every report dashboard, `OrdersReport`, the period
close engine, `Trip` planner, KPI engine, `OutletFact` aggregator.

### Gotchas

- `ORDER_ID` is generated client-side as a GUID; mobile submits with
  `REAL_ID` so the server can map after offline-write reconciliation.
- `STATUS=3` (Delivered) does NOT automatically pay the order. The
  finans ledger needs a separate `ClientTransaction` (write
  `TRANS_TYPE = order`) — see the order finans payment lifecycle in
  `docs/concepts/order-lifecycle.md`.
- `BONUS_TYPE` is overloaded: `-1` means auto-bonus generated by the
  engine, `-2` means skip bonus, any other value is the `BONUS_ID` of
  the manual bonus that was selected.
- `DOB_STATUS` ('picking', 'picked') is **independent** of `STATUS`. A
  row can be `STATUS=1 New` and `DOB_STATUS=picked` if the warehouse
  picked before the manager approved.
- Soft delete uses `ACTIVE='N'`; downstream reports must filter by
  `ACTIVE='Y'`.

---

## `OrderDetail`

Source: `protected/models/OrderDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_detail}}`, resolves to
`d0_fN_order_detail`. Primary key `ORDER_DET_ID`. Live DB: 29 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ORDER_DET_ID` | string | PK (UUID-like). |
| `ORDER_ID` | string | FK to `Order.ORDER_ID`. |
| `DILER_ID` | string | Tenant subdivision. |
| `CLIENT_ID` | string | Denormalised from parent order. |
| `CLIENT_CAT` | string | Denormalised from `Client.CLIENT_CAT`. |
| `CITY_ID` | string | Denormalised from parent. |
| `STORE_ID` | string | Source warehouse for this line. |
| `PRODUCT_CAT` | string | FK to `ProductCategory`. |
| `PRODUCT` | string | FK to `Product.PRODUCT_ID`. |
| `COUNT` | float | Units ordered. |
| `PRICE` | float | Unit price at submit time in `CURRENCY`. |
| `SUMMA` | float | `COUNT * PRICE - DISCOUNT`. |
| `DISCOUNT` | float | Line-level discount applied. |
| `DISCOUNT_ID` | string | FK to `Skidka` rule that produced the discount. |
| `SKIDKA_MANUAL_ID` | string | FK to `SkidkaManual` if a manager-override discount was applied. |
| `VOLUME` | float | Cubic m3 for the line. |
| `CURRENCY` | string | Currency of `PRICE`. |
| `CURRENCY_SYMBOL` | string | Denormalised. |
| `UNIT` | string | UOM at line level. |
| `UNIT_SYMBOL` | string | UOM display symbol. |
| `DEFECT` | float | Count of units rejected on delivery (used by defect-return flow). |
| `COMMENT` | string | Free-text. |
| `ID` | int | Surrogate auto-increment. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `SYNC` | string | Sync ledger. |
| `TIMESTAMP_X` | datetime | Trigger-managed. |
| `CREATE_BY` / `UPDATE_BY` | string | Audit user. |

### Relationships

| Name | Type | Target |
|------|------|--------|
| `Order` | BELONGS_TO | `Order` on `ORDER_ID` |
| `Product` | BELONGS_TO | `Product` on `PRODUCT` to `PRODUCT_ID` |
| `Unit` | HAS_ONE | `Unit` on `UNIT` to `UNIT_ID` |
| `Currency` | HAS_ONE | `Currency` on `CURRENCY` to `CURRENCY_ID` |

### Read / write surface

Writes: same controllers as `Order` — every order write fans out to a
batch insert / update on `OrderDetail`. Reads: sales-by-product
reports, the AKB calculator, bonus engine (input set), defect-return
flow (matches `DEFECT > 0` lines).

### Gotchas

- The `DEFECT` column is on the **line**, not on the order. To compute
  total defect for an order, sum `OrderDetail.DEFECT * PRICE`.
- The order-line audit trail is in `OrderDetailHistory` (28 columns) —
  any non-cosmetic edit creates a history row keyed by `ORDER_DET_ID`.
- `STORE_ID` on the line can differ from the order's `STORE_ID` when
  multi-store picking is enabled (rare; controlled by server setting).

---

## `OrderHistory`

Source: `protected/models/OrderHistory.php`. Extends `BaseFilial`.
`filialTable()` returns `{{order_history}}`, resolves to
`d0_fN_order_history`. Primary key `ID` (auto-increment). Live DB: 38 columns.

### Columns

Mirrors the bulk of `Order` columns (`ORDER_ID`, `DILER_ID`,
`CLIENT_ID`, `AGENT_ID`, `CLIENT_CAT`, `CITY_ID`, `PRICE_TYPE`,
`COUNT`, `SUMMA`, `DATE`, `STATUS`, `DATE_LOAD`, `DATE_DELIVERED`,
`DATE_CANCEL`, `DATE_STATUS`, `DEBT`, `TIMESTAMP_X`, `COMMENT`,
`ACTIVE`, `SYNC`, `TIME`, `VOLUME`, `CURRENCY`, `CURRENCY_SYMBOL`,
`UNIT`, `UNIT_SYMBOL`, `DISCOUNT`, `EXPEDITOR`, `TYPE`, `CONSIGNMENT`,
`CONSIG_DATE`, `DEFECT`, `XML_ID`, `CREATE_BY`, `UPDATE_BY`,
`CREATE_AT`, `UPDATE_AT`). Adds `ID` auto-increment PK and links every
row back to the live `Order` via `ORDER_ID`.

### Read / write surface

Writes: `Order::afterSave()` snapshots the row into `OrderHistory` on
every transition. Reads: the order-history UI, audit reports, the
"who-changed-what-when" view used by support.

### Gotchas

- This is an **append-only** log. Edits or deletes are not allowed
  outside DB maintenance.
- `OrderDetailHistory` (sister table) plays the same role for line
  changes.
- The history row is keyed by autoincrement `ID`, not by `ORDER_ID`,
  so a single order can have dozens of rows.

---

## `Client`

Source: `protected/models/Client.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client}}`, resolves to `d0_fN_client`.
Primary key `CLIENT_ID`. Live DB: 58 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `CLIENT_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant subdivision. |
| `TEL` | string | Primary phone (multiple phones live in `ClientPhones`). |
| `FIRM_NAME` | string | Legal name. |
| `NAME` | string | Display name. |
| `ADRESS` | string | Free-text address (note legacy spelling). |
| `CLIENT_CAT` | string | FK to `ClientCategory.CLIENT_CAT_ID`. |
| `ORIENT` | string | Landmark for navigation. |
| `REGION` | string | FK to `Region`. |
| `CITY` | string | FK to `City.CITY_ID`. |
| `CONTACT_PERSON` | string | Free-text. |
| `FORM_SOB` | string | Ownership form code. |
| `BALANS` | float | Cached running balance — recomputed nightly from `ClientTransaction`. |
| `PRICE_TYPE_ID` | string | FK to `PriceType`. Default price list. |
| `BONUS_ID` | string | FK to `Bonus`. Active bonus program. |
| `DISCOUNT_ID` | string | FK to `Skidka`. Active discount rule. |
| `DATE_EXP` | datetime | Last expedition / delivery date — refreshed by the trip flow. |
| `LON`, `LAT` | float | Geo for geofencing during agent visit. |
| `ALLOW_CONSIG` | int | 1 if consignment sales allowed. |
| `ALLOW_KREDIT` | int | 1 if credit sales allowed. |
| `XML_ID` | string | External 1C / ERP ID. |
| `BAR_CODE` | string | Loyalty barcode. |
| `EXPEDITOR` | string | Default `Expeditor.EXPEDITOR_ID`. |
| `PHOTO` | string | URL to outlet photo. |
| `ACCOUNT`, `BANK`, `MFO`, `OKED` | string | Banking details for Faktura.uz invoices. |
| `CODE_NDS`, `NSP_CODE` | string | Tax registration codes. |
| `PINF` | string | Personal identity number (Uzbekistan). |
| `CONTRACT` | string | Contract reference code. |
| `CONTRACT_DATE` | datetime | Contract activation date. |
| `CHANNEL` | string | FK to `ClientChannel.ID`. |
| `CLASS` | string | FK to `ClientClass.ID`. |
| `NEED_TO_AUDIT` | string | `Y` triggers an audit on next visit. |
| `TYPE` | int | Client type code (B2B / B2C / chain / etc.). |
| `SALES_CAT` | string | FK to `SalesCategory`. |
| `CODE_2` | string | Secondary code used by some 1C integrations. |
| `CONTRAGENT` | string | FK to `Contragent.CLIENT_ID` when contragent mode is on. |
| `TGIS_ID` | string | Tax-system foreign key. |
| `ACTIVE` | char(1) | Soft-delete flag. |
| `APPROVED` | int | 0 pending, 1 approved (rejected new-outlet workflow). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Indexes

`d0_client` has 58 columns. Live indexes: `CITY`, `CLIENT_CAT`,
`XML_ID`, `EXPEDITOR`, `CHANNEL`, plus the PK on `CLIENT_ID`.

### Relationships

The model declares no `relations()` itself but is referenced by every
financial and order model. Cross-table joins go through `CLIENT_ID`.

### Read / write surface

Writes: `ClientController::actionSave`, mobile API new-outlet flow,
`ClientPending` approval flow (when `APPROVED=0` transitions to 1),
1C / Faktura sync, KPI engine (updates `NEED_TO_AUDIT`). Reads:
practically every report.

### Gotchas

- `BALANS` is a **cache**; the truth is in `ClientTransaction`. Run
  `ClientFinans::recompute` if it drifts.
- The `ADRESS` column is the legacy spelling and is the actual DB
  column name. Do not rename to `ADDRESS`.
- `APPROVED=0` clients can be created by agents in the field but do
  not appear in invoicing reports until a manager approves.

---

## `ClientTransaction`

Source: `protected/models/ClientTransaction.php`. Extends `BaseFilial`.
`filialTable()` returns `{{client_transaction}}`, resolves to
`d0_fN_client_transaction`. Primary key `CLIENT_TRANS_ID`. Live DB: 40 columns.

This is the **canonical finans ledger** of sd-main. Every order,
payment, defect, manual adjustment, transfer, and bonus money-effect
posts at least one row here.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `CLIENT_TRANS_ID` | string | PK (UUID-like). |
| `DILER_ID` | string | Tenant subdivision. |
| `CLIENT_ID` | string | FK to `Client`. |
| `SUMMA` | float | Signed amount in `CURRENCY`. Positive grows the client's debt to us (sale); negative reduces it (payment). |
| `IDEN` | string | Identity tag for cross-row grouping. |
| `DATE` | datetime | Effective business date (NOT row creation). |
| `DATE_EXP` | datetime | Expected close date for receivables. |
| `COMMENT` | string | Free-text. |
| `TIMESTAMP_X` | datetime | Trigger-managed last write. |
| `TYPE` | string | High-level type: cash, card, transfer, defect, adjust, bonus. |
| `TRANS_TYPE` | string | Origin event: `order`, `payment`, `defect_return`, `bonus`, `manual`. |
| `STATUS` | string | Posting state — relevant for confirm-on-delivery flow. |
| `CURRENCY` | string | FK to `Currency.CURRENCY_ID`. |
| `CURRENCY_SYMBOL` | string | Display symbol. |
| `CURRENCY_RATE` | float | Snapshot of FX rate at posting. |
| `CONVERTATION` | float | Converted-to-base-currency amount. |
| `COMISSION` | float | Bank/processor commission deducted. |
| `COMPUTATION` | float | Sum used by reports — derived from `SUMMA` + `CONVERTATION`. |
| `EXPEDITOR` | string | Expeditor who collected the cash (if any). |
| `AGENT_ID` | string | Agent who created the row (if any). |
| `USER_ID` | string | Office user who created the row (if any). |
| `HISTORY` | string | JSON blob describing edit history. |
| `CASHBOX` | string | FK to `Cashbox.ID`. |
| `OFD_ID` | string | Fiscal device cheque ID. |
| `DATE_CLOSE` | datetime | Closure date (period-close mechanic). |
| `STORE_ID` | string | Source warehouse / cashier. |
| `XML_ID` | string | External 1C ID. |
| `CONFIRM_ID` | string | Set when a pending row is confirmed. |
| `CONFIRM_USER` | string | Confirming user. |
| `ONLINE_PAYMENT_ID` | int | FK to `OnlinePayment` when posted through Payme / Click / etc. |
| `ACTIVE` | char(1) | Soft-delete. |
| `SYNC` | string | Sync ledger. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: order-save (one row of type `order`), payment flow
(`PaymentDeliver`, `Cashbox` UI, online-payment webhooks), defect
return (`OrderDefectController`), manual adjustment by accountant
(`FinansController::actionEdit`), bonus engine (when bonus
materialises as money), period-close (writes `DATE_CLOSE`). Reads:
every finans report, the client balance widget, sd-cs and sd-billing
aggregators.

### Gotchas

- `SUMMA` sign convention is **positive = client owes us, negative =
  we owe client**. Reports that show debt as a positive number must
  not negate before display.
- A `STATUS='pending'` row (confirm-on-delivery flow) does NOT count
  in the client balance until the expeditor confirms and the row
  flips to confirmed. Don't aggregate raw rows naively.
- `Cashbox.KASSIR` lookup is by user; `CASHBOX` on this row is by
  cashbox ID — don't confuse them.
- `ClientTransactionHistory` (32 cols) keeps the append-only history
  of edits to a row.

---

## `Agent`

Source: `protected/models/Agent.php`. Extends `BaseFilial`.
`filialTable()` returns `{{agent}}`, resolves to `d0_fN_agent`. Primary
key `AGENT_ID`. Live DB: 29 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `AGENT_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Phone. |
| `PASSPORT_COPY` | string | URL to passport scan. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | Profile photo URL. |
| `DILER_ID` | int | Tenant subdivision. |
| `EMAIL` | string | Email. |
| `ACTIVE` | char(1) | `Y` / `N`. |
| `VAN_SELLING` | int | 1 if van-selling enabled (mobile expeditor flow). |
| `AUDIT` | string | `Y` if agent does audits. |
| `SYNC` | string | Sync ledger. |
| `XML_ID` | string | External ID. |
| `FILTER` | string | JSON filter scoping the agent's outlet visibility. |
| `APP_VERSION` | string | Last reported mobile app version. |
| `DEVICE_MODEL` | string | Last reported device model. |
| `LAST_SYNC_TIME` | datetime | Last successful sync push from this user. |
| `IP_ADDRESS` | string | Last sync IP. |
| `CASHBOX` | string | FK to `Cashbox.ID` — agent's default cashbox. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Relationships

The model declares HAS_ONE to `User` on `AGENT_ID = USER.AGENT_ID` so
the API layer can resolve credentials and role.

### Read / write surface

Writes: `AgentController` admin UI, RBAC role-assignment, mobile-app
metadata pings on each sync. Reads: visit module, KPI engine,
sales-by-agent report, the trip planner.

### Gotchas

- `Agent` is the **business identity**. The login (`User`) is a
  separate row joined by `AGENT_ID`. Disabling login means setting
  `User.ACTIVE='N'`, not `Agent.ACTIVE='N'`.
- `FILTER` is JSON; legal values are documented in the
  `AgentFilter` helper.
- `LAST_SYNC_TIME` is what the sd-cs central console reads to
  detect "offline > 24h" agents.

---

## `Supervayzer`

Source: `protected/models/Supervayzer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{supervayzer}}`, resolves to
`d0_fN_supervayzer`. Primary key `SV_AGENT_ID`. Live DB: 11 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `SV_AGENT_ID` | string | PK. |
| `USER_ID` | string | FK to `User.USER_ID` (the login). |
| `DILER_ID` | string | Tenant subdivision. |
| `AGENT_ID` | string | FK to `Agent.AGENT_ID` — the subordinate agent supervised. |
| `POSITION_ID` | int | FK to position lookup. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standard audit / sync. |

### Read / write surface

Writes: `SupervayzerController` admin UI. Reads: supervisor-scoped
report filters, the KPI engine (a supervisor inherits all subordinate
agents' KPIs).

### Gotchas

- One supervisor may supervise many agents — multiple rows with the
  same `USER_ID` and different `AGENT_ID`.
- Removing a supervisor row does not log the change anywhere — diff
  via `model_log` if you need an audit trail.
- The supervisor role does NOT see other supervisors' data unless
  `ServerSettings::isCrossSupervayzer()` is on.

---

## `Expeditor`

Source: `protected/models/Expeditor.php`. Extends `BaseFilial`.
`filialTable()` returns `{{expeditor}}`, resolves to `d0_fN_expeditor`.
Primary key `EXPEDITOR_ID`. Live DB: 28 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `EXPEDITOR_ID` | string | PK. |
| `FIO` | string | Full name. |
| `TEL` | string | Phone. |
| `AUTONUM` | string | Vehicle plate number. |
| `AUTOBRAND` | string | Vehicle brand. |
| `DILER_ID` | string | Tenant subdivision. |
| `PASSPORT_COPY` | string | Scan URL. |
| `DATE_BIRTH` | datetime | Birthday. |
| `ADDRESS` | string | Free-text. |
| `PHOTO` | string | Photo URL. |
| `CITY_ID` | string | FK to `City`. |
| `EMAIL` | string | Email. |
| `PINFL` | string | Tax / passport identifier. |
| `ADD_FILTER` | string | JSON additional scoping filter. |
| `DEFECT_STORE` | string | FK to `Store.STORE_ID` — store where this expeditor returns defective goods. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME`, `ID` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: `ExpeditorController`, trip-assignment job, mobile expeditor
app on sync. Reads: trip planner (`Trip`), expeditor KPI engine
(`ExpeditorKpiJob`, `ExpeditorKpiSetup`), expeditor-load reports
(`ExpeditorLoad`, `ExpeditorLoadDetail`).

### Gotchas

- A login (`User.EXPEDITOR_ID`) can map to an `Expeditor` row, and a
  `Cashbox` is typically attached at trip time.
- `DEFECT_STORE` defaults to a designated quarantine store; orders
  marked as defect return there until a manager re-stocks.

---

## `User`

Source: `protected/models/User.php`. Extends `BaseFilial`.
`filialTable()` returns `{{user}}`, resolves to `d0_fN_user`. Primary
key `USER_ID`. Live DB: 22 columns. Authentication / role-bearer row;
paired with one of `Agent`, `Expeditor`, `Supervayzer`, `Auditor`,
or none (back-office user).

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `USER_ID` | int | PK (autoincrement). |
| `NAME` | string | Display name. |
| `EMAIL` | string | Email. |
| `DILER_ID` | int | Tenant subdivision. |
| `AGENT_ID` | int | FK to `Agent.AGENT_ID` (when role = agent). |
| `EXPEDITOR_ID` | string | FK to `Expeditor.EXPEDITOR_ID` (when role = expeditor). |
| `ROLE` | int | Role code (cross-references `authassignment`). |
| `LOGIN` | string | Login name. |
| `PASSWORD` | string | bcrypt hash. |
| `CODE` | string | Recovery code. |
| `XML_ID` | string | External ID. |
| `PAY` | int | Pay-period flag. |
| `TEL` | string | Phone. |
| `ACTIVE` | char(1) | Soft-delete. Disables login. |
| `DIVICE_ID` | string | Last device identifier (note legacy spelling). |
| `SYNC` | string | Sync ledger. |

### Read / write surface

Writes: `UserController`, mobile registration flow, password reset.
Reads: every authenticated controller (`Yii::app()->user->getUser()`),
RBAC checker, license counter.

### Gotchas

- The actual permission grant lives in `authassignment` and
  `authitem`, not in `User`. `ROLE` is a denormalised hint.
- The legacy column name is `DIVICE_ID` (typo) — preserve when
  writing migrations.
- `ACTIVE='N'` immediately blocks login on next request, including
  any open mobile sync session.

---

## `Product`

Source: `protected/models/Product.php`. Extends `CActiveRecord`
directly — **filial-shared** master row. `tableName()` returns
`d0_product`. Primary key `PRODUCT_ID`. Live DB: 50+ columns.

### Columns (selected)

| Column | Type | Purpose |
|--------|------|---------|
| `PRODUCT_ID` | string | PK. |
| `TRADE_ID` | int | FK to `TradeDirection`. |
| `PRODUCT_CAT_ID` | string | FK to `ProductCategory`. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `VOLUME` | float | Cubic m3 per unit. |
| `PACK_QUANTITY` | float | Units per pack. |
| `SAP_CODE` | string | ERP code. |
| `BAR_CODE` | string | EAN / UPC. |
| `IKPU` | string | Uzbekistan tax classification code. |
| `IKPU_PACK_CODE`, `IKPU_UNIT_CODE` | string | Variant IKPU codes. |
| `GTIN` | string | Global trade item number. |
| `ETTN_CODE` | string | ETTN / e-waybill code. |
| `VAT_RATE` | float | Output VAT %. |
| `EXCISE_RATE`, `EXCISE_RATE_TYPE` | float / int | Excise. |
| `TARA_ID` | string | FK to `Tara` (packaging deposit). |
| `WEIGHT` | float | Per-unit weight. |
| `BLOCKS_IN_BOX` | int | Pack hierarchy info. |
| `SHELF_LIFE` | int | Days. |
| `PHOTO` | string | Image URL. |
| `UNIT_ID` | string | FK to `Unit`. |
| `PACK` | int | Pack-mode flag. |
| `SEGMENT`, `BRAND`, `PRODUCER` | int | Catalog dimensions. |
| `PROPERTY`, `PROPERTY1`, `PROPERTY2` | int | Free-form classification. |
| `BY_BLOCK` | string | 1 if sales must be in blocks. |
| `CASE_TYPE_ID` | int | Case-pack type. |
| `IS_MML` | string | 1 if part of "must-have" mandatory list. |
| `IS_OUR`, `IS_LOCAL` | string | Ownership / locality flags. |
| `CS_PRODUCT`, `CS_ID`, `CS_CAT_ID` | string / int | Cross-system catalog binding. |
| `XML_ID` | string | External ERP ID. |
| `DESCRIPTION` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: `ProductController`, 1C import, Faktura.uz sync (IKPU). Reads:
every catalog screen, every order line, every audit (`AdtAudit`,
`AudProduct`), every stock query.

### Gotchas

- `Product` is filial-shared. To restrict a product to a filial use
  `ProductFilial` (= `d0_filial_product`).
- IKPU codes and excise are mandatory for invoiceable products under
  Uzbekistan tax law; missing IKPU blocks ESF submission.
- `BLOCKS_IN_BOX`, `PACK_QUANTITY`, `BY_BLOCK` interact: read
  `docs/concepts/tara.md` for the rules.

---

## `ProductPriceMarkup`

Source: `protected/models/ProductPriceMarkup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_product_subcategory` (the
table name is a misnomer; the model handles per-product markup rules).
Primary key `ID`. Filial-shared.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `PRODUCT` | string | FK to `Product.PRODUCT_ID`. |
| `PRICE_TYPE` | string | Target price type. |
| `BASE_PRICE_TYPE` | string | Source price type. |
| `MARKUP` | float | Multiplier (`1.20` = +20%). |
| `ROUND_METHOD` | int | 0 nearest, 1 up, 2 down. |
| `ROUND_ACCURACY` | float | Rounding step (100, 500, 1000 etc). |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: `PriceTypeController::actionMarkup`, price-recalc cron.
Reads: order submit (calculates `OrderDetail.PRICE` if a markup rule
is active), the price-list export.

### Gotchas

- A bare `Product` row does NOT store prices. Prices come from a
  markup rule + a base price-type, or are loaded directly into
  `OldPrice` / similar tables.
- `ROUND_ACCURACY` defaults are tenant-dependent — never assume 1000.

---

## `PriceType`

Source: `protected/models/PriceType.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_price_type`. Primary key
`PRICE_TYPE_ID`.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `PRICE_TYPE_ID` | string | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | FK to `Currency`. |
| `PARENT` | string | Optional parent PriceType (markup chains). |
| `TYPE` | string | Sales / purchase / contract. |
| `FOR_CLIENT` | int | 1 if visible to clients. |
| `OLD_PRICE_TYPE` | string | Legacy ID. |
| `FILIAL` | int | Optional filial scoping. |
| `DILER` | string | Tenant subdivision. |
| `DESCRIPTION` | string | Free-text. |
| `SORT` | int | Display order. |
| `VALYUTA_ID` | int | FK to `Valyuta` (currency alt). |
| `DEALER_PRICE` | int | 1 if this is a dealer-tier price. |
| `HAND_EDIT` | string | Y if hand-overridden. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: `PriceTypeController`, 1C import. Reads: client default
(`Client.PRICE_TYPE_ID`), order submit, every report that shows
prices.

### Gotchas

- A client can override the default at order-submit by selecting a
  different price type — only price types where `FOR_CLIENT=1` are
  selectable in the mobile app.
- `PARENT` enables price-type chaining; cycles are not detected at
  insert and will deadlock the markup engine.
- `PriceTypeFilial` is the binding model that restricts a price type
  to specific filials.

---

## `Stock` (operational stock — see also `WarehouseDetail`)

The `Stock` concept in sd-main is not a single table. There are three
related tables:

- `d0_fN_warehouse_detail` — per-warehouse per-product on-hand row.
  Model `WarehouseDetail`. **This is the canonical "stock" table.**
- `d0_fN_store_detail` — per-store per-product mirror used by the
  van-selling flow (`Store` + `StoreDetail`).
- `d0_stock_exp` — expeditor's truck-load on-hand. Model `StockExp`.

The shallow `Stock` reference in the old version of this doc has been
replaced by the three sections below.

### `WarehouseDetail`

Source: `protected/models/WarehouseDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse_detail}}`. PK `WAREHOUSE_DETAIL_ID`.
Live DB: 14 columns.

| Column | Type | Purpose |
|--------|------|---------|
| `WAREHOUSE_DETAIL_ID` | string | PK. |
| `WAREHOUSE_ID` | string | FK to `Warehouse`. |
| `STORE_ID` | string | FK to `Store` (when warehouse is wrapped by a store). |
| `PRODUCT_CAT_ID` | string | FK to `ProductCategory`. |
| `PRODUCT_ID` | string | FK to `Product`. |
| `TYPE` | string | Stock type / status. |
| `IDEN` | string | Identity tag for grouping. |
| `COUNT` | int | On-hand units. Can be negative if `Store.NEGATIVE_COUNT='Y'`. |
| `DILER_ID` | string | Tenant subdivision. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standard. |

### `StoreDetail`

Source: `protected/models/StoreDetail.php`. Extends `BaseFilial`.
`filialTable()` returns `{{store_detail}}`. PK `STORE_DETAIL_ID`.

`STORE_DETAIL_ID`, `STORE_ID`, `PRODUCT_CAT_ID`, `PRODUCT_ID`,
`COUNT`, `DILER_ID`, `TIMESTAMP_X`, `ACTIVE`, `SYNC`. Mirror of
`WarehouseDetail` aligned to the `Store` model used by the van-selling
flow.

### `StockExp`

Source: `protected/models/StockExp.php`. Extends `BaseFilial`.
`filialTable()` returns `{{stock_exp}}`. PK `ID`.

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | string | PK. |
| `PRODUCT_ID` | string | FK. |
| `CLIENT_ID` | string | FK (consignment to client, used for VS / mobile sale). |
| `AGENT_ID` | string | FK. |
| `USER_ID` | string | FK. |
| `COUNT` | float | Units. |
| `DATE` | datetime | Event date. |
| `DATE_PRO`, `DATE_EXP` | datetime | Manufacture / expiry. |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standard. |
| `CREATE_BY` / `CREATE_AT` / `UPDATE_BY` / `UPDATE_AT` | – | Audit. |

### Gotchas

- The two stock tables (`WarehouseDetail` + `StoreDetail`) are kept
  in sync by `StoreLog` triggers / job. Drift requires a re-sync.
- Negative stock is allowed when `Store.NEGATIVE_COUNT='Y'`; many
  reports silently filter out negatives.
- `StockExp` rows are the expeditor's truck inventory while a trip is
  active. Reconcile via `ExpeditorLoad` on trip close.

---

## `Warehouse`

Source: `protected/models/Warehouse.php`. Extends `BaseFilial`.
`filialTable()` returns `{{warehouse}}`, resolves to `d0_fN_warehouse`.
Primary key `WAREHOUSE_ID`. Live DB: 14 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `WAREHOUSE_ID` | string | PK. |
| `DILER_ID` | string | Tenant subdivision. |
| `TYPE` | string | Storage type. |
| `TYPE_LIMIT` | string | Allowed product-type filter. |
| `NAME` | string | Display name. |
| `IDEN` | string | Identity tag. |
| `COUNT` | int | Snapshot. |
| `CONDITION` | string | Free-text (e.g. cold-storage). |
| `COMMENT` | string | Free-text. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X`, `ID` | – | Standard. |

### Read / write surface

Writes: `WarehouseController`, 1C import. Reads: stock-on-hand
queries, trip planner (pick from `STORE_ID -> WAREHOUSE_ID` chain),
inventory module (`Inventory*`).

### Gotchas

- `Warehouse` ≠ `Store`. A `Store` (model `Store`, table `d0_store`)
  is the **vending** unit (cash register / point-of-sale or
  expeditor van). A `Warehouse` is a **storage** unit, mapped by
  `WarehouseLocation` when the two diverge.
- `WarehouseDetail` carries the actual on-hand by product.

---

## `Visit`

Source: `protected/models/Visit.php`. Extends `BaseFilial`.
`filialTable()` returns `{{visit}}`. Primary key composite (`ID`,
`DATE`). Live DB: 28 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | Part of PK (autoincrement). |
| `DATE` | datetime | Part of PK; visit start time. |
| `AGENT_ID` | string | FK to `Agent`. |
| `USER_ID` | string | FK to `User`. |
| `CLIENT_ID` | string | FK to `Client`. |
| `VISITED` | char(1) | `Y` if check-in happened. |
| `ORDER` | char(1) | `Y` if an order was placed. |
| `REJECT` | char(1) | `Y` if a rejection / no-buy reason was logged. |
| `PHOTO` | char(1) | `Y` if photo was attached. |
| `AUDIT` | char(1) | `Y` if an audit was performed. |
| `LON`, `LAT` | float | Check-in geocoordinates. |
| `DISTANCE` | float | Meters from outlet, computed server-side at save. |
| `GPS_STATUS` | int | GPS quality: 0 disabled, 1 ok, 2 stale, 3 mock. |
| `CHECK_IN_TIME` | datetime | Mobile-side check-in moment. |
| `CHECK_OUT_TIME` | datetime | Check-out moment. |
| `PLANED` | char(1) | `Y` if visit was on plan. |
| `STORE_CHECK` | char(1) | `Y` if shelf check was performed. |
| `PAYMENT`, `DELIVERY`, `POLL`, `ORDER_REPLACE`, `ORDER_DEFECT` | char(1) | Per-step completion flags. |
| `SYNC_TIME` | datetime | When sync completed. |
| `DAY` | date | Truncated `DATE` for fast grouping. |
| `POSITION_ID` | string | Role / position at visit time. |
| `ROLE` | string | Role text. |

### Read / write surface

Writes: mobile API check-in + check-out + step-completion endpoints.
Reads: visit dashboard, KPI engine, audit module, outlet-fact
aggregator.

### Gotchas

- `GPS_STATUS=3` (mock GPS) flags potential fraud — many reports
  filter it out and the visit does not count toward KPI.
- The composite PK means two visits to the same client on the same
  `DATE` second collide. Mobile retries should use unique
  timestamps.
- `DISTANCE` is server-computed from `Client.LON / LAT`; outlets
  without geo coordinates always report 0.

---

## `Gps`

Source: `protected/models/Gps.php`. Extends `BaseFilial`.
`filialTable()` returns `{{gps}}`. PK composite (`ID`, `DATE`). Live
DB: 20 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | Part of PK (autoincrement). |
| `DATE` | datetime | Part of PK. |
| `AGENT_ID` | string | FK to `Agent`. |
| `USER_ID` | string | FK to `User`. |
| `TYPE` | string | Event type. |
| `ORDER_ID` | string | FK to `Order` if ping is attached to an order. |
| `CLIENT_ID` | string | FK to `Client` if ping is attached to a visit. |
| `LAT`, `LON` | float | Coordinates. |
| `BATTERY` | int | Battery % at ping time. |
| `PROVIDER` | string | `gps` / `network` / `fused`. |
| `SIGNAL` | int | Signal strength. |
| `MODE` | string | Mobile activity mode. |
| `INTERNET_STATUS` | int | Connectivity. |
| `GPS_STATUS` | int | Mock-detection. |
| `MOB_TIMESTAMP` | string | Client clock at ping. |
| `TIMESTAMP_X` | datetime | Server receipt. |
| `DAY` | date | Truncated date for indexing. |
| `DEVICE` | string | Device identifier. |

### Read / write surface

Writes: mobile sync (high volume — a ping every few seconds during
active hours). Reads: GPS-history view, fraud detection (mock GPS),
trip replay tool.

### Gotchas

- This is the **highest-volume per-tenant table**. Plan partitioning
  before scaling out — `DATE` composite-PK is the right axis.
- Old rows are archived to a separate cold table by the period-close
  job; if you read older than 90d, target the archive.
- `MOB_TIMESTAMP` is the source-of-truth time when device clocks
  drift; `TIMESTAMP_X` is the server arrival.

---

## `Trip`

Source: `protected/models/Trip.php`. Extends `BaseFilial`.
`filialTable()` returns `{{trip}}`. Primary key `ID`. Live DB has the
sister `TripOrder` model for the trip-line many-to-many.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `CAR_ID` | int | FK to `Car`. |
| `COURIER_ID` | string | FK to `Expeditor.EXPEDITOR_ID` (courier role). |
| `EXPEDITOR_ID` | string | FK to `Expeditor.EXPEDITOR_ID` (assigned expeditor). |
| `STORE_ID` | string | FK to `Store.STORE_ID` (origin). |
| `DATE` | datetime | Planned departure. |
| `STATUS` | int | 1 waiting, 2 active, 3 done, 4 cancelled. |
| `ACTIVE` | char(1) | Soft delete. |

### `TripOrder`

PK `ID`. Columns `TRIP_ID`, `ORDER_ID`, `SORT`. Many-to-many between
trips and orders with an explicit ordering.

### Read / write surface

Writes: trip-planner UI, expeditor mobile app on departure / arrival.
Reads: expeditor view, trip-progress dashboard.

### Gotchas

- `COURIER_ID` and `EXPEDITOR_ID` are separate roles — a courier may
  drive while the expeditor is responsible for cash collection.
- See `docs/concepts/trip-lifecycle.md` for the full state machine.

---

## `Payment` (sd-main payment row)

In sd-main "payment" is not a single table. The relevant tables are:

- `d0_fN_payment_deliver` — confirm-on-delivery payment captured by
  the expeditor. Model `PaymentDeliver`.
- `d0_fN_payment_transfer` — multi-step transfer between cashboxes /
  filials. Model `PaymentTransfer`.
- `d0_fN_payment_displacement` — internal displacement ledger.
  Model `PaymentDisplacement`.

The sd-billing `Payment` (in a different schema) is unrelated; do
not mix them.

---

## `PaymentDeliver`

Source: `protected/models/PaymentDeliver.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_deliver}}`. PK `ID`. Live DB: 23 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `CLIENT_ID` | string | FK to `Client`. |
| `ORDER_ID` | string | FK to `Order`. |
| `SUMMA` | float | Paid amount. |
| `CURRENCY` | string | FK to `Currency`. |
| `DATE` | datetime | Payment date. |
| `USER_ID` | string | Cashier user (if any). |
| `AGENT_ID` | string | Collecting agent (if any). |
| `TRADE_ID` | string | FK to `TradeDirection`. |
| `TERM` | string | Payment terms / channel. |
| `CONFIRM` | string | Confirmation status. |
| `COMMENT` | string | Free-text. |
| `CREATE_BY` / `UPDATE_BY` / `CREATE_AT` / `UPDATE_AT` | – | Audit. |

### Read / write surface

Writes: expeditor mobile API at delivery confirmation, cashier UI.
Reads: order debt reconciliation, daily-cash report.

### Gotchas

- A `PaymentDeliver` row is the **trigger** for posting a
  `ClientTransaction` of type `payment` once the manager confirms.
  Until then it sits in a pending state.
- `CONFIRM='Y'` is what flips the related `ClientTransaction.STATUS`
  to confirmed.

---

## `PaymentTransfer`

Source: `protected/models/PaymentTransfer.php`. Extends `BaseFilial`.
`filialTable()` returns `{{payment_transfer}}`. PK
`PAYMENT_TRANSFER_ID`. Live DB: 13 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `PAYMENT_TRANSFER_ID` | string | PK. |
| `DOCUMENT_ID` | string | Source document ID (often a parent transfer or order). |
| `OPERATION_ID` | int | 1 sending, 2 receiving. |
| `FILIAL_ID` | int | Filial the row applies to. |
| `CURRENCY_ID` | string | FK to `Currency`. |
| `SUMMA` | float | Transfer amount. |
| `STATUS` | int | 1 new, 2 pending, 3 accepted, 4 rejected, 5 cancelled. |
| `COMMENT` | string | Free-text. |
| `CREATE_AT` / `CREATE_BY` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: cross-filial transfer UI, reconciliation cron. Reads: finans
dashboard, the transfer-status modal.

### Gotchas

- Each transfer typically lives as **two rows**: a `OPERATION_ID=1`
  sending row in the source filial, a `OPERATION_ID=2` receiving row
  in the destination filial. Both must reach `STATUS=3` for the
  transfer to be considered done.
- `STATUS=4` (rejected) leaves money in limbo until a manual
  adjustment in `ClientTransaction`.

---

## `Cashbox`

Source: `protected/models/Cashbox.php`. Extends `BaseFilial`.
`filialTable()` returns `{{cashbox}}`. PK `ID`. Live DB: 15 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `NAME` | string | Display name. |
| `CURRENCY` | string | FK to `Currency`. |
| `KASSIR` | string | FK to `User.USER_ID` of the cashier. |
| `SORT` | int | Display order. |
| `XML_ID` | string | External ID. |
| `ACTIVE`, `SYNC`, `TIMESTAMP_X`, `TIME` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: `CashboxController`. Reads: every `ClientTransaction` that
involves cash, daily cash close, sd-billing's cashbox aggregator.

### Gotchas

- `CashboxDisplacement` (`d0_cashbox_displacement`) records movement
  between cashboxes; closing balance derives from the running sum.
- A `Cashbox` row is filial-scoped via `BaseFilial`. Don't share IDs
  across filials.

---

## `AdtAuditResult`

Source: `protected/models/AdtAuditResult.php`. Extends `BaseFilial`.
`filialTable()` returns `{{adt_audit_result}}`. PK `ID`. Live DB: 12 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `VISIT_ID` | int | FK to `Visit.ID`. |
| `DATE` | datetime | Audit timestamp. |
| `CLIENT_ID` | string | FK to `Client`. |
| `POSITION_ID` | int | Role / position at audit time. |
| `AUDIT_ID` | int | FK to `AdtAudit.ID`. |
| `USER_ID` | string | FK to `User`. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: audit module via the agent's mobile audit step. Reads:
audit dashboard, KPI engine, photo-report cross-references.

### Gotchas

- `AdtAuditResult` is the audit **header**. Per-SKU rows go in
  `AdtAuditResultData`.
- This is the v2 audit engine ("ADT"). The older `AuditStorchekCat`
  / `Auditor` tables are for the v1 engine. They coexist.

---

## `AdtAuditResultData`

Source: `protected/models/AdtAuditResultData.php`. Extends
`BaseFilial`. `filialTable()` returns `{{adt_audit_result_data}}`.
PK `ID`. Live DB: 12 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `RESULT_ID` | int | FK to `AdtAuditResult.ID`. |
| `PRODUCT_ID` | int | FK to `Product`. |
| `PRICE` | float | Observed shelf price. |
| `FACE` | int | Facing count. |
| `SOLD` | int | Reported sold-out count since last visit. |
| `STORE` | int | Observed shelf-stock. |
| `AVAILABLE` | bool | TRUE if SKU is on shelf. |
| `OUT_OF_STOCK` | bool | TRUE if shelf-empty. |
| `CREATE_AT` / `UPDATE_AT` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: same as parent. Reads: shelf-share report, OOS report, KPI
engine.

### Gotchas

- Both `AVAILABLE` and `OUT_OF_STOCK` exist because of edge cases —
  a SKU can be `AVAILABLE=false` (not listed) which is different
  from `AVAILABLE=true && OUT_OF_STOCK=true` (listed but empty).
- The audit can record price even if the SKU is OOS — `PRICE` is the
  last-seen shelf price.

---

## `KpiTask`

Source: `protected/models/KpiTask.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task}}`. PK `KPI_TASK_ID`. Live DB: 58 columns.

The KPI engine row. One `KpiTask` row = one KPI assigned to an agent
(or scope) for a date window.

### Columns (selected)

| Column | Type | Purpose |
|--------|------|---------|
| `KPI_TASK_ID` | string | PK. |
| `KPI_ID` | string | FK to `Kpi` (the KPI master). |
| `DILER_ID` | string | Tenant subdivision. |
| `NAME` | string | Display name. |
| `SORT` | int | Display order. |
| `TASK_TYPE` | string | Task code (sales-sum, AKB, OOS, etc.). |
| `VALUE` | float | Target / threshold value. |
| `DATE_TYPE` | string | Day / week / month / quarter. |
| `STATUS` | string | Active / paused. |
| `PRODUCT_ID`, `PRODUCT_CAT` | string | Optional product / category scoping. |
| `CLIENT_CAT`, `CLIENT_CLASS`, `CITY_ID`, `AGENT` | string | Optional dimensional scoping. |
| `CURRENCY` | string | FK to `Currency`. |
| `KPI_SHARE` | float | Weight of this KPI in the agent's total. |
| `BONUS_TYPE` | string | Bonus payout mode. |
| `BONUS` | float | Bonus amount when threshold reached. |
| `MARK`, `MARK2..MARK5` | int | Threshold marks. |
| `MARK2_KPI_SHARE`, `MARK2_BONUS_SHARE`, … `MARK5_*` | int | Share at each threshold. |
| `ACTIVE`, `SYNC`, `TIME`, `TIMESTAMP_X` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: KPI admin UI, KPI templating job. Reads: KPI dashboard,
payroll, the agent mobile dashboard "tasks" panel.

### Gotchas

- `KpiTask` is **per-period** — one row per period per agent. The
  template (see `KpiTaskTemplate`) is what gets cloned to produce
  these rows.
- The `MARK2..MARK5` ladder encodes a tiered bonus payout — higher
  marks unlock larger `MARK*_BONUS_SHARE`. Use the ladder helper in
  `KpiCalculator` instead of recomputing.

---

## `KpiTaskTemplate`

Source: `protected/models/KpiTaskTemplate.php`. Extends `BaseFilial`.
`filialTable()` returns `{{kpi_task_template}}`. PK `ID`. Live DB: 62 columns.

Mirrors `KpiTask` columns, but a template row is the design-time
specification rather than a period-realised task. Templates are
cloned into `KpiTask` rows by the template-instantiation job at the
start of each period. The extra columns versus `KpiTask` include
`MIN_SUM`, `NEW_CLIENTS`, `REPLACEMENTS`, `SUPERVISER`,
`ACCESS_TO_OTHERS`, `ACCESS_TO_USE`, `MAX_BONUS` — design-time knobs.

### Read / write surface

Writes: KPI admin UI. Reads: period-instantiation cron — produces
the `KpiTask` rows for the next period.

### Gotchas

- Templates live in `KpiTaskTemplateGroup` (small grouping table);
  re-grouping a template does NOT re-instantiate already-active
  `KpiTask` rows.

---

## `KpiTaskTemplateGroup`

Source: `protected/models/KpiTaskTemplateGroup.php`. Extends
`CActiveRecord`. `tableName()` returns `d0_kpi_task_template_group`.
PK `ID`. Live DB: 10 columns.

Lightweight grouping table — name, description, sort order, audit.
Used to organise KPI templates in the admin UI.

---

## `Plan`

Source: `protected/models/Plan.php`. Extends `BaseFilial`.
`filialTable()` returns `{{plan}}`. PK `PLAN_ID`. Live DB: 12 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `PLAN_ID` | int | PK. |
| `DILER_ID` | int | Tenant subdivision. |
| `PLAN` | string | Plan payload (often JSON of sub-plans). |
| `NAME` | string | Display name. |
| `MONTH`, `YEAR` | int | Period. |
| `PLAN_COMPLETED` | string | Cached completion %. |
| `TIMESTAMP_X` | datetime | Standard. |
| `ACTIVE` | char(1) | Soft delete. |
| `SYNC` | string | Sync. |

### `PlanProduct`

Sister table for per-product plan rows. PK `ID`. 13 columns including
`PLAN_ID`, `PRODUCT_ID`, `COUNT`, `SUMMA`.

### Read / write surface

Writes: planning admin UI, plan-import job. Reads: KPI engine, the
sales-vs-plan dashboard, payroll calculator.

### Gotchas

- A `Plan` is filial-scoped via `BaseFilial`, so cross-filial
  planning means writing one row per filial.
- The `PLAN_COMPLETED` cache is recomputed hourly; do not rely on it
  for live SLAs.

---

## `Bonus`

Source: `protected/models/Bonus.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_bonus`. PK `BONUS_ID`. Live
DB: 36 columns. Buy-X-get-Y promo engine row.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `BONUS_ID` | string | PK. |
| `DILER_ID` | string | Tenant subdivision. |
| `NAME` | string | Display name. |
| `BONUS_TYPE` | int | Type code (gift, discount, free SKU, etc.). |
| `PRODUCT` | string | Trigger product IDs (CSV / JSON). |
| `CURRENCY` | string | FK. |
| `CLIENT_TYPE`, `CLIENT_CHANNEL`, `CLIENT_CAT` | string | Client scoping. |
| `PRICE_TYPE` | string | FK to `PriceType`. |
| `BONUS_PRODUCTS` | string | Gift / bonus product IDs. |
| `BONUS` | string | Bonus payload (count / pct / amount). |
| `PARENT` | string | Parent bonus chain. |
| `VALUE` | string | Trigger threshold (count or sum). |
| `AGENT_ID` | string | Optional agent scoping. |
| `CITY` | string | Optional city scoping. |
| `MIN_COUNT`, `MAX_COUNT` | string | Trigger ranges. |
| `DATE`, `DATE_FROM`, `DATE_TO` | datetime | Active window. |
| `IS_PUBLIC` | string | Public-listing flag. |
| `ONLY_ONE_TIME` | int | 1 = single redemption per client. |
| `MAX_BONUS` | int | Cap on payout. |
| `MANUAL` | string | Manual / auto flag. |
| `ACTIVE`, `SYNC`, `TIME`, `ID` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: bonus admin UI. Reads: order-submit engine — every order
runs the bonus rules and may produce a child `BonusOrder` row.

### Gotchas

- The trigger fields (`PRODUCT`, `MIN_COUNT`, etc.) are
  string-encoded — read the parsing helper in `BonusComponent`
  before assuming CSV.
- A bonus may be **automatic** (`MANUAL=N`, the engine applies it on
  qualifying orders) or **manual** (agent picks the bonus at
  submit).
- See also `BonusOrder`, `BonusOrderDetail`, `BonusOrderHistory`,
  `BonusRelation`, `BonusAgent`, `BonusCity`, `BonusExclude`,
  `BonusFilial`, `BonusLimit` — the bonus engine fans out into many
  satellite tables.

---

## `BonusRelation`

Source: `protected/models/BonusRelation.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_bonus_relation`. PK `ID`. Live DB: 7 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `ID` | int | PK. |
| `PARENT_ID` | string | Parent `BONUS_ID`. |
| `RELATED_BONUS_ID` | string | Related child `BONUS_ID`. |
| audit columns | – | Standard. |

### Gotchas

- This table encodes bonus **chains** — buying X qualifies for
  bonus B1 which in turn qualifies for B2 if extra conditions are
  met. Cycles must not be created at insert time.

---

## `Skidka`

Source: `protected/models/Skidka.php`. Extends `CActiveRecord` —
filial-shared. `tableName()` returns `d0_skidka`. PK `SKIDKA_ID`. Live
DB: 37 columns. Discount-rule engine row. Sister tables:
`SkidkaAgent`, `SkidkaBudget`, `SkidkaExclude`, `SkidkaFilial`,
`SkidkaManual`, `SkidkaOrder`, `SkidkaRelation`, `SkidkaStore`.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `SKIDKA_ID` | string | PK. |
| `NAME` | string | Display name. |
| `DILER_ID` | string | Tenant. |
| `SKIDKA_TYPE` | int | Type code (% off, fixed, threshold etc.). |
| `PRODUCT` | string | Trigger products. |
| `CLIENT_CAT`, `CLIENT_TYPE`, `CLIENT_CHANNEL`, `CITY` | string | Scoping. |
| `CURRENCY` | string | FK. |
| `VALUE` | float | Threshold value. |
| `SKIDKA` | float | Discount value (percent or amount). |
| `PARENT` | string | Parent chain. |
| `DATE_FROM`, `DATE_TO` | datetime | Active window. |
| `BUDGET` | float | Hard cap across all redemptions. |
| `COMMENT` | string | Free-text. |
| `IS_PUBLIC` | string | Visible to clients. |
| `ONLY_ONE_TIME` | int | 1 = single redemption. |
| `NUM_CATEGORIES` | int | Cross-category threshold support. |
| `ACTIVE`, `SYNC`, `TIME`, `ID`, `TIMESTAMP_X` | – | Standard. |
| `CREATE_AT` / `UPDATE_AT` / `CREATE_BY` / `UPDATE_BY` | – | Audit. |

### Read / write surface

Writes: discount admin UI. Reads: order-submit engine — applies the
rule and posts `SkidkaOrder` row. Manual overrides go via
`SkidkaManual`.

### Gotchas

- A `SkidkaManual` row is created when a manager applies a
  one-off discount — it has its own PK and budget.
- `BUDGET` is a hard cap. Subsequent qualifying orders will not
  receive the discount once the budget is consumed; verify via the
  `SkidkaBudget` running total.

---

## `Filial`

Source: `protected/models/Filial.php`. Extends `CActiveRecord` —
**not** `BaseFilial` (it's the root table that defines the prefixes).
`tableName()` returns `d0_filial`. PK `id`. Live DB: 8 columns.

### Columns

| Column | Type | Purpose |
|--------|------|---------|
| `id` | int | PK. |
| `domain` | string | Tenant domain assignment. |
| `is_main` | int | 1 if root filial. |
| `prefix` | string | Per-filial table prefix (`f0`, `f1`, …). |
| `xml_id` | string | External ID. |

### Read / write surface

Writes: tenant onboarding flow (rare; usually once per tenant).
Reads: `FilialComponent` on every request, every `BaseFilial`
descendant.

### Gotchas

- Changing `prefix` after rows exist breaks every per-filial table
  lookup. Always create a new filial; never re-prefix.
- `is_main=1` should appear exactly once per tenant; root filial is
  where `Bonus`, `Skidka`, `Product`, `PriceType` etc. live.

---

## `ClientCategory`

Source: `protected/models/ClientCategory.php`. Extends
`CActiveRecord` — filial-shared. `tableName()` returns
`d0_client_category`. PK `CLIENT_CAT_ID`. Live DB: 15 columns.

### Columns

`CLIENT_CAT_ID`, `NAME`, `DESCRIPTION`, `SORT`, `XML_ID`, `ACTIVE`,
`SYNC`, `CREATE_AT`, `UPDATE_AT`, `CREATE_BY`, `UPDATE_BY`,
`TIMESTAMP_X`, `ID`.

### Read / write surface

Writes: directory admin UI, 1C import. Reads: filters across reports
(`Client.CLIENT_CAT`, `Order.CLIENT_CAT`, KPI scoping).

### Gotchas

- Deleting a category does not cascade — orphaned `CLIENT_CAT`
  references will silently return empty joins in reports.

---

## `ClientChannel`

Source: `protected/models/ClientChannel.php`. Extends `CActiveRecord`.
`tableName()` returns `d0_client_channel`. PK `ID`. Live DB: 8 columns.

### Columns

`ID`, `NAME`, `XML_ID`, `CREATE_BY`, `UPDATE_BY`, `CREATE_AT`,
`UPDATE_AT`.

### Read / write surface

Writes: directory admin. Reads: `Client.CHANNEL`, scoping on bonuses
(`Bonus.CLIENT_CHANNEL`) and discounts (`Skidka.CLIENT_CHANNEL`).

### Gotchas

- `ClientChannel` and `ClientClass` are distinct dimensions; do not
  conflate.

---

## `Contract` / `ContractClient`

Status: the model classes `Contract.php` and `ContractClient.php` are
**deprecated** in the codebase (renamed to `.obsolete`), but the live
table `d0_contract` (16 columns, InnoDB / utf8mb3, no Yii model) is
still queried by reports and by the Faktura / Didox integration.
Contract data for new code lives instead in the `Contragent` family
(`d0_contragent`, `d0_contragent_history`, `d0_contragent_log`).

### `d0_contract` (legacy, no model)

Cross-referenced by `Order.CONTRACT_ID`. Read directly via DAO for
backwards compatibility. New work should target `Contragent` model.

### `d0_contragent` (current)

Model `Contragent` (`protected/models/Contragent.php`). 39 columns.
PK `CLIENT_ID`. Stores the legally-incorporated counterparty linked
to a `Client` (when `ServerSettings::isContragent()` is on). Carries
banking details, IKPU defaults, contract anchor data, and is the
source row Faktura.uz and Didox use to build invoices.

### Gotchas

- Do not extend `Contract.php.obsolete`. New columns go on
  `Contragent`.
- A `Client` may have a 1:1 `Contragent` mirror (when contragent mode
  is on) or none — the order code is defensive about the join via
  `ServerSettings::isContragent()`.

---

## Domain groupings

The 30 tables documented above grouped by domain. Use this index to
jump from a domain to the relevant section.

| Domain | Tables |
|--------|--------|
| Orders | `Order`, `OrderDetail`, `OrderHistory` |
| Catalog | `Product`, `PriceType`, `ProductPriceMarkup` |
| Stock | `WarehouseDetail`, `Warehouse`, `StockExp` (under "Stock" section) |
| Clients | `Client`, `ClientCategory`, `ClientChannel`, `Contract` / `Contragent` |
| Finans | `ClientTransaction`, `PaymentDeliver`, `PaymentTransfer`, `Cashbox` |
| Team | `Agent`, `Supervayzer`, `Expeditor`, `User` |
| Visits & GPS | `Visit`, `Gps`, `Trip` (+ `TripOrder`) |
| Audit | `AdtAuditResult`, `AdtAuditResultData` |
| KPI | `KpiTask`, `KpiTaskTemplate`, `KpiTaskTemplateGroup`, `Plan` |
| Promo | `Bonus`, `BonusRelation`, `Skidka` |
| Tenant | `Filial` |

For the **full 306-model index** with column counts, PKs, and live DB
cross-checks, see `docs/data/schema-reference.md`. For higher-level
flows (order to finans, visit to KPI), see the diagrams under
`docs/architecture/diagrams.md` and the concept docs under
`docs/concepts/`.
