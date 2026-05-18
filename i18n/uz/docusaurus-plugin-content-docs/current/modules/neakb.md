---
sidebar_position: 32
title: neakb
audience: Backend engineers, QA, PM, Sales ops
summary: Placeholder module — NeAKB ("non-active AKB") was originally a dedicated dashboard for clients who dropped out of the active customer base. The module is disabled; the live NeAKB logic now lives inside the report and clients modules.
topics: [neakb, akb, placeholder, customer-base, deprecated, history]
---

# `neakb` module

`neakb` is a **historical placeholder** in the sd-main module
directory. All of its files — controllers, models, and the module
bootstrap — are renamed to `.obsolete` and the module is **not
loaded by the application**. None of its routes resolve.

The **concept** of NeAKB (Не-АКБ — "non-active customer base") is
very much alive in the product — see [`concepts/akb.md`](../concepts/akb.md)
for the definition — but the data and the UI now live in the
`report` and `clients` modules, not here.

## What is NeAKB?

**AKB** (Активная Клиентская База / Active Customer Base) is the set
of clients who **placed at least one order in the configured AKB
window** (typically the trailing month). **NeAKB** is its
complement — every client who **was** in the AKB recently but **fell
out** of it for the period being analysed.

The neakb screen historically presented:

- A **grid of clients dropped from AKB** broken down by agent,
  type, category, and filter month.
- A **lost-sales matrix** showing the prior-period order value that
  is now missing.
- Drill-downs by agent and by client.

These screens were superseded by the report module's customer-side
reports, which include the same data alongside positive AKB and RFM.

## Folder

```
protected/modules/neakb/
├── NeakbModule.php.obsolete              # module bootstrap — disabled
├── controllers/
│   ├── BackendController.php.obsolete    # 9 JSON actions: all, agent, clients,
│   │                                     #   agents, filters, categories, types,
│   │                                     #   allSales, agentSales
│   └── FrontendController.php.obsolete   # 3 actions: index, sales, directiveFilters
├── models/
│   ├── Neakb.php.obsolete                # static helpers: allAkb, agentAkb, clientsAkb,
│   │                                     #   agentsAll, filtersAll, categoriesAll, typesAll
│   └── Sales.php.obsolete                # static helpers: allSales, agentSales
├── views/
│   └── frontend/                         # index, sales, _filters
└── assets/
```

## Active controllers

**None.** The module currently exposes **0 actions**. Any
`/neakb/*` URL returns `404 Not Found`.

## Historical scope (for archaeology)

Reading the `.obsolete` files, the original API was a small AngularJS
SPA driven by these endpoints:

### Backend (JSON) — was at `/neakb/backend/*`

| Action | Inputs | Purpose |
|---|---|---|
| `all` | `filterId, typeId, categoryId, year, month, agentId` | NeAKB matrix across all dimensions — `Neakb::allAkb($params)` |
| `agent` | `filterId, typeId, agentId, year, month` | NeAKB breakdown for one agent — `Neakb::agentAkb` |
| `clients` | `column, typeId, categoryId, agentId, year, month` | Drill-down to the client list — `Neakb::clientsAkb` |
| `agents` | – | Agent reference list — `Neakb::agentsAll` |
| `filters` | – | Filter catalogue — `Neakb::filtersAll` |
| `categories` | – | Category catalogue — `Neakb::categoriesAll` |
| `types` | – | Type catalogue — `Neakb::typesAll` |
| `allSales` | `filterId, typeId, categoryId, year, month, agentId` | Companion lost-sales matrix — `Sales::allSales` |
| `agentSales` | `filterId, typeId, agentId, year, month` | Per-agent lost-sales — `Sales::agentSales` |

### Frontend (HTML) — was at `/neakb/frontend/*`

| Action | Purpose |
|---|---|
| `index` | NeAKB matrix landing page |
| `sales` | Lost-sales companion page |
| `directiveFilters` | AngularJS directive — filter sidebar partial |

