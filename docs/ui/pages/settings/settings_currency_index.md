---
title: "Currencies"
audience: All sd-main developers, QA
summary: Live admin page at /settings/currency/index
topics: [settings, currency, page, ui]
---

# Currencies

**URL**: `/settings/currency/index` · **Module**: `settings` · **Controller**: `CurrencyController::index` · **RBAC**: `operation.settings.currency` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

CRUD grid for currencies and their daily rates. Used by finans and orders to convert between the base currency (typically `UZS`) and quote currencies (`USD`, `RUB`). The rate is loaded automatically from the Central Bank of Uzbekistan feed when the integration is enabled; manual edits override the feed.

## Grid columns

| # | Column |
|---|---|
| 1 | ISO code |
| 2 | Name |
| 3 | Symbol |
| 4 | Rate to base |
| 5 | Effective date |
| 6 | Source (feed / manual) |
| 7 | Active |

## Actions

- Add currency
- Edit currency
- Edit rate for date (modal — `updateAjax`)
- Toggle active
- Refresh from feed

## Backend route

- **Controller file**: `protected/modules/settings/controllers/CurrencyController.php` (line 41)
- **Action kind**: inline (`$this->render('admingrid_diler', …)`)
- **View rendered**: `views/currency/admingrid_diler.php`
- **Required permission**: `operation.settings.currency`
- **Sibling endpoints**: `getData`, `getUpdatedRow`, `updateAjax`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Multi-currency rounding: [/concepts/multi-currency-rounding](/docs/concepts/multi-currency-rounding)
