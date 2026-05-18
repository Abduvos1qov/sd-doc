---
title: "Import prices (Excel)"
audience: All sd-main developers, QA
summary: Live admin page at /settings/prices/importExcel
topics: [settings, price, import, page, ui]
---

# Import prices (Excel)

**URL**: `/settings/prices/importExcel` · **Module**: `settings` · **Controller**: `PricesController::importExcel` · **RBAC**: `operation.settings.prices` · **Role harvested**: `admin`

:::note Screenshot pending — harvester re-run needed:::

## Purpose

Bulk-upload prices from an Excel sheet. Pick a price type and an effective date, upload the file (column A = product code, column B = price), preview the diff, and commit. Mismatched product codes are highlighted and skipped on commit. Unlike the `priceList` cell editor, this endpoint accepts large books in a single transaction and is the canonical path for monthly price updates from suppliers.

## Fields

| Label | Name | Type | Required |
|---|---|---|---|
| Price type | `priceTypeId` | select | yes |
| Effective date | `dateStart` | date | yes |
| File | `file` | xlsx upload | yes |
| Treat empty cell as | `emptyMode` | select (skip / zero) | no |

## Actions

- Upload & preview
- Confirm & commit
- Cancel & reupload

## Backend route

- **Controller file**: `protected/modules/settings/controllers/PricesController.php` (line 196)
- **Action kind**: inline (`$this->render('import-prices')`)
- **View rendered**: `views/prices/import-prices.php`
- **Required permission**: `operation.settings.prices`

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Price-list page: [`/settings/prices/priceList`](./settings_prices_priceList)
- Prices home: [`/settings/prices/index`](./settings_prices_index)
