---
title: "Импорт цен (Excel)"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/prices/importExcel
topics: [settings, price, import, page, ui]
---

# Импорт цен (Excel)

**URL**: `/settings/prices/importExcel` · **Модуль**: `settings` · **Контроллер**: `PricesController::importExcel` · **RBAC**: `operation.settings.prices` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Массовая загрузка цен из Excel-листа. Выберите тип цены и дату начала, загрузите файл (колонка A — код товара, колонка B — цена), посмотрите diff, подтвердите. Несовпавшие коды подсвечиваются и пропускаются при коммите. В отличие от редактора ячеек в `priceList`, этот эндпоинт принимает большие книги одной транзакцией и используется как штатный путь для ежемесячных обновлений от поставщиков.

## Поля

| Метка | Имя | Тип | Обязательно |
|---|---|---|---|
| Тип цены | `priceTypeId` | селект | да |
| Дата начала | `dateStart` | дата | да |
| Файл | `file` | загрузка xlsx | да |
| Считать пустую ячейку | `emptyMode` | селект (skip / zero) | нет |

## Действия

- Загрузить и посмотреть превью
- Подтвердить и закоммитить
- Отменить и перезагрузить

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/PricesController.php` (строка 196)
- **Тип действия**: inline (`$this->render('import-prices')`)
- **Рендерится вьюха**: `views/prices/import-prices.php`
- **Требуется доступ**: `operation.settings.prices`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Прайс-лист: [`/settings/prices/priceList`](./settings_prices_priceList)
- Главная цен: [`/settings/prices/index`](./settings_prices_index)
