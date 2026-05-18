---
sidebar_position: 1
title: sd-billing · schema reference
audience: [engineer, dba, support-engineer]
summary: Every d0_ table in the sd-billing database — purpose, columns, foreign keys, who writes it, and notable gotchas. Compiled from the 55 migrations and the Yii ActiveRecord models.
topics: [data, billing, schema, migrations]
---

# sd-billing · schema reference

sd-billing is the vendor-side ledger: every dealer (tenant), every
license-issuing subscription, every money-in row, and the async
notifications that keep dealer tenants in sync. All tables use the prefix
`d0_` — the `tablePrefix` setting in `protected/config/db.php` rewrites
Yii's `{{tableName}}` placeholders to `d0_tableName` at runtime.

Unlike sd-cs / sd-main (where `{{filial}}` is a per-row field), sd-billing
is a single shared database. The dealer boundary lives in `d0_diler.HOST`
and `d0_diler.DOMAIN` — the "tenant key" the rest of the stack joins on.

## How the schema is organised

The sd-billing schema was bootstrapped from a legacy 2017-era SQL dump
that predates the migration history. The 55 numbered migrations in
`protected/migrations/` evolve it incrementally: each migration adds a
column, creates a small helper table, fixes a charset, or seeds an access
permission. There is no single migration creating `d0_diler`, `d0_payment`,
or `d0_subscription` — those are pre-history.

The authoritative shape of each table is the `@property` docblock on the
corresponding `protected/models/*.php` (plus per-module models under
`protected/modules/*/models/`).

## Headline numbers

- 55 migration files between `m220210` and `m260428`.
- 35 top-level models in `protected/models/`, plus 17 in module folders.
- ~50 live `d0_*` tables; ~340 distinct columns.
- 5 dedicated query indexes added by `m260310_120000` plus per-table
  `idx_*` indexes on `d0_dealer_blacklist`, `d0_notify_cron`,
  `d0_dealer_origin`, `d0_month_mentor`, `d0_dealer_key_account`,
  `d0_tariff_package`, `d0_notify_bot`.

## Domain grouping

1. **Dealer & subscription** — `d0_diler`, `d0_subscription`, `d0_package`,
   `d0_tariff`, `d0_tariff_package`, `d0_diler_package`, `d0_diler_bonus`,
   `d0_dealer_contact`, `d0_dealer_inns`, `d0_dealer_origin`,
   `d0_dealer_key_account`, `d0_dealer_blacklist`, `d0_competitors`,
   `d0_classification`, `d0_diler_group`, `d0_diler_direction`,
   `d0_customer_type`, `d0_server`.
2. **Distributor (regional parent)** — `d0_distributor`, `d0_distr_payment`,
   `d0_distr_comp_details`, `d0_log_distr_balans`.
3. **Money** — `d0_payment`, `d0_cashbox`, `d0_currency`, `d0_comp_details`,
   `d0_log_balans`, `d0_paynet_transaction`, `d0_payme_transaction`,
   `d0_click_transaction`, `d0_services`, `d0_bought_packages`,
   `d0_sms_packages`.
4. **Notification** — `d0_notify_cron`, `d0_notify_bot`, `d0_notification`.
5. **Reference data** — `d0_country`, `d0_city`, `d0_countrysale`.
6. **Bonus calculation** — `d0_quarters`, `d0_quarter_details`,
   `d0_plan_sales`, `d0_month_mentor`.
7. **Operations / audit** — `d0_user`, `d0_user_country`, `d0_access_users`,
   `d0_access_operations`, `d0_access_relations`, `d0_system_log`,
   `d0_active_record_log`, `d0_pivot_template`, `d0_stat_models`,
   `d0_stat_visit`.

---

## Dealer & subscription

### `d0_diler`

The dealer record. This single row IS the tenant in sd-billing's worldview.
Every other table that mentions `DILER_ID` joins back here.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DISTR_ID` | int | FK to `d0_distributor.ID` (regional parent) |
| `COUNTRYSALE_ID` | int | FK to `d0_countrysale.ID` (umbrella country tenancy) |
| `BALANS` | int | Current balance. Adjusted by `Payment::afterSave` and `Diler::changeBalans` |
| `MIN_SUMMA` | float | Minimum balance threshold |
| `MIN_LICENSE` | int | Minimum license count (added m250617_053432) |
| `NAME` | varchar(60) | Display name |
| `FIRM_NAME` | varchar(60) | Legal name |
| `HOST` | varchar(20) | Subdomain — the cross-project join key |
| `DOMAIN` | varchar(200) | Full URL e.g. `https://acme.salesdoc.io` |
| `COUNTRY_ID` | int | FK to `d0_country.ID` |
| `CITY_ID` | int | FK to `d0_city.ID` |
| `CURRENCY_ID` | int | FK to `d0_currency.ID` |
| `GROUP_ID` | int | FK to `d0_diler_group.ID` |
| `TARIFF_ID` | int | FK to `d0_tariff.id` (added m250723_085002) |
| `DIRECTION_ID` | int | FK to `d0_diler_direction.ID` |
| `CUSTOMER_TYPE_ID` | int | FK to `d0_customer_type.ID` |
| `ACTIVE_TO` | date | License-active-to. Sentinel: yesterday means "expired" |
| `STATUS` | int | 0 / 10 / 20 / 30 — none / active / deleted / archive |
| `USER_ID` | int | Responsible manager (FK to `d0_user.USER_ID`) |
| `SALE_ID` | int | Salesman who closed it |
| `INN` | varchar(200) | Tax ID for 1C |
| `CONTACT` | varchar(200) | Free-text contact info |
| `HAS_DISTRIBUTOR` | int | 0 = no, 10 = yes |
| `IS_DEMO` | int | 1 = demo tenant, 0 = paying |
| `FREE_TO` | date | Free-license-to date. Set null when zero by m260428_115900 |
| `ACCESS_BONUS` | int | "Discount months" — 0 / 1 |
| `MONTHLY` | tinyint | Bitmask, default 15 (all packages). Set by m240320_083432 |
| `MIGRATION_ID` | int | Legacy migration tracker |
| `CREDIT_LIMIT` | int | Credit allowance |
| `CREDIT_DATE` | date | Credit expiry. Set null when zero by m260428_115900 |
| `AGREEMENT` | varchar(200) | Contract reference |
| `COMMENT` | varchar(200) | Free-text |
| `COMPETITOR_ID` | int | FK to `d0_competitors.ID`, default 1 (added m240207_103637) |
| `FIRST_SUB_DATE` | date | First subscription date. Nullable, cleaned by m260428_115900 |
| `UPDATED_BY`, `CREATED_BY` | int | FK to `d0_user.USER_ID` |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Primary key**: `ID`.
- **Source migrations**: pre-history, plus `m240207_103637` (COMPETITOR_ID),
  `m250617_053432` (MIN_LICENSE), `m240320_083432` (MONTHLY tinyint),
  `m250723_085002` (TARIFF_ID), `m260428_115900` (zero-date cleanup),
  `m260428_120000` (utf8mb4 conversion).
