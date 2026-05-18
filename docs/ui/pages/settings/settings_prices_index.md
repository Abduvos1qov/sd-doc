---
title: "Prices home"
audience: All sd-main developers, QA
summary: Live admin page at /settings/prices/index
topics: [settings, price, page, ui]
---

# Prices home

**URL**: `/settings/prices/index` · **Module**: `settings` · **Controller**: `PricesController::index` · **RBAC**: `operation.settings.prices` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Landing page for price-list management. Lets the user pick a price type, an effective date and a scope (territory / brand / category) before navigating into the editable price list. The page itself just renders the `views/prices/index.php` shell; the heavy grid logic lives behind the [Price list](./settings_prices_priceList) page.

## Actions

- Pick price type (loads available types from `PriceTypeController`)
- Pick effective date (defaults to today)
- Pick scope filters
- Open price list
- Open Excel import dialog

## Backend route

- **Controller file**: `protected/modules/settings/controllers/PricesController.php` (line 7)
- **Action kind**: inline (`$this->render('index')`)
- **View rendered**: `views/prices/index.php`
- **Required permission**: `operation.settings.prices`
- **Sibling write endpoints**: `save`, `multiSave`, `saveWithout`, `config`, `markup`, `stock`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Price-list page: [`/settings/prices/priceList`](./settings_prices_priceList)
- Import: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Price types: [`/settings/priceType/index`](./settings_priceType_index)
