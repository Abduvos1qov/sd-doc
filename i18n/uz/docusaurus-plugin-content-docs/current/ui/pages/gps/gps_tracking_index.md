---
title: "Маршрут (Tracking)"
audience: All sd-main developers, QA
summary: Admin page at /gps/tracking/route — route map for a delivery trip
topics: [gps, tracking, page, ui]
---

# Маршрут (Tracking)

**URL**: `/gps/tracking/route` · **Module**: `gps` · **Controller**: `TrackingController::route` · **RBAC**: `operation.other.gps` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Map view of a single delivery / trip's route. Shows all stops in sequence with the polyline between them and per-stop status. Most commonly opened from the Trips page (`/orders/view/trips`) via a "Show on map" link.

> `actionIndex($id)` is a no-render passthrough; the user-facing view is `actionRoute`.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Trip id | URL param | int | yes (passed via the calling page) |
| Дата | date filter | date | no |

## Grid columns

Map view. Bottom panel lists stops:

| # | Column |
|---|---|
| 1 | Порядковый номер |
| 2 | Outlet |
| 3 | Время прибытия (план) |
| 4 | Время прибытия (факт) |
| 5 | Статус |

## Actions

- Toggle satellite / street map
- Click stop — opens outlet popup
- Excel export of stops

## Backend route

- **Controller file**: `protected/modules/gps/controllers/TrackingController.php`
- **Actions**: `actionIndex($id)` (line 34) — no-op; `actionRoute` (line 37) — `H::access('operation.other.gps')` then renders `index` view
- **Required permission**: `operation.other.gps`

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Orders trips view: [/ui/pages/orders/orders_view_trips](/docs/ui/pages/orders/orders_view_trips)