- **Index**: `idx_diler_distr_hasdist` on `(DISTR_ID, HAS_DISTRIBUTOR)`
  from `m260310_120000`.
- **Model**: `protected/models/Diler.php`.
- **Writers**: `DilerController` (CRUD), `Payment::afterSave` (balance),
  `Subscription::beforeSave` (resets ACTIVE_TO), license-API callbacks.
- **Gotcha 1**: `HOST` was utf8mb3_general_ci until `m260428_120000`. The
  collation mismatch caused intermittent SQLSTATE 1267 errors on MySQL 8.
- **Gotcha 2**: zero dates (`'0000-00-00'`) lurked in `FREE_TO`,
  `CREDIT_DATE`, `FIRST_SUB_DATE`, `ACTIVE_TO`. `m260428_115900` rewrites
  them with sql_mode relaxation; do not store new zero dates.

### `d0_subscription`

A single active dealer subscription. One row per package per period.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `DISTRIBUTOR_ID` | int | Snapshotted from `Diler.distr.ID` in beforeSave |
| `PACKAGE_ID` | int | FK to `d0_package.ID` |
| `SD_USER_ID` | varchar | Tenant-side user receiving the license |
| `COUNT` | int | Quantity (e.g. 5 agent slots) |
| `START_FROM` | date | Period start |
| `ACTIVE_TO` | date | Period end |
| `IS_DELETED` | tinyint | 0 / 1 |
| `ADD_BONUS` | int | Is this subscription eligible for bonus? |
| `SD_USER_LOGIN` | varchar(250) | Optional login slug |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Index**: `idx_sub_diler_deleted_start` on `(DILER_ID, IS_DELETED, START_FROM)`.
- **Model**: `protected/models/Subscription.php`.
- **Writers**: `SubscriptionController`, partner API.
- **Gotcha**: `DISTRIBUTOR_ID` is denormalised from `Diler.DISTR_ID` in
  `beforeSave`. Renaming a dealer's distributor does not retroactively
  rewrite past subscriptions.

### `d0_package`

What a subscription delivers — defines license count, SMS quota, and the
recurring price.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `CURRENCY_ID` | int | FK |
| `SUBSCRIP_TYPE` | varchar(40) | `admin`, `agent`, `merchant`, `dastavchik`, `supervisor`, `vansel`, `seller`, `bot_order`, `bot_report`, `smpro_user`, `smpro_bot` |
| `NAME` | varchar(40) | Display label |
| `AMOUNT` | double | Price per period |
| `PACKAGE_TYPE` | int | 1=paid, 2=free/bonus, 3=demo |
| `CLIENT_TYPE` | int | 1=private, 2=public |
| `TYPE` | smallint | Period length: 1 / 10 / 20 / 30 / 90 / 180 / 360 (days). Changed to SMALLINT by m240307_080831 |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Model**: `protected/models/Package.php`.
- **Writers**: `PackageController`, `DilerBonus::saveLimits`.

### `d0_tariff` (renamed from `d0_group` in m250723_051327)

A pricing tier that bundles multiple packages together.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `name` | varchar(255) | |
| `created_at` | timestamp | DEFAULT CURRENT_TIMESTAMP |

- **Source migrations**: `m250626_124123` (created as `d0_group`),
  `m250723_051327` (renamed to `d0_tariff`).
- **Model**: `protected/modules/operation/models/Tariff.php`.

### `d0_tariff_package` (renamed from `d0_group_package`)

Many-to-many between tariff and package.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `tariff_id` | int | FK to `d0_tariff.id` (was `group_id`) |
| `package_id` | int | FK to `d0_package.ID` |
| `created_at` | timestamp | |

- **Source migrations**: `m250626_123931` (created), `m250723_051326`
  (renamed + column renamed `group_id` → `tariff_id`).
- **Unique index**: `idx_tariff_package_unique` on `(tariff_id, package_id)`.
- **Model**: `protected/modules/operation/models/TariffPackage.php`.

### `d0_diler_package`

