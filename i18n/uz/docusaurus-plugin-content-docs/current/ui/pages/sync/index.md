---
title: "Sync UI pages"
audience: All sd-main developers, QA
summary: Sync module has no user-facing UI pages — backend-only
topics: [sync, ui, page-index]
---

# Sync UI pages

The `sync` module is **backend-only** and has no user-facing UI pages in the current build.

## Why no pages

Every controller and view in `protected/modules/sync/` is suffixed `.obsolete`:

| File | Status |
|---|---|
| `controllers/DefaultController.php.obsolete` | obsolete |
| `controllers/DilerController.php.obsolete` | obsolete |
| `controllers/ProductController.php.obsolete` | obsolete |
| `controllers/PurchaseController.php.obsolete` | obsolete |
| `controllers/ServerController.php.obsolete` | obsolete |
| `controllers/SettingController.php.obsolete` | obsolete |
| `views/default/index.php.obsolete` | obsolete |
| `views/diler/index.php.obsolete` | obsolete |
| `views/product/index.php.obsolete` | obsolete |
| `views/purchase/index.php.obsolete` | obsolete |
| `views/purchase/index2.php.obsolete` | obsolete |
| `views/server/index.php.obsolete` | obsolete |
| `views/setting/index.php.obsolete` | obsolete |

These files are retained for historical reference but are not loaded by Yii (the `.obsolete` extension is non-routable). All sync responsibilities have been moved to background processes and the v3/v4 sync APIs.

## What replaced these pages

- **Mobile sync** is now handled by the `api` module endpoints (`/api/v3/sync/*`, `/api/v4/sync/*`).
- **Diler / server sync** is handled by the `serversync` / `cron` jobs documented under [/modules/cron](/docs/modules/cron).
- **Product / purchase / setting** flows live in their respective top-level modules.

## See also

- Module reference: [/modules/sync](/docs/modules/sync)
- Sync conflict-resolution flow: [/flows/sync-conflict-resolution](/docs/flows/sync-conflict-resolution)
- API reference (v3/v4 sync endpoints): [/api/overview](/docs/api/overview)
