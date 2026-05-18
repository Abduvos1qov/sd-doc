---
sidebar_position: 9
title: operation · Tariff plans
---

# operation · Tariff plans

## 1. Purpose

A tariff is a named bundle of packages used as a default offer for a
dealer. It exists so the sales team can say "this dealer is on Tariff
*Standard*" instead of attaching individual packages one-by-one. The
tariff record itself is lightweight (`id`, `name`, `created_at`) and
the body of the bundle lives in `d0_tariff_package`, a simple
many-to-many bridge to `d0_package`. Dealers reference a tariff via
`Diler.TARIFF_ID`, and the subscription-creation flow uses that link as
a starting point when offering packages to that dealer.

---

## 2. Who uses it

| Role | Access key | Permitted operations |
|------|-----------|----------------------|
| Admin (`IS_ADMIN = 1`) | `operation.tariff.index` | All four operations |
| Operator (ROLE = 5) | `operation.tariff.index` | Subject to bitmask grant |
| Manager (ROLE = 4) | `operation.tariff.index` | Typically SHOW; CRUD only if explicitly granted |

Permission is checked via `Access::check('operation.tariff.index', $type)` inside each action's `authorize()` call where `$type` is one of:

| Constant | Value | Required by |
|----------|-------|-------------|
| `Access::SHOW` | 4 | `list` |
| `Access::CREATE` | 1 | `create` |
| `Access::UPDATE` | 2 | `update` |
| `Access::DELETE` | 8 | `delete` |

---

## 3. Where it lives

| Item | Path |
|------|------|
| Controller | `protected/modules/operation/controllers/TariffController.php` |
| Action classes | `protected/modules/operation/actions/tariff/` |
| Tariff model | `protected/modules/operation/models/Tariff.php` |
| Tariff-package bridge model | `protected/modules/operation/models/TariffPackage.php` |
| TariffService helper | `protected/components/TariffService.php` |
| Dashboard consumer (dealer admin) | `protected/modules/dashboard/controllers/DealerController.php` → `getTariffs()` |

URL pattern (Yii `operation` module routes):

```
GET    /operation/tariff/list
POST   /operation/tariff/create
POST   /operation/tariff/update
DELETE /operation/tariff/delete
```

Actions exposed:

| Action | Class | Method | Access |
|--------|-------|--------|--------|
| `list` | `TariffListAction` | GET | SHOW |
| `create` | `TariffCreateAction` | POST | CREATE |
| `update` | `TariffUpdateAction` | POST | UPDATE |
| `delete` | `TariffDeleteAction` | DELETE | DELETE |

---

## 4. Workflow

```mermaid
sequenceDiagram
  participant U as Operator
  participant FE as Browser (Vue)
  participant A as TariffXxxAction
  participant DB as MySQL

  U->>FE: Opens tariff manager screen
  FE->>A: GET /operation/tariff/list
  A->>DB: SELECT t.*, GROUP_CONCAT(package_id) FROM tariff t
  A-->>FE: JSON [{id, name, created_at, package_ids: "1,2,5"}]
  U->>FE: Click "Add" / "Edit" / "Delete"
  FE->>A: POST /create | /update or DELETE /delete
  A->>DB: BEGIN; insert/update Tariff; rewrite TariffPackage rows; COMMIT
  A-->>FE: {result: {id, name, created_at}}
```

### 4a. Create (`POST /operation/tariff/create`)

1. Caller POSTs `name` and `package_ids[]` (array of `Package.ID`).
2. `TariffCreateAction` checks `name` is non-empty and `package_ids` is non-empty.
3. `Package::model()->findAllByPk($packageIds)` is run; if the returned count is less than the requested count, the request is rejected ("Some packages are not found").
4. Inside a single DB transaction: a `Tariff` row is inserted, then one `TariffPackage` row per package id.
5. On any save failure the transaction rolls back and an error is returned with field-level `getErrors()`. On success the transaction commits and the new tariff `{id, name, created_at}` is returned.

### 4b. Update (`POST /operation/tariff/update`)

1. Caller POSTs `id`, `name`, `package_ids[]`.
2. `TariffUpdateAction` looks up the `Tariff` by `id` (rejects if missing), then validates the package list identically to create.
3. Inside a transaction: the tariff's `name` is updated, **all existing `TariffPackage` rows for this tariff are deleted in one shot** via `deleteAllByAttributes`, and the new package list is re-inserted. The bridge is rewritten wholesale, not diffed.
4. Transaction commits; response mirrors create.

### 4c. Delete (`DELETE /operation/tariff/delete?id=…`)