Per-dealer assignment of a package, separate from a paid subscription —
used by the bot/SMPro flows.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `PACKAGE_ID` | int | FK |
| `CREATED_AT` | datetime | |

- **Model**: `protected/models/DilerPackage.php`.

### `d0_diler_bonus`

Per-dealer cap on bonus subscription slots, by role.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `AGENT_LIMIT`, `MERCHANT_LIMIT`, `DASTAVCHIK_LIMIT`, `SUPERVISER_LIMIT`, `VANSEL_LIMIT`, `SELLER_LIMIT` | int | Per-role bonus caps |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Model**: `protected/models/DilerBonus.php`. Yes, it confusingly returns
  `'{{diler_bonus}}'` while its `@property` block still mentions
  `{{package}}` — that is a copy-paste relic.

### `d0_dealer_contact`

Multiple human contacts per dealer (decision-maker, finance, etc.).

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `dealer_id` | int | |
| `position` | varchar(200) | |
| `name` | varchar(200) | |
| `phone` | varchar(20) | |

- **Source migration**: `m240604_110458_create_table_contact`.

### `d0_dealer_inns`

Tax IDs the dealer files under (multiple INNs per dealer).

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `dealer_id` | int | |
| `inn` | varchar(200) | |
| `created_at` | datetime | |

- **Source migrations**: `m250325_120304` (created), `m250617_133727`
  (dropped — superseded), but the table is still referenced in the model.
  Note the table was re-introduced under the same name.

### `d0_dealer_origin`

Replacement table — links a successor dealer to the dealer it replaced
(after host migration / restart).

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `origin_id` | int | FK to original `d0_diler.ID` |
| `successor_id` | int | FK to new `d0_diler.ID` |
| `attached_date` | varchar(7) | `YYYY-MM` |

- Unique index on `origin_id` (one successor per origin).
- **Source migration**: `m240515_071438_create_replacement_table`.

### `d0_dealer_key_account`

Tracks which key-account manager owns the dealer in a given month.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `dealer_id` | bigint | |
| `key_account_id` | bigint | FK to `d0_user.USER_ID` |
| `started_month` | varchar(7) | `YYYY-MM` |
| `created_by` | int | |
| `created_at` | timestamp | |

- Unique on `(dealer_id, started_month)`.
- **Source migration**: `m240626_073505_create_dealer_key_account_table`.

### `d0_dealer_blacklist`

Dealers marked as blacklisted (defaulted / suspicious).

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `dealer_id` | int | FK |
| `reason` | varchar(50) | `not_paid_licenses` / `another` |
| `comment` | text | |
| `created_by` | int | |
| `created_at` | datetime | |
| `removed_by` | int | Nullable — null if still blacklisted |
| `removed_at` | datetime | Nullable |

- Index `idx_dealer_id` on `dealer_id`.
- **Source migration**: `m251201_120000_create_dealer_blacklist_table`.

### `d0_competitors`

Competitor master — used to record what software the dealer used before
SalesDoctor.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(200) | |

- **Source migration**: `m240207_103637`. Seeded with: "Не использует
  систему", "Smartup", "Sales Doctor", "Mobi C", "Ritm", "E sale",
  "Своя программа". Same migration adds `COMPETITOR_ID` to `d0_diler`.

### `d0_classification`

Dealer classification tier (A / B / C) based on a numeric range.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `title` | varchar(200) | e.g. "A", "B" |
| `from_value` | int | Lower bound of monthly revenue |
| `to_value` | int | Upper bound |
| `created_by` | int | |
| `created_at` | timestamp | DEFAULT CURRENT_TIMESTAMP |

- **Source migration**: `m240716_084325_create_classification_table`.
- **Model**: `protected/modules/setting/models/Classification.php`.

### `d0_diler_group`, `d0_diler_direction`, `d0_customer_type`

Three simple lookup tables — `ID`, `NAME`, `IS_DELETED`, `CREATED_AT`.
Used as FKs from `d0_diler.GROUP_ID`, `DIRECTION_ID`, `CUSTOMER_TYPE_ID`.

### `d0_server`

The fleet-state row that records the tenant's database connection
information after provisioning.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `diler_id` | int | FK |
| `domain` | varchar(200) | |
| `db_user`, `db_name`, `db_password` | varchar(200) | `db_password` added m250915_091616 |
| `status` | int | 1=new, 2=sent, 3=opened, 5=deleted, 6=archive |
| `db_server`, `web_server`, `web_branch` | varchar(200) | |
| `status_code` | int | HTTP status from provision callback (added m251103_120000) |
| `response_body` | text | Raw provision response (added m251103_120000) |

- **Model**: `protected/models/Server.php`.
- **Writes**: `Diler::createServer()` calls the provisioning API at
  `rwzyzdxaprjaclbcjjgp.salesdoc.io`. `status_code` / `response_body`
  capture the round-trip for debugging.

---

## Distributor

### `d0_distributor`

The regional parent of a group of dealers.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(60) | |
| `DIRECTION` | varchar(255) | |
| `NOT_DISTRIBUTED` | int | Computed unallocated balance |
| `CURRENCY_ID` | int | FK |
| `TYPE` | int | |
| `CITY_ID`, `COUNTRY_ID`, `COUNTRYSALE_ID` | int | FKs |
| `RESPONSIBLE` | int | FK to `d0_user.USER_ID` |
| `INN` | varchar(200) | Tax ID |
| `AGREEMENT` | varchar(200) | |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Model**: `protected/models/Distributor.php`.
- Relation `dilers` filters on `HAS_DISTRIBUTOR = 10`.

### `d0_distr_payment`

