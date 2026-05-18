---
title: "Карта точек продаж (Market)"
audience: All sd-main developers, QA
summary: Admin page at /gps/frontend/market — map of outlets with coverage info
topics: [gps, page, ui, market]
---

# Карта точек продаж (Market)

**URL**: `/gps/frontend/market` · **Module**: `gps` · **Controller**: `FrontendController::market` · **RBAC**: `operation.clients.map` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Map of all outlets / "markets" in the diler's territory, with filters for region, agent group, days since last visit, and category. Supervisors use it to identify uncovered outlets ("white spots") and reassign them.

## Fields (filter bar)

| Label | Name | Type | Required |
|---|---|---|---|
| Агенты | filter | multi-select | no |
| Регионы | filter | multi-select | no |
| Категории | filter | multi-select | no |
| Дней с последнего визита | filter | number | no |

The map header shows `Общая: {market.total.TOTAL}` — total markets matching the filter.

## Grid columns

Side panel / popup per outlet:

| # | Field | Source |
|---|---|---|
| 1 | Адрес | outlet address |
| 2 | Ориентир | landmark / cross-street |
| 3 | Телефон | outlet phone |
| 4 | Контактное лицо | contact name |
| 5 | Агенты | list of agents assigned |

## Actions

- Фильтр (`market.getMarkets()`) — re-runs the search
- Click marker — opens outlet popup

## Backend route

- **Controller file**: `protected/modules/gps/controllers/FrontendController.php`
- **Action**: `actionMarket` (line 18) — `H::access('operation.clients.map')` then renders `market` view
- **Data sources**: `BackendController::actionMarkets`, `actionMarketAgents`, `actionRegions`, `actionCategories`
- **Required permission**: `operation.clients.map`

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Pages index: [/ui/pages/gps](./index.md)