The two static-helper models (`Neakb`, `Sales`) ran raw SQL against
`order_detail`, `client`, `agent`, and the visit/store tables to
compute the matrices on demand. They had no Active Record schema —
they were pure aggregators.

## Where NeAKB logic lives now

| What | Where it moved to |
|---|---|
| AKB / NeAKB definition (window, exclusions) | [`concepts/akb.md`](../concepts/akb.md) |
| Live NeAKB matrix | [`report`](./report.md) — `CustomerController` and `AnalyzeController` |
| Per-agent AKB / NeAKB | [`report`](./report.md) — `AgentController` |
| Client drill-down | [`clients`](./clients.md) — client list with AKB filter |
| KPI rollups including NeAKB | [`rating`](./rating.md), [`dashboard`](./dashboard.md) |
| Reference catalogues (agents/filters/categories/types) | [`settings`](./settings.md) (master data) + [`agents`](./agents.md) |

There is **no dedicated NeAKB endpoint** in sd-main as of the current
revision; the matrix is rendered inside the report module's
customer-side screens with a `mode=neakb` (or similar) toggle.

## Reviving the namespace (if you must)

If you genuinely need a standalone NeAKB module again (e.g. as a
dedicated tenant feature):

1. Rename `NeakbModule.php.obsolete` → `NeakbModule.php` and
   register it in `protected/config/main.php` under `modules`.
2. Replace the `.obsolete` models with new ones — the originals
   reference table layouts that may have shifted in the intervening
   schema migrations.
3. Wire `operation.neakb.*` RBAC entries via [`access`](./access.md).
4. Cross-link from this page so future readers know the namespace
   is alive again.

## Cross-module touchpoints

None — the module is disabled. Its conceptual successors touch:

- **`report`** — reads `order`, `order_detail`, `client`, `visit`
  to compute the AKB / NeAKB sets.
- **`clients`** — exposes a filter `In AKB` / `Not in AKB` on the
  client list.
- **`settings`** — defines the AKB window length via dynamic params
  (`Yii::app()->params['akbDays']` or similar — see the actual key
  name in [`settings.md`](./settings.md) Workflow 1.3).

## Permissions

None — the module is unrouted. Any `/neakb/...` URL falls through to
Yii's 404 handler. The successor screens are gated by
`operation.report.*` and `operation.clients.list`.

## Gotchas

- **Do not re-route `/neakb/*` without a new module.** The
  `.obsolete` controllers will fatal on the first call because
  `Neakb::allAkb` and `Sales::allSales` execute raw SQL whose column
  names may have drifted (e.g. `order_detail.SUMMA` → other
  rounding fields).
- **Do not confuse with the AKB concept.** AKB / NeAKB are
  **first-class concepts** even though the **module** is dead. New
  feature requests like "show NeAKB on dashboard" go in the
  [`report`](./report.md) and [`dashboard`](./dashboard.md)
  backlogs, not here.
- **`Neakb` (the model class) is a static helper, not Active
  Record.** Re-using the class name in a new module would shadow
  business logic if both ever load simultaneously.
- **AngularJS frontend was front-end-only AKB filter** — the
  `_filters` partial maintained a local state object. The modern
  successor in `report` uses the shared `ReportBuilderController`
  filter infrastructure instead.
- **No background jobs touched this module.** All matrices were
  request-driven; revival should preserve that property to keep
  cache invalidation simple.

## See also

- [`concepts/akb.md`](../concepts/akb.md) — definition of AKB / NeAKB
- [`report`](./report.md) — current home of NeAKB matrices
- [`clients`](./clients.md) — client list with AKB / NeAKB filter
- [`rating`](./rating.md) — KPI that includes AKB / NeAKB metrics
- [`dashboard`](./dashboard.md) — top-line AKB indicators
- [`overview`](./overview.md) — module index
