---
title: "Brands"
audience: All sd-main developers, QA
summary: Live admin page at /settings/brand/index
topics: [settings, product, page, ui]
---

# Brands

**URL**: `/settings/brand/index` · **Module**: `settings` · **Controller**: `BrandController::index` · **RBAC**: `operation.settings.brand` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Simple CRUD grid for brands. Every `Product` row points at one `Brand`. Brands also drive several reports and act as a filter on the orders board, KPI screens and the price list, so deleting a brand that's referenced by products is blocked by the controller.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Name |
| 3 | Producer |
| 4 | Sort order |
| 5 | Active |
| 6 | Updated at |

## Actions

- Add brand
- Edit brand (`update`)
- Save (`save`)
- Toggle active

## Backend route

- **Controller file**: `protected/modules/settings/controllers/BrandController.php` (line 35)
- **Action kind**: inline (`$this->render('admingrid_diler')`)
- **View rendered**: `views/brand/admingrid_diler.php`
- **Required permission**: `operation.settings.brand`
- **Sibling endpoints**: `getData`, `save`, `update`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Product master: [`/settings/product/index`](./settings_product_index)
- Producers: `/settings/producer/index`
