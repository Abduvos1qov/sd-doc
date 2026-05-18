---
title: "Карта агентов (live track)"
audience: All sd-main developers, QA
summary: Admin page at /gps/frontend/track — live agent positions on the map
topics: [gps, page, ui, live]
---

# Карта агентов (live track)

**URL**: `/gps/frontend/track` · **Module**: `gps` · **Controller**: `FrontendController::track` · **RBAC**: module-level · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Live "where are my agents right now?" map. Periodically polls `GetController::actionReturnAgents` and `actionReturnLastAction` to refresh each agent's marker. Side panel lists agents with online/offline status, battery, and last activity. Clicking an agent zooms the map and shows the recent path.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Регион / Супервайзер | filter | select | no |
| Категория клиента | filter | select | no |

## Grid columns

Map view. Side panel rows:

| # | Field | Source |
|---|---|---|
| 1 | Агент | `User.NAME` |
| 2 | Координаты | last GPS fix |
| 3 | Батарея | percent |
| 4 | Последнее действие | label (visit / order / track) |

## Actions

- Мониторинг — link to `/gps/monitoring`
- Маршрут — link to per-agent history
- Re-center / zoom controls

## Backend route

- **Controller file**: `protected/modules/gps/controllers/FrontendController.php`
- **Action**: `actionTrack` (line 6) — renders `track` view
- **Data sources**: `GetController::actionReturnAgents`, `actionReturnLastAction`, `actionGetCurrentTypeCords`
- **Required permission**: module-level

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Per-agent history: [/ui/pages/gps/gps_frontend_history](./gps_frontend_history.md)
