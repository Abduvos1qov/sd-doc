---
title: "Типы цен"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/priceType/index
topics: [settings, price, page, ui]
---

# Типы цен

**URL**: `/settings/priceType/index` · **Модуль**: `settings` · **Контроллер**: `PriceTypeController::index` · **RBAC**: `operation.settings.priceType` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

CRUD-таблица типов цен. *Тип цены* — это канальная размерность прайсинга (розница / опт / партнёр / промо и т. д.); каждая строка `Price` ключуется тройкой `(productId, priceTypeId, dateStart)`, так что новый тип сразу даёт новую колонку во всех представлениях прайс-листа.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Название (i18n) |
| 3 | Короткий код |
| 4 | Порядок |
| 5 | Флаг «по умолчанию» |
| 6 | Активен |
| 7 | Обновлено |

## Действия

- Добавить тип цены (модал — `createAjax`)
- Редактировать тип цены (модал — `updateAjax`)
- Переключить активность
- Переставлять (drag-ручка)

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/PriceTypeController.php` (строка 47)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/priceType/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.priceType`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `createAjax`, `updateAjax`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Цены: [`/settings/prices/index`](./settings_prices_index)
- Прайс-лист: [`/settings/prices/priceList`](./settings_prices_priceList)
