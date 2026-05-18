---
title: "Список агентов (Monitoring)"
audience: All sd-main developers, QA
summary: Admin page at /gps/monitoring — list of agents with live status, battery and last update
topics: [gps, monitoring, page, ui]
---

# Список агентов (Monitoring)

**URL**: `/gps/monitoring` · **Module**: `gps` · **Controller**: `MonitoringController::index` · **RBAC**: `operation.other.gps` · **Role harvested**: `admin`

:::note
Screenshot pending — harvester re-run needed.
:::

## Purpose

Tabular live view of every agent with their GPS / device status. Used by supervisors to spot agents who are offline, have a flat battery, or stopped reporting. Each row links into the per-agent map (`/gps/frontend/track`) and history (`/gps/frontend/history`).

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Регион | filter | select | no |
| Супервайзер | filter | select | no |
| Статус | filter | select | no |

## Grid columns

| # | Column | Source |
|---|---|---|
| 1 | Агент | `User.NAME` |
| 2 | Статус | online / offline indicator |
| 3 | Последнее обновление | timestamp |
| 4 | Батарея | percent |

## Actions

- Мониторинг — link to `/gps/frontend/track`
- Маршрут — link to per-agent history
- Фильтр

## Backend route

- **Controller file**: `protected/modules/gps/controllers/MonitoringController.php`
- **Action**: `actionIndex` (line 34) — renders `index` view
- **Required permission**: `H::access('operation.other.gps')`

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Live agent map: [/ui/pages/gps/gps_frontend_track](./gps_frontend_track.md)
