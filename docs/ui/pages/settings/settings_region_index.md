---
title: "Regions"
audience: All sd-main developers, QA
summary: Live admin page at /settings/region/index
topics: [settings, geo, page, ui]
---

# Regions

**URL**: `/settings/region/index` · **Module**: `settings` · **Controller**: `RegionController::index` · **RBAC**: `operation.settings.region` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Region directory — the coarser geographic level above `City`. Drives the territory-level dimension in KPI / sales reports and is the typical scope unit for supervisors. Most tenants seed this with the 14 Uzbek viloyats (regions) plus Tashkent City.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Name |
| 3 | Code |
| 4 | Sort order |
| 5 | Active |

## Actions

- Add region
- Edit region (`updateAjax`)
- Mass delete (`ajaxMassDelete`)
- Toggle active

## Backend route

- **Controller file**: `protected/modules/settings/controllers/RegionController.php` (line 38)
- **Action kind**: inline (`$this->render('admin', …)` shell + `_ajaxmassdelete`)
- **View rendered**: `views/region/admin.php`
- **Required permission**: `operation.settings.region`
- **Sibling endpoints**: `updateAjax`, `ajaxMassDelete`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Cities: [`/settings/city/index`](./settings_city_index)
