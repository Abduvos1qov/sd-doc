---
sidebar_position: 8
title: operation · Package management
---

# operation · Package management

## 1. Purpose

The Package management feature is the catalog editor for every billing
package the system can sell. A package is the smallest priced unit a
dealer can subscribe to — it carries a price, a duration (`TYPE`), a
target role (`SUBSCRIP_TYPE` — admin / agent / merchandiser / …), and a
visibility flag (`PACKAGE_TYPE` paid / bonus / demo and `CLIENT_TYPE`
private / public). Operators and managers use this screen to publish new
packages, fix pricing for a country, or retire a SKU. Two distinct
catalogs share the same `d0_package` table: the classic dealer packages
(handled by `PackageController`) and the SMPro variants
(`PackageSMProController`), separated by `SUBSCRIP_TYPE`.

---

## 2. Who uses it

| Role | Access key | Capability |
|------|-----------|------------|
| Admin (`IS_ADMIN = 1`) | `operation.package.index` / `operation.package.smpro` | Full CRUD on both catalogs |
| Operator (ROLE = 5) | `operation.package.index` | CRUD on classic packages subject to bitmask |
| Manager (ROLE = 4) | `operation.package.index` | Typically SHOW; CRUD only if explicitly granted |
| Key-account (ROLE = 9) | `operation.package.index` | Read-only for pricing reference |

Access is checked per action via `Access::check('operation.package.index', Access::SHOW/CREATE/UPDATE/DELETE)` for classic packages and `Access::check('operation.package.smpro', …)` for SMPro packages.

---

## 3. Where it lives

| Item | Path |
|------|------|
| Classic controller | `protected/modules/operation/controllers/PackageController.php` |
| SMPro controller | `protected/modules/operation/controllers/PackageSMProController.php` |
| Model | `protected/models/Package.php` |
| Per-dealer override model | `protected/models/DilerPackage.php` |
| URL (classic) | `/operation/package/index` |
| URL (SMPro) | `/operation/packageSMPro/index` |

Actions exposed by each controller:

| Action | Method | Access constant |
|--------|--------|-----------------|
| `actionIndex` | GET | SHOW |
| `actionGetData` | POST | SHOW |
| `actionCreateOrUpdate` | POST | CREATE or UPDATE (decided per-record) |
| `actionDeleteOne` | POST | DELETE |

The classic `actionGetData` filter is `WHERE p.SUBSCRIP_TYPE NOT IN ('smpro_user', 'smpro_bot')`; the SMPro controller inverts that filter (`IN`). The two screens never overlap.

---

## 4. Workflow

```mermaid
sequenceDiagram
  participant U as Operator
  participant FE as Browser (Vue)
  participant C as PackageController
  participant DB as MySQL

  U->>FE: Opens /operation/package/index
  FE->>C: GET actionIndex
  C->>DB: Load currencies, types, clientTypes, packageTypes, subTypes
  C-->>FE: Render page with dropdowns + dynamic options
  FE->>C: POST actionGetData
  C->>DB: SELECT p.*, NOT EXISTS(subscription WHERE PACKAGE_ID=p.ID) AS changeable
  C-->>FE: JSON list (price, type label, changeable flag)
  U->>FE: Add / edit / delete
  FE->>C: POST actionCreateOrUpdate or actionDeleteOne
  C->>DB: BEGIN; validate; save / delete; COMMIT
  C-->>FE: {"success": true}
```

### 4a. Create / update

1. Operator clicks **Add package** or selects an existing row.
2. Browser POSTs to `actionCreateOrUpdate` with `id` (null for new), `name`, `currency_id`, `type` (one of `getTypes()` — 10, 20, 30, 90, 180, 360 days), `stype` (one of `getSubscripTypes()`), `ctype` (`CLIENT_PRIVATE` or `CLIENT_PUBLIC`), `ptype` (`PACKAGE_PAID`, `PACKAGE_FREE`, `PACKAGE_DEMO`), and `amount`.
3. Controller validates currency, type, stype, ctype, ptype membership; rejects `ptype = PACKAGE_PAID` with `amount <= 0`.
4. For updates, a duplicate-check loop runs: for every `DilerPackage` linked to this package, it scans the dealer's other `DilerPackage` rows and rejects if another package has the same `TYPE` + `SUBSCRIP_TYPE` (different ID). This stops the same dealer from getting two equivalent overrides.
5. New records get `CREATED_BY = current user`; updates stamp `UPDATED_BY`. `Package::beforeSave` zeroes `AMOUNT` when `PACKAGE_TYPE != PACKAGE_PAID`.
6. Transaction commits and the browser refreshes the list.

### 4b. Delete

1. Operator clicks **Delete**.
2. Browser POSTs to `actionDeleteOne` with `{id}`.
3. Controller refuses if the package's `SUBSCRIP_TYPE` is outside the allowed set for the screen (SMPro types cannot be deleted from the classic screen and vice versa).
4. Controller refuses if any `Subscription` row references `PACKAGE_ID = id`. This is a hard delete; once a subscription has been sold, the package is permanent.
5. On success, `$package->delete()` removes the row; transaction commits.

