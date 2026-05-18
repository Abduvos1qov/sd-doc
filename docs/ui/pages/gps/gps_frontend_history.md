---
title: "История маршрута агента"
audience: All sd-main developers, QA
summary: Admin page at /gps/frontend/history/agent/<USER_ID> — replay an agent's route for a day
topics: [gps, page, ui, history]
---

# История маршрута агента

**URL**: `/gps/frontend/history/agent/<USER_ID>` · **Module**: `gps` · **Controller**: `FrontendController::history` · **RBAC**: module-level · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Per-agent map replay. Reads the day's GPS track plus visit, order, and defect markers (from `GetController` JSON endpoints) and renders them on a Leaflet/Yandex map. Supervisors use this to verify the agent visited the planned outlets, see where rejects happened, and audit time-on-route.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Агент | URL param `agent` | int | yes |
| Дата | date picker | date | no (defaults to today) |

## Grid columns

This page is a map, not a grid. Side panel shows per-visit detail:

| Row | Field | Source |
|---|---|---|
| 1 | Батарея | last-known battery percent at visit time |
| 2 | Причина отказа | reject reason if defect / отказ |
| 3 | Клиент | outlet name |
| 4 | Телефон | outlet phone |
| 5 | Время | visit timestamp |

## Actions

- Мониторинг — back to live map (`/gps/frontend/track`)
- Маршрут — toggle to route polyline view
- Дата picker — re-fetch for a different day

## Backend route

- **Controller file**: `protected/modules/gps/controllers/FrontendController.php`
- **Action**: `actionHistory($agent)` (line 12) — renders `history` view
- **Data sources** (XHR from view): `GetController::actionGetVisitings`, `actionGetOrders`, `actionGetDefects`, `actionGetTracks`
- **Required permission**: module-level

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Live agent map: [/ui/pages/gps/gps_frontend_track](./gps_frontend_track.md)
