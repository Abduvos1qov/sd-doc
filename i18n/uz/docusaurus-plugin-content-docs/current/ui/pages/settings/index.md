---
title: "Settings — interfeys sahifalari"
sidebar_position: 1
---

# Settings — interfeys sahifalari

**Settings** moduli — sd-main ning markaziy konfiguratsiya sirtidir. Bu yerda global parametrlar muharriri, barcha maʼlumotnoma katalog'lari (shaharlar, mintaqalar, brendlar, birliklar, valyutalar, tovar masteri), narx turi va narx konfiguratsiya ekranlari, foydalanuvchi boshqaruvi va zaxira / eksport markazi joylashgan. Kontroller'larning toʻliq roʻyxati `protected/modules/settings/controllers/` da; quyidagi jadvalda eng muhim interfeys kirish nuqtalari keltirilgan.

| URL | Sahifa | Kontroller |
|---|---|---|
| `/settings/settings/index` | [Sozlamalar bosh sahifasi](./settings_settings_index) | `SettingsController::index` |
| `/settings/params/index` | [Global parametrlar](./settings_params_index) | `ParamsController::index` |
| `/settings/priceType/index` | [Narx turlari](./settings_priceType_index) | `PriceTypeController::index` |
| `/settings/prices/index` | [Narxlar bosh sahifasi](./settings_prices_index) | `PricesController::index` |
| `/settings/prices/priceList` | [Narxlar roʻyxati](./settings_prices_priceList) | `PricesController::priceList` |
| `/settings/prices/importExcel` | [Narxlarni import qilish (Excel)](./settings_prices_importExcel) | `PricesController::importExcel` |
| `/settings/currency/index` | [Valyutalar](./settings_currency_index) | `CurrencyController::index` |
| `/settings/product/index` | [Tovar masteri](./settings_product_index) | `ProductController::index` |
| `/settings/brand/index` | [Brendlar](./settings_brand_index) | `BrandController::index` |
| `/settings/city/index` | [Shaharlar](./settings_city_index) | `CityController::index` |
| `/settings/region/index` | [Mintaqalar](./settings_region_index) | `RegionController::index` |
| `/settings/unit/index` | [Oʻlchov birliklari](./settings_unit_index) | `UnitController::index` |
| `/settings/user/index` | [Foydalanuvchilar](./settings_user_index) | `UserController::index` |
| `/settings/backup/index` | [Zaxira / eksport](./settings_backup_index) | `BackupController::index` |

Boshqa maʼlumotnoma kontroller'lari (`channel`, `clientCategory`, `clientClass`, `clientFirm`, `clientType`, `closed`, `diler`, `inventoryGroup`, `inventoryType`, `knowledgeCategory`, `knowledgePost`, `loyalty`, `orderComment`, `photoReportCategory`, `producer`, `productCaseType`, `productCategory`, `productGroup`, `reject`, `rejectDefect`, `rlpBonus`, `royalty`, `segment`, `skidka`, `skidkaManual`, `smartUp`, `smartup5x`, `systemLog`, `tag`, `tara`, `taskType`, `telegramReport`, `tgBot`, `tgBot2`, `tgBot3`, `tradeDirection`, `view`, `workingDays`, `applications`, `bonus`, `integration`, `license`, `printer`, `subProductCategory`, `permission`, `api`) bir xil admin-grid namunasi boʻyicha ishlaydi: `actionIndex` `admingrid_diler` view'ini render qiladi, `actionGetData` JSON qaytaradi, `actionCreateAjax` / `actionUpdateAjax` / `actionDeleteAjax` esa oʻzgartiradi. Namuna sifatida `priceType` yoki `brand` sahifalariga qarang.

## Shuningdek qarang

- Modul maʼlumotnomasi: [/modules/settings](/docs/modules/settings)
- Sozlamalar katalog'i: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Marshrutlar reestri: [`static/data/routes.json`](/data/routes.json)