### 4c. SMPro variant

The SMPro screen is functionally identical but locked to two stypes (`SUBSCRIP_SMPRO_USER`, `SUBSCRIP_SMPRO_BOT`), always sets `PACKAGE_TYPE = PACKAGE_PAID` and `CLIENT_TYPE = CLIENT_PRIVATE`, and uses a different access key (`operation.package.smpro`). Types come from `Package::getSMProTypes()` which adds `TYPE_DAY = 1` to the standard duration list.

---

## 5. Rules

- `SUBSCRIP_TYPE` must be one of the 11 keys in `Package::getSubscripTypes("all")`: `admin`, `agent`, `merchant`, `dastavchik`, `supervisor`, `vansel`, `seller`, `bot_report`, `bot_order`, `smpro_user`, `smpro_bot`. The classic screen rejects the two `smpro_*` keys; the SMPro screen only accepts those two.
- `TYPE` must be one of `getTypes()` (`10`, `20`, `30`, `90`, `180`, `360`) for classic packages, or `getSMProTypes()` (adds `1`) for SMPro.
- `PACKAGE_TYPE = PACKAGE_PAID (1)` with `AMOUNT <= 0` is rejected. `PACKAGE_FREE (2)` and `PACKAGE_DEMO (3)` always force `AMOUNT = 0` via `Package::beforeSave`.
- `CLIENT_TYPE = CLIENT_PRIVATE (1)` packages are only visible to dealers who have a matching `DilerPackage` override row; `CLIENT_PUBLIC (2)` packages are visible to every dealer in that currency. The `api/license/packages` lookup queries with `CLIENT_TYPE = 2 AND PACKAGE_TYPE = 1` for the public list.
- Updates run a duplicate guard: for every dealer linked via `DilerPackage`, no two packages with the same `(TYPE, SUBSCRIP_TYPE)` may co-exist for that dealer.
- Delete is **hard** (`$package->delete()`), but only allowed when no `Subscription` references it. There is no soft-delete column on `d0_package`.
- The list query exposes a `changeable` boolean derived from `NOT EXISTS (SELECT 1 FROM subscription WHERE PACKAGE_ID = p.ID)`. The UI uses this to disable edits to in-use packages even before submission.
- `bot_report` packages have a tiered price computed at sell-time by `Package::getBotPackages()` (per-country, per-duration table baked into the model). The `AMOUNT` written to `d0_package` is the headline price and may be overridden by a `DilerPackage` row carrying a flat per-dealer amount.

---

## 6. Data sources

| Table | DB / connection | Why read |
|-------|-----------------|----------|
| `d0_package` | sd-billing default DB | Primary entity — listed, created, updated, deleted |
| `d0_currency` | sd-billing default DB | Currency dropdown; FK target of `Package.CURRENCY_ID` |
| `d0_subscription` | sd-billing default DB | `changeable` flag (cannot edit if a subscription references the row); delete guard |
| `d0_diler_package` | sd-billing default DB | Per-dealer overrides — read during the duplicate guard on update |

---

## 7. Gotchas

**Two screens, one table.** Classic and SMPro packages share `d0_package` and are separated only by `SUBSCRIP_TYPE`. Mass renames or migrations that touch the table must respect both screens' invariants.

**`changeable = false` only blocks the UI, not the controller.** The controller has no equivalent "in-use" guard for *updates*. A direct POST to `actionCreateOrUpdate` with an in-use package ID will succeed and silently re-price existing subscriptions' future renewals. Only **delete** is enforced server-side via the `Subscription::findByAttributes(["PACKAGE_ID" => …])` check.

**The duplicate guard is one-way.** `actionCreateOrUpdate` rejects a save if it would create a duplicate `(TYPE, SUBSCRIP_TYPE)` against any dealer's `DilerPackage`. But `DilerPackage` itself has no equivalent check — adding a duplicate via the relation controller bypasses this.

**`bot_report` price is *not* the price clients pay.** `Package.AMOUNT` for `SUBSCRIP_BOT_REPORT` rows is a headline value; the actual amount written to `Payment.AMOUNT` is resolved at subscription-create time via `Package::getBotPackages($diler, $amount, $type)`, which returns a tiered table keyed by quantity, country, and duration. Editing the package's `AMOUNT` does not retroactively update existing subscriptions.

**Downstream consumers.** Packages are referenced by `Subscription.PACKAGE_ID`, `DilerPackage.PACKAGE_ID`, and `TariffPackage.package_id`. Adding a new package immediately exposes it in:
1. The dashboard subscription create flow (`SubscriptionCreateAction`).
2. The `/api/license/packages` lookup that `sd-main` calls at login.
3. The tariff editor's package picker (`TariffController`).

---

## 8. See also

- [Tariff plans](./operation-tariff.md) — groups packages into a sellable bundle assignable to a dealer.
- [Subscription lifecycle](./operation-subscription.md) — consumes `Package` rows to issue subscriptions.
- [Domain model](../domain-model.md) — `Package`, `Subscription`, `DilerPackage`, `Tariff` schemas.
- Source: `protected/modules/operation/controllers/PackageController.php` and `PackageSMProController.php`
