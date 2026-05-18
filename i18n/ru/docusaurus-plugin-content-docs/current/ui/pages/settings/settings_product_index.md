---
title: "Мастер товаров"
audience: Разработчики sd-main, QA
summary: Живая страница админки /settings/product/index
topics: [settings, product, page, ui]
---

# Мастер товаров

**URL**: `/settings/product/index` · **Модуль**: `settings` · **Контроллер**: `ProductController::index` · **RBAC**: `operation.settings.product` · **Снятая роль**: `admin`

:::note Скриншот в процессе — нужен повторный запуск харвестера:::

## Назначение

Главная таблица мастер-данных по товарам. Здесь зарегистрирован каждый SKU тенанта: код, название, категория, бренд, базовая единица, упаковка, налоговые флаги, фото, штрих-код, локальный код, флаг маркировки (CRPT). Сопутствующие экраны покрывают массовый импорт, сортировку, деактивацию, группы товаров, привязку локальных кодов и апдейты.

## Колонки таблицы

| № | Колонка |
|---|---|
| 1 | ID |
| 2 | Код |
| 3 | Название |
| 4 | Категория |
| 5 | Подкатегория |
| 6 | Бренд |
| 7 | Производитель |
| 8 | Базовая единица |
| 9 | Размер упаковки |
| 10 | Штрих-код |
| 11 | Локальный код |
| 12 | Маркировка |
| 13 | Активен |
| 14 | Создан |

## Действия

- Добавить товар (модал — `createAjax`)
- Редактировать товар (модал — `updateAjax`)
- Удалить товар (`deleteProduct`, `checkDelete`)
- Массовое добавление (`addProducts`)
- Импорт из Excel (`import_xls`)
- Импорт локальных кодов (`import_local_code`)
- Импорт апдейтов (`import_update`)
- Сортировка (`sort_product`)
- Деактивация выделения (`deactivate`)
- Группы товаров (`product_group`)
- Проверка дубликатов (`check`)

## Бэкенд-маршрут

- **Файл контроллера**: `protected/modules/settings/controllers/ProductController.php` (строка 65)
- **Тип действия**: inline (`$this->render('admingrid_diler', …)`)
- **Рендерится вьюха**: `views/product/admingrid_diler.php`
- **Требуется доступ**: `operation.settings.product`
- **Соседние эндпоинты**: `getData`, `getUpdatedRow`, `getExtras`, `createAjax`, `updateAjax`, `deleteProduct`, `addProducts`

## См. также

- Справочник модуля: [/modules/settings](/docs/modules/settings)
- Бренды: [`/settings/brand/index`](./settings_brand_index)
- Единицы: [`/settings/unit/index`](./settings_unit_index)
- Управление партиями: [/concepts/lot-management](/docs/concepts/lot-management)