A "mirror" of `d0_payment` on the distributor side. Every payment to a
dealer with a distributor gets a paired row here so distributor balance
adds up.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `CASHBOX_ID`, `DISTR_ID`, `CURRENCY_ID` | int | FKs |
| `AMOUNT`, `COMP` | varchar(12) | Stored as decimal-as-string |
| `TYPE` | int | Same enum as `d0_payment.TYPE` |
| `DATE` | date | |
| `COMMENT` | varchar(200) | |
| `IS_DELETED` | tinyint | 0 / 1 |
| `DILER_ID` | int | The dealer who triggered this distributor row |
| `PAYMENT_1C` | varchar(200) | 1C code |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Index**: `idx_distrpay_distr_deleted` on `(DISTR_ID, IS_DELETED)`.
- **Model**: `protected/models/DistrPayment.php`.
- **Gotcha**: `afterSave` modifies `d0_distributor.NOT_DISTRIBUTED` —
  bypassing it via `saveWithoutAfterSave()` skips that math.

### `d0_distr_comp_details`

Distributor-side debt computation trail — who paid whom on behalf of whom.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DISTR_ID` | int | The distributor whose balance moved |
| `FROM_ID`, `TO_ID` | int | Source and target reference IDs |
| `AMOUNT` | int | |
| `CREATED_BY` | int | |
| `CREATED_AT` | datetime | |

### `d0_log_distr_balans`

Audit-trail of distributor balance changes.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DISTR_ID` | int | |
| `SUMMA` | varchar(12) | Decimal-as-string |
| `USER_ID` | int | Who triggered it |
| `CREATED_AT` | datetime | |

---

## Money

### `d0_payment`

Every money-in row. The single most-written table in sd-billing.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `CASHBOX_ID` | int | FK to `d0_cashbox.ID` (0 = no cashbox, e.g. service payments) |
| `DILER_ID` | int | FK |
| `DISTRIBUTOR_ID` | int | Current distributor of the dealer (snapshot at payment time) |
| `CURRENCY_ID` | int | FK |
| `AMOUNT` | double | |
| `DISCOUNT` | double | |
| `COMP` | double | Computation amount |
| `TYPE` | int | See enum below |
| `DATE` | date | |
| `COMMENT` | varchar(200) | |
| `IS_DELETED` | tinyint | 0 / 1 |
| `SUBSCRIPTION_ID` | int | Optional FK back to `d0_subscription.ID` |
| `DISTR_ID` | int | The distributor THIS payment was routed through (used in Распределение) |
| `DISTR_PAYMENT_ID` | int | FK to `d0_distr_payment.ID` mirror row |
| `PAYMENT_1C` | varchar(200) | 1C code |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

`TYPE` enum (from `Payment` class constants):

- 1 = `TYPE_CASH` — Нал
- 2 = `TYPE_CASHLESS` — Безнал
- 3 = `TYPE_P2PCLICK` — P2P Click
- 10 = `TYPE_LICENSE` — Licence allocation
- 11 = `TYPE_DISTRIBUTE` — Распределение (routes through DISTR_ID)
- 12 = `TYPE_PAYMEONLINE` — Payme online
- 13 = `TYPE_CLICKONLINE` — Click online
- 14 = `TYPE_SERVICE` — Service / dev work payment
- 15 = `TYPE_PAYNETONLINE` — Paynet online
- 16 = `TYPE_MBANK` — MBANK for KG

- **Index**: `idx_pay_diler_deleted` on `(DILER_ID, IS_DELETED)`.
- **Model**: `protected/models/Payment.php`.
- **Writers**: `PaymentController`, `Service::afterSave` (for `TYPE_SERVICE`),
  Payme/Click/Paynet callbacks in `protected/modules/api/`.
- **Trigger note**: `m221114_070346_create_triggers_to_payment` defines an
  `AfterInsertToPayment` trigger that recomputes `d0_diler.BALANS`, but the
  migration's `$this->execute($sql)` is commented out — the comment marks
  it as "xato ishlayapti" (working incorrectly). Balance is maintained in
  PHP via `Payment::afterSave` instead.
- **Gotcha**: `DISTRIBUTOR_ID` and `DISTR_ID` are not the same column.
  The first is "current distributor of the dealer"; the second is
  "the distributor this specific payment is routed through".

### `d0_cashbox`

Vendor cashier register.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(250) | |
| `USER_ID` | int | Cashier assigned |
| `CODE` | varchar(200) | |
| `IS_DELETED` | tinyint | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |
| `UPDATED_BY`, `CREATED_BY` | int | |

- **Model**: `protected/modules/cashbox/models/Cashbox.php`.
- Constant `Cashbox::CASHBOX_NONE = 0` is reserved for service-only payments.

### `d0_currency`

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | string | "UZS", "USD", "KZT", "KGS" |
| `SHORT` | string | Symbol |
| `CODE` | int | ISO-4217 |
| `RATE` | int | Last FX rate against base |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

### `d0_comp_details`

Debt computation trail at dealer level (the dealer-side mirror of
`d0_distr_comp_details`).

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `FROM_ID`, `TO_ID` | int | Reference IDs |
| `AMOUNT` | int | |
| `CREATED_BY` | int | |
| `CREATED_AT` | datetime | |

### `d0_log_balans`

Audit-trail of dealer balance changes — every adjustment to `d0_diler.BALANS`.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `USER_ID` | int | Who triggered |
| `SUMMA` | int | Delta |
| `CREATED_AT` | datetime | |

- **Model**: `protected/models/LogBalans.php` — note the model docblock
  still references `{{diler}}` (stale copy).
