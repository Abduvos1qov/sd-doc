---
title: "Units"
audience: All sd-main developers, QA
summary: Live admin page at /settings/unit/index
topics: [settings, product, page, ui]
---

# Units

**URL**: `/settings/unit/index` · **Module**: `settings` · **Controller**: `UnitController::index` · **RBAC**: `operation.settings.unit` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Unit-of-measure directory. Each product has a base unit (piece, kg, litre) and may sell in packs (10 piece = 1 box). Units are also referenced by stock, finans and reports for quantity rendering. Conversion factors between units are stored on the `Product` row, not here — this screen only catalogs the unit names and short labels.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Name |
| 3 | Short label |
| 4 | Sort order |
| 5 | Active |

## Actions

- Add unit
- Edit unit (`updateAjax`)
- Toggle active

## Backend route

- **Controller file**: `protected/modules/settings/controllers/UnitController.php` (line 46)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/unit/admingrid_diler.php`
- **Required permission**: `operation.settings.unit`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `updateAjax`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Product master: [`/settings/product/index`](./settings_product_index)
- Tara / packaging: [/concepts/tara-packaging](/docs/concepts/tara-packaging)
