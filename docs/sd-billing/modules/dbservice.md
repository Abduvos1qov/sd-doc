---
sidebar_position: 2
title: dbservice module
audience: [engineering, ops, sre]
summary: DB maintenance and tenant-server health utilities. Lists every dealer's database/web-server registration alongside their last active subscription so ops can spot stuck records and stale tenants.
topics: [sd-billing, dbservice, ops, maintenance, server-health]
---

# sd-billing `dbservice` module

The `dbservice` module is the operations console for sd-billing's view of the SD-app server fleet. Every dealer (`d0_diler`) has a paired row in `d0_server` describing where their MySQL database and web frontend live, which branch is deployed, and the last health check result. This module surfaces that data joined to the dealer's most recent active subscription so the ops team can see at a glance which tenants are deployed but unsubscribed, subscribed but unreachable, or in any other broken combination.

Despite the name, this module does not run destructive jobs in-page. The single non-trivial action is a read query. Bulk DB fixes and ad-hoc migrations live in the `protected/commands/` cron commands and the `api/MaintenanceController`, not here. Use this module to **see** what needs fixing; use the cron or the maintenance endpoints to **do** the fixing.

## Key features

| Feature | What it does | Owner role(s) |
|---|---|---|
| Server registry view | Renders a server-list page joining `d0_server` with `d0_diler` and the dealer's last `d0_subscription.ACTIVE_TO` | admin, ops |
| Last-active filter | Filters out tenants whose last subscription expired before the date cutoff (helps surface stale servers) | admin, ops |
| Read-only by design | No CREATE/UPDATE/DELETE endpoints — edits happen through the dashboard or direct DB intervention | n/a |

## Folder

```
protected/modules/dbservice/
  DbserviceModule.php
  controllers/
    ServiceController.php       (2 actions: index, list)
  actions/
    service/
      ListAction.php            # JSON data for the list view
  views/
    service/
      index.php
```

## Controllers

| Controller | Purpose | Actions | Auth |
|---|---|---|---|
| `ServiceController` | Server fleet visibility | `index` (render view), `list` (delegated to `ListAction`) | `Access::check('operation.server.index', Access::SHOW)` on `index`; `ListAction` calls `authorize([], ['operation.server.index', Access::SHOW])` |

### `ServiceController::actionIndex`

| Method | Permission gate | What it does |
|---|---|---|
| GET | `operation.server.index` SHOW | Renders `views/service/index.php` — a server-list page that fetches its data from the `list` action |

### `ServiceController::list` (delegates to `ListAction`)

| Method | Permission gate | What it does |
|---|---|---|
| GET | `operation.server.index` SHOW | Returns JSON rows joining `d0_server` with `d0_diler` and the dealer's last active subscription |

Returned columns:

| Column | Source | Meaning |
|---|---|---|
| `id` | `d0_server.id` | Server registration id |
| `name` | `d0_diler.NAME` | Dealer display name |
| `host` | `d0_diler.HOST` | Internal host alias (used for SMS callbacks and notify cron) |
| `diler_id` | `d0_server.diler_id` | FK to `d0_diler.ID` |
| `db_name`, `db_user`, `db_server` | `d0_server` | MySQL connection target |
| `status`, `status_code` | `d0_server` | Last health check result |
| `domain` | `d0_diler.DOMAIN` | Public SD-app URL |
| `web_server`, `web_branch` | `d0_server` | Frontend host and deployed git branch |
| `created` | `d0_diler.CREATED_AT` | Dealer onboarding date |
| `dstatus` | `d0_diler.STATUS` | 10 = active, 20 = deleted, 30 = archive |
| `last_sub` | `MAX(d0_subscription.ACTIVE_TO)` where `IS_DELETED = 0` | Latest subscription expiry |

### Optional `date` filter

`ListAction::run` accepts `?date=MM/DD/YYYY` via `getSearchParams()`. When present and valid (`DateHelper::validateDate`), it normalizes to the **last day** of that month (`date('Y-m-t', strtotime($date))`) and adds `HAVING last_sub <= :last_sub` to the query. The intent: "show me tenants whose subscription expired on or before end-of-month X" — that is, tenants you can probably decommission.

Note that the action emits `AND HAVING ...` with the `AND` prefix, which is fine because the outer `WHERE s.ID` is always present, but `HAVING` belongs after `GROUP BY` in standard SQL — the current query has neither a `GROUP BY` nor a true aggregate. The condition works because MySQL accepts `HAVING` after `WHERE` even without grouping, but the construction is fragile.

## Cross-module touchpoints

- **`d0_server`** is written by the SD-app onboarding pipeline (out-of-band of sd-billing) and by the `api/HostController` server-status callback from each tenant. See [sd-billing api module](./api.md).
- **`d0_subscription`** is owned by the `operation` module and the cron-based settlement command. The "last active subscription" join here is the authoritative answer to "is this tenant currently paying?".
- **`api/MaintenanceController`** is where destructive cleanup lives (orphaned records, stale tokens, log truncation). It is gated by a hard-coded TOKEN and runs via cron. This module is the read-side counterpart.
- **`dashboard` module** has its own server-status widgets — they share the underlying `d0_server` table but render differently. Use `dbservice` for the engineering view; use `dashboard` for the operations dashboard.

## Gotchas

- **Read-only is not a guarantee — it is a convention.** The module name suggests "DB service" which historically included destructive helpers. If a future action is added, ensure it goes through `Access::check` with the appropriate bit (CREATE/UPDATE/DELETE), not just SHOW.
- **The `HAVING` clause without `GROUP BY` is brittle.** MySQL allows it but a stricter `ANSI` mode or a switch to PostgreSQL would break the date filter. If you touch this query, convert to `WHERE` or add an explicit `GROUP BY s.id`.
- **No pagination.** The page renders every row in `d0_server`. For installations with thousands of tenants the page will be slow; the existing date filter is the only way to narrow the result set.
- **The view does not include unsubscribed tenants by default.** If a dealer has zero subscription rows, `MAX(ACTIVE_TO)` returns `NULL` and the `HAVING last_sub <= :date` filter excludes them. Drop the filter to see tenants who never subscribed.
- **`status_code` semantics live in the SD-app, not here.** The integer code is set by the tenant's own status push to `api/host`. Decoding it requires cross-referencing the SD-app source.
- **No destructive operation lives in this module today, but the access key `operation.server.index` exists in `d0_access_operations`.** Granting it to non-admins reveals every tenant's DB credentials in the JSON response. Treat the SHOW bit on this key as effectively admin-level.

## See also

- [api module](./api.md) — `HostController` server-status callback that writes `d0_server.status`
- [Cron and settlement](../cron-and-settlement.md) — when subscription rows become inactive
- [Domain model](../domain-model.md) — `d0_server` and `d0_diler` schema
- Source: `protected/modules/dbservice/controllers/ServiceController.php` and `protected/modules/dbservice/actions/service/ListAction.php`