- Written by `Diler::changeBalans()`.

### `d0_paynet_transaction`

Paynet callback trail.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `transaction_id` | bigint | |
| `amount` | double(16,2) | |
| `host` | varchar(200) | Dealer host |
| `timestamp` | datetime | |
| `status` | tinyint | |
| `payment_id` | int | FK to `d0_payment.ID` |
| `updated_at`, `created_at` | timestamp | |

- **Source migration**: `m220317_063421_create_paynet_transaction_table`.

### `d0_payme_transaction`

Payme callback trail. States: 1=created, 2=completed, -1=cancelled,
-2=cancelled_after_complete.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `DILER_ID` | int | FK |
| `HOST` | varchar | |
| `STATUS` | int | |
| `AMOUNT` | int | In tiyin |
| `TRANS_ID` | varchar | Payme transaction ID |
| `TRANS_CREATE_TIME`, `TRANS_PERFORM_TIME`, `TRANS_CANCEL_TIME` | datetime | |
| `PAYMENT_ID` | int | FK |
| `REASON` | int | |

### `d0_click_transaction`

Click callback trail.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `TRANS_ID` | int | Click side ID |
| `PAYDOC_ID` | int | |
| `AMOUNT` | int | |
| `STATUS` | int | 0=prepare, 1=complete, 2=cancelled |
| `DILER_ID` | int | FK |
| `HOST` | varchar | |
| `CREATE_AT`, `UPDATE_AT` | datetime | |

### `d0_services`

Custom development / one-off services billed to a dealer or distributor.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(200) | |
| `DESCRIPTION` | text | |
| `EXPIRE_DATE` | date | |
| `TYPE` | int | 1=Diler, 2=Distributor |
| `OBJECT_ID` | int | Polymorphic — points at dealer OR distributor based on `TYPE` |
| `CATEGORY_ID` | int | 1..8 (Накладной / Загруз-зав.Склад / Отчет / Интеграция / Акт-Сверки / Доп. Функционал / Прочие / Смс пакет) |
| `STATUS` | int | 1=new, 2=in_progress, 3=test, 4=done |
| `IS_DELETED` | tinyint | |
| `PAYMENT_ID` | int | FK — only set after STATUS = done |
| `PRICE` | double | |
| `FILE` | varchar(200) | Uploaded TZ file |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- **Model**: `protected/models/Service.php`.
- **Gotcha**: `Service::afterSave` auto-creates a matching `d0_payment` or
  `d0_distr_payment` row with `TYPE = TYPE_SERVICE = 14` once `STATUS`
  reaches DONE. Deleting the service un-deletes/deletes the payment too.

### `d0_sms_packages`, `d0_bought_packages`

SMS pack catalog and per-dealer purchases. `SmsPackage` has `NAME, COUNT,
PRICE, CURRENCY_ID, SORT, IS_DELETED`. `BoughtPackage` has `PACKAGE_ID,
TYPE, OBJECT_ID, BOUGHT_ID, SERVICE_ID, AMOUNT, IS_DELETED`.

---

## Notification

### `d0_notify_cron`

Async outbound notification queue. Picked up by `NotifyCommand`.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `chat_id` | bigint | Telegram chat OR `0` for non-Telegram |
| `bot_id` | int nullable | FK to `d0_notify_bot.id` (added m260420_120001) |
| `text` | text utf8mb4 | Payload; emoji-safe since m260420_120002 |
| `parse_mode` | varchar(16) | Default `HTML` (added m260421_120005) |
| `type` | varchar(32) | `telegram` / `license_delete` / `visit_write` (added m260422_120006) |
| `status` | tinyint | 0=default, 1=run |
| `error_response` | text nullable | (added m260422_120006) |
| `created_by` | int | |
| `created_at` | timestamp | |

- **Indexes**: `idx_notify_cron_bot_id` on `bot_id`,
  `idx_notify_cron_status_type` on `(status, type)`.
- **Model**: `protected/models/NotifyCron.php` (factory methods
  `create`, `createLicenseDelete`).
- **Gotcha**: charset was utf8mb3 originally — `m260420_120002` converted
  the whole table to utf8mb4 because emoji payloads from `TLogger` were
  failing with SQLSTATE HY000 / 1366. Do not roll back without truncation.

### `d0_notify_bot`

Catalog of Telegram bots the platform sends from.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `name` | varchar(50) unique | `default`, `billing`, `password_reset`, `sd_token` (and dropped: `dashboard`, `cleaner`) |
| `token` | varchar(255) | Bot token |
| `api_url` | varchar(255) | `https://api.telegram.org/bot<token>/` |
| `created_at` | timestamp | |

- **Source migrations**: `m260420_120000` (created + seeded 5 bots),
  `m260421_120003` (dropped `dashboard`).
- **Model**: `protected/models/NotifyBot.php` — lookup by name via
  `NotifyBot::idByName('billing')`.

### `d0_notification`

In-app bell — alerts shown on the dealer's portal.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `TITLE` | varchar(200) utf8mb4 | |
| `TYPE` | int | 1=news, 2=alert, 3=warning, 4=tally |
| `PREVIEW` | varchar(255) utf8mb4 | |
| `DETAIL` | text utf8mb4 | |
| `STATUS` | int | 1=new, 2=in_process, 3=sent |
| `DISTR_IDS`, `DILER_IDS`, `CURRENCIES`, `ROLES` | varchar | Comma-separated targeting |
| `AUTO` | string | Schedule cron-spec |
| `IS_DELETED` | tinyint | 0/1 |
| `CREATED_BY`, `UPDATED_BY` | int | |
| `CREATED_AT`, `UPDATED_AT` | datetime | |

