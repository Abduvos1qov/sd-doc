---
title: "Главная цен"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/prices/index
topics: [settings, price, page, ui]
---

# Главная цен

**URL**: `/settings/prices/index` · **Модуль**: `settings` · **Контроллер**: `PricesController::index` · **RBAC**: `operation.settings.prices` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Лендинг для управления прайс-листами. Позволяет выбрать тип цены, дату начала действия и область (территория / бренд / категория), прежде чем перейти в редактируемый прайс-лист. Сам экран только рендерит шелл `views/prices/index.php`; тяжёлая логика таблицы — в [Прайс-листе](./settings_prices_priceList).

## Действия

- Выбрать тип цены (типы загружаются из `PriceTypeController`)
- Выбрать дату начала (по умолчанию — сегодня)
- Выбрать фильтры по области
- Открыть прайс-лист
- Открыть диалог импорта из Excel

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/PricesController.php` (строка 7)
- **Тип действия**: inline (`$this->render('index')`)
- **Рендерится вьюха**: `views/prices/index.php`
- **Требуется доступ**: `operation.settings.prices`
- **Соседние write-эндпоинты**: `save`, `multiSave`, `saveWithout`, `config`, `markup`, `stock`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Прайс-лист: [`/settings/prices/priceList`](./settings_prices_priceList)
- Импорт: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Типы цен: [`/settings/priceType/index`](./settings_priceType_index)
