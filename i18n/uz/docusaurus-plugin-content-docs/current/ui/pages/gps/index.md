---
title: "GPS UI pages"
audience: All sd-main developers, QA
summary: Index of UI page reference docs for the gps (legacy) module
topics: [gps, ui, page-index]
---

# GPS UI pages

The `gps` module is the original GPS tracking subsystem. It powers the agent monitoring map, the route history view, the market (outlets) map, and the per-order GPS audit page. Most of the module is API/cron — only the views below are user-facing.

> The newer `gps2` module supersedes most screens here for new deployments. The legacy module remains for backwards-compat and is still wired into a number of admin sidebars.

## Pages

| Page | Route | Audience |
|---|---|---|
| [Live agent monitoring](./gps_monitoring_index.md) | `/gps/monitoring` | admin / supervisor |
| [Agent route history](./gps_frontend_history.md) | `/gps/frontend/history/agent/<USER_ID>` | admin / supervisor |
| [Live agent map (track)](./gps_frontend_track.md) | `/gps/frontend/track` | admin / supervisor |
| [Markets / outlets map](./gps_frontend_market.md) | `/gps/frontend/market` | admin / supervisor |
| [Orders GPS audit](./gps_ordersGps_index.md) | `/gps/ordersGps` | admin |
| [Tracking route view](./gps_tracking_index.md) | `/gps/tracking/route` | admin / supervisor |

## Other endpoints (backend-only)

| Controller | Purpose |
|---|---|
| `BackendController` | Server-to-server endpoints (`actionLast`, `actionAgent`, `actionMarkets`, etc.) — no view rendered |
| `GetController` | JSON endpoints consumed by the frontend (visitings, orders, defects, tracks) |
| `ClientInMapController` | Obsolete (`.obsolete` suffix on view) |

## See also

- Module reference: [/modules/gps](/docs/modules/gps)
- Page-to-module map: [/quality/page-to-module-map](/docs/quality/page-to-module-map)