- Converted to utf8mb4 by `m251028_115044`.
- **Model**: `protected/models/Notification.php`.

---

## Reference data

### `d0_country`

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(60) | |
| `CODE` | varchar(10) | ISO-3166 alpha-3 (added m230221_062735, default 'UZB') |
| `LOCAL_CODE` | varchar(200) | Internal grouping code, e.g. `smpro` / `sdpro` (added m240801_105334) |

### `d0_city`

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(60) | |
| `COUNTRY` | int | FK to `d0_country.ID` (column is `COUNTRY`, not `COUNTRY_ID`) |
| `LOCAL_CODE` | varchar(200) | Added m240801_110321 |
| `TIMEZONE` | string | e.g. `Asia/Tashkent` |

### `d0_countrysale`

Umbrella country-level tenancy — owns multiple distributors, holds the
country-database hostname.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME`, `FIRM_NAME`, `HOST`, `DOMAIN` | varchar | |
| `STATUS` | int | 0/1 |
| `DB_USER`, `DB_COUNTRY`, `DB_FILIAL` | varchar(200) | Connection metadata |
| `HOST_FILIAL` | varchar(200) | Where dealer hosts are provisioned |
| `DB_SERVER` | varchar(200) | DB host |
| `CREATED_BY`, `UPDATED_BY` | int | |
| `CREATED_AT`, `UPDATED_AT` | datetime | |

---

## Bonus calculation

### `d0_quarters`

Bonus quarters master.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `NAME` | varchar(200) | "Q1 2025" |
| `IS_DELETED` | tinyint | |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

- `m220210_095227` dropped `LOW` and `HIGHT` columns from this table.

### `d0_quarter_details`

Per-quarter percent / bonus breakdown.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `QUARTER_ID` | int | FK |
| `NAME` | string | |
| `PERCENT` | float(10,2) | |
| `BONUS` | float(10,2) | |

- **Source migration**: `m220210_101636_create_quarter_detail_table`.

### `d0_plan_sales`

Per-salesman targets per quarter per country.

| Column | Type | Notes |
|---|---|---|
| `ID` | int PK | |
| `QUARTER_ID` | int | FK |
| `SALE_ID` | int | FK to `d0_user.USER_ID` |
| `AMOUNT` | varchar(16) | Decimal-as-string |
| `QUANTITY` | int | Target dealer count |
| `DATE` | date | |
| `COUNTRY_ID` | int | |
| `UPDATED_BY`, `CREATED_BY` | int | |
| `UPDATED_AT`, `CREATED_AT` | datetime | |

### `d0_month_mentor`

Monthly mentor-bonus tracking. One row per dealer per month.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `dealer_id` | int | |
| `mentor_id` | int | FK to `d0_user.USER_ID` |
| `month` | varchar(7) | `YYYY-MM` |

- Unique on `(dealer_id, month)`.
- **Source migration**: `m240624_082759`.

---

## Operations & audit

### `d0_user`

Internal SalesDoctor staff.

| Column | Type | Notes |
|---|---|---|
| `USER_ID` | int PK | (Yes — `USER_ID`, not `ID`) |
| `NAME` | varchar | |
| `ROLE` | int | 3=admin, 4=manager, 5=operator, 6=api, 7=sale, 8=mentor, 9=key_account, 10=partner |
| `LOGIN` | varchar(50) | |
| `PASSWORD` | varchar(200) | md5 |
| `PHONE_NUMBER` | varchar(200) | |
| `CHAT_ID` | int | Telegram chat ID |
| `ACTIVE` | int | 1/0 |
| `IS_ADMIN` | int | Super-admin flag |
| `ACCESS_CASHBOX` | int | "Access all cashboxes" override |
| `TOKEN` | varchar(200) | API token |
| `LAST_AUTH` | datetime | |

- **Migration**: `m240222_071158` dropped the old `COUNTRY_ID` column —
  multi-country mapping moved to `d0_user_country`.

### `d0_user_country`

Country scope per user (many-to-many).

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `user_id` | int | FK |
| `country_id` | int | FK |

### `d0_access_users`, `d0_access_operations`, `d0_access_relations`

The RBAC tables.

`d0_access_operations` — every defined permission.

| Column | Type | Notes |
|---|---|---|
| `operations` | varchar(200) | e.g. `operation.dealer.payment` |
| `name` | varchar(200) | Russian label |
| `type` | enum('operation','role','task') | |
| `accessable` | tinyint(2) | Bitmask `SHOW=1 / CREATE=2 / UPDATE=4 / DELETE=8`, default 15 (added m240223_093521) |

Unique: `operation_unique` on `operations`.

`d0_access_users` — per-user operation grants.

| Column | Type | Notes |
|---|---|---|
| `user_id` | bigint | FK |
| `access` | tinyint | Bitmask |
| `operations` | varchar(200) | FK to `d0_access_operations.operations` |

Unique: `user_unique` on `(user_id, operations)`.

`d0_access_relations` — role / task hierarchy.

| Column | Type | Notes |
|---|---|---|
| `parent` | varchar(200) | |
| `child` | varchar(200) | |

- **Source migrations**: `m220422_090150` (created), `m220422_092441`
  (unique constraints), `m240223_093521` (`accessable`), plus seven later
  migrations that insert specific operations
  (`m220426_105355`, `m250218_100000`, `m250618_063630`,
  `m250630_085201`, `m250707_104841`, `m250805_084724`, `m251104_130000`).

### `d0_system_log`

Page-visit audit log.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `path` | varchar | URL |
| `user_id` | int | |
| `user_os`, `user_browser`, `user_ip` | varchar | |
| `content` | text | |

### `d0_active_record_log`

Generic before/after diff log of any model that includes
`ActiveRecordLogableBehavior` — currently `Diler` only.

| Column | Type | Notes |
|---|---|---|
| `id` | string | |
| `description` | varchar(255) | |
| `action` | varchar(20) | `CREATED` / `CHANGE` / `DELETE` |
| `model` | varchar(45) | e.g. `Diler` |
| `idModel` | varchar(10) | PK value |
| `field`, `oldValue`, `newValue` | varchar(45) | |
| `creationdate` | datetime | |
| `userid` | varchar(45) | |

### `d0_pivot_template`

Saved pivot-table templates for the reports module.

| Column | Type | Notes |
|---|---|---|
| `id` | int PK | |
| `title` | varchar(200) | |
| `template` | text | JSON config |
| `created_by` | int | |
| `created_at` | timestamp | |

- **Source migration**: `m240704_092207`.

### `d0_stat_models`, `d0_stat_visit`

Daily roll-ups pulled from each dealer's sd-cs for cross-tenant analytics.

`d0_stat_models`: `id, dilerId, quantity, model, day`.
`d0_stat_visit`: `id, dilerId, visit, role, visited, orders, reject, photo,
agentId, userId, day, lastVisit`.

---

## Migration index

All 55 migrations, chronological, one-line each.

| Migration | Effect |
|---|---|
| `m220210_085952` | Drop `d0_sale_bonus` |
| `m220210_092559` | Drop `d0_given_bonus` |
| `m220210_095227` | Drop `LOW`, `HIGHT` from `d0_quarters` |
| `m220210_101636` | Create `d0_quarter_details` |
| `m220317_063421` | Create `d0_paynet_transaction` |
| `m220422_090150` | Create `d0_access_users`, `d0_access_operations`, `d0_access_relations` |
| `m220422_092441` | Unique constraints on access tables |
| `m220426_105355` | Seed 3 dealer ops into `d0_access_operations` |
| `m221114_070346` | Payment balance trigger DDL (execute commented — no-op) |
| `m230221_062735` | Add `CODE` to `d0_country` (default 'UZB') |
| `m231205_113008` | Drop `d0_page_analytics` |
| `m240207_103637` | Create `d0_competitors`, seed 7 rows, add `COMPETITOR_ID` to `d0_diler` |
| `m240222_071158` | Drop `COUNTRY_ID` from `d0_user` |
| `m240223_093521` | Add `accessable` (default 15) to `d0_access_operations` |
| `m240305_125428` | Create `d0_package_group` (later dropped) |
| `m240307_080831` | `d0_package.TYPE` → SMALLINT |
| `m240307_105102` | Drop `d0_package_group` |
| `m240320_083432` | `d0_diler.MONTHLY` → tinyint(2) default 15 |
| `m240515_071438` | Create `d0_dealer_origin` |
| `m240604_110458` | Create `d0_dealer_contact` |
| `m240614_091729` | Create `d0_notify_cron` |
| `m240624_082759` | Create `d0_month_mentor` |
| `m240626_073505` | Create `d0_dealer_key_account` |
| `m240704_092207` | Create `d0_pivot_template` |
| `m240716_084325` | Create `d0_classification` |
| `m240801_105334` | Add `LOCAL_CODE` to `d0_country` |
| `m240801_110321` | Add `LOCAL_CODE` to `d0_city` |
| `m250218_100000` | Seed `operation.partner.subscription`, `operation.partner.payment` |
| `m250325_120304` | Create `d0_dealer_inns` |
| `m250617_053432` | Add `MIN_LICENSE` to `d0_diler` |
| `m250617_133727` | Drop `d0_dealer_inns` |
| `m250618_063630` | Seed `operation.dealer.min.license` |
| `m250626_123931` | Create `d0_group_package` (idempotent) |
| `m250626_124123` | Create `d0_group` |
| `m250630_085201` | Seed `operation.report.clients.by.packages` |
| `m250707_104841` | Seed `operation.dealer.package.index` |
| `m250723_051326` | Rename `d0_group_package` → `d0_tariff_package`, `group_id` → `tariff_id` |
| `m250723_051327` | Rename `d0_group` → `d0_tariff` |
| `m250723_085002` | Add `TARIFF_ID` to `d0_diler` |
| `m250805_084724` | Seed `operation.tariff.index` |
| `m250915_091616` | Add `db_password` to `d0_server` |
| `m251028_115044` | Convert `d0_notification` to utf8mb4 |
| `m251103_120000` | Add `status_code`, `response_body` to `d0_server` |
| `m251104_130000` | Seed `operation.partner.dealer`, `operation.partner.report.subscription` |
| `m251201_120000` | Create `d0_dealer_blacklist` |
| `m260310_120000` | 4 indexes for the license-API hot path |
| `m260420_120000` | Create `d0_notify_bot` + seed 5 bots |
| `m260420_120001` | Add `bot_id` to `d0_notify_cron` |
| `m260420_120002` | Convert `d0_notify_cron` to utf8mb4 |
| `m260421_120003` | Remove `dashboard` bot |
| `m260421_120004` | Drop `d0_telegram_group` |
| `m260421_120005` | Add `parse_mode` to `d0_notify_cron` |
| `m260422_120006` | Add `type`, `error_response` to `d0_notify_cron` + composite index |
| `m260428_115900` | Replace '0000-00-00' in `d0_diler` date columns |
| `m260428_120000` | Convert `d0_diler` to utf8mb4_unicode_ci |

---

## Cross-project touchpoints

- `d0_diler.HOST` is the same string that appears as filial id (or the
  hostname half of one) in sd-main and sd-cs. It is the join key for every
  cross-project lookup. Per the
  [tenant lifecycle](/docs/concepts/license-tenant-lifecycle) doc, the
  provisioning flow is sd-billing creates the `d0_diler` row,
  `Diler::createServer()` POSTs to `rwzyzdxaprjaclbcjjgp.salesdoc.io`,
  which spins up the dealer's sd-cs / sd-main DBs and reports back via the
  `status_code` / `response_body` columns of `d0_server`.
- `d0_subscription.SD_USER_ID` / `SD_USER_LOGIN` refer to a user on the
  dealer's sd-cs, NOT to `d0_user.USER_ID`. There is no FK — the link is
  best-effort.
- License push: when a payment is recorded with `TYPE_LICENSE` (10), the
  `d0_subscription.ACTIVE_TO` is recomputed in `Diler::resetActiveLicense`
  and a `d0_notify_cron` row of `type=license_delete` is enqueued. The
  cron then posts to the dealer's sd-cs to invalidate the cached license.
- sd-main's per-dealer `filial` concept matches one `d0_diler` row.
  `d0_diler.COUNTRYSALE_ID` maps the dealer up to a country-database
  (`d0_countrysale.DB_COUNTRY`, `DB_FILIAL`).

## Gotchas

1. **`d0_diler.HOST` collation**: until April 2026 this column was
   utf8mb3_general_ci. Mixing it in WHERE clauses with utf8mb4 parameters
   raised SQLSTATE HY000 / 1267 on MySQL 8 default install. Migration
   `m260428_120000` fixes it.
2. **Zero dates in `d0_diler`**: `'0000-00-00'` lurked in `FREE_TO`,
   `CREDIT_DATE`, `FIRST_SUB_DATE`, `ACTIVE_TO`. Strict-mode MySQL 8
   rejects them. `m260428_115900` cleans up and uses session-level
   `sql_mode = ''` to do so. Do not insert zero dates afterwards — the
   model layer will not protect you.
3. **`d0_payment` balance triggers are dead code**:
   `m221114_070346_create_triggers_to_payment` defines a procedure +
   triggers but its `execute()` is commented out as broken. Balance is
   maintained by `Payment::afterSave` PHP, not SQL.
4. **Two `DISTR_*` columns on `d0_payment`**: `DISTRIBUTOR_ID` is the
   dealer's current distributor snapshot. `DISTR_ID` is the distributor
   THIS payment was routed through (used in Распределение). They are
   often equal but not always.
5. **`d0_diler_bonus` model docblock is stale**: the model file
   `DilerBonus.php` still mentions `{{package}}` in its header docblock
   while its `tableName()` returns `{{diler_bonus}}`. The table is
   `d0_diler_bonus`.
6. **`d0_dealer_inns` was created, dropped, re-introduced**: migrations
   `m250325_120304` and `m250617_133727`. The current model
   `DealerInn.php` returns `{{dealer_inns}}` so a re-creation lives
   somewhere outside the migration history.
7. **`d0_notify_cron` charset**: emoji-bearing logs (💳 🌐 💸 💰 from
   `TLogger::billingLog`) require the utf8mb4 conversion. Do not roll
   that migration back on production data.
8. **`d0_services` is polymorphic**: `OBJECT_ID` points at `d0_diler.ID`
   when `TYPE = TYPE_DILER (1)` and at `d0_distributor.ID` when
   `TYPE = TYPE_DISTR (2)`. No FK enforces this. `Service::getObject()`
   does the routing.
9. **Direct cashbox = 0 means "no cashbox"**: payments with
   `CASHBOX_ID = 0` are system-driven (service work, subscription auto).
   Do not treat 0 as "missing FK".
10. **The `Cashbox::CASHBOX_NONE` constant** is the convention; using a
    NULL `CASHBOX_ID` will fail validation rules on `d0_payment`.
11. **`d0_user.USER_ID` not `ID`**: most other tables use `ID` as PK —
    `d0_user` is the holdout. When writing JOINs remember `ON p.CREATED_BY
    = u.USER_ID`.

## See also

- [/docs/sd-billing/overview](/docs/sd-billing/overview) — module map.
- [/docs/sd-billing/modules/operation](/docs/sd-billing/modules/operation) —
  the controllers that write `d0_payment`, `d0_subscription`.
- [/docs/sd-billing/modules/notification](/docs/sd-billing/modules/notification) —
  how `d0_notify_cron` / `d0_notify_bot` are consumed.
- [/docs/sd-billing/workflows/operation-payment](/docs/sd-billing/workflows/operation-payment) —
  end-to-end of a payment row's life.
- [/docs/sd-billing/workflows/operation-subscription](/docs/sd-billing/workflows/operation-subscription) —
  same for a subscription.
- [/docs/sd-billing/workflows/api-click](/docs/sd-billing/workflows/api-click) —
  how `d0_click_transaction` rows arrive.
- [/docs/data/conventions](/docs/data/conventions) — naming, casing, and FK
  conventions across the whole SalesDoctor data layer.
- [/docs/data/schema-reference](/docs/data/schema-reference) — the
  dealer-side (sd-cs / sd-main) counterpart.
- [/docs/concepts/license-tenant-lifecycle](/docs/concepts/license-tenant-lifecycle) —
  how a `d0_diler` row becomes a live tenant.
