---
title: "Price types"
audience: All sd-main developers, QA
summary: Live admin page at /settings/priceType/index
topics: [settings, price, page, ui]
---

# Price types

**URL**: `/settings/priceType/index` · **Module**: `settings` · **Controller**: `PriceTypeController::index` · **RBAC**: `operation.settings.priceType` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

CRUD grid for price types. A *price type* is the channel-level dimension of pricing (retail / wholesale / partner / promo / etc.); each `Price` row is keyed by `(productId, priceTypeId, dateStart)` so adding a new type instantly creates a new column in every price-list view.

## Grid columns

| # | Column |
|---|---|
| 1 | ID |
| 2 | Name (i18n) |
| 3 | Short code |
| 4 | Sort order |
| 5 | Default flag |
| 6 | Active |
| 7 | Updated at |

## Actions

- Add price type (modal — `createAjax`)
- Edit price type (modal — `updateAjax`)
- Toggle active
- Reorder (drag handle)

## Backend route

- **Controller file**: `protected/modules/settings/controllers/PriceTypeController.php` (line 47)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/priceType/admingrid_diler.php`
- **Required permission**: `operation.settings.priceType`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Prices: [`/settings/prices/index`](./settings_prices_index)
- Price-list page: [`/settings/prices/priceList`](./settings_prices_priceList)
