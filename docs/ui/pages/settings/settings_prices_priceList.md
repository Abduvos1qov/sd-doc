---
title: "Price list"
audience: All sd-main developers, QA
summary: Live admin page at /settings/prices/priceList
topics: [settings, price, page, ui]
---

# Price list

**URL**: `/settings/prices/priceList` · **Module**: `settings` · **Controller**: `PricesController::priceList` · **RBAC**: `operation.settings.prices` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

The actual editable price list. Renders one row per product and one column per `priceType`; each cell is editable inline. On save, prices are POSTed through `actionSave` (single row), `actionMultiSave` (bulk) or `actionSaveWithout` (specific products excluded). The grid supports markup propagation (apply a percentage to the chosen base column) and a stock overlay to highlight rows with positive stock.

## Grid columns

| # | Column |
|---|---|
| 1 | Product code |
| 2 | Product name |
| 3 | Category |
| 4 | Brand |
| 5 | Unit |
| 6 | Stock (when overlay is on) |
| 7+ | One column per active price type |

## Actions

- Inline-edit cell
- Bulk-edit selection
- Apply markup (`actionMarkup`)
- Toggle stock overlay (`actionStock`)
- Filter by category / brand / search
- Export to Excel
- Open Excel import

## Backend route

- **Controller file**: `protected/modules/settings/controllers/PricesController.php` (line 191)
- **Action kind**: inline (`$this->render('priceList')`)
- **View rendered**: `views/prices/priceList.php`
- **Required permission**: `operation.settings.prices`
- **Save endpoints**: `save`, `multiSave`, `saveWithout`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Prices home: [`/settings/prices/index`](./settings_prices_index)
- Excel import: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Price types: [`/settings/priceType/index`](./settings_priceType_index)
