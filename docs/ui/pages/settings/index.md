---
title: "Settings — UI pages"
sidebar_position: 1
---

# Settings — UI pages

The **Settings** module is the central configuration surface of sd-main. It hosts the global params editor, every reference directory (cities, regions, brands, units, currencies, product master), the price-type and price configuration screens, user management, and the backup / export hub. The full controller list lives at `protected/modules/settings/controllers/`; the table below lists the highest-impact UI entry points.

| URL | Page | Controller |
|---|---|---|
| `/settings/settings/index` | [Settings home](./settings_settings_index) | `SettingsController::index` |
| `/settings/params/index` | [Global params](./settings_params_index) | `ParamsController::index` |
| `/settings/priceType/index` | [Price types](./settings_priceType_index) | `PriceTypeController::index` |
| `/settings/prices/index` | [Prices home](./settings_prices_index) | `PricesController::index` |
| `/settings/prices/priceList` | [Price list](./settings_prices_priceList) | `PricesController::priceList` |
| `/settings/prices/importExcel` | [Import prices (Excel)](./settings_prices_importExcel) | `PricesController::importExcel` |
| `/settings/currency/index` | [Currencies](./settings_currency_index) | `CurrencyController::index` |
| `/settings/product/index` | [Product master](./settings_product_index) | `ProductController::index` |
| `/settings/brand/index` | [Brands](./settings_brand_index) | `BrandController::index` |
| `/settings/city/index` | [Cities](./settings_city_index) | `CityController::index` |
| `/settings/region/index` | [Regions](./settings_region_index) | `RegionController::index` |
| `/settings/unit/index` | [Units](./settings_unit_index) | `UnitController::index` |
| `/settings/user/index` | [Users](./settings_user_index) | `UserController::index` |
| `/settings/backup/index` | [Backup / export](./settings_backup_index) | `BackupController::index` |

Smaller directory controllers (`channel`, `clientCategory`, `clientClass`, `clientFirm`, `clientType`, `closed`, `diler`, `inventoryGroup`, `inventoryType`, `knowledgeCategory`, `knowledgePost`, `loyalty`, `orderComment`, `photoReportCategory`, `producer`, `productCaseType`, `productCategory`, `productGroup`, `reject`, `rejectDefect`, `rlpBonus`, `royalty`, `segment`, `skidka`, `skidkaManual`, `smartUp`, `smartup5x`, `systemLog`, `tag`, `tara`, `taskType`, `telegramReport`, `tgBot`, `tgBot2`, `tgBot3`, `tradeDirection`, `view`, `workingDays`, `applications`, `bonus`, `integration`, `license`, `printer`, `subProductCategory`, `permission`, `api`) all follow the same admin-grid pattern: `actionIndex` renders an `admingrid_diler` view; `actionGetData` returns JSON for the grid; `actionCreateAjax` / `actionUpdateAjax` / `actionDeleteAjax` mutate. They share the conventions documented here — start with `priceType` or `brand` as the canonical template.

## See also

- Module reference: [/modules/settings](/docs/modules/settings)
- Settings catalog: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Routes inventory: [`static/data/routes.json`](/data/routes.json)
