---
sidebar_position: 31
title: manager
audience: Backend engineers, QA, PM
summary: Placeholder module — the `manager` namespace exists on disk but has no active controllers. All historical manager-tier UI has been folded into team, dashboard, and orders. Documented here to prevent re-creation.
topics: [manager, placeholder, deprecated, history]
---

# `manager` module

`manager` is a **historical placeholder** in the sd-main module
directory. All of its controller files are renamed to `.obsolete`
and the module bootstrap class itself is `ManagerModule.php.obsolete`,
so the module is **not loaded by the application** and **none of its
routes resolve**.

This page exists so that:

1. Future maintainers don't re-add the namespace by accident.
2. Anyone looking for "where the manager-role UI lives today" finds
   the active pointers (see [Where manager-tier UI lives now](#where-manager-tier-ui-lives-now)).
3. A future revival of the namespace (e.g. for a dedicated
   manager-tier admin shell) has a clean spot to slot in.

## Folder

```
protected/modules/manager/
├── ManagerModule.php.obsolete            # module bootstrap — disabled
├── controllers/
│   ├── DefaultController.php.obsolete    # actionIndex — renders 'index' against //layouts/mainAdmin
│   └── OrdersController.php.obsolete     # legacy Purchase / PurchaseDetail CRUD using AjaxCrudBehavior
└── views/
    ├── default/
    └── orders/
```

## Active controllers

**None.** The module currently exposes **0 actions**. Any
`/manager/*` URL returns `404 Not Found`.

## Historical scope (for archaeology)

Reading the `.obsolete` files, the original intent was:

| Legacy controller | Original purpose | Replaced by |
|---|---|---|
| `DefaultController::actionIndex` | A landing page for a "manager" admin role, rendered against `//layouts/mainAdmin` | [`dashboard`](./dashboard.md) — manager-role users now land on the shared admin dashboard |
| `OrdersController::actionIndex` + `actionEdit` + `actionView` + `actionChangeStatus` | Manager-side `Purchase` / `PurchaseDetail` CRUD using `AjaxCrudBehavior`, with status transitions and per-row sync flagging | [`orders`](./orders.md) — the modern `Order` model + the orders module's status transitions; `vs.CreateOrderController` for vansel; `stock/purchase` for the purchase-order surface |

The legacy `OrdersController` worked on the **`Purchase`** model
(pre-sales purchase order), not the customer-facing `Order` model
used everywhere today. That entity is itself largely deprecated in
favour of the modern order pipeline.

## Where manager-tier UI lives now

The "manager" role (typically `User::ROLE = 2`) operates entirely out
of these existing modules:

| Manager activity | Module |
|---|---|
| Daily KPI overview | [`dashboard`](./dashboard.md) |
| Order review, status change, manual create | [`orders`](./orders.md) |
| Team configuration (agents, supervisors, auditors) | [`team`](./team.md) |
| Internal HR (agents/supervisors/expeditors CRUD) | [`staff`](./staff.md) |
| RBAC assignment | [`access`](./access.md) |
| Pricing, master data, tenant config | [`settings`](./settings.md) |
| KPI / agent rating | [`rating`](./rating.md) |
| Sales / debt / coverage reports | [`report`](./report.md) |
| Visit / audit oversight | [`audit-adt`](./audit-adt.md), [`gps`](./gps.md) |
| Planning + daily plans | [`planning`](./planning.md) |

There is **no dedicated manager-only namespace** in sd-main as of
the current revision; every manager-relevant action is RBAC-gated
inside its home module via `operation.*` checks.

## Reviving the namespace (if you must)

If a future feature genuinely needs a manager-only module shell:

1. Rename `ManagerModule.php.obsolete` → `ManagerModule.php` and
   register it in `protected/config/main.php` under `modules`.
2. Create fresh controllers — **do not** rename the
   `.obsolete` files back into service; they reference deleted
   models (`Purchase`, `PurchaseDetail`) and outdated layout names.
3. Pick a sidebar slot under "Admin & ops" with an
   `operation.manager.*` RBAC prefix.
4. Cross-link from this page so future readers know the namespace
   is alive again.

## Cross-module touchpoints

None — the module is disabled. The historical controllers had
touched `Purchase` / `PurchaseDetail` and `Price` (for re-pricing
on edit); those flows are now in `stock` and `settings` respectively.

## Permissions

None — the module is unrouted. Any `/manager/...` URL falls through
to Yii's 404 handler.

## Gotchas

- **Do not re-route `/manager/*` without a new module.** The
  `.obsolete` controllers will fatal on first hit because the
  `Purchase` model they reference may have moved or been removed.
- **Layout name `//layouts/mainAdmin` may not exist anymore** —
  reviving `DefaultController` would need a layout audit.
- **`OrdersController` does its own ad-hoc accessRules** (`array(
  '*' )` — i.e. wide open). Never re-enable without first wiring
  in `H::access(...)`.
- **No tests** — there is no QA suite for the `manager` namespace.
  If revived, write the QA workflow alongside the module.

## See also

- [`overview`](./overview.md) — the module index that this page links
  back from
- [`dashboard`](./dashboard.md) — current manager landing page
- [`orders`](./orders.md) — order management used by the manager role
- [`access`](./access.md) — RBAC role and operation catalogue
