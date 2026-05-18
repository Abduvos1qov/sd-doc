---
title: "Cities"
audience: All sd-main developers, QA
summary: Live admin page at /settings/city/index
topics: [settings, geo, page, ui]
---

# Cities

**URL**: `/settings/city/index` · **Module**: `settings` · **Controller**: `CityController::index` · **RBAC**: `operation.settings.city` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

City directory. Used as the address-level granularity for clients, agents and warehouses, and as a geographic filter on KPI / sales reports. Each city is attached to a `Region`. Includes an Excel-import endpoint so a fresh tenant can be seeded from a master spreadsheet rather than typed in.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Name |
| 3 | Region |
| 4 | Postal code |
| 5 | Sort order |
| 6 | Active |

## Actions

- Add city (modal — `createAjax`)
- Edit city (modal — `updateAjax`)
- Import from Excel (`importXls`)
- Toggle active

## Backend route

- **Controller file**: `protected/modules/settings/controllers/CityController.php` (line 46)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/city/admingrid_diler.php`
- **Required permission**: `operation.settings.city`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`, `importXls`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Regions: [`/settings/region/index`](./settings_region_index)
