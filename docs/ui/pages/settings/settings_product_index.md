---
title: "Product master"
audience: All sd-main developers, QA
summary: Live admin page at /settings/product/index
topics: [settings, product, page, ui]
---

# Product master

**URL**: `/settings/product/index` · **Module**: `settings` · **Controller**: `ProductController::index` · **RBAC**: `operation.settings.product` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

The product master grid. Every SKU sold by the tenant is registered here: code, name, category, brand, base unit, packaging, tax flags, photo, barcode, local code, marking (Markirovka / CRPT) flag. Companion screens cover bulk import, sort, deactivation, product groups, local-code mapping and updates.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Code |
| 3 | Name |
| 4 | Category |
| 5 | Sub-category |
| 6 | Brand |
| 7 | Producer |
| 8 | Base unit |
| 9 | Pack size |
| 10 | Barcode |
| 11 | Local code |
| 12 | Marking |
| 13 | Active |
| 14 | Created at |

## Actions

- Add product (modal — `createAjax`)
- Edit product (modal — `updateAjax`)
- Delete product (`deleteProduct`, `checkDelete`)
- Add products in bulk (`addProducts`)
- Import from Excel (`import_xls`)
- Import local codes (`import_local_code`)
- Import updates (`import_update`)
- Sort products (`sort_product`)
- Deactivate selection (`deactivate`)
- Manage product groups (`product_group`)
- Check duplicates (`check`)

## Backend route

- **Controller file**: `protected/modules/settings/controllers/ProductController.php` (line 65)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/product/admingrid_diler.php`
- **Required permission**: `operation.settings.product`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `getExtras`, `createAjax`, `updateAjax`, `deleteProduct`, `addProducts`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Brands: [`/settings/brand/index`](./settings_brand_index)
- Units: [`/settings/unit/index`](./settings_unit_index)
- Lot management: [/concepts/lot-management](/docs/concepts/lot-management)
