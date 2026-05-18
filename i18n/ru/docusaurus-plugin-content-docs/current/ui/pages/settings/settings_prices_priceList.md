---
title: "Прайс-лист"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/prices/priceList
topics: [settings, price, page, ui]
---

# Прайс-лист

**URL**: `/settings/prices/priceList` · **Модуль**: `settings` · **Контроллер**: `PricesController::priceList` · **RBAC**: `operation.settings.prices` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Собственно редактируемый прайс-лист. Рендерит по строке на товар и по колонке на каждый `priceType`; каждая ячейка редактируется inline. При сохранении цены POST'ятся через `actionSave` (одна строка), `actionMultiSave` (массово) или `actionSaveWithout` (с исключением товаров). Таблица поддерживает распространение наценки (наложить процент на выбранную базовую колонку) и наложение стока, чтобы подсветить строки с положительным остатком.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | Код товара |
| 2 | Название товара |
| 3 | Категория |
| 4 | Бренд |
| 5 | Единица |
| 6 | Остаток (когда наложение включено) |
| 7+ | По колонке на каждый активный тип цены |

## Действия

- Редактировать ячейку inline
- Массовое редактирование выделения
- Применить наценку (`actionMarkup`)
- Включить/выключить наложение стока (`actionStock`)
- Фильтр по категории / бренду / поиску
- Экспорт в Excel
- Открыть импорт Excel

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/PricesController.php` (строка 191)
- **Тип действия**: inline (`$this->render('priceList')`)
- **Рендерится вьюха**: `views/prices/priceList.php`
- **Требуется доступ**: `operation.settings.prices`
- **Save-эндпоинты**: `save`, `multiSave`, `saveWithout`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Главная цен: [`/settings/prices/index`](./settings_prices_index)
- Импорт Excel: [`/settings/prices/importExcel`](./settings_prices_importExcel)
- Типы цен: [`/settings/priceType/index`](./settings_priceType_index)
