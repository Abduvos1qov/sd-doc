---
title: "Settings — страницы интерфейса"
sidebar_position: 1
---

# Settings — страницы интерфейса

Модуль **Settings** — центральная конфигурационная поверхность sd-main. Здесь живут редактор глобальных параметров, все справочники (города, регионы, бренды, единицы, валюты, мастер товаров), экраны типов и значений цен, управление пользователями и узел резервного копирования / экспорта. Полный список контроллеров — в `protected/modules/settings/controllers/`; в таблице ниже — самые значимые точки входа интерфейса.

| URL | Страница | Контроллер |
|---|---|---|
| `/settings/settings/index` | [Главная настроек](./settings_settings_index) | `SettingsController::index` |
| `/settings/params/index` | [Глобальные параметры](./settings_params_index) | `ParamsController::index` |
| `/settings/priceType/index` | [Типы цен](./settings_priceType_index) | `PriceTypeController::index` |
| `/settings/prices/index` | [Главная цен](./settings_prices_index) | `PricesController::index` |
| `/settings/prices/priceList` | [Прайс-лист](./settings_prices_priceList) | `PricesController::priceList` |
| `/settings/prices/importExcel` | [Импорт цен (Excel)](./settings_prices_importExcel) | `PricesController::importExcel` |
| `/settings/currency/index` | [Валюты](./settings_currency_index) | `CurrencyController::index` |
| `/settings/product/index` | [Мастер товаров](./settings_product_index) | `ProductController::index` |
| `/settings/brand/index` | [Бренды](./settings_brand_index) | `BrandController::index` |
| `/settings/city/index` | [Города](./settings_city_index) | `CityController::index` |
| `/settings/region/index` | [Регионы](./settings_region_index) | `RegionController::index` |
| `/settings/unit/index` | [Единицы измерения](./settings_unit_index) | `UnitController::index` |
| `/settings/user/index` | [Пользователи](./settings_user_index) | `UserController::index` |
| `/settings/backup/index` | [Бэкап / экспорт](./settings_backup_index) | `BackupController::index` |

Остальные справочные контроллеры (`channel`, `clientCategory`, `clientClass`, `clientFirm`, `clientType`, `closed`, `diler`, `inventoryGroup`, `inventoryType`, `knowledgeCategory`, `knowledgePost`, `loyalty`, `orderComment`, `photoReportCategory`, `producer`, `productCaseType`, `productCategory`, `productGroup`, `reject`, `rejectDefect`, `rlpBonus`, `royalty`, `segment`, `skidka`, `skidkaManual`, `smartUp`, `smartup5x`, `systemLog`, `tag`, `tara`, `taskType`, `telegramReport`, `tgBot`, `tgBot2`, `tgBot3`, `tradeDirection`, `view`, `workingDays`, `applications`, `bonus`, `integration`, `license`, `printer`, `subProductCategory`, `permission`, `api`) идут по одинаковому шаблону admin-grid: `actionIndex` рендерит `admingrid_diler`, `actionGetData` отдаёт JSON, `actionCreateAjax` / `actionUpdateAjax` / `actionDeleteAjax` пишут. Для шаблона смотрите страницы `priceType` или `brand`.

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Каталог настроек: [/quality/settings-catalog](/docs/quality/settings-catalog)
- Реестр маршрутов: [`static/data/routes.json`](/data/routes.json)