1. Caller sends `id` as a query string.
2. `TariffDeleteAction` looks up the tariff (rejects if missing).
3. A guard query runs: `SELECT COUNT(*) FROM d0_diler WHERE TARIFF_ID = :tariff_id`. If any dealer references this tariff, deletion is refused.
4. Inside a transaction: every `TariffPackage` row for this tariff is hard-deleted, then the `Tariff` row itself is hard-deleted.

### 4d. Consumption by subscription creation

When a dealer with `Diler.TARIFF_ID` set opens the subscription/package picker in the dashboard, the UI may use the tariff as a default selection set (the in-use Vue dashboard reads tariffs via `DealerController::getTariffs()`). The tariff is **advisory** — the actual subscription is created against individual `PACKAGE_ID`s, not against the tariff. There is no `Subscription.TARIFF_ID` column; the tariff link disappears once subscriptions exist.

---

## 5. Rules

- `name` is required and capped at 255 characters by the model rules.
- `package_ids` must be non-empty on both create and update.
- Every id in `package_ids` must resolve to an existing `Package` row — partial lookups are rejected.
- `TariffPackage` has a unique constraint expressed as a model rule on `(tariff_id, package_id)` — the `unique` rule in the model is keyed by `package_id` so a package may only appear once in a given tariff (although the rule syntax is quirky; see Gotchas).
- A tariff cannot be deleted while any `Diler.TARIFF_ID` references it. Reassign or null out dealer tariff references first.
- Tariff has no soft-delete column — both `TariffPackage` rows and the `Tariff` row are hard-deleted on `delete`.
- `TariffPackage` rewrite is **not idempotent in time**: each update deletes-and-recreates the bridge, so `TariffPackage.id` values change every save. Do not rely on bridge-row IDs as stable identifiers.
- The tariff does not constrain what packages a dealer can subscribe to. It is a *suggested bundle*, not a permission gate. The actual gate for whether a package shows in `api/license/packages` for a dealer is `CLIENT_TYPE` (public) or a matching `DilerPackage` row (private).

---

## 6. Data sources

| Table | DB / connection | Why read |
|-------|-----------------|----------|
| `d0_tariff` | sd-billing default DB | Primary entity — listed, created, updated, deleted |
| `d0_tariff_package` | sd-billing default DB | Many-to-many bridge to `d0_package`; rewritten on update |
| `d0_package` | sd-billing default DB | Validates `package_ids` on create/update |
| `d0_diler` | sd-billing default DB | Read by delete guard to refuse deletion when `Diler.TARIFF_ID` references the tariff |

---

## 7. Gotchas

**Update is rewrite, not diff.** `TariffUpdateAction` calls `TariffPackage::deleteAllByAttributes(["tariff_id" => $id])` and then re-inserts. There is no detection of which packages were added/removed. The `TariffPackage.id` and `created_at` of every link change on every save, so any external system observing this bridge will see "everything changed" each time.

**The `unique` rule is misleading.** `TariffPackage::rules()` has two `attributeName` keys in the same array — PHP keeps the last one (`package_id`) — so the model-level uniqueness check is on `package_id` alone, not on the composite `(tariff_id, package_id)`. This means model validation will refuse to add a package that already belongs to *any* tariff. The DB-level guarantee, if any, is on the schema not the model.

**No transaction boundary on the delete guard.** The "is this tariff used by any dealer?" check (`SELECT COUNT(*) FROM d0_diler WHERE TARIFF_ID = :tariff_id`) runs **before** the transaction starts. A race with a concurrent `Diler.TARIFF_ID = X` write can leak through. In practice the screen is low-traffic and admin-only, so this is rarely hit.

**Tariff is advisory, not enforced.** Once `Diler.TARIFF_ID` is set, nothing in the subscription creation flow checks that the chosen package belongs to the tariff. Operators can sell any package to any dealer (subject to currency match and `CLIENT_TYPE`), regardless of the dealer's tariff. The tariff is purely a UI default.

**Delete is hard.** There is no `IS_DELETED` flag — `Tariff::delete()` and `TariffPackage::delete()` both DROP the rows. Renaming-to-archive is the only way to retire a tariff while keeping history.

---

## 8. See also

- [Package management](./operation-package.md) — the underlying `Package` rows that tariffs group.
- [Subscription lifecycle](./operation-subscription.md) — how `Package` rows are sold to a dealer (tariff is advisory at this stage).
- [Domain model](../domain-model.md) — `Tariff`, `TariffPackage`, `Package`, `Diler` schemas.
- Source: `protected/modules/operation/controllers/TariffController.php` and `protected/modules/operation/actions/tariff/`
