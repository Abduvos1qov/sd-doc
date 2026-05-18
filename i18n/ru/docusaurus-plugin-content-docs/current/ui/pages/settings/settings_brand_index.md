---
title: "Бренды"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/brand/index
topics: [settings, product, page, ui]
---

# Бренды

**URL**: `/settings/brand/index` · **Модуль**: `settings` · **Контроллер**: `BrandController::index` · **RBAC**: `operation.settings.brand` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Простая CRUD-таблица брендов. Каждая строка `Product` указывает на один `Brand`. Бренды также используются в нескольких отчётах и как фильтр на доске заявок, KPI-экранах и прайс-листе, поэтому удалить бренд, на который ссылаются товары, контроллер не даст.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Название |
| 3 | Производитель |
| 4 | Порядок |
| 5 | Активен |
| 6 | Обновлено |

## Действия

- Добавить бренд
- Редактировать бренд (`update`)
- Сохранить (`save`)
- Переключить активность

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/BrandController.php` (строка 35)
- **Тип действия**: inline (`$this->render('admingrid_diler')`)
- **Рендерится вьюха**: `views/brand/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.brand`
- **Соседние эндпоинты**: `getData`, `save`, `update`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Мастер товаров: [`/settings/product/index`](./settings_product_index)
- Производители: `/settings/producer/index`
